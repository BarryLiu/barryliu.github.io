---
layout: post
title: Ollama 学习笔记（由易到难）
category: skill
tags: ollama ai llm
keywords: ollama, 本地大模型, LLM, RAG, embeddings
description: Ollama 从入门到进阶的实践记录与参考链接
---

## 认识 Ollama

- Ollama 是本地运行大语言模型的工具，支持 Windows、macOS、Linux。
- 通过一条命令即可拉取和运行模型，提供 HTTP API，易于集成到应用。
- 适合开发者在本地做原型、私有数据推理、离线研发。
- 官方文档：<https://ollama.com/docs>

## 安装与启动（入门）

- 下载地址：<https://ollama.com/download>
- 安装后默认运行本地服务，API 端口为 `11434`。
- 基本检查：

```shell
ollama --version
ollama list
```

- 首次运行示例：

```shell
ollama run llama3 "你好，介绍下你自己"
```

- 更多：安装与使用概览 <https://ollama.com/docs/usage>

## 模型管理（入门）

- 拉取模型：

```shell
ollama pull llama3
ollama pull qwen2
ollama pull mistral
```

- 列出/删除模型：

```shell
ollama list
ollama rm llama3
```

- 模型目录与体积说明（参考）：<https://ollama.com/docs/models>

## 基本对话与参数（基础）

- 直接对话：

```shell
ollama run qwen2
```

- 一次性提示：

```shell
ollama run mistral -p "请用要点解释 Transformer 的注意力机制"
```

- 常用参数（更多见 <https://ollama.com/docs/parameters>）：
- `-p` 传入 prompt；`-m` 指定模型；`-t` 模板相关（在 Modelfile 中更常见）。
- 推理控制：`temperature`、`top_p`、`top_k`、`num_predict`、`repeat_penalty`、`mirostat`。
- 上下文长度：`num_ctx`（影响长文能力与内存占用）。

## 本地 API 调用（基础）

- API 概览：<https://ollama.com/docs/api>
- 生成文本（流式/非流式）：`POST /api/generate`
- 多轮对话：`POST /api/chat`

- `curl` 示例：

```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3",
    "prompt": "用三句话解释RAG",
    "stream": false
  }'
```

- Python 示例：

```python
import requests

url = "http://localhost:11434/api/chat"
payload = {
    "model": "llama3",
    "messages": [
        {"role": "user", "content": "给我一个Python生成示例"}
    ],
    "stream": False
}
resp = requests.post(url, json=payload, timeout=60)
print(resp.json())
```

- Node.js 示例：

```js
const fetch = require('node-fetch');

(async () => {
  const res = await fetch('http://localhost:11434/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: 'qwen2', prompt: '列出三条LLM提示工程建议', stream: false })
  });
  const data = await res.json();
  console.log(data);
})();
```

## Embeddings（进阶）

- 生成向量：`POST /api/embeddings`
- 文档：<https://ollama.com/docs/embeddings>

```bash
curl -X POST http://localhost:11434/api/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3",
    "prompt": "大语言模型是什么"
  }'
```

- 用途：为 RAG、语义搜索、相似度检索提供向量表示；可配合 `faiss`、`pgvector`、`milvus` 等库。

## Modelfile 与自定义模型（进阶）

- 文档：<https://docs.ollama.com/modelfile>
- 通过 `Modelfile` 在基础模型上添加系统提示、模板、参数等，生成自己的可复用模型。

```dockerfile
# 文件名: Modelfile
FROM llama3
PARAMETER temperature 0.7
PARAMETER num_ctx 4096
SYSTEM "你是一名资深中文助理，回答要简洁、有条理。"
TEMPLATE "用户：{{ .Prompt }}\n助理："
```

```bash
ollama create my-llama -f Modelfile
ollama run my-llama -p "请用要点解释Attention"
```

- 常见参数与说明：<https://ollama.com/docs/parameters>
- 将 `keep_alive` 设置为如 `5m` 可提高多次调用的响应速度（模型常驻内存）。

## 个人模型制作与推送（进阶）

### 模型制作概述

- **制作思路**：基于基础模型，通过 `Modelfile` 配置系统提示、模板、参数，必要时引入 LoRA 适配器，创建个人化模型。
- **适用场景**：定制化助手、特定领域知识库、风格化对话、企业私有模型等。
- **参考文档**：<https://docs.ollama.com/modelfile>、<https://docs.ollama.com/import>

