"""
TensorFlow数据操作示例
学习目标：使用实际数据文件进行TensorFlow操作
"""

import tensorflow as tf
import numpy as np
import os
import json


def get_data_path(filename):
    """获取数据文件路径"""
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, '..', 'datas')
    return os.path.join(data_dir, filename)


def demo_load_numpy_data():
    """加载NumPy数据到TensorFlow"""
    print("=" * 60)
    print("加载NumPy数据到TensorFlow")
    print("=" * 60)
    
    # 加载向量数据
    vectors_path = get_data_path('vectors.npy')
    if not os.path.exists(vectors_path):
        print(f"数据文件不存在: {vectors_path}")
        print("请先运行: python tests/datas/generate_data.py")
        return
    
    # NumPy加载
    vectors_np = np.load(vectors_path)
    print(f"NumPy数组形状: {vectors_np.shape}")
    print(f"NumPy数据类型: {vectors_np.dtype}")
    
    # 转换为TensorFlow Tensor
    vectors_tf = tf.constant(vectors_np)
    print(f"\nTensorFlow Tensor形状: {vectors_tf.shape}")
    print(f"TensorFlow数据类型: {vectors_tf.dtype}")
    print(f"设备: {vectors_tf.device}")
    
    # 转换为numpy（查看值）
    print(f"\nTensor值（前5个元素）: {vectors_tf.numpy()[:5, :5]}")


def demo_tensor_operations():
    """Tensor操作示例"""
    print("\n" + "=" * 60)
    print("Tensor操作示例")
    print("=" * 60)
    
    # 加载矩阵数据
    matrix_path = get_data_path('matrix_medium.npy')
    if not os.path.exists(matrix_path):
        print("数据文件不存在，请先运行: python tests/datas/generate_data.py")
        return
    
    matrix_np = np.load(matrix_path)
    matrix = tf.constant(matrix_np)
    
    print(f"矩阵形状: {matrix.shape}")
    
    # Tensor统计
    print(f"\nTensor统计:")
    print(f"  均值: {tf.reduce_mean(matrix).numpy():.4f}")
    print(f"  标准差: {tf.math.reduce_std(matrix).numpy():.4f}")
    print(f"  最小值: {tf.reduce_min(matrix).numpy():.4f}")
    print(f"  最大值: {tf.reduce_max(matrix).numpy():.4f}")
    
    # Tensor运算
    print(f"\nTensor运算:")
    print(f"  矩阵转置形状: {tf.transpose(matrix).shape}")
    print(f"  按行求和形状: {tf.reduce_sum(matrix, axis=1).shape}")
    print(f"  按列求和形状: {tf.reduce_sum(matrix, axis=0).shape}")


def demo_training_data_loading():
    """训练数据加载示例"""
    print("\n" + "=" * 60)
    print("训练数据加载示例")
    print("=" * 60)
    
    X_path = get_data_path('train_X.npy')
    y_path = get_data_path('train_y.npy')
    
    if not os.path.exists(X_path) or not os.path.exists(y_path):
        print("数据文件不存在，请先运行: python tests/datas/generate_data.py")
        return
    
    # 加载数据
    X_np = np.load(X_path)
    y_np = np.load(y_path)
    
    X = tf.constant(X_np, dtype=tf.float32)
    y = tf.constant(y_np, dtype=tf.int32)
    
    print(f"特征数据: {X.shape}, 类型: {X.dtype}")
    print(f"标签数据: {y.shape}, 类型: {y.dtype}")
    
    # 数据预处理
    # 归一化
    X_mean = tf.reduce_mean(X, axis=0)
    X_std = tf.math.reduce_std(X, axis=0)
    X_normalized = (X - X_mean) / (X_std + 1e-8)  # 避免除零
    
    print(f"\n归一化后:")
    print(f"  均值: {tf.reduce_mean(X_normalized).numpy():.6f}")
    print(f"  标准差: {tf.math.reduce_std(X_normalized).numpy():.6f}")
    
    # 创建Dataset
    dataset = tf.data.Dataset.from_tensor_slices((X_normalized, y))
    dataset = dataset.batch(32).shuffle(1000)
    
    print(f"\nDataset:")
    print(f"  批次大小: 32")
    
    # 查看一个批次
    for batch_X, batch_y in dataset.take(1):
        print(f"\n第一个批次:")
        print(f"  特征形状: {batch_X.shape}")
        print(f"  标签形状: {batch_y.shape}")
        break


