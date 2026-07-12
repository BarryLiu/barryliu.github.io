"""
04 - Streaming agent demo.

This example uses RunConfig(streaming_mode=StreamingMode.SSE) to print partial
text chunks while MiniMax is generating the response.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from google.adk.agents import Agent
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

try:
    from .runtime import collect_text_from_event, create_minimax_model
    from .runtime import has_minimax_model_config, strip_thinking_blocks
except ImportError:
    project_root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(project_root))
    from tests.t06_adk.runtime import collect_text_from_event, create_minimax_model
    from tests.t06_adk.runtime import has_minimax_model_config
    from tests.t06_adk.runtime import strip_thinking_blocks


APP_NAME = "dreams_ai_adk_streaming_demo"
USER_ID = "streaming_user"


streaming_agent = Agent(
    name="adk_streaming_agent",
    model=create_minimax_model(),
    description="Streams short Chinese ADK learning explanations.",
    instruction=(
        "你是 Google Agent Development Kit（ADK）流式输出演示助手。"
        "ADK 在这里只指 Google Agent Development Kit，不是 Azure Data Explorer。"
        "用中文分段、简洁地回答，方便观察流式文本块。不要输出推理过程。"
    ),
)


async def run_streaming_query(query: str) -> str:
    """Run a streaming query and print partial chunks."""

    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    runner = Runner(
        agent=streaming_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    message = types.Content(role="user", parts=[types.Part(text=query)])
    run_config = RunConfig(streaming_mode=StreamingMode.SSE)

    raw_text = ""
    displayed_text = ""
    final_text = ""
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message,
        run_config=run_config,
    ):
        text = collect_text_from_event(event)
        if event.partial and text:
            raw_text += text
            visible_text = strip_thinking_blocks(raw_text)
            chunk = visible_text[len(displayed_text) :]
            if chunk:
                print(chunk, end="", flush=True)
                displayed_text = visible_text
        elif event.is_final_response() and text:
            final_text = strip_thinking_blocks(text)

    if final_text and final_text != displayed_text:
        print(final_text)

    return final_text or displayed_text


async def main() -> None:
    if not has_minimax_model_config():
        print("请先在根目录 .env 中设置 MINIMAX_API_KEY，再运行流式智能体示例。")
        return

    query = "用三段话解释 ADK 里的流式输出适合什么场景。"
    await run_streaming_query(query)
    print("\n\nStreaming demo finished.")


if __name__ == "__main__":
    asyncio.run(main())
