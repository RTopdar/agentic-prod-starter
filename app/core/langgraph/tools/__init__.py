from langchain_core.tools.base import BaseTool
from app.core.langgraph.duckduckgosearch import duckduckgo_search_tool

# Central registry of tools available to the agent
tools: list[BaseTool] = [duckduckgo_search_tool]
