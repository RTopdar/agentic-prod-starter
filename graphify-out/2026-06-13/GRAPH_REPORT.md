# Graph Report - .  (2026-06-13)

## Corpus Check
- Corpus is ~32,036 words - fits in a single context window. You may not need a graph.

## Summary
- 357 nodes · 531 edges · 31 communities (25 shown, 6 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 69 edges (avg confidence: 0.62)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_LangGraph Agent & Messages|LangGraph Agent & Messages]]
- [[_COMMUNITY_User & Session Models|User & Session Models]]
- [[_COMMUNITY_Auth Schemas & Validation|Auth Schemas & Validation]]
- [[_COMMUNITY_FastAPI App Main|FastAPI App Main]]
- [[_COMMUNITY_Logging Context Manager|Logging Context Manager]]
- [[_COMMUNITY_Logging Configuration|Logging Configuration]]
- [[_COMMUNITY_Pydantic Config Settings|Pydantic Config Settings]]
- [[_COMMUNITY_LLM Service|LLM Service]]
- [[_COMMUNITY_Graphify Pipeline|Graphify Pipeline]]
- [[_COMMUNITY_Graphify Query & References|Graphify Query & References]]
- [[_COMMUNITY_Architecture & Infra Docs|Architecture & Infra Docs]]
- [[_COMMUNITY_Observability Stack|Observability Stack]]
- [[_COMMUNITY_Update & Export Workflows|Update & Export Workflows]]
- [[_COMMUNITY_Config Tests|Config Tests]]
- [[_COMMUNITY_Coding Guidelines|Coding Guidelines]]
- [[_COMMUNITY_Start Script|Start Script]]
- [[_COMMUNITY_CLI Entry Point|CLI Entry Point]]
- [[_COMMUNITY_Opencode Plugin Config|Opencode Plugin Config]]
- [[_COMMUNITY_Opencode Plugin Package|Opencode Plugin Package]]
- [[_COMMUNITY_Auth & Security Docs|Auth & Security Docs]]
- [[_COMMUNITY_Extraction & Transcription|Extraction & Transcription]]
- [[_COMMUNITY_GitHub & Merge Workflows|GitHub & Merge Workflows]]
- [[_COMMUNITY_Skill Discovery|Skill Discovery]]
- [[_COMMUNITY_System Prompt Template|System Prompt Template]]
- [[_COMMUNITY_Token Benchmark|Token Benchmark]]

## God Nodes (most connected - your core abstractions)
1. `Session` - 22 edges
2. `Environment` - 19 edges
3. `User` - 18 edges
4. `DatabaseService` - 18 edges
5. `BaseModel` - 14 edges
6. `Graphify Pipeline` - 14 edges
7. `Settings` - 12 edges
8. `LangGraphAgent` - 12 edges
9. `UserCreate` - 10 edges
10. `Message` - 9 edges

## Surprising Connections (you probably didn't know these)
- `Graphify Pipeline` --conceptually_related_to--> `Production Agentic System`  [INFERRED]
  .claude/skills/graphify/SKILL.md → .github/copilot-instructions.md
- `Native CLAUDE.md Graphify Integration` --conceptually_related_to--> `Graphify Instructions for Claude`  [INFERRED]
  .claude/skills/graphify/references/hooks.md → CLAUDE.md
- `FastAPI Project Architecture` --conceptually_related_to--> `LangGraph Multi-Agent Architecture`  [INFERRED]
  AGENTS.md → README.md
- `FastAPI Project Architecture` --conceptually_related_to--> `LLM Service with Retry and Fallback`  [INFERRED]
  AGENTS.md → README.md
- `Graphify Pipeline` --conceptually_related_to--> `Parallel Subagent Dispatch`  [EXTRACTED]
  .claude/skills/graphify/SKILL.md → .opencode/skills/graphify/SKILL.md

## Import Cycles
- 1-file cycle: `app/main.py -> app/main.py`
- 1-file cycle: `app/core/langgraph/graph.py -> app/core/langgraph/graph.py`

