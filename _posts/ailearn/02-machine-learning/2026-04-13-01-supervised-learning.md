---
layout: post
title: "监督学习算法详解 - 线性模型与决策树"
date: 2026-04-13
categories: ailearn
tags: [AI, 机器学习, 监督学习, scikit-learn]
keywords: 线性回归, 逻辑回归, 决策树, 分类, 回归
description: 深入学习监督学习核心算法，掌握线性回归、逻辑回归、决策树的原理与实现
---

* content
{:toc}

> **前置知识**：需要先掌握 [NumPy/Pandas基础]({{ site.baseurl }}{% post_url /ailearn/01-numpy-pandas/2026-04-12-numpy-basic %})
>
> **本文重点**：理解监督学习核心算法原理，掌握 scikit-learn 实现

---

## 一、监督学习概述

### 1.1 什么是监督学习

监督学习是最常见的机器学习类型，核心特点是**每个训练样本都有对应的标签**。

```
监督学习
├── 回归问题 (连续输出)
│   ├── 线性回归
│   ├── 岭回归
│   └── 支持向量回归
└── 分类问题 (离散输出)
    ├── 逻辑回归
    ├── 决策树
    ├── 支持向量机
    └── 集成方法
```

### 1.2 核心概念

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# 核心概念示例
"""
特征 (Features): 输入数据的属性，记为 X
标签 (Labels): 需要预测的目标，记为 y
训练集: 用于学习模型参数的数据
测试集: 用于评估模型性能的数据
模型: 学习得到的映射函数 f: X -> y
"""

# 示例：房价预测
# 特征: 面积、卧室数、位置等
# 标签: 房价

# 生成示例数据
np.random.seed(42)
n_samples = 1000

# 特征
area = np.random.uniform(50, 200, n_samples)      # 面积 50-200平米
bedrooms = np.random.randint(1, 5, n_samples)     # 卧室数 1-4
floor = np.random.randint(1, 20, n_samples)       # 楼层 1-19
distance = np.random.uniform(1, 20, n_samples)    # 距地铁距离

X = np.column_stack([area, bedrooms, floor, distance])

# 标签：房价 = 基础价 + 面积*单价 + 卧室数*附加值 - 距离*折价 + 噪声
y = 50 + area * 3 + bedrooms * 10 - distance * 2 + np.random.randn(n_samples) * 10

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"训练集大小: {X_train.shape}")
print(f"测试集大小: {X_test.shape}")
```

---

## 二、线性回归

### 2.1 算法原理

线性回归假设目标变量与特征之间存在线性关系：

$$y = w_1x_1 + w_2x_2 + ... + w_nx_n + b$$

目标：找到最优参数 $w$ 和 $b$，使得预测值与真实值的误差最小。

**损失函数（均方误差 MSE）**：

$$MSE = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$

### 2.2 代码实现

```python
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# ===== 1. 简单线性回归 =====
# 生成简单数据
np.random.seed(42)
X_simple = np.random.randn(100, 1) * 10
y_simple = 3 * X_simple.ravel() + 5 + np.random.randn(100) * 3

# 划分数据
X_train, X_test, y_train, y_test = train_test_split(X_simple, y_simple, test_size=0.2, random_state=42)

# 创建并训练模型
lr = LinearRegression()
lr.fit(X_train, y_train)

# 预测
y_pred = lr.predict(X_test)

# 评估
print("=== 简单线性回归 ===")
print(f"权重 (w): {lr.coef_[0]:.4f}")      # 真实值: 3
print(f"偏置 (b): {lr.intercept_:.4f}")    # 真实值: 5
print(f"均方误差 (MSE): {mean_squared_error(y_test, y_pred):.4f}")
print(f"决定系数 (R²): {r2_score(y_test, y_pred):.4f}")
print(f"平均绝对误差 (MAE): {mean_absolute_error(y_test, y_pred):.4f}")

# 可视化
plt.figure(figsize=(10, 6))
plt.scatter(X_test, y_test, color='blue', alpha=0.5, label='真实值')
plt.plot(X_test, y_pred, color='red', linewidth=2, label='预测线')
plt.xlabel('X')
plt.ylabel('y')
plt.title('简单线性回归')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('linear_regression_simple.png', dpi=100, bbox_inches='tight')
plt.close()

