# AI 大模型技术全景与专业术语文章 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 新增一篇沿大模型技术生命周期讲解核心技术与专业术语、适合科普阅读和技术面试复习的中文长文。

**Architecture:** 文章使用一份独立 Markdown 文件承载正文，通过章节目录把数据、架构、训练、对齐、推理、RAG、Agent、部署、评测和安全串成完整链路。术语定义优先引用原始论文、标准或项目官方文档；正文提供重点解释，文末速查表覆盖低频术语。

**Tech Stack:** Astro 5 Content Collections、Markdown、YAML frontmatter、Node test runner、Astro build

---

## 文件结构

- Create: `content/posts/ailearn/llm-technology-glossary.md`：文章 frontmatter、目录、正文、面试题与术语速查表。
- Reference: `docs/superpowers/specs/2026-07-13-llm-technology-glossary-design.md`：已确认的内容边界与完成标准。
- No change: `src/content/config.ts`、站点样式、迁移脚本、Cloudflare 配置以及当前工作区其他未提交文件。

### Task 1: 建立来源清单与文章骨架

**Files:**
- Create: `content/posts/ailearn/llm-technology-glossary.md`
- Reference: `content/posts/ailearn/05-transformer-advanced.md`
- Reference: `content/posts/ailearn/06-llm-application.md`

- [ ] **Step 1: 核验基础架构与训练的一手来源**

核验并记录以下页面能够直接支持相应定义：

- Transformer：`https://arxiv.org/abs/1706.03762`
- BERT：`https://arxiv.org/abs/1810.04805`
- GPT-3 与 In-context Learning：`https://arxiv.org/abs/2005.14165`
- RoPE：`https://arxiv.org/abs/2104.09864`
- Scaling Laws：`https://arxiv.org/abs/2001.08361`
- PyTorch autograd：`https://pytorch.org/docs/stable/autograd.html`
- PyTorch distributed：`https://pytorch.org/docs/stable/distributed.html`

对链接页面逐项确认标题、发布方和术语含义，不引用搜索结果摘要。

- [ ] **Step 2: 核验微调、对齐与推理的一手来源**

核验以下原始论文或官方文档：

- LoRA：`https://arxiv.org/abs/2106.09685`
- QLoRA：`https://arxiv.org/abs/2305.14314`
- InstructGPT / RLHF：`https://arxiv.org/abs/2203.02155`
- PPO：`https://arxiv.org/abs/1707.06347`
- DPO：`https://arxiv.org/abs/2305.18290`
- Constitutional AI：`https://arxiv.org/abs/2212.08073`
- Hugging Face generation strategies：`https://huggingface.co/docs/transformers/generation_strategies`
- vLLM PagedAttention：`https://arxiv.org/abs/2309.06180`

- [ ] **Step 3: 核验 RAG、Agent、协议、评测与安全来源**

核验以下一手来源：

- RAG：`https://arxiv.org/abs/2005.11401`
- Sentence Transformers：`https://www.sbert.net/`
- FAISS：`https://faiss.ai/`
- ReAct：`https://arxiv.org/abs/2210.03629`
- MCP specification：`https://modelcontextprotocol.io/specification/`
- Tool / function calling：使用主要模型 API 的官方开发文档，并将其描述为接口能力而非模型架构。
- MMLU：`https://arxiv.org/abs/2009.03300`
- HumanEval：`https://arxiv.org/abs/2107.03374`
- OWASP LLM Top 10：`https://genai.owasp.org/llm-top-10/`
- NIST AI Risk Management Framework：`https://www.nist.gov/itl/ai-risk-management-framework`

- [ ] **Step 4: 写入 frontmatter 和可点击目录**

Frontmatter 使用以下确定字段：

```yaml
---
title: "AI 大模型技术全景：从 Transformer 到 RAG、Agent 的专业术语手册"
date: 2026-07-13
postSlug: "ailearn/llm-technology-glossary"
categories:
  - ailearn
tags:
  - AI
  - LLM
  - Transformer
  - RAG
  - Agent
  - "技术面试"
description: "沿大模型技术生命周期系统讲解数据、Transformer、训练对齐、推理、RAG、Agent、部署、评测与安全等核心技术和专业术语。"
keywords: "AI大模型, LLM术语, Transformer, RLHF, RAG, AI Agent, 大模型面试"
featured: false
---
```

