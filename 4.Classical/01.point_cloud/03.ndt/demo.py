"""
NDT (Normal Distributions Transform) 点云配准算法示例
"""
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Voxel:
    """NDT体素单元"""
    def __init__(self):
        self.points = []
        self.mean = None
        self.cov = None
        self.cov_inv = None
        self.valid = False

    def add_point(self, point):
        """添加点"""
        self.points.append(point)

    def compute_distribution(self, min_points=3):
        """计算正态分布参数"""
        if len(self.points) < min_points:
            self.valid = False
            return

        points = np.array(self.points)
        self.mean = np.mean(points, axis=0)

        # 计算协方差矩阵
        centered = points - self.mean
        self.cov = (centered.T @ centered) / len(points)

        # 添加正则化以避免奇异矩阵
        self.cov += np.eye(3) * 0.01

        try:
            self.cov_inv = np.linalg.inv(self.cov)
            self.valid = True
        except np.linalg.LinAlgError:
            self.valid = False

    def probability(self, point):
        """计算点在此体素中的概率"""
        if not self.valid:
            return 0.0

        diff = point - self.mean
        mahal = diff @ self.cov_inv @ diff

        # 正态分布概率密度
        det = np.linalg.det(self.cov)
        prob = np.exp(-0.5 * mahal) / (np.sqrt((2 * np.pi) ** 3 * det))

        return prob

    def gradient_hessian(self, point):
        """计算梯度和Hessian贡献"""
        if not self.valid:
            return None, None

        diff = point - self.mean
        prob = self.probability(point)

        # 梯度: -prob * Σ⁻¹ * (p - μ)
        grad = -prob * (self.cov_inv @ diff)

        # Hessian简化 (对角近似)
        hess = prob * self.cov_inv

        return grad, hess


