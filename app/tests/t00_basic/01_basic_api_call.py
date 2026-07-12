"""
阶段一：基础API调用示例
学习目标：掌握如何调用大模型API

需要掌握的技能：
- HTTP请求处理
- API认证
- 错误处理
- 响应解析
"""

import os
import requests
from typing import Optional, Dict, Any


class BasicAPIClient:
    """基础API客户端示例"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.openai.com/v1"):
        """
        初始化API客户端
        
        Args:
            api_key: API密钥，如果为None则从环境变量获取
            base_url: API基础URL
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API密钥未设置，请设置OPENAI_API_KEY环境变量")
        
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat_completion(
        self,
        messages: list,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        发送聊天完成请求
        
        Args:
            messages: 消息列表，格式为 [{"role": "user", "content": "..."}]
            model: 模型名称
            temperature: 温度参数，控制随机性
            max_tokens: 最大token数
        
        Returns:
            API响应字典
        """
        url = f"{self.base_url}/chat/completions"
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()  # 如果状态码不是200，抛出异常
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"API调用失败: {e}")
            if hasattr(e.response, 'text'):
                print(f"错误详情: {e.response.text}")
            raise
    
    def extract_content(self, response: Dict[str, Any]) -> str:
        """
        从API响应中提取内容
        
        Args:
            response: API响应字典
        
        Returns:
            模型生成的文本内容
        """
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            print(f"解析响应失败: {e}")
            print(f"响应内容: {response}")
            raise


def example_basic_call():
    """基础调用示例"""
    print("=" * 50)
    print("示例1: 基础API调用")
    print("=" * 50)
    
    # 注意：实际使用时需要设置OPENAI_API_KEY环境变量
    # export OPENAI_API_KEY="your-api-key-here"
    
    try:
        client = BasicAPIClient()
        
        messages = [
            {"role": "user", "content": "请用一句话介绍Python编程语言"}
        ]
        
        response = client.chat_completion(messages, temperature=0.7)
        content = client.extract_content(response)
        
        print(f"模型回复: {content}")
        print(f"\n完整响应结构:")
        print(f"- 模型: {response.get('model')}")
        print(f"- Token使用: {response.get('usage', {})}")
        
    except ValueError as e:
        print(f"配置错误: {e}")
        print("\n提示: 请设置OPENAI_API_KEY环境变量")
    except Exception as e:
        print(f"调用失败: {e}")


def example_conversation():
    """对话示例"""
    print("\n" + "=" * 50)
    print("示例2: 多轮对话")
    print("=" * 50)
    
    try:
        client = BasicAPIClient()
        
        # 第一轮对话
        messages = [
            {"role": "user", "content": "我的名字是张三"}
        ]
        response1 = client.chat_completion(messages)
        assistant_reply = client.extract_content(response1)
        print(f"用户: 我的名字是张三")
        print(f"助手: {assistant_reply}")
        
        # 第二轮对话（保持上下文）
        messages.append({"role": "assistant", "content": assistant_reply})
        messages.append({"role": "user", "content": "我刚才说我叫什么名字？"})
        
        response2 = client.chat_completion(messages)
        content2 = client.extract_content(response2)
        print(f"\n用户: 我刚才说我叫什么名字？")
        print(f"助手: {content2}")
        
    except Exception as e:
        print(f"调用失败: {e}")


def example_error_handling():
    """错误处理示例"""
    print("\n" + "=" * 50)
    print("示例3: 错误处理")
    print("=" * 50)
    
    # 使用错误的API密钥
    try:
        client = BasicAPIClient(api_key="invalid-key")
        messages = [{"role": "user", "content": "测试"}]
        response = client.chat_completion(messages)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP错误: {e}")
        print("这是预期的错误，演示了错误处理机制")
    except Exception as e:
        print(f"其他错误: {e}")


if __name__ == "__main__":
    print("阶段一：基础API调用学习示例\n")
    print("本示例演示了：")
    print("1. 如何初始化API客户端")
    print("2. 如何发送请求")
    print("3. 如何解析响应")
    print("4. 如何处理错误")
    print("\n注意：运行前请设置OPENAI_API_KEY环境变量\n")
    
    # 运行示例（需要有效的API密钥）
    # example_basic_call()
    # example_conversation()
    # example_error_handling()
    
    print("\n提示：取消注释上面的函数调用来运行实际示例")

