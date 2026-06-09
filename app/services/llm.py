from typing import Any, Dict, List
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openrouter import ChatOpenRouter
from openai import APIError, APITimeoutError, OpenAIError, RateLimitError
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.core.config import settings
from app.core.logging import logger


class LLMRegistry:
    LLMS: List[Dict[str, Any]] = [
        {
            "name": "base",
            "llm": ChatOpenRouter(
                model=settings.openrouter_model,
                temperature=0.7,
                openai_api_key=settings.openrouter_api_key,
            ),
        },
        {
            "name": "backup",
            "llm": ChatOpenRouter(
                model=settings.openrouter_backup_model,
                temperature=0.7,
                openai_api_key=settings.openrouter_api_key,
            ),
        },
    ]

    @classmethod
    def get(cls, model_name: str) -> BaseChatModel:
        for entry in cls.LLMS:
            if entry["name"] == model_name:
                return entry["llm"]
        return cls.LLMS[0]["llm"]

    @classmethod
    def get_all_names(cls) -> List[str]:
        return [entry["name"] for entry in cls.LLMS]