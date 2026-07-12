"""
08 - LoopAgent digital human workflow demo.

This example follows the ADK LoopAgent pattern:

script writer -> LoopAgent(reviewer, refiner) -> final presenter

The loop checks and revises a digital-human speaking script. The reviewer can
call the built-in ``exit_loop`` tool to stop the loop early when the script is
good enough. LoopAgent is a workflow agent API; ADK 2.x also recommends the
newer graph/dynamic Workflow APIs for production orchestration.
"""

from __future__ import annotations

import asyncio
import sys
import warnings
from pathlib import Path

from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import exit_loop
from google.genai import types

try:
    from .runtime import collect_text_from_event, create_minimax_model
    from .runtime import has_minimax_model_config, strip_thinking_blocks
except ImportError:
    project_root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(project_root))
    from tests.t06_adk.runtime import collect_text_from_event
    from tests.t06_adk.runtime import create_minimax_model
    from tests.t06_adk.runtime import has_minimax_model_config
    from tests.t06_adk.runtime import strip_thinking_blocks


APP_NAME = "dreams_ai_adk_loop_digital_human_demo"
USER_ID = "loop_digital_human_user"
STATE_SCRIPT = "digital_human_script"
STATE_REVIEW = "digital_human_review"
MAX_LOOP_ITERATIONS = 3

warnings.filterwarnings(
    "ignore",
    message="LoopAgent is deprecated*",
    category=DeprecationWarning,
)
warnings.filterwarnings(
    "ignore",
    message="SequentialAgent is deprecated*",
    category=DeprecationWarning,
)


script_writer_agent = Agent(
    name="digital_human_script_writer",
    model=create_minimax_model(),
    description="Creates the first digital-human speaking script.",
    instruction=(
        "你是数字人口播脚本策划。根据用户主题写第一版短脚本。"
        "脚本要适合虚拟数字人出镜，包含：开场钩子、主体讲解、镜头/动作提示、"
        "结尾行动号召。控制在 60-90 秒口播长度，不要输出思考过程。"
    ),
    output_key=STATE_SCRIPT,
)


digital_human_reviewer = Agent(
    name="digital_human_reviewer",
    model=create_minimax_model(),
    description="Checks whether the digital-human script is ready.",
    instruction=(
        "你是数字人视频导演，负责评审当前口播脚本。\n"
        f"当前脚本保存在状态 {{{STATE_SCRIPT}}}。\n\n"
        "合格标准：\n"
        "1. 开场 5 秒内有明确钩子。\n"
        "2. 语言口语化，适合数字人自然播报。\n"
        "3. 包含镜头、表情或动作提示。\n"
        "4. 结构完整，有开场、主体、结尾 CTA。\n"
        "5. 时长适合 60-90 秒短视频。\n\n"
        "如果全部合格，必须调用 exit_loop 工具提前结束循环，不要再输出普通文本。"
        "如果不合格，只输出 3-5 条具体修改建议，方便下一个 Agent 改稿。"
    ),
    tools=[exit_loop],
    output_key=STATE_REVIEW,
)


digital_human_refiner = Agent(
    name="digital_human_refiner",
    model=create_minimax_model(),
    description="Rewrites the digital-human script according to review notes.",
    instruction=(
        "你是数字人口播改稿助手。根据当前脚本和评审建议输出新版完整脚本。\n"
        f"当前脚本：{{{STATE_SCRIPT}}}\n\n"
        f"评审建议：{{{STATE_REVIEW}}}\n\n"
        "输出要求：只输出新版脚本；保留镜头/表情/动作提示；不要解释修改过程。"
    ),
    output_key=STATE_SCRIPT,
)


digital_human_loop = LoopAgent(
    name="digital_human_loop_agent",
    description="Loops over review and revision until the digital-human script is ready.",
    max_iterations=MAX_LOOP_ITERATIONS,
    sub_agents=[digital_human_reviewer, digital_human_refiner],
)


final_presenter_agent = Agent(
    name="digital_human_final_presenter",
    model=create_minimax_model(),
    description="Presents the final digital-human script.",
    instruction=(
        "你是数字人脚本交付助手。根据状态中的最终脚本输出交付结果。\n"
        f"最终脚本：{{{STATE_SCRIPT}}}\n\n"
        "输出格式：\n"
        "1. 用一句话说明循环工作流已经完成。\n"
        "2. 输出最终数字人口播脚本。\n"
        "3. 最后列出 2-3 条拍摄/生成数字人视频时的执行提示。"
    ),
)


digital_human_workflow = SequentialAgent(
    name="digital_human_loop_workflow",
    description="A SequentialAgent + LoopAgent workflow for digital-human scripts.",
    sub_agents=[
        script_writer_agent,
        digital_human_loop,
        final_presenter_agent,
    ],
)


async def run_digital_human_loop(topic: str) -> str:
    """Run the digital-human loop workflow and return the final text."""

    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    runner = Runner(
        agent=digital_human_workflow,
        app_name=APP_NAME,
        session_service=session_service,
    )
    message = types.Content(role="user", parts=[types.Part(text=topic)])

    final_text = ""
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message,
    ):
        text = strip_thinking_blocks(collect_text_from_event(event)).strip()
        if text:
            print(f"{event.author}: {text}\n")
            final_text = text

        for function_call in event.get_function_calls():
            print(f"Tool call: {function_call.name}({function_call.args})")
        for function_response in event.get_function_responses():
            print(
                f"Tool response: {function_response.name} -> "
                f"{function_response.response}"
            )

    return final_text


def assert_loop_agent_structure() -> None:
    """Check the teaching example structure without calling MiniMax."""

    assert digital_human_loop.max_iterations == MAX_LOOP_ITERATIONS
    assert [agent.name for agent in digital_human_loop.sub_agents] == [
        "digital_human_reviewer",
        "digital_human_refiner",
    ]
    assert digital_human_reviewer.tools == [exit_loop]
    assert digital_human_workflow.sub_agents[-1].name == "digital_human_final_presenter"


async def main() -> None:
    assert_loop_agent_structure()

    if not has_minimax_model_config():
        print(
            "请先在根目录 .env 中设置 MINIMAX_API_KEY，再运行 MiniMax LoopAgent 数字人示例。"
        )
        return

    topic = "为 Google ADK 初学者生成一段 60 秒数字人口播脚本，介绍 LoopAgent 的价值。"
    final_output = await run_digital_human_loop(topic)
    print("\nDigital human loop workflow final output:")
    print(final_output)


if __name__ == "__main__":
    asyncio.run(main())
