# 第一章 度量空间与完备性

## 几何意义

度量空间是 Euclid 几何最自然的抽象推广。在 Euclid 空间 $\mathbb{R}^n$ 中，两点之间的距离由

$$
d(x,y) = \sqrt{(x_1-y_1)^2 + (x_2-y_2)^2 + \cdots + (x_n-y_n)^2}
$$

给出。度量空间将"距离"这个概念从 $\mathbb{R}^n$ 抽象到任意集合上，只保留距离的本质属性：

- **非负性与正定性**：距离非负，两点重合时距离为零
- **对称性**：从 $x$ 到 $y$ 的距离等于从 $y$ 到 $x$ 的距离
- **三角不等式**：绕行不会使距离缩短

这种抽象使得我们可以在函数空间、序列空间等各种无穷维空间中讨论"接近""收敛""连续"等几何与分析概念。

**完备性**的几何直觉是：空间中没有"空洞"。如果一个序列的各项彼此越来越近（Cauchy 序列），那么它必定趋向于空间中的某个点。$\mathbb{Q}$ 相对于 $\mathbb{R}$ 就是不完备的——有理数序列可以逼近 $\sqrt{2}$，但 $\sqrt{2}$ 不在有理数集中。

**压缩映射原理**的几何图像是：一个将空间向自身压缩的映射，反复迭代后必然收缩到某个固定点。这就像把一张橡皮膜不断向中心拉伸缩小，最终所有点都汇聚到同一个位置。

## 应用场景

1. **常微分方程解的存在唯一性**：Picard 迭代法利用 Banach 不动点定理证明初值问题 $y' = f(t,y)$, $y(t_0) = y_0$ 在适当条件下存在唯一解。

2. **积分方程**：Fredholm 积分方程和 Volterra 积分方程的求解可以转化为压缩映射的不动点问题。

3. **数值分析中的迭代法**：Newton 迭代法、Jacobi 迭代法、Gauss-Seidel 迭代法等的收敛性分析。

4. **分形几何**：自相似分形（如 Sierpinski 三角形、Cantor 集）可以看作迭代函数系统的不动点。

5. **图像压缩**：分形图像压缩基于迭代函数系统的吸引子（即不动点）。

## 数学理论（及推导）

### 1.1 度量空间的定义

**定义 1.1**（度量空间） 设 $X$ 是非空集合，映射 $d: X \times X \to \mathbb{R}$ 若满足以下公理，则称 $(X,d)$ 为**度量空间**：

1. **非负性**：$d(x,y) \geq 0$，且 $d(x,y) = 0 \iff x = y$
2. **对称性**：$d(x,y) = d(y,x)$
3. **三角不等式**：$d(x,z) \leq d(x,y) + d(y,z)$

其中 $d$ 称为 $X$ 上的**度量**（距离函数）。

**例 1.1**（欧氏空间） $\mathbb{R}^n$ 上的欧氏度量 $d(x,y) = \left(\sum_{i=1}^n |x_i - y_i|^2\right)^{1/2}$ 满足度量公理。

**例 1.2**（函数空间 $C[a,b]$） 设 $C[a,b]$ 为 $[a,b]$ 上连续函数全体，定义

$$
d(f,g) = \max_{t \in [a,b]} |f(t) - g(t)|
$$

则 $(C[a,b], d)$ 是度量空间。这是**一致收敛**度量的自然推广。

**例 1.3**（$L^p$ 空间） 设 $(X, \mathcal{F}, \mu)$ 为测度空间，$1 \leq p < \infty$，定义

$$
d(f,g) = \left( \int_X |f(x) - g(x)|^p \, d\mu(x) \right)^{1/p}
$$

在几乎处处相等的等价类上，$(L^p, d)$ 构成度量空间。

**例 1.4**（离散度量） 设 $X$ 为任意非空集合，定义

$$
d(x,y) = \begin{cases} 0 & x = y \\ 1 & x \neq y \end{cases}
$$

这是最简单的非平凡度量。

### 1.2 开集、闭集与连续映射

**定义 1.2**（开球） 度量空间 $(X,d)$ 中，以 $x_0$ 为心、$r > 0$ 为半径的**开球**定义为

$$
B(x_0, r) = \{ x \in X : d(x, x_0) < r \}
$$

**定义 1.3**（开集） $X$ 的子集 $G$ 称为**开集**，若对每个 $x \in G$，存在 $r > 0$ 使得 $B(x, r) \subset G$。

