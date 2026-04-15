---
layout: post
title: "AI项目实战 - 智能客服系统"
date: 2026-04-20
categories: ailearn
tags: [AI, 项目实战, RAG, 客服系统]
keywords: AI客服, RAG, 对话系统, FastAPI
description: 从零构建智能客服系统，实现多轮对话与知识库检索
---

* content
{:toc}

> **前置知识**：需要先掌握 RAG基础
>
> **本文重点**：完整项目实现与部署

---

## 一、项目架构

```
智能客服系统架构：

┌─────────────────────────────────────┐
│            前端界面                   │
│         (Vue/React)                  │
└─────────────────┬───────────────────┘
                  │ HTTP/WebSocket
                  ▼
┌─────────────────────────────────────┐
│            后端服务                   │
│  ┌─────────────────────────────────┐│
│  │  API层 (FastAPI)                ││
│  ├─────────────────────────────────┤│
│  │  对话管理                        ││
│  │  意图识别                        ││
│  ├─────────────────────────────────┤│
│  │  RAG引擎                         ││
│  │  - 知识库检索                    ││
│  │  - 上下文理解                    ││
│  │  - 答案生成                      ││
│  └─────────────────────────────────┘│
└─────────────────┬───────────────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
┌───────┐   ┌───────┐   ┌───────┐
│ 向量库 │   │ 数据库 │   │ LLM  │
│Chroma │   │SQLite │   │ API  │
└───────┘   └───────┘   └───────┘
```

---

## 二、后端实现

### 2.1 核心服务

```python
# services/chat_service.py
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

class CustomerServiceBot:
    """智能客服机器人"""
    
    def __init__(self, config):
        self.llm = ChatOpenAI(model=config["llm_model"], temperature=0.7)
        self.embeddings = OpenAIEmbeddings(model=config["embedding_model"])
        
        self.vectorstore = Chroma(
            persist_directory=config["persist_dir"],
            embedding_function=self.embeddings
        )
        
        self.sessions = {}
        
        self.system_prompt = """你是一个专业的客服助手。
        
请根据以下规则回答问题：
1. 如果问题在知识库中有答案，基于知识库回答
2. 如果知识库没有答案，礼貌告知用户并建议转人工
3. 保持友好、专业的态度

知识库内容：
{context}

用户问题：{question}

请回答："""
    
    def get_session(self, session_id):
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "memory": ConversationBufferMemory(
                    memory_key="chat_history",
                    return_messages=True
                ),
                "history": []
            }
        return self.sessions[session_id]
    
    def chat(self, session_id, question):
        session = self.get_session(session_id)
        
        docs = self.vectorstore.similarity_search(question, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        prompt = PromptTemplate.from_template(self.system_prompt)
        chain = prompt | self.llm
        
        response = chain.invoke({"context": context, "question": question})
        
        session["history"].append({"role": "user", "content": question})
        session["history"].append({"role": "assistant", "content": response.content})
        
        return {
            "answer": response.content,
            "sources": [{"content": doc.page_content[:100]} for doc in docs]
        }
```

### 2.2 API路由

```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI(title="智能客服系统")

bot = CustomerServiceBot({
    "llm_model": "gpt-3.5-turbo",
    "embedding_model": "text-embedding-ada-002",
    "persist_dir": "./chroma_db"
})

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sources: list

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())
    result = bot.chat(session_id, request.message)
    return ChatResponse(session_id=session_id, **result)

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

---

## 三、前端实现

```vue
<!-- Chat.vue -->
<template>
  <div class="chat-container">
    <div class="messages" ref="messagesContainer">
      <div v-for="msg in messages" :key="msg.id"
           :class="['message', msg.role]">
        <div class="content">{{ msg.content }}</div>
      </div>
    </div>
    
    <div class="input-area">
      <input v-model="inputText" 
             @keyup.enter="sendMessage"
             placeholder="输入您的问题..." />
      <button @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import axios from 'axios'

const messages = ref([])
const inputText = ref('')
const sessionId = ref(null)

const sendMessage = async () => {
  if (!inputText.value.trim()) return
  
  const userMessage = inputText.value
  inputText.value = ''
  
  messages.value.push({ id: Date.now(), role: 'user', content: userMessage })
  
  try {
    const response = await axios.post('/api/chat', {
      session_id: sessionId.value,
      message: userMessage
    })
    
    sessionId.value = response.data.session_id
    messages.value.push({ id: Date.now() + 1, role: 'assistant', content: response.data.answer })
  } catch (error) {
    console.error('Error:', error)
  }
}
</script>
```

---

## 四、部署配置

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./chroma_db:/app/chroma_db
  
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

---

## 参考资源

> - [FastAPI文档](https://fastapi.tiangolo.com/)
> - [LangChain文档](https://python.langchain.com/)
> - [Vue.js文档](https://vuejs.org/)

---

**返回**：[AI项目实战]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-12-ai-project %})

*最后更新: 2026年4月20日*