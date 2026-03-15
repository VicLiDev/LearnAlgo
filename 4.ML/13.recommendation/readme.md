# 推荐系统 (Recommendation System)

## 1. 简介

推荐系统是一种信息过滤系统，预测用户对物品的评分或偏好，从而向用户推荐可能感兴趣的物品。

### 推荐系统类型

| 类型 | 方法 | 特点 |
|------|------|------|
| 协同过滤 | User-CF, Item-CF | 基于用户行为 |
| 基于内容 | Content-Based | 基于物品特征 |
| 混合推荐 | Hybrid | 结合多种方法 |
| 深度学习 | Neural CF, NCF | 端到端学习 |

## 2. 协同过滤

### 2.1 基于用户的协同过滤 (User-CF)

**核心思想**：找相似用户，推荐相似用户喜欢的物品

**相似度计算**：
- 余弦相似度：`sim(u,v) = cos(r_u, r_v)`
- 皮尔逊相关系数
- Jaccard相似度

**预测公式**：
```
r̂(u,i) = r̄ᵤ + Σ sim(u,v) × (r(v,i) - r̄ᵥ) / Σ |sim(u,v)|
```

### 2.2 基于物品的协同过滤 (Item-CF)

**核心思想**：推荐与用户历史喜欢的物品相似的物品

**相似度计算**：
```
sim(i,j) = Σ r(u,i) × r(u,j) / √(Σ r(u,i)² × Σ r(u,j)²)
```

**预测公式**：
```
r̂(u,i) = Σ sim(i,j) × r(u,j) / Σ |sim(i,j)|
```

### 2.3 User-CF vs Item-CF

| 特性 | User-CF | Item-CF |
|------|---------|---------|
| 适用场景 | 社交、新闻 | 电商、电影 |
| 用户数变化 | 敏感 | 不敏感 |
| 物品数变化 | 不敏感 | 敏感 |
| 解释性 | 弱 | 强 |
| 冷启动 | 用户冷启动难 | 物品冷启动难 |

## 3. 矩阵分解

### 3.1 原理

将用户-物品评分矩阵分解为两个低维矩阵：
```
R ≈ U × Vᵀ
```
- U：用户隐因子矩阵 (n_users × k)
- V：物品隐因子矩阵 (n_items × k)
- k：隐因子维度

### 3.2 SVD分解

```
R = U Σ Vᵀ
```

### 3.3 带偏置的矩阵分解

```
r̂(u,i) = μ + bᵤ + bᵢ + pᵤ · qᵢ
```
- μ：全局平均评分
- bᵤ：用户偏置
- bᵢ：物品偏置
- pᵤ：用户隐向量
- qᵢ：物品隐向量

### 3.4 优化目标

```
min Σ (r(u,i) - r̂(u,i))² + λ(||pᵤ||² + ||qᵢ||²)
```

优化方法：
- SGD（随机梯度下降）
- ALS（交替最小二乘）

### 3.5 实现 (Surprise库)

```python
from surprise import SVD, Dataset, accuracy
from surprise.model_selection import train_test_split

data = Dataset.load_builtin('ml-100k')
trainset, testset = train_test_split(data, test_size=0.2)

algo = SVD(n_factors=100, n_epochs=20, lr_all=0.005, reg_all=0.02)
algo.fit(trainset)

predictions = algo.test(testset)
accuracy.rmse(predictions)
```

## 4. 基于内容推荐

### 4.1 原理

根据物品特征和用户偏好进行匹配：
1. 构建物品特征向量
2. 构建用户偏好向量
3. 计算相似度

### 4.2 TF-IDF

用于文本特征提取：
```
TF-IDF(t,d) = TF(t,d) × IDF(t)
IDF(t) = log(N / df(t))
```

### 4.3 实现

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 物品描述
descriptions = ["动作电影...", "爱情电影...", ...]
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(descriptions)

# 计算相似度
cosine_sim = cosine_similarity(tfidf_matrix)
```

## 5. 评估指标

### 5.1 预测准确性

| 指标 | 公式 | 说明 |
|------|------|------|
| MAE | Σ\|r - r̂\|/n | 平均绝对误差 |
| RMSE | √(Σ(r-r̂)²/n) | 均方根误差 |

### 5.2 排序质量

| 指标 | 说明 |
|------|------|
| Precision@K | 前K个推荐中相关物品比例 |
| Recall@K | 相关物品被推荐的比例 |
| NDCG | 考虑位置的排序指标 |
| MAP | 平均精度均值 |

### 5.3 覆盖率

- **物品覆盖率**：被推荐物品占总物品比例
- **用户覆盖率**：收到推荐的用户比例

## 6. 冷启动问题

### 6.1 用户冷启动
- 基于人口统计学推荐
- 热门物品推荐
- 注册时收集偏好

### 6.2 物品冷启动
- 基于内容推荐
- 利用物品属性
- 专家标注

## 7. 高级方法

### 7.1 隐语义模型 (LFM)
- 从评分矩阵学习隐因子
- 类似于矩阵分解

### 7.2 神经网络协同过滤 (NCF)
- 用神经网络学习用户-物品交互
- 结合MF和MLP

### 7.3 序列推荐
- 基于RNN/LSTM
- 考虑时间顺序

## 8. 实践建议

1. **数据预处理**
   - 归一化评分
   - 处理缺失值
   - 去除异常值

2. **特征工程**
   - 时间特征
   - 用户行为序列
   - 上下文信息

3. **模型选择**
   - 小数据：协同过滤
   - 有内容：混合推荐
   - 大数据：深度学习

## 9. 应用场景

- **电商**：商品推荐
- **视频**：电影/短视频推荐
- **音乐**：歌曲推荐
- **新闻**：文章推荐
- **社交**：好友推荐

## 10. 示例代码

见 `demo.py` 文件，包含：
- User-CF实现
- Item-CF实现
- 矩阵分解
- 推荐评估

## 11. 参考资料

- Koren, Y., et al. (2009). Matrix Factorization Techniques for Recommender Systems
- He, X., et al. (2017). Neural Collaborative Filtering
- Recommender Systems Handbook
- Surprise文档: https://surprise.readthedocs.io/
