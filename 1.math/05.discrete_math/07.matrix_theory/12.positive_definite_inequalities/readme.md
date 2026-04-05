# 第十二章 正定矩阵与矩阵不等式

## 1. 几何意义

### 正定矩阵

$A \succ 0$（对称正定）意味着二次型 $x^T A x > 0$（$x \neq 0$）。

**几何含义**：$x^T A x = 1$ 定义了一个 $n$ 维椭球面，各轴方向为 $A$ 的特征向量方向，半轴长度为 $1/\sqrt{\lambda_i}$。

- 正定：椭球面（所有方向都"向外弯"）
- 半正定：椭柱面（某些方向被"压扁"）
- 不定：双曲面（有些方向向外，有些方向向内）

### 矩阵不等式

$A \succeq B$（即 $A - B \succeq 0$）表示在所有方向上，$A$ 的二次型都不小于 $B$ 的。

---

## 2. 应用场景

| 领域 | 应用 |
|------|------|
| 优化理论 | 凸函数的Hessian矩阵正定保证全局最优 |
| 统计学 | 协方差矩阵半正定；Fisher信息矩阵正定 |
| 机器学习 | 核矩阵必须是半正定的（Mercer定理） |
| 控制理论 | Lyapunov方程 $A^TP + PA + Q = 0$ 中 $P \succ 0$ 判定稳定性 |
| 半定规划 | 矩阵不等式约束下的优化 |
| 信号处理 | 自相关矩阵的正定性保证谱估计的物理可解释性 |

---

## 3. 数学理论

### 3.1 正定矩阵的等价定义

设 $A \in \mathbb{R}^{n \times n}$ 对称，以下命题等价：

1. $A$ 正定（$x^T A x > 0$，$x \neq 0$）
2. $A$ 的所有特征值 $\lambda_i > 0$
3. $A = LL^T$（Cholesky分解存在）
4. $A$ 的所有顺序主子式 $\det(A_k) > 0$（Sylvester准则）
5. 存在可逆矩阵 $B$ 使得 $A = B^T B$
6. $A$ 的所有主子式 $> 0$

**Sylvester准则推导（必要性）**：

设 $A$ 正定，取子矩阵 $A_k = A[1:k, 1:k]$，对任意 $y \in \mathbb{R}^k$（$y \neq 0$），令 $x = (y^T, 0^T)^T \neq 0$，则 $y^T A_k y = x^T A x > 0$，故 $A_k$ 正定，从而 $\det(A_k) > 0$。

### 3.2 正定矩阵的基本性质

- 若 $A, B$ 正定，则 $A + B$ 正定
- 若 $A$ 正定，$\alpha > 0$，则 $\alpha A$ 正定
- 若 $A$ 正定，则 $A^{-1}$ 正定（特征值取倒数仍为正）
- 若 $A$ 正定，则 $A^T = A$（已蕴含在对称假设中），$A^k$ 正定（$k > 0$）
- **Schur乘积定理**：若 $A, B$ 正定，则 $A \circ B$（Hadamard积/逐元素乘积）正定
- **主子矩阵保持正定性**：正定矩阵的任何主子矩阵仍正定

### 3.3 常用矩阵不等式

#### Cauchy-Schwarz不等式（矩阵形式）

设 $A$ 对称正定，则

$$(x^T y)^2 \leq (x^T A x)(y^T A^{-1} y)$$

等号当且仅当 $x$ 与 $A^{-1}y$ 成比例。

**推导**：对任意 $t \in \mathbb{R}$，$(x + t A^{-1}y)^T A (x + t A^{-1}y) \geq 0$，展开得二次不等式，判别式 $\leq 0$ 即得。

#### Weyl不等式

设 $A, B$ 为 $n \times n$ Hermite矩阵，特征值按递减排列，则

$$\lambda_i(A + B) \leq \lambda_j(A) + \lambda_{i-j+1}(B), \quad 1 \leq j \leq i \leq n$$

特别地，$\lambda_{\max}(A + B) \leq \lambda_{\max}(A) + \lambda_{\max}(B)$。

#### LMI（线性矩阵不等式）

形如 $F(x) = F_0 + \sum_{i=1}^{m} x_i F_i \succeq 0$ 的约束称为线性矩阵不等式。

这是半定规划（SDP）的标准形式，在控制、优化等领域有广泛应用。

### 3.4 Schur补与正定性判定

设分块矩阵 $M = \begin{pmatrix} A & B \\ B^T & D \end{pmatrix}$，其中 $A$ 可逆。

**Schur补**：$S = D - B^T A^{-1} B$。

**正定性等价条件**（$M$ 对称）：

$$M \succ 0 \iff A \succ 0 \text{ 且 } S \succ 0$$

**推导**：对 $M$ 做合同变换：

$$\begin{pmatrix} I & 0 \\ -B^T A^{-1} & I \end{pmatrix} \begin{pmatrix} A & B \\ B^T & D \end{pmatrix} \begin{pmatrix} I & -A^{-1}B \\ 0 & I \end{pmatrix} = \begin{pmatrix} A & 0 \\ 0 & D - B^T A^{-1}B \end{pmatrix}$$

合同变换不改变正定性，故 $M \succ 0 \iff A \succ 0$ 且 $S = D - B^T A^{-1}B \succ 0$。

### 3.5 Lyapunov方程

$$A^T P + PA + Q = 0$$

其中 $A$ 给定，$Q$ 对称正定，求 $P$。

**定理**：若 $A$ 稳定（所有特征值实部 $< 0$），则 Lyapunov 方程有唯一对称正定解 $P$。

**与稳定性的关系**：连续线性系统 $\dot{x} = Ax$ 渐近稳定的充要条件是存在 $P \succ 0$ 使得 $A^T P + PA \prec 0$。

**推导（充分性）**：取 Lyapunov 函数 $V(x) = x^T P x$，则

$$\dot{V} = \dot{x}^T P x + x^T P \dot{x} = x^T A^T P x + x^T P A x = x^T(A^T P + PA)x < 0$$

$V$ 正定且单调递减至零，故系统渐近稳定。

### 3.6 矩阵均值不等式

**算术-几何-调和均值不等式（矩阵形式）**：

设 $A, B \succ 0$，则

$$\frac{A + B}{2} \succeq A \# B \succeq \frac{2}{A^{-1} + B^{-1}}$$

其中 $A \# B = A^{1/2}(A^{-1/2}BA^{-1/2})^{1/2}A^{1/2}$ 为**几何均值**（矩阵几何均值）。

- 左式为算术均值（AM），右式为调和均值（HM）

### 3.7 Loewner序

**定义**：$A \succeq B$ 表示 $A - B$ 为半正定矩阵。

**性质**：
- $A \succeq B \succeq 0 \implies \lambda_i(A) \geq \lambda_i(B)$（特征值单调性）
- $A \succeq B \succ 0 \implies B^{-1} \succeq A^{-1}$（逆序）
- $A \succeq B \succeq 0 \implies \det(A) \geq \det(B)$
- $A \succeq B \succeq 0 \implies \text{tr}(A) \geq \text{tr}(B)$

**推导逆序性**：$A \succeq B \succ 0 \implies B^{-1/2}AB^{-1/2} \succeq I$

$(B^{-1/2}AB^{-1/2})^{-1} \preceq I \implies B^{1/2}A^{-1}B^{1/2} \preceq I \implies A^{-1} \preceq B^{-1}$