# ===== 2. 多元线性回归 =====
from sklearn.datasets import fetch_california_housing

# 加载加州房价数据集
housing = fetch_california_housing()
X, y = housing.data, housing.target

# 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 训练模型
lr_multi = LinearRegression()
lr_multi.fit(X_train, y_train)

# 预测和评估
y_pred = lr_multi.predict(X_test)

print("\n=== 多元线性回归 (加州房价) ===")
print(f"R² 分数: {r2_score(y_test, y_pred):.4f}")
print(f"MSE: {mean_squared_error(y_test, y_pred):.4f}")

# 特征系数
print("\n特征系数:")
for name, coef in zip(housing.feature_names, lr_multi.coef_):
    print(f"  {name}: {coef:.4f}")

# ===== 3. 正则化回归 =====
# 岭回归 (L2正则化)
ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)
print(f"\n岭回归 R²: {ridge.score(X_test, y_test):.4f}")

# Lasso回归 (L1正则化)
lasso = Lasso(alpha=0.1)
lasso.fit(X_train, y_train)
print(f"Lasso回归 R²: {lasso.score(X_test, y_test):.4f}")
print(f"Lasso非零系数数: {np.sum(lasso.coef_ != 0)}")  # 特征选择效果
```

### 2.3 正则化详解

```python
import numpy as np
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.model_selection import validation_curve
import matplotlib.pyplot as plt

# 正则化的作用：防止过拟合
"""
L2正则化 (Ridge): 损失 = MSE + α * Σw²
- 所有系数变小，但不为0
- 适合特征间有共线性

L1正则化 (Lasso): 损失 = MSE + α * Σ|w|
- 部分系数变为0（特征选择）
- 适合高维稀疏数据

ElasticNet: 结合L1和L2
- 损失 = MSE + α1 * Σ|w| + α2 * Σw²
"""

# 创建模拟数据展示正则化效果
np.random.seed(42)
n_samples, n_features = 100, 50
X = np.random.randn(n_samples, n_features)
# 只有前5个特征有用
coef_true = np.array([5, 3, 2, 1, 0.5] + [0] * 45)
y = X @ coef_true + np.random.randn(n_samples) * 0.5

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 比较不同正则化强度
alphas = [0.001, 0.01, 0.1, 1, 10, 100]
ridge_scores = []
lasso_scores = []

for alpha in alphas:
    ridge = Ridge(alpha=alpha)
    ridge.fit(X_train, y_train)
    ridge_scores.append(ridge.score(X_test, y_test))
    
    lasso = Lasso(alpha=alpha, max_iter=10000)
    lasso.fit(X_train, y_train)
    lasso_scores.append(lasso.score(X_test, y_test))

print("\n=== 正则化强度对比 ===")
print(f"alpha值: {alphas}")
print(f"Ridge R²: {[f'{s:.4f}' for s in ridge_scores]}")
print(f"Lasso R²: {[f'{s:.4f}' for s in lasso_scores]}")

# 可视化正则化路径
alphas_path = np.logspace(-4, 2, 50)
coefs_lasso = []
coefs_ridge = []

for a in alphas_path:
    lasso = Lasso(alpha=a, max_iter=10000)
    lasso.fit(X_train, y_train)
    coefs_lasso.append(lasso.coef_[:5])  # 只看前5个系数
    
    ridge = Ridge(alpha=a)
    ridge.fit(X_train, y_train)
    coefs_ridge.append(ridge.coef_[:5])

coefs_lasso = np.array(coefs_lasso)
coefs_ridge = np.array(coefs_ridge)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for i in range(5):
    axes[0].plot(alphas_path, coefs_lasso[:, i], label=f'特征{i+1}')
    axes[1].plot(alphas_path, coefs_ridge[:, i], label=f'特征{i+1}')