目录必须包含 15 个一级知识章节，链接分别指向概念边界、数据与表示、模型架构、模型训练、微调与对齐、推理与生成、提示与能力、RAG、Agent、AI 编程与软件开发、多模态与新架构、推理优化与部署、评测与安全、面试复习、术语速查表。

### Task 2: 完成模型形成阶段正文

**Files:**
- Modify: `content/posts/ailearn/llm-technology-glossary.md`

- [ ] **Step 1: 写概念边界和生命周期总览**

用一条从“数据 → Token → Transformer → 预训练 → 微调与对齐 → 推理 → RAG/Agent → 部署与评测”的链路解释各章节关系。明确 AI、机器学习、深度学习、生成式 AI、基础模型和 LLM 的包含关系，避免把生成式 AI 与 LLM 视为同义词。

- [ ] **Step 2: 写数据、Token 与向量表示**

解释语料库、数据清洗、去重、数据配比、Token、Tokenizer、Vocabulary、Embedding、上下文窗口和 OOV。至少对比字符、单词和子词切分，并说明 Token 数不等于字符数或单词数。

- [ ] **Step 3: 写 Transformer 架构**

解释 Self-Attention、Q/K/V、Scaled Dot-Product Attention、Multi-Head Attention、Causal Mask、Position Encoding、RoPE、Encoder、Decoder、FFN、Residual Connection、LayerNorm/RMSNorm 和 MoE。保留注意力核心公式，并用“查询、索引、内容”的类比解释 Q/K/V；明确 Encoder-only、Decoder-only、Encoder-Decoder 的区别。

- [ ] **Step 4: 写训练机制**

解释 Parameter、Hyperparameter、Forward Pass、Loss、Cross-Entropy、Backpropagation、Gradient、Optimizer、Learning Rate、Batch、Epoch、Pretraining、Scaling Law、Data/Tensor/Pipeline Parallelism、Gradient Accumulation 和 Mixed Precision。重点回答“训练为什么是预测下一个 Token”和“参数量不等于知识量”。

### Task 3: 完成训练后阶段正文

**Files:**
- Modify: `content/posts/ailearn/llm-technology-glossary.md`

- [ ] **Step 1: 写微调与对齐**

解释 SFT、Instruction Tuning、Full Fine-tuning、PEFT、LoRA、QLoRA、Preference Data、Reward Model、RLHF、PPO、DPO 和 Constitutional AI。提供 LoRA 与全参数微调、RLHF 与 DPO 的表格对比，并明确微调主要改变行为模式，不适合替代频繁更新的外部知识库。

- [ ] **Step 2: 写推理与生成**

解释 Inference、Prefill、Decode、Autoregressive Generation、KV Cache、Logits、Softmax、Temperature、Top-k、Top-p、Greedy Search、Beam Search、Stop Sequence 和 Streaming。说明 Temperature 为 0 的工程语义依赖具体 API 实现，避免把它写成统一数学规则。

- [ ] **Step 3: 写提示、上下文能力与幻觉**

解释 Prompt、System Prompt、Zero-shot、Few-shot、In-context Learning、Chain of Thought、Structured Output、Grounding、Context Engineering 和 Hallucination。明确 Prompt Engineering 不会修改模型参数，In-context Learning 也不等于训练或微调。

### Task 4: 完成应用系统阶段正文

**Files:**
- Modify: `content/posts/ailearn/llm-technology-glossary.md`

- [ ] **Step 1: 写 RAG 生命周期**

沿“文档加载 → 清洗 → Chunking → Embedding → Index → Retrieval → Reranking → Prompt Augmentation → Generation”解释 RAG。覆盖 Dense Retrieval、Sparse Retrieval、Hybrid Search、Recall、Precision、Reranker、Vector Database 和 Citation，并用表格对比 RAG、微调和长上下文。

- [ ] **Step 2: 写 Agent 系统**

解释 Tool Calling、Function Calling、Agent、Planning、Memory、Workflow、ReAct、MCP、Multi-agent 和 Human-in-the-loop。明确模型负责生成决策，宿主程序负责实际执行工具；MCP 是上下文与工具连接协议，不是 Agent 框架或模型。

- [ ] **Step 3: 写多模态与新架构**

