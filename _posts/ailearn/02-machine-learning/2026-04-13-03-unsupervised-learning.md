---
layout: post
title: "无监督学习 - 聚类与降维算法"
date: 2026-04-13
categories: ailearn
tags: [AI, 机器学习, 无监督学习, 聚类, 降维]
keywords: K-Means, DBSCAN, 层次聚类, PCA, t-SNE, 降维
description: 深入学习无监督学习核心算法，掌握聚类和降维的原理与实践
---

* content
{:toc}

> **前置知识**：需要先掌握 [监督学习算法]({{ site.baseurl }}{% post_url /ailearn/02-machine-learning/2026-04-13-01-supervised-learning %})
>
> **本文重点**：理解无监督学习原理，掌握聚类和降维算法

---

## 一、无监督学习概述

### 1.1 什么是无监督学习

无监督学习处理**没有标签**的数据，目标是发现数据内在结构和模式。

```
无监督学习
├── 聚类 (Clustering)
│   ├── K-Means
│   ├── DBSCAN
│   └── 层次聚类
├── 降维 (Dimensionality Reduction)
│   ├── PCA
│   ├── t-SNE
│   └── UMAP
└── 关联规则
    └── Apriori, FP-Growth
```

### 1.2 应用场景

```python
"""
无监督学习应用场景：

1. 客户细分：根据行为数据划分客户群体
2. 异常检测：识别偏离正常模式的异常点
3. 图像压缩：降维减少存储空间
4. 推荐系统：发现相似用户/物品
5. 数据可视化：高维数据可视化
6. 特征提取：自动学习数据特征
"""
```

---

## 二、聚类算法

### 2.1 K-Means 聚类

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.datasets import make_blobs, make_moons, make_circles
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.preprocessing import StandardScaler

# ===== 1. 基础K-Means =====
# 生成模拟数据
X, y_true = make_blobs(
    n_samples=500,
    n_features=2,
    centers=4,
    cluster_std=1.5,
    random_state=42
)

# K-Means聚类
kmeans = KMeans(
    n_clusters=4,          # 聚类数量
    init='k-means++',      # 初始化方法
    n_init=10,             # 运行次数
    max_iter=300,          # 最大迭代
    random_state=42
)
kmeans.fit(X)

# 获取结果
labels = kmeans.labels_
centers = kmeans.cluster_centers_

print("=== K-Means聚类 ===")
print(f"聚类中心:\n{centers}")
print(f"惯性(Inertia): {kmeans.inertia_:.2f}")  # 样本到最近中心的距离平方和
print(f"轮廓系数: {silhouette_score(X, labels):.4f}")

# 可视化
plt.figure(figsize=(12, 5))

plt.subplot(121)
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', alpha=0.6)
plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='x', s=200, linewidths=3)
plt.title('K-Means聚类结果')
plt.xlabel('特征1')
plt.ylabel('特征2')

# 真实标签
plt.subplot(122)
plt.scatter(X[:, 0], X[:, 1], c=y_true, cmap='viridis', alpha=0.6)
plt.title('真实标签')
plt.xlabel('特征1')

plt.tight_layout()
plt.savefig('kmeans_basic.png', dpi=100, bbox_inches='tight')
plt.close()

# ===== 2. 确定最优K值 =====
# 肘部法则
inertias = []
silhouettes = []
K_range = range(2, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)
    silhouettes.append(silhouette_score(X, kmeans.labels_))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 肘部法则图
axes[0].plot(K_range, inertias, 'bo-')
axes[0].set_xlabel('聚类数量 K')
axes[0].set_ylabel('惯性 (Inertia)')
axes[0].set_title('肘部法则')
axes[0].grid(True, alpha=0.3)

# 轮廓系数图
axes[1].plot(K_range, silhouettes, 'go-')
axes[1].set_xlabel('聚类数量 K')
axes[1].set_ylabel('轮廓系数')
axes[1].set_title('轮廓系数法')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('kmeans_optimal_k.png', dpi=100, bbox_inches='tight')
plt.close()

print(f"\n最优K值(轮廓系数): {K_range[np.argmax(silhouettes)]}")

# ===== 3. Mini-Batch K-Means =====
# 大数据集使用
X_large, _ = make_blobs(n_samples=50000, centers=10, random_state=42)

