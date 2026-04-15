---
layout: post
title: "图像分割 - 语义分割与实例分割"
date: 2026-04-20
categories: ailearn
tags: [AI, 计算机视觉, 图像分割, UNet]
keywords: 图像分割, UNet, Mask R-CNN, 语义分割
---

* content
{:toc}

> **前置知识**：需要先掌握 CNN基础
>
> **本文重点**：图像分割原理与实现

---

## 一、图像分割概述

```
图像分割分类：

1. 语义分割 (Semantic Segmentation)
   - 为每个像素分配类别标签
   - 同类物体不可区分
   - 例如：UNet, DeepLab, PSPNet

2. 实例分割 (Instance Segmentation)
   - 检测并分割每个物体实例
   - 同类物体可区分
   - 例如：Mask R-CNN, YOLACT

3. 全景分割 (Panoptic Segmentation)
   - 语义分割 + 实例分割
   - 背景类用语义分割，前景用实例分割
```

---

## 二、UNet语义分割

### 2.1 UNet架构

```python
import torch
import torch.nn as nn

class DoubleConv(nn.Module):
    """双卷积块"""
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )
    
    def forward(self, x):
        return self.conv(x)

class UNet(nn.Module):
    """UNet网络"""
    def __init__(self, in_channels=3, out_channels=1):
        super().__init__()
        
        # 编码器
        self.enc1 = DoubleConv(in_channels, 64)
        self.enc2 = DoubleConv(64, 128)
        self.enc3 = DoubleConv(128, 256)
        self.enc4 = DoubleConv(256, 512)
        
        self.pool = nn.MaxPool2d(2)
        
        # 瓶颈层
        self.bottleneck = DoubleConv(512, 1024)
        
        # 解码器
        self.upconv4 = nn.ConvTranspose2d(1024, 512, 2, stride=2)
        self.dec4 = DoubleConv(1024, 512)
        
        self.upconv3 = nn.ConvTranspose2d(512, 256, 2, stride=2)
        self.dec3 = DoubleConv(512, 256)
        
        self.upconv2 = nn.ConvTranspose2d(256, 128, 2, stride=2)
        self.dec2 = DoubleConv(256, 128)
        
        self.upconv1 = nn.ConvTranspose2d(128, 64, 2, stride=2)
        self.dec1 = DoubleConv(128, 64)
        
        self.final = nn.Conv2d(64, out_channels, 1)
    
    def forward(self, x):
        # 编码
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool(e1))
        e3 = self.enc3(self.pool(e2))
        e4 = self.enc4(self.pool(e3))
        
        # 瓶颈
        b = self.bottleneck(self.pool(e4))
        
        # 解码 + 跳跃连接
        d4 = self.upconv4(b)
        d4 = torch.cat([d4, e4], dim=1)
        d4 = self.dec4(d4)
        
        d3 = self.upconv3(d4)
        d3 = torch.cat([d3, e3], dim=1)
        d3 = self.dec3(d3)
        
        d2 = self.upconv2(d3)
        d2 = torch.cat([d2, e2], dim=1)
        d2 = self.dec2(d2)
        
        d1 = self.upconv1(d2)
        d1 = torch.cat([d1, e1], dim=1)
        d1 = self.dec1(d1)
        
        return self.final(d1)
```

### 2.2 训练UNet

```python
import torch.optim as optim
from torch.utils.data import DataLoader

# 损失函数
class DiceLoss(nn.Module):
    """Dice损失"""
    def __init__(self):
        super().__init__()
    
    def forward(self, pred, target):
        pred = torch.sigmoid(pred)
        intersection = (pred * target).sum()
        dice = (2. * intersection) / (pred.sum() + target.sum() + 1e-8)
        return 1 - dice

# 组合损失
class CombinedLoss(nn.Module):
    def __init__(self):
        super().__init__()
        self.bce = nn.BCEWithLogitsLoss()
        self.dice = DiceLoss()
    
    def forward(self, pred, target):
        return self.bce(pred, target) + self.dice(pred, target)

# 训练
model = UNet(in_channels=3, out_channels=1)
criterion = CombinedLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)

def train_epoch(model, loader, criterion, optimizer, device):
    model.train()
    total_loss = 0
    
    for images, masks in loader:
        images, masks = images.to(device), masks.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, masks)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    return total_loss / len(loader)
```

---

## 三、Mask R-CNN实例分割

```python
import torchvision
from torchvision.models.detection import maskrcnn_resnet50_fpn
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor

# 加载预训练模型
model = maskrcnn_resnet50_fpn(pretrained=True)

# 修改类别数
num_classes = 2  # 背景 + 1类

# 修改框预测器
in_features = model.roi_heads.box_predictor.cls_score.in_features
model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

# 修改掩码预测器
in_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
hidden_layer = 256
model.roi_heads.mask_predictor = MaskRCNNPredictor(in_features_mask, hidden_layer, num_classes)

# 推理
model.eval()
with torch.no_grad():
    prediction = model([image_tensor])

# 解析结果
boxes = prediction[0]['boxes']
labels = prediction[0]['labels']
scores = prediction[0]['scores']
masks = prediction[0]['masks']

# 可视化掩码
for i, (box, mask) in enumerate(zip(boxes, masks)):
    if scores[i] > 0.5:
        mask_binary = mask[0] > 0.5
        # 应用掩码绘制
```

---

## 四、DeepLab系列

```python
from torchvision.models.segmentation import deeplabv3_resnet50

# 加载预训练模型
model = deeplabv3_resnet50(pretrained=True, num_classes=21)

# 修改输出类别
model.classifier[4] = nn.Conv2d(256, num_classes, 1)

# 推理
model.eval()
with torch.no_grad():
    output = model(input_tensor)['out']
    pred = output.argmax(1)
```

---

## 参考资源

> - [UNet论文](https://arxiv.org/abs/1505.04597)
> - [Mask R-CNN论文](https://arxiv.org/abs/1703.06870)
> - [DeepLab论文](https://arxiv.org/abs/1606.00915)

---

**返回**：[计算机视觉基础]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-09-computer-vision %})

*最后更新: 2026年4月20日*