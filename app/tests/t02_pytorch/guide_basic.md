# PyTorch 常用函数参考

本文档列出了PyTorch中最常用的函数及其作用，适用于模型训练和开发。

## Tensor创建

### 基础创建

| 函数 | 作用 | 示例 |
|------|------|------|
| `torch.tensor()` | 从数据创建Tensor | `torch.tensor([1, 2, 3])` |
| `torch.zeros()` | 创建全零Tensor | `torch.zeros(3, 4)` |
| `torch.ones()` | 创建全1Tensor | `torch.ones(3, 4)` |
| `torch.empty()` | 创建未初始化Tensor | `torch.empty(3, 4)` |
| `torch.full()` | 创建填充指定值的Tensor | `torch.full((3, 4), 5)` |
| `torch.arange()` | 创建等差Tensor | `torch.arange(0, 10, 2)` |
| `torch.linspace()` | 创建等间隔Tensor | `torch.linspace(0, 1, 5)` |
| `torch.rand()` | 创建[0,1)随机Tensor | `torch.rand(3, 4)` |
| `torch.randn()` | 创建标准正态分布Tensor | `torch.randn(3, 4)` |
| `torch.randint()` | 创建随机整数Tensor | `torch.randint(0, 10, (3, 4))` |
| `torch.eye()` | 创建单位矩阵 | `torch.eye(3)` |

### 从NumPy创建

| 函数 | 作用 | 示例 |
|------|------|------|
| `torch.from_numpy()` | 从NumPy数组创建（共享内存） | `torch.from_numpy(np_arr)` |
| `torch.as_tensor()` | 从数组创建Tensor | `torch.as_tensor(arr)` |

## Tensor属性

| 属性/函数 | 作用 | 示例 |
|-----------|------|------|
| `.shape` | Tensor形状 | `tensor.shape` |
| `.dtype` | 数据类型 | `tensor.dtype` |
| `.device` | 设备（CPU/GPU） | `tensor.device` |
| `.requires_grad` | 是否需要梯度 | `tensor.requires_grad` |
| `.grad` | 梯度值 | `tensor.grad` |
| `.size()` | 获取大小 | `tensor.size()` |
| `.numel()` | 元素总数 | `tensor.numel()` |
| `.dim()` | 维度数 | `tensor.dim()` |

## Tensor操作

### 索引和切片

| 操作 | 作用 | 示例 |
|------|------|------|
| `tensor[i]` | 索引单个元素 | `tensor[0]` |
| `tensor[i:j]` | 切片 | `tensor[1:5]` |
| `tensor[i, j]` | 多维索引 | `tensor[0, 1]` |
| `tensor[:, j]` | 选择列 | `tensor[:, 1]` |
| `tensor[i, :]` | 选择行 | `tensor[1, :]` |
| `tensor[mask]` | 布尔索引 | `tensor[tensor > 5]` |

### 形状操作

| 函数 | 作用 | 示例 |
|------|------|------|
| `.reshape()` | 改变形状 | `tensor.reshape(3, 4)` |
| `.view()` | 改变视图 | `tensor.view(3, 4)` |
| `.flatten()` | 展平 | `tensor.flatten()` |
| `.squeeze()` | 移除单维度 | `tensor.squeeze()` |
| `.unsqueeze()` | 增加维度 | `tensor.unsqueeze(0)` |
| `.transpose()` | 转置 | `tensor.transpose(0, 1)` |
| `.T` | 转置（属性） | `tensor.T` |
| `.permute()` | 维度重排 | `tensor.permute(1, 0, 2)` |

### Tensor连接

| 函数 | 作用 | 示例 |
|------|------|------|
| `torch.cat()` | 连接Tensor | `torch.cat([a, b], dim=0)` |
| `torch.stack()` | 堆叠Tensor | `torch.stack([a, b])` |
| `torch.chunk()` | 分割Tensor | `torch.chunk(tensor, 3)` |
| `torch.split()` | 分割Tensor | `torch.split(tensor, 2)` |

## 数学运算

### 基本运算

| 函数 | 作用 | 示例 |
|------|------|------|
| `torch.add()` | 加法 | `torch.add(a, b)` |
| `torch.sub()` | 减法 | `torch.sub(a, b)` |
| `torch.mul()` | 乘法 | `torch.mul(a, b)` |
| `torch.div()` | 除法 | `torch.div(a, b)` |
| `torch.pow()` | 幂运算 | `torch.pow(a, 2)` |
| `torch.sqrt()` | 平方根 | `torch.sqrt(tensor)` |
| `torch.abs()` | 绝对值 | `torch.abs(tensor)` |
| `torch.sign()` | 符号函数 | `torch.sign(tensor)` |

