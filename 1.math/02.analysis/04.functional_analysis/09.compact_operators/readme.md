# 第九章 紧算子与Fredholm理论

## 几何意义

紧算子是无穷维空间中最接近有限维算子的一类算子。在有限维空间中，线性算子（矩阵）自动将有界集映为有界集，且由于有界闭集是紧集，线性算子实际上将有界闭集映为紧集。在无穷维空间中，大多数有界算子不具备这个性质（Riesz 引理表明无穷维空间的单位球不紧），但**紧算子**恰好保留了这一有限维特征。

紧算子的几何图像：将有界集"压缩"到一个"近似有限维"的子集中。例如，积分算子

$$
(Tf)(s) = \int_a^b K(s,t) f(t) \, dt
$$

将一个函数空间中的有界函数族映射为一个"更光滑"的函数族——光滑函数族可以很好地被有限维子空间逼近（Arzela-Ascoli 定理）。

Riesz-Schauder 理论揭示了紧算子谱的有限维特征：除了 $0$ 以外，紧算子的谱只包含特征值，每个特征值的重数有限，且特征值最多可数地聚积于 $0$。这与有限维矩阵的特征值理论极为相似。

Fredholm 择一性是线性代数中 $Ax = b$ 的解的存在性条件的推广：要么方程有唯一解，要么齐次方程有非零解。

## 应用场景

1. **积分方程**：Fredholm 积分方程 $f(x) - \lambda \int_a^b K(x,y) f(y) \, dy = g(x)$ 的解的存在性和唯一性。

2. **微分方程的特征值问题**：Green 函数将微分方程特征值问题转化为紧算子的特征值问题。

3. **数值分析**：有限秩算子（有限维逼近）是紧算子的子类；Galerkin 方法和配置方法的收敛性分析。

4. **物理**：量子力学中的散射理论、统计物理中的相变理论。

5. **逆问题**：紧算子的不适定性分析（紧算子的逆不连续）。

## 数学理论（及推导）

### 9.1 紧算子的定义与性质

**定义 9.1**（紧算子） 设 $X, Y$ 是赋范线性空间。线性算子 $T: X \to Y$ 称为**紧算子**（全连续算子），若 $T$ 将 $X$ 中的有界集映为 $Y$ 中的**相对紧集**（即 $\overline{T(B)}$ 是紧集，其中 $B$ 是 $X$ 的有界集）。

等价条件：对 $X$ 中的任意有界序列 $\{x_n\}$，$\{Tx_n\}$ 有收敛子列。

记紧算子之集为 $\mathcal{K}(X,Y)$，简记 $\mathcal{K}(X) = \mathcal{K}(X,X)$。

**命题 9.1** 紧算子是有界线性算子。

**证明**：若 $T$ 不有界，则存在序列 $\{x_n\}$ 使得 $\|x_n\| = 1$ 但 $\|Tx_n\| \to \infty$。$\{x_n\}$ 有界，但 $\{Tx_n\}$ 无收敛子列（因为收敛序列必有界），矛盾。$\blacksquare$

**例 9.1**（有限秩算子） 设 $T: X \to Y$ 的值域是有限维的（$\dim \text{ran}(T) < \infty$），则 $T$ 是紧算子。特别地，形如

$$
Tx = \sum_{k=1}^n f_k(x) y_k
$$

的算子（$f_k \in X^*$，$y_k \in Y$）是紧的。

**例 9.2**（积分算子） 设 $K \in C([a,b] \times [a,b])$，积分算子

$$
(Tf)(s) = \int_a^b K(s,t) f(t) \, dt
$$

是 $C[a,b] \to C[a,b]$ 的紧算子（由 Arzela-Ascoli 定理）。

**例 9.3**（对角算子） 在 $\ell^2$ 上，对角算子 $Tx = (\lambda_1 x_1, \lambda_2 x_2, \ldots)$ 是紧的当且仅当 $\lambda_n \to 0$。

### 9.2 紧算子的代数性质

**定理 9.1** 设 $X, Y, Z$ 是赋范线性空间。

**(a)** $\mathcal{K}(X,Y)$ 是 $\mathcal{B}(X,Y)$ 的闭子空间。

**(b)** 若 $T \in \mathcal{K}(X,Y)$，$S \in \mathcal{B}(Y,Z)$，则 $ST \in \mathcal{K}(X,Z)$。

**(c)** 若 $T \in \mathcal{K}(X,Y)$，$S \in \mathcal{B}(Z,X)$，则 $TS \in \mathcal{K}(Z,Y)$。

