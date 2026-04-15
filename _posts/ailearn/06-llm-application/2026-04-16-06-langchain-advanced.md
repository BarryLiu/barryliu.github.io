---
layout: post
title: "LangChain高级应用 - 复杂工作流开发"
date: 2026-04-16
categories: ailearn
tags: [AI, LangChain, LCEL, Chain, 工作流]
keywords: LangChain, LCEL, Chain, Runnable, 工作流编排
description: 掌握LangChain高级特性，构建复杂的AI应用工作流
---

* content
{:toc}

> **前置知识**：需要先掌握 [大模型API应用]({{ site.baseurl }}{% post_url /ailearn/06-llm-application/2026-04-16-01-llm-api %})
>
> **本文重点**：LCEL、自定义Chain、工作流编排

---

## 一、LCEL (LangChain Expression Language)

### 1.1 LCEL基础

```python
"""
LCEL (LangChain Expression Language)
LangChain的表达式语言，用于组合组件

核心概念：
- Runnable: 可执行的组件
- | : 管道操作符，连接组件
- 自动处理输入输出
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

# 基本链
model = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_template("讲一个关于{topic}的笑话")
output_parser = StrOutputParser()

# 使用LCEL组合
chain = prompt | model | output_parser

# 执行
result = chain.invoke({"topic": "程序员"})
print(result)

# 批量执行
results = chain.batch([{"topic": "猫"}, {"topic": "狗"}])
for r in results:
    print(r)

# 流式输出
for chunk in chain.stream({"topic": "AI"}):
    print(chunk, end="", flush=True)
```

### 1.2 Runnable接口

```python
from langchain.schema.runnable import RunnableLambda, RunnableParallel, RunnablePassthrough

# RunnableLambda: 自定义函数
def parse_length(text):
    return {"text": text, "length": len(text)}

parse_runnable = RunnableLambda(parse_length)

# RunnablePassthrough: 透传输入
passthrough = RunnablePassthrough()

# RunnableParallel: 并行执行
parallel = RunnableParallel(
    original=RunnablePassthrough(),
    upper=lambda x: x.upper(),
    length=lambda x: len(x)
)

result = parallel.invoke("hello")
print(result)
# {'original': 'hello', 'upper': 'HELLO', 'length': 5}

# 组合使用
def analyze_text(text):
    prompt = ChatPromptTemplate.from_template(
        "分析这段文本的情感和主题：{text}"
    )
    chain = (
        {"text": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    return chain.invoke(text)
```

### 1.3 复杂链组合

```python
from langchain.schema.runnable import RunnableBranch

# 条件分支
branch = RunnableBranch(
    # (条件, 处理器)
    (lambda x: len(x) < 10, lambda x: f"短文本: {x}"),
    (lambda x: len(x) < 50, lambda x: f"中等文本: {x}"),
    # 默认处理器
    lambda x: f"长文本: {x[:50]}..."
)

# 带检索的RAG链
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# 创建向量存储
vectorstore = Chroma.from_texts(
    ["AI是人工智能的缩写", "机器学习是AI的子领域"],
    embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()

# 构建RAG链
template = """基于以下上下文回答问题：
{context}

问题：{question}
"""

prompt = ChatPromptTemplate.from_template(template)

rag_chain = (
    {
        "context": retriever | (lambda docs: "\n".join(doc.page_content for doc in docs)),
        "question": RunnablePassthrough()
    }
    | prompt
    | model
    | StrOutputParser()
)

# 执行
answer = rag_chain.invoke("什么是AI？")
print(answer)
```

---

## 二、自定义组件

### 2.1 自定义Runnable

```python
from langchain.schema.runnable import Runnable, RunnableConfig
from typing import TypeVar, Generic, Optional

InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")

class CustomRunnable(Runnable[InputType, OutputType]):
    """自定义Runnable组件"""
    
    def __init__(self, func):
        self.func = func
    
    def invoke(self, input: InputType, config: Optional[RunnableConfig] = None) -> OutputType:
        return self.func(input)
    
    def batch(self, inputs: list[InputType], config: Optional[RunnableConfig] = None) -> list[OutputType]:
        return [self.invoke(input, config) for input in inputs]

# 使用自定义Runnable
def uppercase(text):
    return text.upper()

upper_runnable = CustomRunnable(uppercase)
print(upper_runnable.invoke("hello"))  # HELLO

# 更实用的示例：数据处理管道
class DataProcessor(Runnable[dict, dict]):
    """数据处理Runnable"""
    
    def __init__(self, operations):
        self.operations = operations
    
    def invoke(self, input: dict, config: Optional[RunnableConfig] = None) -> dict:
        result = input.copy()
        for op in self.operations:
            result = op(result)
        return result

# 定义操作
def add_timestamp(data):
    from datetime import datetime
    data["timestamp"] = datetime.now().isoformat()
    return data

def add_word_count(data):
    data["word_count"] = len(data.get("text", "").split())
    return data

# 创建处理器
processor = DataProcessor([add_timestamp, add_word_count])
result = processor.invoke({"text": "Hello World"})
print(result)
```