### 矩阵运算

| 函数 | 作用 | 示例 |
|------|------|------|
| `torch.matmul()` | 矩阵乘法 | `torch.matmul(a, b)` |
| `torch.mm()` | 矩阵乘法（2D） | `torch.mm(a, b)` |
| `torch.bmm()` | 批量矩阵乘法 | `torch.bmm(a, b)` |
| `@` | 矩阵乘法运算符 | `a @ b` |
| `torch.dot()` | 向量点积 | `torch.dot(a, b)` |
| `torch.t()` | 转置 | `torch.t(tensor)` |

### 统计函数

| 函数 | 作用 | 示例 |
|------|------|------|
| `torch.sum()` | 求和 | `torch.sum(tensor)` |
| `torch.mean()` | 平均值 | `torch.mean(tensor)` |
| `torch.median()` | 中位数 | `torch.median(tensor)` |
| `torch.std()` | 标准差 | `torch.std(tensor)` |
| `torch.var()` | 方差 | `torch.var(tensor)` |
| `torch.min()` | 最小值 | `torch.min(tensor)` |
| `torch.max()` | 最大值 | `torch.max(tensor)` |
| `torch.argmin()` | 最小值索引 | `torch.argmin(tensor)` |
| `torch.argmax()` | 最大值索引 | `torch.argmax(tensor)` |

### 按维度操作

| 函数 | 作用 | 示例 |
|------|------|------|
| `torch.sum(dim=0)` | 按维度求和 | `torch.sum(tensor, dim=0)` |
| `torch.mean(dim=1)` | 按维度求平均 | `torch.mean(tensor, dim=1)` |
| `torch.max(dim=0)` | 按维度求最大值 | `torch.max(tensor, dim=0)` |
| `torch.norm()` | 范数 | `torch.norm(tensor, dim=1)` |

## 自动微分（Autograd）

### 梯度计算

| 函数/方法 | 作用 | 示例 |
|-----------|------|------|
| `.requires_grad=True` | 启用梯度计算 | `x = torch.tensor(2.0, requires_grad=True)` |
| `.backward()` | 反向传播 | `loss.backward()` |
| `.grad` | 访问梯度 | `x.grad` |
| `torch.no_grad()` | 禁用梯度 | `with torch.no_grad(): ...` |
| `.detach()` | 分离计算图 | `x.detach()` |
| `.grad_fn` | 梯度函数 | `tensor.grad_fn` |

### 示例

```python
# 创建需要梯度的变量
x = torch.tensor(2.0, requires_grad=True)
y = x ** 2

# 反向传播
y.backward()

# 查看梯度
print(x.grad)  # 4.0
```

## 神经网络模块 (torch.nn)

### 基础层

| 层 | 作用 | 示例 |
|----|------|------|
| `nn.Linear()` | 全连接层 | `nn.Linear(10, 5)` |
| `nn.Conv2d()` | 2D卷积层 | `nn.Conv2d(1, 32, 3)` |
| `nn.Conv1d()` | 1D卷积层 | `nn.Conv1d(1, 32, 3)` |
| `nn.ReLU()` | ReLU激活 | `nn.ReLU()` |
| `nn.Sigmoid()` | Sigmoid激活 | `nn.Sigmoid()` |
| `nn.Tanh()` | Tanh激活 | `nn.Tanh()` |
| `nn.Softmax()` | Softmax激活 | `nn.Softmax(dim=1)` |
| `nn.Dropout()` | Dropout层 | `nn.Dropout(0.5)` |
| `nn.BatchNorm2d()` | 批归一化 | `nn.BatchNorm2d(32)` |

### 池化层

| 层 | 作用 | 示例 |
|----|------|------|
| `nn.MaxPool2d()` | 最大池化 | `nn.MaxPool2d(2, 2)` |
| `nn.AvgPool2d()` | 平均池化 | `nn.AvgPool2d(2, 2)` |
| `nn.AdaptiveAvgPool2d()` | 自适应平均池化 | `nn.AdaptiveAvgPool2d(1)` |

### 损失函数

| 函数 | 作用 | 示例 |
|------|------|------|
| `nn.MSELoss()` | 均方误差 | `nn.MSELoss()` |
| `nn.CrossEntropyLoss()` | 交叉熵 | `nn.CrossEntropyLoss()` |
| `nn.BCELoss()` | 二分类交叉熵 | `nn.BCELoss()` |
| `nn.BCEWithLogitsLoss()` | 带logits的BCE | `nn.BCEWithLogitsLoss()` |
| `nn.NLLLoss()` | 负对数似然 | `nn.NLLLoss()` |
| `nn.L1Loss()` | L1损失 | `nn.L1Loss()` |

