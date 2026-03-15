"""
几何算法示例：RANSAC, 凸包, KD-Tree
"""
import numpy as np
from scipy.spatial import KDTree, ConvexHull
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def ransac_line(points, n_iterations=100, threshold=0.1, min_inliers=10):
    """
    RANSAC直线拟合

    Args:
        points: 点集 (N, 2)
        n_iterations: 迭代次数
        threshold: 内点阈值
        min_inliers: 最小内点数

    Returns:
        best_line: 最佳直线参数 [a, b, c] (ax + by + c = 0)
        best_inliers: 内点索引
    """
    best_inliers = []
    best_line = None

    for _ in range(n_iterations):
        # 随机选2个点
        idx = np.random.choice(len(points), 2, replace=False)
        p1, p2 = points[idx]

        # 计算直线参数 ax + by + c = 0
        a = p2[1] - p1[1]
        b = p1[0] - p2[0]
        c = p2[0] * p1[1] - p1[0] * p2[1]

        # 归一化
        norm = np.sqrt(a**2 + b**2)
        if norm < 1e-10:
            continue
        a, b, c = a/norm, b/norm, c/norm

        # 计算所有点到直线的距离
        distances = np.abs(a * points[:, 0] + b * points[:, 1] + c)

        # 统计内点
        inliers = np.where(distances < threshold)[0]

        if len(inliers) > len(best_inliers):
            best_inliers = inliers
            best_line = [a, b, c]

    return best_line, best_inliers


def ransac_plane(points, n_iterations=100, threshold=0.1):
    """
    RANSAC平面拟合

    Args:
        points: 点集 (N, 3)
        n_iterations: 迭代次数
        threshold: 内点阈值

    Returns:
        best_plane: 最佳平面参数 [a, b, c, d] (ax + by + cz + d = 0)
        best_inliers: 内点索引
    """
    best_inliers = []
    best_plane = None

    for _ in range(n_iterations):
        # 随机选3个点
        idx = np.random.choice(len(points), 3, replace=False)
        p1, p2, p3 = points[idx]

        # 计算平面参数
        v1 = p2 - p1
        v2 = p3 - p1
        normal = np.cross(v1, v2)

        norm = np.linalg.norm(normal)
        if norm < 1e-10:
            continue
        normal = normal / norm
        d = -np.dot(normal, p1)

        # 计算所有点到平面的距离
        distances = np.abs(points @ normal + d)

        # 统计内点
        inliers = np.where(distances < threshold)[0]

        if len(inliers) > len(best_inliers):
            best_inliers = inliers
            best_plane = [normal[0], normal[1], normal[2], d]

    return best_plane, best_inliers


def graham_scan(points):
    """
    Graham扫描算法求2D凸包

    Args:
        points: 点集 (N, 2)

    Returns:
        hull_points: 凸包顶点
    """
    # 找最低点
    start = points[np.argmin(points[:, 1])]

    # 按极角排序
    def polar_angle(p):
        return np.arctan2(p[1] - start[1], p[0] - start[0])

    sorted_indices = np.argsort([polar_angle(p) for p in points])
    sorted_points = points[sorted_indices]

    # 构建凸包
    hull = [sorted_points[0], sorted_points[1]]

    for p in sorted_points[2:]:
        while len(hull) >= 2:
            v1 = hull[-1] - hull[-2]
            v2 = p - hull[-1]
            cross = v1[0] * v2[1] - v1[1] * v2[0]

            if cross <= 0:  # 右转，弹出
                hull.pop()
            else:
                break
        hull.append(p)

    return np.array(hull)


