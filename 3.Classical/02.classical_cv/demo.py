"""
传统计算机视觉 (Classical Computer Vision) 示例代码

包含内容:
1. Harris角点检测
2. SIFT特征检测与匹配
3. ORB特征检测与匹配
4. HOG特征提取
5. Canny边缘检测
6. 特征匹配与可视化
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.ndimage import gaussian_filter, sobel
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


# =====================================================
# 1. Harris角点检测
# =====================================================

def harris_corner_detection(image, k=0.04, threshold=0.01):
    """
    Harris角点检测

    Args:
        image: 灰度图像
        k: Harris参数 (通常0.04-0.06)
        threshold: 响应阈值

    Returns:
        corners: 角点坐标
        response: 响应图
    """
    # 计算梯度
    Ix = sobel(image, axis=1)
    Iy = sobel(image, axis=0)

    # 计算梯度乘积
    Ix2 = Ix ** 2
    Iy2 = Iy ** 2
    Ixy = Ix * Iy

    # 高斯平滑
    Ix2 = gaussian_filter(Ix2, sigma=1)
    Iy2 = gaussian_filter(Iy2, sigma=1)
    Ixy = gaussian_filter(Ixy, sigma=1)

    # 计算响应函数
    det = Ix2 * Iy2 - Ixy ** 2
    trace = Ix2 + Iy2
    response = det - k * trace ** 2

    # 阈值处理
    threshold_value = threshold * response.max()
    corners = np.where(response > threshold_value)

    return corners, response


# =====================================================
# 2. SIFT特征检测 (简化实现)
# =====================================================

def create_gaussian_pyramid(image, num_octaves=4, num_scales=5, sigma=1.6):
    """创建高斯金字塔"""
    pyramid = []
    for octave in range(num_octaves):
        octave_images = []
        for scale in range(num_scales):
            sigma_effective = sigma * (2 ** (scale / num_scales))
            blurred = gaussian_filter(image, sigma_effective)
            octave_images.append(blurred)
        pyramid.append(octave_images)
        image = image[::2, ::2]  # 下采样
    return pyramid


def compute_dog(pyramid):
    """计算DoG金字塔"""
    dog_pyramid = []
    for octave in pyramid:
        dog_octave = []
        for i in range(len(octave) - 1):
            dog = octave[i+1] - octave[i]
            dog_octave.append(dog)
        dog_pyramid.append(dog_octave)
    return dog_pyramid


def find_keypoints(dog_pyramid, contrast_threshold=0.03):
    """寻找关键点（简化版）"""
    keypoints = []
    for octave_idx, octave in enumerate(dog_pyramid):
        for scale_idx in range(1, len(octave) - 1):
            dog = octave[scale_idx]
            # 寻找局部极值
            for i in range(1, dog.shape[0] - 1):
                for j in range(1, dog.shape[1] - 1):
                    val = dog[i, j]
                    if abs(val) > contrast_threshold:
                        keypoints.append((octave_idx, scale_idx, i, j, val))
    return keypoints


def compute_sift_descriptor(image, keypoint, patch_size=16):
    """计算SIFT描述子（简化版）"""
    x, y = int(keypoint[2]), int(keypoint[3])

    # 确保在图像范围内
    half = patch_size // 2
    if x < half or x >= image.shape[0] - half or y < half or y >= image.shape[1] - half:
        return None

    # 提取patch
    patch = image[x-half:x+half, y-half:y+half]

    # 计算梯度
    gx = sobel(patch, axis=1)
    gy = sobel(patch, axis=0)

    # 计算梯度幅值和方向
    magnitude = np.sqrt(gx**2 + gy**2)
    orientation = np.arctan2(gy, gx) * 180 / np.pi

    # 创建4x4网格，每个格子8个方向
    descriptor = np.zeros(128)
    cell_size = patch_size // 4

    for i in range(4):
        for j in range(4):
            cell_mag = magnitude[i*cell_size:(i+1)*cell_size, j*cell_size:(j+1)*cell_size]
            cell_ori = orientation[i*cell_size:(i+1)*cell_size, j*cell_size:(j+1)*cell_size]

            # 8方向直方图
            hist, _ = np.histogram(cell_ori, bins=8, range=(-180, 180), weights=cell_mag)
            idx = (i * 4 + j) * 8
            descriptor[idx:idx+8] = hist

    # 归一化
    norm = np.linalg.norm(descriptor)
    if norm > 0:
        descriptor = descriptor / norm

    return descriptor


# =====================================================
# 3. ORB特征检测
# =====================================================

def fast_corner_detection(image, threshold=20):
    """
    FAST角点检测（简化版）
    """
    corners = []
    h, w = image.shape

    for i in range(3, h - 3):
        for j in range(3, w - 3):
            center = int(image[i, j])

            # 16个周围点
            circle_points = [
                (0, 3), (1, 3), (2, 2), (3, 1), (3, 0), (3, -1), (2, -2), (1, -3),
                (0, -3), (-1, -3), (-2, -2), (-3, -1), (-3, 0), (-3, 1), (-2, 2), (-1, 3)
            ]

            brighter = 0
            darker = 0

            for dx, dy in circle_points:
                pixel = int(image[i + dy, j + dx])
                if pixel > center + threshold:
                    brighter += 1
                elif pixel < center - threshold:
                    darker += 1

            if brighter >= 12 or darker >= 12:
                corners.append((i, j))

    return corners


def brief_descriptor(image, keypoints, patch_size=31):
    """
    BRIEF描述子（简化版）
    """
    descriptors = []
    half = patch_size // 2
    h, w = image.shape

    # 预定义的点对
    np.random.seed(42)
    num_pairs = 256
    pairs = np.random.randint(-half, half + 1, (num_pairs, 2, 2))

    for kp in keypoints:
        y, x = int(kp[0]), int(kp[1])

        if y < half or y >= h - half or x < half or x >= w - half:
            descriptors.append(None)
            continue

        descriptor = np.zeros(num_pairs, dtype=np.uint8)
        patch = image[y-half:y+half+1, x-half:x+half+1]

        for i, (p1, p2) in enumerate(pairs):
            v1 = patch[p1[0] + half, p1[1] + half]
            v2 = patch[p2[0] + half, p2[1] + half]
            descriptor[i] = 1 if v1 < v2 else 0

        descriptors.append(descriptor)

    return descriptors


# =====================================================
# 4. HOG特征
# =====================================================

def compute_hog(image, cell_size=8, block_size=2, num_bins=9):
    """
    HOG特征提取

    Args:
        image: 灰度图像
        cell_size: cell大小
        block_size: block包含的cell数
        num_bins: 直方图bin数

    Returns:
        hog_features: HOG特征向量
    """
    # 计算梯度
    gx = sobel(image, axis=1)
    gy = sobel(image, axis=0)

    # 梯度幅值和方向
    magnitude = np.sqrt(gx**2 + gy**2)
    orientation = np.arctan2(gy, gx) * 180 / np.pi
    orientation[orientation < 0] += 360

    # 计算cell直方图
    h, w = image.shape
    n_cells_y = h // cell_size
    n_cells_x = w // cell_size

    histograms = np.zeros((n_cells_y, n_cells_x, num_bins))

    bin_width = 360 / num_bins

    for i in range(n_cells_y):
        for j in range(n_cells_x):
            cell_mag = magnitude[i*cell_size:(i+1)*cell_size, j*cell_size:(j+1)*cell_size]
            cell_ori = orientation[i*cell_size:(i+1)*cell_size, j*cell_size:(j+1)*cell_size]

            for mag, ori in zip(cell_mag.flatten(), cell_ori.flatten()):
                bin_idx = int(ori / bin_width) % num_bins
                histograms[i, j, bin_idx] += mag

    # 块归一化
    hog_features = []

    for i in range(n_cells_y - block_size + 1):
        for j in range(n_cells_x - block_size + 1):
            block = histograms[i:i+block_size, j:j+block_size].flatten()
            norm = np.linalg.norm(block) + 1e-6
            normalized_block = block / norm
            hog_features.extend(normalized_block)

    return np.array(hog_features)


# =====================================================
# 5. Canny边缘检测
# =====================================================

def canny_edge_detection(image, low_threshold=50, high_threshold=150, sigma=1.0):
    """
    Canny边缘检测

    Args:
        image: 灰度图像
        low_threshold: 低阈值
        high_threshold: 高阈值
        sigma: 高斯平滑参数

    Returns:
        edges: 边缘图像
    """
    # 1. 高斯平滑
    smoothed = gaussian_filter(image.astype(float), sigma=sigma)

    # 2. 计算梯度
    gx = sobel(smoothed, axis=1)
    gy = sobel(smoothed, axis=0)

    magnitude = np.sqrt(gx**2 + gy**2)
    orientation = np.arctan2(gy, gx) * 180 / np.pi

    # 3. 非极大值抑制
    h, w = image.shape
    suppressed = np.zeros_like(magnitude)

    for i in range(1, h - 1):
        for j in range(1, w - 1):
            angle = orientation[i, j]

            # 量化到4个方向
            if (angle >= -22.5 and angle < 22.5) or (angle >= 157.5 or angle < -157.5):
                neighbors = [magnitude[i, j-1], magnitude[i, j+1]]
            elif (angle >= 22.5 and angle < 67.5) or (angle >= -157.5 and angle < -112.5):
                neighbors = [magnitude[i-1, j-1], magnitude[i+1, j+1]]
            elif (angle >= 67.5 and angle < 112.5) or (angle >= -112.5 and angle < -67.5):
                neighbors = [magnitude[i-1, j], magnitude[i+1, j]]
            else:
                neighbors = [magnitude[i-1, j+1], magnitude[i+1, j-1]]

            if magnitude[i, j] >= max(neighbors):
                suppressed[i, j] = magnitude[i, j]

    # 4. 双阈值
    strong_edges = suppressed > high_threshold
    weak_edges = (suppressed >= low_threshold) & (suppressed <= high_threshold)

    # 5. 滞后阈值（边缘连接）
    edges = strong_edges.copy()

    # 连接弱边缘
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            if weak_edges[i, j]:
                if np.any(strong_edges[i-1:i+2, j-1:j+2]):
                    edges[i, j] = True

    return edges


# =====================================================
# 演示函数
# =====================================================

def demo_harris():
    """Harris角点检测演示"""
    print("=" * 60)
    print("1. Harris角点检测")
    print("=" * 60)

    # 创建测试图像
    image = np.zeros((200, 200))
    # 添加一些几何图形
    image[30:70, 30:70] = 255  # 正方形
    image[100:150, 50:150] = 255  # 矩形
    image[50:150, 130:180] = 255  # 矩形

    # 添加一些噪声
    image = image + np.random.randn(200, 200) * 10
    image = np.clip(image, 0, 255)

    corners, response = harris_corner_detection(image, k=0.04, threshold=0.01)

    print(f"检测到 {len(corners[0])} 个角点")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 原图
    axes[0].imshow(image, cmap='gray')
    axes[0].set_title('原图', fontsize=14)
    axes[0].axis('off')

    # 角点检测结果
    axes[1].imshow(image, cmap='gray')
    axes[1].scatter(corners[1], corners[0], c='red', s=50, marker='o')
    axes[1].set_title(f'Harris角点检测 (检测到{len(corners[0])}个角点)', fontsize=14)
    axes[1].axis('off')

    plt.tight_layout()
    plt.savefig('cv_harris.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Harris角点检测图已保存为 cv_harris.png\n")


def demo_sift():
    """SIFT特征检测演示"""
    print("=" * 60)
    print("2. SIFT特征检测")
    print("=" * 60)

    # 创建测试图像
    image = np.zeros((128, 128))
    # 添加一些特征
    image[20:60, 20:60] = 255
    image[70:110, 70:110] = 128

    # 添加噪声
    image = image + np.random.randn(128, 128) * 5
    image = np.clip(image, 0, 255)

    # 创建高斯金字塔和DoG
    pyramid = create_gaussian_pyramid(image, num_octaves=2, num_scales=4)
    dog_pyramid = compute_dog(pyramid)

    # 寻找关键点
    keypoints = find_keypoints(dog_pyramid)
    print(f"检测到 {len(keypoints)} 个关键点")

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # 原图
    axes[0].imshow(image, cmap='gray')
    axes[0].set_title('原图', fontsize=14)
    axes[0].axis('off')

    # DoG第一层
    if len(dog_pyramid) > 0 and len(dog_pyramid[0]) > 0:
        axes[1].imshow(dog_pyramid[0][0], cmap='gray')
        axes[1].set_title('DoG金字塔 (第1层)', fontsize=14)
        axes[1].axis('off')

    # 关键点
    axes[2].imshow(image, cmap='gray')
    # 简化显示
    for i, (octave, scale, x, y, val) in enumerate(keypoints[:20]):
        scale_factor = 2 ** octave
        axes[2].scatter(y * scale_factor, x * scale_factor, c='red', s=30)
    axes[2].set_title(f'SIFT关键点 (显示前20个)', fontsize=14)
    axes[2].axis('off')

    plt.tight_layout()
    plt.savefig('cv_sift.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("SIFT特征检测图已保存为 cv_sift.png\n")


def demo_orb():
    """ORB特征检测演示"""
    print("=" * 60)
    print("3. ORB特征检测")
    print("=" * 60)

    # 创建测试图像
    image = np.zeros((150, 150))
    image[20:50, 20:50] = 255
    image[80:120, 60:120] = 200
    image = image + np.random.randn(150, 150) * 5
    image = np.clip(image, 0, 255)

    # FAST角点检测
    corners = fast_corner_detection(image, threshold=20)
    print(f"FAST检测到 {len(corners)} 个角点")

    # BRIEF描述子
    descriptors = brief_descriptor(image, corners[:50])

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.imshow(image, cmap='gray')
    if corners:
        y_coords = [c[0] for c in corners[:50]]
        x_coords = [c[1] for c in corners[:50]]
        ax.scatter(x_coords, y_coords, c='red', s=30, marker='o')
    ax.set_title(f'ORB特征检测 (FAST角点)', fontsize=14)
    ax.axis('off')

    plt.tight_layout()
    plt.savefig('cv_orb.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("ORB特征检测图已保存为 cv_orb.png\n")


def demo_hog():
    """HOG特征演示"""
    print("=" * 60)
    print("4. HOG特征提取")
    print("=" * 60)

    # 创建测试图像（简单的人形轮廓）
    image = np.zeros((128, 64))

    # 简化的人形
    image[10:30, 25:40] = 255  # 头
    image[30:70, 20:45] = 200  # 身体
    image[70:100, 15:25] = 150  # 左腿
    image[70:100, 35:45] = 150  # 右腿

    # 计算HOG特征
    hog_features = compute_hog(image, cell_size=8, block_size=2, num_bins=9)

    print(f"HOG特征维度: {len(hog_features)}")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 原图
    axes[0].imshow(image, cmap='gray')
    axes[0].set_title('原图 (人形轮廓)', fontsize=14)
    axes[0].axis('off')

    # HOG特征可视化
    axes[1].bar(range(len(hog_features[:100])), hog_features[:100], color='steelblue')
    axes[1].set_xlabel('特征索引', fontsize=12)
    axes[1].set_ylabel('特征值', fontsize=12)
    axes[1].set_title(f'HOG特征 (前100维)', fontsize=14)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('cv_hog.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("HOG特征图已保存为 cv_hog.png\n")


def demo_canny():
    """Canny边缘检测演示"""
    print("=" * 60)
    print("5. Canny边缘检测")
    print("=" * 60)

    # 创建测试图像
    image = np.zeros((150, 150))
    image[30:60, 30:60] = 255
    image[80:120, 40:110] = 200
    image = image + np.random.randn(150, 150) * 3
    image = np.clip(image, 0, 255)

    # Canny边缘检测
    edges = canny_edge_detection(image, low_threshold=10, high_threshold=30, sigma=1.0)

    print(f"边缘像素数: {np.sum(edges)}")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].imshow(image, cmap='gray')
    axes[0].set_title('原图', fontsize=14)
    axes[0].axis('off')

    axes[1].imshow(edges, cmap='gray')
    axes[1].set_title(f'Canny边缘检测', fontsize=14)
    axes[1].axis('off')

    plt.tight_layout()
    plt.savefig('cv_canny.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Canny边缘检测图已保存为 cv_canny.png\n")


def demo_comparison():
    """算法对比"""
    print("=" * 60)
    print("6. 特征检测算法对比")
    print("=" * 60)

    # 创建测试图像
    image = np.zeros((200, 200))
    image[30:80, 30:80] = 255
    image[100:160, 50:150] = 200
    image = image + np.random.randn(200, 200) * 5
    image = np.clip(image, 0, 255)

    # 检测
    corners_harris, _ = harris_corner_detection(image)
    corners_fast = fast_corner_detection(image, threshold=15)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Harris
    axes[0].imshow(image, cmap='gray')
    axes[0].scatter(corners_harris[1], corners_harris[0], c='red', s=20)
    axes[0].set_title(f'Harris ({len(corners_harris[0])}个角点)', fontsize=14)
    axes[0].axis('off')

    # FAST
    axes[1].imshow(image, cmap='gray')
    if corners_fast:
        axes[1].scatter([c[1] for c in corners_fast[:100]], [c[0] for c in corners_fast[:100]], c='green', s=20)
    axes[1].set_title(f'FAST ({len(corners_fast)}个角点)', fontsize=14)
    axes[1].axis('off')

    # Canny
    edges = canny_edge_detection(image, low_threshold=10, high_threshold=30)
    axes[2].imshow(edges, cmap='gray')
    axes[2].set_title(f'Canny边缘', fontsize=14)
    axes[2].axis('off')

    plt.suptitle('传统计算机视觉算法对比', fontsize=14)
    plt.tight_layout()
    plt.savefig('cv_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("算法对比图已保存为 cv_comparison.png\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("传统计算机视觉 (Classical CV) 完整示例")
    print("=" * 60 + "\n")

    demo_harris()
    demo_sift()
    demo_orb()
    demo_hog()
    demo_canny()
    demo_comparison()

    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
