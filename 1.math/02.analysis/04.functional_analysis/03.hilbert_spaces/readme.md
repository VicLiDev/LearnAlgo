# 第三章 内积空间与Hilbert空间

## 几何意义

内积空间是最接近 Euclid 空间的无穷维推广。在 $\mathbb{R}^n$ 中，内积（点积）$\langle x, y \rangle = \sum_{i=1}^n x_i y_i$ 不仅是"长度"（$\|x\| = \sqrt{\langle x, x \rangle}$）的来源，更是"角度"和"正交性"的来源。两个向量的夹角余弦为：

$$
\cos\theta = \frac{\langle x, y \rangle}{\|x\| \cdot \|y\|}
$$

正交（$\langle x, y \rangle = 0$）意味着两个向量互相"垂直"——这是几何中最核心的关系之一。

内积空间保留了 Euclid 几何的三个核心结构：
- **长度**：$\|x\| = \sqrt{\langle x, x \rangle}$
- **角度**：通过 Cauchy-Schwarz 不等式定义
- **投影**：向量到子空间的最佳逼近（正交投影）

Hilbert 空间是**完备的**内积空间。完备性保证了正交投影的存在性和 Fourier 展开的收敛性——这是无穷维中不能忽视的微妙之处。

正交分解定理 $H = M \oplus M^\perp$（$M$ 是闭子空间）是"勾股定理"在无穷维的完美推广。在 $\mathbb{R}^3$ 中，任何向量可以分解为平面上的投影与法向量之和；在 Hilbert 空间中，任何元素都可以分解为闭子空间上的投影与正交补上的分量之和。

## 应用场景

1. **Fourier 分析**：$L^2[0, 2\pi]$ 上的三角函数系 $\{e^{inx}\}$ 构成标准正交基，Parseval 恒等式说明能量在时域和频域守恒。

2. **量子力学**：量子态由 Hilbert 空间 $L^2(\mathbb{R}^3)$ 中的向量表示，可观测量的本征函数构成正交基。

3. **信号处理**：正交变换（如 DFT、DCT、小波变换）本质上是信号在不同正交基下的表示。

4. **偏微分方程的特征值问题**：Laplace 算子的特征函数构成 $L^2$ 空间的正交基。

5. **统计学**：最佳线性估计（回归分析）可以看作 $L^2$ 空间中的正交投影。

6. **机器学习**：再生核 Hilbert 空间（RKHS）是核方法的理论基础。

## 数学理论（及推导）

### 3.1 内积空间的定义

**定义 3.1**（内积空间） 设 $X$ 是 $\mathbb{K}$（$\mathbb{R}$ 或 $\mathbb{C}$）上的线性空间。映射 $\langle \cdot, \cdot \rangle: X \times X \to \mathbb{K}$ 若满足：

1. **正定性**：$\langle x, x \rangle \geq 0$，且 $\langle x, x \rangle = 0 \iff x = 0$
2. **第一变元的线性**：$\langle \alpha x + \beta y, z \rangle = \alpha \langle x, z \rangle + \beta \langle y, z \rangle$
3. **共轭对称性**：$\langle x, y \rangle = \overline{\langle y, x \rangle}$

则称 $\langle \cdot, \cdot \rangle$ 为 $X$ 上的**内积**，$(X, \langle \cdot, \cdot \rangle)$ 为**内积空间**。

**命题 3.1** 内积诱导的范数 $\|x\| = \sqrt{\langle x, x \rangle}$ 满足范数公理，因此内积空间自动成为赋范线性空间。

**定义 3.2**（Hilbert 空间） 完备的内积空间称为 **Hilbert 空间**。

### 3.2 Cauchy-Schwarz 不等式

**定理 3.1**（Cauchy-Schwarz 不等式） 在内积空间 $(X, \langle \cdot, \cdot \rangle)$ 中，

$$
|\langle x, y \rangle| \leq \|x\| \cdot \|y\|, \quad \forall\, x, y \in X
$$

等号成立当且仅当 $x$ 与 $y$ 线性相关。

