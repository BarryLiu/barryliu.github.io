"""
03 - Agent team demo.

This example creates a coordinator agent with three focused sub-agents. The
coordinator decides which specialist should handle weather, calculation, and
ADK concept questions.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

try:
    from .runtime import collect_text_from_event, create_minimax_model
    from .runtime import has_minimax_model_config, print_tool_activity
    from .tools import calculate_expression, explain_ai_topic, get_weather
except ImportError:
    project_root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(project_root))
    from tests.t06_adk.runtime import collect_text_from_event, create_minimax_model
    from tests.t06_adk.runtime import has_minimax_model_config, print_tool_activity
    from tests.t06_adk.tools import calculate_expression, explain_ai_topic, get_weather


APP_NAME = "dreams_ai_adk_team_demo"
USER_ID = "team_user"


weather_agent = Agent(
    name="weather_agent",
    model=create_minimax_model(),
    description="Handles city weather lookup tasks.",
    instruction="你只处理天气查询。需要天气时调用 get_weather，并用中文简短回复。",
    tools=[get_weather],
)

calculator_agent = Agent(
    name="calculator_agent",
    model=create_minimax_model(),
    description="Handles arithmetic calculation tasks.",
    instruction="你只处理算术计算。需要计算时调用 calculate_expression，并解释结果。",
    tools=[calculate_expression],
)

concept_agent = Agent(
    name="concept_agent",
    model=create_minimax_model(),
    description="Explains ADK and AI application development concepts.",
    instruction="你只解释 ADK 和 Agent 概念。需要术语解释时调用 explain_ai_topic。",
    tools=[explain_ai_topic],
)

team_agent = Agent(
    name="adk_agent_team",
    model=create_minimax_model(),
    description="Coordinates a small ADK specialist agent team.",
    instruction=(
        "你是智能体团队协调员。把天气、计算、ADK 概念问题分别交给合适的子智能体，"
        "最后汇总成中文答案。"
    ),
    sub_agents=[weather_agent, calculator_agent, concept_agent],
)


async def run_team_query(query: str) -> str:
    """Run one query through the coordinator team agent."""

    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    runner = Runner(
        agent=team_agent,
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
        if event.author:
            print(f"Event author: {event.author}")
        print_tool_activity(event)
        if event.is_final_response() and event.content:
            final_text_parts.append(collect_text_from_event(event))

    return "\n".join(part for part in final_text_parts if part)


async def main() -> None:
    if not has_minimax_model_config():
        print("请先在根目录 .env 中设置 MINIMAX_API_KEY，再运行智能体团队示例。")
        return

    query = "请团队协作：查北京天气，计算 (15 + 25) * 3，并解释 ADK 的 agent。"
    response = await run_team_query(query)
    print("\nTeam final response:")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
