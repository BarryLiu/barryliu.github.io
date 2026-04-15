---
layout: post
title: "AI项目实战 - 智能搜索引擎"
date: 2026-04-20
categories: ailearn
tags: [AI, 项目实战, 搜索引擎, RAG]
keywords: 智能搜索, 语义检索, 混合搜索, 重排序
---

* content
{:toc}

> **前置知识**：需要先掌握 RAG基础
>
> **本文重点**：智能搜索引擎设计与实现

---

## 一、搜索引擎架构

```
智能搜索引擎架构：

用户查询 → 查询理解 → 检索 → 重排序 → 生成
                ↓          ↓        ↓
            意图识别    混合检索   LLM增强
                ↓          ↓        ↓
            查询改写    向量+关键词  答案生成
```

---

## 二、查询处理

### 2.1 查询理解

```python
from openai import OpenAI

class QueryUnderstanding:
    """查询理解"""
    
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    
    def analyze_intent(self, query):
        """分析查询意图"""
        prompt = f"""
        分析以下查询的意图，返回JSON格式：
        查询：{query}
        
        返回格式：
        {{
            "intent": "信息查询/比较/导航/交易",
            "entities": ["实体1", "实体2"],
            "keywords": ["关键词1", "关键词2"],
            "query_type": "事实/观点/导航"
        }}
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        import json
        return json.loads(response.choices[0].message.content)
    
    def rewrite_query(self, query):
        """查询改写"""
        prompt = f"""
        将以下查询改写为更适合检索的形式：
        原查询：{query}
        
        要求：
        1. 补充缺失的关键词
        2. 修正拼写错误
        3. 展开缩写
        4. 保留原始语义
        
        直接返回改写后的查询。
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content
    
    def expand_query(self, query):
        """查询扩展"""
        prompt = f"""
        对以下查询进行同义词扩展：
        查询：{query}
        
        返回3-5个相关查询，JSON数组格式。
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        import json
        return json.loads(response.choices[0].message.content)
```

---

## 三、混合检索

### 3.1 向量检索 + 关键词检索

```python
from rank_bm25 import BM25
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import numpy as np

class HybridSearch:
    """混合检索"""
    
    def __init__(self, documents):
        self.documents = documents
        self.texts = [doc["content"] for doc in documents]
        
        # BM25
        tokenized = [doc.split() for doc in self.texts]
        self.bm25 = BM25(tokenized)
        
        # 向量检索
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma.from_texts(
            self.texts,
            self.embeddings,
            metadatas=documents
        )
    
    def search(self, query, top_k=10, alpha=0.5):
        """混合搜索
        
        Args:
            query: 查询文本
            top_k: 返回结果数
            alpha: 向量检索权重 (0-1)，关键词权重为 1-alpha
        """
        # BM25检索
        bm25_scores = self.bm25.get_scores(query.split())
        bm25_results = [
            {"doc": self.documents[i], "score": score}
            for i, score in enumerate(bm25_scores)
        ]
        bm25_results.sort(key=lambda x: x["score"], reverse=True)
        
        # 向量检索
        vector_results = self.vectorstore.similarity_search_with_score(query, k=top_k)
        vector_results = [
            {"doc": doc.metadata, "score": 1 - score}  # 距离转相似度
            for doc, score in vector_results
        ]
        
        # 融合分数
        combined = {}
        
        for i, result in enumerate(bm25_results[:top_k]):
            doc_id = result["doc"].get("id", i)
            combined[doc_id] = combined.get(doc_id, 0)
            combined[doc_id] += (1 - alpha) * (1 / (i + 1))  # RRF
        
        for i, result in enumerate(vector_results):
            doc_id = result["doc"].get("id", i)
            combined[doc_id] = combined.get(doc_id, 0)
            combined[doc_id] += alpha * (1 / (i + 1))  # RRF
        
        # 排序
        ranked = sorted(combined.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for doc_id, score in ranked[:top_k]:
            doc = next((d for d in self.documents if d.get("id") == doc_id), None)
            if doc:
                results.append({"document": doc, "score": score})
        
        
        return results
```

---

## 四、重排序

```python
class ReRanker:
    """重排序器"""
    
    def __init__(self, model="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        from sentence_transformers import CrossEncoder
        self.model = CrossEncoder(model)
    
    def rerank(self, query, documents, top_k=5):
        """重排序"""
        # 准备输入对
        pairs = [(query, doc["content"]) for doc in documents]
        
        # 计算相关性分数
        scores = self.model.predict(pairs)
        
        # 排序
        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [{"document": doc, "rerank_score": score} for doc, score in ranked[:top_k]]
```

---

## 五、完整搜索引擎

```python
class AISearchEngine:
    """智能搜索引擎"""
    
    def __init__(self, documents, openai_api_key):
        self.query_understanding = QueryUnderstanding(openai_api_key)
        self.hybrid_search = HybridSearch(documents)
        self.reranker = ReRanker()
        self.client = OpenAI(api_key=openai_api_key)
    
    def search(self, query, top_k=5):
        """搜索"""
        # 1. 查询理解
        intent = self.query_understanding.analyze_intent(query)
        rewritten = self.query_understanding.rewrite_query(query)
        
        # 2. 混合检索
        results = self.hybrid_search.search(rewritten, top_k=top_k * 2)
        
        # 3. 重排序
        docs = [r["document"] for r in results]
        reranked = self.reranker.rerank(rewritten, docs, top_k=top_k)
        
        # 4. 生成答案
        answer = self._generate_answer(query, reranked)
        
        return {
            "query": query,
            "rewritten_query": rewritten,
            "intent": intent,
            "answer": answer,
            "results": reranked
        }
    
    def _generate_answer(self, query, results):
        """生成答案"""
        context = "\n\n".join([
            r["document"]["content"]
            for r in results[:3]
        ])
        
        prompt = f"""
        基于以下搜索结果回答问题：
        
        问题：{query}
        
        搜索结果：
        {context}
        
        请给出简洁准确的回答：
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content

# 使用示例
documents = [
    {"id": "1", "content": "Python是一种高级编程语言...", "title": "Python简介"},
    {"id": "2", "content": "机器学习是人工智能的一个分支...", "title": "机器学习概述"}
]

engine = AISearchEngine(documents, "your-api-key")
result = engine.search("什么是机器学习")
print(result["answer"])
```

---

## 参考资源

> - [BM25算法](https://en.wikipedia.org/wiki/Okapi_BM25)
> - [ColBERT](https://github.com/stanford-futuredata/ColBERT)
> - [混合搜索最佳实践](https://www.pinecone.io/learn/hybrid-search/)

---

**返回**：[AI项目实战]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-12-ai-project %})

*最后更新: 2026年4月20日*