# 第二章 随机变量及其分布

## 1. 几何意义

### 1.1 随机变量的几何直觉

随机变量是将样本空间 $\Omega$ 映射到实数轴 $\mathbb{R}$ 的函数 $X: \Omega \to \mathbb{R}$。其几何意义在于：

- **可测函数**：$X$ 不是普通的函数，它必须是**可测的**，即对任意 Borel 集 $B \in \mathcal{B}(\mathbb{R})$，原像 $X^{-1}(B) = \{\omega \in \Omega : X(\omega) \in B\}$ 必须属于 $\mathcal{F}$。几何上，这意味着随机变量将样本空间中的"可测区域"映射到实数轴上的"可测区间"。

- **离散型随机变量的几何图示**：离散型随机变量取有限或可数个值 $\{x_1, x_2, \ldots\}$，在数轴上表现为一个个"质点"，每个质点 $x_k$ 带有一个"质量" $P(X = x_k)$。所有质点的质量之和为 1。

- **连续型随机变量的几何图示**：连续型随机变量取值充满某个区间（或 $\mathbb{R}$），其概率密度函数 $f(x)$ 可以理解为一条"密度曲线"，曲线下方某区间 $[a, b]$ 上的面积即为 $P(a \leq X \leq b)$。

### 1.2 分布函数的几何意义

分布函数 $F(x) = P(X \leq x)$ 的图像是一条从左到右单调递增的阶梯/连续曲线，起始于 $( -\infty, 0 )$，终止于 $(+\infty, 1)$。

- 对离散型随机变量，$F(x)$ 是一个**右连续的阶梯函数**，在随机变量的每个取值处有一个跳跃。
- 对连续型随机变量，$F(x)$ 是一个**连续函数**（事实上是绝对连续函数），其导数即为密度函数 $f(x) = F'(x)$。

### 1.3 多维随机变量的几何意义

二维随机变量 $(X, Y)$ 可以理解为平面 $\mathbb{R}^2$ 上的"概率密度曲面"或"质点分布"。联合分布函数 $F(x, y) = P(X \leq x, Y \leq y)$ 表示随机点落入 $(-\infty, x] \times (-\infty, y]$ 区域的概率。

- **边缘分布**：将二维分布"投影"到 $x$ 轴或 $y$ 轴上。
- **条件分布**：在 $Y = y$ 的条件下，$X$ 的分布可以理解为"切片"。

---

## 2. 应用场景

### 2.1 随机变量建模

- **通信系统**：信号传输中的噪声建模（常用正态分布随机变量）。
- **金融工程**：股票价格、利率的随机建模（对数正态分布、几何布朗运动中的随机变量）。
- **排队论**：服务时间和到达间隔用指数分布随机变量建模。

### 2.2 分布函数的应用

- **质量控制**：利用分布函数计算产品合格率，设定控制上限和下限。
- **保险精算**：利用损失分布计算保费、准备金。

### 2.3 随机变量函数的分布

- **信号处理**：系统输出 $Y = g(X)$ 的分布由输入 $X$ 的分布和系统函数 $g$ 决定。
- **统计推断**：统计量（如样本均值、样本方差）是随机变量的函数，其分布是推断的基础。

---

## 3. 数学理论（及推导）

### 3.1 随机变量的定义

**定义 3.1.1（随机变量）**：设 $(\Omega, \mathcal{F}, P)$ 为概率空间。函数 $X: \Omega \to \mathbb{R}$ 称为**随机变量**（random variable），若对任意 $x \in \mathbb{R}$，

$$\{\omega \in \Omega : X(\omega) \leq x\} = X^{-1}((-\infty, x]) \in \mathcal{F}$$

等价地，$X$ 是 $(\Omega, \mathcal{F})$ 到 $(\mathbb{R}, \mathcal{B}(\mathbb{R}))$ 的**可测函数**。

