---
layout: post
title: "MCP协议详解 - AI与工具的标准化连接"
date: 2026-04-18
categories: ailearn
tags: [AI, MCP, 工具调用, 协议]
keywords: MCP, Model Context Protocol, Claude, 工具集成
description: 深入理解MCP协议，构建AI与工具的标准化连接
---

* content
{:toc}

> **前置知识**：需要先掌握 [AI Agent]({{ site.baseurl }}{% post_url /ailearn/06-llm-application/2026-04-16-02-ai-agent %})
>
> **本文重点**：MCP协议原理与实战开发

---

## 一、MCP概述

### 1.1 什么是MCP

```
MCP (Model Context Protocol)

由Anthropic推出的开放协议，用于：
├── 连接AI助手与外部数据源
├── 标准化工具调用接口
├── 提供上下文给AI模型
└── 实现AI应用的即插即用

核心价值：
- 一次开发，多端使用
- 标准化接口，降低集成成本
- 安全可控的数据访问
- 开放生态，社区驱动
```

### 1.2 架构设计

```
MCP架构：

┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   AI Client  │────▶│  MCP Server  │────▶│  Data Source │
│  (Claude等)   │◀────│  (工具提供者)  │◀────│  (文件/API等) │
└──────────────┘     └──────────────┘     └──────────────┘

核心概念：
1. MCP Client：AI应用（如Claude Desktop）
2. MCP Server：提供工具/资源的服务
3. Transport：通信层（stdio/SSE/WebSocket）

通信协议：
- JSON-RPC 2.0
- 双向通信
- 类型安全
```

---

## 二、MCP核心概念

### 2.1 Resources（资源）

```python
"""
Resources：提供只读数据访问

用途：
- 读取文件内容
- 获取数据库记录
- 访问API数据

特点：
- 只读访问
- URI标识
- 可订阅更新
"""

# 资源定义示例
{
    "uri": "file:///project/src/main.py",
    "name": "main.py",
    "description": "主程序入口",
    "mimeType": "text/x-python"
}
```

### 2.2 Tools（工具）

```python
"""
Tools：提供可执行的函数/操作

用途：
- 执行命令
- 调用API
- 修改数据

特点：
- 可执行操作
- 输入参数校验
- 返回执行结果
"""

# 工具定义示例
{
    "name": "search_web",
    "description": "在网络上搜索信息",
    "inputSchema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "搜索关键词"
            }
        },
        "required": ["query"]
    }
}
```

### 2.3 Prompts（提示模板）

```python
"""
Prompts：预定义的提示模板

用途：
- 常用任务模板
- 标准化工作流
- 提高效率

特点：
- 参数化模板
- 可组合
- 可分享
"""

# 提示模板示例
{
    "name": "analyze_code",
    "description": "分析代码质量",
    "arguments": [
        {
            "name": "file_path",
            "description": "要分析的文件路径",
            "required": true
        }
    ]
}
```

---

## 三、MCP Server开发

### 3.1 Python SDK

```python
# 安装SDK
# pip install mcp

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio

# 创建服务器
server = Server("example-server")

# 定义工具
@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_weather",
            description="获取指定城市的天气信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    }
                },
                "required": ["city"]
            }
        )
    ]

# 实现工具逻辑
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_weather":
        city = arguments.get("city")
        # 实际调用天气API
        weather_info = f"{city}今天晴，气温20-28℃"
        return [TextContent(type="text", text=weather_info)]
    
    raise ValueError(f"Unknown tool: {name}")

# 启动服务器
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())
```

### 3.2 TypeScript SDK

```typescript
// 安装SDK
// npm install @modelcontextprotocol/sdk

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

// 创建服务器
const server = new Server(
  { name: "example-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// 定义工具列表
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "calculate",
        description: "执行数学计算",
        inputSchema: {
          type: "object",
          properties: {
            expression: {
              type: "string",
              description: "数学表达式",
            },
          },
          required: ["expression"],
        },
      },
    ],
  };
});

// 实现工具逻辑
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "calculate") {
    const expression = request.params.arguments.expression;
    const result = eval(expression); // 注意：实际应用需要安全处理
    return {
      content: [{ type: "text", text: String(result) }],
    };
  }
  throw new Error("Unknown tool");
});

// 启动服务器
const transport = new StdioServerTransport();
await server.connect(transport);
```

