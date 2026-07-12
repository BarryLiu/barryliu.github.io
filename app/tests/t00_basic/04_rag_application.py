"""
阶段三：RAG（检索增强生成）应用示例
学习目标：掌握RAG系统的构建

需要掌握的技能：
- 文档加载与预处理
- 文本分块策略
- 检索策略设计
- 上下文注入
- RAG流程实现
"""

from typing import List, Dict, Any, Tuple
import re


class DocumentProcessor:
    """文档处理器"""
    
    @staticmethod
    def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        将文本分割成块
        
        Args:
            text: 原始文本
            chunk_size: 每块的大小（字符数）
            overlap: 块之间的重叠大小
        
        Returns:
            文本块列表
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # 尝试在句号、换行符等位置分割
            if end < len(text):
                # 向后查找合适的分割点
                for sep in ['\n\n', '。', '.\n', '\n']:
                    last_sep = chunk.rfind(sep)
                    if last_sep > chunk_size * 0.5:  # 至少保留一半内容
                        chunk = chunk[:last_sep + len(sep)]
                        end = start + len(chunk)
                        break
            
            chunks.append(chunk.strip())
            start = end - overlap  # 重叠部分
        
        return chunks
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        清理文本
        
        Args:
            text: 原始文本
        
        Returns:
            清理后的文本
        """
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        # 移除特殊字符（根据需要调整）
        # text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)
        return text.strip()


class RAGSystem:
    """RAG系统实现"""
    
    def __init__(self):
        """初始化RAG系统"""
        self.documents: List[str] = []
        self.chunks: List[str] = []
        self.chunk_embeddings: List[Any] = []  # 实际应用中存储向量
        self.vector_store = None  # 实际应用中连接向量数据库
    
    def add_documents(self, texts: List[str], chunk_size: int = 500):
        """
        添加文档到RAG系统
        
        Args:
            texts: 文档文本列表
            chunk_size: 分块大小
        """
        processor = DocumentProcessor()
        
        for text in texts:
            # 清理文本
            cleaned = processor.clean_text(text)
            
            # 分割成块
            chunks = processor.split_text(cleaned, chunk_size=chunk_size)
            
            # 存储
            self.documents.append(cleaned)
            self.chunks.extend(chunks)
            
            # 实际应用中：为每个chunk生成embedding并存储到向量数据库
            # for chunk in chunks:
            #     embedding = get_embedding(chunk)
            #     self.vector_store.add(chunk, embedding)
        
        print(f"已添加 {len(texts)} 个文档，共 {len(self.chunks)} 个文本块")
    
    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        similarity_threshold: float = 0.7
    ) -> List[Tuple[str, float]]:
        """
        检索相关文档块
        
        Args:
            query: 查询文本
            top_k: 返回top_k个最相关的结果
            similarity_threshold: 相似度阈值
        
        Returns:
            [(文档块, 相似度分数), ...]
        """
        # 实际应用中：
        # 1. 将query转换为embedding
        # 2. 在向量数据库中搜索相似文档块
        # 3. 返回top_k结果
        
        # 这里使用简化的文本匹配作为演示
        results = []
        query_lower = query.lower()
        
        for chunk in self.chunks:
            # 简单的关键词匹配（实际应使用向量相似度）
            chunk_lower = chunk.lower()
            matches = sum(1 for word in query_lower.split() if word in chunk_lower)
            score = matches / len(query_lower.split()) if query_lower.split() else 0
            
            if score >= similarity_threshold:
                results.append((chunk, score))
        
        # 按分数排序
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def generate_context(self, query: str, top_k: int = 3) -> str:
        """
        生成检索到的上下文
        
        Args:
            query: 查询文本
            top_k: 检索top_k个文档块
        
        Returns:
            组合后的上下文
        """
        retrieved = self.retrieve(query, top_k=top_k)
        
        if not retrieved:
            return "未找到相关文档。"
        
        context_parts = []
        for i, (chunk, score) in enumerate(retrieved, 1):
            context_parts.append(f"[文档片段 {i}] (相关度: {score:.2f})\n{chunk}")
        
        return "\n\n".join(context_parts)
    
    def rag_prompt(self, query: str, top_k: int = 3) -> List[Dict[str, str]]:
        """
        构建RAG Prompt
        
        Args:
            query: 用户查询
            top_k: 检索的文档数量
        
        Returns:
            格式化的消息列表
        """
        context = self.generate_context(query, top_k=top_k)
        
        return [
            {
                "role": "system",
                "content": "你是一个智能助手，基于提供的文档内容回答问题。如果文档中没有相关信息，请明确说明。"
            },
            {
                "role": "user",
                "content": f"""基于以下文档内容回答问题：

文档内容：
{context}

问题：{query}

