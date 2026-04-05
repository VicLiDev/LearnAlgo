# 第五章 三大基本定理

## 几何意义

泛函分析的"三大基本定理"（开映射定理、逆算子定理、闭图像定理、一致有界性原理）是无穷维空间分析的核心工具，它们深刻地刻画了有界线性算子（连续线性算子）在无穷维空间中的行为。

**开映射定理**说：Banach 空间之间的有界线性**满射**将开集映为开集。这意味着无穷维空间之间的"好的"线性映射不会"坍缩"空间——开球的像仍然包含一个开球。在有限维中这是显然的（线性映射的矩阵非奇异时满射，像就是整个空间），但在无穷维中需要完备性条件。

**逆算子定理**是开映射定理的直接推论：若 Banach 空间之间的有界线性算子是双射，则其逆也是有界的。在有限维中这也是显然的（矩阵可逆则逆矩阵有界），但无穷维中需要深刻地利用完备性。

**闭图像定理**提供了一个判断线性算子是否有界的强大工具：只需验证其图像（图像 $= \{(x, Tx) : x \in X\}$）是否闭，而不必直接估计 $\|Tx\|$。这在处理复杂算子时极为方便。

**一致有界性原理**（共鸣定理）说：如果一族有界线性算子在每一点处有界，那么它们在算子范数意义下一致有界。直观地说，"逐点有界"蕴含"一致有界"——这在无穷维中绝非平凡。

## 应用场景

1. **微分方程理论**：闭图像定理用于证明微分算子在某些 Banach 空间上的连续性。

2. **Fourier 级数的发散**：一致有界性原理的经典应用——存在连续函数，其 Fourier 级数在某些点发散。

3. **PDE 的适定性**：开映射定理和逆算子定理用于证明偏微分方程解的存在性和连续依赖性。

4. **算子理论**：谱理论中大量依赖三大基本定理来分析算子的性质。

5. **数值分析**：一致性原理用于分析有限元方法的稳定性。

## 数学理论（及推导）

### 5.1 预备知识

**引理 5.1**（Baire 纲定理） 完备度量空间不能表示为可数个无处稠密集的并集。

等价表述：完备度量空间中，可数个稠密开集的交集仍然稠密。

**证明思路**（第一形式）：设 $X = \bigcup_{n=1}^\infty F_n$，$F_n$ 是闭集。若每个 $F_n$ 无处稠密（即 int$(F_n) = \emptyset$），则可以构造一个 Cauchy 序列 $\{x_n\}$ 使得 $x_n \notin F_n$。由完备性，$x_n \to x$，但 $x \notin F_n$ 对所有 $n$ 成立，矛盾。$\blacksquare$

Baire 纲定理是三大基本定理共同的理论基石。

### 5.2 开映射定理

**定理 5.1**（开映射定理） 设 $X, Y$ 是 Banach 空间，$T \in \mathcal{B}(X,Y)$ 是满射（$TX = Y$），则 $T$ 是**开映射**：对 $X$ 中的每个开集 $U$，$TU$ 是 $Y$ 中的开集。

**证明**：

**第一步**：证明 $T(B_X)$ 在 $0$ 点"厚"。其中 $B_X = \{x \in X : \|x\| < 1\}$ 是 $X$ 的开单位球。

因 $T$ 是满射，$Y = T(X) = \bigcup_{n=1}^\infty T(nB_X) = \bigcup_{n=1}^\infty nT(B_X)$。由 Baire 纲定理，存在某个 $n$ 使得 $\overline{nT(B_X)}$ 含有内点，从而 $\overline{T(B_X)}$ 含有某个开球 $B(y_0, \varepsilon)$。

于是 $B(0, \varepsilon) \subset \overline{T(B_X)} - y_0 \subset \overline{T(B_X) - y_0} \subset \overline{T(2B_X)}$（利用对称性和 $y_0 \in \overline{T(B_X)}$ 的性质）。因此

$$
\overline{T(B_X)} \supset B\left(0, \frac{\varepsilon}{2}\right)
$$

**第二步**：由 $\overline{T(B_X)}$ 含球提升为 $T(B_X)$ 含球。

由第一步，$\overline{T(B_{1/2})} \supset B(0, \varepsilon/4)$。给定 $y \in Y$，$\|y\| < \varepsilon/4$，存在 $x_1 \in B_{1/2}$ 使得 $\|y - Tx_1\| < \varepsilon/8$。

一般地，取 $x_n \in B_{1/2^n}$ 使得 $\left\|y - \sum_{k=1}^n Tx_k\right\| < \varepsilon / 2^{n+2}$。令 $x = \sum_{k=1}^\infty x_k$，则

