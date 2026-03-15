# 梯度提升算法 (Gradient Boosting)

## 1. 算法简介

梯度提升是一种强大的集成学习技术，通过迭代地训练弱学习器（通常是决策树）来纠正前一轮的错误，最终组合成强学习器。

### 核心思想
- **Boosting**：串行训练多个弱学习器
- **梯度下降**：在函数空间中进行梯度优化
- **前向分步**：每一步添加一个新模型来减少残差

## 2. 算法原理

### 2.1 基本流程

```
初始化: F₀(x) = argmin_c Σ L(yᵢ, c)

对于 m = 1 到 M:
    1. 计算负梯度（伪残差）:
       rᵢₘ = -∂L(yᵢ, F(xᵢ))/∂F(xᵢ) |_{F=F_{m-1}}

    2. 用基学习器拟合残差:
       hₘ(x) = fit({(xᵢ, rᵢₘ)})

    3. 线性搜索找最优步长:
       γₘ = argmin_γ Σ L(yᵢ, F_{m-1}(xᵢ) + γhₘ(xᵢ))

    4. 更新模型:
       Fₘ(x) = F_{m-1}(x) + γₘhₘ(x)

输出: F_M(x)
```

### 2.2 损失函数

| 任务 | 损失函数 | 负梯度 |
|------|---------|--------|
| 回归 | 均方误差 (MSE) | y - F(x) |
| 回归 | 绝对误差 (MAE) | sign(y - F(x)) |
| 分类 | 对数损失 (Log Loss) | y - σ(F(x)) |
| 分类 | 指数损失 | y·e^{-yF(x)} |

### 2.3 正则化

1. **学习率 (Learning Rate / Shrinkage)**
   ```
   Fₘ(x) = Fₘ₋₁(x) + ν·γₘhₘ(x)
   ```
   - ν 通常取 0.01-0.3
   - 较小的学习率需要更多的树

2. **子采样 (Subsampling)**
   - 每轮只使用部分样本
   - 类似随机森林的特征采样

3. **树的深度限制**
   - 限制决策树的深度
   - 通常使用浅层树 (深度3-8)

4. **早停 (Early Stopping)**
   - 验证集性能不再提升时停止

## 3. 主要算法变体

### 3.1 AdaBoost

**特点**：
- 通过调整样本权重来关注难分样本
- 指数损失函数
- 二分类的经典方法

**算法流程**：
```
1. 初始化样本权重 wᵢ = 1/n
2. 训练弱分类器 hₘ
3. 计算加权错误率 εₘ
4. 计算分类器权重 αₘ = 0.5·log((1-εₘ)/εₘ)
5. 更新样本权重 wᵢ ← wᵢ·exp(αₘ·I(yᵢ≠hₘ(xᵢ)))
6. 最终分类器: H(x) = sign(Σαₘhₘ(x))
```

### 3.2 GBDT (Gradient Boosting Decision Tree)

**特点**：
- 使用决策树作为基学习器
- 回归树用于回归，分类树用于分类
- 使用负梯度作为残差近似

**Scikit-learn实现**：
```python
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor

# 分类
clf = GradientBoostingClassifier(
    n_estimators=100,    # 树的数量
    learning_rate=0.1,   # 学习率
    max_depth=3,         # 树的最大深度
    subsample=0.8,       # 子采样比例
    random_state=42
)

# 回归
reg = GradientBoostingRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3
)
```

### 3.3 XGBoost

**特点**：
- 正则化的目标函数（L1+L2）
- 二阶泰勒展开优化
- 支持并行计算
- 处理缺失值
- 列采样

**目标函数**：
```
Obj = Σ L(yᵢ, ŷᵢ) + Σ Ω(fₖ)
```

其中正则项：
```
Ω(f) = γT + 0.5λ||w||²
```
- T：叶节点数
- w：叶节点权重