axes[0].set_xscale('log')
axes[0].set_xlabel('Alpha (log scale)')
axes[0].set_ylabel('Coefficient')
axes[0].set_title('Lasso 正则化路径')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].set_xscale('log')
axes[1].set_xlabel('Alpha (log scale)')
axes[1].set_ylabel('Coefficient')
axes[1].set_title('Ridge 正则化路径')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('regularization_path.png', dpi=100, bbox_inches='tight')
plt.close()
```

---

## 三、逻辑回归

### 3.1 算法原理

逻辑回归用于二分类问题，通过 Sigmoid 函数将线性输出映射到 [0, 1] 区间：

$$P(y=1|x) = \frac{1}{1 + e^{-(w^Tx + b)}}$$

**Sigmoid 函数特性**：
- 输出范围 (0, 1)，可解释为概率
- 当 z=0 时，σ(z)=0.5
- 导数为 σ(z)(1-σ(z))，计算方便

### 3.2 代码实现

```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification, load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (accuracy_score, confusion_matrix, 
                             classification_report, roc_auc_score, roc_curve,
                             precision_score, recall_score, f1_score)
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# ===== 1. 二分类示例 =====
# 生成数据
X, y = make_classification(
    n_samples=1000,
    n_features=2,
    n_redundant=0,
    n_informative=2,
    n_clusters_per_class=1,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 训练逻辑回归
lr = LogisticRegression()
lr.fit(X_train, y_train)

# 预测
y_pred = lr.predict(X_test)
y_prob = lr.predict_proba(X_test)[:, 1]  # 正类概率

# 评估
print("=== 逻辑回归评估 ===")
print(f"准确率: {accuracy_score(y_test, y_pred):.4f}")
print(f"精确率: {precision_score(y_test, y_pred):.4f}")
print(f"召回率: {recall_score(y_test, y_pred):.4f}")
print(f"F1分数: {f1_score(y_test, y_pred):.4f}")
print(f"AUC: {roc_auc_score(y_test, y_prob):.4f}")

print("\n混淆矩阵:")
print(confusion_matrix(y_test, y_pred))

print("\n分类报告:")
print(classification_report(y_test, y_pred))

# ===== 2. 决策边界可视化 =====
def plot_decision_boundary(X, y, model, title):
    h = 0.02
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    
    Z = model.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
    Z = Z.reshape(xx.shape)
    
    plt.figure(figsize=(10, 8))
    plt.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.RdBu)
    plt.contour(xx, yy, Z, [0.5], linewidths=2, colors='black')
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.RdBu, edgecolors='black')
    plt.xlabel('特征1')
    plt.ylabel('特征2')
    plt.title(title)
    plt.colorbar(label='预测概率')
    plt.savefig('logistic_decision_boundary.png', dpi=100, bbox_inches='tight')
    plt.close()

plot_decision_boundary(X, y, lr, '逻辑回归决策边界')

# ===== 3. ROC曲线 =====
fpr, tpr, thresholds = roc_curve(y_test, y_prob)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC曲线 (AUC = {roc_auc_score(y_test, y_prob):.4f})')
plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--', label='随机分类')
plt.xlabel('假正率 (FPR)')
plt.ylabel('真正率 (TPR)')
plt.title('ROC曲线')
plt.legend(loc='lower right')
plt.grid(True, alpha=0.3)
plt.savefig('roc_curve.png', dpi=100, bbox_inches='tight')
plt.close()

# ===== 4. 多分类逻辑回归 =====
from sklearn.datasets import load_iris

iris = load_iris()
X, y = iris.data, iris.target

# 标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# 多分类逻辑回归 (OvR策略)
lr_multi = LogisticRegression(multi_class='ovr', max_iter=1000)
lr_multi.fit(X_train, y_train)

