# 计算数学（Computational Mathematics）

研究用计算机求解数学问题的数值方法及其理论分析。

## 子学科

| 学科         | 英文名                     | 核心内容                                          | 难度  |
|--------------|----------------------------|---------------------------------------------------|-------|
| 数值分析     | Numerical Analysis         | 误差分析、插值、数值积分、数值微分                | ★★★☆☆ |
| 数值线性代数 | Numerical Linear Algebra   | 直接法(LU/Cholesky)、迭代法(CG/GMRES)、特征值算法 | ★★★☆☆ |
| 数值优化     | Numerical Optimization     | 梯度下降、牛顿法、凸优化、线性规划、约束优化      | ★★★★☆ |
| 蒙特卡洛方法 | Monte Carlo Methods        | 随机采样、重要性采样、MCMC、方差缩减技术          | ★★★☆☆ |
| 有限元方法   | Finite Element Method      | 变分形式、网格离散、误差估计、自适应方法          | ★★★★☆ |
| 高性能计算   | High Performance Computing | 并行算法、GPU计算、分布式计算                     | ★★★★☆ |

## 适用场景

科学计算、工程仿真、深度学习训练、金融衍生品定价。

## 核心公式

- Newton迭代法：$x_{k+1} = x_k - [f'(x_k)]^{-1} f(x_k)$
- 梯形法则：$\int_a^b f(x) \, dx \approx \frac{h}{2}\left[f(a) + 2\sum_{i=1}^{n-1}f(x_i) + f(b)\right]$
- KKT条件（约束优化）：$\nabla f(x^*) + \sum_i \lambda_i \nabla g_i(x^*) + \sum_j \mu_j \nabla h_j(x^*) = 0$

## 参考教材

- 《Numerical Analysis》 — Burden & Faires
- 《Convex Optimization》 — Boyd & Vandenberghe
