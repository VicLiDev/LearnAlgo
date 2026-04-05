# 第六章 Hahn-Banach 定理

## 几何意义

Hahn-Banach 定理是泛函分析中最基本也最深刻的定理之一，它有解析形式和几何形式两种等价表述。

**解析形式**的几何直觉是：在子空间上定义的一个"受控"的线性泛函，可以延拓到整个空间上而保持控制条件不变。就像在一个平面上定义了一个"有界的"线性函数，我们可以将其延伸到整个三维空间中，同时不超出原来的"界"。

**几何形式**（分离定理）的直觉更加直观：两个不相交的凸集可以被一个超平面分开。在 $\mathbb{R}^2$ 中，这就像用一条直线将两个不相交的圆分开；在 $\mathbb{R}^3$ 中，用一个平面将两个不相交的球体分开。超平面分离是凸几何的基本工具。

Hahn-Banach 定理的核心价值在于：它保证了**泛函足够多**。对于 Banach 空间中的每个非零元素 $x$，都存在有界线性泛函 $f$ 使得 $f(x) = \|x\|$（"取到范数"）。这意味着我们可以通过有界线性泛函来"探测"Banach 空间中的每个元素——泛函充当了无穷维空间中"坐标"的角色。

在 Hilbert 空间中，这个结论由 Riesz 表示定理自然给出；但在一般的 Banach 空间中，需要 Hahn-Banach 定理。

## 应用场景

1. **优化理论**：凸集分离定理是凸优化中 KKT 条件和对偶理论的理论基础。

2. **偏微分方程**：弱解的定义需要验证泛函的延拓性；变分方法中的极小化序列分析。

3. **概率论**：Daniell 积分通过 Hahn-Banach 延拓来构造测度。

4. **经济学**：竞争均衡的存在性证明依赖于凸集分离定理（第二福利定理）。

5. **度量几何**：证明 Banach 空间中某些距离函数的性质。

6. **量子信息**：密度算子与态的分离。

## 数学理论（及推导）

### 6.1 解析形式：控制延拓定理

**定义 6.1**（次线性泛函） 设 $X$ 是实线性空间，$p: X \to \mathbb{R}$ 称为**次线性泛函**（sublinear functional），若：

1. **正齐次性**：$p(\alpha x) = \alpha p(x)$，$\forall\, \alpha \geq 0$
2. **次可加性**：$p(x + y) \leq p(x) + p(y)$

**定理 6.1**（Hahn-Banach 延拓定理——实数形式） 设 $X$ 是实线性空间，$p: X \to \mathbb{R}$ 是次线性泛函，$M \subset X$ 是线性子空间，$f: M \to \mathbb{R}$ 是线性泛函且满足

$$
f(x) \leq p(x), \quad \forall\, x \in M
$$

则存在线性泛函 $\tilde{f}: X \to \mathbb{R}$ 使得

1. $\tilde{f}|_M = f$（延拓）
2. $\tilde{f}(x) \leq p(x)$，$\forall\, x \in X$（控制）

**证明**（使用 Zorn 引理）：

设 $\mathcal{F}$ 是所有满足条件的延拓对 $(N, g)$ 的集合，其中 $M \subset N \subset X$ 是子空间，$g: N \to \mathbb{R}$ 线性，$g|_M = f$，$g(x) \leq p(x)$（$x \in N$）。在 $\mathcal{F}$ 上定义偏序：$(N_1, g_1) \leq (N_2, g_2)$ 当且仅当 $N_1 \subset N_2$ 且 $g_2|_{N_1} = g_1$。

**第一步**：每条链有上界。设 $\{(N_\alpha, g_\alpha)\}$ 是一条链。令 $N = \bigcup_\alpha N_\alpha$，在 $N$ 上定义 $g(x) = g_\alpha(x)$（$x \in N_\alpha$）。由链的一致性，$g$ 的定义良定。$g$ 显然是线性的且满足 $g(x) \leq p(x)$。故 $(N, g) \in \mathcal{F}$ 是上界。

**第二步**（关键步骤）：一步延拓。需要证明若 $(N, g) \in \mathcal{F}$ 且 $N \neq X$，则存在严格更大的延拓。取 $z \in X \setminus N$，令 $N' = N \oplus \mathbb{R}z = \{x + tz : x \in N, t \in \mathbb{R}\}$。$N'$ 上的线性泛函 $g'$ 由 $g'(x + tz) = g(x) + ta$ 完全确定，其中 $a = g'(z) \in \mathbb{R}$ 待定。

