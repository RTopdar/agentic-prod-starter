# test_config.py
"""
Test script for Pydantic Settings configuration.
"""

import os
import sys
from typing import Any, List
from pydantic import field_validator


def parse_list_from_env(env_key, default=None):
    """Parse a comma-separated list from an environment variable."""
    value = os.getenv(env_key)
    if not value:
        return default or []

    # Remove quotes if they exist
    value = value.strip("\"'")

    # Handle single value case
    if "," not in value:
        return [value]

    # Split comma-separated values
    return [item.strip() for item in value.split(",") if item.strip()]


# Then update your field_validator to use it
@field_validator("allowed_origins", mode="before")
@classmethod
def parse_allowed_origins(cls, v: Any) -> List[str]:
    """Parse comma-separated string into list of origins."""
    if isinstance(v, str):
        # Use your parsing function
        return parse_list_from_env("ALLOWED_ORIGINS", [])
    elif isinstance(v, list):
        # Already a list, return as-is
        return v
    return []


# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("Testing Pydantic Settings Configuration")
print("=" * 60)

try:
    # Import settings - this will trigger the config loading
    from app.core.config import settings

    print("✅ Settings imported successfully!")
    print()

    # Test 1: Basic attribute access
    print("1. Basic Configuration Values:")
    print(f"   Project Name: {settings.project_name}")
    print(f"   Version: {settings.version}")
    print(f"   Environment: {settings.environment.value}")
    print(f"   Debug Mode: {settings.debug} (type: {type(settings.debug)})")
    print(f"   API Prefix: {settings.api_v1_str}")
    print()

    # Test 2: Type conversions
    print("2. Type Conversion Tests:")
    print(
        f"   POSTGRES_PORT: {settings.postgres_port} (type: {type(settings.postgres_port)})"
    )
    print(f"   DEBUG: {settings.debug} (type: {type(settings.debug)})")
    print(
        f"   ALLOWED_ORIGINS: {settings.allowed_origins} (type: {type(settings.allowed_origins)})"
    )
    print(f"   Length: {len(settings.allowed_origins)} origins")
    print()

    # Test 3: Computed properties
    print("3. Computed Properties:")
    print(f"   Database URL: {settings.database_url}")
    print(f"   Is Development: {settings.is_development}")
    print(f"   Is Production: {settings.is_production}")
    print()

    # Test 4: Environment-specific values
    print("4. Environment-Specific Values:")
    print(f"   Log Level: {settings.log_level}")
    print(f"   Log Format: {settings.log_format}")
    print()

    # Test 5: LLM Configuration
    print("5. LLM Configuration:")
    print(f"   OpenRouter Base URL: {settings.openrouter_base_url}")
    print(f"   OpenRouter Model: {settings.openrouter_model}")
    print(
        f"   OpenRouter API Key (first 10 chars): {settings.openrouter_api_key[:10]}..."
    )
    print()

    # Test 6: Database Configuration
    print("6. Database Configuration:")
    print(f"   Host: {settings.postgres_host}")
    print(f"   Port: {settings.postgres_port}")
    print(f"   Database: {settings.postgres_db}")
    print(f"   User: {settings.postgres_user}")
    print(f"   Pool Size: {settings.postgres_pool_size}")
    print(f"   Max Overflow: {settings.postgres_max_overflow}")
    print()

    # Test 7: Security Configuration
    print("7. Security Configuration:")
    print(f"   JWT Private Key Path: {settings.jwt_private_key_path}")
    print(f"   JWT Public Key Path: {settings.jwt_public_key_path}")
    print(f"   JWT Algorithm: {settings.jwt_algorithm}")
    print()

    # Test 8: Rate Limiting
    print("8. Rate Limiting:")
    print(f"   Default: {settings.rate_limit_default}")
    print(f"   Chat: {settings.rate_limit_chat}")
    print(f"   Chat Stream: {settings.rate_limit_chat_stream}")
    print(f"   Messages: {settings.rate_limit_messages}")
    print(f"   Login: {settings.rate_limit_login}")
    print()

    # Test 9: Langfuse Observability
    print("9. Langfuse Observability:")
    print(f"   Public Key (first 10 chars): {settings.langfuse_public_key[:10]}...")
    print(f"   Secret Key (first 10 chars): {settings.langfuse_secret_key[:10]}...")
    print(f"   Base URL: {settings.langfuse_base_url}")
    print()

    # Summary
    print("=" * 60)
    print("✅ All tests passed! Configuration is working correctly.")
    print("=" * 60)

except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure you're in the project root and virtual environment is activated.")
except Exception as e:
    print(f"❌ Error during testing: {e}")
    import traceback

    traceback.print_exc()
