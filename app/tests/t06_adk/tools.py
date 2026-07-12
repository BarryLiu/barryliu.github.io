"""
ADK Function Tool examples.

These functions are intentionally deterministic so learners can understand tool
inputs and outputs before connecting the agent to an external service.
"""

from __future__ import annotations

import ast
import operator
from typing import Any


_WEATHER_DATA = {
    "北京": "晴，25°C，适合户外活动",
    "上海": "多云，28°C，湿度偏高",
    "深圳": "阵雨，30°C，建议携带雨具",
    "杭州": "晴，26°C，适合西湖散步",
}

_AI_TOPICS = {
    "adk": "Google Agent Development Kit，用于构建、运行和评估智能体应用。",
    "agent": "Agent 会结合模型、指令、工具和状态来完成用户任务。",
    "tool": "Tool 是 Agent 可调用的外部能力，可以是普通 Python 函数。",
    "runner": "Runner 负责把用户消息、会话和 Agent 执行流程串起来。",
    "workflow": "Workflow 用图节点、条件分支、汇合节点或动态调度来编排可观测任务流程。",
}

_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def get_weather(city: str) -> dict[str, str]:
    """Get sample weather for a Chinese city.

    Args:
        city: City name, for example "北京", "上海", "深圳", or "杭州".

    Returns:
        A dictionary containing status and weather report text.
    """

    report = _WEATHER_DATA.get(city)
    if report is None:
        return {
            "status": "error",
            "message": f"暂时没有 {city} 的天气数据，可以尝试北京、上海、深圳或杭州。",
        }

    return {"status": "success", "city": city, "report": report}


def explain_ai_topic(keyword: str) -> dict[str, str]:
    """Explain an AI or ADK learning keyword.

    Args:
        keyword: Topic keyword, for example "adk", "agent", "tool", "runner",
            or "workflow".

    Returns:
        A dictionary containing status, normalized keyword, and explanation.
    """

    normalized = keyword.strip().lower()
    explanation = _AI_TOPICS.get(normalized)
    if explanation is None:
        known_topics = "、".join(sorted(_AI_TOPICS))
        return {
            "status": "error",
            "message": f"暂时没有 {keyword} 的解释，可查询：{known_topics}。",
        }

    return {
        "status": "success",
        "keyword": normalized,
        "explanation": explanation,
    }


def calculate_expression(expression: str) -> dict[str, Any]:
    """Calculate a simple arithmetic expression safely.

    Args:
        expression: Arithmetic expression using numbers and +, -, *, /, //, %, **.

    Returns:
        A dictionary containing status and calculated result or error message.
    """

    try:
        syntax_tree = ast.parse(expression, mode="eval")
        result = _evaluate_node(syntax_tree)
    except Exception as exc:
        return {"status": "error", "message": f"无法计算表达式：{exc}"}

    return {"status": "success", "expression": expression, "result": result}


def _evaluate_node(node: ast.AST) -> int | float:
    if isinstance(node, ast.Expression):
        return _evaluate_node(node.body)

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp):
        operator_type = type(node.op)
        if operator_type not in _BINARY_OPERATORS:
            raise ValueError(f"不支持的运算符 {operator_type.__name__}")

        left = _evaluate_node(node.left)
        right = _evaluate_node(node.right)
        if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)) and right == 0:
            raise ZeroDivisionError("除数不能为 0")
        return _BINARY_OPERATORS[operator_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operator_type = type(node.op)
        if operator_type not in _UNARY_OPERATORS:
            raise ValueError(f"不支持的一元运算符 {operator_type.__name__}")

        return _UNARY_OPERATORS[operator_type](_evaluate_node(node.operand))

    raise ValueError("只支持数字和基础算术表达式")
