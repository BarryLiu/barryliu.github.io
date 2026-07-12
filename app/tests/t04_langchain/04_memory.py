"""
LangChain Memory示例
学习目标：掌握对话记忆管理
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


def demo_buffer_memory():
    """Buffer Memory示例"""
    print("\n" + "=" * 60)
    print("ConversationBufferMemory")
    print("=" * 60)

    from langchain.memory import ConversationBufferMemory
    from langchain.chains import ConversationChain
    from langchain_core.output_parsers import StrOutputParser

    llm = get_llm()

    memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=True
    )

    chain = ConversationChain(
        llm=llm,
        memory=memory,
        output_parser=StrOutputParser()
    )

    print("\n--- 对话1 ---")
    response = chain.invoke({"input": "你好，我叫张三"})
    print(f"你: 你好，我叫张三")
    print(f"AI: {response['response']}")

    print("\n--- 对话2 ---")
    response = chain.invoke({"input": "我喜欢编程，特别是Python"})
    print(f"你: 我喜欢编程，特别是Python")
    print(f"AI: {response['response']}")

    print("\n--- 对话3 - 测试记忆 ---")
    response = chain.invoke({"input": "我叫什么名字？"})
    print(f"你: 我叫什么名字？")
    print(f"AI: {response['response']}")

    print("\n--- 查看记忆 ---")
    history = memory.load_memory_variables({})
    print(f"记忆内容: {history['history']}")


def demo_summary_memory():
    """Summary Memory示例"""
    print("\n" + "=" * 60)
    print("ConversationSummaryMemory")
    print("=" * 60)

    from langchain.memory import ConversationSummaryMemory
    from langchain.chains import ConversationChain
    from langchain_core.output_parsers import StrOutputParser

    llm = get_llm()

    memory = ConversationSummaryMemory(
        llm=llm,
        memory_key="summary",
        return_messages=True
    )

    chain = ConversationChain(
        llm=llm,
        memory=memory,
        output_parser=StrOutputParser()
    )

    print("\n--- 多轮对话 ---")
    inputs = [
        "今天天气真好，我想去公园散步",
        "然后去咖啡店喝杯咖啡",
        "最后回家休息"
    ]

    for user_input in inputs:
        response = chain.invoke({"input": user_input})
        print(f"你: {user_input}")
        print(f"AI: {response['response']}")
        print()

    print("--- 查看摘要记忆 ---")
    summary = memory.load_memory_variables({})
    print(f"摘要: {summary['summary']}")


def demo_window_memory():
    """Window Memory示例"""
    print("\n" + "=" * 60)
    print("ConversationBufferWindowMemory")
    print("=" * 60)

    from langchain.memory import ConversationBufferWindowMemory
    from langchain.chains import ConversationChain
    from langchain_core.output_parsers import StrOutputParser

    llm = get_llm()

    memory = ConversationBufferWindowMemory(
        k=2,
        memory_key="history",
        return_messages=True
    )

    chain = ConversationChain(
        llm=llm,
        memory=memory,
        output_parser=StrOutputParser()
    )

    print("\n--- 添加5条对话 ---")
    for i in range(1, 6):
        user_input = f"这是第{i}条消息"
        response = chain.invoke({"input": user_input})
        print(f"对话 {i}: {user_input}")

    print("\n--- 查看窗口记忆（最近2条）---")
    history = memory.load_memory_variables({})
    messages = history["history"]
    print(f"记忆数量: {len(messages)}")
    for i, msg in enumerate(messages):
        content = msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
        print(f"  {i+1}. {content}")


def demo_entity_memory():
    """Entity Memory示例"""
    print("\n" + "=" * 60)
    print("EntityMemory")
    print("=" * 60)

    from langchain.memory import EntityMemory

    llm = get_llm()

    memory = EntityMemory(
        llm=llm,
        memory_key="entities"
    )

    print("\n--- 保存实体信息 ---")
    memory.save_context(
        {"input": "我叫李明，在Google工作，担任高级软件工程师"},
        {"output": "你好李明！很高兴认识你，Google的高级软件工程师。"}
    )

    memory.save_context(
        {"input": "我的邮箱是 liming@gmail.com"},
        {"output": "好的，我记下了，你的邮箱是 liming@gmail.com"}
    )

    print("\n--- 查看实体记忆 ---")
    entities = memory.load_memory_variables({})
    print(f"实体信息: {entities['entities']}")


def main():
    """主函数"""
    print("LangChain Memory示例（阿里百炼）\n")

    if not DASHSCOPE_API_KEY:
        print("错误: 请设置 DASHSCOPE_API_KEY 环境变量")
        return

    demo_buffer_memory()
    demo_summary_memory()
    demo_window_memory()
    demo_entity_memory()

    print("\n" + "=" * 60)
    print("Memory示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
