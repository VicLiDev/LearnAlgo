# 离散数学与组合学（Discrete Mathematics & Combinatorics）

研究离散、可数结构的学科，是计算机科学的理论基础。

## 子学科

| 学科       | 英文名                    | 核心内容                                                 | 难度  |
|------------|---------------------------|----------------------------------------------------------|-------|
| 集合论     | Set Theory                | 集合运算、势(Cardinality)、ZFC公理系统                   | ★★☆☆☆ |
| 逻辑学     | Mathematical Logic        | 命题逻辑、一阶逻辑、可计算性、Gödel不完备定理            | ★★★☆☆ |
| 图论       | Graph Theory              | 图、树、网络流、匹配、着色、图着色定理                   | ★★★☆☆ |
| 组合计数   | Enumerative Combinatorics | 排列组合、生成函数、容斥原理、Polya计数                  | ★★★☆☆ |
| 组合设计   | Combinatorial Design      | 拉丁方、区组设计、Steiner系统                            | ★★★★☆ |
| Ramsey理论 | Ramsey Theory             | 组合结构的存在性、Ramsey数                               | ★★★★☆ |
| 矩阵论     | Matrix Theory             | 矩阵分解、广义逆、矩阵函数、矩阵分析（线性代数高阶延伸） | ★★★★☆ |

> **关于矩阵论**：矩阵论是线性代数的高阶延伸，严格归类属于代数学分支，同时与泛函分析和数值分析深度交叉，在机器学习、图像处理、控制论等领域有广泛应用。

## 适用场景

算法设计、数据库理论、编译原理、网络路由、密码学。

## 核心公式

- Catalan数：$C_n = \frac{1}{n+1}\binom{2n}{n}$
- 容斥原理：$|\bigcup_{i=1}^n A_i| = \sum_i |A_i| - \sum_{i<j}|A_i \cap A_j| + \cdots + (-1)^{n+1}|\bigcap_{i=1}^n A_i|$
- Turán定理（极值图论）：$\text{ex}(n, K_{r+1}) \leq \left(1 - \frac{1}{r}\right)\frac{n^2}{2}$
