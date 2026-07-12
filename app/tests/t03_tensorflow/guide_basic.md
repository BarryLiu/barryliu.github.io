# TensorFlow 常用函数参考

本文档列出了TensorFlow中最常用的函数及其作用，适用于模型训练和开发。

## Tensor创建

### 基础创建

| 函数 | 作用 | 示例 |
|------|------|------|
| `tf.constant()` | 创建常量Tensor | `tf.constant([1, 2, 3])` |
| `tf.zeros()` | 创建全零Tensor | `tf.zeros((3, 4))` |
| `tf.ones()` | 创建全1Tensor | `tf.ones((3, 4))` |
| `tf.fill()` | 创建填充指定值的Tensor | `tf.fill((3, 4), 5)` |
| `tf.range()` | 创建等差Tensor | `tf.range(0, 10, 2)` |
| `tf.linspace()` | 创建等间隔Tensor | `tf.linspace(0.0, 1.0, 5)` |
| `tf.random.normal()` | 创建正态分布Tensor | `tf.random.normal((3, 4))` |
| `tf.random.uniform()` | 创建均匀分布Tensor | `tf.random.uniform((3, 4))` |
| `tf.random.truncated_normal()` | 截断正态分布 | `tf.random.truncated_normal((3, 4))` |
| `tf.eye()` | 创建单位矩阵 | `tf.eye(3)` |

### 从NumPy创建

| 函数 | 作用 | 示例 |
|------|------|------|
| `tf.constant(np_arr)` | 从NumPy数组创建 | `tf.constant(np.array([1, 2, 3]))` |
| `tf.convert_to_tensor()` | 转换为Tensor | `tf.convert_to_tensor(arr)` |

### 变量创建

| 函数 | 作用 | 示例 |
|------|------|------|
| `tf.Variable()` | 创建变量 | `tf.Variable([1, 2, 3])` |
| `.assign()` | 赋值 | `var.assign([4, 5, 6])` |
| `.read_value()` | 读取值 | `var.read_value()` |

## Tensor属性

| 属性/方法 | 作用 | 示例 |
|-----------|------|------|
| `.shape` | Tensor形状 | `tensor.shape` |
| `.dtype` | 数据类型 | `tensor.dtype` |
| `.device` | 设备 | `tensor.device` |
| `.numpy()` | 转为NumPy数组 | `tensor.numpy()` |
| `tf.size()` | 获取大小 | `tf.size(tensor)` |
| `tf.rank()` | 获取维度 | `tf.rank(tensor)` |

## Tensor操作

### 索引和切片

| 操作 | 作用 | 示例 |
|------|------|------|
| `tensor[i]` | 索引单个元素 | `tensor[0]` |
| `tensor[i:j]` | 切片 | `tensor[1:5]` |
| `tensor[i, j]` | 多维索引 | `tensor[0, 1]` |
| `tensor[:, j]` | 选择列 | `tensor[:, 1]` |
| `tensor[i, :]` | 选择行 | `tensor[1, :]` |
| `tf.gather()` | 按索引收集 | `tf.gather(tensor, indices)` |
| `tf.gather_nd()` | 多维索引收集 | `tf.gather_nd(tensor, indices)` |

### 形状操作

| 函数 | 作用 | 示例 |
|------|------|------|
| `tf.reshape()` | 改变形状 | `tf.reshape(tensor, (3, 4))` |
| `tf.expand_dims()` | 增加维度 | `tf.expand_dims(tensor, axis=0)` |
| `tf.squeeze()` | 移除单维度 | `tf.squeeze(tensor)` |
| `tf.transpose()` | 转置 | `tf.transpose(tensor)` |
| `tf.concat()` | 连接Tensor | `tf.concat([a, b], axis=0)` |
| `tf.stack()` | 堆叠Tensor | `tf.stack([a, b])` |
| `tf.split()` | 分割Tensor | `tf.split(tensor, 3)` |

## 数学运算

### 基本运算

