"""
决策树算法示例
演示决策树分类和回归的使用方法
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris, load_wine, make_regression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, mean_squared_error, r2_score)
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def demo_classification_basic():
    """决策树分类基础示例"""
    print("=" * 60)
    print("1. 决策树分类基础示例 (鸢尾花数据集)")
    print("=" * 60)

    # 加载数据
    iris = load_iris()
    X, y = iris.data, iris.target
    feature_names = iris.feature_names
    class_names = iris.target_names

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # 训练模型
    clf = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=42)
    clf.fit(X_train, y_train)

    # 预测
    y_pred = clf.predict(X_test)

    # 评估
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n模型准确率: {accuracy:.4f}")
    print(f"树的深度: {clf.get_depth()}")
    print(f"叶节点数量: {clf.get_n_leaves()}")

    print("\n分类报告:")
    print(classification_report(y_test, y_pred, target_names=class_names))

    # 可视化决策树
    plt.figure(figsize=(15, 10))
    plot_tree(clf, feature_names=feature_names, class_names=class_names,
              filled=True, rounded=True, fontsize=10)
    plt.title('决策树可视化 - 鸢尾花数据集')
    plt.tight_layout()
    plt.savefig('decision_tree_iris.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n决策树可视化已保存: decision_tree_iris.png")

    # 混淆矩阵
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('混淆矩阵')
    plt.colorbar()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=45)
    plt.yticks(tick_marks, class_names)

    # 添加数值标签
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], 'd'),
                     ha="center", va="center",
                     color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('真实标签')
    plt.xlabel('预测标签')
    plt.tight_layout()
    plt.savefig('confusion_matrix_iris.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("混淆矩阵已保存: confusion_matrix_iris.png")


def demo_regression():
    """决策树回归示例"""
    print("\n" + "=" * 60)
    print("2. 决策树回归示例")
    print("=" * 60)

    # 生成数据
    np.random.seed(42)
    X = np.sort(5 * np.random.rand(200, 1), axis=0)
    y = np.sin(X).ravel() + np.random.randn(200) * 0.1

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # 训练不同深度的树
    depths = [1, 3, 5, 10]
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.ravel()

    for idx, depth in enumerate(depths):
        # 训练模型
        reg = DecisionTreeRegressor(max_depth=depth, random_state=42)
        reg.fit(X_train, y_train)

        # 预测
        y_pred = reg.predict(X_test)

        # 评估
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"\n深度={depth}: MSE={mse:.4f}, R²={r2:.4f}")

        # 可视化
        X_plot = np.linspace(0, 5, 500).reshape(-1, 1)
        y_plot = reg.predict(X_plot)

        axes[idx].scatter(X_test, y_test, alpha=0.5, s=30, label='测试数据')
        axes[idx].plot(X_plot, y_plot, 'r-', linewidth=2, label='预测')
        axes[idx].set_xlabel('X')
        axes[idx].set_ylabel('y')
        axes[idx].set_title(f'决策树回归 (深度={depth})\nMSE={mse:.4f}, R²={r2:.4f}')
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('decision_tree_regression.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: decision_tree_regression.png")


def demo_hyperparameter_tuning():
    """超参数调优示例"""
    print("\n" + "=" * 60)
    print("3. 超参数调优示例")
    print("=" * 60)

    # 加载数据
    wine = load_wine()
    X, y = wine.data, wine.target

    # 测试不同的max_depth
    depths = range(1, 21)
    train_scores = []
    test_scores = []
    cv_scores = []

    for depth in depths:
        clf = DecisionTreeClassifier(max_depth=depth, random_state=42)

        # 使用交叉验证
        cv_score = cross_val_score(clf, X, y, cv=5, scoring='accuracy').mean()
        cv_scores.append(cv_score)

        # 训练集和测试集分数
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )
        clf.fit(X_train, y_train)
        train_scores.append(clf.score(X_train, y_train))
        test_scores.append(clf.score(X_test, y_test))

    # 绘制学习曲线
    plt.figure(figsize=(12, 6))
    plt.plot(depths, train_scores, 'o-', label='训练集准确率', linewidth=2)
    plt.plot(depths, test_scores, 's-', label='测试集准确率', linewidth=2)
    plt.plot(depths, cv_scores, '^-', label='交叉验证准确率', linewidth=2)

    plt.xlabel('树的深度 (max_depth)')
    plt.ylabel('准确率')
    plt.title('决策树深度对性能的影响')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(depths)

    # 找到最佳深度
    best_depth = depths[np.argmax(cv_scores)]
    plt.axvline(x=best_depth, color='r', linestyle='--', label=f'最佳深度={best_depth}')
    plt.legend()

    plt.tight_layout()
    plt.savefig('hyperparameter_tuning.png', dpi=150, bbox_inches='tight')
    plt.close()

    print(f"\n最佳深度: {best_depth}")
    print(f"最佳交叉验证准确率: {max(cv_scores):.4f}")
    print("\n图表已保存: hyperparameter_tuning.png")


def demo_feature_importance():
    """特征重要性示例"""
    print("\n" + "=" * 60)
    print("4. 特征重要性示例")
    print("=" * 60)

    # 加载数据
    wine = load_wine()
    X, y = wine.data, wine.target
    feature_names = wine.feature_names

    # 训练模型
    clf = DecisionTreeClassifier(max_depth=5, random_state=42)
    clf.fit(X, y)

    # 获取特征重要性
    importance = clf.feature_importances_
    indices = np.argsort(importance)[::-1]

    print("\n特征重要性排名:")
    print("-" * 50)
    for i, idx in enumerate(indices):
        print(f"{i+1}. {feature_names[idx]:30s}: {importance[idx]:.4f}")

    # 可视化特征重要性
    plt.figure(figsize=(12, 8))
    plt.bar(range(len(importance)), importance[indices], align='center')
    plt.xticks(range(len(importance)), [feature_names[i] for i in indices], rotation=45, ha='right')
    plt.xlabel('特征')
    plt.ylabel('重要性')
    plt.title('决策树特征重要性')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: feature_importance.png")


def demo_criterion_comparison():
    """分裂准则对比示例"""
    print("\n" + "=" * 60)
    print("5. 分裂准则对比示例 (Gini vs Entropy)")
    print("=" * 60)

    # 加载数据
    iris = load_iris()
    X, y = iris.data, iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    criteria = ['gini', 'entropy', 'log_loss']
    results = {}

    for criterion in criteria:
        # 训练模型
        clf = DecisionTreeClassifier(criterion=criterion, max_depth=3, random_state=42)
        clf.fit(X_train, y_train)

        # 评估
        train_acc = clf.score(X_train, y_train)
        test_acc = clf.score(X_test, y_test)
        cv_acc = cross_val_score(clf, X, y, cv=5, scoring='accuracy').mean()

        results[criterion] = {
            'train_acc': train_acc,
            'test_acc': test_acc,
            'cv_acc': cv_acc,
            'depth': clf.get_depth(),
            'leaves': clf.get_n_leaves()
        }

        print(f"\n{criterion}:")
        print(f"  训练准确率: {train_acc:.4f}")
        print(f"  测试准确率: {test_acc:.4f}")
        print(f"  交叉验证准确率: {cv_acc:.4f}")
        print(f"  树深度: {clf.get_depth()}")
        print(f"  叶节点数: {clf.get_n_leaves()}")

    # 可视化对比
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    metrics = ['train_acc', 'test_acc', 'cv_acc']
    titles = ['训练准确率', '测试准确率', '交叉验证准确率']

    for idx, (metric, title) in enumerate(zip(metrics, titles)):
        values = [results[c][metric] for c in criteria]
        axes[idx].bar(criteria, values, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
        axes[idx].set_ylabel('准确率')
        axes[idx].set_title(title)
        axes[idx].set_ylim([0.9, 1.0])

        for i, v in enumerate(values):
            axes[idx].text(i, v + 0.002, f'{v:.4f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('criterion_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: criterion_comparison.png")


def demo_pruning():
    """剪枝示例"""
    print("\n" + "=" * 60)
    print("6. 剪枝示例 (代价复杂度剪枝)")
    print("=" * 60)

    # 加载数据
    wine = load_wine()
    X, y = wine.data, wine.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # 训练完整树
    clf = DecisionTreeClassifier(random_state=42)
    path = clf.cost_complexity_pruning_path(X_train, y_train)
    ccp_alphas = path.ccp_alphas

    # 测试不同的alpha值
    clfs = []
    for ccp_alpha in ccp_alphas:
        clf = DecisionTreeClassifier(random_state=42, ccp_alpha=ccp_alpha)
        clf.fit(X_train, y_train)
        clfs.append(clf)

    # 计算准确率
    train_scores = [clf.score(X_train, y_train) for clf in clfs]
    test_scores = [clf.score(X_test, y_test) for clf in clfs]

    # 绘制剪枝曲线
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(ccp_alphas, train_scores, 'o-', label='训练集', drawstyle="steps-post")
    ax1.plot(ccp_alphas, test_scores, 's-', label='测试集', drawstyle="steps-post")
    ax1.set_xlabel('Alpha (剪枝强度)')
    ax1.set_ylabel('准确率')
    ax1.set_title('剪枝对准确率的影响')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 绘制树的大小
    node_counts = [clf.tree_.node_count for clf in clfs]
    depth = [clf.tree_.max_depth for clf in clfs]

    ax2.plot(ccp_alphas, node_counts, 'o-', label='节点数', drawstyle="steps-post")
    ax2.set_xlabel('Alpha (剪枝强度)')
    ax2.set_ylabel('节点数')
    ax2.set_title('剪枝对树大小的影响')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 添加第二个y轴显示深度
    ax2_twin = ax2.twinx()
    ax2_twin.plot(ccp_alphas, depth, '^-', label='深度', drawstyle="steps-post", color='orange')
    ax2_twin.set_ylabel('深度', color='orange')
    ax2_twin.legend(loc='center right')

    plt.tight_layout()
    plt.savefig('pruning.png', dpi=150, bbox_inches='tight')
    plt.close()

    # 找到最佳alpha
    best_idx = np.argmax(test_scores)
    best_alpha = ccp_alphas[best_idx]
    print(f"\n最佳alpha值: {best_alpha:.6f}")
    print(f"对应的测试准确率: {test_scores[best_idx]:.4f}")
    print("\n图表已保存: pruning.png")


def demo_decision_boundary():
    """决策边界可视化"""
    print("\n" + "=" * 60)
    print("7. 决策边界可视化")
    print("=" * 60)

    # 加载数据（只使用两个特征）
    iris = load_iris()
    X = iris.data[:, :2]  # 只使用前两个特征
    y = iris.target
    feature_names = iris.feature_names[:2]

    # 训练不同深度的树
    depths = [1, 3, 5, None]
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    axes = axes.ravel()

    for idx, depth in enumerate(depths):
        # 训练模型
        clf = DecisionTreeClassifier(max_depth=depth, random_state=42)
        clf.fit(X, y)

        # 创建网格
        x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
        y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                             np.linspace(y_min, y_max, 200))

        # 预测
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        # 绘制
        axes[idx].contourf(xx, yy, Z, alpha=0.3, cmap='rainbow')
        scatter = axes[idx].scatter(X[:, 0], X[:, 1], c=y, cmap='rainbow',
                                     edgecolors='black', s=50, alpha=0.7)
        axes[idx].set_xlabel(feature_names[0])
        axes[idx].set_ylabel(feature_names[1])

        depth_str = str(depth) if depth is not None else '无限制'
        acc = clf.score(X, y)
        axes[idx].set_title(f'深度={depth_str}, 准确率={acc:.4f}')

    plt.tight_layout()
    plt.savefig('decision_boundary.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: decision_boundary.png")


def main():
    """主函数"""
    print("决策树算法演示程序")
    print("=" * 60)

    # 运行所有示例
    demo_classification_basic()
    demo_regression()
    demo_hyperparameter_tuning()
    demo_feature_importance()
    demo_criterion_comparison()
    demo_pruning()
    demo_decision_boundary()

    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
