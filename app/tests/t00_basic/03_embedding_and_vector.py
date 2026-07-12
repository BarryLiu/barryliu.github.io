"""
阶段三：向量化与Embedding示例
学习目标：掌握文本向量化和相似度计算

需要掌握的技能：
- 理解向量和Embedding概念
- 使用Embedding模型
- 文本向量化
- 向量相似度计算
- 基础向量检索
"""

import numpy as np
from typing import List, Tuple
import math


class SimpleEmbedding:
    """简单的Embedding示例（用于理解概念）"""
    
    @staticmethod
    def simple_word_embedding(word: str, vocab_size: int = 100) -> np.ndarray:
        """
        简单的词向量示例（仅用于演示概念）
        
        实际应用中应使用专业的Embedding模型如：
        - OpenAI text-embedding-ada-002
        - sentence-transformers
        - 开源模型（BGE、M3E等）
        
        Args:
            word: 要向量化的词
            vocab_size: 词汇表大小
        
        Returns:
            向量表示
        """
        # 这是一个简化的示例，实际Embedding是训练得到的
        # 这里使用hash作为演示
        np.random.seed(hash(word) % 2**32)
        return np.random.randn(128).astype(np.float32)
    
    @staticmethod
    def text_to_embedding(text: str) -> np.ndarray:
        """
        将文本转换为向量（简化示例）
        
        Args:
            text: 输入文本
        
        Returns:
            文本的向量表示
        """
        # 实际应用中应该使用专业的Embedding API
        # 这里仅作概念演示
        words = text.split()
        if not words:
            return np.zeros(128)
        
        # 简单平均（实际应用中更复杂）
        embeddings = [SimpleEmbedding.simple_word_embedding(word) for word in words]
        return np.mean(embeddings, axis=0)


