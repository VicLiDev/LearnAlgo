"""
回归算法示例
演示各种回归算法的使用方法
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def generate_data(n_samples=100, noise=10, random_state=42):
    """生成示例数据"""
    np.random.seed(random_state)
    X = np.random.rand(n_samples, 1) * 10
    y = 2 * X.ravel() + 1 + np.random.randn(n_samples) * noise
    return X, y


def generate_nonlinear_data(n_samples=100, noise=5, random_state=42):
    """生成非线性数据"""
    np.random.seed(random_state)
    X = np.sort(np.random.rand(n_samples, 1) * 5, axis=0)
    y = np.sin(X).ravel() + np.random.randn(n_samples) * noise * 0.1
    return X, y


def print_metrics(y_true, y_pred, model_name):
    """打印评估指标"""
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    print(f"\n{model_name} 评估指标:")
    print(f"  MSE:  {mse:.4f}")
    print(f"  RMSE: {rmse:.4f}")
    print(f"  MAE:  {mae:.4f}")
    print(f"  R²:   {r2:.4f}")
    return r2


def plot_results(X_test, y_test, predictions, title, filename):
    """绘制结果"""
    plt.figure(figsize=(12, 5))

    # 排序用于绘制平滑曲线
    sort_idx = np.argsort(X_test.ravel())

    plt.subplot(1, 2, 1)
    plt.scatter(X_test, y_test, alpha=0.5, label='真实值', s=30)

    for name, y_pred in predictions.items():
        plt.plot(X_test[sort_idx], y_pred[sort_idx],
                 label=name, linewidth=2, alpha=0.8)

    plt.xlabel('X')
    plt.ylabel('y')
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)

    # 绘制残差图
    plt.subplot(1, 2, 2)
    for name, y_pred in predictions.items():
        residuals = y_test - y_pred
        plt.scatter(y_pred, residuals, alpha=0.5, label=f'{name} 残差', s=30)

    plt.axhline(y=0, color='r', linestyle='--', linewidth=1)
    plt.xlabel('预测值')
    plt.ylabel('残差')
    plt.title('残差图')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n图表已保存: {filename}")


def demo_linear_regression():
    """线性回归示例"""
    print("=" * 60)
    print("1. 线性回归示例")
    print("=" * 60)

    # 生成数据
    X, y = generate_data(n_samples=200, noise=5)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # 训练模型
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print(f"\n模型参数:")
    print(f"  斜率 (w): {model.coef_[0]:.4f}")
    print(f"  截距 (b): {model.intercept_:.4f}")

    print_metrics(y_test, y_pred, "线性回归")

    # 可视化
    predictions = {"线性回归": y_pred}
    plot_results(X_test, y_test, predictions,
                 "线性回归", "linear_regression.png")


def demo_polynomial_regression():
    """多项式回归示例"""
    print("\n" + "=" * 60)
    print("2. 多项式回归示例")
    print("=" * 60)

    # 生成非线性数据
    X, y = generate_nonlinear_data(n_samples=200, noise=2)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    predictions = {}

    # 尝试不同次数的多项式
    for degree in [1, 3, 5, 10]:
        model = Pipeline([
            ('poly', PolynomialFeatures(degree=degree)),
            ('linear', LinearRegression())
        ])
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        predictions[f'{degree}次多项式'] = y_pred

        r2 = print_metrics(y_test, y_pred, f"{degree}次多项式回归")

    # 可视化
    plot_results(X_test, y_test, predictions,
                 "多项式回归对比", "polynomial_regression.png")


def demo_regularized_regression():
    """正则化回归示例 (Ridge, Lasso, ElasticNet)"""
    print("\n" + "=" * 60)
    print("3. 正则化回归示例")
    print("=" * 60)

    # 生成数据
    X, y = generate_data(n_samples=200, noise=5)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    predictions = {}

    # 1. 线性回归（基线）
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    predictions['线性回归'] = y_pred_lr
    print_metrics(y_test, y_pred_lr, "线性回归")

    # 2. 岭回归
    ridge = Ridge(alpha=1.0)
    ridge.fit(X_train, y_train)
    y_pred_ridge = ridge.predict(X_test)
    predictions['岭回归'] = y_pred_ridge
    print_metrics(y_test, y_pred_ridge, "岭回归 (α=1.0)")

    # 3. Lasso回归
    lasso = Lasso(alpha=0.1)
    lasso.fit(X_train, y_train)
    y_pred_lasso = lasso.predict(X_test)
    predictions['Lasso'] = y_pred_lasso
    print_metrics(y_test, y_pred_lasso, "Lasso (α=0.1)")

    # 4. 弹性网络
    elastic = ElasticNet(alpha=0.1, l1_ratio=0.5)
    elastic.fit(X_train, y_train)
    y_pred_elastic = elastic.predict(X_test)
    predictions['弹性网络'] = y_pred_elastic
    print_metrics(y_test, y_pred_elastic, "弹性网络 (α=0.1, l1_ratio=0.5)")

    # 可视化
    plot_results(X_test, y_test, predictions,
                 "正则化回归对比", "regularized_regression.png")


def demo_ridge_alpha_tuning():
    """岭回归参数调优示例"""
    print("\n" + "=" * 60)
    print("4. 岭回归参数调优示例")
    print("=" * 60)

    # 生成数据
    X, y = generate_data(n_samples=200, noise=5)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # 测试不同的alpha值
    alphas = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]
    train_scores = []
    test_scores = []

    print("\n不同alpha值的R²分数:")
    print("-" * 40)

    for alpha in alphas:
        ridge = Ridge(alpha=alpha)
        ridge.fit(X_train, y_train)

        train_pred = ridge.predict(X_train)
        test_pred = ridge.predict(X_test)

        train_r2 = r2_score(y_train, train_pred)
        test_r2 = r2_score(y_test, test_pred)

        train_scores.append(train_r2)
        test_scores.append(test_r2)

        print(f"α={alpha:6.3f}: 训练R²={train_r2:.4f}, 测试R²={test_r2:.4f}")

    # 绘制学习曲线
    plt.figure(figsize=(10, 6))
    plt.semilogx(alphas, train_scores, 'o-', label='训练集 R²', linewidth=2)
    plt.semilogx(alphas, test_scores, 's-', label='测试集 R²', linewidth=2)
    plt.xlabel('Alpha (正则化强度)')
    plt.ylabel('R² 分数')
    plt.title('岭回归参数调优')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('ridge_alpha_tuning.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: ridge_alpha_tuning.png")


def main():
    """主函数"""
    print("回归算法演示程序")
    print("=" * 60)

    # 运行所有示例
    demo_linear_regression()
    demo_polynomial_regression()
    demo_regularized_regression()
    demo_ridge_alpha_tuning()

    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
