# 第三章 数字特征

## 1. 几何意义

### 1.1 数学期望的几何直觉

数学期望（均值）$E[X]$ 的几何意义可以从多个角度理解：

- **质心 / 重心**：将随机变量的分布视为一个"质量系统"，各取值处的概率（或密度）就是"质量"。$E[X]$ 就是该质量系统的重心位置。对于离散型，$E[X] = \sum x_k p(x_k)$ 类似于加权平均；对于连续型，$E[X] = \int x f(x) \, dx$ 类似于质心的一阶矩。

- **分布的"中心"**：期望是分布围绕其"展开"的中心点。正态分布 $N(\mu, \sigma^2)$ 的期望 $\mu$ 正是其密度曲线的对称轴。

- **线性泛函**：在 $L^1$ 空间中，期望是线性泛函 $E: L^1 \to \mathbb{R}$，满足 $E[aX + bY] = aE[X] + bE[Y]$。

### 1.2 方差的几何直觉

方差 $\mathrm{Var}(X)$ 的几何意义：

- **散布程度**：方差衡量随机变量的取值围绕期望的"分散"程度。方差越大，分布越"分散"。
- **二阶中心矩**：$\mathrm{Var}(X) = E[(X - E[X])^2]$ 就是分布关于重心的"转动惯量"。
- **$L^2$ 范数**：在 $L^2$ 空间中，$\mathrm{Var}(X) = \|X - E[X]\|_{L^2}^2$，即 $X$ 到其期望的距离的平方。

### 1.3 相关系数的几何意义

相关系数 $\rho(X, Y)$ 的几何意义：

- **方向余弦**：在 $L^2$ 空间中，将 $X - E[X]$ 和 $Y - E[Y]$ 视为向量，$\rho(X, Y)$ 就是这两个向量之间夹角的余弦值：
$$\rho(X, Y) = \frac{\mathrm{Cov}(X, Y)}{\sqrt{\mathrm{Var}(X)} \cdot \sqrt{\mathrm{Var}(Y)}} = \cos \theta$$

- 当 $\rho = 1$ 时，$X - E[X]$ 与 $Y - E[Y]$ 同方向（完全正相关）；
- 当 $\rho = -1$ 时，方向相反（完全负相关）；
- 当 $\rho = 0$ 时，正交（不相关）。

### 1.4 Jensen 不等式的几何直觉

Jensen 不等式说明，对于凸函数 $\varphi$，$E[\varphi(X)] \geq \varphi(E[X])$。几何上，凸函数的图像在其切线的上方。$E[\varphi(X)]$ 可以理解为分布中各点在凸函数上的"加权平均高度"，而 $\varphi(E[X])$ 是期望点处的高度。由于凸函数曲线向上弯曲，前者总是大于后者。

---

## 2. 应用场景

### 2.1 期望与方差的应用

- **风险评估**：投资组合的期望收益（$E[R]$）与风险（$\mathrm{Var}(R)$ 或 $\sigma_R$）是金融中最重要的两个指标。
- **质量控制**：产品尺寸的期望应等于设计目标值，方差越小质量越稳定。
- **蒙特卡洛方法**：用随机变量的期望来估计积分值。

### 2.2 协方差与相关系数的应用

- **投资分散化**：选择相关系数低的资产组合以降低风险。
- **数据分析**：Pearson 相关系数衡量两个变量线性关系的强度。
- **信号处理**：协方差用于分析噪声与信号的相关性。

### 2.3 Jensen 不等式的应用

- **信息论**：证明 $D_{KL}(P \| Q) \geq 0$（KL 散度的非负性）。
- **金融学**：证明风险厌恶投资者的效用函数是凹的，从而 $E[u(W)] \leq u(E[W])$。
- **统计学**：证明 AM-GM 不等式等。

---

## 3. 数学理论（及推导）

### 3.1 数学期望

**定义 3.1.1（离散型随机变量的期望）**：设 $X$ 为离散型随机变量，取值 $\{x_1, x_2, \ldots\}$，概率质量函数为 $p(x_k)$。若 $\sum_k |x_k| p(x_k) < \infty$，则

$$E[X] = \sum_k x_k \, p(x_k)$$

**定义 3.1.2（连续型随机变量的期望）**：设 $X$ 为连续型随机变量，密度函数为 $f(x)$。若 $\int_{-\infty}^{+\infty} |x| f(x) \, dx < \infty$，则

$$E[X] = \int_{-\infty}^{+\infty} x \, f(x) \, dx$$

**定义 3.1.3（一般随机变量的期望——Lebesgue 积分）**：

$$E[X] = \int_\Omega X(\omega) \, dP(\omega)$$

**绝对可积条件**：要求 $E[|X|] < \infty$（即 $X \in L^1(P)$），以保证期望定义良好，不受求和/积分顺序的影响。

### 3.2 期望的性质（推导）

**性质 3.2.1（线性性）**：设 $X, Y \in L^1$，$a, b \in \mathbb{R}$，则

$$E[aX + bY] = aE[X] + bE[Y]$$

**性质 3.2.2（单调性）**：若 $X \leq Y$（a.s.），则 $E[X] \leq E[Y]$。

**性质 3.2.3（期望的期望 / 全期望公式的特殊情形）**：若 $E[X]$ 存在，$g$ 为 Borel 可测函数，则

$$E[g(X)] = \begin{cases} \displaystyle\sum_k g(x_k) p(x_k), & \text{离散型} \\[10pt] \displaystyle\int_{-\infty}^{+\infty} g(x) f(x) \, dx, & \text{连续型} \end{cases}$$

**证明**（离散型 Lottery Lemma）：$E[g(X)] = \sum_k g(x_k) P(X = x_k)$ 可由期望的定义和可测函数积分的定义直接得到。$\blacksquare$

**性质 3.2.4（独立性下的乘积）**：若 $X$ 与 $Y$ 独立且 $E[|X|], E[|Y|] < \infty$，则

$$E[XY] = E[X] \cdot E[Y]$$

**证明**（连续型）：$X, Y$ 独立意味着 $f(x, y) = f_X(x) f_Y(y)$，故

$$E[XY] = \iint_{\mathbb{R}^2} xy \, f(x, y) \, dx \, dy = \int_{-\infty}^{+\infty} x f_X(x) \, dx \cdot \int_{-\infty}^{+\infty} y f_Y(y) \, dy = E[X] \cdot E[Y] \quad \blacksquare$$

### 3.3 方差

**定义 3.3.1（方差）**：设 $E[X^2] < \infty$，则

$$\mathrm{Var}(X) = E\left[(X - E[X])^2\right] = E[X^2] - (E[X])^2$$

**标准差**：$\sigma_X = \sqrt{\mathrm{Var}(X)}$。

**定理 3.3.1（方差的计算公式推导）**：

$$\mathrm{Var}(X) = E[X^2] - (E[X])^2$$

**证明**：

$$\mathrm{Var}(X) = E\left[(X - E[X])^2\right] = E[X^2 - 2XE[X] + (E[X])^2]$$
$$= E[X^2] - 2E[X] \cdot E[X] + (E[X])^2 = E[X^2] - (E[X])^2 \quad \blacksquare$$

### 3.4 方差的性质（推导）

**性质 3.4.1（非负性）**：$\mathrm{Var}(X) \geq 0$，等号成立当且仅当 $X = E[X]$（a.s.，即 $X$ 为退化随机变量）。

**性质 3.4.2（平移不变性）**：$\mathrm{Var}(X + c) = \mathrm{Var}(X)$，$c \in \mathbb{R}$。

**证明**：$E[X + c] = E[X] + c$，故

$$\mathrm{Var}(X + c) = E[(X + c - E[X] - c)^2] = E[(X - E[X])^2] = \mathrm{Var}(X) \quad \blacksquare$$

**性质 3.4.3（缩放性）**：$\mathrm{Var}(aX) = a^2 \mathrm{Var}(X)$，$a \in \mathbb{R}$。

**证明**：$E[aX] = aE[X]$，故

$$\mathrm{Var}(aX) = E[(aX - aE[X])^2] = E[a^2(X - E[X])^2] = a^2 \mathrm{Var}(X) \quad \blacksquare$$

**性质 3.4.4（独立变量的方差可加性）**：若 $X$ 与 $Y$ 独立，则

$$\mathrm{Var}(X + Y) = \mathrm{Var}(X) + \mathrm{Var}(Y)$$

**证明**：利用协方差（见下一节），$\mathrm{Var}(X + Y) = \mathrm{Var}(X) + \mathrm{Var}(Y) + 2\mathrm{Cov}(X, Y)$，而独立变量 $\mathrm{Cov}(X, Y) = 0$。$\blacksquare$

**推广**：若 $X_1, X_2, \ldots, X_n$ 两两独立，则

$$\mathrm{Var}\left(\sum_{k=1}^{n} X_k\right) = \sum_{k=1}^{n} \mathrm{Var}(X_k)$$