# 标准K-Means
import time
start = time.time()
kmeans_full = KMeans(n_clusters=10, random_state=42)
kmeans_full.fit(X_large)
time_full = time.time() - start

# Mini-Batch K-Means
start = time.time()
kmeans_mini = MiniBatchKMeans(n_clusters=10, batch_size=1000, random_state=42)
kmeans_mini.fit(X_large)
time_mini = time.time() - start

print(f"\n标准K-Means时间: {time_full:.2f}s")
print(f"Mini-Batch K-Means时间: {time_mini:.2f}s")
```

### 2.2 DBSCAN 密度聚类

```python
from sklearn.cluster import DBSCAN

"""
DBSCAN原理：
1. 核心点：半径ε内至少有min_samples个点
2. 边界点：在核心点ε邻域内，但自身不满足核心点条件
3. 噪声点：既非核心点也非边界点

优点：
- 不需要预设聚类数量
- 能发现任意形状的簇
- 能识别噪声点
"""

# 生成非凸数据
X_moons, _ = make_moons(n_samples=300, noise=0.05, random_state=42)
X_circles, _ = make_circles(n_samples=300, noise=0.05, factor=0.5, random_state=42)

# K-Means vs DBSCAN对比
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

for idx, (X, title) in enumerate([(X_moons, '月牙形数据'), (X_circles, '环形数据')]):
    # K-Means
    kmeans = KMeans(n_clusters=2, random_state=42)
    kmeans_labels = kmeans.fit_predict(X)
    
    axes[idx, 0].scatter(X[:, 0], X[:, 1], c=kmeans_labels, cmap='viridis', alpha=0.6)
    axes[idx, 0].set_title(f'{title} - K-Means')
    
    # DBSCAN
    dbscan = DBSCAN(eps=0.2, min_samples=5)
    dbscan_labels = dbscan.fit_predict(X)
    
    axes[idx, 1].scatter(X[:, 0], X[:, 1], c=dbscan_labels, cmap='viridis', alpha=0.6)
    axes[idx, 1].set_title(f'{title} - DBSCAN')

plt.tight_layout()
plt.savefig('kmeans_vs_dbscan.png', dpi=100, bbox_inches='tight')
plt.close()

# ===== DBSCAN参数调优 =====
from sklearn.neighbors import NearestNeighbors

# 寻找最优eps
X, _ = make_moons(n_samples=500, noise=0.05, random_state=42)

# K-distance图
neighbors = NearestNeighbors(n_neighbors=5)
neighbors.fit(X)
distances, indices = neighbors.kneighbors(X)
distances = np.sort(distances[:, 4])

plt.figure(figsize=(10, 6))
plt.plot(distances)
plt.xlabel('样本索引（排序后）')
plt.ylabel('第5近邻距离')
plt.title('K-distance图（用于选择eps）')
plt.axhline(y=0.15, color='r', linestyle='--', label='建议eps')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('dbscan_eps.png', dpi=100, bbox_inches='tight')
plt.close()

# 不同参数的DBSCAN
eps_values = [0.1, 0.15, 0.2]
min_samples_values = [3, 5, 10]

fig, axes = plt.subplots(len(eps_values), len(min_samples_values), figsize=(15, 12))

for i, eps in enumerate(eps_values):
    for j, min_samples in enumerate(min_samples_values):
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(X)
        
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise = list(labels).count(-1)
        
        axes[i, j].scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', alpha=0.6)
        axes[i, j].set_title(f'eps={eps}, min_samples={min_samples}\n簇数={n_clusters}, 噪声={n_noise}')

plt.tight_layout()
plt.savefig('dbscan_params.png', dpi=100, bbox_inches='tight')
plt.close()
```

### 2.3 层次聚类

```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

"""
层次聚类：
1. 自底向上（凝聚）：每个点开始是一个簇，逐步合并
2. 自顶向下（分裂）：所有点开始是一个簇，逐步分裂

链接方式：
- ward：最小方差（默认）
- complete：最大距离
- average：平均距离
- single：最小距离
"""

# 生成数据
X, _ = make_blobs(n_samples=150, centers=3, random_state=42)

# 层次聚类
linkage_methods = ['ward', 'complete', 'average', 'single']

fig, axes = plt.subplots(2, 2, figsize=(14, 12))

