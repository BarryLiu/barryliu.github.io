---
layout: post
title: "【AI学习路线 03】深度学习基础 - 神经网络理论与实践"
date: 2026-04-10
categories: ailearn
tags: [AI, 深度学习, 神经网络, PyTorch, CNN, RNN]
keywords: 深度学习, 神经网络, 卷积神经网络, 循环神经网络, 反向传播, PyTorch
description: AI学习路线第3篇 - 从神经网络基础概念到CNN、RNN等核心架构，结合PyTorch实践代码
---

* content
{:toc}

> **学习顺序说明**：本文是AI学习路线的第3篇，建议按顺序学习：
> - 01 入门基础 → 02 机器学习 → 03 深度学习（本文）→ 04 NLP基础 → 05 Transformer进阶 → 06 大模型应用 → 07 RAG系统 → 08 AI工具链

深度学习是机器学习的一个子领域，通过多层神经网络自动学习数据的层次化表示。本文将介绍深度学习的核心概念和主流架构。

## 深度学习概述

### 发展历程

```
感知机(1958) → 多层感知机(1986) → CNN(1998) → 深度学习复兴(2012) → Transformer(2017) → 大模型时代(2020+)
```

### 核心优势

- **自动特征提取**：无需人工设计特征，网络自动学习
- **层次化表示**：从低级特征到高级语义的逐层抽象
- **端到端学习**：直接从输入到输出的优化