$$
\|x\| \leq \sum_{k=1}^\infty \|x_k\| \leq \sum_{k=1}^\infty \frac{1}{2^k} = 1
$$

且 $Tx = y$。这说明 $B(0, \varepsilon/4) \subset T(B_X)$。

**第三步**：$T$ 是开映射。设 $U \subset X$ 开，$y_0 \in T(U)$。取 $x_0 \in U$ 使 $Tx_0 = y_0$。因 $U$ 开，存在 $\delta > 0$ 使得 $B(x_0, \delta) \subset U$。由第二步，$T(B(0, \delta)) \supset B(0, c\delta)$（$c = \varepsilon/4$），故

$$
T(U) \supset T(B(x_0, \delta)) = y_0 + T(B(0,\delta)) \supset y_0 + B(0, c\delta) = B(y_0, c\delta)
$$

故 $T(U)$ 是开集。$\blacksquare$

### 5.3 逆算子定理

**定理 5.2**（逆算子定理/有界逆定理） 设 $X, Y$ 是 Banach 空间，$T \in \mathcal{B}(X,Y)$ 是双射（既单又满），则 $T^{-1} \in \mathcal{B}(Y,X)$（即 $T^{-1}$ 也是有界线性算子）。

**证明**：由开映射定理，$T$ 将开集映为开集。$T$ 是双射意味着 $T^{-1}$ 存在，且 $(T^{-1})^{-1}(U) = T(U)$ 对每个开集 $U$ 是开集，故 $T^{-1}$ 连续，即 $T^{-1} \in \mathcal{B}(Y,X)$。$\blacksquare$

**推论 5.1** 设 $X$ 是线性空间，$\|\cdot\|_1$ 和 $\|\cdot\|_2$ 是 $X$ 上的两个范数，且 $(X, \|\cdot\|_1)$ 和 $(X, \|\cdot\|_2)$ 都是 Banach 空间。若存在 $C > 0$ 使得 $\|x\|_2 \leq C\|x\|_1$，则两个范数等价。

**证明**：恒等映射 $I: (X, \|\cdot\|_1) \to (X, \|\cdot\|_2)$ 有界（因 $\|Ix\|_2 = \|x\|_2 \leq C\|x\|_1$）。由逆算子定理，$I^{-1} = I: (X, \|\cdot\|_2) \to (X, \|\cdot\|_1)$ 也有界，即存在 $C' > 0$ 使得 $\|x\|_1 \leq C'\|x\|_2$。$\blacksquare$

### 5.4 闭图像定理

**定义 5.1**（图像） 设 $T: X \to Y$ 是线性算子（不必有界），定义 $T$ 的**图像**为乘积空间 $X \times Y$ 的子集：

$$
\Gamma(T) = \{(x, Tx) : x \in D(T)\} \subset X \times Y
$$

其中 $D(T) \subset X$ 是 $T$ 的定义域。

**定义 5.2**（闭算子） 线性算子 $T: D(T) \subset X \to Y$ 称为**闭算子**，若其图像 $\Gamma(T)$ 在 $X \times Y$ 中是闭集。

等价条件：$x_n \to x$（$x_n \in D(T)$）且 $Tx_n \to y$ 蕴含 $x \in D(T)$ 且 $Tx = y$。

**注**：有界线性算子的图像总是闭的（因为 $T$ 连续，$\Gamma(T)$ 是连续映射 $x \mapsto (x, Tx)$ 的像，连续映射将闭集映为闭集——更准确地说，$\Gamma(T)$ 是映射 $x \mapsto (x,Tx)$ 的像，这个映射是到其像的同胚）。

**定理 5.3**（闭图像定理） 设 $X, Y$ 是 Banach 空间，$T: X \to Y$ 是线性算子（$D(T) = X$）。则 $T$ 有界当且仅当 $T$ 是闭算子。

**证明**：

$(\Rightarrow)$：已知。

$(\Leftarrow)$：$X \times Y$ 在范数 $\|(x,y)\| = \|x\| + \|y\|$ 下是 Banach 空间。$\Gamma(T)$ 是 $X \times Y$ 的闭子空间，故 $\Gamma(T)$ 本身也是 Banach 空间。

定义投影 $\pi_1: \Gamma(T) \to X$，$\pi_1(x, Tx) = x$。$\pi_1$ 是线性的、双射的、有界的（$\|\pi_1(x, Tx)\| = \|x\| \leq \|(x,Tx)\|$）。由逆算子定理，$\pi_1^{-1}$ 有界：

