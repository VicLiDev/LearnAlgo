# 第九章 矩阵的广义逆

## 1. 几何意义

当矩阵 $A$ 不可逆（非方阵或奇异矩阵）时，"逆矩阵"的概念不再适用。广义逆（伪逆）是逆矩阵的自然推广。

**几何含义**：

对于 $A \in \mathbb{R}^{m \times n}$，$A^+$ 满足：

- $AA^+$ 是到 $\text{Col}(A)$ 的**正交投影**
- $A^+A$ 是到 $\text{Col}(A^T)$（行空间）的**正交投影**

即 $A^+$ 实现了从 $\text{Col}(A)$ 沿 $\text{Nul}(A^T)$ 方向回到 $\text{Col}(A^T)$ 的"反转"，在零空间方向上保持为零。

**类比**：正交投影好比"压扁"，伪逆好比"恢复"——在可恢复的维度上精确还原，在不可恢复的维度上给出零。

---

## 2. 应用场景

| 领域 | 应用 |
|------|------|
| 最小二乘 | $\min\|Ax - b\|_2$ 的最小范数解 $x = A^+ b$ |
| 线性方程组 | 亏秩系统的最优解 |
| 回归分析 | 多重共线性时的岭回归与伪逆的关系 |
| 机器人学 | 冗余机械臂的逆运动学 |
| 信号处理 | 最小范数滤波器设计 |
| 控制理论 | MIMO系统的伪逆控制分配 |

---

## 3. 数学理论

### 3.1 Moore-Penrose伪逆的定义

**定义**：对矩阵 $A \in \mathbb{R}^{m \times n}$，Moore-Penrose伪逆 $A^+$ 是满足以下四个Penrose方程的唯一矩阵 $X \in \mathbb{R}^{n \times m}$：

1. $AXA = A$（广义逆的基本性质）
2. $XAX = X$
3. $(AX)^T = AX$（$AX$ 是对称矩阵）
4. $(XA)^T = XA$（$XA$ 是对称矩阵）

**唯一性证明**：设 $X, Y$ 都满足四个方程，则

$$X = XAX = X(AX)^T = X X^T A^T = X X^T (AYA)^T = X X^T A^T Y^T A^T Y A = X(AX)^T(AY) = XAXAY = XAY$$

$$Y = YAY = (YA)^T Y = A^T Y^T Y = (AXA)^T Y^T Y = A^T X^T A^T Y^T Y = (XA)^T(AY) = XAYAY = XAY$$

故 $X = Y$。

### 3.2 满秩分解与伪逆构造

**定理**：设 $A = BC$（满秩分解），其中 $B \in \mathbb{R}^{m \times r}$ 列满秩，$C \in \mathbb{R}^{r \times n}$ 行满秩，$r = \text{rank}(A)$，则

$$A^+ = C^T(CC^T)^{-1}(B^TB)^{-1}B^T$$

**推导**：验证四个Penrose方程。

$A^+ A = C^T(CC^T)^{-1}(B^TB)^{-1}B^TBC = C^T(CC^T)^{-1}C$

$(A^+ A)^T = C^T(CC^T)^{-1}C$（对称，满足条件4）

$AA^+ = BC \cdot C^T(CC^T)^{-1}(B^TB)^{-1}B^T = B(B^TB)^{-1}B^T$

$(AA^+)^T = B(B^TB)^{-1}B^T$（对称，满足条件3）

类似验证条件1和2。

### 3.3 基于SVD的伪逆

设 $A = U\Sigma V^T$ 为 SVD，$\Sigma = \text{diag}(\sigma_1, \ldots, \sigma_r, 0, \ldots, 0)$，则

$$A^+ = V\Sigma^+ U^T$$

其中 $\Sigma^+ = \text{diag}(\sigma_1^{-1}, \ldots, \sigma_r^{-1}, 0, \ldots, 0)$（非零奇异值取倒数，零保持为零）。

**验证条件1**：$AA^+A = U\Sigma V^T V \Sigma^+ U^T U \Sigma V^T = U\Sigma\Sigma^+\Sigma V^T$

$\Sigma\Sigma^+\Sigma = \Sigma$，因为非零位置上 $\sigma_i \cdot \sigma_i^{-1} \cdot \sigma_i = \sigma_i$。

### 3.4 伪逆的基本性质

- $(A^+)^+ = A$
- $(A^T)^+ = (A^+)^T$
- $(\alpha A)^+ = \alpha^{-1} A^+$（$\alpha \neq 0$）
- $A^+ = A^{-1}$（当 $A$ 可逆时退化）
- $(AA^T)^+ = (A^+)^T A^+$，$(A^TA)^+ = A^+(A^+)^T$
- 若 $A$ 列满秩：$A^+ = (A^TA)^{-1}A^T$（左逆）
- 若 $A$ 行满秩：$A^+ = A^T(AA^T)^{-1}$（右逆）
- $A^+ = (A^T A)^+ A^T = A^T (AA^T)^+$

### 3.5 伪逆与正交投影

**定理**：

$$P_{\text{Col}(A)} = AA^+, \quad P_{\text{Col}(A^T)} = A^+A$$

$$P_{\text{Nul}(A^T)} = I - AA^+, \quad P_{\text{Nul}(A)} = I - A^+A$$

其中 $P_S$ 表示到子空间 $S$ 的正交投影矩阵。

**推导**（验证 $AA^+$ 为正交投影到 $\text{Col}(A)$）：

1. 幂等性：$(AA^+)^2 = A(A^+AA^+) = AA^+$（由条件2）
2. 对称性：$(AA^+)^T = AA^+$（由条件3）
3. 像空间：$\text{Im}(AA^+) = \text{Col}(A)$

### 3.6 用伪逆求解最小二乘问题

**问题**：$\min_x \|Ax - b\|_2$。

**最小范数解**：$x^* = A^+ b$。

**推导**：

将 $b$ 分解到 $\text{Col}(A)$ 和 $\text{Nul}(A^T)$：

$$b = AA^+b + (I - AA^+)b$$

$\|Ax - b\|_2^2 = \|Ax - AA^+b\|_2^2 + \|(I - AA^+)b\|_2^2$

第一项在 $A^+b$ 处取零（因为 $AA^+b \in \text{Col}(A)$，存在 $x$ 使得 $Ax = AA^+b$，取 $x = A^+b$）。

若解不唯一（$\text{Nul}(A) \neq \{0\}$），$A^+b$ 是所有解中范数最小的，因为 $A^+b \in \text{Col}(A^T) = \text{Nul}(A)^\perp$。

### 3.7 Tikhonov正则化（岭回归）

当 $A$ 病态时，直接求 $A^+b$ 会放大噪声。Tikhonov正则化：

$$x_\alpha = (A^TA + \alpha I)^{-1}A^Tb, \quad \alpha > 0$$

**SVD视角**：设 $A = U\Sigma V^T$，则

$$x_\alpha = V(\Sigma^T\Sigma + \alpha I)^{-1}\Sigma^T U^T b = \sum_{i=1}^{r} \frac{\sigma_i}{\sigma_i^2 + \alpha} (u_i^T b) v_i$$

对比伪逆解 $x^+ = \sum_{i=1}^{r} \frac{1}{\sigma_i}(u_i^T b) v_i$，Tikhonov 将 $1/\sigma_i$ 替换为 $\sigma_i/(\sigma_i^2 + \alpha)$，对小的 $\sigma_i$ 起到平滑作用。

当 $\alpha \to 0$ 时，$x_\alpha \to x^+$。
