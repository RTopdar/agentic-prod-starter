# Graph Report - .  (2026-06-14)

## Corpus Check
- 53 files · ~24,969 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 605 nodes · 891 edges · 51 communities (39 shown, 12 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 96 edges (avg confidence: 0.61)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Auth & Database Layer|Auth & Database Layer]]
- [[_COMMUNITY_LangGraph Agent Infrastructure|LangGraph Agent Infrastructure]]
- [[_COMMUNITY_README Architecture Concepts|README Architecture Concepts]]
- [[_COMMUNITY_Coding Principles (skills.md)|Coding Principles (skills.md)]]
- [[_COMMUNITY_JWT Auth Utilities|JWT Auth Utilities]]
- [[_COMMUNITY_GitHub Copilot Instructions|GitHub Copilot Instructions]]
- [[_COMMUNITY_Graphify Skill Pipeline|Graphify Skill Pipeline]]
- [[_COMMUNITY_Graphify Concepts & Pipeline|Graphify Concepts & Pipeline]]
- [[_COMMUNITY_Config & Settings|Config & Settings]]
- [[_COMMUNITY_Logging Demo|Logging Demo]]
- [[_COMMUNITY_Logging Processors|Logging Processors]]
- [[_COMMUNITY_LLM Service|LLM Service]]
- [[_COMMUNITY_AGENTS.md Guidelines|AGENTS.md Guidelines]]
- [[_COMMUNITY_Middleware Layer|Middleware Layer]]
- [[_COMMUNITY_Chat Routes|Chat Routes]]
- [[_COMMUNITY_Main App & Langfuse|Main App & Langfuse]]
- [[_COMMUNITY_Chart Schemas|Chart Schemas]]
- [[_COMMUNITY_System Prompt|System Prompt]]
- [[_COMMUNITY_Config Tests|Config Tests]]
- [[_COMMUNITY_Startup Script|Startup Script]]
- [[_COMMUNITY_Graphify References Query|Graphify References: Query]]
- [[_COMMUNITY_Graphify References Exports|Graphify References: Exports]]
- [[_COMMUNITY_Graphify References AddWatch|Graphify References: Add/Watch]]
- [[_COMMUNITY_Graphify References Hooks|Graphify References: Hooks]]
- [[_COMMUNITY_Graphify References Query|Graphify References: Query]]
- [[_COMMUNITY_Graphify References Update|Graphify References: Update]]
- [[_COMMUNITY_CLI Entry|CLI Entry]]
- [[_COMMUNITY_OpenCode Plugin Config|OpenCode Plugin Config]]
- [[_COMMUNITY_OpenCode Dependencies|OpenCode Dependencies]]
- [[_COMMUNITY_Readme Security Concepts|Readme Security Concepts]]
- [[_COMMUNITY_Graphify References Transcribe|Graphify References: Transcribe]]
- [[_COMMUNITY_Graphify References GitHub Merge|Graphify References: GitHub Merge]]
- [[_COMMUNITY_Cross-Repo Merge|Cross-Repo Merge]]
- [[_COMMUNITY_Transcription Pipeline|Transcription Pipeline]]
- [[_COMMUNITY_Skill Discovery|Skill Discovery]]
- [[_COMMUNITY_OpenCode Graphify Plugin|OpenCode Graphify Plugin]]
- [[_COMMUNITY_Prompt Template|Prompt Template]]
- [[_COMMUNITY_Extraction Spec|Extraction Spec]]
- [[_COMMUNITY_Rate Limiter|Rate Limiter]]
- [[_COMMUNITY_DuckDuckGo Search|DuckDuckGo Search]]
- [[_COMMUNITY_Token Benchmark|Token Benchmark]]
- [[_COMMUNITY_Utils Init|Utils Init]]
- [[_COMMUNITY_Middleware & Metrics|Middleware & Metrics]]
- [[_COMMUNITY_Metrics Setup|Metrics Setup]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 49|Community 49]]

