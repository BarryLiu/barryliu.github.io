"""
阶段四：Agent开发示例
学习目标：掌握Agent系统的构建

需要掌握的技能：
- 理解Agent工作原理
- ReAct模式实现
- Tool使用与Function Calling
- Agent循环与决策
- 多Agent协作
"""

from typing import List, Dict, Any, Callable, Optional
from enum import Enum
import json


class AgentState(Enum):
    """Agent状态"""
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    OBSERVING = "observing"
    COMPLETED = "completed"
    ERROR = "error"


class Tool:
    """工具基类"""
    
    def __init__(self, name: str, description: str, func: Callable):
        """
        初始化工具
        
        Args:
            name: 工具名称
            description: 工具描述
            func: 工具函数
        """
        self.name = name
        self.description = description
        self.func = func
    
    def execute(self, **kwargs) -> Any:
        """
        执行工具
        
        Args:
            **kwargs: 工具参数
        
        Returns:
            工具执行结果
        """
        try:
            return self.func(**kwargs)
        except Exception as e:
            return f"工具执行错误: {str(e)}"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（用于Function Calling）"""
        return {
            "name": self.name,
            "description": self.description,
            # 实际应用中需要定义完整的参数schema
        }


class SimpleAgent:
    """简单的Agent实现"""
    
    def __init__(self, name: str, tools: List[Tool] = None):
        """
        初始化Agent
        
        Args:
            name: Agent名称
            tools: 可用工具列表
        """
        self.name = name
        self.tools = tools or []
        self.state = AgentState.IDLE
        self.memory: List[Dict[str, Any]] = []
        self.current_task: Optional[str] = None
    
    def think(self, observation: str) -> str:
        """
        思考阶段（Reasoning）
        
        Args:
            observation: 当前观察
        
        Returns:
            思考结果/下一步行动
        """
        self.state = AgentState.THINKING
        
        # 实际应用中，这里会调用LLM进行推理
        # 这里使用简化的逻辑演示
        
        # 分析是否需要使用工具
        for tool in self.tools:
            if tool.name.lower() in observation.lower():
                return f"需要使用工具: {tool.name}"
        
        # 分析任务是否完成
        if "完成" in observation or "结果" in observation:
            return "任务已完成"
        
        return "继续执行任务"
    
    def act(self, action: str) -> Dict[str, Any]:
        """
        行动阶段（Acting）
        
        Args:
            action: 要执行的动作
        
        Returns:
            行动结果
        """
        self.state = AgentState.ACTING
        
        # 解析动作，决定使用哪个工具
        for tool in self.tools:
            if tool.name in action:
                # 提取参数（简化处理）
                result = tool.execute()
                return {
                    "tool": tool.name,
                    "result": result,
                    "success": True
                }
        
        # 如果没有匹配的工具，返回默认响应
        return {
            "tool": None,
            "result": "未找到合适的工具",
            "success": False
        }
    
    def observe(self, action_result: Dict[str, Any]) -> str:
        """
        观察阶段（Observing）
        
        Args:
            action_result: 行动结果
        
        Returns:
            观察描述
        """
        self.state = AgentState.OBSERVING
        
        if action_result.get("success"):
            return f"工具 {action_result.get('tool')} 执行成功: {action_result.get('result')}"
        else:
            return f"行动未成功: {action_result.get('result')}"
    
    def react_cycle(self, task: str, max_iterations: int = 5) -> str:
        """
        ReAct循环：Reasoning + Acting
        
        Args:
            task: 任务描述
            max_iterations: 最大迭代次数
        
        Returns:
            最终结果
        """
        self.current_task = task
        self.state = AgentState.IDLE
        observation = f"任务: {task}"
        
        print(f"\nAgent {self.name} 开始执行任务: {task}")
        print("-" * 60)
        
        for iteration in range(max_iterations):
            print(f"\n迭代 {iteration + 1}:")
            
            # 思考
            thought = self.think(observation)
            print(f"思考: {thought}")
            self.memory.append({"iteration": iteration + 1, "thought": thought})
            
            # 判断是否完成
            if "完成" in thought:
                self.state = AgentState.COMPLETED
                print(f"\n任务完成！")
                return "任务已完成"
            
            # 行动
            action_result = self.act(thought)
            print(f"行动: {action_result}")
            
            # 观察
            observation = self.observe(action_result)
            print(f"观察: {observation}")
            
            if not action_result.get("success"):
                self.state = AgentState.ERROR
                return f"任务失败: {observation}"
        
        self.state = AgentState.ERROR
        return "达到最大迭代次数，任务未完成"


# 示例工具
def calculator(operation: str, a: float, b: float) -> float:
    """计算器工具"""
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else float('inf')
    }
    op_func = operations.get(operation.lower())
    if op_func:
        return op_func(a, b)
    return 0


def search_knowledge_base(query: str) -> str:
    """知识库搜索工具"""
    # 简化的知识库
    kb = {
        "python": "Python是一种高级编程语言",
        "ai": "人工智能是计算机科学的一个分支",
        "ml": "机器学习是AI的子领域"
    }
    
    query_lower = query.lower()
    for key, value in kb.items():
        if key in query_lower:
            return value
    return "未找到相关信息"


def demonstrate_basic_agent():
    """演示基础Agent"""
    print("=" * 60)
    print("基础Agent示例")
    print("=" * 60)
    
    # 创建工具
    tools = [
        Tool("calculator", "执行数学计算", calculator),
        Tool("search", "搜索知识库", search_knowledge_base)
    ]
    
    # 创建Agent
    agent = SimpleAgent("助手", tools=tools)
    
    # 执行任务
    result = agent.react_cycle("计算 10 + 5 的结果")
    print(f"\n最终结果: {result}")


class MultiAgentSystem:
    """多Agent系统"""
    
    def __init__(self):
        """初始化多Agent系统"""
        self.agents: Dict[str, SimpleAgent] = {}
        self.message_queue: List[Dict[str, Any]] = []
    
    def add_agent(self, agent: SimpleAgent):
        """添加Agent"""
        self.agents[agent.name] = agent
    
    def send_message(self, from_agent: str, to_agent: str, message: str):
        """发送消息"""
        self.message_queue.append({
            "from": from_agent,
            "to": to_agent,
            "message": message,
            "timestamp": len(self.message_queue)
        })
    
    def process_messages(self):
        """处理消息队列"""
        for msg in self.message_queue:
            to_agent = self.agents.get(msg["to"])
            if to_agent:
                print(f"\n消息: {msg['from']} -> {msg['to']}: {msg['message']}")
                # 实际应用中，Agent会根据消息更新状态或执行任务
        self.message_queue.clear()


def demonstrate_multi_agent():
    """演示多Agent系统"""
    print("\n" + "=" * 60)
    print("多Agent系统示例")
    print("=" * 60)
    
    system = MultiAgentSystem()
    
    # 创建不同类型的Agent
    research_agent = SimpleAgent("研究员", [])
    writer_agent = SimpleAgent("写作者", [])
    reviewer_agent = SimpleAgent("审查员", [])
    
    system.add_agent(research_agent)
    system.add_agent(writer_agent)
    system.add_agent(reviewer_agent)
    
    # Agent协作流程
    print("\n模拟Agent协作:")
    system.send_message("研究员", "写作者", "研究完成，请撰写报告")
    system.send_message("写作者", "审查员", "报告已撰写，请审查")
    system.send_message("审查员", "写作者", "审查通过，可以发布")
    
    system.process_messages()


def agent_best_practices():
    """Agent开发最佳实践"""
    print("\n" + "=" * 60)
    print("Agent开发最佳实践")
    print("=" * 60)
    
    practices = [
        {
            "要点": "明确Agent职责",
            "说明": "每个Agent应该有明确的职责范围",
            "建议": [
                "单一职责原则",
                "避免功能重叠",
                "清晰的输入输出定义"
            ]
        },
        {
            "要点": "工具设计",
            "说明": "设计好用且安全的工具",
            "建议": [
                "工具功能明确",
                "参数验证",
                "错误处理",
                "工具描述清晰（用于Function Calling）"
            ]
        },
        {
            "要点": "状态管理",
            "说明": "合理管理Agent状态",
            "建议": [
                "跟踪执行状态",
                "保存历史记录",
                "处理异常情况",
                "支持状态恢复"
            ]
        },
        {
            "要点": "循环控制",
            "说明": "避免无限循环",
            "建议": [
                "设置最大迭代次数",
                "定义终止条件",
                "超时处理",
                "成本控制"
            ]
        },
        {
            "要点": "多Agent协作",
            "说明": "设计清晰的协作机制",
            "建议": [
                "定义通信协议",
                "消息队列管理",
                "任务分配策略",
                "冲突解决机制"
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
    print("阶段四：Agent开发学习示例\n")
    
    demonstrate_basic_agent()
    demonstrate_multi_agent()
    agent_best_practices()
    
    print("\n" + "=" * 60)
    print("学习要点总结")
    print("=" * 60)
    print("""
1. Agent核心概念：
   - Agent = 感知 + 思考 + 行动
   - ReAct模式：Reasoning + Acting循环
   - 工具使用扩展Agent能力

2. 关键组件：
   - 工具系统（Tools）
   - 状态管理（State）
   - 记忆系统（Memory）
   - 决策逻辑（Reasoning）

3. 开发流程：
   - 定义Agent职责
   - 设计工具接口
   - 实现ReAct循环
   - 测试和优化

4. 多Agent系统：
   - Agent间通信
   - 任务分解与分配
   - 协作机制设计
   - 冲突处理

5. 实际应用：
   - 使用LangChain、LlamaIndex等框架
   - 集成Function Calling
   - 实现复杂的Agent系统
    """)

