---
layout: post
title: "NLP基础 - 文本处理与词向量"
date: 2026-04-15
categories: ailearn
tags: [AI, NLP, 自然语言处理, 词向量]
keywords: NLP, 文本处理, Word2Vec, 词嵌入, 文本分类
description: 深入学习自然语言处理基础，掌握文本处理流程与词向量技术
---

* content
{:toc}

> **前置知识**：需要先掌握 [深度学习基础]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-03-deep-learning %})
>
> **本文重点**：理解NLP基础概念，掌握文本处理与词向量

---

## 一、NLP概述

### 1.1 什么是自然语言处理

NLP是让计算机理解、生成和处理人类语言的技术。

```
NLP任务分类：
├── 文本分类
│   ├── 情感分析
│   ├── 文本分类
│   └── 垃圾邮件检测
├── 序列标注
│   ├── 命名实体识别 (NER)
│   ├── 词性标注 (POS)
│   └── 分词
├── 文本生成
│   ├── 机器翻译
│   ├── 文本摘要
│   └── 对话系统
└── 关系抽取
    ├── 语义关系
    └── 知识图谱
```

### 1.2 NLP开发环境

```python
# 常用库安装
# pip install nltk spacy gensim transformers datasets

import nltk
import spacy
import re
from collections import Counter

# 下载NLTK数据
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

print("NLP开发环境准备完成")
```

---

## 二、文本预处理

### 2.1 文本清洗

```python
import re
import string

# 示例文本
text = """
Hello World! This is a sample text with <html>HTML tags</html>, 
URLs like https://example.com, and numbers 12345.
Don't forget emails: test@example.com
"""

def clean_text(text):
    """文本清洗"""
    # 转小写
    text = text.lower()
    
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    
    # 移除URL
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # 移除邮箱
    text = re.sub(r'\S+@\S+', '', text)
    
    # 移除数字
    text = re.sub(r'\d+', '', text)
    
    # 移除标点
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # 移除多余空格
    text = ' '.join(text.split())
    
    return text

cleaned = clean_text(text)
print(f"清洗后: {cleaned}")
```

### 2.2 分词

```python
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

text = "Hello World! How are you today? I'm learning NLP."

# 句子分词
sentences = sent_tokenize(text)
print(f"句子: {sentences}")

# 单词分词
words = word_tokenize(text)
print(f"单词: {words}")

# 使用spaCy
try:
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    spacy_tokens = [token.text for token in doc]
    print(f"spaCy分词: {spacy_tokens}")
except:
    print("spaCy模型未安装，运行: python -m spacy download en_core_web_sm")

# 中文分词
try:
    import jieba
    chinese_text = "自然语言处理是人工智能的重要分支"
    chinese_tokens = jieba.lcut(chinese_text)
    print(f"中文分词: {chinese_tokens}")
except:
    print("jieba未安装，运行: pip install jieba")
```

### 2.3 去停用词

```python
from nltk.corpus import stopwords

# 获取英文停用词
stop_words = set(stopwords.words('english'))

text = "This is a sample sentence with some common words"
tokens = word_tokenize(text.lower())

filtered_tokens = [w for w in tokens if w not in stop_words]
print(f"原词: {tokens}")
print(f"过滤后: {filtered_tokens}")

# 自定义停用词
custom_stopwords = stop_words.union({'said', 'would', 'could'})
```

### 2.4 词形还原与词干提取

```python
from nltk.stem import PorterStemmer, WordNetLemmatizer

# 词干提取 (粗略)
stemmer = PorterStemmer()
words = ['running', 'ran', 'runs', 'easily', 'fairly']
stems = [stemmer.stem(w) for w in words]
print(f"词干提取: {list(zip(words, stems))}")

# 词形还原 (精确)
lemmatizer = WordNetLemmatizer()
lemmas = [lemmatizer.lemmatize(w, pos='v') for w in words]  # pos='v' 指定为动词
print(f"词形还原: {list(zip(words, lemmas))}")
```

