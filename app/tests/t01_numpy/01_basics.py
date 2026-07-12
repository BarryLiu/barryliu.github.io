"""
NumPy基础操作示例
学习目标：掌握NumPy的基本操作
"""

import numpy as np


def array_creation():
    """数组创建"""
    print("=" * 60)
    print("数组创建")
    print("=" * 60)
    
    # 从列表创建
    arr1 = np.array([1, 2, 3, 4, 5])
    print(f"从列表创建: {arr1}")
    
    # 创建全零数组
    zeros = np.zeros(5)
    print(f"全零数组: {zeros}")
    
    # 创建全1数组
    ones = np.ones(5)
    print(f"全1数组: {ones}")
    
    # 创建指定范围的数组
    arange = np.arange(0, 10, 2)
    print(f"arange(0, 10, 2): {arange}")
    
    # 创建线性空间
    linspace = np.linspace(0, 1, 5)
    print(f"linspace(0, 1, 5): {linspace}")
    
    # 创建随机数组
    random_arr = np.random.rand(5)
    print(f"随机数组: {random_arr}")
    
    # 创建矩阵
    matrix = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"矩阵:\n{matrix}")


def array_properties():
    """数组属性"""
    print("\n" + "=" * 60)
    print("数组属性")
    print("=" * 60)
    
    arr = np.array([[1, 2, 3], [4, 5, 6]])
    
    print(f"数组: \n{arr}")
    print(f"形状 (shape): {arr.shape}")
    print(f"维度 (ndim): {arr.ndim}")
    print(f"大小 (size): {arr.size}")
    print(f"数据类型 (dtype): {arr.dtype}")
    print(f"元素大小 (itemsize): {arr.itemsize} bytes")


def array_indexing():
    """数组索引和切片"""
    print("\n" + "=" * 60)
    print("数组索引和切片")
    print("=" * 60)
    
    arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    print(f"原数组: {arr}")
    
    # 基本索引
    print(f"arr[0]: {arr[0]}")
    print(f"arr[-1]: {arr[-1]}")
    
    # 切片
    print(f"arr[2:5]: {arr[2:5]}")
    print(f"arr[:5]: {arr[:5]}")
    print(f"arr[5:]: {arr[5:]}")
    print(f"arr[::2]: {arr[::2]}")  # 步长为2
    
    # 多维数组索引
    matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(f"\n矩阵:\n{matrix}")
    print(f"matrix[0, 1]: {matrix[0, 1]}")
    print(f"matrix[1, :]: {matrix[1, :]}")
    print(f"matrix[:, 1]: {matrix[:, 1]}")


def array_operations():
    """数组运算"""
    print("\n" + "=" * 60)
    print("数组运算")
    print("=" * 60)
    
    a = np.array([1, 2, 3, 4])
    b = np.array([5, 6, 7, 8])
    
    print(f"数组a: {a}")
    print(f"数组b: {b}")
    
    # 基本运算
    print(f"\na + b: {a + b}")
    print(f"a - b: {a - b}")
    print(f"a * b: {a * b}")
    print(f"a / b: {a / b}")
    print(f"a ** 2: {a ** 2}")
    
    # 矩阵运算
    matrix_a = np.array([[1, 2], [3, 4]])
    matrix_b = np.array([[5, 6], [7, 8]])
    
    print(f"\n矩阵A:\n{matrix_a}")
    print(f"矩阵B:\n{matrix_b}")
    print(f"矩阵乘法 (A @ B):\n{matrix_a @ matrix_b}")
    print(f"点积 (np.dot):\n{np.dot(matrix_a, matrix_b)}")


def array_reshaping():
    """数组重塑"""
    print("\n" + "=" * 60)
    print("数组重塑")
    print("=" * 60)
    
    arr = np.arange(12)
    print(f"原数组: {arr}")
    
    # reshape
    reshaped = arr.reshape(3, 4)
    print(f"重塑为3x4:\n{reshaped}")
    
    # flatten
    flattened = reshaped.flatten()
    print(f"展平: {flattened}")
    
    # transpose
    transposed = reshaped.T
    print(f"转置:\n{transposed}")


if __name__ == "__main__":
    print("NumPy基础操作示例\n")
    array_creation()
    array_properties()
    array_indexing()
    array_operations()
    array_reshaping()

