from typing import Any, Dict, List, Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from openai import (
    APIError,
    APIConnectionError,
    APITimeoutError,
    InternalServerError,
    RateLimitError,
)
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
            "name": f"{settings.openrouter_model}",
            "llm": ChatOpenAI(
                model=settings.openrouter_model,
                temperature=0.7,
                api_key=settings.openrouter_api_key,
                base_url=settings.openrouter_base_url,
            ),
        },
        {
            "name": f"{settings.openrouter_backup_model}",
            "llm": ChatOpenAI(
                model=settings.openrouter_backup_model,
                temperature=0.7,
                api_key=settings.openrouter_api_key,
                base_url=settings.openrouter_base_url,
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


# ==================================================
# LLM Service (The Resilience Layer)
# ==================================================


class LLMService:
    """
    Manages LLM calls with automatic retries and fallback logic.
    """

    def __init__(self):
        self._llm: Optional[BaseChatModel] = None
        self._current_model_index: int = 0

        # Initialize with the default model from settings
        try:
            self._llm = LLMRegistry.get(settings.openrouter_model)
            all_names = LLMRegistry.get_all_names()
            self._current_model_index = all_names.index(settings.openrouter_model)
        except ValueError:
            # Fallback safety
            self._llm = LLMRegistry.LLMS[0]["llm"]

    def _switch_to_next_model(self) -> bool:
        """
        Circular Fallback: Switches to the next available model in the registry.
        Returns True if successful.
        """
        try:
            next_index = (self._current_model_index + 1) % len(LLMRegistry.LLMS)
            next_model_entry = LLMRegistry.LLMS[next_index]

            logger.warning(
                "switching_model_fallback",
                old_index=self._current_model_index,
                new_model=next_model_entry["name"],
            )
            self._current_model_index = next_index
            self._llm = next_model_entry["llm"]
            return True
        except Exception as e:
            logger.error("model_switch_failed", error=str(e))
            return False

    # --------------------------------------------------
    # The Retry Decorator
    # --------------------------------------------------
    # This is the magic. If the function raises specific exceptions,
    # Tenacity will wait (exponentially) and try again.
    @retry(
        stop=stop_after_attempt(settings.max_llm_call_retries),  # Stop after N tries
        wait=wait_exponential(multiplier=1, min=2, max=10),  # Wait 2s, 4s, 8s...
        retry=retry_if_exception_type(
            (
                RateLimitError,
                APITimeoutError,
                APIConnectionError,
                InternalServerError,
                APIError,
            )
        ),
        before_sleep=before_sleep_log(logger, "WARNING"),  # Log before waiting
        reraise=True,
    )
    async def _call_with_retry(self, messages: List[BaseMessage]) -> BaseMessage:
        """Internal method that executes the actual API call."""
        if not self._llm:
            raise RuntimeError("LLM not initialized")
        return await self._llm.ainvoke(messages)

    async def call(self, messages: List[BaseMessage]) -> BaseMessage:
        """
        Public interface. Wraps the retry logic with a Fallback loop.
        If the primary model fails after exhausting retries, we switch to
        the next available model and try again.
        """
        total_models = len(LLMRegistry.LLMS)
        models_tried = 0

        while models_tried < total_models:
            current_model = LLMRegistry.LLMS[self._current_model_index]["name"]

            try:
                result = await self._call_with_retry(messages)
                return result

            except Exception as e:
                models_tried += 1
                logger.error(
                    "model_failed_exhausted_retries",
                    model=current_model,
                    error=str(e),
                )

                if models_tried >= total_models:
                    break

                self._switch_to_next_model()

        raise RuntimeError(
            "Failed to get response from any LLM after exhausting all options."
        )

    def get_llm(self) -> BaseChatModel:
        return self._llm

    def bind_tools(self, tools: List) -> "LLMService":
        """Bind tools to the current LLM instance."""
        if self._llm:
            self._llm = self._llm.bind_tools(tools)
        return self


# Create global instance
llm_service = LLMService()
