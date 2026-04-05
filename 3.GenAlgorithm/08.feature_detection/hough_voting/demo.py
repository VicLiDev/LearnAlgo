"""
霍夫投票算法示例：直线检测、圆检测、广义霍夫变换、3D平面检测
"""
import argparse
import numpy as np
import os
import matplotlib
import sys

# 根据命令行参数决定后端（需要在导入pyplot之前设置）
if '--show' in sys.argv or '-s' in sys.argv:
    # 使用交互式后端 - 优先使用TkAgg避免Qt冲突
    try:
        matplotlib.use('TkAgg')
    except:
        pass  # 使用默认后端
else:
    # 使用非交互式后端
    matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from skimage import draw
from skimage.feature import canny
from skimage.transform import hough_line, hough_line_peaks
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.draw import circle_perimeter

# 设置OpenCV不使用Qt GUI（避免与matplotlib冲突）
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
import cv2

# 全局变量：是否显示图形
SHOW_PLOTS = False


def show_or_close():
    """显示或关闭图形"""
    if SHOW_PLOTS:
        plt.show()
    else:
        plt.close()


# ============================================================================
# 1. 标准霍夫直线检测
# ============================================================================

def hough_line_transform(image, theta_res=1, rho_res=1):
    """
    标准霍夫直线变换

    Args:
        image: 二值边缘图像
        theta_res: 角度分辨率(度)
        rho_res: 距离分辨率(像素)

    Returns:
        accumulator: 累加器数组
        thetas: 角度数组
        rhos: 距离数组
    """
    # 设置角度和距离范围
    thetas = np.deg2rad(np.arange(-90.0, 90.0, theta_res))
    height, width = image.shape
    diag_len = int(np.sqrt(height**2 + width**2))
    rhos = np.linspace(-diag_len, diag_len, int(2 * diag_len / rho_res))

    # 初始化累加器
    accumulator = np.zeros((len(rhos), len(thetas)), dtype=np.uint64)

    # 获取边缘点坐标
    y_idxs, x_idxs = np.nonzero(image)

    # 投票
    for i in range(len(x_idxs)):
        x = x_idxs[i]
        y = y_idxs[i]

        for t_idx, theta in enumerate(thetas):
            # 计算rho = x*cos(theta) + y*sin(theta)
            rho = x * np.cos(theta) + y * np.sin(theta)
            rho_idx = np.argmin(np.abs(rhos - rho))
            accumulator[rho_idx, t_idx] += 1

    return accumulator, thetas, rhos


def find_lines_manual(image, threshold=100, theta_res=1, rho_res=1):
    """
    手动实现霍夫直线检测

    Args:
        image: 二值边缘图像
        threshold: 投票阈值
        theta_res: 角度分辨率(度)
        rho_res: 距离分辨率(像素)

    Returns:
        lines: 检测到的直线列表 [(rho, theta), ...]
    """
    accumulator, thetas, rhos = hough_line_transform(image, theta_res, rho_res)

    # 找到峰值
    lines = []
    acc_copy = accumulator.copy()

    while True:
        max_idx = np.unravel_index(np.argmax(acc_copy), acc_copy.shape)
        max_val = acc_copy[max_idx]

        if max_val < threshold:
            break

        rho_idx, theta_idx = max_idx
        lines.append((rhos[rho_idx], thetas[theta_idx]))

        # 非极大值抑制：清除邻域
        y_min = max(0, rho_idx - 10)
        y_max = min(acc_copy.shape[0], rho_idx + 10)
        x_min = max(0, theta_idx - 10)
        x_max = min(acc_copy.shape[1], theta_idx + 10)
        acc_copy[y_min:y_max, x_min:x_max] = 0

    return lines, accumulator, thetas, rhos


def detect_lines_skimage(image):
    """
    使用skimage进行霍夫直线检测

    Args:
        image: 灰度图像

    Returns:
        lines: 检测到的直线
        accumulator: 累加器
        angles: 角度数组
        distances: 距离数组
    """
    # 边缘检测
    edges = canny(image, sigma=2)

    # 霍夫变换
    tested_angles = np.linspace(-np.pi/2, np.pi/2, 180)
    accumulator, angles, distances = hough_line(edges, theta=tested_angles)

    # 检测峰值
    peaks = hough_line_peaks(accumulator, angles, distances, threshold=0.5*np.max(accumulator))

    return peaks, edges, accumulator, angles, distances


