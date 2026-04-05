# 第十三章 矩阵的Kronecker积与向量化

## 1. 几何意义

### Kronecker积

Kronecker积 $A \otimes B$ 将两个矩阵的元素做"外积式"的乘法组合，结果是一个大矩阵。

**几何含义**：若 $A$ 表示 $\mathbb{R}^n$ 上的变换，$B$ 表示 $\mathbb{R}^m$ 上的变换，则 $A \otimes B$ 表示 $\mathbb{R}^{n \times m} \cong \mathbb{R}^{nm}$ 上的"联合变换"——独立地对两个子空间施加各自变换。

直观类比：两个旋转的组合不是"先转一个再转另一个"（那是矩阵乘法），而是"同时对两个独立维度旋转"。

### 向量化

$\text{vec}(X)$ 将矩阵 $X$ 逐列堆叠成一个长向量。

**几何含义**：将 $\mathbb{R}^{m \times n}$ 等同于 $\mathbb{R}^{mn}$，将矩阵空间展平为向量空间。

---

## 2. 应用场景

| 领域 | 应用 |
|------|------|
| 偏微分方程 | 二维/三维网格离散后导出 Kronecker 积结构 |
| 多元统计 | 多元正态分布协方差矩阵的 Kronecker 结构 |
| 信号处理 | MIMO 信道建模（Kronecker信道模型） |
| 量子计算 | 多量子比特系统的状态空间是单比特空间的Kronecker积 |
| 深度学习 | 权重矩阵的向量化用于优化算法 |
| 方程组求解 | Sylvester/Lyapunov方程可化为线性方程组 |

---

## 3. 数学理论

### 3.1 Kronecker积的定义

设 $A \in \mathbb{R}^{m \times n}$，$B \in \mathbb{R}^{p \times q}$，则

$$A \otimes B = \begin{pmatrix} a_{11}B & a_{12}B & \cdots & a_{1n}B \\ a_{21}B & a_{22}B & \cdots & a_{2n}B \\ \vdots & \vdots & \ddots & \vdots \\ a_{m1}B & a_{m2}B & \cdots & a_{mn}B \end{pmatrix} \in \mathbb{R}^{mp \times nq}$$

结果大小为 $mp \times nq$。

### 3.2 Kronecker积的基本性质

- **双线性**：$(A + B) \otimes C = A \otimes C + B \otimes C$，$A \otimes (B + C) = A \otimes B + A \otimes C$
- **结合律**：$(A \otimes B) \otimes C = A \otimes (B \otimes C)$
- **混合积**：$(A \otimes B)(C \otimes D) = (AC) \otimes (BD)$（维度相容时）
- **转置**：$(A \otimes B)^T = A^T \otimes B^T$
- **行列式**：$\det(A \otimes B) = \det(A)^p \cdot \det(B)^m$（$A \in \mathbb{R}^{m \times m}$，$B \in \mathbb{R}^{p \times p}$）
- **迹**：$\text{tr}(A \otimes B) = \text{tr}(A) \cdot \text{tr}(B)$
- **逆**：$(A \otimes B)^{-1} = A^{-1} \otimes B^{-1}$
- **秩**：$\text{rank}(A \otimes B) = \text{rank}(A) \cdot \text{rank}(B)$

**推导混合积**：

设 $A \in \mathbb{R}^{m \times n}$，$B \in \mathbb{R}^{p \times q}$，$C \in \mathbb{R}^{n \times r}$，$D \in \mathbb{R}^{q \times s}$。

$[(A \otimes B)(C \otimes D)]_{(i-1)p+k, (j-1)s+l}$

$= \sum_{\alpha,\beta} (A \otimes B)_{(i-1)p+k, (\alpha-1)q+\beta} \cdot (C \otimes D)_{(\alpha-1)q+\beta, (j-1)s+l}$

$= \sum_{\alpha} a_{i\alpha} c_{\alpha j} \cdot b_{k\beta} d_{\beta l} = (AC \otimes BD)_{(i-1)p+k, (j-1)s+l}$

### 3.3 Kronecker积的特征值与特征向量

**定理**：若 $A$ 的特征值为 $\lambda_1, \ldots, \lambda_m$（对应特征向量 $u_i$），$B$ 的特征值为 $\mu_1, \ldots, \mu_p$（对应特征向量 $v_j$），则 $A \otimes B$ 的特征值为 $\lambda_i \mu_j$（对应特征向量 $u_i \otimes v_j$）。

**推导**：

$$(A \otimes B)(u_i \otimes v_j) = (Au_i) \otimes (Bv_j) = (\lambda_i u_i) \otimes (\mu_j v_j) = \lambda_i \mu_j (u_i \otimes v_j)$$

### 3.4 向量化（vec算子）

**定义**：$\text{vec}(X)$ 将 $X \in \mathbb{R}^{m \times n}$ 逐列堆叠为 $mn$ 维向量：

$$\text{vec}\begin{pmatrix} x_1 & x_2 & \cdots & x_n \end{pmatrix} = \begin{pmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{pmatrix}$$

其中 $x_j$ 为 $X$ 的第 $j$ 列。

### 3.5 vec与Kronecker积的关系

**核心恒等式**：

$$\text{vec}(AXB) = (B^T \otimes A) \text{vec}(X)$$

**推导**：

设 $A \in \mathbb{R}^{m \times p}$，$X \in \mathbb{R}^{p \times q}$，$B \in \mathbb{R}^{q \times n}$。

$(AXB)_{ij} = \sum_{k,l} a_{ik} x_{kl} b_{lj}$

$\text{vec}(AXB)$ 的第 $(j-1)m + i$ 个元素为 $(AXB)_{ij} = \sum_{k,l} a_{ik} x_{kl} b_{lj}$。

$(B^T \otimes A)$ 的第 $((j-1)m + i, (l-1)p + k)$ 个元素为 $b_{lj} a_{ik}$。

$[(B^T \otimes A) \text{vec}(X)]_{(j-1)m+i} = \sum_{k,l} a_{ik} b_{lj} x_{kl} = (AXB)_{ij}$

**重要特例**：

- $\text{vec}(AX) = (I \otimes A) \text{vec}(X)$
- $\text{vec}(XB) = (B^T \otimes I) \text{vec}(X)$
- $\text{vec}(AXA^T) = (A \otimes A) \text{vec}(X)$

### 3.6 vec与迹的关系

$$\text{tr}(A^T B) = \text{vec}(A)^T \text{vec}(B) = \langle \text{vec}(A), \text{vec}(B) \rangle$$

**推导**：$\text{tr}(A^TB) = \sum_{i,j} a_{ij} b_{ij} = \text{vec}(A)^T \text{vec}(B)$。

### 3.7 应用：矩阵方程向量化

**Sylvester方程**：$AX + XB = C$

**向量化**：$\text{vec}(AX + XB) = (I_n \otimes A) \text{vec}(X) + (B^T \otimes I_m) \text{vec}(X) = (I_n \otimes A + B^T \otimes I_m) \text{vec}(X)$

化为线性方程组：$(I_n \otimes A + B^T \otimes I_m) \text{vec}(X) = \text{vec}(C)$

系数矩阵大小为 $mn \times mn$。

**Lyapunov方程**：$AX + XA^T = Q$

$(I_n \otimes A + A \otimes I_n) \text{vec}(X) = \text{vec}(Q)$

**存在唯一解的条件**：$A$ 和 $-A^T$ 无公共特征值。

由 Kronecker 积特征值公式，系数矩阵的特征值为 $\lambda_i(A) + \lambda_j(A)$。当 $A$ 的所有特征值实部 $> 0$ 时，$\lambda_i + \lambda_j \neq 0$，系数矩阵可逆。

### 3.8 Khatri-Rao积

**定义**：设 $A \in \mathbb{R}^{m \times n}$，$B \in \mathbb{R}^{p \times n}$（列数相同），Khatri-Rao积为对应列的Kronecker积：

$$A \odot B = [a_1 \otimes b_1, \quad a_2 \otimes b_2, \quad \cdots, \quad a_n \otimes b_n] \in \mathbb{R}^{mp \times n}$$

**应用**：张量分解（CP分解）、多线性代数、盲源分离。

### 3.9 向量化在矩阵微分中的应用

利用 vec 和 Kronecker 积可以系统地处理矩阵微分。

**法则**：$d(AXB) = A(dX)B \implies \text{vec}(d(AXB)) = (B^T \otimes A) \text{vec}(dX)$

$$\frac{\partial \text{vec}(AXB)}{\partial \text{vec}(X)} = B^T \otimes A$$

**例**：$\frac{\partial \text{vec}(X^T A X)}{\partial \text{vec}(X)}$

$d(X^T A X) = (dX)^T A X + X^T A dX$

$\text{vec}(d(X^T A X)) = (X^T A^T \otimes I + I \otimes X^T A) K \text{ vec}(dX)$

其中 $K$ 是交换矩阵（commutation matrix），满足 $\text{vec}(X^T) = K \text{vec}(X)$。
