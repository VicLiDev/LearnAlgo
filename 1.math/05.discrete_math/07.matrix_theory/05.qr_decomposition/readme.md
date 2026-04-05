# 第五章 矩阵分解（二）：QR分解

## 1. 几何意义

QR分解将矩阵 $A \in \mathbb{R}^{m \times n}$ 分解为正交矩阵 $Q$ 和上三角矩阵 $R$ 的乘积：$A = QR$。

**几何含义**：

- $Q$ 是一个**旋转/反射**（正交变换，保持长度和角度不变），它将标准正交基旋转到 $A$ 的列空间上
- $R$ 是一个**上三角变换**，表示在 $Q$ 的新坐标系下，从高维到低维的逐步"消除"过程

具体来说，QR分解的过程就像是 Gram-Schmidt 正交化的矩阵化：用列空间的一组正交基（$Q$ 的列）来重新表示 $A$ 的各列。

**等价理解**：$A = QR$ 中，$A$ 的第 $j$ 列 $a_j = Q r_j$（$r_j$ 为 $R$ 的第 $j$ 列），即 $a_j$ 是 $Q$ 的前 $j$ 列的线性组合（因为 $R$ 是上三角的），组合系数就是 $R$ 的第 $j$ 列。

---

## 2. 应用场景

| 领域 | 应用 |
|------|------|
| 最小二乘问题 | $Ax = b$ 的最小二乘解 $x = R^{-1} Q^T b$，数值稳定性优于正规方程 |
| 特征值计算 | QR算法是计算矩阵全部特征值的最重要方法 |
| 线性方程组 | 正交变换不会放大误差，比 LU 分解数值更稳定 |
| 正交化 | Gram-Schmidt 过程的数值稳定版本 |
| 奇异值分解 | SVD 可通过 QR 分解分步计算 |

---

## 3. 数学理论

### 3.1 正交矩阵回顾

**定义**：矩阵 $Q \in \mathbb{R}^{m \times m}$ 为正交矩阵，若 $Q^T Q = QQ^T = I$。

等价条件：
- $Q^T = Q^{-1}$
- $Q$ 的列向量构成标准正交基
- $Q$ 的行向量构成标准正交基
- $Q$ 保持内积：$\langle Qx, Qy \rangle = \langle x, y \rangle$
- $Q$ 保持范数：$\|Qx\|_2 = \|x\|_2$
- $\det(Q) = \pm 1$（$+1$ 对应旋转，$-1$ 对应反射）

### 3.2 QR分解的存在唯一性

**定理（Gram-Schmidt构造）**：若 $A \in \mathbb{R}^{m \times n}$ 列满秩（$\text{rank}(A) = n$），则存在唯一分解 $A = QR$，其中 $Q \in \mathbb{R}^{m \times n}$ 满足 $Q^T Q = I_n$（列正交），$R \in \mathbb{R}^{n \times n}$ 为上三角矩阵且对角元素为正。

**推广**：对任意 $A \in \mathbb{R}^{m \times n}$（$m \geq n$），存在 $Q \in \mathbb{R}^{m \times m}$（完整正交矩阵）和 $R \in \mathbb{R}^{m \times n}$（上三角）使得 $A = QR$。

### 3.3 Gram-Schmidt正交化

**经典 Gram-Schmidt（CGS）**：

输入：线性无关向量组 $\{a_1, a_2, \ldots, a_n\}$

$$q_1 = \frac{a_1}{\|a_1\|}$$

$$\tilde{q}_j = a_j - \sum_{k=1}^{j-1} \langle a_j, q_k \rangle q_k, \quad q_j = \frac{\tilde{q}_j}{\|\tilde{q}_j\|}, \quad j = 2, \ldots, n$$

**矩阵形式**：$R_{kj} = q_k^T a_j$（$k < j$），$R_{jj} = \|\tilde{q}_j\|$，则 $A = QR$。

**经典 Gram-Schmidt 的数值不稳定性**：当列向量接近线性相关时，CGS 中正交性会迅速丧失（正交误差可达机器精度的 $\sqrt{n}$ 倍甚至更差）。

### 3.4 修改的Gram-Schmidt（MGS）

**改进**：将投影过程改为逐步进行，而不是一次性从 $a_j$ 中减去所有投影。

```text
for j = 1 to n:
    v_j = a_j
for j = 1 to n:
    for i = 1 to j-1:
        R_{ij} = q_i^T v_j
        v_j = v_j - R_{ij} q_i
    R_{jj} = ||v_j||
    q_j = v_j / R_{jj}
```

**关键区别**：MGS 中每步投影都使用已更新的 $v_j$，而不是原始的 $a_j$。这在数值上更稳定，因为舍入误差累积更小。

