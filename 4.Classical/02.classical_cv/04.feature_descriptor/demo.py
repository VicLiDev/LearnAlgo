"""
特征描述子示例：HOG、LBP、SIFT描述子
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.ndimage import gaussian_filter


def create_test_image():
    """创建测试图像"""
    img = np.zeros((128, 64), dtype=np.float64)

    # 添加边缘和区域
    img[20:60, 10:30] = 100
    img[20:60, 34:54] = 200
    img[70:110, 10:54] = 150

    # 添加噪声
    img += np.random.randn(128, 64) * 10

    return np.clip(img, 0, 255)


def compute_gradients(img):
    """计算图像梯度"""
    gx = np.zeros_like(img)
    gy = np.zeros_like(img)

    gx[:, 1:-1] = img[:, 2:] - img[:, :-2]
    gy[1:-1, :] = img[2:, :] - img[:-2, :]

    magnitude = np.sqrt(gx**2 + gy**2)
    orientation = np.arctan2(gy, gx) * 180 / np.pi  # 转换为度
    orientation[orientation < 0] += 180  # 0-180度

    return magnitude, orientation


def compute_hog_descriptor(img, cell_size=8, block_size=2, nbins=9):
    """
    计算HOG描述子

    Args:
        img: 输入图像 (h, w)
        cell_size: cell大小
        block_size: block大小 (cells)
        nbins: 方向bin数

    Returns:
        hog_descriptor: HOG描述子
        hog_image: HOG可视化
    """
    h, w = img.shape

    # 计算梯度
    magnitude, orientation = compute_gradients(img)

    # 计算cell直方图
    n_cells_y = h // cell_size
    n_cells_x = w // cell_size

    # 初始化cell直方图
    cell_histograms = np.zeros((n_cells_y, n_cells_x, nbins))

    bin_width = 180 / nbins

    for cy in range(n_cells_y):
        for cx in range(n_cells_x):
            # 提取cell区域
            y_start = cy * cell_size
            x_start = cx * cell_size
            cell_mag = magnitude[y_start:y_start+cell_size, x_start:x_start+cell_size]
            cell_ori = orientation[y_start:y_start+cell_size, x_start:x_start+cell_size]

            # 双线性插值到bin
            for y in range(cell_size):
                for x in range(cell_size):
                    mag = cell_mag[y, x]
                    ori = cell_ori[y, x]

                    bin_idx = ori / bin_width
                    bin_low = int(bin_idx) % nbins
                    bin_high = (bin_low + 1) % nbins

                    # 线性插值权重
                    weight_high = bin_idx - int(bin_idx)
                    weight_low = 1 - weight_high

                    cell_histograms[cy, cx, bin_low] += mag * weight_low
                    cell_histograms[cy, cx, bin_high] += mag * weight_high

    # Block归一化
    n_blocks_y = n_cells_y - block_size + 1
    n_blocks_x = n_cells_x - block_size + 1

    hog_descriptor = []

    for by in range(n_blocks_y):
        for bx in range(n_blocks_x):
            # 提取block
            block = cell_histograms[by:by+block_size, bx:bx+block_size, :].flatten()

            # L2归一化
            norm = np.sqrt(np.sum(block**2) + 1e-6)
            block_normalized = block / norm

            hog_descriptor.extend(block_normalized)

    # 创建HOG可视化
    hog_image = np.zeros_like(img)
    for cy in range(n_cells_y):
        for cx in range(n_cells_x):
            y_center = cy * cell_size + cell_size // 2
            x_center = cx * cell_size + cell_size // 2

            for bin_idx in range(nbins):
                angle = (bin_idx + 0.5) * bin_width
                magnitude = cell_histograms[cy, cx, bin_idx]

                # 画方向线
                dx = magnitude * np.cos(np.radians(angle)) * 3
                dy = magnitude * np.sin(np.radians(angle)) * 3

                y1 = int(y_center - dy)
                x1 = int(x_center - dx)
                y2 = int(y_center + dy)
                x2 = int(x_center + dx)

                # 简单的线绘制
                for t in np.linspace(0, 1, 10):
                    y = int(y1 + t * (y2 - y1))
                    x = int(x1 + t * (x2 - x1))
                    if 0 <= y < h and 0 <= x < w:
                        hog_image[y, x] = min(255, hog_image[y, x] + magnitude)

    return np.array(hog_descriptor), hog_image


def compute_lbp_descriptor(img, radius=1, n_points=8):
    """
    计算LBP描述子

    Args:
        img: 输入图像
        radius: 邻域半径
        n_points: 邻域点数

    Returns:
        lbp_image: LBP图像
        histogram: LBP直方图
    """
    h, w = img.shape
    lbp = np.zeros((h, w), dtype=np.uint8)

    # 计算采样点位置
    angles = 2 * np.pi * np.arange(n_points) / n_points
    sample_points = np.column_stack([
        radius * np.sin(angles),
        radius * np.cos(angles)
    ])

    # 对每个像素计算LBP
    for y in range(radius, h - radius):
        for x in range(radius, w - radius):
            center = img[y, x]
            lbp_val = 0

            for i, (dy, dx) in enumerate(sample_points):
                # 双线性插值
                y_sample = y + dy
                x_sample = x + dx

                y0, x0 = int(y_sample), int(x_sample)
                y1, x1 = y0 + 1, x0 + 1

                if y1 >= h or x1 >= w:
                    continue

                fy = y_sample - y0
                fx = x_sample - x0

                interpolated = (
                    (1 - fy) * (1 - fx) * img[y0, x0] +
                    (1 - fy) * fx * img[y0, x1] +
                    fy * (1 - fx) * img[y1, x0] +
                    fy * fx * img[y1, x1]
                )

                if interpolated >= center:
                    lbp_val |= (1 << i)

            lbp[y, x] = lbp_val

    # 计算直方图
    histogram, _ = np.histogram(lbp.ravel(), bins=256, range=(0, 256))

    return lbp, histogram


def compute_uniform_lbp(img, radius=1, n_points=8):
    """
    计算Uniform LBP

    Uniform LBP: 0-1跳变次数不超过2的模式

    Args:
        img: 输入图像
        radius: 邻域半径
        n_points: 邻域点数

    Returns:
        lbp_image: Uniform LBP图像
        histogram: 直方图 (n_points*(n_points-1)+3 维)
    """
    h, w = img.shape

    # 计算uniform模式的映射
    def count_transitions(pattern):
        """计算0-1跳变次数"""
        binary = bin(pattern)[2:].zfill(n_points)
        transitions = 0
        for i in range(len(binary)):
            if binary[i] != binary[(i + 1) % len(binary)]:
                transitions += 1
        return transitions

    # 构建映射表
    uniform_map = {}
    uniform_idx = 0

    for pattern in range(256):
        if n_points == 8 and count_transitions(pattern) <= 2:
            uniform_map[pattern] = uniform_idx
            uniform_idx += 1
        elif n_points != 8:
            # 通用情况
            if count_transitions(pattern) <= 2:
                uniform_map[pattern] = uniform_idx
                uniform_idx += 1

    # 计算LBP
    lbp, _ = compute_lbp_descriptor(img, radius, n_points)

    # 映射到uniform值
    n_uniform = n_points * (n_points - 1) + 3
    uniform_lbp = np.zeros_like(lbp)

    for y in range(h):
        for x in range(w):
            pattern = lbp[y, x]
            if pattern in uniform_map:
                uniform_lbp[y, x] = uniform_map[pattern]
            else:
                uniform_lbp[y, x] = n_uniform - 1  # 非uniform模式

    # 直方图
    histogram, _ = np.histogram(uniform_lbp.ravel(), bins=n_uniform, range=(0, n_uniform))

    return uniform_lbp, histogram


def compute_sift_descriptor(img, keypoint_y, keypoint_x, scale=1.0):
    """
    计算简化的SIFT描述子

    Args:
        img: 输入图像
        keypoint_y, keypoint_x: 关键点位置
        scale: 尺度

    Returns:
        descriptor: 128维描述子
    """
    # 描述子窗口大小
    window_size = 16

    # 计算梯度
    magnitude, orientation = compute_gradients(img)

    # 以关键点为中心的窗口
    half_size = window_size // 2

    y_start = max(0, int(keypoint_y - half_size))
    y_end = min(img.shape[0], int(keypoint_y + half_size))
    x_start = max(0, int(keypoint_x - half_size))
    x_end = min(img.shape[1], int(keypoint_x + half_size))

    if y_end - y_start < window_size or x_end - x_start < window_size:
        return np.zeros(128)

    # 提取窗口
    window_mag = magnitude[y_start:y_end, x_start:x_end]
    window_ori = orientation[y_start:y_end, x_start:x_end]

    # 计算主方向 (简化)
    hist, _ = np.histogram(window_ori.ravel(), bins=36, range=(0, 180), weights=window_mag.ravel())
    dominant_orientation = np.argmax(hist) * 5  # 主方向

    # 旋转到主方向
    window_ori = (window_ori - dominant_orientation) % 180

    # 分成4x4子区域
    subregion_size = 4
    descriptor = []

    for i in range(4):
        for j in range(4):
            # 提取子区域
            y_s = i * subregion_size
            x_s = j * subregion_size
            sub_mag = window_mag[y_s:y_s+subregion_size, x_s:x_s+subregion_size]
            sub_ori = window_ori[y_s:y_s+subregion_size, x_s:x_s+subregion_size]

            # 8方向直方图
            hist, _ = np.histogram(sub_ori.ravel(), bins=8, range=(0, 180), weights=sub_mag.ravel())
            descriptor.extend(hist)

    # 归一化
    descriptor = np.array(descriptor)
    norm = np.sqrt(np.sum(descriptor**2) + 1e-6)
    descriptor = descriptor / norm

    # 阈值截断
    descriptor = np.clip(descriptor, 0, 0.2)

    # 再次归一化
    norm = np.sqrt(np.sum(descriptor**2) + 1e-6)
    descriptor = descriptor / norm

    return descriptor


def demonstrate_hog():
    """演示HOG描述子"""
    print("=" * 50)
    print("HOG (Histogram of Oriented Gradients)")
    print("=" * 50)

    img = create_test_image()

    # 计算HOG
    descriptor, hog_image = compute_hog_descriptor(img, cell_size=8, block_size=2, nbins=9)

    print(f"HOG描述子维度: {descriptor.shape[0]}")
    print(f"描述子范围: [{descriptor.min():.3f}, {descriptor.max():.3f}]")

    # 可视化
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))

    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('原始图像')

    # 梯度幅值
    mag, ori = compute_gradients(img)
    axes[0, 1].imshow(mag, cmap='hot')
    axes[0, 1].set_title('梯度幅值')

    # 梯度方向
    axes[0, 2].imshow(ori, cmap='hsv')
    axes[0, 2].set_title('梯度方向')

    # HOG可视化
    axes[1, 0].imshow(hog_image, cmap='gray')
    axes[1, 0].set_title('HOG可视化')

    # 描述子前100维
    axes[1, 1].bar(range(100), descriptor[:100])
    axes[1, 1].set_xlabel('维度')
    axes[1, 1].set_ylabel('值')
    axes[1, 1].set_title('描述子 (前100维)')

    # 描述子直方图
    axes[1, 2].hist(descriptor, bins=30)
    axes[1, 2].set_xlabel('值')
    axes[1, 2].set_ylabel('频次')
    axes[1, 2].set_title('描述子分布')

    for ax in axes[:1, :].flat:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def demonstrate_lbp():
    """演示LBP描述子"""
    print("\n" + "=" * 50)
    print("LBP (Local Binary Pattern)")
    print("=" * 50)

    img = create_test_image()

    # 不同半径的LBP
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))

    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('原始图像')

    # 基本LBP
    lbp, hist = compute_lbp_descriptor(img, radius=1, n_points=8)
    axes[0, 1].imshow(lbp, cmap='gray')
    axes[0, 1].set_title('LBP (r=1, p=8)')

    axes[1, 0].bar(range(256), hist)
    axes[1, 0].set_xlabel('LBP值')
    axes[1, 0].set_ylabel('频次')
    axes[1, 0].set_title('LBP直方图')

    # Uniform LBP
    uniform_lbp, uniform_hist = compute_uniform_lbp(img, radius=1, n_points=8)
    axes[0, 2].imshow(uniform_lbp, cmap='gray')
    axes[0, 2].set_title('Uniform LBP')

    axes[1, 1].bar(range(len(uniform_hist)), uniform_hist)
    axes[1, 1].set_xlabel('Uniform LBP值')
    axes[1, 1].set_ylabel('频次')
    axes[1, 1].set_title('Uniform LBP直方图 (59 bins)')

    # 更大半径
    lbp2, hist2 = compute_lbp_descriptor(img, radius=2, n_points=8)
    axes[0, 3].imshow(lbp2, cmap='gray')
    axes[0, 3].set_title('LBP (r=2, p=8)')

    axes[1, 2].bar(range(256), hist2)
    axes[1, 2].set_xlabel('LBP值')
    axes[1, 2].set_ylabel('频次')
    axes[1, 2].set_title('LBP直方图 (r=2)')

    # 比较不同参数
    print(f"LBP (r=1) 非零模式数: {np.count_nonzero(hist)}")
    print(f"Uniform LBP 非零模式数: {np.count_nonzero(uniform_hist)}")
    print(f"LBP (r=2) 非零模式数: {np.count_nonzero(hist2)}")

    # 隐藏最后一个子图
    axes[1, 3].axis('off')

    for ax in axes[0, :].flat:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def demonstrate_sift_descriptor():
    """演示SIFT描述子"""
    print("\n" + "=" * 50)
    print("SIFT描述子")
    print("=" * 50)

    img = create_test_image()

    # 在几个关键点计算描述子
    keypoints = [
        (40, 20),  # 第一个块中心
        (40, 44),  # 第二个块中心
        (90, 32),  # 第三个块中心
    ]

    descriptors = []
    for y, x in keypoints:
        desc = compute_sift_descriptor(img, y, x)
        descriptors.append(desc)

    # 可视化
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))

    axes[0, 0].imshow(img, cmap='gray')

    # 标记关键点
    for i, (y, x) in enumerate(keypoints):
        circle = plt.Circle((x, y), 8, color='red', fill=False, linewidth=2)
        axes[0, 0].add_patch(circle)
        axes[0, 0].annotate(f'KP{i+1}', (x, y-15), color='red', fontsize=10)

    axes[0, 0].set_title('关键点位置')

    # 显示每个描述子
    for i, desc in enumerate(descriptors):
        # 4x4x8 = 128维的网格可视化
        desc_grid = desc.reshape(4, 4, 8)

        # 求和得到4x4的热图
        ax = axes[0, i + 1]
        im = ax.imshow(desc_grid.sum(axis=2), cmap='hot')
        ax.set_title(f'KP{i+1} 描述子强度')
        plt.colorbar(im, ax=ax)

        # 直方图
        ax = axes[1, i]
        ax.bar(range(128), desc, width=1)
        ax.set_xlabel('维度')
        ax.set_ylabel('值')
        ax.set_title(f'KP{i+1} 128维描述子')

    axes[1, 3].axis('off')

    plt.tight_layout()
    plt.show()


def demonstrate_descriptor_comparison():
    """对比不同描述子"""
    print("\n" + "=" * 50)
    print("描述子对比")
    print("=" * 50)

    img = create_test_image()

    # 计算各种描述子
    hog_desc, _ = compute_hog_descriptor(img)
    _, lbp_hist = compute_lbp_descriptor(img)
    _, uniform_lbp_hist = compute_uniform_lbp(img)
    sift_desc = compute_sift_descriptor(img, 64, 32)

    # 比较维度和计算复杂度
    print("\n描述子对比:")
    print(f"HOG:         维度={len(hog_desc)}, 范围=[{hog_desc.min():.3f}, {hog_desc.max():.3f}]")
    print(f"LBP:         维度={len(lbp_hist)}, 非零bin={np.count_nonzero(lbp_hist)}")
    print(f"Uniform LBP: 维度={len(uniform_lbp_hist)}, 非零bin={np.count_nonzero(uniform_lbp_hist)}")
    print(f"SIFT:        维度={len(sift_desc)}, 范围=[{sift_desc.min():.3f}, {sift_desc.max():.3f}]")

    # 可视化
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))

    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('原始图像')

    # HOG
    axes[0, 1].bar(range(min(100, len(hog_desc))), hog_desc[:100])
    axes[0, 1].set_title(f'HOG ({len(hog_desc)} dim)')

    # LBP
    axes[0, 2].bar(range(len(lbp_hist)), lbp_hist)
    axes[0, 2].set_title(f'LBP ({len(lbp_hist)} bins)')

    # Uniform LBP
    axes[0, 3].bar(range(len(uniform_lbp_hist)), uniform_lbp_hist)
    axes[0, 3].set_title(f'Uniform LBP ({len(uniform_lbp_hist)} bins)')

    # SIFT
    axes[1, 0].bar(range(len(sift_desc)), sift_desc)
    axes[1, 0].set_title(f'SIFT ({len(sift_desc)} dim)')

    # 归一化后的比较
    all_norm = lambda x: x / (np.linalg.norm(x) + 1e-6)

    # 描述子能量分布
    axes[1, 1].plot(np.cumsum(sorted(hog_desc, reverse=True)) / np.sum(hog_desc), label='HOG')
    axes[1, 1].plot(np.cumsum(sorted(lbp_hist.astype(float), reverse=True)) / np.sum(lbp_hist), label='LBP')
    axes[1, 1].plot(np.cumsum(sorted(sift_desc, reverse=True)) / np.sum(sift_desc), label='SIFT')
    axes[1, 1].set_xlabel('维度索引')
    axes[1, 1].set_ylabel('累积能量')
    axes[1, 1].set_title('描述子能量分布')
    axes[1, 1].legend()

    # 隐藏空子图
    axes[1, 2].axis('off')
    axes[1, 3].axis('off')

    plt.tight_layout()
    plt.show()


def demo():
    """运行所有演示"""
    demonstrate_hog()
    demonstrate_lbp()
    demonstrate_sift_descriptor()
    demonstrate_descriptor_comparison()


if __name__ == "__main__":
    demo()
