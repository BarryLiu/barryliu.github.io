---
layout: post
title: "集成学习方法 - 随机森林、GBDT与XGBoost"
date: 2026-04-13
categories: ailearn
tags: [AI, 机器学习, 集成学习, XGBoost]
keywords: 随机森林, GBDT, XGBoost, LightGBM, 集成学习
description: 深入学习集成学习核心算法，掌握随机森林、GBDT、XGBoost、LightGBM的原理与实践
---

* content
{:toc}

> **前置知识**：需要先掌握 [监督学习算法]({{ site.baseurl }}{% post_url /ailearn/02-machine-learning/2026-04-13-01-supervised-learning %})
>
> **本文重点**：理解集成学习原理，掌握主流集成算法的使用与调优

---

## 一、集成学习概述

### 1.1 为什么需要集成学习

集成学习通过**组合多个基学习器**来获得比单一学习器更好的性能。

```
核心思想：
- 弱学习器 → 组合 → 强学习器
- 三个臭皮匠，顶个诸葛亮

集成学习
├── Bagging (并行集成)
│   └── 代表：随机森林
├── Boosting (串行集成)
│   ├── AdaBoost
│   ├── GBDT
│   ├── XGBoost
│   └── LightGBM
└── Stacking (堆叠集成)
    └── 多模型堆叠
```

### 1.2 偏差与方差

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier

"""
偏差-方差权衡 (Bias-Variance Tradeoff)

偏差 (Bias): 预测值与真实值的差异
- 高偏差 = 欠拟合
- 低偏差 = 模型足够复杂

方差 (Variance): 模型对数据变化的敏感度
- 高方差 = 过拟合
- 低方差 = 模型稳定性好

集成学习的作用：
- Bagging: 降低方差（适合高方差模型）
- Boosting: 降低偏差（适合高偏差模型）
"""

# 演示偏差-方差
np.random.seed(42)

# 生成数据
X, y = make_classification(n_samples=1000, n_features=20, n_informative=15, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 不同深度决策树的对比（偏差-方差演示）
depths = range(1, 20)
train_scores = []
test_scores = []

for depth in depths:
    dt = DecisionTreeClassifier(max_depth=depth, random_state=42)
    dt.fit(X_train, y_train)
    train_scores.append(dt.score(X_train, y_train))
    test_scores.append(dt.score(X_test, y_test))

plt.figure(figsize=(10, 6))
plt.plot(depths, train_scores, 'o-', label='训练集准确率')
plt.plot(depths, test_scores, 's-', label='测试集准确率')
plt.xlabel('决策树深度')
plt.ylabel('准确率')
plt.title('偏差-方差权衡演示')
plt.legend()
plt.grid(True, alpha=0.3)
plt.axvline(x=5, color='red', linestyle='--', alpha=0.5, label='最优深度')
plt.savefig('bias_variance_tradeoff.png', dpi=100, bbox_inches='tight')
plt.close()
```

---

## 二、Bagging与随机森林

### 2.1 Bagging原理

Bagging (Bootstrap Aggregating) 的核心思想：
1. **Bootstrap采样**：从训练集中有放回地抽取样本
2. **并行训练**：独立训练多个基学习器
3. **聚合预测**：分类用投票，回归用平均

### 2.2 随机森林实现

```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.datasets import make_classification, fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error
import matplotlib.pyplot as plt

# ===== 1. 随机森林分类 =====
X, y = make_classification(
    n_samples=2000,
    n_features=20,
    n_informative=15,
    n_redundant=3,
    n_clusters_per_class=2,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 训练随机森林
rf = RandomForestClassifier(
    n_estimators=100,      # 树的数量
    max_depth=10,          # 最大深度
    min_samples_split=5,   # 分裂最小样本数
    min_samples_leaf=2,    # 叶节点最小样本数
    max_features='sqrt',   # 每棵树使用的特征数
    random_state=42,
    n_jobs=-1,             # 并行计算
    oob_score=True         # 袋外评分
)
rf.fit(X_train, y_train)

# 预测
y_pred = rf.predict(X_test)
y_prob = rf.predict_proba(X_test)

print("=== 随机森林分类 ===")
print(f"测试集准确率: {accuracy_score(y_test, y_pred):.4f}")
print(f"袋外(OOB)得分: {rf.oob_score_:.4f}")

# 特征重要性
importances = rf.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(10, 6))
plt.title('特征重要性 (随机森林)')
plt.bar(range(X.shape[1]), importances[indices], align='center')
plt.xticks(range(X.shape[1]), [f'特征{i}' for i in indices], rotation=45)
plt.xlabel('特征')
plt.ylabel('重要性')
plt.tight_layout()
plt.savefig('rf_feature_importance.png', dpi=100, bbox_inches='tight')
plt.close()

# ===== 2. 随机森林回归 =====
housing = fetch_california_housing()
X, y = housing.data, housing.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_reg = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)
rf_reg.fit(X_train, y_train)

