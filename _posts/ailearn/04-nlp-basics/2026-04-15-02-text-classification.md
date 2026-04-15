---
layout: post
title: "文本分类实战 - 从传统方法到深度学习"
date: 2026-04-15
categories: ailearn
tags: [AI, NLP, 文本分类, 深度学习]
keywords: 文本分类, 情感分析, TF-IDF, BERT分类
description: 全面掌握文本分类技术，从传统机器学习到深度学习方法
---

* content
{:toc}

> **前置知识**：需要先掌握 [NLP基础]({{ site.baseurl }}{% post_url /ailearn/04-nlp-basics/2026-04-15-01-nlp-overview %})
>
> **本文重点**：文本分类完整流程与多种方法对比

---

## 一、文本分类概述

### 1.1 任务定义

```
文本分类：给定文本，预测其所属类别

常见应用：
├── 情感分析：正面/负面/中性
├── 新闻分类：体育/财经/科技...
├── 垃圾邮件检测：垃圾/正常
├── 意图识别：查询/下单/投诉...
└── 主题分类：多标签分类
```

### 1.2 方法演进

```
文本分类方法演进：

传统方法 (2010年前)
├── 规则匹配
├── 朴素贝叶斯
├── SVM + TF-IDF
└── 优点：快速、可解释

深度学习 (2014-2018)
├── TextCNN
├── BiLSTM + Attention
├── FastText
└── 优点：自动特征学习

预训练模型 (2018至今)
├── BERT
├── RoBERTa
├── DistilBERT
└── 优点：性能最优、迁移学习
```

---

## 二、传统机器学习方法

### 2.1 数据准备

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix

# 示例数据（实际应用中使用真实数据集）
data = {
    'text': [
        "这部电影太精彩了，强烈推荐！",
        "浪费时间，剧情无聊透顶",
        "演员演技在线，值得一看",
        "简直是烂片中的烂片",
        "还不错，可以看看",
        "完全没有逻辑，差评",
        "经典之作，百看不厌",
        "太失望了，期待落空"
    ],
    'label': [1, 0, 1, 0, 1, 0, 1, 0]  # 1:正面, 0:负面
}

df = pd.DataFrame(data)
print(f"数据量: {len(df)}")
print(f"类别分布:\n{df['label'].value_counts()}")

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(
    df['text'], df['label'], test_size=0.2, random_state=42
)
```

### 2.2 文本预处理

```python
import jieba
import re

class TextPreprocessor:
    """中文文本预处理器"""
    
    def __init__(self, stopwords_path=None):
        self.stopwords = set()
        if stopwords_path:
            with open(stopwords_path, 'r', encoding='utf-8') as f:
                self.stopwords = set(f.read().splitlines())
        
        # 添加基本停用词
        self.stopwords.update(['的', '了', '是', '在', '我', '有', '和', '就',
                               '不', '人', '都', '一', '一个', '上', '也', '很', '要'])
    
    def clean_text(self, text):
        """清洗文本"""
        # 去除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        # 去除特殊字符
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)
        # 去除多余空格
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def tokenize(self, text):
        """分词"""
        return list(jieba.cut(text))
    
    def remove_stopwords(self, tokens):
        """去除停用词"""
        return [t for t in tokens if t not in self.stopwords and len(t) > 1]
    
    def preprocess(self, text):
        """完整预处理流程"""
        text = self.clean_text(text)
        tokens = self.tokenize(text)
        tokens = self.remove_stopwords(tokens)
        return ' '.join(tokens)

# 使用预处理器
preprocessor = TextPreprocessor()
X_train_clean = X_train.apply(preprocessor.preprocess)
X_test_clean = X_test.apply(preprocessor.preprocess)

print("预处理示例:")
print(f"原文: {X_train.iloc[0]}")
print(f"处理后: {X_train_clean.iloc[0]}")
```

### 2.3 TF-IDF + 朴素贝叶斯

```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score

# 创建Pipeline
nb_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
    ('clf', MultinomialNB(alpha=1.0))
])

# 训练
nb_pipeline.fit(X_train_clean, y_train)

# 预测
y_pred = nb_pipeline.predict(X_test_clean)

# 评估
print("朴素贝叶斯结果:")
print(classification_report(y_test, y_pred))

# 交叉验证
cv_scores = cross_val_score(nb_pipeline, X_train_clean, y_train, cv=5)
print(f"交叉验证准确率: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
```

### 2.4 SVM分类器

```python
from sklearn.svm import SVC

svm_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
    ('clf', SVC(kernel='linear', C=1.0))
])

