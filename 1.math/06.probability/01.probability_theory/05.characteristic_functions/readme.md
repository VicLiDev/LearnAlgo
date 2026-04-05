# 第五章 特征函数与矩母函数

## 1. 几何意义

### 1.1 特征函数的几何直觉

特征函数 $\varphi_X(t) = E[e^{itX}]$ 是随机变量 $X$ 的 Fourier 变换。其几何意义可以从以下几个角度理解：

- **频率域表示**：正如 Fourier 变换将时域信号转换为频域表示，特征函数将概率分布从"空间域"（概率密度/质量函数）转换到"频率域"。特征函数的形状编码了分布的所有信息。

- **"指纹"**：特征函数与分布之间是一一对应的（在连续点处）。每个分布都有唯一的特征函数，就像人的指纹一样。因此，要证明两个分布相同，只需证明它们的特征函数相同。

- **周期性**：由于 $e^{itX} = \cos(tX) + i\sin(tX)$，特征函数将随机变量映射到单位圆上。$\varphi_X(t)$ 可以理解为 $e^{itX}$ 在单位圆上的"加权平均位置"。

### 1.2 矩母函数的几何直觉

矩母函数 $M_X(t) = E[e^{tX}]$ 是 Laplace 变换（双侧）。它在原点处的 $k$ 阶导数就是 $X$ 的 $k$ 阶原点矩：

$$M_X^{(k)}(0) = E[X^k]$$

几何上，$M_X(t)$ 在 $t = 0$ 处的 Taylor 展开就是矩的生成序列：

$$M_X(t) = 1 + E[X] t + \frac{E[X^2]}{2!} t^2 + \frac{E[X^3]}{3!} t^3 + \cdots$$

### 1.3 逆转公式的几何意义

逆转公式从特征函数恢复分布函数，类似于 Fourier 逆变换从频域恢复时域信号。这使得特征函数成为分析分布的有力工具。

---

## 2. 应用场景

### 2.1 特征函数的应用

- **判断分布相同**：证明两个随机变量具有相同分布的经典方法。
- **计算独立随机变量之和的分布**：独立和的特征函数等于特征函数的乘积，极大地简化了卷积运算。
- **证明极限定理**：CLT 的经典证明方法就是利用特征函数和 Levy 连续性定理。

### 2.2 矩母函数的应用

- **求矩**：通过求导方便地计算各阶矩。
- **识别分布**：已知 MGF 可以唯一确定分布。
- **分支过程**：矩母函数在 Galton-Watson 分支过程的分析中起核心作用。

---

## 3. 数学理论（及推导）

### 3.1 特征函数的定义与性质

**定义 3.1.1（特征函数）**：随机变量 $X$ 的**特征函数**（characteristic function）定义为

$$\varphi_X(t) = E\left[e^{itX}\right] = \begin{cases} \displaystyle\sum_k e^{itx_k} p(x_k), & \text{离散型} \\[10pt] \displaystyle\int_{-\infty}^{+\infty} e^{itx} f(x) \, dx, & \text{连续型} \end{cases}$$

其中 $t \in \mathbb{R}$，$i = \sqrt{-1}$。

### 3.2 特征函数的基本性质（证明）

**性质 3.2.1**：$|\varphi_X(t)| \leq \varphi_X(0) = 1$。

**证明**：$|\varphi_X(t)| = |E[e^{itX}]| \leq E[|e^{itX}|] = E[1] = 1$。且 $\varphi_X(0) = E[e^{0}] = 1$。$\blacksquare$

**性质 3.2.2（共轭对称性）**：$\varphi_X(-t) = \overline{\varphi_X(t)}$。

**证明**：$\varphi_X(-t) = E[e^{-itX}] = E[\overline{e^{itX}}] = \overline{E[e^{itX}]} = \overline{\varphi_X(t)}$。$\blacksquare$

