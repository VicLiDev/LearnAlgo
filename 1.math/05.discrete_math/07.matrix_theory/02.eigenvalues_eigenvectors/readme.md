# 第二章 特征值与特征向量

## 1. 几何意义

特征值与特征向量刻画了矩阵变换中**不变的方向**。

**核心直觉**：对于方阵 $A$，若存在非零向量 $v$ 和标量 $\lambda$，使得

$$Av = \lambda v$$

则 $v$ 是 $A$ 的一个**特征向量**，$\lambda$ 是对应的**特征值**。

几何含义：向量 $v$ 在经过变换 $A$ 之后，方向不变（或反向），只是长度缩放了 $\lambda$ 倍。

- $|\lambda| > 1$：该方向被拉伸
- $|\lambda| < 1$：该方向被压缩
- $\lambda < 0$：该方向被翻转
- $\lambda = 0$：该方向被压扁到零（对应零空间）
- $\lambda$ 为复数：变换中包含旋转分量

**几何图像（2D）**：

设 $A = \begin{pmatrix} 3 & 1 \\ 0 & 2 \end{pmatrix}$，特征值为 $\lambda_1 = 3, \lambda_2 = 2$，对应特征向量为 $v_1 = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$ 和 $v_2 = \begin{pmatrix} 1 \\ -1 \end{pmatrix}$。

该变换将平面沿 $v_1$ 方向拉伸 3 倍，沿 $v_2$ 方向拉伸 2 倍。整个变换的效果可以理解为：先旋转到特征向量坐标系，沿各轴缩放，再旋转回来。

---

## 2. 应用场景

| 领域 | 应用 |
|------|------|
| 主成分分析（PCA） | 协方差矩阵的特征向量即为数据的主方向，特征值表示方差大小 |
| 振动分析 | 结构的固有频率和振型即为刚度矩阵的特征值和特征向量 |
| 马尔可夫链 | 转移矩阵的特征值 1 对应的特征向量为平稳分布 |
| 图论 | 图的邻接矩阵的最大特征值用于分析网络连通性 |
| 量子力学 | 算子的特征值即为可观测量的可能测量值 |
| 页面排名（PageRank） | 网络链接矩阵的主特征向量即为网页重要性排序 |
| 控制理论 | 系统矩阵的特征值决定系统的稳定性（实部 $< 0$ 则稳定） |

---

## 3. 数学理论

### 3.1 定义与特征方程

**定义**：设 $A \in \mathbb{C}^{n \times n}$，若存在 $\lambda \in \mathbb{C}$ 和非零 $x \in \mathbb{C}^n$，使得 $Ax = \lambda x$，则 $\lambda$ 为 $A$ 的特征值，$x$ 为对应于 $\lambda$ 的特征向量。

**特征方程**：$Ax = \lambda x \iff (A - \lambda I)x = 0$，有非零解的充要条件为

$$\det(A - \lambda I) = 0$$

这称为 $A$ 的**特征方程**（Characteristic Equation），其左端展开后得到 $A$ 的**特征多项式**：

$$p(\lambda) = \det(A - \lambda I) = \lambda^n + c_{n-1}\lambda^{n-1} + \cdots + c_1 \lambda + c_0$$

### 3.2 特征多项式的系数

特征多项式可表示为：

$$p(\lambda) = \det(\lambda I - A) = \lambda^n - \text{tr}(A) \lambda^{n-1} + \cdots + (-1)^n \det(A)$$

即：
- $\lambda^{n-1}$ 的系数为 $-\text{tr}(A)$
- 常数项（$\lambda^0$）为 $(-1)^n \det(A)$

**推论**：
- 特征值之和 = 迹：$\sum_{i=1}^{n} \lambda_i = \text{tr}(A)$
- 特征值之积 = 行列式：$\prod_{i=1}^{n} \lambda_i = \det(A)$

**推导**（Vieta公式）：

由代数基本定理，特征多项式可分解为 $p(\lambda) = \prod_{i=1}^{n}(\lambda - \lambda_i)$，展开后用 Vieta 定理即得。

### 3.3 特征值的基本性质

**定理**：三角矩阵（上三角、下三角、对角矩阵）的特征值等于其主对角线元素。

**证明**：若 $A$ 为上三角矩阵，则 $A - \lambda I$ 也是上三角矩阵，其行列式等于对角元素之积：

$$\det(A - \lambda I) = \prod_{i=1}^{n}(a_{ii} - \lambda) = 0 \implies \lambda = a_{ii}$$

**相似不变性**：若 $B = P^{-1}AP$，则 $A$ 与 $B$ 有相同的特征值。

**证明**：

$$\det(B - \lambda I) = \det(P^{-1}AP - \lambda P^{-1}P) = \det(P^{-1}(A - \lambda I)P)$$
$$= \det(P^{-1}) \det(A - \lambda I) \det(P) = \det(A - \lambda I)$$

