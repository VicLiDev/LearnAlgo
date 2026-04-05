# 数学（Mathematics）

数学是研究数量、结构、空间、变化等概念的形式科学，是一切自然科学与工程技术的
理论基础。本文档对数学的主要分支进行系统性梳理。

---

## 目录结构

```
1.math
├── readme.md                           # 本文档
├── 01.algebra/                         # 代数学
│   ├── 01.elementary_algebra/          # 初等代数
│   ├── 02.linear_algebra/              # 线性代数
│   ├── 03.advanced_algebra/            # 高等代数
│   ├── 04.abstract_algebra/            # 抽象代数
│   ├── 05.commutative_algebra/         # 交换代数
│   ├── 06.lie_algebra/                 # 李代数
│   └── 07.homological_algebra/         # 同调代数
├── 02.analysis/                        # 分析学
│   ├── 01.calculus/                    # 微积分
│   ├── 02.real_analysis/               # 实分析
│   ├── 03.complex_analysis/            # 复分析
│   ├── 04.functional_analysis/         # 泛函分析
│   ├── 05.harmonic_analysis/           # 调和分析
│   ├── 06.differential_equations/      # 微分方程
│   └── 07.calculus_of_variations/      # 变分法
├── 03.geometry/                        # 几何学
│   ├── 01.euclidean_geometry/          # 欧几里得几何
│   ├── 02.analytic_geometry/           # 解析几何
│   ├── 03.projective_geometry/         # 射影几何
│   ├── 04.differential_geometry/       # 微分几何
│   ├── 05.algebraic_geometry/          # 代数几何
│   ├── 06.computational_geometry/      # 计算几何
│   └── 07.topology/                    # 拓扑学
├── 04.number_theory/                   # 数论
│   ├── 01.elementary_number_theory/    # 初等数论
│   ├── 02.analytic_number_theory/      # 解析数论
│   ├── 03.algebraic_number_theory/     # 代数数论
│   ├── 04.computational_number_theory/ # 计算数论
│   └── 05.transcendental_number_theory/# 超越数论
├── 05.discrete_math/                   # 离散数学与组合学
│   ├── 01.set_theory/                  # 集合论
│   ├── 02.mathematical_logic/          # 逻辑学
│   ├── 03.graph_theory/                # 图论
│   ├── 04.enumerative_combinatorics/   # 组合计数
│   ├── 05.combinatorial_design/        # 组合设计
│   ├── 06.ramsey_theory/               # Ramsey理论
│   └── 07.matrix_theory/               # 矩阵论
├── 06.probability/                     # 概率论与数理统计
│   ├── 01.probability_theory/          # 概率论基础
│   ├── 02.mathematical_statistics/     # 数理统计
│   ├── 03.stochastic_processes/        # 随机过程
│   ├── 04.bayesian_statistics/         # 贝叶斯统计
│   ├── 05.stochastic_analysis/         # 随机分析
│   ├── 06.time_series_analysis/        # 时间序列分析
│   └── 07.nonparametric_statistics/    # 非参数统计
├── 07.computational_math/              # 计算数学
│   ├── 01.numerical_analysis/          # 数值分析
│   ├── 02.numerical_linear_algebra/    # 数值线性代数
│   ├── 03.numerical_optimization/      # 数值优化
│   ├── 04.monte_carlo_methods/         # 蒙特卡洛方法
│   ├── 05.finite_element_method/       # 有限元方法
│   └── 06.high_performance_computing/  # 高性能计算
├── 08.math_physics/                    # 数学物理方法
│   ├── 01.equations_of_math_physics/   # 数学物理方程
│   ├── 02.classical_mechanics/         # 经典力学
│   ├── 03.math_foundations_of_qm/      # 量子力学数学基础
│   ├── 04.statistical_mechanics/       # 统计力学
│   └── 05.general_relativity/          # 广义相对论
└── 09.operations_research/             # 运筹学与控制论
    ├── 01.linear_programming/          # 线性规划
    ├── 02.nonlinear_programming/       # 非线性规划
    ├── 03.dynamic_programming/         # 动态规划
    ├── 04.game_theory/                 # 博弈论
    ├── 05.queueing_theory/             # 排队论
    ├── 06.control_theory/              # 控制理论
    └── 07.optimal_control/             # 最优控制
```

