实现---
layout: post
title: "NumPy 基础教程 - Python 数值计算基石"
date: 2026-04-12
categories: ailearn
tags: [AI, Python, NumPy, 数值计算]
keywords: NumPy, 数组操作, 数值计算, Python科学计算
description: 深入学习 NumPy 基础操作，掌握数组创建、索引切片、形状变换等核心技能
---

* content
{:toc}

> **前置知识**：本文是 AI 学习路线的扩展教程，需要先掌握 [Python 基础语法]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-01-ai-foundation %})。
>
> **本文重点**：理解 NumPy 数组的核心概念，掌握基础操作，为机器学习打下基础。

NumPy（Numerical Python）是 Python 科学计算的核心库，几乎所有 AI/ML 框架（TensorFlow、PyTorch、scikit-learn）都基于 NumPy 构建。本文将系统讲解 NumPy 的核心用法。

---

## 一、NumPy 简介

### 1.1 为什么需要 NumPy？

Python 原生列表在处理大规模数值计算时存在性能瓶颈：

```python
# 原生列表计算 100 万个元素的平方
import time

# 方法1：Python 原生列表（慢）
start = time.time()
python_list = list(range(1_000_000))
result = [x ** 2 for x in python_list]
print(f"Python列表耗时: {time.time() - start:.4f}秒")

# 方法2：NumPy 数组（快 50-100 倍）
import numpy as np
start = time.time()
numpy_array = np.arange(1_000_000)
result = numpy_array ** 2
print(f"NumPy数组耗时: {time.time() - start:.4f}秒")
```

**NumPy 的优势**：
- **性能**：底层 C 实现，比 Python 快 50-100 倍
- **内存**：连续存储，内存占用更小
- **向量化**：无需循环即可批量操作
- **生态**：Pandas、Matplotlib、scikit-learn 的基础

### 1.2 安装与导入

```bash
# 安装
pip install numpy

# 升级
pip install --upgrade numpy
```

```python
import numpy as np

# 查看版本
print(np.__version__)  # 如: 1.26.4
```

---

## 二、数组创建

### 2.1 从列表/元组创建

```python
import numpy as np

# 一维数组
arr1d = np.array([1, 2, 3, 4, 5])
print(arr1d)        # [1 2 3 4 5]
print(arr1d.dtype)  # int64
print(arr1d.shape)  # (5,)

# 二维数组
arr2d = np.array([[1, 2, 3], 
                   [4, 5, 6]])
print(arr2d)
# [[1 2 3]
#  [4 5 6]]
print(arr2d.shape)  # (2, 3) - 2行3列
print(arr2d.ndim)   # 2 - 维度

# 三维数组（如图像数据）
arr3d = np.array([[[1, 2], [3, 4]], 
                   [[5, 6], [7, 8]]])
print(arr3d.shape)  # (2, 2, 2)

# 指定数据类型
arr_float = np.array([1, 2, 3], dtype=np.float32)
print(arr_float.dtype)  # float32

arr_complex = np.array([1, 2, 3], dtype=np.complex128)
print(arr_complex)  # [1.+0.j 2.+0.j 3.+0.j]
```

### 2.2 使用内置函数创建

```python
import numpy as np

# ===== 零与一 =====
# 全零数组
zeros = np.zeros((3, 4))  # 3行4列的全零矩阵
print(zeros)
# [[0. 0. 0. 0.]
#  [0. 0. 0. 0.]
#  [0. 0. 0. 0.]]

# 全一数组
ones = np.ones((2, 3))
print(ones)
# [[1. 1. 1.]
#  [1. 1. 1.]]

# 指定填充值
full = np.full((2, 3), fill_value=7)
print(full)
# [[7 7 7]
#  [7 7 7]]

# ===== 单位矩阵 =====
identity = np.eye(4)  # 4x4 单位矩阵
print(identity)
# [[1. 0. 0. 0.]
#  [0. 1. 0. 0.]
#  [0. 0. 1. 0.]
#  [0. 0. 0. 1.]]

# ===== 序列数组 =====
# arange - 类似 range
seq1 = np.arange(0, 10, 2)      # [0, 2, 4, 6, 8]
seq2 = np.arange(10)             # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# linspace - 线性等分
linear = np.linspace(0, 1, 5)    # [0., 0.25, 0.5, 0.75, 1.]
print(f"等分点: {linear}")

# logspace - 对数等分
log_spaced = np.logspace(0, 2, 5)  # 10^0 到 10^2 分5个点
print(f"对数等分: {log_spaced}")

# ===== 随机数组 =====
# 均匀分布 [0, 1)
rand_uniform = np.random.rand(2, 3)  # 2行3列
print("均匀分布随机数:\n", rand_uniform)

# 正态分布
rand_normal = np.random.randn(2, 3)  # 均值0，标准差1
print("正态分布随机数:\n", rand_normal)

# 指定范围的随机整数
rand_int = np.random.randint(0, 100, size=(2, 3))
print("随机整数:\n", rand_int)

# 设置随机种子（确保可复现）
np.random.seed(42)
rand_seeded = np.random.rand(3)
print("固定种子随机数:", rand_seeded)
```

