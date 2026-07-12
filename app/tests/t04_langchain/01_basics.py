"""
LangChain基础操作示例
学习目标：掌握LangChain的基本组件和用法
"""

import os

# 优先从 .env 加载，如果存在且 python-dotenv 可用
try:
    from dotenv import load_dotenv
    # 尝试加载项目根目录的 .env 文件
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
except ImportError:
    pass

DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")


def basic_llm_call():
    """基础LLM调用（阿里百炼）"""
    print("=" * 60)
    print("基础LLM调用（阿里百炼）")
    print("=" * 60)

    if not DASHSCOPE_API_KEY:
        print("错误: 请设置 DASHSCOPE_API_KEY 环境变量")
        return

    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        model="qwen-plus",  # qwen-plus 性价比更高
        temperature=0.7,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/",
        api_key=DASHSCOPE_API_KEY,
    )

    response = llm.invoke("你好，请介绍一下你自己")
    print(f"回复: {response.content}")


def prompt_template_demo():
    """Prompt模板示例"""
    print("\n" + "=" * 60)
    print("Prompt模板")
    print("=" * 60)

    from langchain_core.prompts import PromptTemplate

    # 简单模板
    prompt = PromptTemplate.from_template("请回答以下问题：{question}")
    result = prompt.invoke({"question": "什么是人工智能？"})
    print(result)

    # 带 Few-shot 的模板
    prompt = PromptTemplate.from_template(
        """请根据以下示例回答问题：

示例：
问题：苹果是什么？
回答：苹果是一种水果。

问题：{question}
回答："""
    )
    result = prompt.invoke({"question": "天空是什么？"})
    print(result)


def chain_example():
    """Chain组合示例"""
    print("\n" + "=" * 60)
    print("Chain组合")
    print("=" * 60)

    if not DASHSCOPE_API_KEY:
        print("错误: 请设置 DASHSCOPE_API_KEY 环境变量")
        return

    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    llm = ChatOpenAI(
        model="qwen-plus",
        temperature=0.7,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/",
        api_key=DASHSCOPE_API_KEY,
    )

    prompt = PromptTemplate.from_template(
        "请用一句话介绍{topic}"
    )

    # 使用 | 符号组合Chain
    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({"topic": "人工智能"})
    print(f"结果: {result}")


def output_parser_example():
    """输出解析示例"""
    print("\n" + "=" * 60)
    print("输出解析")
    print("=" * 60)

    if not DASHSCOPE_API_KEY:
        print("错误: 请设置 DASHSCOPE_API_KEY 环境变量")
        return

    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import JsonOutputParser
    from pydantic import BaseModel

    llm = ChatOpenAI(
        model="qwen-plus",
        temperature=0.7,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/",
        api_key=DASHSCOPE_API_KEY,
    )

    # 定义输出结构
    class Answer(BaseModel):
        topic: str
        description: str

    parser = JsonOutputParser(pydantic_schema=Answer)

    prompt = PromptTemplate.from_template(
        "请介绍{topic}，并以JSON格式输出，包含topic和description字段"
    )

    chain = prompt | llm | parser
    result = chain.invoke({"topic": "机器学习"})
    print(f"结果: {result}")


def main():
    """主函数"""
    print("LangChain基础操作示例\n")
    print("使用阿里百炼 API")
    print("API Key:", "已设置" if DASHSCOPE_API_KEY else "未设置！请在 .env 文件中设置\n")

    basic_llm_call()
    prompt_template_demo()
    chain_example()
    output_parser_example()


if __name__ == "__main__":
    main()