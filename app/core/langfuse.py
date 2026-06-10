from langfuse import get_client as _get_client
from langfuse.langchain import CallbackHandler

from app.core.config import settings
from app.core.logging import logger

_handler: CallbackHandler | None = None


def get_callback_handler() -> CallbackHandler:
    global _handler
    if _handler is None:
        _handler = CallbackHandler()
    return _handler


def get_langfuse_client():
    return _get_client()


def init_langfuse() -> None:
    client = _get_client()
    try:
        if client.auth_check():
            logger.info("langfuse_initialized", host=settings.langfuse_base_url)
        else:
            logger.warning("langfuse_auth_failed", host=settings.langfuse_base_url)
    except Exception as e:
        logger.warning("langfuse_init_error", error=str(e))


def flush_langfuse() -> None:
    _get_client().flush()


def shutdown_langfuse() -> None:
    _get_client().shutdown()
