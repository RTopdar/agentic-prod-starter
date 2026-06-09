# app/openrouter_config.py
"""
OpenRouter configuration for OpenAI SDK and LangChain compatibility.

All values are loaded from environment variables via Pydantic Settings.
The same variables are defined in `.env.example` for reference.
"""

from app.core.config import settings

# OpenRouter connection settings
OPENROUTER_BASE_URL = (
    settings.openrouter_base_url
)  # e.g. "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = settings.openrouter_api_key  # your OpenRouter API key
OPENROUTER_MODEL = settings.openrouter_model  # e.g. "gpt-4o"

# Initialize the OpenAI SDK client to use OpenRouter as the backend
import openai

openai_client = openai.OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
)

# Export symbols for convenient importing
__all__ = [
    "openai_client",
    "OPENROUTER_BASE_URL",
    "OPENROUTER_API_KEY",
    "OPENROUTER_MODEL",
]