### 3.5 Householder变换

**定义**：Householder矩阵（初等反射矩阵）

$$H = I - 2 \frac{vv^T}{v^T v}$$

其中 $v \in \mathbb{R}^m$ 为任意非零向量。

**性质**：
- $H^T = H$（对称）
- $H^2 = I$（对合）
- $H^T H = I$（正交）
- $\det(H) = -1$（反射）
- 保持范数：$\|Hx\|_2 = \|x\|_2$

**零化向量**：给定 $x \in \mathbb{R}^m$，构造 $v$ 使得 $Hx = \alpha e_1$。

取 $v = x + \text{sign}(x_1) \|x\| e_1$，则

$$Hx = x - 2\frac{v^T x}{v^T v} v = x - v = -\text{sign}(x_1)\|x\| e_1$$

**推导**：

令 $\alpha = -\text{sign}(x_1)\|x\|$，要求 $Hx = \alpha e_1$。

由 $Hx = x - \frac{2v^T x}{v^T v}v$，取 $v = x - \alpha e_1$，则

$$\frac{2v^T x}{v^T v} = \frac{2(x - \alpha e_1)^T x}{\|x - \alpha e_1\|^2} = \frac{2(\|x\|^2 - \alpha x_1)}{\|x\|^2 - 2\alpha x_1 + \alpha^2}$$

代入 $\alpha^2 = \|x\|^2$，分子分母均化简为 $2(\|x\|^2 - \alpha x_1)$，故比值为 1。

$$Hx = x - v = x - (x - \alpha e_1) = \alpha e_1 \quad \checkmark$$

### 3.6 Householder QR分解

**算法**：

对 $k = 1, 2, \ldots, n$：

1. 取 $A$ 的第 $k$ 列从第 $k$ 行起的子向量 $x = A[k:m, k]$
2. 构造 Householder 向量 $v_k$ 使得 $H_k x = \alpha e_1$
3. 将 $H_k$ 作用于 $A$ 的右下角子矩阵：$A[k:m, k:n] = (I - 2v_k v_k^T / v_k^T v_k) A[k:m, k:n]$

最终 $A$ 变为上三角矩阵 $R$，$Q = H_1 H_2 \cdots H_n$。

**复杂度**：$\frac{2}{3}n^2(3m - n)$ 次乘法。

**数值优势**：Householder QR 的正交性损失为 $O(\epsilon_{\text{mach}})$，远优于经典 Gram-Schmidt 的 $O(\sqrt{n}\epsilon_{\text{mach}})$。

### 3.7 Givens旋转

**定义**：Givens旋转矩阵 $G(i, j, \theta)$ 是在 $(i,j)$ 平面上的旋转：

$$G_{ij} = \begin{pmatrix} 1 & & & \\ & \cos\theta & & \sin\theta \\ & & 1 & \\ & -\sin\theta & & \cos\theta \end{pmatrix}$$

**作用**：$G_{ij}$ 仅修改第 $i$ 和第 $j$ 行（或列），可将指定位置的元素置零。

**应用**：Givens旋转特别适合稀疏矩阵（只操作非零元素）和硬件实现（适合流水线并行）。

### 3.8 QR分解求解最小二乘问题

**问题**：$\min_x \|Ax - b\|_2$，其中 $A \in \mathbb{R}^{m \times n}$（$m > n$）。

**方法**：设 $A = QR$（$Q \in \mathbb{R}^{m \times m}$），则

$$\|Ax - b\|_2^2 = \|QRx - b\|_2^2 = \|Rx - Q^T b\|_2^2$$

设 $Q^T b = \begin{pmatrix} c_1 \\ c_2 \end{pmatrix}$（$c_1 \in \mathbb{R}^n$），$R = \begin{pmatrix} R_1 \\ 0 \end{pmatrix}$（$R_1 \in \mathbb{R}^{n \times n}$ 上三角），则

$$\|Ax - b\|_2^2 = \|R_1 x - c_1\|_2^2 + \|c_2\|_2^2$$

最小值在 $R_1 x = c_1$ 时取得，残差为 $\|c_2\|_2$。

**与正规方程的比较**：

| 方法 | 条件数放大 | 数值稳定性 | 复杂度 |
|------|-----------|-----------|--------|
| 正规方程 $A^TAx = A^Tb$ | $\kappa(A^TA) = \kappa(A)^2$ | 较差 | $\frac{2}{3}n^3 + 2n^2 m$ |
| QR分解 | $\kappa(A)$ | 好 | $\frac{2}{3}n^2(3m-n) + 2n^2$ |
