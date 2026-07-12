"""
阶段二：Prompt工程示例
学习目标：掌握如何设计有效的Prompt

需要掌握的技能：
- 编写清晰的指令
- Few-shot示例
- 角色设定
- 输出格式控制
- Chain-of-Thought提示
"""

from typing import List, Dict, Any
import json


class PromptExamples:
    """Prompt工程示例集合"""
    
    @staticmethod
    def basic_instruction() -> List[Dict[str, str]]:
        """
        示例1: 基础指令Prompt
        
        技能点：
        - 明确的任务描述
        - 清晰的输出要求
        """
        return [
            {
                "role": "user",
                "content": "请将以下文本翻译成英文：\n\n你好，世界！"
            }
        ]
    
    @staticmethod
    def few_shot_example() -> List[Dict[str, str]]:
        """
        示例2: Few-shot示例
        
        技能点：
        - 提供示例让模型学习模式
        - 通过示例展示期望的输出格式
        """
        return [
            {
                "role": "user",
                "content": """请根据以下示例，将情感分类：

示例1:
输入: 今天天气真好！
输出: 积极

示例2:
输入: 这个电影太无聊了。
输出: 消极

现在请分类：
输入: 我很喜欢这个产品
输出:"""
            }
        ]
    
    @staticmethod
    def role_playing() -> List[Dict[str, str]]:
        """
        示例3: 角色设定
        
        技能点：
        - 通过角色设定引导模型行为
        - 让模型以特定身份回答问题
        """
        return [
            {
                "role": "system",
                "content": "你是一位经验丰富的Python编程导师，擅长用简单易懂的方式解释复杂概念。"
            },
            {
                "role": "user",
                "content": "请解释什么是装饰器（decorator）？"
            }
        ]
    
    @staticmethod
    def structured_output() -> List[Dict[str, str]]:
        """
        示例4: 结构化输出
        
        技能点：
        - 指定输出格式（JSON、XML等）
        - 确保输出可解析
        """
        return [
            {
                "role": "user",
                "content": """请分析以下文本的情感，并以JSON格式输出：

文本: "这个产品非常好用，强烈推荐！"

要求输出格式：
{
    "sentiment": "积极/消极/中性",
    "confidence": 0.0-1.0之间的浮点数,
    "keywords": ["关键词1", "关键词2"]
}"""
            }
        ]
    
    @staticmethod
    def chain_of_thought() -> List[Dict[str, str]]:
        """
        示例5: Chain-of-Thought（思维链）
        
        技能点：
        - 引导模型展示推理过程
        - 提高复杂问题的准确性
        """
        return [
            {
                "role": "user",
                "content": """请解决以下数学问题，并展示你的思考过程：

问题: 一个班级有30个学生，其中60%是女生。如果班级又来了10个学生，其中5个是女生，那么现在班级中女生的比例是多少？

请按以下步骤思考：
1. 先计算初始女生人数
2. 计算新来的学生后的总人数和女生人数
3. 计算最终比例"""
            }
        ]
    
    @staticmethod
    def multi_step_task() -> List[Dict[str, str]]:
        """
        示例6: 多步骤任务
        
        技能点：
        - 将复杂任务分解为步骤
        - 明确每个步骤的要求
        """
        return [
            {
                "role": "user",
                "content": """请帮我完成以下任务：

任务: 分析一篇技术文章

步骤：
1. 提取文章的主要观点（3-5个）
2. 识别文章的目标受众
3. 评估文章的技术深度（初级/中级/高级）
4. 给出改进建议

文章内容：
[这里放置文章内容]"""
            }
        ]


class PromptOptimizer:
    """Prompt优化工具类"""
    
    @staticmethod
    def add_constraints(prompt: str, constraints: List[str]) -> str:
        """
        为Prompt添加约束条件
        
        Args:
            prompt: 原始Prompt
            constraints: 约束条件列表
        
        Returns:
            优化后的Prompt
        """
        constraints_text = "\n".join([f"- {c}" for c in constraints])
        return f"""{prompt}

约束条件：
{constraints_text}"""
    
    @staticmethod
    def add_examples(prompt: str, examples: List[Dict[str, str]]) -> str:
        """
        为Prompt添加示例
        
        Args:
            prompt: 原始Prompt
            examples: 示例列表，格式为 [{"input": "...", "output": "..."}]
        
        Returns:
            优化后的Prompt
        """
        examples_text = "\n\n".join([
            f"示例{i+1}:\n输入: {ex['input']}\n输出: {ex['output']}"
            for i, ex in enumerate(examples)
        ])
        return f"""{prompt}

示例：
{examples_text}"""
    
    @staticmethod
    def format_for_json(prompt: str, schema: Dict[str, Any]) -> str:
        """
        格式化Prompt以输出JSON
        
        Args:
            prompt: 原始Prompt
            schema: JSON Schema定义
        
        Returns:
            优化后的Prompt
        """
        schema_str = json.dumps(schema, indent=2, ensure_ascii=False)
        return f"""{prompt}

请以JSON格式输出，格式如下：
```json
{schema_str}
```"""


