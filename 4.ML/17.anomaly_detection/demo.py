"""
异常检测 (Anomaly Detection) 示例代码

包含内容:
1. 统计方法 (Z-score, IQR)
2. 局部离群因子 (LOF)
3. 孤立森林 (Isolation Forest)
4. One-Class SVM
5. 方法对比
6. 实战案例：信用卡欺诈检测
"""

import numpy as np
import matplotlib.pyplot as plt
from t01_mpl import chinese_font
from sklearn.datasets import make_blobs, make_circles, load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def demo_statistical_methods():
    """统计方法：Z-score和IQR"""
    print("=" * 60)
    print("1. 统计方法：Z-score和IQR")
    print("=" * 60)

    np.random.seed(42)

    # 生成正态分布数据 + 异常值
    normal_data = np.random.normal(0, 1, 1000)
    outliers = np.array([5, -4.5, 6, -5.5, 7])
    data = np.concatenate([normal_data, outliers])

    # Z-score方法
    mean = np.mean(data)
    std = np.std(data)
    z_scores = np.abs((data - mean) / std)
    z_outliers = data[z_scores > 3]

    # IQR方法
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    iqr_outliers = data[(data < lower_bound) | (data > upper_bound)]

    print(f"数据点数: {len(data)}")
    print(f"真实异常点数: {len(outliers)}")
    print(f"\nZ-score方法 (阈值=3):")
    print(f"  检测到异常点: {len(z_outliers)}个")
    print(f"  异常值: {sorted(z_outliers, reverse=True)[:5]}")

    print(f"\nIQR方法:")
    print(f"  下界: {lower_bound:.3f}, 上界: {upper_bound:.3f}")
    print(f"  检测到异常点: {len(iqr_outliers)}个")
    print(f"  异常值: {sorted(iqr_outliers, reverse=True)[:5]}")

    # 可视化
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Z-score
    ax1 = axes[0]
    ax1.hist(data, bins=50, alpha=0.7, color='steelblue', edgecolor='black')
    ax1.axvline(mean + 3*std, color='red', linestyle='--', linewidth=2, label=f'+3σ = {mean+3*std:.2f}')
    ax1.axvline(mean - 3*std, color='red', linestyle='--', linewidth=2, label=f'-3σ = {mean-3*std:.2f}')
    ax1.scatter(z_outliers, np.zeros_like(z_outliers) + 5, color='red', s=50, zorder=5, label='检测到的异常')
    ax1.set_xlabel('值', fontsize=12)
    ax1.set_ylabel('频数', fontsize=12)
    ax1.set_title('Z-score异常检测', fontsize=14)
    ax1.legend(loc='upper right')

    # IQR
    ax2 = axes[1]
    ax2.boxplot(data, vert=False)
    ax2.scatter(iqr_outliers, np.ones_like(iqr_outliers), color='red', s=50, zorder=5, label='检测到的异常')
    ax2.axvline(lower_bound, color='green', linestyle='--', linewidth=2, label=f'下界 = {lower_bound:.2f}')
    ax2.axvline(upper_bound, color='green', linestyle='--', linewidth=2, label=f'上界 = {upper_bound:.2f}')
    ax2.set_xlabel('值', fontsize=12)
    ax2.set_title('IQR异常检测 (箱线图)', fontsize=14)
    ax2.legend(loc='upper right')

    plt.tight_layout()
    plt.savefig('anomaly_statistical.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("\n统计方法图已保存为 anomaly_statistical.png\n")


def demo_lof():
    """局部离群因子 (LOF)"""
    print("=" * 60)
    print("2. 局部离群因子 (LOF)")
    print("=" * 60)

    # 生成包含不同密度簇的数据
    np.random.seed(42)

    # 两个不同密度的簇
    X1, _ = make_blobs(n_samples=200, centers=[[0, 0]], cluster_std=0.3, random_state=42)
    X2, _ = make_blobs(n_samples=100, centers=[[3, 3]], cluster_std=0.8, random_state=42)
    X = np.vstack([X1, X2])

    # 添加一些异常点
    outliers = np.array([[0, 3], [3, 0], [-2, 2], [5, 1], [1, -2]])
    X = np.vstack([X, outliers])

    # LOF检测
    lof = LocalOutlierFactor(n_neighbors=20, contamination=0.05)
    y_pred = lof.fit_predict(X)

    # 获取LOF分数（负值，越小越异常）
    lof_scores = -lof.negative_outlier_factor_

    print(f"数据点数: {len(X)}")
    print(f"检测到异常点: {np.sum(y_pred == -1)}个")

    # 可视化
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 预测结果
    ax1 = axes[0]
    normal = X[y_pred == 1]
    anomaly = X[y_pred == -1]
    ax1.scatter(normal[:, 0], normal[:, 1], c='blue', alpha=0.6, label='正常点')
    ax1.scatter(anomaly[:, 0], anomaly[:, 1], c='red', s=100, marker='x', linewidths=2, label='异常点')
    ax1.set_xlabel('特征1', fontsize=12)
    ax1.set_ylabel('特征2', fontsize=12)
    ax1.set_title('LOF异常检测结果', fontsize=14)
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)

    # LOF分数
    ax2 = axes[1]
    scatter = ax2.scatter(X[:, 0], X[:, 1], c=lof_scores, cmap='RdYlGn_r', s=30)
    ax2.scatter(anomaly[:, 0], anomaly[:, 1], c='red', s=100, marker='x', linewidths=2)
    plt.colorbar(scatter, ax=ax2, label='LOF分数')
    ax2.set_xlabel('特征1', fontsize=12)
    ax2.set_ylabel('特征2', fontsize=12)
    ax2.set_title('LOF分数分布 (红色=高异常)', fontsize=14)

    plt.tight_layout()
    plt.savefig('anomaly_lof.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("LOF检测图已保存为 anomaly_lof.png\n")

    print("LOF特点:")
    print("  - 考虑局部密度，能检测局部异常")
    print("  - 适合密度不均匀的数据")
    print("  - 计算复杂度O(n²)，不适合大数据\n")


def demo_isolation_forest():
    """孤立森林 (Isolation Forest)"""
    print("=" * 60)
    print("3. 孤立森林 (Isolation Forest)")
    print("=" * 60)

    # 生成数据
    np.random.seed(42)
    X, _ = make_blobs(n_samples=300, centers=[[0, 0], [5, 5]], cluster_std=0.6, random_state=42)

    # 添加异常点
    outliers = np.array([[10, 10], [-3, 5], [8, -2], [2, 8], [-2, -2]])
    X = np.vstack([X, outliers])

    # Isolation Forest
    iso_forest = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    y_pred = iso_forest.fit_predict(X)

    # 异常分数
    scores = iso_forest.score_samples(X)

    print(f"数据点数: {len(X)}")
    print(f"检测到异常点: {np.sum(y_pred == -1)}个")

    # 可视化
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 预测结果
    ax1 = axes[0]
    normal = X[y_pred == 1]
    anomaly = X[y_pred == -1]
    ax1.scatter(normal[:, 0], normal[:, 1], c='blue', alpha=0.6, label='正常点')
    ax1.scatter(anomaly[:, 0], anomaly[:, 1], c='red', s=100, marker='x', linewidths=2, label='异常点')
    ax1.set_xlabel('特征1', fontsize=12)
    ax1.set_ylabel('特征2', fontsize=12)
    ax1.set_title('Isolation Forest异常检测结果', fontsize=14)
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)

    # 异常分数分布
    ax2 = axes[1]
    ax2.hist(scores[y_pred == 1], bins=30, alpha=0.7, color='blue', label='正常点')
    ax2.hist(scores[y_pred == -1], bins=30, alpha=0.7, color='red', label='异常点')
    ax2.set_xlabel('异常分数', fontsize=12)
    ax2.set_ylabel('频数', fontsize=12)
    ax2.set_title('异常分数分布', fontsize=14)
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('anomaly_isolation_forest.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Isolation Forest检测图已保存为 anomaly_isolation_forest.png\n")

    print("Isolation Forest特点:")
    print("  - 计算效率高O(n)，适合大数据")
    print("  - 无需计算距离矩阵")
    print("  - 适合高维数据")
    print("  - 结果有一定随机性\n")


def demo_one_class_svm():
    """One-Class SVM"""
    print("=" * 60)
    print("4. One-Class SVM")
    print("=" * 60)

    # 生成数据
    np.random.seed(42)
    X, _ = make_blobs(n_samples=200, centers=[[0, 0]], cluster_std=0.5, random_state=42)

    # 添加异常点
    outliers = np.array([[3, 3], [-3, 3], [3, -3], [-3, -3], [0, 4]])
    X = np.vstack([X, outliers])

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # One-Class SVM
    ocsvm = OneClassSVM(kernel='rbf', gamma='scale', nu=0.05)
    y_pred = ocsvm.fit_predict(X_scaled)

    print(f"数据点数: {len(X)}")
    print(f"检测到异常点: {np.sum(y_pred == -1)}个")

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 8))

    # 创建决策边界网格
    xx, yy = np.meshgrid(np.linspace(-4, 4, 100), np.linspace(-4, 4, 100))
    Z = ocsvm.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # 绘制决策边界
    ax.contourf(xx, yy, Z, levels=np.linspace(Z.min(), 0, 7), cmap=plt.cm.Blues_r)
    ax.contour(xx, yy, Z, levels=[0], linewidths=2, colors='red', linestyles='--')

    # 绘制数据点
    normal = X_scaled[y_pred == 1]
    anomaly = X_scaled[y_pred == -1]
    ax.scatter(normal[:, 0], normal[:, 1], c='blue', alpha=0.6, label='正常点')
    ax.scatter(anomaly[:, 0], anomaly[:, 1], c='red', s=100, marker='x', linewidths=2, label='异常点')

    ax.set_xlabel('特征1 (标准化)', fontsize=12)
    ax.set_ylabel('特征2 (标准化)', fontsize=12)
    ax.set_title('One-Class SVM异常检测 (决策边界)', fontsize=14)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('anomaly_ocsvm.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("One-Class SVM检测图已保存为 anomaly_ocsvm.png\n")

    print("One-Class SVM特点:")
    print("  - 学习正常数据的边界")
    print("  - 核函数可处理非线性边界")
    print("  - nu参数控制异常比例")
    print("  - 计算复杂度较高\n")


def demo_methods_comparison():
    """方法对比"""
    print("=" * 60)
    print("5. 异常检测方法对比")
    print("=" * 60)

    # 生成不同类型的数据
    np.random.seed(42)

    # 1. 球形簇
    X1, _ = make_blobs(n_samples=200, centers=[[0, 0]], cluster_std=0.5, random_state=42)

    # 2. 环形数据
    X2, _ = make_circles(n_samples=200, noise=0.05, factor=0.5, random_state=42)

    datasets = [
        ('球形簇', X1),
        ('环形数据', X2)
    ]

    # 添加异常点
    for name, X in datasets:
        outliers = np.random.uniform(low=-3, high=3, size=(10, 2))
        X = np.vstack([X, outliers])

    methods = {
        'LOF': LocalOutlierFactor(n_neighbors=20, contamination=0.05),
        'Isolation Forest': IsolationForest(n_estimators=100, contamination=0.05, random_state=42),
        'One-Class SVM': OneClassSVM(kernel='rbf', gamma='scale', nu=0.05)
    }

    fig, axes = plt.subplots(2, 4, figsize=(16, 8))

    for row, (data_name, X) in enumerate(datasets):
        # 标准化
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # 原始数据
        ax = axes[row, 0]
        ax.scatter(X_scaled[:-10, 0], X_scaled[:-10, 1], c='blue', alpha=0.6, s=20)
        ax.scatter(X_scaled[-10:, 0], X_scaled[-10:, 1], c='red', s=50, marker='x', linewidths=2)
        ax.set_title(f'{data_name} - 原始数据', fontsize=11)
        ax.set_xlabel('特征1')
        ax.set_ylabel('特征2')
        ax.grid(True, alpha=0.3)

        # 各种方法
        for col, (method_name, method) in enumerate(methods.items(), 1):
            ax = axes[row, col]

            if method_name == 'LOF':
                y_pred = method.fit_predict(X_scaled)
            else:
                y_pred = method.fit_predict(X_scaled)

            normal = X_scaled[y_pred == 1]
            anomaly = X_scaled[y_pred == -1]

            ax.scatter(normal[:, 0], normal[:, 1], c='blue', alpha=0.6, s=20)
            ax.scatter(anomaly[:, 0], anomaly[:, 1], c='red', s=50, marker='x', linewidths=2)

            n_detected = len(anomaly)
            ax.set_title(f'{method_name}\n检测到{n_detected}个异常', fontsize=11)
            ax.set_xlabel('特征1')
            ax.grid(True, alpha=0.3)

    plt.suptitle('异常检测方法对比', fontsize=14)
    plt.tight_layout()
    plt.savefig('anomaly_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("方法对比图已保存为 anomaly_comparison.png\n")


def demo_fraud_detection():
    """实战案例：信用卡欺诈检测"""
    print("=" * 60)
    print("6. 实战案例：异常检测模拟")
    print("=" * 60)

    # 模拟信用卡交易数据
    np.random.seed(42)
    n_normal = 1000
    n_fraud = 50

    # 正常交易
    normal_transactions = np.random.multivariate_normal(
        mean=[0, 0, 0, 0],
        cov=[[1, 0.5, 0.3, 0.1],
             [0.5, 1, 0.2, 0.2],
             [0.3, 0.2, 1, 0.4],
             [0.1, 0.2, 0.4, 1]],
        size=n_normal
    )

    # 欺诈交易（不同的分布）
    fraud_transactions = np.random.multivariate_normal(
        mean=[3, 3, -2, 2],
        cov=[[1, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 0, 1, 0],
             [0, 0, 0, 1]],
        size=n_fraud
    )

    X = np.vstack([normal_transactions, fraud_transactions])
    y_true = np.array([0] * n_normal + [1] * n_fraud)

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print(f"总交易数: {len(X)}")
    print(f"正常交易: {n_normal}, 欺诈交易: {n_fraud}")
    print(f"欺诈比例: {n_fraud/len(X)*100:.1f}%")

    # 使用Isolation Forest检测
    iso_forest = IsolationForest(n_estimators=100, contamination=n_fraud/len(X), random_state=42)
    y_pred = iso_forest.fit_predict(X_scaled)
    y_pred = (y_pred == -1).astype(int)  # 转换为0/1

    # 评估
    print(f"\n检测结果:")
    print("-" * 40)
    print(classification_report(y_true, y_pred, target_names=['正常', '欺诈']))

    # 使用PCA可视化
    pca = PCA(n_components=2)
    X_2d = pca.fit_transform(X_scaled)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 真实标签
    ax1 = axes[0]
    ax1.scatter(X_2d[y_true==0, 0], X_2d[y_true==0, 1], c='blue', alpha=0.5, s=20, label='正常')
    ax1.scatter(X_2d[y_true==1, 0], X_2d[y_true==1, 1], c='red', s=50, marker='x', linewidths=2, label='欺诈')
    ax1.set_xlabel('PC1', fontsize=12)
    ax1.set_ylabel('PC2', fontsize=12)
    ax1.set_title('真实标签', fontsize=14)
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)

    # 预测标签
    ax2 = axes[1]
    ax2.scatter(X_2d[y_pred==0, 0], X_2d[y_pred==0, 1], c='blue', alpha=0.5, s=20, label='预测正常')
    ax2.scatter(X_2d[y_pred==1, 0], X_2d[y_pred==1, 1], c='red', s=50, marker='x', linewidths=2, label='预测欺诈')
    ax2.set_xlabel('PC1', fontsize=12)
    ax2.set_ylabel('PC2', fontsize=12)
    ax2.set_title('Isolation Forest预测', fontsize=14)
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)

    plt.suptitle('信用卡欺诈检测 (PCA可视化)', fontsize=14)
    plt.tight_layout()
    plt.savefig('anomaly_fraud_detection.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("欺诈检测图已保存为 anomaly_fraud_detection.png\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("异常检测 (Anomaly Detection) 完整示例")
    print("=" * 60 + "\n")

    # 运行所有示例
    demo_statistical_methods()
    demo_lof()
    demo_isolation_forest()
    demo_one_class_svm()
    demo_methods_comparison()
    demo_fraud_detection()

    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
