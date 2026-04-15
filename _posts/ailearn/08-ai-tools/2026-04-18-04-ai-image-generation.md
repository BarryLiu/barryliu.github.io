---
layout: post
title: "AI绘图工具指南 - Stable Diffusion与Midjourney"
date: 2026-04-18
categories: ailearn
tags: [AI, 绘图, Stable Diffusion, Midjourney]
keywords: AI绘图, Stable Diffusion, Midjourney, 文生图, 提示词
description: 全面掌握主流AI绘图工具，创作高质量AI艺术作品
---

* content
{:toc}

> **前置知识**：了解基本的AI概念
>
> **本文重点**：主流AI绘图工具使用与提示词技巧

---

## 一、AI绘图概述

### 1.1 技术原理

```
AI绘图核心技术：扩散模型 (Diffusion Model)

工作原理：
1. 前向扩散：逐步向图像添加噪声
2. 反向去噪：学习从噪声恢复图像
3. 条件引导：通过文本提示控制生成

主流模型：
├── Stable Diffusion: 开源、可本地部署
├── Midjourney: 托管服务、艺术效果强
├── DALL-E 3: OpenAI、理解能力强
└── Adobe Firefly: 商业安全、版权友好
```

### 1.2 工具对比

```
AI绘图工具对比：

┌─────────────┬──────────┬──────────┬──────────┬──────────┐
│    特性      │    SD    │   MJ     │  DALL-E  │ Firefly  │
├─────────────┼──────────┼──────────┼──────────┼──────────┤
│ 开源免费     │    ✓     │    ✗     │    ✗     │    ✗     │
│ 本地部署     │    ✓     │    ✗     │    ✗     │    ✗     │
│ 商业使用     │    ✓     │ 付费版   │  付费    │    ✓     │
│ 学习曲线     │   陡峭   │   平缓   │   平缓   │   平缓   │
│ 控制精细度   │    高    │   中     │   中     │   中     │
│ 艺术风格     │   多样   │   强     │   中     │   中     │
│ 中文支持     │   一般   │   弱     │   强     │   强     │
└─────────────┴──────────┴──────────┴──────────┴──────────┘
```

---

## 二、Stable Diffusion

### 2.1 本地部署

```bash
# 方案一：使用Automatic1111 WebUI（推荐）
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
cd stable-diffusion-webui
./webui.sh

# 方案二：使用ComfyUI（节点式工作流）
git clone https://github.com/comfyanonymous/ComfyUI.git
# 按照README安装依赖

# 方案三：使用Diffusers库（Python）
pip install diffusers transformers accelerate
```

### 2.2 Python API使用

```python
from diffusers import StableDiffusionPipeline
import torch

# 加载模型
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    safety_checker=None
)
pipe = pipe.to("cuda")

# 生成图像
prompt = "a beautiful sunset over the ocean, highly detailed, 4k"
negative_prompt = "blurry, low quality, distorted"

image = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    num_inference_steps=30,
    guidance_scale=7.5,
    width=512,
    height=512
).images[0]

image.save("output.png")
```

### 2.3 提示词技巧

```python
"""
Stable Diffusion提示词结构：

[主体描述] + [风格] + [质量词] + [技术参数]

示例：
- 主体：a young woman with long hair
- 风格：in the style of anime, studio ghibli
- 质量：masterpiece, best quality, highly detailed
- 技术：8k uhd, sharp focus, cinematic lighting

负向提示词（避免出现的内容）：
- blurry, low quality, distorted
- bad anatomy, extra fingers, missing limbs
- watermark, text, signature
"""

# 高质量提示词模板
quality_prompts = {
    "realistic": """
        masterpiece, best quality, ultra realistic, 
        8k uhd, photorealistic, sharp focus,
        cinematic lighting, highly detailed,
        professional photography
    """,
    
    "anime": """
        masterpiece, best quality, anime style,
        highly detailed, vibrant colors,
        studio ghibli style, makoto shinkai
    """,
    
    "fantasy": """
        masterpiece, best quality, fantasy art,
        digital painting, concept art,
        trending on artstation, detailed
    """
}

negative_prompts = """
    low quality, bad quality, sketches, 
    bad anatomy, deformed, disfigured, 
    extra limbs, missing limbs, 
    floating limbs, disconnected limbs,
    mutation, mutated, ugly, disgusting,
    blurry, amputation, watermark, text
"""

def generate_with_style(prompt, style="realistic"):
    """带风格模板的生成"""
    full_prompt = f"{prompt}, {quality_prompts[style]}"
    
    image = pipe(
        prompt=full_prompt,
        negative_prompt=negative_prompts,
        num_inference_steps=30,
        guidance_scale=7.5
    ).images[0]
    
    return image
```

### 2.4 高级功能

