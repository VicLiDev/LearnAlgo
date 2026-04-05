# 机器学习算法文档与示例

本目录包含常用机器学习算法的详细文档和可运行的示例代码，按照从入门到进阶的顺序组织。

## 目录结构

```
4.ML/
├── readme.md                       # 本文件
│
├── Part 1: 基础入门
│   ├── 01.linear_regression/       # 线性回归
│   ├── 02.logistic_regression/     # 逻辑回归
│   ├── 03.knn/                     # K近邻算法
│   └── 04.naive_bayes/             # 朴素贝叶斯
│
├── Part 2: 核心算法
│   ├── 05.decision_tree/           # 决策树
│   ├── 06.svm/                     # 支持向量机
│   └── 07.neural_network/          # 神经网络
│
├── Part 3: 集成学习
│   ├── 08.ensemble_methods/        # 集成方法 (Bagging, Boosting)
│   └── 09.gradient_boosting/       # 梯度提升 (GBDT, XGBoost, LightGBM)
│
├── Part 4: 无监督学习
│   ├── 10.clustering/              # 聚类算法 (K-Means, DBSCAN等)
│   ├── 11.dimensionality_reduction/# 降维算法 (PCA, t-SNE等)
│   └── 12.association_rules/       # 关联规则 (Apriori, FP-Growth)
│
├── Part 5: 进阶应用
│   ├── 13.recommendation/          # 推荐系统 (协同过滤, 矩阵分解)
│   ├── 14.reinforcement_learning/  # 强化学习 (Q-Learning, SARSA, DQN)
│   ├── 15.time_series/             # 时间序列分析 (ARIMA, Prophet)
│   └── 16.semi_supervised/         # 半监督学习 (标签传播, 自训练)
│
├── Part 6: 异常检测
│   └── 17.anomaly_detection/       # 异常检测 (LOF, Isolation Forest)
│
└── Part 7: 工程实践
    └── 18.feature_engineering/     # 特征工程
```

---

## Part 1: 基础入门

### 01. 线性回归 (Linear Regression)
**难度**: ★☆☆☆☆

**内容**:
- 简单线性回归与多元线性回归
- 最小二乘法
- 正则化 (Ridge, Lasso, Elastic Net)
- 多项式回归

**适用场景**: 房价预测、销量预测、趋势分析

```bash
cd 01.linear_regression && python demo.py
```

---

### 02. 逻辑回归 (Logistic Regression)
**难度**: ★☆☆☆☆

**内容**:
- Sigmoid函数
- 二分类与多分类
- 交叉熵损失
- 正则化 (L1, L2)
- ROC/AUC分析

**适用场景**: 信用评分、医疗诊断、垃圾邮件分类

```bash
cd 02.logistic_regression && python demo.py
```

---

### 03. K近邻 (KNN)
**难度**: ★☆☆☆☆

**内容**:
- KNN分类与回归
- 距离度量 (欧氏、曼哈顿、闵可夫斯基)
- K值选择策略
- 加权KNN
- KD树加速

**适用场景**: 推荐系统、图像识别、模式识别

```bash
cd 03.knn && python demo.py
```

---

### 04. 朴素贝叶斯 (Naive Bayes)
**难度**: ★★☆☆☆

**内容**:
- 贝叶斯定理
- 高斯/多项式/伯努利朴素贝叶斯
- 拉普拉斯平滑
- 文本分类应用

**适用场景**: 文本分类、垃圾邮件过滤、情感分析

```bash
cd 04.naive_bayes && python demo.py
```

---

## Part 2: 核心算法

### 05. 决策树 (Decision Tree)
**难度**: ★★☆☆☆

**内容**:
- ID3, C4.5, CART算法
- 信息增益、增益率、基尼指数
- 剪枝策略 (预剪枝、后剪枝)
- 特征重要性

**适用场景**: 分类、回归、特征选择

```bash
cd 05.decision_tree && python demo.py
```

---

### 06. 支持向量机 (SVM)
**难度**: ★★★☆☆

**内容**:
- 线性SVM与非线性SVM
- 核函数 (线性、多项式、RBF)
- 软间隔与硬间隔
- SVM回归 (SVR)
- 参数调优 (C, gamma)

**适用场景**: 图像分类、文本分类、生物信息

```bash
cd 06.svm && python demo.py
```

---

### 07. 神经网络 (Neural Network)
**难度**: ★★★☆☆

