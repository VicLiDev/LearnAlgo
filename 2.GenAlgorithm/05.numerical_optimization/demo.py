"""
数值优化算法示例：梯度下降、牛顿法、BFGS
"""
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt


def gradient_descent(f, grad_f, x0, learning_rate=0.01, max_iter=1000, tol=1e-6):
    """
    梯度下降法

    Args:
        f: 目标函数
        grad_f: 梯度函数
        x0: 初始点
        learning_rate: 学习率
        max_iter: 最大迭代次数
        tol: 收敛阈值

    Returns:
        x: 最优解
        history: 迭代历史
    """
    x = x0.copy()
    history = [x.copy()]

    for i in range(max_iter):
        g = grad_f(x)
        x_new = x - learning_rate * g

        if np.linalg.norm(x_new - x) < tol:
            print(f"梯度下降收敛于第 {i+1} 次迭代")
            break

        x = x_new
        history.append(x.copy())

    return x, np.array(history)


def newton_method(f, grad_f, hessian_f, x0, max_iter=100, tol=1e-6):
    """
    牛顿法

    Args:
        f: 目标函数
        grad_f: 梯度函数
        hessian_f: Hessian矩阵函数
        x0: 初始点
        max_iter: 最大迭代次数
        tol: 收敛阈值

    Returns:
        x: 最优解
        history: 迭代历史
    """
    x = x0.copy()
    history = [x.copy()]

    for i in range(max_iter):
        g = grad_f(x)
        H = hessian_f(x)

        # 牛顿方向: -H^{-1} * g
        try:
            delta = np.linalg.solve(H, -g)
        except np.linalg.LinAlgError:
            delta = -g  # 如果Hessian奇异，退化为梯度下降

        x_new = x + delta

        if np.linalg.norm(x_new - x) < tol:
            print(f"牛顿法收敛于第 {i+1} 次迭代")
            break

        x = x_new
        history.append(x.copy())

    return x, np.array(history)


def bfgs_method(f, grad_f, x0, max_iter=100, tol=1e-6):
    """
    BFGS拟牛顿法

    Args:
        f: 目标函数
        grad_f: 梯度函数
        x0: 初始点
        max_iter: 最大迭代次数
        tol: 收敛阈值

    Returns:
        x: 最优解
        history: 迭代历史
    """
    n = len(x0)
    x = x0.copy()
    B = np.eye(n)  # Hessian近似，初始化为单位矩阵
    g = grad_f(x)
    history = [x.copy()]

    for i in range(max_iter):
        # 搜索方向
        p = np.linalg.solve(B, -g)

        # 线搜索 (简化版：固定步长)
        alpha = 1.0
        for _ in range(20):
            if f(x + alpha * p) < f(x):
                break
            alpha *= 0.5

        # 更新
        s = alpha * p
        x_new = x + s
        g_new = grad_f(x_new)
        y = g_new - g

        # BFGS更新
        sy = s @ y
        if sy > 1e-10:
            B = B - np.outer(B @ s, s @ B) / (s @ B @ s) + np.outer(y, y) / sy

        if np.linalg.norm(x_new - x) < tol:
            print(f"BFGS收敛于第 {i+1} 次迭代")
            break

        x = x_new
        g = g_new
        history.append(x.copy())

    return x, np.array(history)


def rosenbrock(x):
    """Rosenbrock函数 (经典测试函数)"""
    return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2


def rosenbrock_grad(x):
    """Rosenbrock梯度"""
    return np.array([
        -2 * (1 - x[0]) - 400 * x[0] * (x[1] - x[0]**2),
        200 * (x[1] - x[0]**2)
    ])


def rosenbrock_hessian(x):
    """Rosenbrock Hessian矩阵"""
    return np.array([
        [2 - 400 * x[1] + 1200 * x[0]**2, -400 * x[0]],
        [-400 * x[0], 200]
    ])


def quadratic(x):
    """二次函数"""
    A = np.array([[4, 1], [1, 3]])
    b = np.array([1, 2])
    return 0.5 * x @ A @ x - b @ x


def quadratic_grad(x):
    """二次函数梯度"""
    A = np.array([[4, 1], [1, 3]])
    b = np.array([1, 2])
    return A @ x - b


def quadratic_hessian(x):
    """二次函数Hessian"""
    return np.array([[4, 1], [1, 3]])


