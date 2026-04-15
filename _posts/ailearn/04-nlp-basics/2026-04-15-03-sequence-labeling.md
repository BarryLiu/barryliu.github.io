---
layout: post
title: "序列标注实战 - NER与分词"
date: 2026-04-15
categories: ailearn
tags: [AI, NLP, 序列标注, NER]
keywords: 序列标注, NER, 命名实体识别, CRF, BiLSTM-CRF
description: 掌握序列标注任务，实现NER命名实体识别
---

* content
{:toc}

> **前置知识**：需要先掌握 [文本分类]({{ site.baseurl }}{% post_url /ailearn/04-nlp-basics/2026-04-15-02-text-classification %})
>
> **本文重点**：序列标注模型与NER实战

---

## 一、序列标注概述

### 1.1 任务定义

```
序列标注：为序列中的每个元素分配标签

常见任务：
├── 命名实体识别 (NER)
│   识别文本中的人名、地名、机构名等
├── 词性标注 (POS)
│   为每个词标注词性（名词、动词等）
├── 分词
│   判断字是否为词的边界
└── 语义角色标注 (SRL)
    标注谓词论元关系

示例（NER）：
输入：北 京 是 中 国 的 首 都
标签：B-LOC I-LOC O B-LOC I-LOC O O O O

实体：北京(LOC)、中国(LOC)
```

### 1.2 标注体系

```python
"""
常用标注体系：

1. BIO标注
B-X: 实体X的开始
I-X: 实体X的内部
O:   非实体

2. BIOES标注
B-X: 实体开始
I-X: 实体内部
O:   非实体
E-X: 实体结束
S-X: 单字实体

3. BMES标注（中文分词常用）
B: 词首
M: 词中
E: 词尾
S: 单字词
"""

# 标注示例
text = "张三在北京工作"
labels_bio = ["B-PER", "I-PER", "O", "B-LOC", "I-LOC", "O", "O", "O"]

# 实体提取
def extract_entities(tokens, labels):
    """从BIO标签提取实体"""
    entities = []
    current_entity = None
    
    for i, (token, label) in enumerate(zip(tokens, labels)):
        if label.startswith("B-"):
            if current_entity:
                entities.append(current_entity)
            entity_type = label[2:]
            current_entity = {"text": token, "type": entity_type, "start": i}
        elif label.startswith("I-") and current_entity:
            current_entity["text"] += token
        else:
            if current_entity:
                entities.append(current_entity)
                current_entity = None
    
    if current_entity:
        entities.append(current_entity)
    
    return entities

tokens = list("张三在北京工作")
entities = extract_entities(tokens, labels_bio)
print(entities)
# [{'text': '张三', 'type': 'PER', 'start': 0}, {'text': '北京', 'type': 'LOC', 'start': 3}]
```

---

## 二、传统方法

### 2.1 HMM与CRF

```python
"""
隐马尔可夫模型 (HMM)
- 生成式模型
- 假设状态只依赖前一状态
- 简单但表达能力有限

条件随机场 (CRF)
- 判别式模型
- 考虑全局最优
- 可引入丰富特征
- 序列标注经典方法
"""

import sklearn_crfsuite
from sklearn_crfsuite import metrics

def word2features(sent, i):
    """提取特征"""
    word = sent[i]
    
    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
    }
    
    # 前一个词的特征
    if i > 0:
        word1 = sent[i-1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
        })
    else:
        features['BOS'] = True  # 句首
    
    # 后一个词的特征
    if i < len(sent)-1:
        word1 = sent[i+1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
        })
    else:
        features['EOS'] = True  # 句尾
    
    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent_labels):
    return sent_labels

# 示例数据
train_sents = [
    [('张三', 'B-PER'), ('在', 'O'), ('北京', 'B-LOC'), ('工作', 'O')],
    [('苹果', 'B-ORG'), ('公司', 'I-ORG'), ('发布', 'O'), ('新', 'O'), ('产品', 'O')]
]

# 提取特征
X_train = [sent2features(s) for s in train_sents]
y_train = [sent2labels([l for _, l in s]) for s in train_sents]

# 训练CRF
crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True
)

crf.fit(X_train, y_train)

# 预测
y_pred = crf.predict(X_train)
print(metrics.flat_classification_report(y_train, y_pred))
```

---

## 三、深度学习方法

### 3.1 BiLSTM-CRF

