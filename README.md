# agentic-prod-starter

A production-grade reference template for building agentic AI systems with FastAPI, PostgreSQL, and a full observability stack.

> **Status**: This is a work-in-progress template. Many modules are structurally defined but not yet wired into working endpoints. The table of contents below reflects the intended architecture.

---

## Table of Contents

- [Creating Modular Codebase](#creating-modular-codebase)
  - [Managing Dependencies](#managing-dependencies)
  - [Setting Environment Configuration](#setting-environment-configuration)
  - [Containerization Strategy](#containerization-strategy)
- [Building Data Persistence Layer](#building-data-persistence-layer)
  - [Structured Modeling](#structured-modeling)
  - [Entity Definition](#entity-definition)
  - [Data Transfer Objects (DTOs)](#data-transfer-objects-dtos)
- [Security & Safeguards Layer](#security--safeguards-layer)
  - [Rate Limiting Feature](#rate-limiting-feature)
  - [Sanitization Check Logic](#sanitization-check-logic)
  - [Context Management](#context-management)
- [The Service Layer for AI Agents](#the-service-layer-for-ai-agents)
  - [Connection Pooling](#connection-pooling)
  - [LLM Unavailability Handling](#llm-unavailability-handling)
  - [Circuit Breaking](#circuit-breaking)
- [Multi-Agentic Architecture](#multi-agentic-architecture)
  - [Long-Term Memory Integration](#long-term-memory-integration)
  - [Tool Calling Feature](#tool-calling-feature)
- [Building The API Gateway](#building-the-api-gateway)
  - [Auth Endpoints](#auth-endpoints)
  - [Real-Time Streaming](#real-time-streaming)
- [Observability & Operational Testing](#observability--operational-testing)
  - [Creating Metrics to Evaluate](#creating-metrics-to-evaluate)
  - [Middleware Based Testing](#middleware-based-testing)
  - [Streaming Endpoints Interaction](#streaming-endpoints-interaction)
  - [Context Management Using Async](#context-management-using-async)
  - [DevOps Automation](#devops-automation)
- [Evaluation Framework](#evaluation-framework)
  - [LLM-as-a-Judge](#llm-as-a-judge)
  - [Automated Grading](#automated-grading)
- [Architecture Stress Testing](#architecture-stress-testing)
  - [Simulating Traffic](#simulating-traffic)
  - [Performance Analysis](#performance-analysis)

---

## Quick Start

```bash
# 1. Clone and install dependencies
uv sync

# 2. Copy environment configuration
cp .env.example .env.dev
# Edit .env.dev with your API keys

# 3. Start infrastructure (PostgreSQL, Prometheus, Grafana)
docker-compose up -d

# (Optional) Start Langfuse — locally in background or use Langfuse Cloud
# Update LANGFUSE_BASE_URL in .env.dev accordingly

# 4. Run the FastAPI server
uvicorn app.main:app --reload

# 5. Verify
curl http://localhost:8000/health
```

## Lint / Test

```bash
ruff check app/ && ruff format --check app/
pytest
```

---

## Codebase Knowledge Graph

This project has a persistent knowledge graph built with [graphify](https://github.com/safishamsi/graphify). After running `/graphify` (triggered via `AGENTS.md`), the graph lives in `graphify-out/` and includes:

| Output | Purpose |
| ------ | ------- |
| `graph.html` | Interactive visualization — open in any browser |
| `GRAPH_REPORT.md` | Plain-language audit with god nodes, community detection, and surprising connections |
| `graph.json` | GraphRAG-ready raw data |
| `cost.json` | Token usage across runs |

**When exploring the codebase**, use `graphify query "<question>"` instead of grepping raw files — it returns a scoped subgraph via BFS/DFS traversal and cites `source_location` for every fact. For relationships between two concepts, run `graphify path "ConceptA" "ConceptB"`.

The graph is rebuilt incrementally (`--update`) and automatically excludes `.env`, `.pem`, and other sensitive files. See `graphify-out/GRAPH_REPORT.md` for extracted entities, inferred connections, and cross-community bridges.

---

## Creating Modular Codebase

### Managing Dependencies

Dependencies are managed via [uv](https://github.com/astral-sh/uv) and declared in `pyproject.toml`. Synchronize with:

```bash
uv sync                        # install all deps
uv sync --group dev            # lint/format tools
uv sync --group test           # pytest + httpx
```

Python 3.13 is required (see `.python-version`).

### Setting Environment Configuration

Environment-specific `.env` files are loaded by `app/core/config.py` via Pydantic Settings. Priority order (first found wins): `.env.dev` → `.env.stage` → `.env.prod` → `.env.local` → `.env`. Runtime environment is controlled by the `APP_ENV` variable.

### Containerization Strategy

`docker-compose.yml` orchestrates the core stack. Langfuse (LLM observability) runs externally — either locally in the background or cloud-hosted — configured via `LANGFUSE_*` env vars.

| Service   | Container             | Port  | In docker-compose |
| --------- | --------------------- | ----- | ----------------- |
| App       | FastAPI (Uvicorn)     | 8000  | Yes               |
| Database  | PostgreSQL + pgvector | 5432  | Yes               |
| Metrics   | Prometheus            | 9090  | Yes               |
| Viz       | Grafana               | 3001  | Yes               |
| Container | cAdvisor              | 8080  | Yes               |
| LLM Obs   | Langfuse              | 3000  | External          |

Start core services with `docker-compose up -d`. Start Langfuse separately (e.g. `docker compose -f docker-compose.langfuse.yml up -d` or use Langfuse Cloud).

Start everything with `docker-compose up -d`.

---

## Building Data Persistence Layer

### Structured Modeling

SQLModel-based ORM with declarative table definitions in `app/models/`. Base class (`BaseModel`) provides `created_at` timestamps automatically.

### Entity Definition

| Model     | File                    | Key Fields                                |
| --------- | ----------------------- | ----------------------------------------- |
| `User`    | `app/models/user.py`   | `id`, `email` (unique), `hashed_password` |
| `Session` | `app/models/session.py` | `id`, `user_id` (FK), `name`              |
| `Thread`  | `app/models/thread.py`  | `id` (str, PK), `created_at`              |

All models are re-exported via `app/models/database.py` for convenient imports.

### Data Transfer Objects (DTOs)

Pydantic schemas in `app/schemas/`:

| Schema            | File                         | Purpose                                              |
| ----------------- | ---------------------------- | ---------------------------------------------------- |
| `UserCreate`      | `app/schemas/auth.py`        | Registration input with zxcvbn password validation    |
| `Token`           | `app/schemas/auth.py`        | JWT token response                                   |
| `UserResponse`    | `app/schemas/auth.py`        | Public user profile (no password)                    |
| `Message`         | `app/schemas/chat.py`        | Chat message with content validation  |
| `ChatRequest`     | `app/schemas/chat.py`        | Chat endpoint payload                |
| `StreamResponse`  | `app/schemas/chat.py`        | SSE streaming chunk format           |
| `GraphState`      | `app/schemas/graph.py`       | LangGraph state with memory context   |

---

## Security & Safeguards Layer

### Rate Limiting Feature

SlowAPI-based IP rate limiting defined in `app/core/limiter.py`. Per-endpoint limits are configured via settings (`RATE_LIMIT_DEFAULT`, `RATE_LIMIT_CHAT`, `RATE_LIMIT_LOGIN`, etc.).

### Sanitization Check Logic

Utilities in `app/utils/sanitization.py` provide:
- `sanitize_string()` — HTML-escapes input, strips script tags, removes null bytes
- `sanitize_email()` — validates and normalizes email format

The `Message` schema also includes a `field_validator` that rejects messages containing `<script>` tags.

**Password Validation**: `UserCreate` schema uses `zxcvbn` (score ≥ 3 required) to evaluate password strength, with contextual feedback messages.

### Context Management

**JWT Authentication**: Asymmetric RS256 tokens with separate access/refresh flows implemented in `app/utils/auth.py`. Key pair stored in `security/jwt_private.pem` / `security/jwt_public.pem`. Supports token creation, verification, and refresh.

**Password Hashing**: bcrypt via `User.hash_password()` / `User.verify_password()`.

---

## The Service Layer for AI Agents

### Connection Pooling

`DatabaseService` (singleton in `app/services/database.py`) creates a SQLAlchemy `QueuePool` with configurable `pool_size`, `max_overflow`, `pool_timeout`, and `pool_recycle`. Tables are auto-created on initialization (code-first migration).

Key methods:
- **User**: `create_user()`, `get_user_by_email()` (login flow), `get_user_by_id()` (token-based lookups)
- **Session**: `create_session()`, `get_session()` (single fetch), `get_user_sessions()` (list by user)

### LLM Unavailability Handling

`LLMRegistry` in `app/services/llm.py` registers primary and backup models via `ChatOpenAI` pointed at any OpenAI-compatible API. The `LLMService` resilience layer combines two strategies:

1. **Tenacity retry** — each LLM call retries up to `MAX_LLM_CALL_RETRIES` times with exponential backoff (2s, 4s, 8s...). Catches rate limits, timeouts, connection drops, and 5xx errors.
2. **Model fallback** — if retries are exhausted for one model, `LLMService` switches to the next registered model and retries from scratch. Fails only after all models are exhausted.

This means a transient provider hiccup is absorbed by retries, while a model-specific outage triggers automatic fallback to the backup model (e.g. primary → fallback).

### Circuit Breaking

> **Not yet implemented.** The directory structure and tenacity dependency are in place. Planned for `app/services/llm.py`.

---

## Multi-Agentic Architecture

### Long-Term Memory Integration

`LangGraphAgent` in `app/core/langgraph/graph.py` integrates mem0ai for long-term memory backed by pgvector:
- On each user message, it searches pgvector for relevant memories and injects them into the system prompt via `{long_term_memory}`.
- After each response, extracted facts are saved to pgvector asynchronously (fire-and-forget).
- Configured via `POSTGRES_*` env vars; uses `text-embedding-3-small` for embeddings.

### LangGraph Workflow (StateGraph + Checkpointing)

The `LangGraphAgent` builds a two-node `StateGraph`:
- **`chat` node** — loads system prompt (with memory context), calls `LLMService`, routes to `tool_call` or `END` if the model requests a tool.
- **`tool_call` node** — executes the requested tool and loops back to `chat`.
- Persistence is handled by `AsyncPostgresSaver` (PostgreSQL checkpointer), enabling session-level state history per `thread_id`.

### Tool Calling Feature

Tools are registered in `app/core/langgraph/tools/__init__.py`. Currently available:
- **DuckDuckGo Search** (`app/core/langgraph/duckduckgosearch.py`) — web search via `DuckDuckGoSearchResults` (10 results, error-tolerant).

System prompts live in `app/core/prompts/` as markdown templates with `{variable}` injection via `load_system_prompt()`.

---

## Building The API Gateway

### Auth Endpoints

`app/api/v1/auth.py` defines 4 endpoints and 2 FastAPI dependency functions used for protected routes:

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/auth/register` | POST | None | Register user with zxcvbn password validation |
| `/auth/login` | POST | None | Authenticate and return JWT token pair |
| `/auth/session` | POST | Bearer token | Create a new chat session |
| `/auth/sessions` | GET | Bearer token | List all historical sessions for the user |

**Dependencies:**

- **`get_current_user`** — validates the JWT access token, extracts user ID from `sub` claim, and verifies the user exists via `get_user_by_id()`
- **`get_current_session`** — validates a session-specific JWT token, fetches the session via `get_session()`, and verifies it belongs to the authenticated user (returns 403 on mismatch)

Schema-level password validation uses `zxcvbn` (score ≥ 3 required) with contextual feedback. Routes are wired under the `/api/v1/auth` prefix via `app.include_router`. Code/test infrastructure and refresh-token rotation are planned extensions.

### Chat Endpoints

`app/api/v1/chat.py` implements 4 endpoints for conversational AI:

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/chatbot/chat` | POST | Session token | Standard request/response chat via LangGraph agent |
| `/chatbot/chat/stream` | POST | Session token | Server-Sent Events (SSE) streaming chat |
| `/chatbot/messages` | GET | Session token | Retrieve full conversation history for a session |
| `/chatbot/messages` | DELETE | Session token | Clear (hard delete) session conversation history |

The `POST /chat` endpoint delegates to `LangGraphAgent.get_response()`, which runs the full StateGraph workflow. `POST /chat/stream` returns a `StreamingResponse` with SSE-formatted chunks (`data: {"content": "...", "done": false}\n\n`), terminated by a `"done": true` signal.

### Real-Time Streaming

The `POST /chatbot/chat/stream` endpoint uses SSE (`text/event-stream`) to stream LLM output character-by-character. The `StreamResponse` schema defines the chunk format with `content` and `done` fields. The LangGraph agent's `get_stream_response()` async generator feeds the stream. Error handling within the stream yields an error chunk before terminating.

---

## Observability & Operational Testing

### Creating Metrics to Evaluate

Prometheus metrics are defined in `app/core/metrics.py` and wired via `setup_metrics(app)` in `app/main.py`, which exposes the `/metrics` scrape endpoint:

| Metric | Type | Labels | Purpose |
|---|---|---|---|
| `http_requests_total` | Counter | method, endpoint, status | Request count per route |
| `http_request_duration_seconds` | Histogram | method, endpoint | Latency distribution (p50/p95/p99) |
| `db_connections` | Gauge | — | Active database connections (leak detection) |
| `llm_inference_duration_seconds` | Histogram | model | LLM inference latency (buckets: 0.1s-30s) |
| `llm_stream_duration_seconds` | Histogram | model | Streaming LLM latency (buckets: 0.1s-60s) |

- **`MetricsMiddleware`** (`app/core/middleware.py`) auto-records `http_requests_total` and `http_request_duration_seconds` on every request, filtering out `/metrics` and `/health`.
- **`LoggingContextMiddleware`** (`app/core/middleware.py`) extracts User/Session IDs from JWT tokens before routing and binds them to structlog context. Both middleware are registered in `app/main.py`.
- Prometheus, Grafana, and cAdvisor are configured in `docker-compose.yml` with provisioning directory mounts.
- Grafana dashboards are planned but not yet provisioned.

### Langfuse Tracing (LLM Observability)

Langfuse is configured for per-request traces spanning HTTP, graph execution, memory operations, and LLM generations:

- **HTTP middleware** (`langfuse_tracing_middleware` in `app/main.py`) — creates a root span per HTTP request (method + path). All downstream operations nest under this span automatically via Langfuse's async context propagation.
- **Graph layer** (`LangGraphAgent` in `app/core/langgraph/graph.py`) — the `CallbackHandler` is passed in the graph's `config` so every LLM `ainvoke()` is traced as a generation (tokens, model, latency, cost). Manual spans wrap `memory_search` in `get_response()`, each tool invocation in `_tool_call()`, and `memory_add` in the fire-and-forget task.
- **LLM service** (`LLMService` in `app/services/llm.py`) — intentionally has zero Langfuse code. The `CallbackHandler` from the graph config propagates to the LLM via LangChain's run context. Tenacity retries preserve the callback on every attempt.
- **Lifecycle** — client initializes at startup (`init_langfuse()`) and flushes/shuts down on shutdown.

The resulting trace hierarchy per request:

```
Span: "GET /chat" (middleware)              ← root
  ├─ Span: "memory_search"                  ← manual
  ├─ Generation: "{model_name}"             ← auto (CallbackHandler)
  ├─ Span: "tool_call:duckduckgo_search"    ← manual (per tool)
  ├─ Generation: "{model_name}"             ← auto (2nd LLM call)
  └─ (fire-and-forget)
       Trace: "memory_add" (session=X)      ← standalone, linked by session_id
```

Configured via `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_BASE_URL` in `.env`.

### Middleware Based Testing

Structured logging middleware is active in `app/main.py`:
- `logging_middleware` logs every HTTP request/response
- `http_exception_handler`, `validation_exception_handler`, and `generic_exception_handler` capture errors with structured context

### Streaming Endpoints Interaction

> **Not yet implemented.**

### Context Management Using Async

The application uses FastAPI's async lifecycle (`lifespan` context manager) and async exception handlers. `DatabaseService` exposes `async` methods. The `examples/logging_demo.py` script demonstrates async request logging patterns.

### DevOps Automation

- `docker-compose.yml` includes health checks, restart policies, and volume management for all services.
- `start.sh` is deprecated — use `docker-compose up -d` instead.

---

## Evaluation Framework

### LLM-as-a-Judge

> **Not yet implemented.** Directory at `evals/` exists for future evaluation scripts.

### Automated Grading

> **Not yet implemented.**

---

## Architecture Stress Testing

### Simulating Traffic

> **Not yet implemented.** `scripts/` directory exists for load testing scripts.

### Performance Analysis

> **Not yet implemented.**

---



Built with FastAPI, LangChain/LangGraph, SQLModel, OpenAI-compatible LLMs, Langfuse, Prometheus/Grafana.
