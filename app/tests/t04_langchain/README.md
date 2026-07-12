# LangChain学习包

LangChain是构建LLM应用的主流框架，主要用于**RAG、Agent、聊天机器人等应用开发**。

**默认使用阿里云百炼 API**

## 为什么学习LangChain？

- ✅ **RAG应用**：检索增强生成的核心框架
- ✅ **Agent开发**：智能体编排和控制
- ✅ **Chain组合**：复杂业务流程编排
- ✅ **Prompt模板**：高效的提示词管理
- ✅ **工具调用**：LLM与外部系统集成

## 文件说明

### 01_basics.py - 基础操作
- LangChain组件介绍
- LLM调用（阿里百炼）
- Prompt模板（PromptTemplate）
- 输出解析（OutputParser）
- 简单Chain组合

**学习时间**：1-2天

### 02_rag.py - RAG应用（核心）
- 文档加载（Document Loader）
- 文本分割（Text Splitter）
- 向量存储（Vector Store）
- 嵌入模型（阿里百炼DashScopeEmbeddings）
- 检索器（Retriever）
- 完整RAG Chain

**学习时间**：2-3天
**重要性**：⭐⭐⭐⭐⭐（RAG开发必须掌握）

### 03_agent.py - Agent开发
- Agent类型介绍
- 工具定义（Tool）
- AgentExecutor
- 状态管理

**学习时间**：2-3天

### 04_memory.py - 记忆管理
- ConversationBufferMemory
- ConversationSummaryMemory
- 窗口记忆

**学习时间**：1-2天

## 环境配置

```bash
# 安装依赖
pip install langchain langchain-openai langchain-community dashscope chromadb beautifulsoup4

# 设置环境变量
export DASHSCOPE_API_KEY="your-api-key"
```

## 学习顺序

1. **基础操作**（01_basics.py）
2. **RAG应用**（02_rag.py）— 重点
3. **Agent开发**（03_agent.py）
4. **记忆管理**（04_memory.py）

## 运行示例

```bash
# 基础操作
python tests/t04_langchain/01_basics.py

# RAG应用
python tests/t04_langchain/02_rag.py

# Agent开发
python tests/t04_langchain/03_agent.py

# 记忆管理
python tests/t04_langchain/04_memory.py
```

## 核心概念

### LLM调用（阿里百炼）

```python
import os
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="qwen-max",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/",
    api_key=os.getenv("DASHSCOPE_API_KEY")
)

response = llm.invoke("你好，请介绍一下你自己")
print(response.content)
```

### Prompt模板

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "请根据以下信息回答问题：\n\nContext: {context}\n\nQuestion: {question}"
)

chain = prompt | llm
response = chain.invoke({"context": "...", "question": "..."})
```

### Chain组合

```python
from langchain_core.output_parsers import StrOutputParser

chain = prompt | llm | StrOutputParser()
response = chain.invoke({"context": "...", "question": "..."})
```

### RAG Chain（阿里百炼）

```python
import os
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# 1. 加载文档
loader = TextLoader("document.txt")
documents = loader.load()

# 2. 分割文本
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# 3. 创建向量存储（阿里百炼嵌入）
embeddings = DashScopeEmbeddings(
    model="text-embedding-v2",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)
vectorstore = Chroma.from_documents(chunks, embeddings)

# 4. 创建检索器
retriever = vectorstore.as_retriever()

# 5. LLM（阿里百炼）
llm = ChatOpenAI(
    model="qwen-max",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/",
    api_key=os.getenv("DASHSCOPE_API_KEY")
)

# 6. 构建RAG Chain
from langchain.chains import RetrievalQA
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# 7. 查询
response = qa_chain.invoke("什么是人工智能？")
```

## 与其他框架的关系

| 框架 | 用途 | LangChain关系 |
|------|------|---------------|
| NumPy | 向量计算 | ✅ 底层依赖 |
| PyTorch | 模型训练 | ❌ 不需要 |
| LangChain | 应用开发 | ✅ 核心框架 |

## 应用场景

| 场景 | 需要LangChain? | 说明 |
|------|----------------|------|
| 简单LLM调用 | ⚠️ 可选 | 可直接用SDK |
| RAG应用 | ✅ 必须 | 核心功能 |
| Agent开发 | ✅ 必须 | 编排能力 |
| 聊天机器人 | ✅ 必须 | 对话管理 |
| 复杂工作流 | ✅ 必须 | Chain编排 |

## 学习建议

1. **理解组件**：LCEL、Chain、Prompt、Memory等
2. **掌握RAG**：最重要的应用场景
3. **实践Agent**：理解工具调用和决策
4. **参考文档**：LangChain官方文档非常完善

## 下一步

掌握LangChain后，可以继续学习：
- RAG项目实战
- Agent系统开发
- 聊天机器人开发
- 企业知识库构建