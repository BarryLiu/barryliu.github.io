# PyTorch学习包

PyTorch是深度学习的主流框架，主要用于**模型训练和开发**。

## ⚠️ 重要说明

**对于大模型应用开发**：
- ❌ **通常不需要** PyTorch
- ✅ 只需要 NumPy + API调用

**什么时候需要PyTorch**：
- ✅ 训练自己的模型
- ✅ 深度定制微调
- ✅ 研究模型架构
- ✅ 从零开发模型

## 文件说明

### 01_basics.py - 基础操作
- Tensor创建
- Tensor属性
- Tensor运算
- 梯度计算（自动微分）
- GPU操作
- NumPy互操作

**学习时间**：1-2周

### 02_neural_networks.py - 神经网络
- 线性模型
- 多层神经网络
- 训练示例
- CNN（卷积神经网络）
- RNN/LSTM
- Transformer（大模型基础）

**学习时间**：2-3周

### 03_training.py - 完整训练流程
- 数据集和数据加载器
- 完整训练循环
- 模型保存和加载
- 迁移学习

**学习时间**：2-3周

## 学习顺序

1. **基础操作**（01_basics.py）
2. **神经网络**（02_neural_networks.py）
3. **训练流程**（03_training.py）

## 运行示例

```bash
# 需要先安装PyTorch
pip install torch

# 基础操作
python tests/pytorch/01_basics.py

# 神经网络
python tests/pytorch/02_neural_networks.py

# 训练流程
python tests/pytorch/03_training.py
```

## 核心概念

### 自动微分（Autograd）

```python
x = torch.tensor(2.0, requires_grad=True)
y = x ** 2
y.backward()
print(x.grad)  # 4.0
```

### 模型定义

```python
class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 1)
    
    def forward(self, x):
        return self.fc(x)
```

### 训练循环

```python
for epoch in range(num_epochs):
    for batch_x, batch_y in dataloader:
        # 前向传播
        output = model(batch_x)
        loss = criterion(output, batch_y)
        
        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

## 与NumPy的关系

- **NumPy**：CPU计算，用于数据处理
- **PyTorch**：GPU加速，用于模型训练
- **互操作**：可以相互转换

## 学习建议

1. **先掌握NumPy**：NumPy是基础
2. **理解自动微分**：PyTorch的核心
3. **实践训练流程**：完整的训练循环
4. **使用GPU加速**：提高训练效率

## 应用开发 vs 模型训练

| 场景 | 需要PyTorch? | 需要NumPy? |
|------|-------------|-----------|
| API调用大模型 | ❌ | ✅ |
| RAG应用 | ❌ | ✅ |
| Agent开发 | ❌ | ✅ |
| 训练模型 | ✅ | ✅ |
| 微调模型 | ✅ | ✅ |
| 研究模型 | ✅ | ✅ |

## 下一步

如果目标是**应用开发**：
- 回到 NumPy 学习
- 学习 API 调用
- 学习 RAG/Agent

如果目标是**模型训练**：
- 深入学习 PyTorch
- 学习 Transformer 架构
- 学习模型优化