**证明**：若 $y = 0$，等式显然成立。设 $y \neq 0$。对任意 $\alpha \in \mathbb{K}$，由内积的正定性：

$$
0 \leq \langle x + \alpha y, x + \alpha y \rangle = \|x\|^2 + \alpha \langle y, x \rangle + \overline{\alpha} \langle x, y \rangle + |\alpha|^2 \|y\|^2
$$

取 $\alpha = -\dfrac{\langle x, y \rangle}{\|y\|^2}$（使 $x + \alpha y$ 成为 $x$ 在 $y$ 方向上的投影的残差），代入：

$$
0 \leq \|x\|^2 - \frac{|\langle x, y \rangle|^2}{\|y\|^2} - \frac{|\langle x, y \rangle|^2}{\|y\|^2} + \frac{|\langle x, y \rangle|^2}{\|y\|^2} = \|x\|^2 - \frac{|\langle x, y \rangle|^2}{\|y\|^2}
$$

整理得 $|\langle x, y \rangle|^2 \leq \|x\|^2 \|y\|^2$。$\blacksquare$

### 3.3 正交性与正交投影定理

**定义 3.3**（正交） 设 $H$ 是内积空间。元素 $x, y \in H$ 称为**正交**的（记为 $x \perp y$），若 $\langle x, y \rangle = 0$。

**定义 3.4**（正交补） 设 $M \subset H$，定义 $M$ 的**正交补**为：

$$
M^\perp = \{ x \in H : \langle x, y \rangle = 0, \, \forall\, y \in M \}
$$

**命题 3.2** $M^\perp$ 总是 $H$ 的闭子空间。

**定理 3.2**（正交投影定理） 设 $H$ 是 Hilbert 空间，$M$ 是 $H$ 的闭子空间。则对任意 $x \in H$，存在唯一的 $y \in M$ 和 $z \in M^\perp$ 使得

$$
x = y + z
$$

即 $H = M \oplus M^\perp$。元素 $y$ 称为 $x$ 在 $M$ 上的**正交投影**，记为 $y = P_M x$。

**证明**：

**(a) 存在性**。令 $d = \inf_{m \in M} \|x - m\|$。取极小化序列 $\{y_n\} \subset M$ 使得 $\|x - y_n\| \to d$。由平行四边形恒等式：

$$
\|y_m - y_n\|^2 = 2\|y_m - x\|^2 + 2\|y_n - x\|^2 - 4\left\|\frac{y_m + y_n}{2} - x\right\|^2
$$

因 $M$ 是子空间，$(y_m + y_n)/2 \in M$，故 $\|(y_m + y_n)/2 - x\| \geq d$。因此：

$$
\|y_m - y_n\|^2 \leq 2\|y_m - x\|^2 + 2\|y_n - x\|^2 - 4d^2 \to 0
$$

故 $\{y_n\}$ 是 Cauchy 序列。由 $H$ 的完备性和 $M$ 的闭性，$y_n \to y \in M$。

令 $z = x - y$，下证 $z \in M^\perp$。对任意 $w \in M$ 和 $\alpha \in \mathbb{K}$，$y + \alpha w \in M$，故：

$$
d^2 \leq \|x - (y + \alpha w)\|^2 = \|z - \alpha w\|^2 = d^2 - 2\text{Re}(\alpha \langle z, w \rangle) + |\alpha|^2 \|w\|^2
$$

取 $\alpha = t \cdot \dfrac{\langle z, w \rangle}{\|w\|^2}$（$t > 0$ 为实数），得：

$$
0 \leq -2t \frac{|\langle z, w \rangle|^2}{\|w\|^2} + t^2 \frac{|\langle z, w \rangle|^2}{\|w\|^2}
$$

两边除以 $t$ 再令 $t \to 0^+$，得 $\langle z, w \rangle = 0$。故 $z \perp M$，即 $z \in M^\perp$。

**(b) 唯一性**。设 $x = y_1 + z_1 = y_2 + z_2$，$y_1, y_2 \in M$，$z_1, z_2 \in M^\perp$，则 $y_1 - y_2 = z_2 - z_1$。左边属于 $M$，右边属于 $M^\perp$，故 $\|y_1 - y_2\|^2 = \langle y_1 - y_2, z_2 - z_1 \rangle = 0$，得 $y_1 = y_2$，从而 $z_1 = z_2$。$\blacksquare$