**使用方法**：
```python
import xgboost as xgb

# 分类
model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,    # L1正则化
    reg_lambda=1.0,   # L2正则化
    random_state=42
)

model.fit(X_train, y_train)
```

### 3.4 LightGBM

**特点**：
- 基于直方图的算法，速度快
- GOSS (Gradient-based One-Side Sampling)
- EFB (Exclusive Feature Bundling)
- Leaf-wise生长策略（相比Level-wise）

**Leaf-wise vs Level-wise**：
| 策略 | 优点 | 缺点 |
|------|------|------|
| Level-wise | 不易过拟合 | 效率低 |
| Leaf-wise | 收敛快、精度高 | 小数据易过拟合 |

**使用方法**：
```python
import lightgbm as lgb

model = lgb.LGBMClassifier(
    n_estimators=100,
    max_depth=-1,        # -1表示不限制
    num_leaves=31,       # 叶节点数
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(X_train, y_train)
```

### 3.5 CatBoost

**特点**：
- 原生支持类别特征
- Ordered Boosting减少过拟合
- 对称树结构

**使用方法**：
```python
from catboost import CatBoostClassifier

model = CatBoostClassifier(
    iterations=100,
    depth=6,
    learning_rate=0.1,
    cat_features=[0, 1, 2],  # 类别特征索引
    random_state=42
)

model.fit(X_train, y_train)
```

## 4. 算法对比

| 特性 | GBDT | XGBoost | LightGBM | CatBoost |
|------|------|---------|----------|----------|
| 速度 | 慢 | 中等 | 快 | 中等 |
| 内存 | 高 | 中等 | 低 | 高 |
| 精度 | 好 | 很好 | 很好 | 很好 |
| 类别特征 | 需编码 | 需编码 | 支持有限 | 原生支持 |
| 缺失值 | 不支持 | 支持 | 支持 | 支持 |
| 并行化 | 无 | 特征并行 | 特征+数据并行 | 特征并行 |

## 5. 参数调优指南

### 5.1 核心参数

| 参数 | 说明 | 推荐范围 |
|------|------|---------|
| n_estimators | 树的数量 | 100-1000+ |
| learning_rate | 学习率 | 0.01-0.3 |
| max_depth | 树的最大深度 | 3-10 |
| min_samples_split | 分裂最小样本数 | 2-20 |
| subsample | 样本采样比例 | 0.5-1.0 |
| colsample_bytree | 特征采样比例 | 0.5-1.0 |

### 5.2 调优策略

1. **固定学习率，调树数量**：
   - 设置 learning_rate=0.1
   - 通过早停找最优 n_estimators

2. **调树参数**：
   - max_depth, min_samples_split

3. **调正则化参数**：
   - subsample, colsample_bytree
   - reg_alpha, reg_lambda

4. **降低学习率，增加树数量**：
   - learning_rate=0.01, n_estimators=1000+

## 6. 优缺点

### 优点
- 预测精度高
- 可处理各种类型特征
- 自动特征选择
- 可解释性较好（特征重要性）
- 对异常值鲁棒

### 缺点
- 训练时间较长（串行）
- 容易过拟合（需要正则化）
- 超参数较多
- 对噪声数据敏感

## 7. 适用场景

- **推荐场景**：
  - 结构化数据的分类/回归
  - 特征工程后的表格数据
  - 需要高精度的预测任务

- **典型应用**：
  - 点击率预测
  - 排序学习
  - 风险评分
  - Kaggle竞赛

## 8. 示例代码

见 `demo.py` 文件，包含：
- 基础GBDT示例
- 学习率和树数量影响
- XGBoost/LightGBM对比
- 特征重要性分析
- 早停机制

## 9. 参考资料

- Friedman, J. H. (2001). Greedy Function Approximation: A Gradient Boosting Machine
- Chen, T., & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System
- Ke, G., et al. (2017). LightGBM: A Highly Efficient Gradient Boosting Decision Tree
- Prokhorenkova, L., et al. (2018). CatBoost: unbiased boosting with categorical features
