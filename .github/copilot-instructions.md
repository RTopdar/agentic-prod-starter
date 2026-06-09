# Copilot Instructions for Agentic Production System

This document provides essential context for working effectively in this production-grade agentic system repository.

## Project Overview

This is a **production-grade agentic system** built with FastAPI, PostgreSQL, and comprehensive observability tooling. The system is designed to understand and implement layers of production systems including authentication, observability, monitoring, and rate limiting.

## Build, Test, and Lint Commands

### Environment Setup
```bash
# Install dependencies using uv (preferred)
uv sync

# Alternative using pip
pip install -e ".[dev,test]"

# Set up environment variables
cp .env.example .env.dev
# Edit .env.dev with your configuration
```

### Development Server
```bash
# Start all services (PostgreSQL, FastAPI, Prometheus, Grafana, cAdvisor)
docker-compose up -d

# Check service health
docker-compose ps

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

### Testing
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run a specific test file
pytest path/to/test_file.py

# Run a specific test
pytest path/to/test_file.py::test_function_name
```

### Linting and Code Quality
```bash
# Format code with black
black app/

# Sort imports with isort
isort app/

# Lint with ruff
ruff check app/
ruff format --check app/

# Type checking (if configured)
mypy app/

# Cyclomatic complexity analysis
radon cc app/
```

### Database Operations
```bash
# Apply migrations (when Alembic is added)
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"

# Reset database (development only)
docker-compose down -v
docker-compose up -d
```

## High-Level Architecture

### Core Components
1. **FastAPI Application** (`app/`) - Main application with modular structure:
   - `core/` - Configuration, middleware, shared utilities
   - `api/v1/` - API endpoints (currently empty, structure defined)
   - `models/` - SQLModel database models with PostgreSQL
   - `schemas/` - Pydantic schemas for request/validation
   - `services/` - Business logic layer
   - `utils/` - Shared utilities

2. **Observability Stack** - Built-in monitoring:
   - **Prometheus** - Metrics collection on port 9090
   - **Grafana** - Dashboards on port 3001 (admin/admin)
   - **cAdvisor** - Container metrics on port 8080
   - **Langfuse** - LLM tracing and analytics (external service, running in port 3000 for local development)

3. **Database** - PostgreSQL with pgvector extension for embedding storage

### Configuration Management
- Uses **Pydantic Settings** with environment-specific `.env` files
- Priority order: `.env.dev` → `.env.stage` → `.env.prod` → `.env.local` → `.env`
- Environment detection via `APP_ENV` variable
- Centralized configuration in `app/core/config.py`

### Security Implementation
- **Asymmetric JWT** with RSA keys (private/public key pairs)
- Rate limiting via **SlowAPI** with endpoint-specific limits
- CORS configured with explicit allowed origins
- Password hashing with **bcrypt**

## Key Conventions

### Code Organization
1. **Database Models** (`app/models/`) - Use SQLModel with type annotations
2. **Pydantic Schemas** (`app/schemas/`) - Separate from models for API validation
3. **Service Layer** (`app/services/`) - Business logic, database operations
4. **API Routes** (`app/api/v1/`) - FastAPI endpoints, minimal logic

### Environment Handling
- Always use `settings` from `app.core.config` for configuration
- Environment-specific behavior via `settings.environment` (Enum: DEVELOPMENT, STAGING, PRODUCTION, TEST)
- Development mode enables debug features, production enforces security

### Logging and Monitoring
- Structured logging with **structlog**
- Metrics exposed at `/metrics` endpoint via **prometheus-client**
- LLM operations traced with **Langfuse** integration
- Container-level monitoring with **cAdvisor**

### Docker Development
- Multi-service setup with `docker-compose.yml`
- Health checks for all services
- Volume mounting for hot-reload during development
- Persistent data volumes for PostgreSQL and Grafana

### API Design
- Versioned API paths (`/api/v1/`)
- Rate limiting configured per endpoint type
- JWT authentication for protected routes
- OpenAPI documentation automatically generated at `/docs`

### Error Handling
- Centralized exception handling middleware
- Structured error responses
- Appropriate HTTP status codes
- Log errors with context for debugging

## Development Workflow

1. **Local Setup**: Copy `.env.example` to `.env.dev` and configure
2. **Start Services**: `docker-compose up -d`
3. **Run Tests**: `pytest` to verify changes
4. **Code Quality**: Run `black`, `isort`, `ruff` before committing
5. **Database Changes**: Use Alembic migrations (to be implemented)
6. **Monitoring**: Check Grafana at http://localhost:3001 for metrics

## Important Notes

- **JWT Keys**: Generate RSA key pairs in `security/` directory before first run
- **Langfuse**: Requires external account setup for LLM tracing
- **OpenRouter**: Configure API key for LLM model access
- **Production**: Change `DEBUG=false` and restrict `ALLOWED_ORIGINS`
- **Database**: Uses pgvector for potential embedding/vector search functionality

## Project Dependencies

Key production dependencies:
- **FastAPI** - Web framework with async support
- **SQLModel** - SQL database models with Pydantic
- **Langchain** - LLM framework integration
- **LangGraph** - Agent orchestration
- **Prometheus-client** - Metrics export
- **SlowAPI** - Rate limiting middleware
- **Structlog** - Structured logging