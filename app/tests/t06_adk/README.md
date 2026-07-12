# Google ADK 2.x 学习包

本目录演示如何用 Google Agent Development Kit 2.x 构建 Python Agent 项目，并通过 uv 管理依赖。

## 文件说明

- `agent.py`：ADK CLI 入口，暴露 `root_agent`。
- `runtime.py`：公共运行配置，读取根目录 `.env` 并创建 MiniMax 模型。
- `tools.py`：公共函数工具组件，包括天气查询、术语解释和安全计算。
- `01_tools.py`：第一步，直接运行本地工具，不调用大模型。
- `02_run_agent.py`：第二步，使用 `Runner` 在 Python 代码中调用同一个 Agent。
- `03_agent_team.py`：第三步，演示 coordinator + specialist 的智能体团队。
- `04_streaming_agent.py`：第四步，演示 SSE 流式智能体输出。
- `05_graph_workflow.py`：第五步，演示 ADK 2.x 图工作流。
- `06_dynamic_workflow.py`：第六步，演示 `ctx.run_node(...)` 动态调度工作流。
- `07_writing_workflow.py`：第七步，演示 MiniMax 大纲、草稿、评审、改稿写作工作流。
- `08_loop_agent_digital_human.py`：第八步，演示 LoopAgent 数字人口播稿循环优化。

## 环境准备

项目依赖由根目录 `pyproject.toml` 管理：

```bash
uv sync
```

在根目录 `.env` 中填写或确认 MiniMax 配置：

```bash
MINIMAX_API_KEY=your_minimax_api_key_here
MINIMAX_BASE_URL=https://api.minimaxi.com/v1
MINIMAX_MODEL=MiniMax-M2.7
```

示例通过 ADK 的 `LiteLlm` 接入 MiniMax OpenAI 兼容接口，模型字符串为 `openai/MiniMax-M2.7`。

## 运行本地工具示例

这个命令不调用大模型，适合先理解工具输入输出：

```bash
uv run python tests/t06_adk/01_tools.py
```

## 使用 ADK CLI 运行 Agent

```bash
uv run adk run tests/t06_adk
```

启动 Web 调试界面：

```bash
#uv run adk web
uv run adk web tests
```

打开页面后选择 `t06_adk` 对应的 Agent。`adk web` 的参数是 agent 父目录，
不是单个 agent 目录。

## 在 Python 代码中调用 Agent

```bash
uv run python tests/t06_adk/02_run_agent.py
```

`02_run_agent.py` 使用 `InMemorySessionService` 创建会话，用 `Runner.run_async()` 发送用户消息，并打印工具调用、工具响应和最终回复。

## 智能体团队

```bash
uv run python tests/t06_adk/03_agent_team.py
```

`03_agent_team.py` 创建一个团队协调员，并把天气、计算、ADK 概念解释分别交给三个 specialist 子智能体。

## 流式智能体

```bash
uv run python tests/t06_adk/04_streaming_agent.py
```

`04_streaming_agent.py` 使用 `RunConfig(streaming_mode=StreamingMode.SSE)` 打印部分文本事件，适合观察 Web UI 或聊天应用中的流式输出。

## 图工作流

```bash
uv run python tests/t06_adk/05_graph_workflow.py
```

`05_graph_workflow.py` 使用 `Workflow`、fan-out 和 `JoinNode` 构建确定性的图执行流程，不调用大模型，也不需要 MiniMax Key。

## 动态工作流

```bash
uv run python tests/t06_adk/06_dynamic_workflow.py
```

`06_dynamic_workflow.py` 使用 `@node(rerun_on_resume=True)` 创建调度节点，
并在运行时通过 `ctx.run_node(...)` 选择天气、计算、概念解释等子节点。
这个示例不调用大模型，也不需要 MiniMax Key。

## 写作工作流

```bash
uv run python tests/t06_adk/07_writing_workflow.py
```

`07_writing_workflow.py` 使用 MiniMax 和四个 `single_turn` 写作 Agent，
按“大纲 -> 草稿 -> 评审 -> 改稿”的顺序生成最终稿。

## LoopAgent 数字人循环工作流

```bash
uv run python tests/t06_adk/08_loop_agent_digital_human.py
```

`08_loop_agent_digital_human.py` 使用 `SequentialAgent` 串起初稿、循环优化和最终交付。
中间的 `LoopAgent(max_iterations=3)` 会反复执行数字人导演评审和口播稿改稿；
评审 Agent 满足质量标准时会调用 ADK 内置 `exit_loop` 工具提前结束循环。
ADK 2.x 已提示这类 workflow agent 后续会让位给新版 `Workflow`，这里保留为文档学习案例。

## 学习重点

1. `root_agent` 是 ADK CLI 默认查找的入口变量。
2. 普通 Python 函数可以直接放入 `tools` 列表，由 ADK 转成可被模型调用的工具。
3. `Runner` 适合把 Agent 嵌入到自己的 Python 应用中。
4. `sub_agents` 可以把学习规划等职责拆给子 Agent。
5. `StreamingMode.SSE` 适合做打字机式输出。
6. `Workflow` 适合把确定性任务拆成图节点、分支和汇合节点。
7. `ctx.run_node(...)` 适合在工作流运行时动态决定下一步要跑哪些节点。
8. 写作工作流适合把创作拆成大纲、草稿、评审、改稿等可观测步骤。
9. `LoopAgent` 适合演示“评审 -> 修改 -> 再评审”的循环流程，并可通过 `exit_loop` 提前退出。

## 参考文档

- [ADK Python 快速开始](https://adk.wiki/get-started/python/)
- [ADK Function tools](https://adk.wiki/tools-custom/function-tools/)
- [ADK Agent team / collaboration](https://adk.wiki/workflows/collaboration/)
- [ADK Workflows](https://adk.wiki/workflows/)
- [ADK Loop agents](https://adk.wiki/agents/workflow-agents/loop-agents/)
