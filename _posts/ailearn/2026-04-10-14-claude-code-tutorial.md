---
layout: post
title: "【AI学习路线 14】Claude Code 使用教程 - 快捷键与实战技巧"
date: 2026-04-10
categories: ailearn
tags: [AI, Claude Code, AI编程, 快捷键, 使用教程]
keywords: Claude Code, Claude Code快捷键, Claude Code使用教程, AI编程助手, Anthropic CLI
description: AI学习路线第14篇 - 系统学习Claude Code的安装配置、快捷键、斜杠命令以及实战细节注意点
---

* content
{:toc}

> **学习顺序说明**：本文是AI学习路线的第14篇，可在完成前面学习或有编程基础后阅读：
> - ... → 12 项目实战 → 13 Vibe Coding → 14 Claude Code（本文）

Claude Code 是 Anthropic 官方发布的 CLI（命令行）AI 编程工具，深度集成到终端和 IDE，能够理解整个代码库上下文，自主完成复杂的编程任务。

## Claude Code 概述

### 与其他工具的对比

```
Cursor / Copilot：
  运行在 IDE 中，以代码补全和对话为主

Claude Code：
  运行在终端，可以直接读写文件、执行命令、管理 Git
  具备更强的代码库整体理解能力
  支持 Agent 模式自主完成多步骤任务
```

### 核心能力

| 能力 | 说明 |
|------|------|
| **代码理解** | 读取整个仓库，理解架构和依赖关系 |
| **文件操作** | 自主读写、创建、删除文件 |
| **命令执行** | 运行测试、构建、Git 等 shell 命令 |
| **多步骤规划** | 拆解复杂任务，按步骤自主完成 |
| **MCP 扩展** | 通过 MCP 协议接入外部工具和数据源 |

