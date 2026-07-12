"""
PyTorch数据操作示例
学习目标：使用实际数据文件进行PyTorch操作
"""

import torch
import numpy as np
import os
import json


def get_data_path(filename):
    """获取数据文件路径"""
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, '..', 'datas')
    return os.path.join(data_dir, filename)


def demo_load_numpy_data():
    """加载NumPy数据到PyTorch"""
    print("=" * 60)
    print("加载NumPy数据到PyTorch")
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
    
    # 转换为PyTorch Tensor
    vectors_torch = torch.from_numpy(vectors_np)
    print(f"\nPyTorch Tensor形状: {vectors_torch.shape}")
    print(f"PyTorch数据类型: {vectors_torch.dtype}")
    print(f"设备: {vectors_torch.device}")
    
    # 注意：共享内存
    print("\n注意：from_numpy创建的Tensor与NumPy数组共享内存")
    vectors_np[0, 0] = 999.0
    print(f"修改NumPy后，Tensor也改变: {vectors_torch[0, 0].item()}")


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
    matrix = torch.from_numpy(matrix_np)
    
    print(f"矩阵形状: {matrix.shape}")
    
    # Tensor统计
    print(f"\nTensor统计:")
    print(f"  均值: {torch.mean(matrix).item():.4f}")
    print(f"  标准差: {torch.std(matrix).item():.4f}")
    print(f"  最小值: {torch.min(matrix).item():.4f}")
    print(f"  最大值: {torch.max(matrix).item():.4f}")
    
    # Tensor运算
    print(f"\nTensor运算:")
    print(f"  矩阵转置形状: {matrix.T.shape}")
    print(f"  按行求和形状: {torch.sum(matrix, dim=1).shape}")
    print(f"  按列求和形状: {torch.sum(matrix, dim=0).shape}")


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
    
    X = torch.from_numpy(X_np).float()
    y = torch.from_numpy(y_np).long()
    
    print(f"特征数据: {X.shape}, 类型: {X.dtype}")
    print(f"标签数据: {y.shape}, 类型: {y.dtype}")
    
    # 数据预处理
    # 归一化
    X_mean = torch.mean(X, dim=0)
    X_std = torch.std(X, dim=0)
    X_normalized = (X - X_mean) / (X_std + 1e-8)  # 避免除零
    
    print(f"\n归一化后:")
    print(f"  均值: {torch.mean(X_normalized):.6f}")
    print(f"  标准差: {torch.std(X_normalized):.6f}")
    
    # 创建DataLoader（简化示例）
    from torch.utils.data import TensorDataset, DataLoader
    
    dataset = TensorDataset(X_normalized, y)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    print(f"\nDataLoader:")
    print(f"  数据集大小: {len(dataset)}")
    print(f"  批次大小: 32")
    print(f"  批次数: {len(dataloader)}")
    
    # 查看一个批次
    for batch_X, batch_y in dataloader:
        print(f"\n第一个批次:")
        print(f"  特征形状: {batch_X.shape}")
        print(f"  标签形状: {batch_y.shape}")
        break


def demo_gpu_operations():
    """GPU操作示例"""
    print("\n" + "=" * 60)
    print("GPU操作示例")
    print("=" * 60)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"使用设备: {device}")
    
    # 加载数据
    vectors_path = get_data_path('vectors.npy')
    if not os.path.exists(vectors_path):
        print("数据文件不存在，请先运行: python tests/datas/generate_data.py")
        return
    
    vectors_np = np.load(vectors_path)
    vectors = torch.from_numpy(vectors_np).float()
    
    # 移动到GPU（如果可用）
    vectors_gpu = vectors.to(device)
    
    print(f"CPU Tensor形状: {vectors.shape}")
    print(f"GPU Tensor形状: {vectors_gpu.shape}")
    print(f"GPU Tensor设备: {vectors_gpu.device}")
    
    # GPU上的运算
    if torch.cuda.is_available():
        # 矩阵乘法（GPU加速）
        result = torch.matmul(vectors_gpu, vectors_gpu.T)
        print(f"\nGPU矩阵乘法结果形状: {result.shape}")
        print(f"结果设备: {result.device}")