### Modelfile 详解

`Modelfile` 是定义自定义模型的核心配置文件，支持以下指令：

#### 基础指令说明

- `FROM <模型名>`：指定基础模型（必需）
- `SYSTEM <提示词>`：设置系统提示，定义模型角色和行为
- `TEMPLATE <模板字符串>`：定义对话模板格式
- `PARAMETER <参数名> <值>`：设置模型推理参数
- `ADAPTER <路径>`：引入 LoRA 适配器（可选）
- `LICENSE <许可证>`：声明模型许可证
- `MESSAGE <角色> <内容>`：添加示例对话消息

#### Modelfile 语法格式详解

##### 1. FROM 指令

**语法**：
```dockerfile
FROM <模型名>[:<标签>]
```

**说明**：
- 必需指令，必须放在文件开头
- 指定基础模型，可以是官方模型或已存在的自定义模型
- 支持标签指定版本（如 `llama3:8b`）

**示例**：
```dockerfile
FROM llama3              # 使用默认版本
FROM llama3:8b           # 使用 8b 版本
FROM qwen2:7b            # 使用 qwen2 的 7b 版本
FROM myuser/mymodel      # 使用自定义模型
FROM myuser/mymodel:1.0  # 使用自定义模型的特定版本
```

##### 2. SYSTEM 指令

**语法**：
```dockerfile
SYSTEM "<单行提示词>"
# 或
SYSTEM """多行提示词
可以包含换行
支持多行内容"""
```

**说明**：
- 定义模型的系统提示词，描述模型角色、行为规范
- 可以使用单引号 `"` 或三引号 `"""` 包裹
- 三引号支持多行内容，保留换行格式
- 可以多次使用，后面的会覆盖前面的

**示例**：
```dockerfile
# 单行
SYSTEM "你是一名专业的AI助手。"

# 多行
SYSTEM """你是一名资深软件工程师。
你的职责包括：
1. 编写高质量代码
2. 进行代码审查
3. 提供技术建议"""

# 使用变量（在模板中）
SYSTEM "你是一个{{ .Language }}编程专家。"
```

##### 3. TEMPLATE 指令

**语法**：
```dockerfile
TEMPLATE "<模板字符串>"
# 或
TEMPLATE """多行模板
支持换行"""
```

**说明**：
- 定义对话模板，控制用户输入和模型输出的格式
- 使用 Go 模板语法（`{{ }}`）
- 可用变量：
  - `{{ .Prompt }}`：用户输入
  - `{{ .System }}`：系统提示词
  - `{{ .Response }}`：模型响应（在生成时可用）

**模板语法**：
- `{{ .变量名 }}`：输出变量值
- `{{ if .条件 }}...{{ end }}`：条件判断
- `{{ if .条件 }}...{{ else }}...{{ end }}`：条件判断（带 else）
- `\n`：换行符
- `\t`：制表符

**示例**：
```dockerfile
# 简单模板
TEMPLATE "用户：{{ .Prompt }}\n助手："

# 条件模板
TEMPLATE """{{ if .System }}系统：{{ .System }}

{{ end }}用户：{{ .Prompt }}

助手："""

# 复杂模板（多轮对话格式）
TEMPLATE """{{ if .System }}<|system|>
{{ .System }}<|end|>
{{ end }}<|user|>
{{ .Prompt }}<|end|>
<|assistant|>
"""
```

**常见模型模板格式**：

```dockerfile
# ChatML 格式（OpenAI 风格）
TEMPLATE """<|im_start|>system
{{ .System }}<|im_end|>
<|im_start|>user
{{ .Prompt }}<|im_end|>
<|im_start|>assistant
"""

# Alpaca 格式
TEMPLATE """Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{{ .Prompt }}

### Response:
"""

# Vicuna 格式
TEMPLATE """USER: {{ .Prompt }}
ASSISTANT: """
```

##### 4. PARAMETER 指令

**语法**：
```dockerfile
PARAMETER <参数名> <值>
```

**说明**：
- 设置模型推理参数
- 参数名不区分大小写
- 可以多次使用设置不同参数
- 数值参数可以是整数或浮点数

**常用参数列表**：

