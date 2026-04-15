---
layout: post
title: "深度学习训练技巧 - 优化与正则化"
date: 2026-04-14
categories: ailearn
tags: [AI, 深度学习, 优化, 正则化]
keywords: 深度学习优化, 正则化, 学习率调度, 梯度问题
description: 掌握深度学习训练核心技巧，提升模型训练效果
---

* content
{:toc}

> **前置知识**：需要先掌握 [神经网络基础]({{ site.baseurl }}{% post_url /ailearn/03-deep-learning/2026-04-14-01-nn-basics %})
>
> **本文重点**：训练技巧、优化算法、正则化方法

---

## 一、优化算法

### 1.1 梯度下降变体

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

"""
梯度下降算法演进：

1. SGD (Stochastic Gradient Descent)
   θ = θ - lr * ∇θ
   
2. Momentum
   v = β * v + ∇θ
   θ = θ - lr * v
   积累历史梯度，加速收敛

3. NAG (Nesterov Accelerated Gradient)
   先"预测"再计算梯度
   
4. AdaGrad
   自适应学习率，适合稀疏数据
   
5. RMSprop
   解决AdaGrad学习率衰减问题
   
6. Adam
   结合Momentum和RMSprop
   最常用的优化器
"""

# 创建示例模型
model = nn.Sequential(
    nn.Linear(10, 50),
    nn.ReLU(),
    nn.Linear(50, 1)
)

# 不同优化器对比
optimizers = {
    'SGD': optim.SGD(model.parameters(), lr=0.01),
    'SGD+Momentum': optim.SGD(model.parameters(), lr=0.01, momentum=0.9),
    'Adam': optim.Adam(model.parameters(), lr=0.001),
    'AdamW': optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01),
}

# Adam优化器参数详解
adam = optim.Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999), eps=1e-8)
"""
Adam参数说明：
- lr: 学习率，默认0.001
- betas: (β1, β2) 动量参数，默认(0.9, 0.999)
- eps: 数值稳定性，默认1e-8
- weight_decay: L2正则化系数

工作原理：
m_t = β1 * m_{t-1} + (1-β1) * g_t     # 一阶矩估计
v_t = β2 * v_{t-1} + (1-β2) * g_t²    # 二阶矩估计
m̂_t = m_t / (1-β1^t)                   # 偏差修正
v̂_t = v_t / (1-β2^t)
θ_t = θ_{t-1} - lr * m̂_t / (√v̂_t + ε)
"""
```

### 1.2 学习率调度

```python
"""
学习率调度策略：

1. StepLR: 每隔N个epoch降低学习率
2. ExponentialLR: 指数衰减
3. CosineAnnealingLR: 余弦退火
4. ReduceLROnPlateau: 指标停止改善时降低
5. OneCycleLR: 超收敛策略
6. Warmup: 预热学习率
"""

import torch.optim.lr_scheduler as scheduler

model = nn.Linear(10, 1)
optimizer = optim.SGD(model.parameters(), lr=0.1)

# 1. 阶梯式衰减
step_scheduler = scheduler.StepLR(optimizer, step_size=30, gamma=0.1)
# 每30个epoch，lr = lr * 0.1

# 2. 余弦退火（推荐）
cosine_scheduler = scheduler.CosineAnnealingLR(
    optimizer, 
    T_max=100,      # 周期
    eta_min=1e-6    # 最小学习率
)

# 3. 自适应调整
plateau_scheduler = scheduler.ReduceLROnPlateau(
    optimizer,
    mode='min',       # 监控指标越小越好
    factor=0.1,       # 衰减因子
    patience=10,      # 等待10个epoch
    verbose=True
)

# 4. 预热 + 余弦退火（大模型训练常用）
class WarmupCosineScheduler:
    """带预热的余弦退火调度器"""
    
    def __init__(self, optimizer, warmup_epochs, total_epochs, warmup_lr=1e-6, min_lr=1e-6):
        self.optimizer = optimizer
        self.warmup_epochs = warmup_epochs
        self.total_epochs = total_epochs
        self.warmup_lr = warmup_lr
        self.min_lr = min_lr
        self.base_lr = optimizer.param_groups[0]['lr']
        self.current_epoch = 0
    
    def step(self):
        if self.current_epoch < self.warmup_epochs:
            # 线性预热
            lr = self.warmup_lr + (self.base_lr - self.warmup_lr) * \
                 self.current_epoch / self.warmup_epochs
        else:
            # 余弦退火
            progress = (self.current_epoch - self.warmup_epochs) / \
                      (self.total_epochs - self.warmup_epochs)
            lr = self.min_lr + 0.5 * (self.base_lr - self.min_lr) * \
                 (1 + np.cos(np.pi * progress))
        
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = lr
        
        self.current_epoch += 1
        return lr

