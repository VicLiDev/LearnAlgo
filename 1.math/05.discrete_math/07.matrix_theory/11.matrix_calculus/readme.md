# 第十一章 矩阵微积分

## 1. 几何意义

矩阵微积分将标量的微积分概念推广到矩阵变量。核心问题：当矩阵的元素发生微小变化时，依赖它的函数如何变化？

**几何直觉**：

- 标量对向量的导数 $\nabla f(x)$：指向函数增长最快的方向（梯度）
- 标量对矩阵的导数 $\frac{\partial f}{\partial X}$：一个矩阵，每个元素表示函数对该位置变化的敏感度
- 矩阵对矩阵的导数：一个四维张量，但在实践中通常通过**向量化**降维处理

---

## 2. 应用场景

| 领域 | 应用 |
|------|------|
| 机器学习 | 梯度下降中损失函数对权重矩阵的导数 |
| 深度学习 | 反向传播的本质是链式法则在矩阵上的应用 |
| 统计学 | MLE中似然函数对参数矩阵的导数 |
| 优化理论 | Newton法中Hessian矩阵的计算 |
| 控制理论 | 灵敏度分析 |
| 计量经济学 | GLS估计中的矩阵导数 |

---

## 3. 数学理论

### 3.1 标量对向量的导数

设 $f : \mathbb{R}^n \to \mathbb{R}$，梯度定义为

$$\nabla f(x) = \frac{\partial f}{\partial x} = \begin{pmatrix} \frac{\partial f}{\partial x_1} \\ \vdots \\ \frac{\partial f}{\partial x_n} \end{pmatrix}$$

**常用公式**：

| $f(x)$ | $\nabla f(x)$ |
|---------|---------------|
| $a^T x$ | $a$ |
| $x^T A x$（$A$ 对称） | $2Ax$ |
| $x^T x$ | $2x$ |
| $\|x\|_2$ | $x / \|x\|_2$ |
| $\|Ax - b\|_2^2$ | $2A^T(Ax - b)$ |

**推导** $x^T A x$（$A$ 对称）：

$$f = \sum_{i,j} a_{ij} x_i x_j$$

$$\frac{\partial f}{\partial x_k} = \sum_j a_{kj} x_j + \sum_i a_{ik} x_i = (Ax)_k + (A^T x)_k = 2(Ax)_k$$

### 3.2 标量对矩阵的导数

设 $f : \mathbb{R}^{m \times n} \to \mathbb{R}$，导数定义为同阶矩阵：

$$\left[\frac{\partial f}{\partial X}\right]_{ij} = \frac{\partial f}{\partial X_{ij}}$$

**常用公式**：

| $f(X)$ | $\frac{\partial f}{\partial X}$ |
|---------|-------------------------------|
| $\text{tr}(X)$ | $I$ |
| $\text{tr}(AX)$ | $A^T$ |
| $\text{tr}(X^T A)$ | $A$ |
| $\text{tr}(AX^T)$ | $A$ |
| $a^T X b$ | $ab^T$ |
| $\text{tr}(X^T X)$ | $2X$ |
| $\det(X)$ | $\det(X)(X^{-1})^T$ |
| $\log\det(X)$ | $(X^{-1})^T$ |

**推导** $\frac{\partial}{\partial X}\text{tr}(AX) = A^T$：

$$\text{tr}(AX) = \sum_{i,j} a_{ij} x_{ji}$$

$$\frac{\partial}{\partial x_{kl}} \text{tr}(AX) = a_{lk} = (A^T)_{kl}$$

**推导** $\frac{\partial}{\partial X}\log\det(X)$（$X$ 可逆）：

$$\frac{\partial}{\partial X_{ij}} \log\det(X) = \frac{1}{\det(X)} \frac{\partial \det(X)}{\partial X_{ij}}$$

由 Jacobi 公式 $d\det(X) = \det(X) \text{tr}(X^{-1} dX)$：

$$\frac{\partial \det(X)}{\partial X_{ij}} = \det(X) (X^{-T})_{ij}$$

$$\frac{\partial \log\det(X)}{\partial X_{ij}} = (X^{-T})_{ij}$$

