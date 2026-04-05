# 第四章 矩阵分解（一）：LU分解与Cholesky分解

## 1. 几何意义

### LU分解

将矩阵 $A$ 分解为下三角矩阵 $L$ 和上三角矩阵 $U$ 的乘积：$A = LU$。

**几何含义**：任何线性变换 $y = Ax$ 都可以分解为两步：
1. $u = Ux$：上三角变换——先处理高维方向（$x_n$），逐步传播到低维方向
2. $y = Lu$：下三角变换——先处理低维方向（$u_1$），逐步传播到高维方向

这类似于将一个复杂的坐标变换拆分为"从上到下"和"从下到上"两个简单步骤。

### Cholesky分解

对于正定矩阵 $A$，分解为 $A = LL^T$（$L$ 为下三角矩阵）。

**几何含义**：正定矩阵对应的二次型 $x^T A x = x^T L L^T x = \|L^T x\|^2$ 表示在 $L^T$ 变换后的空间中的欧几里得范数。Cholesky分解揭示了正定矩阵本质上是"旋转+缩放"后的恒等变换。

---

## 2. 应用场景

| 领域 | 应用 |
|------|------|
| 线性方程组求解 | $Ax = b$ 分解为 $Ly = b$（前代）和 $Ux = y$（回代），复杂度 $O(n^3)$ |
| 行列式计算 | $\det(A) = \det(L)\det(U) = \prod u_{ii}$ |
| 矩阵求逆 | 通过 LU 分解高效求逆 |
| 优化问题 | Newton法中求解线性方程组 |
| Kalman滤波 | 协方差更新中利用 Cholesky 分解保证数值稳定性 |
| 蒙特卡洛模拟 | 从多元正态分布采样需要 Cholesky 分解协方差矩阵 |

---

## 3. 数学理论

### 3.1 LU分解的存在性

**定理**：若 $A \in \mathbb{R}^{n \times n}$ 的所有顺序主子式均非零，即

$$\det(A_k) \neq 0, \quad A_k = A[1:k, 1:k], \quad k = 1, 2, \ldots, n$$

则 $A$ 存在唯一的 LU 分解（$L$ 的对角元素为 1，$U$ 的对角元素非零）。

**Doolittle分解算法**（$L$ 单位下三角）：

对 $i = 1, 2, \ldots, n$：

$$u_{ij} = a_{ij} - \sum_{k=1}^{i-1} l_{ik} u_{kj}, \quad j = i, i+1, \ldots, n$$

$$l_{ji} = \frac{1}{u_{ii}}\left(a_{ji} - \sum_{k=1}^{i-1} l_{jk} u_{ki}\right), \quad j = i+1, i+2, \ldots, n$$

### 3.2 带部分选主元的LU分解（PLU分解）

当顺序主子式可能出现零或接近零时，需要行交换。

**定理**：对任意非奇异矩阵 $A$，存在置换矩阵 $P$、单位下三角矩阵 $L$、上三角矩阵 $U$，使得

$$PA = LU$$

**选主元策略**：在第 $k$ 步，选取第 $k$ 列中（从第 $k$ 行起）绝对值最大的元素作为主元，通过行交换将其移到 $(k,k)$ 位置。

### 3.3 利用LU分解求解线性方程组

给定 $Ax = b$，已知 $PA = LU$：

1. 求解 $Ly = Pb$（前代/Forward substitution）：

$$y_i = (Pb)_i - \sum_{j=1}^{i-1} l_{ij} y_j, \quad i = 1, 2, \ldots, n$$

2. 求解 $Ux = y$（回代/Back substitution）：

$$x_i = \frac{1}{u_{ii}}\left(y_i - \sum_{j=i+1}^{n} u_{ij} x_j\right), \quad i = n, n-1, \ldots, 1$$

**复杂度**：
- LU 分解：$\frac{2}{3}n^3$ 次乘法
- 每次求解（前代+回代）：$2n^2$ 次乘法
- 多右端项时，分解一次即可复用

### 3.4 行列式计算

$$\det(A) = \det(P^{-1}LU) = \det(P^{-1}) \det(L) \det(U) = (-1)^s \prod_{i=1}^{n} u_{ii}$$

其中 $s$ 为行交换次数，$\det(P^{-1}) = (-1)^s$。

### 3.5 Cholesky分解

**定理**：若 $A \in \mathbb{R}^{n \times n}$ 为对称正定矩阵，则存在唯一的下三角矩阵 $L$（对角元素为正），使得

$$A = LL^T$$

**算法**：

对 $j = 1, 2, \ldots, n$：

$$l_{jj} = \sqrt{a_{jj} - \sum_{k=1}^{j-1} l_{jk}^2}$$

$$l_{ij} = \frac{1}{l_{jj}}\left(a_{ij} - \sum_{k=1}^{j-1} l_{ik} l_{jk}\right), \quad i = j+1, j+2, \ldots, n$$

**推导**：展开 $A = LL^T$，即 $\sum_{k=1}^{j} l_{ik} l_{jk} = a_{ij}$。

- 当 $i = j$ 时：$\sum_{k=1}^{j} l_{jk}^2 = a_{jj}$，解出 $l_{jj}$
- 当 $i > j$ 时：$\sum_{k=1}^{j} l_{ik} l_{jk} = a_{ij}$，其中 $l_{ik}$（$k < j$）已由前轮计算得出

**正定性保证**：$l_{jj}^2 = a_{jj} - \sum_{k=1}^{j-1} l_{jk}^2 > 0$，故根号下始终为正，算法不会中断。

**复杂度**：$\frac{1}{3}n^3$ 次乘法（仅为 LU 分解的一半），存储量减半（只需存储 $L$）。

### 3.6 Cholesky分解与多元正态分布

设 $x \sim \mathcal{N}(0, \Sigma)$，其中 $\Sigma$ 为正定协方差矩阵。Cholesky 分解 $\Sigma = LL^T$。

**采样方法**：若 $z \sim \mathcal{N}(0, I)$，则 $x = Lz \sim \mathcal{N}(0, \Sigma)$。

**推导**：

$$\mathbb{E}[x] = L \mathbb{E}[z] = 0$$

$$\text{Cov}(x) = \mathbb{E}[xx^T] = \mathbb{E}[Lzz^T L^T] = L \mathbb{E}[zz^T] L^T = L I L^T = LL^T = \Sigma$$

### 3.7 分块Cholesky更新

当 $A = \begin{pmatrix} A_{11} & A_{21}^T \\ A_{21} & A_{22} \end{pmatrix}$ 正定时，分块 Cholesky 分解为：

$$A_{11} = L_{11} L_{11}^T$$
$$L_{21} = A_{21} L_{11}^{-T}$$
$$S = A_{22} - L_{21} L_{21}^T$$ （Schur补）
$$S = L_{22} L_{22}^T$$

$$A = \begin{pmatrix} L_{11} & 0 \\ L_{21} & L_{22} \end{pmatrix} \begin{pmatrix} L_{11}^T & L_{21}^T \\ 0 & L_{22}^T \end{pmatrix}$$

这在稀疏矩阵和并行计算中非常重要。
