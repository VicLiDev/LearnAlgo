"""
角点检测算法示例：Harris, Shi-Tomasi, FAST
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt


def harris_corner(image, k=0.04, blockSize=2, ksize=3):
    """
    Harris角点检测

    Args:
        image: 输入图像 (灰度)
        k: Harris参数 (0.04-0.06)
        blockSize: 邻域大小
        ksize: Sobel核大小

    Returns:
        corner_response: 角点响应图
    """
    # 计算梯度
    Ix = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=ksize)
    Iy = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=ksize)

    # 计算M矩阵的分量
    Ix2 = Ix ** 2
    Iy2 = Iy ** 2
    Ixy = Ix * Iy

    # 高斯加权
    Ix2 = cv2.GaussianBlur(Ix2, (blockSize * 2 + 1, blockSize * 2 + 1), 0)
    Iy2 = cv2.GaussianBlur(Iy2, (blockSize * 2 + 1, blockSize * 2 + 1), 0)
    Ixy = cv2.GaussianBlur(Ixy, (blockSize * 2 + 1, blockSize * 2 + 1), 0)

    # 计算响应函数 R = det(M) - k * trace(M)²
    det = Ix2 * Iy2 - Ixy ** 2
    trace = Ix2 + Iy2
    response = det - k * trace ** 2

    return response


def shi_tomasi_corner(image, max_corners=100, quality_level=0.01, min_distance=10):
    """
    Shi-Tomasi角点检测 (goodFeaturesToTrack)

    Args:
        image: 输入图像
        max_corners: 最大角点数
        quality_level: 质量阈值 (相对于最强角点)
        min_distance: 角点间最小距离

    Returns:
        corners: 角点坐标 (N, 1, 2)
    """
    corners = cv2.goodFeaturesToTrack(
        image,
        maxCorners=max_corners,
        qualityLevel=quality_level,
        minDistance=min_distance,
        blockSize=7
    )
    return corners


def fast_corner(image, threshold=10, nonmax_suppression=True):
    """
    FAST角点检测

    Args:
        image: 输入图像
        threshold: 亮度差阈值
        nonmax_suppression: 是否使用非极大值抑制

    Returns:
        keypoints: 关键点列表
    """
    fast = cv2.FastFeatureDetector_create(
        threshold=threshold,
        nonmaxSuppression=nonmax_suppression
    )
    keypoints = fast.detect(image, None)
    return keypoints


def compare_corner_detectors(image):
    """比较不同角点检测算法"""
    # Harris
    harris_response = harris_corner(image)
    harris_corners = np.where(harris_response > 0.01 * harris_response.max())

    # Shi-Tomasi
    shi_tomasi_corners = shi_tomasi_corner(image, max_corners=100)

    # FAST
    fast_kp = fast_corner(image)

    # 可视化
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))

    # 原图
    axes[0, 0].imshow(image, cmap='gray')
    axes[0, 0].set_title('原图')
    axes[0, 0].axis('off')

    # Harris
    axes[0, 1].imshow(image, cmap='gray')
    axes[0, 1].scatter(harris_corners[1], harris_corners[0], c='r', s=5)
    axes[0, 1].set_title(f'Harris ({len(harris_corners[0])} 角点)')
    axes[0, 1].axis('off')

    # Shi-Tomasi
    axes[1, 0].imshow(image, cmap='gray')
    if shi_tomasi_corners is not None:
        axes[1, 0].scatter(
            shi_tomasi_corners[:, 0, 0],
            shi_tomasi_corners[:, 0, 1],
            c='g', s=30, marker='o', facecolors='none'
        )
    axes[1, 0].set_title(f'Shi-Tomasi ({len(shi_tomasi_corners) if shi_tomasi_corners is not None else 0} 角点)')
    axes[1, 0].axis('off')

    # FAST
    axes[1, 1].imshow(image, cmap='gray')
    for kp in fast_kp:
        axes[1, 1].scatter(kp.pt[0], kp.pt[1], c='b', s=30, marker='x')
    axes[1, 1].set_title(f'FAST ({len(fast_kp)} 角点)')
    axes[1, 1].axis('off')

    plt.tight_layout()
    plt.show()


def harris_response_visualization(image):
    """可视化Harris响应图"""
    response = harris_corner(image)

    # 归一化响应图用于显示
    response_norm = cv2.normalize(response, None, 0, 255, cv2.NORM_MINMAX)
    response_norm = response_norm.astype(np.uint8)

    # 应用颜色映射
    response_color = cv2.applyColorMap(response_norm, cv2.COLORMAP_JET)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(image, cmap='gray')
    axes[0].set_title('原图')
    axes[0].axis('off')

    axes[1].imshow(response_norm, cmap='hot')
    axes[1].set_title('Harris响应 (热力图)')
    axes[1].axis('off')

    axes[2].imshow(cv2.cvtColor(response_color, cv2.COLOR_BGR2RGB))
    axes[2].set_title('Harris响应 (彩色)')
    axes[2].axis('off')

    plt.tight_layout()
    plt.show()


def fast_threshold_demo(image):
    """FAST阈值参数演示"""
    thresholds = [5, 10, 20, 50]

    fig, axes = plt.subplots(2, 2, figsize=(12, 12))

    for ax, thresh in zip(axes.flat, thresholds):
        kp = fast_corner(image, threshold=thresh)

        ax.imshow(image, cmap='gray')
        for p in kp:
            ax.scatter(p.pt[0], p.pt[1], c='r', s=10)
        ax.set_title(f'FAST threshold={thresh} ({len(kp)} 角点)')
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def corner_properties_demo():
    """角点性质演示"""
    # 创建测试图像
    img = np.zeros((300, 300), dtype=np.uint8)

    # 平坦区域
    cv2.rectangle(img, (20, 20), (80, 80), 200, -1)

    # 边缘
    cv2.rectangle(img, (120, 20), (180, 80), 200, -1)
    cv2.line(img, (120, 50), (180, 50), 255, 2)

    # 角点
    cv2.rectangle(img, (220, 20), (280, 80), 200, -1)
    img[220:280, 20:80] = 200
    img[20:80, 220:280] = 200

    # 计算Harris响应
    response = harris_corner(img)
    response_norm = cv2.normalize(response, None, 0, 255, cv2.NORM_MINMAX)

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    axes[0].imshow(img, cmap='gray')
    axes[0].set_title('测试图像\n(左:平坦, 中:边缘, 右:角点)')
    axes[0].axis('off')

    axes[1].imshow(response_norm, cmap='hot')
    axes[1].set_title('Harris响应\n(角点区域响应高)')
    axes[1].axis('off')

    plt.tight_layout()
    plt.show()


def demo():
    """运行所有演示"""
    print("=" * 50)
    print("角点检测算法演示")
    print("=" * 50)

    # 读取或创建测试图像
    image = cv2.imread('chessboard.png', cv2.IMREAD_GRAYSCALE)
    if image is None:
        # 创建棋盘格图像
        image = np.zeros((400, 400), dtype=np.uint8)
        square_size = 50
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    image[i*square_size:(i+1)*square_size,
                          j*square_size:(j+1)*square_size] = 255

    print("\n1. 角点检测算法对比")
    compare_corner_detectors(image)

    print("\n2. Harris响应可视化")
    harris_response_visualization(image)

    print("\n3. FAST阈值参数演示")
    fast_threshold_demo(image)

    print("\n4. 角点性质演示")
    corner_properties_demo()


if __name__ == "__main__":
    demo()
