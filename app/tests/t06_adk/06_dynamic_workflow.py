"""
06 - Dynamic workflow demo.

This example uses one static workflow node as a runtime dispatcher. The
dispatcher chooses which child nodes to run with ``ctx.run_node(...)`` based on
the user request.

It does not call an LLM, so it can be run without MiniMax credentials.
"""

from __future__ import annotations

import asyncio
import re
import sys
from pathlib import Path
from typing import Any

from google.adk.agents.context import Context
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.workflow import Workflow, node
from google.genai import types

try:
    from .tools import calculate_expression, explain_ai_topic, get_weather
except ImportError:
    project_root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(project_root))
    from tests.t06_adk.tools import calculate_expression
    from tests.t06_adk.tools import explain_ai_topic
    from tests.t06_adk.tools import get_weather


APP_NAME = "dreams_ai_adk_dynamic_workflow_demo"
USER_ID = "dynamic_workflow_user"


def normalize_dynamic_request(node_input: str) -> dict[str, str]:
    """Normalize free-form text into stable demo fields."""

    city = "北京"
    for candidate in ["北京", "上海", "深圳", "杭州", "广州"]:
        if candidate in node_input:
            city = candidate
            break

    math_match = re.search(r"(?:计算|算)\s*([^，。,.]+)", node_input)
    if math_match:
        expression = math_match.group(1).strip()
    else:
        math_chunks = re.findall(
            r"(?:\([0-9+\-*/().\s]+\)|[0-9.]+)"
            r"(?:\s*[+\-*/]\s*(?:\([0-9+\-*/().\s]+\)|[0-9.]+))*",
            node_input,
        )
        expression = max(math_chunks, key=len).strip() if math_chunks else "(12 + 8) * 5"

    topic = "workflow" if "工作流" in node_input or "workflow" in node_input.lower() else "agent"
    return {
        "request": node_input,
        "city": city,
        "expression": expression,
        "topic": topic,
    }


def plan_dynamic_steps(node_input: dict[str, str]) -> dict[str, object]:
    """Choose workflow steps at runtime from the normalized request."""

    request = node_input["request"]
    lowered = request.lower()
    steps: list[dict[str, str]] = []

    if "天气" in request or "weather" in lowered:
        steps.append({"type": "weather", "city": node_input["city"]})
    if "计算" in request or "算" in request or any(op in request for op in "+-*/"):
        steps.append({"type": "calculation", "expression": node_input["expression"]})
    if "adk" in lowered or "agent" in lowered or "工作流" in request or "workflow" in lowered:
        steps.append({"type": "concept", "topic": node_input["topic"]})
    if not steps:
        steps.append({"type": "concept", "topic": "agent"})

    return {
        **node_input,
        "steps": steps,
    }


def run_weather_step(node_input: dict[str, str]) -> dict[str, object]:
    """Run the weather branch selected by the dynamic dispatcher."""

    return {
        "step": "weather",
        "input": node_input["city"],
        "result": get_weather(node_input["city"]),
    }


def run_calculation_step(node_input: dict[str, str]) -> dict[str, object]:
    """Run the calculation branch selected by the dynamic dispatcher."""

    return {
        "step": "calculation",
        "input": node_input["expression"],
        "result": calculate_expression(node_input["expression"]),
    }


def run_concept_step(node_input: dict[str, str]) -> dict[str, object]:
    """Run the concept explanation branch selected by the dynamic dispatcher."""

    return {
        "step": "concept",
        "input": node_input["topic"],
        "result": explain_ai_topic(node_input["topic"]),
    }


def merge_dynamic_outputs(node_input: dict[str, Any]) -> str:
    """Merge all dynamically selected child-node outputs."""

    plan = node_input["plan"]
    outputs = node_input["outputs"]
    selected_steps = ", ".join(step["type"] for step in plan["steps"])

    lines = [
        "动态工作流完成：",
        f"- 运行时选择步骤：{selected_steps}",
    ]
    for output in outputs:
        lines.append(f"- {output['step']}：{output['result']}")
    return "\n".join(lines)


STEP_NODES = {
    "weather": run_weather_step,
    "calculation": run_calculation_step,
    "concept": run_concept_step,
}


@node(rerun_on_resume=True)
async def dynamic_dispatcher(ctx: Context, node_input: str) -> str:
    """Dispatch runtime-selected child nodes with ctx.run_node."""

    normalized = await ctx.run_node(
        normalize_dynamic_request,
        node_input,
        run_id="dyn_normalize",
        use_sub_branch=True,
    )
    plan = await ctx.run_node(
        plan_dynamic_steps,
        normalized,
        run_id="dyn_plan",
        use_sub_branch=True,
    )

    outputs: list[dict[str, object]] = []
    for index, step in enumerate(plan["steps"], start=1):
        step_type = step["type"]
        result = await ctx.run_node(
            STEP_NODES[step_type],
            step,
            run_id=f"dyn_{step_type}_{index}",
            use_sub_branch=True,
        )
        outputs.append(result)

    return await ctx.run_node(
        merge_dynamic_outputs,
        {"plan": plan, "outputs": outputs},
        run_id="dyn_merge",
        use_sub_branch=True,
    )


dynamic_workflow = Workflow(
    name="adk_dynamic_workflow",
    description="A runtime-dispatched ADK workflow demo.",
    edges=[("START", dynamic_dispatcher)],
)


async def run_dynamic_workflow(query: str) -> str:
    """Run the dynamic workflow and return the final node output."""

    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    runner = Runner(
        node=dynamic_workflow,
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
    query = "请动态决定步骤：查北京天气，计算 (12 + 8) * 5，并解释 ADK workflow。"
    final_output = await run_dynamic_workflow(query)
    print("\nDynamic workflow final output:")
    print(final_output)


if __name__ == "__main__":
    asyncio.run(main())