### 2.3 数组属性

```python
import numpy as np

arr = np.array([[1, 2, 3, 4], 
                [5, 6, 7, 8]])

print(f"形状 shape: {arr.shape}")      # (2, 4) - 各维度大小
print(f"维度 ndim: {arr.ndim}")        # 2 - 维度数量
print(f"元素数 size: {arr.size}")      # 8 - 总元素数
print(f"数据类型 dtype: {arr.dtype}")  # int64
print(f"每个元素字节 itemsize: {arr.itemsize}")  # 8
print(f"总字节数 nbytes: {arr.nbytes}")          # 64 (8 * 8)
```

---

## 三、索引与切片

### 3.1 基础索引

```python
import numpy as np

arr = np.array([[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]])

# 一维索引
print(arr[0])         # [1 2 3 4] - 第一行
print(arr[-1])        # [9 10 11 12] - 最后一行

# 二维索引 [行, 列]
print(arr[0, 0])      # 1 - 第一行第一列
print(arr[1, 2])      # 7 - 第二行第三列
print(arr[-1, -1])    # 12 - 最后一行最后一列

# 修改元素
arr[0, 0] = 100
print(arr[0, 0])      # 100
```

### 3.2 切片操作

```python
import numpy as np

arr = np.array([[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]])

# 语法: arr[start:stop:step]

# 行切片
print(arr[0:2])       # 前两行
# [[1 2 3 4]
#  [5 6 7 8]]

# 列切片
print(arr[:, 0:2])    # 所有行，前两列
# [[ 1  2]
#  [ 5  6]
#  [ 9 10]]

# 组合切片
print(arr[0:2, 1:3])  # 前两行，第2-3列
# [[2 3]
#  [6 7]]

# 步长切片
print(arr[::2, ::2])  # 隔行隔列
# [[ 1  3]
#  [ 9 11]]

# 反转
print(arr[::-1])      # 行反转
# [[ 9 10 11 12]
#  [ 5  6  7  8]
#  [ 1  2  3  4]]
```

### 3.3 高级索引

```python
import numpy as np

arr = np.array([[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]])

# ===== 整数数组索引 =====
# 选择特定行
rows = np.array([0, 2])
print(arr[rows])
# [[ 1  2  3  4]
#  [ 9 10 11 12]]

# 选择特定位置的元素
rows = np.array([0, 1, 2])
cols = np.array([1, 2, 3])
print(arr[rows, cols])  # [ 2  7 12] - (0,1), (1,2), (2,3)

# ===== 布尔索引 =====
# 条件筛选
print(arr[arr > 5])    # [ 6  7  8  9 10 11 12]

# 组合条件
mask = (arr > 5) & (arr < 10)
print(arr[mask])       # [6 7 8 9]

# 使用布尔数组修改
arr_copy = arr.copy()
arr_copy[arr_copy > 5] = 0
print(arr_copy)
# [[1 2 3 4]
#  [5 0 0 0]
#  [0 0 0 0]]

# ===== 花式索引 =====
# 选择不连续的行
fancy_rows = [0, 2, 0]  # 选择第0行、第2行、第0行
print(arr[fancy_rows])

# 选择特定矩形区域
print(arr[np.ix_([0, 2], [1, 3])])
# [[ 2  4]
#  [10 12]]
```

---

## 四、形状变换

### 4.1 reshape 与 resize

