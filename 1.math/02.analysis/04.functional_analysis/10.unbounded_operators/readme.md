# 第十章 无界算子与自伴算子

## 几何意义

在前面的章节中，我们主要讨论有界线性算子——这类算子在整个空间上定义且保持连续性。然而，数学物理中最核心的算子往往是无界的——**微分算子**本质上就是无界算子（因为微分会放大高频成分）。无界算子不能在整个空间上定义（否则与闭图像定理矛盾），而只能在空间的某个稠密子空间（定义域）上有意义。

**自伴算子**是无界算子理论中最重要的一类算子。它是有限维 Hermite 矩阵（$A = A^*$）在无穷维的推广。在 $\mathbb{R}^n$ 中，实对称矩阵的特征值是实的，特征向量可以选为正交的；在无穷维 Hilbert 空间中，自伴算子的谱也是实数子集，且存在"谱分解"——将算子表示为"连续的"特征值分解。

**对称**与**自伴**的区别是无穷维分析中最微妙也最重要的概念之一。在有限维中，对称矩阵自动是自伴的；但在无穷维中，对称算子的定义域可能"不够大"——虽然 $\langle Tx, y \rangle = \langle x, Ty \rangle$ 在定义域中成立，但算子的共轭可能定义在更大的空间上，导致 $T \neq T^*$。这种区别直接影响到谱的性质：对称算子的谱未必是实数，但自伴算子的谱一定是实数。

**谱定理**是算子理论的巅峰：它将一般的自伴算子表示为"积分型"的对角化——就像 Fourier 变换将函数分解为不同频率的成分一样，谱定理将自伴算子分解为不同"频率"（谱值）上的投影算子的"积分"。

## 应用场景

1. **量子力学**：位置算子 $\hat{x} = x$、动量算子 $\hat{p} = -i\hbar \frac{d}{dx}$、哈密顿量 $\hat{H} = -\frac{\hbar^2}{2m}\Delta + V(x)$ 都是自伴算子。

2. **偏微分方程**：Laplace 算子 $-\Delta$ 在适当的定义域上自伴，其谱决定了热方程、波动方程解的性态。

3. **Sturm-Liouville 理论**：二阶ODE特征值问题 $-y'' + q(x)y = \lambda y$ 归结为自伴算子的谱分析。

4. **量子信息**：密度算子（正的迹类自伴算子）描述量子态；POVM（正算子值测度）描述量子测量。

5. **随机过程**：无穷维 Ornstein-Uhlenbeck 过程的生成元是自伴算子。

## 数学理论（及推导）

### 10.1 无界算子的定义

**定义 10.1**（稠定算子） 设 $H$ 是 Hilbert 空间。线性算子 $T: D(T) \subset H \to H$ 称为**稠定算子**，若其定义域 $D(T)$ 在 $H$ 中稠密（$\overline{D(T)} = H$）。

**定义 10.2**（图与闭算子） $T$ 的**图像**（graph）定义为：

$$
\Gamma(T) = \{(x, Tx) : x \in D(T)\} \subset H \times H
$$

$T$ 称为**闭算子**，若 $\Gamma(T)$ 在 $H \times H$ 中是闭子空间。

等价条件：若 $x_n \to x$（$x_n \in D(T)$），$Tx_n \to y$，则 $x \in D(T)$ 且 $Tx = y$。

**命题 10.1** 有界线性算子是闭算子。无界算子可能闭也可能不闭。

**命题 10.2**（Hellinger-Toeplitz 定理） 设 $T: H \to H$ 是定义在整个 Hilbert 空间上的对称算子（$\langle Tx, y \rangle = \langle x, Ty \rangle$），则 $T$ 有界。

**意义**：无界的对称算子**不可能**在整个空间上定义。这解释了为什么无界算子只能定义在稠密子空间上。

### 10.2 伴随算子

