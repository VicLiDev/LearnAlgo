# 异常检测 (Anomaly Detection)

## 1. 算法简介

异常检测是识别数据中与正常模式显著不同的数据点。异常值（也称为离群点）可能表示错误、欺诈或罕见事件。

### 异常类型
- **点异常**：单个数据点与整体分布不同
- **上下文异常**：在特定上下文中异常（如时间序列中的季节性）
- **集体异常**：一组数据点一起构成异常

## 2. 常用方法

### 2.1 方法分类

| 类别     | 方法             | 特点         |
|----------|------------------|--------------|
| 统计方法 | Z-score、IQR     | 简单、可解释 |
| 基于距离 | KNN、LOF         | 考虑局部密度 |
| 基于密度 | DBSCAN、LODA     | 适合任意形状 |
| 基于聚类 | K-Means、GMM     | 无监督       |
| 基于树   | Isolation Forest | 高效、可扩展 |
| 基于重构 | Autoencoder      | 深度学习方法 |

## 3. 统计方法

### 3.1 Z-Score方法

```
z = (x - μ) / σ
```

- |z| > 3 通常被认为是异常值
- 适用于正态分布数据

### 3.2 IQR方法（四分位距）

```
IQR = Q3 - Q1
下界 = Q1 - 1.5 × IQR
上界 = Q3 + 1.5 × IQR
```

- 不受极端值影响
- 适用于偏态分布

## 4. 局部离群因子 (LOF)

### 4.1 算法原理

LOF通过比较局部密度来识别异常。一个点的LOF值表示其密度与邻居密度的比值。

**计算步骤**：
1. 计算k-距离：到第k近邻居的距离
2. 计算可达距离：max(k-距离, 实际距离)
3. 计算局部可达密度 (LRD)
4. 计算LOF：邻居LRD的平均值 / 自身LRD

### 4.2 LOF解读

| LOF值 | 含义                       |
|-------|----------------------------|
| `≈ 1` | 与邻居密度相似（正常）     |
| `> 1` | 比邻居密度低（可能是异常） |
| `< 1` | 比邻居密度高（密集区域）   |

### 4.3 Scikit-learn实现

```python
from sklearn.neighbors import LocalOutlierFactor

lof = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
y_pred = lof.fit_predict(X)  # 1: 正常, -1: 异常
```

## 5. 孤立森林 (Isolation Forest)

### 5.1 算法原理

孤立森林基于一个直觉：异常点更容易被孤立（分离）。

**核心思想**：
- 随机选择特征和分割点构建树
- 异常点需要更少的分割次数就能被隔离
- 路径长度短的点更可能是异常

### 5.2 异常分数

```
s(x, n) = 2^(-E(h(x)) / c(n))
```

- h(x)：路径长度
- c(n)：归一化因子
- s接近1：异常
- s接近0.5：正常

### 5.3 优缺点

**优点**：
- 计算效率高，O(n)
- 不需要计算距离矩阵
- 适合高维数据
- 可处理大规模数据

**缺点**：
- 对密集区域的异常检测效果较差
- 参数选择影响结果

### 5.4 Scikit-learn实现

```python
from sklearn.ensemble import IsolationForest

iso_forest = IsolationForest(
    n_estimators=100,
    contamination=0.1,
    random_state=42
)
y_pred = iso_forest.fit_predict(X)
```

## 6. One-Class SVM

### 6.1 算法原理

One-Class SVM学习一个将正常数据包围起来的边界，边界外的点被认为是异常。

**目标**：找到最小的超球面包含所有（或大部分）正常样本

### 6.2 核函数选择

| 核函数 | 适用场景     |
|--------|--------------|
| RBF    | 通用，最常用 |
| Linear | 线性可分数据 |
| Poly   | 多项式边界   |

### 6.3 Scikit-learn实现

```python
from sklearn.svm import OneClassSVM

ocsvm = OneClassSVM(kernel='rbf', nu=0.1)
y_pred = ocsvm.fit_predict(X)
```

## 7. 基于重构的方法

### 7.1 Autoencoder

**原理**：
1. 训练自编码器重构正常数据
2. 正常数据重构误差小
3. 异常数据重构误差大

**步骤**：
1. 只用正常数据训练AE
2. 计算重构误差
3. 误差超过阈值的为异常

## 8. 方法对比

| 方法             | 复杂度     | 优点         | 缺点           |
|------------------|------------|--------------|----------------|
| Z-score          | O(n)       | 简单快速     | 仅适合正态分布 |
| IQR              | O(n log n) | 鲁棒         | 单变量         |
| LOF              | O(n²)      | 检测局部异常 | 计算慢         |
| Isolation Forest | O(n)       | 高效、可扩展 | 随机性         |
| One-Class SVM    | O(n²~n³)   | 效果好       | 参数敏感       |
| Autoencoder      | O(n)       | 非线性       | 需要大量数据   |

## 9. 评估指标

### 9.1 有标签评估

- **Precision**: 检测出的异常中真正的异常比例
- **Recall**: 真实异常被检测出的比例
- **F1-Score**: Precision和Recall的调和平均

### 9.2 无标签评估

- **轮廓系数**：聚类质量
- **可视化检查**：2D/3D可视化

## 10. 参数选择

### contamination参数

表示数据集中异常点的预期比例：
- 已知比例：直接设置
- 未知：可从0.01开始尝试

### n_neighbors (LOF)

- 通常取10-50
- 太小：对噪声敏感
- 太大：可能漏掉局部异常

## 11. 应用场景

- **金融**：信用卡欺诈检测
- **网络安全**：入侵检测
- **工业**：设备故障预测
- **医疗**：疾病诊断
- **日志分析**：异常日志检测

## 12. 示例代码

见 `demo.py` 文件，包含：
- 统计方法（Z-score、IQR）
- LOF异常检测
- Isolation Forest
- One-Class SVM
- 方法对比

## 13. 参考资料

- Liu, F. T., et al. (2008). Isolation Forest
- Breunig, M. M., et al. (2000). LOF: Identifying Density-Based Local Outliers
- Schölkopf, B., et al. (2001). Estimating the Support of a High-Dimensional Distribution
- scikit-learn异常检测: https://scikit-learn.org/stable/modules/outlier_detection.html
