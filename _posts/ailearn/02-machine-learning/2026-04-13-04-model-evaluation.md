---
layout: post
title: "模型评估与超参数调优"
date: 2026-04-13
categories: ailearn
tags: [AI, 机器学习, 模型评估, 超参数调优]
keywords: 交叉验证, GridSearch, 随机搜索, 贝叶斯优化, 特征工程
description: 深入学习模型评估方法与超参数调优技术，掌握机器学习工程实践技能
---

* content
{:toc}

> **前置知识**：需要先掌握 [监督学习]({{ site.baseurl }}{% post_url /ailearn/02-machine-learning/2026-04-13-01-supervised-learning %}) 和 [集成学习]({{ site.baseurl }}{% post_url /ailearn/02-machine-learning/2026-04-13-02-ensemble-learning %})
>
> **本文重点**：掌握模型评估、超参数调优、特征工程等工程实践技能

---

## 一、模型评估方法

### 1.1 交叉验证详解

```python
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    cross_validate,
    KFold,
    StratifiedKFold,
    RepeatedKFold,
    LeaveOneOut,
    ShuffleSplit
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# 加载数据
data = load_breast_cancer()
X, y = data.data, data.target

# 创建管道
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
])

# ===== 1. K折交叉验证 =====
print("=== K折交叉验证 ===")
kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores_kf = cross_val_score(pipe, X, y, cv=kf, scoring='accuracy')
print(f"各折得分: {scores_kf}")
print(f"平均得分: {scores_kf.mean():.4f} (+/- {scores_kf.std()*2:.4f})")

# ===== 2. 分层K折交叉验证 =====
print("\n=== 分层K折交叉验证 ===")
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores_skf = cross_val_score(pipe, X, y, cv=skf, scoring='accuracy')
print(f"各折得分: {scores_skf}")
print(f"平均得分: {scores_skf.mean():.4f} (+/- {scores_skf.std()*2:.4f})")

# ===== 3. 多指标交叉验证 =====
print("\n=== 多指标交叉验证 ===")
scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
results = cross_validate(pipe, X, y, cv=skf, scoring=scoring, return_train_score=True)

for metric in scoring:
    test_scores = results[f'test_{metric}']
    train_scores = results[f'train_{metric}']
    print(f"{metric}:")
    print(f"  训练集: {train_scores.mean():.4f} (+/- {train_scores.std()*2:.4f})")
    print(f"  测试集: {test_scores.mean():.4f} (+/- {test_scores.std()*2:.4f})")

# ===== 4. 重复K折 =====
print("\n=== 重复K折交叉验证 ===")
rkf = RepeatedKFold(n_splits=5, n_repeats=3, random_state=42)
scores_rkf = cross_val_score(pipe, X, y, cv=rkf, scoring='accuracy')
print(f"平均得分: {scores_rkf.mean():.4f} (+/- {scores_rkf.std()*2:.4f})")

# ===== 5. 留一法 =====
# 适用于小数据集
print("\n=== 留一法交叉验证 ===")
loo = LeaveOneOut()
# 只使用部分数据演示（太慢）
scores_loo = cross_val_score(pipe, X[:100], y[:100], cv=loo, scoring='accuracy')
print(f"平均得分: {scores_loo.mean():.4f}")

# ===== 6. Shuffle Split =====
print("\n=== Shuffle Split ===")
ss = ShuffleSplit(n_splits=5, test_size=0.3, random_state=42)
scores_ss = cross_val_score(pipe, X, y, cv=ss, scoring='accuracy')
print(f"平均得分: {scores_ss.mean():.4f}")
```

### 1.2 学习曲线

```python
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve

# 学习曲线：评估模型是否欠拟合或过拟合
train_sizes, train_scores, test_scores = learning_curve(
    pipe, X, y,
    cv=5,
    n_jobs=-1,
    train_sizes=np.linspace(0.1, 1.0, 10),
    scoring='accuracy',
    random_state=42
)

train_mean = train_scores.mean(axis=1)
train_std = train_scores.std(axis=1)
test_mean = test_scores.mean(axis=1)
test_std = test_scores.std(axis=1)

plt.figure(figsize=(10, 6))
plt.plot(train_sizes, train_mean, 'o-', color='r', label='训练集')
plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color='r')
plt.plot(train_sizes, test_mean, 'o-', color='g', label='交叉验证')
plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, alpha=0.1, color='g')
plt.xlabel('训练样本数')
plt.ylabel('准确率')
plt.title('学习曲线')
plt.legend(loc='lower right')
plt.grid(True, alpha=0.3)
plt.savefig('learning_curve.png', dpi=100, bbox_inches='tight')
plt.close()

print("学习曲线分析:")
if train_mean[-1] - test_mean[-1] > 0.1:
    print("  模型可能过拟合，考虑增加训练数据或正则化")
elif train_mean[-1] < 0.9 and test_mean[-1] < 0.9:
    print("  模型可能欠拟合，考虑增加模型复杂度")
else:
    print("  模型拟合良好")
```