解释 Multimodal Model、VLM、Vision Encoder、Cross-modal Alignment、Diffusion Model、Long Context、Reasoning Model 和 Test-time Compute。只解释稳定概念，不罗列未经确认的商业模型参数。

### Task 5: 完成工程化、评测、安全和面试部分

**Files:**
- Modify: `content/posts/ailearn/llm-technology-glossary.md`

- [ ] **Step 0: 写 AI 编程与软件开发生命周期**

沿“需求与 Issue → 仓库上下文 → 计划与规格 → 生成 Patch → 测试与静态检查 → 根据失败调试 → 人工审查 Diff → Commit / PR”解释 AI 编程。覆盖 Code Completion、Fill-in-the-Middle、Code Generation、Code Understanding、Repository Context、Repo Map、Coding Agent、IDE/CLI/云端 Agent、LSP、AST、Tree-sitter、Sandbox、Diff、Patch、Checkpoint、Rollback、Spec-driven Development、TDD、CI、SWE-bench 和 Vibe Coding。明确模型生成建议，工具和宿主环境实际执行；AI 生成代码必须经过测试、静态分析、权限限制和人工审查。

- [ ] **Step 1: 写推理优化与部署**

解释 Quantization、Distillation、Pruning、Speculative Decoding、Continuous Batching、PagedAttention、Model Serving、Throughput、Latency、TTFT、TPOT/TPS、GPU Memory 和 OOM。用表格说明吞吐量与延迟、量化与蒸馏、Prefill 与 Decode 的区别。

- [ ] **Step 2: 写评测与安全**

解释 Perplexity、BLEU、ROUGE、MMLU、HumanEval、LLM-as-a-Judge、Benchmark Contamination、Prompt Injection、Jailbreak、Guardrail、PII、Model/Data Leakage、Red Teaming、Alignment 和 Interpretability。强调单一榜单不能代表真实业务效果，安全评测需要覆盖模型、应用和工具权限三个层面。

- [ ] **Step 3: 写面试复习和术语速查表**

添加至少 25 道高频面试问题，覆盖 Transformer、训练对齐、推理、RAG、Agent、AI 编程和部署。按“算法/训练岗位、模型推理岗位、AI 应用岗位、软件开发岗位”列出复习重点。术语速查表至少包含 110 个中英文术语，其中 AI 编程与软件工程术语不少于 20 个，并标注所属生命周期环节。

- [ ] **Step 4: 做内容一致性检查**

全文检查以下误区没有出现：Token 等于单词、Embedding 数据库等于向量数据库、RAG 会训练模型、Agent 等于大模型、MCP 等于 Function Calling、Temperature 越高模型知道得越多、上下文窗口等于长期记忆、参数量等于能力、量化必然提高生成质量。

### Task 6: 验证文章与站点

**Files:**
- Verify: `content/posts/ailearn/llm-technology-glossary.md`

- [ ] **Step 1: 检查 Markdown 与链接结构**

运行：

```bash
rg -n '^#{1,6} ' content/posts/ailearn/llm-technology-glossary.md
rg -o 'https?://[^)> ]+' content/posts/ailearn/llm-technology-glossary.md | sort -u
```

预期：标题层级从 `##` 开始递进；链接清单不包含搜索结果页、空 URL 或重复拼写错误。

- [ ] **Step 2: 运行仓库测试**

运行：

```bash
npm run test
```

预期：Node 测试全部通过。

- [ ] **Step 3: 运行生产构建**

运行：

```bash
npm run build
```

预期：Astro 构建成功，生成 `dist/posts/ailearn/llm-technology-glossary/index.html`，内容集合无 schema 或重复 slug 错误。

- [ ] **Step 4: 检查关键静态路由**

运行：

```bash
for path in index.html ai-notes/index.html knowledge/index.html about/index.html archive/index.html posts/ailearn/llm-technology-glossary/index.html rss.xml; do test -f "dist/$path" || exit 1; done
```

预期：命令退出码为 0，所有关键路由文件存在。

- [ ] **Step 5: 检查 Git 范围并提交文章**

运行：

```bash
git diff --check -- content/posts/ailearn/llm-technology-glossary.md
git status --short
```

确认文章之外的已有工作区改动没有被修改或加入本次提交。只暂存文章和计划中属于本任务的文件，提交信息使用：

```bash
git commit -m "新增大模型技术术语科普"
```
