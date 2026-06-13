# Graph Report - .  (2026-06-13)

## Corpus Check
- 0 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 550 nodes · 744 edges · 43 communities (34 shown, 9 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 69 edges (avg confidence: 0.62)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Auth & Database Models|Auth & Database Models]]
- [[_COMMUNITY_LangGraph & LLM Pipeline|LangGraph & LLM Pipeline]]
- [[_COMMUNITY_Structured Logging|Structured Logging]]
- [[_COMMUNITY_Project Documentation|Project Documentation]]
- [[_COMMUNITY_FastAPI App Entrypoint|FastAPI App Entrypoint]]
- [[_COMMUNITY_Agent Behavioral Guidelines|Agent Behavioral Guidelines]]
- [[_COMMUNITY_JWT Authentication|JWT Authentication]]
- [[_COMMUNITY_Copilot Instructions|Copilot Instructions]]
- [[_COMMUNITY_Graphify Pipeline|Graphify Pipeline]]
- [[_COMMUNITY_Infrastructure & Observability|Infrastructure & Observability]]
- [[_COMMUNITY_Application Configuration|Application Configuration]]
- [[_COMMUNITY_AGENTS.md Guidelines|AGENTS.md Guidelines]]
- [[_COMMUNITY_LLM Service Registry|LLM Service Registry]]
- [[_COMMUNITY_Find Skills|Find Skills]]
- [[_COMMUNITY_Graphify Reference Docs|Graphify Reference Docs]]
- [[_COMMUNITY_Export Formats|Export Formats]]
- [[_COMMUNITY_Infrastructure Stack|Infrastructure Stack]]
- [[_COMMUNITY_Update & Watch|Update & Watch]]
- [[_COMMUNITY_Chat Schemas|Chat Schemas]]
- [[_COMMUNITY_System Prompts|System Prompts]]
- [[_COMMUNITY_Test Utilities|Test Utilities]]
- [[_COMMUNITY_Startup Script|Startup Script]]
- [[_COMMUNITY_Add Watch Reference|Add Watch Reference]]
- [[_COMMUNITY_Hooks Reference|Hooks Reference]]
- [[_COMMUNITY_Query Reference|Query Reference]]
- [[_COMMUNITY_Update Reference|Update Reference]]
- [[_COMMUNITY_Main Entrypoint|Main Entrypoint]]
- [[_COMMUNITY_OpenCode Plugin|OpenCode Plugin]]
- [[_COMMUNITY_OpenCode Package|OpenCode Package]]
- [[_COMMUNITY_JWT & Sanitization|JWT & Sanitization]]
- [[_COMMUNITY_Extraction Spec|Extraction Spec]]
- [[_COMMUNITY_GitHub Clone & Merge|GitHub Clone & Merge]]
- [[_COMMUNITY_Cross-Repo Merge|Cross-Repo Merge]]
- [[_COMMUNITY_Transcribe Reference|Transcribe Reference]]
- [[_COMMUNITY_Skill Discovery|Skill Discovery]]
- [[_COMMUNITY_Prompt Templates|Prompt Templates]]
- [[_COMMUNITY_Extraction Subagent|Extraction Subagent]]
- [[_COMMUNITY_Token Benchmark|Token Benchmark]]

## God Nodes (most connected - your core abstractions)
1. `Session` - 22 edges
2. `Environment` - 19 edges
3. `User` - 18 edges
4. `DatabaseService` - 18 edges
5. `BaseModel` - 16 edges
6. `agentic-prod-starter` - 14 edges
7. `Graphify Pipeline` - 14 edges
8. `Settings` - 13 edges
9. `LangGraphAgent` - 12 edges
10. `create_access_token()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `Native CLAUDE.md Graphify Integration` --conceptually_related_to--> `Graphify Instructions for Claude`  [INFERRED]
  .claude/skills/graphify/references/hooks.md → CLAUDE.md
- `FastAPI Project Architecture` --conceptually_related_to--> `LangGraph Multi-Agent Architecture`  [INFERRED]
  AGENTS.md → README.md
- `FastAPI Project Architecture` --conceptually_related_to--> `LLM Service with Retry and Fallback`  [INFERRED]
  AGENTS.md → README.md
- `Graphify Pipeline` --conceptually_related_to--> `Production Agentic System`  [INFERRED]
  .claude/skills/graphify/SKILL.md → .github/copilot-instructions.md
- `Graphify Pipeline` --conceptually_related_to--> `Parallel Subagent Dispatch`  [EXTRACTED]
  .claude/skills/graphify/SKILL.md → .opencode/skills/graphify/SKILL.md

## Import Cycles
- 1-file cycle: `app/main.py -> app/main.py`

## Communities (43 total, 9 thin omitted)

### Community 0 - "Auth & Database Models"
Cohesion: 0.06
Nodes (54): Request, User, User, ChatSession, HTTPAuthorizationCredentials, HTTPException, BaseModel, Database Models Export. This allows simple imports like: `from app.models.databa (+46 more)