**内容**:
- 多层感知机 (MLP)
- 激活函数 (ReLU, Sigmoid, Tanh)
- 反向传播算法
- 优化算法 (SGD, Adam)
- 正则化 (Dropout, L2)

**适用场景**: 图像识别、自然语言处理、复杂非线性问题

```bash
cd 07.neural_network && python demo.py
```

---

## Part 3: 集成学习

### 08. 集成方法 (Ensemble Methods)
**难度**: ★★☆☆☆

**内容**:
- Bagging集成思想
- 随机特征选择
- 袋外误差 (OOB)
- 特征重要性
- 极端随机树

**适用场景**: 分类、回归、特征选择

```bash
cd 08.ensemble_methods && python demo.py
```

---

### 09. 梯度提升 (Gradient Boosting)
**难度**: ★★★☆☆

**内容**:
- GBDT (梯度提升决策树)
- AdaBoost
- XGBoost
- LightGBM
- CatBoost
- 早停机制

**适用场景**: 结构化数据、Kaggle竞赛、点击率预测

```bash
cd 09.gradient_boosting && python demo.py
```

---

## Part 4: 无监督学习

### 10. 聚类算法 (Clustering)
**难度**: ★★☆☆☆

**内容**:
- K-Means及其变体
- 层次聚类
- DBSCAN
- 高斯混合模型 (GMM)
- 谱聚类

**适用场景**: 客户分群、图像分割、异常检测

```bash
cd 10.clustering && python demo.py
```

---

### 11. 降维算法 (Dimensionality Reduction)
**难度**: ★★☆☆☆

**内容**:
- PCA (主成分分析)
- LDA (线性判别分析)
- t-SNE
- UMAP
- Kernel PCA

**适用场景**: 数据可视化、特征压缩、降噪

```bash
cd 11.dimensionality_reduction && python demo.py
```

---

### 12. 关联规则 (Association Rules)
**难度**: ★★☆☆☆

**内容**:
- Apriori算法
- FP-Growth算法
- 支持度、置信度、提升度
- 购物篮分析

**适用场景**: 零售分析、交叉销售、Web挖掘

```bash
cd 12.association_rules && python demo.py
```

---

## Part 5: 进阶应用

### 13. 推荐系统 (Recommendation System)
**难度**: ★★★☆☆

**内容**:
- 协同过滤 (User-CF, Item-CF)
- 矩阵分解 (SVD, ALS)
- 基于内容推荐
- 推荐评估指标

**适用场景**: 电商推荐、电影推荐、内容推荐

```bash
cd 13.recommendation && python demo.py
```

---

### 14. 强化学习 (Reinforcement Learning)
**难度**: ★★★★☆

**内容**:
- MDP (马尔可夫决策过程)
- Q-Learning
- SARSA
- Deep Q-Network (DQN)
- 探索与利用

**适用场景**: 游戏AI、机器人控制、自动驾驶

```bash
cd 14.reinforcement_learning && python demo.py
```

---

### 15. 时间序列分析 (Time Series)
**难度**: ★★★☆☆

**内容**:
- 时间序列分解
- 平稳性检验 (ADF)
- ARIMA/SARIMA
- 指数平滑 (Holt-Winters)
- Prophet

**适用场景**: 销量预测、股票分析、负荷预测

```bash
cd 15.time_series && python demo.py
```

---

### 16. 半监督学习 (Semi-Supervised)
**难度**: ★★★☆☆

**内容**:
- 自训练 (Self-Training)
- 标签传播 (Label Propagation)
- 标签扩散 (Label Spreading)
- 协同训练

**适用场景**: 标签数据稀缺、医学影像、文本分类

```bash
cd 16.semi_supervised && python demo.py
```

---

## Part 6: 异常检测

### 17. 异常检测 (Anomaly Detection)
**难度**: ★★★☆☆

**内容**:
- 统计方法 (Z-score, IQR)
- LOF (局部离群因子)
- Isolation Forest
- One-Class SVM

**适用场景**: 欺诈检测、入侵检测、设备故障预测

```bash
cd 17.anomaly_detection && python demo.py
```

---

## Part 7: 工程实践

### 18. 特征工程 (Feature Engineering)
**难度**: ★★☆☆☆

**内容**:
- 缺失值处理
- 特征缩放 (标准化、归一化)
- 类别编码 (Label, One-Hot, Target)
- 特征选择 (Filter, Wrapper, Embedded)
- 特征构造
- Scikit-learn流水线

