---
layout: post
title: "OpenCV图像处理基础"
date: 2026-04-20
categories: ailearn
tags: [AI, 计算机视觉, OpenCV]
keywords: OpenCV, 图像处理, 边缘检测, 轮廓提取
description: 掌握OpenCV基础操作，实现常用图像处理功能
---

* content
{:toc}

> **前置知识**：需要先掌握 NumPy基础
>
> **本文重点**：OpenCV核心功能与实战应用

---

## 一、OpenCV入门

### 1.1 安装与基础

```python
# 安装
# pip install opencv-python

import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取图像
img = cv2.imread('image.jpg')  # BGR格式
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转为RGB

# 显示图像
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 图像属性
print(f"形状: {img.shape}")      # (height, width, channels)
print(f"数据类型: {img.dtype}")   # uint8
print(f"像素总数: {img.size}")
```

### 1.2 颜色空间转换

```python
# BGR <-> RGB
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# BGR <-> GRAY
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# BGR <-> HSV
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 颜色分割（HSV空间）
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])
mask = cv2.inRange(img_hsv, lower_red, upper_red)
red_region = cv2.bitwise_and(img, img, mask=mask)
```

---

## 二、图像基本操作

### 2.1 图像裁剪与缩放

```python
# 裁剪
height, width = img.shape[:2]
cropped = img[100:400, 200:500]  # [y1:y2, x1:x2]

# 缩放
resized = cv2.resize(img, (800, 600))  # 指定尺寸
resized = cv2.resize(img, None, fx=0.5, fy=0.5)  # 按比例

# 翻转
flipped_h = cv2.flip(img, 1)  # 水平翻转
flipped_v = cv2.flip(img, 0)  # 垂直翻转

# 旋转
rows, cols = img.shape[:2]
M = cv2.getRotationMatrix2D((cols/2, rows/2), 45, 1)
rotated = cv2.warpAffine(img, M, (cols, rows))
```

### 2.2 绘图功能

```python
canvas = np.zeros((500, 500, 3), dtype=np.uint8)

# 绘制线条
cv2.line(canvas, (0, 0), (500, 500), (0, 255, 0), 2)

# 绘制矩形
cv2.rectangle(canvas, (50, 50), (200, 200), (255, 0, 0), -1)

# 绘制圆形
cv2.circle(canvas, (300, 300), 100, (0, 0, 255), 3)

# 添加文字
cv2.putText(canvas, 'OpenCV', (100, 450), 
            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
```

---

## 三、图像滤波

### 3.1 模糊与平滑

```python
# 均值滤波
blur = cv2.blur(img, (5, 5))

# 高斯滤波
gaussian = cv2.GaussianBlur(img, (5, 5), 0)

# 中值滤波（去噪效果好）
median = cv2.medianBlur(img, 5)

# 双边滤波（保边去噪）
bilateral = cv2.bilateralFilter(img, 9, 75, 75)
```

### 3.2 边缘检测

```python
# Sobel边缘检测
sobel_x = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)
sobel = np.sqrt(sobel_x**2 + sobel_y**2)

# Canny边缘检测（推荐）
edges = cv2.Canny(img_gray, 100, 200)
```

---

## 四、形态学操作

```python
kernel = np.ones((5, 5), np.uint8)

# 腐蚀
erosion = cv2.erode(img_gray, kernel, iterations=1)

# 膨胀
dilation = cv2.dilate(img_gray, kernel, iterations=1)

# 开运算（先腐蚀后膨胀，去噪点）
opening = cv2.morphologyEx(img_gray, cv2.MORPH_OPEN, kernel)

# 闭运算（先膨胀后腐蚀，填充空洞）
closing = cv2.morphologyEx(img_gray, cv2.MORPH_CLOSE, kernel)
```

---

## 五、轮廓检测

```python
# 二值化
ret, thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

# 查找轮廓
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 绘制轮廓
cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

# 轮廓特征
for cnt in contours:
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt, True)
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
```

---

## 六、实战案例

### 6.1 人脸检测

```python
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
```

### 6.2 视频处理

```python
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Video', gray)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## 参考资源

> - [OpenCV官方文档](https://docs.opencv.org/4.x/)
> - [OpenCV-Python教程](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)

---

**返回**：[计算机视觉基础]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-09-computer-vision %})

*最后更新: 2026年4月20日*