---

## 一、代数学（Algebra）

研究数学符号及其运算规则的学科，核心对象是**代数结构**（群、环、域、向量空间等）。

| 学科     | 英文名              | 核心内容                                       | 难度  |
|----------|---------------------|------------------------------------------------|-------|
| 初等代数 | Elementary Algebra  | 多项式、方程求根、因式分解、不等式             | ★☆☆☆☆ |
| 线性代数 | Linear Algebra      | 向量空间、矩阵运算、线性变换、特征值与特征向量 | ★★☆☆☆ |
| 高等代数 | Advanced Algebra    | 线性代数的深化，二次型、Jordan标准型           | ★★★☆☆ |
| 抽象代数 | Abstract Algebra    | 群论、环论、域论、伽罗瓦理论                   | ★★★★☆ |
| 交换代数 | Commutative Algebra | 交换环、理想、Noether环、局部化                | ★★★★★ |
| 李代数   | Lie Algebra         | 李括号、表示论、半单纯李代数分类               | ★★★★★ |
| 同调代数 | Homological Algebra | 范畴、函子、正合列、导出函子                   | ★★★★★ |

**适用场景**：线性方程组求解、特征值分解、编码理论、密码学、量子力学。

**核心公式**：

- 特征方程：$\det(A - \lambda I) = 0$
- Cayley-Hamilton定理：$p(A) = 0$，其中 $p(\lambda)$ 为 $A$ 的特征多项式
- 群的同态基本定理：$G / \ker(\varphi) \cong \text{im}(\varphi)$

---

## 二、分析学（Analysis）

以极限、连续、微分、积分、收敛为核心概念的学科，是微积分的延伸与深化。

| 学科     | 英文名                 | 核心内容                                     | 难度  |
|----------|------------------------|----------------------------------------------|-------|
| 微积分   | Calculus               | 极限、导数、积分、级数                       | ★☆☆☆☆ |
| 实分析   | Real Analysis          | 实数完备性、测度论、Lebesgue积分、收敛性     | ★★★★☆ |
| 复分析   | Complex Analysis       | 复变函数、解析函数、Cauchy积分定理、留数定理 | ★★★★☆ |
| 泛函分析 | Functional Analysis    | 赋范空间、Banach空间、Hilbert空间、算子理论  | ★★★★★ |
| 调和分析 | Harmonic Analysis      | Fourier级数、Fourier变换、小波分析           | ★★★★☆ |
| 微分方程 | Differential Equations | 常微分方程(ODE)、偏微分方程(PDE)、稳定性理论 | ★★★☆☆ |
| 变分法   | Calculus of Variations | 泛函极值、Euler-Lagrange方程、最速降线       | ★★★★☆ |

**适用场景**：信号处理（Fourier变换）、物理场建模（PDE）、最优化理论、量子力学算子。

**核心公式**：

- Fourier变换：$\hat{f}(\xi) = \int_{-\infty}^{+\infty} f(x) e^{-2\pi i x \xi} \, dx$
- Cauchy积分公式：$f(z_0) = \frac{1}{2\pi i} \oint_\gamma \frac{f(z)}{z - z_0} \, dz$
- Euler-Lagrange方程：$\frac{\partial L}{\partial q} - \frac{d}{dt}\frac{\partial L}{\partial \dot{q}} = 0$

---

## 三、几何学（Geometry）

研究空间形状、大小、位置关系以及空间变换的学科。

| 学科         | 英文名                | 核心内容                                     | 难度  |
|--------------|-----------------------|----------------------------------------------|-------|
| 欧几里得几何 | Euclidean Geometry    | 平面几何、立体几何、公理化体系               | ★☆☆☆☆ |
| 解析几何     | Analytic Geometry     | 坐标系、曲线方程、曲面方程                   | ★★☆☆☆ |
| 射影几何     | Projective Geometry   | 透视变换、齐次坐标、交比不变量               | ★★★☆☆ |
| 微分几何     | Differential Geometry | 曲线与曲面、流形、Riemann度量、曲率张量      | ★★★★★ |
| 代数几何     | Algebraic Geometry | 代数簇、概形(Scheme)、层(Sheaf)、上同调         | ★★★★★ |
| 计算几何     | Computational Geometry | 凸包、Voronoi图、Delaunay三角剖分、网格生成 | ★★★☆☆ |
| 拓扑学       | Topology | 拓扑空间、同伦、同调、基本群、纽结理论                    | ★★★★☆ |