### Community 1 - "LangGraph & LLM Pipeline"
Cohesion: 0.05
Nodes (42): Message, BaseChatModel, BaseMessage, Message, AsyncConnectionPool, AsyncMemory, CallbackHandler, Command (+34 more)

### Community 2 - "Structured Logging"
Cohesion: 0.07
Nodes (41): Any, BoundLogger, add_environment(), add_log_level(), add_process_id(), add_service_name(), add_timestamp(), add_version() (+33 more)

### Community 3 - "Project Documentation"
Cohesion: 0.05
Nodes (41): agentic-prod-starter, Architecture Stress Testing, Auth Endpoints, Automated Grading, Building Data Persistence Layer, Building The API Gateway, Circuit Breaking, Codebase Knowledge Graph (+33 more)

### Community 4 - "FastAPI App Entrypoint"
Cohesion: 0.09
Nodes (31): error_example(), generic_exception_handler(), get_status(), health_check(), http_exception_handler(), langfuse_tracing_middleware(), lifespan(), log_demo() (+23 more)

### Community 5 - "Agent Behavioral Guidelines"
Cohesion: 0.10
Nodes (27): 1. Think Before Coding, 2. Simplicity First, 3. Surgical Changes, 4. Goal-Driven Execution, Anti-Patterns Summary, CLAUDE.md, Customization, Example 1: Drive-by Refactoring (+19 more)

### Community 6 - "JWT Authentication"
Cohesion: 0.18
Nodes (22): Any, Schema for the JWT Access Token response., Token, Token, create_access_token(), create_refresh_token(), create_tokens(), _load_private_key() (+14 more)

### Community 7 - "Copilot Instructions"
Cohesion: 0.09
Nodes (22): API Design, Build, Test, and Lint Commands, Code Organization, Configuration Management, Copilot Instructions for Agentic Production System, Core Components, Database Operations, Development Server (+14 more)

### Community 8 - "Graphify Pipeline"
Cohesion: 0.09
Nodes (22): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Interpreter guard for subcommands, Part A - Structural extraction for code files, Part B - Semantic extraction (parallel subagents) (+14 more)

### Community 9 - "Infrastructure & Observability"
Cohesion: 0.12
Nodes (22): Graphify Trigger (CLAUDE.md), Asymmetric JWT Authentication, FastAPI Application, Observability Stack, PostgreSQL with pgvector, Production Agentic System, Pydantic Settings Configuration, SlowAPI Rate Limiting (+14 more)

### Community 10 - "Application Configuration"
Cohesion: 0.12
Nodes (11): Any, BaseSettings, Generate PostgreSQL connection URL., Check if running in development environment., Check if running in production environment., Parse comma-separated string into list of origins., Parse debug flag from string to boolean., Parse integer fields from string. (+3 more)

### Community 11 - "AGENTS.md Guidelines"
Cohesion: 0.13
Nodes (17): 1. Think Before Coding, 3. Surgical Changes, 4. Goal-Driven Execution, AGENTS.md — prod-agentic-practice, Architecture, Auth Routes — Key Details, Behavioral Guidelines, Goal-Driven Execution (+9 more)