# ============================================================================
# 2. 霍夫圆检测
# ============================================================================

def hough_circle_transform(image, radius_range, sigma=2):
    """
    霍夫圆检测

    Args:
        image: 灰度图像
        radius_range: 半径范围 (min_radius, max_radius)
        sigma: Canny边缘检测的sigma参数

    Returns:
        centers: 圆心列表 [(x, y, radius), ...]
        edges: 边缘图像
        accumulator: 累加器
    """
    # 边缘检测
    edges = canny(image, sigma=sigma)

    # 生成半径范围
    min_radius, max_radius = radius_range
    radii = np.arange(min_radius, max_radius, 1)

    # 霍夫圆变换
    accumulator = hough_circle(edges, radii)

    # 检测峰值
    # hough_circle_peaks返回 (accum, cx, cy, radii)
    accum, cx, cy, radii_found = hough_circle_peaks(accumulator, radii, total_num_peaks=5)

    centers = []
    for center_x, center_y, radius in zip(cx, cy, radii_found):
        centers.append((center_x, center_y, radius))

    return centers, edges, accumulator


def hough_circle_manual(image, radius, threshold=0.6):
    """
    手动实现霍夫圆检测（单半径）

    Args:
        image: 二值边缘图像
        radius: 要检测的圆半径
        threshold: 峰值阈值比例

    Returns:
        centers: 圆心列表 [(x, y), ...]
        accumulator: 累加器
    """
    height, width = image.shape
    accumulator = np.zeros((height, width), dtype=np.uint64)

    # 获取边缘点
    y_idxs, x_idxs = np.nonzero(image)

    # 使用梯度信息加速（这里简化处理）
    # 对每个边缘点，在半径为r的圆上投票
    for i in range(len(x_idxs)):
        x = x_idxs[i]
        y = y_idxs[i]

        # 在半径为r的圆上投票
        for angle in np.linspace(0, 2*np.pi, 36):
            cx = int(x + radius * np.cos(angle))
            cy = int(y + radius * np.sin(angle))

            if 0 <= cx < width and 0 <= cy < height:
                accumulator[cy, cx] += 1

    # 找峰值
    centers = []
    max_val = np.max(accumulator)
    threshold_val = threshold * max_val

    # 简单的峰值检测
    acc_copy = accumulator.copy()
    while np.max(acc_copy) > threshold_val:
        cy, cx = np.unravel_index(np.argmax(acc_copy), acc_copy.shape)
        centers.append((cx, cy))

        # 非极大值抑制
        y_min = max(0, cy - radius//2)
        y_max = min(height, cy + radius//2)
        x_min = max(0, cx - radius//2)
        x_max = min(width, cx + radius//2)
        acc_copy[y_min:y_max, x_min:x_max] = 0

    return centers, accumulator


# ============================================================================
# 3. 广义霍夫变换
# ============================================================================

class GeneralizedHoughTransform:
    """
    广义霍夫变换实现
    """

    def __init__(self, n_angles=36):
        """
        初始化

        Args:
            n_angles: 梯度方向的量化级数
        """
        self.n_angles = n_angles
        self.r_table = {i: [] for i in range(n_angles)}
        self.reference_point = None
        self.template_shape = None

    def _angle_to_index(self, angle):
        """将角度转换为R-table索引"""
        # 将角度归一化到[0, 2π)
        angle = angle % (2 * np.pi)
        # 转换为索引
        index = int(angle / (2 * np.pi) * self.n_angles) % self.n_angles
        return index

    def build_r_table(self, template_image, reference_point=None):
        """
        构建R-table

        Args:
            template_image: 模板图像（二值边缘）
            reference_point: 参考点（默认为中心）
        """
        height, width = template_image.shape
        self.template_shape = (height, width)

        # 设置参考点
        if reference_point is None:
            # 使用质心作为参考点
            y_coords, x_coords = np.nonzero(template_image)
            self.reference_point = (np.mean(x_coords), np.mean(y_coords))
        else:
            self.reference_point = reference_point

        # 计算梯度
        grad_x = cv2.Sobel(template_image.astype(np.float32), cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(template_image.astype(np.float32), cv2.CV_64F, 0, 1, ksize=3)

        # 获取边缘点
        y_coords, x_coords = np.nonzero(template_image)

        # 构建R-table
        self.r_table = {i: [] for i in range(self.n_angles)}

        for x, y in zip(x_coords, y_coords):
            # 计算梯度方向
            gx = grad_x[y, x]
            gy = grad_y[y, x]
            grad_mag = np.sqrt(gx**2 + gy**2)

            if grad_mag > 1e-6:
                grad_angle = np.arctan2(gy, gx)
                # 计算相对向量
                rx = self.reference_point[0] - x
                ry = self.reference_point[1] - y

                # 存入R-table
                angle_idx = self._angle_to_index(grad_angle)
                self.r_table[angle_idx].append((rx, ry))

    def detect(self, test_image, threshold=0.5):
        """
        在测试图像中检测模板

        Args:
            test_image: 测试图像（灰度）
            threshold: 检测阈值

        Returns:
            detections: 检测结果列表 [(x, y, score), ...]
        """
        # 边缘检测
        edges = canny(test_image, sigma=2)

        # 计算梯度
        grad_x = cv2.Sobel(test_image.astype(np.float32), cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(test_image.astype(np.float32), cv2.CV_64F, 0, 1, ksize=3)

        # 初始化累加器
        height, width = test_image.shape
        accumulator = np.zeros((height, width), dtype=np.float64)

        # 获取边缘点
        y_coords, x_coords = np.nonzero(edges)

        # 投票
        for x, y in zip(x_coords, y_coords):
            gx = grad_x[y, x]
            gy = grad_y[y, x]
            grad_mag = np.sqrt(gx**2 + gy**2)

            if grad_mag > 1e-6:
                grad_angle = np.arctan2(gy, gx)
                angle_idx = self._angle_to_index(grad_angle)

                # 从R-table获取偏移向量
                for rx, ry in self.r_table[angle_idx]:
                    cx = int(x + rx)
                    cy = int(y + ry)

                    if 0 <= cx < width and 0 <= cy < height:
                        accumulator[cy, cx] += 1

        # 归一化
        if len(self.r_table[0]) > 0:
            max_votes = max(len(v) for v in self.r_table.values())
            accumulator = accumulator / max_votes

        # 检测峰值
        detections = []
        threshold_val = threshold * np.max(accumulator)

        acc_copy = accumulator.copy()
        while np.max(acc_copy) > threshold_val:
            cy, cx = np.unravel_index(np.argmax(acc_copy), acc_copy.shape)
            score = acc_copy[cy, cx]
            detections.append((cx, cy, score))

            # 非极大值抑制
            radius = 20
            y_min = max(0, cy - radius)
            y_max = min(height, cy + radius)
            x_min = max(0, cx - radius)
            x_max = min(width, cx + radius)
            acc_copy[y_min:y_max, x_min:x_max] = 0

        return detections, accumulator, edges


# ============================================================================
# 4. 3D霍夫变换 - 平面检测
# ============================================================================

def hough_plane_3d(points, theta_res=10, phi_res=10, rho_res=0.1):
    """
    3D点云中的平面检测（霍夫变换）

    Args:
        points: 点云 (N, 3)
        theta_res: theta角度分辨率(度)
        phi_res: phi角度分辨率(度)
        rho_res: 距离分辨率

    Returns:
        planes: 检测到的平面列表 [(nx, ny, nz, rho), ...]
        accumulator: 累加器
    """
    # 参数空间范围
    thetas = np.deg2rad(np.arange(0, 180, theta_res))
    phis = np.deg2rad(np.arange(0, 360, phi_res))

    # 计算最大距离
    max_dist = np.max(np.linalg.norm(points, axis=1))
    rhos = np.arange(-max_dist, max_dist, rho_res)

    # 初始化累加器
    accumulator = np.zeros((len(thetas), len(phis), len(rhos)), dtype=np.uint64)

    # 投票
    for point in points:
        x, y, z = point

        for i, theta in enumerate(thetas):
            for j, phi in enumerate(phis):
                # 法向量
                nx = np.sin(theta) * np.cos(phi)
                ny = np.sin(theta) * np.sin(phi)
                nz = np.cos(theta)

                # 计算rho
                rho = nx * x + ny * y + nz * z

                # 找到最近的rho索引
                k = np.argmin(np.abs(rhos - rho))
                accumulator[i, j, k] += 1

    # 找峰值
    planes = []
    threshold = 0.3 * np.max(accumulator)
    acc_copy = accumulator.copy()

    while np.max(acc_copy) > threshold:
        idx = np.unravel_index(np.argmax(acc_copy), acc_copy.shape)
        i, j, k = idx

        theta = thetas[i]
        phi = phis[j]
        rho = rhos[k]

        # 计算法向量
        nx = np.sin(theta) * np.cos(phi)
        ny = np.sin(theta) * np.sin(phi)
        nz = np.cos(theta)

        planes.append((nx, ny, nz, rho))

        # 非极大值抑制
        i_min, i_max = max(0, i-2), min(len(thetas), i+3)
        j_min, j_max = max(0, j-2), min(len(phis), j+3)
        k_min, k_max = max(0, k-2), min(len(rhos), k+3)
        acc_copy[i_min:i_max, j_min:j_max, k_min:k_max] = 0

    return planes, accumulator


def visualize_plane(points, plane_params):
    """
    可视化平面和点云

    Args:
        points: 点云 (N, 3)
        plane_params: 平面参数 (nx, ny, nz, rho)
    """
    nx, ny, nz, rho = plane_params

    # 创建平面网格
    xx, yy = np.meshgrid(
        np.linspace(points[:, 0].min(), points[:, 0].max(), 20),
        np.linspace(points[:, 1].min(), points[:, 1].max(), 20)
    )

    # 计算z值: nx*x + ny*y + nz*z = rho => z = (rho - nx*x - ny*y) / nz
    if abs(nz) > 1e-6:
        zz = (rho - nx * xx - ny * yy) / nz
    else:
        zz = np.zeros_like(xx)

    return xx, yy, zz


# ============================================================================
# 5. 演示函数
# ============================================================================

def create_test_image_with_lines():
    """创建带有直线的测试图像"""
    image = np.zeros((200, 200), dtype=np.uint8)

    # 添加几条直线
    rr, cc = draw.line(20, 20, 180, 80)
    image[rr, cc] = 255

    rr, cc = draw.line(20, 180, 180, 120)
    image[rr, cc] = 255

    rr, cc = draw.line(50, 50, 150, 50)
    image[rr, cc] = 255

    # 添加一些噪声
    noise = np.random.rand(200, 200) > 0.98
    image[noise] = 255

    return image


def create_test_image_with_circles():
    """创建带有圆形的测试图像"""
    image = np.zeros((200, 200), dtype=np.uint8)

    # 添加几个圆
    rr, cc = circle_perimeter(60, 60, 30)
    image[rr, cc] = 255

    rr, cc = circle_perimeter(140, 140, 40)
    image[rr, cc] = 255

    rr, cc = circle_perimeter(100, 100, 25)
    image[rr, cc] = 255

    return image


def demonstrate_hough_lines():
    """演示霍夫直线检测"""
    print("=" * 60)
    print("霍夫直线检测演示")
    print("=" * 60)

    # 创建测试图像
    image = create_test_image_with_lines()

    # 边缘检测
    edges = canny(image, sigma=2)

    # 使用skimage进行检测
    peaks, edges_sk, accumulator, angles, distances = detect_lines_skimage(image)

    print(f"检测到 {len(peaks[0])} 条直线")

    # 可视化
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # 原图
    axes[0].imshow(image, cmap='gray')
    axes[0].set_title('Original Image')
    axes[0].axis('off')

    # 边缘图像
    axes[1].imshow(edges, cmap='gray')
    axes[1].set_title('Edge Detection')
    axes[1].axis('off')

    # 检测结果
    axes[2].imshow(image, cmap='gray')

    for _, angle, dist in zip(*peaks):
        y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
        y1 = (dist - image.shape[1] * np.cos(angle)) / np.sin(angle)
        axes[2].plot((0, image.shape[1]), (y0, y1), '-r')

    axes[2].set_title('Detected Lines')
    axes[2].set_xlim((0, image.shape[1]))
    axes[2].set_ylim((image.shape[0], 0))
    axes[2].axis('off')

    plt.tight_layout()
    plt.savefig('hough_lines_result.png', dpi=150, bbox_inches='tight')
    show_or_close()


def demonstrate_hough_circles():
    """演示霍夫圆检测"""
    print("\n" + "=" * 60)
    print("霍夫圆检测演示")
    print("=" * 60)

    # 创建测试图像
    image = create_test_image_with_circles()

    # 霍夫圆检测
    centers, edges, accumulator = hough_circle_transform(image, (20, 50), sigma=2)

    print(f"检测到 {len(centers)} 个圆")

    # 可视化
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # 原图
    axes[0].imshow(image, cmap='gray')
    axes[0].set_title('Original Image')
    axes[0].axis('off')

    # 边缘图像
    axes[1].imshow(edges, cmap='gray')
    axes[1].set_title('Edge Detection')
    axes[1].axis('off')

    # 检测结果
    axes[2].imshow(image, cmap='gray')

    for cx, cy, radius in centers:
        circle = plt.Circle((cx, cy), radius, color='red', fill=False, linewidth=2)
        axes[2].add_patch(circle)
        axes[2].plot(cx, cy, 'ro', markersize=5)

    axes[2].set_title('Detected Circles')
    axes[2].axis('off')

    plt.tight_layout()
    plt.savefig('hough_circles_result.png', dpi=150, bbox_inches='tight')
    show_or_close()


def demonstrate_accumulator_space():
    """演示累加器空间"""
    print("\n" + "=" * 60)
    print("累加器空间可视化")
    print("=" * 60)

    # 创建测试图像
    image = create_test_image_with_lines()
    edges = canny(image, sigma=2)

    # 计算累加器
    accumulator, thetas, rhos = hough_line(edges, theta=np.linspace(-np.pi/2, np.pi/2, 180))

    # 可视化
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # 边缘图像
    axes[0].imshow(edges, cmap='gray')
    axes[0].set_title('Edge Image')
    axes[0].axis('off')

    # 累加器空间 - 原始（hot colormap）
    im1 = axes[1].imshow(accumulator, cmap='hot', aspect='auto',
                         extent=[np.rad2deg(thetas[-1]), np.rad2deg(thetas[0]), rhos[-1], rhos[0]],
                         vmin=0, vmax=np.max(accumulator)*0.8)
    axes[1].set_title('Hough Accumulator (hot)')
    axes[1].set_xlabel('Angle (degrees)')
    axes[1].set_ylabel('Distance (pixels)')
    fig.colorbar(im1, ax=axes[1], shrink=0.8)

    # 标记峰值
    peaks = hough_line_peaks(accumulator, thetas, rhos, threshold=0.5*np.max(accumulator))
    for _, angle, dist in zip(*peaks):
        axes[1].plot(np.rad2deg(angle), dist, 'co', markersize=10, markeredgecolor='white')

    # 累加器空间 - 使用viridis colormap + 浅色背景
    # 创建一个带浅色背景的版本
    acc_display = accumulator.astype(float)
    acc_normalized = acc_display / (np.max(acc_display) + 1e-10)  # 归一化到[0,1]

    im2 = axes[2].imshow(acc_normalized, cmap='viridis', aspect='auto',
                         extent=[np.rad2deg(thetas[-1]), np.rad2deg(thetas[0]), rhos[-1], rhos[0]],
                         vmin=0, vmax=1)
    axes[2].set_title('Hough Accumulator (viridis, normalized)')
    axes[2].set_xlabel('Angle (degrees)')
    axes[2].set_ylabel('Distance (pixels)')
    fig.colorbar(im2, ax=axes[2], shrink=0.8)

    # 标记峰值
    for _, angle, dist in zip(*peaks):
        axes[2].plot(np.rad2deg(angle), dist, 'ro', markersize=10, markeredgecolor='white')

    plt.tight_layout()
    plt.savefig('hough_accumulator.png', dpi=150, bbox_inches='tight')
    show_or_close()


def demonstrate_generalized_hough():
    """演示广义霍夫变换"""
    print("\n" + "=" * 60)
    print("广义霍夫变换演示")
    print("=" * 60)

    # 创建模板（简单形状：矩形）
    template = np.zeros((100, 100), dtype=np.uint8)
    template[30:70, 30:70] = 255

    # 创建测试图像（包含旋转和噪声）
    test_image = np.zeros((200, 200), dtype=np.uint8)

    # 添加模板的变换版本
    test_image[50:90, 30:70] = 255  # 原始位置
    test_image[100:140, 100:140] = 255  # 另一个位置

    # 添加噪声
    noise = np.random.rand(200, 200) > 0.97
    test_image[noise] = 255

    # 构建GHT
    ght = GeneralizedHoughTransform(n_angles=36)
    template_edges = canny(template, sigma=1)
    ght.build_r_table(template_edges)

    # 检测
    detections, accumulator, edges = ght.detect(test_image, threshold=0.3)

    print(f"检测到 {len(detections)} 个目标")

    # 可视化
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))

    # 模板
    axes[0].imshow(template, cmap='gray')
    axes[0].set_title('Template')
    axes[0].axis('off')

    # 测试图像
    axes[1].imshow(test_image, cmap='gray')
    axes[1].set_title('Test Image')
    axes[1].axis('off')

    # 边缘
    axes[2].imshow(edges, cmap='gray')
    axes[2].set_title('Edges')
    axes[2].axis('off')

    # 检测结果
    axes[3].imshow(test_image, cmap='gray')
    for cx, cy, score in detections:
        axes[3].plot(cx, cy, 'ro', markersize=10)
        axes[3].annotate(f'{score:.2f}', (cx, cy), color='yellow',
                         fontsize=10, ha='center', va='bottom')

    axes[3].set_title(f'Detections: {len(detections)}')
    axes[3].axis('off')

    plt.tight_layout()
    plt.savefig('hough_ght_result.png', dpi=150, bbox_inches='tight')
    show_or_close()


def demonstrate_3d_plane_detection():
    """演示3D平面检测"""
    print("\n" + "=" * 60)
    print("3D平面检测演示")
    print("=" * 60)

    # 生成平面点云 + 噪声
    np.random.seed(42)

    # 平面1: z = 0.5x + 0.3y + 1
    x1 = np.random.rand(200) * 10
    y1 = np.random.rand(200) * 10
    z1 = 0.5 * x1 + 0.3 * y1 + 1 + np.random.randn(200) * 0.1
    points1 = np.column_stack([x1, y1, z1])

    # 平面2: z = -0.2x + 0.4y + 5
    x2 = np.random.rand(150) * 10
    y2 = np.random.rand(150) * 10
    z2 = -0.2 * x2 + 0.4 * y2 + 5 + np.random.randn(150) * 0.1
    points2 = np.column_stack([x2, y2, z2])

    # 离群点
    noise_points = np.random.rand(50, 3) * 10

    # 合并
    points = np.vstack([points1, points2, noise_points])

    # 3D霍夫变换检测平面
    print("执行3D霍夫变换（可能较慢）...")
    planes, accumulator = hough_plane_3d(points, theta_res=15, phi_res=15, rho_res=0.5)

    print(f"检测到 {len(planes)} 个平面")
    for i, (nx, ny, nz, rho) in enumerate(planes):
        print(f"  平面{i+1}: {nx:.3f}x + {ny:.3f}y + {nz:.3f}z = {rho:.3f}")

    # 可视化
    fig = plt.figure(figsize=(12, 5))

    # 点云
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.scatter(points[:, 0], points[:, 1], points[:, 2], c='blue', s=10, alpha=0.5)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title('Point Cloud')

    # 点云 + 检测到的平面
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.scatter(points[:, 0], points[:, 1], points[:, 2], c='blue', s=10, alpha=0.3)

    colors = ['red', 'green', 'blue']
    for i, plane_params in enumerate(planes[:3]):
        xx, yy, zz = visualize_plane(points, plane_params)
        ax2.plot_surface(xx, yy, zz, alpha=0.3, color=colors[i % len(colors)])

    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    ax2.set_title('Detected Planes')

    plt.tight_layout()
    plt.savefig('hough_3d_planes.png', dpi=150, bbox_inches='tight')
    show_or_close()


def demonstrate_comparison_with_ransac():
    """演示霍夫变换与RANSAC的比较"""
    print("\n" + "=" * 60)
    print("霍夫变换 vs RANSAC 比较")
    print("=" * 60)

    # 创建带噪声和离群点的直线数据
    np.random.seed(42)

    # 内点
    n_inliers = 100
    x_inliers = np.random.rand(n_inliers) * 100
    y_inliers = 2 * x_inliers + 10 + np.random.randn(n_inliers) * 2

    # 离群点
    n_outliers = 50
    x_outliers = np.random.rand(n_outliers) * 100
    y_outliers = np.random.rand(n_outliers) * 200

    # 合并
    points = np.column_stack([
        np.concatenate([x_inliers, x_outliers]),
        np.concatenate([y_inliers, y_outliers])
    ])

    # 创建图像（用于霍夫变换）
    image = np.zeros((250, 110), dtype=np.uint8)
    for x, y in points:
        ix, iy = int(x), int(y)
        if 0 <= ix < 110 and 0 <= iy < 250:
            image[iy, ix] = 255

    # 霍夫变换
    edges = canny(image, sigma=1)
    peaks, _, accumulator, angles, distances = detect_lines_skimage(image)

    print(f"霍夫变换检测到 {len(peaks[0])} 条直线")

    # 可视化比较
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # 原始数据
    axes[0].scatter(points[:, 0], points[:, 1], c='blue', s=10)
    axes[0].set_title('Original Data')
    axes[0].set_xlabel('X')
    axes[0].set_ylabel('Y')
    axes[0].grid(True)

    # 霍夫变换结果
    axes[1].imshow(image, cmap='gray', origin='lower')
    for _, angle, dist in zip(*peaks):
        y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
        y1 = (dist - 110 * np.cos(angle)) / np.sin(angle)
        axes[1].plot([0, 110], [y0, y1], '-r', linewidth=2)
    axes[1].set_title('Hough Transform')
    axes[1].axis('off')

    # 累加器
    axes[2].imshow(accumulator, cmap='hot', aspect='auto',
                   extent=[np.rad2deg(angles[-1]), np.rad2deg(angles[0]),
                           distances[-1], distances[0]])
    axes[2].set_title('Accumulator Space')
    axes[2].set_xlabel('Angle (degrees)')
    axes[2].set_ylabel('Distance (pixels)')

    plt.tight_layout()
    plt.savefig('hough_vs_ransac.png', dpi=150, bbox_inches='tight')
    show_or_close()


def demo(show=False):
    """运行所有演示"""
    global SHOW_PLOTS
    SHOW_PLOTS = show

    print("\n")
    print("*" * 60)
    print("*" + " " * 20 + "霍夫投票算法演示" + " " * 20 + "*")
    print("*" * 60)

    demonstrate_hough_lines()
    demonstrate_hough_circles()
    demonstrate_accumulator_space()
    demonstrate_generalized_hough()
    demonstrate_3d_plane_detection()
    demonstrate_comparison_with_ransac()

    print("\n所有演示完成！")
    print("生成的图像文件：")
    print("  - hough_lines_result.png")
    print("  - hough_circles_result.png")
    print("  - hough_accumulator.png")
    print("  - hough_ght_result.png")
    print("  - hough_3d_planes.png")
    print("  - hough_vs_ransac.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='霍夫投票算法演示')
    parser.add_argument('--show', '-s', action='store_true',
                        help='显示图形窗口（默认只保存图片）')
    args = parser.parse_args()

    demo(show=args.show)