class VectorSimilarity:
    """向量相似度计算工具"""
    
    @staticmethod
    def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        计算余弦相似度
        
        余弦相似度范围：[-1, 1]
        值越接近1，表示向量越相似
        
        Args:
            vec1: 向量1
            vec2: 向量2
        
        Returns:
            相似度分数
        """
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    @staticmethod
    def euclidean_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        计算欧氏距离
        
        距离越小，表示向量越相似
        
        Args:
            vec1: 向量1
            vec2: 向量2
        
        Returns:
            距离值
        """
        return np.linalg.norm(vec1 - vec2)
    
    @staticmethod
    def dot_product(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        计算点积
        
        Args:
            vec1: 向量1
            vec2: 向量2
        
        Returns:
            点积值
        """
        return np.dot(vec1, vec2)


class SimpleVectorStore:
    """简单的向量存储示例"""
    
    def __init__(self):
        """初始化向量存储"""
        self.documents: List[str] = []
        self.embeddings: List[np.ndarray] = []
    
    def add_document(self, text: str, embedding: np.ndarray):
        """
        添加文档和对应的向量
        
        Args:
            text: 文档文本
            embedding: 文档的向量表示
        """
        self.documents.append(text)
        self.embeddings.append(embedding)
    
    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 3,
        similarity_threshold: float = 0.0
    ) -> List[Tuple[str, float]]:
        """
        向量相似度搜索
        
        Args:
            query_embedding: 查询向量
            top_k: 返回最相似的k个结果
            similarity_threshold: 相似度阈值
        
        Returns:
            [(文档文本, 相似度分数), ...] 列表，按相似度降序排列
        """
        if not self.embeddings:
            return []
        
        # 计算所有文档与查询的相似度
        similarities = [
            VectorSimilarity.cosine_similarity(query_embedding, emb)
            for emb in self.embeddings
        ]
        
        # 创建(索引, 相似度)对
        indexed_similarities = list(enumerate(similarities))
        
        # 过滤并排序
        filtered = [
            (idx, sim) for idx, sim in indexed_similarities
            if sim >= similarity_threshold
        ]
        filtered.sort(key=lambda x: x[1], reverse=True)
        
        # 返回top_k结果
        results = []
        for idx, sim in filtered[:top_k]:
            results.append((self.documents[idx], sim))
        
        return results


def demonstrate_embedding():
    """演示向量化过程"""
    print("=" * 60)
    print("向量化示例")
    print("=" * 60)
    
    embedding_tool = SimpleEmbedding()
    
    texts = [
        "人工智能是计算机科学的一个分支",
        "机器学习是人工智能的核心技术",
        "深度学习是机器学习的一个子领域",
        "今天天气真好"
    ]
    
    print("\n文本向量化:")
    print("-" * 60)
    embeddings = []
    for text in texts:
        embedding = embedding_tool.text_to_embedding(text)
        embeddings.append(embedding)
        print(f"文本: {text}")
        print(f"向量维度: {embedding.shape}")
        print(f"向量前5个值: {embedding[:5]}")
        print()


def demonstrate_similarity():
    """演示相似度计算"""
    print("=" * 60)
    print("向量相似度计算示例")
    print("=" * 60)
    
    embedding_tool = SimpleEmbedding()
    similarity_tool = VectorSimilarity()
    
    # 准备文本
    text1 = "人工智能和机器学习"
    text2 = "AI和ML技术"
    text3 = "今天天气不错"
    
    # 向量化
    vec1 = embedding_tool.text_to_embedding(text1)
    vec2 = embedding_tool.text_to_embedding(text2)
    vec3 = embedding_tool.text_to_embedding(text3)
    
    # 计算相似度
    sim_12 = similarity_tool.cosine_similarity(vec1, vec2)
    sim_13 = similarity_tool.cosine_similarity(vec1, vec3)
    
    print(f"\n文本1: {text1}")
    print(f"文本2: {text2}")
    print(f"文本3: {text3}\n")
    
    print(f"文本1 vs 文本2 余弦相似度: {sim_12:.4f}")
    print(f"文本1 vs 文本3 余弦相似度: {sim_13:.4f}")
    
    print("\n说明:")
    print("- 相似度接近1表示文本语义相似")
    print("- 相似度接近0表示文本不相关")


def demonstrate_vector_search():
    """演示向量搜索"""
    print("\n" + "=" * 60)
    print("向量搜索示例")
    print("=" * 60)
    
    embedding_tool = SimpleEmbedding()
    vector_store = SimpleVectorStore()
    
    # 添加文档到向量库
    documents = [
        "Python是一种高级编程语言",
        "机器学习使用算法从数据中学习",
        "深度学习是神经网络的多层结构",
        "自然语言处理让计算机理解人类语言",
        "计算机视觉处理图像和视频数据"
    ]
    
    print("\n添加文档到向量库:")
    print("-" * 60)
    for doc in documents:
        embedding = embedding_tool.text_to_embedding(doc)
        vector_store.add_document(doc, embedding)
        print(f"✓ {doc}")
    
    # 执行搜索
    query = "人工智能和机器学习"
    print(f"\n查询: {query}")
    print("-" * 60)
    
    query_embedding = embedding_tool.text_to_embedding(query)
    results = vector_store.search(query_embedding, top_k=3)
    
    print("\n搜索结果（按相似度排序）:")
    for i, (doc, score) in enumerate(results, 1):
        print(f"{i}. 相似度: {score:.4f}")
        print(f"   文档: {doc}\n")


def embedding_best_practices():
    """Embedding最佳实践"""
    print("=" * 60)
    print("Embedding使用最佳实践")
    print("=" * 60)
    
    practices = [
        {
            "要点": "选择合适的模型",
            "说明": "根据任务选择适合的Embedding模型",
            "建议": [
                "通用任务: OpenAI text-embedding-ada-002",
                "中文任务: BGE、M3E等中文优化模型",
                "多语言: multilingual模型"
            ]
        },
        {
            "要点": "文本预处理",
            "说明": "在向量化前进行适当的文本清理",
            "建议": [
                "去除无关字符",
                "统一编码格式",
                "处理特殊符号"
            ]
        },
        {
            "要点": "批量处理",
            "说明": "批量向量化可以提高效率",
            "建议": [
                "使用批量API",
                "合理设置批次大小",
                "注意API限制"
            ]
        },
        {
            "要点": "向量归一化",
            "说明": "某些场景下需要归一化向量",
            "建议": [
                "余弦相似度通常不需要归一化",
                "某些向量数据库要求归一化",
                "检查模型输出是否已归一化"
            ]
        },
        {
            "要点": "维度选择",
            "说明": "根据需求选择合适的向量维度",
            "建议": [
                "更高维度通常包含更多信息",
                "但也需要更多存储和计算",
                "平衡准确性和效率"
            ]
        }
    ]
    
    for practice in practices:
        print(f"\n{practice['要点']}")
        print(f"说明: {practice['说明']}")
        print("建议:")
        for suggestion in practice['建议']:
            print(f"  - {suggestion}")


if __name__ == "__main__":
    print("阶段三：向量化与Embedding学习示例\n")
    print("注意：本示例使用简化的向量生成方法，仅用于理解概念")
    print("实际应用中应使用专业的Embedding API或模型\n")
    
    demonstrate_embedding()
    demonstrate_similarity()
    demonstrate_vector_search()
    embedding_best_practices()
    
    print("\n" + "=" * 60)
    print("学习要点总结")
    print("=" * 60)
    print("""
1. Embedding概念：
   - 将文本转换为数值向量
   - 语义相似的文本向量也相似
   - 向量维度通常为128-1536

2. 相似度计算：
   - 余弦相似度：最常用，范围[-1, 1]
   - 欧氏距离：距离越小越相似
   - 点积：某些场景下使用

3. 向量搜索：
   - 计算查询向量与所有文档向量的相似度
   - 按相似度排序
   - 返回top_k结果

4. 实际应用：
   - 使用专业的Embedding API
   - 考虑使用向量数据库（Chroma、Pinecone等）
   - 注意成本和性能平衡
    """)

