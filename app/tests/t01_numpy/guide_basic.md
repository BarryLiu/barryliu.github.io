# NumPy 常用函数参考

本文档列出了NumPy中最常用的函数及其作用，适用于AI应用开发。

## 数组创建

### 基础创建

| 函数 | 作用 | 示例 |
|------|------|------|
| `np.array()` | 从列表/数组创建ndarray | `np.array([1, 2, 3])` |
| `np.zeros()` | 创建全零数组 | `np.zeros((3, 4))` |
| `np.ones()` | 创建全1数组 | `np.ones((3, 4))` |
| `np.empty()` | 创建未初始化的数组 | `np.empty((3, 4))` |
| `np.full()` | 创建填充指定值的数组 | `np.full((3, 4), 5)` |
| `np.arange()` | 创建等差数组 | `np.arange(0, 10, 2)` |
| `np.linspace()` | 创建等间隔数组 | `np.linspace(0, 1, 5)` |
| `np.random.rand()` | 创建[0,1)随机数组 | `np.random.rand(3, 4)` |
| `np.random.randn()` | 创建标准正态分布数组 | `np.random.randn(3, 4)` |
| `np.random.randint()` | 创建随机整数数组 | `np.random.randint(0, 10, (3, 4))` |

## 数组属性

| 函数/属性 | 作用 | 示例 |
|-----------|------|------|
| `.shape` | 数组形状 | `arr.shape` |
| `.dtype` | 数据类型 | `arr.dtype` |
| `.size` | 元素总数 | `arr.size` |
| `.ndim` | 数组维度 | `arr.ndim` |
| `.itemsize` | 每个元素字节数 | `arr.itemsize` |
| `np.shape()` | 获取形状 | `np.shape(arr)` |
| `np.size()` | 获取大小 | `np.size(arr)` |

## 数组操作

### 索引和切片

| 操作 | 作用 | 示例 |
|------|------|------|
| `arr[i]` | 索引单个元素 | `arr[0]` |
| `arr[i:j]` | 切片 | `arr[1:5]` |
| `arr[i:j:k]` | 步长切片 | `arr[::2]` |
| `arr[i, j]` | 多维索引 | `arr[0, 1]` |
| `arr[:, j]` | 选择列 | `arr[:, 1]` |
| `arr[i, :]` | 选择行 | `arr[1, :]` |
| `arr[condition]` | 布尔索引 | `arr[arr > 5]` |

### 形状操作

| 函数 | 作用 | 示例 |
|------|------|------|
| `.reshape()` | 改变数组形状 | `arr.reshape(3, 4)` |
| `.flatten()` | 展平数组 | `arr.flatten()` |
| `.ravel()` | 返回展平视图 | `arr.ravel()` |
| `.transpose()` | 转置 | `arr.transpose()` |
| `.T` | 转置（属性） | `arr.T` |
| `np.reshape()` | 改变形状 | `np.reshape(arr, (3, 4))` |
| `np.expand_dims()` | 增加维度 | `np.expand_dims(arr, axis=0)` |
| `np.squeeze()` | 移除单维度 | `np.squeeze(arr)` |

### 数组连接

| 函数 | 作用 | 示例 |
|------|------|------|
| `np.concatenate()` | 连接数组 | `np.concatenate([a, b])` |
| `np.stack()` | 堆叠数组 | `np.stack([a, b])` |
| `np.hstack()` | 水平堆叠 | `np.hstack([a, b])` |
| `np.vstack()` | 垂直堆叠 | `np.vstack([a, b])` |
| `np.column_stack()` | 列堆叠 | `np.column_stack([a, b])` |

## 数学运算

### 基本运算

| 函数 | 作用 | 示例 |
|------|------|------|
| `np.add()` | 加法 | `np.add(a, b)` |
| `np.subtract()` | 减法 | `np.subtract(a, b)` |
| `np.multiply()` | 乘法 | `np.multiply(a, b)` |
| `np.divide()` | 除法 | `np.divide(a, b)` |
| `np.power()` | 幂运算 | `np.power(a, 2)` |
| `np.sqrt()` | 平方根 | `np.sqrt(arr)` |
| `np.abs()` | 绝对值 | `np.abs(arr)` |
| `np.sign()` | 符号函数 | `np.sign(arr)` |

### 三角函数

| 函数 | 作用 | 示例 |
|------|------|------|
| `np.sin()` | 正弦 | `np.sin(arr)` |
| `np.cos()` | 余弦 | `np.cos(arr)` |
| `np.tan()` | 正切 | `np.tan(arr)` |
| `np.arcsin()` | 反正弦 | `np.arcsin(arr)` |
| `np.arccos()` | 反余弦 | `np.arccos(arr)` |
| `np.arctan()` | 反正切 | `np.arctan(arr)` |

### 指数和对数

| 函数 | 作用 | 示例 |
|------|------|------|
| `np.exp()` | 自然指数 | `np.exp(arr)` |
| `np.log()` | 自然对数 | `np.log(arr)` |
| `np.log10()` | 常用对数 | `np.log10(arr)` |
| `np.log2()` | 以2为底对数 | `np.log2(arr)` |

