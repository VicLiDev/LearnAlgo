"""
光流算法示例：Lucas-Kanade、Horn-Schunck、Farneback
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.ndimage import gaussian_filter


def create_moving_sequence(n_frames=10, img_size=64):
    """
    创建移动序列

    Args:
        n_frames: 帧数
        img_size: 图像大小

    Returns:
        frames: 帧序列
        true_flow: 真实光流
    """
    frames = []

    # 创建带纹理的图像
    x = np.linspace(0, 4*np.pi, img_size)
    y = np.linspace(0, 4*np.pi, img_size)
    X, Y = np.meshgrid(x, y)

    # 基础图案
    base = (np.sin(X) + np.sin(Y) + 2) * 60

    # 真实运动 (向右下移动)
    true_flow = np.array([0.5, 0.3])  # (vy, vx)

    for t in range(n_frames):
        # 平移
        shift_x = t * true_flow[1]
        shift_y = t * true_flow[0]

        frame = np.zeros((img_size, img_size))
        for i in range(img_size):
            for j in range(img_size):
                src_i = i - shift_y
                src_j = j - shift_x

                # 双线性插值
                i0 = int(np.floor(src_i))
                j0 = int(np.floor(src_j))
                i1 = i0 + 1
                j1 = j0 + 1

                if i0 >= 0 and i1 < img_size and j0 >= 0 and j1 < img_size:
                    fi = src_i - i0
                    fj = src_j - j0
                    frame[i, j] = (
                        (1-fi) * (1-fj) * base[i0, j0] +
                        (1-fi) * fj * base[i0, j1] +
                        fi * (1-fj) * base[i1, j0] +
                        fi * fj * base[i1, j1]
                    )

        frames.append(frame)

    return frames, true_flow


def compute_spatial_derivatives(img):
    """计算空间导数"""
    Ix = np.zeros_like(img)
    Iy = np.zeros_like(img)

    # Sobel算子
    Ix[:, 1:-1] = (img[:, 2:] - img[:, :-2]) / 2
    Iy[1:-1, :] = (img[2:, :] - img[:-2, :]) / 2

    return Ix, Iy


def compute_temporal_derivative(img1, img2):
    """计算时间导数"""
    It = img2 - img1
    return It


def lucas_kanade(img1, img2, window_size=15):
    """
    Lucas-Kanade光流算法

    Args:
        img1, img2: 连续两帧
        window_size: 窗口大小

    Returns:
        flow_y, flow_x: 光流场
    """
    h, w = img1.shape

    # 计算导数
    Ix, Iy = compute_spatial_derivatives(img1)
    It = compute_temporal_derivative(img1, img2)

    # 初始化光流场
    flow_y = np.zeros((h, w))
    flow_x = np.zeros((h, w))

    half_window = window_size // 2

    for y in range(half_window, h - half_window):
        for x in range(half_window, w - half_window):
            # 提取窗口
            win_Ix = Ix[y-half_window:y+half_window+1, x-half_window:x+half_window+1].flatten()
            win_Iy = Iy[y-half_window:y+half_window+1, x-half_window:x+half_window+1].flatten()
            win_It = It[y-half_window:y+half_window+1, x-half_window:x+half_window+1].flatten()

            # 构建A和b矩阵
            A = np.column_stack([win_Ix, win_Iy])
            b = -win_It

            # 最小二乘求解 (A^T A) v = A^T b
            ATA = A.T @ A
            ATb = A.T @ b

            # 检查ATA是否可逆
            if np.linalg.det(ATA) > 1e-6:
                v = np.linalg.solve(ATA, ATb)
                flow_y[y, x] = v[1]
                flow_x[y, x] = v[0]

    return flow_y, flow_x


def horn_schunck(img1, img2, alpha=1.0, num_iterations=100):
    """
    Horn-Schunck光流算法

    Args:
        img1, img2: 连续两帧
        alpha: 平滑参数
        num_iterations: 迭代次数

    Returns:
        flow_y, flow_x: 光流场
    """
    h, w = img1.shape

    # 计算导数
    Ix, Iy = compute_spatial_derivatives(img1)
    It = compute_temporal_derivative(img1, img2)

    # 初始化光流场
    flow_y = np.zeros((h, w))
    flow_x = np.zeros((h, w))

    # 平均核
    avg_kernel = np.array([[0, 0.25, 0],
                          [0.25, 0, 0.25],
                          [0, 0.25, 0]])

    for _ in range(num_iterations):
        # 计算局部平均
        flow_y_avg = ndimage.convolve(flow_y, avg_kernel, mode='reflect')
        flow_x_avg = ndimage.convolve(flow_x, avg_kernel, mode='reflect')

        # 更新公式
        denominator = alpha**2 + Ix**2 + Iy**2

        flow_y = flow_y_avg - Iy * (Ix * flow_x_avg + Iy * flow_y_avg + It) / denominator
        flow_x = flow_x_avg - Ix * (Ix * flow_x_avg + Iy * flow_y_avg + It) / denominator

    return flow_y, flow_x


def farneback(img1, img2, pyr_scale=0.5, levels=3, winsize=15, iterations=3, poly_n=5, poly_sigma=1.1):
    """
    Farneback光流算法 (简化版)

    使用多项式展开来估计光流

    Args:
        img1, img2: 连续两帧
        pyr_scale: 金字塔缩放因子
        levels: 金字塔层数
        winsize: 窗口大小
        iterations: 每层迭代次数
        poly_n: 多项式展开邻域大小
        poly_sigma: 高斯标准差

    Returns:
        flow_y, flow_x: 光流场
    """
    h, w = img1.shape

    # 初始化光流
    flow_y = np.zeros((h, w))
    flow_x = np.zeros((h, w))

    # 简化实现：只使用单尺度
    # 多项式展开系数 (使用二阶多项式近似)
    def polynomial_expansion(img, poly_n, poly_sigma):
        """多项式展开"""
        # 对每个像素，用二次多项式拟合邻域
        # f(x) ~ r1 + r2*x + r3*y + r4*x^2 + r5*y^2 + r6*xy

        # 简化：使用高斯加权平均
        smoothed = gaussian_filter(img, poly_sigma)

        # 计算一阶和二阶导数
        fx = np.zeros_like(img)
        fy = np.zeros_like(img)

        fx[:, 1:-1] = (smoothed[:, 2:] - smoothed[:, :-2]) / 2
        fy[1:-1, :] = (smoothed[2:, :] - smoothed[:-2, :]) / 2

        fxx = np.zeros_like(img)
        fyy = np.zeros_like(img)
        fxy = np.zeros_like(img)

        fxx[:, 1:-1] = (smoothed[:, 2:] - 2*smoothed[:, 1:-1] + smoothed[:, :-2])
        fyy[1:-1, :] = (smoothed[2:, :] - 2*smoothed[1:-1, :] + smoothed[:-2, :])

        return fx, fy, fxx, fyy, fxy

    # 计算两帧的多项式展开
    fx1, fy1, fxx1, fyy1, fxy1 = polynomial_expansion(img1, poly_n, poly_sigma)
    fx2, fy2, fxx2, fyy2, fxy2 = polynomial_expansion(img2, poly_n, poly_sigma)

    # 基于位移估计光流 (简化)
    for iteration in range(iterations):
        # 使用当前光流估计warp第二帧
        flow_y_avg = gaussian_filter(flow_y, winsize/5)
        flow_x_avg = gaussian_filter(flow_x, winsize/5)

        # 更新光流
        delta_y = (fy2 - fy1) / (np.abs(fy2) + np.abs(fy1) + 1)
        delta_x = (fx2 - fx1) / (np.abs(fx2) + np.abs(fx1) + 1)

        flow_y = flow_y_avg + 0.5 * delta_y
        flow_x = flow_x_avg + 0.5 * delta_x

    return flow_y, flow_x


def pyramidal_lucas_kanade(img1, img2, levels=3, window_size=15):
    """
    金字塔Lucas-Kanade

    Args:
        img1, img2: 连续两帧
        levels: 金字塔层数
        window_size: 窗口大小

    Returns:
        flow_y, flow_x: 光流场
    """
    h, w = img1.shape

    # 构建高斯金字塔
    def build_pyramid(img, levels):
        pyramid = [img]
        for _ in range(levels - 1):
            # 下采样
            smoothed = gaussian_filter(pyramid[-1], sigma=1)
            downsampled = smoothed[::2, ::2]
            pyramid.append(downsampled)
        return pyramid

    pyr1 = build_pyramid(img1, levels)
    pyr2 = build_pyramid(img2, levels)

    # 从最粗层开始
    flow_y = None
    flow_x = None

    for level in range(levels - 1, -1, -1):
        current_h, current_w = pyr1[level].shape

        # 初始化或上采样光流
        if flow_y is None:
            flow_y = np.zeros((current_h, current_w))
            flow_x = np.zeros((current_h, current_w))
        else:
            # 上采样并乘以2
            flow_y = 2 * ndimage.zoom(flow_y, 2, order=1)
            flow_x = 2 * ndimage.zoom(flow_x, 2, order=1)

            # 确保尺寸匹配
            if flow_y.shape[0] != current_h or flow_y.shape[1] != current_w:
                flow_y = flow_y[:current_h, :current_w]
                flow_x = flow_x[:current_h, :current_w]

        # 在当前层计算增量光流
        delta_y, delta_x = lucas_kanade(pyr1[level], pyr2[level], window_size=max(5, window_size // (2**level)))

        # 累加光流
        flow_y += delta_y
        flow_x += delta_x

    return flow_y, flow_x


def visualize_flow(flow_y, flow_x, step=2):
    """
    可视化光流场

    Args:
        flow_y, flow_x: 光流场
        step: 显示步长

    Returns:
        可视化图像
    """
    h, w = flow_y.shape

    # 创建HSV图像
    hsv = np.zeros((h, w, 3), dtype=np.uint8)

    # 计算幅值和角度
    magnitude = np.sqrt(flow_x**2 + flow_y**2)
    angle = np.arctan2(flow_y, flow_x)

    # 归一化
    if magnitude.max() > 0:
        magnitude_norm = magnitude / magnitude.max()
    else:
        magnitude_norm = magnitude

    # HSV编码
    hsv[:, :, 0] = ((angle + np.pi) / (2 * np.pi) * 180).astype(np.uint8)  # 色调 = 方向
    hsv[:, :, 1] = 255  # 饱和度
    hsv[:, :, 2] = (magnitude_norm * 255).astype(np.uint8)  # 亮度 = 幅值

    return hsv


def plot_flow_arrows(ax, flow_y, flow_x, step=4, color='blue'):
    """在坐标轴上绘制光流箭头"""
    h, w = flow_y.shape

    for y in range(0, h, step):
        for x in range(0, w, step):
            dy = flow_y[y, x]
            dx = flow_x[y, x]

            if abs(dy) > 0.01 or abs(dx) > 0.01:
                ax.arrow(x, y, dx * 5, dy * 5, head_width=1, head_length=0.5, fc=color, ec=color, alpha=0.7)


def demonstrate_lucas_kanade():
    """演示Lucas-Kanade算法"""
    print("=" * 50)
    print("Lucas-Kanade光流")
    print("=" * 50)

    frames, true_flow = create_moving_sequence(n_frames=2, img_size=64)
    img1, img2 = frames[0], frames[1]

    # 不同窗口大小
    window_sizes = [5, 11, 21]

    fig, axes = plt.subplots(2, 4, figsize=(16, 8))

    axes[0, 0].imshow(img1, cmap='gray')
    axes[0, 0].set_title('帧1')

    axes[0, 1].imshow(img2, cmap='gray')
    axes[0, 1].set_title('帧2')

    # 差分图
    axes[0, 2].imshow(np.abs(img2 - img1), cmap='hot')
    axes[0, 2].set_title('帧差')

    for idx, win_size in enumerate(window_sizes):
        flow_y, flow_x = lucas_kanade(img1, img2, window_size=win_size)

        # 可视化
        ax = axes[0, 3] if idx == 0 else axes[1, idx - 1]

        ax.imshow(img1, cmap='gray', alpha=0.5)
        plot_flow_arrows(ax, flow_y, flow_x, step=4, color='blue')

        # 计算误差
        mean_flow_y = np.mean(flow_y[flow_y != 0])
        mean_flow_x = np.mean(flow_x[flow_x != 0])

        ax.set_title(f'LK (window={win_size})\nmean flow: ({mean_flow_y:.2f}, {mean_flow_x:.2f})')
        print(f"Window={win_size}: mean flow = ({mean_flow_y:.3f}, {mean_flow_x:.3f}), true = {true_flow}")

    # 光流颜色编码
    flow_y, flow_x = lucas_kanade(img1, img2, window_size=15)
    flow_vis = visualize_flow(flow_y, flow_x)
    axes[1, 3].imshow(flow_vis)
    axes[1, 3].set_title('光流颜色编码\n(色调=方向, 亮度=幅值)')

    for ax in axes.flat:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def demonstrate_horn_schunck():
    """演示Horn-Schunck算法"""
    print("\n" + "=" * 50)
    print("Horn-Schunck光流")
    print("=" * 50)

    frames, true_flow = create_moving_sequence(n_frames=2, img_size=64)
    img1, img2 = frames[0], frames[1]

    # 不同alpha值
    alphas = [0.5, 1.0, 2.0, 5.0]

    fig, axes = plt.subplots(2, 3, figsize=(14, 9))

    axes[0, 0].imshow(img1, cmap='gray')
    axes[0, 0].set_title('帧1')

    axes[0, 1].imshow(img2, cmap='gray')
    axes[0, 1].set_title('帧2')

    for idx, alpha in enumerate(alphas):
        flow_y, flow_x = horn_schunck(img1, img2, alpha=alpha, num_iterations=100)

        ax = axes.flat[idx + 2]

        # 光流幅值
        magnitude = np.sqrt(flow_x**2 + flow_y**2)
        im = ax.imshow(magnitude, cmap='hot')

        mean_mag = np.mean(magnitude)
        ax.set_title(f'α={alpha}\nmean magnitude={mean_mag:.3f}')

        print(f"α={alpha}: mean magnitude = {mean_mag:.3f}")

    # 最后一个子图显示颜色编码
    flow_y, flow_x = horn_schunck(img1, img2, alpha=1.0, num_iterations=100)
    flow_vis = visualize_flow(flow_y, flow_x)
    axes[1, 2].imshow(flow_vis)
    axes[1, 2].set_title('光流颜色编码')

    for ax in axes.flat:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def demonstrate_pyramidal():
    """演示金字塔方法"""
    print("\n" + "=" * 50)
    print("金字塔Lucas-Kanade")
    print("=" * 50)

    frames, true_flow = create_moving_sequence(n_frames=2, img_size=64)
    img1, img2 = frames[0], frames[1]

    # 单尺度 vs 多尺度
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))

    # 单尺度LK
    flow_y_single, flow_x_single = lucas_kanade(img1, img2, window_size=15)

    axes[0, 0].imshow(img1, cmap='gray', alpha=0.5)
    plot_flow_arrows(axes[0, 0], flow_y_single, flow_x_single, step=4)
    axes[0, 0].set_title('单尺度 LK')

    # 多尺度LK
    for level in range(1, 4):
        flow_y_pyramid, flow_x_pyramid = pyramidal_lucas_kanade(img1, img2, levels=level, window_size=15)

        ax = axes.flat[level]

        ax.imshow(img1, cmap='gray', alpha=0.5)
        plot_flow_arrows(ax, flow_y_pyramid, flow_x_pyramid, step=4)

        mean_flow = np.sqrt(np.mean(flow_x_pyramid**2 + flow_y_pyramid**2))
        ax.set_title(f'金字塔 LK (levels={level})\nmean mag={mean_flow:.3f}')

        print(f"Levels={level}: mean magnitude = {mean_flow:.3f}")

    # 比较光流分布
    axes[1, 3].hist(flow_y_single.flatten(), bins=30, alpha=0.5, label='单尺度')
    flow_y_pyr, _ = pyramidal_lucas_kanade(img1, img2, levels=3, window_size=15)
    axes[1, 3].hist(flow_y_pyr.flatten(), bins=30, alpha=0.5, label='金字塔')
    axes[1, 3].set_xlabel('光流值 (y方向)')
    axes[1, 3].set_ylabel('频次')
    axes[1, 3].legend()
    axes[1, 3].set_title('光流分布比较')

    for ax in axes[:1, :].flat:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def demonstrate_flow_quality():
    """演示光流质量评估"""
    print("\n" + "=" * 50)
    print("光流质量评估")
    print("=" * 50)

    frames, true_flow = create_moving_sequence(n_frames=2, img_size=64)
    img1, img2 = frames[0], frames[1]

    print(f"真实光流: vy={true_flow[0]:.3f}, vx={true_flow[1]:.3f}")

    # 不同算法
    algorithms = {
        'Lucas-Kanade': lambda: lucas_kanade(img1, img2, window_size=15),
        'Horn-Schunck': lambda: horn_schunck(img1, img2, alpha=1.0, num_iterations=100),
        'Pyramidal LK': lambda: pyramidal_lucas_kanade(img1, img2, levels=3, window_size=15),
    }

    fig, axes = plt.subplots(2, 4, figsize=(16, 8))

    axes[0, 0].imshow(img1, cmap='gray')
    axes[0, 0].set_title('帧1')

    axes[0, 1].imshow(img2, cmap='gray')
    axes[0, 1].set_title('帧2')

    results = []

    for idx, (name, algo) in enumerate(algorithms.items()):
        flow_y, flow_x = algo()

        # 过滤零值
        mask = (flow_x != 0) | (flow_y != 0)

        mean_vy = np.mean(flow_y[mask]) if mask.any() else 0
        mean_vx = np.mean(flow_x[mask]) if mask.any() else 0

        # 端点误差
        if mask.any():
            epe = np.mean(np.sqrt((flow_y[mask] - true_flow[0])**2 +
                                   (flow_x[mask] - true_flow[1])**2))
        else:
            epe = float('inf')

        results.append({
            'name': name,
            'mean_vy': mean_vy,
            'mean_vx': mean_vx,
            'epe': epe
        })

        print(f"{name}: vy={mean_vy:.3f}, vx={mean_vx:.3f}, EPE={epe:.3f}")

        # 可视化
        ax = axes[0, idx + 2] if idx < 2 else axes[1, idx - 2]

        ax.imshow(img1, cmap='gray', alpha=0.5)
        plot_flow_arrows(ax, flow_y, flow_x, step=4)
        ax.set_title(f'{name}\nEPE={epe:.3f}')

    # 比较柱状图
    names = [r['name'] for r in results]
    epes = [r['epe'] for r in results]

    axes[1, 2].bar(names, epes)
    axes[1, 2].set_ylabel('端点误差 (EPE)')
    axes[1, 2].set_title('算法比较')
    axes[1, 2].tick_params(axis='x', rotation=15)

    axes[1, 3].axis('off')

    for ax in axes[0, :].flat:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def demo():
    """运行所有演示"""
    demonstrate_lucas_kanade()
    demonstrate_horn_schunck()
    demonstrate_pyramidal()
    demonstrate_flow_quality()


if __name__ == "__main__":
    demo()
