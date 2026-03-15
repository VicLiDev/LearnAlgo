"""
多层感知机 (MLP) 示例代码

包含内容:
1. 激活函数可视化
2. 手动实现MLP
3. PyTorch实现
4. 训练过程可视化
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


# ========== 激活函数 ==========
def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))


def tanh(x):
    return np.tanh(x)


def relu(x):
    return np.maximum(0, x)


def leaky_relu(x, alpha=0.01):
    return np.where(x > 0, x, alpha * x)


def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)


# ========== 手动实现MLP ==========
class MLP:
    """手动实现的多层感知机"""

    def __init__(self, layer_sizes, activation='relu'):
        self.weights = []
        self.biases = []
        self.activation = activation

        for i in range(len(layer_sizes) - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * np.sqrt(2.0 / layer_sizes[i])
            b = np.zeros((1, layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)

    def _activate(self, x):
        if self.activation == 'relu':
            return relu(x)
        elif self.activation == 'sigmoid':
            return sigmoid(x)
        elif self.activation == 'tanh':
            return tanh(x)

    def _activate_derivative(self, x):
        if self.activation == 'relu':
            return (x > 0).astype(float)
        elif self.activation == 'sigmoid':
            s = sigmoid(x)
            return s * (1 - s)
        elif self.activation == 'tanh':
            return 1 - tanh(x) ** 2

    def forward(self, X):
        self.activations = [X]
        self.z_values = []

        for i in range(len(self.weights) - 1):
            z = self.activations[-1] @ self.weights[i] + self.biases[i]
            self.z_values.append(z)
            self.activations.append(self._activate(z))

        # 输出层
        z = self.activations[-1] @ self.weights[-1] + self.biases[-1]
        self.z_values.append(z)
        self.activations.append(softmax(z) if z.shape[1] > 1 else sigmoid(z))

        return self.activations[-1]

    def backward(self, y, lr=0.01):
        m = y.shape[0]
        y_onehot = np.eye(self.activations[-1].shape[1])[y] if len(y.shape) == 1 else y

        delta = self.activations[-1] - y_onehot

        for i in range(len(self.weights) - 1, -1, -1):
            dW = self.activations[i].T @ delta / m
            db = np.sum(delta, axis=0, keepdims=True) / m

            if i > 0:
                delta = (delta @ self.weights[i].T) * self._activate_derivative(self.z_values[i-1])

            self.weights[i] -= lr * dW
            self.biases[i] -= lr * db

    def train(self, X, y, epochs=100, lr=0.1):
        losses = []
        for _ in range(epochs):
            output = self.forward(X)
            loss = -np.mean(np.log(output[np.arange(len(y)), y] + 1e-8))
            losses.append(loss)
            self.backward(y, lr)
        return losses


def demo_activations():
    """激活函数可视化"""
    print("=" * 60)
    print("1. 激活函数可视化")
    print("=" * 60)

    x = np.linspace(-5, 5, 100)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 激活函数
    ax = axes[0]
    ax.plot(x, sigmoid(x), label='Sigmoid', linewidth=2)
    ax.plot(x, tanh(x), label='Tanh', linewidth=2)
    ax.plot(x, relu(x), label='ReLU', linewidth=2)
    ax.plot(x, leaky_relu(x), label='Leaky ReLU', linewidth=2)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x)', fontsize=12)
    ax.set_title('激活函数', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-1.5, 2)

    # 导数
    ax = axes[1]
    ax.plot(x, sigmoid(x) * (1 - sigmoid(x)), label="Sigmoid'", linewidth=2)
    ax.plot(x, 1 - tanh(x)**2, label="Tanh'", linewidth=2)
    ax.plot(x, (x > 0).astype(float), label="ReLU'", linewidth=2)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel("f'(x)", fontsize=12)
    ax.set_title('激活函数导数', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('mlp_activations.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("激活函数图已保存\n")


def demo_mlp_training():
    """MLP训练演示"""
    print("=" * 60)
    print("2. MLP训练演示")
    print("=" * 60)

    # 生成数据
    np.random.seed(42)
    X = np.random.randn(200, 2)
    y = (X[:, 0] * X[:, 1] > 0).astype(int)

    # 训练
    mlp = MLP([2, 16, 8, 2], activation='relu')
    losses = mlp.train(X, y, epochs=200, lr=0.5)

    # 预测
    preds = mlp.forward(X).argmax(axis=1)
    acc = (preds == y).mean()
    print(f"训练准确率: {acc:.4f}")

    # 可视化
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 损失曲线
    ax = axes[0]
    ax.plot(losses, color='steelblue', linewidth=2)
    ax.set_xlabel('Epoch', fontsize=12)
    ax.set_ylabel('Loss', fontsize=12)
    ax.set_title('训练损失曲线', fontsize=14)
    ax.grid(True, alpha=0.3)

    # 决策边界
    ax = axes[1]
    h = 0.02
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = mlp.forward(np.c_[xx.ravel(), yy.ravel()]).argmax(axis=1).reshape(xx.shape)

    ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.RdYlBu)
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.RdYlBu, edgecolors='black')
    ax.set_xlabel('X1', fontsize=12)
    ax.set_ylabel('X2', fontsize=12)
    ax.set_title('决策边界', fontsize=14)

    plt.tight_layout()
    plt.savefig('mlp_training.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("训练可视化图已保存\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("多层感知机 (MLP) 完整示例")
    print("=" * 60 + "\n")

    demo_activations()
    demo_mlp_training()

    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
