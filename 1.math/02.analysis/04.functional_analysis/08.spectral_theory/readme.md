# 第八章 谱理论

## 几何意义

谱理论是泛函分析中研究线性算子"内在结构"的核心工具，它是有限维线性代数中特征值理论的深刻推广。

在有限维空间中，矩阵 $A$ 的特征值 $\lambda$ 满足 $\det(A - \lambda I) = 0$，即 $(A - \lambda I)x = 0$ 有非零解。特征值刻画了矩阵的"振荡模式"——通过特征值分解 $A = PDP^{-1}$，线性变换被对角化，复杂的变换被分解为简单的标量乘法。

在无穷维空间中，算子的谱（spectrum）是特征值概念的推广。谱不仅包含点谱（特征值），还包含连续谱和剩余谱。谱的存在和分布直接决定了算子的性质——例如，算子的范数与其谱半径密切相关（谱半径公式），算子的可逆性与零点是否在谱中有关。

谱理论的几何图像可以理解为：将复平面上的每个点 $\lambda$ 与算子 $T - \lambda I$ 的"好坏"对应起来。$\lambda$ 在正则集中意味着 $T - \lambda I$ 有良好定义的有界逆；$\lambda$ 在谱中意味着 $T - \lambda I$ 在某种意义上"退化"了。

Banach 代数框架为谱理论提供了更统一、更强大的语言。在这个框架下，可以证明谱总是非空紧集——这是代数（Gelfand 理论）与分析（泛函分析）的完美结合。

## 应用场景

1. **量子力学**：可观测量对应自伴算子，其谱是可能的测量值。位置算子的谱是 $\mathbb{R}$（连续谱），氢原子哈密顿量的谱是分立的（点谱）。

2. **微分方程**：微分算子的谱决定了方程解的性态。热方程的解趋于零的速度由 Laplace 算子的谱决定。

3. **信号处理**：滤波器的频率响应可以用算子的谱来描述。

4. **振动分析**：弦、膜的振动频率由 Laplace 算子的特征值给出。

5. **数值线性代数**：迭代法的收敛速度由迭代矩阵的谱半径决定；特征值算法（QR 算法）的理论基础。

## 数学理论（及推导）

### 8.1 谱的基本概念

**定义 8.1**（正则集与谱） 设 $X$ 是复 Banach 空间，$T \in \mathcal{B}(X)$。复数 $\lambda \in \mathbb{C}$ 称为 $T$ 的**正则值**（正则点），若 $T - \lambda I$ 是双射（既单又满）。

$T - \lambda I$ 的逆 $(T - \lambda I)^{-1}$ 称为 $T$ 在 $\lambda$ 处的**预解算子**，记为 $R(\lambda, T)$。

$T$ 的**谱**定义为所有不是正则值的复数之集：

$$
\sigma(T) = \mathbb{C} \setminus \rho(T)
$$

其中 $\rho(T)$ 是正则集。

**定义 8.2**（谱的分类） 谱 $\sigma(T)$ 可以进一步分为三部分：

1. **点谱** $\sigma_p(T)$：$\lambda$ 使得 $T - \lambda I$ 不是单射。等价地，存在 $x \neq 0$ 使得 $Tx = \lambda x$。此时 $\lambda$ 称为**特征值**，$x$ 称为对应的**特征向量**。

2. **连续谱** $\sigma_c(T)$：$\lambda$ 使得 $T - \lambda I$ 是单射、值域稠密，但值域不是全空间（即逆存在但不有界）。

3. **剩余谱** $\sigma_r(T)$：$\lambda$ 使得 $T - \lambda I$ 是单射、值域不稠密。

因此：$\sigma(T) = \sigma_p(T) \cup \sigma_c(T) \cup \sigma_r(T)$（不相交并）。

### 8.2 谱的基本性质

**定理 8.1** 设 $X$ 是复 Banach 空间，$T \in \mathcal{B}(X)$。

**(a)** $\rho(T)$ 是开集，$\sigma(T)$ 是闭集。

**(b)** 对 $\lambda \in \rho(T)$，预解算子 $R(\lambda, T) \in \mathcal{B}(X)$。