需要选择 $a$ 使得 $g'(x + tz) \leq p(x + tz)$，即：

- 当 $t > 0$：$g(x/t) + a \leq p(x/t + z)$，即 $a \leq p(u + z) - g(u)$（$u = x/t \in N$）
- 当 $t < 0$：$g(x/t) + a \geq -p(-x/t - z)$，即 $a \geq g(v) - p(v - z)$（$v = -x/t \in N$）

因此需要：

$$
g(v) - p(v - z) \leq a \leq p(u + z) - g(u), \quad \forall\, u, v \in N
$$

这样的 $a$ 存在当且仅当：

$$
g(v) - p(v - z) \leq p(u + z) - g(u), \quad \forall\, u, v \in N
$$

即 $g(u) + g(v) \leq p(u + z) + p(v - z)$。由 $g$ 的控制条件：

$$
g(u) + g(v) = g(u + v) \leq p(u + v) = p((u + z) + (v - z)) \leq p(u + z) + p(v - z)
$$

故这样的 $a$ 存在。

**第三步**：由 Zorn 引理，$\mathcal{F}$ 有极大元 $(\tilde{X}, \tilde{f})$。若 $\tilde{X} \neq X$，由第二步可进一步延拓，与极大性矛盾。故 $\tilde{X} = X$。$\blacksquare$

**定理 6.2**（Hahn-Banach 延拓定理——复数形式） 设 $X$ 是复线性空间，$p: X \to \mathbb{R}$ 满足 $p(\alpha x) = |\alpha| p(x)$ 和 $p(x + y) \leq p(x) + p(y)$。设 $M \subset X$ 是线性子空间，$f: M \to \mathbb{C}$ 是线性泛函满足 $|f(x)| \leq p(x)$（$x \in M$）。则存在线性泛函 $\tilde{f}: X \to \mathbb{C}$ 满足：

1. $\tilde{f}|_M = f$
2. $|\tilde{f}(x)| \leq p(x)$，$\forall\, x \in X$

**证明思路**：设 $f = u + iv$，$u, v: M \to \mathbb{R}$。可以证明 $u$ 是实线性的，且 $f(x) = u(x) - iu(ix)$。将 $u$ 延拓为 $\tilde{u}: X \to \mathbb{R}$（实延拓），令 $\tilde{f}(x) = \tilde{u}(x) - i\tilde{u}(ix)$。验证 $\tilde{f}$ 是复线性的且 $|\tilde{f}(x)| \leq p(x)$。$\blacksquare$

### 6.2 有界线性泛函的延拓

**定理 6.3**（Hahn-Banach 延拓定理——赋范空间形式） 设 $X$ 是赋范线性空间，$M \subset X$ 是子空间，$f \in M^*$。则存在 $\tilde{f} \in X^*$ 使得：

1. $\tilde{f}|_M = f$
2. $\|\tilde{f}\| = \|f\|_{M^*}$（保范延拓）

**证明**：取 $p(x) = \|f\| \cdot \|x\|$（次线性泛函）。$|f(x)| \leq \|f\|\|x\| = p(x)$ 对 $x \in M$。由延拓定理，存在线性泛函 $\tilde{f}$ 使得 $\tilde{f}|_M = f$ 且 $|\tilde{f}(x)| \leq p(x) = \|f\| \cdot \|x\|$。故 $\|\tilde{f}\| \leq \|f\|$。又 $\tilde{f}|_M = f$，故 $\|\tilde{f}\| \geq \|f\|$。$\blacksquare$

### 6.3 重要推论

**推论 6.1**（泛函充分多） 设 $X$ 是赋范线性空间，$x_0 \neq 0$。则存在 $f \in X^*$ 使得 $f(x_0) = \|x_0\|$ 且 $\|f\| = 1$。

**证明**：在 $M = \text{span}\{x_0\}$ 上定义 $f(\alpha x_0) = \alpha \|x_0\|$。则 $\|f\|_{M^*} = 1$，$f(x_0) = \|x_0\|$。由延拓定理保范延拓到 $X$。$\blacksquare$

**推论 6.2** $x = 0$ 当且仅当对所有 $f \in X^*$，$f(x) = 0$。

**证明**：$\Rightarrow$ 显然。$\Leftarrow$：若 $x \neq 0$，由推论 6.1，存在 $f \in X^*$ 使 $f(x) = \|x\| \neq 0$，矛盾。$\blacksquare$