```python
import numpy as np

arr = np.arange(12)  # [0, 1, 2, ..., 11]

# reshape - 返回新数组，不修改原数组
reshaped = arr.reshape(3, 4)
print(reshaped)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# 使用 -1 自动推断维度
auto_reshaped = arr.reshape(3, -1)  # 自动计算列数
auto_reshaped2 = arr.reshape(-1, 4)  # 自动计算行数

# 展平
flattened = reshaped.reshape(-1)  # 或 reshaped.flatten()
print(flattened)  # [ 0  1  2  3  4  5  6  7  8  9 10 11]

# resize - 直接修改原数组
arr_resize = np.arange(12)
arr_resize.resize(2, 6)
print(arr_resize)
# [[ 0  1  2  3  4  5]
#  [ 6  7  8  9 10 11]]
```

### 4.2 转置与轴交换

```python
import numpy as np

arr = np.arange(12).reshape(3, 4)
print("原数组:\n", arr)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# 转置
print("转置后:\n", arr.T)
# [[ 0  4  8]
#  [ 1  5  9]
#  [ 2  6 10]
#  [ 3  7 11]]

# transpose 方法
print("transpose:\n", np.transpose(arr))

# 高维数组的轴交换
arr3d = np.arange(24).reshape(2, 3, 4)
print(f"原形状: {arr3d.shape}")  # (2, 3, 4)

# 交换轴 0 和 2
swapped = arr3d.transpose(2, 1, 0)
print(f"交换后: {swapped.shape}")  # (4, 3, 2)

# swapaxes - 交换两个轴
swapped_axes = arr3d.swapaxes(0, 2)
print(f"swapaxes后: {swapped_axes.shape}")  # (4, 3, 2)
```

### 4.3 数组合并与分割

```python
import numpy as np

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

# ===== 合并 =====
# 垂直合并（沿行方向）
vstack = np.vstack((a, b))
print("vstack:\n", vstack)
# [[1 2]
#  [3 4]
#  [5 6]
#  [7 8]]

# 水平合并（沿列方向）
hstack = np.hstack((a, b))
print("hstack:\n", hstack)
# [[1 2 5 6]
#  [3 4 7 8]]

# concatenate - 指定轴合并
concat_0 = np.concatenate((a, b), axis=0)  # 同 vstack
concat_1 = np.concatenate((a, b), axis=1)  # 同 hstack

# stack - 创建新维度
stacked = np.stack((a, b), axis=0)
print(f"stack形状: {stacked.shape}")  # (2, 2, 2)

# ===== 分割 =====
arr = np.arange(12).reshape(3, 4)
print("原数组:\n", arr)

# 垂直分割
vsplit = np.vsplit(arr, 3)  # 分成3份
print("vsplit:", [x.tolist() for x in vsplit])

# 水平分割
hsplit = np.hsplit(arr, 2)  # 分成2份
print("hsplit:", [x.tolist() for x in hsplit])

# array_split - 不等分
arr2 = np.arange(10)
split_result = np.array_split(arr2, 3)  # 10个元素分3份
print("不等分:", [x.tolist() for x in split_result])
# [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9]]
```

---

## 五、广播机制

广播是 NumPy 处理不同形状数组运算的机制。

### 5.1 广播规则

```python
import numpy as np

# 规则：从右向左比较维度
# 1. 维度相等
# 2. 其中一个维度为 1
# 3. 其中一个数组没有该维度

# 案例1：数组与标量
arr = np.array([1, 2, 3])
result = arr + 10  # 标量广播到 [10, 10, 10]
print(result)  # [11 12 13]

# 案例2：不同形状数组
a = np.array([[1, 2, 3],
              [4, 5, 6]])  # shape (2, 3)
b = np.array([10, 20, 30])  # shape (3,)

# b 广播为 [[10, 20, 30],
#          [10, 20, 30]]
print(a + b)
# [[11 22 33]
#  [14 25 36]]

# 案例3：列向量广播
c = np.array([[1], [2]])  # shape (2, 1)
# c 广播为 [[1, 1, 1],
#          [2, 2, 2]]
print(a + c)
# [[2 3 4]
#  [6 7 8]]

# 案例4：广播失败
try:
    d = np.array([1, 2])  # shape (2,)
    print(a + d)  # (2,3) + (2,) 无法广播
except ValueError as e:
    print(f"广播失败: {e}")
```

### 5.2 广播应用实例

