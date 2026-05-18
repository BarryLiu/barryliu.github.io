# Claude Code 高级操作指南

> Claude Code 是一款由 Anthropic 开发的 AI 编程助手，旨在帮助开发者更高效地完成编码任务。本文将介绍一些 Claude Code 的高级操作技巧，让你更好地利用这个强大的工具。

## 1. 智能体与任务规划

### 1.1 使用 Plan 模式进行复杂任务规划

当面对复杂的实现任务时，使用 Plan 模式可以让你在编写代码前先理清思路：

```
/plan
```

Plan 模式会帮助你：
- 分析代码库结构
- 设计实现方案
- 识别关键文件和依赖
- 提供分步骤的实施计划

### 1.2 委托子任务给专业智能体

Claude Code 支持启动子智能体来处理特定任务：

```
Agent({
  description: "代码审查任务",
  subagent_type: "code-reviewer",
  prompt: "审查 migration_0042_user_schema.sql 文件的安全性..."
})
```

适合场景：
- 并行研究多个问题
- 代码审查和性能分析
- 复杂的多步骤搜索任务

## 2. 高效代码编辑

### 2.1 精准编辑操作

```javascript
// 使用精确上下文编辑
Edit({
  file_path: "/path/to/file.js",
  old_string: "function oldFunction() { ... }",
  new_string: "function newFunction() { ... }"
})

// 使用 replace_all 进行全局替换
Edit({
  file_path: "/path/to/file.js",
  old_string: "oldValue",
  new_string: "newValue",
  replace_all: true
})
```

### 2.2 多文件协同编辑

Claude Code 可以同时处理多个文件：

1. **读取多个文件获取上下文**
2. **批量编辑相关文件**
3. **自动追踪文件间的依赖关系**

### 2.3 代码重写与简化

使用 `/simplify` 命令可以：
- 审查代码复用性和质量
- 识别代码重复
- 提出优化建议
- 修复发现的问题

## 3. 搜索与导航

### 3.1 强大的搜索能力

```javascript
// 搜索文件名
Glob({ pattern: "**/*.tsx" })

// 搜索文件内容
Grep({
  output_mode: "content",
  path: "/src",
  pattern: "API.*endpoints"
})

// 搜索特定类型的文件
Grep({
  pattern: "function\\s+\\w+",
  type: "js"
})
```

### 3.2 上下文感知搜索

- 支持正则表达式
- 可以限制搜索范围
- 高亮显示匹配结果
- 显示行号便于导航

## 4. Git 操作

### 4.1 安全的 Git 工作流

Claude Code 内置 Git Safety Protocol：

```bash
# 遵循最佳实践
git add file1.js file2.js  # 指定文件而非 -A
git commit -m "描述性提交信息"
```

**安全原则：**
- 不执行破坏性操作（除非明确要求）
- 创建新提交而非修改已发布提交
- 不跳过 hooks 或绕过签名
- 在执行 force push 前提示确认

### 4.2 提交信息规范

```
feat: 添加用户认证功能

- 实现 JWT token 验证
- 添加登录/登出端点
- 集成现有用户系统

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

## 5. 终端与执行

### 5.1 后台任务执行

```javascript
// 在后台运行长时间任务
Bash({
  command: "npm run build",
  run_in_background: true
})

// 任务完成时自动通知
```

### 5.2 有条件执行

```javascript
// 链式执行
command1 && command2

// 容错执行
command1; command2
```

### 5.3 定时任务

```javascript
// 创建循环任务（每10分钟）
CronCreate({
  cron: "*/10 * * * *",
  prompt: "检查部署状态",
  recurring: true
})

// 创建一次性提醒
CronCreate({
  cron: "30 14 28 2 *",  // 2月28日 14:30
  prompt: "会议提醒",
  recurring: false
})
```

## 6. 文件操作

### 6.1 直接写入文件

```javascript
// 创建或覆盖文件
Write({
  content: "文件内容...",
  file_path: "/path/to/newfile.txt"
})

