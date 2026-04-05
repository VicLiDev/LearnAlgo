# 第六章 矩阵分解（三）：奇异值分解（SVD）

## 1. 几何意义

奇异值分解（SVD）是矩阵论中最重要的分解之一。对于任意矩阵 $A \in \mathbb{R}^{m \times n}$，存在分解

$$A = U \Sigma V^T$$

其中 $U \in \mathbb{R}^{m \times m}$ 为正交矩阵，$\Sigma \in \mathbb{R}^{m \times n}$ 为对角矩阵（对角元素 $\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_r > 0$），$V \in \mathbb{R}^{n \times n}$ 为正交矩阵。

**几何含义**：任何线性变换都可以分解为三个基本变换的复合：

$$\text{旋转}(V^T) \to \text{缩放}(\Sigma) \to \text{旋转}(U)$$

1. $V^T$：在输入空间 $\mathbb{R}^n$ 中旋转到一组"最优"正交基
2. $\Sigma$：沿各坐标轴独立缩放（可能降维），$\sigma_i$ 就是第 $i$ 个方向的缩放因子
3. $U$：在输出空间 $\mathbb{R}^m$ 中旋转到另一组正交基

**关键几何事实**：

- $A$ 将 $\mathbb{R}^n$ 中的单位球映射为 $\mathbb{R}^m$ 中的超椭球
- 各半轴的长度就是奇异值 $\sigma_1, \sigma_2, \ldots, \sigma_r$
- 半轴的方向由 $U$ 的列给出
- 映射前对应的"最优"输入方向由 $V$ 的列给出

**低秩逼近的几何含义**：只保留前 $k$ 个最大奇异值，相当于用最扁的方向来近似原来的椭球——这是最佳可能的 $k$ 维近似。

---

## 2. 应用场景

| 领域 | 应用 |
|------|------|
| 降维/压缩 | 截断SVD（保留前 $k$ 个奇异值）用于数据压缩、图像压缩 |
| 主成分分析 | PCA 的本质就是对数据矩阵做 SVD |
| 最小二乘 | SVD 可求解任意（包括亏秩）最小二乘问题 |
| 伪逆 | $A^+ = V \Sigma^+ U^T$，基于 SVD 计算广义逆 |
| 推荐系统 | Netflix 竞赛中 SVD 成为协同过滤的核心方法 |
| 自然语言处理 | 潜在语义分析（LSA）通过 SVD 发现词-文档关联 |
| 信号处理 | 奇异值谱分析用于信号去噪 |
| 低秩矩阵恢复 | 奇异值阈值化（SVT）用于矩阵补全 |
| 图像处理 | 图像去噪、水印提取 |
| 数值秩判定 | 有效秩 = 大于阈值的奇异值个数 |

---

## 3. 数学理论

### 3.1 SVD的存在性定理

**定理**：设 $A \in \mathbb{R}^{m \times n}$，$\text{rank}(A) = r$，则存在正交矩阵 $U \in \mathbb{R}^{m \times m}$ 和 $V \in \mathbb{R}^{n \times n}$，以及对角矩阵 $\Sigma = \text{diag}(\sigma_1, \ldots, \sigma_r, 0, \ldots, 0) \in \mathbb{R}^{m \times n}$，其中 $\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_r > 0$，使得

$$A = U \Sigma V^T$$

**证明**：

$A^T A$ 为 $n \times n$ 实对称半正定矩阵，特征值为 $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_r > 0 = \lambda_{r+1} = \cdots = \lambda_n$。

取 $V = [v_1, \ldots, v_n]$ 为 $A^T A$ 的正交特征向量矩阵。定义

$$\sigma_i = \sqrt{\lambda_i}, \quad u_i = \frac{Av_i}{\sigma_i}, \quad i = 1, \ldots, r$$

**验证 $u_i$ 标准正交**：

$$u_i^T u_j = \frac{v_i^T A^T A v_j}{\sigma_i \sigma_j} = \frac{\lambda_j v_i^T v_j}{\sigma_i \sigma_j} = \frac{\lambda_j \delta_{ij}}{\sigma_i \sigma_j} = \delta_{ij}$$

将 $\{u_1, \ldots, u_r\}$ 扩充为 $\mathbb{R}^m$ 的标准正交基得到 $U$。

**验证分解**：$AV = U\Sigma$ 逐列展开，对 $i \leq r$：$Av_i = \sigma_i u_i$；对 $i > r$：$Av_i = 0$（因为 $A^T A v_i = 0 \implies v_i^T A^T A v_i = 0 \implies Av_i = 0$）。故 $A = U\Sigma V^T$。

### 3.2 SVD与特征值的关系

