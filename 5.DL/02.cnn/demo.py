"""
卷积神经网络 (CNN) 示例代码

包含内容:
1. 卷积操作演示
2. 池化操作演示
3. 经典网络结构
4. 特征可视化
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def conv2d(input_data, kernel, stride=1, padding=0):
    """2D卷积操作"""
    if padding > 0:
        input_data = np.pad(input_data, padding, mode='constant')

    h, w = input_data.shape
    kh, kw = kernel.shape

    out_h = (h - kh) // stride + 1
    out_w = (w - kw) // stride + 1
    output = np.zeros((out_h, out_w))

    for i in range(out_h):
        for j in range(out_w):
            region = input_data[i*stride:i*stride+kh, j*stride:j*stride+kw]
            output[i, j] = np.sum(region * kernel)

    return output


def max_pool2d(input_data, pool_size=2, stride=2):
    """最大池化"""
    h, w = input_data.shape
    out_h, out_w = h // stride, w // stride
    output = np.zeros((out_h, out_w))

    for i in range(out_h):
        for j in range(out_w):
            region = input_data[i*stride:i*stride+pool_size, j*stride:j*stride+pool_size]
            output[i, j] = np.max(region)

    return output


def demo_convolution():
    """卷积操作演示"""
    print("=" * 60)
    print("1. 卷积操作演示")
    print("=" * 60)

    # 创建示例图像
    image = np.array([
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25]
    ], dtype=float)

    # 不同卷积核
    kernels = {
        '边缘检测': np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]),
        '锐化': np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]),
        '模糊': np.ones((3, 3)) / 9
    }

    fig, axes = plt.subplots(2, 2, figsize=(10, 10))

    # 原图
    axes[0, 0].imshow(image, cmap='gray')
    axes[0, 0].set_title('原图', fontsize=14)
    axes[0, 0].axis('off')

    # 卷积结果
    for (name, kernel), ax in zip(kernels.items(), [axes[0, 1], axes[1, 0], axes[1, 1]]):
        result = conv2d(image, kernel)
        ax.imshow(result, cmap='gray')
        ax.set_title(f'{name}卷积', fontsize=14)
        ax.axis('off')
        print(f"{name}卷积结果:\n{result}\n")

    plt.tight_layout()
    plt.savefig('cnn_convolution.png', dpi=150, bbox_inches='tight')
    plt.show()


def demo_pooling():
    """池化操作演示"""
    print("=" * 60)
    print("2. 池化操作演示")
    print("=" * 60)

    feature_map = np.array([
        [1, 3, 2, 4],
        [5, 6, 7, 8],
        [9, 2, 3, 1],
        [4, 5, 6, 7]
    ], dtype=float)

    pooled = max_pool2d(feature_map, pool_size=2, stride=2)

    print(f"原始特征图:\n{feature_map}")
    print(f"\n最大池化后 (2x2):\n{pooled}")

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    axes[0].imshow(feature_map, cmap='Blues')
    axes[0].set_title('原始特征图', fontsize=14)
    for i in range(4):
        for j in range(4):
            axes[0].text(j, i, f'{int(feature_map[i,j])}', ha='center', va='center')

    axes[1].imshow(pooled, cmap='Blues')
    axes[1].set_title('最大池化后', fontsize=14)
    for i in range(2):
        for j in range(2):
            axes[1].text(j, i, f'{int(pooled[i,j])}', ha='center', va='center')

    for ax in axes:
        ax.axis('off')

    plt.tight_layout()
    plt.savefig('cnn_pooling.png', dpi=150, bbox_inches='tight')
    plt.show()


def demo_architecture():
    """网络架构演示"""
    print("=" * 60)
    print("3. 经典CNN架构")
    print("=" * 60)

    # LeNet-5结构
    print("\nLeNet-5 结构:")
    print("  Input(32x32x1)")
    print("  -> Conv(5x5,6) -> 28x28x6")
    print("  -> Pool(2x2) -> 14x14x6")
    print("  -> Conv(5x5,16) -> 10x10x16")
    print("  -> Pool(2x2) -> 5x5x16")
    print("  -> FC(120) -> FC(84) -> FC(10)")

    # 可视化特征图尺寸变化
    fig, ax = plt.subplots(figsize=(14, 4))

    layers = ['Input', 'Conv1', 'Pool1', 'Conv2', 'Pool2', 'FC1', 'FC2', 'Output']
    sizes = [1024, 4704, 1176, 1600, 400, 120, 84, 10]
    colors = ['#3498db', '#e74c3c', '#e74c3c', '#e74c3c', '#e74c3c', '#2ecc71', '#2ecc71', '#9b59b6']

    bars = ax.bar(layers, sizes, color=colors, alpha=0.8)
    ax.set_ylabel('特征数量', fontsize=12)
    ax.set_title('LeNet-5 特征图尺寸变化', fontsize=14)
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('cnn_architecture.png', dpi=150, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("卷积神经网络 (CNN) 完整示例")
    print("=" * 60 + "\n")

    demo_convolution()
    demo_pooling()
    demo_architecture()

    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
