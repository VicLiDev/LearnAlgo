"""
点云预处理算法示例
包括：体素滤波、离群点移除、法向量估计
"""
import numpy as np
from scipy.spatial import KDTree
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def voxel_grid_filter(points, voxel_size):
    """
    体素滤波降采样

    Args:
        points: 点云 (N, 3)
        voxel_size: 体素大小

    Returns:
        降采样后的点云
    """
    # 计算每个点所属的体素索引
    voxel_indices = (points // voxel_size).astype(int)

    # 找出唯一的体素
    unique_voxels = np.unique(voxel_indices, axis=0)

    # 对每个体素计算质心
    downsampled = []
    for voxel in unique_voxels:
        mask = np.all(voxel_indices == voxel, axis=1)
        points_in_voxel = points[mask]
        centroid = np.mean(points_in_voxel, axis=0)
        downsampled.append(centroid)

    return np.array(downsampled)


def random_downsample(points, ratio=0.5):
    """
    随机降采样

    Args:
        points: 点云 (N, 3)
        ratio: 保留比例

    Returns:
        降采样后的点云
    """
    n_points = len(points)
    n_sample = int(n_points * ratio)
    indices = np.random.choice(n_points, n_sample, replace=False)
    return points[indices]


def statistical_outlier_removal(points, k=30, std_ratio=1.0):
    """
    统计离群点移除 (SOR)

    Args:
        points: 点云 (N, 3)
        k: 最近邻数量
        std_ratio: 标准差倍数阈值

    Returns:
        过滤后的点云, 过滤掩码
    """
    # 构建KDTree
    tree = KDTree(points)

    # 计算每个点到k个最近邻的平均距离
    distances, _ = tree.query(points, k=k+1)  # +1 因为包含自己
    mean_distances = np.mean(distances[:, 1:], axis=1)  # 排除自己

    # 计算全局统计量
    global_mean = np.mean(mean_distances)
    global_std = np.std(mean_distances)

    # 设置阈值
    threshold = global_mean + std_ratio * global_std

    # 过滤
    mask = mean_distances < threshold
    return points[mask], mask


def radius_outlier_removal(points, radius=0.5, min_neighbors=5):
    """
    半径离群点移除

    Args:
        points: 点云 (N, 3)
        radius: 搜索半径
        min_neighbors: 最小邻居数

    Returns:
        过滤后的点云, 过滤掩码
    """
    tree = KDTree(points)

    # 查询每个点半径内的邻居数
    neighbors_count = tree.query_ball_point(points, radius, return_length=True)

    # 过滤
    mask = neighbors_count >= min_neighbors
    return points[mask], mask


def estimate_normals(points, k=30, view_point=None):
    """
    使用PCA估计法向量

    Args:
        points: 点云 (N, 3)
        k: 最近邻数量
        view_point: 视点位置，用于确定法向量方向

    Returns:
        法向量 (N, 3)
    """
    if view_point is None:
        view_point = np.array([0, 0, 0])

    tree = KDTree(points)
    normals = np.zeros_like(points)

    for i, point in enumerate(points):
        # 找k个最近邻
        _, indices = tree.query(point, k=k+1)
        neighbors = points[indices[1:]]  # 排除自己

        # 计算协方差矩阵
        centered = neighbors - np.mean(neighbors, axis=0)
        cov = centered.T @ centered / len(neighbors)

        # 特征值分解
        eigenvalues, eigenvectors = np.linalg.eigh(cov)

        # 最小特征值对应的特征向量即为法向量
        normal = eigenvectors[:, 0]
        normals[i] = normal

    # 确定法向量方向（朝向视点）
    view_direction = view_point - points
    dot_product = np.sum(normals * view_direction, axis=1)
    normals[dot_product < 0] *= -1

    return normals


def crop_box(points, min_bound, max_bound):
    """
    盒子裁剪

    Args:
        points: 点云 (N, 3)
        min_bound: 最小边界 [x_min, y_min, z_min]
        max_bound: 最大边界 [x_max, y_max, z_max]

    Returns:
        裁剪后的点云
    """
    mask = np.all((points >= min_bound) & (points <= max_bound), axis=1)
    return points[mask], mask


def add_noise(points, noise_level=0.05):
    """添加高斯噪声"""
    noise = np.random.randn(*points.shape) * noise_level
    return points + noise


def add_outliers(points, ratio=0.05, scale=1.0):
    """添加离群点"""
    n_outliers = int(len(points) * ratio)
    outliers = np.random.randn(n_outliers, 3) * scale
    return np.vstack([points, outliers])


def visualize_preprocessing(original, processed, title="预处理效果"):
    """可视化预处理结果"""
    fig = plt.figure(figsize=(12, 5))

    ax1 = fig.add_subplot(121, projection='3d')
    ax1.scatter(original[:, 0], original[:, 1], original[:, 2], c='b', s=1)
    ax1.set_title(f'原始点云 ({len(original)} 点)')

    ax2 = fig.add_subplot(122, projection='3d')
    ax2.scatter(processed[:, 0], processed[:, 1], processed[:, 2], c='r', s=1)
    ax2.set_title(f'处理后点云 ({len(processed)} 点)')

    plt.suptitle(title)
    plt.tight_layout()
    plt.show()


def visualize_normals(points, normals, sample_rate=10):
    """可视化法向量"""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # 采样显示
    indices = np.arange(0, len(points), sample_rate)
    sample_points = points[indices]
    sample_normals = normals[indices]

    # 绘制点
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], c='b', s=1, alpha=0.3)

    # 绘制法向量
    ax.quiver(
        sample_points[:, 0], sample_points[:, 1], sample_points[:, 2],
        sample_normals[:, 0] * 0.1, sample_normals[:, 1] * 0.1, sample_normals[:, 2] * 0.1,
        color='r', arrow_length_ratio=0.3
    )

    ax.set_title(f'法向量可视化 (每{sample_rate}个点显示一个)')
    plt.show()


