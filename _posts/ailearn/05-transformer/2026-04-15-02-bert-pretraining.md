---
layout: post
title: "BERT与预训练模型 - NLP新范式"
date: 2026-04-15
categories: ailearn
tags: [AI, NLP, BERT, 预训练模型, Transformer]
keywords: BERT, 预训练, 微调, Hugging Face, 文本分类
description: 深入理解BERT原理，掌握预训练模型微调技术
---

* content
{:toc}

> **前置知识**：需要先掌握 [Transformer基础]({{ site.baseurl }}{% post_url /ailearn/05-transformer/2026-04-15-01-transformer-basics %})
>
> **本文重点**：理解预训练-微调范式，掌握BERT应用

---

## 一、预训练模型概述

### 1.1 NLP发展历程

```
NLP技术演进：

Word2Vec (2013)
├── 词向量表示
├── 静态向量
└── 无法处理多义词

ELMo (2018)
├── 双向LSTM
├── 上下文相关
└── 特征提取模式

BERT (2018)
├── 双向Transformer
├── 深度双向编码
└── 预训练-微调范式

GPT系列 (2018-2023)
├── 单向Transformer
├── 生成式模型
└── GPT-4: 多模态大模型
```

### 1.2 预训练任务

```python
"""
BERT预训练任务：

1. Masked Language Model (MLM)
   - 随机遮蔽15%的词
   - 预测被遮蔽的词
   - 学习双向上下文表示

2. Next Sentence Prediction (NSP)
   - 判断两句话是否连续
   - 学习句子级别关系

GPT预训练任务：
- 因果语言模型 (CLM)
- 预测下一个词
- 单向自回归
"""
```

---

## 二、BERT架构详解

### 2.1 模型结构

```python
import torch
import torch.nn as nn
from transformers import BertModel, BertConfig

# BERT配置
config = BertConfig(
    vocab_size=30522,      # 词表大小
    hidden_size=768,       # 隐藏层维度
    num_hidden_layers=12,  # Transformer层数
    num_attention_heads=12, # 注意力头数
    intermediate_size=3072, # FFN中间层维度
    max_position_embeddings=512, # 最大序列长度
    type_vocab_size=2,     # Segment类型数
    hidden_dropout_prob=0.1,
    attention_probs_dropout_prob=0.1
)

# 创建模型
model = BertModel(config)
print(f"BERT参数量: {sum(p.numel() for p in model.parameters()):,}")

# BERT输入
batch_size, seq_len = 2, 128
input_ids = torch.randint(0, config.vocab_size, (batch_size, seq_len))
attention_mask = torch.ones(batch_size, seq_len)
token_type_ids = torch.zeros(batch_size, seq_len, dtype=torch.long)

# 前向传播
outputs = model(
    input_ids=input_ids,
    attention_mask=attention_mask,
    token_type_ids=token_type_ids
)

last_hidden_state = outputs.last_hidden_state  # (batch, seq_len, hidden_size)
pooler_output = outputs.pooler_output          # (batch, hidden_size)

print(f"序列输出形状: {last_hidden_state.shape}")
print(f"池化输出形状: {pooler_output.shape}")
```

### 2.2 输入表示

```python
from transformers import BertTokenizer

# 加载分词器
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

# 文本编码
text = "自然语言处理很有趣"
encoding = tokenizer(
    text,
    padding='max_length',
    truncation=True,
    max_length=32,
    return_tensors='pt'
)

print(f"Input IDs: {encoding['input_ids']}")
print(f"Attention Mask: {encoding['attention_mask']}")
print(f"Token Type IDs: {encoding['token_type_ids']}")

# 解码
decoded = tokenizer.decode(encoding['input_ids'][0])
print(f"解码: {decoded}")

# BERT特殊Token
print(f"\n特殊Token:")
print(f"[CLS] (分类): {tokenizer.cls_token_id}")
print(f"[SEP] (分隔): {tokenizer.sep_token_id}")
print(f"[PAD] (填充): {tokenizer.pad_token_id}")
print(f"[UNK] (未知): {tokenizer.unk_token_id}")
print(f"[MASK] (遮蔽): {tokenizer.mask_token_id}")
```

---

## 三、BERT微调实战

### 3.1 文本分类

