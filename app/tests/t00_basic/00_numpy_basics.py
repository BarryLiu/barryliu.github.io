"""
NumPy基础学习示例
学习目标：掌握NumPy的基础操作，特别是向量计算

注意：这是应用开发路径中唯一需要学习的"框架"
PyTorch和TensorFlow在应用开发中通常不需要
"""

import numpy as np


def demonstrate_array_basics():
    """演示NumPy数组基础操作"""
    print("=" * 60)
    print("NumPy数组基础操作")
    print("=" * 60)
    
    # 创建数组
    arr1 = np.array([1, 2, 3, 4, 5])
    arr2 = np.array([6, 7, 8, 9, 10])
    
    print(f"数组1: {arr1}")
    print(f"数组2: {arr2}")
    print(f"数组形状: {arr1.shape}")
    print(f"数组维度: {arr1.ndim}")
    print(f"数组类型: {arr1.dtype}")
    
    # 基本运算
    print(f"\n数组相加: {arr1 + arr2}")
    print(f"数组相乘: {arr1 * 2}")
    print(f"数组点积: {np.dot(arr1, arr2)}")


def demonstrate_vector_operations():
    """演示向量操作（AI应用中最常用）"""
    print("\n" + "=" * 60)
    print("向量操作（AI应用核心）")
    print("=" * 60)
    
    # 创建向量（模拟Embedding）
    vec1 = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    vec2 = np.array([0.2, 0.3, 0.4, 0.5, 0.6])
    
    print(f"向量1: {vec1}")
    print(f"向量2: {vec2}")
    
    # 向量范数（长度）
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    print(f"\n向量1的范数（长度）: {norm1:.4f}")
    print(f"向量2的范数（长度）: {norm2:.4f}")
    
    # 点积（用于相似度计算）
    dot_product = np.dot(vec1, vec2)
    print(f"\n点积: {dot_product:.4f}")
    
    # 余弦相似度（AI应用中最常用）
    cosine_sim = dot_product / (norm1 * norm2)
    print(f"余弦相似度: {cosine_sim:.4f}")
    
    # 欧氏距离
    euclidean_dist = np.linalg.norm(vec1 - vec2)
    print(f"欧氏距离: {euclidean_dist:.4f}")


def demonstrate_matrix_operations():
    """演示矩阵操作"""
    print("\n" + "=" * 60)
    print("矩阵操作")
    print("=" * 60)
    
    # 创建矩阵
    matrix = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ])
    
    print("矩阵:")
    print(matrix)
    print(f"\n矩阵形状: {matrix.shape}")
    print(f"矩阵转置:")
    print(matrix.T)
    
    # 矩阵乘法
    vec = np.array([1, 2, 3])
    result = np.dot(matrix, vec)
    print(f"\n矩阵 × 向量: {result}")


def demonstrate_embedding_operations():
    """演示Embedding相关操作（实际应用场景）"""
    print("\n" + "=" * 60)
    print("Embedding操作（实际应用）")
    print("=" * 60)
    
    # 模拟多个文档的Embedding
    embeddings = np.array([
        [0.1, 0.2, 0.3, 0.4],
        [0.2, 0.3, 0.4, 0.5],
        [0.5, 0.6, 0.7, 0.8],
        [0.9, 0.1, 0.2, 0.3]
    ])
    
    # 查询向量
    query = np.array([0.15, 0.25, 0.35, 0.45])
    
    print("文档Embeddings:")
    print(embeddings)
    print(f"\n查询向量: {query}")
    
    # 计算所有文档与查询的相似度
    print("\n计算相似度:")
    for i, emb in enumerate(embeddings):
        # 归一化（某些场景需要）
        emb_norm = emb / np.linalg.norm(emb)
        query_norm = query / np.linalg.norm(query)
        
        # 余弦相似度
        similarity = np.dot(emb_norm, query_norm)
        print(f"文档 {i+1} 相似度: {similarity:.4f}")
    
    # 批量计算（更高效）
    print("\n批量计算（推荐方式）:")
    # 归一化所有向量
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings_norm = embeddings / norms
    query_norm = query / np.linalg.norm(query)
    
    # 批量计算相似度
    similarities = np.dot(embeddings_norm, query_norm)
    print(f"所有相似度: {similarities}")
    
    # 找到最相似的文档
    most_similar_idx = np.argmax(similarities)
    print(f"\n最相似的文档: 文档 {most_similar_idx + 1} (相似度: {similarities[most_similar_idx]:.4f})")