| 参数名 | 类型 | 默认值 | 说明 | 取值范围 |
|--------|------|--------|------|----------|
| `temperature` | float | 0.8 | 采样温度，控制随机性 | 0.0-2.0 |
| `top_p` | float | 0.9 | 核采样参数 | 0.0-1.0 |
| `top_k` | int | 40 | Top-K 采样，限制候选词数 | 1-100 |
| `num_ctx` | int | 2048 | 上下文窗口大小（token数） | 512-32768 |
| `num_predict` | int | -1 | 最大生成 token 数（-1 表示无限制） | -1 或正整数 |
| `repeat_penalty` | float | 1.1 | 重复惩罚系数 | 0.0-2.0 |
| `repeat_last_n` | int | 64 | 考虑重复惩罚的最近 token 数 | 0-2048 |
| `seed` | int | -1 | 随机种子（-1 表示随机） | -1 或非负整数 |
| `numa` | bool | false | 是否使用 NUMA | true/false |
| `num_thread` | int | 自动 | CPU 线程数 | 正整数 |
| `num_gpu` | int | 自动 | GPU 层数 | 非负整数 |
| `main_gpu` | int | 0 | 主 GPU 索引 | 非负整数 |
| `low_vram` | bool | false | 低显存模式 | true/false |
| `f16_kv` | bool | true | 使用 FP16 存储 KV 缓存 | true/false |
| `logits_all` | bool | false | 返回所有 token 的 logits | true/false |
| `vocab_only` | bool | false | 仅加载词汇表 | true/false |
| `use_mmap` | bool | true | 使用内存映射 | true/false |
| `use_mlock` | bool | false | 锁定内存 | true/false |
| `embedding_only` | bool | false | 仅用于 embeddings | true/false |
| `mirostat` | int | 0 | Mirostat 采样算法（0=禁用，1=Mirostat，2=Mirostat 2.0） | 0/1/2 |
| `mirostat_lr` | float | 0.1 | Mirostat 学习率 | 0.0-1.0 |
| `mirostat_eta` | float | 0.1 | Mirostat eta 参数 | 0.0-1.0 |
| `penalize_newline` | bool | true | 惩罚换行符 | true/false |
| `stop` | string | - | 停止序列（可多次使用） | 字符串 |

**示例**：
```dockerfile
# 基础参数
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40

# 上下文和生成长度
PARAMETER num_ctx 4096
PARAMETER num_predict 2048

# 重复控制
PARAMETER repeat_penalty 1.1
PARAMETER repeat_last_n 64

# 随机种子（用于可复现性）
PARAMETER seed 42

# 停止序列（可多次使用）
PARAMETER stop "用户："
PARAMETER stop "Human:"
PARAMETER stop "\n\n\n"

# GPU 配置
PARAMETER num_gpu 2
PARAMETER main_gpu 0
PARAMETER low_vram true

# 采样算法
PARAMETER mirostat 2
PARAMETER mirostat_lr 0.1
PARAMETER mirostat_eta 0.1
```

##### 5. MESSAGE 指令

**语法**：
```dockerfile
MESSAGE <角色> "<内容>"
# 或
MESSAGE <角色> """多行内容
支持换行"""
```

**说明**：
- 添加示例对话消息（few-shot learning）
- 用于训练模型理解特定对话格式或提供示例
- 角色通常是 `user` 或 `assistant`
- 可以多次使用，按顺序组成对话历史

**示例**：
```dockerfile
# 单轮对话示例
MESSAGE user "什么是 Python？"
MESSAGE assistant "Python 是一种高级编程语言，以简洁和可读性著称。"

# 多轮对话示例
MESSAGE user "如何学习编程？"
MESSAGE assistant "学习编程可以从以下几个方面入手：\n1. 选择一门语言\n2. 练习基础语法\n3. 做项目实践"

MESSAGE user "推荐一些学习资源"
MESSAGE assistant "推荐资源：\n- 官方文档\n- 在线教程\n- 编程练习平台"

# 复杂格式示例
MESSAGE user """请帮我写一个 Python 函数，计算斐波那契数列的第 n 项。"""
MESSAGE assistant """```python
def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```"""
```

##### 6. ADAPTER 指令

**语法**：
```dockerfile
ADAPTER <路径>
```