y_pred = lr_multi.predict(X_test)
print("\n=== 多分类逻辑回归 (鸢尾花) ===")
print(f"准确率: {accuracy_score(y_test, y_pred):.4f}")
print("\n分类报告:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# ===== 5. 正则化与交叉验证 =====
from sklearn.linear_model import LogisticRegressionCV

# 使用交叉验证自动选择最优正则化参数
lr_cv = LogisticRegressionCV(
    Cs=10,              # 候选C值数量
    cv=5,               # 5折交叉验证
    penalty='l2',       # L2正则化
    solver='lbfgs',
    max_iter=1000,
    random_state=42
)
lr_cv.fit(X_train, y_train)

print(f"\n最优C值: {lr_cv.C_[0]:.4f}")
print(f"交叉验证准确率: {lr_cv.score(X_test, y_test):.4f}")
```

### 3.3 概率校准

```python
from sklearn.calibration import calibration_curve, CalibratedClassifierCV

# 概率校准：确保预测概率反映真实概率
"""
为什么需要校准？
- 模型输出的"概率"可能不准确
- 如模型预测概率0.8，实际正例比例应接近0.8
"""

# 生成不平衡数据
X, y = make_classification(
    n_samples=5000,
    n_features=20,
    n_informative=10,
    n_redundant=5,
    weights=[0.9, 0.1],  # 90%负例
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 原始逻辑回归
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)

# 校准后的逻辑回归
lr_calibrated = CalibratedClassifierCV(lr, cv=5, method='sigmoid')
lr_calibrated.fit(X_train, y_train)

# 绘制校准曲线
plt.figure(figsize=(10, 6))

for model, name in [(lr, '原始'), (lr_calibrated, '校准后')]:
    if name == '原始':
        prob_pos = model.predict_proba(X_test)[:, 1]
    else:
        prob_pos = model.predict_proba(X_test)[:, 1]
    
    fraction_of_positives, mean_predicted_value = calibration_curve(
        y_test, prob_pos, n_bins=10
    )
    
    plt.plot(mean_predicted_value, fraction_of_positives, 's-', label=name)

plt.plot([0, 1], [0, 1], 'k--', label='完美校准')
plt.xlabel('平均预测概率')
plt.ylabel('正例比例')
plt.title('概率校准曲线')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('calibration_curve.png', dpi=100, bbox_inches='tight')
plt.close()
```

---

## 四、决策树

### 4.1 算法原理

决策树通过一系列 if-then 规则对数据进行划分，形成树状结构。

**核心概念**：
- **节点分裂**：选择最优特征和分裂点
- **信息增益**：分裂前后的熵减少量
- **基尼系数**：衡量节点纯度

**分裂标准**：
- 信息增益 (ID3): $IG = H(D) - H(D|A)$
- 信息增益率 (C4.5): 对特征取值多的惩罚
- 基尼系数 (CART): $Gini(p) = 1 - \sum p_k^2$

### 4.2 代码实现

```python
import numpy as np
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree
from sklearn.datasets import load_iris, load_wine
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt

# ===== 1. 决策树分类 =====
iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 训练决策树
dt = DecisionTreeClassifier(
    criterion='gini',       # 分裂标准: 'gini' 或 'entropy'
    max_depth=3,           # 最大深度
    min_samples_split=5,   # 分裂所需最小样本数
    min_samples_leaf=2,    # 叶节点最小样本数
    random_state=42
)
dt.fit(X_train, y_train)

# 预测
y_pred = dt.predict(X_test)
print("=== 决策树分类 (鸢尾花) ===")
print(f"准确率: {accuracy_score(y_test, y_pred):.4f}")

# 特征重要性
print("\n特征重要性:")
for name, importance in zip(iris.feature_names, dt.feature_importances_):
    print(f"  {name}: {importance:.4f}")

# 可视化决策树
plt.figure(figsize=(15, 10))
plot_tree(
    dt,
    feature_names=iris.feature_names,
    class_names=iris.target_names,
    filled=True,
    rounded=True,
    fontsize=10
)
plt.title('决策树可视化')
plt.savefig('decision_tree_iris.png', dpi=150, bbox_inches='tight')
plt.close()

# ===== 2. 剪枝与调参 =====
# 预剪枝 vs 后剪枝

# 预剪枝：限制树的生长
dt_prepruned = DecisionTreeClassifier(
    max_depth=5,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42
)

# 后剪枝：基于成本复杂度剪枝
dt_pruned = DecisionTreeClassifier(random_state=42)
path = dt_pruned.cost_complexity_pruning_path(X_train, y_train)
ccp_alphas = path.ccp_alphas

# 找最优alpha
clfs = []
for ccp_alpha in ccp_alphas:
    clf = DecisionTreeClassifier(random_state=42, ccp_alpha=ccp_alpha)
    clf.fit(X_train, y_train)
    clfs.append(clf)

# 绘制alpha与准确率的关系
train_scores = [clf.score(X_train, y_train) for clf in clfs]
test_scores = [clf.score(X_test, y_test) for clf in clfs]

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlabel("alpha")
ax.set_ylabel("accuracy")
ax.set_title("Accuracy vs alpha for training and testing sets")
ax.plot(ccp_alphas, train_scores, marker='o', label="train", drawstyle="steps-post")
ax.plot(ccp_alphas, test_scores, marker='o', label="test", drawstyle="steps-post")
ax.legend()
ax.grid(True, alpha=0.3)
plt.savefig('pruning_alpha.png', dpi=100, bbox_inches='tight')
plt.close()

# ===== 3. 决策树回归 =====
from sklearn.metrics import mean_squared_error, r2_score

# 生成回归数据
np.random.seed(42)
X = np.sort(5 * np.random.rand(200, 1), axis=0)
y = np.sin(X).ravel() + np.random.randn(200) * 0.1

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 不同max_depth的对比
depths = [1, 3, 5, 10]
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

for ax, depth in zip(axes.ravel(), depths):
    dt_reg = DecisionTreeRegressor(max_depth=depth, random_state=42)
    dt_reg.fit(X_train, y_train)
    
    # 预测
    X_test_sorted = np.sort(X_test, axis=0)
    y_pred = dt_reg.predict(X_test_sorted)
    
    ax.scatter(X_train, y_train, s=20, edgecolor="black", c="darkorange", label="训练数据", alpha=0.5)
    ax.plot(X_test_sorted, y_pred, color="cornflowerblue", label=f"预测 (depth={depth})", linewidth=2)
    ax.set_xlabel("X")
    ax.set_ylabel("y")
    ax.set_title(f"深度={depth}, R²={dt_reg.score(X_test, y_test):.3f}")
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('decision_tree_regression.png', dpi=100, bbox_inches='tight')
plt.close()

# ===== 4. 决策边界可视化 =====
from sklearn.datasets import make_moons

# 生成非线性数据
X, y = make_moons(n_samples=500, noise=0.25, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

def plot_tree_decision_boundary(X, y, model, title, filename):
    h = 0.02
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    plt.figure(figsize=(10, 8))
    plt.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.RdBu)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.RdBu, edgecolors='black')
    plt.xlabel('特征1')
    plt.ylabel('特征2')
    plt.title(title)
    plt.savefig(filename, dpi=100, bbox_inches='tight')
    plt.close()

