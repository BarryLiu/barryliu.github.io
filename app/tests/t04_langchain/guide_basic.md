# LangChain 常用函数参考

本文档列出了LangChain中最常用的组件和函数及其作用，适用于LLM应用开发。

**默认使用阿里云百炼 API**

## 安装

```bash
# 核心包
pip install langchain langchain-core

# OpenAI兼容接口（用于阿里百炼）
pip install langchain-openai

# 社区组件（文档加载器、向量存储等）
pip install langchain-community

# 阿里百炼SDK（用于嵌入）
pip install dashscope

# 额外依赖
pip install beautifulsoup4 chromadb
```

## 环境变量

```bash
# 阿里云百炼 API Key
export DASHSCOPE_API_KEY="your-api-key"
```

## LLM调用（阿里百炼）

### 基础调用

| 类/函数 | 作用 | 示例 |
|--------|------|------|
| `ChatOpenAI` | 阿里百炼聊天模型 | `ChatOpenAI(model="qwen-max")` |
| `.invoke()` | 发送请求 | `llm.invoke("你好")` |
| `.batch()` | 批量请求 | `llm.batch(["问题1", "问题2"])` |

### 阿里百炼模型

| 模型 | 说明 |
|------|------|
| `qwen-max` | 最强推理，token成本最高 |
| `qwen-plus` | 中等性能，推荐日常使用 |
| `qwen-turbo` | 快速响应，低延迟 |

### 参数配置

| 参数 | 作用 | 示例 |
|------|------|------|
| `model` | 模型名称 | `model="qwen-max"` |
| `temperature` | 随机性（0-1） | `temperature=0.7` |
| `max_tokens` | 最大token数 | `max_tokens=1000` |
| `base_url` | API地址 | `base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/"` |
| `api_key` | API密钥 | `api_key=os.getenv("DASHSCOPE_API_KEY")` |

### 示例（阿里百炼）

```python
import os
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="qwen-max",
    temperature=0.7,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/",
    api_key=os.getenv("DASHSCOPE_API_KEY")
)

response = llm.invoke("请介绍一下人工智能")
print(response.content)
```

## Prompt模板

### 创建模板

| 类/函数 | 作用 | 示例 |
|--------|------|------|
| `PromptTemplate.from_template()` | 从字符串创建 | `PromptTemplate.from_template("{question}")` |
| `ChatPromptTemplate.from_messages()` | 从消息列表创建 | `ChatPromptTemplate.from_messages([...])` |
| `.invoke()` | 渲染模板 | `prompt.invoke({"question": "..."})` |

### 模板语法

| 语法 | 作用 | 示例 |
|------|------|------|
| `{variable}` | 变量占位符 | `{question}` |
| `{variable:default}` | 带默认值的变量 | `{name:张三}` |

### 示例

```python
from langchain_core.prompts import PromptTemplate

# 简单模板
prompt = PromptTemplate.from_template(
    "请回答以下问题：{question}"
)
result = prompt.invoke({"question": "什么是AI？"})

# 带默认值的模板
prompt = PromptTemplate.from_template(
    "请介绍{topic:人工智能}"
)

# 多变量模板
prompt = PromptTemplate.from_template(
    "根据以下Context回答Question：\n\nContext: {context}\nQuestion: {question}"
)
```

### 聊天模板

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的{language}助手"),
    ("human", "{user_input}"),
    ("ai", "好的，我会用{language}回答")
])

result = prompt.invoke({
    "language": "中文",
    "user_input": "什么是机器学习"
})
```

## Chain（链）

### LCEL语法

| 操作符 | 作用 | 示例 |
|--------|------|------|
| `|` | 组合组件 | `prompt \| llm` |
| `RunnableParallel` | 并行执行 | `RunnableParallel({"a": chain1, "b": chain2})` |
| `RunnablePassthrough` | 传递输入 | `RunnablePassthrough()` |

### 常用Chain

| Chain | 作用 | 示例 |
|-------|------|------|
| `LLMChain` | 基础LLM链 | `LLMChain(llm=llm, prompt=prompt)` |
| `SimpleSequentialChain` | 简单顺序链 | `SimpleSequentialChain(chains=[chain1, chain2])` |
| `SequentialChain` | 多输入输出顺序链 | `SequentialChain(chains=[...], ...)` |
| `RetrievalQA` | RAG问答链 | `RetrievalQA.from_chain_type(llm=llm, retriever=retriever)` |

### 示例

```python
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 阿里百炼 LLM
llm = ChatOpenAI(
    model="qwen-max",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/",
    api_key=os.getenv("DASHSCOPE_API_KEY")
)

prompt = PromptTemplate.from_template("用一句话介绍：{topic}")

