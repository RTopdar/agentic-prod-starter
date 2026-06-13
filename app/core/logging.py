"""
Structured logging configuration using structlog.

This module provides a comprehensive logging setup with:
- Colorful console output for development
- Structured JSON logs for production
- Request/response logging middleware
- Context binding for traceability
- Integration with FastAPI and async context
"""

import contextvars
import logging
import sys
import time
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4

import structlog
from structlog.types import EventDict, Processor

from app.core.config import settings

# ============================================================================
# Log Level Configuration
# ============================================================================
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


# ============================================================================
# Structlog Processors
# ============================================================================
def add_timestamp(_: Any, __: Any, event_dict: EventDict) -> EventDict:
    """Add ISO 8601 timestamp to log entries."""
    event_dict["timestamp"] = datetime.utcnow().isoformat()
    return event_dict


def add_log_level(_: Any, __: Any, event_dict: EventDict) -> EventDict:
    """Add log level to log entries."""
    event_dict["level"] = event_dict.get("level", "info").upper()
    return event_dict


def add_process_id(_: Any, __: Any, event_dict: EventDict) -> EventDict:
    """Add process ID to log entries."""
    event_dict["process_id"] = str(uuid4())[:8]
    return event_dict


def add_environment(_: Any, __: Any, event_dict: EventDict) -> EventDict:
    """Add environment information to log entries."""
    event_dict["environment"] = settings.environment.value
    return event_dict


def filter_log_level(_: Any, __: Any, event_dict: EventDict) -> EventDict:
    """Filter logs based on configured log level."""
    log_level = LOG_LEVELS.get(settings.log_level.upper(), logging.INFO)
    event_level = event_dict.get("level", "info").upper()

    # Convert event level to numeric
    event_level_num = LOG_LEVELS.get(event_level, logging.INFO)

    # Filter out logs below configured level
    if event_level_num < log_level:
        raise structlog.DropEvent

    return event_dict


def add_service_name(_: Any, __: Any, event_dict: EventDict) -> EventDict:
    """Add service name to log entries."""
    event_dict["service"] = settings.project_name
    return event_dict


def add_version(_: Any, __: Any, event_dict: EventDict) -> EventDict:
    """Add application version to log entries."""
    event_dict["version"] = settings.version
    return event_dict


# ============================================================================
# Logging Configuration
# ============================================================================
def configure_logging() -> None:
    """Configure structlog for colorful development logs or JSON production logs."""

    # Share config with stdlib logging so library logs are captured too
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=LOG_LEVELS.get(settings.log_level.upper(), logging.INFO),
    )

    # --- Processors shared across all environments ---
    shared_processors: list[Processor] = [
        structlog.stdlib.filter_by_level,
        add_timestamp,
        add_log_level,
        add_service_name,
        add_version,
        add_environment,
        add_request_context,
        filter_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    # --- Development: colourful console ---
    if settings.is_development:
        from structlog.dev import ConsoleRenderer

        processors = [
            *shared_processors,
            structlog.processors.ExceptionPrettyPrinter(),
            ConsoleRenderer(colors=True, force_colors=True),
        ]
    # --- Production / Staging: JSON ---
    else:
        processors = [
            *shared_processors,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Keep stdlib loggers in sync
    structlog.stdlib.recreate_defaults(
        log_level=LOG_LEVELS.get(settings.log_level.upper(), logging.INFO)
    )


# ============================================================================
# Logger Factory
# ============================================================================
def get_logger(name: Optional[str] = None) -> structlog.stdlib.BoundLogger:
    """Get a configured structlog logger.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured structlog logger
    """
    if name is None:
        name = "app"

    return structlog.get_logger(name)


# ============================================================================
# Context Management
# ============================================================================

# Thread-safe per-request context storage
_request_context: contextvars.ContextVar[Dict[str, Any]] = contextvars.ContextVar(
    "_request_context", default={}
)


def bind_context(**kwargs) -> None:
    """Bind key-value pairs to the current request context.

    All subsequent log calls within this request will include these key-value pairs.
    """
    current = _request_context.get()
    current.update(kwargs)
    _request_context.set(current)


def clear_context() -> None:
    """Clear the current request context entirely.

    Must be called at the end of each request to prevent context leaking
    between requests in async workers.
    """
    _request_context.set({})


def add_request_context(_: Any, __: Any, event_dict: EventDict) -> EventDict:
    """Structlog processor that merges request context into every log entry."""
    ctx = _request_context.get()
    if ctx:
        event_dict.update(ctx)
    return event_dict


class LogContext:
    """Context manager for adding context to logs."""

    def __init__(self, logger: structlog.stdlib.BoundLogger, **context):
        self.logger = logger
        self.context = context

    def __enter__(self):
        """Enter context and bind context variables."""
        self.logger = self.logger.bind(**self.context)
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context."""
        pass


def with_context(logger: structlog.stdlib.BoundLogger, **context) -> LogContext:
    """Create a log context with bound variables.

    Example:
        with logger.with_context(user_id=123, request_id="abc"):
            logger.info("Processing request")
    """
    return LogContext(logger, **context)


# ============================================================================
# Request/Response Logging Middleware
# ============================================================================
async def log_request_response(request, call_next):
    """FastAPI middleware for logging requests and responses."""
    logger = get_logger("http")

    # Generate request ID
    request_id = str(uuid4())

    # Log request
    start_time = time.time()

    with with_context(
        logger,
        request_id=request_id,
        method=request.method,
        url=str(request.url),
        client_host=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    ):
        logger.info(
            "Request received",
            path=request.url.path,
            query_params=dict(request.query_params),
        )

    # Process request
    response = await call_next(request)

    # Log response
    duration = time.time() - start_time

    with with_context(
        logger,
        request_id=request_id,
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        duration_ms=round(duration * 1000, 2),
    ):
        log_level = "info" if response.status_code < 400 else "warning"
        getattr(logger, log_level)(
            "Request completed",
            path=request.url.path,
        )

    return response


# ============================================================================
# Initialize logging on module import
# ============================================================================
configure_logging()

# Global logger instance
logger = get_logger("app")
