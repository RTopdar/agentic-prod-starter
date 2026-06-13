from typing import Any

from langfuse.api import TraceWithDetails


def get_input_output(trace: TraceWithDetails) -> tuple[str, str]:
    input_text = _stringify(trace.input) if trace.input is not None else ""
    output_text = _stringify(trace.output) if trace.output is not None else ""
    return input_text, output_text


def _stringify(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return value.get("content", str(value))
    return str(value)
