"""
ICP (Iterative Closest Point) 点云配准算法示例
"""
import numpy as np
from scipy.spatial import KDTree
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def generate_test_point_cloud(n_points=100, noise=0.01):
    """生成测试点云（一个简单的平面）"""
    points = np.random.rand(n_points, 3)
    points[:, 2] = points[:, 0] * 0.5 + points[:, 1] * 0.3 + np.random.randn(n_points) * noise
    return points


def transform_points(points, R, t):
    """应用刚体变换"""
    return points @ R.T + t


def rotation_matrix(axis, angle):
    """生成绕指定轴的旋转矩阵"""
    axis = axis / np.linalg.norm(axis)
    c, s = np.cos(angle), np.sin(angle)
    x, y, z = axis
    return np.array([
        [c + x*x*(1-c), x*y*(1-c) - z*s, x*z*(1-c) + y*s],
        [y*x*(1-c) + z*s, c + y*y*(1-c), y*z*(1-c) - x*s],
        [z*x*(1-c) - y*s, z*y*(1-c) + x*s, c + z*z*(1-c)]
    ])


def find_correspondences(source, target, tree):
    """使用KDTree找最近点对应"""
    distances, indices = tree.query(source)
    return indices, distances


def compute_transformation(source, target):
    """使用SVD计算最优刚体变换"""
    # 计算质心
    centroid_s = np.mean(source, axis=0)
    centroid_t = np.mean(target, axis=0)

    # 去中心化
    source_centered = source - centroid_s
    target_centered = target - centroid_t

    # 计算协方差矩阵
    H = source_centered.T @ target_centered

    # SVD分解
    U, S, Vt = np.linalg.svd(H)

    # 计算旋转矩阵
    R = Vt.T @ U.T

    # 处理反射情况
    if np.linalg.det(R) < 0:
        Vt[-1, :] *= -1
        R = Vt.T @ U.T

    # 计算平移向量
    t = centroid_t - R @ centroid_s

    return R, t


def icp(source, target, max_iterations=50, tolerance=1e-6):
    """
    ICP算法实现

    Args:
        source: 源点云 (N, 3)
        target: 目标点云 (M, 3)
        max_iterations: 最大迭代次数
        tolerance: 收敛阈值

    Returns:
        R: 旋转矩阵 (3, 3)
        t: 平移向量 (3,)
        errors: 每次迭代的误差
    """
    # 构建目标点云的KDTree
    tree = KDTree(target)

    # 初始化
    R_total = np.eye(3)
    t_total = np.zeros(3)
    transformed_source = source.copy()
    errors = []

    for i in range(max_iterations):
        # 找对应点
        indices, distances = find_correspondences(transformed_source, target, tree)
        corresponding_target = target[indices]

        # 计算变换
        R, t = compute_transformation(transformed_source, corresponding_target)

        # 应用变换
        transformed_source = transform_points(transformed_source, R, t)

        # 累积变换
        t_total = R @ t_total + t
        R_total = R @ R_total

        # 计算误差
        error = np.mean(distances ** 2)
        errors.append(error)

        # 检查收敛
        if i > 0 and abs(errors[-2] - errors[-1]) < tolerance:
            print(f"ICP收敛于第 {i+1} 次迭代")
            break

    return R_total, t_total, errors


