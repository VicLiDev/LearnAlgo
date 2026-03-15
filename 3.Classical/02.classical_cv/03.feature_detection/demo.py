"""
特征检测示例：SIFT、SURF、ORB、Harris
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.ndimage import gaussian_filter


def create_test_image():
    """创建测试图像"""
    img = np.zeros((200, 200), dtype=np.float64)

    # 添加一些几何形状
    # 矩形
    img[30:70, 30:70] = 200
    # 圆形
    y, x = np.ogrid[:200, :200]
    mask = (x - 130)**2 + (y - 50)**2 <= 30**2
    img[mask] = 150
    # 三角形
    for i in range(40):
        img[100+i, 50+i:150-i] = 100

    # 添加噪声
    img += np.random.randn(200, 200) * 10

    return np.clip(img, 0, 255)


def gaussian_kernel(size, sigma):
    """生成高斯核"""
    x = np.arange(size) - (size - 1) / 2
    kernel_1d = np.exp(-x**2 / (2 * sigma**2))
    kernel_2d = np.outer(kernel_1d, kernel_1d)
    return kernel_2d / kernel_2d.sum()


def build_gaussian_pyramid(img, num_octaves=4, num_scales=5, sigma=1.6):
    """
    构建高斯金字塔

    Args:
        img: 输入图像
        num_octaves: 八度数量
        num_scales: 每个八度的尺度数
        sigma: 基础sigma

    Returns:
        金字塔列表
    """
    pyramid = []

    for octave in range(num_octaves):
        octave_images = []
        current_img = img if octave == 0 else ndimage.zoom(img, 0.5**octave)

        for scale in range(num_scales):
            k = 2 ** (scale / (num_scales - 1))
            blurred = gaussian_filter(current_img, sigma * k)
            octave_images.append(blurred)

        pyramid.append(octave_images)

    return pyramid


def compute_dog_pyramid(gaussian_pyramid):
    """
    计算DoG金字塔

    Args:
        gaussian_pyramid: 高斯金字塔

    Returns:
        DoG金字塔
    """
    dog_pyramid = []

    for octave in gaussian_pyramid:
        dog_octave = []
        for i in range(len(octave) - 1):
            dog = octave[i + 1] - octave[i]
            dog_octave.append(dog)
        dog_pyramid.append(dog_octave)

    return dog_pyramid


def find_keypoints_in_dog(dog_pyramid, contrast_threshold=0.03):
    """
    在DoG金字塔中检测关键点 (简化版)

    Args:
        dog_pyramid: DoG金字塔
        contrast_threshold: 对比度阈值

    Returns:
        关键点列表 [(octave, scale, y, x), ...]
    """
    keypoints = []

    for octave_idx, dog_octave in enumerate(dog_pyramid):
        for scale_idx in range(1, len(dog_octave) - 1):
            dog = dog_octave[scale_idx]
            dog_prev = dog_octave[scale_idx - 1]
            dog_next = dog_octave[scale_idx + 1]

            h, w = dog.shape

            # 检查是否为局部极值
            for y in range(1, h - 1):
                for x in range(1, w - 1):
                    val = dog[y, x]

                    # 对比度检查
                    if abs(val) < contrast_threshold * 255:
                        continue

                    # 检查26个邻域点
                    is_extremum = True

                    # 当前尺度的8个邻域
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dy == 0 and dx == 0:
                                continue
                            if val > 0 and dog[y + dy, x + dx] >= val:
                                is_extremum = False
                            if val < 0 and dog[y + dy, x + dx] <= val:
                                is_extremum = False

                    if not is_extremum:
                        continue

                    # 上下尺度的18个邻域
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if val > 0:
                                if dog_prev[y + dy, x + dx] >= val or dog_next[y + dy, x + dx] >= val:
                                    is_extremum = False
                            if val < 0:
                                if dog_prev[y + dy, x + dx] <= val or dog_next[y + dy, x + dx] <= val:
                                    is_extremum = False

                    if is_extremum:
                        keypoints.append((octave_idx, scale_idx, y, x))

    return keypoints


def compute_gradients(img):
    """计算图像梯度"""
    gx = np.zeros_like(img)
    gy = np.zeros_like(img)

    gx[:, 1:-1] = img[:, 2:] - img[:, :-2]
    gy[1:-1, :] = img[2:, :] - img[:-2, :]

    magnitude = np.sqrt(gx**2 + gy**2)
    orientation = np.arctan2(gy, gx)

    return magnitude, orientation


def detect_harris_corners(img, k=0.04, threshold_ratio=0.01):
    """
    Harris角点检测

    Args:
        img: 输入图像
        k: Harris参数
        threshold_ratio: 阈值比例

    Returns:
        角点响应图和角点坐标
    """
    # 计算梯度
    gx = np.zeros_like(img)
    gy = np.zeros_like(img)

    gx[:, 1:-1] = img[:, 2:] - img[:, :-2]
    gy[1:-1, :] = img[2:, :] - img[:-2, :]

    # 计算M矩阵分量
    Ixx = gaussian_filter(gx * gx, sigma=1)
    Iyy = gaussian_filter(gy * gy, sigma=1)
    Ixy = gaussian_filter(gx * gy, sigma=1)

    # Harris响应
    det_M = Ixx * Iyy - Ixy * Ixy
    trace_M = Ixx + Iyy

    R = det_M - k * trace_M**2

    # 非极大值抑制
    local_max = ndimage.maximum_filter(R, size=5)
    corners_mask = (R == local_max) & (R > threshold_ratio * R.max())

    corners = np.argwhere(corners_mask)

    return R, corners


def detect_fast_corners(img, threshold=20):
    """
    FAST角点检测 (简化版)

    Args:
        img: 输入图像
        threshold: 强度阈值

    Returns:
        角点坐标
    """
    h, w = img.shape
    corners = []

    # Bresenham圆上的16个点
    circle = [
        (0, -3), (1, -3), (2, -2), (3, -1), (3, 0), (3, 1), (2, 2), (1, 3),
        (0, 3), (-1, 3), (-2, 2), (-3, 1), (-3, 0), (-3, -1), (-2, -2), (-1, -3)
    ]

    for y in range(3, h - 3):
        for x in range(3, w - 3):
            center = img[y, x]

            # 检查圆上的点
            brighter = 0
            darker = 0

            for dy, dx in circle:
                pixel = img[y + dy, x + dx]
                if pixel > center + threshold:
                    brighter += 1
                elif pixel < center - threshold:
                    darker += 1

            # 如果有连续9个点更亮或更暗，则是角点
            if brighter >= 9 or darker >= 9:
                corners.append((y, x))

    return np.array(corners)


def detect_blobs_simple(img, threshold=0.1):
    """
    简单的斑点检测 (LoG近似)

    Args:
        img: 输入图像
        threshold: 阈值

    Returns:
        斑点列表 [(y, x, radius), ...]
    """
    blobs = []

    # 多尺度检测
    for sigma in range(2, 15, 2):
        # LoG = 高斯二阶导
        log_response = ndimage.gaussian_laplace(img, sigma)
        log_response = log_response * sigma**2  # 归一化

        # 寻找局部极大值
        local_max = ndimage.maximum_filter(np.abs(log_response), size=5)
        mask = (np.abs(log_response) == local_max) & (np.abs(log_response) > threshold * np.abs(log_response).max())

        positions = np.argwhere(mask)
        for y, x in positions:
            blobs.append((y, x, sigma))

    return blobs


def demonstrate_sift_detection():
    """演示SIFT特征检测流程"""
    print("=" * 50)
    print("SIFT特征检测流程")
    print("=" * 50)

    img = create_test_image()

    # 构建高斯金字塔
    gaussian_pyramid = build_gaussian_pyramid(img, num_octaves=3, num_scales=5)

    # 计算DoG金字塔
    dog_pyramid = compute_dog_pyramid(gaussian_pyramid)

    # 检测关键点
    keypoints = find_keypoints_in_dog(dog_pyramid)

    print(f"检测到 {len(keypoints)} 个关键点")

    # 可视化
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))

    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('原始图像')

    # 显示不同八度的DoG
    for i, dog_octave in enumerate(dog_pyramid[:3]):
        if i < 2:
            axes[0, i + 1].imshow(dog_octave[1], cmap='RdBu')
            axes[0, i + 1].set_title(f'DoG Octave {i}')

    # 显示关键点
    axes[1, 0].imshow(img, cmap='gray')
    for octave, scale, y, x in keypoints[:50]:
        scale_factor = 2 ** octave
        axes[1, 0].scatter(x * scale_factor, y * scale_factor, c='red', s=30, marker='+')
    axes[1, 0].set_title('检测到的关键点')

    # 梯度幅值
    mag, ori = compute_gradients(img)
    axes[1, 1].imshow(mag, cmap='hot')
    axes[1, 1].set_title('梯度幅值')

    # 梯度方向
    axes[1, 2].imshow(ori, cmap='hsv')
    axes[1, 2].set_title('梯度方向')

    for ax in axes.flat:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def demonstrate_harris_detection():
    """演示Harris角点检测"""
    print("\n" + "=" * 50)
    print("Harris角点检测")
    print("=" * 50)

    img = create_test_image()

    # 不同k值的Harris检测
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))

    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('原始图像')

    k_values = [0.02, 0.04, 0.06, 0.08, 0.1]

    for idx, k in enumerate(k_values):
        response, corners = detect_harris_corners(img, k=k)

        ax = axes.flat[idx + 1]
        ax.imshow(img, cmap='gray')

        if len(corners) > 0:
            ax.scatter(corners[:, 1], corners[:, 0], c='red', s=20, marker='+')

        ax.set_title(f'Harris (k={k}), {len(corners)} corners')
        print(f"k={k}: 检测到 {len(corners)} 个角点")

    for ax in axes.flat:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def demonstrate_fast_detection():
    """演示FAST角点检测"""
    print("\n" + "=" * 50)
    print("FAST角点检测")
    print("=" * 50)

    img = create_test_image()

    fig, axes = plt.subplots(2, 2, figsize=(10, 10))

    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('原始图像')

    thresholds = [10, 20, 30]

    for idx, threshold in enumerate(thresholds):
        corners = detect_fast_corners(img, threshold=threshold)

        ax = axes.flat[idx + 1]
        ax.imshow(img, cmap='gray')

        if len(corners) > 0:
            ax.scatter(corners[:, 1], corners[:, 0], c='green', s=15, marker='x')

        ax.set_title(f'FAST (threshold={threshold}), {len(corners)} corners')
        print(f"threshold={threshold}: 检测到 {len(corners)} 个角点")

    for ax in axes.flat:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def demonstrate_blob_detection():
    """演示斑点检测"""
    print("\n" + "=" * 50)
    print("斑点检测")
    print("=" * 50)

    img = create_test_image()

    blobs = detect_blobs_simple(img)

    print(f"检测到 {len(blobs)} 个斑点")

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.imshow(img, cmap='gray')
    ax.set_title('斑点检测 (LoG)')

    for y, x, radius in blobs[:30]:
        circle = plt.Circle((x, y), radius, color='red', fill=False, linewidth=1)
        ax.add_patch(circle)

    ax.axis('off')
    plt.tight_layout()
    plt.show()


def demonstrate_detector_comparison():
    """对比不同检测器"""
    print("\n" + "=" * 50)
    print("检测器对比")
    print("=" * 50)

    img = create_test_image()

    # 各检测器
    _, harris_corners = detect_harris_corners(img)
    fast_corners = detect_fast_corners(img)
    blobs = detect_blobs_simple(img)

    # 构建金字塔并检测SIFT
    gaussian_pyramid = build_gaussian_pyramid(img, num_octaves=2, num_scales=5)
    dog_pyramid = compute_dog_pyramid(gaussian_pyramid)
    sift_kps = find_keypoints_in_dog(dog_pyramid)

    fig, axes = plt.subplots(2, 2, figsize=(12, 12))

    detectors = [
        ('Harris', harris_corners, 'red', '+'),
        ('FAST', fast_corners, 'green', 'x'),
        ('Blob (LoG)', blobs, 'blue', 'o'),
        ('DoG (SIFT-like)', sift_kps, 'yellow', '*')
    ]

    for ax, (name, points, color, marker) in zip(axes.flat, detectors):
        ax.imshow(img, cmap='gray')

        if len(points) > 0:
            if name == 'Blob (LoG)':
                for y, x, r in points[:30]:
                    circle = plt.Circle((x, y), r, color=color, fill=False)
                    ax.add_patch(circle)
            elif name == 'DoG (SIFT-like)':
                for octave, scale, y, x in points[:50]:
                    scale_factor = 2 ** octave
                    ax.scatter(x * scale_factor, y * scale_factor, c=color, s=30, marker=marker)
            else:
                ax.scatter(points[:, 1], points[:, 0], c=color, s=15, marker=marker)

        ax.set_title(f'{name}: {len(points)} features')

    for ax in axes.flat:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def demo():
    """运行所有演示"""
    demonstrate_sift_detection()
    demonstrate_harris_detection()
    demonstrate_fast_detection()
    demonstrate_blob_detection()
    demonstrate_detector_comparison()


if __name__ == "__main__":
    demo()