## Hyperedges (group relationships)
- **Karpathy-Inspired Coding Behavioral Principles** — agents_think_before_coding, agents_simplicity_first, agents_surgical_changes, agents_goal_driven_execution, skills_karpathy_principles [EXTRACTED 1.00]
- **Graphify Query and Traversal Modes** — references_query_bfs_traversal, references_query_dfs_traversal, references_query_path_query, references_query_explain_query, references_query_vocabulary_expansion [EXTRACTED 1.00]
- **Graphify Export Targets** — references_exports_graph_export, references_exports_mcp_server, references_exports_token_benchmark [EXTRACTED 1.00]
- **Graphify Pipeline Components** — graphify_skill_ast_extraction, graphify_skill_semantic_extraction, graphify_skill_community_detection, graphify_skill_knowledge_graph, graphify_skill_god_nodes, graphify_skill_html_viz, graphify_skill_graph_report, graphify_skill_extraction_cache, graphify_skill_subagent_dispatch [EXTRACTED 1.00]
- **Production System Architecture Stack** — _github_copilot_instructions_fastapi_app, _github_copilot_instructions_observability_stack, _github_copilot_instructions_postgresql_pgvector, _github_copilot_instructions_asymmetric_jwt, _github_copilot_instructions_slowapi_rate_limiting, _github_copilot_instructions_pydantic_settings, _github_copilot_instructions_structlog_logging [EXTRACTED 1.00]

## Communities (31 total, 6 thin omitted)

### Community 0 - "LangGraph Agent & Messages"
Cohesion: 0.06
Nodes (42): Message, BaseChatModel, BaseMessage, Message, AsyncConnectionPool, AsyncMemory, CallbackHandler, Command (+34 more)

