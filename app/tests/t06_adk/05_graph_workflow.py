"""
05 - Graph workflow demo.

This example uses ADK 2.x Workflow to build a deterministic graph:
START -> normalize_task -> weather/math fan-out -> JoinNode -> summarize.
It does not call an LLM, so it can be run without MiniMax credentials.
"""

from __future__ import annotations

import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.workflow import JoinNode, Workflow
from google.genai import types

try:
    from .tools import calculate_expression, get_weather
except ImportError:
    from tools import calculate_expression, get_weather


APP_NAME = "dreams_ai_adk_graph_demo"
USER_ID = "graph_user"


def normalize_task(node_input: str) -> dict[str, str]:
    """Extract stable demo inputs from the user request."""

    return {
        "request": node_input,
        "city": "北京",
        "expression": "(15 + 25) * 3",
    }


def weather_branch(node_input: dict[str, str]) -> dict[str, object]:
    """Run the weather branch of the graph."""

    return {
        "branch": "weather",
        "input": node_input["city"],
        "result": get_weather(node_input["city"]),
    }


def math_branch(node_input: dict[str, str]) -> dict[str, object]:
    """Run the calculation branch of the graph."""

    return {
        "branch": "math",
        "input": node_input["expression"],
        "result": calculate_expression(node_input["expression"]),
    }


def summarize_branches(node_input: dict[str, dict[str, object]]) -> str:
    """Summarize all joined branch outputs."""

    weather_result = node_input["weather_branch"]["result"]
    math_result = node_input["math_branch"]["result"]
    return "\n".join(
        [
            "图工作流完成：",
            f"- 天气分支：{weather_result}",
            f"- 计算分支：{math_result}",
        ]
    )


join_results = JoinNode(name="join_results")

graph_workflow = Workflow(
    name="adk_graph_workflow",
    description="A deterministic ADK graph workflow demo.",
    edges=[
        (
            "START",
            normalize_task,
            (weather_branch, math_branch),
            join_results,
            summarize_branches,
        )
    ],
    max_concurrency=2,
)


async def run_graph_workflow(query: str) -> str:
    """Run the workflow and return the last node output."""

    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    runner = Runner(
        node=graph_workflow,
        app_name=APP_NAME,
        session_service=session_service,
    )
    message = types.Content(role="user", parts=[types.Part(text=query)])

    final_output = ""
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message,
    ):
        if event.output is not None:
            print(f"{event.author}: {event.output}")
            final_output = str(event.output)

    return final_output


async def main() -> None:
    query = "请用图工作流查北京天气并计算 (15 + 25) * 3。"
    final_output = await run_graph_workflow(query)
    print("\nGraph workflow final output:")
    print(final_output)


if __name__ == "__main__":
    asyncio.run(main())
