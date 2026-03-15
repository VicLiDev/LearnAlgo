"""
随机森林算法示例
演示随机森林分类和回归的使用方法
"""

import numpy as np
import matplotlib.pyplot as plt
from t01_mpl import chinese_font
from sklearn.datasets import load_iris, load_wine, load_breast_cancer, make_regression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, mean_squared_error, r2_score)
import time
import warnings
warnings.filterwarnings('ignore')



def demo_basic_classification():
    """随机森林分类基础示例"""
    print("=" * 60)
    print("1. 随机森林分类基础示例")
    print("=" * 60)

    # 加载数据
    wine = load_wine()
    X, y = wine.data, wine.target
    feature_names = wine.feature_names
    class_names = wine.target_names

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # 训练模型
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1,
        oob_score=True
    )
    rf.fit(X_train, y_train)

    # 预测
    y_pred = rf.predict(X_test)

    # 评估
    train_acc = rf.score(X_train, y_train)
    test_acc = accuracy_score(y_test, y_pred)
    oob_acc = rf.oob_score_

    print(f"\n模型参数:")
    print(f"  树的数量: {rf.n_estimators}")
    print(f"  最大深度: {rf.max_depth}")

    print(f"\n评估指标:")
    print(f"  训练准确率: {train_acc:.4f}")
    print(f"  测试准确率: {test_acc:.4f}")
    print(f"  OOB准确率: {oob_acc:.4f}")

    print("\n分类报告:")
    print(classification_report(y_test, y_pred, target_names=class_names))

    # 特征重要性
    importance = rf.feature_importances_
    indices = np.argsort(importance)[::-1]

    print("\n前5个最重要的特征:")
    for i in range(min(5, len(feature_names))):
        idx = indices[i]
        print(f"  {i+1}. {feature_names[idx]}: {importance[idx]:.4f}")

    # 可视化特征重要性
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(importance)), importance[indices], align='center')
    plt.xticks(range(len(importance)), [feature_names[i] for i in indices],
               rotation=45, ha='right')
    plt.xlabel('特征')
    plt.ylabel('重要性')
    plt.title('随机森林特征重要性')
    plt.tight_layout()
    plt.savefig('rf_feature_importance.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: rf_feature_importance.png")


def demo_regression():
    """随机森林回归示例"""
    print("\n" + "=" * 60)
    print("2. 随机森林回归示例")
    print("=" * 60)

    # 生成数据
    np.random.seed(42)
    X = np.sort(10 * np.random.rand(500, 1), axis=0)
    y = np.sin(X).ravel() + np.random.randn(500) * 0.3

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # 训练模型
    rf = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1,
        oob_score=True
    )
    rf.fit(X_train, y_train)

    # 预测
    y_pred = rf.predict(X_test)

    # 评估
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    oob_r2 = rf.oob_score_

    print(f"\n评估指标:")
    print(f"  MSE: {mse:.4f}")
    print(f"  RMSE: {rmse:.4f}")
    print(f"  R²: {r2:.4f}")
    print(f"  OOB R²: {oob_r2:.4f}")

    # 可视化
    plt.figure(figsize=(12, 6))

    # 排序用于绘制
    sort_idx = np.argsort(X_test.ravel())

    plt.scatter(X_test, y_test, alpha=0.5, s=30, label='真实值')
    plt.plot(X_test[sort_idx], y_pred[sort_idx], 'r-', linewidth=2, label='预测值', alpha=0.8)

    plt.xlabel('X')
    plt.ylabel('y')
    plt.title(f'随机森林回归 (R²={r2:.4f})')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('rf_regression.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: rf_regression.png")


def demo_n_estimators_tuning():
    """树数量调优示例"""
    print("\n" + "=" * 60)
    print("3. 树数量调优示例")
    print("=" * 60)

    # 加载数据
    data = load_breast_cancer()
    X, y = data.data, data.target

    # 测试不同的树数量
    n_estimators_list = [10, 20, 50, 100, 150, 200, 300, 500]
    train_scores = []
    test_scores = []
    oob_scores = []
    times = []

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    print("\n不同树数量的性能:")
    print("-" * 60)

    for n_est in n_estimators_list:
        start_time = time.time()

        rf = RandomForestClassifier(
            n_estimators=n_est,
            random_state=42,
            n_jobs=-1,
            oob_score=True
        )
        rf.fit(X_train, y_train)

        elapsed = time.time() - start_time

        train_scores.append(rf.score(X_train, y_train))
        test_scores.append(rf.score(X_test, y_test))
        oob_scores.append(rf.oob_score_)
        times.append(elapsed)

        print(f"n_estimators={n_est:3d}: "
              f"测试准确率={rf.score(X_test, y_test):.4f}, "
              f"OOB={rf.oob_score_:.4f}, "
              f"耗时={elapsed:.3f}s")

    # 可视化
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # 准确率曲线
    ax1.plot(n_estimators_list, train_scores, 'o-', label='训练集', linewidth=2)
    ax1.plot(n_estimators_list, test_scores, 's-', label='测试集', linewidth=2)
    ax1.plot(n_estimators_list, oob_scores, '^-', label='OOB', linewidth=2)
    ax1.set_xlabel('树的数量')
    ax1.set_ylabel('准确率')
    ax1.set_title('树数量对准确率的影响')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 训练时间曲线
    ax2.plot(n_estimators_list, times, 'o-', linewidth=2, color='green')
    ax2.set_xlabel('树的数量')
    ax2.set_ylabel('训练时间 (秒)')
    ax2.set_title('树数量对训练时间的影响')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('rf_n_estimators_tuning.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: rf_n_estimators_tuning.png")


def demo_comparison_with_decision_tree():
    """随机森林与决策树对比"""
    print("\n" + "=" * 60)
    print("4. 随机森林 vs 决策树对比")
    print("=" * 60)

    # 加载数据
    iris = load_iris()
    X, y = iris.data, iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # 决策树
    dt = DecisionTreeClassifier(random_state=42)
    dt.fit(X_train, y_train)
    dt_train_acc = dt.score(X_train, y_train)
    dt_test_acc = dt.score(X_test, y_test)
    dt_cv_acc = cross_val_score(dt, X, y, cv=5, scoring='accuracy').mean()

    # 随机森林
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    rf_train_acc = rf.score(X_train, y_train)
    rf_test_acc = rf.score(X_test, y_test)
    rf_cv_acc = cross_val_score(rf, X, y, cv=5, scoring='accuracy').mean()

    print("\n决策树:")
    print(f"  训练准确率: {dt_train_acc:.4f}")
    print(f"  测试准确率: {dt_test_acc:.4f}")
    print(f"  交叉验证准确率: {dt_cv_acc:.4f}")

    print("\n随机森林:")
    print(f"  训练准确率: {rf_train_acc:.4f}")
    print(f"  测试准确率: {rf_test_acc:.4f}")
    print(f"  交叉验证准确率: {rf_cv_acc:.4f}")

    # 可视化对比
    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(3)
    width = 0.35

    dt_scores = [dt_train_acc, dt_test_acc, dt_cv_acc]
    rf_scores = [rf_train_acc, rf_test_acc, rf_cv_acc]

    bars1 = ax.bar(x - width/2, dt_scores, width, label='决策树', color='#1f77b4')
    bars2 = ax.bar(x + width/2, rf_scores, width, label='随机森林', color='#ff7f0e')

    ax.set_ylabel('准确率')
    ax.set_title('决策树 vs 随机森林')
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
    plt.savefig('rf_vs_dt.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: rf_vs_dt.png")


def demo_extra_trees():
    """极端随机树示例"""
    print("\n" + "=" * 60)
    print("5. 极端随机树 (Extra Trees) 示例")
    print("=" * 60)

    # 加载数据
    data = load_breast_cancer()
    X, y = data.data, data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # 训练时间对比
    print("\n训练时间对比:")

    # 随机森林
    start = time.time()
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    rf_time = time.time() - start
    rf_acc = rf.score(X_test, y_test)

    # 极端随机树
    start = time.time()
    et = ExtraTreesClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    et.fit(X_train, y_train)
    et_time = time.time() - start
    et_acc = et.score(X_test, y_test)

    print(f"  随机森林: 训练时间={rf_time:.3f}s, 准确率={rf_acc:.4f}")
    print(f"  极端随机树: 训练时间={et_time:.3f}s, 准确率={et_acc:.4f}")

    # 可视化对比
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # 准确率对比
    algorithms = ['随机森林', '极端随机树']
    accuracies = [rf_acc, et_acc]
    colors = ['#1f77b4', '#ff7f0e']

    ax1.bar(algorithms, accuracies, color=colors)
    ax1.set_ylabel('准确率')
    ax1.set_title('准确率对比')
    ax1.set_ylim([0.9, 1.0])
    for i, v in enumerate(accuracies):
        ax1.text(i, v + 0.005, f'{v:.4f}', ha='center', va='bottom')
    ax1.grid(True, alpha=0.3, axis='y')

    # 训练时间对比
    times = [rf_time, et_time]
    ax2.bar(algorithms, times, color=colors)
    ax2.set_ylabel('训练时间 (秒)')
    ax2.set_title('训练时间对比')
    for i, v in enumerate(times):
        ax2.text(i, v + 0.01, f'{v:.3f}s', ha='center', va='bottom')
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('rf_vs_extra_trees.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: rf_vs_extra_trees.png")


def demo_oob_error():
    """OOB误差分析"""
    print("\n" + "=" * 60)
    print("6. OOB误差分析")
    print("=" * 60)

    # 加载数据
    data = load_breast_cancer()
    X, y = data.data, data.target

    # 测试不同的树数量
    n_estimators_list = range(10, 201, 10)
    oob_errors = []

    for n_est in n_estimators_list:
        rf = RandomForestClassifier(
            n_estimators=n_est,
            random_state=42,
            n_jobs=-1,
            oob_score=True
        )
        rf.fit(X, y)
        oob_error = 1 - rf.oob_score_
        oob_errors.append(oob_error)

    # 找到最佳树数量
    best_idx = np.argmin(oob_errors)
    best_n_est = n_estimators_list[best_idx]

    print(f"\n最佳树数量: {best_n_est}")
    print(f"最低OOB误差: {oob_errors[best_idx]:.4f}")

    # 可视化
    plt.figure(figsize=(10, 6))
    plt.plot(n_estimators_list, oob_errors, 'o-', linewidth=2)
    plt.axhline(y=oob_errors[best_idx], color='r', linestyle='--', alpha=0.5)
    plt.axvline(x=best_n_est, color='r', linestyle='--', alpha=0.5)
    plt.scatter([best_n_est], [oob_errors[best_idx]], color='red', s=100, zorder=5)
    plt.xlabel('树的数量')
    plt.ylabel('OOB误差')
    plt.title(f'OOB误差随树数量的变化\n最佳: {best_n_est}棵树')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('rf_oob_error.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: rf_oob_error.png")


def demo_max_features():
    """max_features参数影响"""
    print("\n" + "=" * 60)
    print("7. max_features参数影响")
    print("=" * 60)

    # 加载数据
    data = load_breast_cancer()
    n_features = data.data.shape[1]
    X, y = data.data, data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # 测试不同的max_features
    max_features_options = ['sqrt', 'log2', None, 0.5, 0.3]
    results = {}

    print("\n不同max_features的性能:")
    print("-" * 60)

    for max_feat in max_features_options:
        rf = RandomForestClassifier(
            n_estimators=100,
            max_features=max_feat,
            random_state=42,
            n_jobs=-1
        )
        rf.fit(X_train, y_train)

        train_acc = rf.score(X_train, y_train)
        test_acc = rf.score(X_test, y_test)
        cv_acc = cross_val_score(rf, X, y, cv=5, scoring='accuracy').mean()

        # 计算实际使用的特征数
        if max_feat is None:
            actual_features = n_features
        elif isinstance(max_feat, float):
            actual_features = int(max_feat * n_features)
        elif max_feat == 'sqrt':
            actual_features = int(np.sqrt(n_features))
        elif max_feat == 'log2':
            actual_features = int(np.log2(n_features))

        results[str(max_feat)] = {
            'train': train_acc,
            'test': test_acc,
            'cv': cv_acc,
            'features': actual_features
        }

        print(f"max_features={str(max_feat):6s}: "
              f"测试准确率={test_acc:.4f}, "
              f"CV准确率={cv_acc:.4f}, "
              f"实际特征数={actual_features}")

    # 可视化
    fig, ax = plt.subplots(figsize=(12, 6))

    labels = list(results.keys())
    test_scores = [results[k]['test'] for k in labels]
    cv_scores = [results[k]['cv'] for k in labels]

    x = np.arange(len(labels))
    width = 0.35

    ax.bar(x - width/2, test_scores, width, label='测试集', color='#1f77b4')
    ax.bar(x + width/2, cv_scores, width, label='交叉验证', color='#ff7f0e')

    ax.set_ylabel('准确率')
    ax.set_xlabel('max_features')
    ax.set_title('max_features对模型性能的影响')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_ylim([0.9, 1.0])
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('rf_max_features.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: rf_max_features.png")


def main():
    """主函数"""
    print("随机森林算法演示程序")
    print("=" * 60)

    # 运行所有示例
    demo_basic_classification()
    demo_regression()
    demo_n_estimators_tuning()
    demo_comparison_with_decision_tree()
    demo_extra_trees()
    demo_oob_error()
    demo_max_features()

    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