**说明**：
- 引入 LoRA 适配器
- 路径可以是相对路径或绝对路径
- 适配器目录应包含适配器权重文件

**示例**：
```dockerfile
# 相对路径
ADAPTER ./lora_adapter
ADAPTER ./adapters/code_assistant

# 绝对路径
ADAPTER /home/user/adapters/my_adapter
ADAPTER C:\Users\user\adapters\my_adapter
```

##### 7. LICENSE 指令

**语法**：
```dockerfile
LICENSE "<许可证名称>"
# 或
LICENSE """多行许可证文本
可以包含完整的许可证内容"""
```

**说明**：
- 声明模型许可证
- 可以是许可证名称或完整许可证文本

**示例**：
```dockerfile
# 许可证名称
LICENSE "MIT"
LICENSE "Apache-2.0"
LICENSE "CC-BY-4.0"

# 完整许可证文本
LICENSE """MIT License

Copyright (c) 2024

Permission is hereby granted...
"""
```

##### 8. 注释语法

**语法**：
```dockerfile
# 单行注释
# 这是注释内容
```

**说明**：
- 使用 `#` 开头表示注释
- 注释会被忽略，不影响模型配置
- 可用于说明配置意图

**示例**：
```dockerfile
# 这是一个代码助手模型
FROM llama3:8b

# 系统提示：定义模型角色
SYSTEM "你是一名专业的代码助手。"

# 推理参数：平衡创造性和准确性
PARAMETER temperature 0.7  # 适中的随机性
PARAMETER top_p 0.9        # 核采样
```

##### 9. 多行字符串语法

**语法**：
```dockerfile
# 使用三引号
"""多行内容
可以包含换行
保留格式"""
```

**说明**：
- 使用三个双引号 `"""` 包裹多行内容
- 保留换行和空格格式
- 适用于 SYSTEM、TEMPLATE、MESSAGE、LICENSE 等指令

**示例**：
```dockerfile
SYSTEM """你是一名专业助手。
你的回答需要：
1. 准确
2. 详细
3. 有条理"""

TEMPLATE """{{ if .System }}系统：{{ .System }}

{{ end }}用户：{{ .Prompt }}

助手："""
```

##### 10. 指令顺序与优先级

**推荐顺序**：
1. `FROM`（必需，放在最前）
2. `ADAPTER`（如果有）
3. `SYSTEM`
4. `TEMPLATE`
5. `PARAMETER`（可以多个）
6. `MESSAGE`（可以多个）
7. `LICENSE`

**优先级规则**：
- 相同指令多次使用时，后面的会覆盖前面的
- `PARAMETER` 可以多次使用设置不同参数
- `MESSAGE` 按顺序累积，形成对话历史

**示例**：
```dockerfile
# 正确的顺序示例
FROM llama3:8b
ADAPTER ./my_adapter
SYSTEM "你是一名助手。"
TEMPLATE "用户：{{ .Prompt }}\n助手："
PARAMETER temperature 0.7
PARAMETER num_ctx 4096
MESSAGE user "示例1"
MESSAGE assistant "回复1"
MESSAGE user "示例2"
MESSAGE assistant "回复2"
LICENSE "MIT"
```

##### 11. 转义字符

**常用转义字符**：
- `\n`：换行符
- `\t`：制表符
- `\"`：双引号
- `\\`：反斜杠
- `\r`：回车符

**示例**：
```dockerfile
# 在单引号字符串中使用转义
TEMPLATE "用户：{{ .Prompt }}\n助手："

# 在多行字符串中也可以使用
SYSTEM "第一行\n第二行\n第三行"
```

#### 完整 Modelfile 示例

```dockerfile
# 文件名: Modelfile
# 基于 llama3 创建专业代码助手

FROM llama3:8b

# 系统提示：定义模型角色
SYSTEM """你是一名资深的软件工程师和代码审查专家。
你的回答需要：
1. 代码示例清晰、可运行
2. 解释简洁、有条理
3. 提供最佳实践建议
4. 指出潜在问题和改进方向"""

# 对话模板：定义用户和助手的交互格式
TEMPLATE """{{ if .System }}系统：{{ .System }}

{{ end }}{{ if .Prompt }}用户：{{ .Prompt }}

{{ end }}助手："""

# 推理参数配置
PARAMETER temperature 0.7        # 创造性（0-1，越高越随机）
PARAMETER top_p 0.9              # 核采样参数
PARAMETER top_k 40               # Top-K 采样
PARAMETER num_ctx 4096           # 上下文窗口大小
PARAMETER num_predict 2048       # 最大生成 token 数
PARAMETER repeat_penalty 1.1     # 重复惩罚（>1 减少重复）
PARAMETER seed 42                # 随机种子（固定可复现）

# 示例对话（few-shot learning）
MESSAGE user "如何优化 Python 列表查找性能？"
MESSAGE assistant """对于频繁查找，可以使用集合（set）替代列表：

```python
# 慢：O(n)
if item in my_list:
    pass

# 快：O(1)
if item in my_set:
    pass
```

对于有序数据，使用二分查找（bisect 模块）。"""

# 许可证声明
LICENSE "MIT"
```

#### 不同场景的 Modelfile 示例

**示例 1：中文对话助手**

```dockerfile
FROM qwen2:7b
SYSTEM "你是一个友好、专业的中文AI助手。回答要自然、易懂，适当使用表情符号。"
TEMPLATE "用户：{{ .Prompt }}\n\n助手："
PARAMETER temperature 0.8
PARAMETER num_ctx 8192
```

**示例 2：技术文档生成器**

```dockerfile
FROM mistral:7b
SYSTEM """你是一个技术文档编写专家。
输出格式要求：
- 使用 Markdown 格式
- 代码块包含语言标识
- 提供清晰的步骤说明
- 包含注意事项和最佳实践"""
TEMPLATE "{{ .Prompt }}\n\n请按照上述要求生成文档：\n\n"
PARAMETER temperature 0.3
PARAMETER num_predict 4096
```

**示例 3：数据分析助手**

```dockerfile
FROM llama3:8b
SYSTEM "你擅长数据分析和统计。回答时提供具体的数据处理步骤、代码示例和可视化建议。"
PARAMETER temperature 0.5
PARAMETER num_ctx 16384
```

### 创建自定义模型

#### 基本创建流程

```bash
# 1. 准备 Modelfile（在当前目录创建 Modelfile 文件）
cat > Modelfile << 'EOF'
FROM llama3
SYSTEM "你是一名专业助理。"
PARAMETER temperature 0.7
EOF

# 2. 创建模型
ollama create mymodel -f Modelfile

# 3. 测试模型
ollama run mymodel -p "介绍一下你自己"
```

#### 量化选项（降低资源占用）

```bash
# 不同量化等级（从高到低质量，从大到小体积）
ollama create mymodel -f Modelfile --quantize q8_0    # 8位量化，质量最高
ollama create mymodel -f Modelfile --quantize q6_K     # 6位量化，平衡选择
ollama create mymodel -f Modelfile --quantize q4_K_M   # 4位量化，推荐
ollama create mymodel -f Modelfile --quantize q4_0     # 4位量化，最小体积
```

**量化等级说明**：
- `q8_0`：8位量化，接近原始质量，体积较大
- `q6_K`：6位量化，质量与体积的平衡点
- `q4_K_M`：4位量化（中等），推荐用于大多数场景
- `q4_0`：4位量化（基础），体积最小但质量略低

#### 查看和管理模型

```bash
# 查看模型详细信息
ollama show mymodel

# 查看模型的 Modelfile 配置
ollama show mymodel --modelfile

# 列出所有模型
ollama list

# 复制模型（用于创建变体）
ollama cp mymodel mymodel-v2

# 删除模型
ollama rm mymodel
```

### LoRA 适配器集成

LoRA（Low-Rank Adaptation）是一种参数高效的微调方法，可以在不修改基础模型的情况下添加特定能力。

#### 准备 LoRA 适配器

```bash
# LoRA 适配器通常是一个目录，包含适配器权重文件
# 目录结构示例：
# adapter_dir/
#   ├── adapter_config.json
#   └── adapter_model.bin
```

#### 在 Modelfile 中使用 LoRA

```dockerfile
FROM llama3:8b
ADAPTER ./adapter_dir
SYSTEM "你是一名经过专业领域训练的AI助手。"
PARAMETER temperature 0.7
```

#### 创建带 LoRA 的模型

```bash
# 确保 adapter_dir 目录存在且包含适配器文件
ollama create mymodel-lora -f Modelfile
```

