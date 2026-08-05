---
title: AI 大模型技术全景：从 Transformer 到 RAG、Agent 的专业术语手册
date: 2026-07-13
postSlug: ailearn/llm-technology-glossary
categories:
  - ailearn
tags:
  - AI
  - LLM
  - Transformer
  - RAG
  - Agent
  - 技术面试
description: 沿大模型技术生命周期系统讲解数据、Transformer、训练对齐、推理、RAG、Agent、部署、评测与安全等核心技术和专业术语。
keywords: AI大模型, LLM术语, Transformer, RLHF, RAG, AI Agent, 大模型面试
featured: false
---

如果把大模型术语单独背下来，你会记住很多缩写，却仍然回答不了一个关键问题：**一段原始文本究竟怎样变成模型参数，又怎样在用户提问后生成答案？**

这篇文章不按字母顺序堆砌概念，而是沿着大模型的技术生命周期展开：

```text
原始数据
  ↓ 清洗、去重、切分
Token 与向量表示
  ↓
Transformer
  ↓ 预训练
基础模型
  ↓ 指令微调、偏好对齐
可对话模型
  ↓ 推理、采样
文本输出
  ↓ 接入外部知识与工具
RAG / Agent
  ↓
部署、评测、安全治理
```

读完后，你应该能建立一张完整的知识地图，并能够解释面试中最常见的概念区别。

> 链接说明：本文优先链接原始论文、规范、标准或项目官方文档。部分术语并不存在唯一的“官方定义”，此时链接会指向最早论文或公认的一手技术资料。

## 目录

