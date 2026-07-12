"""
07 - Writing workflow demo.

This example builds a MiniMax-backed writing pipeline with ADK Workflow and
dynamic ``ctx.run_node(...)`` calls:

topic -> outline agent -> draft agent -> review agent -> revision agent.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from google.adk.agents import Agent
from google.adk.agents.context import Context
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.workflow import Workflow, node
from google.genai import types

try:
    from .runtime import create_minimax_model, has_minimax_model_config
    from .runtime import strip_thinking_blocks
except ImportError:
    project_root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(project_root))
    from tests.t06_adk.runtime import create_minimax_model
    from tests.t06_adk.runtime import has_minimax_model_config
    from tests.t06_adk.runtime import strip_thinking_blocks


APP_NAME = "dreams_ai_adk_writing_workflow_demo"
USER_ID = "writing_workflow_user"


outline_agent = Agent(
    name="writing_outline_agent",
    model=create_minimax_model(),
    description="Creates a concise Chinese article outline.",
    mode="single_turn",
    instruction=(
        "你是中文写作策划。根据主题输出文章大纲。"
        "只输出 4-6 个小节标题，每个标题后用一句话说明要点。"
    ),
)


draft_agent = Agent(
    name="writing_draft_agent",
    model=create_minimax_model(),
    description="Writes a first draft from an outline.",
    mode="single_turn",
    instruction=(
        "你是中文技术写作者。根据主题和大纲写一版短文草稿。"
        "结构清楚，控制在 500 字以内，不要输出思考过程。"
    ),
)


review_agent = Agent(
    name="writing_review_agent",
    model=create_minimax_model(),
    description="Reviews a draft and returns actionable revision notes.",
    mode="single_turn",
    instruction=(
        "你是严格的中文编辑。只评审草稿，不重写全文。"
        "输出 3-5 条具体修改建议，覆盖结构、清晰度和读者价值。"
    ),
)


revision_agent = Agent(
    name="writing_revision_agent",
    model=create_minimax_model(),
    description="Revises a draft using editor feedback.",
    mode="single_turn",
    instruction=(
        "你是中文改稿助手。根据原稿和编辑建议输出最终稿。"
        "保留有价值内容，修正结构和表达，不要输出思考过程。"
    ),
)


def _clean_agent_text(output: object) -> str:
    """Normalize model output before passing it to the next writing step."""

    return strip_thinking_blocks(str(output or "")).strip()


@node(rerun_on_resume=True)
async def writing_director(ctx: Context, node_input: str) -> str:
    """Coordinate outline, draft, review, and revision agents dynamically."""

    topic = node_input.strip()
    outline = _clean_agent_text(
        await ctx.run_node(
            outline_agent,
            f"写作主题：{topic}",
            run_id="writing_outline",
            use_sub_branch=True,
        )
    )
    draft = _clean_agent_text(
        await ctx.run_node(
            draft_agent,
            f"写作主题：{topic}\n\n文章大纲：\n{outline}",
            run_id="writing_draft",
            use_sub_branch=True,
        )
    )
    review = _clean_agent_text(
        await ctx.run_node(
            review_agent,
            f"写作主题：{topic}\n\n草稿：\n{draft}",
            run_id="writing_review",
            use_sub_branch=True,
        )
    )
    final_article = _clean_agent_text(
        await ctx.run_node(
            revision_agent,
            f"写作主题：{topic}\n\n草稿：\n{draft}\n\n编辑建议：\n{review}",
            run_id="writing_revision",
            use_sub_branch=True,
        )
    )

    return "\n\n".join(
        [
            "写作工作流完成：",
            "## 大纲",
            outline,
            "## 编辑建议",
            review,
            "## 最终稿",
            final_article,
        ]
    )


writing_workflow = Workflow(
    name="adk_writing_workflow",
    description="A MiniMax-backed writing workflow demo.",
    edges=[("START", writing_director)],
)


async def run_writing_workflow(topic: str) -> str:
    """Run the writing workflow and return the final output."""

    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    runner = Runner(
        node=writing_workflow,
        app_name=APP_NAME,
        session_service=session_service,
    )
    message = types.Content(role="user", parts=[types.Part(text=topic)])

    final_output = ""
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message,
    ):
        if event.output is not None:
            text = _clean_agent_text(event.output)
            if text:
                print(f"{event.author}: {text}")
                final_output = text

    return final_output


async def main() -> None:
    if not has_minimax_model_config():
        print(
            "请先在根目录 .env 中设置 MINIMAX_API_KEY，再运行 MiniMax 写作工作流示例。"
        )
        return

    topic = "写一篇给 Python 初学者看的短文，说明 Google ADK 工作流适合什么场景。"
    final_output = await run_writing_workflow(topic)
    print("\nWriting workflow final output:")
    print(final_output)


if __name__ == "__main__":
    asyncio.run(main())
