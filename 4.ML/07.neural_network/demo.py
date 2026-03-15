"""
神经网络算法示例
演示MLP分类和回归的使用方法
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris, load_wine, make_classification, make_regression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelBinarizer
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, mean_squared_error, r2_score)
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def demo_mlp_classification_basic():
    """MLP分类基础示例"""
    print("=" * 60)
    print("1. MLP分类基础示例")
    print("=" * 60)

    # 加载数据
    iris = load_iris()
    X, y = iris.data, iris.target
    feature_names = iris.feature_names
    class_names = iris.target_names

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.3, random_state=42
    )

    # 训练模型
    mlp = MLPClassifier(
        hidden_layer_sizes=(100, 50),
        activation='relu',
        solver='adam',
        max_iter=1000,
        random_state=42,
        verbose=False
    )
    mlp.fit(X_train, y_train)

    # 预测
    y_pred = mlp.predict(X_test)

    # 评估
    accuracy = accuracy_score(y_test, y_pred)
    cv_score = cross_val_score(mlp, X_scaled, y, cv=5).mean()

    print(f"\n模型参数:")
    print(f"  隐藏层结构: {mlp.hidden_layer_sizes}")
    print(f"  激活函数: {mlp.activation}")
    print(f"  优化器: {mlp.solver}")
    print(f"  迭代次数: {mlp.n_iter_}")
    print(f"  最终损失: {mlp.loss_:.4f}")

    print(f"\n评估指标:")
    print(f"  测试准确率: {accuracy:.4f}")
    print(f"  交叉验证准确率: {cv_score:.4f}")

    print("\n分类报告:")
    print(classification_report(y_test, y_pred, target_names=class_names))

    # 可视化损失曲线
    plt.figure(figsize=(10, 6))
    plt.plot(mlp.loss_curve_, linewidth=2)
    plt.xlabel('迭代次数')
    plt.ylabel('损失值')
    plt.title('MLP训练损失曲线')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('mlp_loss_curve.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: mlp_loss_curve.png")


def demo_mlp_regression():
    """MLP回归示例"""
    print("\n" + "=" * 60)
    print("2. MLP回归示例")
    print("=" * 60)

    # 生成数据
    np.random.seed(42)
    X = np.sort(10 * np.random.rand(500, 1), axis=0)
    y = np.sin(X).ravel() + np.random.randn(500) * 0.3

    # 标准化
    scaler_X = StandardScaler()
    scaler_y = StandardScaler()
    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y.reshape(-1, 1)).ravel()

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_scaled, test_size=0.3, random_state=42
    )

    # 训练模型
    mlp = MLPRegressor(
        hidden_layer_sizes=(100, 50, 25),
        activation='relu',
        solver='adam',
        max_iter=1000,
        random_state=42,
        verbose=False
    )
    mlp.fit(X_train, y_train)

    # 预测
    y_pred_scaled = mlp.predict(X_test)
    y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1)).ravel()
    y_test_orig = scaler_y.inverse_transform(y_test.reshape(-1, 1)).ravel()

    # 评估
    mse = mean_squared_error(y_test_orig, y_pred)
    r2 = r2_score(y_test_orig, y_pred)

    print(f"\n模型参数:")
    print(f"  隐藏层结构: {mlp.hidden_layer_sizes}")
    print(f"  迭代次数: {mlp.n_iter_}")

    print(f"\n评估指标:")
    print(f"  MSE: {mse:.4f}")
    print(f"  R²: {r2:.4f}")

    # 可视化
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # 回归结果
    X_orig = scaler_X.inverse_transform(X_test)
    sort_idx = np.argsort(X_orig.ravel())

    ax1.scatter(X_orig, y_test_orig, alpha=0.5, s=30, label='真实值')
    ax1.plot(X_orig[sort_idx], y_pred[sort_idx], 'r-', linewidth=2,
             label='预测值', alpha=0.8)
    ax1.set_xlabel('X')
    ax1.set_ylabel('y')
    ax1.set_title(f'MLP回归 (R²={r2:.4f})')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 损失曲线
    ax2.plot(mlp.loss_curve_, linewidth=2)
    ax2.set_xlabel('迭代次数')
    ax2.set_ylabel('损失值')
    ax2.set_title('训练损失曲线')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('mlp_regression.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: mlp_regression.png")


def demo_activation_functions():
    """激活函数对比示例"""
    print("\n" + "=" * 60)
    print("3. 激活函数对比示例")
    print("=" * 60)

    # 加载数据
    wine = load_wine()
    X, y = wine.data, wine.target

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.3, random_state=42
    )

    # 测试不同的激活函数
    activations = ['relu', 'tanh', 'logistic', 'identity']
    results = {}

    print("\n不同激活函数的性能:")
    print("-" * 50)

    for activation in activations:
        mlp = MLPClassifier(
            hidden_layer_sizes=(100, 50),
            activation=activation,
            solver='adam',
            max_iter=1000,
            random_state=42,
            verbose=False
        )
        mlp.fit(X_train, y_train)

        train_acc = mlp.score(X_train, y_train)
        test_acc = mlp.score(X_test, y_test)
        cv_acc = cross_val_score(mlp, X_scaled, y, cv=5).mean()

        results[activation] = {
            'train': train_acc,
            'test': test_acc,
            'cv': cv_acc,
            'n_iter': mlp.n_iter_,
            'loss_curve': mlp.loss_curve_
        }

        print(f"{activation:10s}: "
              f"测试准确率={test_acc:.4f}, "
              f"CV准确率={cv_acc:.4f}, "
              f"迭代次数={mlp.n_iter_}")

    # 可视化
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # 准确率对比
    x = np.arange(len(activations))
    width = 0.25

    train_scores = [results[a]['train'] for a in activations]
    test_scores = [results[a]['test'] for a in activations]
    cv_scores = [results[a]['cv'] for a in activations]

    ax1.bar(x - width, train_scores, width, label='训练集')
    ax1.bar(x, test_scores, width, label='测试集')
    ax1.bar(x + width, cv_scores, width, label='交叉验证')

    ax1.set_ylabel('准确率')
    ax1.set_title('不同激活函数的性能对比')
    ax1.set_xticks(x)
    ax1.set_xticklabels(activations)
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')

    # 损失曲线
    for activation in activations:
        ax2.plot(results[activation]['loss_curve'], label=activation, linewidth=2)

    ax2.set_xlabel('迭代次数')
    ax2.set_ylabel('损失值')
    ax2.set_title('不同激活函数的损失曲线')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('activation_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: activation_comparison.png")


def demo_hidden_layer_sizes():
    """隐藏层结构对比示例"""
    print("\n" + "=" * 60)
    print("4. 隐藏层结构对比示例")
    print("=" * 60)

    # 加载数据
    wine = load_wine()
    X, y = wine.data, wine.target

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.3, random_state=42
    )

    # 测试不同的隐藏层结构
    architectures = [
        (10,),
        (50,),
        (100,),
        (100, 50),
        (100, 50, 25),
        (200, 100, 50)
    ]

    print("\n不同隐藏层结构的性能:")
    print("-" * 60)

    results = {}
    for arch in architectures:
        mlp = MLPClassifier(
            hidden_layer_sizes=arch,
            activation='relu',
            solver='adam',
            max_iter=1000,
            random_state=42,
            verbose=False
        )
        mlp.fit(X_train, y_train)

        train_acc = mlp.score(X_train, y_train)
        test_acc = mlp.score(X_test, y_test)
        cv_acc = cross_val_score(mlp, X_scaled, y, cv=5).mean()

        # 计算参数数量
        n_params = sum([coef.size for coef in mlp.coefs_]) + sum([intercept.size for intercept in mlp.intercepts_])

        results[str(arch)] = {
            'train': train_acc,
            'test': test_acc,
            'cv': cv_acc,
            'n_params': n_params
        }

        print(f"{str(arch):20s}: "
              f"测试准确率={test_acc:.4f}, "
              f"CV准确率={cv_acc:.4f}, "
              f"参数数量={n_params}")

    # 可视化
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    names = list(results.keys())
    test_scores = [results[n]['test'] for n in names]
    cv_scores = [results[n]['cv'] for n in names]
    n_params = [results[n]['n_params'] for n in names]

    # 准确率对比
    x = np.arange(len(names))
    width = 0.35

    ax1.bar(x - width/2, test_scores, width, label='测试集')
    ax1.bar(x + width/2, cv_scores, width, label='交叉验证')

    ax1.set_ylabel('准确率')
    ax1.set_title('不同隐藏层结构的性能对比')
    ax1.set_xticks(x)
    ax1.set_xticklabels(names, rotation=45, ha='right')
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')

    # 参数数量
    ax2.bar(names, n_params, color='green', alpha=0.7)
    ax2.set_ylabel('参数数量')
    ax2.set_title('不同结构的参数数量')
    ax2.set_xticklabels(names, rotation=45, ha='right')
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('hidden_layer_sizes.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: hidden_layer_sizes.png")


def demo_regularization():
    """正则化参数对比示例"""
    print("\n" + "=" * 60)
    print("5. 正则化参数 (alpha) 对比示例")
    print("=" * 60)

    # 加载数据
    wine = load_wine()
    X, y = wine.data, wine.target

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.3, random_state=42
    )

    # 测试不同的alpha值
    alphas = [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0]

    print("\n不同alpha值的性能:")
    print("-" * 50)

    results = {}
    for alpha in alphas:
        mlp = MLPClassifier(
            hidden_layer_sizes=(100, 50),
            activation='relu',
            solver='adam',
            alpha=alpha,
            max_iter=1000,
            random_state=42,
            verbose=False
        )
        mlp.fit(X_train, y_train)

        train_acc = mlp.score(X_train, y_train)
        test_acc = mlp.score(X_test, y_test)
        cv_acc = cross_val_score(mlp, X_scaled, y, cv=5).mean()

        results[alpha] = {
            'train': train_acc,
            'test': test_acc,
            'cv': cv_acc
        }

        print(f"alpha={alpha:6.4f}: "
              f"训练准确率={train_acc:.4f}, "
              f"测试准确率={test_acc:.4f}, "
              f"CV准确率={cv_acc:.4f}")

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(alphas))
    width = 0.25

    train_scores = [results[a]['train'] for a in alphas]
    test_scores = [results[a]['test'] for a in alphas]
    cv_scores = [results[a]['cv'] for a in alphas]

    ax.bar(x - width, train_scores, width, label='训练集')
    ax.bar(x, test_scores, width, label='测试集')
    ax.bar(x + width, cv_scores, width, label='交叉验证')

    ax.set_ylabel('准确率')
    ax.set_xlabel('alpha (正则化强度)')
    ax.set_title('正则化参数对性能的影响')
    ax.set_xticks(x)
    ax.set_xticklabels([str(a) for a in alphas])
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('regularization.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: regularization.png")


def demo_learning_rate():
    """学习率对比示例"""
    print("\n" + "=" * 60)
    print("6. 学习率对比示例")
    print("=" * 60)

    # 加载数据
    wine = load_wine()
    X, y = wine.data, wine.target

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.3, random_state=42
    )

    # 测试不同的学习率
    learning_rates = [0.001, 0.01, 0.1, 0.5, 1.0]

    print("\n不同学习率的性能:")
    print("-" * 50)

    loss_curves = {}
    for lr in learning_rates:
        mlp = MLPClassifier(
            hidden_layer_sizes=(100, 50),
            activation='relu',
            solver='adam',
            learning_rate_init=lr,
            max_iter=500,
            random_state=42,
            verbose=False
        )
        mlp.fit(X_train, y_train)

        test_acc = mlp.score(X_test, y_test)
        loss_curves[lr] = mlp.loss_curve_

        print(f"lr={lr:5.3f}: "
              f"测试准确率={test_acc:.4f}, "
              f"迭代次数={mlp.n_iter_}")

    # 可视化损失曲线
    fig, ax = plt.subplots(figsize=(10, 6))

    for lr, curve in loss_curves.items():
        ax.plot(curve, label=f'lr={lr}', linewidth=2)

    ax.set_xlabel('迭代次数')
    ax.set_ylabel('损失值')
    ax.set_title('不同学习率的损失曲线')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 2])

    plt.tight_layout()
    plt.savefig('learning_rate.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: learning_rate.png")


def demo_solvers():
    """优化器对比示例"""
    print("\n" + "=" * 60)
    print("7. 优化器 (solver) 对比示例")
    print("=" * 60)

    # 加载数据
    wine = load_wine()
    X, y = wine.data, wine.target

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.3, random_state=42
    )

    # 测试不同的优化器
    solvers = ['adam', 'sgd', 'lbfgs']

    print("\n不同优化器的性能:")
    print("-" * 50)

    results = {}
    for solver in solvers:
        mlp = MLPClassifier(
            hidden_layer_sizes=(100, 50),
            activation='relu',
            solver=solver,
            max_iter=1000,
            random_state=42,
            verbose=False
        )
        mlp.fit(X_train, y_train)

        train_acc = mlp.score(X_train, y_train)
        test_acc = mlp.score(X_test, y_test)
        cv_acc = cross_val_score(mlp, X_scaled, y, cv=5).mean()

        results[solver] = {
            'train': train_acc,
            'test': test_acc,
            'cv': cv_acc,
            'n_iter': mlp.n_iter_
        }

        # lbfgs没有loss_curve_
        has_loss_curve = hasattr(mlp, 'loss_curve_')
        loss_info = f"损失曲线: {'有' if has_loss_curve else '无'}"

        print(f"{solver:6s}: "
              f"测试准确率={test_acc:.4f}, "
              f"CV准确率={cv_acc:.4f}, "
              f"迭代次数={mlp.n_iter_}, "
              f"{loss_info}")

    # 可视化
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # 准确率对比
    x = np.arange(len(solvers))
    width = 0.25

    train_scores = [results[s]['train'] for s in solvers]
    test_scores = [results[s]['test'] for s in solvers]
    cv_scores = [results[s]['cv'] for s in solvers]

    ax1.bar(x - width, train_scores, width, label='训练集')
    ax1.bar(x, test_scores, width, label='测试集')
    ax1.bar(x + width, cv_scores, width, label='交叉验证')

    ax1.set_ylabel('准确率')
    ax1.set_title('不同优化器的性能对比')
    ax1.set_xticks(x)
    ax1.set_xticklabels(solvers)
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')

    # 迭代次数
    iterations = [results[s]['n_iter'] for s in solvers]
    ax2.bar(solvers, iterations, color='orange', alpha=0.7)
    ax2.set_ylabel('迭代次数')
    ax2.set_title('不同优化器的收敛速度')
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('solvers_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: solvers_comparison.png")


def demo_decision_boundary():
    """决策边界可视化"""
    print("\n" + "=" * 60)
    print("8. 决策边界可视化")
    print("=" * 60)

    # 加载数据（只使用前两个特征）
    iris = load_iris()
    X = iris.data[:, :2]
    y = iris.target

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 训练不同复杂度的模型
    architectures = [(10,), (50,), (100, 50)]

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    print("\n不同复杂度的决策边界:")
    print("-" * 50)

    for idx, arch in enumerate(architectures):
        mlp = MLPClassifier(
            hidden_layer_sizes=arch,
            activation='relu',
            solver='adam',
            max_iter=1000,
            random_state=42,
            verbose=False
        )
        mlp.fit(X_scaled, y)

        acc = mlp.score(X_scaled, y)
        print(f"结构{arch}: 准确率={acc:.4f}")

        # 创建网格
        x_min, x_max = X_scaled[:, 0].min() - 1, X_scaled[:, 0].max() + 1
        y_min, y_max = X_scaled[:, 1].min() - 1, X_scaled[:, 1].max() + 1
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                             np.linspace(y_min, y_max, 200))

        # 预测
        Z = mlp.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        # 绘制
        axes[idx].contourf(xx, yy, Z, alpha=0.3, cmap='rainbow')
        scatter = axes[idx].scatter(X_scaled[:, 0], X_scaled[:, 1], c=y,
                                     cmap='rainbow', edgecolors='black',
                                     s=50, alpha=0.7)
        axes[idx].set_xlabel('特征1 (标准化)')
        axes[idx].set_ylabel('特征2 (标准化)')
        axes[idx].set_title(f'隐藏层结构: {arch}\n准确率: {acc:.4f}')

    plt.tight_layout()
    plt.savefig('mlp_decision_boundary.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: mlp_decision_boundary.png")


def main():
    """主函数"""
    print("神经网络算法演示程序")
    print("=" * 60)

    # 运行所有示例
    demo_mlp_classification_basic()
    demo_mlp_regression()
    demo_activation_functions()
    demo_hidden_layer_sizes()
    demo_regularization()
    demo_learning_rate()
    demo_solvers()
    demo_decision_boundary()

    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
