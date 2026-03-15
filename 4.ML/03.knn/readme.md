# K近邻算法 (K-Nearest Neighbors, KNN)

## 1. 算法简介

K近邻算法是一种基本的分类与回归方法，是最简单、最直观的机器学习算法之一。

### 核心思想
- **物以类聚**：相似的样本具有相似的标签
- 对于新样本，在训练集中找到距离最近的K个邻居
- 分类任务：采用**多数投票**决定类别
- 回归任务：采用**平均值**作为预测结果

## 2. 算法原理

### 2.1 距离度量

常用的距离度量方法：

1. **欧氏距离 (Euclidean Distance)**
   ```
   d(x, y) = √(Σ(xi - yi)²)
   ```

2. **曼哈顿距离 (Manhattan Distance)**
   ```
   d(x, y) = Σ|xi - yi|
   ```

3. **闵可夫斯基距离 (Minkowski Distance)**
   ```
   d(x, y) = (Σ|xi - yi|^p)^(1/p)
   ```
   - p=1 时为曼哈顿距离
   - p=2 时为欧氏距离

4. **余弦相似度 (Cosine Similarity)**
   ```
   cos(θ) = (x·y) / (||x|| × ||y||)
   ```

### 2.2 K值选择

| K值 | 影响 |
|-----|------|
| K较小 | 模型复杂，容易过拟合，对噪声敏感 |
| K较大 | 模型简单，容易欠拟合，决策边界更平滑 |

**选择方法**：
- 交叉验证选择最优K值
- 通常取奇数（二分类问题避免平票）
- 经验法则：K ≤ √n（n为样本数）

### 2.3 算法流程

```
输入: 训练集 D, 测试样本 x, 邻居数 K
输出: 预测类别

1. 计算 x 与训练集中每个样本的距离
2. 按距离升序排序
3. 选取前 K 个最近的样本
4. 统计这 K 个样本的类别
5. 返回出现次数最多的类别（分类）或平均值（回归）
```

## 3. 算法优缺点

### 优点
- 简单直观，易于理解和实现
- 无需训练过程（懒惰学习）
- 对数据分布无假设
- 可用于分类和回归
- 对异常值不敏感（K较大时）

### 缺点
- 计算复杂度高，预测速度慢
- 存储所有训练数据，内存消耗大
- 高维数据表现差（维度灾难）
- 对不相关特征敏感
- 样本不平衡时效果差

## 4. 优化方法

### 4.1 距离加权
- 给近邻赋予更大的权重
- 常用权重：w = 1/d²

### 4.2 KD树 (KD-Tree)
- 加速近邻搜索
- 适用于低维数据
- 构建复杂度：O(n log n)

### 4.3 球树 (Ball Tree)
- 适用于高维数据
- 在某些情况下比KD树更高效

## 5. Scikit-learn 实现

### 分类
```python
from sklearn.neighbors import KNeighborsClassifier

# 创建模型
knn = KNeighborsClassifier(
    n_neighbors=5,      # 邻居数
    weights='uniform',  # 权重: 'uniform' 或 'distance'
    algorithm='auto',   # 算法: 'auto', 'ball_tree', 'kd_tree', 'brute'
    metric='minkowski', # 距离度量
    p=2                 # 闵可夫斯基距离的p值
)

# 训练（实际上是存储数据）
knn.fit(X_train, y_train)

# 预测
y_pred = knn.predict(X_test)
```

### 回归
```python
from sklearn.neighbors import KNeighborsRegressor

knn_reg = KNeighborsRegressor(n_neighbors=5)
knn_reg.fit(X_train, y_train)
y_pred = knn_reg.predict(X_test)
```

## 6. 参数说明

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| n_neighbors | 邻居数量 | 3-10，交叉验证选择 |
| weights | 权重函数 | 'distance'通常更好 |
| algorithm | 搜索算法 | 'auto'自动选择 |
| metric | 距离度量 | 'minkowski' (p=2) |
| leaf_size | 叶节点大小 | 30 (默认) |

## 7. 适用场景

- **推荐场景**：
  - 小到中等规模数据集
  - 低维数据
  - 多分类问题
  - 推荐系统（协同过滤）

- **不推荐场景**：
  - 大规模数据集
  - 高维数据
  - 实时预测系统

## 8. 示例代码

见 `demo.py` 文件，包含：
- 基础KNN分类示例
- K值对决策边界的影响
- 不同距离度量的比较
- KNN回归示例
- 使用KD树加速

## 9. 与其他算法对比

| 特性 | KNN | 决策树 | SVM |
|------|-----|--------|-----|
| 训练速度 | 极快 | 快 | 慢 |
| 预测速度 | 慢 | 快 | 中等 |
| 可解释性 | 中等 | 高 | 低 |
| 处理高维 | 差 | 好 | 好 |
| 处理噪声 | 中等 | 差 | 好 |

## 10. 参考资料

- Cover, T., & Hart, P. (1967). Nearest neighbor pattern classification
- scikit-learn KNN文档: https://scikit-learn.org/stable/modules/neighbors.html