### 3.3 配置文件

```json
// claude_desktop_config.json
// Claude Desktop的MCP配置

{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/projects"
      ]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your-token-here"
      }
    },
    "custom-server": {
      "command": "python",
      "args": ["/path/to/your/server.py"]
    }
  }
}
```

---

## 四、实战案例

### 4.1 文件系统MCP Server

```python
"""
文件系统MCP Server
提供文件读写能力
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Resource
import os
import json

server = Server("filesystem-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="read_file",
            description="读取文件内容",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "文件路径"}
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="write_file",
            description="写入文件内容",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "文件路径"},
                    "content": {"type": "string", "description": "文件内容"}
                },
                "required": ["path", "content"]
            }
        ),
        Tool(
            name="list_directory",
            description="列出目录内容",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "目录路径"}
                },
                "required": ["path"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    path = arguments.get("path")
    
    # 安全检查：确保路径在允许的目录内
    allowed_dir = os.environ.get("ALLOWED_DIR", "/tmp")
    if not os.path.abspath(path).startswith(allowed_dir):
        return [TextContent(type="text", text="Error: Path not allowed")]
    
    if name == "read_file":
        try:
            with open(path, 'r') as f:
                content = f.read()
            return [TextContent(type="text", text=content)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    elif name == "write_file":
        try:
            content = arguments.get("content", "")
            with open(path, 'w') as f:
                f.write(content)
            return [TextContent(type="text", text=f"Successfully wrote to {path}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    elif name == "list_directory":
        try:
            items = os.listdir(path)
            result = json.dumps(items, indent=2)
            return [TextContent(type="text", text=result)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    raise ValueError(f"Unknown tool: {name}")

# 启动服务器
if __name__ == "__main__":
    import asyncio
    asyncio.run(stdio_server(server))
```

### 4.2 数据库MCP Server

```python
"""
数据库MCP Server
提供数据库查询能力
"""

import sqlite3
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("database-server")

# 数据库连接
DB_PATH = "/path/to/database.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="query",
            description="执行SQL查询（只读）",
            inputSchema={
                "type": "object",
                "properties": {
                    "sql": {
                        "type": "string",
                        "description": "SELECT语句"
                    }
                },
                "required": ["sql"]
            }
        ),
        Tool(
            name="describe_table",
            description="获取表结构",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "表名"
                    }
                },
                "required": ["table_name"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    conn = get_connection()
    
    try:
        if name == "query":
            sql = arguments.get("sql", "")
            
            # 安全检查：只允许SELECT
            if not sql.strip().upper().startswith("SELECT"):
                return [TextContent(type="text", text="Error: Only SELECT queries allowed")]
            
            cursor = conn.execute(sql)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            
            result = {
                "columns": columns,
                "rows": rows,
                "rowCount": len(rows)
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "describe_table":
            table = arguments.get("table_name")
            cursor = conn.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            
            result = [
                {
                    "name": col[1],
                    "type": col[2],
                    "notNull": bool(col[3]),
                    "primaryKey": bool(col[5])
                }
                for col in columns
            ]
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    finally:
        conn.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(stdio_server(server))
```

### 4.3 Web搜索MCP Server

```python
"""
Web搜索MCP Server
提供网络搜索能力
"""

import aiohttp
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("web-search-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="web_search",
            description="搜索网络信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "返回结果数量",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "web_search":
        query = arguments.get("query")
        num = arguments.get("num_results", 5)
        
        # 使用搜索API（示例使用DuckDuckGo）
        async with aiohttp.ClientSession() as session:
            url = f"https://api.duckduckgo.com/?q={query}&format=json"
            async with session.get(url) as response:
                data = await response.json()
        
        # 解析结果
        results = []
        if "RelatedTopics" in data:
            for topic in data["RelatedTopics"][:num]:
                if "Text" in topic:
                    results.append({
                        "title": topic.get("Text", "")[:100],
                        "url": topic.get("FirstURL", "")
                    })
        
        return [TextContent(type="text", text=json.dumps(results, indent=2))]
    
    raise ValueError(f"Unknown tool: {name}")

if __name__ == "__main__":
    import asyncio
    import json
    asyncio.run(stdio_server(server))
```