**适用场景**: 所有机器学习项目的数据预处理

```bash
cd 18.feature_engineering && python demo.py
```

---

## 快速开始

### 环境要求

```bash
# 基础环境
pip install numpy scipy scikit-learn matplotlib pandas

# 可选依赖 (部分示例需要)
pip install xgboost lightgbm statsmodels mlxtend
```

### 运行所有示例

```bash
# 按顺序运行所有算法的示例代码
for dir in 01.linear_regression 02.logistic_regression 03.knn 04.naive_bayes \
           05.decision_tree 06.svm 07.neural_network \
           08.random_forest 09.gradient_boosting \
           10.clustering 11.dimensionality_reduction 12.association_rules 13.anomaly_detection \
           14.time_series 15.recommendation 16.semi_supervised \
           17.reinforcement_learning 18.feature_engineering; do
    echo "Running $dir..."
    cd $dir && python demo.py && cd ..
done
```

---

## 学习路径

### 入门阶段 (1-3周)
1. **线性回归** → 理解基本的监督学习
2. **逻辑回归** → 分类问题入门
3. **KNN** → 最简单的分类算法
4. **朴素贝叶斯** → 概率分类方法
5. **特征工程** → 数据预处理基础

### 进阶阶段 (2-4周)
6. **决策树** → 可解释性强的模型
7. **随机森林** → 集成学习入门
8. **SVM** → 核方法理解
9. **聚类算法** → 无监督学习
10. **降维算法** → 高维数据处理

### 高级阶段 (3-6周)
11. **梯度提升** → 强大的集成方法
12. **神经网络** → 深度学习基础
13. **异常检测** → 实用技能
14. **时间序列** → 序列数据分析

### 专业方向 (按需学习)
15. **推荐系统** → 电商/内容行业
16. **半监督学习** → 标签稀缺场景
17. **强化学习** → 游戏/机器人领域
18. **关联规则** → 零售/数据分析

---

## 算法选择指南

| 问题类型 | 数据特点         | 推荐算法              |
|----------|------------------|-----------------------|
| 回归     | 线性关系         | 线性回归              |
| 回归     | 非线性关系       | 梯度提升、神经网络    |
| 分类     | 小样本、线性可分 | 逻辑回归、SVM(线性核) |
| 分类     | 小样本、非线性   | SVM(RBF核)、随机森林  |
| 分类     | 大样本           | 梯度提升、神经网络    |
| 分类     | 文本数据         | 朴素贝叶斯、逻辑回归  |
| 分类     | 需要概率输出     | 逻辑回归              |
| 分类     | 简单直观         | KNN                   |
| 聚类     | 球形簇           | K-Means               |
| 聚类     | 任意形状         | DBSCAN                |
| 降维     | 可视化           | t-SNE、UMAP           |
| 降维     | 特征压缩         | PCA                   |
| 表格数据 | 追求高精度       | XGBoost、LightGBM     |
| 时间序列 | 趋势+季节性      | ARIMA、Prophet        |
| 推荐系统 | 用户行为丰富     | 协同过滤              |
| 异常检测 | 无标签           | Isolation Forest      |

---

## 评估指标速查

### 分类指标
- **准确率** (Accuracy): (TP+TN)/(TP+FP+FN+TN)
- **精确率** (Precision): TP/(TP+FP)
- **召回率** (Recall): TP/(TP+FN)
- **F1分数**: 2×P×R/(P+R)
- **ROC-AUC**: 真正率与假正率曲线下面积

### 回归指标
- **MAE**: 平均绝对误差
- **MSE**: 均方误差
- **RMSE**: 均方根误差
- **R²**: 决定系数

### 聚类指标
- **轮廓系数** (Silhouette Score)
- **Calinski-Harabasz指数**
- **Davies-Bouldin指数**

---

## 参考资料

### 书籍
- 《统计学习方法》- 李航
- 《机器学习》- 周志华
- 《Pattern Recognition and Machine Learning》- Christopher Bishop
- 《Deep Learning》- Ian Goodfellow
- 《Feature Engineering for Machine Learning》- Alice Zheng

### 在线资源
- [Scikit-learn官方文档](https://scikit-learn.org/)
- [机器学习速成课程 - Google](https://developers.google.com/machine-learning/crash-course)
- [CS229: Machine Learning - Stanford](http://cs229.stanford.edu/)

---

## 贡献

欢迎提交Issue和Pull Request来完善这些文档和示例！

## 许可证

MIT License