**定义 10.3**（伴随算子） 设 $T: D(T) \subset H \to H$ 是稠定算子。定义 $T$ 的**伴随算子** $T^*$，其定义域为：

$$
D(T^*) = \{y \in H : \exists\, z \in H \text{ 使得 } \langle Tx, y \rangle = \langle x, z \rangle, \, \forall\, x \in D(T)\}
$$

对 $y \in D(T^*)$，定义 $T^*y = z$（由 Riesz 表示定理，$z$ 唯一确定）。

即 $T^*$ 由如下关系定义：

$$
\langle Tx, y \rangle = \langle x, T^*y \rangle, \quad \forall\, x \in D(T), y \in D(T^*)
$$

**命题 10.3** $T^*$ 是闭算子（即使 $T$ 不是闭的）。

**命题 10.4** $T$ 有界闭当且仅当 $D(T) = H$ 且 $T \in \mathcal{B}(H)$。

### 10.3 对称算子与自伴算子

**定义 10.4**（对称算子） 稠定算子 $T$ 称为**对称的**（symmetric / Hermitian），若：

$$
D(T) \subset D(T^*), \quad T^*|_{D(T)} = T
$$

即 $\langle Tx, y \rangle = \langle x, Ty \rangle$ 对所有 $x, y \in D(T)$ 成立。

等价条件：$\langle Tx, x \rangle \in \mathbb{R}$ 对所有 $x \in D(T)$（$H$ 是复 Hilbert 空间时）。

**定义 10.5**（自伴算子） 稠定算子 $T$ 称为**自伴的**（self-adjoint），若：

$$
T = T^*
$$

即 $D(T) = D(T^*)$ 且 $T = T^*|_{D(T)}$。

**定义 10.6**（本质自伴算子） 对称算子 $T$ 称为**本质自伴的**，若其闭包 $\overline{T}$ 是自伴的。

**关键区别**：

| 性质 | 对称算子 | 自伴算子 |
|------|---------|---------|
| 定义域 | $D(T) \subset D(T^*)$ | $D(T) = D(T^*)$ |
| 谱 | $\sigma(T) \subset \mathbb{C}$，可能含非实数 | $\sigma(T) \subset \mathbb{R}$ |
| 谱分解 | 不一定有 | 有（谱定理） |
| 生成酉群 | 不一定 | 有（Stone 定理） |
| 量子力学 | 不可观测量 | 可观测量 |

### 10.4 谱定理

谱定理是算子理论的核心成果，有多种等价表述形式。

**定理 10.1**（谱定理——乘法算子形式） 设 $A$ 是 Hilbert 空间 $H$ 上的自伴算子，则存在测度空间 $(M, \mu)$、可测函数 $a: M \to \mathbb{R}$ 和酉算子 $U: H \to L^2(M, \mu)$ 使得：

$$
(UAU^{-1}f)(m) = a(m) f(m), \quad f \in L^2(M, \mu)
$$

即 $A$ 酉等价于 $L^2$ 空间上的乘法算子。

**定理 10.2**（谱定理——投影值测度形式） 设 $A$ 是 Hilbert 空间 $H$ 上的自伴算子，则存在唯一的投影值测度（spectral measure / resolution of identity）$E: \mathcal{B}(\mathbb{R}) \to \mathcal{B}(H)$ 使得：

$$
A = \int_{-\infty}^{+\infty} \lambda \, dE(\lambda)
$$

即对任意 $x \in D(A)$，

$$
\langle Ax, x \rangle = \int_{-\infty}^{+\infty} \lambda \, d\langle E(\lambda)x, x \rangle
$$

**投影值测度** $E$ 满足：
1. $E(\emptyset) = 0$，$E(\mathbb{R}) = I$
2. $E(\Delta \cap \Delta') = E(\Delta)E(\Delta')$（投影的乘幂性）
3. $E\left(\bigcup_{n=1}^\infty \Delta_n\right) = \sum_{n=1}^\infty E(\Delta_n)$（强算子拓扑下的可数可加性）

