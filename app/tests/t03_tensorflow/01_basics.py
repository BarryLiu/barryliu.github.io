"""
TensorFlow基础操作示例
学习目标：掌握TensorFlow的基本操作

注意：TensorFlow主要用于模型训练，应用开发通常不需要
"""

import tensorflow as tf
import numpy as np


def tensor_creation():
    """Tensor创建"""
    print("=" * 60)
    print("Tensor创建")
    print("=" * 60)
    
    # 从列表创建
    t1 = tf.constant([1, 2, 3, 4, 5])
    print(f"从列表创建: {t1}")
    print(f"值: {t1.numpy()}")
    
    # 从NumPy创建
    np_arr = np.array([1, 2, 3, 4, 5])
    t2 = tf.constant(np_arr)
    print(f"\n从NumPy创建: {t2}")
    
    # 创建全零Tensor
    zeros = tf.zeros(5)
    print(f"\n全零Tensor: {zeros}")
    
    # 创建全1Tensor
    ones = tf.ones(5)
    print(f"全1Tensor: {ones}")
    
    # 创建随机Tensor
    random_t = tf.random.normal([5])
    print(f"随机Tensor: {random_t}")
    
    # 指定形状
    matrix = tf.random.normal([3, 4])
    print(f"\n随机矩阵 (3x4):\n{matrix}")


def tensor_properties():
    """Tensor属性"""
    print("\n" + "=" * 60)
    print("Tensor属性")
    print("=" * 60)
    
    t = tf.constant([[1, 2, 3], [4, 5, 6]])
    
    print(f"Tensor:\n{t}")
    print(f"形状 (shape): {t.shape}")
    print(f"维度 (ndim): {t.ndim}")
    print(f"大小 (size): {tf.size(t).numpy()}")
    print(f"数据类型 (dtype): {t.dtype}")
    print(f"设备: {t.device}")


def tensor_operations():
    """Tensor运算"""
    print("\n" + "=" * 60)
    print("Tensor运算")
    print("=" * 60)
    
    a = tf.constant([1, 2, 3, 4])
    b = tf.constant([5, 6, 7, 8])
    
    print(f"Tensor a: {a}")
    print(f"Tensor b: {b}")
    
    # 基本运算
    print(f"\na + b: {a + b}")
    print(f"a - b: {a - b}")
    print(f"a * b: {a * b}")
    print(f"a / b: {a / b}")
    print(f"a ** 2: {a ** 2}")
    
    # 矩阵乘法
    matrix_a = tf.constant([[1, 2], [3, 4]])
    matrix_b = tf.constant([[5, 6], [7, 8]])
    
    print(f"\n矩阵A:\n{matrix_a}")
    print(f"矩阵B:\n{matrix_b}")
    print(f"矩阵乘法 (A @ B):\n{tf.matmul(matrix_a, matrix_b)}")


def gradient_computation():
    """梯度计算（自动微分）"""
    print("\n" + "=" * 60)
    print("梯度计算（自动微分）")
    print("=" * 60)
    
    # 创建变量
    x = tf.Variable(2.0)
    y = tf.Variable(3.0)
    
    # 使用GradientTape记录操作
    with tf.GradientTape() as tape:
        z = x ** 2 + y ** 2
    
    # 计算梯度
    dz_dx, dz_dy = tape.gradient(z, [x, y])
    
    print(f"x = {x.numpy()}, y = {y.numpy()}")
    print(f"z = x^2 + y^2 = {z.numpy()}")
    print(f"\n∂z/∂x = {dz_dx.numpy()}")
    print(f"∂z/∂y = {dz_dy.numpy()}")
    print(f"验证: ∂z/∂x = 2x = {2 * x.numpy()}, ∂z/∂y = 2y = {2 * y.numpy()}")


def gpu_operations():
    """GPU操作"""
    print("\n" + "=" * 60)
    print("GPU操作")
    print("=" * 60)
    
    # 检查GPU是否可用
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
        
        # 创建GPU Tensor
        with tf.device('/GPU:0'):
            t_gpu = tf.random.normal([1000, 1000])
            print(f"\nGPU Tensor形状: {t_gpu.shape}")
    else:
        print("未检测到GPU，使用CPU")
        t_cpu = tf.random.normal([1000, 1000])
        print(f"CPU Tensor形状: {t_cpu.shape}")


def numpy_interop():
    """NumPy互操作"""
    print("\n" + "=" * 60)
    print("NumPy互操作")
    print("=" * 60)
    
    # NumPy -> TensorFlow
    np_arr = np.array([1, 2, 3, 4, 5])
    tf_tensor = tf.constant(np_arr)
    print(f"NumPy数组: {np_arr}")
    print(f"TensorFlow Tensor: {tf_tensor}")
    
    # TensorFlow -> NumPy
    tf_tensor2 = tf.constant([6, 7, 8, 9, 10])
    np_arr2 = tf_tensor2.numpy()
    print(f"\nTensorFlow Tensor: {tf_tensor2}")
    print(f"NumPy数组: {np_arr2}")


def eager_execution():
    """即时执行模式"""
    print("\n" + "=" * 60)
    print("即时执行模式（Eager Execution）")
    print("=" * 60)
    
    # TensorFlow 2.x默认启用即时执行
    print("TensorFlow 2.x默认使用即时执行模式")
    
    # 可以直接执行操作
    a = tf.constant(2.0)
    b = tf.constant(3.0)
    c = a + b
    
    print(f"a = {a.numpy()}")
    print(f"b = {b.numpy()}")
    print(f"c = a + b = {c.numpy()}")
    
    print("\n即时执行的优势：")
    print("- 代码更直观，类似NumPy")
    print("- 易于调试")
    print("- 支持Python控制流")


if __name__ == "__main__":
    print("TensorFlow基础操作示例\n")
    print("注意：TensorFlow主要用于模型训练，应用开发通常不需要\n")
    
    tensor_creation()
    tensor_properties()
    tensor_operations()
    gradient_computation()
    gpu_operations()
    numpy_interop()
    eager_execution()