svm_pipeline.fit(X_train_clean, y_train)
y_pred_svm = svm_pipeline.predict(X_test_clean)

print("SVM结果:")
print(classification_report(y_test, y_pred_svm))
```

### 2.5 传统方法对比

```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# 对比多种传统方法
models = {
    'Naive Bayes': MultinomialNB(),
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'SVM': SVC(kernel='linear'),
    'Random Forest': RandomForestClassifier(n_estimators=100)
}

results = []
for name, clf in models.items():
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000)),
        ('clf', clf)
    ])
    
    cv_scores = cross_val_score(pipeline, X_train_clean, y_train, cv=5)
    results.append({
        'Model': name,
        'Mean Acc': cv_scores.mean(),
        'Std': cv_scores.std()
    })

results_df = pd.DataFrame(results)
print(results_df)
```

---

## 三、深度学习方法

### 3.1 TextCNN

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class TextCNN(nn.Module):
    """TextCNN文本分类模型"""
    
    def __init__(self, vocab_size, embedding_dim, num_filters, filter_sizes, num_classes, dropout=0.5):
        super().__init__()
        
        # Embedding层
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        
        # 多尺度卷积
        self.convs = nn.ModuleList([
            nn.Conv2d(1, num_filters, (fs, embedding_dim))
            for fs in filter_sizes
        ])
        
        # 全连接层
        self.fc = nn.Linear(num_filters * len(filter_sizes), num_classes)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x):
        # x: (batch, seq_len)
        embedded = self.embedding(x)  # (batch, seq_len, embed_dim)
        embedded = embedded.unsqueeze(1)  # (batch, 1, seq_len, embed_dim)
        
        # 多尺度卷积
        conv_outputs = []
        for conv in self.convs:
            conv_out = F.relu(conv(embedded)).squeeze(3)  # (batch, num_filters, seq_len - fs + 1)
            pooled = F.max_pool1d(conv_out, conv_out.size(2)).squeeze(2)  # (batch, num_filters)
            conv_outputs.append(pooled)
        
        # 拼接
        concat = torch.cat(conv_outputs, dim=1)  # (batch, num_filters * len(filter_sizes))
        concat = self.dropout(concat)
        
        # 分类
        logits = self.fc(concat)
        return logits

# 创建模型
model = TextCNN(
    vocab_size=10000,
    embedding_dim=128,
    num_filters=100,
    filter_sizes=[3, 4, 5],
    num_classes=2
)
print(f"TextCNN参数量: {sum(p.numel() for p in model.parameters()):,}")
```

### 3.2 BiLSTM + Attention

```python
class Attention(nn.Module):
    """注意力机制"""
    
    def __init__(self, hidden_dim):
        super().__init__()
        self.attention = nn.Linear(hidden_dim, 1)
    
    def forward(self, lstm_output, mask=None):
        # lstm_output: (batch, seq_len, hidden_dim)
        attention_weights = torch.softmax(self.attention(lstm_output), dim=1)
        
        if mask is not None:
            attention_weights = attention_weights * mask.unsqueeze(-1)
        
        context = torch.sum(attention_weights * lstm_output, dim=1)
        return context, attention_weights

class BiLSTMAttention(nn.Module):
    """BiLSTM + Attention文本分类"""
    
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_classes, num_layers=2, dropout=0.5):
        super().__init__()
        
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.lstm = nn.LSTM(
            embedding_dim, hidden_dim // 2,
            num_layers=num_layers,
            bidirectional=True,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )
        self.attention = Attention(hidden_dim)
        self.fc = nn.Linear(hidden_dim, num_classes)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x):
        embedded = self.embedding(x)
        lstm_output, _ = self.lstm(embedded)
        context, _ = self.attention(lstm_output)
        context = self.dropout(context)
        logits = self.fc(context)
        return logits

# 创建模型
model_bilstm = BiLSTMAttention(
    vocab_size=10000,
    embedding_dim=128,
    hidden_dim=256,
    num_classes=2
)
print(f"BiLSTM+Attention参数量: {sum(p.numel() for p in model_bilstm.parameters()):,}")
```

---

## 四、预训练模型方法

### 4.1 BERT文本分类

```python
from transformers import BertForSequenceClassification, BertTokenizer, Trainer, TrainingArguments

# 加载预训练模型
model_name = 'bert-base-chinese'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)

# 数据处理
class TextClassificationDataset(torch.utils.data.Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
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

# 创建数据集
train_dataset = TextClassificationDataset(X_train.tolist(), y_train.tolist(), tokenizer)
test_dataset = TextClassificationDataset(X_test.tolist(), y_test.tolist(), tokenizer)

# 训练参数
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    warmup_steps=100,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    evaluation_strategy='epoch',
    save_strategy='epoch',
    load_best_model_at_end=True
)

# 训练
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)

# trainer.train()
```