| 函数 | 作用 | 示例 |
|------|------|------|
| `tf.add()` | 加法 | `tf.add(a, b)` |
| `tf.subtract()` | 减法 | `tf.subtract(a, b)` |
| `tf.multiply()` | 乘法 | `tf.multiply(a, b)` |
| `tf.divide()` | 除法 | `tf.divide(a, b)` |
| `tf.pow()` | 幂运算 | `tf.pow(a, 2)` |
| `tf.sqrt()` | 平方根 | `tf.sqrt(tensor)` |
| `tf.abs()` | 绝对值 | `tf.abs(tensor)` |
| `tf.sign()` | 符号函数 | `tf.sign(tensor)` |
| `tf.round()` | 四舍五入 | `tf.round(tensor)` |
| `tf.floor()` | 向下取整 | `tf.floor(tensor)` |
| `tf.ceil()` | 向上取整 | `tf.ceil(tensor)` |

### 矩阵运算

| 函数 | 作用 | 示例 |
|------|------|------|
| `tf.matmul()` | 矩阵乘法 | `tf.matmul(a, b)` |
| `@` | 矩阵乘法运算符 | `a @ b` |
| `tf.linalg.inv()` | 矩阵求逆 | `tf.linalg.inv(A)` |
| `tf.linalg.pinv()` | 伪逆矩阵 | `tf.linalg.pinv(A)` |
| `tf.linalg.det()` | 行列式 | `tf.linalg.det(A)` |
| `tf.linalg.eigvals()` | 特征值 | `tf.linalg.eigvals(A)` |
| `tf.linalg.solve()` | 解线性方程组 | `tf.linalg.solve(A, b)` |
| `tf.linalg.norm()` | 范数 | `tf.linalg.norm(tensor)` |

### 统计函数

| 函数 | 作用 | 示例 |
|------|------|------|
| `tf.reduce_sum()` | 求和 | `tf.reduce_sum(tensor)` |
| `tf.reduce_mean()` | 平均值 | `tf.reduce_mean(tensor)` |
| `tf.reduce_max()` | 最大值 | `tf.reduce_max(tensor)` |
| `tf.reduce_min()` | 最小值 | `tf.reduce_min(tensor)` |
| `tf.reduce_prod()` | 乘积 | `tf.reduce_prod(tensor)` |
| `tf.reduce_std()` | 标准差 | `tf.reduce_std(tensor)` |
| `tf.reduce_variance()` | 方差 | `tf.reduce_variance(tensor)` |
| `tf.argmax()` | 最大值索引 | `tf.argmax(tensor, axis=0)` |
| `tf.argmin()` | 最小值索引 | `tf.argmin(tensor, axis=0)` |

### 按维度操作

| 函数 | 作用 | 示例 |
|------|------|------|
| `tf.reduce_sum(axis=0)` | 按维度求和 | `tf.reduce_sum(tensor, axis=0)` |
| `tf.reduce_mean(axis=1)` | 按维度求平均 | `tf.reduce_mean(tensor, axis=1)` |
| `tf.reduce_max(axis=0)` | 按维度求最大值 | `tf.reduce_max(tensor, axis=0)` |

## 自动微分（GradientTape）

### 梯度计算

| 函数/类 | 作用 | 示例 |
|---------|------|------|
| `tf.GradientTape()` | 梯度记录器 | `with tf.GradientTape() as tape: ...` |
| `tape.gradient()` | 计算梯度 | `tape.gradient(loss, variables)` |
| `tape.watch()` | 监视变量 | `tape.watch(tensor)` |
| `tf.stop_gradient()` | 停止梯度 | `tf.stop_gradient(tensor)` |

### 示例

```python
x = tf.Variable(2.0)
with tf.GradientTape() as tape:
    y = x ** 2
dy_dx = tape.gradient(y, x)
print(dy_dx)  # 4.0
```

## Keras API (tf.keras)

### 模型定义

| 类/函数 | 作用 | 示例 |
|---------|------|------|
| `keras.Sequential()` | 顺序模型 | `keras.Sequential([...])` |
| `keras.Model()` | 函数式API | `keras.Model(inputs, outputs)` |
| `keras.Input()` | 输入层 | `keras.Input(shape=(784,))` |

### 层（Layers）