### 1.3 验证曲线

```python
from sklearn.model_selection import validation_curve

# 验证曲线：评估超参数影响
param_range = np.arange(10, 210, 20)

train_scores, test_scores = validation_curve(
    pipe, X, y,
    param_name='clf__n_estimators',
    param_range=param_range,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)

train_mean = train_scores.mean(axis=1)
train_std = train_scores.std(axis=1)
test_mean = test_scores.mean(axis=1)
test_std = test_scores.std(axis=1)

plt.figure(figsize=(10, 6))
plt.plot(param_range, train_mean, 'o-', color='r', label='训练集')
plt.fill_between(param_range, train_mean - train_std, train_mean + train_std, alpha=0.1, color='r')
plt.plot(param_range, test_mean, 'o-', color='g', label='交叉验证')
plt.fill_between(param_range, test_mean - test_std, test_mean + test_std, alpha=0.1, color='g')
plt.xlabel('n_estimators')
plt.ylabel('准确率')
plt.title('验证曲线 (n_estimators)')
plt.legend(loc='lower right')
plt.grid(True, alpha=0.3)
plt.savefig('validation_curve.png', dpi=100, bbox_inches='tight')
plt.close()
```

---

## 二、超参数调优

### 2.1 网格搜索 GridSearchCV

```python
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

# 定义参数网格
param_grid = {
    'clf__n_estimators': [50, 100, 200],
    'clf__max_depth': [5, 10, 15, None],
    'clf__min_samples_split': [2, 5, 10],
    'clf__min_samples_leaf': [1, 2, 4]
}

# 网格搜索
grid_search = GridSearchCV(
    pipe,
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    verbose=1,
    return_train_score=True
)

print("=== 网格搜索 ===")
grid_search.fit(X, y)

print(f"最优参数: {grid_search.best_params_}")
print(f"最优得分: {grid_search.best_score_:.4f}")
print(f"最优模型: {grid_search.best_estimator_}")

# 查看结果
results = pd.DataFrame(grid_search.cv_results_)
print("\nTop 5 参数组合:")
print(results[['params', 'mean_test_score', 'std_test_score', 'rank_test_score']]
      .sort_values('rank_test_score').head())
```

### 2.2 随机搜索 RandomizedSearchCV

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

# 定义参数分布
param_dist = {
    'clf__n_estimators': randint(50, 300),
    'clf__max_depth': randint(5, 30),
    'clf__min_samples_split': randint(2, 20),
    'clf__min_samples_leaf': randint(1, 10),
    'clf__max_features': uniform(0.1, 0.9)
}

# 随机搜索
random_search = RandomizedSearchCV(
    pipe,
    param_dist,
    n_iter=50,          # 采样次数
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    random_state=42,
    verbose=1
)

print("\n=== 随机搜索 ===")
random_search.fit(X, y)

print(f"最优参数: {random_search.best_params_}")
print(f"最优得分: {random_search.best_score_:.4f}")
```

### 2.3 贝叶斯优化

```python
# 需要安装: pip install optuna
try:
    import optuna
    from optuna.samplers import TPESampler
    
    def objective(trial):
        """优化目标函数"""
        n_estimators = trial.suggest_int('n_estimators', 50, 300)
        max_depth = trial.suggest_int('max_depth', 5, 30)
        min_samples_split = trial.suggest_int('min_samples_split', 2, 20)
        min_samples_leaf = trial.suggest_int('min_samples_leaf', 1, 10)
        
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=42,
            n_jobs=-1
        )
        
        score = cross_val_score(model, X, y, cv=5, scoring='accuracy', n_jobs=-1).mean()
        return score
    
    print("\n=== 贝叶斯优化 (Optuna) ===")
    study = optuna.create_study(direction='maximize', sampler=TPESampler(seed=42))
    study.optimize(objective, n_trials=50, show_progress_bar=True)
    
    print(f"最优参数: {study.best_params}")
    print(f"最优得分: {study.best_value:.4f}")
    
    # 优化历史可视化
    optuna.visualization.matplotlib.plot_optimization_history(study)
    plt.savefig('optuna_history.png', dpi=100, bbox_inches='tight')
    plt.close()
    
    # 参数重要性
    optuna.visualization.matplotlib.plot_param_importances(study)
    plt.savefig('optuna_importance.png', dpi=100, bbox_inches='tight')
    plt.close()
    
