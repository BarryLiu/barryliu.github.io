---
layout: post
title: "【AI学习路线 10】多模态大模型 - 图像与文本的融合"
date: 2026-04-10
categories: ailearn
tags: [AI, 多模态, VLM, GPT-4V, CLIP, LLaVA]
keywords: 多模态大模型, CLIP, GPT-4V, LLaVA, 图像理解, 视觉语言模型
description: AI学习路线第10篇 - 学习多模态大模型技术，掌握图像与文本融合的核心方法
---

* content
{:toc}

> **学习顺序说明**：本文是AI学习路线的第10篇，建议按顺序学习：
> - ... → 09 计算机视觉 → 10 多模态大模型（本文）→ 11 AI Agent → 12 项目实战

多模态大模型(VLM)能够同时理解图像和文本，是当前AI的前沿方向。本文介绍多模态模型的核心技术和应用。

## 多模态大模型概述

### 什么是多模态

```
单模态模型：
- GPT: 文本输入 → 文本输出
- ResNet: 图像输入 → 类别输出

多模态模型：
- GPT-4V: 图像+文本输入 → 文本输出
- CLIP: 图像+文本 → 相似度
- Stable Diffusion: 文本 → 图像
```

### 主要任务

| 任务 | 输入 | 输出 | 代表模型 |
|------|------|------|----------|
| 图像描述 | 图像 | 文本 | BLIP, LLaVA |
| 视觉问答 | 图像+问题 | 答案 | GPT-4V, Qwen-VL |
| 图文检索 | 文本/图像 | 匹配分数 | CLIP |
| 文生图 | 文本 | 图像 | Stable Diffusion |
| 图像编辑 | 图像+指令 | 图像 | InstructPix2Pix |