def demo_gpu_operations():
    """GPU操作示例"""
    print("\n" + "=" * 60)
    print("GPU操作示例")
    print("=" * 60)
    
    gpus = tf.config.list_physical_devices('GPU')
    print(f"可用GPU数量: {len(gpus)}")
    
    if gpus:
        print(f"GPU设备: {gpus}")
        # 设置内存增长
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print("已启用GPU内存增长")
        except RuntimeError as e:
            print(e)
    
    # 加载数据
    vectors_path = get_data_path('vectors.npy')
    if not os.path.exists(vectors_path):
        print("数据文件不存在，请先运行: python tests/datas/generate_data.py")
        return
    
    vectors_np = np.load(vectors_path)
    
    # 移动到GPU（如果可用）
    with tf.device('/GPU:0' if gpus else '/CPU:0'):
        vectors = tf.constant(vectors_np, dtype=tf.float32)
        print(f"\nTensor形状: {vectors.shape}")
        print(f"Tensor设备: {vectors.device}")
        
        # 矩阵乘法（GPU加速）
        result = tf.matmul(vectors, tf.transpose(vectors))
        print(f"矩阵乘法结果形状: {result.shape}")
        print(f"结果设备: {result.device}")


def demo_embedding_similarity():
    """Embedding相似度计算（TensorFlow版本）"""
    print("\n" + "=" * 60)
    print("Embedding相似度计算（TensorFlow版本）")
    print("=" * 60)
    
    # 加载文档Embedding
    embeddings_path = get_data_path('document_embeddings.npy')
    queries_path = get_data_path('query_vectors.npy')
    docs_path = get_data_path('documents.json')
    queries_json_path = get_data_path('queries.json')
    
    if not all(os.path.exists(p) for p in [embeddings_path, queries_path, docs_path, queries_json_path]):
        print("数据文件不存在，请先运行: python tests/datas/generate_data.py")
        return
    
    # 加载数据
    doc_embeddings_np = np.load(embeddings_path)
    query_vectors_np = np.load(queries_path)
    
    with open(docs_path, 'r', encoding='utf-8') as f:
        docs_data = json.load(f)
    documents = docs_data['documents']
    
    with open(queries_json_path, 'r', encoding='utf-8') as f:
        queries_data = json.load(f)
    query_texts = queries_data['queries']
    
    # 转换为TensorFlow Tensor
    doc_embeddings = tf.constant(doc_embeddings_np, dtype=tf.float32)
    query_vectors = tf.constant(query_vectors_np, dtype=tf.float32)
    
    # 归一化
    doc_norms = tf.norm(doc_embeddings, axis=1, keepdims=True)
    doc_embeddings_norm = doc_embeddings / doc_norms
    
    # 对每个查询进行搜索
    for i, query_text in enumerate(query_texts[:2]):  # 只显示前2个查询
        print(f"\n查询 {i+1}: {query_text}")
        print("-" * 60)
        
        query_vec = query_vectors[i]
        query_norm = query_vec / tf.norm(query_vec)
        
        # 计算相似度（批量计算）
        similarities = tf.matmul(doc_embeddings_norm, tf.expand_dims(query_norm, 1))
        similarities = tf.squeeze(similarities)
        
        # 找到top-3
        top_k = 3
        top_values, top_indices = tf.nn.top_k(similarities, k=top_k)
        
        print(f"Top-{top_k}最相似的文档:")
        for rank, (value, idx) in enumerate(zip(top_values.numpy(), top_indices.numpy()), 1):
            print(f"  {rank}. [{value:.4f}] {documents[idx]}")