# 无限制的决策树（过拟合）
dt_unrestricted = DecisionTreeClassifier(random_state=42)
dt_unrestricted.fit(X_train, y_train)

# 限制深度的决策树
dt_limited = DecisionTreeClassifier(max_depth=4, random_state=42)
dt_limited.fit(X_train, y_train)

plot_tree_decision_boundary(X, y, dt_unrestricted, 
                           f'无限制决策树 (depth={dt_unrestricted.get_depth()})', 
                           'dt_unrestricted.png')
plot_tree_decision_boundary(X, y, dt_limited, 
                           f'限制深度决策树 (depth=4)', 
                           'dt_limited.png')

print(f"\n无限制树深度: {dt_unrestricted.get_depth()}")
print(f"无限制树叶节点数: {dt_unrestricted.get_n_leaves()}")
print(f"无限制树测试准确率: {dt_unrestricted.score(X_test, y_test):.4f}")
print(f"限制深度树测试准确率: {dt_limited.score(X_test, y_test):.4f}")
```

---

## 五、模型评估

### 5.1 回归评估指标

```python
from sklearn.metrics import (
    mean_squared_error,      # 均方误差
    mean_absolute_error,     # 平均绝对误差
    r2_score,                # 决定系数
    mean_absolute_percentage_error  # 平均绝对百分比误差
)

def regression_metrics(y_true, y_pred):
    """计算所有回归指标"""
    metrics = {
        'MSE': mean_squared_error(y_true, y_pred),
        'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
        'MAE': mean_absolute_error(y_true, y_pred),
        'R²': r2_score(y_true, y_pred),
        'MAPE': mean_absolute_percentage_error(y_true, y_pred)
    }
    return metrics

# 示例
np.random.seed(42)
y_true = np.random.randn(100)
y_pred = y_true + np.random.randn(100) * 0.5

metrics = regression_metrics(y_true, y_pred)
print("=== 回归评估指标 ===")
for name, value in metrics.items():
    print(f"{name}: {value:.4f}")
