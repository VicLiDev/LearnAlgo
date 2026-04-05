"""
循环神经网络 (RNN) 示例代码

包含内容:
1. 基础RNN实现
2. LSTM实现
3. GRU实现
4. 序列预测
"""

import numpy as np
import matplotlib.pyplot as plt
from t01_mpl import chinese_font

plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


# ========== 基础RNN ==========
class SimpleRNN:
    def __init__(self, input_size, hidden_size, output_size):
        self.hidden_size = hidden_size
        self.W_xh = np.random.randn(input_size, hidden_size) * 0.01
        self.W_hh = np.random.randn(hidden_size, hidden_size) * 0.01
        self.W_hy = np.random.randn(hidden_size, output_size) * 0.01
        self.b_h = np.zeros((1, hidden_size))
        self.b_y = np.zeros((1, output_size))

    def forward(self, x):
        h = np.zeros((1, self.hidden_size))
        self.hidden_states = [h]

        for t in range(len(x)):
            h = np.tanh(x[t:t+1] @ self.W_xh + h @ self.W_hh + self.b_h)
            self.hidden_states.append(h)

        self.output = self.hidden_states[-1] @ self.W_hy + self.b_y
        return self.output

    def predict(self, x):
        return self.forward(x)


# ========== LSTM ==========
class LSTM:
    def __init__(self, input_size, hidden_size):
        self.hidden_size = hidden_size
        # 合并所有门的权重
        self.W = np.random.randn(input_size + hidden_size, 4 * hidden_size) * 0.01
        self.b = np.zeros((1, 4 * hidden_size))

    def forward(self, x):
        h = np.zeros((1, self.hidden_size))
        c = np.zeros((1, self.hidden_size))
        self.hidden_states = [h]

        for t in range(len(x)):
            combined = np.concatenate([x[t:t+1], h], axis=1)
            gates = combined @ self.W + self.b

            f = self.sigmoid(gates[:, :self.hidden_size])
            i = self.sigmoid(gates[:, self.hidden_size:2*self.hidden_size])
            c_tilde = np.tanh(gates[:, 2*self.hidden_size:3*self.hidden_size])
            o = self.sigmoid(gates[:, 3*self.hidden_size:])

            c = f * c + i * c_tilde
            h = o * np.tanh(c)
            self.hidden_states.append(h)

        return h

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))


# ========== GRU ==========
class GRU:
    def __init__(self, input_size, hidden_size):
        self.hidden_size = hidden_size
        self.W_z = np.random.randn(input_size + hidden_size, hidden_size) * 0.01
        self.W_r = np.random.randn(input_size + hidden_size, hidden_size) * 0.01
        self.W_h = np.random.randn(input_size + hidden_size, hidden_size) * 0.01

    def forward(self, x):
        h = np.zeros((1, self.hidden_size))
        self.hidden_states = [h]

        for t in range(len(x)):
            combined = np.concatenate([x[t:t+1], h], axis=1)
            z = self.sigmoid(combined @ self.W_z)
            r = self.sigmoid(combined @ self.W_r)
            combined_r = np.concatenate([x[t:t+1], r * h], axis=1)
            h_tilde = np.tanh(combined_r @ self.W_h)
            h = (1 - z) * h + z * h_tilde
            self.hidden_states.append(h)

        return h

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))


def demo_sequence_prediction():
    """序列预测演示"""
    print("=" * 60)
    print("序列预测演示")
    print("=" * 60)

    np.random.seed(42)

    # 生成正弦波数据
    t = np.linspace(0, 4*np.pi, 100)
    data = np.sin(t).reshape(-1, 1)

    # 创建并训练简单的RNN
    rnn = SimpleRNN(input_size=1, hidden_size=16, output_size=1)

    # 简单的前向传播测试
    sequence = data[:20]
    output = rnn.forward(sequence)

    print(f"输入序列长度: {len(sequence)}")
    print(f"输出形状: {output.shape}")
    print(f"隐藏状态数量: {len(rnn.hidden_states)}")

    # 可视化
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 原始序列
    axes[0].plot(t, data, 'b-', linewidth=2, label='正弦波')
    axes[0].set_xlabel('时间', fontsize=12)
    axes[0].set_ylabel('值', fontsize=12)
    axes[0].set_title('输入序列', fontsize=14)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # 隐藏状态变化
    hidden_states = np.array([h.flatten() for h in rnn.hidden_states])
    axes[1].plot(hidden_states[:, :3], linewidth=2)
    axes[1].set_xlabel('时间步', fontsize=12)
    axes[1].set_ylabel('隐藏状态值', fontsize=12)
    axes[1].set_title('RNN隐藏状态变化', fontsize=14)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('rnn_sequence.png', dpi=150, bbox_inches='tight')
    plt.show()


def demo_lstm_gru_comparison():
    """LSTM vs GRU 对比"""
    print("=" * 60)
    print("LSTM vs GRU 结构对比")
    print("=" * 60)

    print("\nLSTM结构:")
    print("  - 遗忘门 (f_t): 控制哪些信息从细胞状态中丢弃")
    print("  - 输入门 (i_t): 控制哪些新信息添加到细胞状态")
    print("  - 输出门 (o_t): 控制输出哪些信息")

    print("\nGRU结构:")
    print("  - 更新门 (z_t): 控制新旧状态的混合比例")
    print("  - 重置门 (r_t): 控制前一状态对当前状态的影响")

    print("\n参数对比:")
    input_size, hidden_size = 10, 20
    lstm_params = (input_size + hidden_size) * 4 * hidden_size
    gru_params = (input_size + hidden_size) * 3 * hidden_size
    print(f"  LSTM参数量: {lstm_params}")
    print(f"  GRU参数量: {gru_params}")
    print(f"  GRU比LSTM少: {(1 - gru_params/lstm_params)*100:.1f}%")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("循环神经网络 (RNN) 完整示例")
    print("=" * 60 + "\n")

    demo_sequence_prediction()
    demo_lstm_gru_comparison()

    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