```python
# 1. 图生图 (Image-to-Image)
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image

img2img = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda")

init_image = Image.open("input.png").convert("RGB")
init_image = init_image.resize((512, 512))

image = img2img(
    prompt="a oil painting of the image",
    image=init_image,
    strength=0.75,  # 变换强度 0-1
    guidance_scale=7.5
).images[0]

# 2. 局部重绘 (Inpainting)
from diffusers import StableDiffusionInpaintPipeline

inpaint = StableDiffusionInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-inpainting",
    torch_dtype=torch.float16
).to("cuda")

# 原图和掩码图
original = Image.open("original.png")
mask = Image.open("mask.png")  # 白色区域将被重绘

result = inpaint(
    prompt="a cat sitting on the chair",
    image=original,
    mask_image=mask,
    guidance_scale=7.5
).images[0]

# 3. ControlNet（精确控制）
# pip install controlnet-aux

from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from diffusers.utils import load_image

# 加载ControlNet模型
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-canny",
    torch_dtype=torch.float16
)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch.float16
).to("cuda")

# 准备控制图像（如边缘检测图）
control_image = load_image("control.png")

image = pipe(
    prompt="a modern building",
    image=control_image,
    num_inference_steps=20
).images[0]
```

---

## 三、Midjourney

### 3.1 基本使用

```
Midjourney通过Discord使用：

基本命令：
/imagine prompt: [描述]
/blend: 混合多张图片
/describe: 根据图片生成描述
/shorten: 优化提示词

参数：
--ar 16:9     设置宽高比
--v 6         使用版本6
--q 2         质量参数(1-2)
--s 750       风格化程度(0-1000)
--c 50        混沌度(0-100)
--seed 12345  随机种子
--no xxx      负向提示词
```

### 3.2 提示词技巧

```
Midjourney提示词结构：

[主体] + [环境] + [风格] + [参数]

示例提示词：

1. 人像：
A portrait of a young woman, 
soft natural lighting, 
bokeh background, 
shot on 85mm lens, 
cinematic look --ar 2:3 --v 6

2. 风景：
Majestic mountain landscape at sunset, 
dramatic clouds, 
golden hour lighting, 
epic scale, 
photorealistic --ar 16:9 --v 6

3. 概念艺术：
A futuristic city with flying cars, 
neon lights reflecting on wet streets, 
cyberpunk style, 
highly detailed --ar 21:9 --v 6

4. 产品渲染：
Smart watch product photography, 
minimalist white background, 
studio lighting, 
professional product shot --ar 1:1 --v 6

风格关键词：
- photorealistic: 照片级真实
- anime: 动漫风格
- oil painting: 油画风格
- watercolor: 水彩画
- 3d render: 3D渲染
- pixel art: 像素艺术
- minimalist: 极简主义
```

### 3.3 高级技巧

```
1. 多提示词（权重控制）
cat::2, dog::1  # cat权重是dog的两倍

2. 图像提示
/imagine prompt: https://url1.png https://url2.png 
a blend of these images --iw 0.5

3. 平铺图案
/seamless pattern of flowers, 
repeating design --tile

4. 角色一致性（使用角色参考）
--cref https://url.png

5. 风格参考
--sref https://style-image.png

6. 负向提示词
beautiful landscape --no people, buildings

7. Niji模式（动漫专用）
/niji prompt: anime girl, detailed
```

---

## 四、DALL-E 3

### 4.1 API使用

```python
from openai import OpenAI

client = OpenAI()

# 生成图像
response = client.images.generate(
    model="dall-e-3",
    prompt="a futuristic city at night with neon lights",
    size="1024x1024",
    quality="hd",  # standard or hd
    n=1,
    style="vivid"  # vivid or natural
)

image_url = response.data[0].url
print(f"图像URL: {image_url}")

# 图像编辑
response = client.images.edit(
    model="dall-e-2",
    image=open("original.png", "rb"),
    mask=open("mask.png", "rb"),
    prompt="add a cat to the image",
    n=1,
    size="1024x1024"
)

# 变体生成
response = client.images.create_variation(
    image=open("original.png", "rb"),
    n=3,
    size="1024x1024"
)
```

### 4.2 提示词优化

```python
"""
DALL-E 3提示词特点：
- 自然语言理解强
- 支持复杂描述
- 会自动优化提示词

提示词建议：
1. 描述性强：详细描述场景
2. 指定风格：明确艺术风格
3. 说明用途：如"海报设计"
"""

# 提示词示例
prompts = [
    # 插画
    """A whimsical children's book illustration showing 
    a small mouse having a tea party with a butterfly 
    in a cozy mushroom house, warm colors, gentle lighting""",
    
    # 产品
    """Professional product photography of a luxury 
    watch on a dark marble surface, dramatic lighting, 
    reflecting the watch's gold details, high-end 
    advertisement style""",
    
    # 概念艺术
    """A digital concept art of a floating island city 
    with waterfalls cascading over the edges, 
    bioluminescent plants, fantasy architecture, 
    epic scale, dramatic sky"""
]
```

