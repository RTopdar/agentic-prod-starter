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

`docker-compose.yml` orchestrates the full stack:

| Service  | Container            | Port  |
| -------- | -------------------- | ----- |
| App      | FastAPI (Uvicorn)    | 8000  |
| Database | PostgreSQL + pgvector | 5432  |
| Metrics  | Prometheus           | 9090  |
| Viz      | Grafana              | 3001  |
| Container | cAdvisor            | 8080  |
| LLM Obs  | Langfuse             | 3000  |

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

| Schema            | File                         | Purpose                              |
| ----------------- | ---------------------------- | ------------------------------------ |
| `UserCreate`      | `app/schemas/auth.py`        | Registration input with validation    |
| `Token`           | `app/schemas/auth.py`        | JWT token response                   |
| `UserResponse`    | `app/schemas/auth.py`        | Public user profile (no password)    |
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

### Context Management

**JWT Authentication**: Asymmetric RS256 tokens with separate access/refresh flows implemented in `app/utils/auth.py`. Key pair stored in `security/jwt_private.pem` / `security/jwt_public.pem`. Supports token creation, verification, and refresh.

**Password Hashing**: bcrypt via `User.hash_password()` / `User.verify_password()`.

---

## The Service Layer for AI Agents

### Connection Pooling

`DatabaseService` (singleton in `app/services/database.py`) creates a SQLAlchemy `QueuePool` with configurable `pool_size`, `max_overflow`, `pool_timeout`, and `pool_recycle`. Tables are auto-created on initialization (code-first migration).

### LLM Unavailability Handling

`LLMRegistry` in `app/services/llm.py` registers primary and backup models via `ChatOpenRouter`. The backup model serves as a fallback when the primary is unavailable.

### Circuit Breaking

> **Not yet implemented.** The directory structure and tenacity dependency are in place. Planned for `app/services/llm.py`.

---

## Multi-Agentic Architecture

### Long-Term Memory Integration

> **Stubbed.** `mem0ai` dependency is declared in `pyproject.toml`, and `GraphState` includes a `long_term_memory` field. Integration with `app/utils/graph.py` is planned.

### Tool Calling Feature

> **Stubbed.** Directory exists at `app/core/langgraph/tools/`. No tool implementations yet.

---

## Building The API Gateway

### Auth Endpoints

> **Stubbed.** Schemas (`UserCreate`, `Token`, `UserResponse`) and utils (`create_tokens`, `verify_token`, `refresh_access_token`) are fully implemented but no routes are wired in `app/api/v1/`.

### Real-Time Streaming

> **Stubbed.** `StreamResponse` schema and SSE chunk format are defined. Streaming endpoints are planned but not yet implemented.

---

## Observability & Operational Testing

### Creating Metrics to Evaluate

- Prometheus and Grafana are configured in `docker-compose.yml` with provisioning directories (`prometheus/`, `grafana/`).
- `prometheus-client` is a declared dependency.
- No custom metrics or dashboards are defined yet.

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

## Quick Start

```bash
# 1. Clone and install dependencies
uv sync

# 2. Copy environment configuration
cp .env.example .env.dev
# Edit .env.dev with your API keys

# 3. Start infrastructure (PostgreSQL, Langfuse, Prometheus, Grafana)
docker-compose up -d

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

Built with FastAPI, LangChain/LangGraph, SQLModel, OpenRouter, Langfuse, Prometheus/Grafana.
