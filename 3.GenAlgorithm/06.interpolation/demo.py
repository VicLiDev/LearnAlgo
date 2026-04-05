"""
插值算法示例：线性插值、双线性插值、三次样条
"""
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from PIL import Image


def linear_interpolation_1d(x, y, x_new):
    """
    一维线性插值

    Args:
        x: 已知点的x坐标
        y: 已知点的y坐标
        x_new: 需要插值的x坐标

    Returns:
        y_new: 插值结果
    """
    y_new = np.zeros_like(x_new)

    for i, xi in enumerate(x_new):
        # 找到区间
        idx = np.searchsorted(x, xi) - 1
        idx = max(0, min(idx, len(x) - 2))

        # 线性插值
        t = (xi - x[idx]) / (x[idx + 1] - x[idx])
        y_new[i] = y[idx] + t * (y[idx + 1] - y[idx])

    return y_new


def bilinear_interpolation(image, new_size):
    """
    双线性插值缩放图像

    Args:
        image: 输入图像 (H, W) 或 (H, W, C)
        new_size: 目标大小 (new_H, new_W)

    Returns:
        缩放后的图像
    """
    if len(image.shape) == 2:
        image = image[:, :, np.newaxis]

    h, w, c = image.shape
    new_h, new_w = new_size

    # 创建坐标网格
    y_new = np.linspace(0, h - 1, new_h)
    x_new = np.linspace(0, w - 1, new_w)

    result = np.zeros((new_h, new_w, c))

    for i, y in enumerate(y_new):
        for j, x in enumerate(x_new):
            # 找到四个邻近点
            y0, x0 = int(y), int(x)
            y1, x1 = min(y0 + 1, h - 1), min(x0 + 1, w - 1)

            # 计算权重
            wy = y - y0
            wx = x - x0

            # 双线性插值
            for k in range(c):
                result[i, j, k] = (
                    (1 - wx) * (1 - wy) * image[y0, x0, k] +
                    wx * (1 - wy) * image[y0, x1, k] +
                    (1 - wx) * wy * image[y1, x0, k] +
                    wx * wy * image[y1, x1, k]
                )

    return result.squeeze() if c == 1 else result.astype(image.dtype)


def cubic_spline_interpolation(x, y, x_new):
    """
    三次样条插值

    Args:
        x: 已知点的x坐标
        y: 已知点的y坐标
        x_new: 需要插值的x坐标

    Returns:
        y_new: 插值结果
    """
    # 使用scipy的三次样条
    cs = interpolate.CubicSpline(x, y)
    return cs(x_new)


