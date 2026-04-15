---
layout: post
title: "NumPy 进阶教程 - 线性代数与高级操作"
date: 2026-04-12
categories: ailearn
tags: [AI, Python, NumPy, 线性代数]
keywords: NumPy, 线性代数, 矩阵运算, 特征值, 深度学习数学基础
description: 深入学习 NumPy 线性代数运算、高级索引技巧和性能优化，为深度学习奠定数学基础
---

* content
{:toc}

> **前置知识**：需要先掌握 [NumPy 基础教程]({{ site.baseurl }}{% post_url /ailearn/01-numpy-pandas/2026-04-12-numpy-basic %})。
>
> **本文重点**：线性代数运算、高级数组操作、性能优化技巧。

本文深入讲解 NumPy 的线性代数功能，这些是理解深度学习神经网络运算的基础。

---

## 一、线性代数基础

### 1.1 向量运算

```python
import numpy as np

# 向量定义
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])

# 向量加法
v_add = v1 + v2
print(f"向量加法: {v_add}")  # [5 7 9]

# 向量减法
v_sub = v2 - v1
print(f"向量减法: {v_sub}")  # [3 3 3]

# 标量乘法
v_scaled = 3 * v1
print(f"标量乘法: {v_scaled}")  # [3 6 9]

# 向量点积（内积）
dot_product = np.dot(v1, v2)
print(f"点积: {dot_product}")  # 1*4 + 2*5 + 3*6 = 32

# 使用 @ 运算符（Python 3.5+）
dot_product_2 = v1 @ v2
print(f"点积 (@): {dot_product_2}")

# 向量的范数（长度）
l2_norm = np.linalg.norm(v1)  # L2范数（欧几里得范数）
print(f"L2范数: {l2_norm}")  # sqrt(1+4+9) ≈ 3.742

l1_norm = np.linalg.norm(v1, ord=1)  # L1范数
print(f"L1范数: {l1_norm}")  # 1+2+3 = 6

# 向量夹角余弦值
cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
print(f"余弦相似度: {cos_angle}")

# 向量的外积
outer = np.outer(v1, v2)
print(f"外积:\n{outer}")
# [[ 4  5  6]
#  [ 8 10 12]
#  [12 15 18]]
```

### 1.2 矩阵运算

```python
import numpy as np

# 矩阵定义
A = np.array([[1, 2, 3],
              [4, 5, 6]])
B = np.array([[7, 8],
              [9, 10],
              [11, 12]])

print(f"A形状: {A.shape}")  # (2, 3)
print(f"B形状: {B.shape}")  # (3, 2)

# 矩阵乘法
C = np.dot(A, B)  # 或 A @ B
print(f"矩阵乘法结果:\n{C}")
# [[ 58  64]
#  [139 154]]

# 元素级乘法（Hadamard积）
A_square = np.array([[1, 2], [3, 4]])
B_square = np.array([[5, 6], [7, 8]])
hadamard = A_square * B_square  # 对应元素相乘
print(f"Hadamard积:\n{hadamard}")
# [[ 5 12]
#  [21 32]]

# 矩阵转置
A_T = A.T
print(f"转置后形状: {A_T.shape}")  # (3, 2)

# 矩阵加法
C_add = A_square + B_square
print(f"矩阵加法:\n{C_add}")

# 标量与矩阵
scaled = 2 * A
print(f"标量乘矩阵:\n{scaled}")
```

### 1.3 特殊矩阵

```python
import numpy as np

# 单位矩阵
I = np.eye(4)
print(f"单位矩阵:\n{I}")

# 零矩阵
Z = np.zeros((3, 3))
print(f"零矩阵:\n{Z}")

# 对角矩阵
diag = np.diag([1, 2, 3, 4])
print(f"对角矩阵:\n{diag}")

# 从矩阵提取对角线
A = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])
diagonal = np.diag(A)
print(f"对角线元素: {diagonal}")  # [1 5 9]

# 三角矩阵
upper = np.triu(A)  # 上三角
lower = np.tril(A)  # 下三角
print(f"上三角:\n{upper}")
print(f"下三角:\n{lower}")

# 对称矩阵
symmetric = np.array([[1, 2, 3],
                       [2, 4, 5],
                       [3, 5, 6]])
print(f"是否对称: {np.allclose(symmetric, symmetric.T)}")

# 正定矩阵检查
def is_positive_definite(M):
    """检查矩阵是否正定"""
    try:
        np.linalg.cholesky(M)
        return True
    except np.linalg.LinAlgError:
        return False

pd_matrix = np.array([[2, 1], [1, 2]])
print(f"是否正定: {is_positive_definite(pd_matrix)}")
```

