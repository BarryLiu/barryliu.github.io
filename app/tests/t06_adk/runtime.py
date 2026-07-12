"""Shared runtime helpers for ADK examples."""

from __future__ import annotations

import os
from pathlib import Path

from google.adk.models.lite_llm import LiteLlm


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_root_env() -> None:
    """Load the repository root .env if python-dotenv is installed."""

    try:
        from dotenv import load_dotenv
    except ImportError:
        return

    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=False)


def has_minimax_model_config() -> bool:
    """Return whether MiniMax credentials are available."""

    load_root_env()
    return bool(os.getenv("MINIMAX_API_KEY"))


def create_minimax_model() -> LiteLlm:
    """Create a MiniMax OpenAI-compatible model for ADK."""

    load_root_env()
    model_name = os.getenv("MINIMAX_MODEL", "MiniMax-M2.7")
    base_url = os.getenv("MINIMAX_BASE_URL", "https://api.minimaxi.com/v1")
    api_key = os.getenv("MINIMAX_API_KEY", "")

    kwargs = {
        "model": f"openai/{model_name}",
        "base_url": base_url,
    }
    if api_key:
        kwargs["api_key"] = api_key

    return LiteLlm(**kwargs)


def collect_text_from_event(event) -> str:
    """Collect text parts from an ADK event."""

    if not event.content or not event.content.parts:
        return ""

    return "".join(part.text or "" for part in event.content.parts)


def strip_thinking_blocks(text: str) -> str:
    """Remove model reasoning blocks from display text."""

    output_parts: list[str] = []
    remaining = text
    while remaining:
        start = remaining.find("<think>")
        if start == -1:
            output_parts.append(remaining)
            break

        output_parts.append(remaining[:start])
        end = remaining.find("</think>", start)
        if end == -1:
            break

        remaining = remaining[end + len("</think>") :]

    return "".join(output_parts)


def print_tool_activity(event) -> None:
    """Print function tool calls and responses from an ADK event."""

    for function_call in event.get_function_calls():
        print(f"Tool call: {function_call.name}({function_call.args})")

    for function_response in event.get_function_responses():
        print(f"Tool response: {function_response.name} -> {function_response.response}")