**定义 1.4**（连续映射） 设 $(X,d_1)$ 和 $(Y,d_2)$ 是两个度量空间，映射 $f: X \to Y$ 称为在 $x_0 \in X$ 处**连续**，若对任意 $\varepsilon > 0$，存在 $\delta > 0$ 使得

$$
d_1(x, x_0) < \delta \implies d_2(f(x), f(x_0)) < \varepsilon
$$

等价表述：$f$ 连续当且仅当开集的原像是开集。

### 1.3 完备性与 Cauchy 序列

**定义 1.5**（Cauchy 序列） 度量空间 $(X,d)$ 中的序列 $\{x_n\}$ 称为 **Cauchy 序列**（基本序列），若对任意 $\varepsilon > 0$，存在 $N \in \mathbb{N}$ 使得

$$
\forall\, m, n \geq N: \quad d(x_m, x_n) < \varepsilon
$$

**定义 1.6**（完备性） 度量空间 $(X,d)$ 称为**完备的**，若其中每个 Cauchy 序列都收敛于 $X$ 中的元素。

**命题 1.1** 任何收敛序列都是 Cauchy 序列，但反之不然。

**证明**：设 $x_n \to x$，则对任意 $\varepsilon > 0$，存在 $N$ 使得 $n \geq N$ 时 $d(x_n, x) < \varepsilon/2$。于是当 $m, n \geq N$ 时，

$$
d(x_m, x_n) \leq d(x_m, x) + d(x, x_n) < \varepsilon/2 + \varepsilon/2 = \varepsilon \quad \blacksquare
$$

**例 1.5**（不完备的例子） $(\mathbb{Q}, |\cdot|)$ 不完备。Cauchy 序列 $x_n = (1 + 1/n)^n \to e \notin \mathbb{Q}$。

**例 1.6** $(C[0,1], d)$ 在 $L^1$ 度量 $d(f,g) = \int_0^1 |f - g| \, dx$ 下不完备。可以构造连续函数序列逼近阶梯函数（阶梯函数不连续）。

**定理 1.1**（$C[a,b]$ 的完备性） $(C[a,b], d_\infty)$ 是完备的度量空间，其中 $d_\infty(f,g) = \max_{t \in [a,b]} |f(t) - g(t)|$。

**证明思路**：设 $\{f_n\}$ 是 $C[a,b]$ 中的一致 Cauchy 序列。对每个 $t \in [a,b]$，$\{f_n(t)\}$ 是 $\mathbb{R}$ 中的 Cauchy 序列（因为 $|f_n(t) - f_m(t)| \leq d_\infty(f_n, f_m)$），故有极限 $f(t) = \lim_{n\to\infty} f_n(t)$。由一致收敛的连续性定理，$f \in C[a,b]$，且 $d_\infty(f_n, f) \to 0$。$\blacksquare$

**定理 1.2**（$L^p$ 空间的完备性——Riesz-Fischer 定理） 设 $(X, \mathcal{F}, \mu)$ 为完备测度空间，$1 \leq p \leq \infty$，则 $L^p(X, \mu)$ 在度量 $d(f,g) = \|f - g\|_p$ 下完备。

### 1.4 压缩映射原理（Banach 不动点定理）

**定义 1.7**（压缩映射） 设 $(X,d)$ 是度量空间，映射 $T: X \to X$ 称为**压缩映射**，若存在常数 $0 \leq q < 1$ 使得

$$
d(Tx, Ty) \leq q \cdot d(x, y), \quad \forall\, x, y \in X
$$

其中 $q$ 称为压缩系数。

**定理 1.3**（Banach 不动点定理） 设 $(X,d)$ 是非空完备度量空间，$T: X \to X$ 是压缩系数为 $q$（$0 \leq q < 1$）的压缩映射，则：

1. **存在性**：$T$ 在 $X$ 中存在唯一不动点 $x^* \in X$，即 $Tx^* = x^*$。
2. **收敛性**：对任意初始点 $x_0 \in X$，迭代序列 $x_{n+1} = Tx_n$ 收敛于 $x^*$。
3. **误差估计**：
   - 先验估计：$d(x_n, x^*) \leq \frac{q^n}{1-q} d(x_0, x_1)$
   - 后验估计：$d(x_n, x^*) \leq \frac{q}{1-q} d(x_{n-1}, x_n)$

**证明**：

**(a) 不动点的存在性**：任取 $x_0 \in X$，令 $x_{n+1} = Tx_n$。先证 $\{x_n\}$ 是 Cauchy 序列。由压缩性，