**推论 3.1** 正交投影 $P_M: H \to M$ 是线性算子，且 $\|P_M\| = 1$（$M \neq \{0\}$ 时）。

### 3.4 Riesz 表示定理

**定理 3.3**（Riesz 表示定理） 设 $H$ 是 Hilbert 空间，$f: H \to \mathbb{K}$ 是有界线性泛函。则存在唯一的 $u \in H$ 使得

$$
f(x) = \langle x, u \rangle, \quad \forall\, x \in H
$$

且 $\|f\| = \|u\|$。

**证明**：

**(a) 存在性**。若 $f = 0$，取 $u = 0$ 即可。设 $f \neq 0$。令 $M = \ker f = \{x : f(x) = 0\}$，则 $M$ 是 $H$ 的真闭子空间。由正交投影定理，$H = M \oplus M^\perp$，且 $M^\perp$ 是一维的（否则 $f$ 在 $M^\perp$ 上不全为零，可以找到更多线性无关的向量）。

取 $v \in M^\perp$，$v \neq 0$。令 $u = \dfrac{\overline{f(v)}}{\|v\|^2} v$。对任意 $x \in H$，分解 $x = m + \alpha v$（$m \in M$），则：

$$
f(x) = f(m) + \alpha f(v) = \alpha f(v)
$$

而

$$
\langle x, u \rangle = \langle m + \alpha v, u \rangle = \langle m, u \rangle + \alpha \langle v, u \rangle = 0 + \alpha \frac{f(v)}{\|v\|^2} \langle v, v \rangle = \alpha f(v)
$$

故 $f(x) = \langle x, u \rangle$。

**(b) 唯一性**。若 $f(x) = \langle x, u_1 \rangle = \langle x, u_2 \rangle$，则 $\langle x, u_1 - u_2 \rangle = 0$ 对所有 $x \in H$ 成立，取 $x = u_1 - u_2$ 得 $\|u_1 - u_2\|^2 = 0$。

**(c) 范数等式**。由 Cauchy-Schwarz 不等式：

$$
|f(x)| = |\langle x, u \rangle| \leq \|x\| \cdot \|u\|
$$

故 $\|f\| \leq \|u\|$。取 $x = u$：

$$
|f(u)| = \langle u, u \rangle = \|u\|^2
$$

故 $\|f\| \geq |f(u)|/\|u\| = \|u\|$。综上 $\|f\| = \|u\|$。$\blacksquare$

### 3.5 正交系与正交基

**定义 3.5**（正交系） 内积空间 $H$ 中的子集 $\{e_\alpha\}_{\alpha \in A}$ 称为**正交系**，若 $\langle e_\alpha, e_\beta \rangle = 0$（$\alpha \neq \beta$）。若进一步 $\|e_\alpha\| = 1$，则称为**标准正交系**。

**定理 3.4**（Bessel 不等式） 设 $\{e_n\}$ 是内积空间 $H$ 中的标准正交系，则对任意 $x \in H$：

$$
\sum_{n=1}^\infty |\langle x, e_n \rangle|^2 \leq \|x\|^2
$$

**证明**：令 $s_N = \sum_{n=1}^N \langle x, e_n \rangle e_n$，则 $x - s_N \perp s_N$（因为 $\langle x - s_N, e_k \rangle = \langle x, e_k \rangle - \langle x, e_k \rangle = 0$ 对 $k \leq N$）。由勾股定理：

$$
\|x\|^2 = \|s_N\|^2 + \|x - s_N\|^2 \geq \|s_N\|^2 = \sum_{n=1}^N |\langle x, e_n \rangle|^2
$$

令 $N \to \infty$ 即得。$\blacksquare$

**定义 3.6**（完全正交系） 标准正交系 $\{e_n\}$ 称为**完全的**（完备的），若 $\text{span}\{e_n\}$ 在 $H$ 中稠密。

