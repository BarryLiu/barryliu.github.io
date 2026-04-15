---
layout: post
title: "Agent记忆系统 - 上下文管理"
date: 2026-04-20
categories: ailearn
tags: [AI, Agent, 记忆系统, RAG]
keywords: Agent记忆, 向量记忆, 对话管理, 上下文
---

* content
{:toc}

> **前置知识**：需要先掌握 向量数据库
>
> **本文重点**：Agent记忆系统设计与实现

---

## 一、记忆系统概述

```
Agent记忆类型：

1. 短期记忆 (Short-term Memory)
   - 当前对话上下文
   - 有限的窗口大小
   - 即时交互

2. 长期记忆 (Long-term Memory)
   - 向量数据库存储
   - 检索式回忆
   - 跨会话持久化

3. 工作记忆 (Working Memory)
   - 当前任务状态
   - 中间结果存储
   - 临时缓冲区
```

---

## 二、对话记忆

### 2.1 简单缓冲记忆

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI

# 创建记忆
memory = ConversationBufferMemory()

# 创建对话链
llm = ChatOpenAI(model="gpt-3.5-turbo")
chain = ConversationChain(llm=llm, memory=memory, verbose=True)

# 对话
response1 = chain.predict(input="我叫张三")
response2 = chain.predict(input="我叫什么名字？")  # 会记住张三

# 查看记忆
print(memory.load_memory_variables({}))
```

### 2.2 窗口记忆

```python
from langchain.memory import ConversationBufferWindowMemory

# 只保留最近k轮对话
memory = ConversationBufferWindowMemory(k=5)

chain = ConversationChain(llm=llm, memory=memory)
```

### 2.3 摘要记忆

```python
from langchain.memory import ConversationSummaryMemory

# 自动总结历史对话
memory = ConversationSummaryMemory(llm=llm)

chain = ConversationChain(llm=llm, memory=memory)

# 长对话自动压缩
for i in range(20):
    chain.predict(input=f"第{i+1}条消息")

print(memory.load_memory_variables({}))
```

---

## 三、向量记忆

### 3.1 基本实现

```python
from langchain.memory import VectorStoreRetrieverMemory
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# 创建向量存储
embeddings = OpenAIEmbeddings()
vectorstore = Chroma(embedding_function=embeddings, persist_directory="./memory_db")

# 创建向量记忆
memory = VectorStoreRetrieverMemory(
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)

# 保存记忆
memory.save_context(
    {"input": "我喜欢编程"},
    {"output": "好的，我会记住你喜欢编程"}
)

memory.save_context(
    {"input": "我住在北京"},
    {"output": "北京是个好地方"}
)

# 检索相关记忆
relevant = memory.load_memory_variables({"input": "我的爱好是什么？"})
print(relevant)
```

### 3.2 完整记忆系统

```python
class AgentMemory:
    """完整的Agent记忆系统"""
    
    def __init__(self, llm, persist_dir="./memory"):
        self.llm = llm
        
        # 短期记忆
        self.short_term = ConversationBufferWindowMemory(k=10)
        
        # 长期记忆
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma(
            embedding_function=self.embeddings,
            persist_directory=persist_dir
        )
        self.long_term = VectorStoreRetrieverMemory(
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5})
        )
    
    def add_memory(self, user_input, assistant_output):
        """添加记忆"""
        # 短期记忆
        self.short_term.save_context(
            {"input": user_input},
            {"output": assistant_output}
        )
        
        # 长期记忆（重要信息）
        if self._is_important(user_input, assistant_output):
            self.long_term.save_context(
                {"input": user_input},
                {"output": assistant_output}
            )
    
    def _is_important(self, user_input, assistant_output):
        """判断是否是重要信息"""
        keywords = ["喜欢", "讨厌", "名字", "住", "工作", "爱好"]
        return any(kw in user_input for kw in keywords)
    
    def get_context(self, current_input):
        """获取相关上下文"""
        # 短期上下文
        short_context = self.short_term.load_memory_variables({})
        
        # 长期相关记忆
        long_context = self.long_term.load_memory_variables({"input": current_input})
        
        return {
            "recent_conversation": short_context.get("history", ""),
            "relevant_memories": long_context.get("history", "")
        }
    
    def chat(self, user_input):
        """带记忆的对话"""
        context = self.get_context(user_input)
        
        prompt = f"""
历史对话：{context['recent_conversation']}

相关记忆：{context['relevant_memories']}

用户：{user_input}

请回答："""
        
        response = self.llm.invoke(prompt).content
        self.add_memory(user_input, response)
        
        return response
```

---

## 四、实体记忆

```python
from langchain.memory import ConversationEntityMemory

# 提取和记忆实体
memory = ConversationEntityMemory(llm=llm)

chain = ConversationChain(llm=llm, memory=memory)

# 自动提取实体
response = chain.predict(input="我和小明在北京见面了")

# 查看实体记忆
print(memory.entity_store)
```

---

## 五、知识图谱记忆

```python
class KnowledgeGraphMemory:
    """知识图谱记忆"""
    
    def __init__(self):
        self.entities = {}  # 实体
        self.relations = []  # 关系
    
    def add_triple(self, subject, relation, obj):
        """添加三元组"""
        self.relations.append({
            "subject": subject,
            "relation": relation,
            "object": obj
        })
        
        if subject not in self.entities:
            self.entities[subject] = []
        self.entities[subject].append({"relation": relation, "object": obj})
    
    def query_entity(self, entity):
        """查询实体"""
        return self.entities.get(entity, [])
    
    def extract_and_store(self, text):
        """从文本提取实体和关系"""
        # 使用LLM提取
        prompt = f"""从以下文本中提取实体和关系：

文本：{text}

输出格式：实体1 | 关系 | 实体2
每行一个三元组。"""
        
        response = self.llm.invoke(prompt).content
        
        for line in response.split("\n"):
            if "|" in line:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) == 3:
                    self.add_triple(parts[0], parts[1], parts[2])
```

---

## 参考资源

> - [LangChain Memory](https://python.langchain.com/docs/modules/memory/)
> - [MemGPT](https://github.com/cpacker/MemGPT)
> - [Letta](https://github.com/letta-ai/letta)

---

**返回**：[AI Agent智能体]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-11-ai-agent %})

*最后更新: 2026年4月20日*