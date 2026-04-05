# 第三章 Jordan标准型

## 1. 几何意义

Jordan标准型回答了一个根本问题：**任何方阵在适当坐标系下最简形式是什么？**

当矩阵可以对角化时，它在特征向量构成的坐标系下变为对角矩阵（各方向独立缩放）。但当矩阵不能对角化时（特征向量不够），Jordan标准型是最接近对角化的形式——对角线上是特征值，上方可能出现 1，表示方向之间存在"耦合"。

**几何图像（2D）**：

$$J = \begin{pmatrix} \lambda & 1 \\ 0 & \lambda \end{pmatrix}$$

这不是简单的缩放。设 $e_1 = (1, 0)^T$，$e_2 = (0, 1)^T$：

- $Je_1 = \lambda e_1$（$e_1$ 是特征向量，被缩放）
- $Je_2 = e_1 + \lambda e_2$（$e_2$ 先被缩放 $\lambda$ 倍，再叠加一个 $e_1$ 方向的分量）

这种"叠加"使得 $e_2$ 方向在反复变换中会"螺旋式偏转"到 $e_1$ 方向，形成一种**剪切+缩放**的复合效果。

**Jordan块的几何意义**：

每个 Jordan 块 $J_k(\lambda)$ 对应一个**广义特征向量链**：

$$v_1 \xrightarrow{A - \lambda I} v_2 \xrightarrow{A - \lambda I} \cdots \xrightarrow{A - \lambda I} v_k \xrightarrow{A - \lambda I} 0$$

几何上，这描述了一条"不变子空间链"——每经一次 $(A - \lambda I)$ 变换，维度降一维，最终映射到零。

---

## 2. 应用场景

| 领域 | 应用 |
|------|------|
| 常微分方程组 | $x' = Ax$ 的通解由 Jordan 标准型确定 |
| 矩阵函数计算 | $f(A)$ 可通过 $f(J)$ 直接计算 |
| 矩阵幂 $A^k$ | 通过 Jordan 块的幂运算高效计算 |
| 控制理论 | 系统的能控/能观性与 Jordan 结构相关 |
| 交换代数 | Jordan 标准型是有限维代数表示论的经典结果 |

---

## 3. 数学理论

### 3.1 对角化

**定理**：$A \in \mathbb{C}^{n \times n}$ 可对角化的充要条件是 $A$ 有 $n$ 个线性无关的特征向量。

**等价条件**：
1. $A$ 有 $n$ 个线性无关的特征向量
2. 每个特征值的代数重数等于几何重数
3. $A$ 的极小多项式无重根

若 $A$ 可对角化，则存在可逆矩阵 $P$ 使得

$$P^{-1}AP = \Lambda = \text{diag}(\lambda_1, \lambda_2, \ldots, \lambda_n)$$

其中 $P$ 的列向量为 $A$ 的特征向量。

**推导**：由 $AP = P\Lambda$ 逐列展开即得 $Ap_i = \lambda_i p_i$。

### 3.2 代数重数与几何重数

设 $\lambda$ 是 $A$ 的特征值：

- **代数重数** $m_a(\lambda)$：$\lambda$ 作为特征多项式根的重数
- **几何重数** $m_g(\lambda)$：$\lambda$ 对应的线性无关特征向量的个数，即 $\dim(\text{Nul}(A - \lambda I))$

**基本关系**：$1 \leq m_g(\lambda) \leq m_a(\lambda)$

**证明**：$m_g \geq 1$ 因为 $\det(A - \lambda I) = 0$ 保证了零空间非平凡。

$m_g \leq m_a$ 的证明：设 $\lambda$ 有 $m_g$ 个线性无关的特征向量，可扩充为 $\mathbb{C}^n$ 的一组基，在此基下 $A$ 分块为 $\begin{pmatrix} \lambda I & * \\ 0 & B \end{pmatrix}$。取行列式得 $p(\lambda) = (\lambda - \lambda_0)^{m_g} \det(B - \lambda I)$，故代数重数至少为 $m_g$。

### 3.3 广义特征向量

当 $m_g(\lambda) < m_a(\lambda)$ 时，特征向量不够用，需要引入**广义特征向量**。

**定义**：设 $\lambda$ 是 $A$ 的特征值。向量 $v$ 称为 $A$ 的属于 $\lambda$ 的**$k$ 阶广义特征向量**，若