**注意事项**：
- LoRA 适配器需要与基础模型兼容
- 适配器文件通常由训练框架（如 PEFT、LoRA）生成
- 适配器可以叠加使用，但需要确保兼容性

### 模型推送详细流程

#### 前置准备

1. **注册 Ollama 账号**
   - 访问 <https://ollama.com/>
   - 注册并登录账号

2. **获取 Ollama Public Key**
   ```bash
   # 查看本机的公钥
   ollama key
   # 或查看公钥文件位置（通常在 ~/.ollama/id_ed25519.pub）
   ```

3. **添加公钥到账号**
   - 登录 <https://ollama.com/>
   - 进入 Settings → Ollama Keys
   - 点击 "Add Key"，粘贴公钥内容
   - 保存设置

#### 推送步骤详解

**步骤 1：命名模型（使用命名空间）**

模型名称必须遵循 `<用户名>/<模型名>` 的格式：

```bash
# 如果模型已存在，需要复制并重命名
ollama cp mymodel <你的用户名>/mymodel

# 或者创建时直接使用命名空间
ollama create <你的用户名>/mymodel -f Modelfile
```

**示例**（假设用户名为 `john`）：
```bash
ollama cp mymodel john/code-assistant
```

**步骤 2：验证模型**

推送前建议先本地测试：

```bash
# 测试模型功能
ollama run <你的用户名>/mymodel -p "测试提示"

# 查看模型信息
ollama show <你的用户名>/mymodel
```

**步骤 3：推送模型**

```bash
# 推送模型到 Ollama 模型库
ollama push <你的用户名>/mymodel
```

推送过程会显示进度：
```
pushing manifest
pushing 2/2 layers (100%)
pushed successfully
```

**步骤 4：验证推送结果**

- 访问 <https://ollama.com/library> 查看你的模型
- 或使用 API 检查：
```bash
curl https://ollama.com/api/tags | grep "<你的用户名>/mymodel"
```

#### 版本管理与标签

使用标签管理模型版本，便于迭代和回滚：

```bash
# 创建带版本标签的模型
ollama cp <你的用户名>/mymodel <你的用户名>/mymodel:1.0
ollama cp <你的用户名>/mymodel <你的用户名>/mymodel:latest

# 推送特定版本
ollama push <你的用户名>/mymodel:1.0
ollama push <你的用户名>/mymodel:latest

# 更新模型后创建新版本
ollama cp <你的用户名>/mymodel <你的用户名>/mymodel:2.0
ollama push <你的用户名>/mymodel:2.0
```

**版本命名建议**：
- `latest`：最新稳定版
- `1.0`、`1.1`、`2.0`：语义化版本号
- `dev`、`beta`：开发/测试版本
- `2024-12-01`：日期版本

#### 他人使用你的模型

推送成功后，其他人可以通过以下方式使用：

```bash
# 拉取模型
ollama pull <你的用户名>/mymodel

# 或拉取特定版本
ollama pull <你的用户名>/mymodel:1.0

# 运行模型
ollama run <你的用户名>/mymodel -p "你好"
```

### 推送常见问题与解决方案

#### 问题 1：推送失败 - 认证错误

**症状**：
```
Error: unauthorized
```

**解决方案**：
1. 确认已登录 <https://ollama.com/>
2. 检查公钥是否正确添加到账号
3. 重新生成密钥对（如需要）：
   ```bash
   # 删除旧密钥（谨慎操作）
   rm ~/.ollama/id_ed25519*
   # Ollama 会在下次操作时自动生成新密钥
   ollama key  # 查看新公钥
   ```

#### 问题 2：推送失败 - 网络超时

**症状**：
```
Error: timeout
```

**解决方案**：
1. 检查网络连接
2. 使用代理（如需要）：
   ```bash
   export HTTP_PROXY=http://proxy:port
   export HTTPS_PROXY=http://proxy:port
   ollama push <你的用户名>/mymodel
   ```
3. 分块推送大模型（Ollama 自动处理）

#### 问题 3：模型名称格式错误

**症状**：
```
Error: invalid model name
```

**解决方案**：
- 确保模型名称格式为 `<用户名>/<模型名>`
- 用户名必须与 Ollama 账号一致
- 模型名不能包含特殊字符（建议使用字母、数字、连字符）