请基于上述文档内容回答，如果文档中没有相关信息，请说明。"""
            }
        ]


def demonstrate_rag_workflow():
    """演示RAG工作流程"""
    print("=" * 60)
    print("RAG系统工作流程演示")
    print("=" * 60)
    
    # 创建RAG系统
    rag = RAGSystem()
    
    # 添加文档
    documents = [
        """
        人工智能（AI）是计算机科学的一个分支，旨在创建能够执行通常需要人类智能的任务的系统。
        机器学习是AI的一个子领域，它使计算机能够从数据中学习，而无需明确编程。
        深度学习是机器学习的一个分支，使用神经网络来模拟人脑的工作方式。
        """,
        """
        Python是一种高级编程语言，以其简洁的语法和强大的功能而闻名。
        它广泛用于数据科学、Web开发、人工智能等领域。
        Python拥有丰富的库生态系统，如NumPy、Pandas、TensorFlow等。
        """,
        """
        自然语言处理（NLP）是AI的一个分支，专注于计算机与人类语言之间的交互。
        NLP技术包括文本分类、情感分析、机器翻译、问答系统等。
        现代NLP大量使用深度学习技术，特别是Transformer架构。
        """
    ]
    
    print("\n步骤1: 添加文档")
    print("-" * 60)
    rag.add_documents(documents)
    
    # 执行查询
    query = "什么是机器学习？"
    print(f"\n步骤2: 用户查询")
    print("-" * 60)
    print(f"查询: {query}")
    
    print(f"\n步骤3: 检索相关文档")
    print("-" * 60)
    retrieved = rag.retrieve(query, top_k=2)
    for i, (chunk, score) in enumerate(retrieved, 1):
        print(f"\n结果 {i} (相关度: {score:.2f}):")
        print(chunk[:200] + "..." if len(chunk) > 200 else chunk)
    
    print(f"\n步骤4: 构建RAG Prompt")
    print("-" * 60)
    prompt = rag.rag_prompt(query, top_k=2)
    print("系统消息:")
    print(prompt[0]['content'])
    print("\n用户消息:")
    print(prompt[1]['content'][:300] + "...")


def demonstrate_chunking_strategies():
    """演示不同的分块策略"""
    print("\n" + "=" * 60)
    print("文本分块策略示例")
    print("=" * 60)
    
    processor = DocumentProcessor()
    
    sample_text = """
    人工智能是计算机科学的一个分支。它旨在创建能够执行通常需要人类智能的任务的系统。
    
    机器学习是AI的一个子领域。它使计算机能够从数据中学习，而无需明确编程。
    
    深度学习是机器学习的一个分支。它使用神经网络来模拟人脑的工作方式。
    """
    
    print("原始文本:")
    print(sample_text)
    
    print("\n策略1: 固定大小分块（无重叠）")
    print("-" * 60)
    chunks1 = processor.split_text(sample_text, chunk_size=100, overlap=0)
    for i, chunk in enumerate(chunks1, 1):
        print(f"块 {i}: {chunk[:80]}...")
    
    print("\n策略2: 固定大小分块（有重叠）")
    print("-" * 60)
    chunks2 = processor.split_text(sample_text, chunk_size=100, overlap=20)
    for i, chunk in enumerate(chunks2, 1):
        print(f"块 {i}: {chunk[:80]}...")


def rag_best_practices():
    """RAG最佳实践"""
    print("\n" + "=" * 60)
    print("RAG系统最佳实践")
    print("=" * 60)
    
    practices = [
        {
            "要点": "文档预处理",
            "说明": "在分块前进行适当的预处理",
            "建议": [
                "清理格式和特殊字符",
                "统一编码",
                "处理多语言内容"
            ]
        },
        {
            "要点": "分块策略",
            "说明": "选择合适的分块大小和方法",
            "建议": [
                "根据模型上下文窗口调整",
                "保持语义完整性",
                "使用重叠避免信息丢失",
                "考虑文档结构（段落、章节）"
            ]
        },
        {
            "要点": "检索优化",
            "说明": "提高检索的准确性和相关性",
            "建议": [
                "使用高质量的Embedding模型",
                "调整top_k参数",
                "设置相似度阈值",
                "考虑重排序（reranking）"
            ]
        },
        {
            "要点": "上下文管理",
            "说明": "合理组织检索到的上下文",
            "建议": [
                "控制上下文长度",
                "按相关性排序",
                "添加元数据（来源、时间等）",
                "避免信息重复"
            ]
        },
        {
            "要点": "Prompt设计",
            "说明": "设计有效的RAG Prompt",
            "建议": [
                "明确指示使用提供的文档",
                "要求标注信息来源",
                "处理“不知道”的情况",
                "优化输出格式"
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
    print("阶段三：RAG应用学习示例\n")
    
    demonstrate_rag_workflow()
    demonstrate_chunking_strategies()
    rag_best_practices()
    
    print("\n" + "=" * 60)
    print("学习要点总结")
    print("=" * 60)
    print("""
1. RAG工作流程：
   文档 → 分块 → 向量化 → 存储 → 检索 → 生成

2. 关键组件：
   - 文档处理器：加载、清理、分块
   - 向量存储：存储和检索文档块
   - 检索器：找到相关文档
   - 生成器：基于检索内容生成回答

3. 优化方向：
   - 提高检索准确性
   - 优化分块策略
   - 改进Prompt设计
   - 处理长上下文

4. 常见挑战：
   - 检索不准确
   - 上下文过长
   - 信息重复
   - 处理"不知道"的情况
    """)

