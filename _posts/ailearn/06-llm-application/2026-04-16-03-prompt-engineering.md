---
layout: post
title: "Prompt Engineering - 提示词工程实战"
date: 2026-04-16
categories: ailearn
tags: [AI, Prompt, 提示词, 大模型]
keywords: Prompt Engineering, 提示词优化, Few-shot, Chain of Thought
description: 掌握提示词工程核心技术，提升大模型应用效果
---

* content
:{:toc}

> **前置知识**：需要先掌握 [大模型API应用]({{ site.baseurl }}{% post_url /ailearn/06-llm-application/2026-04-16-01-llm-api %})
>
> **本文重点**：提示词设计原则与高级技巧

---

## 一、Prompt Engineering概述

### 1.1 什么是Prompt Engineering

```
Prompt Engineering：设计和优化输入提示词的技术

目标：
├── 引导模型生成期望的输出
├── 提高输出的质量和一致性
├── 减少幻觉和错误
└── 解锁模型的潜在能力

重要性：
- 同样的模型，不同的Prompt效果差异巨大
- 好的Prompt = 更好的结果 + 更低的成本
```

### 1.2 Prompt基本结构

```python
"""
Prompt基本结构：

[系统角色设定] + [上下文/背景] + [任务描述] + [输出格式] + [示例(Few-shot)] + [用户输入]

示例：
"""

basic_prompt = """
【系统角色】
你是一位专业的Python开发工程师，擅长代码审查和优化。

【任务】
请审查以下代码，指出潜在问题并提供优化建议。

【输出格式】
1. 问题列表（按严重程度排序）
2. 优化建议
3. 优化后的代码

【代码】
{code}

请开始审查：
"""
```

---

## 二、基础技巧

### 2.1 角色设定

```python
# 角色1：专业专家
expert_prompt = """
你是一位有20年经验的资深{domain}专家。
请以专业、严谨的语气回答问题。
回答时引用相关的行业标准或最佳实践。
"""

# 角色2：教学助手
teacher_prompt = """
你是一位耐心的{subject}教师。
请用简单易懂的语言解释概念。
每个解释都配一个生活化的例子。
"""

# 角色3：代码助手
coder_prompt = """
你是一位全栈开发工程师。
代码风格遵循PEP8规范。
每个函数都添加类型注解和文档字符串。
"""
```

### 2.2 明确约束

```python
# 好的示例
good_prompt = """
请将以下英文翻译为中文。

要求：
1. 保持原文的专业术语
2. 使用正式书面语
3. 人名地名保留英文

原文：{text}
"""

# 避免
bad_prompt = """
把这段话翻译一下：{text}
"""
```

### 2.3 输出格式控制

```python
# JSON格式输出
json_prompt = """
请从以下文本中提取关键信息，以JSON格式输出：

输出格式：
{
    "人物": ["人物1", "人物2"],
    "地点": ["地点1"],
    "时间": "时间信息",
    "事件": "事件描述"
}

文本：{text}
"""

# Markdown表格输出
table_prompt = """
请对比以下两种方案的优劣，以Markdown表格形式输出：

| 维度 | 方案A | 方案B | 优胜方 |
|------|-------|-------|--------|
| 成本 | ... | ... | ... |
| 性能 | ... | ... | ... |
| 可维护性 | ... | ... | ... |
"""

# 分步骤输出
step_prompt = """
请按以下步骤分析问题：

Step 1: 问题理解
- 问题的核心是什么？

Step 2: 分析思路
- 需要考虑哪些因素？

Step 3: 解决方案
- 具体的解决步骤？

Step 4: 验证方法
- 如何验证方案有效？
"""
```

---

## 三、高级技巧

### 3.1 Few-Shot Learning

