"""
01 - ADK Function Tool basics.

Run this file first. It does not call an LLM, so learners can inspect the
deterministic function outputs before wiring the tools into an Agent.
"""

from __future__ import annotations

try:
    from .tools import calculate_expression, explain_ai_topic, get_weather
except ImportError:
    from tools import calculate_expression, explain_ai_topic, get_weather


def main() -> None:
    """Run local tool examples without calling an LLM."""

    print("天气工具:", get_weather("北京"))
    print("术语解释:", explain_ai_topic("adk"))
    print("安全计算:", calculate_expression("(15 + 25) * 3"))


if __name__ == "__main__":
    main()
