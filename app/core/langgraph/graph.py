import asyncio
from typing import Optional
from urllib.parse import quote_plus

from langchain_core.messages import ToolMessage, convert_to_openai_messages
from langfuse.langchain import CallbackHandler
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.graph import END, StateGraph
from langgraph.graph.state import Command, CompiledStateGraph
from langgraph.types import RunnableConfig

from mem0 import AsyncMemory

from psycopg_pool import AsyncConnectionPool
from app.core.config import settings
from app.core.langfuse import get_langfuse_client
from app.core.langgraph.tools import tools
from app.core.logging import logger
from app.core.prompts import load_system_prompt
from app.schemas import GraphState, Message
from app.services.llm import llm_service
from app.utils import dump_messages, prepare_messages, process_llm_response


class LangGraphAgent:
    """
    Manages the LangGraph Workflow, LLM interactions, and Memory persistence.
    """

    def __init__(self):
        # Bind tools to the LLM service so the model knows what functions it can call
        self.llm_service = llm_service.bind_tools(tools)
        self.tools_by_name = {tool.name: tool for tool in tools}

        self._connection_pool: Optional[AsyncConnectionPool] = None
        self._graph: Optional[CompiledStateGraph] = None
        self.memory: Optional[AsyncMemory] = None
        logger.info("langgraph_agent_initialized", model=settings.openrouter_model)

    async def _long_term_memory(self) -> AsyncMemory:
        """
        Lazy-load the mem0ai memory client with pgvector configuration.
        """
        if self.memory is None:
            self.memory = await AsyncMemory.from_config(
                config_dict={
                    "vector_store": {
                        "provider": "pgvector",
                        "config": {
                            "collection_name": "agent_memory",
                            "dbname": settings.postgres_db,
                            "user": settings.postgres_user,
                            "password": settings.postgres_password,
                            "host": settings.postgres_host,
                            "port": settings.postgres_port,
                        },
                    },
                    "llm": {
                        "provider": "openai",
                        "config": {
                            "model": settings.openrouter_model,
                            "openai_base_url": settings.openrouter_base_url,
                        },
                    },
                    "embedder": {
                        "provider": "openai",
                        "config": {
                            "model": settings.openrouter_embedding_model,
                            "openai_base_url": settings.openrouter_base_url,
                        },
                    },
                }
            )
        return self.memory

    async def _get_connection_pool(self) -> AsyncConnectionPool:
        """
        Establish a connection pool specifically for LangGraph checkpointers.
        """
        if self._connection_pool is None:
            connection_url = (
                "postgresql://"
                f"{quote_plus(settings.postgres_user)}:{quote_plus(settings.postgres_password)}"
                f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
            )
            self._connection_pool = AsyncConnectionPool(
                connection_url,
                open=False,
                max_size=settings.postgres_pool_size,
                kwargs={"autocommit": True},
            )
            await self._connection_pool.open()
        return self._connection_pool

    # ==================================================
    # Node Logic
    # ==================================================
    async def _chat(self, state: GraphState, config: RunnableConfig) -> Command:
        """
        The main Chat Node.
        1. Loads system prompt with memory context.
        2. Prepares messages (trimming if needed).
        3. Calls LLM Service.
        """
        # Load system prompt with the Long-Term Memory retrieved from previous steps
        SYSTEM_PROMPT = load_system_prompt(long_term_memory=state.long_term_memory)

        # Prepare context window (trimming)
        current_llm = self.llm_service.get_llm()
        messages = prepare_messages(state.messages, current_llm, SYSTEM_PROMPT)
        try:
            # Invoke LLM (with retries handled by service)
            response_message = await self.llm_service.call(dump_messages(messages))
            response_message = process_llm_response(response_message)
            # Determine routing: If LLM wants to use a tool, go to 'tool_call', else END.
            if response_message.tool_calls:
                goto = "tool_call"
            else:
                goto = END
            # Return command to update state and route
            return Command(update={"messages": [response_message]}, goto=goto)

        except Exception as e:
            logger.error("llm_call_node_failed", error=str(e))
            raise

    async def _tool_call(self, state: GraphState) -> Command:
        """
        The Tool Execution Node.
        Executes requested tools and returns results back to the chat node.
        """
        langfuse = get_langfuse_client()
        outputs = []
        for tool_call in state.messages[-1].tool_calls:
            with langfuse.start_as_current_observation(
                name=f"tool_call:{tool_call['name']}", as_type="span"
            ) as span:
                span.set_input({"args": tool_call["args"]})
                tool_result = await self.tools_by_name[tool_call["name"]].ainvoke(
                    tool_call["args"]
                )
                span.set_output({"result": str(tool_result)[:500]})

                outputs.append(
                    ToolMessage(
                        content=str(tool_result),
                        name=tool_call["name"],
                        tool_call_id=tool_call["id"],
                    )
                )

        return Command(update={"messages": outputs}, goto="chat")

    # ==================================================
    # Graph Compilation
    # ==================================================
    async def create_graph(self) -> CompiledStateGraph:
        """
        Builds the state graph and attaches the Postgres checkpointer.
        """
        if self._graph is not None:
            return self._graph
        graph_builder = StateGraph(GraphState)

        # Add Nodes
        graph_builder.add_node("chat", self._chat)
        graph_builder.add_node("tool_call", self._tool_call)

        # Define Flow
        graph_builder.set_entry_point("chat")

        # Setup Persistence
        connection_pool = await self._get_connection_pool()
        checkpointer = AsyncPostgresSaver(connection_pool)
        await checkpointer.setup()  # Ensure tables exist
        self._graph = graph_builder.compile(checkpointer=checkpointer)
        return self._graph

    # ==================================================
    # Public Methods
    # ==================================================
    async def get_response(
        self, messages: list[Message], session_id: str, user_id: str
    ) -> list[dict]:
        """
        Primary entry point for the API.
        Handles memory retrieval + graph execution + memory update.
        """
        if self._graph is None:
            await self.create_graph()

        langfuse = get_langfuse_client()

        # 1. Retrieve relevant facts from Long-Term Memory (Vector Search)
        with langfuse.start_as_current_observation(
            name="memory_search", as_type="span"
        ) as span:
            span.set_input({"user_id": user_id, "query": messages[-1].content})
            memory_client = await self._long_term_memory()
            relevant_memory = await memory_client.search(
                user_id=user_id, query=messages[-1].content
            )
            memory_context = "\n".join(
                [f"* {res['memory']}" for res in relevant_memory.get("results", [])]
            )
            span.set_output(
                {
                    "result_count": len(relevant_memory.get("results", [])),
                    "context_length": len(memory_context),
                }
            )

        # 2. Run the Graph
        config = {
            "configurable": {"thread_id": session_id},
            "callbacks": [CallbackHandler()],  # Langfuse Tracing
        }

        input_state = {
            "messages": dump_messages(messages),
            "long_term_memory": memory_context or "No relevant memory found.",
        }

        final_state = await self._graph.ainvoke(input_state, config=config)
        # 3. Update Memory in Background (Fire and Forget)
        # We don't want the user to wait for us to save new memories.
        asyncio.create_task(
            self._update_long_term_memory(user_id, session_id, final_state["messages"])
        )
        return self._process_messages(final_state["messages"])

    async def _update_long_term_memory(
        self, user_id: str, session_id: str, messages: list
    ) -> None:
        """Extracts and saves new facts from the conversation to pgvector."""
        try:
            langfuse = get_langfuse_client()
            trace = langfuse.trace(
                name="memory_add",
                session_id=session_id,
                user_id=user_id,
                input={"message_count": len(messages)},
            )
            memory_client = await self._long_term_memory()
            # mem0ai automatically extracts facts using an LLM
            await memory_client.add(messages, user_id=user_id)
            trace.update(output={"status": "success"})
        except Exception as e:
            logger.error("memory_update_failed", error=str(e))

    def _process_messages(self, messages: list) -> list[Message]:
        """Convert internal LangChain messages back to Pydantic schemas."""
        openai_msgs = convert_to_openai_messages(messages)
        return [
            Message(role=m["role"], content=str(m["content"]))
            for m in openai_msgs
            if m["role"] in ["assistant", "user"] and m["content"]
        ]