---

## 三、词向量

### 3.1 One-Hot编码

```python
import numpy as np

# 词汇表
vocab = ['cat', 'dog', 'bird', 'fish']
word2idx = {w: i for i, w in enumerate(vocab)}

def one_hot_encode(word, vocab_size):
    """One-Hot编码"""
    vec = np.zeros(vocab_size)
    vec[word2idx[word]] = 1
    return vec

for word in vocab:
    print(f"{word}: {one_hot_encode(word, len(vocab))}")

print("\n缺点: 维度高、稀疏、无法表达语义相似性")
```

### 3.2 Word2Vec

```python
from gensim.models import Word2Vec
from gensim.test.utils import common_texts

print("示例语料:")
print(common_texts[:5])

# 训练Word2Vec
model = Word2Vec(
    sentences=common_texts,
    vector_size=100,  # 词向量维度
    window=5,         # 上下文窗口
    min_count=1,      # 最小词频
    workers=4,
    sg=0              # 0=CBOW, 1=Skip-gram
)

# 获取词向量
word_vector = model.wv['computer']
print(f"\n'computer'词向量形状: {word_vector.shape}")

# 相似词
similar_words = model.wv.most_similar('computer', topn=5)
print(f"\n与'computer'相似的词:")
for word, score in similar_words:
    print(f"  {word}: {score:.4f}")

# 类比推理: king - man + woman = queen
try:
    result = model.wv.most_similar(positive=['king', 'woman'], negative=['man'], topn=1)
    print(f"\nking - man + woman = {result}")
except:
    print("\n语料太小，无法进行类比推理")
```

### 3.3 GloVe

```python
# GloVe: Global Vectors for Word Representation
# 预训练词向量下载: https://nlp.stanford.edu/projects/glove/

def load_glove_embeddings(file_path):
    """加载预训练GloVe词向量"""
    embeddings = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], dtype='float32')
            embeddings[word] = vector
    return embeddings

# 使用示例 (需要下载glove.6B.50d.txt)
# glove = load_glove_embeddings('glove.6B.50d.txt')
# print(f"词汇量: {len(glove)}")
# print(f"'the'的词向量: {glove.get('the', '未找到')}")

print("GloVe特点: 利用全局共现统计，更好的语义捕捉")
```

### 3.4 FastText

```python
from gensim.models import FastText

# FastText: 考虑子词信息，能处理未登录词
fasttext_model = FastText(
    sentences=common_texts,
    vector_size=100,
    window=5,
    min_count=1,
    workers=4
)

# 可以处理未登录词 (通过子词向量组合)
oov_word = 'computering'  # 未登录词
try:
    oov_vector = fasttext_model.wv[oov_word]
    print(f"未登录词 '{oov_word}' 向量形状: {oov_vector.shape}")
except:
    print("未登录词处理")
```

---

## 四、文本分类实战

### 4.1 数据准备

```python
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from collections import Counter
import numpy as np

# 模拟电影评论数据
reviews = [
    ("This movie was excellent, I loved it!", 1),
    ("Terrible film, waste of time", 0),
    ("Amazing acting and great story", 1),
    ("Boring and predictable plot", 0),
    ("One of the best movies this year", 1),
    ("I fell asleep during this movie", 0),
    ("Highly recommended!", 1),
    ("Don't waste your money", 0),
    ("Brilliant performance by the lead actor", 1),
    ("Poor script and bad direction", 0),
]

# 构建词汇表
def build_vocab(texts, min_freq=1):
    counter = Counter()
    for text, _ in texts:
        tokens = text.lower().split()
        counter.update(tokens)
    
    vocab = {'<PAD>': 0, '<UNK>': 1}
    for word, freq in counter.items():
        if freq >= min_freq:
            vocab[word] = len(vocab)
    
    return vocab

vocab = build_vocab(reviews)
print(f"词汇表大小: {len(vocab)}")

# 编码函数
def encode_text(text, vocab, max_len=20):
    tokens = text.lower().split()
    ids = [vocab.get(t, vocab['<UNK>']) for t in tokens]
    # 填充或截断
    if len(ids) < max_len:
        ids += [vocab['<PAD>']] * (max_len - len(ids))
    else:
        ids = ids[:max_len]
    return ids

# 数据集类
class TextDataset(Dataset):
    def __init__(self, data, vocab, max_len=20):
        self.data = data
        self.vocab = vocab
        self.max_len = max_len
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        text, label = self.data[idx]
        ids = encode_text(text, self.vocab, self.max_len)
        return torch.LongTensor(ids), torch.LongTensor([label])

# 创建数据集
dataset = TextDataset(reviews, vocab)
dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

print(f"\n数据集大小: {len(dataset)}")
```