#### 问题 4：推送进度缓慢

**原因与优化**：
- 模型体积大：考虑使用量化版本
- 网络带宽限制：使用稳定网络环境
- 首次推送较慢：后续更新只推送变更部分

### 模型更新与维护

#### 更新已推送的模型

```bash
# 1. 修改 Modelfile
vim Modelfile

# 2. 重新创建模型（使用相同名称）
ollama create <你的用户名>/mymodel -f Modelfile

# 3. 推送更新
ollama push <你的用户名>/mymodel
```

#### 删除已推送的模型

```bash
# 注意：删除操作需要谨慎，可能影响其他用户
# 在 Ollama 网站上进行删除操作更安全
```

#### 模型描述与文档

在推送模型时，建议：
1. 在 Modelfile 中添加注释说明模型用途
2. 在 Ollama 网站为模型添加描述
3. 提供使用示例和参数说明

### 高级技巧

#### 1. 模型组合与继承

```dockerfile
# 基于已有自定义模型创建新模型
FROM <你的用户名>/mymodel
SYSTEM "在原有基础上，你还需要擅长数据分析。"
PARAMETER temperature 0.6
```

#### 2. 条件模板

```dockerfile
TEMPLATE """{{ if .System }}系统指令：{{ .System }}

{{ end }}{{ if .Prompt }}用户：{{ .Prompt }}

{{ end }}助手："""
```

#### 3. 多轮对话示例

```dockerfile
MESSAGE user "什么是 RAG？"
MESSAGE assistant "RAG（Retrieval-Augmented Generation）是一种结合检索和生成的技术..."

MESSAGE user "它有什么优势？"
MESSAGE assistant "RAG 的主要优势包括：1. 可以访问最新信息 2. 减少幻觉..."
```

### API 参考

- 推送接口：<https://docs.ollama.com/api/push>
- 模型管理：<https://docs.ollama.com/api/tag>
- Modelfile 完整文档：<https://docs.ollama.com/modelfile>

## 性能与上下文（进阶）

- 上下文长度 `num_ctx`：增大可处理更长文本，但显著提升内存与算力需求。
- 生成长度 `num_predict`：限制最大输出 token 数，避免响应过长。
- 流式输出：API 中 `stream: true` 可边生成边传输，提升交互体验。
- 并发建议：控制并发到机器可承受范围；复用常驻模型以减少冷启动。

## RAG 快速示例（进阶）

- 指南与案例：<https://ollama.com/docs/examples>
- 思路：
- 1）将本地文档分块并生成 embeddings（用 Ollama 的 `/api/embeddings`）。
- 2）存入向量库（FAISS/pgvector），检索相似片段。
- 3）将检索到的内容拼接为上下文，走 `/api/chat` 作为系统/用户提示。

## 多模型与多模态（进阶）

- 可同时安装多种模型：`llama3`、`qwen2`、`mistral`、`phi3` 等。
- 多模态（图像理解）模型如 `llava` 需要额外输入；参考：<https://ollama.com/docs/models>

## Windows 常见问题（进阶）

- 端口占用：确保 `11434` 未被占用；或通过环境变量更改端口。
- 显存/内存不足：选择更小的量化模型（如 `q4`）；降低 `num_ctx`。
- 启动失败排查：查看日志与服务状态；参考：<https://ollama.com/docs/usage>

## 实用命令速查（综合）

```bash
# 拉取/运行
ollama pull llama3
ollama run llama3 -p "用5点说明提示工程"

# 查看模型
ollama list

# 删除模型
ollama rm llama3

# 创建自定义模型
ollama create my-llama -f Modelfile
ollama run my-llama -p "测试"

# 生成向量
curl -s http://localhost:11434/api/embeddings -d '{"model":"llama3","prompt":"示例"}'
```

## 参考资料

- 官方文档主页：<https://ollama.com/docs>
- 下载页：<https://ollama.com/download>
- 使用指南：<https://ollama.com/docs/usage>
- API：<https://ollama.com/docs/api>
- Embeddings：<https://ollama.com/docs/embeddings>
- Modelfile：<https://ollama.com/docs/modelfile>
- 参数：<https://ollama.com/docs/parameters>
- 模型目录：<https://ollama.com/docs/models>
