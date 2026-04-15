---
layout: post
title: "Transformer架构详解 - 注意力机制革命"
date: 2026-04-15
categories: ailearn
tags: [AI, Transformer, 注意力机制, 深度学习]
keywords: Transformer, Self-Attention, 注意力机制, 位置编码, BERT
description: 深入理解Transformer架构，掌握自注意力机制原理与实现
---

* content
{:toc}

> **前置知识**：需要先掌握 [NLP基础]({{ site.baseurl }}{% post_url /ailearn/04-nlp-basics/2026-04-15-01-nlp-overview %}) 和 [RNN]({{ site.baseurl }}{% post_url /ailearn/03-deep-learning/2026-04-14-03-rnn %})
>
> **本文重点**：理解Transformer核心原理，掌握注意力机制

---

## 一、Transformer概述

### 1.1 为什么需要Transformer

RNN/LSTM的问题：
- **顺序计算**：无法并行
- **长距离依赖**：信息衰减
- **梯度问题**：难以训练深层网络

Transformer的优势：
- **完全并行**：所有位置同时计算
- **全局依赖**：任意位置直接连接
- **可扩展**：支持更大模型和数据

### 1.2 架构概览

```
Transformer架构:
┌─────────────────────────────┐
│         Output Layer        │
├─────────────────────────────┤
│  Decoder (Nx layers)        │
│  ├── Masked Self-Attention  │
│  ├── Cross-Attention        │
│  └── Feed Forward           │
├─────────────────────────────┤
│  Encoder (Nx layers)        │
│  ├── Self-Attention         │
│  └── Feed Forward           │
├─────────────────────────────┤
│    Input Embedding + PE     │
└─────────────────────────────┘
```

---

## 二、注意力机制