## 统计函数

### 聚合函数

| 函数 | 作用 | 示例 |
|------|------|------|
| `np.sum()` | 求和 | `np.sum(arr)` |
| `np.mean()` | 平均值 | `np.mean(arr)` |
| `np.median()` | 中位数 | `np.median(arr)` |
| `np.std()` | 标准差 | `np.std(arr)` |
| `np.var()` | 方差 | `np.var(arr)` |
| `np.min()` | 最小值 | `np.min(arr)` |
| `np.max()` | 最大值 | `np.max(arr)` |
| `np.argmin()` | 最小值索引 | `np.argmin(arr)` |
| `np.argmax()` | 最大值索引 | `np.argmax(arr)` |
| `np.percentile()` | 百分位数 | `np.percentile(arr, 50)` |

### 按轴聚合

| 函数 | 作用 | 示例 |
|------|------|------|
| `np.sum(axis=0)` | 按列求和 | `np.sum(arr, axis=0)` |
| `np.sum(axis=1)` | 按行求和 | `np.sum(arr, axis=1)` |
| `np.mean(axis=0)` | 按列求平均 | `np.mean(arr, axis=0)` |
| `np.mean(axis=1)` | 按行求平均 | `np.mean(arr, axis=1)` |

## 线性代数（AI应用核心）

### 向量运算

| 函数 | 作用 | 示例 |
|------|------|------|
| `np.dot()` | 点积/矩阵乘法 | `np.dot(a, b)` |
| `np.vdot()` | 向量点积 | `np.vdot(a, b)` |
| `np.inner()` | 内积 | `np.inner(a, b)` |
| `np.outer()` | 外积 | `np.outer(a, b)` |
| `np.cross()` | 叉积 | `np.cross(a, b)` |

### 矩阵运算

| 函数 | 作用 | 示例 |
|------|------|------|
| `np.matmul()` | 矩阵乘法 | `np.matmul(A, B)` |
| `@` | 矩阵乘法运算符 | `A @ B` |
| `np.linalg.inv()` | 矩阵求逆 | `np.linalg.inv(A)` |
| `np.linalg.pinv()` | 伪逆矩阵 | `np.linalg.pinv(A)` |
| `np.linalg.det()` | 行列式 | `np.linalg.det(A)` |
| `np.linalg.eig()` | 特征值和特征向量 | `np.linalg.eig(A)` |
| `np.linalg.solve()` | 解线性方程组 | `np.linalg.solve(A, b)` |

### 向量范数（重要）

| 函数 | 作用 | 示例 |
|------|------|------|
| `np.linalg.norm()` | 向量/矩阵范数 | `np.linalg.norm(vec)` |
| `np.linalg.norm(ord=1)` | L1范数 | `np.linalg.norm(vec, ord=1)` |
| `np.linalg.norm(ord=2)` | L2范数（默认） | `np.linalg.norm(vec, ord=2)` |
| `np.linalg.norm(ord=np.inf)` | 无穷范数 | `np.linalg.norm(vec, ord=np.inf)` |

## 相似度计算（AI应用最常用）

### 余弦相似度

```python
def cosine_similarity(vec1, vec2):
    """计算两个向量的余弦相似度"""
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)
```

### 欧氏距离

```python
def euclidean_distance(vec1, vec2):
    """计算两个向量的欧氏距离"""
    return np.linalg.norm(vec1 - vec2)
```

### 批量相似度计算

```python
# 归一化所有向量
norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
normalized = embeddings / norms

# 批量计算相似度
similarities = np.dot(normalized, query_normalized)
```

## 数组比较

| 函数 | 作用 | 示例 |
|------|------|------|
| `np.equal()` | 相等比较 | `np.equal(a, b)` |
| `np.not_equal()` | 不等比较 | `np.not_equal(a, b)` |
| `np.greater()` | 大于 | `np.greater(a, b)` |
| `np.greater_equal()` | 大于等于 | `np.greater_equal(a, b)` |
| `np.less()` | 小于 | `np.less(a, b)` |
| `np.less_equal()` | 小于等于 | `np.less_equal(a, b)` |
| `np.all()` | 所有元素为True | `np.all(arr > 0)` |
| `np.any()` | 任一元素为True | `np.any(arr > 0)` |

## 数组搜索和排序

| 函数 | 作用 | 示例 |
|------|------|------|
| `np.where()` | 条件查找 | `np.where(arr > 5)` |
| `np.searchsorted()` | 二分查找 | `np.searchsorted(arr, value)` |
| `np.sort()` | 排序 | `np.sort(arr)` |
| `np.argsort()` | 排序索引 | `np.argsort(arr)` |
| `np.argmax()` | 最大值索引 | `np.argmax(arr)` |
| `np.argmin()` | 最小值索引 | `np.argmin(arr)` |
| `np.unique()` | 唯一值 | `np.unique(arr)` |