| 层 | 作用 | 示例 |
|----|------|------|
| `layers.Dense()` | 全连接层 | `layers.Dense(64, activation='relu')` |
| `layers.Conv2D()` | 2D卷积层 | `layers.Conv2D(32, 3, activation='relu')` |
| `layers.Conv1D()` | 1D卷积层 | `layers.Conv1D(32, 3, activation='relu')` |
| `layers.LSTM()` | LSTM层 | `layers.LSTM(64)` |
| `layers.GRU()` | GRU层 | `layers.GRU(64)` |
| `layers.Embedding()` | 嵌入层 | `layers.Embedding(1000, 64)` |
| `layers.Dropout()` | Dropout层 | `layers.Dropout(0.5)` |
| `layers.BatchNormalization()` | 批归一化 | `layers.BatchNormalization()` |
| `layers.MaxPooling2D()` | 最大池化 | `layers.MaxPooling2D(2, 2)` |
| `layers.AveragePooling2D()` | 平均池化 | `layers.AveragePooling2D(2, 2)` |
| `layers.Flatten()` | 展平层 | `layers.Flatten()` |
| `layers.GlobalAveragePooling2D()` | 全局平均池化 | `layers.GlobalAveragePooling2D()` |

### 激活函数

| 函数 | 作用 | 示例 |
|------|------|------|
| `tf.nn.relu()` | ReLU激活 | `tf.nn.relu(x)` |
| `tf.nn.sigmoid()` | Sigmoid激活 | `tf.nn.sigmoid(x)` |
| `tf.nn.tanh()` | Tanh激活 | `tf.nn.tanh(x)` |
| `tf.nn.softmax()` | Softmax激活 | `tf.nn.softmax(x, axis=1)` |
| `tf.nn.leaky_relu()` | Leaky ReLU | `tf.nn.leaky_relu(x)` |

### 损失函数

| 函数 | 作用 | 示例 |
|------|------|------|
| `keras.losses.MeanSquaredError()` | 均方误差 | `keras.losses.MSE()` |
| `keras.losses.CategoricalCrossentropy()` | 分类交叉熵 | `keras.losses.CategoricalCrossentropy()` |
| `keras.losses.SparseCategoricalCrossentropy()` | 稀疏分类交叉熵 | `keras.losses.SparseCategoricalCrossentropy()` |
| `keras.losses.BinaryCrossentropy()` | 二分类交叉熵 | `keras.losses.BinaryCrossentropy()` |
| `keras.losses.MeanAbsoluteError()` | 平均绝对误差 | `keras.losses.MAE()` |

### 优化器

| 优化器 | 作用 | 示例 |
|--------|------|------|
| `keras.optimizers.SGD()` | 随机梯度下降 | `keras.optimizers.SGD(lr=0.01)` |
| `keras.optimizers.Adam()` | Adam优化器 | `keras.optimizers.Adam(lr=0.001)` |
| `keras.optimizers.RMSprop()` | RMSprop优化器 | `keras.optimizers.RMSprop(lr=0.001)` |
| `keras.optimizers.Adagrad()` | Adagrad优化器 | `keras.optimizers.Adagrad(lr=0.01)` |

### 模型方法

| 方法 | 作用 | 示例 |
|------|------|------|
| `.compile()` | 编译模型 | `model.compile(optimizer, loss, metrics)` |
| `.fit()` | 训练模型 | `model.fit(X, y, epochs=10)` |
| `.evaluate()` | 评估模型 | `model.evaluate(X, y)` |
| `.predict()` | 预测 | `model.predict(X)` |
| `.summary()` | 显示模型结构 | `model.summary()` |
| `.save()` | 保存模型 | `model.save('model.h5')` |
| `keras.models.load_model()` | 加载模型 | `keras.models.load_model('model.h5')` |

## 数据加载 (tf.data)

### Dataset操作

| 函数/类 | 作用 | 示例 |
|---------|------|------|
| `tf.data.Dataset.from_tensor_slices()` | 从Tensor创建 | `tf.data.Dataset.from_tensor_slices((X, y))` |
| `tf.data.Dataset.from_tensors()` | 从Tensor创建 | `tf.data.Dataset.from_tensors(data)` |
| `.batch()` | 批处理 | `dataset.batch(32)` |
| `.shuffle()` | 打乱 | `dataset.shuffle(1000)` |
| `.repeat()` | 重复 | `dataset.repeat(10)` |
| `.map()` | 映射函数 | `dataset.map(lambda x: x * 2)` |
| `.take()` | 取前N个 | `dataset.take(100)` |
| `.skip()` | 跳过N个 | `dataset.skip(100)` |
| `.prefetch()` | 预取 | `dataset.prefetch(1)` |

### 示例

```python
dataset = tf.data.Dataset.from_tensor_slices((X, y))
dataset = dataset.shuffle(1000).batch(32).prefetch(1)

for batch_x, batch_y in dataset:
    # 训练
    pass
```

