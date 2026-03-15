"""
基础滤波与边缘检测示例
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt


def add_noise(image, noise_type='gaussian', **kwargs):
    """添加噪声"""
    if noise_type == 'gaussian':
        mean = kwargs.get('mean', 0)
        sigma = kwargs.get('sigma', 25)
        noise = np.random.normal(mean, sigma, image.shape)
        noisy = np.clip(image + noise, 0, 255).astype(np.uint8)
    elif noise_type == 'salt_pepper':
        prob = kwargs.get('prob', 0.05)
        noisy = image.copy()
        # 盐噪声
        salt = np.random.random(image.shape[:2]) < prob / 2
        noisy[salt] = 255
        # 椒噪声
        pepper = np.random.random(image.shape[:2]) < prob / 2
        noisy[pepper] = 0
    return noisy


def compare_filters(image):
    """比较不同滤波器效果"""
    # 均值滤波
    mean_filtered = cv2.blur(image, (5, 5))

    # 高斯滤波
    gaussian_filtered = cv2.GaussianBlur(image, (5, 5), 1.0)

    # 中值滤波
    median_filtered = cv2.medianBlur(image, 5)

    # 双边滤波
    bilateral_filtered = cv2.bilateralFilter(image, 9, 75, 75)

    # 可视化
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    images = [
        (image, '原图'),
        (mean_filtered, '均值滤波'),
        (gaussian_filtered, '高斯滤波'),
        (median_filtered, '中值滤波'),
        (bilateral_filtered, '双边滤波'),
    ]

    for ax, (img, title) in zip(axes.flat, images):
        ax.imshow(img, cmap='gray' if len(img.shape) == 2 else None)
        ax.set_title(title)
        ax.axis('off')

    axes.flat[-1].axis('off')
    plt.tight_layout()
    plt.show()


def compare_edge_detectors(image):
    """比较不同边缘检测算子"""
    # Sobel
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    sobel = np.sqrt(sobel_x**2 + sobel_y**2)
    sobel = np.uint8(sobel / sobel.max() * 255)

    # Laplacian
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    laplacian = np.uint8(np.abs(laplacian) / laplacian.max() * 255)

    # Canny
    canny = cv2.Canny(image, 50, 150)

    # 可视化
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    images = [
        (image, '原图'),
        (sobel, 'Sobel'),
        (laplacian, 'Laplacian'),
        (canny, 'Canny'),
    ]

    for ax, (img, title) in zip(axes.flat, images):
        ax.imshow(img, cmap='gray')
        ax.set_title(title)
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def canny_threshold_demo(image):
    """Canny阈值参数演示"""
    thresholds = [
        (30, 90),
        (50, 150),
        (100, 200),
        (150, 250),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    for ax, (low, high) in zip(axes.flat, thresholds):
        edges = cv2.Canny(image, low, high)
        ax.imshow(edges, cmap='gray')
        ax.set_title(f'Canny: ({low}, {high})')
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def bilateral_filter_demo(image):
    """双边滤波参数演示"""
    params = [
        (5, 50, 50),
        (9, 75, 75),
        (15, 100, 100),
        (20, 150, 150),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    for ax, (d, sigma_color, sigma_space) in zip(axes.flat, params):
        filtered = cv2.bilateralFilter(image, d, sigma_color, sigma_space)
        ax.imshow(filtered, cmap='gray' if len(filtered.shape) == 2 else None)
        ax.set_title(f'双边滤波: d={d}, σ_c={sigma_color}, σ_s={sigma_space}')
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def denoise_comparison():
    """去噪效果对比"""
    # 创建测试图像
    image = np.zeros((200, 200), dtype=np.uint8)
    cv2.rectangle(image, (50, 50), (150, 150), 255, -1)
    cv2.circle(image, (100, 100), 30, 0, -1)

    # 添加噪声
    gaussian_noisy = add_noise(image, 'gaussian', sigma=30)
    sp_noisy = add_noise(image, 'salt_pepper', prob=0.1)

    # 高斯噪声 - 高斯滤波
    gaussian_denoised = cv2.GaussianBlur(gaussian_noisy, (5, 5), 1.0)

    # 椒盐噪声 - 中值滤波
    median_denoised = cv2.medianBlur(sp_noisy, 5)

    # 可视化
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))

    axes[0, 0].imshow(gaussian_noisy, cmap='gray')
    axes[0, 0].set_title('高斯噪声')
    axes[0, 1].imshow(gaussian_denoised, cmap='gray')
    axes[0, 1].set_title('高斯滤波去噪')

    axes[1, 0].imshow(sp_noisy, cmap='gray')
    axes[1, 0].set_title('椒盐噪声')
    axes[1, 1].imshow(median_denoised, cmap='gray')
    axes[1, 1].set_title('中值滤波去噪')

    for ax in axes.flat:
        ax.axis('off')

    axes[0, 2].axis('off')
    axes[1, 2].axis('off')

    plt.tight_layout()
    plt.show()


def demo():
    """运行所有演示"""
    print("=" * 50)
    print("基础滤波与边缘检测演示")
    print("=" * 50)

    # 读取图像
    image = cv2.imread('lena.png', cv2.IMREAD_GRAYSCALE)
    if image is None:
        # 如果没有图像，创建测试图像
        image = np.zeros((256, 256), dtype=np.uint8)
        cv2.rectangle(image, (50, 50), (200, 200), 255, -1)
        cv2.circle(image, (125, 125), 50, 0, -1)
        image = cv2.GaussianBlur(image, (5, 5), 1.0)

    print("\n1. 滤波器对比")
    compare_filters(image)

    print("\n2. 边缘检测对比")
    compare_edge_detectors(image)

    print("\n3. Canny阈值演示")
    canny_threshold_demo(image)

    print("\n4. 去噪效果对比")
    denoise_comparison()


if __name__ == "__main__":
    demo()
