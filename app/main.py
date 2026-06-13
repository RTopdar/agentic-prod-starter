#!/usr/bin/env python3
"""
FastAPI application entry point with structured logging.

This module creates the FastAPI application and integrates
the structured logging middleware.
"""

from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.langfuse import (
    get_langfuse_client,
    init_langfuse,
    flush_langfuse,
    shutdown_langfuse,
)
from app.core.logging import logger, log_request_response
from app.api.v1.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle events."""
    # Startup
    logger.info(
        "FastAPI application starting",
        environment=settings.environment.value,
        debug=settings.debug,
        allowed_origins=settings.allowed_origins,
    )

    init_langfuse()

    yield

    # Shutdown
    logger.info("FastAPI application shutting down")
    flush_langfuse()
    shutdown_langfuse()


# Create FastAPI application
app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    description="Production-grade agentic system with structured logging",
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(auth_router, prefix="/api/v1")


# Add structured logging middleware
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """Log all HTTP requests and responses."""
    return await log_request_response(request, call_next)


# Add Langfuse tracing middleware
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
    """Capture HTTP errors and emit structured logs."""
    logger.bind(
        path=request.url.path,
        method=request.method,
        request_id=str(request.headers.get("x-request-id", "unknown")),
        client_ip=request.client.host if request.client else None,
    ).warning(
        "HTTP exception raised",
        status_code=exc.status_code,
        detail=exc.detail,
        headers=exc.headers,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
        headers=exc.headers,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Capture validation errors with field context."""
    logger.bind(
        path=request.url.path,
        method=request.method,
        request_id=str(request.headers.get("x-request-id", "unknown")),
        client_ip=request.client.host if request.client else None,
    ).error(
        "Request validation failed",
        errors=exc.errors(),
        body=exc.model_dump() if hasattr(exc, "model_dump") else None,
    )
    return JSONResponse(
        status_code=422,
        content={"error": "Validation error", "detail": exc.errors()},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Capture all unhandled exceptions in one place."""
    logger.bind(
        path=request.url.path,
        method=request.method,
        request_id=str(request.headers.get("x-request-id", "unknown")),
        client_ip=request.client.host if request.client else None,
    ).exception(
        "Unhandled exception caught by FastAPI exception handler",
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


# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint with detailed logging."""
    logger.debug("Health check requested")

    health_data = {
        "status": "healthy",
        "service": settings.project_name,
        "version": settings.version,
        "environment": settings.environment.value,
    }

    logger.info("Health check completed", **health_data)
    return health_data


# Root endpoint
@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint with welcome message."""
    logger.info("Root endpoint accessed")

    return {
        "message": f"Welcome to {settings.project_name}",
        "version": settings.version,
        "environment": settings.environment.value,
        "docs": "/docs" if settings.is_development else None,
        "health": "/health",
    }


# Example protected endpoint
@app.get("/api/v1/status")
async def get_status(request: Request) -> Dict[str, Any]:
    """Example API endpoint with request context logging."""
    # Log with request context
    logger.info(
        "Status endpoint accessed",
        client_ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    return {
        "status": "operational",
        "timestamp": "2024-03-15T10:30:00Z",
        "metrics": {
            "uptime": "24h",
            "requests_processed": 1000,
            "error_rate": 0.01,
        },
    }


# Error handling example
@app.get("/api/v1/error-example")
async def error_example():
    """Example endpoint that demonstrates error logging."""
    try:
        # Simulate an error
        result = 1 / 0
        return {"result": result}
    except ZeroDivisionError as e:
        logger.exception(
            "Division by zero error occurred",
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=True,
        )
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "message": str(e)},
        )


# Log demonstration endpoint
@app.get("/api/v1/log-demo")
async def log_demo():
    """Endpoint to demonstrate different log levels."""
    logger.debug("Debug message - detailed information for developers")
    logger.info("Info message - general application flow")
    logger.warning("Warning message - potential issue detected")

    # Structured logging example
    logger.info(
        "Structured log example",
        user_id=123,
        action="log_demo",
        metadata={
            "endpoint": "/api/v1/log-demo",
            "timestamp": "2024-03-15T10:30:00Z",
        },
        tags=["demo", "logging", "structured"],
    )

    return {
        "message": "Log demonstration completed",
        "logs_generated": ["debug", "info", "warning", "structured"],
        "check_console": "View colorful logs in development mode",
    }


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
        log_config=None,  # Use our structlog configuration instead
    )
