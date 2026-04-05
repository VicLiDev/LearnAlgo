# 降维算法 (Dimensionality Reduction)

## 1. 算法简介

降维是将高维数据映射到低维空间的技术，同时尽可能保留原始数据的重要信息。

### 为什么需要降维？
- **维度灾难**：高维数据稀疏，需要更多样本
- **计算效率**：减少存储和计算开销
- **可视化**：将数据投影到2D/3D便于可视化
- **去噪**：去除噪声和不相关特征
- **避免过拟合**：减少特征数量

## 2. 主要降维方法

### 2.1 线性方法

| 方法 | 特点                   | 适用场景 |
|------|------------------------|----------|
| PCA  | 无监督，保留方差       | 通用降维 |
| LDA  | 有监督，最大化类间距离 | 分类任务 |
| ICA  | 独立成分分析           | 信号分离 |

### 2.2 非线性方法

| 方法       | 特点                   | 适用场景     |
|------------|------------------------|--------------|
| t-SNE      | 保持局部结构           | 可视化       |
| UMAP       | 保持全局和局部结构     | 可视化、聚类 |
| Kernel PCA | 核技巧处理非线性       | 非线性数据   |

## 3. 主成分分析 (PCA)

### 3.1 原理

PCA通过正交变换将原始特征空间投影到新的正交特征空间（主成分），主成分按照方差大小排序。

**算法步骤**：
1. 数据标准化（均值为0）
2. 计算协方差矩阵
3. 计算协方差矩阵的特征值和特征向量
4. 按特征值降序排列
5. 选择前k个特征向量作为主成分
6. 投影数据到新空间

### 3.2 数学表达

协方差矩阵：
```
C = (1/n) X^T X
```

特征分解：
```
C v = λ v
```

降维后：
```
X_reduced = X W_k
```
其中 W_k 是前k个特征向量组成的矩阵。

### 3.3 方差解释比

```
解释方差比 = λ_i / Σλ_j
```

通常选择保留95%以上方差的主成分数量。

### 3.4 Scikit-learn实现

```python
from sklearn.decomposition import PCA

# 创建PCA对象
pca = PCA(n_components=0.95)  # 保留95%方差

# 拟合并转换
X_pca = pca.fit_transform(X)

# 查看解释方差比
print(pca.explained_variance_ratio_)
```

## 4. 线性判别分析 (LDA)

### 4.1 原理

LDA是一种**有监督**降维方法，目标是找到投影方向使得：
- 类内距离最小（类内散度最小）
- 类间距离最大（类间散度最大）

### 4.2 数学表达

目标函数（Fisher准则）：
```
J(w) = (w^T S_B w) / (w^T S_W w)
```

其中：
- S_B：类间散度矩阵
- S_W：类内散度矩阵

### 4.3 与PCA的区别

| 特性       | PCA        | LDA               |
|------------|------------|-------------------|
| 类型       | 无监督     | 有监督            |
| 目标       | 最大化方差 | 最大化类间/类内比 |
| 最大维度   | n_features | n_classes - 1     |
| 适用场景   | 通用降维   | 分类任务          |

### 4.4 Scikit-learn实现

```python
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

lda = LinearDiscriminantAnalysis(n_components=2)
X_lda = lda.fit_transform(X, y)  # 需要标签y
```

## 5. t-SNE

### 5.1 原理

t-SNE（t-Distributed Stochastic Neighbor Embedding）是一种非线性降维方法，特别适合高维数据可视化。

**核心思想**：
- 在高维空间中，将距离转换为概率（相似度）
- 在低维空间中，保持相似的概率分布
- 使用t分布减少拥挤问题

### 5.2 关键参数

| 参数          | 说明                          | 推荐值  |
|---------------|-------------------------------|---------|
| perplexity    | 困惑度，影响局部/全局结构平衡 | 5-50    |
| n_iter        | 迭代次数                      | 1000+   |
| learning_rate | 学习率                        | 10-1000 |

### 5.3 Scikit-learn实现

```python
from sklearn.manifold import TSNE

tsne = TSNE(
    n_components=2,
    perplexity=30,
    n_iter=1000,
    random_state=42
)
X_tsne = tsne.fit_transform(X)
```

### 5.4 注意事项
- t-SNE不保留距离信息，不适合作为预处理
- 不同运行可能产生不同结果
- 主要用于可视化，不用于特征提取

## 6. UMAP

### 6.1 原理

UMAP（Uniform Manifold Approximation and Projection）是一种较新的降维方法，比t-SNE更快且能更好地保留全局结构。

### 6.2 关键参数

| 参数        | 说明             | 推荐值      |
|-------------|------------------|-------------|
| n_neighbors | 局部邻域大小     | 5-50        |
| min_dist    | 嵌入空间最小距离 | 0.0-0.99    |
| metric      | 距离度量         | 'euclidean' |

### 6.3 Scikit-learn实现

```python
from umap import UMAP  # 需要安装umap-learn

umap = UMAP(n_components=2, n_neighbors=15, min_dist=0.1)
X_umap = umap.fit_transform(X)
```

## 7. 核PCA (Kernel PCA)

### 7.1 原理

使用核技巧将PCA扩展到非线性情况，先将数据映射到高维特征空间，再进行PCA。

### 7.2 常用核函数

- RBF核：`exp(-γ||x-y||²)`
- 多项式核：`(x·y + c)^d`
- Sigmoid核：`tanh(αx·y + c)`

### 7.3 Scikit-learn实现

```python
from sklearn.decomposition import KernelPCA

kpca = KernelPCA(
    n_components=2,
    kernel='rbf',
    gamma=0.1
)
X_kpca = kpca.fit_transform(X)
```

## 8. 方法选择指南

| 需求         | 推荐方法          |
|--------------|-------------------|
| 通用降维     | PCA               |
| 分类任务降维 | LDA               |
| 数据可视化   | t-SNE, UMAP       |
| 非线性数据   | Kernel PCA, UMAP  |
| 大规模数据   | PCA, UMAP         |
| 保留可解释性 | PCA, LDA          |

## 9. 示例代码

见 `demo.py` 文件，包含：
- PCA降维与方差解释
- LDA有监督降维
- t-SNE可视化
- Kernel PCA非线性降维
- 方法对比

## 10. 参考资料

- Jolliffe, I. T. (2002). Principal Component Analysis
- van der Maaten, L., & Hinton, G. (2008). Visualizing Data using t-SNE
- McInnes, L., et al. (2018). UMAP: Uniform Manifold Approximation and Projection
- scikit-learn降维文档: https://scikit-learn.org/stable/modules/decomposition.html