def demonstrate_prompt_examples():
    """演示各种Prompt示例"""
    print("=" * 60)
    print("Prompt工程示例演示")
    print("=" * 60)
    
    examples = PromptExamples()
    
    print("\n1. 基础指令Prompt:")
    print("-" * 60)
    for msg in examples.basic_instruction():
        print(f"{msg['role']}: {msg['content']}")
    
    print("\n2. Few-shot示例:")
    print("-" * 60)
    for msg in examples.few_shot_example():
        print(f"{msg['role']}: {msg['content'][:100]}...")
    
    print("\n3. 角色设定:")
    print("-" * 60)
    for msg in examples.role_playing():
        print(f"{msg['role']}: {msg['content']}")
    
    print("\n4. 结构化输出:")
    print("-" * 60)
    for msg in examples.structured_output():
        print(f"{msg['role']}: {msg['content'][:150]}...")
    
    print("\n5. Chain-of-Thought:")
    print("-" * 60)
    for msg in examples.chain_of_thought():
        print(f"{msg['role']}: {msg['content'][:150]}...")


def demonstrate_optimization():
    """演示Prompt优化"""
    print("\n" + "=" * 60)
    print("Prompt优化示例")
    print("=" * 60)
    
    optimizer = PromptOptimizer()
    
    # 原始Prompt
    original = "请写一篇关于人工智能的文章"
    
    print("\n原始Prompt:")
    print(original)
    
    # 添加约束
    constraints = [
        "字数控制在500字以内",
        "面向技术初学者",
        "包含实际应用案例"
    ]
    optimized = optimizer.add_constraints(original, constraints)
    
    print("\n添加约束后:")
    print(optimized)
    
    # 添加示例
    examples = [
        {"input": "主题：机器学习", "output": "[示例文章内容]"}
    ]
    optimized_with_examples = optimizer.add_examples(original, examples)
    
    print("\n添加示例后:")
    print(optimized_with_examples[:200] + "...")


def prompt_best_practices():
    """Prompt最佳实践"""
    print("\n" + "=" * 60)
    print("Prompt设计最佳实践")
    print("=" * 60)
    
    practices = [
        {
            "原则": "明确性",
            "说明": "使用清晰、具体的指令，避免歧义",
            "示例": "❌ 不好: '分析这个'\n✅ 好: '分析以下文本的情感倾向，并给出置信度'"
        },
        {
            "原则": "结构化",
            "说明": "使用列表、步骤、格式来组织Prompt",
            "示例": "使用编号列表、分隔符、明确的格式要求"
        },
        {
            "原则": "提供上下文",
            "说明": "给出足够的背景信息",
            "示例": "说明任务背景、目标受众、使用场景"
        },
        {
            "原则": "示例引导",
            "说明": "通过Few-shot示例展示期望的输出",
            "示例": "提供2-3个高质量的输入输出示例"
        },
        {
            "原则": "迭代优化",
            "说明": "根据结果不断改进Prompt",
            "示例": "测试不同版本，记录效果，持续优化"
        }
    ]
    
    for i, practice in enumerate(practices, 1):
        print(f"\n{i}. {practice['原则']}")
        print(f"   说明: {practice['说明']}")
        print(f"   示例: {practice['示例']}")


if __name__ == "__main__":
    print("阶段二：Prompt工程学习示例\n")
    
    demonstrate_prompt_examples()
    demonstrate_optimization()
    prompt_best_practices()
    
    print("\n" + "=" * 60)
    print("学习要点总结")
    print("=" * 60)
    print("""
1. 好的Prompt应该：
   - 明确具体
   - 结构清晰
   - 提供足够的上下文
   - 包含示例（如需要）
   - 指定输出格式

2. 常见技巧：
   - 使用系统消息设定角色
   - 通过Few-shot示例引导
   - 使用Chain-of-Thought提高准确性
   - 明确指定输出格式

3. 优化方法：
   - 从简单开始，逐步细化
   - 测试不同版本
   - 根据结果迭代改进
    """)

