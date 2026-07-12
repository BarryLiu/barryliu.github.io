"""
NumPy数据操作示例
学习目标：使用实际数据文件进行NumPy操作
"""

import numpy as np
import os
import json


def get_data_path(filename):
    """获取数据文件路径"""
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, '..', 'datas')
    return os.path.join(data_dir, filename)


def demo_vector_operations():
    """向量操作示例"""
    print("=" * 60)
    print("向量操作示例 - 使用实际数据")
    print("=" * 60)
    
    # 加载向量数据
    vectors_path = get_data_path('vectors.npy')
    if not os.path.exists(vectors_path):
        print(f"数据文件不存在: {vectors_path}")
        print("请先运行: python tests/datas/generate_data.py")
        return
    
    vectors = np.load(vectors_path)
    print(f"加载向量数据: {vectors.shape}")
    print(f"向量维度: {vectors.shape[1]}")
    print(f"向量数量: {vectors.shape[0]}")
    
    # 计算向量统计信息
    print(f"\n向量统计信息:")
    print(f"  均值: {np.mean(vectors):.4f}")
    print(f"  标准差: {np.std(vectors):.4f}")
    print(f"  最小值: {np.min(vectors):.4f}")
    print(f"  最大值: {np.max(vectors):.4f}")
    
    # 计算每个向量的范数
    norms = np.linalg.norm(vectors, axis=1)
    print(f"\n向量范数统计:")
    print(f"  平均范数: {np.mean(norms):.4f}")
    print(f"  范数范围: [{np.min(norms):.4f}, {np.max(norms):.4f}]")


def demo_similarity_search():
    """相似度搜索示例"""
    print("\n" + "=" * 60)
    print("相似度搜索示例 - 使用文档Embedding")
    print("=" * 60)
    
    # 加载文档Embedding
    embeddings_path = get_data_path('document_embeddings.npy')
    docs_path = get_data_path('documents.json')
    queries_path = get_data_path('query_vectors.npy')
    queries_json_path = get_data_path('queries.json')
    
    if not all(os.path.exists(p) for p in [embeddings_path, docs_path, queries_path, queries_json_path]):
        print("数据文件不存在，请先运行: python tests/datas/generate_data.py")
        return
    
    # 加载数据
    doc_embeddings = np.load(embeddings_path)
    
    with open(docs_path, 'r', encoding='utf-8') as f:
        docs_data = json.load(f)
    documents = docs_data['documents']
    
    query_vectors = np.load(queries_path)
    
    with open(queries_json_path, 'r', encoding='utf-8') as f:
        queries_data = json.load(f)
    query_texts = queries_data['queries']
    
    print(f"文档数量: {len(documents)}")
    print(f"查询数量: {len(query_texts)}")
    
    # 归一化文档Embedding
    doc_norms = np.linalg.norm(doc_embeddings, axis=1, keepdims=True)
    doc_embeddings_norm = doc_embeddings / doc_norms
    
    # 对每个查询进行搜索
    for i, (query_text, query_vec) in enumerate(zip(query_texts, query_vectors)):
        print(f"\n查询 {i+1}: {query_text}")
        print("-" * 60)
        
        # 归一化查询向量
        query_norm = query_vec / np.linalg.norm(query_vec)
        
        # 计算相似度
        similarities = np.dot(doc_embeddings_norm, query_norm)
        
        # 找到top-3最相似的文档
        top_k = 3
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        print(f"Top-{top_k}最相似的文档:")
        for rank, idx in enumerate(top_indices, 1):
            print(f"  {rank}. [{similarities[idx]:.4f}] {documents[idx]}")


def demo_matrix_operations():
    """矩阵操作示例"""
    print("\n" + "=" * 60)
    print("矩阵操作示例 - 使用实际数据")
    print("=" * 60)
    
    # 加载不同大小的矩阵
    matrix_files = [
        ('matrix_small.npy', '小矩阵'),
        ('matrix_medium.npy', '中等矩阵'),
        ('matrix_large.npy', '大矩阵')
    ]
    
    for filename, name in matrix_files:
        matrix_path = get_data_path(filename)
        if not os.path.exists(matrix_path):
            continue
        
        matrix = np.load(matrix_path)
        print(f"\n{name}: {matrix.shape}")
        
        # 基本统计
        print(f"  均值: {np.mean(matrix):.4f}")
        print(f"  标准差: {np.std(matrix):.4f}")
        
        # 矩阵运算（仅对小矩阵）
        if matrix.shape[0] == matrix.shape[1] and matrix.shape[0] <= 10:
            # 矩阵转置
            transposed = matrix.T
            print(f"  转置形状: {transposed.shape}")
            
            # 矩阵乘法
            if matrix.shape[0] <= 5:
                product = np.dot(matrix, matrix)
                print(f"  矩阵平方形状: {product.shape}")


