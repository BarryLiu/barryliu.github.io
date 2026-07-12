"""
NumPy高级操作示例
学习目标：掌握NumPy的高级特性
"""

import numpy as np


def broadcasting():
    """广播机制"""
    print("=" * 60)
    print("广播机制（NumPy的强大特性）")
    print("=" * 60)
    
    # 示例1: 向量与标量
    arr = np.array([1, 2, 3, 4, 5])
    print(f"数组: {arr}")
    print(f"数组 + 10: {arr + 10}")
    print(f"数组 * 2: {arr * 2}")
    
    # 示例2: 矩阵与向量
    matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    vec = np.array([10, 20, 30])
    
    print(f"\n矩阵:\n{matrix}")
    print(f"向量: {vec}")
    print(f"矩阵 + 向量（广播）:\n{matrix + vec}")
    
    # 示例3: 不同形状的数组
    arr1 = np.array([[1], [2], [3]])  # 形状 (3, 1)
    arr2 = np.array([10, 20, 30])      # 形状 (3,)
    
    print(f"\n数组1 (3x1):\n{arr1}")
    print(f"数组2 (3,): {arr2}")
    print(f"数组1 + 数组2（广播）:\n{arr1 + arr2}")


def boolean_indexing():
    """布尔索引"""
    print("\n" + "=" * 60)
    print("布尔索引")
    print("=" * 60)
    
    arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(f"原数组: {arr}")
    
    # 条件筛选
    mask = arr > 5
    print(f"条件 (arr > 5): {mask}")
    print(f"筛选结果: {arr[mask]}")
    
    # 多个条件
    mask2 = (arr > 3) & (arr < 8)
    print(f"\n条件 (3 < arr < 8): {mask2}")
    print(f"筛选结果: {arr[mask2]}")
    
    # 修改满足条件的元素
    arr[arr > 5] = 0
    print(f"\n修改后 (大于5的元素设为0): {arr}")


def aggregation():
    """聚合函数"""
    print("\n" + "=" * 60)
    print("聚合函数")
    print("=" * 60)
    
    arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(f"数组:\n{arr}")
    
    print(f"\n总和: {np.sum(arr)}")
    print(f"平均值: {np.mean(arr):.2f}")
    print(f"最大值: {np.max(arr)}")
    print(f"最小值: {np.min(arr)}")
    print(f"标准差: {np.std(arr):.2f}")
    
    # 按轴聚合
    print(f"\n按行求和: {np.sum(arr, axis=1)}")
    print(f"按列求和: {np.sum(arr, axis=0)}")
    print(f"按行求平均: {np.mean(arr, axis=1)}")


def linear_algebra():
    """线性代数操作"""
    print("\n" + "=" * 60)
    print("线性代数操作")
    print("=" * 60)
    
    # 矩阵
    A = np.array([[1, 2], [3, 4]])
    print(f"矩阵A:\n{A}")
    
    # 矩阵转置
    print(f"转置A^T:\n{A.T}")
    
    # 矩阵逆
    A_inv = np.linalg.inv(A)
    print(f"逆矩阵A^-1:\n{A_inv}")
    print(f"验证 A @ A^-1:\n{A @ A_inv}")
    
    # 矩阵行列式
    det = np.linalg.det(A)
    print(f"\n行列式: {det:.2f}")
    
    # 特征值和特征向量
    eigenvalues, eigenvectors = np.linalg.eig(A)
    print(f"\n特征值: {eigenvalues}")
    print(f"特征向量:\n{eigenvectors}")


def random_operations():
    """随机操作"""
    print("\n" + "=" * 60)
    print("随机操作")
    print("=" * 60)
    
    # 设置随机种子（可重现）
    np.random.seed(42)
    
    # 随机数组
    random_arr = np.random.rand(5)
    print(f"随机数组 (0-1): {random_arr}")
    
    # 随机整数
    random_int = np.random.randint(1, 10, size=5)
    print(f"随机整数 (1-9): {random_int}")
    
    # 正态分布
    normal = np.random.normal(0, 1, size=5)
    print(f"正态分布 (均值0, 标准差1): {normal}")
    
    # 随机选择
    arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    choice = np.random.choice(arr, size=3, replace=False)
    print(f"从数组随机选择3个: {choice}")
    
    # 打乱数组
    shuffled = np.random.permutation(arr)
    print(f"打乱数组: {shuffled}")


def performance_tips():
    """性能优化技巧"""
    print("\n" + "=" * 60)
    print("性能优化技巧")
    print("=" * 60)
    
    # 向量化操作 vs 循环
    print("向量化操作 vs Python循环:")
    
    arr = np.random.rand(1000000)
    
    # 方法1: Python循环（慢）
    import time
    start = time.time()
    result1 = [x * 2 for x in arr]
    time1 = time.time() - start
    
    # 方法2: NumPy向量化（快）
    start = time.time()
    result2 = arr * 2
    time2 = time.time() - start
    
    print(f"Python循环时间: {time1:.4f}秒")
    print(f"NumPy向量化时间: {time2:.4f}秒")
    print(f"加速比: {time1/time2:.1f}x")
    
    # 预分配数组
    print("\n预分配数组:")
    size = 1000
    arr_preallocated = np.zeros(size)
    print(f"预分配数组形状: {arr_preallocated.shape}")


def practical_example():
    """实际应用示例：文本相似度搜索"""
    print("\n" + "=" * 60)
    print("实际应用：文本相似度搜索")
    print("=" * 60)
    
    # 模拟文档库
    num_docs = 100
    embedding_dim = 128
    
    # 生成随机Embedding（实际应用中来自模型）
    np.random.seed(42)
    document_embeddings = np.random.randn(num_docs, embedding_dim)
    
    # 归一化
    norms = np.linalg.norm(document_embeddings, axis=1, keepdims=True)
    document_embeddings = document_embeddings / norms
    
    # 查询向量
    query_embedding = np.random.randn(embedding_dim)
    query_embedding = query_embedding / np.linalg.norm(query_embedding)
    
    print(f"文档库大小: {num_docs}个文档")
    print(f"Embedding维度: {embedding_dim}")
    
    # 批量计算相似度
    similarities = np.dot(document_embeddings, query_embedding)
    
    # 找到top-5最相似的文档
    top_k = 5
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    print(f"\nTop-{top_k}最相似的文档:")
    for i, idx in enumerate(top_indices, 1):
        print(f"  {i}. 文档{idx}: 相似度 {similarities[idx]:.4f}")


if __name__ == "__main__":
    print("NumPy高级操作示例\n")
    
    broadcasting()
    boolean_indexing()
    aggregation()
    linear_algebra()
    random_operations()
    performance_tips()
    practical_example()

