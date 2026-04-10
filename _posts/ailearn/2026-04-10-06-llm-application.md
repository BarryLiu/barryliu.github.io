---
layout: post
title: "【AI学习路线 06】大模型应用 - 从Prompt工程到微调技术"
date: 2026-04-10
categories: ailearn
tags: [AI, LLM, Prompt, 微调, LoRA, RAG]
keywords: 大语言模型, Prompt工程, LoRA微调, Few-shot, Chain of Thought
description: AI学习路线第6篇 - 掌握大模型应用核心技术，包括Prompt工程、高效微调和应用开发
---

* content
{:toc}

> **学习顺序说明**：本文是AI学习路线的第6篇，建议按顺序学习：
> - 01 入门基础 → 02 机器学习 → 03 深度学习 → 04 NLP基础 → 05 Transformer进阶 → 06 大模型应用（本文）→ 07 RAG系统 → 08 AI工具链

大语言模型(LLM)正在改变AI应用的构建方式。本文将介绍如何有效使用和定制大模型。

## 大模型概述

### 主流大模型

| 模型 | 参数量 | 特点 | 开源 |
|------|--------|------|------|
| GPT-4 | ~1.8T | 多模态、推理能力强 | 否 |
| Claude 3 | ~175B | 长上下文、安全 | 否 |
| LLaMA 3 | 8B-70B | 高性能开源 | 是 |
| Qwen2 | 0.5B-72B | 多语言支持好 | 是 |
| DeepSeek | 7B-67B | 推理能力强 | 是 |

> **参考资源**：[Hugging Face Open LLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard) - 开源模型排行榜

---

## 第一部分：Prompt工程

### 1.1 基础Prompt技巧

**角色设定**

```
你是一位资深的Python开发工程师，擅长编写简洁高效的代码。
请用专业但易懂的方式回答问题。
```

**任务分解**

```
请按以下步骤分析问题：
1. 理解问题的核心需求
2. 列出可能的解决方案
3. 评估各方案的优缺点
4. 给出最佳推荐方案
```

**输出格式控制**

```
请以JSON格式输出结果：
{
  "summary": "问题摘要",
  "solutions": ["方案1", "方案2"],
  "recommendation": "推荐方案"
}
```

### 1.2 Few-shot Learning

```python
# Few-shot Prompt示例
prompt = """
任务：判断文本的情感倾向

示例1：
文本：这个产品非常好用，我很满意！
情感：正面

示例2：
文本：服务态度太差了，再也不来了。
情感：负面

示例3：
文本：今天天气不错，适合出门散步。
情感：正面

现在请判断：
文本：{input_text}
情感：
"""
```

### 1.3 Chain of Thought (CoT)

```
问题：小明有5个苹果，给了小红2个，又买了3个，现在有几个？

请一步步思考：
1. 小明最初有5个苹果
2. 给了小红2个，剩下 5-2=3个
3. 又买了3个，现在有 3+3=6个

答案：6个苹果
```

> **参考资源**：[Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903) - CoT原始论文

### 1.4 使用API调用大模型

```python
import openai
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "你是一个AI助手"},
        {"role": "user", "content": "请解释什么是机器学习"}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

**参数说明**：

| 参数 | 说明 | 建议值 |
|------|------|--------|
| temperature | 随机性 | 0.7 (创意) / 0.2 (事实) |
| top_p | 核采样 | 0.9 |
| max_tokens | 最大输出 | 按需设置 |
| presence_penalty | 话题多样性 | 0.0-1.0 |
| frequency_penalty | 重复惩罚 | 0.0-1.0 |

---

## 第二部分：高效微调技术

### 2.1 LoRA (Low-Rank Adaptation)

LoRA通过低秩分解大幅减少微调参数量。

```python
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM

# 加载基础模型
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf")