def demo_gradient_computation():
    """梯度计算示例（使用实际数据）"""
    print("\n" + "=" * 60)
    print("梯度计算示例（GradientTape）")
    print("=" * 60)
    
    # 加载训练数据
    X_path = get_data_path('train_X.npy')
    y_path = get_data_path('train_y.npy')
    
    if not os.path.exists(X_path) or not os.path.exists(y_path):
        print("数据文件不存在，请先运行: python tests/datas/generate_data.py")
        return
    
    X_np = np.load(X_path)
    y_np = np.load(y_path)
    
    # 转换为Tensor并只用前10个样本
    X = tf.constant(X_np[:10], dtype=tf.float32)
    y = tf.constant(y_np[:10], dtype=tf.int32)
    
    # 创建变量（模型参数）
    W = tf.Variable(tf.random.normal([X.shape[1], 3]))  # 20特征 -> 3类
    b = tf.Variable(tf.zeros([3]))
    
    # 使用GradientTape记录操作
    with tf.GradientTape() as tape:
        # 前向传播
        logits = tf.matmul(X, W) + b
        loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        loss = loss_fn(y, logits)
    
    print(f"输入形状: {X.shape}")
    print(f"输出形状: {logits.shape}")
    print(f"损失值: {loss.numpy():.4f}")
    
    # 计算梯度
    gradients = tape.gradient(loss, [W, b])
    
    # 查看梯度
    print(f"\n模型参数梯度:")
    print(f"  权重梯度形状: {gradients[0].shape}")
    print(f"  偏置梯度形状: {gradients[1].shape}")
    print(f"  权重梯度均值: {tf.reduce_mean(tf.abs(gradients[0])).numpy():.6f}")


def demo_keras_model_with_data():
    """使用Keras模型处理数据"""
    print("\n" + "=" * 60)
    print("Keras模型处理数据示例")
    print("=" * 60)
    
    from tensorflow import keras
    from tensorflow.keras import layers
    
    # 加载训练数据
    X_path = get_data_path('train_X.npy')
    y_path = get_data_path('train_y.npy')
    
    if not os.path.exists(X_path) or not os.path.exists(y_path):
        print("数据文件不存在，请先运行: python tests/datas/generate_data.py")
        return
    
    X_np = np.load(X_path)
    y_np = np.load(y_path)
    
    # 划分训练集和验证集
    split = int(0.8 * len(X_np))
    X_train, X_val = X_np[:split], X_np[split:]
    y_train, y_val = y_np[:split], y_np[split:]
    
    # 归一化
    X_mean = np.mean(X_train, axis=0)
    X_std = np.std(X_train, axis=0)
    X_train = (X_train - X_mean) / (X_std + 1e-8)
    X_val = (X_val - X_mean) / (X_std + 1e-8)
    
    # 创建简单模型
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        layers.Dense(32, activation='relu'),
        layers.Dense(3, activation='softmax')
    ])
    
    # 编译模型
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print(f"模型结构:")
    model.summary()
    
    # 训练（只训练几个epoch作为演示）
    print(f"\n训练数据: {X_train.shape[0]} 样本")
    print(f"验证数据: {X_val.shape[0]} 样本")
    print("\n开始训练（3个epoch）...")
    
    history = model.fit(
        X_train, y_train,
        batch_size=32,
        epochs=3,
        validation_data=(X_val, y_val),
        verbose=1
    )
    
    print(f"\n最终训练准确率: {history.history['accuracy'][-1]:.4f}")
    print(f"最终验证准确率: {history.history['val_accuracy'][-1]:.4f}")


if __name__ == "__main__":
    print("TensorFlow数据操作示例\n")
    print("本示例演示如何使用实际数据文件进行TensorFlow操作\n")
    
    demo_load_numpy_data()
    demo_tensor_operations()
    demo_training_data_loading()
    demo_gpu_operations()
    demo_embedding_similarity()
    demo_gradient_computation()
    demo_keras_model_with_data()
    
    print("\n" + "=" * 60)
    print("总结")
    print("=" * 60)
    print("""
本示例展示了：
1. NumPy和TensorFlow数据互转
2. Tensor操作和统计
3. 训练数据加载和预处理
4. GPU加速操作
5. Embedding相似度计算（TensorFlow版本）
6. 梯度计算（GradientTape）
7. Keras模型训练

这些都是模型训练中的常见操作！
    """)

