"""
半监督学习 (Semi-Supervised Learning) 示例代码

包含内容:
1. 自训练 (Self-Training)
2. 标签传播 (Label Propagation)
3. 标签扩散 (Label Spreading)
4. 协同训练概念
5. 与监督学习对比
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification, make_circles, load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.semi_supervised import LabelPropagation, LabelSpreading, SelfTrainingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def demo_self_training():
    """自训练算法"""
    print("=" * 60)
    print("1. 自训练 (Self-Training)")
    print("=" * 60)

    # 生成数据
    X, y = make_classification(n_samples=500, n_features=2, n_redundant=0,
                               n_informative=2, n_clusters_per_class=1, random_state=42)

    # 标准化
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # 划分有标签、无标签和测试数据
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 只保留10%的标签
    n_labeled = int(len(X_train) * 0.1)
    labeled_indices = np.random.choice(len(X_train), n_labeled, replace=False)

    X_labeled = X_train[labeled_indices]
    y_labeled = y_train[labeled_indices]
    X_unlabeled = np.delete(X_train, labeled_indices, axis=0)

    print(f"有标签样本: {len(X_labeled)}")
    print(f"无标签样本: {len(X_unlabeled)}")
    print(f"测试样本: {len(X_test)}")

    # 1. 仅用有标签数据训练
    baseline = KNeighborsClassifier(n_neighbors=3)
    baseline.fit(X_labeled, y_labeled)
    baseline_acc = baseline.score(X_test, y_test)
    print(f"\n仅用有标签数据准确率: {baseline_acc:.4f}")

    # 2. 自训练
    # 创建半标签数组
    y_semi = np.full(len(X_train), -1)
    y_semi[labeled_indices] = y_labeled

    # 使用SelfTrainingClassifier
    base_estimator = KNeighborsClassifier(n_neighbors=3)
    self_training = SelfTrainingClassifier(base_estimator, threshold=0.8)
    self_training.fit(X_train, y_semi)
    self_training_acc = self_training.score(X_test, y_test)
    print(f"自训练准确率: {self_training_acc:.4f}")

    # 3. 使用全部标签（上限）
    full = KNeighborsClassifier(n_neighbors=3)
    full.fit(X_train, y_train)
    full_acc = full.score(X_test, y_test)
    print(f"全标签训练准确率: {full_acc:.4f}")

    # 可视化
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    titles = ['仅用有标签数据', '自训练', '全标签训练']
    models = [baseline, self_training, full]
    accuracies = [baseline_acc, self_training_acc, full_acc]

    for ax, title, model, acc in zip(axes, titles, models, accuracies):
        # 决策边界
        h = 0.02
        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))

        Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.RdYlBu)

        # 数据点
        ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test,
                  cmap=plt.cm.RdYlBu, edgecolors='black', s=30)
        ax.set_title(f'{title}\n准确率: {acc:.4f}', fontsize=12)
        ax.set_xlabel('特征1')
        ax.set_ylabel('特征2')

    plt.tight_layout()
    plt.savefig('semi_supervised_self_training.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("自训练图已保存为 semi_supervised_self_training.png\n")


def demo_label_propagation():
    """标签传播"""
    print("=" * 60)
    print("2. 标签传播 (Label Propagation)")
    print("=" * 60)

    # 生成两个半月形数据
    np.random.seed(42)
    X, y = make_circles(n_samples=300, noise=0.08, factor=0.5, random_state=42)

    # 标准化
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # 只标记少量样本
    n_labeled = 10
    labeled_indices = []

    # 从每个类选一些
    for c in [0, 1]:
        idx = np.where(y == c)[0]
        labeled_indices.extend(np.random.choice(idx, n_labeled//2, replace=False))

    # 创建半标签
    y_semi = np.full(len(y), -1)
    y_semi[labeled_indices] = y[labeled_indices]

    print(f"总样本: {len(y)}")
    print(f"有标签样本: {len(labeled_indices)}")

    # 标签传播
    lp_rbf = LabelPropagation(kernel='rbf', gamma=20)
    lp_rbf.fit(X, y_semi)

    lp_knn = LabelPropagation(kernel='knn', n_neighbors=5)
    lp_knn.fit(X, y_semi)

    # 评估
    acc_rbf = accuracy_score(y, lp_rbf.transduction_)
    acc_knn = accuracy_score(y, lp_knn.transduction_)

    print(f"\nRBF核标签传播准确率: {acc_rbf:.4f}")
    print(f"KNN核标签传播准确率: {acc_knn:.4f}")

    # 可视化
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # 原始数据
    ax = axes[0]
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.RdYlBu, alpha=0.7)
    ax.scatter(X[labeled_indices, 0], X[labeled_indices, 1],
              c='green', s=100, marker='*', label='已标记')
    ax.set_title('原始数据与标记点', fontsize=12)
    ax.legend(loc='upper right')
    ax.set_xlabel('特征1')
    ax.set_ylabel('特征2')

    # RBF结果
    ax = axes[1]
    ax.scatter(X[:, 0], X[:, 1], c=lp_rbf.transduction_, cmap=plt.cm.RdYlBu, alpha=0.7)
    ax.scatter(X[labeled_indices, 0], X[labeled_indices, 1],
              c='green', s=100, marker='*')
    ax.set_title(f'RBF核标签传播\n准确率: {acc_rbf:.4f}', fontsize=12)
    ax.set_xlabel('特征1')
    ax.set_ylabel('特征2')

    # KNN结果
    ax = axes[2]
    ax.scatter(X[:, 0], X[:, 1], c=lp_knn.transduction_, cmap=plt.cm.RdYlBu, alpha=0.7)
    ax.scatter(X[labeled_indices, 0], X[labeled_indices, 1],
              c='green', s=100, marker='*')
    ax.set_title(f'KNN核标签传播\n准确率: {acc_knn:.4f}', fontsize=12)
    ax.set_xlabel('特征1')
    ax.set_ylabel('特征2')

    plt.tight_layout()
    plt.savefig('semi_supervised_label_propagation.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("标签传播图已保存为 semi_supervised_label_propagation.png\n")


def demo_label_spreading():
    """标签扩散"""
    print("=" * 60)
    print("3. 标签扩散 (Label Spreading)")
    print("=" * 60)

    # 加载数字数据集
    digits = load_digits()
    X, y = digits.data, digits.target

    # 标准化
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # 只标记少量样本
    rng = np.random.RandomState(42)
    n_labeled_per_class = 5
    labeled_indices = []

    for c in range(10):
        idx = np.where(y == c)[0]
        labeled_indices.extend(rng.choice(idx, n_labeled_per_class, replace=False))

    # 创建半标签
    y_semi = np.full(len(y), -1)
    y_semi[labeled_indices] = y[labeled_indices]

    print(f"总样本: {len(y)}")
    print(f"有标签样本: {len(labeled_indices)} (每类{n_labeled_per_class}个)")

    # 1. 仅用有标签数据
    baseline = LogisticRegression(max_iter=1000, random_state=42)
    baseline.fit(X[labeled_indices], y[labeled_indices])
    baseline_acc = baseline.score(X, y)
    print(f"\n仅用有标签数据准确率: {baseline_acc:.4f}")

    # 2. 标签扩散
    ls = LabelSpreading(kernel='knn', n_neighbors=5)
    ls.fit(X, y_semi)
    ls_acc = accuracy_score(y, ls.transduction_)
    print(f"标签扩散准确率: {ls_acc:.4f}")

    # 3. 全标签（上限）
    full = LogisticRegression(max_iter=1000, random_state=42)
    full.fit(X, y)
    full_acc = full.score(X, y)
    print(f"全标签训练准确率: {full_acc:.4f}")

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 6))

    methods = ['仅用有标签\n(50样本)', '标签扩散\n(50标签+1700无标签)', '全标签\n(1797样本)']
    accuracies = [baseline_acc, ls_acc, full_acc]
    colors = ['#3498db', '#e74c3c', '#2ecc71']

    bars = ax.bar(methods, accuracies, color=colors, alpha=0.8)
    ax.set_ylabel('准确率', fontsize=12)
    ax.set_title('半监督学习 vs 监督学习 (手写数字识别)', fontsize=14)
    ax.set_ylim(0, 1.1)

    for bar, acc in zip(bars, accuracies):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
               f'{acc:.4f}', ha='center', va='bottom', fontsize=11)

    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('semi_supervised_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("对比图已保存为 semi_supervised_comparison.png\n")


def demo_different_labeled_ratios():
    """不同标签比例的影响"""
    print("=" * 60)
    print("4. 不同标签比例的影响")
    print("=" * 60)

    # 生成数据
    X, y = make_classification(n_samples=500, n_features=10, n_informative=5,
                               n_redundant=2, random_state=42)

    # 标准化
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # 划分
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 不同的标签比例
    ratios = [0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0]

    results = {
        '仅监督': [],
        '自训练': [],
        '标签传播': []
    }

    for ratio in ratios:
        n_labeled = max(2, int(len(X_train) * ratio))
        labeled_indices = np.random.choice(len(X_train), n_labeled, replace=False)

        y_semi = np.full(len(X_train), -1)
        y_semi[labeled_indices] = y_train[labeled_indices]

        # 仅监督
        baseline = KNeighborsClassifier(n_neighbors=3)
        baseline.fit(X_train[labeled_indices], y_train[labeled_indices])
        results['仅监督'].append(baseline.score(X_test, y_test))

        # 自训练
        self_training = SelfTrainingClassifier(
            KNeighborsClassifier(n_neighbors=3),
            threshold=0.8
        )
        self_training.fit(X_train, y_semi)
        results['自训练'].append(self_training.score(X_test, y_test))

        # 标签传播
        lp = LabelPropagation(kernel='knn', n_neighbors=5)
        lp.fit(X_train, y_semi)
        lp_pred = lp.predict(X_test)
        results['标签传播'].append(accuracy_score(y_test, lp_pred))

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 6))

    for name, accs in results.items():
        ax.plot([r*100 for r in ratios], accs, marker='o', label=name, linewidth=2)

    ax.set_xlabel('有标签数据比例 (%)', fontsize=12)
    ax.set_ylabel('测试集准确率', fontsize=12)
    ax.set_title('半监督学习在不同标签比例下的表现', fontsize=14)
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)
    ax.set_xticks([r*100 for r in ratios])

    plt.tight_layout()
    plt.savefig('semi_supervised_ratios.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("标签比例影响图已保存为 semi_supervised_ratios.png\n")

    print("观察:")
    print("  - 半监督方法在标签稀缺时优势明显")
    print("  - 随着标签增加，差距缩小")
    print("  - 标签传播对小数据集效果好\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("半监督学习 (Semi-Supervised Learning) 完整示例")
    print("=" * 60 + "\n")

    # 运行所有示例
    demo_self_training()
    demo_label_propagation()
    demo_label_spreading()
    demo_different_labeled_ratios()

    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
