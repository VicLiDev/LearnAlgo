# 第十章 矩阵函数

## 1. 几何意义

矩阵函数将标量函数 $f(x)$ 推广到矩阵 $f(A)$。其核心思想是：通过谱分解（或Jordan标准型），将函数"逐特征值"地作用到矩阵上。

**几何含义**：

- $e^A$（矩阵指数）：描述连续旋转/变换的演化。在物理中，$e^{tA}$ 描述了由矩阵 $A$ 生成的连续变换在时间 $t$ 后的效果
- $\sqrt{A}$（矩阵平方根）：对对称正定矩阵，$A^{1/2}$ 是一个变换 $B$ 使得 $B \circ B = A$
- $\log(A)$（矩阵对数）：矩阵指数的逆运算

---

## 2. 应用场景

| 领域 | 应用 |
|------|------|
| 常微分方程 | $x' = Ax$ 的解为 $x(t) = e^{tA} x(0)$ |
| 图论与网络 | 图的邻接矩阵的指数 $e^A$ 用于计算路径数（图上的"热传导"） |
| 量子力学 | 量子态的演化 $|\psi(t)\rangle = e^{-iHt/\hbar}|\psi(0)\rangle$ |
| 控制理论 | 系统的转移矩阵 $\Phi(t) = e^{At}$ |
| 机器学习 | GNN中的图卷积（谱方法）依赖图Laplacian的矩阵函数 |
| 优化 | 拟Newton法中涉及矩阵逆函数的近似 |

---

## 3. 数学理论

### 3.1 矩阵多项式

**定义**：设 $p(x) = a_0 + a_1 x + \cdots + a_k x^k$，则

$$p(A) = a_0 I + a_1 A + \cdots + a_k A^k$$

**Cayley-Hamilton定理的应用**：$n \times n$ 矩阵 $A$ 满足其特征方程 $p(\lambda) = 0$，故 $p(A) = 0$。这意味着 $A^n$ 可由 $I, A, A^2, \ldots, A^{n-1}$ 线性表示。

**推论**：$A$ 的任何多项式都可以化简为次数不超过 $n-1$ 的多项式。

### 3.2 矩阵函数的定义

矩阵函数有多种等价定义方式：

**定义一（谱映射，可对角化情形）**：若 $A = P\Lambda P^{-1}$ 可对角化，则

$$f(A) = P \cdot \text{diag}(f(\lambda_1), \ldots, f(\lambda_n)) \cdot P^{-1}$$

**定义二（Jordan标准型）**：若 $A = PJP^{-1}$，$J = \text{diag}(J_1, \ldots, J_k)$，则

$$f(A) = P \cdot \text{diag}(f(J_1), \ldots, f(J_k)) \cdot P^{-1}$$

对于 Jordan 块 $J_m(\lambda_0)$，$f(J_m(\lambda_0))$ 为上三角 Toeplitz 矩阵：

$$f(J_m(\lambda_0)) = \begin{pmatrix} f(\lambda_0) & f'(\lambda_0) & \frac{f''(\lambda_0)}{2!} & \cdots & \frac{f^{(m-1)}(\lambda_0)}{(m-1)!} \\ & f(\lambda_0) & f'(\lambda_0) & \ddots & \vdots \\ & & \ddots & \ddots & \frac{f''(\lambda_0)}{2!} \\ & & & f(\lambda_0) & f'(\lambda_0) \\ & & & & f(\lambda_0) \end{pmatrix}$$

**推导**：设 $J = \lambda_0 I + N$（$N$ 为幂零矩阵），由 Taylor 展开：

$$f(\lambda_0 I + N) = \sum_{k=0}^{m-1} \frac{f^{(k)}(\lambda_0)}{k!} N^k$$

其中 $N^k$ 在超对角线上方第 $k$ 条对角线处为 1。

**定义三（幂级数）**：若 $f(z) = \sum_{k=0}^{\infty} a_k z^k$ 的收敛半径包含 $A$ 的所有特征值，则

$$f(A) = \sum_{k=0}^{\infty} a_k A^k$$