for ax, method in zip(axes.ravel(), linkage_methods):
    # 凝聚聚类
    cluster = AgglomerativeClustering(n_clusters=3, linkage=method)
    labels = cluster.fit_predict(X)
    
    ax.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', alpha=0.6)
    ax.set_title(f'链接方式: {method}')

plt.tight_layout()
plt.savefig('hierarchical_methods.png', dpi=100, bbox_inches='tight')
plt.close()

# 绘制树状图
plt.figure(figsize=(12, 8))
Z = linkage(X, method='ward')
dendrogram(Z, truncate_mode='level', p=3)
plt.title('层次聚类树状图')
plt.xlabel('样本索引')
plt.ylabel('距离')
plt.savefig('dendrogram.png', dpi=100, bbox_inches='tight')
plt.close()
```

### 2.4 聚类评估

```python
from sklearn.metrics import (
    silhouette_score,       # 轮廓系数 [-1, 1]，越大越好
    calinski_harabasz_score, # CH指数，越大越好
    davies_bouldin_score    # DB指数，越小越好
)

def evaluate_clustering(X, labels, name):
    """评估聚类结果"""
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    
    if n_clusters > 1:
        metrics = {
            '轮廓系数': silhouette_score(X, labels),
            'CH指数': calinski_harabasz_score(X, labels),
            'DB指数': davies_bouldin_score(X, labels)
        }
    else:
        metrics = {'轮廓系数': None, 'CH指数': None, 'DB指数': None}
    
    print(f"\n{name}:")
    print(f"  簇数: {n_clusters}")
    for metric, value in metrics.items():
        if value is not None:
            print(f"  {metric}: {value:.4f}")
        else:
            print(f"  {metric}: 无法计算（簇数<=1）")

# 对比不同聚类方法
X, _ = make_blobs(n_samples=500, centers=4, random_state=42)

# K-Means
kmeans = KMeans(n_clusters=4, random_state=42)
kmeans_labels = kmeans.fit_predict(X)
evaluate_clustering(X, kmeans_labels, "K-Means")

# DBSCAN
dbscan = DBSCAN(eps=0.8, min_samples=5)
dbscan_labels = dbscan.fit_predict(X)
evaluate_clustering(X, dbscan_labels, "DBSCAN")

# 层次聚类
agg = AgglomerativeClustering(n_clusters=4)
agg_labels = agg.fit_predict(X)
evaluate_clustering(X, agg_labels, "层次聚类")
```

---

## 三、降维算法

### 3.1 PCA 主成分分析

```python
from sklearn.decomposition import PCA, IncrementalPCA, KernelPCA
from sklearn.preprocessing import StandardScaler

"""
PCA原理：
1. 标准化数据
2. 计算协方差矩阵
3. 计算特征值和特征向量
4. 选择前k个主成分
5. 转换数据
"""

# ===== 1. 基础PCA =====
from sklearn.datasets import load_digits

# 加载手写数字数据集
digits = load_digits()
X = digits.data
y = digits.target

print(f"原始数据维度: {X.shape}")  # (1797, 64)

# 标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCA降维
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

print(f"降维后维度: {X_pca.shape}")
print(f"解释方差比例: {pca.explained_variance_ratio_}")
print(f"累计解释方差: {pca.explained_variance_ratio_.sum():.4f}")

# 可视化
plt.figure(figsize=(12, 8))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='tab10', alpha=0.6)
plt.colorbar(scatter)
plt.xlabel('第一主成分')
plt.ylabel('第二主成分')
plt.title('PCA降维可视化 (手写数字)')
plt.savefig('pca_digits.png', dpi=100, bbox_inches='tight')
plt.close()

# ===== 2. 选择主成分数量 =====
pca_full = PCA().fit(X_scaled)

plt.figure(figsize=(10, 6))
plt.plot(np.cumsum(pca_full.explained_variance_ratio_), 'bo-')
plt.xlabel('主成分数量')
plt.ylabel('累计解释方差比例')
plt.title('PCA累计解释方差')
plt.axhline(y=0.95, color='r', linestyle='--', label='95%方差')
plt.axvline(x=np.argmax(np.cumsum(pca_full.explained_variance_ratio_) >= 0.95), 
            color='r', linestyle='--')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('pca_variance.png', dpi=100, bbox_inches='tight')
plt.close()