**(c)** 预解方程：对 $\lambda, \mu \in \rho(T)$，

$$
R(\lambda, T) - R(\mu, T) = (\mu - \lambda) R(\lambda, T) R(\mu, T)
$$

**(d)** $\sigma(T)$ 是 $\mathbb{C}$ 中的非空紧集。

**(e)** $\sigma(T) \subset \{ \lambda \in \mathbb{C} : |\lambda| \leq \|T\| \}$。

**证明**：

**(a)** 设 $\lambda_0 \in \rho(T)$。对 $\lambda \in \mathbb{C}$，利用 Neumann 级数：

$$
T - \lambda I = (T - \lambda_0 I) - (\lambda - \lambda_0)I = (T - \lambda_0 I)\left[I - (\lambda - \lambda_0)(T - \lambda_0 I)^{-1}\right]
$$

当 $|\lambda - \lambda_0| \cdot \|(T - \lambda_0 I)^{-1}\| < 1$ 时，$I - (\lambda - \lambda_0)R(\lambda_0, T)$ 可逆（Neumann 级数收敛），故 $\lambda \in \rho(T)$。因此 $\rho(T)$ 是开集。

**(c)** 直接计算：

$$
R(\lambda, T) = (T - \lambda I)^{-1}, \quad R(\mu, T) = (T - \mu I)^{-1}
$$

$$
R(\lambda, T) - R(\mu, T) = R(\lambda, T)(T - \mu I)R(\mu, T) - R(\lambda, T)(T - \lambda I)R(\mu, T)
$$

$$
= R(\lambda, T)[(T - \mu I) - (T - \lambda I)]R(\mu, T) = (\lambda - \mu)R(\lambda, T)R(\mu, T)
$$

**(e)** 若 $|\lambda| > \|T\|$，则

$$
R(\lambda, T) = \frac{1}{\lambda}\left(I - \frac{T}{\lambda}\right)^{-1} = \frac{1}{\lambda}\sum_{n=0}^\infty \frac{T^n}{\lambda^n}
$$

Neumann 级数收敛（因为 $\|T/\lambda\| < 1$），故 $\lambda \in \rho(T)$。因此 $\sigma(T) \subset \overline{B(0, \|T\|)}$。$\blacksquare$

**(d) 的证明**需要更多工具（Liouville 定理），在 8.4 节给出。

### 8.3 谱半径

**定义 8.3**（谱半径） $T \in \mathcal{B}(X)$ 的**谱半径**定义为：

$$
r(T) = \sup\{|\lambda| : \lambda \in \sigma(T)\}
$$

**定理 8.2**（Gelfand 谱半径公式）

$$
r(T) = \lim_{n \to \infty} \|T^n\|^{1/n} = \inf_{n \geq 1} \|T^n\|^{1/n}
$$

**证明思路**：利用 Hadamard 公式。预解算子 $R(\lambda, T) = \sum_{n=0}^\infty T^n / \lambda^{n+1}$ 在 $|\lambda| > r(T)$ 时收敛。由复分析的 Laurent 级数理论，收敛半径恰好是 $r(T)$。故

$$
r(T) = \limsup_{n \to \infty} \|T^n\|^{1/n}
$$

再利用次可乘性 $\|T^{m+n}\| \leq \|T^m\| \cdot \|T^n\|$（Fekete 引理），$\limsup = \lim = \inf$。$\blacksquare$

**推论 8.1** $r(T) \leq \|T\|$，等号不一定成立。

### 8.4 谱的非空性

**定理 8.3**（谱非空） 设 $X$ 是非零的复 Banach 空间，$T \in \mathcal{B}(X)$，则 $\sigma(T) \neq \emptyset$。

**证明**：假设 $\sigma(T) = \emptyset$，则 $\rho(T) = \mathbb{C}$，预解算子 $R(\lambda, T)$ 对所有 $\lambda \in \mathbb{C}$ 有定义且解析。

