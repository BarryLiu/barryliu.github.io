"""
TensorFlow Keras模型示例
学习目标：掌握使用Keras构建和训练模型
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np


def sequential_model():
    """Sequential模型（顺序模型）"""
    print("=" * 60)
    print("Sequential模型")
    print("=" * 60)
    
    # 创建Sequential模型`
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=(784,)),
        layers.Dense(32, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    
    print("模型结构:")
    model.summary()
    
    # 编译模型
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("\n模型已编译")


def functional_api():
    """函数式API"""
    print("\n" + "=" * 60)
    print("函数式API（更灵活）")
    print("=" * 60)
    
    # 定义输入
    inputs = keras.Input(shape=(784,))
    
    # 定义层
    x = layers.Dense(64, activation='relu')(inputs)
    x = layers.Dense(32, activation='relu')(x)
    outputs = layers.Dense(10, activation='softmax')(x)
    
    # 创建模型
    model = keras.Model(inputs=inputs, outputs=outputs)
    
    print("模型结构:")
    model.summary()


def cnn_model():
    """CNN模型"""
    print("\n" + "=" * 60)
    print("CNN模型")
    print("=" * 60)
    
    model = keras.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    
    print("CNN模型结构:")
    model.summary()


def training_example():
    """训练示例"""
    print("\n" + "=" * 60)
    print("训练示例（简化版）")
    print("=" * 60)
    
    # 创建简单模型
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=(20,)),
        layers.Dense(32, activation='relu'),
        layers.Dense(3, activation='softmax')
    ])
    
    # 编译
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # 生成虚拟数据
    x_train = np.random.randn(800, 20)
    y_train = np.random.randint(0, 3, (800,))
    x_val = np.random.randn(200, 20)
    y_val = np.random.randint(0, 3, (200,))
    
    print(f"训练样本: {x_train.shape[0]}")
    print(f"验证样本: {x_val.shape[0]}")
    
    # 训练
    history = model.fit(
        x_train, y_train,
        batch_size=32,
        epochs=5,
        validation_data=(x_val, y_val),
        verbose=1
    )
    
    print("\n训练完成")
    print(f"最终训练准确率: {history.history['accuracy'][-1]:.4f}")
    print(f"最终验证准确率: {history.history['val_accuracy'][-1]:.4f}")


def model_save_load():
    """模型保存和加载"""
    print("\n" + "=" * 60)
    print("模型保存和加载")
    print("=" * 60)
    
    # 创建模型
    model = keras.Sequential([
        layers.Dense(10, activation='relu', input_shape=(5,)),
        layers.Dense(1)
    ])
    
    # 保存模型
    model.save('tf_model')
    print("模型已保存到 tf_model/")
    
    # 加载模型
    loaded_model = keras.models.load_model('tf_model')
    print("模型已加载")
    
    # 测试
    x_test = np.random.randn(1, 5)
    output1 = model.predict(x_test, verbose=0)
    output2 = loaded_model.predict(x_test, verbose=0)
    
    print(f"原模型输出: {output1}")
    print(f"加载模型输出: {output2}")
    print(f"输出是否相同: {np.allclose(output1, output2)}")


def callbacks_example():
    """回调函数示例"""
    print("\n" + "=" * 60)
    print("回调函数示例")
    print("=" * 60)
    
    # 创建回调
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=3,
            restore_best_weights=True
        ),
        keras.callbacks.ModelCheckpoint(
            'best_model.h5',
            monitor='val_loss',
            save_best_only=True
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=2
        )
    ]
    
    print("回调函数:")
    print("1. EarlyStopping: 早停防止过拟合")
    print("2. ModelCheckpoint: 保存最佳模型")
    print("3. ReduceLROnPlateau: 动态调整学习率")


def transfer_learning():
    """迁移学习示例"""
    print("\n" + "=" * 60)
    print("迁移学习示例")
    print("=" * 60)
    
    # 加载预训练模型（示例）
    base_model = keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # 冻结基础模型
    base_model.trainable = False
    
    # 添加自定义层
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    
    print("迁移学习模型结构:")
    print(f"基础模型可训练: {base_model.trainable}")
    print(f"自定义层可训练: {True}")


if __name__ == "__main__":
    print("TensorFlow Keras模型示例\n")
    print("注意：这些内容主要用于模型训练，应用开发通常不需要\n")
    
    sequential_model()
    functional_api()
    cnn_model()
    training_example()
    model_save_load()
    callbacks_example()
    transfer_learning()
    
    # 清理
    import os
    import shutil
    if os.path.exists('tf_model'):
        shutil.rmtree('tf_model')
        print("\n已清理临时目录 tf_model/")
    if os.path.exists('best_model.h5'):
        os.remove('best_model.h5')
        print("已清理临时文件 best_model.h5")

