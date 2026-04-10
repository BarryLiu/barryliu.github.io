---
layout: post
title: "【AI学习路线 09】计算机视觉基础 - 图像处理与目标检测"
date: 2026-04-10
categories: ailearn
tags: [AI, CV, 计算机视觉, 目标检测, 图像分类]
keywords: 计算机视觉, 图像分类, 目标检测, YOLO, 图像分割, OpenCV
description: AI学习路线第9篇 - 学习计算机视觉核心技术，从图像处理到目标检测与图像分割
---

* content
{:toc}

> **学习顺序说明**：本文是AI学习路线的第9篇，建议按顺序学习：
> - 01 入门基础 → ... → 08 AI工具链 → 09 计算机视觉（本文）→ 10 多模态大模型 → 11 AI Agent → 12 项目实战

计算机视觉是AI的重要分支，让机器能够"看懂"图像和视频。本文介绍计算机视觉的核心技术和应用。

## 计算机视觉概述

### 主要任务

```
计算机视觉
├── 图像分类 (Image Classification)
├── 目标检测 (Object Detection)
├── 图像分割 (Image Segmentation)
│   ├── 语义分割
│   └── 实例分割
├── 目标跟踪 (Object Tracking)
├── 图像生成 (Image Generation)
└── 视觉问答 (Visual QA)
```

