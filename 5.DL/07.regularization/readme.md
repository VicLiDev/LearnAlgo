# 正则化技术 (Regularization)

## 1. 简介

正则化是防止过拟合、提升模型泛化能力的技术。

## 2. L1/L2正则化

### 2.1 L2正则化 (Ridge/权重衰减)
```
L_total = L + λ * ||w||²
```
- 权重趋向于较小值
- 防止任一权重过大

### 2.2 L1正则化 (Lasso)
```
L_total = L + λ * ||w||₁
```
- 产生稀疏解
- 可用于特征选择

### 2.3 弹性网络
```
L_total = L + λ1 * ||w||₁ + λ2 * ||w||²
```

## 3. Dropout

### 3.1 原理
训练时随机将神经元输出置零。

### 3.2 实现
```
# 训练时
output = activation(input @ W) * mask / (1-p)
# mask ~ Bernoulli(1-p)

# 测试时
output = activation(input @ W) * (1-p)
```

### 3.3 变体
- **DropConnect**: 随机置零权重
- **Spatial Dropout**: 整个通道dropout
- **DropBlock**: 局部区域dropout

## 4. Batch Normalization

### 4.1 原理
```
μ_B = mean(x_B)
σ²_B = var(x_B)
x̂ = (x - μ_B) / √(σ²_B + ε)
y = γ * x̂ + β
```

### 4.2 作用
- 加速训练
- 允许更大学习率
- 减少对初始化敏感

### 4.3 训练vs推理
- 训练: 使用batch统计
- 推理: 使用移动平均

## 5. Layer Normalization

### 5.1 原理
```
μ = mean(x)
σ² = var(x)
y = (x - μ) / √(σ² + ε) * γ + β
```
- 对单个样本的所有特征归一化
- 适合RNN/Transformer

## 6. 数据增强

### 6.1 图像增强
- 随机裁剪/翻转
- 颜色抖动
- 旋转/缩放

### 6.2 高级增强
- **Mixup**: 混合两个样本
- **CutMix**: 裁剪拼接
- **AutoAugment**: 自动搜索策略

## 7. 早停 (Early Stopping)

```
for epoch in epochs:
    train()
    val_loss = validate()
    if val_loss < best_loss:
        best_loss = val_loss
        save_model()
    if no_improvement > patience:
        break
```

## 8. 正则化效果对比

| 技术 | 参数开销 | 计算开销 | 适用场景 |
|------|---------|---------|---------|
| L2 | 无 | 低 | 通用 |
| Dropout | 无 | 低 | 全连接层 |
| BatchNorm | 2×C | 中 | CNN |
| LayerNorm | 2×D | 低 | RNN/Transformer |
| 数据增强 | 无 | 中/高 | 图像/文本 |

## 9. 实践建议

1. **CNN**: BatchNorm + 数据增强 + L2
2. **Transformer**: LayerNorm + Dropout
3. **小数据集**: 强数据增强 + 早停
4. **过拟合严重**: 增大正则化强度

## 10. 示例代码

见 `demo.py`