**定理 10.3**（谱定理——函数演算形式） 设 $A$ 是自伴算子，$E$ 是其投影值测度。对有界 Borel 函数 $f: \mathbb{R} \to \mathbb{C}$，定义

$$
f(A) = \int_{-\infty}^{+\infty} f(\lambda) \, dE(\lambda)
$$

则映射 $f \mapsto f(A)$ 满足：
1. $(f+g)(A) = f(A) + g(A)$
2. $(fg)(A) = f(A)g(A)$
3. $\bar{f}(A) = f(A)^*$
4. $\|f(A)\| = \|f\|_\infty$（上确界范数）

### 10.5 有界函数演算与谱测度

由谱定理，可以对自伴算子 $A$ 定义各种函数：

- **单位分解**：$I = \int dE(\lambda) = E(\mathbb{R})$
- **算子本身**：$A = \int \lambda \, dE(\lambda)$
- **预解算子**：$(A - zI)^{-1} = \int \frac{1}{\lambda - z} \, dE(\lambda)$（$z \notin \sigma(A)$）
- **指数算子**：$e^{itA} = \int e^{it\lambda} \, dE(\lambda)$
- **正部与负部**：$A_+ = \int_{[0,\infty)} \lambda \, dE(\lambda)$，$A_- = -\int_{(-\infty,0)} \lambda \, dE(\lambda)$

### 10.6 Stone 定理

**定理 10.4**（Stone 定理） 设 $A$ 是 Hilbert 空间 $H$ 上的自伴算子。则 $A$ 生成一个强连续单参数酉群 $\{U(t)\}_{t \in \mathbb{R}}$：

$$
U(t) = e^{itA} = \int_{-\infty}^{+\infty} e^{it\lambda} \, dE(\lambda)
$$

满足：
1. $U(0) = I$
2. $U(t+s) = U(t)U(s)$（群性质）
3. $U(t)^* = U(-t) = U(t)^{-1}$（酉性）
4. $\lim_{t \to 0} \|U(t)x - x\| = 0$（强连续性）

且 $A$ 是无穷小生成元：

$$
Ax = \lim_{t \to 0} \frac{U(t)x - x}{it} \quad (x \in D(A))
$$

**证明**：由谱定理和指数的定义直接得出酉性和强连续性。群性质来自指数函数的加法公式。无穷小生成元的性质来自对 $e^{it\lambda}$ 在 $t = 0$ 处的 Taylor 展开。$\blacksquare$

**逆命题**（Stone 定理的逆）：每个强连续单参数酉群 $\{U(t)\}$ 都由唯一的一个自伴算子 $A$ 生成。

### 10.7 应用：量子力学

**10.7.1 量子力学的基本公设**

在量子力学中，Hilbert 空间 $H = L^2(\mathbb{R}^3)$ 描述系统的量子态空间：

- **量子态**：$H$ 中的单位向量 $\psi$（$\|\psi\| = 1$），相差一个相因子 $e^{i\theta}$ 的态等价。
- **可观测量**：自伴算子 $A$。测量值在 $\sigma(A) \subset \mathbb{R}$ 中。
- **测量值**：测量 $A$ 得到值在 Borel 集 $\Delta \subset \mathbb{R}$ 中的概率为 $\|E(\Delta)\psi\|^2$。
- **期望值**：$\langle A \rangle_\psi = \langle \psi, A\psi \rangle = \int \lambda \, d\langle \psi, E(\lambda)\psi \rangle$。
- **演化**：$\psi(t) = e^{-it\hat{H}/\hbar} \psi(0)$（Schrödinger 方程），其中 $\hat{H}$ 是哈密顿量。

**10.7.2 基本算子**

**(a) 位置算子** $\hat{x}$：在 $L^2(\mathbb{R})$ 中，$(\hat{x}\psi)(x) = x\psi(x)$。

