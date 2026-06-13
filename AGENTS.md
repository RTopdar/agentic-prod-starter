# AGENTS.md — prod-agentic-practice

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

**Note**: Check skills.md for examples if needed

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
- Langfuse is **external** — run it separately (local background or cloud). Configure via `LANGFUSE_*` env vars.
- `start.sh` is **deprecated** — use `docker-compose up -d` instead.

## Test / Lint

```bash
pytest                               # run all (no tests exist yet)
ruff check app/ && ruff format --check app/
black --check app/ && isort --check-only app/
```

No pytest config or conftest.py exists — tests need `pytest-asyncio` for async. No type checker or Alembic is configured.

## Architecture

- **`app/main.py`** — FastAPI app with lifespan, CORS, structlog middleware, `/health`, `/`, 3 demo endpoints
- **`main.py`** — standalone CLI script (not the server)
- **`app/core/config.py`** — Pydantic Settings loads first-found: `.env.dev` > `.env.stage` > `.env.prod` > `.env.local` > `.env`
- **`app/core/logging.py`** — structlog: colorful console (dev) / JSON (prod); `configure_logging()` fires on import
- **`app/core/limiter.py`** — SlowAPI rate limiter (IP-keyed)
- **`app/models/`** — SQLModel: `User`, `Session`, `Thread`. `database.py` re-exports all three.
- **`app/api/v1/auth.py`** — FastAPI dependencies: `get_current_user` (JWT → user lookup), `get_current_session` (session token → existence + ownership check)
- **`app/services/database.py`** — `DatabaseService` singleton: `create_user`, `get_user_by_email`, `get_user_by_id`, `create_session`, `get_session`, `get_user_sessions`
- **`app/schemas/`** — Pydantic: auth (zxcvbn password validation), chat, graph state
- **`app/utils/auth.py`** — asymmetric JWT (RS256) with RSA keys in `security/jwt_*.pem`
- **`app/utils/sanitization.py`** — `sanitize_string`, `sanitize_email`
- **`app/openrouter_config.py`** — OpenAI SDK client pointed at OpenRouter
- **`app/core/langfuse.py`** — Langfuse client init, auth check, flush/shutdown, and `CallbackHandler` factory
- **`app/core/langgraph/graph.py`** — `LangGraphAgent` with StateGraph, Postgres checkpointer (`AsyncPostgresSaver`), mem0ai long-term memory, and centralized Langfuse tracing (LLM generations via `CallbackHandler` + manual spans for memory ops and tool calls)
- **`app/core/langgraph/duckduckgosearch.py`** — DuckDuckGo search tool via `langchain_community`
- **`app/core/prompts/system.md`** — System prompt template with `{variable}` injection
- **`app/core/prompts/__init__.py`** — `load_system_prompt()` — loads markdown template and injects dynamic vars
- **`app/services/llm.py`** — `LLMRegistry` + `LLMService` (tenacity retry + model fallback, no Langfuse code)

Stub directories (empty): `scripts/`, `evals/`. No Grafana dashboards or Prometheus configs exist yet.

## Gotchas

- `.env.dev` is gitignored.
- `ALLOWED_ORIGINS` accepts JSON arrays or comma-separated strings.
- `start.sh` is **deprecated** — use `docker-compose up -d` instead.
- `docker-compose down -v` deletes all volumes (PostgreSQL data, Grafana).

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, invoke the `skill` tool with `skill: "graphify"` before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
