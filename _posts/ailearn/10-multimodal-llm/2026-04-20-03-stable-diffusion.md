---
layout: post
title: "Stable Diffusion - 图像生成与编辑"
date: 2026-04-20
categories: ailearn
tags: [AI, 多模态, Stable Diffusion, 图像生成]
keywords: Stable Diffusion, 文生图, 图生图, ControlNet
---

* content
{:toc}

> **前置知识**：需要先掌握 PyTorch基础
>
> **本文重点**：Stable Diffusion原理与应用

---

## 一、Stable Diffusion概述

```
Stable Diffusion 原理：

核心组件：
1. VAE (变分自编码器)
   - 编码器：图像 → 潜在空间
   - 解码器：潜在空间 → 图像

2. U-Net
   - 在潜在空间进行去噪
   - 使用Cross-Attention注入文本条件

3. Text Encoder (CLIP)
   - 文本 → 向量表示

工作流程：
噪声 → U-Net去噪 → VAE解码 → 图像
```

---

## 二、文生图

### 2.1 基础使用

```python
from diffusers import StableDiffusionPipeline
import torch

# 加载模型
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

# 生成图像
prompt = "a beautiful sunset over mountains, highly detailed, 4k"
image = pipe(prompt).images[0]
image.save("sunset.png")

# 带参数生成
image = pipe(
    prompt=prompt,
    negative_prompt="ugly, distorted, low quality",
    num_inference_steps=30,      # 去噪步数
    guidance_scale=7.5,          # CFG权重
    width=512,
    height=512,
    num_images_per_prompt=4      # 生成多张
).images
```

### 2.2 使用不同模型

```python
# SDXL (更高质量)
from diffusers import StableDiffusionXLPipeline

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16
).to("cuda")

# SD 2.1
pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-1",
    torch_dtype=torch.float16
).to("cuda")
```

---

## 三、图生图

```python
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image

# 加载模型
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda")

# 准备初始图像
init_image = Image.open("input.jpg").convert("RGB")
init_image = init_image.resize((512, 512))

# 图生图
prompt = "cyberpunk style, neon lights, futuristic city"
image = pipe(
    prompt=prompt,
    image=init_image,
    strength=0.7,  # 变化程度 (0-1)
    num_inference_steps=30
).images[0]
```

---

## 四、ControlNet

### 4.1 边缘控制

```python
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
import cv2
import numpy as np

# 加载ControlNet
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-canny",
    torch_dtype=torch.float16
)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch.float16
).to("cuda")

# 准备控制图像
image = Image.open("input.jpg")
np_image = np.array(image)
canny_image = cv2.Canny(np_image, 100, 200)
canny_image = Image.fromarray(canny_image)

# 生成
output = pipe(
    prompt="a modern building",
    image=canny_image,
    num_inference_steps=20
).images[0]
```

### 4.2 姿势控制

```python
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel

# OpenPose ControlNet
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-openpose",
    torch_dtype=torch.float16
)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch.float16
).to("cuda")

# 使用OpenPose图像
pose_image = Image.open("pose.png")

output = pipe(
    prompt="a person dancing",
    image=pose_image
).images[0]
```

---

## 五、Inpainting

```python
from diffusers import StableDiffusionInpaintPipeline

pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-inpainting",
    torch_dtype=torch.float16
).to("cuda")

# 准备图像和掩码
image = Image.open("image.jpg").resize((512, 512))
mask = Image.open("mask.png").resize((512, 512))  # 白色区域会被重绘

# Inpainting
output = pipe(
    prompt="a cat sitting on the grass",
    image=image,
    mask_image=mask
).images[0]
```

---

## 六、LoRA微调

```python
# 加载LoRA
pipe.load_lora_weights("./lora_weights")

# 使用LoRA生成
image = pipe(
    prompt="a photo of sks dog in the park",
    num_inference_steps=30
).images[0]
```

---

## 参考资源

> - [Stable Diffusion论文](https://arxiv.org/abs/2112.10752)
> - [Diffusers文档](https://huggingface.co/docs/diffusers/)
> - [ControlNet论文](https://arxiv.org/abs/2302.05543)

---

**返回**：[多模态大模型]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-10-multimodal-llm %})

*最后更新: 2026年4月20日*