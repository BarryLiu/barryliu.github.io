"""
PyTorch基础操作示例
学习目标：掌握PyTorch的基本操作

注意：PyTorch主要用于模型训练，应用开发通常不需要
"""

import torch
import numpy as np


def tensor_creation():
    """Tensor创建"""
    print("=" * 60)
    print("Tensor创建")
    print("=" * 60)
    
    # 从列表创建
    t1 = torch.tensor([1, 2, 3, 4, 5])
    print(f"从列表创建: {t1}")
    
    # 从NumPy创建
    np_arr = np.array([1, 2, 3, 4, 5])
    t2 = torch.from_numpy(np_arr)
    print(f"从NumPy创建: {t2}")
    
    # 创建全零Tensor
    zeros = torch.zeros(5)
    print(f"全零Tensor: {zeros}")
    
    # 创建全1Tensor
    ones = torch.ones(5)
    print(f"全1Tensor: {ones}")
    
    # 创建随机Tensor
    random_t = torch.rand(5)
    print(f"随机Tensor: {random_t}")
    
    # 指定形状
    matrix = torch.randn(3, 4)
    print(f"随机矩阵 (3x4):\n{matrix}")


def tensor_properties():
    """Tensor属性"""
    print("\n" + "=" * 60)
    print("Tensor属性")
    print("=" * 60)
    
    t = torch.tensor([[1, 2, 3], [4, 5, 6]])
    
    print(f"Tensor:\n{t}")
    print(f"形状 (shape): {t.shape}")
    print(f"维度 (dim): {t.dim()}")
    print(f"大小 (size): {t.size()}")
    print(f"数据类型 (dtype): {t.dtype}")
    print(f"设备 (device): {t.device}")
    print(f"是否需要梯度 (requires_grad): {t.requires_grad}")


def tensor_operations():
    """Tensor运算"""
    print("\n" + "=" * 60)
    print("Tensor运算")
    print("=" * 60)
    
    a = torch.tensor([1, 2, 3, 4])
    b = torch.tensor([5, 6, 7, 8])
    
    print(f"Tensor a: {a}")
    print(f"Tensor b: {b}")
    
    # 基本运算
    print(f"\na + b: {a + b}")
    print(f"a - b: {a - b}")
    print(f"a * b: {a * b}")
    print(f"a / b: {a / b}")
    print(f"a ** 2: {a ** 2}")
    
    # 矩阵乘法
    matrix_a = torch.tensor([[1, 2], [3, 4]])
    matrix_b = torch.tensor([[5, 6], [7, 8]])
    
    print(f"\n矩阵A:\n{matrix_a}")
    print(f"矩阵B:\n{matrix_b}")
    print(f"矩阵乘法 (A @ B):\n{matrix_a @ matrix_b}")
    print(f"矩阵乘法 (torch.mm):\n{torch.mm(matrix_a, matrix_b)}")


def gradient_computation():
    """梯度计算（PyTorch核心特性）"""
    print("\n" + "=" * 60)
    print("梯度计算（自动微分）")
    print("=" * 60)
    
    # 创建需要梯度的Tensor
    x = torch.tensor(2.0, requires_grad=True)
    y = torch.tensor(3.0, requires_grad=True)
    
    # 定义函数 z = x^2 + y^2
    z = x ** 2 + y ** 2
    
    print(f"x = {x.item()}, y = {y.item()}")
    print(f"z = x^2 + y^2 = {z.item()}")
    
    # 反向传播
    z.backward()
    
    # 查看梯度
    print(f"\n∂z/∂x = {x.grad.item()}")
    print(f"∂z/∂y = {y.grad.item()}")
    print(f"验证: ∂z/∂x = 2x = {2 * x.item()}, ∂z/∂y = 2y = {2 * y.item()}")


def gpu_operations():
    """GPU操作"""
    print("\n" + "=" * 60)
    print("GPU操作")
    print("=" * 60)
    
    # 检查GPU是否可用
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"使用设备: {device}")
    
    if torch.cuda.is_available():
        print(f"GPU名称: {torch.cuda.get_device_name(0)}")
        print(f"GPU数量: {torch.cuda.device_count()}")
        
        # 创建GPU Tensor
        t_gpu = torch.randn(3, 3).to(device)
        print(f"\nGPU Tensor:\n{t_gpu}")
    else:
        print("未检测到GPU，使用CPU")
        t_cpu = torch.randn(3, 3)
        print(f"\nCPU Tensor:\n{t_cpu}")


def numpy_interop():
    """NumPy互操作"""
    print("\n" + "=" * 60)
    print("NumPy互操作")
    print("=" * 60)
    
    # NumPy -> PyTorch
    np_arr = np.array([1, 2, 3, 4, 5])
    torch_tensor = torch.from_numpy(np_arr)
    print(f"NumPy数组: {np_arr}")
    print(f"PyTorch Tensor: {torch_tensor}")
    
    # PyTorch -> NumPy
    torch_tensor2 = torch.tensor([6, 7, 8, 9, 10])
    np_arr2 = torch_tensor2.numpy()
    print(f"\nPyTorch Tensor: {torch_tensor2}")
    print(f"NumPy数组: {np_arr2}")
    
    # 注意：共享内存
    print("\n注意：from_numpy创建的Tensor与NumPy数组共享内存")
    np_arr[0] = 999
    print(f"修改NumPy后: {torch_tensor}")


if __name__ == "__main__":
    print("PyTorch基础操作示例\n")
    print("注意：PyTorch主要用于模型训练，应用开发通常不需要\n")
    
    tensor_creation()
    tensor_properties()
    tensor_operations()
    gradient_computation()
    gpu_operations()
    numpy_interop()

