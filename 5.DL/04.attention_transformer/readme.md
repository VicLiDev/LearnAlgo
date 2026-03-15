# 注意力机制与Transformer

## 1. 简介

Transformer是2017年提出的革命性架构，完全基于注意力机制，摒弃了循环和卷积结构。

## 2. 注意力机制

### 2.1 基本概念
```
Attention(Q, K, V) = softmax(QK^T / √d_k) * V
```
- Q (Query): 查询
- K (Key): 键
- V (Value): 值

### 2.2 自注意力 (Self-Attention)
Q、K、V来自同一输入:
```
Q = X * W_Q
K = X * W_K
V = X * W_V
```

### 2.3 多头注意力 (Multi-Head)
```
MultiHead(Q,K,V) = Concat(head_1,...,head_h) * W_O
where head_i = Attention(Q*W_Q_i, K*W_K_i, V*W_V_i)
```

## 3. Transformer架构

### 3.1 编码器
```
输入 -> 多头注意力 -> Add&Norm -> FFN -> Add&Norm
```

### 3.2 解码器
```
输入 -> Masked多头注意力 -> Add&Norm
    -> 编码器-解码器注意力 -> Add&Norm
    -> FFN -> Add&Norm
```

### 3.3 位置编码
```
PE(pos, 2i) = sin(pos / 10000^(2i/d))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
```

## 4. 关键技术

### 4.1 残差连接
```
output = LayerNorm(x + Sublayer(x))
```

### 4.2 层归一化
```
LN(x) = γ * (x - μ) / σ + β
```

### 4.3 前馈网络
```
FFN(x) = max(0, x*W_1 + b_1) * W_2 + b_2
```

## 5. 计算复杂度

| 层类型 | 复杂度 | 序列长度 | 并行性 |
|--------|--------|---------|--------|
| Self-Attention | O(n²·d) | 受限 | 高 |
| RNN | O(n·d²) | 无限 | 低 |
| Conv | O(k·n·d²) | 受限 | 中 |

## 6. 预训练模型

### 6.1 BERT
- 双向编码器
- Masked Language Model
- Next Sentence Prediction

### 6.2 GPT
- 自回归解码器
- 单向注意力
- 生成任务

### 6.3 ViT
- 图像分块作为token
- 纯Transformer处理图像

## 7. 变体

- **Transformer-XL**: 处理长序列
- **Longformer**: 稀疏注意力
- **Performer**: 线性注意力

## 8. 示例代码

见 `demo.py`
