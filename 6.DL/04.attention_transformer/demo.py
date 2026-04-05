"""
注意力机制与Transformer 示例代码

包含内容:
1. 自注意力实现
2. 多头注意力
3. 位置编码
4. 简化Transformer
"""

import numpy as np
import matplotlib.pyplot as plt
from t01_mpl import chinese_font

plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def softmax(x, axis=-1):
    """Softmax函数"""
    exp_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return exp_x / np.sum(exp_x, axis=axis, keepdims=True)


def attention(Q, K, V, mask=None):
    """缩放点积注意力"""
    d_k = Q.shape[-1]
    scores = Q @ K.transpose(0, 2, 1) / np.sqrt(d_k)

    if mask is not None:
        scores = scores + mask * -1e9

    attn_weights = softmax(scores, axis=-1)
    return attn_weights @ V, attn_weights


class MultiHeadAttention:
    """多头注意力"""

    def __init__(self, d_model=512, num_heads=8):
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.W_q = np.random.randn(d_model, d_model) * 0.01
        self.W_k = np.random.randn(d_model, d_model) * 0.01
        self.W_v = np.random.randn(d_model, d_model) * 0.01
        self.W_o = np.random.randn(d_model, d_model) * 0.01

    def forward(self, Q, K, V, mask=None):
        batch_size = Q.shape[0]

        # 线性变换
        Q = Q @ self.W_q
        K = K @ self.W_k
        V = V @ self.W_v

        # 分割多头
        Q = Q.reshape(batch_size, -1, self.num_heads, self.d_k).transpose(0, 2, 1, 3)
        K = K.reshape(batch_size, -1, self.num_heads, self.d_k).transpose(0, 2, 1, 3)
        V = V.reshape(batch_size, -1, self.num_heads, self.d_k).transpose(0, 2, 1, 3)

        # 注意力
        attn_output, attn_weights = attention(Q, K, V, mask)

        # 合并多头
        attn_output = attn_output.transpose(0, 2, 1, 3).reshape(batch_size, -1, self.d_model)

        return attn_output @ self.W_o, attn_weights


def positional_encoding(max_len, d_model):
    """位置编码"""
    PE = np.zeros((max_len, d_model))
    position = np.arange(max_len)[:, np.newaxis]
    div_term = np.exp(np.arange(0, d_model, 2) * -np.log(10000.0) / d_model)

    PE[:, 0::2] = np.sin(position * div_term)
    PE[:, 1::2] = np.cos(position * div_term)

    return PE


def demo_attention_weights():
    """注意力权重可视化"""
    print("=" * 60)
    print("1. 注意力权重可视化")
    print("=" * 60)

    # 模拟简单序列
    np.random.seed(42)
    seq_len = 6
    d_model = 8

    X = np.random.randn(1, seq_len, d_model)
    mha = MultiHeadAttention(d_model=d_model, num_heads=2)

    output, weights = mha.forward(X, X, X)

    print(f"输入形状: {X.shape}")
    print(f"输出形状: {output.shape}")
    print(f"注意力权重形状: {weights.shape}")

    # 可视化注意力权重
    fig, ax = plt.subplots(figsize=(8, 6))

    # 取第一个头的权重
    attn = weights[0, 0]

    im = ax.imshow(attn, cmap='Blues')
    ax.set_xlabel('Key位置', fontsize=12)
    ax.set_ylabel('Query位置', fontsize=12)
    ax.set_title('注意力权重矩阵', fontsize=14)

    for i in range(seq_len):
        for j in range(seq_len):
            ax.text(j, i, f'{attn[i,j]:.2f}', ha='center', va='center')

    plt.colorbar(im, ax=ax)
    plt.tight_layout()
    plt.savefig('transformer_attention.png', dpi=150, bbox_inches='tight')
    plt.show()


def demo_positional_encoding():
    """位置编码可视化"""
    print("=" * 60)
    print("2. 位置编码可视化")
    print("=" * 60)

    max_len = 50
    d_model = 128
    PE = positional_encoding(max_len, d_model)

    print(f"位置编码形状: {PE.shape}")

    fig, ax = plt.subplots(figsize=(12, 6))

    im = ax.imshow(PE.T, cmap='RdBu', aspect='auto')
    ax.set_xlabel('位置', fontsize=12)
    ax.set_ylabel('维度', fontsize=12)
    ax.set_title('正弦位置编码', fontsize=14)
    plt.colorbar(im, ax=ax)

    plt.tight_layout()
    plt.savefig('transformer_pe.png', dpi=150, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("注意力机制与Transformer 完整示例")
    print("=" * 60 + "\n")

    demo_attention_weights()
    demo_positional_encoding()

    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