**适用场景**：计算机图形学、机器人运动规划、广义相对论、弦理论、CAD/CAE。

**核心公式**：

- Gauss曲率：$K = \frac{eg - f^2}{EG - F^2}$（第一基本形式与第二基本形式）
- Euler示性数：$\chi = V - E + F = 2 - 2g$（$g$ 为亏格）
- Gauss-Bonnet定理：$\int_M K \, dA + \int_{\partial M} \kappa_g \, ds = 2\pi\chi(M)$

---

## 四、数论（Number Theory）

研究整数性质与规律的学科，被誉为"数学女王"。

| 学科     | 英文名                       | 核心内容                                            | 难度  |
|----------|------------------------------|-----------------------------------------------------|-------|
| 初等数论 | Elementary Number Theory     | 整除性、素数、同余、中国剩余定理                    | ★★☆☆☆ |
| 解析数论 | Analytic Number Theory       | Riemann Zeta函数、素数定理、Dirichlet级数           | ★★★★★ |
| 代数数论 | Algebraic Number Theory      | 数域、代数整数、理想、类域论                        | ★★★★★ |
| 计算数论 | Computational Number Theory  | 素性测试、大数分解、离散对数                        | ★★★★☆ |
| 超越数论 | Transcendental Number Theory | 超越性证明（$e$, $\pi$）、Lindemann-Weierstrass定理 | ★★★★★ |

**适用场景**：RSA密码学、哈希函数、伪随机数生成、编码理论。

**核心公式**：

- Euler函数：$\varphi(n) = n \prod_{p|n}(1 - \frac{1}{p})$
- Fermat小定理：$a^{p-1} \equiv 1 \pmod{p}$（$p$ 为素数，$\gcd(a,p)=1$）
- 二次互反律（Legendre符号）：$\left(\frac{p}{q}\right)\left(\frac{q}{p}\right) = (-1)^{\frac{(p-1)(q-1)}{4}}$

---

## 五、离散数学与组合学（Discrete Mathematics & Combinatorics）

研究离散、可数结构的学科，是计算机科学的理论基础。

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

**适用场景**：算法设计、数据库理论、编译原理、网络路由、密码学。

**核心公式**：
- Catalan数：$C_n = \frac{1}{n+1}\binom{2n}{n}$
- 容斥原理：$|\bigcup_{i=1}^n A_i| = \sum_i |A_i| - \sum_{i<j}|A_i \cap A_j| + \cdots + (-1)^{n+1}|\bigcap_{i=1}^n A_i|$
- Turán定理（极值图论）：$\text{ex}(n, K_{r+1}) \leq \left(1 - \frac{1}{r}\right)\frac{n^2}{2}$

---

## 六、概率论与数理统计（Probability & Statistics）

研究随机现象规律性的学科。**理论根基是分析学（测度论），传统上归属于应用数学。**

| 学科         | 英文名                   | 核心内容                                  | 难度  |
|--------------|--------------------------|-------------------------------------------|-------|
| 概率论基础   | Probability Theory       | 公理化体系、随机变量、概率分布、极限定理  | ★★★☆☆ |
| 数理统计     | Mathematical Statistics  | 参数估计、假设检验、回归分析、方差分析    | ★★★☆☆ |
| 随机过程     | Stochastic Processes     | Markov链、Poisson过程、Brown运动、鞅论    | ★★★★☆ |
| 贝叶斯统计   | Bayesian Statistics      | 先验分布、后验推断、MCMC采样              | ★★★★☆ |
| 随机分析     | Stochastic Analysis      | Itô积分、随机微分方程(SDE)、Malliavin变分 | ★★★★★ |
| 时间序列分析 | Time Series Analysis     | ARIMA模型、状态空间模型、谱分析           | ★★★★☆ |
| 非参数统计   | Nonparametric Statistics | 核密度估计、秩检验、经验过程              | ★★★★☆ |

**适用场景**：数据分析、机器学习、金融风控、通信系统、质量控制。

