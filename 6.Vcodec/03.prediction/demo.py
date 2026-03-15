"""
预测编码示例：帧内预测、帧间预测
"""
import numpy as np
import matplotlib.pyplot as plt


def intra_prediction_4x4(block, mode):
    """
    H.264 4x4帧内预测

    Args:
        block: 当前块 (4x4)
        mode: 预测模式 (0-8)

    Returns:
        prediction: 预测块
    """
    # 假设参考像素在上边和左边
    # A-M 是参考像素
    # A B C D (上边)
    # E       |
    # F       | 左边
    # G       |
    # H       |

    # 简化：使用块本身的边界作为参考
    pred = np.zeros((4, 4))

    if mode == 0:  # Vertical
        for i in range(4):
            pred[i, :] = block[0, :]

    elif mode == 1:  # Horizontal
        for j in range(4):
            pred[:, j] = block[:, 0]

    elif mode == 2:  # DC
        avg = np.mean(block)
        pred[:, :] = avg

    elif mode == 3:  # Diagonal Down-Left
        for i in range(4):
            for j in range(4):
                pred[i, j] = (block[0, min(j+i, 3)] + block[0, min(j+i+1, 3)]) / 2

    elif mode == 4:  # Diagonal Down-Right
        for i in range(4):
            for j in range(4):
                if i >= j:
                    pred[i, j] = block[i-j, 0]
                else:
                    pred[i, j] = block[0, j-i]

    return pred


def intra_prediction_planar_8x8(reference):
    """
    HEVC Planar模式 (8x8)
    平滑区域的预测
    """
    pred = np.zeros((8, 8))

    # 使用边界像素进行双线性插值
    top = reference[0, :]   # 上边界
    left = reference[:, 0]  # 左边界

    for y in range(8):
        for x in range(8):
            # 双线性插值
            pred[y, x] = ((7-y) * top[x] + (y+1) * left[7] +
                         (7-x) * left[y] + (x+1) * top[7]) / 16

    return pred


def motion_compensation(reference, mv, block_size=16):
    """
    运动补偿

    Args:
        reference: 参考帧
        mv: 运动矢量 (dy, dx)
        block_size: 块大小

    Returns:
        prediction: 预测块
    """
    dy, dx = mv
    h, w = reference.shape

    # 计算参考位置
    y_start = int(dy)
    x_start = int(dx)

    # 边界检查
    y_start = max(0, min(y_start, h - block_size))
    x_start = max(0, min(x_start, w - block_size))

    return reference[y_start:y_start+block_size, x_start:x_start+block_size]


def bilinear_interpolation(reference, mv):
    """
    双线性插值 (1/4像素精度)

    Args:
        reference: 参考帧
        mv: 运动矢量 (可以是小数)

    Returns:
        prediction: 预测块
    """
    dy, dx = mv
    h, w = reference.shape
    bh, bw = 16, 16  # 预测块大小

    prediction = np.zeros((bh, bw))

    for y in range(bh):
        for x in range(bw):
            # 参考位置
            ref_y = dy + y
            ref_x = dx + x

            # 整数部分和小数部分
            y0 = int(np.floor(ref_y))
            x0 = int(np.floor(ref_x))
            fy = ref_y - y0
            fx = ref_x - x0

            # 边界检查
            y0 = max(0, min(y0, h - 2))
            x0 = max(0, min(x0, w - 2))

            # 双线性插值
            prediction[y, x] = (
                (1-fy) * (1-fx) * reference[y0, x0] +
                (1-fy) * fx * reference[y0, x0+1] +
                fy * (1-fx) * reference[y0+1, x0] +
                fy * fx * reference[y0+1, x0+1]
            )

    return prediction