**性质 3.2.3（Hermitian 性）**：$\varphi_X(t)$ 是 Hermitian 函数，即 $\varphi_X(t) = \overline{\varphi_X(-t)}$。

**性质 3.2.4（一致连续性）**：$\varphi_X(t)$ 在 $\mathbb{R}$ 上一致连续。

**证明**：对任意 $t, h \in \mathbb{R}$：

$$|\varphi_X(t + h) - \varphi_X(t)| = \left|E\left[e^{i(t+h)X} - e^{itX}\right]\right| = \left|E\left[e^{itX}(e^{ihX} - 1)\right]\right| \leq E\left|e^{ihX} - 1\right|$$

对任意 $\varepsilon > 0$，取 $M$ 使得 $P(|X| > M) < \varepsilon/4$，则

$$E\left|e^{ihX} - 1\right| = E\left[\left|e^{ihX} - 1\right| \mathbf{1}_{\{|X| \leq M\}}\right] + E\left[\left|e^{ihX} - 1\right| \mathbf{1}_{\{|X| > M\}}\right]$$

$$\leq E\left[|hX| \cdot \mathbf{1}_{\{|X| \leq M\}}\right] + 2 P(|X| > M) \leq |h|M + \frac{\varepsilon}{2}$$

取 $|h| < \varepsilon/(2M)$，则 $|\varphi_X(t+h) - \varphi_X(t)| < \varepsilon$。$\blacksquare$

**性质 3.2.5（非负定性）**：对任意 $n$，任意 $t_1, \ldots, t_n \in \mathbb{R}$，任意 $c_1, \ldots, c_n \in \mathbb{C}$，

$$\sum_{j=1}^n \sum_{k=1}^n c_j \overline{c_k} \, \varphi_X(t_j - t_k) \geq 0$$

**证明**：

$$\sum_{j,k} c_j \overline{c_k} \, \varphi_X(t_j - t_k) = \sum_{j,k} c_j \overline{c_k} E\left[e^{i(t_j - t_k)X}\right] = E\left[\sum_{j,k} c_j \overline{c_k} e^{it_j X} e^{-it_k X}\right]$$

$$= E\left[\left|\sum_{j} c_j e^{it_j X}\right|^2\right] \geq 0 \quad \blacksquare$$

**性质 3.2.6（独立变量的特征函数相乘）**：若 $X$ 与 $Y$ 独立，则

$$\varphi_{X+Y}(t) = \varphi_X(t) \cdot \varphi_Y(t)$$

**证明**：$\varphi_{X+Y}(t) = E[e^{it(X+Y)}] = E[e^{itX} \cdot e^{itY}] = E[e^{itX}] \cdot E[e^{itY}] = \varphi_X(t) \varphi_Y(t)$。$\blacksquare$

### 3.3 矩母函数

**定义 3.3.1（矩母函数）**：随机变量 $X$ 的**矩母函数**（moment generating function, MGF）定义为

$$M_X(t) = E\left[e^{tX}\right], \quad t \in \mathbb{R}$$

（要求在 $t = 0$ 的某个邻域内 $M_X(t) < \infty$。）

### 3.4 矩母函数的性质

**性质 3.4.1**：$M_X(0) = 1$。

**性质 3.4.2（矩的生成）**：若 $M_X(t)$ 在 $t = 0$ 的邻域内存在，则

$$M_X^{(k)}(0) = E[X^k]$$

**证明**：在 $E[e^{tX}]$ 内部展开 Taylor 级数：

$$E[e^{tX}] = E\left[\sum_{k=0}^{\infty} \frac{(tX)^k}{k!}\right] = \sum_{k=0}^{\infty} \frac{t^k}{k!} E[X^k]$$

（交换求期望和求和的顺序需要 $E[|X|^k] < \infty$。）两端对 $t$ 求 $k$ 阶导并令 $t = 0$：

$$M_X^{(k)}(0) = E[X^k] \quad \blacksquare$$