except ImportError:
    print("Optuna未安装，请运行: pip install optuna")
```

### 2.4 调优方法对比

```python
import time
import pandas as pd

# 对比不同调优方法
results_comparison = []

# GridSearch (简化版)
param_grid_simple = {
    'clf__n_estimators': [50, 100, 200],
    'clf__max_depth': [5, 10, 15]
}

start = time.time()
grid = GridSearchCV(pipe, param_grid_simple, cv=5, scoring='accuracy', n_jobs=-1)
grid.fit(X, y)
time_grid = time.time() - start

results_comparison.append({
    'Method': 'GridSearch',
    'Score': grid.best_score_,
    'Time': time_grid,
    'Trials': len(grid.cv_results_['params'])
})

# RandomizedSearch
param_dist_simple = {
    'clf__n_estimators': randint(50, 200),
    'clf__max_depth': randint(5, 15)
}

start = time.time()
random_search = RandomizedSearchCV(pipe, param_dist_simple, n_iter=10, cv=5, 
                                    scoring='accuracy', n_jobs=-1, random_state=42)
random_search.fit(X, y)
time_random = time.time() - start

results_comparison.append({
    'Method': 'RandomizedSearch',
    'Score': random_search.best_score_,
    'Time': time_random,
    'Trials': random_search.n_iter
})

# 结果对比
df_comparison = pd.DataFrame(results_comparison)
print("\n=== 调优方法对比 ===")
print(df_comparison)
```

---

## 三、特征工程

### 3.1 特征选择

```python
from sklearn.feature_selection import (
    SelectKBest,
    f_classif,
    mutual_info_classif,
    RFE,
    SelectFromModel,
    VarianceThreshold
)
from sklearn.linear_model import LogisticRegression

# 方差阈值（删除低方差特征）
vt = VarianceThreshold(threshold=0.1)
X_vt = vt.fit_transform(X)
print(f"方差阈值后特征数: {X_vt.shape[1]} (原: {X.shape[1]})")

# 单变量特征选择
skb = SelectKBest(score_func=f_classif, k=10)
X_skb = skb.fit_transform(X, y)
print(f"SelectKBest后特征数: {X_skb.shape[1]}")

# 查看选择的特征
selected_features = data.feature_names[skb.get_support()]
print(f"选择的特征: {selected_features}")

# 递归特征消除 (RFE)
lr = LogisticRegression(max_iter=1000, random_state=42)
rfe = RFE(estimator=lr, n_features_to_select=10)
X_rfe = rfe.fit_transform(X, y)
print(f"RFE后特征数: {X_rfe.shape[1]}")

# 基于模型的特征选择
rf = RandomForestClassifier(n_estimators=100, random_state=42)
sfm = SelectFromModel(rf, threshold='median')
X_sfm = sfm.fit_transform(X, y)
print(f"基于模型选择后特征数: {X_sfm.shape[1]}")

# 特征重要性可视化
rf.fit(X, y)
importances = rf.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(12, 8))
plt.bar(range(len(importances)), importances[indices])
plt.xticks(range(len(importances)), [data.feature_names[i] for i in indices], rotation=90)
plt.xlabel('特征')
plt.ylabel('重要性')
plt.title('特征重要性 (随机森林)')
plt.tight_layout()
plt.savefig('feature_importance_full.png', dpi=100, bbox_inches='tight')
plt.close()
```

### 3.2 特征变换

```python
from sklearn.preprocessing import (
    StandardScaler,
    MinMaxScaler,
    RobustScaler,
    QuantileTransformer,
    PowerTransformer,
    PolynomialFeatures
)

# 生成示例数据
np.random.seed(42)
X_example = np.random.randn(100, 2) * [10, 0.1] + [100, 5]

