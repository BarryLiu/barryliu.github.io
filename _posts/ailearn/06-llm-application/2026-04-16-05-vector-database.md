---
layout: post
title: "向量数据库详解 - 从原理到实战"
date: 2026-04-16
categories: ailearn
tags: [AI, 向量数据库, Pinecone, Milvus, Chroma]
keywords: 向量数据库, 向量检索, Pinecone, Milvus, Chroma, FAISS
description: 全面掌握向量数据库技术，构建高效的语义检索系统
---

* content
:{:toc}

> **前置知识**：需要先掌握 [大模型API应用]({{ site.baseurl }}{% post_url /ailearn/06-llm-application/2026-04-16-01-llm-api %})
>
> **本文重点**：向量数据库原理与主流方案对比

---

## 一、向量数据库概述

### 1.1 为什么需要向量数据库

```
传统数据库局限：
├── 关键词匹配：语义鸿沟问题
├── 结构化查询：无法处理非结构化数据
├── 精确匹配：不支持相似性检索
└── 扩展性差：大规模数据性能下降

向量数据库优势：
├── 语义检索：理解查询含义
├── 多模态：文本、图像、音频统一表示
├── 高效相似性搜索：ANN算法加速
└── 可扩展：支持十亿级向量

应用场景：
- RAG知识库检索
- 推荐系统
- 以图搜图
- 语义搜索
- 去重与聚类
```

### 1.2 核心概念

```python
"""
向量数据库核心概念：

1. 向量 (Vector/Embedding)
   - 高维数值表示
   - 通常是128-1536维
   - 相似向量距离近

2. 距离度量
   - 欧氏距离 (L2): √Σ(xi-yi)²
   - 余弦相似度: cos(θ) = A·B / (|A||B|)
   - 内积 (IP): A·B

3. ANN (近似最近邻)
   - HNSW: 分层可导航小世界图
   - IVF: 倒排索引
   - LSH: 局部敏感哈希

4. 索引类型
   - FLAT: 暴力搜索，精度高
   - IVF_FLAT: 聚类+搜索
   - IVF_PQ: 乘积量化压缩
   - HNSW: 图索引
"""
```

---

## 二、主流向量数据库

### 2.1 方案对比

```
向量数据库对比：

┌──────────────┬─────────┬─────────┬─────────┬─────────┐
│     特性      │ Pinecone │  Milvus  │ Chroma  │  FAISS  │
├──────────────┼─────────┼─────────┼─────────┼─────────┤
│ 类型         │ 托管服务 │ 开源/云  │ 轻量级  │   库    │
│ 部署复杂度   │   低    │   中     │   低    │   低    │
│ 性能         │   高    │   高     │   中    │   高    │
│ 扩展性       │   高    │   高     │   低    │   中    │
│ 成本         │   高    │   中     │   免费  │  免费   │
│ 适用场景     │ 生产环境 │ 企业级   │ 开发/小 │ 本地/研究│
└──────────────┴─────────┴─────────┴─────────┴─────────┘

选择建议：
- 快速原型：Chroma
- 生产环境：Pinecone / Milvus
- 本地/研究：FAISS
- 企业私有化：Milvus / Qdrant
```

### 2.2 FAISS