对任意 $f \in X^*$ 和 $x \in X$，定义 $F(\lambda) = f(R(\lambda, T)x)$。$F$ 是全纯函数。由预解方程，$R(\lambda, T)R(\mu, T) = R(\mu, T)R(\lambda, T)$。

对 $|\lambda| > \|T\|$，Neumann 级数给出：

$$
R(\lambda, T) = \sum_{n=0}^\infty \frac{T^n}{\lambda^{n+1}}
$$

故

$$
F(\lambda) = \sum_{n=0}^\infty \frac{f(T^n x)}{\lambda^{n+1}}
$$

当 $|\lambda| \to \infty$ 时，$\|R(\lambda, T)\| \leq 1/(|\lambda| - \|T\|) \to 0$，故 $F(\lambda) \to 0$。

由 Liouville 定理，$F$ 恒为零。因此 $f(R(\lambda,T)x) = 0$ 对所有 $f \in X^*$，$x \in X$，$\lambda \in \mathbb{C}$ 成立。由 Hahn-Banach 定理推论，$R(\lambda, T) = 0$，矛盾（$R(\lambda, T)$ 可逆）。$\blacksquare$

### 8.5 Banach 代数中的谱

**定义 8.4**（Banach 代数） 具有乘法的 Banach 空间 $\mathcal{A}$ 称为 **Banach 代数**，若乘法满足结合律和分配律，且

$$
\|ab\| \leq \|a\| \cdot \|b\|, \quad \forall\, a, b \in \mathcal{A}
$$

**例 8.1** $\mathcal{B}(X)$ 是 Banach 代数（算子乘法的范数次可乘性）。$C(K)$（紧 Hausdorff 空间上的连续函数）是交换 Banach 代数。

**定义 8.5** 设 $\mathcal{A}$ 是含单位元的 Banach 代数，$a \in \mathcal{A}$。$a$ 的**谱**定义为：

$$
\sigma(a) = \{\lambda \in \mathbb{C} : a - \lambda e \text{ 不可逆}\}
$$

其中 $e$ 是单位元。

**定理 8.4** 设 $\mathcal{A}$ 是含单位元的复 Banach 代数，$a \in \mathcal{A}$，则：

1. $\sigma(a)$ 是非空紧集
2. $\sigma(a) \subset \{\lambda : |\lambda| \leq \|a\|\}$
3. 谱半径公式：$r(a) = \lim_{n \to \infty} \|a^n\|^{1/n}$

### 8.6 自伴算子的谱

**定理 8.5** 设 $H$ 是 Hilbert 空间，$T \in \mathcal{B}(H)$ 是自伴算子（$T^* = T$），则：

1. $\sigma(T) \subset \mathbb{R}$（谱是实的）
2. 若 $T$ 正（$\langle Tx, x \rangle \geq 0$），则 $\sigma(T) \subset [0, +\infty)$
3. $\|T\| = r(T)$（范数等于谱半径）

**证明**（自伴算子谱为实）：

设 $\lambda = \alpha + i\beta \in \sigma(T)$，$\beta \neq 0$。令 $S = T - \alpha I$（自伴），$\lambda - \alpha = i\beta$。计算

$$
\|(S - i\beta I)x\|^2 = \langle Sx - i\beta x, Sx - i\beta x \rangle = \|Sx\|^2 + |\beta|^2 \|x\|^2 \geq |\beta|^2 \|x\|^2
$$

故 $S - i\beta I$ 有有界逆，$\lambda \notin \sigma(T)$，矛盾。$\blacksquare$

### 8.7 谱映射定理

**定理 8.6**（谱映射定理——多项式版本） 设 $T \in \mathcal{B}(X)$，$p(z) = a_0 + a_1 z + \cdots + a_n z^n$ 是多项式，$p(T) = a_0 I + a_1 T + \cdots + a_n T^n$，则

$$
\sigma(p(T)) = p(\sigma(T)) = \{p(\lambda) : \lambda \in \sigma(T)\}
$$

**例 8.2** 若 $T^2 = I$（对合），则 $\sigma(T) \subset \{-1, 1\}$。

**例 8.3** 若 $T^2 = T$（投影），则 $\sigma(T) \subset \{0, 1\}$。