1. [概念边界：AI、生成式 AI、基础模型与 LLM](#concept-boundary)
2. [数据与表示：从语料库到 Token、Embedding](#data-representation)
3. [模型架构：Transformer 为什么成为基础](#model-architecture)
4. [模型训练：参数是怎样学出来的](#model-training)
5. [微调与对齐：让模型从“续写”走向“助手”](#fine-tuning-alignment)
6. [推理与生成：模型怎样逐 Token 输出](#inference-generation)
7. [提示与能力：Prompt、上下文学习与幻觉](#prompt-capabilities)
8. [知识增强：RAG 的完整生命周期](#rag)
9. [行动能力：Tool Calling、Agent 与 MCP](#agent)
10. [AI 编程：从代码补全到软件开发 Agent](#ai-coding)
11. [多模态与新架构](#multimodal)
12. [推理优化与部署](#deployment)
13. [评测与安全](#evaluation-safety)
14. [高频面试问题与岗位复习路线](#interview)
15. [中英文术语速查表](#glossary)

---

<a id="concept-boundary"></a>

## 1. 概念边界：AI、生成式 AI、基础模型与 LLM

### 1.1 AI、机器学习与深度学习

**人工智能（Artificial Intelligence，AI）** 是最大的概念，目标是让机器表现出感知、推理、规划、学习或行动等智能行为。

**机器学习（Machine Learning，ML）** 是实现 AI 的一种方法：不把所有规则逐条写死，而是让算法从数据中学习规律。

**深度学习（Deep Learning，DL）** 又是机器学习的一类，主要依赖多层神经网络学习复杂表示。今天的大语言模型属于深度学习系统，但 AI 并不等于深度学习，深度学习也不等于大模型。

可以把三者理解为：

```text
人工智能 AI
└── 机器学习 ML
    └── 深度学习 DL
        └── 大语言模型 LLM
```

### 1.2 生成式 AI、基础模型与大语言模型

**生成式人工智能（Generative AI）** 指能够生成文本、图像、音频、视频、代码等新内容的 AI 系统。LLM 是生成式 AI 的重要分支，但图像扩散模型同样属于生成式 AI，却不一定是语言模型。

**[基础模型（Foundation Model）](https://arxiv.org/abs/2108.07258)** 是在大规模、广泛数据上训练，随后能够适配多种下游任务的模型。它强调的是“大规模预训练 + 广泛适配”，模态可以是语言、视觉、语音或多模态。

**大语言模型（Large Language Model，LLM）** 是以语言序列为主要处理对象、通常具有大规模参数和训练数据的语言模型。它的核心训练目标往往不是“把知识存进数据库”，而是学习：

> 给定前面的 Token，下一个 Token 出现的概率是多少？

**模型（Model）**、**产品（Product）** 和 **应用（Application）** 也要区分：

- 模型负责把输入映射为输出概率或表示。
- 产品通常包含模型、系统提示、知识库、工具、权限、审核和界面。
- 应用效果差，不一定说明底层模型差；也可能是检索、提示、工具或数据链路出了问题。

### 1.3 参数、能力与知识不是同一件事

**参数量（Parameter Count）** 是模型中可学习数值的数量，例如权重矩阵中的元素个数。参数更多通常意味着更大的表达容量，但不自动等于：

- 知识一定更准确；
- 推理一定更可靠；
- 每个任务都更强；
- 部署成本更划算。

模型能力还受到训练数据、数据质量、架构、训练计算量、对齐方法、推理策略和工具系统影响。因此，“参数越多越好”不是完整结论。

> **面试关注点：** 生成式 AI 是能力类别，基础模型是训练与适配范式，LLM 是以语言为核心的模型类型，三者不能互换。

---

<a id="data-representation"></a>

## 2. 数据与表示：从语料库到 Token、Embedding

模型首先面对的不是“文字含义”，而是经过清洗和编码的数字序列。

### 2.1 语料库、数据清洗与数据配比

**语料库（Corpus）** 是用于训练或评测的文本集合。大模型预训练语料可能包含网页、书籍、论文、代码、对话和合成数据。

数据进入训练前通常需要：

- **过滤（Filtering）**：删除低质量、乱码、垃圾和不符合策略的内容；
- **去重（Deduplication）**：减少完全重复或近似重复数据，降低记忆和评测污染；
- **脱敏（De-identification）**：处理个人身份信息（PII）；
- **质量打分（Quality Scoring）**：按规则或模型评估内容质量；
- **数据配比（Data Mixture）**：控制自然语言、代码、数学、多语言等数据的比例；
- **数据课程（Curriculum）**：安排不同难度、类型或阶段的数据顺序。

数据量不是唯一目标。重复、错误或偏见数据也会被模型学习，所以行业里常说：**数据质量决定能力上限的一大部分。**

### 2.2 Token 与 Tokenizer

**[Token](https://huggingface.co/docs/transformers/tokenizer_summary)** 是模型处理文本时的离散单位，可以是一个字、词、子词、标点或字节片段。**Tokenizer（分词器）** 负责在文本和 Token ID 序列之间转换。

例如，“大模型正在改变软件开发”可能被某个分词器切成：

```text
["大", "模型", "正在", "改变", "软件", "开发"]
```

另一个分词器可能切成不同结果。因此：

- Token 不等于汉字；
- Token 不等于英文单词；
- 相同文本在不同模型中的 Token 数可能不同；
- API 按 Token 计费时，字符数只能作为粗略估计。

常见子词算法包括：

- **[BPE（Byte Pair Encoding）](https://arxiv.org/abs/1508.07909)**：不断合并高频相邻单元；
- **WordPiece**：与 BPE 相似，但合并标准更偏向提升训练数据似然；
- **Unigram**：从较大候选词表出发，逐步删除贡献较低的子词；
- **SentencePiece**：直接在原始字符流上训练 BPE 或 Unigram，适合不以空格分词的语言。

**Vocabulary（词表）** 是 Token 与整数 ID 的映射集合。词表太小会让序列变长，词表太大则会增加 Embedding 和输出层开销。

**OOV（Out of Vocabulary）** 是“词表外”问题。现代字节级或子词分词器通常能把陌生词拆开，因此比传统整词词表更少遇到完全无法表示的输入。

### 2.3 Embedding：把离散符号变成向量

**Embedding（嵌入）** 是把 Token、句子、图片或其他对象映射为稠密向量的过程。向量中的单个维度通常没有直接的人类语义，但整体方向和距离可以编码某些关系。

需要区分两种常见 Embedding：

1. **模型内部 Token Embedding**：把 Token ID 变成 Transformer 可以计算的向量。
2. **检索用 Embedding**：把整段文本变成便于计算语义相似度的向量，常用于 RAG。可参考 [Sentence Transformers 官方文档](https://www.sbert.net/)。

常见相似度包括：

- **余弦相似度（Cosine Similarity）**：比较方向；
- **点积（Dot Product）**：同时受方向和向量长度影响；
- **欧氏距离（Euclidean Distance）**：比较空间距离。

Embedding 模型不等于生成模型，向量数据库也不等于 Embedding 模型：前者负责生成向量，后者负责存储和检索向量。

### 2.4 上下文窗口与序列长度

**上下文窗口（Context Window）** 是一次推理中模型能够处理的 Token 总预算，通常包括系统提示、历史消息、工具结果、检索文档和预留输出。

上下文窗口很长不代表模型能够同等准确地利用窗口里的每一处信息。还要考虑：

- 重要信息在上下文中的位置；
- 训练时是否覆盖过类似长度；
- 注意力计算和 KV Cache 成本；
- 文档之间是否冲突；
- 输入过长是否稀释关键指令。

上下文窗口也不是长期记忆。请求结束后，模型参数并不会因为读过这段对话而自动更新。

> **面试关注点：** Token 是离散单位，Embedding 是连续向量；Tokenizer 决定文本如何切分，Embedding 层决定 Token ID 如何进入神经网络。

---

<a id="model-architecture"></a>

## 3. 模型架构：Transformer 为什么成为基础

2017 年的论文 **[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** 提出了 Transformer：主要依靠注意力机制处理序列，不再把循环神经网络作为核心。它更适合并行训练，也能够直接建模序列中相距很远的关系。

### 3.1 Self-Attention 与 Q、K、V

**Self-Attention（自注意力）** 让序列中的每个 Token 根据当前上下文，从其他 Token 聚合信息。

核心公式是：

```text
Attention(Q, K, V) = softmax(QKᵀ / √dₖ) V
```

可以用检索系统来类比：

- **Query（Q，查询）**：当前位置想寻找什么信息；
- **Key（K，键）**：每个位置用什么特征供查询匹配；
- **Value（V，值）**：匹配后真正被聚合的内容。

`QKᵀ` 得到相关性分数，除以 `√dₖ` 用于控制数值尺度，Softmax 把分数转成权重，再对 V 加权求和。

**Self-Attention** 的 Q、K、V 来自同一序列；**Cross-Attention（交叉注意力）** 的 Query 与 Key/Value 来自不同序列或模态，例如文本解码器关注图像特征。

### 3.2 Multi-Head Attention、Mask 与位置

**Multi-Head Attention（多头注意力）** 并行计算多组注意力。不同头可以学习不同关系，例如语法依赖、实体指代或局部模式。多头不是“多个模型”，而是一层内部的多个表示子空间。

**Causal Mask（因果掩码）** 阻止 Decoder 在预测当前位置时看到未来 Token。没有它，训练时模型会偷看答案。

注意力本身不天然知道顺序，因此需要位置信息：

- **Positional Encoding（位置编码）**：向 Token 表示加入位置信号；
- **[RoPE（Rotary Position Embedding）](https://arxiv.org/abs/2104.09864)**：通过旋转 Q/K 向量编码相对位置信息；
- **[ALiBi](https://arxiv.org/abs/2108.12409)**：在注意力分数上加入与距离有关的线性偏置。

位置方案会影响长上下文外推能力，但不能单独决定长上下文质量。

### 3.3 Encoder、Decoder 与三类架构

| 架构 | 注意力特点 | 典型用途 | 代表论文 |
|---|---|---|---|
| Encoder-only | 双向理解上下文 | 分类、检索、序列标注 | [BERT](https://arxiv.org/abs/1810.04805) |
| Decoder-only | 因果注意力，逐 Token 生成 | 对话、续写、代码生成 | [GPT-3](https://arxiv.org/abs/2005.14165) |
| Encoder-Decoder | Encoder 理解输入，Decoder 生成输出 | 翻译、摘要、条件生成 | [BART](https://arxiv.org/abs/1910.13461) |

今天通用聊天 LLM 多采用 Decoder-only，但这不意味着其他架构已经失去价值。检索 Embedding、分类和理解任务中，Encoder 模型仍很常见。

### 3.4 FFN、残差连接与归一化

一个 Transformer Block 不只有注意力，还包括：

- **FFN（Feed-Forward Network，前馈网络）**：对每个位置独立执行非线性变换，通常占据大量参数和计算；
- **Residual Connection（残差连接）**：把输入直接加回子层输出，帮助深层网络训练；
- **[LayerNorm](https://arxiv.org/abs/1607.06450)**：对特征做归一化，稳定训练；
- **[RMSNorm](https://arxiv.org/abs/1910.07467)**：使用均方根进行更简化的归一化。

**Pre-Norm** 是先归一化再进入注意力/FFN，**Post-Norm** 是子层输出与残差相加后再归一化。二者在深层网络的训练稳定性上有所不同。

### 3.5 MoE：不是每次都激活全部参数

**[MoE（Mixture of Experts，专家混合）](https://arxiv.org/abs/1701.06538)** 使用多个“专家”子网络和一个路由器。每个 Token 只激活少量专家，从而扩大总参数容量，同时控制单次前向计算量。

需要区分：

- **总参数量**：所有专家参数之和；
- **激活参数量**：一次处理某个 Token 时真正参与计算的参数；
- **路由（Routing）**：决定 Token 进入哪些专家；
- **负载均衡（Load Balancing）**：避免少数专家过载、其他专家闲置。

MoE 的优势是容量与计算可以部分解耦，代价是路由、通信、负载均衡和部署更复杂。

> **面试关注点：** Attention 负责 Token 之间的信息混合，FFN 负责每个 Token 内部的非线性变换；残差和归一化负责让深层网络更容易训练。

---

<a id="model-training"></a>

## 4. 模型训练：参数是怎样学出来的

### 4.1 参数、超参数与一次训练迭代

**Parameter（参数）** 是训练过程中通过梯度更新的数值，例如权重和偏置。

**Hyperparameter（超参数）** 是训练者预先选择的配置，例如学习率、批大小、层数、隐藏维度和优化器设置。

一次典型训练迭代包括：

1. **Forward Pass（前向传播）**：输入经过模型，得到 Logits；
2. **Loss Function（损失函数）**：比较预测与正确答案；
3. **[Backpropagation（反向传播）](https://docs.pytorch.org/docs/stable/autograd.html)**：用链式法则计算每个参数的梯度；
4. **Optimizer Step（优化器更新）**：根据梯度调整参数；
5. 清空或重置梯度，处理下一个 Batch。

**Gradient（梯度）** 表示参数发生微小变化时，损失会如何变化。**Learning Rate（学习率）** 决定每次更新的步幅。

### 4.2 语言模型为什么预测下一个 Token

Decoder-only 语言模型常使用 **Next-Token Prediction（下一个 Token 预测）**：

```text
输入：大模型正在改变软件
目标：模型

输入：大模型正在改变软件模型
目标：开发
```

训练时，一个序列可以并行产生多个预测位置。模型最初只是学习概率分布，但在大规模数据和参数下，为了更准确地预测下一个 Token，它会被迫学习语法、事实关联、风格、代码模式和部分推理结构。

输出层产生 **Logits**，Softmax 将其转换为概率。常见损失是 **[Cross-Entropy Loss（交叉熵损失）](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)**，正确 Token 的预测概率越低，损失通常越大。

### 4.3 Batch、Epoch、Step 与梯度累积

- **Sample**：一条训练样本；
- **Batch**：一次前向和反向传播处理的一组样本；
- **Step / Iteration**：一次参数更新；
- **Epoch**：完整遍历一遍训练数据；
- **Gradient Accumulation（梯度累积）**：连续计算多个小 Batch 的梯度后再更新参数，用较小显存模拟更大的有效 Batch。

对于超大规模、持续混合的数据集，训练过程不一定强调传统意义上的完整 Epoch，更多会按训练 Token 数和 Step 统计。

### 4.4 优化器、学习率与训练稳定性

**[Optimizer（优化器）](https://docs.pytorch.org/docs/stable/optim.html)** 根据梯度决定怎样更新参数。常见方法有 SGD、Adam、AdamW。

重要配套概念包括：

- **Learning Rate Schedule**：训练过程中调整学习率；
- **Warmup**：训练初期逐步提高学习率；
- **Weight Decay**：抑制部分参数无限增大；
- **Gradient Clipping**：限制梯度范数，降低梯度爆炸风险；
- **Checkpoint**：保存模型、优化器和训练状态，便于恢复。

### 4.5 预训练、计算规模与 Scaling Law

**Pretraining（预训练）** 是在大规模通用数据上学习基础能力。模型获得的是参数化的统计规律，不是可以逐条精确查询、随时更新的数据库。

**[Scaling Law（缩放定律）](https://arxiv.org/abs/2001.08361)** 研究模型性能与参数量、数据量、计算量之间的经验关系。核心启示不是“无限加参数”，而是：模型、数据和训练计算需要合理配比。

**Compute-optimal Training** 关注给定计算预算下，参数量与训练 Token 数怎样配置更有效。面试中如果只谈参数规模而忽略数据量和训练计算，答案通常不完整。

### 4.6 分布式训练与混合精度

单张 GPU 无法容纳或高效训练超大模型，因此需要 **[Distributed Training（分布式训练）](https://docs.pytorch.org/docs/stable/distributed.html)**：

- **Data Parallelism（数据并行）**：每张设备持有模型副本，处理不同数据，再同步梯度；
- **Tensor Parallelism（张量并行）**：把同一个矩阵运算拆到多张设备；
- **Pipeline Parallelism（流水线并行）**：把不同层放到不同设备；
- **ZeRO / Sharding（分片）**：分散参数、梯度和优化器状态；
- **Mixed Precision（混合精度）**：结合 FP32、FP16 或 BF16，降低显存与计算成本；
- **Activation Checkpointing**：不保存全部中间激活，反向时重算，以计算换显存。

> **面试关注点：** 数据并行拆 Batch，张量并行拆单层计算，流水线并行拆模型层；实际大模型训练通常组合多种并行方式。

---

<a id="fine-tuning-alignment"></a>

## 5. 微调与对齐：让模型从“续写”走向“助手”

预训练模型擅长补全文本，但用户希望它遵循指令、拒绝危险请求、保持格式并适应业务。这需要训练后阶段。

### 5.1 SFT 与 Instruction Tuning

**SFT（Supervised Fine-Tuning，监督微调）** 使用带标准答案的输入输出对继续训练模型。

**Instruction Tuning（指令微调）** 是 SFT 的常见形式，数据通常是“指令 + 可选上下文 + 理想回答”。它让模型从“继续写下去”转变为“理解并执行用户任务”。

**Full Fine-tuning（全参数微调）** 更新模型全部参数，能力上限高，但训练和存储成本也高。

### 5.2 PEFT、LoRA 与 QLoRA

**PEFT（Parameter-Efficient Fine-Tuning，参数高效微调）** 只训练少量新增或选定参数。

**[LoRA（Low-Rank Adaptation）](https://arxiv.org/abs/2106.09685)** 冻结原模型权重，用两个低秩矩阵近似权重更新：

```text
W' = W + BA
```

其中 `W` 不更新，只训练较小的 `A`、`B`。这样能显著减少可训练参数和适配器存储空间。

**[QLoRA](https://arxiv.org/abs/2305.14314)** 进一步把基础模型量化后冻结，再训练 LoRA 适配器，主要目标是降低微调显存成本。

| 方法 | 更新范围 | 显存/存储成本 | 常见用途 |
|---|---|---:|---|
| 全参数微调 | 全部参数 | 高 | 大规模领域适配、能力深度改变 |
| LoRA | 低秩适配参数 | 较低 | 风格、格式、任务和领域适配 |
| QLoRA | 量化底座 + LoRA | 更低 | 资源受限环境微调较大模型 |

微调并不是更新频繁事实的最佳方案。产品价格、库存、政策等动态知识更适合数据库、搜索或 RAG。

### 5.3 对齐、偏好数据与奖励模型

**Alignment（对齐）** 指让模型行为更符合人类意图、价值约束和产品规则。

**Preference Data（偏好数据）** 通常包含同一问题下的多个回答以及人类或 AI 给出的优劣排序。

**Reward Model（奖励模型）** 学习给回答打分，尝试近似人类偏好。它不是最终生成模型，而是对齐训练中的评价器。

### 5.4 RLHF、PPO、DPO 与 Constitutional AI

**[RLHF（Reinforcement Learning from Human Feedback）](https://arxiv.org/abs/2203.02155)** 使用人类偏好反馈训练模型。经典流程是：

```text
预训练模型 → SFT → 收集偏好排序 → 训练奖励模型 → 强化学习优化策略
```

**[PPO（Proximal Policy Optimization）](https://arxiv.org/abs/1707.06347)** 是 RLHF 中常见的策略优化算法，通过限制每次更新幅度降低训练不稳定。

**[DPO（Direct Preference Optimization）](https://arxiv.org/abs/2305.18290)** 直接利用偏好对优化语言模型，避免显式训练和在线使用独立奖励模型，工程流程通常更简单。

**[Constitutional AI](https://arxiv.org/abs/2212.08073)** 使用一组明确原则指导模型自我批评、修订和基于 AI 反馈的对齐。

| 方法 | 是否显式奖励模型 | 是否使用强化学习循环 | 主要特点 |
|---|---:|---:|---|
| RLHF + PPO | 是 | 是 | 经典但系统复杂、训练敏感 |
| DPO | 否 | 否 | 直接从偏好对学习，流程更简洁 |
| Constitutional AI | 不固定 | 可包含 | 用明确原则生成和筛选反馈 |

对齐不能保证事实正确。一个模型可以非常礼貌、格式完美，却仍然生成错误内容。

> **面试关注点：** SFT 学习“理想回答长什么样”，偏好对齐学习“多个可行回答中哪个更好”；DPO 是偏好优化方法，不等于普通 SFT。

---

<a id="inference-generation"></a>

## 6. 推理与生成：模型怎样逐 Token 输出

训练完成后，模型参数通常保持不变。用户发送请求，模型执行前向计算并生成结果，这个过程叫 **Inference（推理）**。

### 6.1 Autoregressive Generation

**Autoregressive Generation（自回归生成）** 指每次预测一个 Token，再把它追加到上下文中继续预测：

```text
输入：人工智能
输出：正在

输入：人工智能正在
输出：改变

输入：人工智能正在改变
输出：世界
```

因此，生成 100 个 Token 通常需要连续执行多轮解码。模型并不是先在内部写完全文再一次性吐出来。

### 6.2 Prefill、Decode 与 KV Cache

LLM 推理常分为两个阶段：

- **Prefill（预填充）**：并行处理整个输入 Prompt，计算各层表示与注意力缓存；
- **Decode（解码）**：一次生成一个新 Token，重复执行，直到结束。

| 阶段 | 输入特点 | 主要瓶颈 | 常见指标 |
|---|---|---|---|
| Prefill | 一次处理许多输入 Token | 矩阵计算、长上下文 | TTFT |
| Decode | 每轮通常只新增一个 Token | 内存带宽、缓存读取 | TPOT、TPS |

**KV Cache（键值缓存）** 保存之前 Token 在各注意力层产生的 K、V，后续生成时不用反复计算整段历史。它显著加速解码，却会随层数、序列长度、Batch 和精度占用大量显存。

### 6.3 Logits、Softmax 与采样

模型最后输出词表中每个 Token 的 **Logit（未归一化分数）**，再通过 **Softmax** 得到概率分布。

**[Generation Strategy（生成策略）](https://huggingface.co/docs/transformers/generation_strategies)** 决定怎样从概率分布选下一个 Token：

- **Greedy Search（贪心搜索）**：每次选择概率最高的 Token；
- **Sampling（采样）**：按概率随机选取；
- **Top-k**：只在概率最高的 k 个候选中采样；
- **Top-p / Nucleus Sampling**：选择累计概率达到 p 的最小候选集合；
- **Beam Search（束搜索）**：同时保留多个高概率序列，常用于翻译等任务；
- **Stop Sequence（停止序列）**：生成指定字符串或 Token 后结束；
- **Max Tokens**：限制最多输出多少 Token。

**Temperature（温度）** 通常通过缩放 Logits 控制分布平滑度：

- 较低温度：概率更集中，输出更稳定；
- 较高温度：候选更分散，输出更多样；
- 温度不会增加模型知识，也不会修复事实错误；
- `temperature=0` 的具体处理方式依赖 API 或推理框架，不应当作完全统一的数学实现。

### 6.4 Streaming 与 Structured Output

**Streaming（流式输出）** 是服务器在模型仍生成时，持续把增量 Token 或事件发送给客户端。它改善等待体验，但不会减少模型完成全部输出的总计算量。

**Structured Output（结构化输出）** 要求模型输出符合 JSON Schema 等结构。它可以通过提示、约束解码或 API 原生能力实现。结构合法不代表内容正确，仍需业务校验。

> **面试关注点：** KV Cache 省的是重复计算，不是免费内存；长上下文和并发越高，缓存压力通常越大。

---

<a id="prompt-capabilities"></a>

## 7. 提示与能力：Prompt、上下文学习与幻觉

### 7.1 Prompt、System Prompt 与 Context Engineering

**Prompt（提示）** 是提供给模型的输入指令和上下文。

**System Prompt（系统提示）** 通常用于规定角色、规则、工具和输出约束。它在应用层拥有较高优先级，但不是无法被攻击或绕过的安全边界。

**Prompt Engineering（提示工程）** 关注怎样表达任务、提供示例和约束输出。它不会修改模型参数。

**Context Engineering（上下文工程）** 的范围更大：不仅写 Prompt，还决定历史消息、检索文档、工具结果、状态、记忆和权限怎样进入模型上下文。

### 7.2 Zero-shot、Few-shot 与 In-context Learning

- **Zero-shot**：不给任务示例，只给指令；
- **One-shot**：给一个示例；
- **Few-shot**：给少量示例；
- **[In-context Learning（上下文学习）](https://arxiv.org/abs/2005.14165)**：模型根据当前上下文中的指令和示例临时适应任务，不更新参数。

Few-shot 是提示形式，In-context Learning 是模型表现出的上下文适应能力。它们都不等于 Fine-tuning。

### 7.3 Chain of Thought 与推理过程

**[Chain of Thought（CoT，思维链）](https://arxiv.org/abs/2201.11903)** 通过中间步骤帮助模型处理复杂问题。需要注意：

- 输出更长不等于推理一定正确；
- 模型给出的解释可能是事后合理化；
- 产品不一定需要把内部推理过程完整展示给用户；
- 可验证任务应使用代码、计算器、检索或规则校验结果。

**Self-Consistency** 常指对同一问题采样多条推理路径，再对答案聚合。它用更多推理计算换取更高的成功概率，但会增加成本和延迟。

### 7.4 Grounding 与 Hallucination

**Grounding（依据化/落地）** 是让回答基于可验证的输入、文档、数据库、工具结果或现实环境。

**Hallucination（幻觉）** 指模型生成看似合理但缺乏依据、与事实冲突或错误归因的内容。它可能来自：

- 训练数据不足、冲突或过时；
- 问题超出模型知识；
- 检索召回错误；
- 上下文过长或指令冲突；
- 采样随机性；
- 模型倾向于完成语言模式，而不是主动承认未知。

降低幻觉通常需要组合措施：RAG、工具调用、引用、输出约束、置信度策略、拒答规则和人工审核。仅把 Temperature 调低并不能从根本上解决。

---

<a id="rag"></a>

## 8. 知识增强：RAG 的完整生命周期

**[RAG（Retrieval-Augmented Generation，检索增强生成）](https://arxiv.org/abs/2005.11401)** 在生成前从外部知识源检索相关信息，把它们作为上下文提供给模型。它把模型的“参数化记忆”与外部“非参数化记忆”结合起来。

### 8.1 RAG 的离线索引链路

```text
文档加载
  → 清洗与权限标记
  → Chunking
  → Embedding
  → 建立索引
  → 写入向量数据库/搜索引擎
```

**Document Loader** 读取 PDF、网页、数据库、代码仓库等来源。

**Chunking（分块）** 把长文档切成适合检索的片段。块太小会丢上下文，块太大则可能混入无关信息并占用上下文窗口。

常见策略：

- 固定长度切分；
- 按段落、标题或语义边界切分；
- 滑动窗口与重叠；
- 父子块：小块负责召回，大块负责提供上下文。

**Index（索引）** 是为快速检索构建的数据结构。**[FAISS](https://faiss.ai/)** 是相似度搜索与向量聚类库，但它本身不等于完整的业务数据库。

### 8.2 在线检索链路

```text
用户问题
  → Query Rewrite（可选）
  → 生成查询向量
  → 初步召回
  → 权限过滤
  → Rerank
  → 组装上下文
  → LLM 生成并引用来源
```

**Retrieval（检索）** 有三类常见方式：

- **Sparse Retrieval（稀疏检索）**：如 BM25，擅长精确关键词、专有名词和编号；
- **Dense Retrieval（稠密检索）**：使用 Embedding 相似度，擅长语义近似；
- **Hybrid Search（混合检索）**：融合稀疏与稠密结果。

**Recall（召回率）** 关注相关内容是否被找回来，**Precision（精确率）** 关注找回结果中有多少真正相关。RAG 初筛通常优先保证召回，再使用 **Reranker（重排序器）** 提升前几条的精度。Sentence Transformers 官方文档给出了典型的 [Retrieve & Re-Rank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html) 流程。

### 8.3 向量数据库与元数据过滤

**Vector Database（向量数据库）** 提供向量存储、近邻搜索、元数据过滤、更新和服务能力。

RAG 中不能只保存向量，还需要保存：

- 原文和文档 ID；
- 标题、章节、时间和来源；
- 租户、用户和访问权限；
- 版本、有效期和删除状态；
- 可用于引用的 URL 或定位信息。

权限过滤必须发生在把文档送入模型之前，不能只依赖 Prompt 告诉模型“不要泄露”。

### 8.4 RAG、微调和长上下文怎样选择

| 方案 | 主要改变什么 | 适合场景 | 主要风险 |
|---|---|---|---|
| RAG | 推理时提供外部知识 | 动态知识、私有文档、可引用问答 | 召回失败、上下文噪声 |
| 微调 | 模型参数或适配器 | 风格、格式、行为、稳定任务模式 | 数据成本、遗忘、知识更新慢 |
| 长上下文 | 一次提供更多原文 | 少量长文档分析、跨段理解 | 成本高、信息利用不均、冲突 |

真实系统经常组合使用：微调负责行为，RAG 负责知识，长上下文负责承载检索结果和会话状态。

### 8.5 RAG 的常见失败模式

- **Retrieval Miss**：正确文档根本没召回；
- **Ranking Failure**：正确文档有召回，但排名太低；
- **Context Poisoning**：知识库含恶意或错误指令；
- **Lost in the Middle**：关键信息埋在长上下文中间，模型利用不足；
- **Citation Mismatch**：答案与引用来源不一致；
- **Stale Index**：原文已更新，索引仍是旧版本。

因此 RAG 评测至少要拆成“检索质量”和“生成质量”，不能只看最终回答。

> **面试关注点：** RAG 不会自动训练模型；它是在推理时把检索结果加入上下文。检索不到正确内容时，再强的生成模型也很难凭空得到可靠答案。

---

<a id="agent"></a>

## 9. 行动能力：Tool Calling、Agent 与 MCP

LLM 默认只能生成 Token。让它查询数据库、发送请求或修改文件，需要宿主应用提供工具与执行环境。

### 9.1 Function Calling 与 Tool Calling

**[Function Calling / Tool Calling](https://developers.openai.com/api/docs/guides/function-calling)** 是模型按照工具定义生成结构化调用参数的能力。典型流程是：

```text
应用把工具定义发给模型
  → 模型选择工具并生成参数
  → 应用校验参数和权限
  → 应用实际执行工具
  → 工具结果返回模型
  → 模型组织最终回答
```

关键点是：**模型提出调用，宿主程序负责执行。** 模型本身不会因为输出了 `send_email(...)` 就真的发出邮件。

### 9.2 Agent、Workflow 与 ReAct

**AI Agent（智能体）** 通常指能够围绕目标观察环境、制定或调整步骤、调用工具并根据结果继续行动的系统。

**Workflow（工作流）** 是开发者预先定义较固定的步骤和分支；**Agent** 则把更多决策交给模型。两者不是绝对二选一，生产系统通常使用“确定性工作流 + 局部 Agent 决策”。

**[ReAct](https://arxiv.org/abs/2210.03629)** 把 Reasoning 与 Acting 交替结合：模型根据观察决定下一步行动，再根据工具结果继续处理。

Agent 的最小循环可以写成：

```text
Goal → Observe → Decide → Act → Observe → ... → Finish
```

### 9.3 Planning、Memory 与 Human-in-the-loop

**Planning（规划）** 是把目标拆成步骤，可能在执行前一次完成，也可能边执行边调整。

**Memory（记忆）** 在 Agent 系统中可能指：

- **Working Memory**：当前上下文中的临时状态；
- **Episodic Memory**：历史事件或执行轨迹；
- **Semantic Memory**：抽取后的事实和知识；
- **Procedural Memory**：任务步骤、规则或技能。

记忆通常存储在数据库、向量索引或状态系统中，不是模型参数自动永久改变。

**Human-in-the-loop（人在回路）** 在高风险操作前请求人工确认，例如付款、删除数据、发送外部消息或部署生产环境。

### 9.4 MCP 是协议，不是模型

**[MCP（Model Context Protocol）](https://modelcontextprotocol.io/specification/)** 是连接 AI 应用与外部数据、资源和工具的开放协议。它定义客户端、服务器、能力协商和消息交互等机制。

需要避免三个误解：

- MCP 不是大模型；
- MCP 不是 Agent 框架；
- MCP 不等于某一家模型 API 的 Function Calling。

MCP 负责标准化“怎样发现和连接能力”，Agent 负责“何时使用什么能力”，宿主系统负责“怎样安全执行”。

### 9.5 Multi-agent 与单 Agent

**Multi-agent（多智能体）** 让多个 Agent 以不同角色协作，例如研究、实现和审查。它可能提升任务分工和上下文隔离，但也会带来：

- 更多 Token 与延迟；
- 信息传递损耗；
- 重复工作；
- 冲突决策；
- 更复杂的追踪、权限与错误恢复。

如果一个工作流用单 Agent 加明确工具就能完成，不应为了“看起来先进”强行拆成多智能体。

> **面试关注点：** Agent 是由模型、工具、状态、循环控制、权限和错误处理共同构成的系统，不是“给 LLM 加一个循环”就自动可靠。

---

<a id="ai-coding"></a>

## 10. AI 编程：从代码补全到软件开发 Agent

对软件开发者来说，AI 编程不是一个单独功能，而是 AI 逐步进入软件开发生命周期：从补全一行代码，到理解整个仓库、修改多个文件、运行测试、修复 CI，最终生成可审查的 Pull Request。

**[AI Coding Assistant（AI 编程助手）](https://docs.github.com/en/copilot/get-started/what-is-github-copilot)** 通常帮助人类开发者完成局部工作；**Coding Agent（编程智能体）** 则能够围绕任务持续读取环境、修改代码、调用工具并根据结果迭代。

一条较完整的 AI 编程链路是：

```text
需求 / Issue
  → 收集仓库上下文
  → 澄清约束并制定计划
  → 定位文件和符号
  → 生成 Diff / Patch
  → 运行编译、测试和静态检查
  → 根据失败日志定位根因
  → 迭代修改
  → 人工审查 Diff
  → Commit / Pull Request
  → CI 验证与上线反馈
```

### 10.1 Code Completion、FIM 与 Code Generation

**[Code Completion（代码补全）](https://docs.github.com/en/copilot/concepts/completions/code-suggestions)** 根据光标前的代码预测接下来的 Token、表达式或代码块。它强调低延迟和局部上下文，开发者仍掌握编辑节奏。

**[FIM（Fill-in-the-Middle，中间填充）](https://arxiv.org/abs/2207.14255)** 同时利用光标前后的代码，生成中间缺失部分。普通从左到右生成只能看到 Prefix，FIM 还能利用 Suffix，因此更适合在已有函数内部补代码。

```text
Prefix：function calculateTotal(items) {

Middle：模型要补全的内容

Suffix：}
```

**Code Generation（代码生成）** 的范围更大，可以从自然语言、接口定义、测试或示例生成函数、模块甚至多个文件。

**Next Edit Prediction（下一编辑预测）** 不只预测当前光标后面的文字，还预测开发者下一处可能修改的位置和内容。

这些能力的区别主要在上下文和交互粒度：

| 能力 | 主要上下文 | 输出粒度 | 开发者交互 |
|---|---|---|---|
| Code Completion | 光标前局部代码 | Token、行、代码块 | 高频、即时接受或拒绝 |
| FIM | 光标前后代码 | 中间缺失片段 | 在已有结构中插入代码 |
| Code Generation | 需求、示例、接口、文件 | 函数到多文件 | 需要更强验证 |
| Next Edit Prediction | 最近编辑与仓库状态 | 下一处编辑位置和内容 | 预测后续修改序列 |

### 10.2 Code Understanding 与 Repository Context

**Code Understanding（代码理解）** 包括解释代码、识别调用关系、定位 Bug、追踪数据流、分析依赖和总结架构。它不只依赖语言模型能力，也依赖正确的仓库上下文。

**Repository Context（仓库上下文）** 通常包括：

- 目录结构与语言、框架；
- `README`、架构文档和贡献指南；
- `AGENTS.md` 等仓库级开发约定；
- 当前 Git 分支、Diff、最近提交和相关 Issue；
- 类型定义、函数签名、调用点和测试；
- 构建命令、依赖清单和 CI 配置。

把整个仓库无差别塞进上下文通常既昂贵又嘈杂。Coding Agent 更需要 **Context Selection（上下文选择）**：先搜索，再读取最相关文件，并随着证据更新范围。

**Repo Map（仓库地图）** 是对目录、文件、类、函数和依赖关系的压缩表示，用于帮助模型快速找到相关区域。它可以由文本搜索、符号索引、调用图和语法树共同生成。

### 10.3 LSP、AST 与 Tree-sitter

AI 编程工具不能只把代码当普通文本。结构化代码信息能提高定位和修改的准确性。

**[LSP（Language Server Protocol）](https://microsoft.github.io/language-server-protocol/)** 标准化编辑器与语言服务器之间的通信，提供补全、跳转定义、查找引用、悬停文档和诊断等能力。

**AST（Abstract Syntax Tree，抽象语法树）** 用树结构表示代码语法。与纯字符串搜索相比，AST 能区分函数调用、变量声明、类型节点和表达式。

**[Tree-sitter](https://tree-sitter.github.io/tree-sitter/index.html)** 是增量解析器生成工具和解析库，可以在文件编辑时快速更新语法树，并在存在语法错误时尽量提供可用结构。

三者的关系可以理解为：

- LSP 面向“编辑器需要哪些语言能力”；
- AST/CST 面向“代码的语法结构是什么”；
- Tree-sitter 是构建和增量更新语法树的一类工具；
- Coding Agent 可以组合 LSP、Tree-sitter、文本搜索和编译器，而不是只靠模型猜文件位置。

### 10.4 Coding Agent 的执行循环

一个编程 Agent 的核心不是生成一次代码，而是形成闭环：

```text
Observe：读取需求、代码、日志和 Git 状态
Plan：确定影响范围与验证方式
Act：编辑文件、运行命令或查询工具
Verify：检查编译、测试、Lint 和真实行为
Reflect：根据失败证据调整假设
Finish：输出可审查 Diff、验证结果和剩余风险
```

**IDE Agent** 与编辑器状态紧密结合，适合交互式局部修改；**CLI Agent** 直接操作仓库、终端和 Git，适合完整开发任务；**Cloud Agent** 在远程隔离环境异步执行，适合把 Issue 委托为分支或 PR。OpenAI 的 [Codex 用例](https://developers.openai.com/codex/use-cases) 和 GitHub 的 [Copilot Coding Agent 最佳实践](https://docs.github.com/en/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks/best-practices-for-using-copilot-to-work-on-tasks) 都把理解仓库、规划、迭代、测试和审查放在完整工作流中，而不只是代码补全。

### 10.5 Diff、Patch、Checkpoint 与 Rollback

**[Diff](https://git-scm.com/docs/git-diff)** 描述两个版本之间的差异，**[Patch](https://git-scm.com/docs/git-apply)** 是可以应用到文件或 Git 索引的差异文本。

对 AI 编程来说，生成 Patch 通常比重写整个文件更安全，因为它：

- 限定修改范围；
- 方便人工审查；
- 减少覆盖用户未提交改动的风险；
- 可以通过上下文行检测目标代码是否已经变化。

**Checkpoint（检查点）** 是可恢复的中间状态，例如一次小提交、一个工作树或 Agent 保存的任务状态。

**Rollback（回滚）** 是撤销错误变更。可靠的 Coding Agent 应知道自己改了什么，只回滚本任务产生的变化，而不是粗暴清除整个工作区。

### 10.6 Spec-driven、TDD 与验证闭环

**Spec-driven Development（规格驱动开发）** 先明确目标、范围、接口、边界和验收标准，再让 AI 实现。规格越模糊，Agent 越容易“合理地做错事”。

**TDD（Test-Driven Development，测试驱动开发）** 使用 Red-Green-Refactor 循环：先写失败测试，确认它因目标行为缺失而失败，再实现最小代码使其通过，最后重构。

AI 生成代码尤其需要验证，因为语言模型优化的是输出概率，不是“程序一定正确”。常见验证层次：

1. 格式化与 Lint；
2. 类型检查和编译；
3. 单元测试；
4. 集成测试；
5. 端到端或浏览器测试；
6. 安全扫描、依赖审计和性能测试；
7. 人工检查真实业务行为。

**[CI（Continuous Integration，持续集成）](https://docs.github.com/en/actions/get-started/continuous-integration)** 在代码提交后自动执行构建、测试和检查。Agent 本地验证通过不代表 CI 一定通过，因为环境、依赖、操作系统和权限可能不同。

### 10.7 AI Code Review 与 Human Review

**AI Code Review** 可以检查明显 Bug、异常路径、可维护性、安全风险和测试缺口，但它也可能误报、漏报或只依据局部上下文。

GitHub 官方明确提醒：**[Coding Agent 生成的 PR 应像其他贡献一样被认真审查](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/review-copilot-output)**。人工 Review 应重点检查：

- 改动是否真正满足需求；
- 是否意外扩大范围；
- 权限、并发、事务和异常路径；
- 测试是否验证行为而非实现细节；
- 是否引入密钥、恶意依赖或许可证问题；
- 删除和迁移是否可恢复；
- 日志与错误信息是否泄露敏感数据。

AI 可以成为 Reviewer，但不能自动成为自己修改的最终批准者。

### 10.8 HumanEval、SWE-bench 与真实开发能力

**HumanEval** 主要评估根据函数说明生成短代码并通过单元测试的能力。

**[SWE-bench](https://arxiv.org/abs/2310.06770)** 则给模型真实 GitHub Issue 和代码仓库，要求修改代码并通过测试，更接近仓库级软件工程。它要求系统完成定位、理解跨文件依赖、编辑和执行验证，而不只是生成孤立函数。

但 Benchmark 分数不只由模型决定，还受到 Agent Scaffold、工具、上下文检索、执行预算和测试质量影响。OpenAI 对 [SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) 的工作也说明，任务是否清晰、测试是否可靠会显著影响评测可信度。

评估 Coding Agent 时还应关注：

- **Task Success Rate**：真实任务完成率；
- **Patch Correctness**：是否正确且没有破坏其他行为；
- **Scope Discipline**：是否只修改必要范围；
- **Test Pass Rate**：新增和既有测试是否通过；
- **Human Acceptance Rate**：开发者接受或合并变更的比例；
- **Cost to Fix**：完成一个有效修复消耗的时间、Token 和计算；
- **Recovery Ability**：遇到失败时能否定位原因并安全恢复。

### 10.9 Vibe Coding：快速原型不等于无需工程纪律

**Vibe Coding** 通常指开发者主要用自然语言描述意图，让 AI 大量生成代码，再通过运行结果继续调整。它不是严格统一的工程标准，更像一种高 AI 参与度的开发方式。

它适合：原型、一次性脚本、探索交互和低风险内部工具；风险较高的场景包括支付、权限、隐私、医疗、基础设施和难以回滚的数据迁移。

Vibe Coding 的主要风险不是“用了 AI”，而是：开发者不再理解代码、缺少测试、忽略依赖和权限、把“能运行”误认为“正确可维护”。

成熟做法是保留 AI 的速度，同时恢复软件工程约束：小步 Diff、明确规格、自动测试、静态分析、人工 Review、CI 和可回滚发布。

### 10.10 AI 编程的安全边界

Coding Agent 可以读文件、运行命令、访问网络和修改仓库，权限越大，潜在影响越大。

**Sandbox（沙箱）** 用隔离的文件系统、进程、网络或容器限制代码执行。**Approval（审批）** 在高风险操作前要求人类授权。二者解决不同问题：沙箱限制能做什么，审批决定是否允许做。

典型风险包括：

- 仓库文档或依赖中的 Prompt Injection；
- 执行恶意测试、安装脚本或构建脚本；
- 把 API Key、Token、`.env` 或用户数据送入模型；
- 依赖投毒和 Typosquatting；
- 错误删除、强制推送或覆盖未提交改动；
- 自动执行模型生成的 Shell 命令；
- 把不可信网页内容当作高优先级指令。

防护原则包括：最小权限、默认只读、网络白名单、敏感文件隔离、命令审批、依赖锁定、秘密扫描、可审计日志和高风险操作人工确认。

> **面试关注点：** AI 编程系统的质量上限不只取决于代码模型，还取决于上下文选择、工具、执行环境、测试反馈、权限和 Review 流程。

---

<a id="multimodal"></a>

## 11. 多模态与新架构

### 11.1 Multimodal Model 与 VLM

**Multimodal Model（多模态模型）** 能够处理文本、图像、音频、视频等多种信号。

**VLM（Vision-Language Model，视觉语言模型）** 重点连接视觉和语言。常见组成包括：

- **Vision Encoder（视觉编码器）**：把图像转换为视觉特征；
- **Projector / Adapter**：把视觉特征映射到语言模型可接收的空间；
- **Language Model**：结合文本和视觉 Token 进行理解或生成；
- **Cross-modal Alignment（跨模态对齐）**：让图像和文字中的对应语义靠近。

**[CLIP](https://arxiv.org/abs/2103.00020)** 使用图文对比学习，把匹配图像和文本的表示拉近，为跨模态检索和视觉表示学习提供了经典范式。

### 11.2 Diffusion Model

**[Diffusion Model（扩散模型）](https://arxiv.org/abs/2006.11239)** 学习逐步逆转加噪过程，从噪声生成样本。它广泛用于图像、音频和视频生成。

它与自回归 LLM 的主要区别是：

- 自回归模型通常按序逐 Token 生成；
- 扩散模型通常通过多步去噪生成连续或离散数据；
- 二者可以组合，例如语言模型负责规划或文本条件，扩散模型负责图像生成。

### 11.3 Long Context、Reasoning Model 与 Test-time Compute

**Long Context（长上下文）** 关注在一次请求中处理更多 Token。位置编码、注意力机制、训练长度、缓存管理和数据构造都会影响效果。

**Reasoning Model（推理模型）** 通常指针对复杂推理、规划或验证任务进行了专门训练，并可能在回答前使用更多推理计算的模型。这是能力和训练/推理策略描述，不是唯一固定架构。

**Test-time Compute（测试时计算）** 指在推理阶段增加搜索、采样、验证、反思或工具执行等计算，以提高答案质量。常见方式包括：

- 生成多个候选再选择；
- 对中间步骤进行验证；
- 使用搜索树或规划器；
- 调用代码执行器、检索器或定理验证器。

它体现了一种权衡：用更高成本和延迟换取更高的任务成功率。

---

<a id="deployment"></a>

## 12. 推理优化与部署

模型能生成正确答案，不代表它能以可接受的成本支撑生产流量。部署需要同时考虑显存、吞吐量、延迟、稳定性和质量。

### 12.1 Quantization、Distillation 与 Pruning

**Quantization（量化）** 用更低精度表示权重或激活，例如从 FP16 降到 INT8、INT4。它通常能够减少显存和带宽压力，并可能提高推理速度，但质量变化取决于模型、量化算法、硬件和任务。

常见区分：

- **PTQ（Post-Training Quantization）**：训练完成后量化；
- **QAT（Quantization-Aware Training）**：训练时模拟量化误差；
- **Weight-only Quantization**：只量化权重；
- **Weight + Activation Quantization**：同时量化权重和激活。

**[Knowledge Distillation（知识蒸馏）](https://arxiv.org/abs/1503.02531)** 使用较大的 Teacher Model 指导较小的 Student Model 学习，不只是压缩数值精度，而是训练一个更小模型逼近教师行为。

**[Pruning（剪枝）](https://arxiv.org/abs/1510.00149)** 删除不重要的权重、通道、层或结构。非结构化稀疏不一定能直接带来真实硬件加速，部署端还需要相应稀疏算子支持。

| 技术 | 改变对象 | 是否通常需要再训练 | 主要目标 |
|---|---|---:|---|
| 量化 | 数值精度 | 不一定 | 降低显存、带宽和计算成本 |
| 蒸馏 | 模型能力迁移 | 是 | 训练更小的学生模型 |
| 剪枝 | 参数或结构数量 | 经常需要恢复训练 | 删除冗余计算 |

### 12.2 Speculative Decoding

**[Speculative Decoding（推测解码）](https://arxiv.org/abs/2211.17192)** 使用较小 Draft Model 快速提出多个候选 Token，再由较大 Target Model 并行验证。被接受的候选可以一次推进多个位置。

它的目标是在尽量保持目标模型分布不变的前提下降低解码延迟。加速效果取决于草稿模型速度和候选接受率。

### 12.3 Continuous Batching 与 PagedAttention

**Static Batching（静态批处理）** 通常等待一个 Batch 中所有请求结束，短请求可能被长请求拖住。

**Continuous Batching（连续批处理）** 在每个解码迭代动态加入新请求、移除已完成请求，提高 GPU 利用率和吞吐量。

**[PagedAttention](https://arxiv.org/abs/2309.06180)** 借鉴虚拟内存分页管理 KV Cache，减少内存碎片并提高可批处理请求数量。该技术由 [vLLM](https://docs.vllm.ai/en/latest/) 推广到大模型服务场景。

### 12.4 部署指标

- **Latency（延迟）**：请求从开始到完成所需时间；
- **Throughput（吞吐量）**：单位时间处理的请求数或 Token 数；
- **TTFT（Time to First Token）**：从请求发出到第一个输出 Token 的时间；
- **TPOT（Time Per Output Token）**：稳定解码阶段每个输出 Token 的平均耗时；
- **TPS（Tokens Per Second）**：每秒生成或处理的 Token 数，必须说明是单请求、单卡还是系统总体；
- **Concurrency（并发度）**：同时处理的请求数量；
- **SLA / SLO**：服务承诺与内部可靠性目标；
- **OOM（Out of Memory）**：设备或进程内存耗尽。

吞吐量和延迟常常存在张力：更大的 Batch 能提高总体吞吐，却可能增加单个请求等待时间。

### 12.5 Model Serving

**Model Serving（模型服务）** 是把模型包装成稳定在线服务，通常包括：

- 模型加载、权重分片与设备调度；
- Tokenizer 和请求队列；
- 动态批处理与 KV Cache 管理；
- 流式传输、超时、取消和重试；
- 限流、配额、审计和监控；
- 多模型路由、灰度和回滚。

模型服务优化不能只看 Benchmark 的峰值 TPS，还要在真实 Prompt 长度、输出长度、并发和硬件条件下测量尾延迟与稳定性。

> **面试关注点：** TTFT 主要受排队、输入长度和 Prefill 影响；TPOT 更能反映 Decode 速度。回答 TPS 时必须说明统计口径。

---

<a id="evaluation-safety"></a>

## 13. 评测与安全

### 13.1 Perplexity、BLEU 与 ROUGE

**[Perplexity（困惑度，PPL）](https://huggingface.co/docs/transformers/perplexity)** 衡量语言模型对测试序列的预测不确定性，可理解为交叉熵的指数形式。通常同一数据、同一 Tokenization 和同一计算方式下，PPL 越低越好。

但不同分词器会改变 Token 序列，所以跨模型直接比较 PPL 需要非常谨慎。

**[BLEU](https://aclanthology.org/P02-1040/)** 通过 n-gram 精确率等衡量机器翻译输出与参考答案的重合程度。

**[ROUGE](https://aclanthology.org/W04-1013/)** 常用于摘要评测，更关注召回和序列重合。

这些自动指标便宜、可重复，但无法完整衡量事实正确性、逻辑、风格和实际任务价值。

### 13.2 MMLU、HumanEval 与 LLM-as-a-Judge

**[MMLU](https://arxiv.org/abs/2009.03300)** 使用多个学科的选择题评估知识和问题解决能力。

**[HumanEval](https://arxiv.org/abs/2107.03374)** 使用编程题和单元测试评估代码生成，常见指标 **pass@k** 表示生成 k 个候选时至少一个通过测试的概率估计。

**[LLM-as-a-Judge](https://arxiv.org/abs/2306.05685)** 使用语言模型评价其他模型输出，适合难以写精确规则的开放任务，但可能存在位置偏差、风格偏好、自我偏好和领域盲点。

### 13.3 Benchmark 与业务评测

**Benchmark（基准测试）** 是固定数据集和评测流程。常见风险包括：

- **Data Contamination（数据污染）**：测试题进入训练数据；
- **Benchmark Overfitting**：针对榜单优化，不代表真实泛化；
- **Metric Gaming**：优化指标却损害用户体验；
- **Distribution Shift**：线上输入分布与测试集不同。

生产评测应至少分层：

1. 模型基础能力；
2. 检索或工具子系统；
3. 端到端任务成功率；
4. 安全与权限；
5. 延迟、成本和稳定性；
6. 人工抽检与线上反馈。

### 13.4 Prompt Injection 与 Jailbreak

**Prompt Injection（提示注入）** 是攻击者通过输入或外部内容诱导模型忽略原始指令、泄露信息或滥用工具。RAG 文档、网页和邮件都可能成为间接提示注入来源。

**Jailbreak（越狱）** 通常指绕过模型安全约束，使其输出被限制内容。两者有交集，但提示注入更强调应用指令和数据边界受到攻击。

**[OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/)** 将提示注入、敏感信息泄露、不安全输出处理、过度代理权限等列为生成式 AI 应用的重要风险。

### 13.5 Guardrail、Red Teaming 与最小权限

**Guardrail（护栏）** 是输入、输出、工具和业务流程上的约束机制，例如：

- 内容分类与策略过滤；
- JSON Schema 和参数校验；
- 敏感字段脱敏；
- 工具白名单；
- 权限校验与最小权限；
- 高风险操作人工确认；
- 审计日志和异常检测。

**Red Teaming（红队测试）** 主动模拟攻击者寻找系统弱点。

**PII（Personally Identifiable Information）** 是可以识别个人身份的信息。**Data Leakage（数据泄露）** 可能发生在训练数据、Prompt、日志、缓存、检索结果或工具返回值中。

**[NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)** 提供治理、映射、测量和管理 AI 风险的框架。安全不是只给模型加一句“不要泄露”，而是贯穿数据、模型、应用、工具、权限和运维的系统工程。

### 13.6 Interpretability 与 Explainability

**Interpretability（可解释性）** 研究模型内部表示和机制，例如某些神经元、注意力头或特征怎样影响输出。

**Explainability（解释能力）** 更偏向向用户说明为什么给出某个结果。模型生成的自然语言解释不一定忠实反映内部计算，因此不能自动视为证据。

> **面试关注点：** 模型安全和应用安全必须分开看。即使模型拒答能力很强，工具权限设计不当仍可能造成严重事故。

---

<a id="interview"></a>

## 14. 高频面试问题与岗位复习路线

### 14.1 26 道高频问题与回答要点

#### 1. Transformer 相比 RNN 的主要优势是什么？

Transformer 能并行处理序列训练，并通过 Attention 直接建模任意位置之间的关系；RNN 按时间步递归，长距离依赖和并行效率通常更受限制。

#### 2. 为什么 Attention 要除以 `√dₖ`？

当维度增大时，Q、K 点积的方差会变大，Softmax 容易进入饱和区。缩放能稳定数值和梯度。

#### 3. Q、K、V 分别是什么？

Q 表示当前位置要查询什么，K 表示各位置可被匹配的特征，V 是匹配后聚合的内容。它们是输入经过不同线性变换得到的表示。

#### 4. Self-Attention 和 Cross-Attention 有什么区别？

Self-Attention 的 Q/K/V 来自同一序列；Cross-Attention 的 Query 与 Key/Value 来自不同序列或模态。

#### 5. Decoder-only 模型为什么需要 Causal Mask？

为了保证预测当前 Token 时看不到未来 Token，使训练目标与自回归生成一致。

#### 6. Token、Embedding 和向量数据库有什么区别？

Token 是离散文本单位，Embedding 是对象的连续向量表示，向量数据库负责存储和近邻检索这些向量。

#### 7. 预训练和 SFT 有什么区别？

预训练在大规模通用数据上学习语言和世界模式；SFT 使用标注输入输出对，让模型适应指令、任务和回答格式。

#### 8. LoRA 为什么能减少训练成本？

它冻结原权重，只训练低秩更新矩阵，因此可训练参数、梯度和优化器状态都更少。

#### 9. LoRA 和 QLoRA 的区别是什么？

QLoRA 把冻结的基础模型量化后再训练 LoRA 适配器，进一步降低微调显存；LoRA 本身不要求基础模型量化。

#### 10. RLHF 和 DPO 的区别是什么？

经典 RLHF 通常显式训练奖励模型并用 PPO 等强化学习方法优化策略；DPO 直接从偏好对优化语言模型，省去显式奖励模型和在线强化学习循环。

#### 11. RAG 和微调该怎样选择？

动态、私有、可引用知识优先考虑 RAG；风格、格式和稳定行为模式优先考虑微调。两者可以组合。

#### 12. Dense Retrieval 和 Sparse Retrieval 的区别是什么？

Dense Retrieval 使用语义向量相似度，Sparse Retrieval 使用关键词和词频信号。前者擅长语义近似，后者擅长编号、术语和精确匹配。

#### 13. 为什么 RAG 还需要 Reranker？

第一阶段检索要在大规模候选中快速保证召回，Reranker 再用更精确但更昂贵的模型重新排序前若干结果。

#### 14. Agent 和普通聊天机器人有什么区别？

普通聊天机器人主要生成回答；Agent 还包含目标、状态、工具、循环控制、观察结果和继续行动的机制。

#### 15. Function Calling 和 MCP 有什么区别？

Function Calling 是模型 API 表达工具选择与参数的能力；MCP 是 AI 应用发现、连接外部资源和工具的协议。它们可以协作，但不是同一层概念。

#### 16. Prefill 和 Decode 的瓶颈有什么不同？

Prefill 一次处理大量输入 Token，通常更偏计算密集；Decode 每步生成少量 Token，需要频繁读取模型权重和 KV Cache，通常更偏内存带宽受限。

#### 17. KV Cache 为什么占显存？

它为每层、每个 Token、每个并发序列保存 K/V 表示，显存开销随层数、序列长度、Batch 和精度增长。

#### 18. 量化一定会提高速度吗？

不一定。真实加速取决于硬件是否支持相应低精度、算子实现、内存带宽、Batch 和模型结构；量化也可能引入反量化开销或质量损失。

#### 19. 如何评估一个 RAG 系统？

分别评估检索召回、排序质量、上下文相关性、答案正确性、引用一致性、拒答、安全、延迟与成本，再看端到端任务成功率。

#### 20. 如何降低大模型幻觉？

提供可靠上下文或工具、改善检索、要求引用、约束输出、对关键事实做外部验证、允许拒答，并对高风险结果增加人工审核。单靠 Prompt 或低温度不够。

#### 21. Code Completion 和 Coding Agent 有什么区别？

Code Completion 主要根据局部编辑上下文预测后续代码；Coding Agent 围绕任务持续读取仓库、修改多个文件、运行工具、处理失败并交付可审查变更。

#### 22. 为什么 AI 编程需要 FIM？

真实编辑经常发生在已有代码中间。FIM 同时利用 Prefix 和 Suffix，可以生成与函数前后结构都一致的中间片段，比只看左侧上下文更适合代码编辑。

#### 23. AI Coding Agent 怎样理解大型仓库？

它通常组合目录扫描、文本搜索、符号索引、LSP、AST、Repo Map、Git 历史和按需文件读取，逐步收集与任务最相关的上下文，而不是一次塞入整个仓库。

#### 24. 为什么 AI 生成的代码必须运行测试？

语言模型优化的是最可能的代码序列，不是程序语义正确性。编译器、类型检查器和测试能提供可执行反馈，暴露模型仅靠文本判断难以发现的问题。

#### 25. 如何防止 Coding Agent 破坏开发者现有改动？

先检查 Git 状态，限定文件范围，使用小 Patch 或隔离工作树，避免破坏性 Git 命令，记录 Agent 自己的变更，并在回滚时只撤销本任务内容。

#### 26. HumanEval 与 SWE-bench 的区别是什么？

HumanEval 更偏短函数生成和单元测试；SWE-bench 要求根据真实 Issue 理解整个仓库、修改跨文件代码并通过测试，更接近软件工程 Agent 的端到端能力。

### 14.2 按岗位选择复习重点

| 岗位 | 优先掌握 | 需要能深入回答 |
|---|---|---|
| 算法/训练 | Transformer、损失、优化器、并行、SFT、RLHF、DPO | 训练稳定性、数据配比、Scaling Law、分布式训练 |
| 推理/系统 | Prefill、Decode、KV Cache、量化、批处理、并行 | 显存估算、TTFT/TPOT、调度、容错和硬件瓶颈 |
| AI 应用 | Prompt、RAG、Rerank、Tool Calling、Agent、MCP | 权限、安全、评测、状态管理和端到端可靠性 |
| 软件开发 | Code Completion、FIM、仓库上下文、Coding Agent、测试、Diff | LSP/AST、调试闭环、CI、权限隔离和人工 Review |
| 数据/评测 | 数据清洗、去重、Benchmark、LLM-as-a-Judge | 污染检测、评测集设计、人工标注一致性 |
| 产品/架构 | 模型边界、成本、RAG、Agent、Guardrail | 场景拆解、风险分级、SLA 与人机协作 |

复习时不要只背定义。每个核心概念至少要能回答四件事：**它解决什么问题、怎样工作、代价是什么、与相邻技术有什么区别。**

---

<a id="glossary"></a>

## 15. 中英文术语速查表

下表按生命周期排列。点击术语可跳转到论文、标准或官方文档；没有唯一原始定义的工程术语会链接到最接近的一手资料。

| 生命周期 | 术语 | 英文/缩写 | 一句话解释 |
|---|---|---|---|
| 概念 | [人工智能](https://www.nist.gov/artificial-intelligence) | Artificial Intelligence, AI | 让机器执行感知、推理、学习或行动等智能任务的总称 |
| 概念 | 机器学习 | Machine Learning, ML | 从数据中学习映射或规律的方法 |
| 概念 | 深度学习 | Deep Learning, DL | 使用多层神经网络学习表示的机器学习方法 |
| 概念 | 生成式 AI | Generative AI | 生成文本、图像、音频、视频或代码等内容的 AI |
| 概念 | [基础模型](https://arxiv.org/abs/2108.07258) | Foundation Model | 在广泛数据上预训练并适配多种任务的模型 |
| 概念 | 大语言模型 | Large Language Model, LLM | 以语言序列为核心的大规模预训练模型 |
| 数据 | 语料库 | Corpus | 用于训练、微调或评测的文本集合 |
| 数据 | 数据配比 | Data Mixture | 不同语言、领域和任务数据的组合比例 |
| 数据 | 去重 | Deduplication | 删除相同或近似重复样本 |
| 数据 | 数据污染 | Data Contamination | 训练数据包含评测题或受保护数据 |
| 表示 | [Token](https://huggingface.co/docs/transformers/tokenizer_summary) | Token | 模型处理文本的离散单位 |
| 表示 | [Tokenizer](https://huggingface.co/docs/transformers/main/en/main_classes/tokenizer) | Tokenizer | 在文本与 Token ID 之间转换的组件 |
| 表示 | 词表 | Vocabulary | Token 与整数 ID 的映射集合 |
| 表示 | [BPE](https://arxiv.org/abs/1508.07909) | Byte Pair Encoding | 通过合并高频相邻单元构建子词词表 |
| 表示 | OOV | Out of Vocabulary | 输入包含词表无法直接表示的单元 |
| 表示 | [Embedding](https://www.sbert.net/) | Embedding | 把离散对象映射为连续向量 |
| 表示 | 余弦相似度 | Cosine Similarity | 通过向量夹角衡量方向相似性 |
| 表示 | 上下文窗口 | Context Window | 单次推理可以处理的 Token 总预算 |
| 架构 | [Transformer](https://arxiv.org/abs/1706.03762) | Transformer | 以注意力和前馈网络为核心的序列架构 |
| 架构 | 自注意力 | Self-Attention | 让序列位置从同一序列其他位置聚合信息 |
| 架构 | 交叉注意力 | Cross-Attention | Query 与 Key/Value 来自不同输入或模态 |
| 架构 | 查询/键/值 | Query/Key/Value, Q/K/V | 注意力中的匹配请求、索引特征和聚合内容 |
| 架构 | 多头注意力 | Multi-Head Attention, MHA | 在多个表示子空间并行计算注意力 |
| 架构 | 因果掩码 | Causal Mask | 阻止生成模型看到未来 Token |
| 架构 | 位置编码 | Positional Encoding | 向序列表示加入顺序信息 |
| 架构 | [RoPE](https://arxiv.org/abs/2104.09864) | Rotary Position Embedding | 通过旋转 Q/K 编码相对位置 |
| 架构 | [ALiBi](https://arxiv.org/abs/2108.12409) | Attention with Linear Biases | 给注意力分数加入距离相关线性偏置 |
| 架构 | 编码器 | Encoder | 生成输入的上下文化表示 |
| 架构 | 解码器 | Decoder | 结合上下文逐步生成输出 |
| 架构 | 前馈网络 | Feed-Forward Network, FFN | 对每个序列位置执行非线性变换 |
| 架构 | 残差连接 | Residual Connection | 把子层输入直接加回输出 |
| 架构 | [LayerNorm](https://arxiv.org/abs/1607.06450) | Layer Normalization | 在特征维度做归一化以稳定训练 |
| 架构 | [RMSNorm](https://arxiv.org/abs/1910.07467) | Root Mean Square Layer Normalization | 基于均方根的简化归一化方式 |
| 架构 | [MoE](https://arxiv.org/abs/1701.06538) | Mixture of Experts | 每个输入只激活部分专家网络的稀疏架构 |
| 训练 | 参数 | Parameter | 通过训练更新的模型数值 |
| 训练 | 超参数 | Hyperparameter | 训练前选择的模型或优化配置 |
| 训练 | 前向传播 | Forward Pass | 从输入计算模型输出的过程 |
| 训练 | [反向传播](https://docs.pytorch.org/docs/stable/autograd.html) | Backpropagation | 用链式法则计算参数梯度 |
| 训练 | 梯度 | Gradient | 损失相对参数变化的方向和速率 |
| 训练 | [交叉熵](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html) | Cross-Entropy | 分类和语言建模常用损失函数 |
| 训练 | [优化器](https://docs.pytorch.org/docs/stable/optim.html) | Optimizer | 根据梯度更新参数的算法 |
| 训练 | 学习率 | Learning Rate | 每次参数更新的基本步幅 |
| 训练 | Batch | Batch | 一次计算处理的一组样本 |
| 训练 | Epoch | Epoch | 完整遍历一次训练数据 |
| 训练 | 梯度累积 | Gradient Accumulation | 多个小 Batch 累积梯度后再更新 |
| 训练 | 混合精度 | Mixed Precision | 组合不同数值精度训练或推理 |
| 训练 | 数据并行 | Data Parallelism | 不同设备处理不同数据并同步梯度 |
| 训练 | 张量并行 | Tensor Parallelism | 把单层张量运算拆到多设备 |
| 训练 | 流水线并行 | Pipeline Parallelism | 把不同模型层放到不同设备 |
| 训练 | 预训练 | Pretraining | 在大规模通用数据上学习基础能力 |
| 训练 | [Scaling Law](https://arxiv.org/abs/2001.08361) | Scaling Law | 描述性能与参数、数据、计算量的经验关系 |
| 微调 | SFT | Supervised Fine-Tuning | 用标注输入输出对继续训练模型 |
| 微调 | 指令微调 | Instruction Tuning | 用指令和理想回答训练模型遵循任务 |
| 微调 | PEFT | Parameter-Efficient Fine-Tuning | 只训练少量参数的适配方法集合 |
| 微调 | [LoRA](https://arxiv.org/abs/2106.09685) | Low-Rank Adaptation | 用低秩矩阵表示权重更新 |
| 微调 | [QLoRA](https://arxiv.org/abs/2305.14314) | Quantized LoRA | 在量化冻结底座上训练 LoRA |
| 对齐 | 偏好数据 | Preference Data | 标记回答相对优劣的数据 |
| 对齐 | 奖励模型 | Reward Model | 学习预测人类偏好分数的模型 |
| 对齐 | [RLHF](https://arxiv.org/abs/2203.02155) | Reinforcement Learning from Human Feedback | 用人类偏好反馈优化模型行为 |
| 对齐 | [PPO](https://arxiv.org/abs/1707.06347) | Proximal Policy Optimization | 限制策略更新幅度的强化学习算法 |
| 对齐 | [DPO](https://arxiv.org/abs/2305.18290) | Direct Preference Optimization | 直接使用偏好对优化语言模型 |
| 对齐 | [Constitutional AI](https://arxiv.org/abs/2212.08073) | Constitutional AI | 用明确原则指导反馈和行为对齐 |
| 推理 | 推理 | Inference | 使用训练好的参数计算输出 |
| 推理 | 自回归生成 | Autoregressive Generation | 把已生成 Token 作为下一步输入 |
| 推理 | Prefill | Prefill | 并行处理初始输入上下文的阶段 |
| 推理 | Decode | Decode | 逐 Token 生成输出的阶段 |
| 推理 | KV Cache | Key-Value Cache | 缓存历史 Token 的注意力 K/V |
| 推理 | Logit | Logit | Softmax 前的未归一化预测分数 |
| 推理 | Softmax | Softmax | 把一组分数转换为概率分布 |
| 推理 | 温度 | Temperature | 控制生成概率分布集中程度的参数 |
| 推理 | Top-k | Top-k Sampling | 在概率最高的 k 个候选中采样 |
| 推理 | Top-p | Nucleus Sampling | 在累计概率达到 p 的候选集合中采样 |
| 推理 | Beam Search | Beam Search | 并行保留多个高概率候选序列 |
| 提示 | Prompt | Prompt | 给模型的指令、数据和上下文 |
| 提示 | System Prompt | System Prompt | 应用设置的高优先级角色和规则 |
| 提示 | Zero-shot | Zero-shot | 不提供示例完成任务 |
| 提示 | Few-shot | Few-shot | 在上下文中提供少量任务示例 |
| 提示 | [上下文学习](https://arxiv.org/abs/2005.14165) | In-context Learning | 不更新参数而根据上下文临时适应任务 |
| 提示 | [思维链](https://arxiv.org/abs/2201.11903) | Chain of Thought, CoT | 使用中间步骤辅助复杂任务 |
| 提示 | 结构化输出 | Structured Output | 让输出满足 JSON Schema 等结构约束 |
| 可靠性 | Grounding | Grounding | 让回答基于可验证来源或工具结果 |
| 可靠性 | 幻觉 | Hallucination | 生成流畅但错误、虚构或无依据的内容 |
| RAG | [RAG](https://arxiv.org/abs/2005.11401) | Retrieval-Augmented Generation | 检索外部知识后再生成答案 |
| RAG | Chunking | Chunking | 把长文档切成可检索片段 |
| RAG | 稀疏检索 | Sparse Retrieval | 使用关键词和稀疏向量检索 |
| RAG | 稠密检索 | Dense Retrieval | 使用语义 Embedding 检索 |
| RAG | 混合检索 | Hybrid Search | 融合稀疏和稠密检索结果 |
| RAG | 召回率 | Recall | 相关结果被找回的比例 |
| RAG | 精确率 | Precision | 找回结果中真正相关的比例 |
| RAG | 重排序 | Reranking | 对初步召回候选做更精确排序 |
| RAG | [向量索引](https://faiss.ai/) | Vector Index | 用于快速近邻搜索的数据结构 |
| Agent | [工具调用](https://developers.openai.com/api/docs/guides/function-calling) | Tool Calling | 模型生成工具选择和结构化参数 |
| Agent | [ReAct](https://arxiv.org/abs/2210.03629) | Reasoning and Acting | 交替进行推理、行动和观察 |
| Agent | Planning | Planning | 把目标拆成可执行步骤 |
| Agent | Memory | Memory | 在模型外保存短期或长期状态 |
| Agent | Workflow | Workflow | 预定义步骤和分支的执行流程 |
| Agent | [MCP](https://modelcontextprotocol.io/specification/) | Model Context Protocol | 连接 AI 应用与资源、提示和工具的协议 |
| Agent | 多智能体 | Multi-agent | 多个 Agent 分工协作的系统 |
| Agent | 人在回路 | Human-in-the-loop | 在关键环节引入人工判断或批准 |
| AI 编程 | [AI 编程助手](https://docs.github.com/en/copilot/get-started/what-is-github-copilot) | AI Coding Assistant | 在编码、解释、测试和审查中辅助开发者的 AI 工具 |
| AI 编程 | [代码补全](https://docs.github.com/en/copilot/concepts/completions/code-suggestions) | Code Completion | 根据编辑上下文预测后续代码 |
| AI 编程 | [FIM](https://arxiv.org/abs/2207.14255) | Fill-in-the-Middle | 根据前缀和后缀生成中间缺失代码 |
| AI 编程 | 下一编辑预测 | Next Edit Prediction | 预测下一处修改位置及内容 |
| AI 编程 | 代码生成 | Code Generation | 从需求、接口或示例生成代码 |
| AI 编程 | 代码理解 | Code Understanding | 解释代码并分析符号、依赖和数据流 |
| AI 编程 | 仓库上下文 | Repository Context | 与当前任务相关的代码、文档、Git 和配置 |
| AI 编程 | 仓库地图 | Repository Map, Repo Map | 对文件、符号和依赖关系的压缩表示 |
| AI 编程 | 上下文选择 | Context Selection | 搜索并选择与任务最相关的仓库信息 |
| AI 编程 | 编程智能体 | Coding Agent | 能读取、修改、执行和验证代码的 Agent |
| AI 编程 | IDE Agent | IDE Agent | 与编辑器光标、文件和诊断状态结合的编程 Agent |
| AI 编程 | CLI Agent | CLI Agent | 通过终端、文件系统和 Git 操作仓库的 Agent |
| AI 编程 | Cloud Agent | Cloud Agent | 在远程隔离环境异步执行开发任务的 Agent |
| AI 编程 | [LSP](https://microsoft.github.io/language-server-protocol/) | Language Server Protocol | 标准化编辑器与语言服务器通信的协议 |
| AI 编程 | AST | Abstract Syntax Tree | 表示代码语法结构的抽象树 |
| AI 编程 | [Tree-sitter](https://tree-sitter.github.io/tree-sitter/index.html) | Tree-sitter | 增量解析代码并生成语法树的工具 |
| AI 编程 | [Diff](https://git-scm.com/docs/git-diff) | Diff | 两个代码版本之间的差异 |
| AI 编程 | [Patch](https://git-scm.com/docs/git-apply) | Patch | 可应用到文件或索引的差异文本 |
| AI 编程 | Checkpoint | Checkpoint | 可供恢复和审查的中间状态 |
| AI 编程 | Rollback | Rollback | 安全撤销错误变更的过程 |
| AI 编程 | 规格驱动开发 | Spec-driven Development | 先明确规格与验收标准再实现 |
| AI 编程 | 测试驱动开发 | Test-Driven Development, TDD | 按失败测试、实现、重构的循环开发 |
| AI 编程 | [持续集成](https://docs.github.com/en/actions/get-started/continuous-integration) | Continuous Integration, CI | 自动构建和测试频繁提交的代码 |
| AI 编程 | AI 代码审查 | AI Code Review | 使用 AI 分析 Diff 并提出问题或修复建议 |
| AI 编程 | [SWE-bench](https://arxiv.org/abs/2310.06770) | SWE-bench | 评估模型解决真实仓库 Issue 的基准 |
| AI 编程 | Vibe Coding | Vibe Coding | 以自然语言驱动大量代码生成和迭代的开发方式 |
| AI 编程 | 沙箱 | Sandbox | 隔离不可信代码执行影响的环境 |
| AI 编程 | 审批 | Approval | 高风险工具或命令执行前的人类授权 |
| AI 编程 | 任务成功率 | Task Success Rate | Agent 正确完成真实开发任务的比例 |
| AI 编程 | 人工接受率 | Human Acceptance Rate | AI 变更被开发者接受或合并的比例 |
| AI 编程 | 修复成本 | Cost to Fix | 完成一个有效修改消耗的时间、Token 和计算 |
| 多模态 | [CLIP](https://arxiv.org/abs/2103.00020) | Contrastive Language-Image Pretraining | 使用图文对比学习对齐视觉与语言表示 |
| 多模态 | VLM | Vision-Language Model | 联合处理视觉和语言的模型 |
| 多模态 | [扩散模型](https://arxiv.org/abs/2006.11239) | Diffusion Model | 学习逐步逆转加噪过程的生成模型 |
| 部署 | 量化 | Quantization | 用更低数值精度表示权重或激活 |
| 部署 | [知识蒸馏](https://arxiv.org/abs/1503.02531) | Knowledge Distillation | 让小模型学习大模型行为 |
| 部署 | [剪枝](https://arxiv.org/abs/1510.00149) | Pruning | 删除不重要的参数或结构 |
| 部署 | [推测解码](https://arxiv.org/abs/2211.17192) | Speculative Decoding | 小模型起草、大模型并行验证候选 Token |
| 部署 | 连续批处理 | Continuous Batching | 动态加入和移除解码请求 |
| 部署 | [PagedAttention](https://arxiv.org/abs/2309.06180) | PagedAttention | 分页管理 KV Cache 以减少碎片 |
| 部署 | TTFT | Time to First Token | 请求到首个输出 Token 的时间 |
| 部署 | TPOT | Time Per Output Token | 每个输出 Token 的平均生成时间 |
| 部署 | 吞吐量 | Throughput | 单位时间处理的请求或 Token 数 |
| 评测 | [困惑度](https://huggingface.co/docs/transformers/perplexity) | Perplexity, PPL | 衡量语言模型预测不确定性的指标 |
| 评测 | [BLEU](https://aclanthology.org/P02-1040/) | BLEU | 基于 n-gram 精确率的翻译指标 |
| 评测 | [ROUGE](https://aclanthology.org/W04-1013/) | ROUGE | 常用于摘要的文本重合指标 |
| 评测 | [MMLU](https://arxiv.org/abs/2009.03300) | Massive Multitask Language Understanding | 多学科选择题能力基准 |
| 评测 | [HumanEval](https://arxiv.org/abs/2107.03374) | HumanEval | 使用单元测试评估代码生成的基准 |
| 评测 | [LLM-as-a-Judge](https://arxiv.org/abs/2306.05685) | LLM-as-a-Judge | 使用语言模型评价模型输出 |
| 安全 | [Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) | Prompt Injection | 用恶意输入改变应用原始指令或行为 |
| 安全 | Jailbreak | Jailbreak | 绕过模型安全约束的攻击方式 |
| 安全 | Guardrail | Guardrail | 约束输入、输出、权限和工具的机制 |
| 安全 | PII | Personally Identifiable Information | 能够识别个人身份的信息 |
| 安全 | Red Teaming | Red Teaming | 模拟攻击者主动发现系统弱点 |
| 安全 | 可解释性 | Interpretability | 研究模型内部机制与输出原因 |

---

## 结语：把术语放回系统里

大模型不是单一算法，而是一条长链路：数据决定模型看过什么，Tokenizer 决定输入怎样离散化，Transformer 决定信息怎样流动，训练与对齐决定参数和行为，推理系统决定成本与速度，RAG 和 Agent 决定模型怎样接入知识与现实世界，评测和安全则决定它是否真正可用。

面试时，最有价值的回答通常不是背出英文全称，而是能够说明：

1. 这个技术解决什么问题；
2. 它处在生命周期的哪一环；
3. 它依赖什么输入，产生什么输出；
4. 它与相邻方案如何取舍；
5. 它在生产环境里会怎样失败。

当这些概念连成系统，术语就不再是需要死记的缩写，而会成为你分析大模型问题的工具。