// 注意：写入已存在文件前需要先 Read
```

### 6.2 工作树（Worktree）操作

```javascript
// 创建隔离的工作树
EnterWorktree({
  name: "feature-branch"
})

// 完成后清理
ExitWorktree({
  action: "keep"  // 或 "remove"
})
```

适用场景：
- 并行开发多个功能
- 安全地尝试有风险的修改
- 独立验证某个分支的改动

## 7. 网页与外部资源

### 7.1 网页内容获取

```javascript
// 获取网页内容进行分析
WebFetch({
  url: "https://example.com",
  prompt: "提取关于 API 文档的信息"
})

// 自动处理重定向
// 将 HTML 转换为 Markdown 格式
// 支持 PDF 内容提取
```

### 7.2 网络搜索

```javascript
// 搜索最新信息
WebSearch({
  query: "Claude Code 最新功能 2026"
})
```

## 8. 记忆系统

### 8.1 持久化记忆

Claude Code 提供了记忆系统来保存跨会话的信息：

```javascript
// 用户信息
Write({
  content: `---\nname: user_role\ntype: user\n---\n用户是资深后端工程师，擅长 Go 语言...`,
  file_path: "/Users/barryliu/.claude/projects/.../memory/user_role.md"
})

// 项目信息
// 参考信息
// 反馈记录
```

### 8.2 记忆类型

| 类型 | 用途 | 使用场景 |
|------|------|----------|
| user | 用户角色、偏好、知识 | 定制回答方式 |
| feedback | 指导、纠正、偏好 | 避免重复错误 |
| project | 项目目标、约束、deadline | 理解任务背景 |
| reference | 外部系统位置 | 快速定位资源 |

## 9. 任务管理

### 9.1 任务列表

```javascript
// 创建任务列表
TodoWrite({
  todos: [
    { content: "实现用户认证", status: "in_progress" },
    { content: "添加单元测试", status: "pending" },
    { content: "更新文档", status: "pending" }
  ]
})

// 更新任务状态
// 标记完成
```

### 9.2 循环任务

```javascript
// 设置循环检查
/loop 5m /check-status

// 自动执行间隔任务
// 持续监控直到被停止
```

## 10. 特殊命令

### 10.1 帮助与配置

```bash
/help          # 获取帮助信息
/settings     # 配置 Claude Code
/keybindings  # 自定义快捷键
```

### 10.2 模式切换

```bash
/fast          # 启用快速模式（使用更快但可能不太强大的模型）
/model sonnet  # 切换到 Sonnet 模型
/model opus    # 切换到 Opus 模型
```

## 11. 最佳实践

### 11.1 有效提问

- **具体说明文件路径和行号**
- **描述期望的结果**
- **提供相关上下文**
- **说明已尝试的方法**

### 11.2 安全注意事项

⚠️ 执行破坏性操作前确认
⚠️ 避免提交敏感信息到版本控制
⚠️ 重要操作前创建备份
⚠️ 理解命令的后果再执行

### 11.3 性能优化

- 使用后台任务处理长时间运行的进程
- 合理设置循环任务的间隔
- 利用子智能体并行处理任务
- 及时清理不需要的工作树

## 12. 常见问题

### 12.1 如何处理复杂的重构任务？

1. 使用 `/plan` 分析任务
2. 将任务分解为小步骤
3. 逐个完成任务并验证
4. 使用子智能体并行处理独立部分

### 12.2 如何避免误操作？

- Claude Code 默认不执行破坏性操作
- force push 等高风险操作需要确认
- 遵循 Git Safety Protocol

### 12.3 如何高效使用记忆系统？

- 定期更新用户偏好记忆
- 保存项目特定的约束和目标
- 记录外部系统位置方便快速访问

## 总结

Claude Code 不仅仅是一个代码补全工具，它是一个功能强大的编程助手。通过熟练掌握上述高级操作，你可以显著提升开发效率，更好地完成复杂的编程任务。

> 📌 持续关注更新，Claude Code 也在不断进化中！