---

## 二、矩阵分解

### 2.1 特征值与特征向量

```python
import numpy as np

# 对于方阵 A，存在 λ 和 v 使得 Av = λv
A = np.array([[4, -2],
              [1,  1]])

# 计算特征值和特征向量
eigenvalues, eigenvectors = np.linalg.eig(A)

print(f"特征值: {eigenvalues}")
print(f"特征向量（列向量）:\n{eigenvectors}")

# 验证：A @ v = λ @ v
for i in range(len(eigenvalues)):
    v = eigenvectors[:, i]
    lam = eigenvalues[i]
    print(f"验证特征值 {lam:.2f}: {np.allclose(A @ v, lam * v)}")

# 特征值排序
idx = eigenvalues.argsort()[::-1]  # 降序
eigenvalues_sorted = eigenvalues[idx]
eigenvectors_sorted = eigenvectors[:, idx]

# 实对称矩阵的特征值都是实数
symmetric = np.array([[1, 2, 3],
                       [2, 4, 5],
                       [3, 5, 6]])
eigenvalues, eigenvectors = np.linalg.eigh(symmetric)  # eigh 专用于对称矩阵
print(f"对称矩阵特征值: {eigenvalues}")
```

### 2.2 奇异值分解 (SVD)

SVD 是最重要的矩阵分解之一，在推荐系统、图像压缩、PCA 中广泛应用。

```python
import numpy as np

# SVD: A = U @ Σ @ V^T
A = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9],
              [10, 11, 12]])

U, S, Vt = np.linalg.svd(A, full_matrices=False)

print(f"U形状: {U.shape}")    # (4, 3) - 左奇异向量
print(f"S形状: {S.shape}")    # (3,)   - 奇异值
print(f"Vt形状: {Vt.shape}")  # (3, 3) - 右奇异向量

print(f"奇异值: {S}")

# 重构矩阵
A_reconstructed = U @ np.diag(S) @ Vt
print(f"重构误差: {np.allclose(A, A_reconstructed)}")

# ===== 应用：低秩近似（图像压缩）=====
def svd_compress(A, k):
    """保留前k个奇异值进行压缩"""
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    return U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]

# 示例：模拟图像压缩
image = np.random.rand(100, 100)
compressed = svd_compress(image, 20)  # 只保留20个奇异值
print(f"原始数据量: {image.size}")
print(f"压缩数据量: {100*20 + 20 + 20*100}")  # U + S + Vt

# 计算压缩率
original_size = image.size
compressed_size = 100 * 20 + 20 + 20 * 100
print(f"压缩率: {compressed_size / original_size:.2%}")
```

### 2.3 QR 分解

```python
import numpy as np

A = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]], dtype=float)

Q, R = np.linalg.qr(A)

print(f"Q（正交矩阵）:\n{Q}")
print(f"R（上三角矩阵）:\n{R}")

# 验证 Q 的正交性
print(f"Q^T @ Q 是否为单位阵: {np.allclose(Q.T @ Q, np.eye(3))}")

# 验证分解
print(f"Q @ R 是否等于 A: {np.allclose(Q @ R, A)}")
```

### 2.4 Cholesky 分解

```python
import numpy as np

# Cholesky分解要求矩阵对称正定
A = np.array([[4, 2, 2],
              [2, 5, 1],
              [2, 1, 6]], dtype=float)

L = np.linalg.cholesky(A)
print(f"下三角矩阵 L:\n{L}")

# 验证: A = L @ L^T
print(f"验证分解: {np.allclose(L @ L.T, A)}")

# 应用：高效求解线性方程组 Ax = b
# 如果 A 正定，可以用 Cholesky 分解加速
b = np.array([1, 2, 3])

# A @ x = b => L @ L^T @ x = b
# 先解 L @ y = b
y = np.linalg.solve(L, b)
# 再解 L^T @ x = y
x = np.linalg.solve(L.T, y)
print(f"解: {x}")
```