```python
"""
FAISS (Facebook AI Similarity Search)
Meta开源的高效向量检索库
"""

# 安装
# pip install faiss-cpu  # CPU版本
# pip install faiss-gpu  # GPU版本

import numpy as np
import faiss

# 准备数据
d = 128  # 向量维度
nb = 10000  # 数据库大小
nq = 100  # 查询数量

# 生成随机向量
np.random.seed(1234)
xb = np.random.random((nb, d)).astype('float32')
xq = np.random.random((nq, d)).astype('float32')

# 1. 暴力搜索 (IndexFlatL2)
index_flat = faiss.IndexFlatL2(d)
index_flat.add(xb)

k = 5  # 返回最近k个
D, I = index_flat.search(xq, k)
print(f"暴力搜索结果: Top-{k} 索引")
print(I[:5])

# 2. IVF索引 (更快的近似搜索)
nlist = 100  # 聚类中心数
quantizer = faiss.IndexFlatL2(d)
index_ivf = faiss.IndexIVFFlat(quantizer, d, nlist)

# 训练索引
index_ivf.train(xb)
index_ivf.add(xb)

# 搜索
index_ivf.nprobe = 10  # 搜索的聚类数
D, I = index_ivf.search(xq, k)
print(f"IVF搜索结果: Top-{k} 索引")

# 3. HNSW索引 (高性能图索引)
M = 32  # 每个节点的连接数
index_hnsw = faiss.IndexHNSWFlat(d, M)
index_hnsw.add(xb)

D, I = index_hnsw.search(xq, k)
print(f"HNSW搜索结果: Top-{k} 索引")

# 4. 带乘积量化的索引 (压缩存储)
m = 8  # 子向量数
bits = 8  # 每个子向量的位数
quantizer_pq = faiss.IndexFlatL2(d)
index_ivfpq = faiss.IndexIVFPQ(quantizer_pq, d, nlist, m, bits)

index_ivfpq.train(xb)
index_ivfpq.add(xb)

D, I = index_ivfpq.search(xq, k)
print(f"IVF+PQ搜索结果: Top-{k} 索引")

# 保存和加载索引
faiss.write_index(index_ivf, "index_ivf.faiss")
loaded_index = faiss.read_index("index_ivf.faiss")
```

### 2.3 Chroma

```python
"""
Chroma: 轻量级开源向量数据库
适合快速开发和原型验证
"""

# 安装
# pip install chromadb

import chromadb
from chromadb.config import Settings

# 创建客户端
client = chromadb.Client()  # 内存模式
# 或持久化模式
# client = chromadb.PersistentClient(path="./chroma_db")

# 创建集合
collection = client.create_collection(
    name="documents",
    metadata={"description": "My document collection"}
)

# 添加文档
documents = [
    "Python是一种流行的编程语言",
    "机器学习是人工智能的子领域",
    "向量数据库用于语义检索",
    "深度学习使用神经网络",
    "自然语言处理处理文本数据"
]

collection.add(
    documents=documents,
    metadatas=[{"source": f"doc_{i}"} for i in range(len(documents))],
    ids=[f"id_{i}" for i in range(len(documents))]
)

# 查询
results = collection.query(
    query_texts=["什么是AI技术"],
    n_results=3
)

print("查询结果:")
for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
    print(f"- {doc} (来源: {metadata['source']})")

# 使用自定义Embedding
from chromadb.utils import embedding_functions

# OpenAI Embedding
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="your-api-key",
    model_name="text-embedding-ada-002"
)

# HuggingFace Embedding
hf_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# 创建使用自定义Embedding的集合
collection_custom = client.create_collection(
    name="custom_embeddings",
    embedding_function=hf_ef
)
```

### 2.4 Pinecone

```python
"""
Pinecone: 托管式向量数据库
生产环境首选
"""

# 安装
# pip install pinecone

import pinecone

# 初始化
pinecone.init(
    api_key="your-api-key",
    environment="us-west1-gcp"
)

# 创建索引
pinecone.create_index(
    name="my-index",
    dimension=1536,  # 向量维度
    metric="cosine",  # 距离度量: cosine, euclidean, dotproduct
    pod_type="p1.x1"  # 实例类型
)

# 连接索引
index = pinecone.Index("my-index")

# 插入向量
vectors = [
    ("id1", [0.1, 0.2, ...], {"text": "hello", "category": "greeting"}),
    ("id2", [0.3, 0.4, ...], {"text": "world", "category": "noun"}),
]

index.upsert(vectors=vectors)

# 查询
query_vector = [0.15, 0.25, ...]
results = index.query(
    vector=query_vector,
    top_k=10,
    include_metadata=True,
    filter={"category": {"$eq": "greeting"}}  # 元数据过滤
)

print(f"查询结果: {results}")

# 批量操作
# 批量插入
def batch_upsert(index, vectors, batch_size=100):
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i+batch_size]
        index.upsert(vectors=batch)

# 删除
index.delete(ids=["id1", "id2"])

# 删除索引
pinecone.delete_index("my-index")
```