y_pred = rf_reg.predict(X_test)

print("\n=== 随机森林回归 (加州房价) ===")
print(f"R²分数: {rf_reg.score(X_test, y_test):.4f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")

# ===== 3. 超参数调优 =====
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10],
    'max_features': ['sqrt', 'log2', None]
}

# 使用较小的参数网格进行演示
param_grid_simple = {
    'n_estimators': [50, 100],
    'max_depth': [5, 10, 15],
}

rf_grid = GridSearchCV(
    RandomForestClassifier(random_state=42, n_jobs=-1),
    param_grid_simple,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    verbose=1
)
rf_grid.fit(X_train, y_train)

print(f"\n最优参数: {rf_grid.best_params_}")
print(f"最优得分: {rf_grid.best_score_:.4f}")
```

### 2.3 ExtraTrees (极端随机树)

```python
from sklearn.ensemble import ExtraTreesClassifier

# 极端随机树：随机选择分裂点，速度更快
et = ExtraTreesClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)
et.fit(X_train, y_train)

print(f"\n极端随机树准确率: {et.score(X_test, y_test):.4f}")
```

---

## 三、Boosting系列

### 3.1 AdaBoost

```python
from sklearn.ensemble import AdaBoostClassifier

"""
AdaBoost原理：
1. 初始化样本权重（相等）
2. 训练弱学习器
3. 计算错误率，调整样本权重（错分样本权重增加）
4. 组合所有弱学习器（加权投票）
"""

ada = AdaBoostClassifier(
    n_estimators=50,      # 弱学习器数量
    learning_rate=1.0,    # 学习率
    random_state=42
)
ada.fit(X_train, y_train)

y_pred = ada.predict(X_test)

print("=== AdaBoost ===")
print(f"准确率: {accuracy_score(y_test, y_pred):.4f}")

# 查看各学习器权重
plt.figure(figsize=(10, 6))
plt.bar(range(len(ada.estimator_weights_)), ada.estimator_weights_)
plt.xlabel('弱学习器索引')
plt.ylabel('权重')
plt.title('AdaBoost各学习器权重')
plt.savefig('adaboost_weights.png', dpi=100, bbox_inches='tight')
plt.close()
```

### 3.2 GBDT (梯度提升决策树)

```python
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor

"""
GBDT原理：
1. 初始化模型为常数值（如目标均值）
2. 计算残差（负梯度）
3. 用决策树拟合残差
4. 更新模型：F = F + learning_rate * tree
5. 重复2-4直到收敛
"""

# GBDT分类
gbdt = GradientBoostingClassifier(
    n_estimators=100,       # 树的数量
    learning_rate=0.1,      # 学习率
    max_depth=3,            # 每棵树的最大深度（通常较小）
    min_samples_split=5,
    subsample=0.8,          # 子采样比例
    random_state=42
)
gbdt.fit(X_train, y_train)

y_pred = gbdt.predict(X_test)

print("=== GBDT分类 ===")
print(f"准确率: {accuracy_score(y_test, y_pred):.4f}")

# 训练过程可视化
train_scores = list(gbdt.staged_score(X_train, y_train))
test_scores = list(gbdt.staged_score(X_test, y_test))

plt.figure(figsize=(10, 6))
plt.plot(train_scores, label='训练集')
plt.plot(test_scores, label='测试集')
plt.xlabel('迭代次数')
plt.ylabel('准确率')
plt.title('GBDT训练过程')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('gbdt_training_curve.png', dpi=100, bbox_inches='tight')
plt.close()

# GBDT回归
gbdt_reg = GradientBoostingRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)
gbdt_reg.fit(X_train, y_train)