---

## 三、线性方程组求解

### 3.1 直接求解

```python
import numpy as np

# 求解 Ax = b
A = np.array([[3, 1],
              [1, 2]], dtype=float)
b = np.array([9, 8], dtype=float)

# 方法1：linalg.solve
x = np.linalg.solve(A, b)
print(f"解: {x}")  # [2. 3.]
print(f"验证: A @ x = {A @ x}")

# 方法2：使用逆矩阵（不推荐，数值稳定性差）
x_inv = np.linalg.inv(A) @ b
print(f"逆矩阵法解: {x_inv}")

# 行列式（判断是否有唯一解）
det = np.linalg.det(A)
print(f"行列式: {det}")  # 非零则有唯一解

# 矩阵的秩
rank = np.linalg.matrix_rank(A)
print(f"秩: {rank}")
```

### 3.2 最小二乘解

```python
import numpy as np

# 过定方程组（方程数 > 未知数）
A = np.array([[1, 1],
              [1, 2],
              [1, 3],
              [1, 4]], dtype=float)
b = np.array([6, 5, 7, 10], dtype=float)

# 最小二乘解
x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
print(f"最小二乘解: {x}")  # 拟合直线 y = x[0] + x[1]*t

# 计算拟合值
fitted = A @ x
print(f"拟合值: {fitted}")
print(f"残差平方和: {residuals}")

# 等价于：使用伪逆
x_pinv = np.linalg.pinv(A) @ b
print(f"伪逆解: {x_pinv}")

# ===== 应用：线性回归 =====
# 模拟数据
np.random.seed(42)
X = np.random.randn(100, 3)  # 100个样本，3个特征
true_w = np.array([1.5, -2.0, 1.0])
y = X @ true_w + np.random.randn(100) * 0.1  # 添加噪声

# 使用最小二乘求解
X_b = np.c_[np.ones(100), X]  # 添加偏置项
w, _, _, _ = np.linalg.lstsq(X_b, y, rcond=None)
print(f"估计权重: {w}")
print(f"真实权重: [偏置, {true_w}]")
```

### 3.3 范数计算

```python
import numpy as np

# 向量范数
v = np.array([3, 4])

print(f"L1范数: {np.linalg.norm(v, ord=1)}")      # 7
print(f"L2范数: {np.linalg.norm(v, ord=2)}")      # 5.0
print(f"无穷范数: {np.linalg.norm(v, ord=np.inf)}")  # 4

# 矩阵范数
A = np.array([[1, 2], [3, 4]])

print(f"Frobenius范数: {np.linalg.norm(A, 'fro')}")
print(f"核范数（奇异值之和）: {np.linalg.norm(A, 'nuc')}")
print(f"算子范数(2-范数): {np.linalg.norm(A, 2)}")  # 最大奇异值
```

---

## 四、高级数组操作

### 4.1 高级索引技巧

```python
import numpy as np

arr = np.arange(24).reshape(4, 6)
print("原数组:\n", arr)

# ===== np.take - 沿轴取元素 =====
# 从第1维取索引 [0, 2]
taken = np.take(arr, [0, 2], axis=0)
print(f"take行[0,2]:\n{taken}")

# 从展平数组取
taken_flat = np.take(arr, [0, 5, 10, 15, 20])
print(f"take展平索引: {taken_flat}")

# ===== np.put - 放置元素 =====
arr_copy = arr.copy()
np.put(arr_copy, [0, 5, 10], [-1, -2, -3])
print("put后:\n", arr_copy)

# ===== np.choose - 多条件选择 =====
choices = np.array([[0, 1, 2, 3],
                    [4, 5, 6, 7],
                    [8, 9, 10, 11]])
indices = np.array([0, 1, 2, 0])  # 每列选择的行索引
selected = np.choose(indices, choices)
print(f"choose结果: {selected}")  # [0 5 10 3]

# ===== np.extract - 条件提取 =====
arr_flat = np.arange(12)
condition = (arr_flat % 3 == 0)
extracted = np.extract(condition, arr_flat)
print(f"3的倍数: {extracted}")
```