def demonstrate_ransac():
    """演示RANSAC"""
    print("=" * 50)
    print("RANSAC 直线拟合演示")
    print("=" * 50)

    # 生成带噪声的直线数据
    np.random.seed(42)
    n_inliers = 80
    n_outliers = 20

    # 内点：y = 2x + 1 + 噪声
    x_inliers = np.random.rand(n_inliers) * 10
    y_inliers = 2 * x_inliers + 1 + np.random.randn(n_inliers) * 0.5

    # 离群点
    x_outliers = np.random.rand(n_outliers) * 10
    y_outliers = np.random.rand(n_outliers) * 20

    # 合并
    points = np.vstack([
        np.column_stack([x_inliers, y_inliers]),
        np.column_stack([x_outliers, y_outliers])
    ])

    # RANSAC拟合
    line, inliers = ransac_line(points, n_iterations=100, threshold=1.0)

    print(f"拟合直线: {line[0]:.4f}x + {line[1]:.4f}y + {line[2]:.4f} = 0")
    print(f"内点数: {len(inliers)}")

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 6))

    # 所有点
    ax.scatter(points[:, 0], points[:, 1], c='lightgray', s=30, label='所有点')

    # 内点
    ax.scatter(points[inliers, 0], points[inliers, 1], c='blue', s=30, label='内点')

    # 拟合直线
    x_line = np.array([0, 10])
    y_line = -(line[0] * x_line + line[2]) / line[1]
    ax.plot(x_line, y_line, 'r-', linewidth=2, label='RANSAC拟合')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('RANSAC直线拟合')
    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    plt.show()


def demonstrate_convex_hull():
    """演示凸包"""
    print("\n" + "=" * 50)
    print("凸包算法演示")
    print("=" * 50)

    # 生成随机点
    np.random.seed(42)
    points = np.random.rand(50, 2) * 10

    # Graham扫描
    hull_points = graham_scan(points)

    print(f"输入点数: {len(points)}")
    print(f"凸包顶点数: {len(hull_points)}")

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 8))

    # 所有点
    ax.scatter(points[:, 0], points[:, 1], c='blue', s=30, label='输入点')

    # 凸包
    hull_closed = np.vstack([hull_points, hull_points[0]])
    ax.plot(hull_closed[:, 0], hull_closed[:, 1], 'r-', linewidth=2, label='凸包')
    ax.scatter(hull_points[:, 0], hull_points[:, 1], c='red', s=50, zorder=5)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('2D凸包 (Graham扫描)')
    ax.legend()
    ax.grid(True)
    ax.set_aspect('equal')

    plt.tight_layout()
    plt.show()


def demonstrate_kdtree():
    """演示KD-Tree"""
    print("\n" + "=" * 50)
    print("KD-Tree 最近邻搜索演示")
    print("=" * 50)

    # 生成随机点
    np.random.seed(42)
    points = np.random.rand(1000, 2) * 10

    # 构建KD-Tree
    tree = KDTree(points)

    # 查询点
    query_point = np.array([5, 5])

    # 查询最近的k个点
    k = 5
    distances, indices = tree.query(query_point, k=k)

    print(f"查询点: {query_point}")
    print(f"最近{k}个点:")
    for i, (d, idx) in enumerate(zip(distances, indices)):
        print(f"  {i+1}. 点{idx}: {points[idx]}, 距离={d:.4f}")

    # 范围查询
    radius = 1.5
    indices_radius = tree.query_ball_point(query_point, radius)
    print(f"\n半径{radius}内的点数: {len(indices_radius)}")

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 8))

    # 所有点
    ax.scatter(points[:, 0], points[:, 1], c='lightgray', s=10, label='所有点')

    # 范围内的点
    ax.scatter(points[indices_radius, 0], points[indices_radius, 1],
               c='green', s=30, alpha=0.5, label=f'半径{radius}内')

    # 最近k个点
    ax.scatter(points[indices, 0], points[indices, 1],
               c='blue', s=50, label=f'最近{k}个点')

    # 查询点
    ax.scatter(*query_point, c='red', s=100, marker='*', zorder=5, label='查询点')

    # 搜索圆
    circle = plt.Circle(query_point, radius, fill=False, color='green', linestyle='--')
    ax.add_patch(circle)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('KD-Tree最近邻搜索')
    ax.legend()
    ax.grid(True)
    ax.set_aspect('equal')

    plt.tight_layout()
    plt.show()


def demo():
    """运行所有演示"""
    demonstrate_ransac()
    demonstrate_convex_hull()
    demonstrate_kdtree()


if __name__ == "__main__":
    demo()
