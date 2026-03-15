# 决策树算法 (Decision Tree)

## 概述

决策树是一种基本的分类与回归方法，它通过树形结构进行决策。从根节点开始，在每个内部节点根据特征进行判断，最终在叶节点得到预测结果。

## 基本概念

### 1. 节点类型
- **根节点 (Root)**: 树的起始点，包含所有样本
- **内部节点 (Internal Node)**: 进行特征判断的节点
- **叶节点 (Leaf Node)**: 最终的决策结果

### 2. 分裂准则

#### 信息增益 (Information Gain)
- 基于信息熵
- 用于ID3算法
```
Entropy(S) = -Σ pᵢ log₂(pᵢ)
Information Gain = Entropy(parent) - Σ(|Sᵥ|/|S|) × Entropy(Sᵥ)
```

#### 信息增益率 (Information Gain Ratio)
- 信息增益的改进
- 用于C4.5算法
- 解决偏向取值多的特征的问题

#### 基尼指数 (Gini Index)
- 用于CART算法
```
Gini(S) = 1 - Σ pᵢ²
Gini Gain = Gini(parent) - Σ(|Sᵥ|/|S|) × Gini(Sᵥ)
```

### 3. 剪枝策略

#### 预剪枝 (Pre-pruning)
- 在构建过程中提前停止
- 条件：
  - 最大深度限制
  - 叶节点最小样本数
  - 分裂的最小增益阈值

#### 后剪枝 (Post-pruning)
- 先构建完整树，再剪枝
- 方法：
  - 错误率降低剪枝 (REP)
  - 悲观错误剪枝 (PEP)
  - 代价复杂度剪枝 (CCP)

## 决策树算法

### 1. ID3
- 使用信息增益
- 只能处理离散特征
- 容易过拟合

### 2. C4.5
- 使用信息增益率
- 可处理连续特征
- 可处理缺失值
- 使用剪枝防止过拟合

### 3. CART (Classification and Regression Trees)
- 使用基尼指数（分类）或均方误差（回归）
- 构建二叉树
- 可用于分类和回归

## 优缺点

### 优点
1. **易于理解和解释**: 可视化后直观明了
2. **数据预处理简单**: 不需要标准化、归一化
3. **处理混合类型数据**: 同时处理数值型和分类型特征
4. **鲁棒性强**: 对异常值和缺失值不敏感
5. **特征选择**: 可以自动选择重要特征

### 缺点
1. **过拟合**: 容易在训练数据上过拟合
2. **不稳定**: 数据的小变化可能导致完全不同的树
3. **偏向性**: 某些算法偏向于取值较多的特征
4. **局部最优**: 贪心算法无法保证全局最优
5. **复杂决策边界**: 难以学习XOR等复杂关系

## 超参数

### 分类决策树 (DecisionTreeClassifier)
- `criterion`: 分裂准则 ('gini', 'entropy')
- `max_depth`: 树的最大深度
- `min_samples_split`: 分裂节点所需最小样本数
- `min_samples_leaf`: 叶节点最小样本数
- `max_features`: 寻找最佳分裂时考虑的特征数
- `min_impurity_decrease`: 分裂的最小不纯度减少量

### 回归决策树 (DecisionTreeRegressor)
- `criterion`: 分裂准则 ('squared_error', 'friedman_mse', 'absolute_error')
- 其他参数同分类树

## 使用建议

1. **防止过拟合**
   - 设置max_depth
   - 增大min_samples_split和min_samples_leaf
   - 使用剪枝

2. **特征工程**
   - 处理缺失值
   - 对连续特征进行分箱可能有助于决策树

3. **集成方法**
   - 使用随机森林、梯度提升树等集成方法
   - 可以显著提高性能

## 应用场景

- 医疗诊断
- 信用评估
- 客户流失预测
- 特征重要性分析
- 规则提取

## 可视化

决策树可以通过graphviz或matplotlib进行可视化，便于理解和解释模型。

## 参考资料

- [Scikit-learn Decision Trees](https://scikit-learn.org/stable/modules/tree.html)
- [统计学习方法 - 李航](https://book.douban.com/subject/10590856/)
- [机器学习 - 周志华](https://book.douban.com/subject/26708119/)