**(d)** $\mathcal{K}(X)$ 是 $\mathcal{B}(X)$ 的闭双边理想。

**证明**（$a$——紧算子列的极限是紧的）：设 $T_n \in \mathcal{K}(X,Y)$，$\|T_n - T\| \to 0$。设 $\{x_m\}$ 是 $X$ 中的有界序列。对每个 $n$，$\{T_n x_m\}_m$ 有收敛子列。对角线法：取 $n=1$，$\{T_1 x_m\}$ 有收敛子列 $\{T_1 x_{m^{(1)}_k}\}$。对 $n=2$，$\{T_2 x_{m^{(1)}_k}\}$ 有收敛子列 $\{T_2 x_{m^{(2)}_k}\}$。如此继续，对角线序列 $\{x_{m^{(k)}_k}\}$ 使得对每个 $n$，$\{T_n x_{m^{(k)}_k}\}_k$ 收敛。

对 $\varepsilon > 0$，取 $n$ 使 $\|T_n - T\| < \varepsilon/3M$（$M = \sup \|x_m\|$）。因 $\{T_n x_{m^{(k)}_k}\}$ 收敛，存在 $K$ 使 $k, l \geq K$ 时 $\|T_n x_{m^{(k)}_k} - T_n x_{m^{(l)}_l}\| < \varepsilon/3$。则

$$
\|Tx_{m^{(k)}_k} - Tx_{m^{(l)}_l}\| \leq \|Tx_{m^{(k)}_k} - T_n x_{m^{(k)}_k}\| + \|T_n x_{m^{(k)}_k} - T_n x_{m^{(l)}_l}\| + \|T_n x_{m^{(l)}_l} - Tx_{m^{(l)}_l}\| < \varepsilon
$$

故 $\{Tx_{m^{(k)}_k}\}$ 是 Cauchy 列，由 $Y$ 的完备性收敛。$\blacksquare$

### 9.3 Riesz-Schauder 理论

以下设 $X$ 是无穷维 Banach 空间，$T \in \mathcal{K}(X)$。

**定理 9.2**（Riesz-Schauder 理论） 设 $T$ 是 Banach 空间 $X$ 上的紧算子，$\lambda \neq 0$。则以下等价：

1. $\lambda \in \sigma_p(T)$（$\lambda$ 是 $T$ 的特征值）
2. $\lambda \in \sigma(T)$

即对 $\lambda \neq 0$，$T$ 的谱只含点谱（特征值），没有连续谱和剩余谱。

**定理 9.3**（特征空间的有限维性） 对 $\lambda \neq 0$，$T$ 的特征空间（对应特征值 $\lambda$）是有限维的：

$$
\dim \ker(T - \lambda I) < \infty
$$

**证明思路**：若 $\ker(T - \lambda I)$ 无穷维，在单位球上取无穷序列 $\{x_n\}$ 两两正交（或足够分离），则 $Tx_n = \lambda x_n$，$\{Tx_n\}$ 无收敛子列（因 $\|Tx_n - Tx_m\| = |\lambda| \|x_n - x_m\|$），与 $T$ 的紧性矛盾。$\blacksquare$

**定理 9.4**（谱的聚积） $T$ 的非零特征值最多有可数个，且若有无穷多个，则它们聚积于 $0$。

$$
\sigma(T) \setminus \{0\} = \{\lambda_n\}_{n=1}^N \quad (N \leq \infty)
$$

若 $N = \infty$，则 $\lambda_n \to 0$。

**证明思路**：对任意 $\varepsilon > 0$，满足 $|\lambda| \geq \varepsilon$ 的特征值只有有限个（否则可以构造有界序列 $\{x_n\}$ 使得 $\{Tx_n\}$ 无收敛子列）。$\blacksquare$

**例 9.4** 考虑 $\ell^2$ 上的紧算子 $Te_n = \lambda_n e_n$（$\{e_n\}$ 是标准基，$\lambda_n \to 0$）。则 $\sigma(T) = \{0\} \cup \{\lambda_1, \lambda_2, \ldots\}$，每个 $\lambda_n \neq 0$ 都是特征值，$0$ 在谱中（$T$ 不是满射，因为 $T$ 不可能紧且可逆）。

### 9.4 Fredholm 择一性

**定理 9.5**（Fredholm 择一性） 设 $T \in \mathcal{K}(X)$，$\lambda \neq 0$。则以下两条恰有一条成立：

