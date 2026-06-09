#!/usr/bin/env python3
"""
Demonstration of the structured logging system.

This script shows how to use the structlog-based logging system
with colorful console output and structured context.
"""

import asyncio
import sys
from pathlib import Path

# Ensure project root is on sys.path so 'app' is importable
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.core.logging import logger, with_context
from app.core.config import settings


def demonstrate_basic_logging():
    """Demonstrate basic logging with different levels."""
    print("=" * 60)
    print("BASIC LOGGING DEMONSTRATION")
    print("=" * 60)

    logger.debug("This is a debug message - usually for developers")
    logger.info("This is an info message - general information")
    logger.warning("This is a warning message - something might be wrong")
    logger.error("This is an error message - something went wrong")
    logger.critical("This is a critical message - system is in trouble")

    print()


def demonstrate_context_logging():
    """Demonstrate logging with context binding."""
    print("=" * 60)
    print("CONTEXT LOGGING DEMONSTRATION")
    print("=" * 60)

    # Method 1: Direct binding
    logger.info("User logged in", user_id=123, username="john_doe", ip="192.168.1.1")

    # Method 2: Temporary binding with context manager
    with with_context(logger, request_id="req_123", endpoint="/api/v1/users"):
        logger.info("Processing request")
        logger.debug("Fetching user data from database", user_id=456)

        # Nested context
        with with_context(logger, database_query="SELECT * FROM users"):
            logger.info("Executing database query")

    # Back to original context
    logger.info("Request completed")

    print()


def demonstrate_structured_data():
    """Demonstrate logging with complex structured data."""
    print("=" * 60)
    print("STRUCTURED DATA LOGGING")
    print("=" * 60)

    user_data = {
        "id": 123,
        "name": "John Doe",
        "email": "john@example.com",
        "roles": ["admin", "user"],
        "metadata": {
            "created_at": "2024-01-01",
            "last_login": "2024-03-15",
        },
    }

    logger.info(
        "User data processed",
        user=user_data,
        processing_time_ms=45.2,
        success=True,
        tags=["authentication", "user_management"],
    )

    print()


async def demonstrate_request_logging():
    """Demonstrate simulated request/response logging."""
    print("=" * 60)
    print("REQUEST/RESPONSE LOGGING DEMONSTRATION")
    print("=" * 60)

    # Simulate a request
    class MockRequest:
        def __init__(self):
            self.method = "GET"
            self.client = type("obj", (object,), {"host": "192.168.1.100"})()
            self.headers = {"user-agent": "Mozilla/5.0"}
            self._query_params = {"page": "1", "limit": "10"}

        @property
        def url(self):
            return type(
                "obj",
                (object,),
                {
                    "path": "/api/v1/users",
                    "__str__": lambda self: "http://localhost:8000/api/v1/users",
                },
            )()

        @property
        def query_params(self):
            return self._query_params

    class MockResponse:
        def __init__(self):
            self.status_code = 200

    # Create mock objects
    request = MockRequest()
    response = MockResponse()

    # Log the request/response
    logger_http = logger.bind(component="http")

    with with_context(
        logger_http,
        request_id="req_789",
        method=request.method,
        url=str(request.url),
        client_host=request.client.host,
        user_agent=request.headers.get("user-agent"),
    ):
        logger_http.info(
            "Request received",
            path=request.url.path,
            query_params=dict(request.query_params),
        )

        # Simulate processing
        await asyncio.sleep(0.1)

        with with_context(
            logger_http,
            request_id="req_789",
            method=request.method,
            url=str(request.url),
            status_code=response.status_code,
            duration_ms=105.5,
        ):
            logger_http.info("Request completed")

    print()


def demonstrate_environment_specific_output():
    """Show how logging differs between environments."""
    print("=" * 60)
    print("ENVIRONMENT-SPECIFIC OUTPUT")
    print("=" * 60)

    print(f"Current environment: {settings.environment.value}")
    print(f"Log level: {settings.log_level}")
    print(f"Log format: {settings.log_format}")

    print("\nDevelopment environment features:")
    print("- Colorful console output")
    print("- Human-readable format")
    print("- Context shown as key-value pairs")

    print("\nProduction environment features:")
    print("- Structured JSON output")
    print("- Machine-readable format")
    print("- Suitable for log aggregation systems")

    print()


def main():
    """Run all logging demonstrations."""
    print("\n" + "=" * 60)
    print("STRUCTURED LOGGING SYSTEM DEMONSTRATION")
    print("=" * 60 + "\n")

    print(f"Project: {settings.project_name}")
    print(f"Version: {settings.version}")
    print(f"Environment: {settings.environment.value}\n")

    demonstrate_basic_logging()
    demonstrate_context_logging()
    demonstrate_structured_data()

    # Run async demonstration
    asyncio.run(demonstrate_request_logging())

    demonstrate_environment_specific_output()

    print("=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)

    # Final example showing real usage pattern
    print("\n" + "=" * 60)
    print("REAL-WORLD USAGE EXAMPLE")
    print("=" * 60)

    logger.info(
        "Application started successfully",
        features=[
            "Structured logging with structlog",
            "Colorful console output (development)",
            "JSON logging (production)",
            "Request/response middleware",
            "Context binding and management",
        ],
        dependencies=["structlog", "colorama"],
        status="ready",
    )


if __name__ == "__main__":
    main()
