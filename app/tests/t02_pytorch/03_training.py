"""
PyTorch训练完整示例
学习目标：掌握完整的模型训练流程
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np


class SimpleDataset(Dataset):
    """简单数据集"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __len__(self):
        return len(self.x)
    
    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]


class SimpleModel(nn.Module):
    """简单模型"""
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x


def create_dummy_data():
    """创建虚拟数据"""
    # 生成分类数据
    n_samples = 1000
    n_features = 20
    n_classes = 3
    
    x = torch.randn(n_samples, n_features)
    y = torch.randint(0, n_classes, (n_samples,))
    
    return x, y


def training_loop():
    """完整训练循环"""
    print("=" * 60)
    print("完整训练循环示例")
    print("=" * 60)
    
    # 设置随机种子
    torch.manual_seed(42)
    np.random.seed(42)
    
    # 创建数据
    x, y = create_dummy_data()
    
    # 划分训练集和验证集
    train_size = int(0.8 * len(x))
    x_train, x_val = x[:train_size], x[train_size:]
    y_train, y_val = y[:train_size], y[train_size:]
    
    # 创建数据集和数据加载器
    train_dataset = SimpleDataset(x_train, y_train)
    val_dataset = SimpleDataset(x_val, y_val)
    
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
    
    print(f"训练样本数: {len(train_dataset)}")
    print(f"验证样本数: {len(val_dataset)}")
    
    # 创建模型
    model = SimpleModel(input_size=20, hidden_size=64, output_size=3)
    
    # 损失函数和优化器
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # 训练
    num_epochs = 10
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    
    print(f"\n使用设备: {device}")
    print(f"开始训练...\n")
    
    for epoch in range(num_epochs):
        # 训练阶段
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        
        for batch_x, batch_y in train_loader:
            batch_x = batch_x.to(device)
            batch_y = batch_y.to(device)
            
            # 前向传播
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            
            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            # 统计
            train_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            train_total += batch_y.size(0)
            train_correct += (predicted == batch_y).sum().item()
        
        # 验证阶段
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for batch_x, batch_y in val_loader:
                batch_x = batch_x.to(device)
                batch_y = batch_y.to(device)
                
                outputs = model(batch_x)
                loss = criterion(outputs, batch_y)
                
                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                val_total += batch_y.size(0)
                val_correct += (predicted == batch_y).sum().item()
        
        # 打印结果
        train_acc = 100 * train_correct / train_total
        val_acc = 100 * val_correct / val_total
        
        print(f"Epoch [{epoch+1}/{num_epochs}]")
        print(f"  训练 Loss: {train_loss/len(train_loader):.4f}, Acc: {train_acc:.2f}%")
        print(f"  验证 Loss: {val_loss/len(val_loader):.4f}, Acc: {val_acc:.2f}%")
        print()


def model_save_load():
    """模型保存和加载"""
    print("=" * 60)
    print("模型保存和加载")
    print("=" * 60)
    
    # 创建模型
    model = SimpleModel(input_size=20, hidden_size=64, output_size=3)
    
    # 保存模型
    torch.save(model.state_dict(), 'model.pth')
    print("模型已保存到 model.pth")
    
    # 加载模型
    loaded_model = SimpleModel(input_size=20, hidden_size=64, output_size=3)
    loaded_model.load_state_dict(torch.load('model.pth'))
    loaded_model.eval()
    
    print("模型已加载")
    
    # 测试
    x_test = torch.randn(1, 20)
    output1 = model(x_test)
    output2 = loaded_model(x_test)
    
    print(f"原模型输出: {output1}")
    print(f"加载模型输出: {output2}")
    print(f"输出是否相同: {torch.allclose(output1, output2)}")


def transfer_learning_example():
    """迁移学习示例"""
    print("\n" + "=" * 60)
    print("迁移学习示例")
    print("=" * 60)
    
    # 预训练模型（简化示例）
    pretrained_model = SimpleModel(input_size=20, hidden_size=64, output_size=10)
    
    # 冻结部分层
    for param in pretrained_model.fc1.parameters():
        param.requires_grad = False
    
    print("冻结了fc1层的参数")
    print(f"fc1参数可训练: {list(pretrained_model.fc1.parameters())[0].requires_grad}")
    print(f"fc2参数可训练: {list(pretrained_model.fc2.parameters())[0].requires_grad}")
    
    # 只优化未冻结的参数
    optimizer = optim.Adam(
        filter(lambda p: p.requires_grad, pretrained_model.parameters()),
        lr=0.001
    )
    print(f"优化器参数数量: {len(list(optimizer.param_groups[0]['params']))}")


if __name__ == "__main__":
    print("PyTorch训练完整示例\n")
    print("注意：这些内容主要用于模型训练，应用开发通常不需要\n")
    
    training_loop()
    model_save_load()
    transfer_learning_example()
    
    # 清理
    import os
    if os.path.exists('model.pth'):
        os.remove('model.pth')
        print("\n已清理临时文件 model.pth")