print(f"\nGBDT回归 R²: {gbdt_reg.score(X_test, y_test):.4f}")
```

### 3.3 XGBoost

```python
# 需要安装: pip install xgboost
try:
    import xgboost as xgb
    from xgboost import XGBClassifier, XGBRegressor
    
    """
    XGBoost优化：
    1. 正则化：L1 + L2 正则项，控制模型复杂度
    2. 二阶梯度：使用损失函数的二阶导数信息
    3. 列采样：类似随机森林的特征采样
    4. 并行计算：特征粒度的并行
    5. 缺失值处理：自动学习缺失值方向
    """
    
    # XGBoost分类
    xgb_clf = XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.1,       # L1正则化
        reg_lambda=1.0,      # L2正则化
        random_state=42,
        n_jobs=-1,
        eval_metric='logloss',
        use_label_encoder=False
    )
    
    xgb_clf.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        early_stopping_rounds=10,
        verbose=False
    )
    
    y_pred = xgb_clf.predict(X_test)
    
    print("=== XGBoost分类 ===")
    print(f"准确率: {accuracy_score(y_test, y_pred):.4f}")
    print(f"最优迭代次数: {xgb_clf.best_iteration}")
    
    # 特征重要性
    plt.figure(figsize=(10, 6))
    xgb.plot_importance(xgb_clf, max_num_features=10)
    plt.title('XGBoost特征重要性')
    plt.tight_layout()
    plt.savefig('xgboost_importance.png', dpi=100, bbox_inches='tight')
    plt.close()
    
except ImportError:
    print("XGBoost未安装，请运行: pip install xgboost")
```

### 3.4 LightGBM

```python
# 需要安装: pip install lightgbm
try:
    import lightgbm as lgb
    from lightgbm import LGBMClassifier, LGBMRegressor
    
    """
    LightGBM优化：
    1. 直方图算法：将连续值离散化，加速训练
    2. GOSS：基于梯度的单边采样
    3. EFB：互斥特征捆绑
    4. 叶子生长策略：Leaf-wise，更深但更快
    """
    
    lgb_clf = LGBMClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        num_leaves=31,        # 叶子节点数
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=42,
        n_jobs=-1,
        verbose=-1
    )
    
    lgb_clf.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        callbacks=[lgb.early_stopping(10), lgb.log_evaluation(0)]
    )
    
    y_pred = lgb_clf.predict(X_test)
    
    print("=== LightGBM分类 ===")
    print(f"准确率: {accuracy_score(y_test, y_pred):.4f}")
    
except ImportError:
    print("LightGBM未安装，请运行: pip install lightgbm")
```

### 3.5 CatBoost

```python
# 需要安装: pip install catboost
try:
    from catboost import CatBoostClassifier, Pool
    
    """
    CatBoost优化：
    1. 类别特征处理：自动处理类别变量
    2. Ordered Boosting：减少过拟合
    3. 对称树：降低模型复杂度
    """
    
    cat_clf = CatBoostClassifier(
        iterations=100,
        depth=6,
        learning_rate=0.1,
        l2_leaf_reg=3.0,
        random_state=42,
        verbose=False
    )
    
    cat_clf.fit(
        X_train, y_train,
        eval_set=(X_test, y_test),
        early_stopping_rounds=10,
        verbose=False
    )
    
    y_pred = cat_clf.predict(X_test)
    
    print("=== CatBoost分类 ===")
    print(f"准确率: {accuracy_score(y_test, y_pred):.4f}")
    
except ImportError:
    print("CatBoost未安装，请运行: pip install catboost")
```

---

## 四、模型对比与选择

### 4.1 性能对比

```python
import numpy as np
import time
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score

# 创建数据
X, y = make_classification(n_samples=5000, n_features=20, n_informative=15, random_state=42)

models = {
    'Decision Tree': DecisionTreeClassifier(max_depth=5, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1),
    'GBDT': GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42),
}

results = {}
for name, model in models.items():
    start_time = time.time()
    scores = cross_val_score(model, X, y, cv=5, scoring='accuracy', n_jobs=-1)
    train_time = time.time() - start_time
    
    results[name] = {
        'mean_score': scores.mean(),
        'std_score': scores.std(),
        'time': train_time
    }
    print(f"{name}: {scores.mean():.4f} (+/- {scores.std():.4f}), 时间: {train_time:.2f}s")

