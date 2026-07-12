"""
Google ADK 2.x Agent example.

ADK CLI looks for a module-level variable named ``root_agent`` in this file.
Run it from the repository root with:

    uv run adk run tests/t06_adk
"""

from __future__ import annotations

from google.adk.agents import Agent

try:
    from .runtime import create_minimax_model
    from .tools import calculate_expression, explain_ai_topic, get_weather
except ImportError:
    from runtime import create_minimax_model
    from tools import calculate_expression, explain_ai_topic, get_weather


study_planner_agent = Agent(
    name="adk_study_planner",
    model=create_minimax_model(),
    description="Creates short learning plans for Google ADK learners.",
    instruction=(
        "你是 ADK 学习规划助手。根据用户目标输出 3-5 步学习计划，"
        "优先覆盖 agent、tool、runner 和 CLI 运行方式。"
    ),
)


root_agent = Agent(
    name="adk_learning_agent",
    model=create_minimax_model(),
    description="A Google ADK 2.x learning agent with local function tools.",
    instruction=(
        "你是一个中文 AI 应用开发教学助手。"
        "当用户询问天气、数学计算或 ADK/Agent 概念时，优先调用可用工具。"
        "回答时说明你调用了哪个工具，以及工具返回了什么关键信息。"
        "如果用户要求制定学习路线，可以转交给 adk_study_planner。"
    ),
    tools=[get_weather, calculate_expression, explain_ai_topic],
    sub_agents=[study_planner_agent],
)