```python
# 标准Few-Shot
few_shot_prompt = """
请根据示例进行情感分类：

示例：
文本：这款手机电池续航很棒！
分类：正面

文本：服务态度太差了，不推荐。
分类：负面

文本：物流快，质量也不错。
分类：正面

请分类：
文本：{text}
分类：
"""

# 带解释的Few-Shot（更稳定）
explained_few_shot = """
请进行情感分类，并说明理由：

示例：
文本：这款手机电池续航很棒！
分析：用户明确表达了对电池续航的满意
分类：正面

文本：服务态度太差了，不推荐。
分析：用户对服务态度不满，并表示不推荐
分类：负面

请分析并分类：
文本：{text}
"""
```

### 3.2 Chain of Thought (CoT)

```python
# 标准CoT
cot_prompt = """
请一步步思考并回答问题。

问题：{question}

让我们一步步分析：
"""

# Zero-shot CoT（无需示例）
zero_shot_cot = """
{question}

请一步步思考并回答。
"""

# Self-Consistency CoT
self_consistency_prompt = """
问题：{question}

请用三种不同的思路来分析这个问题，然后综合得出结论。

思路1：
...

思路2：
...

思路3：
...

综合结论：
...
"""
```

### 3.3 Self-Ask

```python
self_ask_prompt = """
问题：{question}

在回答之前，先问自己以下问题来更好地理解问题：

需要知道什么信息才能回答这个问题？
- 子问题1：...
  - 答案：...
- 子问题2：...
  - 答案：...

现在我可以回答原始问题了：
答案：...
"""
```

### 3.4 Tree of Thoughts

```python
tot_prompt = """
问题：{question}

让我们用思维树的方法来分析：

状态评估：当前问题的状态是什么？

可能的思路（生成多个候选）：
1. 思路A：...
   - 优点：...
   - 缺点：...
   - 预期结果：...

2. 思路B：...
   - 优点：...
   - 缺点：...
   - 预期结果：...

3. 思路C：...
   - 优点：...
   - 缺点：...
   - 预期结果：...

选择最佳思路：思路X，因为...

执行该思路：
...
"""
```

---

## 四、特定任务Prompt

### 4.1 代码生成

```python
code_gen_prompt = """
请编写一个Python函数实现以下功能：

功能描述：{description}

要求：
1. 函数名使用snake_case命名
2. 添加类型注解
3. 添加详细的docstring
4. 包含参数校验
5. 处理边界情况
6. 提供使用示例

输出格式：
```python
def function_name(param: type) -> return_type:
    \"\"\"
    函数描述
    
    Args:
        param: 参数说明
    
    Returns:
        返回值说明
    
    Raises:
        可能的异常
    
    Example:
        >>> function_name(...)
        expected_output
    \"\"\"
    # 实现
    pass
```
"""
```

### 4.2 文档摘要

```python
summary_prompt = """
请为以下文档生成摘要：

原文档：
{document}

要求：
1. 摘要长度：200-300字
2. 包含关键信息：目的、方法、结果、结论
3. 使用简洁的学术语言

输出格式：
【摘要】
[摘要内容]

【关键词】
关键词1, 关键词2, 关键词3
"""
```

### 4.3 问答系统

```python
qa_prompt = """
你是一个专业的问答助手。请基于提供的上下文回答问题。

上下文：
{context}

问题：{question}

回答要求：
1. 仅基于上下文回答，不要编造信息
2. 如果上下文没有答案，请明确说明
3. 引用相关的上下文片段

回答格式：
答案：[你的回答]

来源：[引用的上下文片段]

置信度：高/中/低（基于上下文的相关性判断）
"""
```

### 4.4 数据分析

```python
data_analysis_prompt = """
你是一位数据分析专家。请分析以下数据：

数据：
{data}

分析维度：
1. 数据概览
   - 数据量、字段含义
   
2. 数据质量
   - 缺失值、异常值
   
3. 统计特征
   - 分布、趋势、异常
   
4. 业务洞察
   - 关键发现
   - 潜在问题
   
5. 建议措施
   - 优化建议

请以结构化的方式输出分析报告。
"""
```

---

## 五、Prompt优化策略

### 5.1 迭代优化流程