$$(A - \lambda I)^k v = 0, \quad (A - \lambda I)^{k-1} v \neq 0$$

- 1 阶广义特征向量就是普通特征向量
- 广义特征向量链：$v_k, v_{k-1} = (A-\lambda I)v_k, \ldots, v_1 = (A-\lambda I)^{k-1}v_k$

### 3.4 Jordan标准型定理

**定理（Jordan标准型）**：设 $A \in \mathbb{C}^{n \times n}$，则存在可逆矩阵 $P$ 使得

$$P^{-1}AP = J = \begin{pmatrix} J_{n_1}(\lambda_1) & & \\ & \ddots & \\ & & J_{n_k}(\lambda_k) \end{pmatrix}$$

其中每个 Jordan 块形如

$$J_{n_i}(\lambda_i) = \begin{pmatrix} \lambda_i & 1 & & \\ & \lambda_i & \ddots & \\ & & \ddots & 1 \\ & & & \lambda_i \end{pmatrix}_{n_i \times n_i}$$

**唯一性**：Jordan 标准型在不计 Jordan 块排列顺序的意义下唯一。

### 3.5 Jordan块的结构确定

设 $\lambda$ 是 $A$ 的特征值，代数重数为 $m$：

- **$k$ 阶广义特征空间的维数**：$d_k = \dim(\text{Nul}((A - \lambda I)^k))$
- **大小 $\geq k$ 的 Jordan 块个数**：$n_k = d_k - d_{k-1}$（约定 $d_0 = 0$）
- **恰为 $k$ 阶的 Jordan 块个数**：$n_k - n_{k+1}$

**例**：$d_1 = 3, d_2 = 5, d_3 = 6, d_4 = 6, \ldots$

- $\geq 1$ 阶块数：$d_1 - d_0 = 3$（共有 3 个 Jordan 块）
- $\geq 2$ 阶块数：$d_2 - d_1 = 2$
- $\geq 3$ 阶块数：$d_3 - d_2 = 1$
- $\geq 4$ 阶块数：$d_4 - d_3 = 0$

故 Jordan 结构为：一个 3 阶块，一个 2 阶块，一个 1 阶块。

### 3.6 极小多项式

**定义**：$A$ 的**极小多项式** $m_A(\lambda)$ 是使 $m_A(A) = 0$ 的最低次数的首一多项式。

**与 Jordan 标准型的关系**：$m_A(\lambda) = \prod_{\lambda_i \text{ 互异}} (\lambda - \lambda_i)^{k_i}$

其中 $k_i$ 是 $\lambda_i$ 对应的最大 Jordan 块的阶数。

**对角化判据**：$A$ 可对角化 $\iff$ 极小多项式无重根。

**推导**：每个 Jordan 块 $J_k(\lambda_0)$ 代入 $(x - \lambda_0)^k$ 为零但代入更低次幂不为零。因此使所有 Jordan 块为零的最低幂次由最大块决定。

### 3.7 利用 Jordan 标准型计算矩阵幂

设 $P^{-1}AP = J$，则 $A^k = P J^k P^{-1}$。

对于单个 Jordan 块 $J_n(\lambda)$：

$$J_n(\lambda)^k = \begin{pmatrix} \lambda^k & \binom{k}{1}\lambda^{k-1} & \binom{k}{2}\lambda^{k-2} & \cdots & \binom{k}{n-1}\lambda^{k-n+1} \\ & \lambda^k & \binom{k}{1}\lambda^{k-1} & \ddots & \vdots \\ & & \ddots & \ddots & \binom{k}{2}\lambda^{k-2} \\ & & & \lambda^k & \binom{k}{1}\lambda^{k-1} \\ & & & & \lambda^k \end{pmatrix}$$

其中 $\binom{k}{j} = \frac{k(k-1)\cdots(k-j+1)}{j!}$（广义二项式系数，$j > k$ 时为 0）。

**推导**：将 $J_n(\lambda) = \lambda I + N$，其中 $N$ 是幂零矩阵（$N^n = 0$），利用二项式定理展开：

$$(\lambda I + N)^k = \sum_{j=0}^{\min(k, n-1)} \binom{k}{j} \lambda^{k-j} N^j$$

注意到 $N^j$ 是超对角线上方第 $j$ 条对角线全为 1、其余为零的矩阵。