**推论 6.3** 设 $M$ 是 Banach 空间 $X$ 的闭子空间，$x_0 \in X \setminus M$。则存在 $f \in X^*$ 使得 $f|_M = 0$，$f(x_0) \neq 0$。

**证明**：在 $M' = M \oplus \mathbb{R} x_0$ 上定义 $f(m + tx_0) = t$。$f|_M = 0$，$f(x_0) = 1$。验证 $f$ 在 $M'$ 上有界（利用 $x_0 \notin M$ 的事实：$d(x_0, M) > 0$），然后延拓。$\blacksquare$

**推论 6.4** 设 $M$ 是赋范线性空间 $X$ 的子空间，则 $\overline{M} = \bigcap_{f \in X^*, f|_M = 0} \ker f$。

即：$M$ 的闭包恰好是所有在 $M$ 上为零的泛函的公共零点集。

### 6.4 几何形式：凸集分离定理

**定义 6.2**（超平面） Banach 空间 $X$ 中的**超平面**是形如 $\{x \in X : f(x) = c\}$ 的集合，其中 $f \in X^* \setminus \{0\}$，$c \in \mathbb{R}$（或 $\mathbb{C}$）。

**定理 6.4**（Hahn-Banach 分离定理——严格分离） 设 $X$ 是实 Banach 空间，$A, B$ 是 $X$ 中两个不相交的非空凸子集，且 $A$ 是开集。则存在 $f \in X^*$ 和 $c \in \mathbb{R}$ 使得

$$
f(a) < c < f(b), \quad \forall\, a \in A, b \in B
$$

即存在超平面严格分离 $A$ 和 $B$。

**证明思路**：取 $x_0 \in B - A = \{b - a : a \in A, b \in B\}$，可以证明 $M = B - A$ 是含 $0$ 的开凸集（因 $A$ 开），且 $x_0 \notin M$ 的某个邻域。取 $p(x) = \inf\{t > 0 : x/t \in M\}$（Minkowski 泛函），则 $p$ 是次线性泛函，$p(x_0) \geq 1$。在 $\text{span}\{x_0\}$ 上定义 $f(tx_0) = t$，则 $f(x) \leq p(x)$ 在子空间上成立。延拓到全空间后，$f$ 分离 $A$ 和 $B$。$\blacksquare$

**定理 6.5**（Hahn-Banach 分离定理——弱分离） 设 $A$ 是实 Banach 空间 $X$ 中的非空闭凸集，$x_0 \notin A$。则存在 $f \in X^*$ 和 $c \in \mathbb{R}$ 使得

$$
f(x_0) > c \geq f(a), \quad \forall\, a \in A
$$

**注**：复 Banach 空间中的分离定理将泛函取实部后应用实数版本。

### 6.5 应用：支撑超平面

**定理 6.6**（支撑超平面定理） 设 $X$ 是 Banach 空间，$K$ 是 $X$ 中具有非空内部的闭凸集，$x_0 \in \partial K$（边界点）。则存在 $f \in X^* \setminus \{0\}$ 使得

$$
f(x) \leq f(x_0), \quad \forall\, x \in K
$$

即存在超平面在 $x_0$ 处"支撑" $K$。

### 6.6 应用：正则性测度

**定理 6.7** 设 $C_0(\mathbb{R}^n)$ 是 $\mathbb{R}^n$ 上在无穷远处趋于零的连续函数空间。每个有界线性泛函 $f \in (C_0(\mathbb{R}^n))^*$ 可以表示为

$$
f(\phi) = \int_{\mathbb{R}^n} \phi(x) \, d\mu(x)
$$

其中 $\mu$ 是 $\mathbb{R}^n$ 上的有限正则 Borel 测度，且 $\|f\| = \|\mu\| = |\mu|(\mathbb{R}^n)$。

这是 **Riesz 表示定理**（$C_0$ 版本），其证明利用 Hahn-Banach 延拓。

### 6.7 Hahn-Banach 定理与选择公理

**注**：Hahn-Banach 定理的证明依赖于 Zorn 引理（等价于选择公理）。实际上，Hahn-Banach 定理弱于选择公理但独立于 ZF 公理系统——在某些没有选择公理的模型中，Hahn-Banach 定理成立但选择公理不成立。

这一事实说明，Hahn-Banach 定理是泛函分析中最"节约"地使用选择公理的核心定理。
