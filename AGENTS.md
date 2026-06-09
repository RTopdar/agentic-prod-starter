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
docker-compose up -d                   # full stack: db + app + langfuse + prometheus + grafana + cadvisor
uvicorn app.main:app --reload          # app only (port 8000, requires external db/langfuse)
python main.py                         # CLI demo only (no server)
python examples/logging_demo.py        # logging demo
```

- Grafana: `localhost:3001` (admin/admin)
- Langfuse UI: `localhost:3000` (admin / admin123)
- cAdvisor: `:8080`
- `start.sh` is **deprecated** — Langfuse is now bundled in docker-compose; run `docker-compose up -d` instead.

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
- **`app/schemas/`** — Pydantic: auth, chat, graph state
- **`app/utils/auth.py`** — asymmetric JWT (RS256) with RSA keys in `security/jwt_*.pem`
- **`app/openrouter_config.py`** — OpenAI SDK client pointed at OpenRouter

Stub directories (empty): `api/v1/`, `services/`, `scripts/`, `evals/`, `core/prompts/`, `core/langgraph/tools/`. No Grafana dashboards or Prometheus configs exist yet.

## Gotchas

- `.env.dev` is gitignored. `.env.example` had `LANGFUSE_HOST` but config uses `LANGFUSE_BASE_URL` — this is now fixed.
- `ALLOWED_ORIGINS` accepts JSON arrays or comma-separated strings.
- `start.sh` is **deprecated** — Langfuse is now bundled in docker-compose; run `docker-compose up -d` instead.
- `docker-compose down -v` deletes all volumes (PostgreSQL data, Grafana).