### 4.2 排序与搜索

```python
import numpy as np

arr = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])

# ===== 排序 =====
# 返回排序后的数组
sorted_arr = np.sort(arr)
print(f"排序: {sorted_arr}")

# 返回排序索引
sorted_indices = np.argsort(arr)
print(f"排序索引: {sorted_indices}")
print(f"通过索引获取: {arr[sorted_indices]}")

# 降序排序
sorted_desc = np.sort(arr)[::-1]
print(f"降序: {sorted_desc}")

# 多维数组排序
arr_2d = np.array([[3, 1, 4], [1, 5, 9], [2, 6, 5]])
print("原数组:\n", arr_2d)

# 按行排序（每行内部排序）
sorted_rows = np.sort(arr_2d, axis=1)
print("按行排序:\n", sorted_rows)

# 按列排序
sorted_cols = np.sort(arr_2d, axis=0)
print("按列排序:\n", sorted_cols)

# ===== 搜索 =====
# argmax/argmin
print(f"最大值索引: {np.argmax(arr)}")
print(f"最小值索引: {np.argmin(arr)}")

# 沿轴的argmax
arr_2d = np.array([[1, 2, 3], [4, 0, 6]])
print(f"每行最大值索引: {np.argmax(arr_2d, axis=1)}")

# nonzero - 非零元素索引
arr_bool = np.array([0, 1, 0, 2, 0, 3, 0])
nonzero_idx = np.nonzero(arr_bool)
print(f"非零索引: {nonzero_idx}")

# where - 条件索引
indices = np.where(arr > 3)
print(f"大于3的索引: {indices}")

# 搜索排序后的位置
sorted_arr = np.sort(arr)
pos = np.searchsorted(sorted_arr, 4)
print(f"4应该插入的位置: {pos}")

# ===== 去重与统计 =====
unique_vals = np.unique(arr)
print(f"唯一值: {unique_vals}")

# 返回唯一值和计数
vals, counts = np.unique(arr, return_counts=True)
print("值与计数:")
for v, c in zip(vals, counts):
    print(f"  {v}: {c}次")
```

### 4.3 集合操作

```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = np.array([4, 5, 6, 7, 8])

# 交集
intersection = np.intersect1d(a, b)
print(f"交集: {intersection}")  # [4 5]

# 并集
union = np.union1d(a, b)
print(f"并集: {union}")  # [1 2 3 4 5 6 7 8]

# 差集 (a - b)
diff = np.setdiff1d(a, b)
print(f"a-b: {diff}")  # [1 2 3]

# 对称差 (a ∪ b - a ∩ b)
symdiff = np.setxor1d(a, b)
print(f"对称差: {symdiff}")  # [1 2 3 6 7 8]

# 判断是否为子集
print(f"a是否包含[1,2]: {np.isin([1, 2], a)}")  # [True True]
print(f"a是否包含[1,6]: {np.isin([1, 6], a)}")  # [True False]
```

---

## 五、随机数高级应用

### 5.1 概率分布

```python
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# ===== 离散分布 =====
# 0-9均匀随机整数
rand_ints = np.random.randint(0, 10, size=1000)

# 二项分布（n次试验成功k次的概率）
# n=10, p=0.5, 做1000次实验
binomial = np.random.binomial(n=10, p=0.5, size=1000)
print(f"二项分布均值: {binomial.mean():.2f} (理论值: 5)")

# 泊松分布
poisson = np.random.poisson(lam=3, size=1000)
print(f"泊松分布均值: {poisson.mean():.2f} (理论值: 3)")

# ===== 连续分布 =====
# 均匀分布 [a, b)
uniform = np.random.uniform(low=0, high=10, size=1000)
print(f"均匀分布均值: {uniform.mean():.2f} (理论值: 5)")

# 正态分布
normal = np.random.normal(loc=0, scale=1, size=10000)
print(f"正态分布均值: {normal.mean():.4f}")
print(f"正态分布标准差: {normal.std():.4f}")

# 指数分布
exponential = np.random.exponential(scale=2, size=1000)
print(f"指数分布均值: {exponential.mean():.2f} (理论值: 2)")

# ===== 多元分布 =====
# 多元正态分布
mean = [0, 0]
cov = [[1, 0.8], [0.8, 1]]  # 协方差矩阵
multivariate = np.random.multivariate_normal(mean, cov, size=1000)
print(f"多元正态分布形状: {multivariate.shape}")

# 狄利克雷分布（用于生成概率分布）
dirichlet = np.random.dirichlet(alpha=[1, 2, 3], size=5)
print("狄利克雷分布样本（每行和为1）:")
print(dirichlet)
print(f"每行和: {dirichlet.sum(axis=1)}")
```