**注**：由于 Borel $\sigma$-代数由形如 $(-\infty, x]$ 的集合生成，可测性条件 $X^{-1}((-\infty, x]) \in \mathcal{F}$ 等价于对任意 Borel 集 $B \in \mathcal{B}(\mathbb{R})$，$X^{-1}(B) \in \mathcal{F}$。

### 3.2 分布函数及其性质

**定义 3.2.1（分布函数）**：随机变量 $X$ 的**累积分布函数**（CDF）定义为

$$F(x) = F_X(x) = P(X \leq x), \quad x \in \mathbb{R}$$

**定理 3.2.1（分布函数的基本性质）**：$F: \mathbb{R} \to [0, 1]$ 是某个随机变量的分布函数，当且仅当它满足：

1. **单调不减**：若 $x_1 < x_2$，则 $F(x_1) \leq F(x_2)$；
2. **右连续**：$\lim_{x \to x_0^+} F(x) = F(x_0)$；
3. $\lim_{x \to -\infty} F(x) = 0$，$\lim_{x \to +\infty} F(x) = 1$。

**证明**：
- (1) 若 $x_1 < x_2$，则 $\{X \leq x_1\} \subseteq \{X \leq x_2\}$，由概率的单调性，$F(x_1) \leq F(x_2)$。
- (2) 令 $x_n \downarrow x_0$，则 $\{X \leq x_n\} \downarrow \{X \leq x_0\}$，由概率的连续性，$\lim_{n \to \infty} F(x_n) = F(x_0)$。
- (3) 令 $A_n = \{X \leq -n\}$，$A_n \downarrow \emptyset$，由连续性 $\lim_{n \to \infty} F(-n) = 0$。类似地，$B_n = \{X \leq n\} \uparrow \Omega$，$\lim_{n \to \infty} F(n) = 1$。$\blacksquare$

**定理 3.2.2**：分布函数 $F$ 的左极限存在，且

$$P(X < x) = F(x-) = \lim_{t \uparrow x} F(t)$$
$$P(X = x) = F(x) - F(x-)$$

**推论**：分布函数的不连续点至多可数，且 $P(X = x) > 0$ 当且仅当 $F$ 在 $x$ 处有跳跃。

### 3.3 离散型随机变量

**定义 3.3.1**：若随机变量 $X$ 的取值集合 $\{x_1, x_2, \ldots\}$ 为有限集或可数集，且 $P(X = x_k) > 0$，$\sum_k P(X = x_k) = 1$，则称 $X$ 为**离散型随机变量**。

**概率质量函数（PMF）**：$p(x_k) = P(X = x_k)$，满足：
1. $p(x_k) \geq 0$；
2. $\sum_k p(x_k) = 1$。

分布函数与 PMF 的关系：

$$F(x) = \sum_{k: x_k \leq x} p(x_k)$$

### 3.4 连续型随机变量

**定义 3.4.1**：若存在非负可积函数 $f: \mathbb{R} \to [0, +\infty)$ 使得

$$F(x) = \int_{-\infty}^{x} f(t) \, dt, \quad \forall x \in \mathbb{R}$$

则称 $X$ 为**连续型随机变量**，$f$ 称为 $X$ 的**概率密度函数**（PDF）。

**概率密度函数的性质**：
1. $f(x) \geq 0$；
2. $\int_{-\infty}^{+\infty} f(x) \, dx = 1$；
3. $P(a \leq X \leq b) = \int_a^b f(x) \, dx$；
4. $F$ 处处连续，且在 $f$ 的连续点处 $F'(x) = f(x)$；
5. **重要**：$P(X = x) = 0$ 对所有 $x \in \mathbb{R}$ 成立（连续型随机变量取任何特定值的概率为零）。

**注**：密度函数不是概率！$f(x)$ 可以大于 1，只有在小区间上的积分才表示概率。事实上，$P(x \leq X \leq x + \Delta x) \approx f(x) \cdot \Delta x$（当 $\Delta x$ 很小时）。

### 3.5 随机变量函数的分布