```python
import numpy as np

# 归一化数据
data = np.random.rand(100, 5)  # 100个样本，5个特征

# 方法1：使用广播
mean = data.mean(axis=0)  # shape (5,)
std = data.std(axis=0)    # shape (5,)
normalized = (data - mean) / std

# 计算距离矩阵
points = np.random.rand(10, 3)  # 10个3D点
# 点i到点j的距离
# |points| = (10, 1, 3)
# |points| = (1, 10, 3)
# 广播后差值 = (10, 10, 3)
diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
distances = np.sqrt(np.sum(diff ** 2, axis=2))
print(f"距离矩阵形状: {distances.shape}")  # (10, 10)
```

---

## 六、通用函数

### 6.1 数学运算

```python
import numpy as np

arr = np.array([1, 4, 9, 16, 25])

# 基本运算
print(np.sqrt(arr))    # [1. 2. 3. 4. 5.] - 平方根
print(np.exp(arr))     # e^x
print(np.log(arr))     # 自然对数
print(np.log10(arr))   # 以10为底的对数
print(np.log2(arr))    # 以2为底的对数

# 三角函数
angles = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])
print(np.sin(angles))
print(np.cos(angles))
print(np.tan(angles))

# 反三角函数
values = np.array([0, 0.5, 1])
print(np.arcsin(values))
print(np.arccos(values))
print(np.arctan(values))

# 取整函数
floats = np.array([-2.5, -1.7, -0.2, 0, 0.3, 1.5, 2.8])
print(f"floor: {np.floor(floats)}")   # 向下取整
print(f"ceil: {np.ceil(floats)}")     # 向上取整
print(f"round: {np.round(floats)}")   # 四舍五入
print(f"trunc: {np.trunc(floats)}")   # 截断

# 绝对值与符号
print(np.abs([-3, -2, -1, 0, 1, 2, 3]))
print(np.sign([-3, -2, -1, 0, 1, 2, 3]))  # [-1 -1 -1  0  1  1  1]
```

### 6.2 聚合函数

```python
import numpy as np

arr = np.random.randint(0, 100, size=(3, 4))
print("数组:\n", arr)

# 基本统计
print(f"求和: {np.sum(arr)}")
print(f"均值: {np.mean(arr)}")
print(f"中位数: {np.median(arr)}")
print(f"标准差: {np.std(arr)}")
print(f"方差: {np.var(arr)}")
print(f"最大值: {np.max(arr)}")
print(f"最小值: {np.min(arr)}")

# 沿轴聚合
print(f"每列求和: {np.sum(arr, axis=0)}")   # shape (4,)
print(f"每行求和: {np.sum(arr, axis=1)}")   # shape (3,)

# argmax/argmin - 返回索引
print(f"最大值索引: {np.argmax(arr)}")
print(f"每行最大值索引: {np.argmax(arr, axis=1)}")

# 累积运算
print(f"累积和: {np.cumsum(arr)}")
print(f"累积积: {np.cumprod(arr)}")

# 百分位数
data = np.random.randn(1000)
print(f"25%分位数: {np.percentile(data, 25)}")
print(f"中位数: {np.percentile(data, 50)}")
print(f"75%分位数: {np.percentile(data, 75)}")
```

### 6.3 条件函数

```python
import numpy as np

arr = np.array([-3, -1, 0, 1, 3])

# where - 条件选择
result = np.where(arr > 0, "正数", "非正数")
print(result)  # ['非正数' '非正数' '非正数' '正数' '正数']

# 多条件
arr2d = np.random.randint(-10, 10, size=(3, 3))
print("原数组:\n", arr2d)
result = np.where(arr2d > 0, arr2d, 0)  # 负数置零
print("负数置零:\n", result)

# select - 多条件选择
conditions = [
    arr < -1,
    (arr >= -1) & (arr <= 1),
    arr > 1
]
choices = ["小", "中", "大"]
result = np.select(conditions, choices)
print(result)  # ['小' '中' '中' '中' '大']

# clip - 裁剪到范围
clipped = np.clip(arr, -2, 2)
print(clipped)  # [-2 -1  0  1  2]
```

---

## 七、实战案例

### 7.1 图像处理基础

```python
import numpy as np
from PIL import Image

# 创建模拟图像数据 (100x100 RGB)
image = np.random.randint(0, 256, size=(100, 100, 3), dtype=np.uint8)

# 转换为灰度图
gray = np.mean(image, axis=2).astype(np.uint8)

# 调整亮度
brightened = np.clip(image.astype(np.int16) + 50, 0, 255).astype(np.uint8)

# 翻转
flipped_h = image[:, ::-1, :]  # 水平翻转
flipped_v = image[::-1, :, :]  # 垂直翻转

# 裁剪
cropped = image[10:90, 10:90, :]

print(f"原图形状: {image.shape}")
print(f"灰度图形状: {gray.shape}")
```

