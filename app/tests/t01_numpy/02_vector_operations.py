"""
NumPy向量操作示例
学习目标：掌握向量运算，这是AI应用的核心
"""

import numpy as np


def vector_basics():
    """向量基础"""
    print("=" * 60)
    print("向量基础")
    print("=" * 60)
    
    # 创建向量
    vec1 = np.array([1, 2, 3, 4, 5])
    vec2 = np.array([6, 7, 8, 9, 10])
    
    print(f"向量1: {vec1}")
    print(f"向量2: {vec2}")
    print(f"向量维度: {vec1.shape}")


def vector_norm():
    """向量范数（长度）"""
    print("\n" + "=" * 60)
    print("向量范数（长度）")
    print("=" * 60)
    
    vec = np.array([3, 4])
    print(f"向量: {vec}")
    
    # L2范数（欧氏距离）
    l2_norm = np.linalg.norm(vec)
    print(f"L2范数: {l2_norm}")
    print(f"验证: sqrt(3^2 + 4^2) = {np.sqrt(3**2 + 4**2)}")
    
    # L1范数（曼哈顿距离）
    l1_norm = np.linalg.norm(vec, ord=1)
    print(f"L1范数: {l1_norm}")
    
    # 归一化向量
    normalized = vec / l2_norm
    print(f"归一化向量: {normalized}")
    print(f"归一化后的范数: {np.linalg.norm(normalized):.6f}")


def dot_product():
    """点积"""
    print("\n" + "=" * 60)
    print("点积（内积）")
    print("=" * 60)
    
    vec1 = np.array([1, 2, 3])
    vec2 = np.array([4, 5, 6])
    
    print(f"向量1: {vec1}")
    print(f"向量2: {vec2}")
    
    # 点积
    dot = np.dot(vec1, vec2)
    print(f"点积: {dot}")
    print(f"验证: 1*4 + 2*5 + 3*6 = {1*4 + 2*5 + 3*6}")
    
    # 使用@运算符
    dot2 = vec1 @ vec2
    print(f"使用@运算符: {dot2}")


def cosine_similarity():
    """余弦相似度（AI应用中最常用）"""
    print("\n" + "=" * 60)
    print("余弦相似度（AI应用核心）")
    print("=" * 60)
    
    # 模拟两个文档的Embedding
    vec1 = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    vec2 = np.array([0.2, 0.3, 0.4, 0.5, 0.6])
    vec3 = np.array([0.9, 0.1, 0.2, 0.3, 0.4])  # 不相关的向量
    
    print(f"向量1: {vec1}")
    print(f"向量2: {vec2}")
    print(f"向量3: {vec3}")
    
    def cosine_sim(a, b):
        """计算余弦相似度"""
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        return dot_product / (norm_a * norm_b)
    
    sim_12 = cosine_sim(vec1, vec2)
    sim_13 = cosine_sim(vec1, vec3)
    
    print(f"\n向量1和向量2的余弦相似度: {sim_12:.4f}")
    print(f"向量1和向量3的余弦相似度: {sim_13:.4f}")
    print(f"\n说明: 相似度接近1表示向量相似，接近0表示不相关")


def euclidean_distance():
    """欧氏距离"""
    print("\n" + "=" * 60)
    print("欧氏距离")
    print("=" * 60)
    
    vec1 = np.array([1, 2, 3])
    vec2 = np.array([4, 5, 6])
    
    print(f"向量1: {vec1}")
    print(f"向量2: {vec2}")
    
    # 欧氏距离
    distance = np.linalg.norm(vec1 - vec2)
    print(f"欧氏距离: {distance:.4f}")
    print(f"验证: sqrt((1-4)^2 + (2-5)^2 + (3-6)^2) = {np.sqrt((1-4)**2 + (2-5)**2 + (3-6)**2):.4f}")


def batch_similarity():
    """批量相似度计算（实际应用场景）"""
    print("\n" + "=" * 60)
    print("批量相似度计算（实际应用）")
    print("=" * 60)
    
    # 多个文档的Embedding
    documents = np.array([
        [0.1, 0.2, 0.3, 0.4],
        [0.2, 0.3, 0.4, 0.5],
        [0.5, 0.6, 0.7, 0.8],
        [0.9, 0.1, 0.2, 0.3]
    ])
    
    # 查询向量
    query = np.array([0.15, 0.25, 0.35, 0.45])
    
    print("文档Embeddings:")
    for i, doc in enumerate(documents):
        print(f"  文档{i+1}: {doc}")
    print(f"查询向量: {query}")
    
    # 方法1: 循环计算（慢）
    print("\n方法1: 循环计算")
    for i, doc in enumerate(documents):
        sim = np.dot(doc, query) / (np.linalg.norm(doc) * np.linalg.norm(query))
        print(f"  文档{i+1}相似度: {sim:.4f}")
    
    # 方法2: 批量计算（快，推荐）
    print("\n方法2: 批量计算（推荐）")
    # 归一化所有向量
    doc_norms = np.linalg.norm(documents, axis=1, keepdims=True)
    docs_normalized = documents / doc_norms
    query_normalized = query / np.linalg.norm(query)
    
    # 批量计算相似度
    similarities = np.dot(docs_normalized, query_normalized)
    print(f"所有相似度: {similarities}")
    
    # 找到最相似的文档
    most_similar_idx = np.argmax(similarities)
    print(f"\n最相似的文档: 文档{most_similar_idx + 1} (相似度: {similarities[most_similar_idx]:.4f})")
    
    # 排序
    sorted_indices = np.argsort(similarities)[::-1]
    print(f"\n按相似度排序:")
    for rank, idx in enumerate(sorted_indices, 1):
        print(f"  第{rank}名: 文档{idx+1} (相似度: {similarities[idx]:.4f})")


def embedding_operations():
    """Embedding相关操作"""
    print("\n" + "=" * 60)
    print("Embedding操作（AI应用核心）")
    print("=" * 60)
    
    # 模拟文本Embedding
    text1_emb = np.random.randn(128)  # 128维Embedding
    text2_emb = np.random.randn(128)
    
    print(f"文本1 Embedding维度: {text1_emb.shape}")
    print(f"文本2 Embedding维度: {text2_emb.shape}")
    
    # 归一化（某些场景需要）
    text1_norm = text1_emb / np.linalg.norm(text1_emb)
    text2_norm = text2_emb / np.linalg.norm(text2_emb)
    
    # 相似度
    similarity = np.dot(text1_norm, text2_norm)
    print(f"归一化后的相似度: {similarity:.4f}")
    
    # 平均Embedding（用于句子/文档）
    word_embeddings = np.random.randn(10, 128)  # 10个词的Embedding
    sentence_emb = np.mean(word_embeddings, axis=0)
    print(f"\n词Embeddings形状: {word_embeddings.shape}")
    print(f"句子Embedding形状: {sentence_emb.shape}")
    print(f"平均Embedding前5维: {sentence_emb[:5]}")


if __name__ == "__main__":
    print("NumPy向量操作示例\n")
    print("重点：向量运算是AI应用的核心技能！\n")
    
    vector_basics()
    vector_norm()
    dot_product()
    cosine_similarity()
    euclidean_distance()
    batch_similarity()
    embedding_operations()