def demonstrate_1d_interpolation():
    """演示一维插值方法"""
    print("=" * 50)
    print("一维插值方法比较")
    print("=" * 50)

    # 已知数据点
    x = np.array([0, 1, 2, 3, 4, 5, 6])
    y = np.array([0, 0.8, 0.9, 0.1, -0.8, -1.0, 0])

    # 插值点
    x_new = np.linspace(0, 6, 100)

    # 各种插值方法
    y_linear = linear_interpolation_1d(x, y, x_new)
    y_cubic = cubic_spline_interpolation(x, y, x_new)

    # 可视化
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 线性插值
    axes[0].scatter(x, y, c='red', s=100, zorder=5, label='原始数据点')
    axes[0].plot(x_new, y_linear, 'b-', linewidth=2, label='线性插值')
    axes[0].set_xlabel('x')
    axes[0].set_ylabel('y')
    axes[0].set_title('线性插值')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # 三次样条
    axes[1].scatter(x, y, c='red', s=100, zorder=5, label='原始数据点')
    axes[1].plot(x_new, y_cubic, 'g-', linewidth=2, label='三次样条')
    axes[1].set_xlabel('x')
    axes[1].set_ylabel('y')
    axes[1].set_title('三次样条插值')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def demonstrate_image_interpolation():
    """演示图像插值"""
    print("\n" + "=" * 50)
    print("图像插值方法比较")
    print("=" * 50)

    # 创建测试图像
    size = 32
    image = np.zeros((size, size), dtype=np.uint8)
    # 添加一些内容
    image[8:24, 8:24] = 200
    image[12:20, 12:20] = 50

    # 目标大小
    new_size = (128, 128)

    # 最近邻插值 (使用PIL)
    img_pil = Image.fromarray(image)
    img_nearest = np.array(img_pil.resize(new_size, Image.NEAREST))

    # 双线性插值
    img_bilinear = bilinear_interpolation(image.astype(float), new_size)
    img_bilinear = np.clip(img_bilinear, 0, 255).astype(np.uint8)

    # 双三次插值 (使用PIL)
    img_bicubic = np.array(img_pil.resize(new_size, Image.BICUBIC))

    # 可视化
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))

    axes[0, 0].imshow(image, cmap='gray', vmin=0, vmax=255)
    axes[0, 0].set_title(f'原图 ({size}×{size})')

    axes[0, 1].imshow(img_nearest, cmap='gray', vmin=0, vmax=255)
    axes[0, 1].set_title('最近邻插值')

    axes[1, 0].imshow(img_bilinear, cmap='gray', vmin=0, vmax=255)
    axes[1, 0].set_title('双线性插值')

    axes[1, 1].imshow(img_bicubic, cmap='gray', vmin=0, vmax=255)
    axes[1, 1].set_title('双三次插值')

    for ax in axes.flat:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def demonstrate_spline_smoothness():
    """演示样条插值的平滑性"""
    print("\n" + "=" * 50)
    print("样条插值平滑性演示")
    print("=" * 50)

    # 少量数据点
    x = np.array([0, 2, 4, 6, 8, 10])
    y = np.array([0, 1, -1, 2, -0.5, 1])

    # 插值点
    x_new = np.linspace(0, 10, 200)

    # 不同阶数的样条
    y_linear = linear_interpolation_1d(x, y, x_new)
    y_cubic = cubic_spline_interpolation(x, y, x_new)

    # 计算导数（用于展示平滑性）
    cs = interpolate.CubicSpline(x, y)
    y_first_deriv = cs(x_new, 1)  # 一阶导数
    y_second_deriv = cs(x_new, 2)  # 二阶导数

    fig, axes = plt.subplots(3, 1, figsize=(12, 10))

    # 函数值
    axes[0].scatter(x, y, c='red', s=100, zorder=5, label='数据点')
    axes[0].plot(x_new, y_linear, 'b--', linewidth=1.5, label='线性插值')
    axes[0].plot(x_new, y_cubic, 'g-', linewidth=2, label='三次样条')
    axes[0].set_ylabel('f(x)')
    axes[0].set_title('插值函数')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # 一阶导数
    axes[1].plot(x_new, y_first_deriv, 'g-', linewidth=2)
    axes[1].set_ylabel("f'(x)")
    axes[1].set_title('一阶导数 (三次样条)')
    axes[1].grid(True, alpha=0.3)

    # 二阶导数
    axes[2].plot(x_new, y_second_deriv, 'g-', linewidth=2)
    axes[2].set_xlabel('x')
    axes[2].set_ylabel("f''(x)")
    axes[2].set_title('二阶导数 (三次样条 - 连续)')
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def demonstrate_downsampling_artifacts():
    """演示降采样混叠效应"""
    print("\n" + "=" * 50)
    print("降采样混叠效应演示")
    print("=" * 50)

    # 创建高频图案
    x = np.linspace(0, 4 * np.pi, 256)
    y = np.sin(8 * x) + 0.5 * np.sin(32 * x)

    # 不带抗混叠滤波的降采样
    y_downsampled_no_filter = y[::4]

    # 带低通滤波的降采样（简化版）
    from scipy.ndimage import gaussian_filter1d
    y_filtered = gaussian_filter1d(y, sigma=2)
    y_downsampled_filtered = y_filtered[::4]

    # 可视化
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))

    # 原始信号
    axes[0, 0].plot(x, y)
    axes[0, 0].set_title('原始信号 (256点)')
    axes[0, 0].set_xlabel('x')
    axes[0, 0].set_ylabel('y')

    # 滤波后信号
    axes[0, 1].plot(x, y_filtered)
    axes[0, 1].set_title('低通滤波后 (σ=2)')
    axes[0, 1].set_xlabel('x')
    axes[0, 1].set_ylabel('y')

    # 直接降采样
    x_down = x[::4]
    axes[1, 0].plot(x_down, y_downsampled_no_filter, 'o-')
    axes[1, 0].set_title('直接降采样 (64点) - 可能有混叠')
    axes[1, 0].set_xlabel('x')
    axes[1, 0].set_ylabel('y')

    # 滤波后降采样
    axes[1, 1].plot(x_down, y_downsampled_filtered, 'o-')
    axes[1, 1].set_title('滤波后降采样 (64点) - 抗混叠')
    axes[1, 1].set_xlabel('x')
    axes[1, 1].set_ylabel('y')

    for ax in axes.flat:
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def demo():
    """运行所有演示"""
    demonstrate_1d_interpolation()
    demonstrate_image_interpolation()
    demonstrate_spline_smoothness()
    demonstrate_downsampling_artifacts()


if __name__ == "__main__":
    demo()