### 7.2 数据预处理

```python
import numpy as np

# 生成模拟数据
np.random.seed(42)
data = np.random.randn(1000, 5)  # 1000个样本，5个特征

# 标准化 (Z-Score)
def standardize(X):
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    return (X - mean) / std

standardized = standardize(data)
print(f"标准化后均值: {standardized.mean(axis=0)}")  # 接近0
print(f"标准化后标准差: {standardized.std(axis=0)}")  # 接近1

# Min-Max 归一化
def min_max_normalize(X):
    min_val = np.min(X, axis=0)
    max_val = np.max(X, axis=0)
    return (X - min_val) / (max_val - min_val)

normalized = min_max_normalize(data)
print(f"归一化后范围: [{normalized.min()}, {normalized.max()}]")

# 处理缺失值
data_with_nan = data.copy()
data_with_nan[np.random.rand(*data.shape) < 0.05] = np.nan  # 5%缺失

# 用均值填充
col_means = np.nanmean(data_with_nan, axis=0)
nan_indices = np.where(np.isnan(data_with_nan))
data_filled = data_with_nan.copy()
data_filled[nan_indices] = np.take(col_means, nan_indices[1])
```

---

## 八、性能优化技巧

```python
import numpy as np
import time

# ===== 向量化 vs 循环 =====
# 错误示范
def slow_sigmoid(x):
    result = np.zeros_like(x)
    for i in range(len(x)):
        result[i] = 1 / (1 + np.exp(-x[i]))
    return result

# 正确示范
def fast_sigmoid(x):
    return 1 / (1 + np.exp(-x))

x = np.random.randn(100000)

start = time.time()
slow_result = slow_sigmoid(x)
slow_time = time.time() - start

start = time.time()
fast_result = fast_sigmoid(x)
fast_time = time.time() - start

print(f"循环耗时: {slow_time:.4f}秒")
print(f"向量化耗时: {fast_time:.4f}秒")
print(f"加速比: {slow_time/fast_time:.1f}倍")

# ===== 内存布局 =====
# C顺序（行优先） vs F顺序（列优先）
arr_c = np.zeros((1000, 1000), order='C')  # 适合行操作
arr_f = np.zeros((1000, 1000), order='F')  # 适合列操作

# 检查内存布局
print(f"C顺序连续: {arr_c.flags['C_CONTIGUOUS']}")  # True
print(f"F顺序连续: {arr_f.flags['F_CONTIGUOUS']}")  # True
```

---

## 总结

| 知识点 | 核心要点 |
|--------|----------|
| 数组创建 | `np.array()`, `zeros()`, `ones()`, `arange()`, `linspace()` |
| 索引切片 | 基础索引、切片、布尔索引、花式索引 |
| 形状变换 | `reshape()`, `T`, `transpose()`, `vstack()`, `hstack()` |
| 广播机制 | 从右向左比较，维度相等或为1即可广播 |
| 通用函数 | `sqrt()`, `exp()`, `sin()`, `sum()`, `mean()`, `where()` |

---

**下一篇**：[NumPy 进阶教程 - 线性代数与高级操作]({{ site.baseurl }}{% post_url /ailearn/01-numpy-pandas/2026-04-12-numpy-advanced %})

**返回**：[AI学习路线总览]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-01-ai-foundation %})

*最后更新: 2026年4月12日*

> 参考资源：
> - [NumPy官方文档](https://numpy.org/doc/stable/user/quickstart.html) - 快速入门指南
> - [NumPy官方用户指南](https://numpy.org/doc/stable/user/index.html) - 完整用户手册
> - [NumPy中文教程](https://www.runoob.com/numpy/numpy-tutorial.html) - 菜鸟教程
> - [SciPy Lecture Notes](https://scipy-lectures.org/intro/numpy/index.html) - SciPy社区教程
> - [NumPy Illustrated Guide](https://betterprogramming.pub/numpy-illustrated-the-visual-guide-to-numpy-3b1d4976de1f) - 可视化NumPy指南
> - [From Python to Numpy](https://www.labri.fr/perso/nrougier/from-python-to-numpy/) - Python到NumPy进阶
> - [100 NumPy Exercises](https://github.com/rougier/numpy-100) - 100道NumPy练习题