scalers = {
    'StandardScaler': StandardScaler(),
    'MinMaxScaler': MinMaxScaler(),
    'RobustScaler': RobustScaler(),
    'QuantileTransformer': QuantileTransformer(output_distribution='normal'),
    'PowerTransformer': PowerTransformer(method='yeo-johnson')
}

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.ravel()

# 原始数据
axes[0].scatter(X_example[:, 0], X_example[:, 1], alpha=0.5)
axes[0].set_title('原始数据')
axes[0].set_xlabel('特征1')
axes[0].set_ylabel('特征2')

# 各种缩放方法
for idx, (name, scaler) in enumerate(scalers.items(), 1):
    X_scaled = scaler.fit_transform(X_example)
    axes[idx].scatter(X_scaled[:, 0], X_scaled[:, 1], alpha=0.5)
    axes[idx].set_title(name)
    axes[idx].set_xlabel('特征1')
    axes[idx].set_ylabel('特征2')

plt.tight_layout()
plt.savefig('scalers_comparison.png', dpi=100, bbox_inches='tight')
plt.close()

# 多项式特征
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X[:5])
print(f"\n多项式特征示例:")
print(f"原始特征数: {X.shape[1]}")
print(f"多项式特征数: {X_poly.shape[1]}")
```

### 3.3 特征管道

```python
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

# 创建混合类型数据
np.random.seed(42)
n_samples = 1000

df = pd.DataFrame({
    'numeric1': np.random.randn(n_samples),
    'numeric2': np.random.randn(n_samples) * 10,
    'category1': np.random.choice(['A', 'B', 'C'], n_samples),
    'category2': np.random.choice(['X', 'Y'], n_samples),
    'target': np.random.randint(0, 2, n_samples)
})

# 引入缺失值
df.loc[np.random.choice(n_samples, 50), 'numeric1'] = np.nan
df.loc[np.random.choice(n_samples, 30), 'category1'] = np.nan

print("数据概览:")
print(df.head())

# 定义预处理管道
numeric_features = ['numeric1', 'numeric2']
categorical_features = ['category1', 'category2']

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# 完整管道
full_pipe = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# 训练
X = df.drop('target', axis=1)
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
full_pipe.fit(X_train, y_train)

print(f"\n管道测试得分: {full_pipe.score(X_test, y_test):.4f}")
```

---

## 四、模型持久化

```python
import joblib
import pickle

# 保存模型
joblib.dump(full_pipe, 'model_pipeline.joblib')

# 加载模型
loaded_model = joblib.load('model_pipeline.joblib')

# 验证
print(f"加载模型得分: {loaded_model.score(X_test, y_test):.4f}")

# 也可以使用pickle
with open('model_pipeline.pkl', 'wb') as f:
    pickle.dump(full_pipe, f)

with open('model_pipeline.pkl', 'rb') as f:
    loaded_model_pkl = pickle.load(f)

print(f"Pickle加载模型得分: {loaded_model_pkl.score(X_test, y_test):.4f}")
```

---

## 参考资源

> - [Scikit-learn模型选择](https://scikit-learn.org/stable/model_selection.html) - 官方模型选择指南
> - [Scikit-learn特征工程](https://scikit-learn.org/stable/modules/preprocessing.html) - 官方预处理文档
> - [Optuna官方文档](https://optuna.readthedocs.io/) - 贝叶斯优化框架
> - [Hyperopt文档](http://hyperopt.github.io/hyperopt/) - 另一个调参框架
> - [Feature Engineering for ML](https://www.oreilly.com/library/view/feature-engineering-for/9781491953235/) - 特征工程书籍
> - [Kaggle模型调参指南](https://www.kaggle.com/code/prashant111/a-guide-on-xgboost-hyperparameters-tuning) - XGBoost调参
> - [AutoML with Scikit-learn](https://scikit-learn.org/stable/modules/grid_search.html) - 自动化机器学习

---

**上一篇**：[无监督学习]({{ site.baseurl }}{% post_url /ailearn/02-machine-learning/2026-04-13-03-unsupervised-learning %})

**下一篇**：[机器学习实战案例]({{ site.baseurl }}{% post_url /ailearn/02-machine-learning/2026-04-13-05-ml-projects %})

**返回**：[机器学习基础]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-02-machine-learning %})

*最后更新: 2026年4月13日*