### 3.5 协方差与相关系数

**定义 3.5.1（协方差）**：

$$\mathrm{Cov}(X, Y) = E\left[(X - E[X])(Y - E[Y])\right] = E[XY] - E[X] \cdot E[Y]$$

**计算公式的推导**：

$$\mathrm{Cov}(X, Y) = E[XY - XE[Y] - YE[X] + E[X]E[Y]]$$
$$= E[XY] - E[X]E[Y] - E[Y]E[X] + E[X]E[Y] = E[XY] - E[X]E[Y] \quad \blacksquare$$

**定义 3.5.2（相关系数）**：

$$\rho(X, Y) = \frac{\mathrm{Cov}(X, Y)}{\sqrt{\mathrm{Var}(X)} \cdot \sqrt{\mathrm{Var}(Y)}} = \frac{\mathrm{Cov}(X, Y)}{\sigma_X \sigma_Y}$$

（要求 $\mathrm{Var}(X) > 0$ 且 $\mathrm{Var}(Y) > 0$。）

**定理 3.5.1（Cauchy-Schwarz 不等式）**：若 $E[X^2], E[Y^2] < \infty$，则

$$(E[XY])^2 \leq E[X^2] \cdot E[Y^2]$$

等号成立当且仅当存在常数 $c$ 使得 $Y = cX$（a.s.）或 $X = cY$（a.s.）。

**证明**：对任意 $t \in \mathbb{R}$，定义 $g(t) = E[(X + tY)^2] = E[X^2] + 2tE[XY] + t^2 E[Y^2] \geq 0$。

由于 $g(t) \geq 0$ 对所有 $t$ 成立，其判别式非正：

$$\Delta = (2E[XY])^2 - 4E[X^2] \cdot E[Y^2] \leq 0$$

即 $(E[XY])^2 \leq E[X^2] \cdot E[Y^2]$。

等号条件：$\Delta = 0$ 意味着方程 $g(t) = 0$ 有重根 $t_0$，故 $E[(X + t_0 Y)^2] = 0$，即 $X + t_0 Y = 0$（a.s.），即 $X = -t_0 Y$（a.s.）。$\blacksquare$

**定理 3.5.2（相关系数的性质）**：

1. **$|\rho(X, Y)| \leq 1$**；

**证明**：令 $\tilde{X} = X - E[X]$，$\tilde{Y} = Y - E[Y]$，由 Cauchy-Schwarz 不等式：

$$(\mathrm{Cov}(X, Y))^2 = (E[\tilde{X}\tilde{Y}])^2 \leq E[\tilde{X}^2] \cdot E[\tilde{Y}^2] = \mathrm{Var}(X) \cdot \mathrm{Var}(Y)$$

故 $|\rho(X, Y)| = |\mathrm{Cov}(X, Y)| / (\sigma_X \sigma_Y) \leq 1$。$\blacksquare$

2. **$\rho(X, Y) = 1$ 当且仅当存在 $a > 0$ 和 $b$ 使得 $Y = aX + b$（a.s.）**；

3. **$\rho(X, Y) = -1$ 当且仅当存在 $a < 0$ 和 $b$ 使得 $Y = aX + b$（a.s.）**；

4. **$\rho(X, Y) = 0$**：称 $X$ 与 $Y$ **不相关**。独立必定不相关，但反之不成立。

**反例（不相关但不独立）**：设 $X \sim U(-1, 1)$（均匀分布），$Y = X^2$。则

$$E[X] = 0, \quad E[XY] = E[X^3] = 0$$

故 $\mathrm{Cov}(X, Y) = 0$，$\rho(X, Y) = 0$。但 $Y = X^2$ 完全由 $X$ 决定，两者不独立。

### 3.6 矩

**定义 3.6.1（原点矩）**：$X$ 的 $k$ 阶原点矩为

$$E[X^k] = \begin{cases} \displaystyle\sum_j x_j^k p(x_j), & \text{离散型} \\[10pt] \displaystyle\int_{-\infty}^{+\infty} x^k f(x) \, dx, & \text{连续型} \end{cases}$$

一阶原点矩即为期望。

**定义 3.6.2（中心矩）**：$X$ 的 $k$ 阶中心矩为

$$E\left[(X - E[X])^k\right]$$

二阶中心矩即为方差。

**常用关系**：
- 三阶中心矩与**偏度**（skewness）有关：$\gamma_1 = E[(X - \mu)^3]/\sigma^3$，衡量分布的偏斜方向。
- 四阶中心矩与**峰度**（kurtosis）有关：$\gamma_2 = E[(X - \mu)^4]/\sigma^4$，衡量分布的尖锐程度。

