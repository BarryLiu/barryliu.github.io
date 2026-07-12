# NumPy学习包

NumPy是Python科学计算的基础库，也是AI应用开发中**唯一必须学习的"框架"**。

## 为什么学习NumPy？

- ✅ **向量计算**：AI应用的核心（相似度、Embedding操作）
- ✅ **数据处理**：数组操作、矩阵运算
- ✅ **性能优化**：向量化操作比Python循环快得多
- ✅ **基础工具**：几乎所有AI库都依赖NumPy

## 文件说明

### 01_basics.py - 基础操作
- 数组创建
- 数组属性
- 索引和切片
- 基本运算
- 数组重塑

**学习时间**：1-2天

### 02_vector_operations.py - 向量操作（核心）
- 向量基础
- 向量范数
- 点积
- **余弦相似度**（AI应用最常用）
- 欧氏距离
- 批量相似度计算
- Embedding操作

**学习时间**：2-3天  
**重要性**：⭐⭐⭐⭐⭐（必须掌握）

### 03_advanced.py - 高级操作
- 广播机制
- 布尔索引
- 聚合函数
- 线性代数
- 随机操作
- 性能优化
- 实际应用示例

**学习时间**：2-3天

## 学习顺序

1. **先学基础**（01_basics.py）
2. **重点掌握向量操作**（02_vector_operations.py）
3. **学习高级特性**（03_advanced.py）

## 运行示例

```bash
# 基础操作
python tests/numpy/01_basics.py

# 向量操作（重点）
python tests/numpy/02_vector_operations.py

# 高级操作
python tests/numpy/03_advanced.py
```

## 核心概念

### 向量相似度计算（最重要）

```python
import numpy as np

# 两个向量的余弦相似度
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

# 批量计算
similarities = np.dot(documents_normalized, query_normalized)
```

### 向量归一化

```python
# 归一化向量
normalized = vector / np.linalg.norm(vector)

# 批量归一化
norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
normalized = embeddings / norms
```

## 学习建议

1. **重点掌握**：向量运算、相似度计算
2. **理解概念**：广播机制、向量化操作
3. **实践应用**：在RAG、Embedding项目中应用
4. **性能优化**：使用向量化替代循环

## 与PyTorch/TensorFlow的关系

- **应用开发**：只需要NumPy ✅
- **模型训练**：需要PyTorch/TensorFlow ❌（应用开发不需要）

## 下一步

掌握NumPy后，可以继续学习：
- API调用（tests/01_basic_api_call.py）
- RAG应用（需要向量计算）
- Embedding操作（需要NumPy）

