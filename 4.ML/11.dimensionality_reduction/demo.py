"""
降维算法 (Dimensionality Reduction) 示例代码

包含内容:
1. PCA降维与方差解释
2. PCA人脸特征提取
3. LDA有监督降维
4. t-SNE可视化
5. Kernel PCA非线性降维
6. 方法对比
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris, load_digits, load_wine, make_swiss_roll, make_circles
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, KernelPCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.manifold import TSNE
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def demo_pca_basic():
    """PCA基础示例"""
    print("=" * 60)
    print("1. PCA降维与方差解释")
    print("=" * 60)

    # 加载葡萄酒数据集
    wine = load_wine()
    X, y = wine.data, wine.target
    feature_names = wine.feature_names

    print(f"原始数据维度: {X.shape}")

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # PCA保留所有成分
    pca = PCA()
    X_pca = pca.fit_transform(X_scaled)

    # 计算累计方差解释比
    cumsum = np.cumsum(pca.explained_variance_ratio_)

    # 可视化
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # 1. 方差解释比
    ax1 = axes[0]
    n_components = len(pca.explained_variance_ratio_)
    ax1.bar(range(1, n_components + 1), pca.explained_variance_ratio_,
           alpha=0.7, label='单个主成分')
    ax1.plot(range(1, n_components + 1), cumsum, 'ro-', label='累计方差')
    ax1.axhline(y=0.95, color='k', linestyle='--', label='95%阈值')
    ax1.set_xlabel('主成分', fontsize=12)
    ax1.set_ylabel('方差解释比', fontsize=12)
    ax1.set_title('PCA方差解释比', fontsize=14)
    ax1.legend(loc='center right')
    ax1.set_xticks(range(1, n_components + 1))
    ax1.grid(True, alpha=0.3)

    # 找到保留95%方差需要的主成分数
    n_95 = np.argmax(cumsum >= 0.95) + 1
    print(f"保留95%方差需要 {n_95} 个主成分")

    # 2. 降维到2D可视化
    ax2 = axes[1]
    pca_2d = PCA(n_components=2)
    X_pca_2d = pca_2d.fit_transform(X_scaled)

    for i, target_name in enumerate(wine.target_names):
        ax2.scatter(X_pca_2d[y == i, 0], X_pca_2d[y == i, 1],
                   label=target_name, alpha=0.7, s=50)

    ax2.set_xlabel(f'PC1 ({pca_2d.explained_variance_ratio_[0]*100:.1f}%)', fontsize=12)
    ax2.set_ylabel(f'PC2 ({pca_2d.explained_variance_ratio_[1]*100:.1f}%)', fontsize=12)
    ax2.set_title('PCA降维到2D', fontsize=14)
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)

    # 3. 主成分载荷热力图
    ax3 = axes[2]
    # 只显示前两个主成分的载荷
    loadings = pca_2d.components_.T[:, :2]
    im = ax3.imshow(loadings, cmap='coolwarm', aspect='auto')
    ax3.set_xticks([0, 1])
    ax3.set_xticklabels(['PC1', 'PC2'])
    ax3.set_yticks(range(len(feature_names)))
    ax3.set_yticklabels(feature_names, fontsize=8)
    ax3.set_title('主成分载荷', fontsize=14)
    plt.colorbar(im, ax=ax3)

    plt.tight_layout()
    plt.savefig('pca_basic.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("PCA基础图已保存为 pca_basic.png\n")


def demo_pca_digits():
    """PCA手写数字降维"""
    print("=" * 60)
    print("2. PCA手写数字降维")
    print("=" * 60)

    # 加载手写数字数据集
    digits = load_digits()
    X, y = digits.data, digits.target

    print(f"原始图像维度: {X.shape[1]} (8x8像素)")

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # PCA保留95%方差
    pca = PCA(n_components=0.95)
    X_pca = pca.fit_transform(X_scaled)

    print(f"降维后维度: {X_pca.shape[1]}")
    print(f"压缩比: {X.shape[1] / X_pca.shape[1]:.2f}x")

    # 可视化
    fig, axes = plt.subplots(2, 5, figsize=(12, 6))

    # 原始图像 vs 重构图像
    for i in range(5):
        # 原始
        ax = axes[0, i]
        ax.imshow(X[i].reshape(8, 8), cmap='gray')
        ax.set_title(f'原始: {y[i]}')
        ax.axis('off')

        # 重构
        ax = axes[1, i]
        X_reconstructed = pca.inverse_transform(X_pca[i:i+1])
        X_reconstructed = scaler.inverse_transform(X_reconstructed)
        ax.imshow(X_reconstructed.reshape(8, 8), cmap='gray')
        ax.set_title(f'重构: {y[i]}')
        ax.axis('off')

    axes[0, 0].set_ylabel('原始图像', fontsize=12)
    axes[1, 0].set_ylabel(f'PCA重构\n({X_pca.shape[1]}成分)', fontsize=12)

    plt.suptitle('PCA降维与重构', fontsize=14)
    plt.tight_layout()
    plt.savefig('pca_digits.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("PCA手写数字图已保存为 pca_digits.png\n")


def demo_lda():
    """LDA有监督降维"""
    print("=" * 60)
    print("3. LDA有监督降维")
    print("=" * 60)

    # 加载葡萄酒数据集
    wine = load_wine()
    X, y = wine.data, wine.target

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # PCA vs LDA 对比
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # 1. PCA 2D
    ax1 = axes[0]
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    for i in range(3):
        ax1.scatter(X_pca[y == i, 0], X_pca[y == i, 1], label=f'类别 {i}', alpha=0.7, s=50)
    ax1.set_xlabel('PC1', fontsize=12)
    ax1.set_ylabel('PC2', fontsize=12)
    ax1.set_title('PCA (无监督)', fontsize=14)
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)

    # 2. LDA 2D
    ax2 = axes[1]
    lda = LinearDiscriminantAnalysis(n_components=2)
    X_lda = lda.fit_transform(X_scaled, y)

    for i in range(3):
        ax2.scatter(X_lda[y == i, 0], X_lda[y == i, 1], label=f'类别 {i}', alpha=0.7, s=50)
    ax2.set_xlabel('LD1', fontsize=12)
    ax2.set_ylabel('LD2', fontsize=12)
    ax2.set_title('LDA (有监督)', fontsize=14)
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)

    # 3. 分类性能对比
    ax3 = axes[2]

    # 划分数据
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

    # 原始数据分类
    clf_original = LogisticRegression(max_iter=1000, random_state=42)
    clf_original.fit(X_train, y_train)
    acc_original = clf_original.score(X_test, y_test)

    # PCA降维后分类
    pca_full = PCA(n_components=2)
    X_train_pca = pca_full.fit_transform(X_train)
    X_test_pca = pca_full.transform(X_test)
    clf_pca = LogisticRegression(max_iter=1000, random_state=42)
    clf_pca.fit(X_train_pca, y_train)
    acc_pca = clf_pca.score(X_test_pca, y_test)

    # LDA降维后分类
    lda_full = LinearDiscriminantAnalysis(n_components=2)
    X_train_lda = lda_full.fit_transform(X_train, y_train)
    X_test_lda = lda_full.transform(X_test)
    clf_lda = LogisticRegression(max_iter=1000, random_state=42)
    clf_lda.fit(X_train_lda, y_train)
    acc_lda = clf_lda.score(X_test_lda, y_test)

    methods = ['原始数据\n(13维)', 'PCA\n(2维)', 'LDA\n(2维)']
    accuracies = [acc_original, acc_pca, acc_lda]
    colors = ['#3498db', '#e74c3c', '#2ecc71']

    bars = ax3.bar(methods, accuracies, color=colors, alpha=0.8)
    ax3.set_ylabel('分类准确率', fontsize=12)
    ax3.set_title('降维后分类性能对比', fontsize=14)
    ax3.set_ylim(0.8, 1.0)

    for bar, acc in zip(bars, accuracies):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{acc:.3f}', ha='center', va='bottom', fontsize=11)

    plt.tight_layout()
    plt.savefig('lda_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("LDA对比图已保存为 lda_comparison.png\n")

    print(f"原始数据分类准确率: {acc_original:.4f}")
    print(f"PCA(2维)分类准确率: {acc_pca:.4f}")
    print(f"LDA(2维)分类准确率: {acc_lda:.4f}")
    print("\n说明: LDA利用标签信息，通常在分类任务上效果更好\n")


def demo_tsne():
    """t-SNE可视化"""
    print("=" * 60)
    print("4. t-SNE可视化")
    print("=" * 60)

    # 加载手写数字数据集
    digits = load_digits()
    X, y = digits.data, digits.target

    print(f"数据维度: {X.shape}")

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 不同perplexity值对比
    perplexities = [5, 30, 50]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for idx, perp in enumerate(perplexities):
        ax = axes[idx]

        tsne = TSNE(n_components=2, perplexity=perp, random_state=42, max_iter=1000)
        X_tsne = tsne.fit_transform(X_scaled)

        scatter = ax.scatter(X_tsne[:, 0], X_tsne[:, 1], c=y, cmap='tab10',
                           alpha=0.7, s=20)
        ax.set_xlabel('t-SNE 1', fontsize=12)
        ax.set_ylabel('t-SNE 2', fontsize=12)
        ax.set_title(f't-SNE (perplexity={perp})', fontsize=14)
        ax.grid(True, alpha=0.3)

    # 添加颜色条
    plt.colorbar(scatter, ax=axes, label='数字类别', shrink=0.8)

    plt.suptitle('t-SNE不同perplexity参数对比', fontsize=14)
    plt.tight_layout()
    plt.savefig('tsne_visualization.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("t-SNE可视化图已保存为 tsne_visualization.png\n")

    print("t-SNE参数说明:")
    print("  - perplexity小: 更关注局部结构，可能分裂成多个小簇")
    print("  - perplexity大: 更关注全局结构，簇会更聚合")
    print("  - 典型值范围: 5-50\n")


def demo_kernel_pca():
    """Kernel PCA非线性降维"""
    print("=" * 60)
    print("5. Kernel PCA非线性降维")
    print("=" * 60)

    # 生成同心圆数据
    X, y = make_circles(n_samples=500, factor=0.3, noise=0.05, random_state=42)

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # 原始数据
    ax = axes[0, 0]
    ax.scatter(X[y == 0, 0], X[y == 0, 1], c='blue', label='类别0', alpha=0.6)
    ax.scatter(X[y == 1, 0], X[y == 1, 1], c='red', label='类别1', alpha=0.6)
    ax.set_xlabel('特征1', fontsize=12)
    ax.set_ylabel('特征2', fontsize=12)
    ax.set_title('原始数据', fontsize=14)
    ax.legend(loc='upper right')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

    # 线性PCA
    ax = axes[0, 1]
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    ax.scatter(X_pca[y == 0, 0], X_pca[y == 0, 1], c='blue', alpha=0.6)
    ax.scatter(X_pca[y == 1, 0], X_pca[y == 1, 1], c='red', alpha=0.6)
    ax.set_xlabel('PC1', fontsize=12)
    ax.set_ylabel('PC2', fontsize=12)
    ax.set_title('线性PCA', fontsize=14)
    ax.grid(True, alpha=0.3)

    # RBF核PCA
    ax = axes[0, 2]
    kpca_rbf = KernelPCA(n_components=2, kernel='rbf', gamma=10)
    X_kpca_rbf = kpca_rbf.fit_transform(X)
    ax.scatter(X_kpca_rbf[y == 0, 0], X_kpca_rbf[y == 0, 1], c='blue', alpha=0.6)
    ax.scatter(X_kpca_rbf[y == 1, 0], X_kpca_rbf[y == 1, 1], c='red', alpha=0.6)
    ax.set_xlabel('KPC1', fontsize=12)
    ax.set_ylabel('KPC2', fontsize=12)
    ax.set_title('RBF核PCA (gamma=10)', fontsize=14)
    ax.grid(True, alpha=0.3)

    # 不同gamma值的效果
    gammas = [1, 5, 20]
    for idx, gamma in enumerate(gammas):
        ax = axes[1, idx]

        kpca = KernelPCA(n_components=2, kernel='rbf', gamma=gamma)
        X_kpca = kpca.fit_transform(X)

        ax.scatter(X_kpca[y == 0, 0], X_kpca[y == 0, 1], c='blue', alpha=0.6)
        ax.scatter(X_kpca[y == 1, 0], X_kpca[y == 1, 1], c='red', alpha=0.6)
        ax.set_xlabel('KPC1', fontsize=12)
        ax.set_ylabel('KPC2', fontsize=12)
        ax.set_title(f'RBF核PCA (gamma={gamma})', fontsize=14)
        ax.grid(True, alpha=0.3)

    plt.suptitle('Kernel PCA: 线性 vs 非线性降维', fontsize=14)
    plt.tight_layout()
    plt.savefig('kernel_pca.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Kernel PCA对比图已保存为 kernel_pca.png\n")

    print("观察:")
    print("  - 线性PCA无法分离同心圆数据")
    print("  - RBF核PCA可以将数据映射到线性可分空间")
    print("  - gamma参数控制核函数的影响范围\n")


def demo_method_comparison():
    """降维方法综合对比"""
    print("=" * 60)
    print("6. 降维方法综合对比")
    print("=" * 60)

    # 加载鸢尾花数据集
    iris = load_iris()
    X, y = iris.data, iris.target
    target_names = iris.target_names

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 不同降维方法
    methods = {
        'PCA': PCA(n_components=2),
        'LDA': LinearDiscriminantAnalysis(n_components=2),
        't-SNE': TSNE(n_components=2, random_state=42, perplexity=30),
        'Kernel PCA (RBF)': KernelPCA(n_components=2, kernel='rbf', gamma=0.5)
    }

    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    axes = axes.flatten()

    for idx, (name, method) in enumerate(methods.items()):
        ax = axes[idx]

        if name == 'LDA':
            X_transformed = method.fit_transform(X_scaled, y)
        else:
            X_transformed = method.fit_transform(X_scaled)

        for i, target_name in enumerate(target_names):
            ax.scatter(X_transformed[y == i, 0], X_transformed[y == i, 1],
                      label=target_name, alpha=0.7, s=60, edgecolors='black')

        ax.set_xlabel('成分1', fontsize=12)
        ax.set_ylabel('成分2', fontsize=12)
        ax.set_title(name, fontsize=14)
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)

    plt.suptitle('降维方法综合对比 - 鸢尾花数据集', fontsize=14)
    plt.tight_layout()
    plt.savefig('dimensionality_reduction_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("降维方法对比图已保存为 dimensionality_reduction_comparison.png\n")

    print("各方法特点:")
    print("  - PCA: 无监督，保留最大方差，类别可能有重叠")
    print("  - LDA: 有监督，最大化类间分离，分类效果好")
    print("  - t-SNE: 非线性，保持局部结构，可视化效果好")
    print("  - Kernel PCA: 非线性，可处理复杂结构\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("降维算法 (Dimensionality Reduction) 完整示例")
    print("=" * 60 + "\n")

    # 运行所有示例
    demo_pca_basic()
    demo_pca_digits()
    demo_lda()
    demo_tsne()
    demo_kernel_pca()
    demo_method_comparison()

    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