**定义四（矩阵演算/函数演算）**：通过 Cauchy 积分公式定义（泛函分析框架下）：

$$f(A) = \frac{1}{2\pi i} \oint_\gamma f(z)(zI - A)^{-1} dz$$

其中 $\gamma$ 包围 $A$ 的所有特征值。

### 3.3 矩阵指数 $e^A$

**定义**：

$$e^A = \sum_{k=0}^{\infty} \frac{A^k}{k!} = I + A + \frac{A^2}{2!} + \frac{A^3}{3!} + \cdots$$

**基本性质**：
- $e^{0} = I$
- $e^A e^{-A} = I$（可逆，逆为 $e^{-A}$）
- $e^{(s+t)A} = e^{sA} e^{tA}$
- **不满足** $e^{A+B} = e^A e^B$（除非 $AB = BA$）
- $\det(e^A) = e^{\text{tr}(A)}$
- $(e^A)^T = e^{A^T}$
- 若 $A = P\Lambda P^{-1}$，则 $e^A = P e^\Lambda P^{-1} = P \text{diag}(e^{\lambda_1}, \ldots, e^{\lambda_n}) P^{-1}$

**推导** $\det(e^A) = e^{\text{tr}(A)}$：

由 Jordan 标准型 $A = PJP^{-1}$，$e^A = Pe^J P^{-1}$。

$\det(e^A) = \det(e^J) = \prod_i \det(e^{J_i})$

对于 Jordan 块 $J_i$，$e^{J_i}$ 是上三角矩阵，对角元素均为 $e^{\lambda_i}$，故 $\det(e^{J_i}) = e^{m_i \lambda_i}$（$m_i$ 为块大小）。

$\det(e^A) = \prod_i e^{m_i \lambda_i} = e^{\sum_i m_i \lambda_i} = e^{\text{tr}(A)}$

### 3.4 矩阵指数的计算方法

**方法一（对角化）**：若 $A = P\Lambda P^{-1}$，则 $e^A = P e^\Lambda P^{-1}$。

**方法二（Jordan标准型）**：对 Jordan 块 $J_m(\lambda)$：

$$e^{J_m(\lambda)} = e^\lambda \begin{pmatrix} 1 & 1 & \frac{1}{2!} & \cdots & \frac{1}{(m-1)!} \\ & 1 & 1 & \ddots & \vdots \\ & & \ddots & \ddots & \frac{1}{2!} \\ & & & 1 & 1 \\ & & & & 1 \end{pmatrix}$$

**方法三（Padé逼近 + 缩放平方）**：

1. 选取缩放因子 $s$ 使 $\|A/2^s\|$ 足够小
2. 用 Padé 逼近计算 $e^{A/2^s} \approx R_{pq}(A/2^s)$
3. 反复平方 $s$ 次：$e^A = (e^{A/2^s})^{2^s}$

这是 MATLAB/NumPy 中 `expm` 函数的标准算法（1977-2009）。

### 3.5 矩阵对数

**定义**：矩阵 $B$ 称为 $A$ 的对数，若 $e^B = A$，记 $B = \log(A)$。

**存在性**：$A$ 有矩阵对数的充要条件是 $A$ 可逆。

**不唯一性**：若 $\log(A) = B$，则 $B + 2\pi i k I$（$k \in \mathbb{Z}$）也是 $A$ 的对数。即使限制为实矩阵，也可能有多个实对数。

**性质**：
- $\log(AB) = \log(A) + \log(B)$ 不一定成立（除非 $A, B$ 可交换）
- $\log(A^{-1}) = -\log(A)$
- $\log(A^n) = n \log(A)$ 不一定成立（类似复数对数的多值性）

### 3.6 矩阵函数的性质

- $f(A^T) = f(A)^T$
- 若 $A = PBP^{-1}$，则 $f(A) = Pf(B)P^{-1}$
- 若 $AB = BA$，则 $f(A)f(B) = f(B)f(A)$
- 同一矩阵的不同函数可交换：$f(A)g(A) = g(A)f(A)$