### 2.5 Milvus

```python
"""
Milvus: 开源企业级向量数据库
支持分布式部署
"""

# 安装
# pip install pymilvus

from pymilvus import (
    connections, 
    Collection, 
    FieldSchema, 
    CollectionSchema, 
    DataType,
    utility
)

# 连接
connections.connect("default", host="localhost", port="19530")

# 定义Schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=128),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=512)
]

schema = CollectionSchema(fields, "Document collection")

# 创建集合
collection = Collection("documents", schema)

# 创建索引
index_params = {
    "metric_type": "L2",
    "index_type": "IVF_FLAT",
    "params": {"nlist": 128}
}
collection.create_index("embedding", index_params)

# 插入数据
entities = [
    [[0.1, 0.2, ...]],  # embeddings
    ["sample text"]      # text
]
collection.insert(entities)

# 加载集合到内存
collection.load()

# 查询
search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
results = collection.search(
    data=[[0.1, 0.2, ...]],  # 查询向量
    anns_field="embedding",
    param=search_params,
    limit=10,
    expr='text like "%python%"'  # 过滤条件
)

# 释放资源
collection.release()
connections.disconnect("default")
```

---

## 三、性能优化

### 3.1 索引选择

```python
"""
索引选择指南：

数据规模 < 10万:
├── IndexFlatL2 / IndexFlatIP (暴力搜索)
└── 精度最高，速度可接受

数据规模 10万 - 100万:
├── IndexIVFFlat
├── nlist = sqrt(N)
└── 精度和速度平衡

数据规模 100万 - 1000万:
├── IndexIVFPQ
├── 或 HNSW
└── 压缩存储，快速检索

数据规模 > 1000万:
├── HNSW + 量化
├── 或分布式Milvus
└── 可扩展性优先

内存受限:
├── IndexIVFPQ
├── 或 DiskANN
└── 牺牲精度换空间

延迟要求高:
├── HNSW
├── 或 IndexIVFFlat + 大nprobe
└── 以空间换时间
"""

def create_optimal_index(vectors, memory_limit_gb=4):
    """根据数据规模选择最优索引"""
    n, d = vectors.shape
    
    # 计算内存需求
    flat_memory = n * d * 4 / 1e9  # GB
    
    if n < 100000:
        # 小规模：暴力搜索
        return faiss.IndexFlatL2(d)
    
    elif n < 1000000:
        # 中等规模：IVF
        nlist = int(np.sqrt(n))
        quantizer = faiss.IndexFlatL2(d)
        return faiss.IndexIVFFlat(quantizer, d, nlist)
    
    elif flat_memory > memory_limit_gb:
        # 内存受限：PQ压缩
        nlist = int(np.sqrt(n))
        m = d // 8
        quantizer = faiss.IndexFlatL2(d)
        return faiss.IndexIVFPQ(quantizer, d, nlist, m, 8)
    
    else:
        # 大规模：HNSW
        M = 32
        return faiss.IndexHNSWFlat(d, M)
```

### 3.2 查询优化