### 3.7 协方差矩阵

**定义 3.7.1（协方差矩阵）**：设 $\mathbf{X} = (X_1, X_2, \ldots, X_n)^T$ 为 $n$ 维随机向量，$E[X_i] = \mu_i$。协方差矩阵定义为

$$\boldsymbol{\Sigma} = \mathrm{Cov}(\mathbf{X}) = E\left[(\mathbf{X} - \boldsymbol{\mu})(\mathbf{X} - \boldsymbol{\mu})^T\right] = \begin{pmatrix} \mathrm{Var}(X_1) & \mathrm{Cov}(X_1, X_2) & \cdots & \mathrm{Cov}(X_1, X_n) \\ \mathrm{Cov}(X_2, X_1) & \mathrm{Var}(X_2) & \cdots & \mathrm{Cov}(X_2, X_n) \\ \vdots & \vdots & \ddots & \vdots \\ \mathrm{Cov}(X_n, X_1) & \mathrm{Cov}(X_n, X_2) & \cdots & \mathrm{Var}(X_n) \end{pmatrix}$$

其中 $\boldsymbol{\mu} = (E[X_1], \ldots, E[X_n])^T$。

**性质**：
1. **对称性**：$\boldsymbol{\Sigma}^T = \boldsymbol{\Sigma}$；
2. **半正定性**：对任意 $\mathbf{c} \in \mathbb{R}^n$，$\mathbf{c}^T \boldsymbol{\Sigma} \mathbf{c} = \mathrm{Var}(\mathbf{c}^T \mathbf{X}) \geq 0$。

### 3.8 Jensen 不等式（证明）

**定理 3.8.1（Jensen 不等式）**：设 $\varphi: \mathbb{R} \to \mathbb{R}$ 为**凸函数**，$X$ 为随机变量且 $E[|X|] < \infty$，$E[|\varphi(X)|] < \infty$，则

$$\varphi(E[X]) \leq E[\varphi(X)]$$

若 $\varphi$ 为**严格凸函数**，则等号成立当且仅当 $X = E[X]$（a.s.）。

**证明**：由于 $\varphi$ 是凸函数，对任意 $x_0 \in \mathbb{R}$，存在一条过 $(x_0, \varphi(x_0))$ 的**支撑线**（supporting line），即存在 $a$ 使得

$$\varphi(x) \geq \varphi(x_0) + a(x - x_0), \quad \forall x \in \mathbb{R}$$

取 $x_0 = E[X]$，则对随机变量 $X$ 的每个取值：

$$\varphi(X(\omega)) \geq \varphi(E[X]) + a(X(\omega) - E[X])$$

两边取期望：

$$E[\varphi(X)] \geq \varphi(E[X]) + a(E[X] - E[X]) = \varphi(E[X])$$

若 $\varphi$ 严格凸，等号要求 $\varphi(X) = \varphi(E[X]) + a(X - E[X])$（a.s.），由于严格凸函数的支撑线仅在 $x_0$ 处与函数相切，故 $X = E[X]$（a.s.）。$\blacksquare$

**推论 3.8.1**：由 Jensen 不等式可得：
- 取 $\varphi(x) = x^2$（凸函数）：$(E[X])^2 \leq E[X^2]$，即 $\mathrm{Var}(X) \geq 0$。
- 取 $\varphi(x) = |x|$（凸函数）：$|E[X]| \leq E[|X|]$。
- 取 $\varphi(x) = e^x$（凸函数）：$e^{E[X]} \leq E[e^X]$。
- 取 $\varphi(x) = -\ln x$（在 $x > 0$ 上凸）：$-\ln(E[X]) \leq E[-\ln X]$，即 $\ln(E[X]) \geq E[\ln X]$。

**应用：AM-GM 不等式的证明**：设 $a_1, a_2, \ldots, a_n > 0$，取 $X$ 为以等概率取 $a_1, \ldots, a_n$ 的离散随机变量，由 $\ln(E[X]) \geq E[\ln X]$：

$$\ln\left(\frac{1}{n}\sum_{k=1}^{n} a_k\right) \geq \frac{1}{n}\sum_{k=1}^{n} \ln a_k = \ln\left(\prod_{k=1}^{n} a_k^{1/n}\right)$$

即 $\frac{1}{n}\sum_{k=1}^{n} a_k \geq \left(\prod_{k=1}^{n} a_k\right)^{1/n}$。$\blacksquare$