# 简单Chain
chain = prompt | llm | StrOutputParser()
result = chain.invoke({"topic": "人工智能"})
print(result)

# 并行Chain
from langchain_core.runnables import RunnableParallel

parallel_chain = RunnableParallel({
    "description": chain,
    "origin": another_chain
})
```

## OutputParser（输出解析）

### 常用解析器

| 类 | 作用 | 示例 |
|-----|------|------|
| `StrOutputParser` | 字符串输出 | `StrOutputParser()` |
| `JsonOutputParser` | JSON输出 | `JsonOutputParser()` |
| `CommaSeparatedListOutputParser` | 列表输出 | `CommaSeparatedListOutputParser()` |

### 自定义解析

```python
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel

class Answer(BaseModel):
    topic: str
    description: str

parser = JsonOutputParser(pydantic_schema=Answer)
chain = prompt | llm | parser
result = chain.invoke({"topic": "AI"})
print(result)  # {'topic': '...', 'description': '...'}
```

## Document Loader（文档加载）

### 常用加载器

| 加载器 | 作用 | 示例 |
|--------|------|------|
| `TextLoader` | 加载文本文件 | `TextLoader("file.txt")` |
| `PDFLoader` | 加载PDF | `PyPDFLoader("file.pdf")` |
| `CSVLoader` | 加载CSV | `CSVLoader("file.csv")` |
| `WebBaseLoader` | 加载网页 | `WebBaseLoader("https://...")` |
| `DirectoryLoader` | 加载目录 | `DirectoryLoader("./docs")` |

### 示例

```python
from langchain_community.document_loaders import TextLoader

# 文本文件
loader = TextLoader("document.txt")
documents = loader.load()

# PDF文件
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader("document.pdf")
documents = loader.load()

# 目录加载
from langchain_community.document_loaders import DirectoryLoader
loader = DirectoryLoader("./docs", glob="**/*.txt")
documents = loader.load()
```

## Text Splitter（文本分割）

### 常用分割器

| 分割器 | 作用 | 示例 |
|--------|------|------|
| `RecursiveCharacterTextSplitter` | 递归字符分割 | `RecursiveCharacterTextSplitter(chunk_size=500)` |
| `CharacterTextSplitter` | 字符分割 | `CharacterTextSplitter(chunk_size=500)` |

### 参数

| 参数 | 作用 | 示例 |
|------|------|------|
| `chunk_size` | 块大小 | `chunk_size=500` |
| `chunk_overlap` | 块重叠 | `chunk_overlap=50` |
| `length_function` | 长度计算函数 | `length_function=len` |
| `separators` | 分隔符列表 | `separators=["\n", ".", "。"]` |

### 示例

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len
)

chunks = splitter.split_documents(documents)
print(f"分割成 {len(chunks)} 个块")
```

## Embeddings（嵌入）

### 阿里百炼嵌入

| 类 | 作用 | 示例 |
|-----|------|------|
| `DashScopeEmbeddings` | 阿里百炼嵌入 | `DashScopeEmbeddings(model="text-embedding-v2")` |

### 示例

```python
import os
from langchain_community.embeddings import DashScopeEmbeddings

embeddings = DashScopeEmbeddings(
    model="text-embedding-v2",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)

# 单个文本
vector = embeddings.embed_query("你好，世界")

# 批量文本
vectors = embeddings.embed_documents(["文本1", "文本2"])
```

## Vector Store（向量存储）

### 常用向量存储

| 存储 | 作用 | 示例 |
|------|------|------|
| `Chroma` | 本地向量数据库 | `Chroma.from_documents(docs, embeddings)` |
| `FAISS` | Facebook向量搜索 | `FAISS.from_documents(docs, embeddings)` |

### 示例

```python
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import DashScopeEmbeddings

# 阿里百炼嵌入
embeddings = DashScopeEmbeddings(
    model="text-embedding-v2",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)

# 创建向量存储
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# 保存
vectorstore.persist()

# 检索
results = vectorstore.similarity_search("什么是人工智能", k=3)
for doc in results:
    print(doc.page_content)
```

## Retriever（检索器）

### 常用检索器

| 检索器 | 作用 | 示例 |
|--------|------|------|
| `vectorstore.as_retriever()` | 向量检索器 | `vectorstore.as_retriever(search_kwargs={"k": 5})` |
| `MultiQueryRetriever` | 多查询检索 | `MultiQueryRetriever(...)` |
| `ContextualCompressionRetriever` | 压缩检索 | `ContextualCompressionRetriever(...)` |

### 参数

