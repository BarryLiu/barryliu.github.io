---
layout: post
title: "AI项目实战 - 知识库问答系统"
date: 2026-04-20
categories: ailearn
tags: [AI, 项目实战, RAG, 知识库]
keywords: 知识库问答, RAG, 文档处理, 向量检索
description: 构建企业级知识库问答系统，支持多种文档格式
---

* content
{:toc}

> **前置知识**：需要先掌握 RAG基础
>
> **本文重点**：企业级知识库系统实现

---

## 一、系统架构

```
知识库问答系统：

文档处理流程：
上传 → 解析 → 分割 → 向量化 → 存储

问答流程：
问题 → 向量化 → 检索 → 重排序 → 生成 → 引用

核心模块：
├── 文档管理：上传、解析、版本控制
├── 向量引擎：索引、检索、更新
├── 问答引擎：理解、检索、生成
└── 管理后台：知识库管理、效果评估
```

---

## 二、文档处理

### 2.1 多格式解析

```python
# document_processor.py
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

class DocumentProcessor:
    """文档处理器"""
    
    def __init__(self, chunk_size=500, chunk_overlap=50):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", "。", "！", "？", "；", " ", ""]
        )
    
    def load_document(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        
        loaders = {
            '.pdf': PyPDFLoader,
            '.docx': Docx2txtLoader,
            '.txt': TextLoader
        }
        
        loader_class = loaders.get(ext, TextLoader)
        loader = loader_class(file_path)
        return loader.load()
    
    def process(self, file_path):
        documents = self.load_document(file_path)
        chunks = self.text_splitter.split_documents(documents)
        
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = f"{os.path.basename(file_path)}_{i}"
            chunk.metadata["source"] = file_path
        
        return chunks
```

### 2.2 表格处理

```python
import pandas as pd

def process_table(file_path):
    """处理Excel/CSV表格"""
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    
    chunks = []
    
    # 表头描述
    header_desc = f"表格包含以下列：{', '.join(df.columns.tolist())}"
    chunks.append({"content": header_desc, "type": "header"})
    
    # 逐行转换
    for idx, row in df.iterrows():
        row_text = " | ".join([f"{col}: {val}" for col, val in row.items()])
        chunks.append({"content": row_text, "type": "row", "row_idx": idx})
    
    return chunks
```

---

## 三、问答引擎

```python
# qa_engine.py
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb

class KnowledgeQA:
    """知识库问答引擎"""
    
    def __init__(self, config):
        self.llm = ChatOpenAI(model=config["model"])
        self.embeddings = OpenAIEmbeddings()
        
        self.client = chromadb.PersistentClient(config["persist_dir"])
        self.collection = self.client.get_or_create_collection("knowledge")
    
    def index_documents(self, documents, doc_id):
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        ids = [f"{doc_id}_{i}" for i in range(len(documents))]
        
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
    
    def query(self, question, top_k=5):
        results = self.collection.query(
            query_texts=[question],
            n_results=top_k
        )
        
        context = "\n\n".join(results['documents'][0])
        
        prompt = f"""基于以下知识库内容回答问题。
如果知识库中没有相关信息，请明确说明。

知识库内容：
{context}

问题：{question}

请回答："""
        
        response = self.llm.invoke(prompt)
        
        return {
            "answer": response.content,
            "sources": [
                {"content": doc[:200], "metadata": meta}
                for doc, meta in zip(results['documents'][0], results['metadatas'][0])
            ]
        }
    
    def delete_document(self, doc_id):
        all_ids = self.collection.get()["ids"]
        doc_ids = [id for id in all_ids if id.startswith(doc_id)]
        if doc_ids:
            self.collection.delete(ids=doc_ids)
```

---

## 四、管理API

```python
# api.py
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import uuid, os

app = FastAPI(title="知识库问答系统")

qa_engine = KnowledgeQA({"model": "gpt-3.5-turbo", "persist_dir": "./db"})
doc_processor = DocumentProcessor()

class QueryRequest(BaseModel):
    question: str
    top_k: int = 5

@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    doc_id = str(uuid.uuid4())
    file_path = f"./uploads/{doc_id}_{file.filename}"
    
    os.makedirs("./uploads", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    chunks = doc_processor.process(file_path)
    qa_engine.index_documents(chunks, doc_id)
    
    return {"doc_id": doc_id, "filename": file.filename, "chunks": len(chunks)}

@app.post("/query")
async def query(request: QueryRequest):
    return qa_engine.query(request.question, request.top_k)

@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    qa_engine.delete_document(doc_id)
    return {"status": "deleted"}
```

---

## 参考资源

> - [LangChain文档加载器](https://python.langchain.com/docs/modules/data_connection/document_loaders/)
> - [Chroma文档](https://docs.trychroma.com/)

---

**返回**：[AI项目实战]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-12-ai-project %})

*最后更新: 2026年4月20日*