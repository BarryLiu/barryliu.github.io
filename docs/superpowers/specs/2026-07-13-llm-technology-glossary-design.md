# AI 大模型技术全景与专业术语文章设计

## 目标

新增一篇面向技术面试准备者的大模型科普长文。文章不按术语字母顺序堆叠定义，而是沿着大模型的完整技术生命周期，从数据准备、模型架构和训练对齐，一直讲到推理、应用、部署、评测与安全，让读者既能建立知识体系，也能快速查阅术语。

文章需要与现有的 AI 学习路线形成互补：现有文章侧重学习顺序和单项技术教程，新文章侧重全景解释、概念联系、易混淆术语和面试复习。

## 读者与写作风格

- 主要读者：希望系统理解大模型并把 AI 用于日常软件开发的软件工程师，以及准备 AI、大模型、算法或 AI 应用开发岗位面试的初中级开发者。
- 科普优先：先用自然语言或类比解释，再补充严格定义和必要公式。
- 全面但有层次：正文覆盖主要技术链路，低频术语放入速查表，避免每个概念平均用力。
- 不把模型厂商的营销名称当作通用技术定义。
- 对参数规模、模型版本等容易过时的信息保持克制，重点解释稳定的技术概念。

## 文章信息

- 标题：`AI 大模型技术全景：从 Transformer 到 RAG、Agent 的专业术语手册`
- 路径：`content/posts/ailearn/llm-technology-glossary.md`
- `postSlug`：`ailearn/llm-technology-glossary`
- 分类：`ailearn`
- 标签：`AI`、`LLM`、`Transformer`、`RAG`、`Agent`、`技术面试`
- 文章日期：`2026-07-13`

## 内容结构

文章按以下生命周期展开：

1. **概念边界**：AI、机器学习、深度学习、生成式 AI、基础模型、大语言模型。
2. **数据与表示**：语料库、数据清洗、Token、Tokenizer、词表、Embedding、上下文窗口。
3. **模型架构**：Transformer、自注意力、多头注意力、Q/K/V、位置编码、RoPE、Encoder、Decoder、FFN、残差连接、归一化、MoE。
4. **模型训练**：参数、超参数、前向传播、损失函数、反向传播、梯度下降、优化器、预训练、Scaling Law、并行训练和混合精度。
5. **微调与对齐**：SFT、Instruction Tuning、PEFT、LoRA、QLoRA、偏好数据、奖励模型、RLHF、PPO、DPO、Constitutional AI。
6. **推理与生成**：Inference、Prefill、Decode、KV Cache、Logits、Softmax、Temperature、Top-k、Top-p、Beam Search、停止条件和流式输出。
7. **提示与模型能力**：Prompt、System Prompt、Zero-shot、Few-shot、In-context Learning、Chain of Thought、Structured Output、Function Calling、幻觉。
8. **知识增强与 RAG**：Chunking、Embedding Model、向量数据库、稠密检索、稀疏检索、混合检索、召回、重排序、Grounding、RAG 与微调的区别。
9. **Agent 系统**：Tool Calling、Agent、Planning、Memory、Workflow、MCP、多智能体，以及 Agent 与普通聊天机器人的区别。
10. **AI 编程与软件开发**：代码补全、FIM、代码生成与理解、仓库上下文、Coding Agent、IDE/CLI/云端 Agent、LSP、AST、Tree-sitter、Sandbox、Patch、测试调试、代码审查、SWE-bench、Vibe Coding 和安全边界。
11. **多模态与新架构**：VLM、视觉编码器、扩散模型、长上下文、推理模型和 Test-time Compute。
12. **推理优化与部署**：Quantization、Distillation、Pruning、Speculative Decoding、Continuous Batching、吞吐量、延迟、TTFT、TPS、模型服务框架。
13. **评测与安全**：Perplexity、BLEU、ROUGE、MMLU、HumanEval、LLM-as-a-Judge、Benchmark 污染、Prompt Injection、越狱、Guardrail、数据泄露与可解释性。
14. **面试复习**：大模型通用问题、AI 编程专项问题，以及按岗位划分的复习重点。
15. **术语速查表**：中英文全称、缩写、所属环节和一句话定义。

AI 编程章节按软件开发生命周期组织：

```text
需求与 Issue → 仓库上下文 → 计划与规格 → 生成 Patch → 测试与静态检查
→ 根据失败调试 → 人工审查 Diff → Commit / PR → CI 与上线反馈
```

该章节重点说明 AI 编程不是单纯的代码生成，而是模型、仓库上下文、开发工具、执行环境、验证反馈、权限和人工审查组成的工程系统。产品名称只用于说明交互形态，稳定技术概念优先引用协议规范、项目文档或原始论文。

## 单个术语的表达模板

核心术语根据重要性使用以下字段，简单术语可以合并表达：

1. 中文名、英文名和常用缩写。
2. 一句话定义。
3. 通俗解释或类比。
4. 它在大模型生命周期中的作用。
5. 与相近概念的区别或常见误区。
6. 一道常见面试问题或面试关注点。
7. 原始论文、官方文档、标准或官方项目主页。

## 导航与链接

- 文章开头提供分层目录，并使用 Markdown 锚点链接到各章节。
- 每个核心术语首次出现时加粗英文全称和缩写，减少重复解释。
- 来源链接优先级依次为：原始论文、标准或协议文档、官方框架文档、研究机构官方说明。
- 如果概念没有唯一的“官方定义”，链接到最早论文或公认的权威项目文档，并注明链接类型。
- 不使用搜索结果页、聚合转载或无法确认出处的二手文章作为定义来源。
- 所有外部链接在写作阶段逐项核验可访问性及其与定义的对应关系。

## 深度控制

- Transformer、训练对齐、RAG、Agent、推理优化属于重点章节，提供原理、对比和面试问题。
- 数学公式只保留帮助理解的核心公式，例如注意力、Softmax、交叉熵和困惑度，不进行完整数学推导。
- 对具体框架提供作用定位和官方入口，不写容易过期的安装教程。
- 术语总量目标不少于 120 个，正文重点解释约 70 至 90 个，其余进入速查表；其中 AI 编程与软件工程术语不少于 20 个。

## 验证与完成标准

- Frontmatter 满足 `src/content/config.ts` 的 schema。
- Markdown 标题层级清晰，目录锚点能够对应正文标题。
- 所有核心术语至少包含定义、作用或区别中的两项；重点术语包含面试关注点。
- 外部定义链接来自可信的一手来源，并在写作时在线核对。
- 不与已有学习路线文章大段重复；必要时链接到现有专题文章继续阅读。
- 完成后运行 `npm run test` 和 `npm run build`。
- 构建后检查文章路由，并确认首页、AI 笔记、知识库、关于页、归档页、任意文章页和 `rss.xml` 未受影响。

## 范围边界

- 本次只新增文章及文章直接需要的静态资源，不修改站点主题、内容 schema、迁移脚本或 Cloudflare 部署配置。
- 不修改当前工作区中与文章无关的已有未提交文件。
- 不在文章中维护具体商业模型排行榜或未经公开确认的参数量。