## 数组操作

### 条件操作

| 函数 | 作用 | 示例 |
|------|------|------|
| `np.where()` | 条件选择 | `np.where(condition, x, y)` |
| `np.select()` | 多条件选择 | `np.select(conditions, choices)` |
| `np.clip()` | 裁剪到范围 | `np.clip(arr, 0, 1)` |

### 数组分割

| 函数 | 作用 | 示例 |
|------|------|------|
| `np.split()` | 分割数组 | `np.split(arr, 3)` |
| `np.array_split()` | 不等分割 | `np.array_split(arr, 3)` |
| `np.hsplit()` | 水平分割 | `np.hsplit(arr, 3)` |
| `np.vsplit()` | 垂直分割 | `np.vsplit(arr, 3)` |

## 数据类型转换

| 函数 | 作用 | 示例 |
|------|------|------|
| `.astype()` | 类型转换 | `arr.astype(np.float32)` |
| `np.float32` | 32位浮点 | `arr.astype(np.float32)` |
| `np.float64` | 64位浮点 | `arr.astype(np.float64)` |
| `np.int32` | 32位整数 | `arr.astype(np.int32)` |
| `np.int64` | 64位整数 | `arr.astype(np.int64)` |
| `np.bool` | 布尔类型 | `arr.astype(np.bool)` |

## 文件I/O

| 函数 | 作用 | 示例 |
|------|------|------|
| `np.save()` | 保存数组 | `np.save('file.npy', arr)` |
| `np.load()` | 加载数组 | `arr = np.load('file.npy')` |
| `np.savez()` | 保存多个数组 | `np.savez('file.npz', a=a, b=b)` |
| `np.load()` | 加载npz文件 | `data = np.load('file.npz')` |
| `np.savetxt()` | 保存为文本 | `np.savetxt('file.txt', arr)` |
| `np.loadtxt()` | 从文本加载 | `arr = np.loadtxt('file.txt')` |

## 随机数生成

| 函数 | 作用 | 示例 |
|------|------|------|
| `np.random.seed()` | 设置随机种子 | `np.random.seed(42)` |
| `np.random.rand()` | [0,1)均匀分布 | `np.random.rand(3, 4)` |
| `np.random.randn()` | 标准正态分布 | `np.random.randn(3, 4)` |
| `np.random.randint()` | 随机整数 | `np.random.randint(0, 10, (3, 4))` |
| `np.random.choice()` | 随机选择 | `np.random.choice(arr, size=5)` |
| `np.random.shuffle()` | 打乱数组 | `np.random.shuffle(arr)` |
| `np.random.permutation()` | 随机排列 | `np.random.permutation(arr)` |
| `np.random.normal()` | 正态分布 | `np.random.normal(0, 1, (3, 4))` |
| `np.random.uniform()` | 均匀分布 | `np.random.uniform(0, 1, (3, 4))` |

## 实用技巧

### 广播机制

```python
# 数组与标量
arr + 10  # 所有元素加10
arr * 2   # 所有元素乘2

# 不同形状的数组
arr1 = np.array([[1], [2], [3]])  # (3, 1)
arr2 = np.array([10, 20, 30])     # (3,)
arr1 + arr2  # 自动广播
```

### 向量归一化

```python
# L2归一化
norms = np.linalg.norm(vectors, axis=1, keepdims=True)
normalized = vectors / norms

# 按特征归一化（标准化）
mean = np.mean(data, axis=0)
std = np.std(data, axis=0)
normalized = (data - mean) / std
```

### 批量操作

```python
# 批量计算相似度
similarities = np.dot(embeddings_normalized, query_normalized)

# 批量归一化
norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
normalized = embeddings / norms
```

## 性能优化建议

1. **使用向量化操作**：避免Python循环，使用NumPy向量化
2. **预分配数组**：使用`np.zeros()`或`np.empty()`预分配
3. **使用视图而非副本**：`reshape()`返回视图，`flatten()`返回副本
4. **合理使用数据类型**：`float32`比`float64`快且省内存
5. **利用广播**：减少显式循环和复制

## 常用模式

### 相似度搜索模式

```python
# 1. 归一化所有向量
norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
embeddings_norm = embeddings / norms

# 2. 归一化查询向量
query_norm = query / np.linalg.norm(query)

# 3. 批量计算相似度
similarities = np.dot(embeddings_norm, query_norm)

# 4. 找到top-k
top_k = 5
top_indices = np.argsort(similarities)[::-1][:top_k]
```

### 数据预处理模式

```python
# 1. 加载数据
data = np.load('data.npy')

# 2. 归一化
mean = np.mean(data, axis=0)
std = np.std(data, axis=0)
normalized = (data - mean) / (std + 1e-8)

# 3. 处理异常值
clipped = np.clip(normalized, -3, 3)
```

---

**注意**：本文档重点列出AI应用开发中最常用的函数。更多详细信息请参考NumPy官方文档。

