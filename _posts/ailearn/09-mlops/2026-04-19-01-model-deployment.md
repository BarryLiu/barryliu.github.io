---
layout: post
title: "模型部署与服务化 - MLOps实践"
date: 2026-04-19
categories: ailearn
tags: [AI, MLOps, 模型部署]
---

* content
{:toc}

## 一、部署概述

训练 -> 转换 -> 部署 -> 运维

## 二、模型导出

```python
import torch
torch.onnx.export(model, dummy_input, "model.onnx")
```

## 三、API服务

```python
from fastapi import FastAPI
app = FastAPI()

@app.post("/predict")
async def predict(data: Input):
    return model.predict(data)
```

## 四、容器化部署

Docker + Kubernetes

## 五、监控优化

Prometheus + Grafana

---

*最后更新: 2026年4月19日*