**(I)** 齐次方程 $(T - \lambda I)x = 0$ 只有零解，且非齐次方程 $(T - \lambda I)x = y$ 对每个 $y \in X$ 有唯一解。

**(II)** 齐次方程 $(T - \lambda I)x = 0$ 有非零解，且非齐次方程 $(T - \lambda I)x = y$ 不是对每个 $y$ 都有解。

等价地：$T - \lambda I$ 要么可逆，要么不是单射（当 $\lambda \neq 0$ 时）。

**证明**：关键在于 $T - \lambda I$ 是 Fredholm 算子（index $= 0$），由 Riesz-Schauder 理论，$T - \lambda I$ 是单射当且仅当它是满射。$\blacksquare$

**命题 9.2** 对 $T - \lambda I$ 和 $T^* - \bar{\lambda} I$（$T^*$ 是 $T$ 的共轭算子），以下维数关系成立：

$$
\dim \ker(T - \lambda I) = \dim \ker(T^* - \bar{\lambda} I) < \infty
$$

$$
\text{ran}(T - \lambda I) = \ker(T^* - \bar{\lambda} I)^\perp
$$

$$
\text{ran}(T^* - \bar{\lambda} I) = \ker(T - \lambda I)^\perp
$$

### 9.5 紧算子的谱分解

**定理 9.6**（紧自伴算子的谱分解） 设 $H$ 是可分的 Hilbert 空间，$T \in \mathcal{K}(H)$ 且自伴（$T^* = T$），则存在 $H$ 的标准正交基 $\{e_n\}$ 和实数列 $\{\lambda_n\}$ 使得：

1. $Te_n = \lambda_n e_n$
2. $\lambda_n \to 0$（或只有有限个非零 $\lambda_n$）
3. $T = \sum_{n=1}^\infty \lambda_n \langle \cdot, e_n \rangle e_n$（按算子范数收敛）

**证明思路**：

由谱定理（自伴紧算子版本），存在正交的特征向量 $\{e_n\}$ 和实特征值 $\{\lambda_n\}$。$\lambda_n \to 0$ 由紧性得出。展开式 $Tx = \sum \lambda_n \langle x, e_n \rangle e_n$ 就是 Fourier 展开在算子值函数上的推广。$\blacksquare$

### 9.6 Fredholm 积分方程

考虑第二类 Fredholm 积分方程：

$$
f(x) - \lambda \int_a^b K(x,y) f(y) \, dy = g(x)
$$

其中 $K \in C([a,b] \times [a,b])$，$g \in C[a,b]$ 给定，$f$ 未知。

定义积分算子 $Tf(x) = \int_a^b K(x,y) f(y) \, dy$，方程可写为：

$$(I - \lambda T)f = g$$

因 $T$ 是紧算子（$C[a,b] \to C[a,b]$），由 Fredholm 择一性：

**推论 9.1** 第二类 Fredholm 积分方程：

- 若 $\lambda^{-1}$ 不是 $T$ 的特征值，则方程有唯一解，可由 Neumann 级数

$$
f = (I - \lambda T)^{-1} g = \sum_{n=0}^\infty \lambda^n T^n g
$$

给出（当 $|\lambda|$ 足够小时收敛）。

- 若 $\lambda^{-1}$ 是 $T$ 的特征值，齐次方程 $(I - \lambda T)f = 0$ 有非零解，非齐次方程有解当且仅当 $g$ 与所有齐次共轭方程的解正交。

### 9.7 迹与迹类算子

**定义 9.2**（迹类算子） Hilbert 空间 $H$ 上的紧算子 $T$ 称为**迹类算子**（trace class），若 $\sum_{n=1}^\infty \langle |T| e_n, e_n \rangle < \infty$，其中 $\{e_n\}$ 是标准正交基，$|T| = (T^* T)^{1/2}$。

**定义 9.3**（迹） 迹类算子 $T$ 的**迹**定义为：

$$
\text{tr}(T) = \sum_{n=1}^\infty \langle Te_n, e_n \rangle
$$

**命题 9.3** 迹的定义与标准正交基的选取无关（Lidskii 定理）。

**命题 9.4**（迹与特征值） 迹类算子的迹等于其特征值之和（计入重数）：

$$
\text{tr}(T) = \sum_{\lambda \in \sigma_p(T)} \lambda \cdot \dim \ker(T - \lambda I)
$$

这是有限维矩阵 $\text{tr}(A) = \sum_i \lambda_i$ 的推广。