# 可视化学习率变化
def plot_learning_rate_schedule():
    epochs = 100
    warmup_epochs = 10
    
    optimizer = optim.SGD([torch.randn(2, 1, requires_grad=True)], lr=0.1)
    scheduler = WarmupCosineScheduler(optimizer, warmup_epochs, epochs)
    
    lrs = []
    for _ in range(epochs):
        lr = scheduler.step()
        lrs.append(lr)
    
    plt.figure(figsize=(10, 4))
    plt.plot(lrs)
    plt.xlabel('Epoch')
    plt.ylabel('Learning Rate')
    plt.title('Warmup + Cosine Annealing Learning Rate Schedule')
    plt.axvline(x=warmup_epochs, color='r', linestyle='--', label='Warmup End')
    plt.legend()
    plt.grid(True)
    plt.savefig('lr_schedule.png', dpi=100)
    plt.show()
```

---

## 二、正则化技术

### 2.1 L1/L2正则化

```python
"""
L1正则化 (Lasso)
Loss = Loss_original + λ * |w|
- 产生稀疏权重
- 特征选择效果

L2正则化 (Ridge/Weight Decay)
Loss = Loss_original + λ * w²
- 防止权重过大
- 常用且稳定
"""

# PyTorch中的实现
model = nn.Linear(10, 1)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=0.01)  # L2

# 手动实现L1正则化
def l1_regularization(model, lambda_l1):
    l1_loss = 0
    for param in model.parameters():
        l1_loss += torch.sum(torch.abs(param))
    return lambda_l1 * l1_loss

# 训练循环
def train_with_regularization(model, dataloader, optimizer, lambda_l1=0.01, lambda_l2=0.01):
    model.train()
    for inputs, targets in dataloader:
        optimizer.zero_grad()
        
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        
        # 添加L1正则化
        loss += l1_regularization(model, lambda_l1)
        # L2已在optimizer中通过weight_decay实现
        
        loss.backward()
        optimizer.step()
```

### 2.2 Dropout

```python
class DropoutModel(nn.Module):
    """带Dropout的网络"""
    
    def __init__(self, input_dim, hidden_dim, output_dim, dropout_prob=0.5):
        super().__init__()
        
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.dropout1 = nn.Dropout(dropout_prob)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.dropout2 = nn.Dropout(dropout_prob)
        self.fc3 = nn.Linear(hidden_dim, output_dim)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.dropout1(x)
        x = torch.relu(self.fc2(x))
        x = self.dropout2(x)
        x = self.fc3(x)
        return x

"""
Dropout要点：
1. 训练时随机丢弃神经元，测试时使用全部
2. 常用dropout概率：0.2-0.5
3. CNN中常用较低dropout或不用
4. 在全连接层之间使用

Dropout变体：
- SpatialDropout: 整个通道丢弃（CNN）
- DropConnect: 丢弃连接而非神经元
- DropBlock: 丢弃连续区域（CNN）
"""

class SpatialDropout(nn.Module):
    """空间Dropout，适用于CNN"""
    
    def __init__(self, drop_prob=0.2):
        super().__init__()
        self.drop_prob = drop_prob
    
    def forward(self, x):
        if not self.training or self.drop_prob == 0:
            return x
        
        # 只在通道维度dropout
        mask = torch.bernoulli(
            torch.ones(x.size(0), x.size(1), 1, 1, device=x.device) * (1 - self.drop_prob)
        )
        return x * mask / (1 - self.drop_prob)
```

### 2.3 Batch Normalization

```python
class BNModel(nn.Module):
    """带BatchNorm的网络"""
    
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.bn2 = nn.BatchNorm1d(hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, output_dim)
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.bn1(x)
        x = torch.relu(x)
        
        x = self.fc2(x)
        x = self.bn2(x)
        x = torch.relu(x)
        
        x = self.fc3(x)
        return x