### 5.2 随机采样与洗牌

```python
import numpy as np

data = np.array(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])

# 随机选择（可重复）
choices = np.random.choice(data, size=5)
print(f"随机选择(可重复): {choices}")

# 随机选择（不重复）
choices_unique = np.random.choice(data, size=5, replace=False)
print(f"随机选择(不重复): {choices_unique}")

# 带权重的选择
weights = [0.4, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0.1]
weighted = np.random.choice(data, size=100, p=weights)
print(f"加权选择统计: {np.unique(weighted, return_counts=True)}")

# 打乱顺序（原地修改）
arr = np.arange(10)
np.random.shuffle(arr)
print(f"打乱后: {arr}")

# 返回打乱的副本（不修改原数组）
arr2 = np.arange(10)
shuffled = np.random.permutation(arr2)
print(f"原数组: {arr2}")
print(f"打乱副本: {shuffled}")

# ===== 应用：数据集划分 =====
def train_test_split(X, y, test_size=0.2, random_state=None):
    """划分训练集和测试集"""
    if random_state:
        np.random.seed(random_state)
    
    n_samples = len(X)
    indices = np.random.permutation(n_samples)
    test_count = int(n_samples * test_size)
    
    test_indices = indices[:test_count]
    train_indices = indices[test_count:]
    
    return X[train_indices], X[test_indices], y[train_indices], y[test_indices]

# 示例
X = np.random.randn(100, 5)
y = np.random.randint(0, 2, 100)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"训练集: {X_train.shape}, 测试集: {X_test.shape}")
```

---

## 六、性能优化进阶

### 6.1 视图与副本

```python
import numpy as np

# ===== 视图（不复制数据）=====
arr = np.arange(10)
view = arr[2:5]  # 切片返回视图
print(f"视图: {view}")

view[0] = 100
print(f"修改视图后原数组: {arr}")  # 原数组也被修改

# ===== 副本（复制数据）=====
arr2 = np.arange(10)
copy = arr2[2:5].copy()
copy[0] = 100
print(f"修改副本后原数组: {arr2}")  # 原数组不变

# ===== 判断是否共享内存 =====
def shares_memory(a, b):
    return np.shares_memory(a, b)

arr = np.arange(10)
view = arr[2:5]
copy = arr[2:5].copy()

print(f"视图共享内存: {shares_memory(arr, view)}")  # True
print(f"副本共享内存: {shares_memory(arr, copy)}")  # False
```

### 6.2 结构化数组

```python
import numpy as np

# 定义结构化数据类型
dt = np.dtype([
    ('name', 'U10'),      # Unicode字符串，最长10
    ('age', 'i4'),        # 4字节整数
    ('height', 'f4'),     # 4字节浮点
    ('score', 'f8')       # 8字节浮点
])

# 创建结构化数组
students = np.array([
    ('Alice', 20, 165.5, 90.5),
    ('Bob', 22, 180.0, 85.0),
    ('Charlie', 21, 175.0, 92.5)
], dtype=dt)

print("结构化数组:")
print(students)

# 访问字段
print(f"\n所有姓名: {students['name']}")
print(f"所有年龄: {students['age']}")

# 条件筛选
print(f"\n年龄>=21的学生: {students[students['age'] >= 21]['name']}")

# 计算统计量
print(f"\n平均身高: {students['height'].mean():.2f}")
print(f"平均成绩: {students['score'].mean():.2f}")
```

### 6.3 内存映射文件

```python
import numpy as np
import os

# 创建大型数组并保存
filename = 'large_array.npy'
if not os.path.exists(filename):
    large_array = np.random.rand(10000, 10000)  # 约800MB
    np.save(filename, large_array)

# 使用内存映射读取（不全部加载到内存）
mmap_arr = np.load(filename, mmap_mode='r')
print(f"内存映射数组形状: {mmap_arr.shape}")
print(f"访问部分数据: {mmap_arr[0:5, 0:5]}")

# 清理
os.remove(filename)
```

