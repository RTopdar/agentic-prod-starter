from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.langfuse import (
    flush_langfuse,
    get_langfuse_client,
    init_langfuse,
    shutdown_langfuse,
)
from app.core.logging import logger, log_request_response
from app.core.metrics import setup_metrics
from app.core.middleware import LoggingContextMiddleware, MetricsMiddleware
from app.services.database import database_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle events."""
    logger.info(
        "application_startup",
        project_name=settings.project_name,
        version=settings.version,
        api_prefix=settings.api_v1_str,
        environment=settings.environment.value,
    )

    init_langfuse()

    yield

    logger.info("application_shutdown")
    flush_langfuse()
    shutdown_langfuse()


app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    description="Production-grade AI Agent API",
    openapi_url=f"{settings.api_v1_str}/openapi.json",
    lifespan=lifespan,
)

# 1. Prometheus metrics scrape endpoint
setup_metrics(app)

# 2. Logging context middleware (outermost — binds request context for everything inside)
app.add_middleware(LoggingContextMiddleware)

# 3. Custom metrics middleware (tracks latency and request count)
app.add_middleware(MetricsMiddleware)

# 4. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. API router
app.include_router(api_router, prefix=settings.api_v1_str)


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """Log all HTTP requests and responses."""
    return await log_request_response(request, call_next)


@app.middleware("http")
async def langfuse_tracing_middleware(request: Request, call_next):
    """Create a Langfuse trace for each HTTP request."""
    langfuse = get_langfuse_client()
    trace_name = f"{request.method} {request.url.path}"

    with langfuse.start_as_current_observation(
        as_type="span",
        name=trace_name,
        input={
            "method": request.method,
            "path": request.url.path,
            "query": dict(request.query_params),
        },
    ) as span:
        response = await call_next(request)
        span.update(
            output={
                "status_code": response.status_code,
            }
        )
        return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Capture HTTP errors with structured logging."""
    logger.bind(
        path=request.url.path,
        method=request.method,
        request_id=str(request.headers.get("x-request-id", "unknown")),
        client_ip=request.client.host if request.client else None,
    ).warning(
        "http_exception",
        status_code=exc.status_code,
        detail=exc.detail,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
        headers=exc.headers,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Format Pydantic validation errors into user-friendly JSON."""
    logger.bind(
        path=request.url.path,
        method=request.method,
        request_id=str(request.headers.get("x-request-id", "unknown")),
        client_ip=request.client.host if request.client else None,
    ).warning(
        "validation_error",
        errors=str(exc.errors()),
    )

    formatted_errors = []
    for error in exc.errors():
        loc = " -> ".join([str(p) for p in error["loc"] if p != "body"])
        formatted_errors.append({"field": loc, "message": error["msg"]})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error", "errors": formatted_errors},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Catch all unhandled exceptions."""
    logger.bind(
        path=request.url.path,
        method=request.method,
        request_id=str(request.headers.get("x-request-id", "unknown")),
        client_ip=request.client.host if request.client else None,
    ).exception(
        "unhandled_exception",
        error_type=type(exc).__name__,
        error_message=str(exc),
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred.",
        },
    )


@app.get("/")
async def root():
    """Root endpoint for basic connectivity tests."""
    logger.info("root_endpoint_called")
    return {
        "name": settings.project_name,
        "version": settings.version,
        "environment": settings.environment.value,
        "docs_url": "/docs",
    }


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Production health check — validates API and database connectivity."""
    db_healthy = await database_service.health_check()

    status_code = (
        status.HTTP_200_OK if db_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    )

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "healthy" if db_healthy else "degraded",
            "components": {
                "api": "healthy",
                "database": "healthy" if db_healthy else "unhealthy",
            },
            "timestamp": datetime.now().isoformat(),
        },
    )


if __name__ == "__main__":
    import uvicorn

    logger.info(
        "Starting FastAPI server",
        host="0.0.0.0",
        port=8000,
        reload=settings.is_development,
    )

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.is_development,
        log_config=None,
    )
