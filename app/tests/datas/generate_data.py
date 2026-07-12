"""
生成测试数据
运行此脚本生成所有测试数据
"""

import numpy as np
import json
import csv
import os


def create_data_directory():
    """创建数据目录"""
    data_dir = os.path.dirname(__file__)
    return data_dir


def generate_vector_data():
    """生成向量数据"""
    data_dir = create_data_directory()
    
    # 生成随机向量（用于相似度计算）
    np.random.seed(42)
    vectors = np.random.randn(100, 128).astype(np.float32)  # 100个128维向量
    
    # 保存为numpy格式
    np.save(os.path.join(data_dir, 'vectors.npy'), vectors)
    
    # 保存为文本格式（前10个向量作为示例）
    with open(os.path.join(data_dir, 'vectors_sample.txt'), 'w') as f:
        f.write("# 向量数据示例（前10个向量）\n")
        f.write("# 格式：每行一个向量，维度128\n")
        for i, vec in enumerate(vectors[:10]):
            f.write(f"Vector_{i}: {','.join(map(str, vec[:5]))}...\n")
    
    print(f"✓ 生成向量数据: {vectors.shape}")
    return vectors


def generate_matrix_data():
    """生成矩阵数据"""
    data_dir = create_data_directory()
    
    # 生成不同类型的矩阵
    np.random.seed(42)
    
    # 小矩阵（用于基础操作）
    small_matrix = np.random.randn(5, 5).astype(np.float32)
    np.save(os.path.join(data_dir, 'matrix_small.npy'), small_matrix)
    
    # 中等矩阵（用于实际应用）
    medium_matrix = np.random.randn(100, 50).astype(np.float32)
    np.save(os.path.join(data_dir, 'matrix_medium.npy'), medium_matrix)
    
    # 大矩阵（用于性能测试）
    large_matrix = np.random.randn(1000, 500).astype(np.float32)
    np.save(os.path.join(data_dir, 'matrix_large.npy'), large_matrix)
    
    print(f"✓ 生成矩阵数据:")
    print(f"  - 小矩阵: {small_matrix.shape}")
    print(f"  - 中等矩阵: {medium_matrix.shape}")
    print(f"  - 大矩阵: {large_matrix.shape}")


def generate_embedding_data():
    """生成Embedding数据（模拟文本Embedding）"""
    data_dir = create_data_directory()
    
    np.random.seed(42)
    
    # 文档Embeddings（用于RAG、相似度搜索）
    documents = [
        "人工智能是计算机科学的一个分支",
        "机器学习是人工智能的核心技术",
        "深度学习是机器学习的一个子领域",
        "自然语言处理让计算机理解人类语言",
        "计算机视觉处理图像和视频数据",
        "强化学习通过试错来学习",
        "神经网络模拟人脑的工作方式",
        "Transformer架构改变了NLP领域",
        "大语言模型如GPT展现了强大的能力",
        "向量数据库用于存储和检索Embedding"
    ]
    
    # 为每个文档生成Embedding（128维）
    embeddings = np.random.randn(len(documents), 128).astype(np.float32)
    
    # 归一化
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / norms
    
    # 保存Embedding
    np.save(os.path.join(data_dir, 'document_embeddings.npy'), embeddings)
    
    # 保存文档文本和Embedding的映射
    doc_data = {
        'documents': documents,
        'embedding_shape': embeddings.shape,
        'embedding_dim': 128
    }
    
    with open(os.path.join(data_dir, 'documents.json'), 'w', encoding='utf-8') as f:
        json.dump(doc_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 生成文档Embedding数据: {embeddings.shape}")
    print(f"  文档数量: {len(documents)}")


def generate_training_data():
    """生成训练数据"""
    data_dir = create_data_directory()
    
    np.random.seed(42)
    
    # 分类数据
    n_samples = 1000
    n_features = 20
    n_classes = 3
    
    X = np.random.randn(n_samples, n_features).astype(np.float32)
    y = np.random.randint(0, n_classes, size=n_samples)
    
    # 保存
    np.save(os.path.join(data_dir, 'train_X.npy'), X)
    np.save(os.path.join(data_dir, 'train_y.npy'), y)
    
    # 保存为CSV（前100个样本作为示例）
    with open(os.path.join(data_dir, 'train_data_sample.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['feature_' + str(i) for i in range(n_features)] + ['label'])
        for i in range(min(100, n_samples)):
            writer.writerow(list(X[i]) + [y[i]])
    
    print(f"✓ 生成训练数据:")
    print(f"  - 特征: {X.shape}")
    print(f"  - 标签: {y.shape}")
    print(f"  - 类别数: {n_classes}")


def generate_time_series_data():
    """生成时间序列数据"""
    data_dir = create_data_directory()
    
    np.random.seed(42)
    
    # 生成简单的时间序列（正弦波 + 噪声）
    t = np.linspace(0, 10, 1000)
    signal = np.sin(2 * np.pi * t) + 0.5 * np.random.randn(1000)
    
    time_series = np.column_stack([t, signal]).astype(np.float32)
    np.save(os.path.join(data_dir, 'time_series.npy'), time_series)
    
    print(f"✓ 生成时间序列数据: {time_series.shape}")


def generate_image_data():
    """生成图像数据（模拟）"""
    data_dir = create_data_directory()
    
    np.random.seed(42)
    
    # 生成模拟图像数据（灰度图）
    images = np.random.randint(0, 256, size=(100, 28, 28), dtype=np.uint8)
    labels = np.random.randint(0, 10, size=100, dtype=np.int32)
    
    np.save(os.path.join(data_dir, 'images.npy'), images)
    np.save(os.path.join(data_dir, 'image_labels.npy'), labels)
    
    print(f"✓ 生成图像数据:")
    print(f"  - 图像: {images.shape}")
    print(f"  - 标签: {labels.shape}")


def generate_query_data():
    """生成查询数据（用于相似度搜索）"""
    data_dir = create_data_directory()
    
    np.random.seed(42)
    
    # 生成查询向量
    queries = np.random.randn(5, 128).astype(np.float32)
    
    # 归一化
    norms = np.linalg.norm(queries, axis=1, keepdims=True)
    queries = queries / norms
    
    np.save(os.path.join(data_dir, 'query_vectors.npy'), queries)
    
    query_texts = [
        "什么是人工智能？",
        "机器学习如何工作？",
        "深度学习的应用",
        "自然语言处理技术",
        "向量数据库的用途"
    ]
    
    query_data = {
        'queries': query_texts,
        'embedding_shape': queries.shape
    }
    
    with open(os.path.join(data_dir, 'queries.json'), 'w', encoding='utf-8') as f:
        json.dump(query_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 生成查询数据: {queries.shape}")


def generate_all_data():
    """生成所有测试数据"""
    print("=" * 60)
    print("生成测试数据")
    print("=" * 60)
    print()
    
    generate_vector_data()
    generate_matrix_data()
    generate_embedding_data()
    generate_training_data()
    generate_time_series_data()
    generate_image_data()
    generate_query_data()
    
    print()
    print("=" * 60)
    print("所有测试数据生成完成！")
    print("=" * 60)


if __name__ == "__main__":
    generate_all_data()