---

## 七、深度学习中的应用

### 7.1 手动实现前向传播

```python
import numpy as np

def sigmoid(x):
    """Sigmoid激活函数"""
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

def relu(x):
    """ReLU激活函数"""
    return np.maximum(0, x)

def softmax(x):
    """Softmax函数"""
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

# 简单的两层神经网络
class SimpleNN:
    def __init__(self, input_size, hidden_size, output_size):
        # Xavier初始化
        self.W1 = np.random.randn(input_size, hidden_size) * np.sqrt(2 / input_size)
        self.b1 = np.zeros(hidden_size)
        self.W2 = np.random.randn(hidden_size, output_size) * np.sqrt(2 / hidden_size)
        self.b2 = np.zeros(output_size)
    
    def forward(self, X):
        # 第一层
        self.z1 = X @ self.W1 + self.b1
        self.a1 = relu(self.z1)
        
        # 第二层
        self.z2 = self.a1 @ self.W2 + self.b2
        self.a2 = softmax(self.z2)
        
        return self.a2
    
    def predict(self, X):
        probs = self.forward(X)
        return np.argmax(probs, axis=1)

# 测试
nn = SimpleNN(input_size=784, hidden_size=128, output_size=10)
X = np.random.randn(32, 784)  # batch_size=32
output = nn.forward(X)
print(f"输出形状: {output.shape}")
print(f"输出概率和: {output.sum(axis=1)}")  # 应该全为1
```

### 7.2 手动实现反向传播

```python
import numpy as np

def sigmoid_derivative(x):
    """Sigmoid的导数"""
    s = 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    return s * (1 - s)

def relu_derivative(x):
    """ReLU的导数"""
    return (x > 0).astype(float)

class NeuralNetwork:
    def __init__(self, layer_sizes):
        self.weights = []
        self.biases = []
        
        # 初始化权重
        for i in range(len(layer_sizes) - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * 0.01
            b = np.zeros((1, layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)
    
    def forward(self, X):
        """前向传播，保存中间结果"""
        self.activations = [X]
        self.z_values = []
        
        current = X
        for w, b in zip(self.weights, self.biases):
            z = current @ w + b
            self.z_values.append(z)
            current = sigmoid(z)
            self.activations.append(current)
        
        return current
    
    def backward(self, X, y, learning_rate=0.1):
        """反向传播"""
        m = X.shape[0]
        
        # 输出层误差
        delta = self.activations[-1] - y
        
        # 从后向前计算梯度
        for i in range(len(self.weights) - 1, -1, -1):
            # 计算梯度
            dW = self.activations[i].T @ delta / m
            db = np.sum(delta, axis=0, keepdims=True) / m
            
            # 更新参数
            self.weights[i] -= learning_rate * dW
            self.biases[i] -= learning_rate * db
            
            # 传播误差到前一层
            if i > 0:
                delta = (delta @ self.weights[i].T) * sigmoid_derivative(self.z_values[i-1])

# 训练示例（异或问题）
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

nn = NeuralNetwork([2, 4, 1])

# 训练
for epoch in range(10000):
    output = nn.forward(X)
    nn.backward(X, y, learning_rate=1.0)
    
    if epoch % 2000 == 0:
        loss = np.mean((output - y) ** 2)
        print(f"Epoch {epoch}, Loss: {loss:.6f}")

# 预测
print("\n预测结果:")
for x, target in zip(X, y):
    pred = nn.forward(x.reshape(1, -1))
    print(f"{x} -> {pred[0, 0]:.4f} (目标: {target[0]})")
```

---

## 八、实战案例

### 8.1 PCA 实现