### 2.2 自定义检索器

```python
from langchain.schema import Document
from langchain.schema.retriever import BaseRetriever
from typing import List

class HybridRetriever(BaseRetriever):
    """混合检索器：结合BM25和向量检索"""
    
    def __init__(self, bm25_retriever, vector_retriever, bm25_weight=0.5):
        self.bm25_retriever = bm25_retriever
        self.vector_retriever = vector_retriever
        self.bm25_weight = bm25_weight
    
    def _get_relevant_documents(self, query: str) -> List[Document]:
        # BM25检索
        bm25_docs = self.bm25_retriever.get_relevant_documents(query)
        
        # 向量检索
        vector_docs = self.vector_retriever.get_relevant_documents(query)
        
        # 合并结果
        doc_scores = {}
        
        for i, doc in enumerate(bm25_docs):
            doc_id = doc.metadata.get("id", id(doc))
            doc_scores[doc_id] = {
                "doc": doc,
                "score": self.bm25_weight * (len(bm25_docs) - i)
            }
        
        for i, doc in enumerate(vector_docs):
            doc_id = doc.metadata.get("id", id(doc))
            if doc_id in doc_scores:
                doc_scores[doc_id]["score"] += (1 - self.bm25_weight) * (len(vector_docs) - i)
            else:
                doc_scores[doc_id] = {
                    "doc": doc,
                    "score": (1 - self.bm25_weight) * (len(vector_docs) - i)
                }
        
        # 排序返回
        sorted_docs = sorted(doc_scores.values(), key=lambda x: x["score"], reverse=True)
        return [item["doc"] for item in sorted_docs]

# 使用
# retriever = HybridRetriever(bm25_retriever, vector_retriever)
```

---

## 三、工作流编排

### 3.1 使用LangGraph

```python
# pip install langgraph

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated

# 定义状态
class AgentState(TypedDict):
    messages: list
    current_step: str
    result: str

# 定义节点函数
def analyze_input(state: AgentState) -> AgentState:
    """分析输入"""
    state["current_step"] = "analyze"
    # 分析逻辑...
    return state

def search_web(state: AgentState) -> AgentState:
    """网络搜索"""
    state["current_step"] = "search"
    # 搜索逻辑...
    return state

def generate_answer(state: AgentState) -> AgentState:
    """生成答案"""
    state["current_step"] = "generate"
    # 生成逻辑...
    state["result"] = "生成的答案"
    return state

def should_search(state: AgentState) -> str:
    """决定是否需要搜索"""
    # 根据内容判断
    return "search" if "最新" in str(state["messages"]) else "generate"

# 构建图
workflow = StateGraph(AgentState)

# 添加节点
workflow.add_node("analyze", analyze_input)
workflow.add_node("search", search_web)
workflow.add_node("generate", generate_answer)

# 添加边
workflow.add_edge("analyze", "search")  # analyze -> search
workflow.add_edge("search", "generate")  # search -> generate
workflow.add_edge("generate", END)       # generate -> END

# 条件边
# workflow.add_conditional_edges(
#     "analyze",
#     should_search,
#     {
#         "search": "search",
#         "generate": "generate"
#     }
# )

# 设置入口
workflow.set_entry_point("analyze")

# 编译并运行
app = workflow.compile()
result = app.invoke({"messages": ["你好"], "current_step": "", "result": ""})
print(result)
```

### 3.2 复杂工作流示例

```python
class ResearchWorkflow:
    """研究助手工作流"""
    
    def __init__(self, llm):
        self.llm = llm
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """构建工作流图"""
        from langgraph.graph import StateGraph, END
        
        class State(TypedDict):
            question: str
            search_results: list
            analysis: str
            answer: str
            feedback: str
        
        def search_node(state):
            # 执行搜索
            # ...
            state["search_results"] = ["result1", "result2"]
            return state
        
        def analyze_node(state):
            # 分析搜索结果
            # ...
            state["analysis"] = "分析结果"
            return state
        
        def draft_node(state):
            # 起草答案
            # ...
            state["answer"] = "草稿答案"
            return state
        
        def review_node(state):
            # 审核答案
            # ...
            state["feedback"] = "需要改进"
            return state
        
        def revise_node(state):
            # 修改答案
            # ...
            state["answer"] = "修改后的答案"
            return state
        
        def quality_check(state):
            # 质量检查
            return "revise" if "改进" in state.get("feedback", "") else END
        
        graph = StateGraph(State)
        graph.add_node("search", search_node)
        graph.add_node("analyze", analyze_node)
        graph.add_node("draft", draft_node)
        graph.add_node("review", review_node)
        graph.add_node("revise", revise_node)
        
        graph.set_entry_point("search")
        graph.add_edge("search", "analyze")
        graph.add_edge("analyze", "draft")
        graph.add_edge("draft", "review")
        graph.add_conditional_edges("review", quality_check)
        graph.add_edge("revise", "review")
        
        return graph.compile()
    
    def run(self, question: str):
        """运行工作流"""
        return self.graph.invoke({
            "question": question,
            "search_results": [],
            "analysis": "",
            "answer": "",
            "feedback": ""
        })
```

