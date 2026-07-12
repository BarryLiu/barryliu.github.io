# 测试数据说明

本目录包含各种格式的测试数据，用于学习和演示。

## 数据文件

### 向量和矩阵数据
- `vectors.npy` - 100个128维随机向量
- `matrix_small.npy` - 5x5小矩阵
- `matrix_medium.npy` - 100x50中等矩阵
- `matrix_large.npy` - 1000x500大矩阵

### Embedding数据
- `document_embeddings.npy` - 10个文档的Embedding（128维）
- `documents.json` - 文档文本和元数据
- `query_vectors.npy` - 5个查询向量（128维）
- `queries.json` - 查询文本和元数据

### 训练数据
- `train_X.npy` - 训练特征（1000样本，20特征）
- `train_y.npy` - 训练标签（1000样本，3类）
- `train_data_sample.csv` - CSV格式示例（前100个样本）

### 其他数据
- `time_series.npy` - 时间序列数据（1000个时间点）
- `images.npy` - 模拟图像数据（100张28x28灰度图）
- `image_labels.npy` - 图像标签

## 生成数据

运行以下命令生成所有测试数据：

```bash
python tests/datas/generate_data.py
```

## 使用示例

### NumPy
```python
import numpy as np
import os

data_dir = 'tests/datas'
vectors = np.load(os.path.join(data_dir, 'vectors.npy'))
print(f"向量形状: {vectors.shape}")
```

### PyTorch
```python
import torch
import numpy as np

vectors_np = np.load('tests/datas/vectors.npy')
vectors_torch = torch.from_numpy(vectors_np)
```

### TensorFlow
```python
import tensorflow as tf
import numpy as np

vectors_np = np.load('tests/datas/vectors.npy')
vectors_tf = tf.constant(vectors_np)
```

## 数据说明

所有数据使用固定随机种子（42）生成，确保可重现性。

