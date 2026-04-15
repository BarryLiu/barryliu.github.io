---
layout: post
title: "高级RAG技术 - 提升检索与生成质量"
date: 2026-04-17
categories: ailearn
tags: [AI, RAG, 高级技术]
---

* content
{:toc}

## 一、RAG优化方向

- 混合检索
- 查询重写
- 重排序
- 上下文压缩

## 二、混合检索

```python
# 语义检索 + 关键词检索
from langchain.retrievers import EnsembleRetriever
```

## 三、重排序

使用CrossEncoder对检索结果重新排序

## 四、幻觉检测

验证生成内容是否基于检索内容

---

*最后更新: 2026年4月17日*