### 2.1 Scaled Dot-Product Attention

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Scaled Dot-Product Attention
    
    Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V
    
    Args:
        Q: (batch, heads, seq_len, d_k)
        K: (batch, heads, seq_len, d_k)
        V: (batch, heads, seq_len, d_v)
        mask: 可选的mask
    """
    d_k = Q.size(-1)
    
    # 计算注意力分数
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
    
    # 应用mask (用于decoder)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    
    # Softmax归一化
    attention_weights = F.softmax(scores, dim=-1)
    
    # 加权求和
    output = torch.matmul(attention_weights, V)
    
    return output, attention_weights

# 演示
batch_size, heads, seq_len, d_k = 2, 8, 10, 64
Q = torch.randn(batch_size, heads, seq_len, d_k)
K = torch.randn(batch_size, heads, seq_len, d_k)
V = torch.randn(batch_size, heads, seq_len, d_k)

output, weights = scaled_dot_product_attention(Q, K, V)
print(f"输出形状: {output.shape}")       # (2, 8, 10, 64)
print(f"注意力权重形状: {weights.shape}") # (2, 8, 10, 10)
```

### 2.2 Multi-Head Attention

```python
class MultiHeadAttention(nn.Module):
    """多头注意力机制"""
    
    def __init__(self, d_model, num_heads):
        super(MultiHeadAttention, self).__init__()
        
        assert d_model % num_heads == 0
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # Q, K, V 线性层
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        
        # 输出线性层
        self.W_o = nn.Linear(d_model, d_model)
    
    def forward(self, x, mask=None):
        batch_size = x.size(0)
        
        # 线性变换
        Q = self.W_q(x)  # (batch, seq, d_model)
        K = self.W_k(x)
        V = self.W_v(x)
        
        # 分割为多头
        Q = Q.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = K.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = V.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        
        # 注意力计算
        attn_output, _ = scaled_dot_product_attention(Q, K, V, mask)
        
        # 合并多头
        attn_output = attn_output.transpose(1, 2).contiguous()
        attn_output = attn_output.view(batch_size, -1, self.d_model)
        
        # 输出投影
        output = self.W_o(attn_output)
        
        return output

# 测试
d_model, num_heads = 512, 8
mha = MultiHeadAttention(d_model, num_heads)
x = torch.randn(2, 10, d_model)
output = mha(x)
print(f"多头注意力输出形状: {output.shape}")
```

### 2.3 位置编码

```python
class PositionalEncoding(nn.Module):
    """位置编码"""
    
    def __init__(self, d_model, max_len=5000):
        super(PositionalEncoding, self).__init__()
        
        # 创建位置编码矩阵
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        
        # 计算sin/cos
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        pe = pe.unsqueeze(0)  # (1, max_len, d_model)
        self.register_buffer('pe', pe)
    
    def forward(self, x):
        # x: (batch, seq_len, d_model)
        x = x + self.pe[:, :x.size(1), :]
        return x

# 可视化位置编码
import matplotlib.pyplot as plt

pe = PositionalEncoding(128, max_len=100)
plt.figure(figsize=(12, 6))
plt.imshow(pe.pe[0, :, :].numpy().T, aspect='auto', cmap='viridis')
plt.xlabel('Position')
plt.ylabel('Dimension')
plt.title('Positional Encoding Visualization')
plt.colorbar()
plt.savefig('positional_encoding.png', dpi=100, bbox_inches='tight')
plt.close()
```

---

## 三、Transformer实现

### 3.1 Feed Forward Network

```python
class PositionwiseFeedForward(nn.Module):
    """前馈网络"""
    
    def __init__(self, d_model, d_ff, dropout=0.1):
        super(PositionwiseFeedForward, self).__init__()
        
        self.fc1 = nn.Linear(d_model, d_ff)
        self.fc2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x
```

### 3.2 Encoder Layer

```python
class EncoderLayer(nn.Module):
    """Transformer编码器层"""
    
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super(EncoderLayer, self).__init__()
        
        self.self_attn = MultiHeadAttention(d_model, num_heads)
        self.ffn = PositionwiseFeedForward(d_model, d_ff, dropout)
        
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, mask=None):
        # 自注意力 + 残差连接 + LayerNorm
        attn_out = self.self_attn(x, mask)
        x = self.norm1(x + self.dropout(attn_out))
        
        # FFN + 残差连接 + LayerNorm
        ffn_out = self.ffn(x)
        x = self.norm2(x + self.dropout(ffn_out))
        
        return x
```

### 3.3 完整Transformer

```python
class TransformerEncoder(nn.Module):
    """Transformer编码器"""
    
    def __init__(self, vocab_size, d_model, num_heads, d_ff, num_layers, num_classes, dropout=0.1):
        super(TransformerEncoder, self).__init__()
        
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoding = PositionalEncoding(d_model)
        
        self.layers = nn.ModuleList([
            EncoderLayer(d_model, num_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])
        
        self.fc = nn.Linear(d_model, num_classes)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, mask=None):
        # 词嵌入 + 位置编码
        x = self.embedding(x)
        x = self.pos_encoding(x)
        x = self.dropout(x)
        
        # 编码器层
        for layer in self.layers:
            x = layer(x, mask)
        
        # 分类 (取第一个token或平均)
        x = x.mean(dim=1)  # 或 x[:, 0, :] 使用[CLS]
        x = self.fc(x)
        
        return x

# 创建模型
model = TransformerEncoder(
    vocab_size=10000,
    d_model=256,
    num_heads=8,
    d_ff=1024,
    num_layers=4,
    num_classes=2
)

print("Transformer编码器:")
print(model)

# 参数量
total_params = sum(p.numel() for p in model.parameters())
print(f"\n参数量: {total_params:,}")
```

---

## 四、注意力可视化

```python
def visualize_attention(attention_weights, tokens=None):
    """可视化注意力权重"""
    import seaborn as sns
    
    # 取第一个样本的第一个头
    weights = attention_weights[0, 0].detach().numpy()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(weights, cmap='Blues', annot=True, fmt='.2f')
    
    if tokens:
        plt.xticks(range(len(tokens)), tokens, rotation=45)
        plt.yticks(range(len(tokens)), tokens, rotation=0)
    
    plt.xlabel('Key')
    plt.ylabel('Query')
    plt.title('Self-Attention Weights')
    plt.tight_layout()
    plt.savefig('attention_visualization.png', dpi=100, bbox_inches='tight')
    plt.close()

# 示例
tokens = ['The', 'cat', 'sat', 'on', 'the', 'mat']
seq_len = len(tokens)
d_model = 64

# 模拟注意力权重
attention = F.softmax(torch.randn(1, 8, seq_len, seq_len), dim=-1)
visualize_attention(attention, tokens)
```

---

## 参考资源

> - [Attention Is All You Need](https://arxiv.org/abs/1706.03762) - Transformer原始论文
> - [The Annotated Transformer](https://nlp.seas.harvard.edu/annotated-transformer/) - 论文逐行解析
> - [Transformer可视化解释](https://jalammar.github.io/illustrated-transformer/) - Jay Alammar博客
> - [BERT论文](https://arxiv.org/abs/1810.04805) - BERT: Pre-training of Deep Bidirectional Transformers
> - [GPT论文](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) - GPT-2论文
> - [Hugging Face Transformers](https://huggingface.co/docs/transformers/) - 预训练模型库
> - [The Illustrated BERT](https://jalammar.github.io/illustrated-bert/) - BERT可视化
> - [Annotated BERT](https://github.com/codertimo/BERT-pytorch) - BERT PyTorch实现

---

**上一篇**：[NLP基础]({{ site.baseurl }}{% post_url /ailearn/04-nlp-basics/2026-04-15-01-nlp-overview %})

**下一篇**：[大模型应用开发]({{ site.baseurl }}{% post_url /ailearn/06-llm-application/2026-04-16-01-llm-api %})

**返回**：[Transformer进阶]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-05-transformer-advanced %})

*最后更新: 2026年4月15日*