def demo_training_data_processing():
    """训练数据处理示例"""
    print("\n" + "=" * 60)
    print("训练数据处理示例")
    print("=" * 60)
    
    # 加载训练数据
    X_path = get_data_path('train_X.npy')
    y_path = get_data_path('train_y.npy')
    
    if not os.path.exists(X_path) or not os.path.exists(y_path):
        print("数据文件不存在，请先运行: python tests/datas/generate_data.py")
        return
    
    X = np.load(X_path)
    y = np.load(y_path)
    
    print(f"特征数据: {X.shape}")
    print(f"标签数据: {y.shape}")
    
    # 数据统计
    print(f"\n数据统计:")
    print(f"  样本数: {X.shape[0]}")
    print(f"  特征数: {X.shape[1]}")
    print(f"  类别数: {len(np.unique(y))}")
    
    # 特征统计
    print(f"\n特征统计:")
    print(f"  特征均值: {np.mean(X, axis=0)[:5]}")  # 前5个特征
    print(f"  特征标准差: {np.std(X, axis=0)[:5]}")
    
    # 标签分布
    unique, counts = np.unique(y, return_counts=True)
    print(f"\n标签分布:")
    for label, count in zip(unique, counts):
        print(f"  类别 {label}: {count} 个样本 ({count/len(y)*100:.1f}%)")
    
    # 数据归一化示例
    X_normalized = (X - np.mean(X, axis=0)) / np.std(X, axis=0)
    print(f"\n归一化后:")
    print(f"  均值: {np.mean(X_normalized):.6f} (应该接近0)")
    print(f"  标准差: {np.std(X_normalized):.6f} (应该接近1)")


def demo_time_series_analysis():
    """时间序列分析示例"""
    print("\n" + "=" * 60)
    print("时间序列分析示例")
    print("=" * 60)
    
    time_series_path = get_data_path('time_series.npy')
    if not os.path.exists(time_series_path):
        print("数据文件不存在，请先运行: python tests/datas/generate_data.py")
        return
    
    data = np.load(time_series_path)
    time = data[:, 0]
    signal = data[:, 1]
    
    print(f"时间序列数据: {data.shape}")
    print(f"时间范围: [{time[0]:.2f}, {time[-1]:.2f}]")
    print(f"信号范围: [{np.min(signal):.4f}, {np.max(signal):.4f}]")
    
    # 统计信息
    print(f"\n信号统计:")
    print(f"  均值: {np.mean(signal):.4f}")
    print(f"  标准差: {np.std(signal):.4f}")
    print(f"  最小值: {np.min(signal):.4f}")
    print(f"  最大值: {np.max(signal):.4f}")
    
    # 滑动平均（简单平滑）
    window_size = 10
    if len(signal) > window_size:
        moving_avg = np.convolve(signal, np.ones(window_size)/window_size, mode='valid')
        print(f"\n滑动平均 (窗口={window_size}):")
        print(f"  原始信号标准差: {np.std(signal):.4f}")
        print(f"  平滑后标准差: {np.std(moving_avg):.4f}")


def demo_image_data_processing():
    """图像数据处理示例"""
    print("\n" + "=" * 60)
    print("图像数据处理示例")
    print("=" * 60)
    
    images_path = get_data_path('images.npy')
    labels_path = get_data_path('image_labels.npy')
    
    if not os.path.exists(images_path) or not os.path.exists(labels_path):
        print("数据文件不存在，请先运行: python tests/datas/generate_data.py")
        return
    
    images = np.load(images_path)
    labels = np.load(labels_path)
    
    print(f"图像数据: {images.shape}")
    print(f"标签数据: {labels.shape}")
    
    # 图像统计
    print(f"\n图像统计:")
    print(f"  图像数量: {images.shape[0]}")
    print(f"  图像尺寸: {images.shape[1]}x{images.shape[2]}")
    print(f"  像素值范围: [{np.min(images)}, {np.max(images)}]")
    
    # 计算每张图像的平均像素值
    image_means = np.mean(images, axis=(1, 2))
    print(f"\n图像平均像素值:")
    print(f"  整体均值: {np.mean(image_means):.2f}")
    print(f"  标准差: {np.std(image_means):.2f}")
    
    # 标签分布
    unique, counts = np.unique(labels, return_counts=True)
    print(f"\n标签分布:")
    for label, count in zip(unique, counts):
        print(f"  类别 {label}: {count} 张图像")


if __name__ == "__main__":
    print("NumPy数据操作示例\n")
    print("本示例演示如何使用实际数据文件进行NumPy操作\n")
    
    demo_vector_operations()
    demo_similarity_search()
    demo_matrix_operations()
    demo_training_data_processing()
    demo_time_series_analysis()
    demo_image_data_processing()
    
    print("\n" + "=" * 60)
    print("总结")
    print("=" * 60)
    print("""
本示例展示了：
1. 加载和保存NumPy数组（.npy格式）
2. 向量相似度计算和搜索
3. 矩阵操作和统计
4. 训练数据预处理
5. 时间序列分析
6. 图像数据处理

这些都是AI应用开发中的常见操作！
    """)

