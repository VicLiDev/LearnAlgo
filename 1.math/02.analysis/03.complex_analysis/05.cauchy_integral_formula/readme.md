# 第五章 Cauchy 积分公式与解析函数性质

## 一、几何意义

### 1.1 Cauchy 积分公式的几何解释

Cauchy 积分公式

$$f(z_0) = \frac{1}{2\pi i}\oint_C \frac{f(z)}{z - z_0}\,dz$$

表明：解析函数在区域内部任意一点的值，完全由其在边界上的值决定。这是一种**加权平均**，权重为 $\frac{1}{z - z_0}$。

几何直观：边界上的点 $z$ 对内部点 $z_0$ 的"贡献"与距离 $|z - z_0|$ 成反比。越近的边界点对函数值的贡献越大。积分沿边界一周，恰好将所有边界点的贡献叠加得到精确的函数值。

### 1.2 高阶导数公式的几何意义

$$f^{(n)}(z_0) = \frac{n!}{2\pi i}\oint_C \frac{f(z)}{(z-z_0)^{n+1}}\,dz$$

高阶导数也是由边界值确定的。这意味着解析函数具有**无穷光滑性**——不像实函数那样可能出现可导但不二阶可导的情况。

### 1.3 最大模原理的几何意义

**最大模原理**：非常数的解析函数在区域内部的模不可能达到最大值。

几何直观：想象将解析函数视为一个"弹性薄膜"覆盖在区域上。如果薄膜不是完全平坦的（非常数），那么最高点一定出现在边界上。这一原理与调和函数的最大值原理一致（因为 $|f(z)|$ 的对数是调和函数）。

### 1.4 均值定理的几何意义

$$f(z_0) = \frac{1}{2\pi}\int_0^{2\pi} f(z_0 + re^{i\theta})\,d\theta$$

解析函数在圆心的值等于其在圆周上的**平均值**。这说明解析函数没有"局部凸起"或"局部凹陷"——任何偏离平均的值都会被对称位置的值补偿。

### 1.5 Schwarz 引理的几何意义

Schwarz 引理限制了解析函数在单位圆内的增长速度。如果 $f: \mathbb{D} \to \mathbb{D}$ 且 $f(0) = 0$，则 $|f(z)| \leq |z|$。

几何直观：单位圆到单位圆的映射在原点附近的"缩放因子"不能超过 1。这限制了保形映射的形变程度。

---

## 二、应用场景

### 2.1 解析延拓

Cauchy 积分公式是**解析延拓**的理论基础。如果两个解析函数在某段曲线上的值相同，则它们在整个区域内相同。这在物理中对应于唯一性定理。

### 2.2 偏微分方程的唯一性

Laplace 方程 $\Delta u = 0$ 的解由边界条件唯一确定（Dirichlet 问题）。这是 Cauchy 积分公式的直接推论。

### 2.3 函数估值

最大模原理常用于估计解析函数的上下界，在数论（如 Riemann zeta 函数的零点分布估计）和数学物理中有重要应用。

### 2.4 整函数的分类

Liouville 定理将有界整函数（全平面上解析的函数）限定为常数。这直接导致了**代数基本定理**的优雅证明。

### 2.5 数值分析

Cauchy 积分公式可用于高精度数值微分。通过选取适当的围道，可以避免有限差分法中的截断误差问题。

---

## 三、数学理论（及推导）

### 3.1 Cauchy 积分公式

**定理**：设 $f(z)$ 在简单闭曲线 $C$ 及其内部 $D$ 上解析，$z_0 \in D$（$z_0$ 不在 $C$ 上），则：

$$f(z_0) = \frac{1}{2\pi i}\oint_C \frac{f(z)}{z - z_0}\,dz$$

**证明**：

由于 $f(z)$ 在 $z_0$ 处连续，$\forall \varepsilon > 0$，$\exists \delta > 0$，当 $|z - z_0| < \delta$ 时，$|f(z) - f(z_0)| < \varepsilon$。

以 $z_0$ 为心、$r < \delta$ 为半径作小圆 $C_r$（正向），由复合闭路定理：

$$\oint_C \frac{f(z)}{z-z_0}\,dz = \oint_{C_r} \frac{f(z)}{z-z_0}\,dz$$

$$= \oint_{C_r} \frac{f(z_0)}{z-z_0}\,dz + \oint_{C_r} \frac{f(z)-f(z_0)}{z-z_0}\,dz$$

第一项：$\oint_{C_r} \frac{f(z_0)}{z-z_0}\,dz = f(z_0) \oint_{C_r} \frac{dz}{z-z_0} = f(z_0) \cdot 2\pi i$

（因为 $\oint_{C_r} \frac{dz}{z-z_0} = \int_0^{2\pi}\frac{ire^{i\theta}}{re^{i\theta}}\,d\theta = 2\pi i$。）

第二项的估计：

$$\left|\oint_{C_r} \frac{f(z)-f(z_0)}{z-z_0}\,dz\right| \leq \oint_{C_r} \frac{|f(z)-f(z_0)|}{|z-z_0|}\,|dz| \leq \frac{\varepsilon}{r} \cdot 2\pi r = 2\pi\varepsilon$$

