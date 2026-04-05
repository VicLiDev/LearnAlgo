# 概率论（Probability Theory）

难度：★★★☆☆

概率论是研究随机现象数量规律的数学分支，是统计学、机器学习、信息论、金融数学等领域的基础。本教程按照从公理化基础到高级专题的逻辑结构，系统覆盖了测度论框架下的现代概率论核心内容。

---

## 目录

| 章节 | 标题 | 核心内容 |
|:----:|------|----------|
| [第一章](./01.probability_spaces/readme.md) | 概率空间 | 样本空间与事件、Kolmogorov 公理、概率的基本性质（推导）、条件概率与 Bayes 公式（推导）、独立性、Borel-Cantelli 引理 |
| [第二章](./02.random_variables/readme.md) | 随机变量及其分布 | 随机变量的定义、分布函数及其性质、离散型（PMF）、连续型（PDF）、随机变量函数的分布、多维随机变量、联合分布与边缘分布 |
| [第三章](./03.numerical_characteristics/readme.md) | 数字特征 | 数学期望（定义、性质、推导）、方差（定义、性质、推导）、协方差与相关系数（Cauchy-Schwarz 不等式推导）、矩、协方差矩阵、Jensen 不等式（证明） |
| [第四章](./04.common_distributions/readme.md) | 常见概率分布 | 离散型（Bernoulli、二项、Poisson、几何、负二项、超几何）、连续型（均匀、指数、正态、Gamma、Beta、$\chi^2$、$t$、$F$）、分布间关系图、特征化（无记忆性等） |
| [第五章](./05.characteristic_functions/readme.md) | 特征函数与矩母函数 | 特征函数的定义与性质（证明）、矩母函数、特征函数与分布的一一对应（逆转公式）、特征函数与矩的关系、多维特征函数、求和分布判定 |
| [第六章](./06.limit_theorems/readme.md) | 极限定理 | Markov/Chebyshev 不等式（证明）、弱/强大数定律（Khinchin/Kolmogorov）、Lindeberg-Levy CLT（证明）、Lindeberg-Feller CLT、De Moivre-Laplace 定理、大偏差初步 |
| [第七章](./07.multivariate_variables/readme.md) | 多维随机变量 | 多维随机向量的联合分布、边缘分布、条件分布、多维正态分布（定义、性质、推导）、独立性判定、协方差矩阵性质、雅可比行列式变换法 |
| [第八章](./08.conditional_expectation/readme.md) | 条件期望 | 条件期望的定义（离散与连续）、全期望公式（推导）、条件期望的几何意义（正交投影）、鞅的初步概念、条件方差的方差分解公式（ANOVA） |

---

## 依赖关系图

各章节之间存在如下依赖关系（箭头表示"依赖于"）：

```
                    第一章：概率空间
                   /        |        \
                  v         v         v
    第二章：随机变量    第三章：数字特征
         |        \       /    |
         |         v     v     |
         |   第四章：常见分布  |
         |         |          |
         v         v          v
    第五章：特征函数 ──> 第六章：极限定理
                            |
                            v
              第七章：多维随机变量
                     |
                     v
              第八章：条件期望
```

**建议学习路径**：

1. **基础路径**（必须按顺序学习）：第一章 -> 第二章 -> 第三章 -> 第四章
2. **进阶路径**：第五章 -> 第六章（需要前三章基础）
3. **高级路径**：第七章 -> 第八章（需要前六章基础）

---

## 参考书目

### 经典教材

| 书名 | 作者 | 特点 |
|------|------|------|
| *Probability: Theory and Examples* (5th Ed.) | Rick Durrett | 现代测度论框架，内容深入全面，适合进阶学习 |
| *Probability and Measure* (3rd Ed.) | Patrick Billingsley | 经典教材，测度论与概率论结合紧密，论述严谨优美 |
| *Real Analysis and Probability* | R. M. Dudley | 实分析与概率论的统一处理，数学要求高 |
| *A Probability Path* | Sidney Resnick | 从实分析过渡到概率论，适合自学，难度适中 |
| *概率论基础* (第3版) | 李贤平 | 中文经典教材，体系完整，适合中文读者入门 |

### 参考与补充

| 书名 | 作者 | 特点 |
|------|------|------|
| *An Introduction to Probability Theory and Its Applications* (Vol. 1 & 2) | William Feller | 经典中的经典，Vol.1 为离散概率，Vol.2 为连续概率，内容丰富 |
| *Probability Theory: The Logic of Science* | E. T. Jaynes | 贝叶斯学派视角，强调概率的逻辑推断解释 |
| *All of Statistics: A Concise Course in Statistical Inference* | Larry Wasserman | 统计推断的简明教程，适合需要快速了解统计的读者 |
| *概率论与数理统计* (第4版) | 浙江大学 盛骤 等 | 国内广泛使用的教材，适合考试复习 |
| *随机过程* (第2版) | 何书元 | 国内随机过程教材，涵盖 Markov 链、Poisson 过程等 |
| *Convergence of Probability Measures* (2nd Ed.) | Patrick Billingsley | 弱收敛理论专著，深入研究极限定理 |

### 在线资源

- [Probability Theory (Stanford, STATS 310)](https://statweb.stanford.edu/~adembo/stat-310b/) -- Stanford 大学概率论课程
- [MIT 18.445 Probability Theory](https://ocw.mit.edu/courses/18-445-probability-theory-fall-2022/) -- MIT 概率论课程

---

## 数学预备知识

学习本教程需要以下数学基础：

- **实分析**：Lebesgue 测度与积分、单调收敛定理、控制收敛定理、Fatou 引理
- **线性代数**：矩阵运算、特征值与特征向量、正定矩阵
- **微积分**：多元微积分、Taylor 展开、分部积分
- **基础概率与统计**：基本概率计算、常见分布

---

## 符号约定

| 符号 | 含义 |
|------|------|
| $(\Omega, \mathcal{F}, P)$ | 概率空间 |
| $\mathcal{B}(\mathbb{R})$ | Borel $\sigma$-代数 |
| $F(x)$ | 累积分布函数 (CDF) |
| $f(x)$ | 概率密度函数 (PDF) |
| $p(x)$ | 概率质量函数 (PMF) |
| $E[X]$ | 数学期望 |
| $\mathrm{Var}(X)$ | 方差 |
| $\mathrm{Cov}(X, Y)$ | 协方差 |
| $\rho(X, Y)$ | 相关系数 |
| $\varphi_X(t)$ | 特征函数 |
| $M_X(t)$ | 矩母函数 |
| $\boldsymbol{\Sigma}$ | 协方差矩阵 |
| $\xrightarrow{P}$ | 依概率收敛 |
| $\xrightarrow{\text{a.s.}}$ | 几乎必然收敛 |
| $\xrightarrow{d}$ | 依分布收敛 |
| $\xrightarrow{L^2}$ | 均方收敛 |
| $\blacksquare$ | 证明结束 |