```python
"""
Prompt优化流程：

1. 定义目标
   - 明确期望的输出
   - 确定评估指标

2. 初版Prompt
   - 基于模板创建
   - 添加基本约束

3. 测试评估
   - 准备测试集
   - 记录问题案例

4. 分析失败
   - 识别失败模式
   - 定位问题原因

5. 优化改进
   - 添加约束/示例
   - 调整结构

6. 重复3-5直到满意
"""

# Prompt版本管理
prompt_versions = {
    "v1": "翻译以下文本：{text}",
    
    "v2": """请将以下英文文本翻译为中文。
要求使用正式书面语，保留专业术语。
原文：{text}""",
    
    "v3": """你是专业的翻译专家，擅长英中翻译。
请将以下英文翻译为中文：

要求：
1. 使用正式书面语
2. 专业术语保留英文并附中文注释
3. 保持原文的逻辑结构

原文：{text}
译文："""
}
```

### 5.2 常见问题与解决

```python
"""
常见问题及解决方案：

问题1：输出太长
解决：添加长度限制，使用分点输出

问题2：格式不一致
解决：提供明确的输出模板，使用Few-shot示例

问题3：幻觉问题
解决：要求引用来源，添加事实核查步骤

问题4：忽略指令
解决：将重要指令放在开头/结尾，重复强调

问题5：能力不足
解决：分解任务，多步处理
"""

# 示例：解决幻觉问题
anti_hallucination_prompt = """
请基于提供的上下文回答问题。

重要约束：
1. 仅使用上下文中的信息
2. 如果上下文没有答案，回复"上下文中没有相关信息"
3. 回答时标注信息来源段落

上下文：
{context}

问题：{question}

回答（请标注来源段落）：
"""
```

---

## 六、Prompt模板库

### 6.1 通用模板

```python
# 通用结构化模板
STRUCTURED_PROMPT = """
【角色设定】
你是一位{role}。

【任务目标】
{task}

【输出要求】
{requirements}

【输入内容】
{input}

【输出】
"""

# 代码审查模板
CODE_REVIEW_TEMPLATE = """
请审查以下{language}代码：

```{language}
{code}
```

审查维度：
1. 代码质量（可读性、规范性）
2. 潜在Bug（边界情况、异常处理）
3. 性能问题
4. 安全风险
5. 改进建议

请按以上维度逐项给出评审意见。
"""
```

### 6.2 使用LangChain管理Prompt

```python
from langchain.prompts import ChatPromptTemplate, FewShotPromptTemplate
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector

# 创建示例选择器
examples = [
    {"input": "开心", "output": "悲伤"},
    {"input": "高大", "output": "矮小"},
    {"input": "聪明", "output": "愚笨"},
]

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}")
])

# Few-shot模板
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="请给出以下词语的反义词：",
    suffix="输入：{input}\n输出：",
    input_variables=["input"]
)

# 使用
formatted = few_shot_prompt.format(input="快速")
print(formatted)
```

---

## 参考资源

> - [OpenAI Prompt指南](https://platform.openai.com/docs/guides/prompt-engineering) - 官方最佳实践
> - [Learn Prompting](https://learnprompting.org/) - 免费教程
> - [Prompt Engineering Guide](https://www.promptingguide.ai/) - 综合指南
> - [Awesome ChatGPT Prompts](https://github.com/f/awesome-chatgpt-prompts) - 示例库
> - [LangChain Prompts](https://python.langchain.com/docs/modules/model_io/prompts/) - 模板管理
> - [CoT论文](https://arxiv.org/abs/2201.11903) - Chain of Thought
> - [ToT论文](https://arxiv.org/abs/2305.10601) - Tree of Thoughts

---

**上一篇**：[大模型API应用]({{ site.baseurl }}{% post_url /ailearn/06-llm-application/2026-04-16-01-llm-api %})

**下一篇**：[模型微调实战]({{ site.baseurl }}{% post_url /ailearn/06-llm-application/2026-04-16-03-fine-tuning %})

**返回**：[大模型应用]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-06-llm-application %})

*最后更新: 2026年4月16日*