- $A^T A = V \Sigma^T \Sigma V^T$：$A^T A$ 的特征值为 $\sigma_i^2$，右奇异向量 $v_i$ 为其特征向量
- $AA^T = U \Sigma \Sigma^T U^T$：$AA^T$ 的特征值为 $\sigma_i^2$，左奇异向量 $u_i$ 为其特征向量
- $A$ 的非零奇异值等于 $\sqrt{A^T A}$（或 $AA^T$）的非零特征值

### 3.3 SVD的紧凑形式与截断形式

**紧凑SVD（Thin SVD）**：

$$A = U_r \Sigma_r V_r^T$$

其中 $U_r \in \mathbb{R}^{m \times r}$，$\Sigma_r \in \mathbb{R}^{r \times r}$，$V_r \in \mathbb{R}^{n \times r}$。

存储量：$r(m + n + 1)$，当 $r \ll \min(m, n)$ 时远小于 $mn$。

**截断SVD（最佳低秩逼近）**：保留前 $k$ 个奇异值：

$$A_k = U_k \Sigma_k V_k^T = \sum_{i=1}^{k} \sigma_i u_i v_i^T$$

### 3.4 Eckart-Young-Mirsky定理

**定理**：设 $\text{rank}(A) = r$，$k < r$，则

$$A_k = \arg\min_{\text{rank}(B) \leq k} \|A - B\|_F = \arg\min_{\text{rank}(B) \leq k} \|A - B\|_2$$

即截断 SVD 给出**在Frobenius范数和谱范数下同时最优**的秩 $k$ 逼近。

**误差**：

$$\|A - A_k\|_F = \sqrt{\sigma_{k+1}^2 + \cdots + \sigma_r^2}$$

$$\|A - A_k\|_2 = \sigma_{k+1}$$

**证明思路**（谱范数情形）：

设 $\text{rank}(B) \leq k$，则 $\dim(\text{Nul}(B)) \geq n - k$。由维数定理，$\text{Nul}(B) \cap \text{span}(v_1, \ldots, v_{k+1})$ 非平凡。

取 $x \in \text{Nul}(B) \cap \text{span}(v_1, \ldots, v_{k+1})$，$\|x\| = 1$，则

$$\|A - B\|_2 \geq \|(A - B)x\|_2 = \|Ax\|_2$$

$$x = \sum_{i=1}^{k+1} \alpha_i v_i, \quad \sum \alpha_i^2 = 1$$

$$\|Ax\|_2^2 = \sum_{i=1}^{k+1} \sigma_i^2 \alpha_i^2 \geq \sigma_{k+1}^2 \sum \alpha_i^2 = \sigma_{k+1}^2$$

### 3.5 SVD与伪逆

利用 SVD 计算伪逆：

$$A^+ = V \Sigma^+ U^T$$

其中 $\Sigma^+ = \text{diag}(\sigma_1^{-1}, \ldots, \sigma_r^{-1}, 0, \ldots, 0)$。

**最小二乘解**：$\min\|Ax - b\|_2$ 的最小范数解为 $x^* = A^+ b$。

### 3.6 SVD与矩阵范数

- $\|A\|_2 = \sigma_1$（最大奇异值）
- $\|A\|_F = \sqrt{\sigma_1^2 + \cdots + \sigma_r^2}$
- **条件数**：$\kappa_2(A) = \sigma_1 / \sigma_r$
- **核范数**（Nuclear Norm）：$\|A\|_* = \sigma_1 + \cdots + \sigma_r$（奇异值之和）

### 3.7 奇异值的几何不等式

**Weyl不等式**：设 $A, B \in \mathbb{R}^{m \times n}$，则

$$\sigma_{i+j-1}(A + B) \leq \sigma_i(A) + \sigma_j(B), \quad i + j - 1 \leq \min(m, n)$$

特别地，$\sigma_1(A + B) \leq \sigma_1(A) + \sigma_1(B)$。

**奇异值交错定理**：设 $A \in \mathbb{R}^{m \times n}$，$B$ 为 $A$ 删去一行/列得到的子矩阵，则

$$\sigma_1(A) \geq \sigma_1(B) \geq \sigma_2(A) \geq \sigma_2(B) \geq \cdots$$

### 3.8 SVD的计算方法

**两阶段法**：

1. **第一阶段**：通过 QR 分解 + Householder 变换将 $A$ 化为双对角矩阵 $B$：$A = U_1 B V_1^T$
2. **第二阶段**：对双对角矩阵 $B$ 用迭代方法（Golub-Kahan SVD 或隐式QR位移）求 SVD

$$A = (U_1 U_2) \Sigma (V_1 V_2)^T$$

**复杂度**：
- 化为双对角：$O(mn^2)$（$m \geq n$）
- 双对角 SVD 迭代：$O(n^2)$ 每步，通常需要几次到几十次迭代
