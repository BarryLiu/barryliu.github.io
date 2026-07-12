"""
LangChain RAG应用示例
学习目标：掌握RAG（检索增强生成）的完整流程
"""

import os

# 优先从 .env 加载
try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
except ImportError:
    pass

DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")


def get_llm():
    """获取阿里百炼LLM实例"""
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model="qwen-plus",
        temperature=0,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/",
        api_key=DASHSCOPE_API_KEY,
    )


def get_embeddings():
    """获取阿里百炼嵌入模型"""
    from langchain_community.embeddings import DashScopeEmbeddings

    return DashScopeEmbeddings(
        model="text-embedding-v2",
        dashscope_api_key=DASHSCOPE_API_KEY,
    )


def demo_document_loading():
    """文档加载示例"""
    print("\n" + "=" * 60)
    print("文档加载")
    print("=" * 60)

    from langchain_community.document_loaders import TextLoader

    # 创建示例文档
    sample_doc = """人工智能（Artificial Intelligence，AI）是计算机科学的一个分支，
    它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
    该领域的研究包括机器人、语音识别、图像识别、自然语言处理和专家系统等。

    机器学习是人工智能的一个子集，它使用统计技术使计算机系统能够从数据中"学习"，
    而无需明确的编程。深度学习是机器学习的一个子集，它利用多层神经网络进行分析。"""

    # 保存示例文档
    doc_path = os.path.join(os.path.dirname(__file__), "sample_doc.txt")
    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(sample_doc)

    # 加载文档
    loader = TextLoader(doc_path, encoding="utf-8")
    documents = loader.load()

    print(f"加载了 {len(documents)} 个文档")
    for doc in documents:
        content = doc.page_content.replace("\n", " ")[:100]
        print(f"内容（前100字）: {content}...")
        print(f"元数据: {doc.metadata}")

    return documents


def demo_text_splitting(documents):
    """文本分割示例"""
    print("\n" + "=" * 60)
    print("文本分割")
    print("=" * 60)

    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
        length_function=len,
    )

    chunks = splitter.split_documents(documents)

    print(f"分割成 {len(chunks)} 个块")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\n块 {i+1}:")
        print(f"  内容: {chunk.page_content[:80]}...")
        print(f"  长度: {len(chunk.page_content)}")

    return chunks


def demo_vector_store(chunks):
    """向量存储示例"""
    print("\n" + "=" * 60)
    print("向量存储")
    print("=" * 60)

    from langchain_community.vectorstores import Chroma

    embeddings = get_embeddings()

    persist_dir = os.path.join(os.path.dirname(__file__), "chroma_db")

    # 清理旧的数据库
    import shutil
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )

    print(f"向量存储已创建，共 {vectorstore._collection.count()} 个向量")

    # 相似度搜索
    results = vectorstore.similarity_search("什么是机器学习", k=2)
    print(f"\n相似度搜索结果（查询：'什么是机器学习'）:")
    for i, doc in enumerate(results):
        print(f"  {i+1}. {doc.page_content[:60]}...")

    return vectorstore


def demo_retrieval(vectorstore):
    """检索示例"""
    print("\n" + "=" * 60)
    print("检索")
    print("=" * 60)

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 2}
    )

    docs = retriever.invoke("人工智能是什么")
    print(f"检索到 {len(docs)} 个相关文档:")
    for i, doc in enumerate(docs):
        print(f"  {i+1}. {doc.page_content[:60]}...")


def demo_rag_chain(vectorstore):
    """RAG Chain示例"""
    print("\n" + "=" * 60)
    print("RAG Chain")
    print("=" * 60)

    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import PromptTemplate
    from langchain_core.runnables import RunnablePassthrough

    llm = get_llm()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    prompt = PromptTemplate.from_template(
        """根据以下上下文回答问题。

上下文：
{context}

问题：{question}

请给出准确、详细的回答。"""
    )

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    result = rag_chain.invoke("机器学习和深度学习有什么关系？")
    print(f"\n问题: 机器学习和深度学习有什么关系？")
    print(f"回答: {result}")


def main():
    """主函数"""
    print("LangChain RAG应用示例（阿里百炼）\n")

    if not DASHSCOPE_API_KEY:
        print("错误: 请设置 DASHSCOPE_API_KEY 环境变量")
        return

    # 1. 加载文档
    documents = demo_document_loading()

    # 2. 分割文本
    chunks = demo_text_splitting(documents)

    # 3. 向量存储
    vectorstore = demo_vector_store(chunks)

    # 4. 检索
    demo_retrieval(vectorstore)

    # 5. RAG Chain
    demo_rag_chain(vectorstore)

    print("\n" + "=" * 60)
    print("RAG示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