```python
import torch
import torch.nn as nn
from torchcrf import CRF

class BiLSTM_CRF(nn.Module):
    """BiLSTM-CRF序列标注模型"""
    
    def __init__(self, vocab_size, tag_size, embedding_dim=100, hidden_dim=200):
        super().__init__()
        
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(
            embedding_dim, hidden_dim // 2,
            num_layers=2,
            bidirectional=True,
            batch_first=True,
            dropout=0.5
        )
        self.hidden2tag = nn.Linear(hidden_dim, tag_size)
        self.crf = CRF(tag_size, batch_first=True)
    
    def forward(self, x, tags=None, mask=None):
        embeddings = self.embedding(x)
        lstm_out, _ = self.lstm(embeddings)
        emissions = self.hidden2tag(lstm_out)
        
        if tags is not None:
            # 训练：返回负对数似然
            loss = -self.crf(emissions, tags, mask=mask)
            return loss
        else:
            # 推理：返回最优路径
            return self.crf.decode(emissions, mask=mask)

# 创建模型
model = BiLSTM_CRF(vocab_size=10000, tag_size=10)
print(f"模型参数量: {sum(p.numel() for p in model.parameters()):,}")
```

### 3.2 训练流程

```python
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence

class NERDataset(Dataset):
    """NER数据集"""
    
    def __init__(self, sentences, tags, word2idx, tag2idx):
        self.sentences = sentences
        self.tags = tags
        self.word2idx = word2idx
        self.tag2idx = tag2idx
    
    def __len__(self):
        return len(self.sentences)
    
    def __getitem__(self, idx):
        sentence = [self.word2idx.get(w, self.word2idx['<UNK>']) for w in self.sentences[idx]]
        tags = [self.tag2idx[t] for t in self.tags[idx]]
        return torch.tensor(sentence), torch.tensor(tags)

def collate_fn(batch):
    """动态padding"""
    sentences, tags = zip(*batch)
    sentences = pad_sequence(sentences, batch_first=True, padding_value=0)
    tags = pad_sequence(tags, batch_first=True, padding_value=0)
    mask = (sentences != 0)
    return sentences, tags, mask

# 训练函数
def train_epoch(model, dataloader, optimizer, device):
    model.train()
    total_loss = 0
    
    for sentences, tags, mask in dataloader:
        sentences = sentences.to(device)
        tags = tags.to(device)
        mask = mask.to(device)
        
        optimizer.zero_grad()
        loss = model(sentences, tags, mask)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    return total_loss / len(dataloader)

# 评估函数
def evaluate(model, dataloader, device, idx2tag):
    model.eval()
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for sentences, tags, mask in dataloader:
            sentences = sentences.to(device)
            mask = mask.to(device)
            
            preds = model(sentences, mask=mask)
            
            for pred, label, m in zip(preds, tags, mask):
                length = m.sum().item()
                all_preds.extend([idx2tag[p] for p in pred[:length]])
                all_labels.extend([idx2tag[l.item()] for l in label[:length]])
    
    return all_preds, all_labels
```

---

## 四、BERT序列标注

### 4.1 BERT-NER

```python
from transformers import BertForTokenClassification, BertTokenizer, Trainer, TrainingArguments

class BertForNER:
    """基于BERT的NER系统"""
    
    def __init__(self, model_name, num_labels):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertForTokenClassification.from_pretrained(
            model_name, 
            num_labels=num_labels
        )
        self.label_map = {
            0: 'O', 1: 'B-PER', 2: 'I-PER',
            3: 'B-LOC', 4: 'I-LOC',
            5: 'B-ORG', 6: 'I-ORG'
        }
    
    def predict(self, text):
        """预测实体"""
        # 分词
        tokens = list(text)
        inputs = self.tokenizer(
            tokens,
            return_tensors='pt',
            is_split_into_words=True,
            truncation=True
        )
        
        # 预测
        outputs = self.model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=2)
        
        # 解码
        labels = [self.label_map[p.item()] for p in predictions[0]]
        
        # 提取实体
        entities = self.extract_entities(tokens, labels)
        return entities
    
    def extract_entities(self, tokens, labels):
        """提取实体"""
        entities = []
        current = None
        
        for token, label in zip(tokens, labels):
            if label.startswith('B-'):
                if current:
                    entities.append(current)
                current = {'text': token, 'type': label[2:]}
            elif label.startswith('I-') and current:
                current['text'] += token
            else:
                if current:
                    entities.append(current)
                    current = None
        
        if current:
            entities.append(current)
        
        return entities

# 使用示例
# ner = BertForNER('bert-base-chinese', num_labels=7)
# entities = ner.predict("张三在北京工作")
# print(entities)
```

### 4.2 处理子词问题

