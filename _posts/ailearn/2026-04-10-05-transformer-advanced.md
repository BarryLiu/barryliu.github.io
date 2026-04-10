---
layout: post
title: "【AI学习路线 05】Transformer进阶 - 深入理解注意力机制"
date: 2026-04-10
categories: ailearn
tags: [AI, Transformer, 注意力机制, 多头注意力, 位置编码]
keywords: Transformer, 注意力机制, 多头注意力, 位置编码, LayerNorm, 残差连接
description: AI学习路线第5篇 - 深入理解Transformer架构细节，掌握多头注意力、位置编码等核心组件
---

* content
{:toc}

> **学习顺序说明**：本文是AI学习路线的第5篇，建议按顺序学习：
> - 01 入门基础 → 02 机器学习 → 03 深度学习 → 04 NLP基础 → 05 Transformer进阶（本文）→ 06 大模型应用 → 07 RAG系统 → 08 AI工具链

本文将深入探讨Transformer架构的各个组件，帮助读者理解这一革命性架构的设计原理。

## Transformer整体架构

```
Encoder端:
输入 → 词嵌入 → 位置编码 → [多头自注意力 → Add&Norm → 前馈网络 → Add&Norm] × N

Decoder端:
输出 → 词嵌入 → 位置编码 → [掩码多头自注意力 → Add&Norm → 编码器-解码器注意力 → Add&Norm → 前馈网络 → Add&Norm] × N → 线性 → Softmax
```

> **参考资源**：[Attention Is All You Need](https://arxiv.org/abs/1706.03762) - Transformer原论文

---

## 第一部分：注意力机制详解

### 1.1 缩放点积注意力

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

**为什么要除以√d_k？**

当d_k很大时，点积的结果会变得很大，导致softmax函数的梯度变得很小（饱和区）。除以√d_k可以防止这种情况。

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class ScaledDotProductAttention(nn.Module):
    """缩放点积注意力"""
    
    def __init__(self, d_k):
        super().__init__()
        self.scale = math.sqrt(d_k)
    
    def forward(self, Q, K, V, mask=None):
        # Q: (batch, heads, seq_len, d_k)
        # K: (batch, heads, seq_len, d_k)
        # V: (batch, heads, seq_len, d_v)
        
        # 计算注意力分数
        scores = torch.matmul(Q, K.transpose(-2, -1)) / self.scale
        
        # 应用掩码（用于解码器）
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        
        # Softmax归一化
        attention_weights = F.softmax(scores, dim=-1)
        
        # 加权求和
        output = torch.matmul(attention_weights, V)
        
        return output, attention_weights
```

### 1.2 多头注意力

**为什么需要多头？**

单头注意力只能学习一种"关联模式"，多头可以让模型同时关注不同位置的不同表示子空间。

```python
class MultiHeadAttention(nn.Module):
    """多头注意力机制"""
    
    def __init__(self, d_model, num_heads):
        super().__init__()
        assert d_model % num_heads == 0
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # Q, K, V 的线性变换
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        
        # 输出线性变换
        self.W_o = nn.Linear(d_model, d_model)
        
        self.attention = ScaledDotProductAttention(self.d_k)
    
    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)
        
        # 线性变换并分割多头
        Q = self.W_q(query).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(key).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(value).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        
        # 注意力计算
        attn_output, attention_weights = self.attention(Q, K, V, mask)
        
        # 合并多头
        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)
        
        # 输出变换
        output = self.W_o(attn_output)
        
        return output, attention_weights
```

**三种注意力类型**：

| 类型 | Query来源 | Key/Value来源 | 应用场景 |
|------|----------|---------------|---------|
| 自注意力 | 输入序列 | 输入序列 | 编码器、解码器 |
| 掩码自注意力 | 输出序列 | 输出序列 | 解码器 |
| 交叉注意力 | 解码器输入 | 编码器输出 | 编码器-解码器 |

> **参考资源**：[The Annotated Transformer](https://nlp.seas.harvard.edu/2018/04/03/attention.html) - 带注释的Transformer实现

---

## 第二部分：位置编码

### 2.1 正弦位置编码

由于Transformer没有循环结构，需要位置编码来注入位置信息。

$$PE_{(pos, 2i)} = \sin(pos / 10000^{2i/d_{model}})$$
$$PE_{(pos, 2i+1)} = \cos(pos / 10000^{2i/d_{model}})$$

```python
class PositionalEncoding(nn.Module):
    """正弦位置编码"""
    
    def __init__(self, d_model, max_len=5000, dropout=0.1):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)
        
        # 计算位置编码
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        pe = pe.unsqueeze(0)  # (1, max_len, d_model)
        self.register_buffer('pe', pe)
    
    def forward(self, x):
        # x: (batch, seq_len, d_model)
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)
```

### 2.2 可学习位置编码

```python
class LearnedPositionalEncoding(nn.Module):
    """可学习位置编码"""
    
    def __init__(self, d_model, max_len=512):
        super().__init__()
        self.pos_embedding = nn.Embedding(max_len, d_model)
    
    def forward(self, x):
        batch_size, seq_len, _ = x.size()
        positions = torch.arange(seq_len, device=x.device).unsqueeze(0).expand(batch_size, -1)
        return x + self.pos_embedding(positions)
