# 第七章 多维随机变量

## 1. 几何意义

### 1.1 多维随机向量的几何直觉

多维随机变量 $\mathbf{X} = (X_1, X_2, \ldots, X_n)^T$ 是从样本空间 $\Omega$ 到 $\mathbb{R}^n$ 的映射。其几何意义可以从以下角度理解：

- **概率密度曲面**：对于连续型二维随机变量 $(X, Y)$，联合密度函数 $f(x, y)$ 可以理解为 $\mathbb{R}^2$ 上方的一张"曲面"。曲面在点 $(x, y)$ 处的高度 $f(x, y)$ 反映了随机点落在 $(x, y)$ 附近的"概率密度"。整个曲面下的总体积为 1。

- **概率质量"山丘"**：三维空间中，密度曲面构成一个"山丘"。落在区域 $D$ 内的概率就是山丘在 $D$ 上方的体积：
$$P((X, Y) \in D) = \iint_D f(x, y) \, dx \, dy$$

### 1.2 边缘分布的几何意义

边缘分布 $f_X(x) = \int_{-\infty}^{+\infty} f(x, y) \, dy$ 的几何意义是：沿着 $y$ 方向对联合密度曲面做"投影"或"积分"。即将 $y$ 方向上的概率质量全部"压缩"到 $x$ 轴上。

- 可以想象为将三维的山丘沿着 $y$ 方向"推平"到 $x$-$z$ 平面上。

### 1.3 条件分布的几何意义

条件密度 $f_{X|Y}(x|y) = f(x, y) / f_Y(y)$ 的几何意义是：在 $Y = y$ 处对联合密度曲面做一个"切片"，然后将切片归一化（使面积/积分为 1）。

- 固定 $y$，$f(x, y)$ 在 $x$ 方向上的轮廓就是 $X$ 在 $Y = y$ 条件下的密度形状（乘以归一化常数）。

### 1.4 多维正态分布的几何意义

多维正态分布 $N(\boldsymbol{\mu}, \boldsymbol{\Sigma})$ 的密度函数等高线是**椭圆**（或超椭球面），其形状和方向由协方差矩阵 $\boldsymbol{\Sigma}$ 决定：

- **$\boldsymbol{\Sigma}$ 的特征向量**决定了椭圆的**主轴方向**；
- **$\boldsymbol{\Sigma}$ 的特征值**决定了椭圆在各主轴方向上的**半轴长度**；
- 当 $\boldsymbol{\Sigma}$ 为对角矩阵（各分量不相关）时，等高线是正椭圆（主轴与坐标轴平行）；
- 当 $\boldsymbol{\Sigma} = \sigma^2 \mathbf{I}$（各分量 i.i.d.）时，等高线是圆（或超球面）。

### 1.5 变换与雅可比行列式

对随机变量做变换 $\mathbf{Y} = g(\mathbf{X})$ 时，密度函数需要乘以雅可比行列式的绝对值。几何上，雅可比行列式衡量了变换对"体积元素"的伸缩因子：变换后的小区域面积等于原区域面积乘以 $|J|$。

---

## 2. 应用场景

### 2.1 多维正态分布的应用

- **多元统计分析**：主成分分析（PCA）、判别分析、聚类分析都基于多维正态模型。
- **信号处理**：多维高斯噪声的建模。
- **机器学习**：高斯混合模型（GMM）、高斯过程。
- **金融**：多维资产收益的联合建模（Markowitz 投资组合理论）。

### 2.2 边缘分布与条件分布

- **贝叶斯推断**：后验分布正比于似然乘以先验，条件分布在其中起核心作用。
- **缺失数据处理**：利用条件分布对缺失值进行插补。
- **图像处理**：马尔可夫随机场中的条件分布建模像素间的关系。

### 2.3 变换方法

- **Box-Muller 变换**：将两个独立均匀分布变换为两个独立标准正态分布。
- **统计量的分布推导**：利用变换方法推导 $\chi^2$、$t$、$F$ 分布。
- **Monte Carlo 方法**：通过逆变换法、拒绝采样法生成各种分布的随机数。

---

## 3. 数学理论（及推导）

### 3.1 多维随机向量的联合分布

**定义 3.1.1（联合分布函数）**：$n$ 维随机向量 $\mathbf{X} = (X_1, \ldots, X_n)^T$ 的联合分布函数为

$$F(\mathbf{x}) = F(x_1, \ldots, x_n) = P(X_1 \leq x_1, \ldots, X_n \leq x_n)$$

**联合密度函数**（连续型）：若存在 $f(\mathbf{x}) \geq 0$ 使得

$$F(\mathbf{x}) = \int_{-\infty}^{x_1} \cdots \int_{-\infty}^{x_n} f(t_1, \ldots, t_n) \, dt_n \cdots dt_1$$

则 $f$ 称为联合密度函数，满足 $\int_{\mathbb{R}^n} f(\mathbf{x}) \, d\mathbf{x} = 1$。

### 3.2 边缘分布

**边缘密度函数**：

$$f_{X_i}(x_i) = \int_{\mathbb{R}^{n-1}} f(x_1, \ldots, x_n) \, dx_1 \cdots dx_{i-1} \, dx_{i+1} \cdots dx_n$$

**二维情形**：

$$f_X(x) = \int_{-\infty}^{+\infty} f(x, y) \, dy, \quad f_Y(y) = \int_{-\infty}^{+\infty} f(x, y) \, dx$$

### 3.3 条件分布

**定义 3.3.1（条件密度函数）**：设 $f_Y(y) > 0$，则给定 $Y = y$ 时 $X$ 的条件密度函数为

$$f_{X|Y}(x|y) = \frac{f(x, y)}{f_Y(y)}$$

**条件分布函数**：

$$F_{X|Y}(x|y) = P(X \leq x | Y = y) = \int_{-\infty}^x f_{X|Y}(t|y) \, dt$$

**乘法公式**：

$$f(x, y) = f_{X|Y}(x|y) \cdot f_Y(y) = f_{Y|X}(y|x) \cdot f_X(x)$$

### 3.4 多维正态分布

**定义 3.4.1（多维正态分布）**：$n$ 维随机向量 $\mathbf{X}$ 服从**多维正态分布**（多元正态分布）$N(\boldsymbol{\mu}, \boldsymbol{\Sigma})$，若其密度函数为

$$f(\mathbf{x}) = \frac{1}{(2\pi)^{n/2} |\boldsymbol{\Sigma}|^{1/2}} \exp\left(-\frac{1}{2}(\mathbf{x} - \boldsymbol{\mu})^T \boldsymbol{\Sigma}^{-1} (\mathbf{x} - \boldsymbol{\mu})\right)$$

其中 $\boldsymbol{\mu} = (E[X_1], \ldots, E[X_n])^T \in \mathbb{R}^n$ 为均值向量，$\boldsymbol{\Sigma} = \mathrm{Cov}(\mathbf{X})$ 为 $n \times n$ 协方差矩阵，$|\boldsymbol{\Sigma}| = \det(\boldsymbol{\Sigma}) > 0$（要求 $\boldsymbol{\Sigma}$ 正定）。

**定义 3.4.2（特征函数刻画）**：$\mathbf{X} \sim N(\boldsymbol{\mu}, \boldsymbol{\Sigma})$ 当且仅当其特征函数为

$$\varphi_{\mathbf{X}}(\mathbf{t}) = \exp\left(i\mathbf{t}^T \boldsymbol{\mu} - \frac{1}{2} \mathbf{t}^T \boldsymbol{\Sigma} \mathbf{t}\right)$$

**定义 3.4.3（线性变换刻画）**：$\mathbf{X} \sim N(\boldsymbol{\mu}, \boldsymbol{\Sigma})$ 当且仅当对任意 $\mathbf{c} \in \mathbb{R}^n$，$\mathbf{c}^T \mathbf{X} \sim N(\mathbf{c}^T \boldsymbol{\mu}, \mathbf{c}^T \boldsymbol{\Sigma} \mathbf{c})$。

### 3.5 多维正态分布的性质（推导）

**性质 3.5.1（线性变换保持正态性）**：若 $\mathbf{X} \sim N(\boldsymbol{\mu}, \boldsymbol{\Sigma})$，$\mathbf{A}$ 为 $m \times n$ 矩阵（$\mathrm{rank}(\mathbf{A}) = m$），$\mathbf{b} \in \mathbb{R}^m$，则

$$\mathbf{Y} = \mathbf{A}\mathbf{X} + \mathbf{b} \sim N(\mathbf{A}\boldsymbol{\mu} + \mathbf{b}, \mathbf{A}\boldsymbol{\Sigma}\mathbf{A}^T)$$