# ===== 3. 增量PCA =====
# 大数据集使用
ipca = IncrementalPCA(n_components=20, batch_size=100)
X_ipca = ipca.fit_transform(X_scaled)
print(f"\n增量PCA解释方差: {ipca.explained_variance_ratio_.sum():.4f}")

# ===== 4. 核PCA =====
# 非线性降维
kpca = KernelPCA(n_components=2, kernel='rbf', gamma=0.1)
X_kpca = kpca.fit_transform(X_scaled)

plt.figure(figsize=(10, 8))
scatter = plt.scatter(X_kpca[:, 0], X_kpca[:, 1], c=y, cmap='tab10', alpha=0.6)
plt.colorbar(scatter)
plt.xlabel('第一核主成分')
plt.ylabel('第二核主成分')
plt.title('核PCA降维可视化')
plt.savefig('kpca_digits.png', dpi=100, bbox_inches='tight')
plt.close()
```

### 3.2 t-SNE 可视化

```python
from sklearn.manifold import TSNE

"""
t-SNE原理：
1. 计算高维空间中点对之间的相似度
2. 计算低维空间中的相似度
3. 最小化两个分布之间的KL散度

特点：
- 非常适合可视化
- 保留局部结构
- 计算量大
"""

# t-SNE降维
tsne = TSNE(
    n_components=2,
    perplexity=30,      # 困惑度，影响局部/全局结构平衡
    learning_rate=200,  # 学习率
    n_iter=1000,        # 迭代次数
    random_state=42
)
X_tsne = tsne.fit_transform(X_scaled)

plt.figure(figsize=(12, 8))
scatter = plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=y, cmap='tab10', alpha=0.6)
plt.colorbar(scatter)
plt.xlabel('t-SNE维度1')
plt.ylabel('t-SNE维度2')
plt.title('t-SNE可视化 (手写数字)')
plt.savefig('tsne_digits.png', dpi=100, bbox_inches='tight')
plt.close()

# 不同perplexity对比
perplexities = [5, 30, 50, 100]

fig, axes = plt.subplots(2, 2, figsize=(14, 12))

for ax, perp in zip(axes.ravel(), perplexities):
    tsne = TSNE(n_components=2, perplexity=perp, random_state=42)
    X_tsne = tsne.fit_transform(X_scaled)
    
    scatter = ax.scatter(X_tsne[:, 0], X_tsne[:, 1], c=y, cmap='tab10', alpha=0.6)
    ax.set_title(f'perplexity={perp}')
    ax.set_xlabel('t-SNE维度1')
    ax.set_ylabel('t-SNE维度2')

plt.tight_layout()
plt.savefig('tsne_perplexity.png', dpi=100, bbox_inches='tight')
plt.close()
```

### 3.3 UMAP

```python
# 需要安装: pip install umap-learn
try:
    import umap
    
    """
    UMAP特点：
    - 比t-SNE更快
    - 更好地保留全局结构
    - 可以用于特征提取
    """
    
    reducer = umap.UMAP(
        n_neighbors=15,
        min_dist=0.1,
        n_components=2,
        random_state=42
    )
    X_umap = reducer.fit_transform(X_scaled)
    
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(X_umap[:, 0], X_umap[:, 1], c=y, cmap='tab10', alpha=0.6)
    plt.colorbar(scatter)
    plt.xlabel('UMAP维度1')
    plt.ylabel('UMAP维度2')
    plt.title('UMAP可视化 (手写数字)')
    plt.savefig('umap_digits.png', dpi=100, bbox_inches='tight')
    plt.close()
    
except ImportError:
    print("UMAP未安装，请运行: pip install umap-learn")
```

### 3.4 降维方法对比

```python
import time

# 对比不同降维方法
methods = {
    'PCA': PCA(n_components=2),
    'KernelPCA': KernelPCA(n_components=2, kernel='rbf', gamma=0.01),
    't-SNE': TSNE(n_components=2, perplexity=30, random_state=42)
}

results = {}
for name, method in methods.items():
    start = time.time()
    X_transformed = method.fit_transform(X_scaled)
    elapsed = time.time() - start
    
    results[name] = {
        'data': X_transformed,
        'time': elapsed
    }
    print(f"{name}: {elapsed:.2f}s")