def demonstrate_broadcasting():
    """演示广播机制（NumPy的强大特性）"""
    print("\n" + "=" * 60)
    print("广播机制")
    print("=" * 60)
    
    # 矩阵
    matrix = np.array([
        [1, 2, 3],
        [4, 5, 6]
    ])
    
    # 向量
    vec = np.array([10, 20, 30])
    
    print("矩阵:")
    print(matrix)
    print(f"\n向量: {vec}")
    
    # 广播：向量会自动扩展到每行
    result = matrix + vec
    print(f"\n矩阵 + 向量（广播）:")
    print(result)
    
    # 另一个例子：归一化每行
    row_norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    normalized = matrix / row_norms
    print(f"\n按行归一化:")
    print(normalized)


def numpy_vs_pytorch_comparison():
    """NumPy vs PyTorch对比说明"""
    print("\n" + "=" * 60)
    print("NumPy vs PyTorch - 何时使用哪个？")
    print("=" * 60)
    
    print("""
应用开发场景（使用NumPy）：
  ✅ 向量相似度计算
  ✅ Embedding操作
  ✅ 数据预处理
  ✅ 简单的数值计算
  
  示例代码：
  import numpy as np
  similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

模型训练场景（使用PyTorch）：
  ✅ 神经网络定义
  ✅ 模型训练
  ✅ 梯度计算
  ✅ GPU加速训练
  
  示例代码：
  import torch
  model = torch.nn.Linear(10, 1)
  loss = criterion(output, target)
  loss.backward()

结论：
  - 应用开发：只需要NumPy
  - 模型训练：需要PyTorch
  - 大多数AI应用开发者只需要NumPy！
    """)


def learning_roadmap():
    """学习路线建议"""
    print("\n" + "=" * 60)
    print("NumPy学习路线")
    print("=" * 60)
    
    roadmap = [
        {
            "阶段": "第1周：基础",
            "内容": [
                "数组创建和基本操作",
                "数组索引和切片",
                "基本数学运算",
                "数组形状操作"
            ]
        },
        {
            "阶段": "第2周：向量计算",
            "内容": [
                "向量运算（点积、范数）",
                "矩阵运算",
                "线性代数函数",
                "广播机制"
            ]
        },
        {
            "阶段": "实际应用",
            "内容": [
                "Embedding相似度计算",
                "向量归一化",
                "批量处理",
                "性能优化"
            ]
        }
    ]
    
    for stage in roadmap:
        print(f"\n{stage['阶段']}:")
        for item in stage['内容']:
            print(f"  - {item}")


if __name__ == "__main__":
    print("NumPy基础学习示例")
    print("=" * 60)
    print("""
重要说明：
1. NumPy是应用开发路径中唯一需要学习的"框架"
2. PyTorch和TensorFlow在应用开发中通常不需要
3. 重点掌握向量计算，这是AI应用的核心

学习目标：
- 理解NumPy数组和向量
- 掌握向量相似度计算
- 学会批量处理操作
- 了解广播机制
    """)
    
    demonstrate_array_basics()
    demonstrate_vector_operations()
    demonstrate_matrix_operations()
    demonstrate_embedding_operations()
    demonstrate_broadcasting()
    numpy_vs_pytorch_comparison()
    learning_roadmap()
    
    print("\n" + "=" * 60)
    print("总结")
    print("=" * 60)
    print("""
对于大模型应用开发：
  ✅ 必须掌握：NumPy（向量计算）
  ❌ 不需要：PyTorch、TensorFlow
  
学习重点：
  1. 向量运算（点积、范数、相似度）
  2. 矩阵操作
  3. 批量处理
  4. 广播机制

学习时间：1-2周即可掌握应用所需的基础
    """)

