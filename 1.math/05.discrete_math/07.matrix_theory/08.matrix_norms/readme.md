# 第八章 向量范数与矩阵范数

## 1. 几何意义

范数是对向量或矩阵"大小"的度量，是欧几里得长度在更一般空间的推广。

**向量范数的几何含义**：

- $\ell_1$ 范数：曼哈顿距离，"沿街道走"的路径长度
- $\ell_2$ 范数：欧几里得直线距离（"鸟飞"的距离）
- $\ell_\infty$ 范数：各分量中绝对值最大的那个，"最远坐标"

单位球形状：
- $\ell_1$：菱形（2D）/ 八面体（3D）
- $\ell_2$：圆/球
- $\ell_\infty$：正方形/立方体

**矩阵范数的几何含义**：矩阵范数 $\|A\|$ 度量的是变换 $A$ 的**最大拉伸比**——输入空间中单位球经变换后，输出空间中像的最大"半径"。

---

## 2. 应用场景

| 领域 | 应用 |
|------|------|
| 数值分析 | 误差估计、收敛性分析 |
| 优化理论 | 梯度下降的收敛速度与Lipschitz常数相关 |
| 机器学习 | 正则化项（$L_1$、$L_2$ 范数）防止过拟合 |
| 控制理论 | $H_\infty$ 范数用于鲁棒控制设计 |
| 信号处理 | 信号能量的度量 |
| 压缩感知 | $L_1$ 范数最小化用于稀疏信号恢复 |

---

## 3. 数学理论

### 3.1 向量范数

**定义**：$\mathbb{R}^n$ 上的范数 $\|\cdot\|$ 满足：
1. **正定性**：$\|x\| \geq 0$，等号当且仅当 $x = 0$
2. **齐次性**：$\|\alpha x\| = |\alpha| \|x\|$
3. **三角不等式**：$\|x + y\| \leq \|x\| + \|y\|$

**常用 $\ell_p$ 范数**：

$$\|x\|_p = \left(\sum_{i=1}^{n} |x_i|^p\right)^{1/p}, \quad 1 \leq p < \infty$$

$$\|x\|_\infty = \max_{i} |x_i|$$

**Hölder不等式**：$\|x^T y\| \leq \|x\|_p \|y\|_q$，其中 $\frac{1}{p} + \frac{1}{q} = 1$。

**Minkowski不等式**（三角不等式的推广）：$\|x + y\|_p \leq \|x\|_p + \|y\|_p$。

### 3.2 向量范数的等价性

**定理**：有限维空间中所有范数等价。即对任意两种范数 $\|\cdot\|_a$ 和 $\|\cdot\|_b$，存在常数 $c_1, c_2 > 0$ 使得

$$c_1 \|x\|_a \leq \|x\|_b \leq c_2 \|x\|_a, \quad \forall x \neq 0$$

**常用等价关系**（$n$ 维空间）：

$$\|x\|_2 \leq \|x\|_1 \leq \sqrt{n} \|x\|_2$$

$$\|x\|_\infty \leq \|x\|_2 \leq \sqrt{n} \|x\|_\infty$$

$$\frac{1}{\sqrt{n}}\|x\|_1 \leq \|x\|_2 \leq \|x\|_1$$

### 3.3 由向量范数诱导的矩阵范数

**定义**：设 $\|\cdot\|$ 为向量范数，则由其诱导的矩阵范数为

$$\|A\| = \max_{x \neq 0} \frac{\|Ax\|}{\|x\|} = \max_{\|x\|=1} \|Ax\|$$

**几何含义**：矩阵范数等于单位球在变换 $A$ 下的像的最大半径。

**诱导范数自动满足的性质**：
- $\|AB\| \leq \|A\| \cdot \|B\|$（次乘性）
- $\|I\| = 1$
- $\|Ax\| \leq \|A\| \cdot \|x\|$

### 3.4 常用矩阵诱导范数

**1-范数（最大列和）**：

$$\|A\|_1 = \max_{1 \leq j \leq n} \sum_{i=1}^{m} |a_{ij}|$$

**推导**：$\|Ax\|_1 = \sum_i |\sum_j a_{ij} x_j| \leq \sum_i \sum_j |a_{ij}| |x_j| = \sum_j |x_j| \sum_i |a_{ij}| \leq \max_j \sum_i |a_{ij}| \cdot \|x\|_1$

等号在取 $x = e_k$（最大列和对应的列）时成立。

**$\infty$-范数（最大行和）**：

$$\|A\|_\infty = \max_{1 \leq i \leq m} \sum_{j=1}^{n} |a_{ij}|$$

**2-范数（谱范数）**：

$$\|A\|_2 = \sigma_{\max}(A) = \sqrt{\lambda_{\max}(A^T A)}$$

**推导**：$\|A\|_2^2 = \max_{\|x\|_2=1} \|Ax\|_2^2 = \max_{\|x\|_2=1} x^T A^T A x$

由 Rayleigh-Ritz 定理，$A^T A$ 的最大特征值即为 $\sigma_1^2$。

### 3.5 Frobenius范数

$$\|A\|_F = \sqrt{\sum_{i=1}^{m} \sum_{j=1}^{n} |a_{ij}|^2} = \sqrt{\text{tr}(A^T A)}$$

**性质**：
- $\|A\|_F = \sqrt{\sigma_1^2 + \cdots + \sigma_r^2}$（奇异值的关系）
- $\|A\|_F = \|A^T\|_F$
- $\|A\|_F$ 满足次乘性：$\|AB\|_F \leq \|A\|_F \|B\|_F$
- $\|A\|_F$ **不是**诱导范数（当 $n > 1$ 时）
- 与2-范数的关系：$\|A\|_2 \leq \|A\|_F \leq \sqrt{r} \|A\|_2$

### 3.6 矩阵的条件数

**定义**：矩阵 $A$ 关于范数 $\|\cdot\|$ 的条件数为

$$\kappa(A) = \|A\| \cdot \|A^{-1}\|$$

（对非方阵或奇异矩阵，用伪逆替代 $A^{-1}$。）

**关于条件数的误差放大**：

求解 $Ax = b$ 时，设 $b$ 有扰动 $\delta b$，解的扰动 $\delta x$ 满足

$$\frac{\|\delta x\|}{\|x\|} \leq \kappa(A) \frac{\|\delta b\|}{\|b\|}$$

若 $A$ 也有扰动 $\delta A$，则

$$\frac{\|\delta x\|}{\|x + \delta x\|} \leq \frac{\kappa(A) \cdot \frac{\|\delta A\|}{\|A\|}}{1 - \kappa(A) \cdot \frac{\|\delta A\|}{\|A\|}}$$

**推导（右端扰动情形）**：

$A(x + \delta x) = b + \delta b \implies A \delta x = \delta b \implies \delta x = A^{-1} \delta b$

$$\|\delta x\| \leq \|A^{-1}\| \|\delta b\|, \quad \|b\| = \|Ax\| \leq \|A\| \|x\|$$

$$\frac{\|\delta x\|}{\|x\|} \leq \|A^{-1}\| \|A\| \frac{\|\delta b\|}{\|b\|} = \kappa(A) \frac{\|\delta b\|}{\|b\|}$$

**条件数的意义**：
- $\kappa(A) = 1$：最优（正交矩阵）
- $\kappa(A)$ 小：良态（well-conditioned）
- $\kappa(A)$ 大：病态（ill-conditioned），解对误差极度敏感
- 关于2-范数：$\kappa_2(A) = \sigma_{\max} / \sigma_{\min}$
