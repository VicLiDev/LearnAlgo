"""
梯度提升算法 (Gradient Boosting) 示例代码

包含内容:
1. 基础GBDT分类与回归
2. 学习率和树数量的影响
3. XGBoost vs LightGBM对比
4. 特征重要性分析
5. 早停机制
"""

import numpy as np
import matplotlib.pyplot as plt
from t01_mpl import chinese_font
from sklearn.datasets import make_classification, make_regression, load_breast_cancer, load_diabetes
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import (
    GradientBoostingClassifier, GradientBoostingRegressor,
    AdaBoostClassifier
)
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 检查是否有XGBoost和LightGBM
try:
    import xgboost as xgb
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False
    print("警告: 未安装xgboost，部分示例将跳过")

try:
    import lightgbm as lgb
    HAS_LIGHTGBM = True
except ImportError:
    HAS_LIGHTGBM = False
    print("警告: 未安装lightgbm，部分示例将跳过")


def demo_basic_gbdt():
    """基础GBDT分类示例"""
    print("=" * 60)
    print("1. 基础GBDT分类示例")
    print("=" * 60)

    # 加载乳腺癌数据集
    data = load_breast_cancer()
    X, y = data.data, data.target
    feature_names = data.feature_names

    # 划分数据
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # 训练GBDT
    gbdt = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        random_state=42
    )
    gbdt.fit(X_train, y_train)

    # 预测
    y_pred = gbdt.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"数据集: 乳腺癌数据集")
    print(f"特征数: {X.shape[1]}")
    print(f"测试集准确率: {accuracy:.4f}")

    # 训练过程可视化 - 使用 staged_predict 手动计算分数
    train_scores = [accuracy_score(y_train, y_pred) for y_pred in gbdt.staged_predict(X_train)]
    test_scores = [accuracy_score(y_test, y_pred) for y_pred in gbdt.staged_predict(X_test)]

    # 特征重要性
    feature_importance = gbdt.feature_importances_
    sorted_idx = np.argsort(feature_importance)[::-1]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 训练过程
    ax1 = axes[0]
    ax1.plot(range(1, len(train_scores)+1), train_scores, 'b-', label='训练集')
    ax1.plot(range(1, len(test_scores)+1), test_scores, 'r-', label='测试集')
    ax1.set_xlabel('迭代次数 (树的数量)', fontsize=12)
    ax1.set_ylabel('准确率', fontsize=12)
    ax1.set_title('GBDT训练过程', fontsize=14)
    ax1.legend(loc='lower right')
    ax1.grid(True, alpha=0.3)

    # 特征重要性 (Top 10)
    ax2 = axes[1]
    top_n = 10
    ax2.barh(range(top_n), feature_importance[sorted_idx[:top_n]][::-1], color='steelblue')
    ax2.set_yticks(range(top_n))
    ax2.set_yticklabels([feature_names[i] for i in sorted_idx[:top_n]][::-1])
    ax2.set_xlabel('重要性', fontsize=12)
    ax2.set_title('特征重要性 (Top 10)', fontsize=14)

    plt.tight_layout()
    plt.savefig('gbdt_basic.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("GBDT基础图已保存为 gbdt_basic.png\n")


def demo_learning_rate_n_estimators():
    """学习率和树数量的影响"""
    print("=" * 60)
    print("2. 学习率和树数量的影响")
    print("=" * 60)

    # 生成数据
    X, y = make_classification(
        n_samples=1000, n_features=20, n_informative=15,
        n_redundant=5, random_state=42
    )

    # 划分数据
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # 测试不同学习率
    learning_rates = [0.01, 0.05, 0.1, 0.2, 0.5]
    n_estimators_range = range(10, 210, 10)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 学习率对比
    ax1 = axes[0]
    for lr in learning_rates:
        gbdt = GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=lr,
            max_depth=3,
            random_state=42
        )
        gbdt.fit(X_train, y_train)

        test_scores = [accuracy_score(y_test, y_pred) for y_pred in gbdt.staged_predict(X_test)]
        ax1.plot(range(10, 210, 10), test_scores[::10], label=f'lr={lr}')

    ax1.set_xlabel('迭代次数', fontsize=12)
    ax1.set_ylabel('测试集准确率', fontsize=12)
    ax1.set_title('不同学习率的学习曲线', fontsize=14)
    ax1.legend(loc='lower right')
    ax1.grid(True, alpha=0.3)

    # 树深度对比
    ax2 = axes[1]
    depths = [1, 2, 3, 5, 10]

    for depth in depths:
        gbdt = GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=depth,
            random_state=42
        )
        gbdt.fit(X_train, y_train)

        test_scores = [accuracy_score(y_test, y_pred) for y_pred in gbdt.staged_predict(X_test)]
        ax2.plot(range(10, 210, 10), test_scores[::10], label=f'depth={depth}')

    ax2.set_xlabel('迭代次数', fontsize=12)
    ax2.set_ylabel('测试集准确率', fontsize=12)
    ax2.set_title('不同树深度的学习曲线', fontsize=14)
    ax2.legend(loc='lower right')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('gbdt_learning_rate.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("学习率对比图已保存为 gbdt_learning_rate.png\n")

    print("观察:")
    print("  - 学习率大: 收敛快但可能过拟合，最终性能可能较差")
    print("  - 学习率小: 收敛慢但通常最终性能更好")
    print("  - 树深度大: 表达能力强但容易过拟合")
    print("  - 树深度小: 正则化效果好，泛化能力强\n")


def demo_adaboost():
    """AdaBoost示例"""
    print("=" * 60)
    print("3. AdaBoost示例")
    print("=" * 60)

    # 生成数据
    X, y = make_classification(
        n_samples=500, n_features=2, n_redundant=0, n_informative=2,
        n_clusters_per_class=1, random_state=42
    )

    # 划分数据
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # 不同数量的弱学习器
    n_estimators_list = [1, 5, 10, 50]

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    for idx, n_est in enumerate(n_estimators_list):
        ax = axes[idx]

        # 训练AdaBoost
        ada = AdaBoostClassifier(
            estimator=DecisionTreeClassifier(max_depth=1),
            n_estimators=n_est,
            learning_rate=1.0,
            random_state=42
        )
        ada.fit(X_train, y_train)

        # 预测
        y_pred = ada.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        # 绘制决策边界
        h = 0.02
        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))

        Z = ada.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.RdYlBu)
        ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test,
                  cmap=plt.cm.RdYlBu, edgecolors='black', s=30)

        ax.set_title(f'AdaBoost (n_estimators={n_est})\n准确率: {accuracy:.3f}', fontsize=12)
        ax.set_xlabel('特征1')
        ax.set_ylabel('特征2')

    plt.suptitle('AdaBoost: 弱学习器数量对决策边界的影响', fontsize=14)
    plt.tight_layout()
    plt.savefig('adaboost_decision_boundary.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("AdaBoost决策边界图已保存为 adaboost_decision_boundary.png\n")


def demo_xgboost_vs_lightgbm():
    """XGBoost vs LightGBM对比"""
    print("=" * 60)
    print("4. XGBoost vs LightGBM对比")
    print("=" * 60)

    if not HAS_XGBOOST and not HAS_LIGHTGBM:
        print("请安装xgboost和lightgbm以运行此示例")
        print("pip install xgboost lightgbm\n")
        return

    # 生成数据
    X, y = make_classification(
        n_samples=5000, n_features=20, n_informative=15,
        n_redundant=5, random_state=42
    )

    # 划分数据
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    results = {}

    # GBDT (sklearn)
    print("训练 GBDT (sklearn)...")
    gbdt = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
    gbdt.fit(X_train, y_train)
    results['GBDT'] = {
        'accuracy': accuracy_score(y_test, gbdt.predict(X_test))
    }

    # XGBoost
    if HAS_XGBOOST:
        print("训练 XGBoost...")
        xgb_model = xgb.XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=3,
                                       use_label_encoder=False, eval_metric='logloss', random_state=42)
        xgb_model.fit(X_train, y_train)
        results['XGBoost'] = {
            'accuracy': accuracy_score(y_test, xgb_model.predict(X_test))
        }

    # LightGBM
    if HAS_LIGHTGBM:
        print("训练 LightGBM...")
        lgb_model = lgb.LGBMClassifier(n_estimators=100, learning_rate=0.1, max_depth=3,
                                        verbose=-1, random_state=42)
        lgb_model.fit(X_train, y_train)
        results['LightGBM'] = {
            'accuracy': accuracy_score(y_test, lgb_model.predict(X_test))
        }

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 6))

    names = list(results.keys())
    accuracies = [results[n]['accuracy'] for n in names]
    colors = ['#3498db', '#e74c3c', '#2ecc71']

    bars = ax.bar(names, accuracies, color=colors[:len(names)], alpha=0.8)
    ax.set_ylabel('测试集准确率', fontsize=12)
    ax.set_title('梯度提升算法对比', fontsize=14)
    ax.set_ylim(0.8, 1.0)

    for bar, acc in zip(bars, accuracies):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
               f'{acc:.4f}', ha='center', va='bottom', fontsize=11)

    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('xgboost_vs_lightgbm.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("算法对比图已保存为 xgboost_vs_lightgbm.png\n")

    print("结果对比:")
    for name, res in results.items():
        print(f"  {name}: {res['accuracy']:.4f}")
    print()


def demo_regression():
    """GBDT回归示例"""
    print("=" * 60)
    print("5. GBDT回归示例")
    print("=" * 60)

    # 加载糖尿病数据集
    data = load_diabetes()
    X, y = data.data, data.target

    # 划分数据
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # 训练回归模型
    gbdt_reg = GradientBoostingRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        random_state=42
    )
    gbdt_reg.fit(X_train, y_train)

    # 预测
    y_pred = gbdt_reg.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    print(f"数据集: 糖尿病数据集")
    print(f"测试集RMSE: {rmse:.4f}")

    # 可视化
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 预测 vs 实际
    ax1 = axes[0]
    ax1.scatter(y_test, y_pred, alpha=0.5, edgecolors='black', linewidth=0.5)
    ax1.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    ax1.set_xlabel('实际值', fontsize=12)
    ax1.set_ylabel('预测值', fontsize=12)
    ax1.set_title(f'GBDT回归: 预测vs实际 (RMSE={rmse:.2f})', fontsize=14)
    ax1.grid(True, alpha=0.3)

    # 训练过程 - 使用 staged_predict 手动计算 R² 分数
    ax2 = axes[1]
    train_scores = [r2_score(y_train, y_pred) for y_pred in gbdt_reg.staged_predict(X_train)]
    test_scores = [r2_score(y_test, y_pred) for y_pred in gbdt_reg.staged_predict(X_test)]

    ax2.plot(range(1, len(train_scores)+1), train_scores, 'b-', label='训练集 R²')
    ax2.plot(range(1, len(test_scores)+1), test_scores, 'r-', label='测试集 R²')
    ax2.set_xlabel('迭代次数', fontsize=12)
    ax2.set_ylabel('R² 分数', fontsize=12)
    ax2.set_title('GBDT回归训练过程', fontsize=14)
    ax2.legend(loc='lower right')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('gbdt_regression.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("GBDT回归图已保存为 gbdt_regression.png\n")


def demo_early_stopping():
    """早停机制示例"""
    print("=" * 60)
    print("6. 早停机制示例")
    print("=" * 60)

    if not HAS_XGBOOST:
        print("需要安装xgboost以运行此示例")
        print("pip install xgboost\n")
        return

    # 生成数据
    X, y = make_classification(
        n_samples=1000, n_features=20, n_informative=15,
        n_redundant=5, random_state=42
    )

    # 划分数据
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # 无早停
    print("训练无早停的模型...")
    model_no_stop = xgb.XGBClassifier(
        n_estimators=500,
        learning_rate=0.1,
        max_depth=3,
        use_label_encoder=False,
        eval_metric='logloss',
        random_state=42
    )
    model_no_stop.fit(X_train, y_train, verbose=False)

    # 有早停
    print("训练有早停的模型...")
    model_early_stop = xgb.XGBClassifier(
        n_estimators=500,
        learning_rate=0.1,
        max_depth=3,
        early_stopping_rounds=10,
        use_label_encoder=False,
        eval_metric='logloss',
        random_state=42
    )
    model_early_stop.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 6))

    # 获取训练历史
    results_no_stop = model_no_stop.evals_result()
    results_early_stop = model_early_stop.evals_result()

    # 无早停的训练曲线（使用验证集评估）
    evals_result = model_early_stop.evals_result()['validation_0']['logloss']
    best_iteration = model_early_stop.best_iteration

    ax.plot(range(len(evals_result)), evals_result, 'b-', label='验证集LogLoss')
    ax.axvline(x=best_iteration, color='r', linestyle='--', label=f'早停点 (n={best_iteration})')
    ax.scatter([best_iteration], [evals_result[best_iteration]], color='red', s=100, zorder=5)

    ax.set_xlabel('迭代次数', fontsize=12)
    ax.set_ylabel('LogLoss', fontsize=12)
    ax.set_title('早停机制: 自动确定最优迭代次数', fontsize=14)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('early_stopping.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("早停机制图已保存为 early_stopping.png\n")

    print(f"早停最优迭代次数: {best_iteration}")
    print(f"无早停训练树数量: 500")
    print("\n早停的优势:")
    print("  - 防止过拟合")
    print("  - 减少训练时间")
    print("  - 自动确定最优树数量\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("梯度提升算法 (Gradient Boosting) 完整示例")
    print("=" * 60 + "\n")

    # 运行所有示例
    demo_basic_gbdt()
    demo_learning_rate_n_estimators()
    demo_adaboost()
    demo_xgboost_vs_lightgbm()
    demo_regression()
    demo_early_stopping()

    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
