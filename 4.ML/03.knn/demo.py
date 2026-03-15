"""
K近邻算法 (K-Nearest Neighbors, KNN) 示例代码

包含内容:
1. 基础KNN分类
2. 不同K值对决策边界的影响
3. 不同距离度量比较
4. KNN回归
5. 加权KNN
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification, make_regression, load_iris, load_wine
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report
import warnings
warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def demo_basic_knn():
    """基础KNN分类示例"""
    print("=" * 60)
    print("1. 基础KNN分类示例")
    print("=" * 60)

    # 生成数据
    X, y = make_classification(
        n_samples=300, n_features=2, n_redundant=0, n_informative=2,
        n_clusters_per_class=1, random_state=42
    )

    # 划分数据
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # 标准化（KNN对尺度敏感）
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 创建并训练KNN模型
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train_scaled, y_train)

    # 预测
    y_pred = knn.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"K=5时的准确率: {accuracy:.4f}")

    # 可视化决策边界
    fig, ax = plt.subplots(figsize=(10, 8))

    # 创建网格
    h = 0.02
    x_min, x_max = X_train_scaled[:, 0].min() - 1, X_train_scaled[:, 0].max() + 1
    y_min, y_max = X_train_scaled[:, 1].min() - 1, X_train_scaled[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    # 预测网格点
    Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # 绘制决策边界
    ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.RdYlBu)

    # 绘制训练点
    scatter = ax.scatter(X_train_scaled[:, 0], X_train_scaled[:, 1],
                        c=y_train, cmap=plt.cm.RdYlBu, edgecolors='black', s=50)
    ax.set_xlabel('特征1 (标准化)', fontsize=12)
    ax.set_ylabel('特征2 (标准化)', fontsize=12)
    ax.set_title(f'KNN分类决策边界 (K=5, 准确率: {accuracy:.4f})', fontsize=14)

    plt.colorbar(scatter, ax=ax, label='类别')
    plt.tight_layout()
    plt.savefig('knn_decision_boundary.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("决策边界图已保存为 knn_decision_boundary.png\n")


def demo_different_k():
    """不同K值对决策边界的影响"""
    print("=" * 60)
    print("2. 不同K值对决策边界的影响")
    print("=" * 60)

    # 生成数据
    X, y = make_classification(
        n_samples=200, n_features=2, n_redundant=0, n_informative=2,
        n_clusters_per_class=1, random_state=42
    )

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 测试不同的K值
    k_values = [1, 3, 5, 11, 21, 51]
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # 创建网格
    h = 0.02
    x_min, x_max = X_scaled[:, 0].min() - 1, X_scaled[:, 0].max() + 1
    y_min, y_max = X_scaled[:, 1].min() - 1, X_scaled[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    for idx, k in enumerate(k_values):
        ax = axes[idx // 3, idx % 3]

        # 训练模型
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_scaled, y)

        # 预测网格点
        Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        # 绘制决策边界
        ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.RdYlBu)

        # 绘制数据点
        ax.scatter(X_scaled[:, 0], X_scaled[:, 1], c=y,
                  cmap=plt.cm.RdYlBu, edgecolors='black', s=30)

        # 计算准确率
        accuracy = cross_val_score(knn, X_scaled, y, cv=5).mean()

        ax.set_title(f'K={k}, 5折交叉验证准确率: {accuracy:.3f}', fontsize=12)
        ax.set_xlabel('特征1')
        ax.set_ylabel('特征2')

    plt.suptitle('不同K值对决策边界的影响', fontsize=14)
    plt.tight_layout()
    plt.savefig('knn_different_k.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("不同K值对比图已保存为 knn_different_k.png\n")

    print("观察:")
    print("  - K=1: 决策边界非常复杂，容易过拟合")
    print("  - K较小: 模型复杂度高，拟合训练数据但可能过拟合")
    print("  - K较大: 决策边界更平滑，可能欠拟合")
    print("  - 需要通过交叉验证选择最优K值\n")


def demo_distance_metrics():
    """不同距离度量比较"""
    print("=" * 60)
    print("3. 不同距离度量比较")
    print("=" * 60)

    # 加载葡萄酒数据集
    wine = load_wine()
    X, y = wine.data, wine.target

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 划分数据
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.3, random_state=42
    )

    # 不同距离度量
    metrics = {
        '欧氏距离 (p=2)': {'metric': 'minkowski', 'p': 2},
        '曼哈顿距离 (p=1)': {'metric': 'minkowski', 'p': 1},
        '切比雪夫距离': {'metric': 'chebyshev', 'p': None},
    }

    print(f"{'距离度量':<20} {'准确率':<10}")
    print("-" * 30)

    results = []
    for name, params in metrics.items():
        if params['p'] is not None:
            knn = KNeighborsClassifier(n_neighbors=5, metric=params['metric'], p=params['p'])
        else:
            knn = KNeighborsClassifier(n_neighbors=5, metric=params['metric'])

        knn.fit(X_train, y_train)
        y_pred = knn.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        results.append((name, accuracy))
        print(f"{name:<20} {accuracy:.4f}")

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 6))
    names = [r[0] for r in results]
    accuracies = [r[1] for r in results]

    bars = ax.bar(names, accuracies, color=['#3498db', '#e74c3c', '#2ecc71'])
    ax.set_ylabel('准确率', fontsize=12)
    ax.set_title('不同距离度量的KNN分类性能比较', fontsize=14)
    ax.set_ylim(0.9, 1.0)

    # 添加数值标签
    for bar, acc in zip(bars, accuracies):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.002,
               f'{acc:.4f}', ha='center', va='bottom', fontsize=11)

    plt.tight_layout()
    plt.savefig('knn_distance_metrics.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("\n距离度量对比图已保存为 knn_distance_metrics.png\n")


def demo_knn_regression():
    """KNN回归示例"""
    print("=" * 60)
    print("4. KNN回归示例")
    print("=" * 60)

    # 生成回归数据
    np.random.seed(42)
    X = np.sort(5 * np.random.rand(100, 1), axis=0)
    y = np.sin(X).ravel() + 0.1 * np.random.randn(100)

    # 添加一些异常值
    y[::10] += 0.5 * (0.5 - np.random.rand(10))

    # 测试不同的K值
    k_values = [1, 5, 10, 20]
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # 测试点
    X_test = np.linspace(0, 5, 200).reshape(-1, 1)

    for idx, k in enumerate(k_values):
        ax = axes[idx // 2, idx % 2]

        # 训练回归模型
        knn_reg = KNeighborsRegressor(n_neighbors=k)
        knn_reg.fit(X, y)

        # 预测
        y_pred = knn_reg.predict(X_test)

        # 计算MSE
        y_train_pred = knn_reg.predict(X)
        mse = mean_squared_error(y, y_train_pred)

        # 绘制
        ax.scatter(X, y, color='blue', label='训练数据', s=30, alpha=0.6)
        ax.plot(X_test, y_pred, color='red', linewidth=2, label=f'KNN预测 (K={k})')
        ax.plot(X_test, np.sin(X_test), 'g--', linewidth=1, label='真实函数')

        ax.set_xlabel('X', fontsize=11)
        ax.set_ylabel('y', fontsize=11)
        ax.set_title(f'KNN回归 (K={k}, 训练MSE: {mse:.4f})', fontsize=12)
        ax.legend(loc='upper right')
        ax.set_xlim(0, 5)
        ax.set_ylim(-1.5, 1.5)

    plt.suptitle('KNN回归：不同K值的影响', fontsize=14)
    plt.tight_layout()
    plt.savefig('knn_regression.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("KNN回归对比图已保存为 knn_regression.png\n")

    print("观察:")
    print("  - K=1: 预测值就是最近邻的真实值，完全拟合训练数据")
    print("  - K较小: 捕捉局部模式，但可能过拟合噪声")
    print("  - K较大: 预测更平滑，但可能忽略局部变化")
    print("  - 需要平衡偏差和方差来选择最优K值\n")


def demo_weighted_knn():
    """加权KNN vs 均匀权重KNN"""
    print("=" * 60)
    print("5. 加权KNN vs 均匀权重KNN")
    print("=" * 60)

    # 加载鸢尾花数据集
    iris = load_iris()
    X, y = iris.data, iris.target

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 测试不同K值
    k_range = range(1, 31)
    uniform_scores = []
    distance_scores = []

    for k in k_range:
        # 均匀权重
        knn_uniform = KNeighborsClassifier(n_neighbors=k, weights='uniform')
        uniform_scores.append(cross_val_score(knn_uniform, X_scaled, y, cv=5).mean())

        # 距离加权
        knn_distance = KNeighborsClassifier(n_neighbors=k, weights='distance')
        distance_scores.append(cross_val_score(knn_distance, X_scaled, y, cv=5).mean())

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(k_range, uniform_scores, 'b-o', label='均匀权重 (uniform)', markersize=5)
    ax.plot(k_range, distance_scores, 'r-s', label='距离加权 (distance)', markersize=5)

    ax.set_xlabel('K值', fontsize=12)
    ax.set_ylabel('5折交叉验证准确率', fontsize=12)
    ax.set_title('均匀权重 vs 距离加权 KNN', fontsize=14)
    ax.legend(loc='lower left')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(k_range[::2])

    # 标记最优K值
    best_k_uniform = k_range[np.argmax(uniform_scores)]
    best_k_distance = k_range[np.argmax(distance_scores)]

    ax.axvline(x=best_k_uniform, color='blue', linestyle='--', alpha=0.5)
    ax.axvline(x=best_k_distance, color='red', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('knn_weighted.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("加权KNN对比图已保存为 knn_weighted.png\n")

    print(f"均匀权重最优K值: {best_k_uniform}, 准确率: {max(uniform_scores):.4f}")
    print(f"距离加权最优K值: {best_k_distance}, 准确率: {max(distance_scores):.4f}")
    print("\n说明:")
    print("  - 距离加权给近邻更大的权重，通常能提高性能")
    print("  - 特别是在K值较大时，距离加权可以减少远距离点的负面影响\n")


def demo_optimal_k():
    """寻找最优K值"""
    print("=" * 60)
    print("6. 寻找最优K值")
    print("=" * 60)

    # 加载葡萄酒数据集
    wine = load_wine()
    X, y = wine.data, wine.target

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 测试K值范围
    k_range = range(1, 50)
    k_scores = []

    for k in k_range:
        knn = KNeighborsClassifier(n_neighbors=k)
        scores = cross_val_score(knn, X_scaled, y, cv=5, scoring='accuracy')
        k_scores.append(scores.mean())

    # 可视化
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(k_range, k_scores, 'b-o', markersize=4)
    ax.set_xlabel('K值', fontsize=12)
    ax.set_ylabel('5折交叉验证准确率', fontsize=12)
    ax.set_title('通过交叉验证选择最优K值', fontsize=14)
    ax.grid(True, alpha=0.3)

    # 标记最优K值
    best_k = k_range[np.argmax(k_scores)]
    best_score = max(k_scores)

    ax.axvline(x=best_k, color='red', linestyle='--', label=f'最优K={best_k}')
    ax.scatter([best_k], [best_score], color='red', s=100, zorder=5)
    ax.annotate(f'最优K={best_k}\n准确率={best_score:.4f}',
                xy=(best_k, best_score), xytext=(best_k+5, best_score-0.05),
                fontsize=10, arrowprops=dict(arrowstyle='->', color='red'))

    ax.legend(loc='lower left')
    ax.set_xticks(range(1, 51, 5))

    plt.tight_layout()
    plt.savefig('knn_optimal_k.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("最优K值选择图已保存为 knn_optimal_k.png\n")

    print(f"最优K值: {best_k}")
    print(f"最优准确率: {best_score:.4f}")
    print("\n选择最优K值的建议:")
    print("  1. 使用交叉验证评估不同K值")
    print("  2. 选择使验证准确率最高的K值")
    print("  3. 避免选择过大的K值导致欠拟合")
    print("  4. 二分类问题可考虑奇数K值避免平票\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("K近邻算法 (KNN) 完整示例")
    print("=" * 60 + "\n")

    # 运行所有示例
    demo_basic_knn()
    demo_different_k()
    demo_distance_metrics()
    demo_knn_regression()
    demo_weighted_knn()
    demo_optimal_k()

    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
