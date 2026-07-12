"""
02 - Programmatic ADK Runner example.

This script shows how to call the same ``root_agent`` from Python code instead
of using ``adk run`` or ``adk web``.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

try:
    from .agent import root_agent
    from .runtime import collect_text_from_event, has_minimax_model_config
    from .runtime import print_tool_activity
except ImportError:
    project_root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(project_root))
    from tests.t06_adk.agent import root_agent
    from tests.t06_adk.runtime import collect_text_from_event
    from tests.t06_adk.runtime import has_minimax_model_config
    from tests.t06_adk.runtime import print_tool_activity


APP_NAME = "dreams_ai_adk_demo"
USER_ID = "local_user"


async def run_query(query: str) -> str:
    """Send a single query to root_agent and return the final text response."""

    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    message = types.Content(role="user", parts=[types.Part(text=query)])

    final_text_parts: list[str] = []
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message,
    ):
        print_tool_activity(event)

        if event.is_final_response() and event.content:
            final_text_parts.append(collect_text_from_event(event))

    return "\n".join(final_text_parts)


async def main() -> None:
    if not has_minimax_model_config():
        print(
            "请先在 .env 中设置 MINIMAX_API_KEY，再运行 MiniMax Agent 调用示例。"
        )
        return

    query = "请查询北京天气，再计算 (15 + 25) * 3，并解释 ADK 里的 tool。"
    response = await run_query(query)
    print("\nFinal response:")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