```python
"""
BERT子词处理问题：

问题：BERT使用WordPiece分词，可能将一个词分成多个子词
解决：使用word_ids()对齐标签

"""

def tokenize_and_align_labels(tokenizer, examples):
    """对齐标签与子词"""
    tokenized_inputs = tokenizer(
        examples['tokens'],
        truncation=True,
        is_split_into_words=True
    )
    
    labels = []
    for i, label in enumerate(examples['ner_tags']):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        
        for word_idx in word_ids:
            # 特殊token设为-100
            if word_idx is None:
                label_ids.append(-100)
            # 只给第一个子词分配标签
            elif word_idx != previous_word_idx:
                label_ids.append(label[word_idx])
            # 其他子词设为-100或延续标签
            else:
                label_ids.append(-100)  # 或 label[word_idx] 延续
            
            previous_word_idx = word_idx
        
        labels.append(label_ids)
    
    tokenized_inputs['labels'] = labels
    return tokenized_inputs
```

---

## 五、中文分词

### 5.1 基于序列标注的分词

```python
"""
中文分词 = 序列标注任务

BMES标注：
B: 词首
M: 词中  
E: 词尾
S: 单字词

示例：
输入：我 爱 北 京 天 安 门
标签：S  S  B  E  B  M  E
分词：我/爱/北京/天安门
"""

class BMESTokenizer:
    """基于BMES的分词器"""
    
    def __init__(self, model):
        self.model = model
        self.tag2label = {0: 'B', 1: 'M', 2: 'E', 3: 'S'}
    
    def tokenize(self, text):
        """分词"""
        chars = list(text)
        # 使用模型预测标签
        # tags = self.model.predict(chars)
        # 这里用简单规则演示
        tags = self.simple_predict(chars)
        
        # 根据BMES标签分词
        words = []
        current_word = ""
        
        for char, tag in zip(chars, tags):
            if tag == 'S':
                if current_word:
                    words.append(current_word)
                words.append(char)
                current_word = ""
            elif tag == 'B':
                if current_word:
                    words.append(current_word)
                current_word = char
            elif tag == 'M':
                current_word += char
            elif tag == 'E':
                current_word += char
                words.append(current_word)
                current_word = ""
        
        if current_word:
            words.append(current_word)
        
        return words
    
    def simple_predict(self, chars):
        """简单预测（演示用）"""
        # 实际使用训练好的模型
        tags = []
        for char in chars:
            # 简单规则：标点单字，其他猜测
            if char in '，。！？、；：':
                tags.append('S')
            else:
                tags.append('B')  # 简化
        return tags

# 使用jieba作为对比
import jieba

text = "我爱北京天安门"
print(f"jieba: {list(jieba.cut(text))}")
# print(f"模型: {tokenizer.tokenize(text)}")
```

---

## 六、评估指标

### 6.1 实体级评估

```python
from collections import defaultdict

def evaluate_ner(y_true, y_pred):
    """实体级评估"""
    
    def extract_entities_from_tags(tokens, tags):
        entities = set()
        current = None
        
        for i, (token, tag) in enumerate(zip(tokens, tags)):
            if tag.startswith('B-'):
                if current:
                    entities.add(current)
                current = (tag[2:], i, i)
            elif tag.startswith('I-') and current:
                current = (current[0], current[1], i)
            else:
                if current:
                    entities.add(current)
                    current = None
        
        if current:
            entities.add(current)
        
        return entities
    
    # 计算指标
    tp, fp, fn = 0, 0, 0
    
    for true_tags, pred_tags in zip(y_true, y_pred):
        true_entities = extract_entities_from_tags(range(len(true_tags)), true_tags)
        pred_entities = extract_entities_from_tags(range(len(pred_tags)), pred_tags)
        
        tp += len(true_entities & pred_entities)
        fp += len(pred_entities - true_entities)
        fn += len(true_entities - pred_entities)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'precision': precision,
        'recall': recall,
        'f1': f1
    }
```

---

## 参考资源

> - [BiLSTM-CRF论文](https://arxiv.org/abs/1508.01991) - 经典序列标注模型
> - [CRF原理](https://toutiao.io/posts/13w1q8/preview) - 条件随机场详解
> - [CoNLL-2003数据集](https://www.clips.uantwerpen.be/conll2003/ner/) - NER基准数据
> - [MSRA NER数据](https://github.com/luopeixiang/ner_msra) - 中文NER数据
> - [HuggingFace NER](https://huggingface.co/models?pipeline_tag=token-classification) - 预训练模型
> - [seqeval](https://github.com/chakki-works/seqeval) - 序列标注评估库

---

**上一篇**：[文本分类]({{ site.baseurl }}{% post_url /ailearn/04-nlp-basics/2026-04-15-02-text-classification %})

**返回**：[NLP基础]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-04-nlp-basics %})

*最后更新: 2026年4月15日*
