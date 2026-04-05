"""
矩阵运算示例：SVD、特征分解、LU分解、QR分解
"""
import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt


def demonstrate_svd():
    """演示SVD分解"""
    print("=" * 50)
    print("SVD (奇异值分解)")
    print("=" * 50)

    # 创建示例矩阵
    A = np.array([
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12]
    ], dtype=float)

    print(f"原矩阵 A ({A.shape[0]}×{A.shape[1]}):")
    print(A)

    # SVD分解
    U, S, Vt = np.linalg.svd(A, full_matrices=False)

    print(f"\nU ({U.shape}):")
    print(np.round(U, 4))

    print(f"\n奇异值 S: {np.round(S, 4)}")

    print(f"\nV^T ({Vt.shape}):")
    print(np.round(Vt, 4))

    # 验证
    A_reconstructed = U @ np.diag(S) @ Vt
    print(f"\n重建误差: {np.linalg.norm(A - A_reconstructed):.2e}")

    # 低秩近似
    print("\n--- 低秩近似 ---")
    for k in [1, 2, 3]:
        A_k = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]
        error = np.linalg.norm(A - A_k)
        print(f"秩{k}近似误差 (Frobenius): {error:.4f}")

    return A, U, S, Vt


def demonstrate_pca_with_svd():
    """演示用SVD做PCA"""
    print("\n" + "=" * 50)
    print("使用SVD进行PCA降维")
    print("=" * 50)

    # 生成2D数据（沿对角线分布）
    np.random.seed(42)
    n = 100
    data = np.random.randn(n, 2) @ np.array([[2, 0.5], [0.5, 1]]) + np.array([3, 5])

    # 中心化
    data_centered = data - data.mean(axis=0)

    # SVD
    U, S, Vt = np.linalg.svd(data_centered, full_matrices=False)

    print("主成分方向:")
    print(Vt)
    print(f"\n奇异值: {S}")
    print(f"解释方差比: {(S**2) / (S**2).sum()}")

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 8))

    ax.scatter(data[:, 0], data[:, 1], alpha=0.5, label='数据点')
    ax.scatter(*data.mean(axis=0), c='red', s=100, marker='x', label='均值')

    # 绘制主成分方向
    scale = 2
    for i, v in enumerate(Vt):
        ax.arrow(data.mean()[0], data.mean()[1],
                v[0] * scale * np.sqrt(S[i]),
                v[1] * scale * np.sqrt(S[i]),
                head_width=0.2, head_length=0.1,
                fc=f'C{i+1}', ec=f'C{i+1}',
                label=f'PC{i+1}')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('PCA: 主成分分析')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.axis('equal')

    plt.tight_layout()
    plt.show()


def demonstrate_eigen():
    """演示特征值分解"""
    print("\n" + "=" * 50)
    print("特征值分解")
    print("=" * 50)

    # 创建对称矩阵
    A = np.array([
        [4, 2, 1],
        [2, 5, 3],
        [1, 3, 6]
    ], dtype=float)

    print("对称矩阵 A:")
    print(A)

    # 特征值分解
    eigenvalues, eigenvectors = np.linalg.eigh(A)

    print(f"\n特征值: {np.round(eigenvalues, 4)}")
    print(f"\n特征向量 (每列):")
    print(np.round(eigenvectors, 4))

    # 验证正交性
    print(f"\n特征向量正交性检验 (V^T V):")
    print(np.round(eigenvectors.T @ eigenvectors, 4))

    # 验证 A = V D V^T
    D = np.diag(eigenvalues)
    A_reconstructed = eigenvectors @ D @ eigenvectors.T
    print(f"\n重建误差: {np.linalg.norm(A - A_reconstructed):.2e}")