- 定义域：$D(\hat{x}) = \{\psi \in L^2(\mathbb{R}) : x\psi(x) \in L^2(\mathbb{R})\}$（稠密）
- 自伴
- 谱：$\sigma(\hat{x}) = \mathbb{R}$（纯连续谱）
- 投影值测度：$E(\Delta)\psi = \chi_\Delta(x)\psi(x)$

**(b) 动量算子** $\hat{p}$：$(\hat{p}\psi)(x) = -i\hbar \psi'(x)$。

- 定义域：Sobolev 空间 $D(\hat{p}) = H^1(\mathbb{R})$（稠密）
- 自伴（需要选择正确的边界条件）
- 通过 Fourier 变换 $\mathcal{F}$ 与位置算子相联系：$\hat{p} = \mathcal{F}^{-1} \hat{x} \mathcal{F}$
- 谱：$\sigma(\hat{p}) = \mathbb{R}$（纯连续谱）

**(c) 对易关系**（Heisenberg 不确定性原理）：

$$
[\hat{x}, \hat{p}] = \hat{x}\hat{p} - \hat{p}\hat{x} = i\hbar I
$$

由此可推出不确定性关系：

$$
\Delta x \cdot \Delta p \geq \frac{\hbar}{2}
$$

**10.7.3 氢原子哈密顿量**

$$
\hat{H} = -\frac{\hbar^2}{2m}\Delta - \frac{e^2}{|x|}
$$

$\hat{H}$ 的谱由两部分组成：
- **离散谱**（点谱）：$E_n = -\frac{me^4}{2\hbar^2 n^2}$，$n = 1, 2, \ldots$（束缚态）
- **连续谱**：$[0, +\infty)$（散射态）

### 10.8 自伴延拓与亏指数

**定义 10.7**（亏指数） 设 $T$ 是对称算子，定义**亏子空间**：

$$
\mathcal{N}_+ = \ker(T^* - iI), \quad \mathcal{N}_- = \ker(T^* + iI)
$$

**亏指数**定义为 $n_\pm = \dim \mathcal{N}_\pm$。

**定理 10.5**（von Neumann 自伴延拓定理） 对称算子 $T$ 有自伴延拓当且仅当 $n_+ = n_-$。自伴延拓的集合与 $\mathcal{N}_+ \to \mathcal{N}_-$ 的酉算子之间存在一一对应。

**例 10.1**（动量算子的自伴延拓） 在 $L^2[0,1]$ 上，考虑 $T = -i\frac{d}{dx}$，$D(T) = C^\infty_0(0,1)$（紧支光滑函数）。$T$ 对称但不是自伴的。亏指数 $n_+ = n_- = 1$，故 $T$ 有自伴延拓。每个自伴延拓对应一个边界条件 $f(1) = e^{i\theta}f(0)$（$\theta \in \mathbb{R}$）。

### 10.9 无界算子的例子总结

| 算子 | 空间 | 定义域 | 类型 | 谱 |
|------|------|--------|------|----|
| $\frac{d}{dx}$ | $L^2[0,\infty)$ | $H^1_0$ | 非自伴 | 右半复平面 |
| $-i\frac{d}{dx}$ | $L^2(\mathbb{R})$ | $H^1(\mathbb{R})$ | 自伴 | $\mathbb{R}$ |
| $-\Delta$ | $L^2(\mathbb{R}^n)$ | $H^2(\mathbb{R}^n)$ | 正自伴 | $[0,+\infty)$ |
| $-\Delta + V(x)$ | $L^2(\mathbb{R}^n)$ | $H^2(\mathbb{R}^n)$ | 自伴 | 依赖 $V$ |
| 谐振子 $-\Delta + x^2$ | $L^2(\mathbb{R})$ | $D$ | 正自伴 | $\{2n+1\}$ |

这些算子构成了量子力学和 PDE 理论中最重要的无界算子家族。