def demonstrate_intra_prediction():
    """演示帧内预测"""
    print("=" * 50)
    print("帧内预测模式")
    print("=" * 50)

    # 创建测试块
    block = np.array([
        [100, 110, 120, 130],
        [105, 115, 125, 135],
        [110, 120, 130, 140],
        [115, 125, 135, 145]
    ], dtype=float)

    modes = {
        0: 'Vertical',
        1: 'Horizontal',
        2: 'DC',
        3: 'Diagonal Down-Left',
        4: 'Diagonal Down-Right'
    }

    fig, axes = plt.subplots(2, 3, figsize=(12, 8))

    # 原始块
    axes[0, 0].imshow(block, cmap='gray', vmin=90, vmax=150)
    axes[0, 0].set_title('原始块')

    for idx, (mode, name) in enumerate(modes.items()):
        pred = intra_prediction_4x4(block, mode)
        residual = block - pred
        mse = np.mean(residual ** 2)

        ax = axes.flat[idx + 1]
        ax.imshow(pred, cmap='gray', vmin=90, vmax=150)
        ax.set_title(f'{name}\nMSE={mse:.1f}')

        print(f"模式{mode} ({name}): MSE = {mse:.2f}")

    for ax in axes.flat:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def demonstrate_motion_compensation():
    """演示运动补偿"""
    print("\n" + "=" * 50)
    print("运动补偿")
    print("=" * 50)

    # 创建参考帧 (带图案)
    h, w = 64, 64
    reference = np.zeros((h, w))
    reference[20:40, 20:40] = 200  # 一个方块

    # 当前帧 (方块移动了)
    current = np.zeros((h, w))
    current[25:45, 30:50] = 200

    # 运动矢量 (从搜索得到)
    mv = (-5, -10)  # 实际运动是 (+5, +10)，所以MV是负的

    # 运动补偿
    prediction = motion_compensation(reference, mv, block_size=20)
    prediction_full = np.zeros((h, w))
    prediction_full[25:45, 30:50] = prediction

    # 残差
    residual = current - prediction_full

    print(f"运动矢量: ({mv[0]}, {mv[1]})")
    print(f"残差能量: {np.sum(residual**2):.1f}")

    # 可视化
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))

    axes[0, 0].imshow(reference, cmap='gray')
    axes[0, 0].set_title('参考帧')

    axes[0, 1].imshow(current, cmap='gray')
    axes[0, 1].set_title('当前帧')

    axes[1, 0].imshow(prediction_full, cmap='gray')
    axes[1, 0].set_title('运动补偿预测')

    axes[1, 1].imshow(np.abs(residual), cmap='hot')
    axes[1, 1].set_title('残差 (绝对值)')

    for ax in axes.flat:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def demonstrate_subpixel_interpolation():
    """演示亚像素插值"""
    print("\n" + "=" * 50)
    print("亚像素精度运动补偿")
    print("=" * 50)

    # 创建参考帧
    h, w = 32, 32
    x = np.linspace(0, 4*np.pi, w)
    y = np.linspace(0, 4*np.pi, h)
    X, Y = np.meshgrid(x, y)
    reference = np.sin(X) + np.sin(Y)
    reference = (reference + 2) * 60  # 缩放到0-240

    # 不同精度的MV
    mvs = [
        (5, 5),      # 整像素
        (5.5, 5.5),  # 1/2像素
        (5.25, 5.25) # 1/4像素
    ]

    fig, axes = plt.subplots(2, 2, figsize=(10, 10))

    axes[0, 0].imshow(reference, cmap='gray')
    axes[0, 0].set_title('参考帧')

    for idx, mv in enumerate(mvs):
        pred = bilinear_interpolation(reference, mv)
        axes.flat[idx + 1].imshow(pred, cmap='gray')
        axes.flat[idx + 1].set_title(f'MV = ({mv[0]}, {mv[1]})')

    for ax in axes.flat:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def demonstrate_residual_coding():
    """演示残差编码"""
    print("\n" + "=" * 50)
    print("残差特性")
    print("=" * 50)

    # 创建原始图像
    h, w = 64, 64
    original = np.zeros((h, w))
    original[20:40, 20:40] = 200

    # 预测 (简单的DC预测)
    prediction = np.ones((h, w)) * np.mean(original)

    # 残差
    residual = original - prediction

    print(f"原始图像能量: {np.sum(original**2):.1f}")
    print(f"残差能量: {np.sum(residual**2):.1f}")

    # 残差直方图
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    axes[0].imshow(original, cmap='gray')
    axes[0].set_title('原始图像')

    axes[1].imshow(prediction, cmap='gray')
    axes[1].set_title('DC预测')

    axes[2].hist(residual.flatten(), bins=50)
    axes[2].set_title('残差直方图')
    axes[2].set_xlabel('残差值')
    axes[2].set_ylabel('频次')

    for ax in axes[:2]:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def demo():
    """运行所有演示"""
    demonstrate_intra_prediction()
    demonstrate_motion_compensation()
    demonstrate_subpixel_interpolation()
    demonstrate_residual_coding()


if __name__ == "__main__":
    demo()