"""
Batch Normalization：
- 计算每个mini-batch的均值和方差
- 标准化后再缩放和平移
- 允许使用更大学习率
- 减少对初始化的依赖

BN vs LN vs IN vs GN：

┌─────────────────────────────────────┐
│ Batch Norm:    [N, C, H, W]         │  沿N维度归一化
│ Layer Norm:    [N, C, H, W]         │  沿C,H,W归一化
│ Instance Norm: [N, C, H, W]         │  沿H,W归一化
│ Group Norm:    [N, G, C//G, H, W]   │  分组归一化
└─────────────────────────────────────┘

选择建议：
- CNN: Batch Norm
- RNN/Transformer: Layer Norm
- 风格迁移: Instance Norm
- 小Batch训练: Group Norm
"""

# LayerNorm（Transformer常用）
class TransformerLayerNorm(nn.Module):
    def __init__(self, hidden_dim, eps=1e-6):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_dim))
        self.bias = nn.Parameter(torch.zeros(hidden_dim))
        self.eps = eps
    
    def forward(self, x):
        mean = x.mean(-1, keepdim=True)
        std = x.std(-1, keepdim=True, unbiased=False)
        return self.weight * (x - mean) / (std + self.eps) + self.bias
```

### 2.4 数据增强

```python
import torchvision.transforms as transforms

