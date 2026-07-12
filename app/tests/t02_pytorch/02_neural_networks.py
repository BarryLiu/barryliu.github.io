"""
PyTorch神经网络示例
学习目标：掌握如何使用PyTorch构建神经网络
"""

import torch
import torch.nn as nn
import torch.optim as optim


def simple_linear_model():
    """简单线性模型"""
    print("=" * 60)
    print("简单线性模型")
    print("=" * 60)
    
    # 定义模型
    model = nn.Linear(in_features=10, out_features=1)
    
    print(f"模型: {model}")
    print(f"权重形状: {model.weight.shape}")
    print(f"偏置形状: {model.bias.shape}")
    
    # 前向传播
    x = torch.randn(5, 10)  # 5个样本，每个10个特征
    output = model(x)
    
    print(f"\n输入形状: {x.shape}")
    print(f"输出形状: {output.shape}")


def multi_layer_network():
    """多层神经网络"""
    print("\n" + "=" * 60)
    print("多层神经网络")
    print("=" * 60)
    
    class SimpleNN(nn.Module):
        def __init__(self, input_size, hidden_size, output_size):
            super(SimpleNN, self).__init__()
            self.fc1 = nn.Linear(input_size, hidden_size)
            self.relu = nn.ReLU()
            self.fc2 = nn.Linear(hidden_size, output_size)
        
        def forward(self, x):
            x = self.fc1(x)
            x = self.relu(x)
            x = self.fc2(x)
            return x
    
    # 创建模型
    model = SimpleNN(input_size=784, hidden_size=128, output_size=10)
    
    print(f"模型结构:")
    print(model)
    
    # 计算参数量
    total_params = sum(p.numel() for p in model.parameters())
    print(f"\n总参数量: {total_params:,}")
    
    # 前向传播
    x = torch.randn(32, 784)  # 32个样本，每个784维（如28x28图像）
    output = model(x)
    print(f"\n输入形状: {x.shape}")
    print(f"输出形状: {output.shape}")


def training_example():
    """训练示例"""
    print("\n" + "=" * 60)
    print("训练示例（简化版）")
    print("=" * 60)
    
    # 定义简单模型
    model = nn.Linear(1, 1)
    
    # 定义损失函数和优化器
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    
    # 生成训练数据（y = 2x + 1）
    x_train = torch.randn(100, 1)
    y_train = 2 * x_train + 1 + 0.1 * torch.randn(100, 1)  # 添加噪声
    
    print(f"训练样本数: {x_train.shape[0]}")
    
    # 训练循环
    num_epochs = 100
    for epoch in range(num_epochs):
        # 前向传播
        y_pred = model(x_train)
        loss = criterion(y_pred, y_train)
        
        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 20 == 0:
            print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}")
    
    # 查看学习到的参数
    print(f"\n学习到的权重: {model.weight.item():.4f} (真实值: 2.0)")
    print(f"学习到的偏置: {model.bias.item():.4f} (真实值: 1.0)")


def cnn_example():
    """卷积神经网络示例"""
    print("\n" + "=" * 60)
    print("卷积神经网络（CNN）示例")
    print("=" * 60)
    
    class SimpleCNN(nn.Module):
        def __init__(self):
            super(SimpleCNN, self).__init__()
            self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
            self.relu = nn.ReLU()
            self.pool = nn.MaxPool2d(2, 2)
            self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
            self.fc = nn.Linear(64 * 7 * 7, 10)
        
        def forward(self, x):
            x = self.pool(self.relu(self.conv1(x)))
            x = self.pool(self.relu(self.conv2(x)))
            x = x.view(-1, 64 * 7 * 7)
            x = self.fc(x)
            return x
    
    model = SimpleCNN()
    print(f"模型结构:")
    print(model)
    
    # 测试输入
    x = torch.randn(1, 1, 28, 28)  # 1个样本，1通道，28x28图像
    output = model(x)
    print(f"\n输入形状: {x.shape}")
    print(f"输出形状: {output.shape}")


def rnn_example():
    """循环神经网络示例"""
    print("\n" + "=" * 60)
    print("循环神经网络（RNN）示例")
    print("=" * 60)
    
    # LSTM示例
    lstm = nn.LSTM(input_size=10, hidden_size=20, num_layers=2, batch_first=True)
    
    # 输入: (batch_size, seq_length, input_size)
    x = torch.randn(5, 10, 10)  # 5个样本，序列长度10，特征维度10
    
    output, (hidden, cell) = lstm(x)
    
    print(f"输入形状: {x.shape}")
    print(f"输出形状: {output.shape}")
    print(f"隐藏状态形状: {hidden.shape}")
    print(f"细胞状态形状: {cell.shape}")


def transformer_example():
    """Transformer示例（大模型基础）"""
    print("\n" + "=" * 60)
    print("Transformer示例（大模型基础）")
    print("=" * 60)
    
    # 使用PyTorch内置的Transformer
    encoder_layer = nn.TransformerEncoderLayer(
        d_model=512,
        nhead=8,
        dim_feedforward=2048,
        batch_first=True
    )
    
    transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=6)
    
    # 输入: (batch_size, seq_length, d_model)
    x = torch.randn(2, 10, 512)  # 2个样本，序列长度10，特征维度512
    
    output = transformer_encoder(x)
    
    print(f"输入形状: {x.shape}")
    print(f"输出形状: {output.shape}")
    print(f"\n说明: Transformer是大语言模型（如GPT）的基础架构")


if __name__ == "__main__":
    print("PyTorch神经网络示例\n")
    print("注意：这些内容主要用于模型训练，应用开发通常不需要\n")
    
    simple_linear_model()
    multi_layer_network()
    training_example()
    cnn_example()
    rnn_example()
    transformer_example()