# LoRA配置
lora_config = LoraConfig(
    r=16,                    # 低秩维度
    lora_alpha=32,           # 缩放系数
    target_modules=["q_proj", "v_proj"],  # 应用LoRA的模块
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# 应用LoRA
model = get_peft_model(model, lora_config)

# 查看可训练参数
model.print_trainable_parameters()
# 输出: trainable params: 4,194,304 || all params: 6,742,609,920 || trainable%: 0.06%
```

**LoRA原理**：

$$W' = W + \Delta W = W + BA$$

其中 B ∈ R^(d×r), A ∈ R^(r×k), r << min(d, k)

> **参考资源**：[LoRA论文](https://arxiv.org/abs/2106.09685) - LoRA原始论文

### 2.2 QLoRA

QLoRA结合量化和LoRA，进一步降低显存需求。

```python
from transformers import BitsAndBytesConfig

# 量化配置
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

# 加载4-bit量化模型
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=bnb_config,
    device_map="auto"
)
```

### 2.3 微调流程

```python
from transformers import TrainingArguments, Trainer
from datasets import load_dataset

# 加载数据集
dataset = load_dataset("your_dataset")

# 训练参数
training_args = TrainingArguments(
    output_dir="./output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_steps=100,
    evaluation_strategy="steps"
)

# 训练
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer
)

trainer.train()
```

---

## 第三部分：模型推理优化

### 3.1 量化推理

```python
# 8-bit量化
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    load_in_8bit=True,
    device_map="auto"
)

# 4-bit量化 (GPTQ/AWQ)
from auto_gptq import AutoGPTQForCausalLM
model = AutoGPTQForCausalLM.from_quantized("model_path", device_map="auto")
```

### 3.2 vLLM加速推理

```python
from vllm import LLM, SamplingParams

# 加载模型
llm = LLM(model="meta-llama/Llama-2-7b-hf")

# 批量推理
prompts = ["你好", "天气如何", "介绍一下AI"]
sampling_params = SamplingParams(temperature=0.7, max_tokens=100)

outputs = llm.generate(prompts, sampling_params)
for output in outputs:
    print(output.outputs[0].text)
```

### 3.3 流式输出

```python
from transformers import TextIteratorStreamer
from threading import Thread

streamer = TextIteratorStreamer(tokenizer, skip_special_tokens=True)

# 在单独线程中生成
generation_kwargs = {
    "input_ids": input_ids,
    "streamer": streamer,
    "max_new_tokens": 100
}
thread = Thread(target=model.generate, kwargs=generation_kwargs)
thread.start()

# 流式输出
for text in streamer:
    print(text, end="", flush=True)
```

---

## 第四部分：应用开发实践

### 4.1 构建对话机器人

```python
class ChatBot:
    def __init__(self, model_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)
        self.history = []
    
    def chat(self, user_input, max_history=5):
        # 构建对话历史
        self.history.append({"role": "user", "content": user_input})
        
        # 限制历史长度
        if len(self.history) > max_history * 2:
            self.history = self.history[-max_history * 2:]
        
        # 生成回复
        input_text = self.tokenizer.apply_chat_template(
            self.history, tokenize=False, add_generation_prompt=True
        )
        inputs = self.tokenizer(input_text, return_tensors="pt")
        
        outputs = self.model.generate(**inputs, max_new_tokens=512)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # 更新历史
        self.history.append({"role": "assistant", "content": response})
        
        return response
```

### 4.2 构建API服务

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    history: list = []

@app.post("/chat")
async def chat(request: ChatRequest):
    response = bot.chat(request.message)
    return {"response": response}

# 启动: uvicorn app:app --host 0.0.0.0 --port 8000
```

---

## 学习资源

### 官方文档
- [Hugging Face PEFT](https://huggingface.co/docs/peft/index) - 高效微调
- [vLLM](https://vllm.readthedocs.io/) - 推理加速
- [LangChain](https://python.langchain.com/) - 应用开发框架

### 推荐论文
- [LoRA](https://arxiv.org/abs/2106.09685) - 低秩适配
- [QLoRA](https://arxiv.org/abs/2305.14314) - 量化+LoRA
- [Chain-of-Thought](https://arxiv.org/abs/2201.11903) - 思维链

---

**上一篇**：[05 Transformer进阶 - 深入理解注意力机制]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-05-transformer-advanced %})

**下一篇**：[07 RAG系统 - 构建知识增强应用]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-07-rag-system %})

*最后更新: 2026年4月10日*

> 本文参考了 [Hugging Face文档](https://huggingface.co/docs) 和 [PEFT文档](https://huggingface.co/docs/peft) 整理