**证明**：利用特征函数：

$$\varphi_{\mathbf{Y}}(\mathbf{t}) = E\left[e^{i\mathbf{t}^T(\mathbf{A}\mathbf{X}+\mathbf{b})}\right] = e^{i\mathbf{t}^T\mathbf{b}} E\left[e^{i(\mathbf{A}^T\mathbf{t})^T \mathbf{X}}\right]$$
$$= e^{i\mathbf{t}^T\mathbf{b}} \exp\left(i(\mathbf{A}^T\mathbf{t})^T \boldsymbol{\mu} - \frac{1}{2}(\mathbf{A}^T\mathbf{t})^T \boldsymbol{\Sigma}(\mathbf{A}^T\mathbf{t})\right)$$
$$= \exp\left(i\mathbf{t}^T(\mathbf{A}\boldsymbol{\mu}+\mathbf{b}) - \frac{1}{2}\mathbf{t}^T(\mathbf{A}\boldsymbol{\Sigma}\mathbf{A}^T)\mathbf{t}\right)$$

这正是 $N(\mathbf{A}\boldsymbol{\mu}+\mathbf{b}, \mathbf{A}\boldsymbol{\Sigma}\mathbf{A}^T)$ 的特征函数。$\blacksquare$

**性质 3.5.2（边缘分布）**：若 $\mathbf{X} \sim N(\boldsymbol{\mu}, \boldsymbol{\Sigma})$，将 $\mathbf{X}$ 分块为

$$\mathbf{X} = \begin{pmatrix} \mathbf{X}_1 \\ \mathbf{X}_2 \end{pmatrix}, \quad \boldsymbol{\mu} = \begin{pmatrix} \boldsymbol{\mu}_1 \\ \boldsymbol{\mu}_2 \end{pmatrix}, \quad \boldsymbol{\Sigma} = \begin{pmatrix} \boldsymbol{\Sigma}_{11} & \boldsymbol{\Sigma}_{12} \\ \boldsymbol{\Sigma}_{21} & \boldsymbol{\Sigma}_{22} \end{pmatrix}$$

则 $\mathbf{X}_1 \sim N(\boldsymbol{\mu}_1, \boldsymbol{\Sigma}_{11})$，$\mathbf{X}_2 \sim N(\boldsymbol{\mu}_2, \boldsymbol{\Sigma}_{22})$。

**证明**：取 $\mathbf{A} = (\mathbf{I}, \mathbf{0})$（适当大小），$\mathbf{Y} = \mathbf{A}\mathbf{X} = \mathbf{X}_1$，由性质 3.5.1 即得。$\blacksquare$

**性质 3.5.3（条件分布）**：在上述分块下，条件分布为

$$\mathbf{X}_1 | \mathbf{X}_2 = \mathbf{x}_2 \sim N\left(\boldsymbol{\mu}_1 + \boldsymbol{\Sigma}_{12}\boldsymbol{\Sigma}_{22}^{-1}(\mathbf{x}_2 - \boldsymbol{\mu}_2), \quad \boldsymbol{\Sigma}_{11} - \boldsymbol{\Sigma}_{12}\boldsymbol{\Sigma}_{22}^{-1}\boldsymbol{\Sigma}_{21}\right)$$

**证明思路**：通过配方（completing the square）可以验证条件密度具有上述形式。$\blacksquare$

**性质 3.5.4（不相关即独立）**：对多维正态分布，$\mathbf{X}_1$ 与 $\mathbf{X}_2$ 不相关（$\boldsymbol{\Sigma}_{12} = \mathbf{0}$）当且仅当 $\mathbf{X}_1$ 与 $\mathbf{X}_2$ 独立。

**证明**：若 $\boldsymbol{\Sigma}_{12} = \mathbf{0}$，则 $\boldsymbol{\Sigma} = \begin{pmatrix} \boldsymbol{\Sigma}_{11} & \mathbf{0} \\ \mathbf{0} & \boldsymbol{\Sigma}_{22} \end{pmatrix}$（分块对角），$|\boldsymbol{\Sigma}| = |\boldsymbol{\Sigma}_{11}| \cdot |\boldsymbol{\Sigma}_{22}|$，$\boldsymbol{\Sigma}^{-1} = \begin{pmatrix} \boldsymbol{\Sigma}_{11}^{-1} & \mathbf{0} \\ \mathbf{0} & \boldsymbol{\Sigma}_{22}^{-1} \end{pmatrix}$。代入密度函数：

