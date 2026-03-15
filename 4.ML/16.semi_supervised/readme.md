# 半监督学习 (Semi-Supervised Learning)

## 1. 简介

半监督学习介于监督学习和无监督学习之间，利用少量有标签数据和大量无标签数据进行学习。

### 为什么需要半监督学习？
- 标签数据获取成本高（需要专家标注）
- 无标签数据容易获取
- 无标签数据包含有价值的信息

### 假设
1. **平滑假设**：相近的样本有相同的标签
2. **聚类假设**：同一簇的样本有相同的标签
3. **流形假设**：数据位于低维流形上

## 2. 主要方法

| 方法 | 代表算法 | 思想 |
|------|---------|------|
| 自训练 | Self-Training | 用模型预测无标签数据 |
| 协同训练 | Co-Training | 多视图互相训练 |
| 图方法 | Label Propagation | 基于图的标签传播 |
| 生成模型 | VAE, GAN | 学习数据分布 |
| 一致性正则化 | Π-Model, Mean Teacher | 增强一致性 |

## 3. 自训练 (Self-Training)

### 3.1 算法流程

```
1. 用有标签数据训练初始模型
2. 用模型预测无标签数据
3. 选择置信度高的样本加入训练集
4. 重新训练模型
5. 重复步骤2-4直到满足条件
```

### 3.2 实现示例

```python
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

# 初始训练
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_labeled, y_labeled)

# 迭代自训练
for _ in range(10):
    # 预测无标签数据
    proba = model.predict_proba(X_unlabeled)
    max_proba = np.max(proba, axis=1)

    # 选择高置信度样本
    threshold = 0.9
    confident_mask = max_proba > threshold

    if not any(confident_mask):
        break

    # 添加到训练集
    X_labeled = np.vstack([X_labeled, X_unlabeled[confident_mask]])
    y_labeled = np.hstack([y_labeled, model.predict(X_unlabeled[confident_mask])])
    X_unlabeled = X_unlabeled[~confident_mask]

    # 重新训练
    model.fit(X_labeled, y_labeled)
```

### 3.3 优缺点

**优点**：
- 简单易实现
- 可用于任何分类器

**缺点**：
- 可能传播错误标签
- 对初始模型敏感

## 4. 协同训练 (Co-Training)

### 4.1 算法思想

使用两个分类器在不同的特征视图上训练，互相标记高置信度样本。

### 4.2 前提条件
- 数据有两个充分冗余的视图
- 每个视图都能独立进行分类

### 4.3 算法流程

```
1. 将特征分为两个视图 V1, V2
2. 在V1和V2上分别训练分类器 C1, C2
3. 每个分类器预测无标签数据
4. 各自选择高置信度样本加入对方的训练集
5. 重新训练两个分类器
6. 重复步骤3-5
```

## 5. 标签传播 (Label Propagation)

### 5.1 图构建

构建一个图，节点是样本，边权重表示相似度：

```
Wij = exp(-||xi - xj||² / 2σ²)
```

### 5.2 标签传播算法

```
1. 构建相似度图
2. 计算转移矩阵 T = D^(-1/2) W D^(-1/2)
3. 初始化标签矩阵 Y
4. 迭代: Y = α T Y + (1-α) Y_0
5. 收敛后给无标签节点分配标签
```

### 5.3 Scikit-learn实现

```python
from sklearn.semi_supervised import LabelPropagation

# 标签中-1表示无标签
y_semi = np.copy(y)
y_semi[unlabeled_indices] = -1

model = LabelPropagation(kernel='rbf', gamma=20)
model.fit(X, y_semi)

# 获取预测
y_pred = model.transduction_
```

## 6. 半监督分类器

Scikit-learn提供两种半监督分类器：

### 6.1 LabelPropagation
- 基于图的方法
- 支持RBF和KNN核

### 6.2 LabelSpreading
- LabelPropagation的变体
- 对噪声更鲁棒
- 使用归一化的图拉普拉斯矩阵

```python
from sklearn.semi_supervised import LabelSpreading

model = LabelSpreading(kernel='knn', n_neighbors=5)
model.fit(X, y_semi)
```

## 7. 一致性正则化

### 7.1 思想

对同一样本的不同扰动版本，模型应该给出一致的预测。

### 7.2 Π-Model

```
L = L_s + λ * Σ ||f(x) - f(Aug(x))||²
```
- L_s: 有标签数据的监督损失
- Aug(x): 数据增强

### 7.3 Mean Teacher

使用指数移动平均更新教师模型：
```
θ'_t = α θ'_{t-1} + (1-α) θ_t
```

## 8. 评估方法

### 8.1 实验设置

1. 固定有标签数据比例
2. 用测试集评估性能
3. 比较不同方法

### 8.2 基准对比

| 方法 | 有标签比例 | 准确率 |
|------|-----------|--------|
| 仅监督 | 10% | 75% |
| 自训练 | 10% | 80% |
| 标签传播 | 10% | 82% |

## 9. 应用场景

- **文本分类**：少量标注文档，大量未标注网页
- **图像识别**：少量标注图片，大量未标注图片
- **语音识别**：少量转录语音，大量未转录语音
- **医学影像**：专家标注成本高

## 10. 实践建议

1. **确认假设适用**：数据是否满足平滑/聚类假设
2. **合理设置阈值**：自训练的置信度阈值
3. **控制迭代次数**：避免错误累积
4. **监控验证集**：防止性能下降

## 11. 示例代码

见 `demo.py` 文件，包含：
- 自训练实现
- 标签传播
- 协同训练
- 方法对比

## 12. 参考资料

- Chapelle, O., et al. (2006). Semi-Supervised Learning
- Zhu, X., & Ghahramani, Z. (2002). Learning from Labeled and Unlabeled Data with Graph Laplacian
- scikit-learn半监督学习: https://scikit-learn.org/stable/modules/label_propagation.html
