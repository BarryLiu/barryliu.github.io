---
layout: post
title: "【AI学习路线 02】机器学习基础 - 从算法原理到实践"
date: 2026-04-10
categories: ailearn
tags: [AI, 机器学习, 算法, scikit-learn]
keywords: 机器学习, 监督学习, 无监督学习, 分类, 回归, 聚类
description: AI学习路线第2篇 - 系统学习机器学习核心算法，从监督学习到无监督学习，理解算法原理并掌握scikit-learn实践
---

* content
{:toc}

> **学习顺序说明**：本文是AI学习路线的第2篇，建议按顺序学习：
> - 01 入门基础 → 02 机器学习（本文）→ 03 深度学习 → 04 NLP基础 → 05 Transformer进阶 → 06 大模型应用 → 07 RAG系统 → 08 AI工具链

机器学习是人工智能的核心领域之一，本文将系统性地介绍机器学习的主要算法类别、核心原理和实践方法。

## 机器学习概述

### 什么是机器学习

机器学习是让计算机从数据中自动学习规律，而无需显式编程的技术。根据学习方式的不同，主要分为以下几类：

```
机器学习
├── 监督学习 (有标签数据)
│   ├── 分类 (离散输出)
│   └── 回归 (连续输出)
├── 无监督学习 (无标签数据)
│   ├── 聚类
│   └── 降维
├── 半监督学习 (部分标签)
└── 强化学习 (奖励反馈)
```

> **核心概念**：
> - **特征(Features)**: 输入数据的属性
> - **标签(Labels)**: 需要预测的目标
> - **训练集**: 用于学习的数据
> - **测试集**: 用于评估的数据
> - **模型**: 学习得到的映射函数