**性质 3.4.3（独立变量）**：若 $X, Y$ 独立，则 $M_{X+Y}(t) = M_X(t) M_Y(t)$。

**注**：矩母函数不一定对所有 $t \in \mathbb{R}$ 都存在（例如 Cauchy 分布），但特征函数总是存在。这是特征函数优于矩母函数的重要原因。

### 3.5 特征函数与分布的一一对应（逆转公式）

**定理 3.5.1（逆转公式 / Inversion Formula）**：设 $\varphi_X(t)$ 是 $X$ 的特征函数，$F(x)$ 是 $X$ 的分布函数。若 $a < b$ 是 $F$ 的连续点，则

$$F(b) - F(a) = \lim_{T \to \infty} \frac{1}{2\pi} \int_{-T}^{T} \frac{e^{-ita} - e^{-itb}}{it} \, \varphi_X(t) \, dt$$

**推论 3.5.1（唯一性定理）**：若两个随机变量 $X$ 和 $Y$ 的特征函数相同，即 $\varphi_X(t) = \varphi_Y(t)$ 对所有 $t \in \mathbb{R}$ 成立，则 $X$ 和 $Y$ 具有相同的分布。

**证明**：由逆转公式，分布函数 $F_X$ 和 $F_Y$ 在所有连续点处的值都相同，故 $F_X = F_Y$。$\blacksquare$

**定理 3.5.2（密度函数的逆转）**：若 $\int_{-\infty}^{+\infty} |\varphi_X(t)| \, dt < \infty$，则 $X$ 是连续型随机变量，其密度函数为

$$f(x) = \frac{1}{2\pi} \int_{-\infty}^{+\infty} e^{-itx} \, \varphi_X(t) \, dt$$

### 3.6 特征函数与矩的关系

**定理 3.6.1**：若 $E[|X|^n] < \infty$，则 $\varphi_X(t)$ 在 $t = 0$ 处 $n$ 次可微，且

$$\varphi_X^{(k)}(0) = i^k E[X^k], \quad k = 0, 1, \ldots, n$$

**证明**（$k = 1$ 的情形）：考虑差商

$$\frac{\varphi_X(t) - \varphi_X(0)}{t} = E\left[\frac{e^{itX} - 1}{t}\right]$$

由控制收敛定理（DCT），当 $t \to 0$ 时（注意 $\left|\frac{e^{itX} - 1}{t}\right| \leq |X|$，由 $E[|X|] < \infty$ 保证 DCT 条件满足）：

$$\varphi_X'(0) = \lim_{t \to 0} E\left[\frac{e^{itX} - 1}{t}\right] = E\left[\lim_{t \to 0} \frac{e^{itX} - 1}{t}\right] = E[iX] = iE[X]$$

一般情形类似。$\blacksquare$

**推论**：特征函数在原点处的 Taylor 展开：

$$\varphi_X(t) = 1 + \sum_{k=1}^{n} \frac{(it)^k}{k!} E[X^k] + o(t^n)$$

### 3.7 多维特征函数

**定义 3.7.1（多维特征函数）**：$n$ 维随机向量 $\mathbf{X} = (X_1, \ldots, X_n)^T$ 的特征函数定义为

$$\varphi_{\mathbf{X}}(\mathbf{t}) = E\left[e^{i\mathbf{t}^T \mathbf{X}}\right] = E\left[\exp\left(i \sum_{k=1}^n t_k X_k\right)\right], \quad \mathbf{t} \in \mathbb{R}^n$$

**性质**：
1. $\varphi_{\mathbf{X}}(\mathbf{0}) = 1$，$|\varphi_{\mathbf{X}}(\mathbf{t})| \leq 1$。
2. 若 $\mathbf{X}$ 的各分量独立，则 $\varphi_{\mathbf{X}}(\mathbf{t}) = \prod_{k=1}^n \varphi_{X_k}(t_k)$。
3. 矩的关系：$E[X_1^{k_1} \cdots X_n^{k_n}] = (-i)^{k_1+\cdots+k_n} \frac{\partial^{k_1+\cdots+k_n}}{\partial t_1^{k_1} \cdots \partial t_n^{k_n}} \varphi_{\mathbf{X}}(\mathbf{t})\Big|_{\mathbf{t} = \mathbf{0}}$。