```

### 5.2 分类评估指标

```python
from sklearn.metrics import (
    accuracy_score,          # 准确率
    precision_score,         # 精确率
    recall_score,            # 召回率
    f1_score,                # F1分数
    confusion_matrix,        # 混淆矩阵
    classification_report,   # 分类报告
    roc_auc_score,           # AUC分数
    roc_curve,               # ROC曲线
    precision_recall_curve,  # PR曲线
    log_loss                 # 对数损失
)

def classification_metrics(y_true, y_pred, y_prob=None):
    """计算所有分类指标"""
    metrics = {
        'Accuracy': accuracy_score(y_true, y_pred),
        'Precision': precision_score(y_true, y_pred, average='weighted'),
        'Recall': recall_score(y_true, y_pred, average='weighted'),
        'F1': f1_score(y_true, y_pred, average='weighted'),
    }
    if y_prob is not None:
        metrics['AUC'] = roc_auc_score(y_true, y_prob, multi_class='ovr', average='weighted')
        metrics['LogLoss'] = log_loss(y_true, y_prob)
    return metrics

# 示例
from sklearn.datasets import load_wine

wine = load_wine()
X, y = wine.data, wine.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)

y_pred = dt.predict(X_test)
y_prob = dt.predict_proba(X_test)

metrics = classification_metrics(y_test, y_pred, y_prob)
print("\n=== 分类评估指标 ===")
for name, value in metrics.items():
    print(f"{name}: {value:.4f}")

# 混淆矩阵可视化
import seaborn as sns

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=wine.target_names,
            yticklabels=wine.target_names)
plt.xlabel('预测标签')
plt.ylabel('真实标签')
plt.title('混淆矩阵')
plt.savefig('confusion_matrix.png', dpi=100, bbox_inches='tight')
plt.close()
```

### 5.3 交叉验证

```python
from sklearn.model_selection import (
    cross_val_score,         # 交叉验证得分
    cross_validate,          # 多指标交叉验证
    KFold,                   # K折交叉验证
    StratifiedKFold,         # 分层K折
    LeaveOneOut,             # 留一法
    GridSearchCV             # 网格搜索
)

# K折交叉验证
X, y = load_iris(return_X_y=True)
dt = DecisionTreeClassifier(random_state=42)

# 简单交叉验证
scores = cross_val_score(dt, X, y, cv=5)
print("\n=== 5折交叉验证 ===")
print(f"各折得分: {scores}")
print(f"平均得分: {scores.mean():.4f} (+/- {scores.std():.4f})")

# 多指标交叉验证
scoring = ['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted']
results = cross_validate(dt, X, y, cv=5, scoring=scoring)
print("\n=== 多指标交叉验证 ===")
for metric in scoring:
    scores = results[f'test_{metric}']
    print(f"{metric}: {scores.mean():.4f} (+/- {scores.std():.4f})")

# 分层K折（保持类别比例）
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores_stratified = cross_val_score(dt, X, y, cv=skf)
print(f"\n分层K折平均得分: {scores_stratified.mean():.4f}")
```

---

## 参考资源

> - [Scikit-learn官方文档 - 监督学习](https://scikit-learn.org/stable/supervised_learning.html) - 完整API参考
> - [斯坦福CS229机器学习](https://cs229.stanford.edu/) - Andrew Ng经典课程
> - [统计学习方法 - 李航](https://book.douban.com/subject/33437381/) - 中文经典教材
> - [Hands-On Machine Learning](https://github.com/ageron/handson-ml3) - 实战教程
> - [机器学习 - 周志华](https://book.douban.com/subject/26708119/) - 西瓜书
> - [Coursera Machine Learning](https://www.coursera.org/learn/machine-learning) - 吴恩达课程
> - [李宏毅机器学习](https://www.youtube.com/c/HungyiLeeNTU) - 中文视频课程
> - [Scikit-learn模型选择指南](https://scikit-learn.org/stable/tutorial/machine_learning_map/index.html) - 模型选择流程图

---

**下一篇**：[集成学习方法 - 随机森林与GBDT]({{ site.baseurl }}{% post_url /ailearn/02-machine-learning/2026-04-13-02-ensemble-learning %})

**返回**：[机器学习基础]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-02-machine-learning %})

*最后更新: 2026年4月13日*