```

### 2.3 旋转位置编码 (RoPE)

RoPE是LLaMA等现代大模型使用的位置编码方式。

```python
class RotaryPositionalEmbedding(nn.Module):
    """旋转位置编码 (RoPE)"""
    
    def __init__(self, dim, max_seq_len=2048, base=10000):
        super().__init__()
        
        inv_freq = 1.0 / (base ** (torch.arange(0, dim, 2).float() / dim))
        self.register_buffer('inv_freq', inv_freq)
        
        # 预计算cos和sin
        self.max_seq_len = max_seq_len
        self._set_cos_sin_cache(max_seq_len)
    
    def _set_cos_sin_cache(self, seq_len):
        t = torch.arange(seq_len, device=self.inv_freq.device, dtype=self.inv_freq.dtype)
        freqs = torch.outer(t, self.inv_freq)
        emb = torch.cat((freqs, freqs), dim=-1)
        self.register_buffer('cos_cached', emb.cos())
        self.register_buffer('sin_cached', emb.sin())
    
    def forward(self, x, seq_len=None):
        return self.cos_cached[:seq_len], self.sin_cached[:seq_len]
```

> **参考资源**：[RoFormer论文](https://arxiv.org/abs/2104.09864) - RoPE原始论文

---

## 第三部分：前馈网络与归一化

### 3.1 前馈网络 (FFN)

```python
class FeedForward(nn.Module):
    """前馈网络"""
    
    def __init__(self, d_model, d_ff, dropout=0.1):
        super().__init__()
        self.linear1 = nn.Linear(d_model, d_ff)
        self.linear2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)
        self.activation = nn.GELU()  # 或 nn.ReLU()
    
    def forward(self, x):
        return self.linear2(self.dropout(self.activation(self.linear1(x))))
```

**激活函数选择**：
- ReLU: 原始Transformer使用
- GELU: BERT、GPT使用，更平滑
- Swish/GLU: LLaMA、PaLM使用

### 3.2 Layer Normalization

```python
class LayerNorm(nn.Module):
    """层归一化"""
    
    def __init__(self, d_model, eps=1e-6):
        super().__init__()
        self.gamma = nn.Parameter(torch.ones(d_model))
        self.beta = nn.Parameter(torch.zeros(d_model))
        self.eps = eps
    
    def forward(self, x):
        mean = x.mean(-1, keepdim=True)
        std = x.std(-1, keepdim=True)
        return self.gamma * (x - mean) / (std + self.eps) + self.beta
```

**Pre-LN vs Post-LN**：

| 方式 | 公式 | 特点 |
|------|------|------|
| Post-LN | x + Sublayer(LN(x)) | 原始Transformer，训练不稳定 |
| Pre-LN | LN(x + Sublayer(x)) | 现代模型常用，训练稳定 |

```python
class TransformerBlock(nn.Module):
    """Pre-LN Transformer块"""
    
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.attention = MultiHeadAttention(d_model, num_heads)
        self.ffn = FeedForward(d_model, d_ff, dropout)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, mask=None):
        # Pre-LN结构
        # 自注意力
        attn_out, _ = self.attention(self.norm1(x), self.norm1(x), self.norm1(x), mask)
        x = x + self.dropout(attn_out)
        
        # 前馈网络
        ffn_out = self.ffn(self.norm2(x))
        x = x + self.dropout(ffn_out)
        
        return x
```

---

## 第四部分：完整Transformer实现

```python
class TransformerEncoder(nn.Module):
    """Transformer编码器"""
    
    def __init__(self, vocab_size, d_model, num_heads, num_layers, d_ff, max_seq_len, dropout=0.1):
        super().__init__()
        
        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.position_encoding = PositionalEncoding(d_model, max_seq_len, dropout)
        
        self.layers = nn.ModuleList([
            TransformerBlock(d_model, num_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])
        
        self.norm = nn.LayerNorm(d_model)
    
    def forward(self, x, mask=None):
        # 词嵌入 + 位置编码
        x = self.token_embedding(x)
        x = self.position_encoding(x)
        
        # Transformer层
        for layer in self.layers:
            x = layer(x, mask)
        
        return self.norm(x)
```

---

## 变体架构

### 4.1 Encoder-Only (BERT系列)

- 双向注意力
- 适合理解任务：分类、NER、问答

### 4.2 Decoder-Only (GPT系列)

- 单向（因果）注意力
- 适合生成任务：文本生成、代码生成

### 4.3 Encoder-Decoder (T5, BART)

- 完整Transformer结构
- 适合序列到序列任务：翻译、摘要

---

## 学习资源

### 经典论文
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) - Transformer原论文
- [BERT](https://arxiv.org/abs/1810.04805) - 双向编码器
- [GPT-2](https://d4mucfpksywv.cloudfront.net/better-language-models/language-models.pdf) - 自回归解码器
- [RoFormer](https://arxiv.org/abs/2104.09864) - RoPE位置编码

### 代码实现
- [The Annotated Transformer](https://nlp.seas.harvard.edu/2018/04/03/attention.html)
- [Hugging Face Transformers](https://github.com/huggingface/transformers)

---

**上一篇**：[04 NLP基础 - 从词向量到Transformer]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-04-nlp-basics %})

**下一篇**：[06 大模型应用 - 从Prompt工程到微调技术]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-06-llm-application %})

*最后更新: 2026年4月10日*

> 本文参考了 [Attention Is All You Need](https://arxiv.org/abs/1706.03762) 和 [The Annotated Transformer](https://nlp.seas.harvard.edu/2018/04/03/attention.html) 整理