```python
# 批量查询
def batch_search(index, queries, batch_size=100, k=10):
    """批量查询优化"""
    results = []
    for i in range(0, len(queries), batch_size):
        batch = queries[i:i+batch_size]
        D, I = index.search(batch, k)
        results.append((D, I))
    return results

# 并行查询
import concurrent.futures

def parallel_search(index, queries, k=10, workers=4):
    """并行查询"""
    def search_single(query):
        D, I = index.search(query.reshape(1, -1), k)
        return D[0], I[0]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(search_single, queries))
    
    return results

# 混合检索（向量+关键词）
def hybrid_search(vector_index, keyword_index, query_vector, query_text, 
                  alpha=0.5, k=10):
    """
    混合检索：结合向量检索和关键词检索
    
    alpha: 向量检索权重 (1-alpha): 关键词检索权重
    """
    # 向量检索
    vector_results = vector_index.search(query_vector, k*2)
    
    # 关键词检索
    keyword_results = keyword_index.search(query_text, k*2)
    
    # 融合排序
    scores = {}
    for i, doc_id in enumerate(vector_results['ids']):
        scores[doc_id] = scores.get(doc_id, 0) + alpha * (k*2 - i)
    
    for i, doc_id in enumerate(keyword_results['ids']):
        scores[doc_id] = scores.get(doc_id, 0) + (1-alpha) * (k*2 - i)
    
    # 排序并返回Top-k
    sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_results[:k]
```

---

## 四、实战案例

### 4.1 构建语义搜索引擎

```python
from sentence_transformers import SentenceTransformer
import chromadb

class SemanticSearchEngine:
    """语义搜索引擎"""
    
    def __init__(self, model_name="all-MiniLM-L6-v2", persist_dir="./search_db"):
        self.encoder = SentenceTransformer(model_name)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection("documents")
    
    def index_documents(self, documents, batch_size=100):
        """索引文档"""
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            embeddings = self.encoder.encode(batch)
            
            self.collection.add(
                documents=batch,
                embeddings=embeddings.tolist(),
                ids=[f"doc_{i+j}" for j in range(len(batch))]
            )
    
    def search(self, query, top_k=5):
        """语义搜索"""
        query_embedding = self.encoder.encode([query])
        
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=top_k
        )
        
        return [
            {"text": doc, "distance": dist}
            for doc, dist in zip(results['documents'][0], results['distances'][0])
        ]
    
    def search_with_filters(self, query, filters=None, top_k=5):
        """带过滤条件的搜索"""
        query_embedding = self.encoder.encode([query])
        
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=top_k,
            where=filters
        )
        
        return results

# 使用示例
engine = SemanticSearchEngine()
# engine.index_documents(documents)
# results = engine.search("机器学习算法")
```

### 4.2 RAG知识库

```python
class RAGKnowledgeBase:
    """RAG知识库"""
    
    def __init__(self, embedding_model="text-embedding-ada-002"):
        self.client = chromadb.PersistentClient("./rag_db")
        self.collection = self.client.get_or_create_collection("knowledge")
        
        from langchain.embeddings.openai import OpenAIEmbeddings
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
    
    def add_texts(self, texts, metadatas=None):
        """添加文本"""
        embeddings = self.embeddings.embed_documents(texts)
        
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas or [{} for _ in texts],
            ids=[f"doc_{i}" for i in range(len(texts))]
        )
    
    def add_pdf(self, pdf_path, chunk_size=500, chunk_overlap=50):
        """添加PDF文档"""
        from langchain.document_loaders import PyPDFLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunks = splitter.split_documents(documents)
        
        texts = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        
        self.add_texts(texts, metadatas)
    
    def retrieve(self, query, top_k=5):
        """检索相关文档"""
        query_embedding = self.embeddings.embed_query(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        return results
```

---

## 参考资源

> - [FAISS Wiki](https://github.com/facebookresearch/faiss/wiki) - FAISS官方文档
> - [Chroma文档](https://docs.trychroma.com/) - Chroma官方指南
> - [Pinecone学习中心](https://www.pinecone.io/learn/) - 向量数据库教程
> - [Milvus文档](https://milvus.io/docs) - Milvus官方文档
> - [Qdrant](https://qdrant.tech/documentation/) - 另一个开源选择
> - [Weaviate](https://weaviate.io/developers/weaviate) - 语义搜索引擎
> - [向量数据库对比](https://github.com/erikbern/ann-benchmarks) - 性能基准

---

**上一篇**：[大模型API应用]({{ site.baseurl }}{% post_url /ailearn/06-llm-application/2026-04-16-01-llm-api %})

**返回**：[大模型应用]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-06-llm-application %})

*最后更新: 2026年4月16日*
