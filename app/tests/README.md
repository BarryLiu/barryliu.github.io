# 框架学习包

本目录包含 AI 应用开发与模型训练相关的学习示例：基础 API、NumPy、PyTorch、TensorFlow、LangChain、LLM 微调和 Google ADK。

## 📦 包结构

```
tests/
├── t00_basic/      # API调用、Prompt、Embedding、RAG、Agent基础
├── t01_numpy/      # NumPy学习包（应用开发必须）
├── t02_pytorch/    # PyTorch学习包（模型训练）
├── t03_tensorflow/ # TensorFlow学习包（模型训练）
├── t04_langchain/  # LangChain、RAG、Agent、Memory
├── t05_llm/        # 小模型训练与上传示例
├── t06_adk/        # Google ADK 2.x Agent开发
└── README.md       # 本文件
```

## 🎯 学习路径选择

### 路径一：大模型应用开发（推荐90%的学习者）

**需要学习的框架**：
- ✅ **NumPy**（必须，1-2周）
- ✅ **LangChain / Google ADK**（Agent、RAG、工具调用）
- ❌ PyTorch（不需要）
- ❌ TensorFlow（不需要）

**学习顺序**：
1. `t01_numpy/01_basics.py` - 基础操作
2. `t01_numpy/02_vector_operations.py` - **向量操作（核心）**
3. `t04_langchain/03_agent.py` - LangChain Agent
4. `t06_adk/01_tools.py` - Google ADK 工具基础
5. `t06_adk/02_run_agent.py` - Google ADK 2.x Agent 调用
6. `t06_adk/03_agent_team.py` - ADK 智能体团队
7. `t06_adk/04_streaming_agent.py` - ADK 流式智能体
8. `t06_adk/05_graph_workflow.py` - ADK 图工作流
9. `t06_adk/06_dynamic_workflow.py` - ADK 动态工作流
10. `t06_adk/07_writing_workflow.py` - ADK 写作工作流
11. `t06_adk/08_loop_agent_digital_human.py` - ADK LoopAgent 数字人循环工作流

**为什么只需要NumPy？**
- 向量计算是AI应用的核心（相似度、Embedding）
- API调用大模型不需要训练框架
- RAG、Agent等应用只需要向量运算

---

### 路径二：模型训练与开发（高级路径）

**需要学习的框架**：
- ✅ NumPy（基础，必须）
- ✅ **PyTorch**（推荐，2-3个月）或 TensorFlow（可选）

**学习顺序**：
1. 先学NumPy基础
2. 选择PyTorch或TensorFlow深入学习
3. 学习神经网络和训练流程

**什么时候需要？**
- 训练自己的模型
- 深度定制微调
- 研究模型架构

---

## 📚 各包详细说明

### NumPy包 (`numpy/`)

**重要性**：⭐⭐⭐⭐⭐（应用开发必须）

**包含文件**：
- `01_basics.py` - 基础操作
- `02_vector_operations.py` - 向量操作（核心）
- `03_advanced.py` - 高级特性
- `README.md` - 详细说明

**学习时间**：1-2周

**核心技能**：
- 向量相似度计算（余弦相似度）
- Embedding操作
- 批量处理

**运行方式**：
```bash
python tests/numpy/01_basics.py
python tests/numpy/02_vector_operations.py
python tests/numpy/03_advanced.py
```

---

### PyTorch包 (`pytorch/`)

**重要性**：⭐⭐（仅模型训练需要）

**包含文件**：
- `01_basics.py` - 基础操作
- `02_neural_networks.py` - 神经网络
- `03_training.py` - 完整训练流程
- `README.md` - 详细说明

**学习时间**：2-3个月

**核心技能**：
- Tensor操作
- 自动微分（Autograd）
- 神经网络构建
- 模型训练

**运行方式**：
```bash
# 需要先安装
pip install torch

python tests/pytorch/01_basics.py
python tests/pytorch/02_neural_networks.py
python tests/pytorch/03_training.py
```

---

### TensorFlow包 (`tensorflow/`)

**重要性**：⭐⭐（仅模型训练需要）

**包含文件**：
- `01_basics.py` - 基础操作
- `02_keras_models.py` - Keras模型
- `README.md` - 详细说明

**学习时间**：2-3个月

**核心技能**：
- Tensor操作
- GradientTape（自动微分）
- Keras模型构建
- 模型训练

**运行方式**：
```bash
# 需要先安装
pip install tensorflow

python tests/tensorflow/01_basics.py
python tests/tensorflow/02_keras_models.py
```

---

## 🔄 框架对比

| 特性 | NumPy | PyTorch | TensorFlow |
|------|-------|---------|-----------|
| **应用开发** | ✅ 必须 | ❌ 不需要 | ❌ 不需要 |
| **模型训练** | ❌ 不支持 | ✅ 推荐 | ✅ 可选 |
| **学习难度** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **学习时间** | 1-2周 | 2-3个月 | 2-3个月 |
| **GPU支持** | ❌ | ✅ | ✅ |
| **自动微分** | ❌ | ✅ | ✅ |

## 💡 学习建议

### 对于应用开发者

1. **重点学习NumPy**
   - 掌握向量运算
   - 理解相似度计算
   - 学会批量处理

2. **跳过PyTorch/TensorFlow**
   - 应用开发不需要
   - 节省学习时间
   - 专注应用技能

3. **实际工作流**
   ```python
   import numpy as np  # ✅ 需要
   import requests     # ✅ 需要
   # import torch      # ❌ 不需要
   ```

### 对于模型训练者

1. **先学NumPy基础**
   - 所有框架的基础

2. **选择PyTorch（推荐）**
   - 研究领域更主流
   - 更灵活易用
   - 社区活跃

3. **或选择TensorFlow**
   - 企业环境常用
   - 部署有优势
   - 生产环境成熟

## 📖 详细文档

每个包都有详细的README文档：
- [NumPy README](t01_numpy/README.md)
- [PyTorch README](t02_pytorch/README.md)
- [TensorFlow README](t03_tensorflow/README.md)

## 🚀 快速开始

### 应用开发路径（推荐）

```bash
# 1. 学习NumPy基础
python tests/numpy/01_basics.py

# 2. 重点学习向量操作
python tests/numpy/02_vector_operations.py

# 3. 学习高级特性
python tests/numpy/03_advanced.py
```

### 模型训练路径

```bash
# 1. 先学NumPy
python tests/numpy/02_vector_operations.py

# 2. 学习PyTorch（推荐）
pip install torch
python tests/pytorch/01_basics.py
python tests/pytorch/02_neural_networks.py
python tests/pytorch/03_training.py

# 或学习TensorFlow
pip install tensorflow
python tests/tensorflow/01_basics.py
python tests/tensorflow/02_keras_models.py
```

## ❓ 常见问题

**Q: 应用开发必须学PyTorch吗？**  
A: 不需要。只需要NumPy。

**Q: PyTorch和TensorFlow都要学吗？**  
A: 不需要。选择一个深入学习即可，PyTorch更推荐。

**Q: NumPy难学吗？**  
A: 不难。1-2周即可掌握应用所需的基础。

**Q: 什么时候需要PyTorch/TensorFlow？**  
A: 只有训练/微调模型时才需要。

## 📝 总结

- **应用开发**：只需要NumPy ✅
- **模型训练**：需要PyTorch或TensorFlow ✅
- **建议**：先走应用开发路径，积累经验后再决定是否需要深入学习训练框架

更多详细信息请查看各包的README文档。
