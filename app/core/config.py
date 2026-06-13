# app/core/config.py
"""
Centralized application configuration using Pydantic Settings Management.

Loads environment variables from .env files with environment-specific overrides.
"""

import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from dotenv import load_dotenv
from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# ============================================================================
# Environment Types
# ============================================================================
class Environment(str, Enum):
    """Application environment types."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"


# ============================================================================
# Environment Loading Utilities
# ============================================================================
def get_environment() -> Environment:
    """Get the current environment from APP_ENV variable."""
    env_value = os.getenv("APP_ENV", "development").lower()
    match env_value:
        case "production" | "prod":
            return Environment.PRODUCTION
        case "staging" | "stage":
            return Environment.STAGING
        case "test":
            return Environment.TEST
        case _:
            return Environment.DEVELOPMENT


def load_env_file() -> Optional[str]:
    """Load environment variables from .env files with fixed priority order.

    Priority order (first found wins):
    1. .env.dev
    2. .env.stage
    3. .env.prod
    4. .env.local
    5. .env

    Note: APP_ENV environment variable still determines runtime environment
    for feature flags and other logic, but config values come from the
    first .env file found in the priority chain.
    """
    # Get base directory (project root)
    base_dir = Path(__file__).parent.parent.parent

    # Define env files in fixed priority order
    env_files = [
        base_dir / ".env.dev",
        base_dir / ".env.stage",
        base_dir / ".env.prod",
        base_dir / ".env.local",
        base_dir / ".env",
    ]

    # Load the first env file that exists
    for env_file in env_files:
        if env_file.exists():
            load_dotenv(dotenv_path=env_file, override=True)
            print(f"✅ Loaded environment from {env_file.name}")
            return str(env_file)

    print("⚠️  No .env file found, using environment variables only")
    return None


# Load environment file immediately
ENV_FILE = load_env_file()


# ============================================================================
# Pydantic Settings Configuration
# ============================================================================
class Settings(BaseSettings):
    """Centralized application configuration using Pydantic Settings."""

    # ------------------------------------------------------------------------
    # Application Basics
    # ------------------------------------------------------------------------
    app_env: str = Field(..., alias="APP_ENV")
    project_name: str = Field(..., alias="PROJECT_NAME")
    version: str = Field(..., alias="VERSION")
    debug: bool = Field(..., alias="DEBUG")
    api_v1_str: str = Field(..., alias="API_V1_STR")
    allowed_origins: List[str] = Field(..., alias="ALLOWED_ORIGINS")

    # ------------------------------------------------------------------------
    # Langfuse Observability
    # ------------------------------------------------------------------------
    langfuse_public_key: str = Field(..., alias="LANGFUSE_PUBLIC_KEY")
    langfuse_secret_key: str = Field(..., alias="LANGFUSE_SECRET_KEY")
    langfuse_base_url: str = Field(..., alias="LANGFUSE_BASE_URL")

    # ------------------------------------------------------------------------
    # OpenRouter LLM Configuration
    # ------------------------------------------------------------------------
    openrouter_base_url: str = Field(..., alias="OPENROUTER_BASE_URL")
    openrouter_api_key: str = Field(..., alias="OPENROUTER_API_KEY")
    openrouter_model: str = Field(..., alias="OPENROUTER_MODEL")
    openrouter_backup_model: str = Field(..., alias="OPENROUTER_BACKUP_MODEL")
    openrouter_embedding_model: str = Field(..., alias="OPENROUTER_EMBEDDING_MODEL")

    # ------------------------------------------------------------------------
    # JWT Security
    # ------------------------------------------------------------------------
    jwt_private_key_path: str = Field(..., alias="JWT_PRIVATE_KEY_PATH")
    jwt_public_key_path: str = Field(..., alias="JWT_PUBLIC_KEY_PATH")
    jwt_algorithm: str = Field(..., alias="JWT_ALGORITHM")

    # ------------------------------------------------------------------------
    # Access and Refresh Token Expiration
    # -------------------------------------------------------------------------
    access_token_expire_minutes: int = Field(..., alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(..., alias="REFRESH_TOKEN_EXPIRE_DAYS")

    # ------------------------------------------------------------------------
    # Database (PostgreSQL)
    # ------------------------------------------------------------------------
    postgres_host: str = Field(..., alias="POSTGRES_HOST")
    postgres_db: str = Field(..., alias="POSTGRES_DB")
    postgres_user: str = Field(..., alias="POSTGRES_USER")
    postgres_port: int = Field(..., alias="POSTGRES_PORT")
    postgres_password: str = Field(..., alias="POSTGRES_PASSWORD")
    postgres_pool_size: int = Field(..., alias="POSTGRES_POOL_SIZE")
    postgres_max_overflow: int = Field(..., alias="POSTGRES_MAX_OVERFLOW")

    # ------------------------------------------------------------------------
    # Rate Limiting (SlowAPI)
    # ------------------------------------------------------------------------
    rate_limit_default: str = Field(..., alias="RATE_LIMIT_DEFAULT")
    rate_limit_chat: str = Field(..., alias="RATE_LIMIT_CHAT")
    rate_limit_chat_stream: str = Field(..., alias="RATE_LIMIT_CHAT_STREAM")
    rate_limit_messages: str = Field(..., alias="RATE_LIMIT_MESSAGES")
    rate_limit_login: str = Field(..., alias="RATE_LIMIT_LOGIN")
    rate_limit_register: str = Field(..., alias="RATE_LIMIT_REGISTER")
    rate_limit: dict[str, str] = Field(default_factory=dict)

    # ------------------------------------------------------------------------
    # LLM Retry Configuration
    # ------------------------------------------------------------------------
    max_llm_call_retries: int = Field(..., alias="MAX_LLM_CALL_RETRIES")

    # ------------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------------
    log_level: str = Field(..., alias="LOG_LEVEL")
    log_format: str = Field(..., alias="LOG_FORMAT")

    # ------------------------------------------------------------------------
    # Computed Properties
    # ------------------------------------------------------------------------
    @property
    def environment(self) -> Environment:
        """Get the current environment as an Enum."""
        return get_environment()

    @property
    def database_url(self) -> str:
        """Generate PostgreSQL connection URL."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == Environment.DEVELOPMENT

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == Environment.PRODUCTION

    # ------------------------------------------------------------------------
    # Field Validators
    # ------------------------------------------------------------------------
    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v: Any) -> List[str]:
        """Parse comma-separated string into list of origins."""
        if isinstance(v, str):
            # Remove quotes if present
            v = v.strip("\"'")
            if "," in v:
                return [item.strip() for item in v.split(",") if item.strip()]
            return [v] if v else []
        elif isinstance(v, list):
            # Already a list, return as-is
            return v
        return []

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, v: Any) -> bool:
        """Parse debug flag from string to boolean."""
        if isinstance(v, str):
            return v.lower() in {"1", "true", "yes", "t"}
        return bool(v)

    @field_validator(
        "postgres_port",
        "postgres_pool_size",
        "postgres_max_overflow",
        "max_llm_call_retries",
        mode="before",
    )
    @classmethod
    def parse_ints(cls, v: Any) -> int:
        """Parse integer fields from string."""
        if isinstance(v, str):
            return int(v)
        return v

    @model_validator(mode="after")
    def assemble_rate_limit_dict(self) -> "Settings":
        self.rate_limit = {
            "default": self.rate_limit_default,
            "chat": self.rate_limit_chat,
            "chat_stream": self.rate_limit_chat_stream,
            "messages": self.rate_limit_messages,
            "login": self.rate_limit_login,
            "register": self.rate_limit_register,
        }
        return self

    # ------------------------------------------------------------------------
    # Pydantic Configuration
    # ------------------------------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=None,
        env_file_encoding="utf-8",
        case_sensitive=False,
        populate_by_name=True,
        extra="ignore",
        env_parse_json=False,
    )

    # ------------------------------------------------------------------------
    # Environment-Specific Settings Overrides
    # ------------------------------------------------------------------------
    def apply_environment_settings(self) -> None:
        """Apply environment-specific overrides after validation."""
        if self.is_development:
            # Development-specific settings
            self.debug = True
            # You could override other dev-specific settings here

        elif self.is_production:
            # Production-specific settings
            self.debug = False
            # Ensure production security even if .env is misconfigured
            if self.allowed_origins == ["*"]:
                self.allowed_origins = []  # Require explicit origins in production

    # ------------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------------
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.apply_environment_settings()


# ============================================================================
# Global Settings Instance
# ============================================================================
settings = Settings()

# Print loaded environment for debugging
print(f"✅ Configuration loaded for {settings.environment.value} environment")
print(f"Project: {settings.project_name} v{settings.version}")
print(f"Debug: {settings.debug}")
print(
    f"Database: {settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
)