## God Nodes (most connected - your core abstractions)
1. `DatabaseService` - 29 edges
2. `Session` - 28 edges
3. `LangGraphAgent` - 24 edges
4. `Environment` - 19 edges
5. `Settings` - 18 edges
6. `User` - 18 edges
7. `BaseModel` - 17 edges
8. `MetricsMiddleware` - 15 edges
9. `LoggingContextMiddleware` - 15 edges
10. `agentic-prod-starter` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Langfuse Trace Hierarchy` --rationale_for--> `LangGraphAgent`  [EXTRACTED]
  README.md → app/core/langgraph/graph.py
- `Long-Term Memory with pgvector Pattern` --rationale_for--> `LangGraphAgent`  [EXTRACTED]
  README.md → app/core/langgraph/graph.py
- `Model Fallback Resilience Pattern` --rationale_for--> `LLMService`  [EXTRACTED]
  README.md → app/services/llm.py
- `Langfuse Trace Hierarchy` --rationale_for--> `Langfuse HTTP Trace Middleware`  [EXTRACTED]
  README.md → app/main.py
- `Native CLAUDE.md Graphify Integration` --conceptually_related_to--> `Graphify Instructions for Claude`  [INFERRED]
  .claude/skills/graphify/references/hooks.md → CLAUDE.md

## Import Cycles
- 1-file cycle: `app/main.py -> app/main.py`

## Hyperedges (group relationships)
- **Authentication and Authorization Flow** — v1_auth_register_user, v1_auth_login, v1_auth_create_session, v1_auth_get_user_sessions, v1_auth_get_current_user, v1_auth_get_current_session, schemas_auth_token, schemas_auth_usercreate, utils_auth_create_tokens, utils_auth_create_access_token, utils_auth_verify_token, services_database_databaseservice, utils_sanitization_sanitize_string, utils_sanitization_sanitize_email [EXTRACTED 1.00]
- **Chat Request-Response Pipeline** — v1_chat_chat, v1_chat_chat_stream, v1_chat_get_session_messages, v1_chat_clear_chat_history, v1_chat_agent, langgraph_graph_langgraphagent, services_llm_llmservice, services_llm_llmregistry, utils_graph_dump_messages, utils_graph_prepare_messages, utils_graph_process_llm_response, core_langgraph_tools [EXTRACTED 1.00]
- **Observability: Metrics + Logging + Tracing** — core_metrics_http_requests_total, core_metrics_http_request_duration_seconds, core_metrics_db_connections, core_metrics_llm_inference_duration_seconds, core_metrics_setup_metrics, core_middleware_metricsmiddleware, core_middleware_loggingcontextmiddleware, core_logging_logger, core_logging_bind_context, core_logging_clear_context, core_logging_log_request_response, main_langfuse_tracing_middleware, README_langfuse_trace_hierarchy [EXTRACTED 1.00]

## Communities (51 total, 12 thin omitted)

### Community 0 - "Auth & Database Layer"
Cohesion: 0.05
Nodes (57): Request, Session, User, User, ChatSession, HTTPAuthorizationCredentials, GET /health Endpoint, BaseModel (+49 more)

### Community 1 - "LangGraph Agent Infrastructure"
Cohesion: 0.05
Nodes (48): Langfuse Trace Hierarchy, Long-Term Memory with pgvector Pattern, Message, BaseChatModel, BaseMessage, Message, AsyncConnectionPool, AsyncMemory (+40 more)

### Community 2 - "README Architecture Concepts"
Cohesion: 0.05
Nodes (41): agentic-prod-starter, Architecture Stress Testing, Auth Endpoints, Automated Grading, Building Data Persistence Layer, Building The API Gateway, Circuit Breaking, Codebase Knowledge Graph (+33 more)

### Community 3 - "Coding Principles (skills.md)"
Cohesion: 0.10
Nodes (27): 1. Think Before Coding, 2. Simplicity First, 3. Surgical Changes, 4. Goal-Driven Execution, Anti-Patterns Summary, CLAUDE.md, Customization, Example 1: Drive-by Refactoring (+19 more)

### Community 4 - "JWT Auth Utilities"
Cohesion: 0.18
Nodes (22): Any, Schema for the JWT Access Token response., Token, Token, create_access_token(), create_refresh_token(), create_tokens(), _load_private_key() (+14 more)

### Community 5 - "GitHub Copilot Instructions"
Cohesion: 0.09
Nodes (22): API Design, Build, Test, and Lint Commands, Code Organization, Configuration Management, Copilot Instructions for Agentic Production System, Core Components, Database Operations, Development Server (+14 more)

### Community 6 - "Graphify Skill Pipeline"
Cohesion: 0.09
Nodes (22): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Interpreter guard for subcommands, Part A - Structural extraction for code files, Part B - Semantic extraction (parallel subagents) (+14 more)

### Community 7 - "Graphify Concepts & Pipeline"
Cohesion: 0.12
Nodes (22): Graphify Trigger (CLAUDE.md), Asymmetric JWT Authentication, FastAPI Application, Observability Stack, PostgreSQL with pgvector, Production Agentic System, Pydantic Settings Configuration, SlowAPI Rate Limiting (+14 more)

### Community 8 - "Config & Settings"
Cohesion: 0.10
Nodes (13): Any, BaseSettings, Generate PostgreSQL connection URL., Check if running in development environment., Check if running in production environment., Parse comma-separated string into list of origins., Parse debug flag from string to boolean., Parse integer fields from string. (+5 more)

### Community 9 - "Logging Demo"
Cohesion: 0.13
Nodes (18): BoundLogger, LogContext, Context manager for adding context to logs., Enter context and bind context variables., Create a log context with bound variables.      Example:         with logger.wit, with_context(), demonstrate_basic_logging(), demonstrate_context_logging() (+10 more)

### Community 10 - "Logging Processors"
Cohesion: 0.17
Nodes (19): Any, add_environment(), add_log_level(), add_process_id(), add_request_context(), add_service_name(), add_timestamp(), add_version() (+11 more)

### Community 11 - "LLM Service"
Cohesion: 0.15
Nodes (10): Model Fallback Resilience Pattern, BaseChatModel, BaseMessage, LLMRegistry, LLMService, Internal method that executes the actual API call., Public interface. Wraps the retry logic with a Fallback loop.         If the pri, Bind tools to the current LLM instance. (+2 more)

### Community 12 - "AGENTS.md Guidelines"
Cohesion: 0.13
Nodes (17): 1. Think Before Coding, 3. Surgical Changes, 4. Goal-Driven Execution, AGENTS.md — prod-agentic-practice, Architecture, Auth Routes — Key Details, Behavioral Guidelines, Goal-Driven Execution (+9 more)

### Community 13 - "Middleware Layer"
Cohesion: 0.18
Nodes (14): Request, BaseHTTPMiddleware, bind_context(), clear_context(), Bind key-value pairs to the current request context.      All subsequent log cal, Clear the current request context entirely.      Must be called at the end of ea, http_request_duration_seconds Histogram, http_requests_total Counter (+6 more)

### Community 14 - "Chat Routes"
Cohesion: 0.33
Nodes (13): Request, Session, ChatRequest, HTTPException, LangGraphAgent Singleton, chat(), chat_stream(), clear_chat_history() (+5 more)

### Community 15 - "Main App & Langfuse"
Cohesion: 0.22
Nodes (12): error_example(), langfuse_tracing_middleware(), lifespan(), log_demo(), Example endpoint that demonstrates error logging., Endpoint to demonstrate different log levels., Manage application lifecycle events., Create a Langfuse trace for each HTTP request. (+4 more)

### Community 16 - "Chart Schemas"
Cohesion: 0.14
Nodes (13): Common Skill Categories, Find Skills, How to Help Users Find Skills, Step 1: Understand What They Need, Step 2: Check the Leaderboard First, Step 3: Search for Skills, Step 4: Verify Quality Before Recommending, Step 5: Present Options to the User (+5 more)

### Community 17 - "System Prompt"
Cohesion: 0.18
Nodes (11): generic_exception_handler(), http_exception_handler(), Request, Capture HTTP errors and emit structured logs., Format Pydantic validation errors into user-friendly JSON., Capture validation errors with field context., Capture all unhandled exceptions in one place., Catch all unhandled exceptions. (+3 more)

### Community 18 - "Config Tests"
Cohesion: 0.20
Nodes (9): logging_middleware(), Log all HTTP requests and responses., get_logger(), log_request_response(), Get a configured structlog logger.      Args:         name: Logger name (usually, FastAPI middleware for logging requests and responses., Configures the Prometheus middleware and exposes the /metrics endpoint., setup_metrics() (+1 more)

### Community 19 - "Startup Script"
Cohesion: 0.22
Nodes (9): get_status(), health_check(), Any, Health check endpoint with detailed logging., Root endpoint for basic connectivity tests., Production health check — validates API and database connectivity., Root endpoint with welcome message., Example API endpoint with request context logging. (+1 more)

### Community 20 - "Graphify References: Query"
Cohesion: 0.28
Nodes (9): Graphify Instructions for Claude, MCP Graph Server, Native CLAUDE.md Graphify Integration, Post-Commit Hook Auto-Rebuild, BFS Graph Traversal, Explain Query for Single Node, Path Query Between Concepts, Query Result Feedback Loop (+1 more)

### Community 21 - "Graphify References: Exports"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 22 - "Graphify References: Add/Watch"
Cohesion: 0.33
Nodes (7): FastAPI Project Architecture, Docker Compose Infrastructure Stack, Database Service with Connection Pooling, Langfuse LLM Observability Tracing, LangGraph Multi-Agent Architecture, LLM Service with Retry and Fallback, Prometheus Grafana Observability Stack

### Community 23 - "Graphify References: Hooks"
Cohesion: 0.29
Nodes (7): Folder Watch for Auto-Update, URL Ingestion and Corpus Addition, Graph Export Formats, Build Merge Function, Cluster-Only Mode, Code-Only Optimized Update, Incremental Update Pipeline

### Community 24 - "Graphify References: Query"
Cohesion: 0.29
Nodes (6): ChatRequest, ChatResponse, Payload sent to the /chat endpoint., Standard response from the /chat endpoint., Chunk format for Server-Sent Events (SSE) streaming., StreamResponse

### Community 25 - "Graphify References: Update"
Cohesion: 0.33
Nodes (5): Current date and time, Instructions, Name: {agent_name}, Role: A world class assistant, What you know about the user

### Community 26 - "CLI Entry"
Cohesion: 0.40
Nodes (5): parse_allowed_origins(), parse_list_from_env(), Any, Parse a comma-separated list from an environment variable., Parse comma-separated string into list of origins.

### Community 27 - "OpenCode Plugin Config"
Cohesion: 0.60
Nodes (3): start.sh script, ensure_postgres(), start_langfuse()

### Community 28 - "OpenCode Dependencies"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 29 - "Readme Security Concepts"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 30 - "Graphify References: Transcribe"
Cohesion: 0.50
Nodes (3): For /graphify explain, For /graphify path, graphify reference: query, path, explain

### Community 31 - "Graphify References: GitHub Merge"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 35 - "OpenCode Graphify Plugin"
Cohesion: 1.00
Nodes (3): JWT Authentication, Rate Limiting, Input Sanitization and Password Validation

### Community 36 - "Prompt Template"
Cohesion: 0.67
Nodes (3): Extraction Subagent Prompt Template, Domain-Aware Whisper Prompt Strategy, Whisper Transcription

### Community 38 - "Rate Limiter"
Cohesion: 0.67
Nodes (3): Cross-Repo Graph Merge, GitHub Repository Clone, Monorepo Multi-Service Merge

## Knowledge Gaps
- **168 isolated node(s):** `$schema`, `plugin`, `@opencode-ai/plugin`, `SecretStr`, `Any` (+163 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LangGraphAgent` connect `LangGraph Agent Infrastructure` to `LLM Service`, `Chat Routes`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `DatabaseService` connect `Auth & Database Layer` to `Config & Settings`, `LangGraph Agent Infrastructure`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Why does `Settings` connect `Config & Settings` to `Auth & Database Layer`, `LangGraph Agent Infrastructure`, `JWT Auth Utilities`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DatabaseService` (e.g. with `Request` and `User`) actually correct?**
  _`DatabaseService` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Session` (e.g. with `Request` and `Session`) actually correct?**
  _`Session` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `LangGraphAgent` (e.g. with `Request` and `Session`) actually correct?**
  _`LangGraphAgent` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Environment` (e.g. with `Message` and `User`) actually correct?**
  _`Environment` has 11 INFERRED edges - model-reasoned connections that need verification._