# 可视化对比
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for ax, (name, result) in zip(axes, results.items()):
    scatter = ax.scatter(result['data'][:, 0], result['data'][:, 1], 
                         c=y, cmap='tab10', alpha=0.6)
    ax.set_title(f'{name} (耗时: {result["time"]:.2f}s)')
    ax.set_xlabel('维度1')
    ax.set_ylabel('维度2')
    plt.colorbar(scatter, ax=ax)

plt.tight_layout()
plt.savefig('dim_reduction_comparison.png', dpi=100, bbox_inches='tight')
plt.close()
```

---

## 四、实战案例：客户细分

```python
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# 生成模拟客户数据
np.random.seed(42)
n_customers = 1000

df = pd.DataFrame({
    'customer_id': range(1, n_customers + 1),
    'age': np.random.randint(18, 70, n_customers),
    'annual_income': np.random.normal(50000, 20000, n_customers),
    'spending_score': np.random.randint(1, 101, n_customers),
    'years_as_customer': np.random.randint(1, 10, n_customers),
    'purchase_frequency': np.random.poisson(5, n_customers)
})

# 确保收入为正
df['annual_income'] = df['annual_income'].clip(lower=10000)

print("客户数据概览:")
print(df.describe())

# 选择特征用于聚类
features = ['age', 'annual_income', 'spending_score', 'years_as_customer', 'purchase_frequency']
X = df[features].values

# 标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 确定最优K值
inertias = []
silhouettes = []
K_range = range(2, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)
    silhouettes.append(silhouette_score(X_scaled, kmeans.labels_))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(K_range, inertias, 'bo-')
axes[0].set_xlabel('聚类数量 K')
axes[0].set_ylabel('惯性')
axes[0].set_title('肘部法则')
axes[0].grid(True, alpha=0.3)

axes[1].plot(K_range, silhouettes, 'go-')
axes[1].set_xlabel('聚类数量 K')
axes[1].set_ylabel('轮廓系数')
axes[1].set_title('轮廓系数法')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('customer_segmentation_k.png', dpi=100, bbox_inches='tight')
plt.close()

# 选择K=4进行聚类
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(X_scaled)

# 使用PCA可视化
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(12, 8))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=df['cluster'], cmap='viridis', alpha=0.6)
plt.colorbar(scatter)
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')
plt.title('客户细分结果 (PCA可视化)')
plt.savefig('customer_segmentation_pca.png', dpi=100, bbox_inches='tight')
plt.close()

# 分析各群体特征
cluster_summary = df.groupby('cluster')[features].mean().round(2)
print("\n各客户群体特征:")
print(cluster_summary)

# 群体命名
cluster_names = {
    0: '普通客户',
    1: '高价值客户',
    2: '潜力客户',
    3: '待激活客户'
}
df['segment'] = df['cluster'].map(cluster_names)

# 群体分布
plt.figure(figsize=(10, 6))
df['segment'].value_counts().plot(kind='bar')
plt.xlabel('客户群体')
plt.ylabel('客户数量')
plt.title('客户群体分布')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('customer_segment_distribution.png', dpi=100, bbox_inches='tight')
plt.close()
```

---

## 参考资源

> - [Scikit-learn聚类文档](https://scikit-learn.org/stable/modules/clustering.html) - 官方聚类指南
> - [Scikit-learn降维文档](https://scikit-learn.org/stable/modules/decomposition.html) - 官方降维指南
> - [t-SNE论文](https://www.jmlr.org/papers/volume9/vandermaaten08a/vandermaaten08a.pdf) - t-SNE原始论文
> - [UMAP文档](https://umap-learn.readthedocs.io/) - UMAP官方文档
> - [斯坦福CS224n - 降维](https://web.stanford.edu/class/cs224n/) - 包含降维技术讲解
> - [如何正确使用t-SNE](https://distill.pub/2016/misread-tsne/) - t-SNE使用指南
> - [聚类算法比较](https://scikit-learn.org/stable/auto_examples/cluster/plot_cluster_comparison.html) - 官方算法对比

---

**上一篇**：[集成学习方法]({{ site.baseurl }}{% post_url /ailearn/02-machine-learning/2026-04-13-02-ensemble-learning %})

**下一篇**：[模型评估与调优]({{ site.baseurl }}{% post_url /ailearn/02-machine-learning/2026-04-13-04-model-evaluation %})

**返回**：[机器学习基础]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-02-machine-learning %})

*最后更新: 2026年4月13日*
