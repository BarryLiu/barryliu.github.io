# TensorFlow学习包

TensorFlow是Google开发的深度学习框架，主要用于**模型训练和部署**。

## ⚠️ 重要说明

**对于大模型应用开发**：
- ❌ **通常不需要** TensorFlow
- ✅ 只需要 NumPy + API调用

**什么时候需要TensorFlow**：
- ✅ 训练自己的模型
- ✅ 使用TensorFlow Serving部署
- ✅ 某些企业环境要求
- ✅ 研究模型架构

**PyTorch vs TensorFlow**：
- **PyTorch**：研究领域更主流，更灵活
- **TensorFlow**：生产部署有优势，企业环境常用
- **建议**：选择一个深入学习即可，PyTorch更推荐

## 文件说明

### 01_basics.py - 基础操作
- Tensor创建
- Tensor属性
- Tensor运算
- 梯度计算（GradientTape）
- GPU操作
- NumPy互操作
- 即时执行模式

**学习时间**：1-2周

### 02_keras_models.py - Keras模型
- Sequential模型
- 函数式API
- CNN模型
- 训练示例
- 模型保存和加载
- 回调函数
- 迁移学习

**学习时间**：2-3周

## 学习顺序

1. **基础操作**（01_basics.py）
2. **Keras模型**（02_keras_models.py）

## 运行示例

```bash
# 需要先安装TensorFlow
pip install tensorflow

# 基础操作
python tests/tensorflow/01_basics.py

# Keras模型
python tests/tensorflow/02_keras_models.py
```

## 核心概念

### 即时执行（Eager Execution）

```python
# TensorFlow 2.x默认启用
a = tf.constant(2.0)
b = tf.constant(3.0)
c = a + b
print(c.numpy())  # 5.0
```

### 自动微分（GradientTape）

```python
x = tf.Variable(2.0)
with tf.GradientTape() as tape:
    y = x ** 2
dy_dx = tape.gradient(y, x)  # 4.0
```

### Keras模型

```python
model = keras.Sequential([
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
model.fit(x_train, y_train, epochs=10)
```

## 与NumPy的关系

- **NumPy**：CPU计算，用于数据处理
- **TensorFlow**：GPU加速，用于模型训练
- **互操作**：可以相互转换

## 学习建议

1. **先掌握NumPy**：NumPy是基础
2. **理解即时执行**：TensorFlow 2.x的核心
3. **学习Keras**：高级API更易用
4. **实践训练流程**：完整的训练循环

## 应用开发 vs 模型训练

| 场景 | 需要TensorFlow? | 需要NumPy? |
|------|----------------|-----------|
| API调用大模型 | ❌ | ✅ |
| RAG应用 | ❌ | ✅ |
| Agent开发 | ❌ | ✅ |
| 训练模型 | ✅ | ✅ |
| 模型部署（TF Serving） | ✅ | ✅ |
| 研究模型 | ⚠️ 可选 | ✅ |

## PyTorch vs TensorFlow

| 特性 | PyTorch | TensorFlow |
|------|---------|-----------|
| 研究领域 | ✅ 更主流 | ⚠️ 较少 |
| 生产部署 | ⚠️ 一般 | ✅ 更好 |
| 易用性 | ✅ 更直观 | ⚠️ 稍复杂 |
| 社区 | ✅ 活跃 | ✅ 活跃 |
| 推荐 | ✅ 更推荐 | ⚠️ 可选 |

## 下一步

如果目标是**应用开发**：
- 回到 NumPy 学习
- 学习 API 调用
- 学习 RAG/Agent

如果目标是**模型训练**：
- 推荐学习 PyTorch（更主流）
- 或深入学习 TensorFlow
- 学习模型优化和部署