> **参考资源**：[Deep Learning Book](https://www.deeplearningbook.org/) - Ian Goodfellow等人所著的深度学习圣经

---

## 第一部分：神经网络基础

### 1.1 感知机与多层感知机

**感知机**是最简单的神经网络，模拟单个神经元的工作方式。

```python
import numpy as np

class Perceptron:
    """简单感知机实现"""
    
    def __init__(self, input_size, learning_rate=0.1, epochs=100):
        self.weights = np.zeros(input_size)
        self.bias = 0
        self.lr = learning_rate
        self.epochs = epochs
    
    def activation(self, x):
        """阶跃激活函数"""
        return 1 if x >= 0 else 0
    
    def predict(self, x):
        """前向传播"""
        z = np.dot(x, self.weights) + self.bias
        return self.activation(z)
    
    def train(self, X, y):
        """训练感知机"""
        for epoch in range(self.epochs):
            for i in range(len(X)):
                y_pred = self.predict(X[i])
                error = y[i] - y_pred
                self.weights += self.lr * error * X[i]
                self.bias += self.lr * error

# 示例：实现AND逻辑门
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([0, 0, 0, 1])
perceptron = Perceptron(input_size=2)
perceptron.train(X, y)
```

**多层感知机(MLP)**通过添加隐藏层解决非线性问题。

```python
import torch
import torch.nn as nn

class MLP(nn.Module):
    """多层感知机"""
    
    def __init__(self, input_size, hidden_size, output_size):
        super(MLP, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.activation = nn.ReLU()
        self.layer2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        x = self.layer1(x)
        x = self.activation(x)
        x = self.layer2(x)
        return x

model = MLP(input_size=784, hidden_size=256, output_size=10)
```

### 1.2 激活函数

激活函数引入非线性，使神经网络能够学习复杂的模式。

```python
import torch
import matplotlib.pyplot as plt

x = torch.linspace(-5, 5, 100)

# 常用激活函数
sigmoid = torch.sigmoid(x)
tanh = torch.tanh(x)
relu = torch.relu(x)
leaky_relu = torch.nn.functional.leaky_relu(x, negative_slope=0.1)
gelu = torch.nn.functional.gelu(x)
```

**激活函数对比**：

| 函数 | 公式 | 优点 | 缺点 |
|------|------|------|------|
| Sigmoid | σ(x) = 1/(1+e⁻ˣ) | 输出[0,1] | 梯度消失、非零中心 |
| Tanh | tanh(x) | 零中心 | 梯度消失 |
| ReLU | max(0, x) | 计算快、无梯度消失 | 神经元死亡 |
| LeakyReLU | max(αx, x) | 解决死亡问题 | 需调参 |
| GELU | x·Φ(x) | 平滑、大模型常用 | 计算较慢 |

### 1.3 反向传播算法

**反向传播**是训练神经网络的核心算法，通过链式法则计算梯度。

```python
import torch
import torch.nn as nn

# PyTorch自动求导
x = torch.randn(10, 5, requires_grad=True)
y = torch.randn(10, 2)

model = nn.Sequential(
    nn.Linear(5, 10),
    nn.ReLU(),
    nn.Linear(10, 2)
)

# 前向传播
output = model(x)
loss = nn.MSELoss()(output, y)

# 反向传播（自动计算梯度）
loss.backward()

# 查看梯度
print("第一层权重梯度形状:", model[0].weight.grad.shape)
```

> **参考资源**：[Calculus on Computational Graphs](http://colah.github.io/posts/2015-08-Backprop/) - Christopher Olah的博客

---

## 第二部分：卷积神经网络 (CNN)

CNN是处理图像数据的核心架构，通过卷积操作提取局部特征。

### 2.1 卷积操作原理

```python
import torch.nn as nn

# 单通道卷积示例
conv = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=3, stride=1, padding=1)

# 输入图像 (batch, channels, height, width)
x = torch.randn(1, 1, 28, 28)
output = conv(x)
print(f"输入形状: {x.shape}, 输出形状: {output.shape}")

# 多通道卷积
conv_multi = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, padding=1)
x_rgb = torch.randn(1, 3, 224, 224)
output = conv_multi(x_rgb)
```

**卷积参数详解**：

| 参数 | 说明 | 影响 |
|------|------|------|
| kernel_size | 卷积核大小 | 感受野大小 |
| stride | 步长 | 输出尺寸 |
| padding | 填充 | 保持尺寸 |
| dilation | 空洞率 | 扩大感受野 |

### 2.2 经典CNN架构

**ResNet残差块** (2015) - 解决深层网络训练问题

```python
class ResidualBlock(nn.Module):
    """ResNet残差块"""
    
    def __init__(self, in_channels, out_channels, stride=1):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, 
                               stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3,
                               stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, 
                         stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
    
    def forward(self, x):
        identity = self.shortcut(x)
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += identity  # 残差连接
        return self.relu(out)
```

> **参考资源**：[ResNet论文](https://arxiv.org/abs/1512.03385) - Deep Residual Learning for Image Recognition

---

## 第三部分：循环神经网络 (RNN)

RNN专门处理序列数据，如文本、时间序列等。

### 3.1 LSTM

LSTM通过门控机制解决RNN的长期依赖问题。

```python
class LSTMModel(nn.Module):
    """LSTM模型"""
    
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, 
                           batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        out, (hn, cn) = self.lstm(x, (h0, c0))
        return self.fc(out[:, -1, :])
```

**LSTM门控机制**：

```
遗忘门: f_t = σ(W_f · [h_{t-1}, x_t] + b_f)
输入门: i_t = σ(W_i · [h_{t-1}, x_t] + b_i)
细胞状态: C_t = f_t * C_{t-1} + i_t * C̃_t
输出门: o_t = σ(W_o · [h_{t-1}, x_t] + b_o)
隐藏状态: h_t = o_t * tanh(C_t)
```

> **参考资源**：[Understanding LSTM Networks](http://colah.github.io/posts/2015-08-Understanding-LSTMs/)

**RNN架构对比**：

| 特性 | RNN | LSTM | GRU |
|------|-----|------|-----|
| 参数量 | 少 | 多 | 中 |
| 训练速度 | 快 | 慢 | 中 |
| 长期依赖 | 差 | 好 | 好 |

---

## 第四部分：训练技巧

### 4.1 正则化技术

```python
import torch.nn as nn

# Dropout
dropout = nn.Dropout(0.5)

# Batch Normalization
bn = nn.BatchNorm1d(20)

# Layer Normalization (Transformer常用)
ln = nn.LayerNorm(20)

# 权重衰减 (L2正则化)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)
```

### 4.2 学习率调度

```python
from torch.optim.lr_scheduler import StepLR, CosineAnnealingLR, ReduceLROnPlateau

model = nn.Linear(10, 2)
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

# 阶梯式衰减
scheduler_step = StepLR(optimizer, step_size=30, gamma=0.1)

# 余弦退火
scheduler_cosine = CosineAnnealingLR(optimizer, T_max=100)

# 基于指标的自适应调整
scheduler_reduce = ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=10)
```

---

## 学习资源汇总

### 官方文档
- [PyTorch官方文档](https://pytorch.org/docs/stable/index.html)
- [PyTorch教程](https://pytorch.org/tutorials/)

### 经典课程
- [CS231n: CNN for Visual Recognition](http://cs231n.stanford.edu/) - Stanford
- [Deep Learning Specialization](https://www.coursera.org/specializations/deep-learning) - Andrew Ng
- [d2l.ai](https://d2l.ai/) - 动手学深度学习

### 推荐书籍
- 《深度学习》- Ian Goodfellow (花书)
- 《动手学深度学习》- 李沐等
- 《Python深度学习》- François Chollet

---

**上一篇**：[02 机器学习基础 - 从算法原理到实践]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-02-machine-learning %})

**下一篇**：[04 NLP基础 - 从词向量到Transformer]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-04-nlp-basics %})

*最后更新: 2026年4月10日*

> 本文参考了 [PyTorch官方文档](https://pytorch.org/docs/stable/) 和 [Deep Learning Book](https://www.deeplearningbook.org/) 整理
