"""
阶段六：部署与生产实践示例
学习目标：掌握AI应用的部署和优化

需要掌握的技能：
- Web框架使用
- API服务设计
- 错误处理与日志
- 性能优化
- 监控与追踪
"""

from typing import Optional, Dict, Any
import time
import logging
from datetime import datetime


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class APIService:
    """API服务示例（模拟FastAPI风格）"""
    
    def __init__(self):
        """初始化API服务"""
        self.request_count = 0
        self.error_count = 0
        self.response_times = []
    
    def log_request(self, endpoint: str, method: str):
        """记录请求"""
        self.request_count += 1
        logger.info(f"请求: {method} {endpoint} (总请求数: {self.request_count})")
    
    def log_error(self, endpoint: str, error: Exception):
        """记录错误"""
        self.error_count += 1
        logger.error(f"错误: {endpoint} - {str(error)} (总错误数: {self.error_count})")
    
    def track_response_time(self, start_time: float):
        """追踪响应时间"""
        elapsed = time.time() - start_time
        self.response_times.append(elapsed)
        return elapsed
    
    def chat_endpoint(self, message: str, model: str = "gpt-3.5-turbo") -> Dict[str, Any]:
        """
        聊天接口示例
        
        Args:
            message: 用户消息
            model: 模型名称
        
        Returns:
            API响应
        """
        start_time = time.time()
        self.log_request("/chat", "POST")
        
        try:
            # 模拟API调用
            # 实际应用中：response = call_llm_api(message, model)
            response_text = f"这是对 '{message}' 的回复（使用模型 {model}）"
            
            elapsed = self.track_response_time(start_time)
            
            return {
                "success": True,
                "data": {
                    "message": response_text,
                    "model": model,
                    "timestamp": datetime.now().isoformat()
                },
                "metadata": {
                    "response_time": f"{elapsed:.3f}s",
                    "request_id": f"req_{self.request_count}"
                }
            }
        
        except Exception as e:
            self.log_error("/chat", e)
            elapsed = self.track_response_time(start_time)
            
            return {
                "success": False,
                "error": str(e),
                "metadata": {
                    "response_time": f"{elapsed:.3f}s",
                    "request_id": f"req_{self.request_count}"
                }
            }
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查接口"""
        avg_response_time = (
            sum(self.response_times[-100:]) / len(self.response_times[-100:])
            if self.response_times else 0
        )
        
        return {
            "status": "healthy",
            "metrics": {
                "total_requests": self.request_count,
                "total_errors": self.error_count,
                "error_rate": f"{self.error_count / self.request_count * 100:.2f}%" if self.request_count > 0 else "0%",
                "avg_response_time": f"{avg_response_time:.3f}s",
                "uptime": "运行中"
            }
        }


class RateLimiter:
    """简单的速率限制器"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        """
        初始化速率限制器
        
        Args:
            max_requests: 时间窗口内最大请求数
            window_seconds: 时间窗口（秒）
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = []
    
    def is_allowed(self) -> bool:
        """
        检查是否允许请求
        
        Returns:
            是否允许
        """
        now = time.time()
        
        # 清理过期请求
        self.requests = [req_time for req_time in self.requests if now - req_time < self.window_seconds]
        
        # 检查是否超过限制
        if len(self.requests) >= self.max_requests:
            return False
        
        # 记录新请求
        self.requests.append(now)
        return True
    
    def get_remaining(self) -> int:
        """获取剩余请求数"""
        return max(0, self.max_requests - len(self.requests))