> **参考资源**：[Multimodal Learning Survey](https://arxiv.org/abs/2307.04206)

---

## 第一部分：CLIP - 图文对齐

### 1.1 CLIP原理

CLIP通过对比学习，将图像和文本映射到同一向量空间。

```python
from transformers import CLIPProcessor, CLIPModel
import torch
from PIL import Image

# 加载模型
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# 图文相似度计算
image = Image.open("cat.jpg")
texts = ["a cat", "a dog", "a bird"]

inputs = processor(text=texts, images=image, return_tensors="pt", padding=True)

with torch.no_grad():
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image  # 图像与文本的相似度
    probs = logits_per_image.softmax(dim=1)  # 转换为概率

print("相似度概率:", probs)
# 输出类似: tensor([[0.95, 0.03, 0.02]])
```

### 1.2 CLIP应用

**零样本图像分类**

```python
def zero_shot_classification(image, class_names):
    """零样本分类"""
    # 构造文本提示
    texts = [f"a photo of a {name}" for name in class_names]
    
    inputs = processor(text=texts, images=image, return_tensors="pt", padding=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
        probs = outputs.logits_per_image.softmax(dim=1)
    
    return class_names[probs.argmax()], probs

# 使用示例
class_names = ["cat", "dog", "car", "flower"]
predicted_class, probs = zero_shot_classification(image, class_names)
print(f"预测类别: {predicted_class}")
```

**图文检索**

```python
import faiss
import numpy as np

class ImageTextRetrieval:
    def __init__(self):
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        self.index = None
        self.image_ids = []
    
    def encode_images(self, images):
        """编码图像"""
        inputs = self.processor(images=images, return_tensors="pt", padding=True)
        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)
        return image_features / image_features.norm(dim=-1, keepdim=True)
    
    def encode_text(self, text):
        """编码文本"""
        inputs = self.processor(text=[text], return_tensors="pt", padding=True)
        with torch.no_grad():
            text_features = self.model.get_text_features(**inputs)
        return text_features / text_features.norm(dim=-1, keepdim=True)
    
    def build_index(self, images, image_ids):
        """构建索引"""
        features = self.encode_images(images)
        features = features.numpy().astype('float32')
        
        self.index = faiss.IndexFlatIP(features.shape[1])
        self.index.add(features)
        self.image_ids = image_ids
    
    def search(self, query_text, top_k=5):
        """文本检索图像"""
        text_features = self.encode_text(query_text).numpy().astype('float32')
        scores, indices = self.index.search(text_features, top_k)
        
        return [(self.image_ids[i], scores[0][j]) for j, i in enumerate(indices[0])]
```

> **参考资源**：[CLIP论文](https://arxiv.org/abs/2103.00020) - Learning Transferable Visual Models

---

## 第二部分：视觉语言模型

### 2.1 LLaVA

LLaVA将视觉编码器与大语言模型连接，实现图像对话。

```python
# 使用LLaVA进行视觉问答
from transformers import LlavaForConditionalGeneration, AutoProcessor

model = LlavaForConditionalGeneration.from_pretrained("llava-hf/llava-1.5-7b-hf")
processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-7b-hf")

# 准备输入
image = Image.open("image.jpg")
conversation = [
    {
        "role": "user",
        "content": [
            {"type": "image"},
            {"type": "text", "text": "请描述这张图片的内容"}
        ]
    }
]

prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
inputs = processor(images=image, text=prompt, return_tensors="pt")

# 生成回答
output = model.generate(**inputs, max_new_tokens=200)
print(processor.decode(output[0], skip_special_tokens=True))
```

### 2.2 Qwen-VL

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig

# 加载Qwen-VL
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-VL-Chat", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen-VL-Chat", 
    trust_remote_code=True,
    device_map="auto"
)

# 视觉问答
query = tokenizer.from_list_format([
    {'image': 'image.jpg'},
    {'text': '描述这张图片'},
])
response, history = model.chat(tokenizer, query=query, history=None)
print(response)

# 多轮对话
query = tokenizer.from_list_format([
    {'text': '图片中有几个人？'},
])
response, history = model.chat(tokenizer, query=query, history=history)
print(response)
```

### 2.3 GPT-4V API

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

# 图像理解
response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "这张图片里有什么？"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://example.com/image.jpg",
                        # 或使用base64
                        # "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
    max_tokens=500
)

print(response.choices[0].message.content)
```

---

## 第三部分：图像生成

### 3.1 Stable Diffusion

```python
from diffusers import StableDiffusionPipeline
import torch

# 加载模型
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

# 文生图
prompt = "a beautiful sunset over mountains, highly detailed, 4k"
image = pipe(prompt).images[0]
image.save("sunset.png")

# 负面提示
image = pipe(
    prompt="a portrait of a woman",
    negative_prompt="ugly, distorted, low quality",
    num_inference_steps=30,
    guidance_scale=7.5
).images[0]

# 图生图
from diffusers import StableDiffusionImg2ImgPipeline

pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda")

init_image = Image.open("input.jpg").convert("RGB")
init_image = init_image.resize((512, 512))

image = pipe(
    prompt="cyberpunk style",
    image=init_image,
    strength=0.7
).images[0]
```

### 3.2 ControlNet

```python
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from diffusers.utils import load_image

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
image = load_image("input.jpg")
# 边缘检测
import cv2
import numpy as np
np_image = np.array(image)
canny_image = cv2.Canny(np_image, 100, 200)
canny_image = Image.fromarray(canny_image)

# 生成
image = pipe(
    prompt="a modern building",
    image=canny_image,
    num_inference_steps=20
).images[0]
```

> **参考资源**：[Stable Diffusion论文](https://arxiv.org/abs/2112.10752)

---

## 第四部分：多模态应用实战

### 4.1 图像问答系统

```python
class VisualQA:
    def __init__(self, model_name="Qwen/Qwen-VL-Chat"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, 
            trust_remote_code=True,
            device_map="auto"
        )
    
    def ask(self, image_path, question):
        query = self.tokenizer.from_list_format([
            {'image': image_path},
            {'text': question}
        ])
        response, _ = self.model.chat(self.tokenizer, query=query, history=None)
        return response
    
    def chat(self, image_path, questions):
        """多轮对话"""
        history = None
        responses = []
        
        for question in questions:
            query = self.tokenizer.from_list_format([
                {'image': image_path},
                {'text': question}
            ])
            response, history = self.model.chat(
                self.tokenizer, query=query, history=history
            )
            responses.append(response)
        
        return responses

# 使用
vqa = VisualQA()
answer = vqa.ask("photo.jpg", "图片中有多少人？")
```

### 4.2 图像描述生成

```python
def generate_caption(image_path):
    """生成图像描述"""
    query = tokenizer.from_list_format([
        {'image': image_path},
        {'text': '请详细描述这张图片的内容'}
    ])
    response, _ = model.chat(tokenizer, query=query, history=None)
    return response

# 批量处理
def batch_caption(image_paths):
    captions = []
    for path in image_paths:
        caption = generate_caption(path)
        captions.append(caption)
    return captions
```

---

## 学习资源

### 模型资源
- [Hugging Face Vision Models](https://huggingface.co/models?pipeline_tag=image-to-text)
- [LLaVA](https://llava-vl.github.io/)
- [Qwen-VL](https://github.com/QwenLM/Qwen-VL)

### 经典论文
- [CLIP](https://arxiv.org/abs/2103.00020) - 对比图文预训练
- [LLaVA](https://arxiv.org/abs/2304.08485) - 视觉指令微调
- [Stable Diffusion](https://arxiv.org/abs/2112.10752) - 图像生成

### 开源项目
- [Diffusers](https://github.com/huggingface/diffusers) - 图像生成库
- [InstructPix2Pix](https://github.com/timothybrooks/instruct-pix2pix) - 图像编辑

---

**上一篇**：[09 计算机视觉基础 - 图像处理与目标检测]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-09-computer-vision %})

**下一篇**：[11 AI Agent智能体 - 自主决策与工具调用]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-11-ai-agent %})

*最后更新: 2026年4月10日*

> 本文参考了 [CLIP论文](https://arxiv.org/abs/2103.00020) 和 [LLaVA项目](https://llava-vl.github.io/) 整理