### 优化器

| 优化器 | 作用 | 示例 |
|--------|------|------|
| `optim.SGD()` | 随机梯度下降 | `optim.SGD(model.parameters(), lr=0.01)` |
| `optim.Adam()` | Adam优化器 | `optim.Adam(model.parameters(), lr=0.001)` |
| `optim.AdamW()` | AdamW优化器 | `optim.AdamW(model.parameters(), lr=0.001)` |
| `optim.RMSprop()` | RMSprop优化器 | `optim.RMSprop(model.parameters(), lr=0.01)` |
| `.zero_grad()` | 清零梯度 | `optimizer.zero_grad()` |
| `.step()` | 更新参数 | `optimizer.step()` |

## 数据加载 (torch.utils.data)

### Dataset和DataLoader

| 类/函数 | 作用 | 示例 |
|---------|------|------|
| `Dataset` | 数据集基类 | `class MyDataset(Dataset): ...` |
| `DataLoader()` | 数据加载器 | `DataLoader(dataset, batch_size=32)` |
| `TensorDataset()` | Tensor数据集 | `TensorDataset(X, y)` |
| `random_split()` | 随机分割 | `random_split(dataset, [800, 200])` |

### 示例

```python
from torch.utils.data import Dataset, DataLoader

class MyDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

dataset = MyDataset(X, y)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
```

## 设备操作

### GPU/CPU操作

| 函数/方法 | 作用 | 示例 |
|-----------|------|------|
| `torch.cuda.is_available()` | 检查GPU可用 | `torch.cuda.is_available()` |
| `.to(device)` | 移动到设备 | `tensor.to('cuda')` |
| `.cuda()` | 移动到GPU | `tensor.cuda()` |
| `.cpu()` | 移动到CPU | `tensor.cpu()` |
| `torch.device()` | 创建设备对象 | `torch.device('cuda:0')` |

### 示例

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tensor = tensor.to(device)
model = model.to(device)
```

## 模型保存和加载

| 函数 | 作用 | 示例 |
|------|------|------|
| `torch.save()` | 保存模型 | `torch.save(model.state_dict(), 'model.pth')` |
| `torch.load()` | 加载模型 | `model.load_state_dict(torch.load('model.pth'))` |
| `.state_dict()` | 获取状态字典 | `model.state_dict()` |
| `.load_state_dict()` | 加载状态字典 | `model.load_state_dict(state_dict)` |

## 实用函数

### 随机数

| 函数 | 作用 | 示例 |
|------|------|------|
| `torch.manual_seed()` | 设置随机种子 | `torch.manual_seed(42)` |
| `torch.cuda.manual_seed()` | GPU随机种子 | `torch.cuda.manual_seed(42)` |

### 类型转换

| 函数/方法 | 作用 | 示例 |
|-----------|------|------|
| `.float()` | 转为float | `tensor.float()` |
| `.long()` | 转为long | `tensor.long()` |
| `.int()` | 转为int | `tensor.int()` |
| `.double()` | 转为double | `tensor.double()` |
| `.to(torch.float32)` | 类型转换 | `tensor.to(torch.float32)` |

### NumPy互操作

| 函数/方法 | 作用 | 示例 |
|-----------|------|------|
| `.numpy()` | 转为NumPy | `tensor.numpy()` |
| `torch.from_numpy()` | 从NumPy创建 | `torch.from_numpy(np_arr)` |

## 常用模式

### 模型定义模式

```python
import torch.nn as nn

class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.fc1 = nn.Linear(784, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 10)
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x
```

### 训练循环模式

```python
model = MyModel()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(num_epochs):
    for batch_x, batch_y in dataloader:
        # 前向传播
        outputs = model(batch_x)
        loss = criterion(outputs, batch_y)
        
        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

### 评估模式

```python
model.eval()
with torch.no_grad():
    for batch_x, batch_y in dataloader:
        outputs = model(batch_x)
        # 计算指标
```

### 梯度裁剪

```python
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```

## 性能优化

### 使用GPU

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
data = data.to(device)
```

### 禁用梯度计算

```python
with torch.no_grad():
    # 不需要梯度的操作
    output = model(input)
```

### 混合精度训练

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()
with autocast():
    output = model(input)
    loss = criterion(output, target)
```

---

**注意**：本文档重点列出模型训练中最常用的函数。更多详细信息请参考PyTorch官方文档。