> **官方文档**：[Claude Code 文档](https://docs.anthropic.com/en/docs/claude-code)

---

## 第一部分：安装与启动

### 1.1 安装

```bash
# 需要 Node.js 18+
npm install -g @anthropic-ai/claude-code

# 验证安装
claude --version
```

### 1.2 启动方式

```bash
# 在项目目录中启动（最常用）
cd your-project
claude

# 直接执行一个任务后退出（非交互模式）
claude -p "帮我写一个 hello world 的 Python 脚本"

# 继续上一次会话
claude --continue

# 从文件读取输入
claude < task.txt
```

### 1.3 首次使用配置

```bash
# 登录 Anthropic 账户
claude login

# 查看当前配置
claude config list

# 设置默认模型
claude config set model claude-opus-4-6
```

---

## 第二部分：界面与交互

### 2.1 主界面布局

```
┌─────────────────────────────────────────────────────────┐
│  Claude Code  v1.x.x                      [model name]  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  > 你的输入在这里                                         │
│                                                         │
│  [Tool Use]  正在读取文件...                              │
│  [Tool Use]  正在执行命令...                              │
│                                                         │
│  Claude 的回复在这里                                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 2.2 权限确认机制

Claude Code 执行敏感操作（写文件、运行命令）前会请求确认：

```
◆ Claude wants to run:
  npm install express

  Allow? (y/n/always/never)
```

| 选项 | 含义 |
|------|------|
| `y` | 本次允许 |
| `n` | 本次拒绝 |
| `always` | 永久允许该类操作 |
| `never` | 永久拒绝该类操作 |

> **注意**：选择 `always` 后可在 settings.json 中管理已授权操作列表。

---

## 第三部分：键盘快捷键

### 3.1 输入框快捷键

| 快捷键 | 功能 |
|--------|------|
| `Enter` | 发送消息 |
| `Shift + Enter` | 换行（不发送） |
| `↑` / `↓` | 切换历史输入 |
| `Ctrl + C` | 取消当前任务（中断 Claude 正在执行的操作） |
| `Ctrl + L` | 清空终端屏幕（不清除对话上下文） |
| `Ctrl + D` | 退出 Claude Code |
| `Tab` | 自动补全斜杠命令 |

### 3.2 对话控制

| 快捷键 / 操作 | 功能 |
|--------------|------|
| `Ctrl + C`（任务执行中） | 中断当前工具调用，Claude 会停下来询问下一步 |
| `Ctrl + C`（两次快速按） | 强制退出整个会话 |
| 输入 `exit` 或 `quit` | 正常退出会话 |

### 3.3 ! 前缀直接运行 Shell

```bash
# 在 Claude Code 提示符中，以 ! 开头直接执行 shell 命令
> ! git log --oneline -5
> ! ls -la
> ! python test.py

# 适用场景：需要交互式登录或查看即时输出时
> ! gcloud auth login
> ! gh auth login
```

> **细节**：`!` 命令的输出会直接出现在对话中，Claude 可以读取并利用这些输出。

---

## 第四部分：斜杠命令（/commands）

### 4.1 常用斜杠命令速查

| 命令 | 功能 |
|------|------|
| `/help` | 查看所有可用命令和帮助 |
| `/clear` | 清除当前对话上下文（开始新对话） |
| `/compact` | 压缩对话历史，释放上下文空间 |
| `/memory` | 查看和管理持久化记忆 |
| `/model` | 切换使用的模型 |
| `/cost` | 查看当前会话的 token 消耗和费用 |
| `/status` | 查看当前会话状态 |
| `/review` | 代码审查模式 |
| `/init` | 初始化项目（生成 CLAUDE.md） |
| `/config` | 查看或修改配置 |
| `/mcp` | 管理 MCP 服务器连接 |

### 4.2 Plan 模式

```
/plan 命令（或通过 EnterPlanMode 触发）

作用：在修改代码前先制定计划，用户确认后再执行
适用场景：多文件修改、架构重构、重要功能开发

工作流：
  1. Claude 探索代码库
  2. 输出详细实施计划
  3. 用户审阅并 approve
  4. Claude 按计划执行
```

### 4.3 /compact 的正确用法

```bash
# 当对话上下文过长时使用
/compact

# Claude 会将历史对话压缩为摘要，保留关键信息
# 压缩后可继续对话，但部分细节会丢失
# 建议：任务阶段性完成后使用，不要在任务进行中途压缩
```

---

## 第五部分：CLAUDE.md 配置文件

### 5.1 作用

CLAUDE.md 是项目级别的"系统提示"，放在项目根目录（或子目录），Claude Code 启动时自动读取。

```
项目结构：
your-project/
├── CLAUDE.md          ← 根目录（全局生效）
├── src/
│   └── CLAUDE.md      ← 子目录（进入该目录时生效）
└── tests/
    └── CLAUDE.md      ← 测试目录专属规则
```

### 5.2 推荐写法

```markdown
# 项目说明
这是一个 FastAPI + React 的全栈应用，使用 PostgreSQL 数据库。

# 技术栈
- 后端：Python 3.11, FastAPI, SQLAlchemy, Alembic
- 前端：React 18, TypeScript, TailwindCSS
- 数据库：PostgreSQL 15

# 代码规范
- Python 使用 Black 格式化，行长 88 字符
- 变量命名使用 snake_case
- 所有 API 端点需要写对应的测试

# 禁止行为
- 不要修改 alembic/versions/ 目录下的迁移文件
- 不要使用 print 调试，使用 logging
- 不要提交 .env 文件

# 常用命令
- 启动开发服务器：uvicorn main:app --reload
- 运行测试：pytest tests/ -v
- 数据库迁移：alembic upgrade head
```

> **最佳实践**：CLAUDE.md 写得越具体，Claude 越能生成符合项目规范的代码。

### 5.3 /init 自动生成

```bash
# 让 Claude 分析项目后自动生成 CLAUDE.md
/init

# Claude 会读取代码库结构，生成包含：
# - 项目描述
# - 技术栈
# - 目录结构说明
# - 常用命令
```

---

## 第六部分：上下文管理

### 6.1 @ 符号引用

```bash
# 引用特定文件（Claude 会读取文件内容作为上下文）
> 帮我优化 @src/api/users.py 的查询性能

# 引用目录（Claude 会了解目录结构）
> 分析 @src/models/ 目录的数据模型设计

# 同时引用多个文件
> 参考 @src/api/users.py 和 @tests/test_users.py 写新的测试
```

### 6.2 上下文窗口管理策略

```
上下文窗口有限（Claude Sonnet/Opus 约 200K tokens）

策略：
1. 任务完成后使用 /clear 开始新对话
2. 上下文较满时用 /compact 压缩
3. 分阶段完成大任务，每阶段独立会话
4. 利用 CLAUDE.md 存储不变的项目信息（节省上下文）
5. 使用 /memory 持久化跨会话信息
```

### 6.3 上下文状态提示

```bash
# 查看当前 token 使用情况
/cost

# 输出示例：
# Input tokens:  45,231
# Output tokens: 8,102
# Total cost:    $0.23
```

---

## 第七部分：权限模式

### 7.1 三种权限模式

```bash
# 默认模式：每个敏感操作都需确认
claude

# 自动接受所有操作（危险，慎用）
claude --dangerously-skip-permissions

# 只读模式：不允许写文件或执行命令
claude --read-only
```

### 7.2 allowedTools 精细控制

在 settings.json 中配置允许的工具：

```json
{
  "allowedTools": [
    "Read",
    "Glob",
    "Grep",
    "Bash(git log:*)",
    "Bash(npm test:*)"
  ]
}
```

| 配置项 | 说明 |
|--------|------|
| `"Read"` | 允许读取文件 |
| `"Write"` | 允许写入文件 |
| `"Bash"` | 允许执行所有命令 |
| `"Bash(git *)"` | 只允许执行 git 命令 |
| `"Bash(npm test:*)"` | 只允许执行 npm test |

---

## 第八部分：MCP（Model Context Protocol）

### 8.1 什么是 MCP

MCP 是 Anthropic 推出的开放协议，允许 Claude Code 连接外部工具和数据源。

```
Claude Code ←→ MCP Server ←→ 外部系统
                              ├── 数据库
                              ├── API 服务
                              ├── 文件系统
                              ├── 浏览器
                              └── 自定义工具
```

### 8.2 配置 MCP 服务器

在 `~/.claude/settings.json` 中配置：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your-token"
      }
    }
  }
}
```

### 8.3 常用 MCP 服务器

| 服务器 | 功能 |
|--------|------|
| `@modelcontextprotocol/server-filesystem` | 扩展文件系统访问 |
| `@modelcontextprotocol/server-github` | GitHub Issues/PR 操作 |
| `@modelcontextprotocol/server-postgres` | 直接查询 PostgreSQL |
| `@modelcontextprotocol/server-puppeteer` | 控制浏览器 |
| `@modelcontextprotocol/server-slack` | 读写 Slack 消息 |

```bash
# 查看已连接的 MCP 服务器
/mcp
```

---

## 第九部分：Hooks（自动化钩子）

### 9.1 什么是 Hooks

Hooks 是在特定事件发生时自动执行的 shell 命令，无需每次手动触发。

```json
// settings.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_TOOL_RESULT_FILE_PATH"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code 完成任务'"
          }
        ]
      }
    ]
  }
}
```

### 9.2 可用 Hook 事件

| 事件 | 触发时机 |
|------|----------|
| `PreToolUse` | 工具调用前 |
| `PostToolUse` | 工具调用后 |
| `Stop` | Claude 完成回复后 |
| `SubagentStop` | 子 Agent 完成后 |

> **实用场景**：写文件后自动格式化、任务完成后发送桌面通知、自动运行 lint 检查。

---

## 第十部分：实战细节与注意点

### 10.1 提示词技巧

```bash
# 好的提示：具体、提供上下文
> 在 src/api/users.py 的 get_user 函数中，
  添加缓存逻辑，使用 Redis，缓存时间 5 分钟，
  key 格式为 "user:{user_id}"

# 不好的提示：模糊
> 给用户接口加缓存
```

```bash
# 让 Claude 先解释再修改（避免直接改错）
> 先解释一下 auth_middleware.py 的工作原理，
  然后告诉我添加 JWT 刷新逻辑的最佳位置

# 分步骤确认
> 第一步：只读取相关文件，告诉我你的修改方案
> （确认方案后）第二步：开始执行修改
```

### 10.2 多文件修改的注意点

```
注意：Claude Code 同时修改多个文件时：

1. 修改前先备份或确认 git 状态干净
   > ! git status

2. 大型重构建议使用 Plan 模式，先审查方案

3. 修改后立即运行测试
   > ! npm test 或 ! pytest

4. 如果结果不对，使用 git diff 查看变化
   > ! git diff
```

### 10.3 Git 工作流最佳实践

```bash
# Claude Code 操作前，确保工作区干净
> ! git status

# 让 Claude 帮你生成规范的提交信息
> 根据本次修改，帮我生成一个规范的 git commit message

# Claude Code 不会自动 push，需要手动确认
> ! git push origin feature/xxx
```

### 10.4 避免上下文污染

```
问题：对话越长，Claude 对早期内容的注意力越分散

解决方案：
1. 完成一个独立功能后，/clear 清除上下文
2. 不同功能的开发在不同会话中进行
3. 将项目核心约定写入 CLAUDE.md，而非依赖对话历史
4. 使用 /memory 保存跨会话的重要信息
```

### 10.5 安全注意事项

```
重要安全规则：

1. 不要在对话中粘贴真实的密钥、密码、token
   - 使用 .env 文件，让 Claude 读取变量名而非值

2. 审查 Claude 生成的 shell 命令再执行
   - 特别注意 rm、chmod、curl | bash 等危险命令

3. 生产环境操作前务必备份
   - Claude Code 的文件操作不可撤销（除非用 git）

4. --dangerously-skip-permissions 仅用于可信任的自动化场景
   - 不要在公共/共享环境中使用

5. 工具结果可能包含恶意内容（Prompt Injection）
   - 如果 Claude 突然建议执行奇怪的命令，立即停止
```

### 10.6 调试技巧

```bash
# 查看 Claude 实际读取了哪些文件
# 观察对话中的 [Tool Use] 标记

# 如果 Claude 理解出错，主动纠正
> 你误解了，我的意思是...请重新理解需求后再执行

# 让 Claude 解释它要做什么
> 在执行前，先告诉我你打算做什么，步骤是什么？

# 如果遇到循环/重复错误
> 停下来，先分析根本原因是什么？
```

### 10.7 长任务管理

```bash
# 复杂任务：明确说明验收标准
> 实现用户登录功能，要求：
  1. 支持邮箱+密码登录
  2. JWT token 有效期 7 天
  3. 密码用 bcrypt 加密
  4. 所有接口有对应测试
  5. 完成后运行 pytest 确认通过

# 中途中断任务
> Ctrl+C  ← 中断当前工具调用
然后可以：
- 继续：告诉 Claude 继续
- 调整：告诉 Claude 修改方向
- 重置：/clear 重新开始
```

---

## 第十一部分：IDE 集成

### 11.1 VS Code 扩展

```
安装 Claude Code 官方 VS Code 扩展后：
- 在 IDE 侧边栏中打开 Claude Code
- 自动同步当前打开的文件作为上下文
- 可以直接在 diff 视图中审查修改
- 快捷键 Ctrl+Esc（Mac: Cmd+Esc）打开 Claude Code 面板
```

### 11.2 JetBrains 集成

```
支持 IntelliJ IDEA、PyCharm、WebStorm 等
安装插件后功能与 VS Code 扩展类似
快捷键：Alt+Shift+C 打开 Claude Code
```

### 11.3 终端 vs IDE 的选择

| 场景 | 推荐方式 |
|------|----------|
| 多文件重构、架构变更 | 终端（完整能力） |
| 当前文件的局部修改 | IDE 扩展（更直观） |
| 运行脚本、git 操作 | 终端 |
| 代码审查、diff 查看 | IDE 扩展 |

---

## 第十二部分：常见问题

### Q1：Claude 修改了文件但结果不对，如何回滚？

```bash
# 如果之前工作区是干净的
! git diff          # 查看所有修改
! git checkout .    # 回滚所有未提交的修改
! git checkout src/specific_file.py  # 回滚单个文件
```

### Q2：上下文不够用怎么办？

```
方案 1：/compact 压缩历史
方案 2：/clear 开始新会话，并在新会话开头重新描述任务
方案 3：使用 CLAUDE.md 减少每次会话需要重复说明的内容
方案 4：切换到 claude --model claude-opus-4-6（更大上下文）
```

### Q3：Claude 一直重复犯同样的错误？

```bash
> 停止。你犯了一个反复出现的错误：[描述错误]
> 根本原因是什么？在继续之前先回答这个问题。
```

### Q4：如何让 Claude 不要修改某些文件？

```markdown
# 在 CLAUDE.md 中声明：
## 禁止修改的文件
- `config/production.yml` - 生产环境配置，只读
- `alembic/versions/` - 数据库迁移文件，不要修改已有文件
- `package-lock.json` - 依赖锁文件，不要手动修改
```

### Q5：API 费用过高怎么控制？

```bash
# 查看每次会话费用
/cost

# 节省 token 的方法：
1. 使用 /compact 压缩长对话
2. 任务完成后及时 /clear
3. 精确的提示词减少来回次数
4. 小任务用 claude-haiku-4-5（更便宜）
5. 合理使用 CLAUDE.md 减少重复描述
```

---

## 快速参考卡片

```
┌─────────────────────────────────────────────────────────┐
│              Claude Code 快速参考                         │
├──────────────────────┬──────────────────────────────────┤
│  快捷键               │  说明                             │
├──────────────────────┼──────────────────────────────────┤
│  Enter               │  发送消息                          │
│  Shift+Enter         │  换行                             │
│  Ctrl+C              │  中断任务                          │
│  Ctrl+L              │  清屏                             │
│  Ctrl+D              │  退出                             │
│  ↑ / ↓              │  历史输入                          │
│  Tab                 │  补全斜杠命令                       │
│  ! <command>         │  直接运行 Shell 命令               │
├──────────────────────┼──────────────────────────────────┤
│  斜杠命令             │  说明                             │
├──────────────────────┼──────────────────────────────────┤
│  /help               │  帮助                             │
│  /clear              │  清除上下文                        │
│  /compact            │  压缩对话历史                       │
│  /memory             │  查看记忆                          │
│  /cost               │  查看费用                          │
│  /init               │  生成 CLAUDE.md                   │
│  /model              │  切换模型                          │
│  /mcp                │  MCP 服务器管理                    │
├──────────────────────┼──────────────────────────────────┤
│  @ 引用               │  说明                             │
├──────────────────────┼──────────────────────────────────┤
│  @文件路径            │  引用文件内容                       │
│  @目录路径            │  引用目录结构                       │
└──────────────────────┴──────────────────────────────────┘
```

---

## 学习资源

- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)
- [MCP 协议文档](https://modelcontextprotocol.io/)
- [Claude Code Issues & 反馈](https://github.com/anthropics/claude-code/issues)

---

*最后更新: 2026年4月11日*