**定理 3.5.1（单调函数情形）**：设 $X$ 为连续型随机变量，其密度函数为 $f_X(x)$。$y = g(x)$ 是严格单调函数，其反函数为 $x = g^{-1}(y)$。则 $Y = g(X)$ 的密度函数为

$$f_Y(y) = f_X\left(g^{-1}(y)\right) \cdot \left|\frac{d}{dy} g^{-1}(y)\right|$$

**证明**：假设 $g$ 严格递增，则

$$F_Y(y) = P(Y \leq y) = P(g(X) \leq y) = P(X \leq g^{-1}(y)) = F_X(g^{-1}(y))$$

求导得

$$f_Y(y) = f_X(g^{-1}(y)) \cdot \frac{d}{dy} g^{-1}(y)$$

若 $g$ 严格递减，则 $F_Y(y) = P(X \geq g^{-1}(y)) = 1 - F_X(g^{-1}(y))$，求导得

$$f_Y(y) = -f_X(g^{-1}(y)) \cdot \frac{d}{dy} g^{-1}(y) = f_X(g^{-1}(y)) \cdot \left|\frac{d}{dy} g^{-1}(y)\right| \quad \blacksquare$$

**定理 3.5.2（一般连续函数情形——分布函数法）**：对一般函数 $Y = g(X)$，先求分布函数：

$$F_Y(y) = P(g(X) \leq y) = \int_{\{x : g(x) \leq y\}} f_X(x) \, dx$$

再求导得 $f_Y(y) = F_Y'(y)$。

**离散型情形**：若 $Y = g(X)$ 且 $X$ 为离散型，则

$$P(Y = y_j) = \sum_{k: g(x_k) = y_j} P(X = x_k)$$

### 3.6 多维随机变量

**定义 3.6.1（多维随机变量 / 随机向量）**：$n$ 个随机变量 $X_1, X_2, \ldots, X_n$ 构成的向量 $\mathbf{X} = (X_1, X_2, \ldots, X_n)$ 称为 $n$ 维随机变量（随机向量）。它是从 $\Omega$ 到 $\mathbb{R}^n$ 的可测映射。

**联合分布函数**：

$$F(x_1, x_2, \ldots, x_n) = P(X_1 \leq x_1, X_2 \leq x_2, \ldots, X_n \leq x_n)$$

**联合密度函数**（连续型）：若存在 $f(x_1, x_2, \ldots, x_n) \geq 0$ 使得

$$F(x_1, \ldots, x_n) = \int_{-\infty}^{x_1} \cdots \int_{-\infty}^{x_n} f(t_1, \ldots, t_n) \, dt_n \cdots dt_1$$

则 $f$ 称为联合密度函数。

### 3.7 联合分布与边缘分布

**边缘分布函数**：二维随机变量 $(X, Y)$ 中，$X$ 的边缘分布函数为

$$F_X(x) = P(X \leq x) = P(X \leq x, Y < +\infty) = F(x, +\infty) = \lim_{y \to +\infty} F(x, y)$$

类似地，$F_Y(y) = F(+\infty, y)$。

**边缘密度函数**（连续型）：

$$f_X(x) = \int_{-\infty}^{+\infty} f(x, y) \, dy$$
$$f_Y(y) = \int_{-\infty}^{+\infty} f(x, y) \, dx$$

**边缘 PMF**（离散型）：

$$p_X(x_i) = \sum_j p(x_i, y_j) = \sum_j P(X = x_i, Y = y_j)$$

**定理 3.7.1（独立性）**：$X$ 与 $Y$ 独立当且仅当

$$F(x, y) = F_X(x) \cdot F_Y(y), \quad \forall x, y \in \mathbb{R}$$

等价地：
- 离散型：$p(x_i, y_j) = p_X(x_i) \cdot p_Y(y_j)$，对所有 $i, j$；
- 连续型：$f(x, y) = f_X(x) \cdot f_Y(y)$（几乎处处成立）。
