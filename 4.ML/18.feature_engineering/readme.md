# 特征工程 (Feature Engineering)

## 1. 简介

特征工程是将原始数据转换为更能代表问题本质的特征的过程。好的特征工程可以显著提升模型性能。

> "特征工程是应用机器学习中最重要、最耗时、也是最需要专业知识的步骤。"
> — Andrew Ng

### 特征工程流程
1. 特征理解：了解每个特征的含义
2. 特征清洗：处理缺失值、异常值
3. 特征变换：标准化、归一化、编码
4. 特征构造：创建新特征
5. 特征选择：选择最有用的特征

## 2. 缺失值处理

### 2.1 缺失值类型
- **MCAR**：完全随机缺失
- **MAR**：随机缺失
- **MNAR**：非随机缺失

### 2.2 处理方法

| 方法       | 说明                | 适用场景         |
|------------|---------------------|------------------|
| 删除       | 删除含缺失值的行/列 | 缺失比例小       |
| 均值填充   | 用均值填充          | 数值型，正态分布 |
| 中位数填充 | 用中位数填充        | 数值型，偏态分布 |
| 众数填充   | 用众数填充          | 类别型           |
| 插值       | 线性/多项式插值     | 时间序列         |
| 模型预测   | 用其他特征预测      | 有相关性         |

### 2.3 实现

```python
from sklearn.impute import SimpleImputer, KNNImputer

# 简单填充
imputer = SimpleImputer(strategy='mean')  # mean, median, most_frequent, constant
X_filled = imputer.fit_transform(X)

# KNN填充
knn_imputer = KNNImputer(n_neighbors=5)
X_filled = knn_imputer.fit_transform(X)
```

## 3. 异常值处理

### 3.1 检测方法
- Z-score: |z| > 3
- IQR: 超过 Q1-1.5×IQR 或 Q3+1.5×IQR
- 孤立森林

### 3.2 处理方法
- 删除
- 截断（Capping）
- 对数变换
- 分箱

## 4. 特征缩放

### 4.1 标准化 (Standardization)

```
x' = (x - μ) / σ
```

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

### 4.2 归一化 (Normalization)

```
x' = (x - x_min) / (x_max - x_min)
```

```python
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
```

### 4.3 鲁棒缩放

使用中位数和IQR，对异常值鲁棒：

```python
from sklearn.preprocessing import RobustScaler

scaler = RobustScaler()
X_scaled = scaler.fit_transform(X)
```

### 4.4 选择指南

| 方法           | 适用场景             |
|----------------|----------------------|
| StandardScaler | 正态分布，需要零均值 |
| MinMaxScaler   | 有界范围，如[0,1]    |
| RobustScaler   | 有异常值             |
| Log            | 右偏分布             |

## 5. 类别特征编码

### 5.1 标签编码 (Label Encoding)

```python
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
X_encoded = le.fit_transform(X)
```

### 5.2 独热编码 (One-Hot Encoding)

```python
from sklearn.preprocessing import OneHotEncoder

ohe = OneHotEncoder(sparse=False)
X_encoded = ohe.fit_transform(X)
```

### 5.3 目标编码 (Target Encoding)

```python
# 计算每个类别的目标均值
target_mean = df.groupby('category')['target'].mean()
df['category_encoded'] = df['category'].map(target_mean)
```

### 5.4 选择指南

| 方法               | 适用场景         |
|--------------------|------------------|
| Label Encoding     | 有序类别         |
| One-Hot            | 无序类别，类别少 |
| Target Encoding    | 无序类别，类别多 |
| Frequency Encoding | 类别频率有意义   |

## 6. 特征构造

### 6.1 数值特征
- 多项式特征
- 对数变换
- 差分
- 比率

```python
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)
```

### 6.2 日期特征
- 年、月、日、星期几
- 是否周末
- 季度
- 节假日

### 6.3 文本特征
- TF-IDF
- 词嵌入
- N-grams

### 6.4 交互特征
```
feature_3 = feature_1 * feature_2
feature_4 = feature_1 / feature_2
```

## 7. 特征选择

### 7.1 过滤法 (Filter)

**方差阈值**：
```python
from sklearn.feature_selection import VarianceThreshold

selector = VarianceThreshold(threshold=0.1)
X_selected = selector.fit_transform(X)
```

**相关系数**：
```python
correlations = df.corr()['target'].abs().sort_values(ascending=False)
```

**卡方检验**：
```python
from sklearn.feature_selection import chi2, SelectKBest

selector = SelectKBest(chi2, k=10)
X_selected = selector.fit_transform(X, y)
```

### 7.2 包装法 (Wrapper)

**递归特征消除 (RFE)**：
```python
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

rfe = RFE(LogisticRegression(), n_features_to_select=10)
X_selected = rfe.fit_transform(X, y)
```

### 7.3 嵌入法 (Embedded)

**L1正则化**：
```python
from sklearn.linear_model import Lasso

lasso = Lasso(alpha=0.1)
lasso.fit(X, y)
# 查看系数非零的特征
```

**树模型重要性**：
```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier()
rf.fit(X, y)
importances = rf.feature_importances_
```

## 8. 特征变换

### 8.1 对数变换
```
x' = log(x + 1)
```
适用于右偏分布。

### 8.2 Box-Cox变换
```
x' = (x^λ - 1) / λ  (λ ≠ 0)
x' = log(x)         (λ = 0)
```

### 8.3 分箱 (Binning)
```python
from sklearn.preprocessing import KBinsDiscretizer

discretizer = KBinsDiscretizer(n_bins=5, encode='onehot', strategy='uniform')
X_binned = discretizer.fit_transform(X)
```

## 9. 特征工程流水线

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# 数值特征处理
numeric_features = ['age', 'income']
numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# 类别特征处理
categorical_features = ['city', 'gender']
categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# 组合
preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)
])

# 完整流水线
clf = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression())
])
```

## 10. 最佳实践

1. **先理解数据**：EDA是特征工程的基础
2. **避免数据泄露**：特征工程只使用训练数据
3. **保持简单**：从简单特征开始
4. **迭代优化**：根据模型反馈调整
5. **记录过程**：便于复现和调试

## 11. 示例代码

见 `demo.py` 文件，包含：
- 缺失值处理
- 特征缩放
- 类别编码
- 特征选择
- 完整流水线

## 12. 参考资料

- Zheng, A., & Casari, A. (2018). Feature Engineering for Machine Learning
- scikit-learn预处理: https://scikit-learn.org/stable/modules/preprocessing.html
- Kaggle特征工程教程