故 $\frac{\partial}{\partial X}\log\det(X) = X^{-T}$。

### 3.3 矩阵的微分与一阶展开

**矩阵微分**：$df$ 表示 $f$ 的线性主部（一阶变分）。

**基本微分法则**：
- $d(X + Y) = dX + dY$
- $d(\alpha X) = \alpha \cdot dX$
- $d(XY) = (dX)Y + X(dY)$（乘积法则）
- $d(X^{-1}) = -X^{-1}(dX)X^{-1}$

**推导逆矩阵微分**：对 $XX^{-1} = I$ 两端微分：

$$dX \cdot X^{-1} + X \cdot d(X^{-1}) = 0$$

$$d(X^{-1}) = -X^{-1}(dX)X^{-1}$$

**常用微分公式**：

| $f(X)$ | $df$ |
|---------|------|
| $a^T X b$ | $a^T (dX) b$ |
| $\text{tr}(AX)$ | $\text{tr}(A \, dX)$ |
| $\text{tr}(X^T X)$ | $2\text{tr}(X^T dX)$ |
| $\det(X)$ | $\det(X)\text{tr}(X^{-1}dX)$ |
| $\log\det(X)$ | $\text{tr}(X^{-1}dX)$ |
| $\text{tr}(X^{-1}A)$ | $-\text{tr}(X^{-1}(dX)X^{-1}A)$ |

### 3.4 链式法则

**标量函数的链式法则**：

$$\frac{\partial f(g(X))}{\partial X} = \text{tr}\left(\frac{\partial f}{\partial g} \cdot \frac{\partial g}{\partial X}\right)$$

在实践中，更方便的做法是先求微分 $df$，再用恒等式 $df = \text{tr}(A^T dX) \implies \frac{\partial f}{\partial X} = A$ 提取梯度。

**示例**：求 $\frac{\partial}{\partial X}\|AX - B\|_F^2$。

$$f = \text{tr}((AX - B)^T(AX - B)) = \text{tr}(X^T A^T AX - X^T A^T B - B^T AX + B^T B)$$

$$df = \text{tr}(dX^T A^T AX + X^T A^T A dX - dX^T A^T B - B^T A dX)$$

利用 $\text{tr}(U) = \text{tr}(U^T)$ 合并同类项：

$$df = 2\text{tr}(X^T A^T A dX - B^T A dX) = 2\text{tr}((A^T AX - A^T B)^T dX)$$

$$\frac{\partial f}{\partial X} = 2(A^T AX - A^T B)$$

### 3.5 向量对向量的导数（Jacobian矩阵）

设 $f : \mathbb{R}^n \to \mathbb{R}^m$，Jacobian矩阵为

$$J = \frac{\partial f}{\partial x} = \begin{pmatrix} \frac{\partial f_1}{\partial x_1} & \cdots & \frac{\partial f_1}{\partial x_n} \\ \vdots & \ddots & \vdots \\ \frac{\partial f_m}{\partial x_1} & \cdots & \frac{\partial f_m}{\partial x_n} \end{pmatrix} \in \mathbb{R}^{m \times n}$$

**链式法则**：$f(g(x))$ 的 Jacobian 为

$$\frac{\partial f}{\partial x} = \frac{\partial f}{\partial g} \cdot \frac{\partial g}{\partial x} = J_f \cdot J_g$$

**常用 Jacobian**：

| $f(x)$ | Jacobian $J$ |
|---------|-------------|
| $Ax$ | $A$ |
| $a^T x$ | $a^T$ |
| $x^T A x$ | $x^T(A + A^T)$ |

### 3.6 矩阵微分的应用：最小二乘的梯度推导

**问题**：$\min_X \|AX - B\|_F^2$，求梯度。

$$f(X) = \text{tr}((AX - B)^T(AX - B))$$

$$df = 2\text{tr}((AX - B)^T A \, dX)$$

$$\nabla_X f = 2A^T(AX - B)$$

令梯度为零：$2A^T(AX - B) = 0 \implies A^TAX = A^TB$（正规方程）。
