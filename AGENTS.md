# AGENTS.md — prod-agentic-practice

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, invoke the `skill` tool with `skill: "graphify"` before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).


## Behavioral Guidelines

### 1. Think Before Coding
- State assumptions explicitly; if uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First
- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

### 3. Surgical Changes
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- Remove imports/variables/functions YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

### 4. Goal-Driven Execution
- Transform tasks into verifiable goals: "Write test → make pass → verify no regressions".
- For multi-step tasks, state a brief plan with verify steps:
  ```
  1. [Step] → verify: [check]
  2. [Step] → verify: [check]
  ```
- Every changed line should trace directly to the user's request.

**Tradeoff:** These bias toward caution over speed. For trivial fixes, use judgment.

---

## Project Setup

```bash
uv sync                        # install all deps
uv sync --group dev            # lint/format tools
uv sync --group test           # pytest + httpx
```

Python 3.13 only (`.python-version`). Use `uv`, not pip.

## Serve

```bash
docker-compose up -d                   # core stack: db + app + prometheus + grafana + cadvisor
uvicorn app.main:app --reload          # app only (port 8000, requires external db)
python main.py                         # CLI demo only (no server)
python examples/logging_demo.py        # logging demo
```

- Grafana: `localhost:3001` (admin/admin)
- cAdvisor: `:8080`
- Langfuse is **external** — run separately (local background or cloud). Configure via `LANGFUSE_*` env vars.
- `start.sh` is **deprecated** — use `docker-compose up -d` instead.

## Test / Lint

```bash
pytest                               # run all
ruff check app/ && ruff format --check app/
black --check app/ && isort --check-only app/
```

No pytest config or conftest.py exists — tests need `pytest-asyncio` for async. No type checker or Alembic configured.

## Architecture

- **`app/main.py`** — FastAPI app with lifespan, CORS, structlog middleware, `/health`, `/`, 3 demo endpoints. **No `include_router` calls** — routes defined in submodules are NOT registered.
- **`app/api/v1/auth.py`** — 4 fully implemented endpoints (`POST /register`, `POST /login`, `POST /session`, `GET /sessions`) + dependencies (`get_current_user`, `get_current_session`)
- **`app/services/database.py`** — `DatabaseService` singleton: `create_user`, `get_user_by_email`, `get_user_by_id`, `create_session`, `get_session(session_id: str)`, `get_user_sessions`
- **`app/models/`** — SQLModel: `User` (int PK), `Session` (str PK — UUID), `Thread` (str PK). `database.py` re-exports all three. `BaseModel` provides `created_at`.
- **`app/schemas/`** — Pydantic: `auth.py` (`UserCreate`, `Token`, `UserResponse`, `SessionResponse`, `TokenResponse`), `chat.py` (`Message`, `ChatRequest`, `ChatResponse`, `StreamResponse`), `graph.py` (`GraphState`)
- **`app/utils/auth.py`** — asymmetric JWT (RS256) with RSA key pair in `security/jwt_*.pem`. Token functions:
  - `create_access_token(subject, data, expire_minutes) -> Token` — `refresh_token=""`
  - `create_refresh_token(subject, data, expire_days) -> Token` — `access_token=""`
  - `create_tokens(subject, data, ...) -> Token` — delegates to both above
  - `refresh_access_token(refresh_token) -> Token` — verified refresh → new access
- **`app/utils/sanitization.py`** — `sanitize_string`, `sanitize_email`
- **`app/core/logging.py`** — structlog: colorful console (dev) / JSON (prod); `configure_logging()` fires on import
- **`app/core/config.py`** — Pydantic Settings loads first-found: `.env.dev` > `.env.stage` > `.env.prod` > `.env.local` > `.env`
- **`app/core/langfuse.py`** — Langfuse client init, `CallbackHandler` factory
- **`app/core/langgraph/graph.py`** — `LangGraphAgent`: StateGraph, Postgres checkpointer, mem0ai long-term memory, Langfuse tracing
- **`app/core/langgraph/duckduckgosearch.py`** — DuckDuckGo search via `langchain_community`
- **`app/core/prompts/`** — system prompt template with `{variable}` injection via `load_system_prompt()`
- **`app/services/llm.py`** — `LLMRegistry` + `LLMService` (ChatOpenAI, tenacity retry + model fallback)

Stub directories (empty): `scripts/`, `evals/`. No Grafana dashboards or Prometheus configs exist yet. No streaming endpoints implemented yet.

## Auth Routes — Key Details

| Endpoint | Auth | Token function | Response model |
|---|---|---|---|
| `POST /register` | None | `create_tokens(...)` | `UserResponse(token=Token(access+refresh))` |
| `POST /login` | None | `create_tokens(...)` | `TokenResponse(token=Token(access+refresh))` |
| `POST /session` | `get_current_user` | `create_access_token(...)` | `SessionResponse(token=Token(access, refresh=""))` |
| `GET /sessions` | `get_current_user` | `create_access_token(...)` | `List[SessionResponse]` |

- Session tokens use `create_access_token` — `refresh_token` is empty string in response
- Password: zxcvbn score ≥ 3 via `UserCreate` validator; bcrypt via `User.hash_password()` / `verify_password()`
- Registration returns full `Token` (auto-login on signup)

## Gotchas

- **Auth router is NOT registered** in `app/main.py`. No `include_router` call exists anywhere. Routes won't respond until added.
- `Session.id` and `Thread.id` are `str` (UUID), not int.
- JWT keys (`security/jwt_private.pem`, `security/jwt_public.pem`) must exist before any token operation. Generate them if missing.
- `.env.dev` is gitignored.
- `ALLOWED_ORIGINS` accepts JSON arrays or comma-separated strings.
- `docker-compose down -v` deletes all volumes (PostgreSQL data, Grafana).
- `start.sh` is **deprecated** — use `docker-compose up -d`.
- Rate-limit decorators (`@limiter.limit`) require a `request: Request` parameter in the handler.