class Cache:
    """简单的缓存实现"""
    
    def __init__(self, ttl_seconds: int = 3600):
        """
        初始化缓存
        
        Args:
            ttl_seconds: 缓存过期时间（秒）
        """
        self.cache: Dict[str, tuple] = {}  # {key: (value, expire_time)}
        self.ttl = ttl_seconds
    
    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存值
        
        Args:
            key: 缓存键
        
        Returns:
            缓存值，如果不存在或过期则返回None
        """
        if key not in self.cache:
            return None
        
        value, expire_time = self.cache[key]
        
        if time.time() > expire_time:
            del self.cache[key]
            return None
        
        return value
    
    def set(self, key: str, value: Any):
        """
        设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值
        """
        expire_time = time.time() + self.ttl
        self.cache[key] = (value, expire_time)
    
    def clear(self):
        """清空缓存"""
        self.cache.clear()


def demonstrate_api_service():
    """演示API服务"""
    print("=" * 60)
    print("API服务示例")
    print("=" * 60)
    
    service = APIService()
    
    # 模拟多个请求
    print("\n模拟API请求:")
    print("-" * 60)
    
    for i in range(3):
        response = service.chat_endpoint(f"测试消息 {i+1}")
        print(f"\n请求 {i+1}:")
        print(f"  成功: {response['success']}")
        print(f"  响应时间: {response['metadata']['response_time']}")
        if response['success']:
            print(f"  回复: {response['data']['message']}")
    
    # 健康检查
    print("\n健康检查:")
    print("-" * 60)
    health = service.health_check()
    print(f"状态: {health['status']}")
    for key, value in health['metrics'].items():
        print(f"  {key}: {value}")


def demonstrate_rate_limiting():
    """演示速率限制"""
    print("\n" + "=" * 60)
    print("速率限制示例")
    print("=" * 60)
    
    limiter = RateLimiter(max_requests=5, window_seconds=60)
    
    print("\n模拟请求（限制: 5次/分钟）:")
    print("-" * 60)
    
    for i in range(7):
        allowed = limiter.is_allowed()
        remaining = limiter.get_remaining()
        
        status = "✓ 允许" if allowed else "✗ 拒绝"
        print(f"请求 {i+1}: {status} (剩余: {remaining})")


def demonstrate_caching():
    """演示缓存"""
    print("\n" + "=" * 60)
    print("缓存示例")
    print("=" * 60)
    
    cache = Cache(ttl_seconds=5)  # 5秒过期
    
    print("\n缓存操作:")
    print("-" * 60)
    
    # 设置缓存
    cache.set("user:123", {"name": "张三", "age": 30})
    print("设置缓存: user:123")
    
    # 获取缓存
    value = cache.get("user:123")
    print(f"获取缓存: {value}")
    
    # 等待过期
    print("\n等待6秒后...")
    time.sleep(6)
    
    value = cache.get("user:123")
    print(f"获取缓存（已过期）: {value}")


def deployment_best_practices():
    """部署最佳实践"""
    print("\n" + "=" * 60)
    print("部署最佳实践")
    print("=" * 60)
    
    practices = [
        {
            "要点": "API设计",
            "说明": "设计清晰、一致的API接口",
            "建议": [
                "使用RESTful风格",
                "统一的响应格式",
                "版本控制（/v1/, /v2/）",
                "清晰的错误码"
            ]
        },
        {
            "要点": "错误处理",
            "说明": "完善的错误处理机制",
            "建议": [
                "捕获所有异常",
                "返回有意义的错误信息",
                "记录详细日志",
                "避免泄露敏感信息"
            ]
        },
        {
            "要点": "性能优化",
            "说明": "提高服务性能",
            "建议": [
                "使用缓存减少API调用",
                "异步处理长时间任务",
                "批量处理请求",
                "连接池管理"
            ]
        },
        {
            "要点": "安全性",
            "说明": "保护API和服务",
            "建议": [
                "API密钥管理",
                "速率限制",
                "输入验证",
                "HTTPS加密"
            ]
        },
        {
            "要点": "监控与日志",
            "说明": "追踪服务状态",
            "建议": [
                "记录关键指标",
                "错误追踪",
                "性能监控",
                "成本追踪"
            ]
        },
        {
            "要点": "可扩展性",
            "说明": "支持服务扩展",
            "建议": [
                "无状态设计",
                "负载均衡",
                "水平扩展",
                "数据库优化"
            ]
        }
    ]
    
    for practice in practices:
        print(f"\n{practice['要点']}")
        print(f"说明: {practice['说明']}")
        print("建议:")
        for suggestion in practice['建议']:
            print(f"  - {suggestion}")


def deployment_checklist():
    """部署检查清单"""
    print("\n" + "=" * 60)
    print("部署检查清单")
    print("=" * 60)
    
    checklist = [
        "✓ 代码审查和测试",
        "✓ 环境变量配置",
        "✓ 依赖管理",
        "✓ 日志系统",
        "✓ 错误处理",
        "✓ 健康检查接口",
        "✓ 速率限制",
        "✓ 监控和告警",
        "✓ 文档完善",
        "✓ 安全审计",
        "✓ 性能测试",
        "✓ 备份策略"
    ]
    
    for item in checklist:
        print(f"  {item}")


if __name__ == "__main__":
    print("阶段六：部署与生产实践学习示例\n")
    
    demonstrate_api_service()
    demonstrate_rate_limiting()
    demonstrate_caching()
    deployment_best_practices()
    deployment_checklist()
    
    print("\n" + "=" * 60)
    print("学习要点总结")
    print("=" * 60)
    print("""
1. API服务设计：
   - 清晰的接口定义
   - 统一的响应格式
   - 完善的错误处理

2. 性能优化：
   - 缓存策略
   - 异步处理
   - 批量操作
   - 连接复用

3. 安全措施：
   - API密钥管理
   - 速率限制
   - 输入验证
   - 访问控制

4. 监控运维：
   - 日志记录
   - 性能指标
   - 错误追踪
   - 健康检查

5. 部署实践：
   - 容器化（Docker）
   - 云平台部署
   - CI/CD流程
   - 灰度发布
    """)