**核心公式**：

- Bayes公式：$P(A_i | B) = \frac{P(B | A_i) P(A_i)}{\sum_{j} P(B | A_j) P(A_j)}$
- 中心极限定理：$\frac{\bar{X}_n - \mu}{\sigma / \sqrt{n}} \xrightarrow{d} N(0,1)$
- Itô引理：$df(X_t) = f'(X_t) \, dX_t + \frac{1}{2}f''(X_t) \, d\langle X \rangle_t$

---

## 七、计算数学（Computational Mathematics）

研究用计算机求解数学问题的数值方法及其理论分析。

| 学科         | 英文名                     | 核心内容                                          | 难度  |
|--------------|----------------------------|---------------------------------------------------|-------|
| 数值分析     | Numerical Analysis         | 误差分析、插值、数值积分、数值微分                | ★★★☆☆ |
| 数值线性代数 | Numerical Linear Algebra   | 直接法(LU/Cholesky)、迭代法(CG/GMRES)、特征值算法 | ★★★☆☆ |
| 数值优化     | Numerical Optimization     | 梯度下降、牛顿法、凸优化、线性规划、约束优化      | ★★★★☆ |
| 蒙特卡洛方法 | Monte Carlo Methods        | 随机采样、重要性采样、MCMC、方差缩减技术          | ★★★☆☆ |
| 有限元方法   | Finite Element Method      | 变分形式、网格离散、误差估计、自适应方法          | ★★★★☆ |
| 高性能计算   | High Performance Computing | 并行算法、GPU计算、分布式计算                     | ★★★★☆ |

**适用场景**：科学计算、工程仿真、深度学习训练、金融衍生品定价。

**核心公式**：

- Newton迭代法：$x_{k+1} = x_k - [f'(x_k)]^{-1} f(x_k)$
-梯形法则：$\int_a^b f(x) \, dx \approx \frac{h}{2}\left[f(a) + 2\sum_{i=1}^{n-1}f(x_i) + f(b)\right]$
- KKT条件（约束优化）：$\nabla f(x^*) + \sum_i \lambda_i \nabla g_i(x^*) + \sum_j \mu_j \nabla h_j(x^*) = 0$

---

## 八、数学物理方法（Mathematical Methods in Physics）

为物理学提供数学框架和方法论的交叉学科。

| 学科             | 英文名                     | 核心内容                                          | 难度  |
|------------------|----------------------------|---------------------------------------------------|-------|
| 数学物理方程     | Equations of Math. Physics | 波动方程、热传导方程、Laplace方程、Green函数      | ★★★★☆ |
| 经典力学         | Classical Mechanics        | Lagrange力学、Hamilton力学、正则变换、Noether定理 | ★★★☆☆ |
| 量子力学数学基础 | Math. Foundations of QM    | Hilbert空间、算子谱论、自伴算子、散射理论         | ★★★★★ |
| 统计力学         | Statistical Mechanics      | 系综理论、遍历定理、相变、Ising模型               | ★★★★☆ |
| 广义相对论       | General Relativity         | Riemann几何、Einstein场方程、测地线、引力波       | ★★★★★ |

**适用场景**：理论物理、天体物理、凝聚态物理、量子信息。

**核心公式**：

- Schrödinger方程：$i\hbar \frac{\partial}{\partial t}|\psi\rangle = \hat{H}|\psi\rangle$
- Einstein场方程：$R_{\mu\nu} - \frac{1}{2}Rg_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4}T_{\mu\nu}$
- Boltzmann分布：$P(E) = \frac{1}{Z} e^{-E / k_B T}$

---

## 九、运筹学与控制论（Operations Research & Control Theory）

运用数学模型对系统进行优化决策的学科。

| 学科       | 英文名                | 核心内容                                          | 难度  |
|------------|-----------------------|---------------------------------------------------|-------|
| 线性规划   | Linear Programming    | 单纯形法、对偶理论、内点法                        | ★★★☆☆ |
| 非线性规划 | Nonlinear Programming | KKT条件、罚函数法、序列二次规划(SQP)              | ★★★★☆ |
| 动态规划   | Dynamic Programming   | Bellman方程、最优性原理、策略迭代                 | ★★★☆☆ |
| 博弈论     | Game Theory           | 纳什均衡、零和博弈、合作博弈、机制设计            | ★★★☆☆ |
| 排队论     | Queueing Theory       | M/M/1模型、Little公式、排队网络                   | ★★★☆☆ |
| 控制理论   | Control Theory        | 状态空间、能控性/能观性、PID、LQR、$H_\infty$控制 | ★★★★☆ |
| 最优控制   | Optimal Control       | Pontryagin极大值原理、动态规划法、轨迹优化        | ★★★★★ |