### 3.8 特征函数的应用：求和分布判定

**例 3.8.1（正态分布的可加性）**：设 $X \sim N(\mu_1, \sigma_1^2)$，$Y \sim N(\mu_2, \sigma_2^2)$ 独立。则 $X + Y \sim N(\mu_1 + \mu_2, \sigma_1^2 + \sigma_2^2)$。

**推导**：

$$\varphi_X(t) = E[e^{itX}] = e^{i\mu_1 t - \sigma_1^2 t^2/2}, \quad \varphi_Y(t) = e^{i\mu_2 t - \sigma_2^2 t^2/2}$$

$$\varphi_{X+Y}(t) = \varphi_X(t) \varphi_Y(t) = e^{i(\mu_1+\mu_2)t - (\sigma_1^2+\sigma_2^2)t^2/2}$$

这正是 $N(\mu_1+\mu_2, \sigma_1^2+\sigma_2^2)$ 的特征函数，由唯一性定理即得。$\blacksquare$

**例 3.8.2（Poisson 分布的可加性）**：设 $X \sim P(\lambda_1)$，$Y \sim P(\lambda_2)$ 独立。则 $X + Y \sim P(\lambda_1 + \lambda_2)$。

**推导**：

$$\varphi_X(t) = E[e^{itX}] = \sum_{k=0}^{\infty} e^{itk} \frac{e^{-\lambda_1}\lambda_1^k}{k!} = e^{-\lambda_1} \sum_{k=0}^{\infty} \frac{(\lambda_1 e^{it})^k}{k!} = e^{\lambda_1(e^{it}-1)}$$

类似地 $\varphi_Y(t) = e^{\lambda_2(e^{it}-1)}$，故

$$\varphi_{X+Y}(t) = e^{(\lambda_1+\lambda_2)(e^{it}-1)}$$

由唯一性定理，$X + Y \sim P(\lambda_1 + \lambda_2)$。$\blacksquare$

**例 3.8.3（Gamma 分布的可加性）**：设 $X \sim \Gamma(\alpha_1, \beta)$，$Y \sim \Gamma(\alpha_2, \beta)$ 独立。则 $X + Y \sim \Gamma(\alpha_1 + \alpha_2, \beta)$。

**推导（利用 MGF）**：

$$M_X(t) = (1 - t/\beta)^{-\alpha_1}, \quad M_Y(t) = (1 - t/\beta)^{-\alpha_2}$$

$$M_{X+Y}(t) = (1 - t/\beta)^{-(\alpha_1 + \alpha_2)}$$

这正是 $\Gamma(\alpha_1 + \alpha_2, \beta)$ 的 MGF。$\blacksquare$

### 3.9 常见分布的特征函数

| 分布 | 特征函数 $\varphi(t)$ |
|------|----------------------|
| $B(1, p)$ | $1 - p + p e^{it}$ |
| $B(n, p)$ | $(1 - p + p e^{it})^n$ |
| $P(\lambda)$ | $\exp(\lambda(e^{it} - 1))$ |
| $U(a, b)$ | $\dfrac{e^{itb} - e^{ita}}{it(b-a)}$ |
| $\mathrm{Exp}(\lambda)$ | $(1 - it/\lambda)^{-1}$ |
| $N(\mu, \sigma^2)$ | $\exp(i\mu t - \sigma^2 t^2/2)$ |
| $\Gamma(\alpha, \beta)$ | $(1 - it/\beta)^{-\alpha}$ |
| $\chi^2(n)$ | $(1 - 2it)^{-n/2}$ |
| Cauchy | $e^{-|t|}$ |
