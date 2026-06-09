#!/usr/bin/env python3
"""
Main entry point for the production agentic system.

This module initializes the application and demonstrates
the structured logging system.
"""

from app.core.logging import logger
from app.core.config import settings


def main():
    """Initialize and run the application."""
    logger.info(
        "Starting production agentic system",
        project=settings.project_name,
        version=settings.version,
        environment=settings.environment.value,
        debug=settings.debug,
    )

    logger.debug(
        "Debug mode is enabled" if settings.debug else "Debug mode is disabled"
    )

    # Demonstrate different log levels
    logger.info("Application initialized successfully")
    logger.warning("This is a sample warning message")

    # Log with context
    logger.info(
        "System components loaded",
        components=["logging", "config", "database", "api"],
        status="ready",
    )

    print(f"\n✅ {settings.project_name} v{settings.version} is ready!")
    print(f"   Environment: {settings.environment.value}")
    print(f"   Log level: {settings.log_level}")
    print(f"   API base: {settings.api_v1_str}")
    print(
        f"   Database: {settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
    )

    # Example of structured logging in action
    logger.info(
        "System status report",
        metrics={
            "log_level": settings.log_level,
            "environment": settings.environment.value,
            "api_endpoints": 0,  # Will be populated when API routes are added
            "database_connected": False,  # Will be true when DB connection is established
        },
        health="initializing",
    )


if __name__ == "__main__":
    main()