class NDT:
    """NDT配准算法"""

    def __init__(self, voxel_size=1.0, min_points_per_voxel=3):
        self.voxel_size = voxel_size
        self.min_points_per_voxel = min_points_per_voxel
        self.voxels = {}

    def _get_voxel_index(self, point):
        """获取体素索引"""
        return tuple((point // self.voxel_size).astype(int))

    def set_target_cloud(self, points):
        """设置目标点云并构建NDT表示"""
        self.voxels = defaultdict(Voxel)

        # 将点分配到体素
        for p in points:
            idx = self._get_voxel_index(p)
            self.voxels[idx].add_point(p)

        # 计算每个体素的分布
        valid_count = 0
        for voxel in self.voxels.values():
            voxel.compute_distribution(self.min_points_per_voxel)
            if voxel.valid:
                valid_count += 1

        print(f"NDT构建完成: {len(self.voxels)} 个体素, {valid_count} 个有效")
        return valid_count

    def _transform_point(self, point, params):
        """
        应用变换
        params: [tx, ty, tz, roll, pitch, yaw]
        """
        tx, ty, tz, roll, pitch, yaw = params

        # 旋转矩阵 (简化版本)
        cr, sr = np.cos(roll), np.sin(roll)
        cp, sp = np.cos(pitch), np.sin(pitch)
        cy, sy = np.cos(yaw), np.sin(yaw)

        Rx = np.array([[1, 0, 0], [0, cr, -sr], [0, sr, cr]])
        Ry = np.array([[cp, 0, sp], [0, 1, 0], [-sp, 0, cp]])
        Rz = np.array([[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]])

        R = Rz @ Ry @ Rx

        return R @ point + np.array([tx, ty, tz])

    def _compute_score(self, points, params):
        """计算得分（对数似然）"""
        score = 0
        for p in points:
            p_transformed = self._transform_point(p, params)
            idx = self._get_voxel_index(p_transformed)

            if idx in self.voxels:
                prob = self.voxels[idx].probability(p_transformed)
                if prob > 1e-10:
                    score += np.log(prob)

        return score

    def _compute_gradient_and_hessian(self, points, params):
        """计算梯度和Hessian"""
        grad = np.zeros(6)
        hess = np.zeros((6, 6))

        for p in points:
            p_transformed = self._transform_point(p, params)
            idx = self._get_voxel_index(p_transformed)

            if idx not in self.voxels:
                continue

            voxel = self.voxels[idx]
            g, h = voxel.gradient_hessian(p_transformed)

            if g is not None:
                # 简化：只更新平移部分
                grad[:3] += g
                hess[:3, :3] += h

        return grad, hess

    def align(self, source_points, init_params=None, max_iterations=50, tolerance=1e-6):
        """
        执行NDT配准

        Args:
            source_points: 源点云
            init_params: 初始变换参数 [tx, ty, tz, roll, pitch, yaw]
            max_iterations: 最大迭代次数
            tolerance: 收敛阈值

        Returns:
            params: 最终变换参数
            scores: 每次迭代的得分
        """
        if init_params is None:
            init_params = np.zeros(6)

        params = np.array(init_params, dtype=float)
        scores = []

        for i in range(max_iterations):
            # 计算当前得分
            score = self._compute_score(source_points, params)
            scores.append(score)

            # 计算梯度和Hessian
            grad, hess = self._compute_gradient_and_hessian(source_points, params)

            # 添加阻尼
            hess += np.eye(6) * 0.1

            # 牛顿法更新
            try:
                delta = np.linalg.solve(hess, grad)
            except np.linalg.LinAlgError:
                delta = np.linalg.lstsq(hess, grad, rcond=None)[0]

            # 线搜索（简化版）
            step = 0.1
            params += step * delta

            # 检查收敛
            if i > 0 and abs(scores[-1] - scores[-2]) < tolerance:
                print(f"NDT收敛于第 {i+1} 次迭代")
                break

        return params, scores


def rotation_matrix(axis, angle):
    """生成旋转矩阵"""
    axis = axis / np.linalg.norm(axis)
    c, s = np.cos(angle), np.sin(angle)
    x, y, z = axis
    return np.array([
        [c + x*x*(1-c), x*y*(1-c) - z*s, x*z*(1-c) + y*s],
        [y*x*(1-c) + z*s, c + y*y*(1-c), y*z*(1-c) - x*s],
        [z*x*(1-c) - y*s, z*y*(1-c) + x*s, c + z*z*(1-c)]
    ])


def visualize_ndt(source, target, transformed, scores):
    """可视化NDT结果"""
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

    # 得分曲线
    ax3 = fig.add_subplot(133)
    ax3.plot(scores, 'b-o')
    ax3.set_xlabel('迭代次数')
    ax3.set_ylabel('对数似然得分')
    ax3.set_title('收敛曲线')
    ax3.grid(True)

    plt.tight_layout()
    plt.show()


def demo():
    """NDT演示"""
    print("=" * 50)
    print("NDT (Normal Distributions Transform) 点云配准演示")
    print("=" * 50)

    # 生成测试数据
    np.random.seed(42)
    n_points = 1000

    # 源点云：随机分布的点
    source = np.random.randn(n_points, 3) * 2

    # 目标点云：对源点云应用变换
    R_true = rotation_matrix([0, 0, 1], np.pi / 6) @ rotation_matrix([1, 0, 0], np.pi / 8)
    t_true = np.array([1.0, 0.5, 0.3])
    target = (R_true @ source.T).T + t_true

    # 添加噪声
    target += np.random.randn(*target.shape) * 0.1

    print(f"\n源点云点数: {len(source)}")
    print(f"目标点云点数: {len(target)}")
    print(f"真实变换:")
    print(f"  平移: {t_true}")

    # 创建NDT并设置目标点云
    ndt = NDT(voxel_size=0.8, min_points_per_voxel=3)
    ndt.set_target_cloud(target)

    # 执行配准
    print("\n运行 NDT...")
    params, scores = ndt.align(source, max_iterations=30)

    print(f"\n估计的变换参数:")
    print(f"  平移: [{params[0]:.4f}, {params[1]:.4f}, {params[2]:.4f}]")
    print(f"  旋转: [{params[3]:.4f}, {params[4]:.4f}, {params[5]:.4f}]")

    # 计算最终误差
    def apply_transform(points, params):
        tx, ty, tz, roll, pitch, yaw = params
        cr, sr = np.cos(roll), np.sin(roll)
        cp, sp = np.cos(pitch), np.sin(pitch)
        cy, sy = np.cos(yaw), np.sin(yaw)
        Rx = np.array([[1, 0, 0], [0, cr, -sr], [0, sr, cr]])
        Ry = np.array([[cp, 0, sp], [0, 1, 0], [-sp, 0, cp]])
        Rz = np.array([[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]])
        R = Rz @ Ry @ Rx
        return (R @ points.T).T + np.array([tx, ty, tz])

    transformed = apply_transform(source, params)
    final_error = np.mean(np.linalg.norm(transformed - target, axis=1))
    print(f"\n平均点距离误差: {final_error:.4f}")

    # 可视化
    visualize_ndt(source, target, transformed, scores)


if __name__ == "__main__":
    demo()
