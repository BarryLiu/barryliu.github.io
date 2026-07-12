# AI大模型应用学习代码示例

本目录包含了AI大模型应用学习的各个阶段的代码示例。

## 文件说明

### 前置：NumPy基础（必须学习）
**文件**: `00_numpy_basics.py`

**学习内容**：
- NumPy数组基础操作
- 向量运算（点积、范数、相似度）
- 矩阵操作
- Embedding相关操作
- 广播机制

**为什么重要**：
- ✅ **NumPy是应用开发路径中唯一需要学习的"框架"**
- ✅ 向量计算是AI应用的核心（相似度、Embedding操作）
- ❌ **不需要** PyTorch/TensorFlow（除非要训练模型）

**运行方式**：
```bash
python tests/00_numpy_basics.py
```

**学习时间**：1-2周

---

### 阶段一：基础API调用
**文件**: `01_basic_api_call.py`

**学习内容**：
- HTTP请求处理
- API认证与密钥管理
- 错误处理与重试机制
- 响应解析

**运行方式**：
```bash
# 需要设置OPENAI_API_KEY环境变量
export OPENAI_API_KEY="your-api-key-here"
python tests/01_basic_api_call.py
```

### 阶段二：Prompt工程
**文件**: `02_prompt_engineering.py`

**学习内容**：
- 编写清晰的指令
- Few-shot示例
- 角色设定
- 输出格式控制
- Chain-of-Thought提示

**运行方式**：
```bash
python tests/02_prompt_engineering.py
```

### 阶段三：向量化与Embedding
**文件**: `03_embedding_and_vector.py`

**学习内容**：
- 理解向量和Embedding概念
- 文本向量化
- 向量相似度计算
- 基础向量检索

**运行方式**：
```bash
python tests/03_embedding_and_vector.py
```

**注意**：本示例使用简化的向量生成方法，仅用于理解概念。实际应用中应使用专业的Embedding API。

### 阶段三：RAG应用
**文件**: `04_rag_application.py`

**学习内容**：
- 文档加载与预处理
- 文本分块策略
- 检索策略设计
- 上下文注入
- RAG流程实现

**运行方式**：
```bash
python tests/04_rag_application.py
```

### 阶段四：Agent开发
**文件**: `05_agent_development.py`

**学习内容**：
- 理解Agent工作原理
- ReAct模式实现
- Tool使用
- Agent循环与决策
- 多Agent协作

**运行方式**：
```bash
python tests/05_agent_development.py
```

### 阶段六：部署与生产实践
**文件**: `06_deployment.py`

**学习内容**：
- API服务设计
- 错误处理与日志
- 速率限制
- 缓存策略
- 监控与追踪

**运行方式**：
```bash
python tests/06_deployment.py
```

## 学习建议

1. **按顺序学习**：建议按照文件编号顺序学习，每个阶段都有前置知识要求。

2. **动手实践**：
   - 阅读代码并理解每个示例
   - 修改参数观察不同效果
   - 尝试实现自己的变体

3. **结合实际**：
   - 将示例代码与实际的API调用结合
   - 使用真实的Embedding模型
   - 部署到实际环境测试

4. **扩展练习**：
   - 每个示例都可以进一步扩展
   - 尝试组合多个技术
   - 解决实际问题

## 依赖说明

基础示例只需要Python标准库，但实际应用需要安装：

```bash
# 基础依赖
pip install requests numpy

# 实际应用可能需要
pip install openai
pip install langchain
pip install chromadb  # 向量数据库
pip install fastapi uvicorn  # Web框架
```

## 注意事项

1. **API密钥**：使用真实API时需要设置相应的环境变量
2. **成本控制**：注意API调用的成本，合理使用
3. **错误处理**：实际应用中需要更完善的错误处理
4. **安全性**：不要将API密钥提交到代码仓库

## 下一步

完成所有示例后，可以：
1. 阅读 `docs/学习路线.md` 了解更深入的内容
2. 尝试实现完整的项目
3. 探索更多高级技术
4. 参与开源项目