```python
import numpy as np

def pca(X, n_components):
    """
    主成分分析
    X: (n_samples, n_features)
    """
    # 标准化
    X_centered = X - np.mean(X, axis=0)
    
    # 计算协方差矩阵
    cov_matrix = np.cov(X_centered.T)
    
    # 特征值分解
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    
    # 按特征值降序排列
    idx = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    
    # 选择前n_components个主成分
    components = eigenvectors[:, :n_components]
    
    # 投影
    X_transformed = X_centered @ components
    
    # 解释方差比例
    explained_variance = eigenvalues[:n_components] / np.sum(eigenvalues)
    
    return X_transformed, components, explained_variance

# 测试
np.random.seed(42)
X = np.random.randn(100, 10)  # 100样本，10维

X_pca, components, explained_var = pca(X, n_components=3)
print(f"降维后形状: {X_pca.shape}")
print(f"解释方差比例: {explained_var}")
print(f"累计解释方差: {np.cumsum(explained_var)}")
```

### 8.2 K-Means 实现

```python
import numpy as np

def kmeans(X, k, max_iters=100, random_state=42):
    """
    K-Means聚类
    X: (n_samples, n_features)
    k: 聚类数量
    """
    np.random.seed(random_state)
    n_samples = X.shape[0]
    
    # 随机初始化中心点
    indices = np.random.choice(n_samples, k, replace=False)
    centroids = X[indices].copy()
    
    for _ in range(max_iters):
        # 计算距离矩阵
        distances = np.sqrt(((X[:, np.newaxis] - centroids) ** 2).sum(axis=2))
        
        # 分配到最近的中心
        labels = np.argmin(distances, axis=1)
        
        # 更新中心点
        new_centroids = np.array([X[labels == i].mean(axis=0) for i in range(k)])
        
        # 检查收敛
        if np.allclose(centroids, new_centroids):
            break
        
        centroids = new_centroids
    
    return labels, centroids

# 测试
np.random.seed(42)
# 生成3个簇的数据
cluster1 = np.random.randn(100, 2) + np.array([0, 0])
cluster2 = np.random.randn(100, 2) + np.array([5, 5])
cluster3 = np.random.randn(100, 2) + np.array([5, 0])
X = np.vstack([cluster1, cluster2, cluster3])

labels, centroids = kmeans(X, k=3)
print(f"聚类中心:\n{centroids}")
print(f"每个簇的样本数: {[np.sum(labels == i) for i in range(3)]}")
```

---

## 总结

| 知识点 | 核心要点 |
|--------|----------|
| 线性代数 | 点积、矩阵乘法、转置、范数 |
| 矩阵分解 | 特征值分解、SVD、QR、Cholesky |
| 方程求解 | `solve()`, `lstsq()`, 伪逆 |
| 高级操作 | 排序、搜索、集合操作、结构化数组 |
| 深度学习 | 手动实现前向/反向传播 |

---

**上一篇**：[NumPy 基础教程]({{ site.baseurl }}{% post_url /ailearn/01-numpy-pandas/2026-04-12-numpy-basic %})

**下一篇**：[Pandas 基础教程 - 数据分析入门]({{ site.baseurl }}{% post_url /ailearn/01-numpy-pandas/2026-04-12-pandas-basic %})

**返回**：[AI学习路线总览]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-01-ai-foundation %})

*最后更新: 2026年4月12日*

> 参考资源：
> - [NumPy线性代数文档](https://numpy.org/doc/stable/reference/routines.linalg.html) - 官方线性代数参考
> - [3Blue1Brown线性代数系列](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab) - 可视化线性代数
> - [MIT 18.06 线性代数](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/) - Gilbert Strang经典课程
> - [线性代数的本质(B站)](https://www.bilibili.com/video/BV1ib411t7YR) - 3Blue1Brown中字版
> - [Khan Academy线性代数](https://www.khanacademy.org/math/linear-algebra) - 可汗学院教程
> - [Interactive Linear Algebra](http://textbooks.math.gatech.edu/ila/) - 交互式线性代数教材
> - [Deep Learning Book - Linear Algebra](https://www.deeplearningbook.org/contents/linear_algebra.html) - 深度学习中的线性代数
> - [Eigenvectors and Eigenvalues可视化](https://setosa.io/ev/eigenvectors-and-eigenvalues/) - 特征向量可视化
> - [SVD可视化教程](http://setosa.io/ev/principal-component-analysis/) - PCA与SVD可视化
> - [线性代数 Cheat Sheet](https://medium.com/@adityam.rv/linear-algebra-cheat-sheet-2b5a5072f8e0) - 线性代数速查表