def icp_point_to_plane(source, target, normals, max_iterations=50, tolerance=1e-6):
    """
    Point-to-Plane ICP 变体
    最小化点到平面的距离，通常收敛更快
    """
    tree = KDTree(target)

    R_total = np.eye(3)
    t_total = np.zeros(3)
    transformed_source = source.copy()
    errors = []

    for i in range(max_iterations):
        indices, distances = find_correspondences(transformed_source, target, tree)
        corresponding_target = target[indices]
        corresponding_normals = normals[indices]

        # 构建线性系统 Ax = b
        # 其中 x = [tx, ty, tz, rx, ry, rz]
        A = []
        b = []

        for j in range(len(transformed_source)):
            p = transformed_source[j]
            q = corresponding_target[j]
            n = corresponding_normals[j]

            # 点到平面距离的雅可比
            row = [
                n[0], n[1], n[2],
                n[2] * p[1] - n[1] * p[2],
                n[0] * p[2] - n[2] * p[0],
                n[1] * p[0] - n[0] * p[1]
            ]
            A.append(row)
            b.append(np.dot(n, q - p))

        A = np.array(A)
        b = np.array(b)

        # 最小二乘求解
        x, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

        # 转换为旋转矩阵和平移向量
        t = x[:3]
        R = rotation_matrix([1, 0, 0], x[3]) @ rotation_matrix([0, 1, 0], x[4]) @ rotation_matrix([0, 0, 1], x[5])

        transformed_source = transform_points(transformed_source, R, t)
        t_total = R @ t_total + t
        R_total = R @ R_total

        error = np.mean(np.array(b) ** 2)
        errors.append(error)

        if i > 0 and abs(errors[-2] - errors[-1]) < tolerance:
            print(f"Point-to-Plane ICP收敛于第 {i+1} 次迭代")
            break

    return R_total, t_total, errors


def visualize_icp(source, target, transformed, errors):
    """可视化ICP结果"""
    fig = plt.figure(figsize=(15, 5))

    # 点云对比
    ax1 = fig.add_subplot(131, projection='3d')
    ax1.scatter(source[:, 0], source[:, 1], source[:, 2], c='r', s=1, label='Source')
    ax1.scatter(target[:, 0], target[:, 1], target[:, 2], c='b', s=1, label='Target')
    ax1.set_title('配准前')
    ax1.legend()

    ax2 = fig.add_subplot(132, projection='3d')
    ax2.scatter(transformed[:, 0], transformed[:, 1], transformed[:, 2], c='g', s=1, label='Transformed')
    ax2.scatter(target[:, 0], target[:, 1], target[:, 2], c='b', s=1, label='Target')
    ax2.set_title('配准后')
    ax2.legend()

    # 误差曲线
    ax3 = fig.add_subplot(133)
    ax3.plot(errors, 'b-o')
    ax3.set_xlabel('迭代次数')
    ax3.set_ylabel('MSE误差')
    ax3.set_title('收敛曲线')
    ax3.grid(True)

    plt.tight_layout()
    plt.show()


def demo():
    """ICP演示"""
    print("=" * 50)
    print("ICP (Iterative Closest Point) 点云配准演示")
    print("=" * 50)

    # 生成测试数据
    np.random.seed(42)
    source = generate_test_point_cloud(n_points=500, noise=0.02)

    # 创建目标点云（对源点云应用变换）
    R_true = rotation_matrix([0, 0, 1], np.pi / 6) @ rotation_matrix([1, 0, 0], np.pi / 8)
    t_true = np.array([0.5, 0.3, 0.1])
    target = transform_points(source, R_true, t_true)

    # 添加噪声
    target += np.random.randn(*target.shape) * 0.01

    print(f"\n源点云点数: {len(source)}")
    print(f"目标点云点数: {len(target)}")
    print(f"真实变换:")
    print(f"  旋转角度: {np.pi/6:.4f} (Z轴), {np.pi/8:.4f} (X轴)")
    print(f"  平移: {t_true}")

    # 运行ICP
    print("\n运行 ICP...")
    R_est, t_est, errors = icp(source, target, max_iterations=50)

    print(f"\n估计的变换:")
    print(f"  旋转矩阵:\n{R_est}")
    print(f"  平移向量: {t_est}")

    # 计算误差
    transformed = transform_points(source, R_est, t_est)
    final_error = np.mean(np.linalg.norm(transformed - target, axis=1) ** 2)
    print(f"\n最终MSE误差: {final_error:.6f}")

    # 可视化
    visualize_icp(source, target, transformed, errors)


if __name__ == "__main__":
    demo()