def demonstrate_lu():
    """演示LU分解"""
    print("\n" + "=" * 50)
    print("LU分解")
    print("=" * 50)

    A = np.array([
        [2, 1, 1],
        [4, 3, 3],
        [8, 7, 9]
    ], dtype=float)

    b = np.array([4, 10, 24], dtype=float)

    print("线性方程组 Ax = b")
    print(f"A:\n{A}")
    print(f"b: {b}")

    # LU分解
    P, L, U = linalg.lu(A)

    print(f"\n置换矩阵 P:\n{P}")
    print(f"\n下三角矩阵 L:\n{np.round(L, 4)}")
    print(f"\n上三角矩阵 U:\n{np.round(U, 4)}")

    # 验证
    print(f"\nPA = LU 验证误差: {np.linalg.norm(P @ A - L @ U):.2e}")

    # 使用LU分解求解
    # Ly = Pb (前代)
    Pb = P @ b
    y = linalg.solve_triangular(L, Pb, lower=True)
    # Ux = y (回代)
    x = linalg.solve_triangular(U, y, lower=False)

    print(f"\n解 x: {x}")
    print(f"验证 Ax - b: {A @ x - b}")


def demonstrate_qr():
    """演示QR分解"""
    print("\n" + "=" * 50)
    print("QR分解")
    print("=" * 50)

    A = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [10, 11, 12]
    ], dtype=float)

    print(f"矩阵 A ({A.shape[0]}×{A.shape[1]}):")
    print(A)

    # QR分解
    Q, R = np.linalg.qr(A, mode='reduced')

    print(f"\n正交矩阵 Q ({Q.shape}):")
    print(np.round(Q, 4))

    print(f"\n上三角矩阵 R ({R.shape}):")
    print(np.round(R, 4))

    # 验证
    print(f"\nQ^T Q (应为单位矩阵):\n{np.round(Q.T @ Q, 4)}")
    print(f"\nQR - A 误差: {np.linalg.norm(Q @ R - A):.2e}")


def demonstrate_cholesky():
    """演示Cholesky分解"""
    print("\n" + "=" * 50)
    print("Cholesky分解 (对称正定矩阵)")
    print("=" * 50)

    # 创建对称正定矩阵
    A = np.array([
        [4, 2, 1],
        [2, 5, 3],
        [1, 3, 6]
    ], dtype=float)

    print("对称正定矩阵 A:")
    print(A)

    # Cholesky分解
    L = np.linalg.cholesky(A)

    print(f"\n下三角矩阵 L:")
    print(np.round(L, 4))

    # 验证
    print(f"\nLL^T - A 误差: {np.linalg.norm(L @ L.T - A):.2e}")


def demonstrate_matrix_norms():
    """演示矩阵范数"""
    print("\n" + "=" * 50)
    print("矩阵范数")
    print("=" * 50)

    A = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ], dtype=float)

    print("矩阵 A:")
    print(A)

    norms = {
        'Frobenius': np.linalg.norm(A, 'fro'),
        '谱范数 (2-范数)': np.linalg.norm(A, 2),
        '1-范数 (列和最大)': np.linalg.norm(A, 1),
        '∞-范数 (行和最大)': np.linalg.norm(A, np.inf),
        '核范数 (奇异值之和)': np.linalg.norm(A, 'nuc')
    }

    for name, value in norms.items():
        print(f"{name}: {value:.4f}")

    # 条件数
    print(f"\n条件数: {np.linalg.cond(A):.4f}")


def demonstrate_pseudoinverse():
    """演示伪逆"""
    print("\n" + "=" * 50)
    print("伪逆 (Moore-Penrose)")
    print("=" * 50)

    # 非方阵
    A = np.array([
        [1, 2],
        [3, 4],
        [5, 6]
    ], dtype=float)

    print(f"矩阵 A ({A.shape[0]}×{A.shape[1]}):")
    print(A)

    # 使用SVD计算伪逆
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    S_pinv = 1 / S
    A_pinv = Vt.T @ np.diag(S_pinv) @ U.T

    # 与numpy比较
    A_pinv_np = np.linalg.pinv(A)

    print(f"\n伪逆 A⁺ ({A_pinv.shape[0]}×{A_pinv.shape[1]}):")
    print(np.round(A_pinv, 4))

    # 验证伪逆性质
    print(f"\nA⁺A (应接近单位):\n{np.round(A_pinv @ A, 4)}")
    print(f"\nAA⁺A = A: {np.allclose(A @ A_pinv @ A, A)}")


def demo():
    """运行所有演示"""
    demonstrate_svd()
    demonstrate_pca_with_svd()
    demonstrate_eigen()
    demonstrate_lu()
    demonstrate_qr()
    demonstrate_cholesky()
    demonstrate_matrix_norms()
    demonstrate_pseudoinverse()


if __name__ == "__main__":
    demo()