$$
\|(x, Tx)\| = \|\pi_1^{-1} x\| \leq \|\pi_1^{-1}\| \cdot \|x\|
$$

即 $\|x\| + \|Tx\| \leq C\|x\|$，故 $\|Tx\| \leq (C-1)\|x\|$，$T$ 有界。$\blacksquare$

**闭图像定理的应用模式**：要证明某个复杂算子 $T$ 有界，可以：
1. 构造序列 $x_n \to x$ 且 $Tx_n \to y$
2. 证明 $y = Tx$（即 $T$ 的图像闭）
3. 由闭图像定理得 $T$ 有界

这往往比直接估计 $\|Tx\|$ 更容易。

### 5.5 一致有界性原理（共鸣定理）

**定理 5.4**（一致有界性原理/共鸣定理） 设 $X$ 是 Banach 空间，$Y$ 是赋范线性空间，$\{T_\alpha\}_{\alpha \in A} \subset \mathcal{B}(X,Y)$ 是一族有界线性算子。若对每个 $x \in X$，

$$
\sup_{\alpha \in A} \|T_\alpha x\| < \infty \quad \text{（逐点有界）}
$$

则

$$
\sup_{\alpha \in A} \|T_\alpha\| < \infty \quad \text{（一致有界）}
$$

**证明**：令

$$
B_n = \{ x \in X : \sup_{\alpha} \|T_\alpha x\| \leq n \} = \bigcap_{\alpha} \{ x : \|T_\alpha x\| \leq n \}
$$

每个集合 $\{x : \|T_\alpha x\| \leq n\}$ 是闭集（$T_\alpha$ 连续），故 $B_n$ 是闭集。由逐点有界条件，$X = \bigcup_{n=1}^\infty B_n$。由 Baire 纲定理，存在某个 $N$ 使得 $B_N$ 含有内点，即存在 $x_0 \in X$ 和 $r > 0$ 使得 $B(x_0, r) \subset B_N$。

于是对任意 $x \in X$，$\|x\| \leq r$ 时，$x_0 + x \in B(x_0, r) \subset B_N$，故

$$
\|T_\alpha(x_0 + x)\| \leq N
$$

又 $x_0 \in B_N$，$\|T_\alpha x_0\| \leq N$，故

$$
\|T_\alpha x\| = \|T_\alpha(x_0 + x) - T_\alpha x_0\| \leq \|T_\alpha(x_0 + x)\| + \|T_\alpha x_0\| \leq 2N
$$

因此 $\|T_\alpha\| = \sup_{\|x\| \leq 1} \|T_\alpha x\| \leq 2N/r$。$\blacksquare$

### 5.6 经典应用：Fourier 级数的发散

**定理 5.5** 存在 $f \in C[0, 2\pi]$（$2\pi$ 周期连续函数），其 Fourier 级数在 $0$ 点发散。

**证明思路**：$f$ 在 $0$ 点的 Fourier 级数第 $n$ 个部分和为：

$$
S_n(f)(0) = \frac{1}{2\pi} \int_{-\pi}^{\pi} f(t) D_n(t) \, dt
$$

其中 $D_n(t) = \frac{\sin((n+1/2)t)}{\sin(t/2)}$ 是 Dirichlet 核。定义线性泛函 $\phi_n(f) = S_n(f)(0)$，其范数为

$$
\|\phi_n\| = \frac{1}{2\pi} \int_{-\pi}^{\pi} |D_n(t)| \, dt = L_n
$$

其中 $L_n$ 是 Lebesgue 常数。可以证明 $L_n \sim \frac{4}{\pi^2} \ln n \to \infty$。

若对每个 $f \in C[0, 2\pi]$，$\sup_n |\phi_n(f)| < \infty$，则由一致有界性原理，$\sup_n \|\phi_n\| = \sup_n L_n < \infty$，矛盾。故存在 $f$ 使得 $\sup_n |S_n(f)(0)| = \infty$，即 Fourier 级数在 $0$ 点发散。$\blacksquare$

### 5.7 三大定理的关系总结

```
Baire 纲定理
├── 开映射定理 ──→ 逆算子定理
│         └──→ 闭图像定理（通过投影映射 + 逆算子定理）
└── 一致有界性原理（共鸣定理）
```

四大定理（含 Baire 纲定理）构成了泛函分析的核心理论框架，它们的共同特点是：
- 都需要 **Banach 空间**（或至少是 Baire 空间）的完备性条件
- 在不完备空间中一般不成立
- 是无穷维分析区别于有限维线性代数的关键所在