---

## 五、MCP生态

### 5.1 官方MCP Servers

```
官方提供的MCP Servers：

文件系统
├── @modelcontextprotocol/server-filesystem
└── 文件读写、目录管理

GitHub
├── @modelcontextprotocol/server-github
└── 仓库操作、Issue、PR

Google Drive
├── @modelcontextprotocol/server-gdrive
└── 文件读取、搜索

PostgreSQL
├── @modelcontextprotocol/server-postgres
└── 数据库查询

Slack
├── @modelcontextprotocol/server-slack
└── 消息发送、频道管理

Puppeteer
├── @modelcontextprotocol/server-puppeteer
└── 网页自动化、截图
```

### 5.2 安装与使用

```bash
# 安装官方MCP Server
npm install -g @modelcontextprotocol/server-filesystem

# 配置Claude Desktop
# 编辑 ~/Library/Application Support/Claude/claude_desktop_config.json

# 重启Claude Desktop即可使用
```

### 5.3 社区MCP Servers

```
社区热门MCP Servers：

数据库类
├── mcp-server-mysql
├── mcp-server-mongodb
└── mcp-server-redis

搜索类
├── mcp-server-brave-search
├── mcp-server-google-search
└── mcp-server-tavily

云服务类
├── mcp-server-aws
├── mcp-server-azure
└── mcp-server-gcp

开发工具
├── mcp-server-docker
├── mcp-server-kubernetes
└── mcp-server-jira
```

---

## 六、最佳实践

### 6.1 安全考虑

```python
"""
MCP Server安全最佳实践：

1. 路径限制
   - 限制可访问的目录
   - 禁止访问敏感文件
   
2. 权限最小化
   - 只暴露必要的工具
   - 只读操作优先
   
3. 输入验证
   - 校验所有输入参数
   - 防止注入攻击
   
4. 错误处理
   - 不泄露敏感信息
   - 提供有用的错误提示
"""

# 安全示例
def validate_path(path: str, allowed_dirs: list) -> bool:
    """验证路径是否在允许的目录内"""
    abs_path = os.path.abspath(path)
    return any(
        abs_path.startswith(allowed_dir) 
        for allowed_dir in allowed_dirs
    )

def sanitize_sql(sql: str) -> bool:
    """验证SQL是否安全"""
    dangerous_keywords = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER"]
    upper_sql = sql.upper()
    return not any(kw in upper_sql for kw in dangerous_keywords)
```

### 6.2 性能优化

```python
"""
性能优化建议：

1. 连接池
   - 复用数据库连接
   - 复用HTTP会话
   
2. 缓存
   - 缓存频繁访问的数据
   - 设置合理的过期时间
   
3. 异步处理
   - 使用async/await
   - 并发处理多个请求
   
4. 超时控制
   - 设置合理的超时时间
   - 避免长时间阻塞
"""

import asyncio
from functools import lru_cache

# 缓存示例
@lru_cache(maxsize=100)
def get_table_schema(table_name: str) -> dict:
    """缓存表结构查询"""
    # ...

# 超时控制示例
async def query_with_timeout(sql: str, timeout: float = 5.0):
    """带超时的查询"""
    try:
        return await asyncio.wait_for(
            execute_query(sql),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        return {"error": "Query timeout"}
```

---

## 参考资源

> - [MCP官网](https://modelcontextprotocol.io/) - 官方文档
> - [MCP规范](https://spec.modelcontextprotocol.io/) - 协议规范
> - [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) - Python开发包
> - [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) - TypeScript开发包
> - [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers) - 社区资源
> - [Claude Desktop](https://claude.ai/download) - 支持MCP的客户端

---

**上一篇**：[Cursor AI编辑器]({{ site.baseurl }}{% post_url /ailearn/08-ai-tools/2026-04-18-02-cursor-guide %})

**返回**：[AI工具链]({{ site.baseurl }}{% post_url /ailearn/2026-04-10-08-ai-tools %})

*最后更新: 2026年4月18日*