def demo_embedding_similarity():
    """Embedding相似度计算（PyTorch版本）"""
    print("\n" + "=" * 60)
    print("Embedding相似度计算（PyTorch版本）")
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
    
    # 转换为PyTorch Tensor
    doc_embeddings = torch.from_numpy(doc_embeddings_np).float()
    query_vectors = torch.from_numpy(query_vectors_np).float()
    
    # 归一化
    doc_norms = torch.norm(doc_embeddings, dim=1, keepdim=True)
    doc_embeddings_norm = doc_embeddings / doc_norms
    
    # 对每个查询进行搜索
    for i, query_text in enumerate(query_texts[:2]):  # 只显示前2个查询
        print(f"\n查询 {i+1}: {query_text}")
        print("-" * 60)
        
        query_vec = query_vectors[i]
        query_norm = query_vec / torch.norm(query_vec)
        
        # 计算相似度（批量计算）
        similarities = torch.matmul(doc_embeddings_norm, query_norm)
        
        # 找到top-3
        top_k = 3
        top_values, top_indices = torch.topk(similarities, k=top_k)
        
        print(f"Top-{top_k}最相似的文档:")
        for rank, (value, idx) in enumerate(zip(top_values, top_indices), 1):
            print(f"  {rank}. [{value.item():.4f}] {documents[idx.item()]}")


def demo_gradient_computation():
    """梯度计算示例（使用实际数据）"""
    print("\n" + "=" * 60)
    print("梯度计算示例")
    print("=" * 60)
    
    # 加载训练数据
    X_path = get_data_path('train_X.npy')
    y_path = get_data_path('train_y.npy')
    
    if not os.path.exists(X_path) or not os.path.exists(y_path):
        print("数据文件不存在，请先运行: python tests/datas/generate_data.py")
        return
    
    X_np = np.load(X_path)
    y_np = np.load(y_path)
    
    # 转换为Tensor并设置requires_grad
    X = torch.from_numpy(X_np[:10]).float()  # 只用前10个样本
    y = torch.from_numpy(y_np[:10]).long()
    
    # 创建简单的线性模型
    model = torch.nn.Linear(X.shape[1], 3)  # 20特征 -> 3类
    
    # 前向传播
    output = model(X)
    loss_fn = torch.nn.CrossEntropyLoss()
    loss = loss_fn(output, y)
    
    print(f"输入形状: {X.shape}")
    print(f"输出形状: {output.shape}")
    print(f"损失值: {loss.item():.4f}")
    
    # 反向传播
    loss.backward()
    
    # 查看梯度
    print(f"\n模型参数梯度:")
    print(f"  权重梯度形状: {model.weight.grad.shape}")
    print(f"  偏置梯度形状: {model.bias.grad.shape}")
    print(f"  权重梯度均值: {torch.mean(torch.abs(model.weight.grad)).item():.6f}")


if __name__ == "__main__":
    print("PyTorch数据操作示例\n")
    print("本示例演示如何使用实际数据文件进行PyTorch操作\n")
    
    demo_load_numpy_data()
    demo_tensor_operations()
    demo_training_data_loading()
    demo_gpu_operations()
    demo_embedding_similarity()
    demo_gradient_computation()
    
    print("\n" + "=" * 60)
    print("总结")
    print("=" * 60)
    print("""
本示例展示了：
1. NumPy和PyTorch数据互转
2. Tensor操作和统计
3. 训练数据加载和预处理
4. GPU加速操作
5. Embedding相似度计算（PyTorch版本）
6. 梯度计算（自动微分）

这些都是模型训练中的常见操作！
    """)