$$
d(x_{n+1}, x_n) = d(Tx_n, Tx_{n-1}) \leq q \cdot d(x_n, x_{n-1}) \leq \cdots \leq q^n d(x_1, x_0)
$$

对 $m > n$，利用三角不等式和几何级数：

$$
\begin{aligned}
d(x_m, x_n) &\leq d(x_m, x_{m-1}) + d(x_{m-1}, x_{m-2}) + \cdots + d(x_{n+1}, x_n) \\
&\leq (q^{m-1} + q^{m-2} + \cdots + q^n) d(x_1, x_0) \\
&= q^n \frac{1 - q^{m-n}}{1 - q} d(x_1, x_0) \\
&\leq \frac{q^n}{1 - q} d(x_1, x_0)
\end{aligned}
$$

因 $0 \leq q < 1$，$\frac{q^n}{1-q} \to 0$，故 $\{x_n\}$ 是 Cauchy 序列。由完备性，存在 $x^* \in X$ 使得 $x_n \to x^*$。

再证 $x^*$ 是不动点。由 $T$ 的连续性（压缩映射自动Lipschitz连续）：

$$
Tx^* = T\left(\lim_{n\to\infty} x_n\right) = \lim_{n\to\infty} Tx_n = \lim_{n\to\infty} x_{n+1} = x^*
$$

**(b) 唯一性**：设 $x^*, y^*$ 都是不动点，则

$$
d(x^*, y^*) = d(Tx^*, Ty^*) \leq q \cdot d(x^*, y^*)
$$

因 $0 \leq q < 1$，必有 $d(x^*, y^*) = 0$，即 $x^* = y^*$。

**(c) 误差估计**：在 (a) 的估计中令 $m \to \infty$，利用距离函数的连续性：

$$
d(x^*, x_n) \leq \frac{q^n}{1-q} d(x_1, x_0) = \frac{q^n}{1-q} d(x_0, x_1)
$$

又

$$
d(x^*, x_n) \leq \sum_{k=n}^{\infty} d(x_{k+1}, x_k) \leq \sum_{k=n}^{\infty} q^k d(x_1, x_0) = \frac{q^n}{1-q} d(x_1, x_0)
$$

对后验估计，注意到 $d(x_{n+1}, x_n) \leq q \cdot d(x_n, x_{n-1})$，类似可得。$\blacksquare$

### 1.5 应用：常微分方程初值问题的解

考虑初值问题：

$$
y'(t) = f(t, y(t)), \quad y(t_0) = y_0
$$

等价的积分方程为：

$$
y(t) = y_0 + \int_{t_0}^t f(s, y(s))\, ds
$$

在 Banach 空间 $C[t_0 - \delta, t_0 + \delta]$ 上定义算子 $T$：

$$
(Ty)(t) = y_0 + \int_{t_0}^t f(s, y(s))\, ds
$$

若 $f$ 关于 $y$ 满足 Lipschitz 条件 $|f(t,y_1) - f(t,y_2)| \leq L|y_1 - y_2|$，取 $\delta$ 足够小使得 $L\delta < 1$，则 $T$ 是压缩映射。由 Banach 不动点定理，初值问题存在唯一解。这就是 **Picard-Lindelöf 定理**。

### 1.6 完备化定理

**定理 1.4**（完备化） 对任意度量空间 $(X,d)$，存在完备度量空间 $(\tilde{X}, \tilde{d})$ 和等距嵌入 $\phi: X \to \tilde{X}$ 使得 $\phi(X)$ 在 $\tilde{X}$ 中稠密。且在等距意义下，这样的完备化是唯一的。

**证明思路**：

1. 定义等价关系：$\{x_n\} \sim \{y_n\}$ 当且仅当 $d(x_n, y_n) \to 0$。
2. $\tilde{X}$ 为所有 Cauchy 序列的等价类的集合。
3. 定义度量 $\tilde{d}([\{x_n\}], [\{y_n\}]) = \lim_{n\to\infty} d(x_n, y_n)$（极限存在且与代表元选取无关）。
4. 嵌入 $\phi(x) = [\{x, x, x, \ldots\}]$。
5. 验证 $\phi(X)$ 在 $\tilde{X}$ 中稠密：给定 Cauchy 序列 $\{x_n\}$，等价类 $[\{x_n\}]$ 可由 $\phi(x_n)$ 逼近。
6. 验证 $\tilde{X}$ 完备，以及唯一性。$\blacksquare$

**例**：$\mathbb{R}$ 是 $\mathbb{Q}$ 的完备化；$L^p$ 空间是 $C[a,b]$ 在 $L^p$ 度量下的完备化。
