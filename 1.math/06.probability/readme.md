# 概率论与数理统计（Probability & Statistics）

研究随机现象规律性的学科。**理论根基是分析学（测度论），传统上归属于应用数学。**

## 子学科

| 学科         | 英文名                   | 核心内容                                  | 难度  |
|--------------|--------------------------|-------------------------------------------|-------|
| 概率论基础   | Probability Theory       | 公理化体系、随机变量、概率分布、极限定理  | ★★★☆☆ |
| 数理统计     | Mathematical Statistics  | 参数估计、假设检验、回归分析、方差分析    | ★★★☆☆ |
| 随机过程     | Stochastic Processes     | Markov链、Poisson过程、Brown运动、鞅论    | ★★★★☆ |
| 贝叶斯统计   | Bayesian Statistics      | 先验分布、后验推断、MCMC采样              | ★★★★☆ |
| 随机分析     | Stochastic Analysis      | Itô积分、随机微分方程(SDE)、Malliavin变分 | ★★★★★ |
| 时间序列分析 | Time Series Analysis     | ARIMA模型、状态空间模型、谱分析           | ★★★★☆ |
| 非参数统计   | Nonparametric Statistics | 核密度估计、秩检验、经验过程              | ★★★★☆ |

## 适用场景

数据分析、机器学习、金融风控、通信系统、质量控制。

## 核心公式

- Bayes公式：$P(A_i | B) = \frac{P(B | A_i) P(A_i)}{\sum_{j} P(B | A_j) P(A_j)}$
- 中心极限定理：$\frac{\bar{X}_n - \mu}{\sigma / \sqrt{n}} \xrightarrow{d} N(0,1)$
- Itô引理：$df(X_t) = f'(X_t) \, dX_t + \frac{1}{2}f''(X_t) \, d\langle X \rangle_t$

## 参考教材

- 《Probability: Theory and Examples》 — Durrett
- 《Statistical Inference》 — Casella & Berger