### Community 1 - "User & Session Models"
Cohesion: 0.07
Nodes (35): Request, User, User, ChatSession, HTTPAuthorizationCredentials, BaseModel, Database Models Export. This allows simple imports like: `from app.models.databa, Represents a user session in the system, linked to a specific user. (+27 more)

### Community 2 - "Auth Schemas & Validation"
Cohesion: 0.09
Nodes (35): Any, HTTPException, Schema for user registration inputs., Schema for the JWT Access Token response., Public user profile schema (safe to return to frontend).     Notice we exclude t, Token, UserCreate, UserResponse (+27 more)

### Community 3 - "FastAPI App Main"
Cohesion: 0.09
Nodes (31): error_example(), generic_exception_handler(), get_status(), health_check(), http_exception_handler(), langfuse_tracing_middleware(), lifespan(), log_demo() (+23 more)

### Community 4 - "Logging Context Manager"
Cohesion: 0.10
Nodes (22): BoundLogger, get_logger(), log_request_response(), LogContext, Get a configured structlog logger.      Args:         name: Logger name (usually, Context manager for adding context to logs., Enter context and bind context variables., Create a log context with bound variables.      Example:         with logger.wit (+14 more)

### Community 5 - "Logging Configuration"
Cohesion: 0.16
Nodes (19): Any, add_environment(), add_log_level(), add_process_id(), add_service_name(), add_timestamp(), add_version(), configure_logging() (+11 more)

### Community 6 - "Pydantic Config Settings"
Cohesion: 0.12
Nodes (11): Any, BaseSettings, Generate PostgreSQL connection URL., Check if running in development environment., Check if running in production environment., Parse comma-separated string into list of origins., Parse debug flag from string to boolean., Parse integer fields from string. (+3 more)

### Community 7 - "LLM Service"
Cohesion: 0.15
Nodes (9): BaseChatModel, BaseMessage, LLMRegistry, LLMService, Internal method that executes the actual API call., Public interface. Wraps the retry logic with a Fallback loop.         If the pri, Bind tools to the current LLM instance., Manages LLM calls with automatic retries and fallback logic. (+1 more)

### Community 8 - "Graphify Pipeline"
Cohesion: 0.20
Nodes (14): Graphify Trigger (CLAUDE.md), AST Structural Extraction, Extraction Audit Trail (EXTRACTED/INFERRED/AMBIGUOUS), Community Detection, Semantic Extraction Cache, Gemini LLM Backend Extraction, God Nodes Analysis, GRAPH_REPORT.md (+6 more)

### Community 9 - "Graphify Query & References"
Cohesion: 0.24
Nodes (10): Graphify Instructions for Claude, MCP Graph Server, Native CLAUDE.md Graphify Integration, Post-Commit Hook Auto-Rebuild, BFS Graph Traversal, DFS Graph Traversal, Explain Query for Single Node, Path Query Between Concepts (+2 more)

### Community 10 - "Architecture & Infra Docs"
Cohesion: 0.29
Nodes (8): Asymmetric JWT Authentication, FastAPI Application, Observability Stack, PostgreSQL with pgvector, Production Agentic System, Pydantic Settings Configuration, SlowAPI Rate Limiting, Structlog Structured Logging

### Community 11 - "Observability Stack"
Cohesion: 0.33
Nodes (7): FastAPI Project Architecture, Docker Compose Infrastructure Stack, Database Service with Connection Pooling, Langfuse LLM Observability Tracing, LangGraph Multi-Agent Architecture, LLM Service with Retry and Fallback, Prometheus Grafana Observability Stack

### Community 12 - "Update & Export Workflows"
Cohesion: 0.29
Nodes (7): Folder Watch for Auto-Update, URL Ingestion and Corpus Addition, Graph Export Formats, Build Merge Function, Cluster-Only Mode, Code-Only Optimized Update, Incremental Update Pipeline

### Community 13 - "Config Tests"
Cohesion: 0.40
Nodes (5): parse_allowed_origins(), parse_list_from_env(), Any, Parse a comma-separated list from an environment variable., Parse comma-separated string into list of origins.

### Community 14 - "Coding Guidelines"
Cohesion: 0.70
Nodes (5): Goal-Driven Execution, Simplicity First, Surgical Changes, Think Before Coding, Karpathy-Inspired Coding Guidelines

### Community 15 - "Start Script"
Cohesion: 0.60
Nodes (3): start.sh script, ensure_postgres(), start_langfuse()

### Community 19 - "Auth & Security Docs"
Cohesion: 1.00
Nodes (3): JWT Authentication, Rate Limiting, Input Sanitization and Password Validation

### Community 20 - "Extraction & Transcription"
Cohesion: 0.67
Nodes (3): Extraction Subagent Prompt Template, Domain-Aware Whisper Prompt Strategy, Whisper Transcription

### Community 21 - "GitHub & Merge Workflows"
Cohesion: 0.67
Nodes (3): Cross-Repo Graph Merge, GitHub Repository Clone, Monorepo Multi-Service Merge

## Knowledge Gaps
- **34 isolated node(s):** `$schema`, `plugin`, `@opencode-ai/plugin`, `RequestValidationError`, `Exception` (+29 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Environment` connect `LangGraph Agent & Messages` to `User & Session Models`?**
  _High betweenness centrality (0.149) - this node is a cross-community bridge._
- **Why does `log_request_response()` connect `Logging Context Manager` to `FastAPI App Main`, `Logging Configuration`?**
  _High betweenness centrality (0.144) - this node is a cross-community bridge._
- **Why does `FastAPI` connect `FastAPI App Main` to `User & Session Models`, `Auth Schemas & Validation`?**
  _High betweenness centrality (0.127) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `Session` (e.g. with `Request` and `User`) actually correct?**
  _`Session` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Environment` (e.g. with `Message` and `User`) actually correct?**
  _`Environment` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `User` (e.g. with `Request` and `User`) actually correct?**
  _`User` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `DatabaseService` (e.g. with `Request` and `User`) actually correct?**
  _`DatabaseService` has 8 INFERRED edges - model-reasoned connections that need verification._