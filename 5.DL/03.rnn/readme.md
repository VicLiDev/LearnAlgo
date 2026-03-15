# 循环神经网络 (RNN)

## 1. 简介

循环神经网络专门处理序列数据，通过隐藏状态记忆历史信息。

## 2. 基础RNN

### 2.1 结构
```
h_t = tanh(W_hh * h_{t-1} + W_xh * x_t + b_h)
y_t = W_hy * h_t + b_y
```

### 2.2 特点
- 参数共享
- 处理变长序列
- 梯度消失/爆炸问题

## 3. LSTM

### 3.1 门控机制
```
f_t = sigmoid(W_f * [h_{t-1}, x_t] + b_f)  # 遗忘门
i_t = sigmoid(W_i * [h_{t-1}, x_t] + b_i)  # 输入门
o_t = sigmoid(W_o * [h_{t-1}, x_t] + b_o)  # 输出门

C_t = f_t * C_{t-1} + i_t * tanh(W_c * [h_{t-1}, x_t] + b_c)
h_t = o_t * tanh(C_t)
```

### 3.2 优势
- 解决长期依赖问题
- 门控机制控制信息流

## 4. GRU

### 4.1 简化结构
```
z_t = sigmoid(W_z * [h_{t-1}, x_t])  # 更新门
r_t = sigmoid(W_r * [h_{t-1}, x_t])  # 重置门

h_t = (1-z_t) * h_{t-1} + z_t * tanh(W * [r_t * h_{t-1}, x_t])
```

### 4.2 对比LSTM
- 参数更少
- 训练更快
- 性能相近

## 5. 变体

### 5.1 双向RNN
```
h_t = [h_t_forward; h_t_backward]
```
同时考虑过去和未来信息。

### 5.2 深层RNN
堆叠多个RNN层。

### 5.3 序列到序列 (Seq2Seq)
- 编码器-解码器结构
- 注意力机制

## 6. 应用场景

| 应用 | 模型 |
|------|------|
| 文本分类 | BiLSTM |
| 机器翻译 | Seq2Seq + Attention |
| 语音识别 | CTC + LSTM |
| 时间序列 | LSTM/GRU |

## 7. 训练技巧

### 7.1 梯度裁剪
```
grad = grad * min(1, max_norm / ||grad||)
```

### 7.2 序列长度
- 截断反向传播 (BPTT)
- 按长度分桶

## 8. 示例代码

见 `demo.py`