```python
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertForSequenceClassification, BertTokenizer, AdamW
from transformers import get_linear_schedule_with_warmup

class TextClassificationDataset(Dataset):
    """文本分类数据集"""
    
    def __init__(self, texts, labels, tokenizer, max_len=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        
        encoding = self.tokenizer(
            text,
            max_length=self.max_len,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].squeeze(),
            'attention_mask': encoding['attention_mask'].squeeze(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

# 示例数据
texts = [
    "这部电影非常好看，强烈推荐！",
    "浪费时间的烂片，不推荐观看",
    "演员演技在线，剧情精彩",
    "剧情拖沓，看了想睡觉"
]
labels = [1, 0, 1, 0]  # 1:正面, 0:负面

# 创建数据集
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
dataset = TextClassificationDataset(texts, labels, tokenizer)
dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

# 加载预训练模型
model = BertForSequenceClassification.from_pretrained(
    'bert-base-chinese',
    num_labels=2
)

# 训练配置
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
optimizer = AdamW(model.parameters(), lr=2e-5)

# 训练函数
def train_epoch(model, dataloader, optimizer, device):
    model.train()
    total_loss = 0
    
    for batch in dataloader:
        optimizer.zero_grad()
        
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)
        
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    return total_loss / len(dataloader)

# 训练
num_epochs = 3
for epoch in range(num_epochs):
    loss = train_epoch(model, dataloader, optimizer, device)
    print(f"Epoch {epoch+1}, Loss: {loss:.4f}")

# 预测
def predict(text, model, tokenizer, device):
    model.eval()
    encoding = tokenizer(text, return_tensors='pt', max_length=128, 
                         padding='max_length', truncation=True)
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)
    
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        probs = torch.softmax(outputs.logits, dim=1)
        pred = torch.argmax(probs, dim=1)
    
    return pred.item(), probs[0].tolist()

# 测试
test_text = "这部电影剧情太棒了！"
pred, probs = predict(test_text, model, tokenizer, device)
print(f"文本: {test_text}")
print(f"预测: {'正面' if pred == 1 else '负面'}")
print(f"概率: {probs}")
```

### 3.2 命名实体识别

```python
from transformers import BertForTokenClassification

# NER数据集示例
sentences = [
    ["我", "是", "北京", "人"],
    ["苹果", "公司", "在", "加州"]
]
ner_tags = [
    ["O", "O", "B-LOC", "O"],
    ["B-ORG", "I-ORG", "O", "B-LOC"]
]

# 标签到ID映射
tag2id = {"O": 0, "B-LOC": 1, "I-LOC": 2, "B-ORG": 3, "I-ORG": 4}
id2tag = {v: k for k, v in tag2id.items()}

# 加载NER模型
model_ner = BertForTokenClassification.from_pretrained(
    'bert-base-chinese',
    num_labels=len(tag2id)
)

print("NER模型加载完成")
```

### 3.3 问答系统

```python
from transformers import BertForQuestionAnswering

# 加载问答模型
model_qa = BertForQuestionAnswering.from_pretrained('bert-base-chinese-finetuned-squad')

def answer_question(question, context, tokenizer, model):
    """抽取式问答"""
    inputs = tokenizer(question, context, return_tensors='pt')
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    # 获取答案位置
    answer_start = torch.argmax(outputs.start_logits)
    answer_end = torch.argmax(outputs.end_logits) + 1
    
    # 解码答案
    answer = tokenizer.decode(inputs['input_ids'][0][answer_start:answer_end])
    
    return answer

# 示例
context = "北京是中国的首都，位于华北平原北部。"
question = "中国的首都是哪里？"
# answer = answer_question(question, context, tokenizer, model_qa)
# print(f"问题: {question}")
# print(f"答案: {answer}")
```

---

## 四、模型优化技术

### 4.1 知识蒸馏

```python
"""
知识蒸馏：大模型 -> 小模型

Teacher模型：BERT-base (110M参数)
Student模型：DistilBERT (66M参数)

蒸馏损失 = α * 硬标签损失 + (1-α) * 软标签损失
"""
```

### 4.2 量化

```python
# 动态量化
model_quantized = torch.quantization.quantize_dynamic(
    model,
    {torch.nn.Linear},
    dtype=torch.qint8
)

# 比较模型大小
def get_model_size(model):
    torch.save(model.state_dict(), 'temp.pth')
    import os
    size = os.path.getsize('temp.pth') / 1e6
    os.remove('temp.pth')
    return size

print(f"原模型大小: {get_model_size(model):.2f} MB")
print(f"量化后大小: {get_model_size(model_quantized):.2f} MB")
```

### 4.3 剪枝

```python
# 简单的权重剪枝
def prune_model(model, amount=0.2):
    """剪枝20%的权重"""
    for name, param in model.named_parameters():
        if 'weight' in name:
            tensor = param.data.cpu().abs()
            threshold = torch.quantile(tensor.flatten(), amount)
            mask = tensor > threshold
            param.data *= mask.float()
    
    return model

# 剪枝后需要微调恢复性能
```

---

## 参考资源

> - [BERT论文](https://arxiv.org/abs/1810.04805) - BERT: Pre-training of Deep Bidirectional Transformers
> - [Hugging Face Transformers](https://huggingface.co/docs/transformers/) - 预训练模型库
> - [BERT代码解析](https://github.com/google-research/bert) - Google官方实现
> - [如何微调BERT](https://huggingface.co/docs/transformers/training) - HuggingFace教程
> - [DistilBERT](https://huggingface.co/docs/transformers/model_doc/distilbert) - 蒸馏模型
> - [ALBERT](https://arxiv.org/abs/1909.11942) - 轻量级BERT
> - [RoBERTa](https://arxiv.org/abs/1907.11692) - 优化的BERT预训练

---

**上一篇**：[Transformer基础]({{ site.baseurl }}{% post_url /ailearn/05-transformer/2026-04-15-01-transformer-basics %})

**下一篇**：[GPT与大语言模型]({{ site.baseurl }}{% post_url /ailearn/05-transformer/2026-04-15-03-gpt-llm %})

**返回**：[Transformer进阶]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-05-transformer-advanced %})

*最后更新: 2026年4月15日*