# 图像数据增强
train_transform = transforms.Compose([
    # 几何变换
    transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(15),
    
    # 颜色变换
    transforms.ColorJitter(
        brightness=0.2,
        contrast=0.2,
        saturation=0.2,
        hue=0.1
    ),
    
    # 高级增强
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
    
    # 转换和标准化
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# 使用Albumentations（更强大）
# pip install albumentations
try:
    import albumentations as A
    from albumentations.pytorch import ToTensorV2
    
    albumentations_transform = A.Compose([
        A.RandomCrop(224, 224),
        A.HorizontalFlip(p=0.5),
        A.Rotate(limit=15),
        A.OneOf([
            A.GaussNoise(),
            A.GaussianBlur(),
        ], p=0.3),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2()
    ])
except ImportError:
    pass

# Mixup增强
def mixup_data(x, y, alpha=0.2):
    """Mixup数据增强"""
    lam = np.random.beta(alpha, alpha)
    batch_size = x.size(0)
    index = torch.randperm(batch_size)
    
    mixed_x = lam * x + (1 - lam) * x[index]
    y_a, y_b = y, y[index]
    
    return mixed_x, y_a, y_b, lam

def mixup_criterion(criterion, pred, y_a, y_b, lam):
    """Mixup损失函数"""
    return lam * criterion(pred, y_a) + (1 - lam) * criterion(pred, y_b)

# CutMix增强
def cutmix_data(x, y, beta=1.0):
    """CutMix数据增强"""
    lam = np.random.beta(beta, beta)
    batch_size = x.size(0)
    index = torch.randperm(batch_size)
    
    # 随机裁剪区域
    W, H = x.size(2), x.size(3)
    cut_rat = np.sqrt(1. - lam)
    cut_w = int(W * cut_rat)
    cut_h = int(H * cut_rat)
    
    cx = np.random.randint(W)
    cy = np.random.randint(H)
    
    bbx1 = np.clip(cx - cut_w // 2, 0, W)
    bby1 = np.clip(cy - cut_h // 2, 0, H)
    bbx2 = np.clip(cx + cut_w // 2, 0, W)
    bby2 = np.clip(cy + cut_h // 2, 0, H)
    
    x[:, :, bbx1:bbx2, bby1:bby2] = x[index, :, bbx1:bbx2, bby1:bby2]
    
    return x, y, y[index], lam
```

---

## 三、梯度问题解决

### 3.1 梯度消失与爆炸

```python
"""
梯度消失原因：
- Sigmoid/Tanh导数小于1
- 多层链式相乘导致梯度指数衰减

解决方案：
1. 使用ReLU及其变体
2. 残差连接
3. BatchNorm
4. 合理的权重初始化
"""

# 激活函数对比
activations = {
    'Sigmoid': nn.Sigmoid(),      # 输出(0,1)，梯度消失严重
    'Tanh': nn.Tanh(),            # 输出(-1,1)，梯度消失较轻
    'ReLU': nn.ReLU(),            # 推荐，无梯度消失问题
    'LeakyReLU': nn.LeakyReLU(0.01),  # 解决ReLU神经元死亡
    'ELU': nn.ELU(),              # 更平滑的ReLU变体
    'GELU': nn.GELU(),            # Transformer常用
    'Swish': nn.SiLU(),           # 平滑自门控
}

# 梯度裁剪（解决梯度爆炸）
def train_with_gradient_clipping(model, dataloader, optimizer, max_norm=1.0):
    model.train()
    for inputs, targets in dataloader:
        optimizer.zero_grad()
        
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        
        # 梯度裁剪
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm)
        
        optimizer.step()
```

### 3.2 权重初始化

```python
"""
权重初始化的重要性：
- 好的初始化加速收敛
- 防止梯度消失/爆炸

常用方法：
1. Xavier初始化 (Glorot)
   - 适用于Sigmoid/Tanh
   - 方差 = 2 / (fan_in + fan_out)

2. Kaiming初始化 (He)
   - 适用于ReLU
   - 方差 = 2 / fan_in
"""

def init_weights_xavier(m):
    """Xavier初始化"""
    if isinstance(m, nn.Linear):
        nn.init.xavier_uniform_(m.weight)
        if m.bias is not None:
            nn.init.zeros_(m.bias)
    elif isinstance(m, nn.Conv2d):
        nn.init.xavier_uniform_(m.weight)
        if m.bias is not None:
            nn.init.zeros_(m.bias)

def init_weights_kaiming(m):
    """Kaiming初始化（ReLU推荐）"""
    if isinstance(m, nn.Linear):
        nn.init.kaiming_normal_(m.weight, mode='fan_in', nonlinearity='relu')
        if m.bias is not None:
            nn.init.zeros_(m.bias)
    elif isinstance(m, nn.Conv2d):
        nn.init.kaiming_normal_(m.weight, mode='fan_in', nonlinearity='relu')
        if m.bias is not None:
            nn.init.zeros_(m.bias)

# 应用初始化
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Linear(256, 10)
)
model.apply(init_weights_kaiming)

# 预训练权重初始化（迁移学习）
def init_from_pretrained(model, pretrained_model):
    """使用预训练权重初始化"""
    pretrained_dict = pretrained_model.state_dict()
    model_dict = model.state_dict()
    
    # 过滤不匹配的键
    pretrained_dict = {k: v for k, v in pretrained_dict.items() 
                       if k in model_dict and v.size() == model_dict[k].size()}
    
    model_dict.update(pretrained_dict)
    model.load_state_dict(model_dict)
    return model
```

---

## 四、高级训练技巧

### 4.1 混合精度训练

```python
from torch.cuda.amp import autocast, GradScaler

"""
混合精度训练 (Mixed Precision)：
- 使用FP16进行前向和反向传播
- FP32保存权重副本
- 减少显存占用，加速训练
"""

def train_mixed_precision(model, dataloader, optimizer, epochs):
    model.train()
    scaler = GradScaler()  # 梯度缩放器
    
    for epoch in range(epochs):
        for inputs, targets in dataloader:
            optimizer.zero_grad()
            
            # 使用混合精度
            with autocast():
                outputs = model(inputs)
                loss = criterion(outputs, targets)
            
            # 缩放损失并反向传播
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
    
    return model
```

### 4.2 梯度累积

```python
"""
梯度累积：模拟大batch训练
适用于显存不足的情况
"""

def train_with_gradient_accumulation(model, dataloader, optimizer, accumulation_steps=4):
    model.train()
    optimizer.zero_grad()
    
    for i, (inputs, targets) in enumerate(dataloader):
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        
        # 归一化损失
        loss = loss / accumulation_steps
        loss.backward()
        
        # 累积到一定步数后更新
        if (i + 1) % accumulation_steps == 0:
            optimizer.step()
            optimizer.zero_grad()
```

### 4.3 Early Stopping

```python
class EarlyStopping:
    """早停机制"""
    
    def __init__(self, patience=7, min_delta=0, mode='min'):
        self.patience = patience
        self.min_delta = min_delta
        self.mode = mode
        self.counter = 0
        self.best_score = None
        self.early_stop = False
    
    def __call__(self, score):
        if self.best_score is None:
            self.best_score = score
        elif self.mode == 'min':
            if score < self.best_score - self.min_delta:
                self.best_score = score
                self.counter = 0
            else:
                self.counter += 1
        else:
            if score > self.best_score + self.min_delta:
                self.best_score = score
                self.counter = 0
            else:
                self.counter += 1
        
        if self.counter >= self.patience:
            self.early_stop = True
        
        return self.early_stop

# 使用示例
early_stopping = EarlyStopping(patience=10, min_delta=0.001)

for epoch in range(100):
    # 训练...
    val_loss = validate(model, val_loader)
    
    if early_stopping(val_loss):
        print(f"Early stopping at epoch {epoch}")
        break
```

### 4.4 模型保存与加载

```python
# 保存完整模型
torch.save(model, 'model_full.pth')

# 只保存权重（推荐）
torch.save(model.state_dict(), 'model_weights.pth')

# 保存检查点（包含优化器状态）
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'scheduler_state_dict': scheduler.state_dict(),
    'loss': loss,
    'best_score': best_score
}
torch.save(checkpoint, 'checkpoint.pth')

# 加载检查点
def load_checkpoint(model, optimizer, scheduler, checkpoint_path):
    checkpoint = torch.load(checkpoint_path)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
    epoch = checkpoint['epoch']
    loss = checkpoint['loss']
    return model, optimizer, scheduler, epoch, loss

# 加载权重
model.load_state_dict(torch.load('model_weights.pth'))
model.eval()  # 切换到评估模式
```

---

## 五、训练监控

### 5.1 TensorBoard

```python
from torch.utils.tensorboard import SummaryWriter

# 创建日志记录器
writer = SummaryWriter('runs/experiment_1')

def train_with_tensorboard(model, train_loader, val_loader, epochs):
    for epoch in range(epochs):
        model.train()
        train_loss = 0
        
        for batch_idx, (inputs, targets) in enumerate(train_loader):
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            
            # 记录每100个batch的损失
            if batch_idx % 100 == 0:
                writer.add_scalar('Loss/train_batch', loss.item(), 
                                epoch * len(train_loader) + batch_idx)
        
        # 记录每个epoch的训练损失
        writer.add_scalar('Loss/train_epoch', train_loss / len(train_loader), epoch)
        
        # 验证
        model.eval()
        val_loss = validate(model, val_loader)
        writer.add_scalar('Loss/val', val_loss, epoch)
        
        # 记录学习率
        writer.add_scalar('Learning_rate', optimizer.param_groups[0]['lr'], epoch)
        
        # 记录参数分布
        for name, param in model.named_parameters():
            writer.add_histogram(f'Parameters/{name}', param, epoch)
            writer.add_histogram(f'Gradients/{name}', param.grad, epoch)
    
    writer.close()

# 在终端运行查看
# tensorboard --logdir=runs
```

### 5.2 进度条

```python
from tqdm import tqdm

def train_with_progress_bar(model, dataloader, epochs):
    for epoch in range(epochs):
        model.train()
        pbar = tqdm(dataloader, desc=f'Epoch {epoch+1}/{epochs}')
        
        for batch_idx, (inputs, targets) in enumerate(pbar):
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            
            # 更新进度条信息
            pbar.set_postfix({
                'loss': f'{loss.item():.4f}',
                'lr': f'{optimizer.param_groups[0]["lr"]:.6f}'
            })
```

---

## 参考资源

> - [Deep Learning Optimization](https://arxiv.org/abs/1609.04747) - 优化算法综述
> - [Batch Normalization论文](https://arxiv.org/abs/1502.03167) - BN原理
> - [Dropout论文](https://arxiv.org/abs/1207.0580) - Dropout原理
> - [ResNet论文](https://arxiv.org/abs/1512.03385) - 残差连接
> - [Adam优化器](https://arxiv.org/abs/1412.6980) - Adam算法
> - [Mixup](https://arxiv.org/abs/1710.09412) - 数据增强
> - [PyTorch教程](https://pytorch.org/tutorials/) - 官方教程

---

**上一篇**：[RNN循环神经网络]({{ site.baseurl }}{% post_url /ailearn/03-deep-learning/2026-04-14-03-rnn %})

**下一篇**：[CNN卷积神经网络]({{ site.baseurl }}{% post_url /ailearn/03-deep-learning/2026-04-14-02-cnn %})

**返回**：[深度学习基础]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-03-deep-learning %})

*最后更新: 2026年4月14日*