由于 $\varepsilon$ 任意，第二项为零。因此：

$$\oint_C \frac{f(z)}{z-z_0}\,dz = 2\pi i f(z_0) \implies f(z_0) = \frac{1}{2\pi i}\oint_C \frac{f(z)}{z-z_0}\,dz \quad \blacksquare$$

### 3.2 高阶导数公式

**定理**：在 Cauchy 积分公式的条件下，$f(z)$ 在 $D$ 内具有任意阶导数：

$$f^{(n)}(z_0) = \frac{n!}{2\pi i}\oint_C \frac{f(z)}{(z-z_0)^{n+1}}\,dz, \quad n = 1, 2, 3, \ldots$$

**证明（用数学归纳法）**：

**基础步骤**（$n=1$）：由 Cauchy 积分公式：

$$f(z_0) = \frac{1}{2\pi i}\oint_C \frac{f(z)}{z-z_0}\,dz$$

考虑差商：

$$\frac{f(z_0 + h) - f(z_0)}{h} = \frac{1}{2\pi i h}\oint_C f(z)\left[\frac{1}{z-z_0-h} - \frac{1}{z-z_0}\right]dz$$

$$= \frac{1}{2\pi i h}\oint_C \frac{f(z)}{(z-z_0)(z-z_0-h)}\,h\,dz = \frac{1}{2\pi i}\oint_C \frac{f(z)}{(z-z_0)(z-z_0-h)}\,dz$$

另一方面：

$$\frac{1}{2\pi i}\oint_C \frac{f(z)}{(z-z_0)^2}\,dz - \frac{f(z_0+h)-f(z_0)}{h}$$

$$= \frac{1}{2\pi i}\oint_C \frac{f(z)}{(z-z_0)^2} - \frac{f(z)}{(z-z_0)(z-z_0-h)}\,dz$$

$$= \frac{h}{2\pi i}\oint_C \frac{f(z)}{(z-z_0)^2(z-z_0-h)}\,dz$$

当 $h \to 0$ 时，利用估值定理，上式的绝对值 $\leq \frac{|h|}{2\pi} \cdot \frac{M \cdot 2\pi R}{d^3} \to 0$（$R$ 为 $C$ 的长度，$d$ 为 $z_0$ 到 $C$ 的距离）。因此：

$$f'(z_0) = \lim_{h\to 0}\frac{f(z_0+h)-f(z_0)}{h} = \frac{1}{2\pi i}\oint_C \frac{f(z)}{(z-z_0)^2}\,dz = \frac{1!}{2\pi i}\oint_C \frac{f(z)}{(z-z_0)^{1+1}}\,dz$$

**归纳步骤**：假设公式对 $n=k$ 成立。类似地，对 $f^{(k)}(z_0+h) - f^{(k)}(z_0)$ 进行估计，可得：

$$f^{(k+1)}(z_0) = \frac{(k+1)!}{2\pi i}\oint_C \frac{f(z)}{(z-z_0)^{k+2}}\,dz \quad \blacksquare$$

**推论（解析函数的无穷可微性）**：解析函数具有任意阶导数，各阶导数仍为解析函数。

### 3.3 Cauchy 不等式

**定理**：设 $f(z)$ 在 $|z-z_0| \leq R$ 上解析，$|f(z)| \leq M$，则：

$$|f^{(n)}(z_0)| \leq \frac{n! \cdot M}{R^n}$$

**证明**：由高阶导数公式和估值不等式：

$$|f^{(n)}(z_0)| = \left|\frac{n!}{2\pi i}\oint_{|z-z_0|=R}\frac{f(z)}{(z-z_0)^{n+1}}\,dz\right| \leq \frac{n!}{2\pi}\cdot\frac{M}{R^{n+1}}\cdot 2\pi R = \frac{n!M}{R^n}$$

### 3.4 Liouville 定理

**定理**：有界的整函数（即全平面上解析且有界的函数）必为常数。

**证明**：设 $f(z)$ 在全平面解析，且 $|f(z)| \leq M$。

由 Cauchy 不等式，对任意 $z_0 \in \mathbb{C}$ 和任意 $R > 0$：

$$|f'(z_0)| \leq \frac{M}{R}$$

令 $R \to \infty$，得 $|f'(z_0)| = 0$，即 $f'(z_0) = 0$。由于 $z_0$ 任意，故 $f(z)$ 为常数。$\blacksquare$

**推论（代数基本定理）**：任何非常数的复系数多项式至少有一个复根。

**证明（Liouville 定理证明）**：设 $p(z) = a_n z^n + \cdots + a_0$（$n \geq 1$，$a_n \neq 0$）在 $\mathbb{C}$ 上无零点。

定义 $f(z) = \frac{1}{p(z)}$，则 $f(z)$ 为整函数。

当 $|z| \to \infty$ 时，$|p(z)| \to \infty$（主项 $a_n z^n$ 主导），故 $f(z) \to 0$。

因此 $f(z)$ 有界（在充分大的圆外 $|f(z)| < \varepsilon$，在圆内连续函数有界）。