### 4.2 文本分类模型

```python
class TextClassifier(nn.Module):
    """基于词嵌入的文本分类器"""
    
    def __init__(self, vocab_size, embed_dim, hidden_size, num_classes, padding_idx=0):
        super(TextClassifier, self).__init__()
        
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=padding_idx)
        
        # 方案1: 平均池化
        self.fc = nn.Sequential(
            nn.Linear(embed_dim, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, num_classes)
        )
    
    def forward(self, x):
        # x: (batch, seq_len)
        embedded = self.embedding(x)  # (batch, seq, embed_dim)
        
        # 平均池化
        mask = (x != 0).unsqueeze(-1).float()
        embedded = embedded * mask
        pooled = embedded.sum(dim=1) / (mask.sum(dim=1) + 1e-8)
        
        # 分类
        out = self.fc(pooled)
        return out

# 创建模型
model = TextClassifier(
    vocab_size=len(vocab),
    embed_dim=50,
    hidden_size=32,
    num_classes=2
)

print("文本分类模型:")
print(model)
```

### 4.3 训练与评估

```python
# 训练配置
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# 训练
num_epochs = 20
for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    
    for texts, labels in dataloader:
        texts, labels = texts.to(device), labels.squeeze().to(device)
        
        optimizer.zero_grad()
        outputs = model(texts)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    if (epoch + 1) % 5 == 0:
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {total_loss/len(dataloader):.4f}")

# 预测函数
def predict_sentiment(text, model, vocab, device):
    model.eval()
    ids = torch.LongTensor([encode_text(text, vocab)]).to(device)
    
    with torch.no_grad():
        output = model(ids)
        prob = torch.softmax(output, dim=1)
        pred = output.argmax(dim=1).item()
    
    sentiment = "正面" if pred == 1 else "负面"
    return sentiment, prob[0][pred].item()

# 测试
test_texts = [
    "This movie was fantastic!",
    "I did not like this film at all",
    "Great acting and wonderful story"
]

print("\n预测结果:")
for text in test_texts:
    sentiment, prob = predict_sentiment(text, model, vocab, device)
    print(f"  '{text}' -> {sentiment} ({prob:.2%})")
```

---

## 参考资源

> - [Speech and Language Processing](https://web.stanford.edu/~jurafsky/slp3/) - NLP经典教材
> - [Natural Language Processing with Python](https://www.nltk.org/book/) - NLTK官方书籍
> - [spaCy官方文档](https://spacy.io/usage) - 工业级NLP库
> - [Word2Vec论文](https://arxiv.org/abs/1301.3781) - Efficient Estimation of Word Representations
> - [GloVe论文](https://nlp.stanford.edu/pubs/glove.pdf) - Global Vectors for Word Representation
> - [CS224n: NLP with Deep Learning](http://web.stanford.edu/class/cs224n/) - 斯坦福NLP课程
> - [Hugging Face NLP Course](https://huggingface.co/learn/nlp-course) - 现代NLP教程

---

**下一篇**：[文本表示进阶]({{ site.baseurl }}{% post_url /ailearn/04-nlp-basics/2026-04-15-02-text-representation %})

**返回**：[NLP基础]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-04-nlp-basics %})

*最后更新: 2026年4月15日*