def visualize_optimization(f, history, title, xlim=(-2, 2), ylim=(-2, 2)):
    """可视化优化过程"""
    fig, ax = plt.subplots(figsize=(10, 8))

    # 等高线
    x = np.linspace(xlim[0], xlim[1], 100)
    y = np.linspace(ylim[0], ylim[1], 100)
    X, Y = np.meshgrid(x, y)
    Z = np.array([[f(np.array([X[i, j], Y[i, j]])) for j in range(len(x))] for i in range(len(y))])

    ax.contour(X, Y, Z, levels=30, cmap='viridis', alpha=0.6)
    ax.contourf(X, Y, Z, levels=30, cmap='viridis', alpha=0.3)

    # 优化路径
    ax.plot(history[:, 0], history[:, 1], 'r.-', linewidth=2, markersize=8, label='优化路径')
    ax.scatter(history[0, 0], history[0, 1], c='green', s=150, marker='*', zorder=5, label='起点')
    ax.scatter(history[-1, 0], history[-1, 1], c='red', s=150, marker='*', zorder=5, label='终点')

    ax.set_xlabel('x₁')
    ax.set_ylabel('x₂')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def compare_methods_on_quadratic():
    """在二次函数上比较不同方法"""
    print("=" * 50)
    print("二次函数优化比较")
    print("=" * 50)

    x0 = np.array([2.0, 2.0])
    print(f"初始点: {x0}")
    print(f"真解: [0.0909, 0.6364]")

    # 梯度下降
    x_gd, hist_gd = gradient_descent(quadratic, quadratic_grad, x0, learning_rate=0.1)
    print(f"\n梯度下降结果: {x_gd}")
    print(f"迭代次数: {len(hist_gd)}")

    # 牛顿法
    x_newton, hist_newton = newton_method(quadratic, quadratic_grad, quadratic_hessian, x0)
    print(f"\n牛顿法结果: {x_newton}")
    print(f"迭代次数: {len(hist_newton)}")

    # BFGS
    x_bfgs, hist_bfgs = bfgs_method(quadratic, quadratic_grad, x0)
    print(f"\nBFGS结果: {x_bfgs}")
    print(f"迭代次数: {len(hist_bfgs)}")

    # 可视化
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    methods = [
        (hist_gd, '梯度下降'),
        (hist_newton, '牛顿法'),
        (hist_bfgs, 'BFGS')
    ]

    x = np.linspace(-1, 3, 100)
    y = np.linspace(-1, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.array([[quadratic(np.array([X[i, j], Y[i, j]])) for j in range(len(x))] for i in range(len(y))])

    for ax, (hist, name) in zip(axes, methods):
        ax.contour(X, Y, Z, levels=30, cmap='viridis', alpha=0.6)
        ax.plot(hist[:, 0], hist[:, 1], 'r.-', linewidth=2, markersize=6)
        ax.scatter(hist[0, 0], hist[0, 1], c='green', s=100, marker='*', zorder=5)
        ax.scatter(hist[-1, 0], hist[-1, 1], c='red', s=100, marker='*', zorder=5)
        ax.set_title(f'{name} ({len(hist)}次迭代)')
        ax.set_xlabel('x₁')
        ax.set_ylabel('x₂')
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def optimize_rosenbrock():
    """优化Rosenbrock函数"""
    print("\n" + "=" * 50)
    print("Rosenbrock函数优化 (经典测试)")
    print("=" * 50)

    x0 = np.array([-1.0, 1.0])
    print(f"初始点: {x0}")
    print(f"真解: [1.0, 1.0]")

    # 使用scipy的BFGS
    result = minimize(rosenbrock, x0, method='BFGS', jac=rosenbrock_grad)
    print(f"\nScipy BFGS结果: {result.x}")
    print(f"迭代次数: {result.nit}")

    # 我们自己的梯度下降
    x_gd, hist_gd = gradient_descent(rosenbrock, rosenbrock_grad, x0, learning_rate=0.002, max_iter=5000)
    print(f"\n梯度下降结果: {x_gd}")
    print(f"迭代次数: {len(hist_gd)}")

    # 可视化
    visualize_optimization(rosenbrock, hist_gd, 'Rosenbrock函数 - 梯度下降优化',
                          xlim=(-2, 2), ylim=(-1, 3))


def demonstrate_learning_rate():
    """演示学习率的影响"""
    print("\n" + "=" * 50)
    print("学习率影响演示")
    print("=" * 50)

    x0 = np.array([2.0, 2.0])
    learning_rates = [0.01, 0.1, 0.5]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    x = np.linspace(-1, 3, 100)
    y = np.linspace(-1, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.array([[quadratic(np.array([X[i, j], Y[i, j]])) for j in range(len(x))] for i in range(len(y))])

    for ax, lr in zip(axes, learning_rates):
        _, hist = gradient_descent(quadratic, quadratic_grad, x0, learning_rate=lr, max_iter=50)

        ax.contour(X, Y, Z, levels=30, cmap='viridis', alpha=0.6)
        ax.plot(hist[:, 0], hist[:, 1], 'r.-', linewidth=2, markersize=6)
        ax.set_title(f'学习率 α = {lr}\n({len(hist)}次迭代)')
        ax.set_xlabel('x₁')
        ax.set_ylabel('x₂')
        ax.grid(True, alpha=0.3)

        print(f"学习率 {lr}: {len(hist)} 次迭代")

    plt.tight_layout()
    plt.show()


def demo():
    """运行所有演示"""
    compare_methods_on_quadratic()
    optimize_rosenbrock()
    demonstrate_learning_rate()


if __name__ == "__main__":
    demo()