## 设备操作

### GPU/CPU操作

| 函数 | 作用 | 示例 |
|------|------|------|
| `tf.config.list_physical_devices()` | 列出设备 | `tf.config.list_physical_devices('GPU')` |
| `tf.device()` | 指定设备 | `with tf.device('/GPU:0'): ...` |
| `tf.config.experimental.set_memory_growth()` | 内存增长 | `tf.config.experimental.set_memory_growth(gpu, True)` |

### 示例

```python
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    with tf.device('/GPU:0'):
        # GPU操作
        pass
```

## 模型保存和加载

| 函数 | 作用 | 示例 |
|------|------|------|
| `model.save()` | 保存模型 | `model.save('model')` |
| `keras.models.load_model()` | 加载模型 | `keras.models.load_model('model')` |
| `tf.saved_model.save()` | 保存SavedModel | `tf.saved_model.save(model, 'model')` |
| `tf.saved_model.load()` | 加载SavedModel | `tf.saved_model.load('model')` |
| `model.save_weights()` | 保存权重 | `model.save_weights('weights.h5')` |
| `model.load_weights()` | 加载权重 | `model.load_weights('weights.h5')` |

## 实用函数

### 随机数

| 函数 | 作用 | 示例 |
|------|------|------|
| `tf.random.set_seed()` | 设置随机种子 | `tf.random.set_seed(42)` |
| `tf.random.normal()` | 正态分布 | `tf.random.normal((3, 4))` |
| `tf.random.uniform()` | 均匀分布 | `tf.random.uniform((3, 4))` |
| `tf.random.shuffle()` | 打乱 | `tf.random.shuffle(tensor)` |

### 类型转换

| 函数/方法 | 作用 | 示例 |
|-----------|------|------|
| `tf.cast()` | 类型转换 | `tf.cast(tensor, tf.float32)` |
| `.numpy()` | 转为NumPy | `tensor.numpy()` |
| `tf.convert_to_tensor()` | 转为Tensor | `tf.convert_to_tensor(arr)` |

### 条件操作

| 函数 | 作用 | 示例 |
|------|------|------|
| `tf.where()` | 条件选择 | `tf.where(condition, x, y)` |
| `tf.cond()` | 条件执行 | `tf.cond(condition, true_fn, false_fn)` |
| `tf.case()` | 多条件选择 | `tf.case([...])` |

## 常用模式

### Sequential模型模式

```python
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(784,)),
    layers.Dense(32, activation='relu'),
    layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(X_train, y_train, epochs=10, validation_data=(X_val, y_val))
```

### 函数式API模式

```python
inputs = keras.Input(shape=(784,))
x = layers.Dense(64, activation='relu')(inputs)
x = layers.Dense(32, activation='relu')(x)
outputs = layers.Dense(10, activation='softmax')(x)

model = keras.Model(inputs=inputs, outputs=outputs)
```

### 自定义训练循环

```python
optimizer = keras.optimizers.Adam()
loss_fn = keras.losses.SparseCategoricalCrossentropy()

for epoch in range(num_epochs):
    for batch_x, batch_y in dataset:
        with tf.GradientTape() as tape:
            predictions = model(batch_x)
            loss = loss_fn(batch_y, predictions)
        
        gradients = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))
```

### 回调函数

```python
callbacks = [
    keras.callbacks.EarlyStopping(monitor='val_loss', patience=3),
    keras.callbacks.ModelCheckpoint('best_model.h5', save_best_only=True),
    keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5)
]

model.fit(X, y, callbacks=callbacks)
```

## 性能优化

### 使用GPU

```python
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    tf.config.experimental.set_memory_growth(gpus[0], True)
    with tf.device('/GPU:0'):
        # 模型操作
        pass
```

### 禁用即时执行（可选）

```python
# TensorFlow 2.x默认启用即时执行
# 如需禁用（不推荐）：
# tf.compat.v1.disable_eager_execution()
```

### 数据管道优化

```python
dataset = dataset.batch(32)
dataset = dataset.prefetch(1)  # 预取下一个批次
dataset = dataset.cache()      # 缓存数据
```

---

**注意**：本文档重点列出模型训练中最常用的函数。TensorFlow 2.x推荐使用Keras API。更多详细信息请参考TensorFlow官方文档。