由 Liouville 定理，$f(z)$ 为常数，从而 $p(z)$ 为常数，矛盾。$\blacksquare$

### 3.5 最大模原理

**定理**：设 $f(z)$ 在区域 $D$ 内解析，在闭区域 $\overline{D}$ 上连续。若 $f(z)$ 不是常数，则 $|f(z)|$ 的最大值只能在 $\overline{D}$ 的边界上达到。

**证明（用均值定理）**：

**均值定理**：设 $f(z)$ 在 $|z - z_0| \leq R$ 上解析，则：

$$f(z_0) = \frac{1}{2\pi}\int_0^{2\pi} f(z_0 + Re^{i\theta})\,d\theta$$

**推导**：由 Cauchy 积分公式，令 $C$ 为 $|z-z_0| = R$：

$$f(z_0) = \frac{1}{2\pi i}\oint_{|z-z_0|=R}\frac{f(z)}{z-z_0}\,dz = \frac{1}{2\pi i}\int_0^{2\pi}\frac{f(z_0+Re^{i\theta})}{Re^{i\theta}}\cdot iRe^{i\theta}\,d\theta = \frac{1}{2\pi}\int_0^{2\pi} f(z_0+Re^{i\theta})\,d\theta$$

**最大模原理的证明**：

用反证法。设在 $z_0 \in D$ 处 $|f(z)|$ 达到最大值 $M = |f(z_0)|$。

由均值定理：

$$|f(z_0)| = \left|\frac{1}{2\pi}\int_0^{2\pi} f(z_0+Re^{i\theta})\,d\theta\right| \leq \frac{1}{2\pi}\int_0^{2\pi} |f(z_0+Re^{i\theta})|\,d\theta \leq M$$

但 $|f(z_0+Re^{i\theta})| \leq M$，要使等号成立（左边 $= M$），必须有 $|f(z_0+Re^{i\theta})| = M$ 对几乎所有 $\theta$ 成立。由连续性，$|f(z)| = M$ 在整个圆 $|z-z_0| = R$ 上成立。

取 $R$ 足够小使圆完全含于 $D$ 中，则 $|f(z)| = M$ 在一个非空开集上成立。由恒等定理（两个解析函数在具有聚点的集合上相同则处处相同，应用于 $f(z)$ 和 $Me^{i\alpha}$），$f(z)$ 为常数。$\blacksquare$

### 3.6 Schwarz 引理

**定理**：设 $f(z)$ 在单位圆 $\mathbb{D} = \{z : |z| < 1\}$ 内解析，满足：
1. $|f(z)| \leq 1$（$z \in \mathbb{D}$）
2. $f(0) = 0$

则：
1. $|f(z)| \leq |z|$（$z \in \mathbb{D}$）
2. $|f'(0)| \leq 1$

且等号在某个 $z_0 \neq 0$ 处成立当且仅当 $f(z) = e^{i\alpha}z$（$\alpha$ 为实常数）。

**证明**：令 $g(z) = \frac{f(z)}{z}$（$z \neq 0$），定义 $g(0) = f'(0)$。

$g(z)$ 在 $|z| < 1$ 内解析。对任意 $0 < r < 1$，在 $|z| = r$ 上：

$$|g(z)| = \frac{|f(z)|}{|z|} \leq \frac{1}{r}$$

由最大模原理，$|g(z)| \leq \frac{1}{r}$ 对一切 $|z| \leq r$ 成立。令 $r \to 1$，得 $|g(z)| \leq 1$，即 $|f(z)| \leq |z|$。

取 $z \to 0$，得 $|f'(0)| = |g(0)| \leq 1$。

若存在 $z_0 \neq 0$ 使 $|f(z_0)| = |z_0|$，则 $|g(z_0)| = 1$。由最大模原理，$g(z)$ 为常数 $e^{i\alpha}$，即 $f(z) = e^{i\alpha}z$。$\blacksquare$

### 3.7 常用推论与不等式汇总

| 定理 | 内容 | 应用 |
|:---:|:---|:---:|
| Cauchy 积分公式 | $f(z_0) = \frac{1}{2\pi i}\oint_C \frac{f(z)}{z-z_0}\,dz$ | 函数值由边界值决定 |
| 高阶导数公式 | $f^{(n)}(z_0) = \frac{n!}{2\pi i}\oint_C \frac{f(z)}{(z-z_0)^{n+1}}\,dz$ | 解析函数无穷可微 |
| Cauchy 不等式 | $\|f^{(n)}(z_0)\| \leq \frac{n!M}{R^n}$ | 导数估计 |
| Liouville 定理 | 有界整函数为常数 | 代数基本定理 |
| 最大模原理 | 解析函数的模在边界上取最大值 | 函数估计 |
| 均值定理 | $f(z_0) = \frac{1}{2\pi}\int_0^{2\pi} f(z_0+re^{i\theta})\,d\theta$ | 平均值性质 |
| Schwarz 引理 | $\|f(z)\| \leq \|z\|$（$f(0)=0$, $\|f\|\leq 1$） | 共形映射的刚性 |