---

## 五、提示词工程

### 5.1 通用提示词模板

```python
class ImagePromptBuilder:
    """AI绘图提示词构建器"""
    
    def __init__(self):
        self.subject = ""
        self.style = ""
        self.quality = ""
        self.lighting = ""
        self.composition = ""
        self.negative = ""
    
    def set_subject(self, subject):
        self.subject = subject
        return self
    
    def set_style(self, style):
        style_map = {
            "realistic": "photorealistic, ultra realistic, real life",
            "anime": "anime style, manga style, cel shading",
            "oil_painting": "oil painting, classical art, masterpiece",
            "digital_art": "digital art, concept art, digital painting",
            "3d": "3d render, octane render, unreal engine",
        }
        self.style = style_map.get(style, style)
        return self
    
    def set_quality(self, level="high"):
        quality_map = {
            "high": "masterpiece, best quality, highly detailed, 8k",
            "medium": "good quality, detailed",
            "low": "normal quality"
        }
        self.quality = quality_map.get(level, level)
        return self
    
    def set_lighting(self, lighting):
        lighting_map = {
            "golden_hour": "golden hour lighting, warm tones",
            "blue_hour": "blue hour, cool tones, twilight",
            "studio": "studio lighting, soft light, professional",
            "dramatic": "dramatic lighting, high contrast, chiaroscuro",
        }
        self.lighting = lighting_map.get(lighting, lighting)
        return self
    
    def set_composition(self, composition):
        composition_map = {
            "portrait": "portrait shot, bokeh background, 85mm",
            "landscape": "landscape shot, wide angle, panoramic",
            "closeup": "close-up shot, macro, detailed",
            "full_body": "full body shot, fashion photography",
        }
        self.composition = composition_map.get(composition, composition)
        return self
    
    def set_negative(self, negative):
        self.negative = negative
        return self
    
    def build(self):
        prompt_parts = [
            self.subject,
            self.style,
            self.quality,
            self.lighting,
            self.composition
        ]
        prompt = ", ".join([p for p in prompt_parts if p])
        
        return {
            "prompt": prompt,
            "negative_prompt": self.negative
        }

# 使用示例
builder = ImagePromptBuilder()
result = builder.set_subject("a beautiful woman in a garden") \
               .set_style("realistic") \
               .set_quality("high") \
               .set_lighting("golden_hour") \
               .set_composition("portrait") \
               .set_negative("blurry, low quality, distorted") \
               .build()

print(result["prompt"])
```

### 5.2 风格参考库

```python
style_library = {
    "photography": {
        "portrait": "professional portrait photography, bokeh, 85mm lens, studio lighting",
        "landscape": "epic landscape photography, wide angle, natural lighting, 16k",
        "macro": "macro photography, extreme detail, shallow depth of field",
        "street": "street photography, candid, urban, documentary style"
    },
    
    "art": {
        "oil_painting": "oil painting, classical art, impasto, rich colors",
        "watercolor": "watercolor painting, soft edges, flowing colors",
        "impressionism": "impressionism style, Claude Monet, visible brushstrokes",
        "surrealism": "surrealism, Salvador Dali style, dreamlike, impossible scenes"
    },
    
    "digital": {
        "concept_art": "concept art, digital painting, artstation trending",
        "fantasy": "fantasy art, magical, epic, detailed digital painting",
        "scifi": "science fiction art, futuristic, cyberpunk, neon lights",
        "anime": "anime style, manga, Japanese animation, vibrant colors"
    },
    
    "3d": {
        "realistic_3d": "3d render, octane render, unreal engine 5, ray tracing",
        "stylized_3d": "stylized 3d, Pixar style, cartoon render",
        "architectural": "architectural visualization, interior design, clean lines"
    }
}
```

---

## 参考资源

> - [Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) - 最流行的界面
> - [ComfyUI](https://github.com/comfyanonymous/ComfyUI) - 节点式工作流
> - [Midjourney文档](https://docs.midjourney.com/) - 官方指南
> - [DALL-E API](https://platform.openai.com/docs/guides/images) - OpenAI图像API
> - [Civitai](https://civitai.com/) - 模型与作品分享平台
> - [PromptHero](https://prompthero.com/) - 提示词搜索库
> - [ControlNet](https://github.com/lllyasviel/ControlNet) - 精确控制生成

---

**上一篇**：[MCP协议详解]({{ site.baseurl }}{% post_url /ailearn/08-ai-tools/2026-04-18-03-mcp-protocol %})

**返回**：[AI工具链]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-08-ai-tools %})

*最后更新: 2026年4月18日*