def demo_voxel_filter():
    """体素滤波演示"""
    print("=" * 50)
    print("体素滤波 (Voxel Grid Filter) 演示")
    print("=" * 50)

    # 生成测试点云
    np.random.seed(42)
    points = np.random.randn(10000, 3) * 2

    print(f"\n原始点云: {len(points)} 点")

    # 体素滤波
    voxel_size = 0.2
    filtered = voxel_grid_filter(points, voxel_size)

    print(f"体素大小: {voxel_size}")
    print(f"滤波后: {len(filtered)} 点")
    print(f"压缩率: {len(filtered)/len(points)*100:.1f}%")

    visualize_preprocessing(points, filtered, "体素滤波")


def demo_outlier_removal():
    """离群点移除演示"""
    print("\n" + "=" * 50)
    print("离群点移除演示")
    print("=" * 50)

    # 生成带噪声和离群点的点云
    np.random.seed(42)
    clean_points = np.random.randn(2000, 3)
    noisy_points = add_noise(clean_points, 0.02)
    points_with_outliers = add_outliers(noisy_points, ratio=0.05, scale=2.0)

    print(f"\n原始点云(含离群点): {len(points_with_outliers)} 点")

    # 统计离群点移除
    sor_filtered, sor_mask = statistical_outlier_removal(
        points_with_outliers, k=20, std_ratio=1.5
    )
    print(f"\nSOR过滤后: {len(sor_filtered)} 点")
    print(f"移除: {len(points_with_outliers) - len(sor_filtered)} 点")

    # 半径离群点移除
    ror_filtered, ror_mask = radius_outlier_removal(
        points_with_outliers, radius=0.3, min_neighbors=10
    )
    print(f"\n半径过滤后: {len(ror_filtered)} 点")
    print(f"移除: {len(points_with_outliers) - len(ror_filtered)} 点")

    visualize_preprocessing(points_with_outliers, sor_filtered, "统计离群点移除 (SOR)")


def demo_normals():
    """法向量估计演示"""
    print("\n" + "=" * 50)
    print("法向量估计演示")
    print("=" * 50)

    # 生成平面点云
    np.random.seed(42)
    n_points = 2000
    points = np.random.rand(n_points, 3) * 2
    points[:, 2] = points[:, 0] * 0.3 + points[:, 1] * 0.2 + np.random.randn(n_points) * 0.02

    print(f"\n点云: {len(points)} 点")
    print("估计法向量中...")

    normals = estimate_normals(points, k=30)

    print(f"法向量形状: {normals.shape}")
    print(f"前5个法向量:\n{normals[:5]}")

    # 验证法向量（平面应该接近 [0, 0, 1]）
    mean_normal = np.mean(normals, axis=0)
    mean_normal = mean_normal / np.linalg.norm(mean_normal)
    print(f"\n平均法向量: {mean_normal}")

    visualize_normals(points, normals, sample_rate=20)


def demo_preprocessing_pipeline():
    """完整预处理流程演示"""
    print("\n" + "=" * 50)
    print("完整预处理流程演示")
    print("=" * 50)

    # 生成原始数据
    np.random.seed(42)
    clean_points = np.random.randn(5000, 3) * 2
    noisy_points = add_noise(clean_points, 0.03)
    points = add_outliers(noisy_points, ratio=0.08, scale=3.0)

    print(f"\n1. 原始点云: {len(points)} 点")

    # 裁剪
    cropped, _ = crop_box(points, np.array([-3, -3, -3]), np.array([3, 3, 3]))
    print(f"2. 裁剪后: {len(cropped)} 点")

    # 离群点移除
    filtered, _ = statistical_outlier_removal(cropped, k=20, std_ratio=1.5)
    print(f"3. SOR后: {len(filtered)} 点")

    # 体素滤波
    downsampled = voxel_grid_filter(filtered, voxel_size=0.15)
    print(f"4. 体素滤波后: {len(downsampled)} 点")

    # 法向量估计
    normals = estimate_normals(downsampled, k=30)
    print(f"5. 法向量估计完成")

    print(f"\n总体压缩率: {len(downsampled)/len(points)*100:.1f}%")

    visualize_preprocessing(points, downsampled, "预处理流程")


def demo():
    """运行所有演示"""
    demo_voxel_filter()
    demo_outlier_removal()
    demo_normals()
    demo_preprocessing_pipeline()


if __name__ == "__main__":
    demo()