**Hamilton-Cayley 定理**：$n \times n$ 矩阵 $A$ 满足其自身的特征方程，即 $p(A) = 0$。

**证明思路**：考虑伴随矩阵 $\text{adj}(\lambda I - A)$，利用 $(\lambda I - A) \text{adj}(\lambda I - A) = \det(\lambda I - A) \cdot I = p(\lambda) I$，将 $\text{adj}(\lambda I - A)$ 展为 $\lambda$ 的多项式，代入 $\lambda = A$ 即可。

### 3.4 特征值的估计（Gershgorin圆盘定理）

**定理（Gershgorin圆盘定理）**：$A = (a_{ij})$ 的每个特征值至少位于一个 Gershgorin 圆盘内：

$$D_i = \left\{ z \in \mathbb{C} : |z - a_{ii}| \leq \sum_{j \neq i} |a_{ij}| \right\}, \quad i = 1, 2, \ldots, n$$

**推论**：若 $k$ 个圆盘与其他圆盘不相交，则这 $k$ 个圆盘的并集中恰好有 $k$ 个特征值。

**证明**：设 $\lambda$ 为特征值，$x$ 为对应特征向量。取 $x_p$ 为绝对值最大的分量，则 $(A - \lambda I)x = 0$ 的第 $p$ 行给出：

$$(a_{pp} - \lambda)x_p + \sum_{j \neq p} a_{pj} x_j = 0$$

$$|\lambda - a_{pp}| = \left|\sum_{j \neq p} a_{pj} \frac{x_j}{x_p}\right| \leq \sum_{j \neq p} |a_{pj}|$$

故 $\lambda \in D_p$。

### 3.5 对称矩阵的特征值

**定理**：实对称矩阵 $A = A^T$ 的特征值全为实数。

**证明**：设 $Ax = \lambda x$，$x \neq 0$。取共轭转置：$\overline{x}^T A = \overline{\lambda} \overline{x}^T$。

$$\overline{x}^T A x = \overline{x}^T (\lambda x) = \lambda \|\overline{x}\|^2$$

$$\overline{x}^T A x = (\overline{\lambda} \overline{x}^T) x = \overline{\lambda} \|\overline{x}\|^2$$

两式相减得 $(\lambda - \overline{\lambda})\|x\|^2 = 0$，故 $\lambda = \overline{\lambda} \in \mathbb{R}$。

**定理**：实对称矩阵的不同特征值对应的特征向量正交。

**证明**：设 $Ax = \lambda_1 x$，$Ay = \lambda_2 y$，$\lambda_1 \neq \lambda_2$。

$$\lambda_1 \langle x, y \rangle = \langle Ax, y \rangle = x^T A^T y = x^T A y = \lambda_2 \langle x, y \rangle$$

$$(\lambda_1 - \lambda_2)\langle x, y \rangle = 0 \implies \langle x, y \rangle = 0$$

### 3.6 Rayleigh商

**定义**：对于实对称矩阵 $A \in \mathbb{R}^{n \times n}$，Rayleigh商定义为

$$R(x) = \frac{x^T A x}{x^T x}, \quad x \neq 0$$

**性质**：
- Rayleigh商的取值范围在最小和最大特征值之间
- 当 $x$ 为特征向量时，$R(x) = \lambda$（对应的特征值）

**定理（Rayleigh-Ritz）**：设 $A$ 的特征值按序排列 $\lambda_1 \leq \lambda_2 \leq \cdots \leq \lambda_n$，则

$$\lambda_1 = \min_{x \neq 0} R(x), \quad \lambda_n = \max_{x \neq 0} R(x)$$

**证明**：由谱分解 $A = Q\Lambda Q^T$，令 $y = Q^T x$，则

$$R(x) = \frac{y^T \Lambda y}{y^T y} = \frac{\sum_i \lambda_i y_i^2}{\sum_i y_i^2}$$

由 $\lambda_1 \sum y_i^2 \leq \sum \lambda_i y_i^2 \leq \lambda_n \sum y_i^2$，得 $\lambda_1 \leq R(x) \leq \lambda_n$。

当 $x$ 取最小/最大特征值对应的特征向量时，等号成立。

### 3.7 Courant-Fischer极小极大定理

**定理**：设 $A$ 的特征值为 $\lambda_1 \leq \lambda_2 \leq \cdots \leq \lambda_n$，则

$$\lambda_k = \min_{\substack{S \subseteq \mathbb{R}^n \\ \dim(S) = k}} \max_{\substack{x \in S \\ x \neq 0}} R(x) = \max_{\substack{S \subseteq \mathbb{R}^n \\ \dim(S) = n-k+1}} \min_{\substack{x \in S \\ x \neq 0}} R(x)$$

这是 Weyl 不等式和特征值交错定理的理论基础。