### Community 12 - "LLM Service Registry"
Cohesion: 0.15
Nodes (9): BaseChatModel, BaseMessage, LLMRegistry, LLMService, Internal method that executes the actual API call., Public interface. Wraps the retry logic with a Fallback loop.         If the pri, Bind tools to the current LLM instance., Manages LLM calls with automatic retries and fallback logic. (+1 more)

### Community 13 - "Find Skills"
Cohesion: 0.14
Nodes (13): Common Skill Categories, Find Skills, How to Help Users Find Skills, Step 1: Understand What They Need, Step 2: Check the Leaderboard First, Step 3: Search for Skills, Step 4: Verify Quality Before Recommending, Step 5: Present Options to the User (+5 more)

### Community 14 - "Graphify Reference Docs"
Cohesion: 0.28
Nodes (9): Graphify Instructions for Claude, MCP Graph Server, Native CLAUDE.md Graphify Integration, Post-Commit Hook Auto-Rebuild, BFS Graph Traversal, Explain Query for Single Node, Path Query Between Concepts, Query Result Feedback Loop (+1 more)

### Community 15 - "Export Formats"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 16 - "Infrastructure Stack"
Cohesion: 0.33
Nodes (7): FastAPI Project Architecture, Docker Compose Infrastructure Stack, Database Service with Connection Pooling, Langfuse LLM Observability Tracing, LangGraph Multi-Agent Architecture, LLM Service with Retry and Fallback, Prometheus Grafana Observability Stack

### Community 17 - "Update & Watch"
Cohesion: 0.29
Nodes (7): Folder Watch for Auto-Update, URL Ingestion and Corpus Addition, Graph Export Formats, Build Merge Function, Cluster-Only Mode, Code-Only Optimized Update, Incremental Update Pipeline

### Community 18 - "Chat Schemas"
Cohesion: 0.29
Nodes (6): ChatRequest, ChatResponse, Payload sent to the /chat endpoint., Standard response from the /chat endpoint., Chunk format for Server-Sent Events (SSE) streaming., StreamResponse

### Community 19 - "System Prompts"
Cohesion: 0.33
Nodes (5): Current date and time, Instructions, Name: {agent_name}, Role: A world class assistant, What you know about the user

### Community 20 - "Test Utilities"
Cohesion: 0.40
Nodes (5): parse_allowed_origins(), parse_list_from_env(), Any, Parse a comma-separated list from an environment variable., Parse comma-separated string into list of origins.

### Community 21 - "Startup Script"
Cohesion: 0.60
Nodes (3): start.sh script, ensure_postgres(), start_langfuse()

### Community 22 - "Add Watch Reference"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 23 - "Hooks Reference"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 24 - "Query Reference"
Cohesion: 0.50
Nodes (3): For /graphify explain, For /graphify path, graphify reference: query, path, explain

### Community 25 - "Update Reference"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 29 - "JWT & Sanitization"
Cohesion: 1.00
Nodes (3): JWT Authentication, Rate Limiting, Input Sanitization and Password Validation

### Community 30 - "Extraction Spec"
Cohesion: 0.67
Nodes (3): Extraction Subagent Prompt Template, Domain-Aware Whisper Prompt Strategy, Whisper Transcription

### Community 32 - "Cross-Repo Merge"
Cohesion: 0.67
Nodes (3): Cross-Repo Graph Merge, GitHub Repository Clone, Monorepo Multi-Service Merge

## Knowledge Gaps
- **163 isolated node(s):** `$schema`, `plugin`, `@opencode-ai/plugin`, `RequestValidationError`, `Exception` (+158 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Environment` connect `LangGraph & LLM Pipeline` to `Auth & Database Models`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Why does `log_request_response()` connect `Structured Logging` to `FastAPI App Entrypoint`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `FastAPI` connect `FastAPI App Entrypoint` to `Auth & Database Models`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `Session` (e.g. with `Request` and `User`) actually correct?**
  _`Session` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Environment` (e.g. with `Message` and `User`) actually correct?**
  _`Environment` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `User` (e.g. with `Request` and `User`) actually correct?**
  _`User` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `DatabaseService` (e.g. with `Request` and `User`) actually correct?**
  _`DatabaseService` has 8 INFERRED edges - model-reasoned connections that need verification._