"""
聚类算法示例
演示各种聚类算法的使用方法
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs, make_moons, make_circles
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering, SpectralClustering
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def generate_datasets():
    """生成不同的数据集"""
    # 1. 球形簇
    blobs_X, blobs_y = make_blobs(n_samples=500, centers=4,
                                   cluster_std=0.8, random_state=42)

    # 2. 月牙形
    moons_X, moons_y = make_moons(n_samples=500, noise=0.05, random_state=42)

    # 3. 圆环形
    circles_X, circles_y = make_circles(n_samples=500, factor=0.5,
                                         noise=0.05, random_state=42)

    datasets = {
        '球形簇': (blobs_X, blobs_y),
        '月牙形': (moons_X, moons_y),
        '圆环形': (circles_X, circles_y)
    }

    return datasets


def plot_clusters(X, labels, title, centers=None, filename=None, ax=None):
    """绘制聚类结果"""
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))

    # 绘制数据点
    unique_labels = set(labels)
    colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_labels)))

    for label, color in zip(unique_labels, colors):
        if label == -1:  # 噪声点
            color = 'gray'
            marker = 'x'
            alpha = 0.3
        else:
            marker = 'o'
            alpha = 0.6

        mask = labels == label
        ax.scatter(X[mask, 0], X[mask, 1],
                   c=[color], marker=marker, alpha=alpha, s=30)

    # 绘制质心
    if centers is not None:
        ax.scatter(centers[:, 0], centers[:, 1],
                   c='black', marker='*', s=200, edgecolors='white')

    ax.set_title(title)
    ax.set_xlabel('特征1')
    ax.set_ylabel('特征2')
    ax.grid(True, alpha=0.3)

    if filename:
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"图表已保存: {filename}")


def evaluate_clustering(X, labels, model_name):
    """评估聚类结果"""
    # 过滤噪声点
    valid_mask = labels != -1
    if len(set(labels[valid_mask])) < 2:
        print(f"\n{model_name}: 簇数不足，无法计算评估指标")
        return

    sil = silhouette_score(X[valid_mask], labels[valid_mask])
    ch = calinski_harabasz_score(X[valid_mask], labels[valid_mask])
    db = davies_bouldin_score(X[valid_mask], labels[valid_mask])

    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)

    print(f"\n{model_name} 评估指标:")
    print(f"  簇数量: {n_clusters}")
    print(f"  噪声点: {n_noise}")
    print(f"  轮廓系数: {sil:.4f} (越大越好)")
    print(f"  CH指数: {ch:.4f} (越大越好)")
    print(f"  DB指数: {db:.4f} (越小越好)")


def demo_kmeans():
    """K-Means聚类示例"""
    print("=" * 60)
    print("1. K-Means 聚类示例")
    print("=" * 60)

    datasets = generate_datasets()

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    for idx, (name, (X, y)) in enumerate(datasets.items()):
        # 标准化
        X_scaled = StandardScaler().fit_transform(X)

        # K-Means聚类
        n_clusters = 2 if name != '球形簇' else 4
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)

        # 评估
        evaluate_clustering(X_scaled, labels, f"K-Means - {name}")

        # 可视化
        plot_clusters(X_scaled, labels, f'K-Means - {name}',
                      centers=kmeans.cluster_centers_, ax=axes[idx])

    plt.tight_layout()
    plt.savefig('kmeans_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: kmeans_comparison.png")


def demo_dbscan():
    """DBSCAN聚类示例"""
    print("\n" + "=" * 60)
    print("2. DBSCAN 聚类示例")
    print("=" * 60)

    datasets = generate_datasets()

    # 不同数据集使用不同参数
    params = {
        '球形簇': {'eps': 0.5, 'min_samples': 5},
        '月牙形': {'eps': 0.2, 'min_samples': 5},
        '圆环形': {'eps': 0.2, 'min_samples': 5}
    }

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    for idx, (name, (X, y)) in enumerate(datasets.items()):
        # 标准化
        X_scaled = StandardScaler().fit_transform(X)

        # DBSCAN聚类
        dbscan = DBSCAN(**params[name])
        labels = dbscan.fit_predict(X_scaled)

        # 评估
        evaluate_clustering(X_scaled, labels, f"DBSCAN - {name}")

        # 可视化
        plot_clusters(X_scaled, labels, f"DBSCAN - {name} (eps={params[name]['eps']})",
                      ax=axes[idx])

    plt.tight_layout()
    plt.savefig('dbscan_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: dbscan_comparison.png")


def demo_hierarchical():
    """层次聚类示例"""
    print("\n" + "=" * 60)
    print("3. 层次聚类示例")
    print("=" * 60)

    datasets = generate_datasets()

    # 不同的链接方式
    linkages = ['ward', 'complete', 'average']

    # 使用球形簇数据演示
    X, y = datasets['球形簇']
    X_scaled = StandardScaler().fit_transform(X)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    for idx, linkage in enumerate(linkages):
        # 层次聚类
        n_clusters = 4
        hc = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
        labels = hc.fit_predict(X_scaled)

        # 评估
        evaluate_clustering(X_scaled, labels, f"层次聚类 - {linkage}")

        # 可视化
        plot_clusters(X_scaled, labels, f'层次聚类 - {linkage}', ax=axes[idx])

    plt.tight_layout()
    plt.savefig('hierarchical_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: hierarchical_comparison.png")


def demo_gmm():
    """高斯混合模型示例"""
    print("\n" + "=" * 60)
    print("4. 高斯混合模型 (GMM) 示例")
    print("=" * 60)

    datasets = generate_datasets()

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    for idx, (name, (X, y)) in enumerate(datasets.items()):
        # 标准化
        X_scaled = StandardScaler().fit_transform(X)

        # GMM聚类
        n_components = 2 if name != '球形簇' else 4
        gmm = GaussianMixture(n_components=n_components, random_state=42)
        labels = gmm.fit_predict(X_scaled)

        # 评估
        evaluate_clustering(X_scaled, labels, f"GMM - {name}")

        # 可视化
        plot_clusters(X_scaled, labels, f'GMM - {name}',
                      centers=gmm.means_, ax=axes[idx])

    plt.tight_layout()
    plt.savefig('gmm_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: gmm_comparison.png")


def demo_spectral():
    """谱聚类示例"""
    print("\n" + "=" * 60)
    print("5. 谱聚类示例")
    print("=" * 60)

    datasets = generate_datasets()

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    for idx, (name, (X, y)) in enumerate(datasets.items()):
        # 标准化
        X_scaled = StandardScaler().fit_transform(X)

        # 谱聚类
        n_clusters = 2 if name != '球形簇' else 4
        spectral = SpectralClustering(n_clusters=n_clusters,
                                       affinity='nearest_neighbors',
                                       random_state=42)
        labels = spectral.fit_predict(X_scaled)

        # 评估
        evaluate_clustering(X_scaled, labels, f"谱聚类 - {name}")

        # 可视化
        plot_clusters(X_scaled, labels, f'谱聚类 - {name}', ax=axes[idx])

    plt.tight_layout()
    plt.savefig('spectral_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: spectral_comparison.png")


def demo_kmeans_k_selection():
    """K-Means K值选择示例"""
    print("\n" + "=" * 60)
    print("6. K-Means K值选择示例 (肘部法则)")
    print("=" * 60)

    # 生成数据
    X, y = make_blobs(n_samples=500, centers=4, cluster_std=0.8, random_state=42)
    X_scaled = StandardScaler().fit_transform(X)

    # 测试不同的K值
    K_range = range(2, 11)
    sse = []
    silhouette_scores = []

    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)

        sse.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))

        print(f"K={k}: SSE={kmeans.inertia_:.2f}, 轮廓系数={silhouette_scores[-1]:.4f}")

    # 绘制肘部图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(K_range, sse, 'bo-', linewidth=2, markersize=8)
    ax1.set_xlabel('簇数量 K')
    ax1.set_ylabel('SSE (误差平方和)')
    ax1.set_title('肘部法则')
    ax1.grid(True, alpha=0.3)

    ax2.plot(K_range, silhouette_scores, 'ro-', linewidth=2, markersize=8)
    ax2.set_xlabel('簇数量 K')
    ax2.set_ylabel('轮廓系数')
    ax2.set_title('轮廓系数法')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('k_selection.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: k_selection.png")


def demo_all_algorithms_comparison():
    """所有算法对比"""
    print("\n" + "=" * 60)
    print("7. 所有聚类算法对比")
    print("=" * 60)

    # 使用月牙形数据
    X, y = make_moons(n_samples=500, noise=0.05, random_state=42)
    X_scaled = StandardScaler().fit_transform(X)

    algorithms = {
        'K-Means': KMeans(n_clusters=2, random_state=42, n_init=10),
        'DBSCAN': DBSCAN(eps=0.2, min_samples=5),
        '层次聚类': AgglomerativeClustering(n_clusters=2, linkage='ward'),
        'GMM': GaussianMixture(n_components=2, random_state=42),
        '谱聚类': SpectralClustering(n_clusters=2, affinity='nearest_neighbors', random_state=42)
    }

    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.ravel()

    # 原始数据
    axes[0].scatter(X_scaled[:, 0], X_scaled[:, 1], c=y, cmap='rainbow', alpha=0.6, s=30)
    axes[0].set_title('原始数据 (真实标签)')
    axes[0].grid(True, alpha=0.3)

    # 各算法结果
    for idx, (name, algorithm) in enumerate(algorithms.items(), 1):
        if hasattr(algorithm, 'fit_predict'):
            labels = algorithm.fit_predict(X_scaled)
        else:
            labels = algorithm.fit(X_scaled).predict(X_scaled)

        evaluate_clustering(X_scaled, labels, name)
        plot_clusters(X_scaled, labels, name, ax=axes[idx])

    plt.tight_layout()
    plt.savefig('all_algorithms_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: all_algorithms_comparison.png")


def main():
    """主函数"""
    print("聚类算法演示程序")
    print("=" * 60)

    # 运行所有示例
    demo_kmeans()
    demo_dbscan()
    demo_hierarchical()
    demo_gmm()
    demo_spectral()
    demo_kmeans_k_selection()
    demo_all_algorithms_comparison()

    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