$$f(\mathbf{x}_1, \mathbf{x}_2) = \frac{1}{(2\pi)^{n/2}|\boldsymbol{\Sigma}_{11}|^{1/2}|\boldsymbol{\Sigma}_{22}|^{1/2}} \exp\left(-\frac{1}{2}(\mathbf{x}_1-\boldsymbol{\mu}_1)^T \boldsymbol{\Sigma}_{11}^{-1}(\mathbf{x}_1-\boldsymbol{\mu}_1)\right) \exp\left(-\frac{1}{2}(\mathbf{x}_2-\boldsymbol{\mu}_2)^T \boldsymbol{\Sigma}_{22}^{-1}(\mathbf{x}_2-\boldsymbol{\mu}_2)\right)$$
$$= f_{\mathbf{X}_1}(\mathbf{x}_1) \cdot f_{\mathbf{X}_2}(\mathbf{x}_2) \quad \blacksquare$$

**注**：这个性质是正态分布特有的。一般情况下，不相关不蕴含独立。

**性质 3.5.5（可加性）**：若 $\mathbf{X} \sim N(\boldsymbol{\mu}_1, \boldsymbol{\Sigma}_1)$，$\mathbf{Y} \sim N(\boldsymbol{\mu}_2, \boldsymbol{\Sigma}_2)$ 独立，则

$$\mathbf{X} + \mathbf{Y} \sim N(\boldsymbol{\mu}_1 + \boldsymbol{\mu}_2, \boldsymbol{\Sigma}_1 + \boldsymbol{\Sigma}_2)$$

### 3.6 协方差矩阵的性质

**定理 3.6.1**：协方差矩阵 $\boldsymbol{\Sigma}$ 具有以下性质：

1. **对称性**：$\boldsymbol{\Sigma}^T = \boldsymbol{\Sigma}$（因为 $\mathrm{Cov}(X_i, X_j) = \mathrm{Cov}(X_j, X_i)$）。
2. **半正定性**：$\boldsymbol{\Sigma} \succeq 0$，即对任意 $\mathbf{c} \in \mathbb{R}^n$，$\mathbf{c}^T \boldsymbol{\Sigma} \mathbf{c} \geq 0$。

**证明**：$\mathbf{c}^T \boldsymbol{\Sigma} \mathbf{c} = \sum_{i,j} c_i \mathrm{Cov}(X_i, X_j) c_j = \mathrm{Var}\left(\sum_i c_i X_i\right) \geq 0$。$\blacksquare$

3. **对角元素非负**：$\boldsymbol{\Sigma}_{ii} = \mathrm{Var}(X_i) \geq 0$。
4. **行列式非负**：$\det(\boldsymbol{\Sigma}) \geq 0$（半正定矩阵的行列式非负）。
5. **Cholesky 分解**：若 $\boldsymbol{\Sigma}$ 正定，则存在下三角矩阵 $\mathbf{L}$ 使得 $\boldsymbol{\Sigma} = \mathbf{L}\mathbf{L}^T$。
6. **谱分解**：$\boldsymbol{\Sigma} = \mathbf{Q} \boldsymbol{\Lambda} \mathbf{Q}^T$，其中 $\mathbf{Q}$ 为正交矩阵（特征向量），$\boldsymbol{\Lambda} = \mathrm{diag}(\lambda_1, \ldots, \lambda_n)$（特征值），$\lambda_i \geq 0$。

**相关系数矩阵**：$\mathbf{R} = \mathbf{D}^{-1} \boldsymbol{\Sigma} \mathbf{D}^{-1}$，其中 $\mathbf{D} = \mathrm{diag}(\sigma_1, \ldots, \sigma_n)$。$\mathbf{R}$ 的对角元素全为 1，非对角元素为 $\rho_{ij} = \mathrm{Corr}(X_i, X_j)$。

### 3.7 独立性判定

**定理 3.7.1（独立性等价条件）**：以下各条等价：

1. $X$ 与 $Y$ 独立；
2. $f(x, y) = f_X(x) f_Y(y)$（几乎处处）；
3. $f_{X|Y}(x|y) = f_X(x)$（几乎处处）；
4. $F(x, y) = F_X(x) F_Y(y)$（对所有 $x, y$）；
5. 对所有 Borel 可测函数 $g, h$：$E[g(X)h(Y)] = E[g(X)] E[h(Y)]$。