**定义 3.7**（Hilbert 基） 完全的标准正交系称为 **Hilbert 基**（标准正交基）。

**定理 3.5**（Parseval 恒等式） 设 $\{e_n\}$ 是 Hilbert 空间 $H$ 的标准正交系，则以下等价：

1. $\{e_n\}$ 是 Hilbert 基（完全正交系）
2. $\forall\, x \in H: \quad \|x\|^2 = \sum_{n=1}^\infty |\langle x, e_n \rangle|^2$（Parseval 恒等式）
3. $\forall\, x \in H: \quad x = \sum_{n=1}^\infty \langle x, e_n \rangle e_n$（Fourier 展开）

**证明**：$(2) \Rightarrow (1)$：若 Parseval 恒等式成立且 $x \perp \{e_n\}$，则 $\|x\|^2 = 0$，故 $x = 0$。

$(3) \Rightarrow (2)$：$x = \sum \langle x, e_n \rangle e_n$，由范数的连续性：

$$
\|x\|^2 = \left\|\sum_{n=1}^\infty \langle x, e_n \rangle e_n\right\|^2 = \sum_{n=1}^\infty |\langle x, e_n \rangle|^2
$$

$(1) \Rightarrow (3)$：因 $\text{span}\{e_n\}$ 稠密，对任意 $\varepsilon > 0$，存在 $s \in \text{span}\{e_n\}$ 使得 $\|x - s\| < \varepsilon$。由正交投影的最优逼近性，$\|x - s_N\| \leq \|x - s\| < \varepsilon$（$s_N$ 是 $s$ 的前 $N$ 项），故 $s_N \to x$。$\blacksquare$

### 3.6 Gram-Schmidt 正交化

**定理 3.6**（Gram-Schmidt 正交化） 设 $\{x_n\}$ 是内积空间 $H$ 中的线性无关序列，则存在标准正交序列 $\{e_n\}$ 使得

$$
\text{span}\{e_1, \ldots, e_n\} = \text{span}\{x_1, \ldots, x_n\}, \quad \forall\, n
$$

**构造**：递归定义如下：

$$
\begin{aligned}
y_1 &= x_1, \quad e_1 = \frac{y_1}{\|y_1\|} \\
y_n &= x_n - \sum_{k=1}^{n-1} \langle x_n, e_k \rangle e_k, \quad e_n = \frac{y_n}{\|y_n\|} \quad (n \geq 2)
\end{aligned}
$$

**证明**：由 $\{x_1, \ldots, x_{n-1}\}$ 线性无关知 $\|y_n\| > 0$（否则 $x_n \in \text{span}\{x_1, \ldots, x_{n-1}\}$，矛盾）。

归纳可证 $y_n \perp e_k$（$k < n$）：

$$
\langle y_n, e_k \rangle = \langle x_n, e_k \rangle - \langle x_n, e_k \rangle \langle e_k, e_k \rangle = 0
$$

故 $\{e_n\}$ 是标准正交系，且由构造方式，$\text{span}\{e_1, \ldots, e_n\} = \text{span}\{x_1, \ldots, x_n\}$。$\blacksquare$

### 3.7 重要 Hilbert 空间例子

**例 3.1**（$L^2$ 空间） $L^2[a,b]$ 是最重要的 Hilbert 空间，内积为：

$$
\langle f, g \rangle = \int_a^b f(t) \overline{g(t)} \, dt
$$

**例 3.2**（$\ell^2$ 空间） 平方可和序列空间 $\ell^2$ 的内积为：

$$
\langle x, y \rangle = \sum_{n=1}^\infty x_n \overline{y_n}
$$

**例 3.3**（Fourier 正交基） 在 $L^2[-\pi, \pi]$ 中，$\left\{\dfrac{e^{inx}}{\sqrt{2\pi}}\right\}_{n=-\infty}^{+\infty}$ 构成标准正交基。Parseval 恒等式给出：

$$
\frac{1}{2\pi} \int_{-\pi}^{\pi} |f(t)|^2 \, dt = \sum_{n=-\infty}^{+\infty} |\hat{f}(n)|^2
$$

这就是 Fourier 分析中能量守恒的数学表达。