> **参考资源**：[CS231n: CNN for Visual Recognition](http://cs231n.stanford.edu/) - Stanford经典课程

---

## 第一部分：图像处理基础

### 1.1 OpenCV基础操作

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取图像
img = cv2.imread('image.jpg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # BGR转RGB

# 基本操作
print(f"图像尺寸: {img.shape}")  # (height, width, channels)

# 调整大小
resized = cv2.resize(img, (224, 224))

# 裁剪
cropped = img[100:300, 200:400]

# 灰度化
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 模糊
blurred = cv2.GaussianBlur(img, (5, 5), 0)

# 边缘检测
edges = cv2.Canny(gray, 100, 200)

# 显示
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### 1.2 图像增强

```python
# 亮度/对比度调整
def adjust_brightness_contrast(img, brightness=0, contrast=0):
    if brightness != 0:
        img = cv2.convertScaleAbs(img, alpha=1, beta=brightness)
    if contrast != 0:
        img = cv2.convertScaleAbs(img, alpha=contrast, beta=0)
    return img

# 直方图均衡化
def histogram_equalization(img):
    if len(img.shape) == 3:
        # 彩色图像，转换到YUV空间
        img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
        return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    else:
        return cv2.equalizeHist(img)

# 数据增强
from torchvision import transforms

transform = transforms.Compose([
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
```

> **参考资源**：[OpenCV官方文档](https://docs.opencv.org/4.x/)

---

## 第二部分：图像分类

### 2.1 经典CNN架构

**ResNet迁移学习**

```python
import torch
import torch.nn as nn
from torchvision import models

# 加载预训练ResNet
model = models.resnet50(pretrained=True)

# 修改最后一层
num_classes = 10
model.fc = nn.Linear(model.fc.in_features, num_classes)

# 冻结特征提取层
for param in model.parameters():
    param.requires_grad = False
for param in model.fc.parameters():
    param.requires_grad = True

# 训练
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.fc.parameters(), lr=0.001)
```

**EfficientNet**

```python
# 使用torchvision的EfficientNet
from torchvision.models import efficientnet_b0

model = efficientnet_b0(pretrained=True)
model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
```

### 2.2 图像分类完整流程

```python
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models

# 数据预处理
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

val_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 加载数据
train_dataset = datasets.ImageFolder('train/', transform=train_transform)
val_dataset = datasets.ImageFolder('val/', transform=val_transform)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32)

# 模型
model = models.resnet50(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, len(train_dataset.classes))
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# 训练循环
def train_epoch(model, loader, criterion, optimizer):
    model.train()
    running_loss = 0.0
    correct = 0
    
    for inputs, labels in loader:
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        correct += predicted.eq(labels).sum().item()
    
    return running_loss / len(loader), correct / len(loader.dataset)
```

---

## 第三部分：目标检测

### 3.1 目标检测概述

| 方法 | 类型 | 特点 |
|------|------|------|
| YOLO | 单阶段 | 速度快，实时检测 |
| SSD | 单阶段 | 多尺度检测 |
| Faster R-CNN | 两阶段 | 精度高，速度较慢 |
| DETR | Transformer | 端到端，无需NMS |

### 3.2 YOLO使用

```python
# 使用ultralytics YOLOv8
from ultralytics import YOLO

# 加载预训练模型
model = YOLO('yolov8n.pt')  # nano版本，速度快

# 推理
results = model('image.jpg')

# 显示结果
for result in results:
    boxes = result.boxes  # 边界框
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]  # 坐标
        confidence = box.conf[0]  # 置信度
        class_id = box.cls[0]  # 类别
        
        print(f"类别: {model.names[int(class_id)]}, 置信度: {confidence:.2f}")
        print(f"边界框: ({x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f})")

# 可视化
result.show()
result.save('output.jpg')

# 训练自定义数据集
model.train(data='dataset.yaml', epochs=50, imgsz=640)
```

### 3.3 目标检测评估指标

```python
# IoU (Intersection over Union)
def calculate_iou(box1, box2):
    """计算两个边界框的IoU"""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    
    inter_area = max(0, x2 - x1) * max(0, y2 - y1)
    
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    
    union_area = box1_area + box2_area - inter_area
    
    return inter_area / union_area if union_area > 0 else 0

# mAP计算
# mAP@0.5: IoU阈值0.5时的平均精度
# mAP@0.5:0.95: IoU阈值从0.5到0.95，步长0.05的平均mAP
```

> **参考资源**：[YOLOv8官方文档](https://docs.ultralytics.com/)

---

## 第四部分：图像分割

### 4.1 语义分割

**U-Net架构**

```python
import torch
import torch.nn as nn

class UNet(nn.Module):
    """简化版U-Net"""
    
    def __init__(self, in_channels=3, out_channels=1):
        super().__init__()
        
        # 编码器
        self.enc1 = self.conv_block(in_channels, 64)
        self.enc2 = self.conv_block(64, 128)
        self.enc3 = self.conv_block(128, 256)
        self.enc4 = self.conv_block(256, 512)
        
        self.pool = nn.MaxPool2d(2)
        
        # 解码器
        self.up3 = nn.ConvTranspose2d(512, 256, 2, stride=2)
        self.dec3 = self.conv_block(512, 256)
        
        self.up2 = nn.ConvTranspose2d(256, 128, 2, stride=2)
        self.dec2 = self.conv_block(256, 128)
        
        self.up1 = nn.ConvTranspose2d(128, 64, 2, stride=2)
        self.dec1 = self.conv_block(128, 64)
        
        self.final = nn.Conv2d(64, out_channels, 1)
    
    def conv_block(self, in_ch, out_ch):
        return nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True)
        )
    
    def forward(self, x):
        # 编码
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool(e1))
        e3 = self.enc3(self.pool(e2))
        e4 = self.enc4(self.pool(e3))
        
        # 解码
        d3 = self.up3(e4)
        d3 = torch.cat([d3, e3], dim=1)
        d3 = self.dec3(d3)
        
        d2 = self.up2(d3)
        d2 = torch.cat([d2, e2], dim=1)
        d2 = self.dec2(d2)
        
        d1 = self.up1(d2)
        d1 = torch.cat([d1, e1], dim=1)
        d1 = self.dec1(d1)
        
        return self.final(d1)
```

### 4.2 实例分割

**使用Mask R-CNN**

```python
import torchvision
from torchvision.models.detection import maskrcnn_resnet50_fpn

# 加载预训练模型
model = maskrcnn_resnet50_fpn(pretrained=True)
model.eval()

# 推理
from PIL import Image
import torchvision.transforms as T

img = Image.open('image.jpg')
img_tensor = T.ToTensor()(img)

with torch.no_grad():
    prediction = model([img_tensor])

# 解析结果
boxes = prediction[0]['boxes']      # 边界框
labels = prediction[0]['labels']    # 类别
scores = prediction[0]['scores']    # 分数
masks = prediction[0]['masks']      # 分割掩码

# 可视化掩码
for i, (box, mask) in enumerate(zip(boxes, masks)):
    if scores[i] > 0.5:  # 置信度阈值
        mask = mask[0].numpy()
        # 应用掩码
        pass
```

> **参考资源**：[Mask R-CNN论文](https://arxiv.org/abs/1703.06870)

---

## 第五部分：实战应用

### 5.1 人脸检测与识别

```python
import cv2

# 加载人脸检测器
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_faces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    return img

# 使用深度学习模型
from facenet_pytorch import InceptionResnetV1, MTCNN

mtcnn = MTCNN()  # 人脸检测
resnet = InceptionResnetV1(pretrained='vggface2').eval()  # 人脸特征提取

# 检测人脸
img = Image.open('face.jpg')
face = mtcnn(img)

# 提取特征向量
embedding = resnet(face.unsqueeze(0))
```

### 5.2 OCR文字识别

```python
# 使用PaddleOCR
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='ch')

result = ocr.ocr('document.jpg', cls=True)
for line in result:
    print(line)
```

---

## 学习资源

### 官方文档
- [OpenCV](https://docs.opencv.org/)
- [YOLOv8](https://docs.ultralytics.com/)
- [Detectron2](https://detectron2.readthedocs.io/)

### 经典课程
- [CS231n](http://cs231n.stanford.edu/) - Stanford
- [Deep Learning for Computer Vision](https://www.youtube.com/playlist?list=PL5-TkQAfAZFbzxjBHtzsFC82KbXXAL7U9)

### 经典论文
- [ResNet](https://arxiv.org/abs/1512.03385)
- [YOLO](https://arxiv.org/abs/1506.02640)
- [Mask R-CNN](https://arxiv.org/abs/1703.06870)

---

**上一篇**：[08 AI工具链 - 开发环境与实践工具]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-08-ai-tools %})

**下一篇**：[10 多模态大模型 - 图像与文本的融合]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-10-multimodal-llm %})

*最后更新: 2026年4月10日*

> 本文参考了 [CS231n课程](http://cs231n.stanford.edu/) 和 [YOLOv8文档](https://docs.ultralytics.com/) 整理