# 可视化对比
names = list(results.keys())
scores = [results[n]['mean_score'] for n in names]
stds = [results[n]['std_score'] for n in names]
times = [results[n]['time'] for n in names]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 准确率对比
axes[0].barh(names, scores, xerr=stds, capsize=5)
axes[0].set_xlabel('准确率')
axes[0].set_title('模型准确率对比')

# 训练时间对比
axes[1].barh(names, times)
axes[1].set_xlabel('训练时间(秒)')
axes[1].set_title('模型训练时间对比')

plt.tight_layout()
plt.savefig('ensemble_comparison.png', dpi=100, bbox_inches='tight')
plt.close()
```

### 4.2 选择建议

```python
"""
模型选择建议：

1. 决策树
   - 优点：可解释性强、无需特征缩放
   - 缺点：容易过拟合、不稳定
   - 适用：需要可解释性、小数据集

2. 随机森林
   - 优点：抗过拟合、并行计算、特征重要性
   - 缺点：模型较大、预测稍慢
   - 适用：大多数场景、高维数据

3. GBDT
   - 优点：高精度、处理非线性
   - 缺点：串行训练、需要调参
   - 适用：精度要求高、表格数据

4. XGBoost
   - 优点：更快、更准、正则化
   - 缺点：参数较多
   - 适用：竞赛、工业应用

5. LightGBM
   - 优点：极快、大数据
   - 缺点：可能过拟合小数据
   - 适用：大数据、实时场景

6. CatBoost
   - 优点：类别特征处理、GPU支持
   - 缺点：训练稍慢
   - 适用：类别特征多、GPU环境
"""
```

---

## 五、Stacking集成

```python
from sklearn.ensemble import StackingClassifier, StackingRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris

"""
Stacking原理：
1. 训练多个基学习器
2. 用基学习器的预测结果作为新特征
3. 训练元学习器在新生成的特征上

Level 0: 基学习器 (多种不同类型)
Level 1: 元学习器 (通常用简单模型)
"""

# 加载数据
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 定义基学习器
estimators = [
    ('rf', RandomForestClassifier(n_estimators=50, random_state=42)),
    ('gbdt', GradientBoostingClassifier(n_estimators=50, random_state=42)),
    ('svm', SVC(probability=True, random_state=42)),
    ('knn', KNeighborsClassifier())
]

# 定义元学习器
final_estimator = LogisticRegression(max_iter=1000)

# 创建Stacking模型
stacking = StackingClassifier(
    estimators=estimators,
    final_estimator=final_estimator,
    cv=5,
    stack_method='predict_proba',  # 使用概率作为特征
    n_jobs=-1
)

stacking.fit(X_train, y_train)
y_pred = stacking.predict(X_test)

print("=== Stacking集成 ===")
print(f"准确率: {accuracy_score(y_test, y_pred):.4f}")

# 对比单个模型
print("\n各基学习器准确率:")
for name, model in estimators:
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(f"  {name}: {score:.4f}")
```

---

## 参考资源

> - [XGBoost官方文档](https://xgboost.readthedocs.io/) - XGBoost完整参考
> - [LightGBM官方文档](https://lightgbm.readthedocs.io/) - LightGBM使用指南
> - [CatBoost官方文档](https://catboost.ai/docs/) - CatBoost教程
> - [Scikit-learn Ensemble Methods](https://scikit-learn.org/stable/modules/ensemble.html) - 官方集成学习指南
> - [Kaggle Ensembling Guide](https://www.kaggle.com/code/arthurtok/introduction-to-ensembling-stacking-in-python) - Kaggle集成教程
> - [GBDT算法原理](https://explained.ai/gradient-boosting/) - 梯度提升可视化解释
> - [XGBoost论文](https://arxiv.org/abs/1603.02754) - XGBoost算法原理
> - [LightGBM论文](https://papers.nips.cc/paper/6907-lightgbm-a-highly-efficient-gradient-boosting-decision-tree) - LightGBM算法原理

---

**上一篇**：[监督学习算法详解]({{ site.baseurl }}{% post_url /ailearn/02-machine-learning/2026-04-13-01-supervised-learning %})

**下一篇**：[无监督学习 - 聚类与降维]({{ site.baseurl }}{% post_url /ailearn/02-machine-learning/2026-04-13-03-unsupervised-learning %})

**返回**：[机器学习基础]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-02-machine-learning %})

*最后更新: 2026年4月13日*