> **参考资源**：[Scikit-learn官方文档](https://scikit-learn.org/stable/) - Python机器学习标准库

---

## 第一部分：监督学习

监督学习是最常见的机器学习类型，每个训练样本都有对应的标签。

### 1.1 线性回归

**原理**：寻找最佳拟合直线，使预测值与真实值的误差最小。

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# 生成示例数据
np.random.seed(42)
X = np.random.randn(100, 1) * 10
y = 2 * X.ravel() + 5 + np.random.randn(100) * 2

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建并训练模型
model = LinearRegression()
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 评估
print(f"权重(w): {model.coef_[0]:.2f}")
print(f"偏置(b): {model.intercept_:.2f}")
print(f"均方误差(MSE): {mean_squared_error(y_test, y_pred):.2f}")
print(f"R²分数: {r2_score(y_test, y_pred):.2f}")
```

**损失函数**：均方误差 (MSE)

$$MSE = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$

> **数学推导**：详见[斯坦福CS229讲义](https://cs229.stanford.edu/notes2022fall/notes2022fall/linear_regression.pdf)

### 1.2 逻辑回归

**原理**：通过Sigmoid函数将线性输出映射到[0,1]区间，用于二分类问题。

```python
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 生成分类数据
X, y = make_classification(n_samples=1000, n_features=2, n_redundant=0, 
                           n_informative=2, random_state=42, n_clusters_per_class=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 训练逻辑回归模型
model = LogisticRegression()
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)  # 预测概率

# 评估
print(f"准确率: {accuracy_score(y_test, y_pred):.2f}")
print("\n混淆矩阵:")
print(confusion_matrix(y_test, y_pred))
print("\n分类报告:")
print(classification_report(y_test, y_pred))
```

### 1.3 决策树

**原理**：通过一系列if-then规则对数据进行划分，形成树状结构。

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.datasets import load_iris

# 加载鸢尾花数据集
iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 训练决策树
model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X_train, y_train)

# 预测与评估
y_pred = model.predict(X_test)
print(f"准确率: {accuracy_score(y_test, y_pred):.2f}")

# 特征重要性
print("\n特征重要性:")
for name, importance in zip(iris.feature_names, model.feature_importances_):
    print(f"  {name}: {importance:.3f}")
```

**关键参数**：
- `max_depth`: 树的最大深度（控制过拟合）
- `min_samples_split`: 分裂节点所需最小样本数
- `min_samples_leaf`: 叶节点最小样本数
- `criterion`: 划分标准（gini或entropy）

> **参考资源**：[决策树算法详解 - 李航《统计学习方法》](https://book.douban.com/subject/33437381/)

### 1.4 随机森林

**原理**：集成多棵决策树，通过Bagging方法降低方差，提高泛化能力。

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

# 生成数据
X, y = make_classification(n_samples=1000, n_features=20, n_informative=10,
                           n_redundant=5, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 训练随机森林
model = RandomForestClassifier(
    n_estimators=100,      # 树的数量
    max_depth=10,         # 最大深度
    min_samples_split=5,  # 分裂最小样本数
    random_state=42,
    n_jobs=-1             # 使用所有CPU核心
)
model.fit(X_train, y_train)

# 评估
y_pred = model.predict(X_test)
print(f"准确率: {accuracy_score(y_test, y_pred):.2f}")

# 特征重要性排序
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]
print("\n特征重要性排序 (前5):")
for i in range(5):
    print(f"  特征 {indices[i]}: {importances[indices[i]]:.3f}")
```

### 1.5 支持向量机 (SVM)

**原理**：找到最优超平面，使不同类别之间的间隔最大化。

```python
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# SVM对特征缩放敏感，需要标准化
model = Pipeline([
    ('scaler', StandardScaler()),
    ('svm', SVC(kernel='rbf', C=1.0, gamma='scale'))
])

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(f"SVM准确率: {accuracy_score(y_test, y_pred):.2f}")
```

**核函数选择**：
- `linear`: 线性核，适用于线性可分数据
- `rbf`: 高斯径向基核，适用于非线性数据
- `poly`: 多项式核
- `sigmoid`: 类似神经网络的核函数

> **参考资源**：[SVM教程 - Stanford CS229](https://cs229.stanford.edu/notes2022fall/notes2022fall/svm.pdf)

---

## 第二部分：无监督学习

无监督学习处理没有标签的数据，发现数据内在结构。

### 2.1 K-Means聚类

**原理**：将数据划分为K个簇，使簇内样本尽可能相似。

```python
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

# 生成聚类数据
X, y_true = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=42)

# 训练K-Means
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
y_pred = kmeans.fit_predict(X)

# 获取聚类中心
centers = kmeans.cluster_centers_

# 肘部法则选择K值
inertias = []
K_range = range(1, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)
```

### 2.2 主成分分析 (PCA)

**原理**：线性降维，找到数据方差最大的方向。

```python
from sklearn.decomposition import PCA
from sklearn.datasets import load_digits

# 加载手写数字数据集
digits = load_digits()
X = digits.data  # 64维特征

# PCA降维到2维
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

print(f"原始维度: {X.shape[1]}")
print(f"降维后维度: {X_pca.shape[1]}")
print(f"解释方差比: {pca.explained_variance_ratio_}")
print(f"累计解释方差: {sum(pca.explained_variance_ratio_):.2%}")
```

### 2.3 DBSCAN

**原理**：基于密度的聚类，可以发现任意形状的簇。

```python
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_moons

# 生成月牙形数据
X, y = make_moons(n_samples=300, noise=0.05, random_state=42)

# DBSCAN聚类
dbscan = DBSCAN(eps=0.3, min_samples=5)
y_pred = dbscan.fit_predict(X)
```

---

## 第三部分：模型评估

### 3.1 分类评估指标

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score, roc_curve, confusion_matrix
)

# 假设有真实标签和预测结果
y_true = np.array([0, 1, 0, 1, 0, 1, 1, 0, 1, 0])
y_pred = np.array([0, 1, 0, 1, 0, 0, 1, 0, 1, 1])
y_prob = np.array([0.1, 0.9, 0.2, 0.8, 0.1, 0.3, 0.7, 0.2, 0.9, 0.6])

# 计算各指标
print(f"准确率(Accuracy): {accuracy_score(y_true, y_pred):.3f}")
print(f"精确率(Precision): {precision_score(y_true, y_pred):.3f}")
print(f"召回率(Recall): {recall_score(y_true, y_pred):.3f}")
print(f"F1分数: {f1_score(y_true, y_pred):.3f}")
print(f"AUC-ROC: {roc_auc_score(y_true, y_prob):.3f}")
```

**指标解释**：

| 指标 | 公式 | 说明 |
|------|------|------|
| 准确率 | (TP+TN)/(TP+TN+FP+FN) | 预测正确的比例 |
| 精确率 | TP/(TP+FP) | 预测为正中真正为正的比例 |
| 召回率 | TP/(TP+FN) | 真正为正中被预测为正的比例 |
| F1分数 | 2*P*R/(P+R) | 精确率和召回率的调和平均 |

### 3.2 交叉验证

```python
from sklearn.model_selection import cross_val_score, GridSearchCV

# K折交叉验证
model = RandomForestClassifier(n_estimators=100, random_state=42)
cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')

print(f"5折交叉验证结果: {cv_scores}")
print(f"平均准确率: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")

# 网格搜索调参
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)
grid_search.fit(X_train, y_train)

print(f"\n最佳参数: {grid_search.best_params_}")
print(f"最佳得分: {grid_search.best_score_:.3f}")
```

---

## 学习建议

### 推荐学习路径

```
线性回归 → 逻辑回归 → 决策树 → 集成方法 → SVM → 无监督学习
```

### 推荐书籍

| 书籍 | 作者 | 特点 |
|------|------|------|
| 《机器学习》 | 周志华 | 西瓜书，国内经典教材 |
| 《统计学习方法》 | 李航 | 算法推导详细 |
| 《Hands-On Machine Learning》 | Aurélien Géron | 实践导向 |
| 《机器学习实战》 | Peter Harrington | 代码实现 |

### 在线资源

- [Scikit-learn官方文档](https://scikit-learn.org/stable/) - 最权威的参考资料
- [Kaggle Learn](https://www.kaggle.com/learn) - 实践教程
- [吴恩达机器学习课程](https://www.coursera.org/learn/machine-learning) - 经典入门课程
- [李宏毅机器学习](https://www.youtube.com/c/HungyiLeeNTU) - 中文视频教程

---

**上一篇**：[01 入门基础 - 数学与编程基础]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-01-ai-foundation %})

**下一篇**：[03 深度学习基础 - 神经网络理论与实践]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-03-deep-learning %})

*最后更新: 2026年4月10日*

> 本文参考了 [Scikit-learn官方文档](https://scikit-learn.org/stable/) 和 [DeepSeek技术社区](https://deepseek.csdn.net/6824682ee47cbf761b6d0f22.html) 的学习路线整理
