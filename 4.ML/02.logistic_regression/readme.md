# 逻辑回归 (Logistic Regression)

## 1. 算法简介

逻辑回归是一种经典的分类算法，尽管名字中带有"回归"，但它实际上是用于分类问题的。它是神经网络和深度学习的基础。

### 核心思想
- 使用**Sigmoid函数**将线性输出映射到[0,1]区间
- 输出可以解释为样本属于正类的**概率**
- 通过阈值（通常0.5）将概率转换为类别

## 2. 算法原理

### 2.1 Sigmoid函数

```
σ(z) = 1 / (1 + e^(-z))
```

特点：
- 输出范围：(0, 1)
- 在z=0时，σ(z)=0.5
- 当z→+∞，σ(z)→1
- 当z→-∞，σ(z)→0

### 2.2 假设函数

对于二分类问题：

```
h(x) = σ(w·x + b) = 1 / (1 + e^(-(w·x + b)))
```

其中：
- w 是权重向量
- b 是偏置项
- h(x) 表示预测为正类的概率

### 2.3 损失函数（交叉熵）

```
L(y, ŷ) = -[y·log(ŷ) + (1-y)·log(1-ŷ)]
```

整个数据集的损失：
```
J(w,b) = -(1/m) * Σ[yⁱ·log(h(xⁱ)) + (1-yⁱ)·log(1-h(xⁱ))]
```

### 2.4 优化方法

**梯度下降**：
```
w := w - α·∂J/∂w
b := b - α·∂J/∂b
```

其中：
```
∂J/∂w = (1/m)·Xᵀ·(h(X) - y)
∂J/∂b = (1/m)·Σ(h(xⁱ) - yⁱ)
```

## 3. 多分类扩展

### 3.1 一对多 (One-vs-Rest, OvR)
- 为每个类别训练一个二分类器
- 预测时选择概率最高的类别

### 3.2 多项逻辑回归 (Softmax)
```
P(y=k|x) = e^(w_k·x) / Σ_j e^(w_j·x)
```

## 4. 正则化

### 4.1 L2正则化 (Ridge)
```
J(w) = 原损失 + (λ/2m)·||w||²
```
- 防止过拟合
- 权重趋向于较小的值

### 4.2 L1正则化 (Lasso)
```
J(w) = 原损失 + (λ/m)·||w||₁
```
- 产生稀疏解
- 可用于特征选择

### 4.3 弹性网络
```
J(w) = 原损失 + α·(λ1·||w||₁ + λ2·||w||²)
```

## 5. 优缺点

### 优点
- 简单高效，训练速度快
- 输出有概率解释
- 可处理线性可分的二分类问题
- 正则化可防止过拟合
- 系数可解释性强

### 缺点
- 只能处理线性可分数据
- 对非线性问题需要特征变换
- 对异常值敏感
- 多重共线性会影响稳定性

## 6. Scikit-learn 实现

```python
from sklearn.linear_model import LogisticRegression

# 创建模型
model = LogisticRegression(
    penalty='l2',        # 正则化类型: 'l1', 'l2', 'elasticnet', 'none'
    C=1.0,               # 正则化强度的倒数（越小正则化越强）
    solver='lbfgs',      # 优化算法
    max_iter=100,        # 最大迭代次数
    multi_class='auto'   # 多分类策略: 'ovr', 'multinomial'
)

# 训练
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)  # 概率
```

## 7. 参数说明

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| penalty | 正则化类型 | 'l2' (默认) |
| C | 正则化强度倒数 | 0.01-100，交叉验证选择 |
| solver | 优化算法 | 'lbfgs' (小数据), 'sag'/'saga' (大数据) |
| max_iter | 最大迭代次数 | 100-1000 |
| class_weight | 类别权重 | 'balanced' (不平衡数据) |

### Solver选择指南

| Solver | 适用场景 | 支持正则化 |
|--------|---------|-----------|
| lbfgs | 小数据集，多分类 | L2, None |
| liblinear | 小数据集，L1正则化 | L1, L2 |
| sag | 大数据集 | L2, None |
| saga | 大数据集，L1正则化 | L1, L2, ElasticNet |
| newton-cg | 多分类 | L2, None |

## 8. 适用场景

- **推荐场景**：
  - 二分类问题
  - 需要概率输出的场景
  - 特征与标签有线性关系
  - 需要可解释性的场景

- **应用领域**：
  - 信用评分
  - 医疗诊断
  - 垃圾邮件检测
  - 点击率预测

## 9. 示例代码

见 `demo.py` 文件，包含：
- 基础逻辑回归
- 多分类逻辑回归
- 正则化效果对比
- 决策边界可视化
- ROC曲线分析

## 10. 评估指标

### 混淆矩阵
| | 预测正类 | 预测负类 |
|--|---------|---------|
| 实际正类 | TP | FN |
| 实际负类 | FP | TN |

### 关键指标
- **准确率**: (TP+TN)/(TP+FP+FN+TN)
- **精确率**: TP/(TP+FP)
- **召回率**: TP/(TP+FN)
- **F1分数**: 2×P×R/(P+R)
- **ROC-AUC**: 真正率与假正率曲线下面积

## 11. 参考资料

- Cox, D. R. (1958). The regression analysis of binary sequences
- scikit-learn LogisticRegression文档: https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression
