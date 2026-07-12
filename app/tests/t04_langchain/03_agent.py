"""
LangChain Agent示例
学习目标：掌握Agent（智能体）开发和工具调用
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


def demo_define_tools():
    """工具定义示例"""
    print("\n" + "=" * 60)
    print("工具定义")
    print("=" * 60)

    from langchain_core.tools import tool

    @tool
    def get_weather(city: str) -> str:
        """获取城市天气
        Args:
            city: 城市名称，如"北京"、"上海"
        Returns:
            天气情况描述
        """
        weather_db = {
            "北京": "晴天，25°C，适宜户外活动",
            "上海": "多云，28°C，湿度较高",
            "深圳": "雨天，30°C，记得带伞",
            "杭州": "晴天，26°C，风景宜人",
        }
        return weather_db.get(city, f"抱歉，没有{city}的天气数据")

    @tool
    def calculate(expression: str) -> str:
        """计算数学表达式
        Args:
            expression: 数学表达式，如 "2+3*5"、"10/2+3"
        Returns:
            计算结果
        """
        try:
            result = eval(expression)
            return f"{expression} = {result}"
        except Exception as e:
            return f"计算错误: {e}"

    @tool
    def search_news(topic: str) -> str:
        """搜索新闻
        Args:
            topic: 新闻主题
        Returns:
            新闻列表
        """
        news_db = {
            "AI": "1. OpenAI发布GPT-5\n2. 谷歌推出Gemini 2.0\n3. Meta开源Llama 3",
            "科技": "1. 苹果发布新款iPhone\n2. 特斯拉自动驾驶新进展\n3. SpaceX完成星舰测试",
            "经济": "1. 美联储维持利率不变\n2. 中国一季度GDP增长5.3%\n3. 比特币突破10万美元",
        }
        return news_db.get(topic, f"暂无{topic}相关新闻")

    print("定义了3个工具：get_weather, calculate, search_news")
    return [get_weather, calculate, search_news]


def demo_initialize_agent(tools):
    """Agent初始化示例"""
    print("\n" + "=" * 60)
    print("Agent初始化和调用")
    print("=" * 60)

    from langchain.agents import initialize_agent, AgentType

    llm = get_llm()

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        max_iterations=5,
    )

    print("\n--- 任务1: 查询天气 ---")
    result = agent.invoke("北京今天天气怎么样？")
    print(f"结果: {result}")

    print("\n--- 任务2: 计算 ---")
    result = agent.invoke("计算 (15+25)*3 等于多少？")
    print(f"结果: {result}")

    print("\n--- 任务3: 搜索新闻 ---")
    result = agent.invoke("有什么AI新闻？")
    print(f"结果: {result}")


def demo_conversational_agent(tools):
    """对话Agent示例"""
    print("\n" + "=" * 60)
    print("对话Agent")
    print("=" * 60)

    from langchain.agents import initialize_agent, AgentType
    from langchain.memory import ConversationBufferMemory

    llm = get_llm()

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True
    )

    print("\n--- 对话1: 自我介绍 ---")
    result = agent.invoke("我叫张三，是一名AI工程师")
    print(f"结果: {result}")

    print("\n--- 对话2: 回忆名字 ---")
    result = agent.invoke("我叫什么名字？")
    print(f"结果: {result}")


def demo_multi_step_reasoning(tools):
    """多步推理示例"""
    print("\n" + "=" * 60)
    print("多步推理")
    print("=" * 60)

    from langchain.agents import initialize_agent, AgentType

    llm = get_llm()

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        max_iterations=10,
    )

    print("\n--- 多步任务: 组合使用工具 ---")
    result = agent.invoke("""
    请帮我完成以下任务：
    1. 先查询北京的天气
    2. 然后计算华氏温度
    3. 最后搜索AI相关新闻
    """)
    print(f"结果: {result}")


def main():
    """主函数"""
    print("LangChain Agent示例（阿里百炼）\n")

    if not DASHSCOPE_API_KEY:
        print("错误: 请设置 DASHSCOPE_API_KEY 环境变量")
        return

    tools = demo_define_tools()
    demo_initialize_agent(tools)
    demo_conversational_agent(tools)
    demo_multi_step_reasoning(tools)

    print("\n" + "=" * 60)
    print("Agent示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