**适用场景**：供应链优化、资源调度、自动驾驶控制、机器人规划、经济模型。

**核心公式**：

- Bellman方程：$V(s) = \max_a \left[ R(s,a) + \gamma \sum_{s'} P(s'|s,a) V(s') \right]$
- LQR最优控制：$u = -Kx$，其中 $K = R^{-1}B^T P$，$P$ 为Riccati方程的解
- Little定律：$L = \lambda W$（系统平均顾客数 = 到达率 × 平均等待时间）

---

## 各领域关系总览

```
                         ┌─────────────┐
                         │   范畴论    │  ← 数学各分支的统一语言
                         └──────┬──────┘
                                │
            ┌───────────────────┼────────────────────┐
            │                   │                    │
     ┌──────┴──────┐     ┌──────┴──────┐      ┌──────┴──────┐
     │   代数学    │     │   分析学    │      │   几何学    │
     │ Algebra     │     │ Analysis    │      │ Geometry    │
     └──────┬──────┘     └──────┬──────┘      └──────┬──────┘
            │                   │                    │
     ┌──────┴──────┐     ┌──────┴──────┐      ┌──────┴──────┐
     │ • 线性代数  │     │ • 实分析    │      │ • 微分几何  │
     │ • 抽象代数  │     │ • 复分析    │      │ • 代数几何  │
     │ • 矩阵论    │     │ • 泛函分析  │      │ • 拓扑学    │
     │ • 数论      │     │ • 微分方程  │      │ • 计算几何  │
     └──────┬──────┘     └──────┬──────┘      └──────┴──────┘
            │                   │                    │
            └───────────┬───────┴───────┬────────────┘
                        │               │
              ┌─────────┴───┐    ┌──────┴──────┐
              │  应用数学   │    │  交叉学科   │
              ├─────────────┤    ├─────────────┤
              │ • 概率论    │    │ • 数学物理  │
              │ • 数理统计  │    │ • 运筹学    │
              │ • 计算数学  │    │ • 控制论    │
              │ • 密码学    │    │ • 信息论    │
              │ • 金融数学  │    │ • 博弈论    │
              └─────────────┘    └─────────────┘
```

---

## 与算法学习的关系

本项目中，数学知识的应用贯穿始终：

| 项目目录         | 依赖的核心数学                            |
|------------------|-------------------------------------------|
| `2.BasicAlgo`    | 离散数学、图论、组合计数                  |
| `3.GenAlgorithm` | 线性代数、数值分析、微分方程、Fourier分析 |
| `4.Classical`    | 线性代数、概率论、优化理论、微分几何      |
| `5.ML`           | 线性代数、概率论与统计、优化理论、信息论  |
| `6.DL`           | 线性代数、微积分、概率论、优化理论        |
| `7.Vcodec`       | 概率论、信息论、线性代数、变换理论        |

---

## 参考教材

| 学科     | 经典教材                                                    |
|----------|-------------------------------------------------------------|
| 线性代数 | 《Linear Algebra Done Right》 — Sheldon Axler               |
| 实分析   | 《Real Analysis》 — Royden                                  |
| 复分析   | 《Complex Analysis》 — Ahlfors                              |
| 抽象代数 | 《Algebra》 — Serge Lang                                    |
| 概率论   | 《Probability: Theory and Examples》 — Durrett              |
| 数理统计 | 《Statistical Inference》 — Casella & Berger                |
| 数值分析 | 《Numerical Analysis》 — Burden & Faires                    |
| 微分几何 | 《Differential Geometry of Curves and Surfaces》 — do Carmo |
| 拓扑学   | 《Topology》 — Munkres                                      |
| 凸优化   | 《Convex Optimization》 — Boyd & Vandenberghe               |