**多维正态的特殊性质**：对于 $\mathbf{X} \sim N(\boldsymbol{\mu}, \boldsymbol{\Sigma})$，$X_i$ 与 $X_j$ 独立 $\Leftrightarrow$ $\rho_{ij} = 0$ $\Leftrightarrow$ $\Sigma_{ij} = 0$。

### 3.8 变换与雅可比行列式法

**定理 3.8.1（变量替换公式）**：设 $\mathbf{X} = (X_1, X_2)$ 具有联合密度 $f_{\mathbf{X}}(\mathbf{x})$。设变换

$$\mathbf{Y} = g(\mathbf{X}), \quad \begin{pmatrix} Y_1 \\ Y_2 \end{pmatrix} = \begin{pmatrix} g_1(X_1, X_2) \\ g_2(X_1, X_2) \end{pmatrix}$$

是一一对应的（双射），且 $g$ 具有连续偏导数。则 $\mathbf{Y}$ 的联合密度为

$$f_{\mathbf{Y}}(\mathbf{y}) = f_{\mathbf{X}}(g^{-1}(\mathbf{y})) \cdot |J|$$

其中 $J$ 是变换的**雅可比行列式**：

$$J = \frac{\partial(x_1, x_2)}{\partial(y_1, y_2)} = \det \begin{pmatrix} \frac{\partial x_1}{\partial y_1} & \frac{\partial x_1}{\partial y_2} \\ \frac{\partial x_2}{\partial y_1} & \frac{\partial x_2}{\partial y_2} \end{pmatrix}$$

**例 3.8.1（Box-Muller 变换）**：设 $U_1, U_2$ i.i.d. $\sim U(0, 1)$，令

$$X_1 = \sqrt{-2\ln U_1} \cos(2\pi U_2), \quad X_2 = \sqrt{-2\ln U_1} \sin(2\pi U_2)$$

则 $X_1, X_2$ i.i.d. $\sim N(0, 1)$。

**推导**：反变换为 $U_1 = e^{-(X_1^2+X_2^2)/2}$，$U_2 = \frac{1}{2\pi}\arctan(X_2/X_1)$。雅可比行列式：

$$|J| = \frac{1}{2\pi} e^{-(x_1^2+x_2^2)/2}$$

$U_1, U_2$ 的联合密度为 $f(u_1, u_2) = 1$（$0 < u_1, u_2 < 1$），故

$$f(x_1, x_2) = 1 \cdot \frac{1}{2\pi} e^{-(x_1^2+x_2^2)/2} = \frac{1}{\sqrt{2\pi}} e^{-x_1^2/2} \cdot \frac{1}{\sqrt{2\pi}} e^{-x_2^2/2}$$

即 $X_1, X_2$ 独立且均服从 $N(0, 1)$。$\blacksquare$

### 3.9 极坐标变换的应用

对于二维正态变量 $(X, Y)$，常利用极坐标变换 $X = R\cos\theta$，$Y = R\sin\theta$ 来推导 $\chi^2$ 分布。若 $X, Y$ i.i.d. $N(0, 1)$，则 $R^2 = X^2 + Y^2 \sim \chi^2(2) = \mathrm{Exp}(1/2)$，$\theta \sim U(0, 2\pi)$，且 $R$ 与 $\theta$ 独立。

**推导**：$(X, Y)$ 的联合密度为 $\frac{1}{2\pi} e^{-(x^2+y^2)/2}$。极坐标变换的雅可比行列式为 $r$，故 $(R, \theta)$ 的联合密度为

$$f(r, \theta) = \frac{1}{2\pi} e^{-r^2/2} \cdot r = \underbrace{\frac{1}{2\pi}}_{f(\theta)} \cdot \underbrace{r e^{-r^2/2}}_{f(r)}, \quad r > 0, \, 0 < \theta < 2\pi$$

密度可分解，故 $R$ 与 $\theta$ 独立。$\theta \sim U(0, 2\pi)$，$R$ 的密度为 $r e^{-r^2/2}$。令 $Z = R^2$，由变换公式 $f_Z(z) = \frac{1}{2} e^{-z/2}$（$z > 0$），即 $\mathrm{Exp}(1/2) = \chi^2(2)$。$\blacksquare$
