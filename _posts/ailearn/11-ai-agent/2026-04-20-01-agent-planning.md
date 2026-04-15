---
layout: post
title: "Agent规划系统 - ReAct与Plan-Execute"
date: 2026-04-20
categories: ailearn
tags: [AI, Agent, 规划, ReAct]
keywords: Agent规划, ReAct, Plan-Execute, 任务分解
description: 掌握Agent规划策略，实现复杂任务自动化
---

* content
{:toc}

> **前置知识**：需要先掌握 AI Agent基础
>
> **本文重点**：Agent规划框架与实现

---

## 一、规划策略概述

```
Agent规划策略：

1. ReAct (Reasoning + Acting)
   - 思考 → 行动 → 观察 → 循环
   - 适合交互式任务

2. Plan-and-Execute
   - 先制定完整计划
   - 再逐步执行
   - 适合复杂多步骤任务

3. Self-Reflection
   - 执行后反思
   - 持续改进
```

---

## 二、ReAct框架

### 2.1 ReAct循环

```python
from langchain.agents import create_react_agent
from langchain_openai import ChatOpenAI
from langchain.tools import Tool

# 定义工具
tools = [
    Tool(name="search", func=search_func, description="搜索信息"),
    Tool(name="calculate", func=calc_func, description="计算")
]

# ReAct提示模板
react_prompt = """
你需要回答问题。可以使用以下工具：

{tools}

使用格式：
Question: 输入问题
Thought: 思考该做什么
Action: 工具名称
Action Input: 工具输入
Observation: 工具输出
... (重复 Thought/Action/Observation)
Thought: 我知道最终答案了
Final Answer: 最终答案

Question: {input}
Thought: {agent_scratchpad}
"""

# 创建Agent
llm = ChatOpenAI(model="gpt-4")
agent = create_react_agent(llm, tools, react_prompt)
```

### 2.2 自定义ReAct Agent

```python
class ReActAgent:
    """自定义ReAct Agent"""
    
    def __init__(self, llm, tools, max_iterations=10):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.max_iterations = max_iterations
    
    def run(self, question):
        scratchpad = ""
        
        for _ in range(self.max_iterations):
            thought = self._think(question, scratchpad)
            scratchpad += f"\nThought: {thought}"
            
            if "Final Answer:" in thought:
                return self._extract_answer(thought)
            
            action, action_input = self._parse_action(thought)
            
            if action in self.tools:
                observation = self.tools[action].func(action_input)
                scratchpad += f"\nAction: {action}\nAction Input: {action_input}\nObservation: {observation}"
        
        return "达到最大迭代次数"
```

---

## 三、Plan-and-Execute

```python
from langchain_experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner
)

llm = ChatOpenAI(model="gpt-4")

# 创建规划器
planner = load_chat_planner(llm)

# 创建执行器
executor = load_agent_executor(llm, tools, verbose=True)

# 创建Plan-and-Execute Agent
agent = PlanAndExecute(
    planner=planner,
    executor=executor,
    verbose=True
)

# 执行复杂任务
result = agent.invoke("帮我研究Python异步编程的最佳实践并总结")
```

---

## 四、LangGraph工作流

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    current_step: str
    result: str

# 定义节点
def analyze(state):
    state["current_step"] = "analyze"
    return state

def plan(state):
    state["current_step"] = "plan"
    return state

def execute(state):
    state["current_step"] = "execute"
    return state

# 构建图
workflow = StateGraph(AgentState)
workflow.add_node("analyze", analyze)
workflow.add_node("plan", plan)
workflow.add_node("execute", execute)

workflow.set_entry_point("analyze")
workflow.add_edge("analyze", "plan")
workflow.add_edge("plan", "execute")
workflow.add_edge("execute", END)

# 编译运行
app = workflow.compile()
result = app.invoke({"messages": ["任务"], "current_step": "", "result": ""})
```

---

## 参考资源

> - [ReAct论文](https://arxiv.org/abs/2210.03629)
> - [LangGraph文档](https://langchain-ai.github.io/langgraph/)

---

**返回**：[AI Agent智能体]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-11-ai-agent %})

*最后更新: 2026年4月20日*