---

## 四、高级特性

### 4.1 回调和追踪

```python
from langchain.callbacks import StdOutCallbackHandler
from langchain.callbacks.tracers import LangChainTracer

# 标准输出回调
handler = StdOutCallbackHandler()

# 在链中使用
chain.invoke({"topic": "AI"}, config={"callbacks": [handler]})

# LangSmith追踪（需要设置环境变量）
# export LANGCHAIN_TRACING_V2=true
# export LANGCHAIN_API_KEY=your-key

tracer = LangChainTracer()

# 使用追踪
result = chain.invoke(
    {"topic": "机器学习"},
    config={"callbacks": [tracer], "run_name": "my_chain_run"}
)
```

### 4.2 错误处理

```python
from langchain.schema.runnable import RunnableRetry

# 重试机制
chain_with_retry = chain.with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True,
    retry_on_exception_types=(Exception,)
)

# 带超时
chain_with_timeout = chain.with_timeout(30)  # 30秒超时

# 带错误处理的链
def handle_error(error):
    return f"抱歉，处理出错了: {str(error)}"

safe_chain = chain.with_fallbacks(
    [RunnableLambda(lambda x: handle_error(x))],
    exceptions_to_handle=(Exception,)
)
```

### 4.3 缓存机制

```python
from langchain.cache import InMemoryCache, SQLiteCache
from langchain.globals import set_llm_cache

# 内存缓存
set_llm_cache(InMemoryCache())

# SQLite缓存（持久化）
set_llm_cache(SQLiteCache(database_path="langchain_cache.db"))

# 开启缓存后，相同输入会直接返回缓存结果
result1 = chain.invoke({"topic": "AI"})  # 调用API
result2 = chain.invoke({"topic": "AI"})  # 使用缓存
```

---

## 五、最佳实践

### 5.1 模块化设计

```python
class AIApplication:
    """AI应用模块化设计"""
    
    def __init__(self, config):
        self.config = config
        self._init_components()
    
    def _init_components(self):
        """初始化组件"""
        # LLM
        self.llm = ChatOpenAI(
            model=self.config.get("model", "gpt-3.5-turbo")
        )
        
        # 检索器
        self.retriever = self._create_retriever()
        
        # 记忆
        self.memory = self._create_memory()
        
        # 构建链
        self.chain = self._build_chain()
    
    def _create_retriever(self):
        """创建检索器"""
        # ...
        pass
    
    def _create_memory(self):
        """创建记忆组件"""
        # ...
        pass
    
    def _build_chain(self):
        """构建处理链"""
        # ...
        pass
    
    def run(self, input_data):
        """运行应用"""
        return self.chain.invoke(input_data)
```

### 5.2 性能优化

```python
# 并行执行
from langchain.schema.runnable import RunnableParallel

parallel_chain = RunnableParallel(
    summary=summary_chain,
    keywords=keyword_chain,
    sentiment=sentiment_chain
)

results = parallel_chain.invoke({"text": "..."})

# 异步执行
async def run_async():
    result = await chain.ainvoke({"topic": "AI"})
    return result

# 批量处理优化
def process_large_dataset(data, chain, batch_size=10):
    """批量处理大数据集"""
    results = []
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        batch_results = chain.batch(batch)
        results.extend(batch_results)
    return results
```

---

## 参考资源

> - [LangChain文档](https://python.langchain.com/docs/get_started/introduction) - 官方文档
> - [LCEL指南](https://python.langchain.com/docs/expression_language/) - 表达式语言
> - [LangGraph文档](https://langchain-ai.github.io/langgraph/) - 工作流编排
> - [LangSmith](https://www.langchain.com/langsmith) - 追踪调试平台
> - [LangChain Cookbook](https://github.com/langchain-ai/langchain/tree/master/cookbook) - 示例代码
> - [LangChain Templates](https://github.com/langchain-ai/langchain/tree/master/templates) - 项目模板

---

**上一篇**：[向量数据库详解]({{ site.baseurl }}{% post_url /ailearn/06-llm-application/2026-04-16-05-vector-database %})

**返回**：[大模型应用]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-06-llm-application %})

*最后更新: 2026年4月16日*