### 4.2 预训练模型对比

```python
"""
不同预训练模型对比：

模型              参数量    特点
───────────────────────────────────
BERT-base        110M     双向编码，分类任务首选
BERT-large       340M     更大更强，训练更慢
DistilBERT       66M      轻量化，速度提升60%
RoBERTa          125M     优化预训练策略
ALBERT           12M      参数共享，极轻量
DeBERTa          184M     解耦注意力，性能最优

选择建议：
- 追求性能：DeBERTa > RoBERTa > BERT
- 追求速度：DistilBERT > ALBERT > BERT
- 平衡选择：BERT-base / RoBERTa-base
"""
```

---

## 五、模型优化技巧

### 5.1 数据增强

```python
import random

class TextAugmentation:
    """文本数据增强"""
    
    def __init__(self):
        pass
    
    def random_delete(self, text, p=0.1):
        """随机删除词语"""
        words = text.split()
        if len(words) == 1:
            return text
        new_words = [w for w in words if random.random() > p]
        return ' '.join(new_words) if new_words else words[0]
    
    def random_swap(self, text, n=1):
        """随机交换词语"""
        words = text.split()
        if len(words) < 2:
            return text
        for _ in range(n):
            i, j = random.sample(range(len(words)), 2)
            words[i], words[j] = words[j], words[i]
        return ' '.join(words)
    
    def synonym_replace(self, text, n=1):
        """同义词替换（需要同义词词典）"""
        # 实际应用中需要同义词词典
        # 这里简化处理
        return text
    
    def augment(self, text, num_aug=4):
        """生成多个增强样本"""
        augmented = []
        augmented.append(self.random_delete(text))
        augmented.append(self.random_swap(text))
        # augmented.append(self.synonym_replace(text))
        return augmented

# 使用增强
aug = TextAugmentation()
original = "这部电影 真的 很好看"
print(f"原文: {original}")
for i, aug_text in enumerate(aug.augment(original)):
    print(f"增强{i+1}: {aug_text}")
```

### 5.2 类别不平衡处理

```python
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from sklearn.utils.class_weight import compute_class_weight

# 计算类别权重
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(y_train),
    y=y_train
)
class_weight_dict = dict(enumerate(class_weights))
print(f"类别权重: {class_weight_dict}")

# 在模型中使用类别权重
# PyTorch
criterion = nn.CrossEntropyLoss(weight=torch.tensor(class_weights, dtype=torch.float))

# sklearn
from sklearn.utils.class_weight import compute_sample_weight
sample_weights = compute_sample_weight('balanced', y_train)
```

### 5.3 模型融合

```python
from sklearn.ensemble import VotingClassifier

# 创建多个基模型
estimators = [
    ('nb', Pipeline([('tfidf', TfidfVectorizer()), ('clf', MultinomialNB())])),
    ('svm', Pipeline([('tfidf', TfidfVectorizer()), ('clf', SVC(kernel='linear', probability=True))])),
    ('lr', Pipeline([('tfidf', TfidfVectorizer()), ('clf', LogisticRegression())]))
]

# 投票融合
ensemble = VotingClassifier(estimators, voting='soft')
ensemble.fit(X_train_clean, y_train)

# 预测
y_pred_ensemble = ensemble.predict(X_test_clean)
print("集成模型结果:")
print(classification_report(y_test, y_pred_ensemble))
```

---

## 参考资源

> - [TextCNN论文](https://arxiv.org/abs/1408.5882) - Convolutional Neural Networks for Sentence Classification
> - [FastText](https://arxiv.org/abs/1607.01759) - 分类与词向量学习
> - [HAN论文](https://arxiv.org/abs/1606.01781) - Hierarchical Attention Networks
> - [BERT论文](https://arxiv.org/abs/1810.04805) - 预训练语言模型
> - [中文文本分类数据集](https://github.com/Toyoyu/Dataset_for_Text_Classification) - 公开数据集
> - [NLP数据增强](https://github.com/makcedward/nlpaug) - 数据增强工具

---

**上一篇**：[NLP基础]({{ site.baseurl }}{% post_url /ailearn/04-nlp-basics/2026-04-15-01-nlp-overview %})

**下一篇**：[序列标注实战]({{ site.baseurl }}{% post_url /ailearn/04-nlp-basics/2026-04-15-03-sequence-labeling %})

**返回**：[NLP基础]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-04-nlp-basics %})

*最后更新: 2026年4月15日*
