---
layout: post
title: "视频分析 - 动作识别与跟踪"
date: 2026-04-20
categories: ailearn
tags: [AI, 计算机视觉, 视频分析, 动作识别]
keywords: 视频分析, 动作识别, 目标跟踪, 行为分析
---

* content
{:toc}

> **前置知识**：需要先掌握 目标检测
>
> **本文重点**：视频分析方法与应用

---

## 一、视频基础处理

### 1.1 视频读写

```python
import cv2

# 读取视频
cap = cv2.VideoCapture('video.mp4')

# 获取视频属性
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"FPS: {fps}, 分辨率: {width}x{height}, 总帧数: {frame_count}")

# 创建视频写入器
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

# 逐帧处理
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # 处理帧
    processed = process_frame(frame)
    
    # 写入
    out.write(processed)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
```

### 1.2 帧差法检测运动

```python
def detect_motion(video_path, threshold=25):
    """简单的运动检测"""
    cap = cv2.VideoCapture(video_path)
    
    ret, prev_frame = cap.read()
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 计算帧差
        diff = cv2.absdiff(prev_gray, gray)
        
        # 二值化
        _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
        
        # 膨胀
        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(thresh, kernel, iterations=2)
        
        # 查找轮廓
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if cv2.contourArea(contour) > 1000:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        cv2.imshow('Motion', frame)
        prev_gray = gray
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
```

---

## 二、目标跟踪

### 2.1 传统跟踪算法

```python
# KCF跟踪器
tracker = cv2.TrackerKCF_create()

# 初始化
ret, frame = cap.read()
bbox = (100, 100, 200, 200)  # 初始边界框
tracker.init(frame, bbox)

# 跟踪
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    success, bbox = tracker.update(frame)
    
    if success:
        x, y, w, h = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    else:
        cv2.putText(frame, "丢失", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    cv2.imshow('Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```

### 2.2 多目标跟踪

```python
from ultralytics import YOLO

model = YOLO('yolov8n.pt')

# 视频跟踪
results = model.track(
    'video.mp4',
    show=True,
    tracker='botsort.yaml',
    save=True
)

# 获取跟踪信息
for result in results:
    boxes = result.boxes
    if boxes.id is not None:
        track_ids = boxes.id.int().cpu().tolist()
        boxes_xyxy = boxes.xyxy.cpu().numpy()
        
        for track_id, box in zip(track_ids, boxes_xyxy):
            print(f"ID: {track_id}, 位置: {box}")
```

---

## 三、动作识别

### 3.1 使用预训练模型

```python
import torch
from torchvision.models.video import r3d_18

# 加载预训练模型
model = r3d_18(pretrained=True)
model.eval()

# 准备视频片段 (B, C, T, H, W)
clip = torch.randn(1, 3, 16, 112, 112)  # 16帧

# 推理
with torch.no_grad():
    output = model(clip)
    pred = output.argmax(1)

# Kinetics-400类别标签
print(f"动作类别: {pred.item()}")
```

### 3.2 使用VideoMAE

```python
from transformers import VideoMAEForVideoClassification, VideoMAEImageProcessor

# 加载模型
model = VideoMAEForVideoClassification.from_pretrained("MCG-NJU/videomae-base-finetuned-kinetics")
processor = VideoMAEImageProcessor.from_pretrained("MCG-NJU/videomae-base-finetuned-kinetics")

# 处理视频
def process_video(video_path, num_frames=16):
    frames = []
    cap = cv2.VideoCapture(video_path)
    
    # 均匀采样
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
    
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    cap.release()
    return frames

# 推理
frames = process_video('action.mp4')
inputs = processor(frames, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)
    pred = outputs.logits.argmax(-1)
    
print(f"动作: {model.config.id2label[pred.item()]}")
```

---

## 四、行为分析实战

```python
class VideoAnalyzer:
    """视频分析系统"""
    
    def __init__(self):
        self.detector = YOLO('yolov8n.pt')
        self.track_history = {}
    
    def analyze(self, video_path):
        """分析视频"""
        cap = cv2.VideoCapture(video_path)
        results_list = []
        
        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # 检测
            results = self.detector.track(frame, persist=True)
            
            # 记录跟踪
            if results[0].boxes.id is not None:
                boxes = results[0].boxes.xywh.cpu()
                track_ids = results[0].boxes.id.int().cpu()
                
                for box, track_id in zip(boxes, track_ids):
                    x, y, w, h = box
                    
                    if track_id not in self.track_history:
                        self.track_history[track_id] = []
                    
                    self.track_history[track_id].append((float(x), float(y), frame_idx))
            
            
            frame_idx += 1
        
        cap.release()
        
        return self.track_history
    
    def get_trajectory(self, track_id):
        """获取轨迹"""
        return self.track_history.get(track_id, [])
    
    def analyze_behavior(self, track_id):
        """分析行为"""
        trajectory = self.get_trajectory(track_id)
        if len(trajectory) < 2:
            return "轨迹太短"
        
        # 计算移动距离
        total_distance = 0
        for i in range(1, len(trajectory)):
            dx = trajectory[i][0] - trajectory[i-1][0]
            dy = trajectory[i][1] - trajectory[i-1][1]
            total_distance += (dx**2 + dy**2)**0.5
        
        if total_distance < 100:
            return "静止"
        elif total_distance < 500:
            return "缓慢移动"
        else:
            return "快速移动"
```

---

## 参考资源

> - [VideoMAE论文](https://arxiv.org/abs/2203.12602)
> - [YOLOv8跟踪](https://docs.ultralytics.com/modes/track/)
> - [OpenCV跟踪API](https://docs.opencv.org/4.x/d9/df8/group__tracking.html)

---

**返回**：[计算机视觉基础]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-09-computer-vision %})

*最后更新: 2026年4月20日*