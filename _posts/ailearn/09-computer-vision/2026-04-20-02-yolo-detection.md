---
layout: post
title: "目标检测实战 - YOLOv8"
date: 2026-04-20
categories: ailearn
tags: [AI, 计算机视觉, 目标检测, YOLO]
keywords: YOLOv8, 目标检测, 目标跟踪, 实例分割
description: 掌握YOLOv8目标检测，实现自定义数据集训练
---

* content
{:toc}

> **前置知识**：需要先掌握 CNN基础
>
> **本文重点**：YOLOv8使用与自定义训练

---

## 一、YOLOv8入门

### 1.1 安装与推理

```python
# 安装
# pip install ultralytics

from ultralytics import YOLO

# 加载预训练模型
model = YOLO('yolov8n.pt')  # nano版本

# 目标检测
results = model('image.jpg')

# 显示结果
results[0].show()

# 获取检测信息
for result in results:
    boxes = result.boxes
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        conf = box.conf[0].cpu().numpy()
        cls = box.cls[0].cpu().numpy()
        class_name = model.names[int(cls)]
        
        print(f"类别: {class_name}, 置信度: {conf:.2f}")
```

### 1.2 模型版本对比

```
YOLOv8模型对比：

模型      参数量    mAP    速度(FPS)
───────────────────────────────────
yolov8n    3.2M    37.3    高(最快)
yolov8s    11.2M   44.9    较高
yolov8m    25.9M   50.2    中等
yolov8l    43.7M   52.9    较低
yolov8x    68.2M   53.9    低(最慢)
```

---

## 二、视频检测

```python
# 视频文件检测
results = model.track('video.mp4', show=True, save=True)

# 摄像头实时检测
import cv2

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    results = model(frame)
    annotated_frame = results[0].plot()
    cv2.imshow('YOLOv8', annotated_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## 三、自定义数据集训练

### 3.1 数据准备

```yaml
# dataset.yaml 配置文件
path: ./datasets/my_dataset
train: images/train
val: images/val

nc: 3  # 类别数量

names:
  0: cat
  1: dog
  2: bird
```

### 3.2 训练模型

```python
from ultralytics import YOLO

model = YOLO('yolov8n.pt')

results = model.train(
    data='dataset.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    device='cuda'
)

# 验证
metrics = model.val()
print(f"mAP50: {metrics.box.map50}")

# 导出模型
model.export(format='onnx')
```

---

## 四、目标跟踪

```python
# 视频目标跟踪
results = model.track(
    'video.mp4',
    show=True,
    tracker='botsort.yaml'
)

# 获取跟踪ID
for result in results:
    boxes = result.boxes
    if boxes.id is not None:
        track_ids = boxes.id.int().cpu().tolist()
```

---

## 五、实例分割

```python
# 使用YOLOv8-seg模型
model = YOLO('yolov8n-seg.pt')

results = model('image.jpg')

# 获取分割掩码
for result in results:
    if result.masks is not None:
        masks = result.masks.data.cpu().numpy()
```

---

## 参考资源

> - [YOLOv8官方文档](https://docs.ultralytics.com/)
> - [YOLOv8 GitHub](https://github.com/ultralytics/ultralytics)

---

**返回**：[计算机视觉基础]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-09-computer-vision %})

*最后更新: 2026年4月20日*