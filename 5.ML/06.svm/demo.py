"""
支持向量机算法示例
演示SVM分类和回归的使用方法
"""

import numpy as np
import matplotlib.pyplot as plt
from t01_mpl import chinese_font
from sklearn import svm
from sklearn.datasets import load_iris, load_wine, make_classification, make_regression
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score, classification_report,
                             mean_squared_error, r2_score)
import warnings
warnings.filterwarnings('ignore')



def make_meshgrid(x, y, h=.02):
    """创建网格用于绘制决策边界"""
    x_min, x_max = x.min() - 1, x.max() + 1
    y_min, y_max = y.min() - 1, y.max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    return xx, yy


def plot_contours(ax, clf, xx, yy, **params):
    """绘制决策边界"""
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    out = ax.contourf(xx, yy, Z, **params)
    return out


def demo_linear_svm():
    """线性SVM示例"""
    print("=" * 60)
    print("1. 线性SVM示例")
    print("=" * 60)

    # 生成线性可分数据
    X, y = make_classification(n_samples=200, n_features=2, n_redundant=0,
                                n_informative=2, random_state=42, n_clusters_per_class=1)

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.3, random_state=42
    )

    # 训练模型
    clf = svm.SVC(kernel='linear', C=1.0)
    clf.fit(X_train, y_train)

    # 评估
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\n模型参数:")
    print(f"  核函数: linear")
    print(f"  C: 1.0")
    print(f"  支持向量数量: {len(clf.support_vectors_)}")

    print(f"\n评估指标:")
    print(f"  测试准确率: {accuracy:.4f}")

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 8))

    # 绘制决策边界
    xx, yy = make_meshgrid(X_scaled[:, 0], X_scaled[:, 1])
    plot_contours(ax, clf, xx, yy, cmap=plt.cm.coolwarm, alpha=0.3)

    # 绘制数据点
    ax.scatter(X_scaled[:, 0], X_scaled[:, 1], c=y, cmap=plt.cm.coolwarm,
               s=50, edgecolors='k', alpha=0.7)

    # 标记支持向量
    ax.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1],
               s=100, linewidth=1.5, facecolors='none', edgecolors='green',
               label='支持向量')

    ax.set_xlabel('特征1')
    ax.set_ylabel('特征2')
    ax.set_title(f'线性SVM决策边界\n准确率: {accuracy:.4f}')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('svm_linear.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: svm_linear.png")


def demo_kernel_comparison():
    """核函数对比示例"""
    print("\n" + "=" * 60)
    print("2. 核函数对比示例")
    print("=" * 60)

    # 生成非线性数据（环形数据）
    from sklearn.datasets import make_circles
    X, y = make_circles(n_samples=300, noise=0.1, factor=0.5, random_state=42)

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 定义不同的核函数
    kernels = {
        '线性核': svm.SVC(kernel='linear', C=1.0),
        '多项式核': svm.SVC(kernel='poly', degree=3, C=1.0),
        'RBF核': svm.SVC(kernel='rbf', C=1.0, gamma='scale'),
        'Sigmoid核': svm.SVC(kernel='sigmoid', C=1.0)
    }

    # 可视化
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    axes = axes.ravel()

    xx, yy = make_meshgrid(X_scaled[:, 0], X_scaled[:, 1])

    print("\n不同核函数的性能:")
    print("-" * 50)

    for idx, (name, clf) in enumerate(kernels.items()):
        # 训练
        clf.fit(X_scaled, y)

        # 评估
        y_pred = clf.predict(X_scaled)
        acc = accuracy_score(y, y_pred)
        cv_acc = cross_val_score(clf, X_scaled, y, cv=5).mean()

        print(f"{name}:")
        print(f"  训练准确率: {acc:.4f}")
        print(f"  交叉验证准确率: {cv_acc:.4f}")
        print(f"  支持向量数: {len(clf.support_vectors_)}")

        # 绘制决策边界
        plot_contours(axes[idx], clf, xx, yy, cmap=plt.cm.coolwarm, alpha=0.3)
        axes[idx].scatter(X_scaled[:, 0], X_scaled[:, 1], c=y,
                          cmap=plt.cm.coolwarm, s=30, edgecolors='k', alpha=0.7)
        axes[idx].set_xlabel('特征1')
        axes[idx].set_ylabel('特征2')
        axes[idx].set_title(f'{name}\n准确率: {acc:.4f}')
        axes[idx].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('svm_kernel_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: svm_kernel_comparison.png")


def demo_c_gamma_tuning():
    """C和gamma参数调优示例"""
    print("\n" + "=" * 60)
    print("3. C和gamma参数调优示例")
    print("=" * 60)

    # 加载数据
    iris = load_iris()
    X, y = iris.data, iris.target

    # 只使用前两个特征用于可视化
    X = X[:, :2]

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 测试不同的C和gamma值
    C_values = [0.1, 1, 10, 100]
    gamma_values = [0.1, 1, 10, 100]

    fig, axes = plt.subplots(4, 4, figsize=(16, 16))

    print("\n不同(C, gamma)组合的准确率:")
    print("-" * 60)

    results = []
    for i, C in enumerate(C_values):
        for j, gamma in enumerate(gamma_values):
            # 训练模型
            clf = svm.SVC(kernel='rbf', C=C, gamma=gamma)
            clf.fit(X_scaled, y)

            # 评估
            y_pred = clf.predict(X_scaled)
            acc = accuracy_score(y, y_pred)
            results.append((C, gamma, acc))

            print(f"C={C:6.1f}, gamma={gamma:6.1f}: 准确率={acc:.4f}")

            # 绘制决策边界
            xx, yy = make_meshgrid(X_scaled[:, 0], X_scaled[:, 1])
            plot_contours(axes[i, j], clf, xx, yy, cmap=plt.cm.coolwarm, alpha=0.3)
            axes[i, j].scatter(X_scaled[:, 0], X_scaled[:, 1], c=y,
                               cmap=plt.cm.coolwarm, s=20, edgecolors='k', alpha=0.5)
            axes[i, j].set_xlabel(f'γ={gamma}')
            axes[i, j].set_ylabel(f'C={C}')
            axes[i, j].set_title(f'acc={acc:.2f}')
            axes[i, j].grid(True, alpha=0.3)

    plt.suptitle('RBF SVM: C和gamma参数对决策边界的影响', fontsize=14)
    plt.tight_layout()
    plt.savefig('svm_c_gamma_tuning.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: svm_c_gamma_tuning.png")


def demo_grid_search():
    """网格搜索调参示例"""
    print("\n" + "=" * 60)
    print("4. 网格搜索调参示例")
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

    # 定义参数网格
    param_grid = {
        'C': [0.1, 1, 10, 100],
        'gamma': ['scale', 'auto', 0.001, 0.01, 0.1, 1],
        'kernel': ['rbf', 'poly', 'sigmoid']
    }

    # 网格搜索
    print("\n正在执行网格搜索...")
    grid_search = GridSearchCV(
        svm.SVC(),
        param_grid,
        cv=5,
        scoring='accuracy',
        n_jobs=-1,
        verbose=0
    )
    grid_search.fit(X_train, y_train)

    print(f"\n最佳参数:")
    for param, value in grid_search.best_params_.items():
        print(f"  {param}: {value}")

    print(f"\n最佳交叉验证分数: {grid_search.best_score_:.4f}")

    # 在测试集上评估
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    test_acc = accuracy_score(y_test, y_pred)

    print(f"测试集准确率: {test_acc:.4f}")

    print("\n分类报告:")
    print(classification_report(y_test, y_pred, target_names=wine.target_names))


def demo_svr():
    """SVM回归示例"""
    print("\n" + "=" * 60)
    print("5. SVM回归 (SVR) 示例")
    print("=" * 60)

    # 生成数据
    np.random.seed(42)
    X = np.sort(5 * np.random.rand(200, 1), axis=0)
    y = np.sin(X).ravel() + np.random.randn(200) * 0.1

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # 标准化
    scaler_X = StandardScaler()
    scaler_y = StandardScaler()
    X_train_scaled = scaler_X.fit_transform(X_train)
    X_test_scaled = scaler_X.transform(X_test)
    y_train_scaled = scaler_y.fit_transform(y_train.reshape(-1, 1)).ravel()

    # 训练不同的SVR模型
    models = {
        '线性SVR': svm.SVR(kernel='linear', C=1.0),
        'RBF SVR': svm.SVR(kernel='rbf', C=1.0, gamma='scale'),
        '多项式SVR': svm.SVR(kernel='poly', degree=3, C=1.0)
    }

    # 可视化
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    print("\n不同SVR的性能:")
    print("-" * 50)

    for idx, (name, model) in enumerate(models.items()):
        # 训练
        model.fit(X_train_scaled, y_train_scaled)

        # 预测
        y_pred_scaled = model.predict(X_test_scaled)
        y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1)).ravel()

        # 评估
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"{name}:")
        print(f"  MSE: {mse:.4f}")
        print(f"  R²: {r2:.4f}")

        # 可视化
        X_plot = np.linspace(X.min(), X.max(), 500).reshape(-1, 1)
        X_plot_scaled = scaler_X.transform(X_plot)
        y_plot_scaled = model.predict(X_plot_scaled)
        y_plot = scaler_y.inverse_transform(y_plot_scaled.reshape(-1, 1)).ravel()

        axes[idx].scatter(X_test, y_test, alpha=0.5, s=30, label='测试数据')
        axes[idx].plot(X_plot, y_plot, 'r-', linewidth=2, label='预测')
        axes[idx].set_xlabel('X')
        axes[idx].set_ylabel('y')
        axes[idx].set_title(f'{name}\nMSE={mse:.4f}, R²={r2:.4f}')
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('svr_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: svr_comparison.png")


def demo_one_class_svm():
    """单类SVM异常检测示例"""
    print("\n" + "=" * 60)
    print("6. 单类SVM异常检测示例")
    print("=" * 60)

    # 生成正常数据
    np.random.seed(42)
    X_train = 0.3 * np.random.randn(100, 2)
    X_train = np.r_[X_train + 2, X_train - 2]

    # 生成测试数据（包含异常点）
    X_test = 0.3 * np.random.randn(20, 2)
    X_test = np.r_[X_test + 2, X_test - 2]
    X_outliers = np.random.uniform(low=-4, high=4, size=(20, 2))

    # 训练单类SVM
    clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
    clf.fit(X_train)

    # 预测
    y_pred_train = clf.predict(X_train)
    y_pred_test = clf.predict(X_test)
    y_pred_outliers = clf.predict(X_outliers)

    # 计算正确率
    n_error_train = y_pred_train[y_pred_train == -1].size
    n_error_test = y_pred_test[y_pred_test == -1].size
    n_error_outliers = y_pred_outliers[y_pred_outliers == 1].size

    print(f"\n正常数据误判为异常的比例: {n_error_train/len(X_train):.2%}")
    print(f"测试数据误判为异常的比例: {n_error_test/len(X_test):.2%}")
    print(f"异常点正确识别的比例: {1-n_error_outliers/len(X_outliers):.2%}")

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 8))

    # 创建网格
    xx, yy = make_meshgrid(np.linspace(-5, 5, 500), np.linspace(-5, 5, 500))

    # 绘制决策边界
    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    ax.contour(xx, yy, Z, levels=[0], linewidths=2, colors='black')
    ax.contourf(xx, yy, Z, levels=np.linspace(Z.min(), 0, 7),
                cmap=plt.cm.Blues_r, alpha=0.3)
    ax.contourf(xx, yy, Z, levels=np.linspace(0, Z.max(), 7),
                cmap=plt.cm.Oranges, alpha=0.3)

    # 绘制数据点
    ax.scatter(X_train[:, 0], X_train[:, 1], c='white', s=40,
               edgecolors='k', label='训练数据')
    ax.scatter(X_test[:, 0], X_test[:, 1], c='green', s=40,
               edgecolors='k', label='测试数据')
    ax.scatter(X_outliers[:, 0], X_outliers[:, 1], c='red', s=40,
               edgecolors='k', label='异常点')

    ax.set_xlabel('特征1')
    ax.set_ylabel('特征2')
    ax.set_title('单类SVM异常检测')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim([-5, 5])
    ax.set_ylim([-5, 5])

    plt.tight_layout()
    plt.savefig('one_class_svm.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: one_class_svm.png")


def demo_svm_vs_logistic():
    """SVM vs 逻辑回归对比"""
    print("\n" + "=" * 60)
    print("7. SVM vs 逻辑回归对比")
    print("=" * 60)

    from sklearn.linear_model import LogisticRegression

    # 加载数据
    iris = load_iris()
    X, y = iris.data, iris.target

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.3, random_state=42
    )

    # 训练模型
    models = {
        'SVM (RBF)': svm.SVC(kernel='rbf', C=1.0, gamma='scale'),
        '逻辑回归': LogisticRegression(max_iter=1000, random_state=42)
    }

    results = {}
    for name, model in models.items():
        # 训练
        model.fit(X_train, y_train)

        # 评估
        train_acc = model.score(X_train, y_train)
        test_acc = model.score(X_test, y_test)
        cv_acc = cross_val_score(model, X_scaled, y, cv=5).mean()

        results[name] = {
            'train': train_acc,
            'test': test_acc,
            'cv': cv_acc
        }

        print(f"\n{name}:")
        print(f"  训练准确率: {train_acc:.4f}")
        print(f"  测试准确率: {test_acc:.4f}")
        print(f"  交叉验证准确率: {cv_acc:.4f}")

    # 可视化对比
    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(3)
    width = 0.35

    svm_scores = [results['SVM (RBF)']['train'],
                  results['SVM (RBF)']['test'],
                  results['SVM (RBF)']['cv']]
    lr_scores = [results['逻辑回归']['train'],
                 results['逻辑回归']['test'],
                 results['逻辑回归']['cv']]

    bars1 = ax.bar(x - width/2, svm_scores, width, label='SVM', color='#1f77b4')
    bars2 = ax.bar(x + width/2, lr_scores, width, label='逻辑回归', color='#ff7f0e')

    ax.set_ylabel('准确率')
    ax.set_title('SVM vs 逻辑回归')
    ax.set_xticks(x)
    ax.set_xticklabels(['训练集', '测试集', '交叉验证'])
    ax.legend()
    ax.set_ylim([0.9, 1.02])
    ax.grid(True, alpha=0.3, axis='y')

    # 添加数值标签
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('svm_vs_logistic.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: svm_vs_logistic.png")


def main():
    """主函数"""
    print("支持向量机算法演示程序")
    print("=" * 60)

    # 运行所有示例
    demo_linear_svm()
    demo_kernel_comparison()
    demo_c_gamma_tuning()
    demo_grid_search()
    demo_svr()
    demo_one_class_svm()
    demo_svm_vs_logistic()

    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