| 参数 | 作用 | 示例 |
|------|------|------|
| `search_type` | 搜索类型 | `search_type="similarity"` 或 `"mmr"` |
| `search_kwargs` | 搜索参数 | `search_kwargs={"k": 5}` |
| `filter` | 元数据过滤 | `filter={"source": "doc.txt"}` |

### 示例

```python
# 创建检索器
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)

# 使用检索器
results = retriever.invoke("什么是机器学习")

# MMR检索（增加多样性）
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 20, "lambda_mult": 0.5}
)
```

## Tool（工具）

### 定义工具

| 方法 | 作用 | 示例 |
|------|------|------|
| `@tool` | 装饰器定义工具 | `@tool` |
| `BaseTool` | 自定义工具基类 | `class MyTool(BaseTool)` |

### 示例

```python
from langchain_core.tools import tool

@tool
def search_database(query: str) -> str:
    """搜索数据库中的相关信息"""
    return f"找到关于 {query} 的结果"

@tool
def calculate(expression: str) -> float:
    """计算数学表达式"""
    return eval(expression)

tools = [search_database, calculate]
```

## Agent（智能体）

### Agent类型

| Agent | 作用 | 示例 |
|-------|------|------|
| `initialize_agent` | 创建Agent | `initialize_agent(tools, llm, agent_type)` |
| `AgentType` | Agent类型枚举 | `AgentType.ZERO_SHOT_REACT_DESCRIPTION` |
| `AgentExecutor` | Agent执行器 | `AgentExecutor.from_agent_and_tools(...)` |

### Agent类型枚举

| 类型 | 作用 |
|------|------|
| `ZERO_SHOT_REACT_DESCRIPTION` | 零样本推理 |
| `CONVERSATIONAL` | 对话式 |

### 示例

```python
from langchain.agents import initialize_agent, AgentType
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """获取城市天气"""
    return f"{city}的天气是晴天，20度"

@tool
def search_news(topic: str) -> str:
    """搜索新闻"""
    return f"关于{topic}的最新新闻..."

tools = [get_weather, search_news]

# 阿里百炼 LLM
llm = ChatOpenAI(
    model="qwen-max",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/",
    api_key=os.getenv("DASHSCOPE_API_KEY")
)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

result = agent.invoke("北京今天的天气怎么样？")
```

## Memory（记忆）

### 常用Memory

| 类 | 作用 | 示例 |
|-----|------|------|
| `ConversationBufferMemory` | 对话缓冲记忆 | `ConversationBufferMemory()` |
| `ConversationSummaryMemory` | 对话摘要记忆 | `ConversationSummaryMemory(llm=llm)` |
| `ConversationBufferWindowMemory` | 窗口记忆 | `ConversationBufferWindowMemory(k=5)` |

### 示例

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

memory = ConversationBufferMemory(
    memory_key="history",
    return_messages=True
)

# 保存对话
memory.save_context(
    {"input": "你好"},
    {"output": "你好！有什么可以帮助你的吗？"}
)

# 加载记忆
history = memory.load_memory_variables({})
print(history["history"])

# 在Chain中使用
chain = ConversationChain(llm=llm, memory=memory)
response = chain.invoke({"input": "我叫张三"})
```

## RAG（检索增强生成）

### 完整RAG流程（阿里百炼）

```python
import os
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# 1. 加载文档
loader = TextLoader("document.txt")
documents = loader.load()

# 2. 分割文本
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# 3. 创建嵌入（阿里百炼）
embeddings = DashScopeEmbeddings(
    model="text-embedding-v2",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)

# 4. 向量存储
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./db")

# 5. 检索器
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 6. LLM（阿里百炼）
llm = ChatOpenAI(
    model="qwen-max",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/",
    api_key=os.getenv("DASHSCOPE_API_KEY")
)

# 7. RAG Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# 8. 查询
result = qa_chain.invoke("文档的主要内容是什么？")
print(result["result"])
```

## 常用模式

### 简单问答Chain

```python
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(
    model="qwen-max",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/",
    api_key=os.getenv("DASHSCOPE_API_KEY")
)

prompt = PromptTemplate.from_template(
    "请根据以下上下文回答问题：\n\nContext: {context}\n\nQuestion: {question}"
)
parser = StrOutputParser()

chain = prompt | llm | parser

result = chain.invoke({
    "context": "人工智能是计算机科学的一个分支...",
    "question": "什么是人工智能？"
})
```

### 带历史记录的对话

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

memory = ConversationBufferMemory()
chain = ConversationChain(llm=llm, memory=memory)

while True:
    user_input = input("你: ")
    if user_input.lower() == "exit":
        break
    response = chain.invoke({"input": user_input})
    print(f"AI: {response['response']}")
```

---

**注意**：本文档默认使用阿里云百炼API。如需使用其他API（如OpenAI），请替换LLM配置。