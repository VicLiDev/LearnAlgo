# 第六章 级数展开

## 一、几何意义

### 1.1 幂级数与收敛圆

幂级数 $\sum_{n=0}^{\infty} a_n(z-z_0)^n$ 的收敛域是一个以 $z_0$ 为圆心的**圆盘** $|z - z_0| < R$（可能 $R = 0$ 或 $R = \infty$）。这是复分析特有的现象——实幂级数的收敛域是一个区间，而复幂级数的收敛域是一个圆盘。

**几何直观**：复平面是二维的，"收敛半径" $R$ 确定了以 $z_0$ 为中心的收敛圆。在圆内级数绝对收敛，在圆外级数发散，在圆周上的行为需要具体分析。

**收敛圆与奇点的关系**：收敛圆上至少存在一个奇点。如果 $f(z)$ 在 $|z-z_0| < R$ 内解析但在 $|z-z_0| = R$ 上有奇点，则幂级数不可能收敛到超过 $R$ 的范围。

### 1.2 Taylor 展开的几何意义

Taylor 级数将解析函数在 $z_0$ 附近的信息编码为各阶导数值：

$$f(z) = \sum_{n=0}^{\infty} \frac{f^{(n)}(z_0)}{n!}(z-z_0)^n$$

几何意义：解析函数在收敛圆内的行为完全由其在圆心处的各阶导数决定。越靠近圆心，低阶项贡献越大；越靠近圆周，需要越多的高阶项。

### 1.3 Laurent 级数的几何意义

Laurent 级数包含正幂项和负幂项：

$$f(z) = \sum_{n=-\infty}^{\infty} a_n(z-z_0)^n = \sum_{n=0}^{\infty} a_n(z-z_0)^n + \sum_{n=1}^{\infty} \frac{a_{-n}}{(z-z_0)^n}$$

- **解析部分**（正幂项）：在 $|z-z_0| < R_2$ 内收敛，描述函数的"正规"行为。
- **主部**（负幂项）：在 $|z-z_0| > R_1$ 内收敛，描述函数在奇点 $z_0$ 附近的"奇异"行为。

收敛域为**环形区域** $R_1 < |z-z_0| < R_2$。

### 1.4 奇点分类的几何意义

- **可去奇点**：函数在该点附近有界，如同"平滑地填补了一个小洞"。
- **极点**：函数在该点附近趋向无穷，像一条"伸向无穷的管道"。$m$ 阶极点对应主部到 $\frac{1}{(z-z_0)^m}$ 项。
- **本性奇点**：函数在该点附近的行为极其复杂——Picard 定理表明，在本性奇点的任意邻域内，函数取到几乎所有的复数值（至多遗漏一个值），故称"本性"。

---

## 二、应用场景

### 2.1 函数逼近与计算

Taylor 级数和 Laurent 级数是计算函数值的数值基础。例如 $e^z$、$\sin z$ 等函数的标准库实现就是基于级数展开。

### 2.2 物理学中的渐近展开

在量子场论和统计力学中，经常需要研究函数在奇点附近的行为。Laurent 展开的主部直接给出了函数的奇异行为（如发散阶数），这对重整化理论至关重要。

### 2.3 信号处理中的滤波器设计

传递函数的极点位置决定了系统的稳定性（极点在左半平面）和频率响应特性。极点和零点的分布（零极点图）是滤波器设计的核心工具。

### 2.4 留数计算的基础

Laurent 级数中 $(z-z_0)^{-1}$ 项的系数 $a_{-1}$ 就是留数。掌握级数展开是计算留数的关键。

### 2.5 解析延拓

利用 Taylor 级数，可以将函数的定义域从一个小圆盘逐步扩展到更大的区域。Riemann zeta 函数的解析延拓就是这种方法论的典型应用。

---

## 三、数学理论（及推导）

### 3.1 复数项级数

**定义**：复数项级数 $\sum_{n=1}^{\infty} z_n$（$z_n = x_n + iy_n$）收敛的充要条件是 $\sum x_n$ 和 $\sum y_n$ 都收敛。

**绝对收敛**：$\sum |z_n|$ 收敛时称 $\sum z_n$ 绝对收敛。绝对收敛蕴含收敛。

**Cauchy 收敛准则**：$\sum z_n$ 收敛 $\iff$ $\forall \varepsilon > 0$，$\exists N$，当 $m > n > N$ 时 $\left|\sum_{k=n+1}^{m} z_k\right| < \varepsilon$。

### 3.2 幂级数

**定义**：形如 $\sum_{n=0}^{\infty} a_n(z-z_0)^n$ 的级数称为**幂级数**（Power series），其中 $a_n \in \mathbb{C}$。

**Abel 定理**：若幂级数在 $z_1 \neq z_0$ 处收敛，则它在 $|z - z_0| < |z_1 - z_0|$ 内绝对收敛。

**证明**：设 $\sum a_n(z_1-z_0)^n$ 收敛，则 $a_n(z_1-z_0)^n \to 0$，故 $|a_n(z_1-z_0)^n| \leq M$。

对 $|z-z_0| < |z_1-z_0|$，令 $\rho = \frac{|z-z_0|}{|z_1-z_0|} < 1$：

$$|a_n(z-z_0)^n| = |a_n(z_1-z_0)^n| \cdot \rho^n \leq M\rho^n$$

由 $\sum M\rho^n$ 收敛（等比级数），$\sum |a_n(z-z_0)^n|$ 收敛。

**收敛半径**：

$$R = \frac{1}{\limsup_{n\to\infty}\sqrt[n]{|a_n|}}$$

（Cauchy-Hadamard 公式）

当 $\lim_{n\to\infty}\left|\frac{a_{n+1}}{a_n}\right|$ 存在时，也可以用比值法：$R = \lim_{n\to\infty}\left|\frac{a_n}{a_{n+1}}\right|$。

### 3.3 幂级数的解析性

**定理**：幂级数 $\sum_{n=0}^{\infty} a_n(z-z_0)^n$ 的和函数 $f(z)$ 在收敛圆 $|z-z_0| < R$ 内解析，且可以逐项求导：

$$f'(z) = \sum_{n=1}^{\infty} na_n(z-z_0)^{n-1}$$

逐项求导后的级数具有相同的收敛半径。

**推论**：幂级数的和函数在其收敛圆内具有任意阶导数。

### 3.4 Taylor 级数展开

**定理（Taylor 展开定理）**：设 $f(z)$ 在 $|z - z_0| < R$ 内解析，则在该圆内：

$$f(z) = \sum_{n=0}^{\infty} \frac{f^{(n)}(z_0)}{n!}(z-z_0)^n$$

且展开式唯一。

**证明**：设 $|z - z_0| = r < R$。取 $\rho$ 满足 $r < \rho < R$，由 Cauchy 积分公式：

$$f(z) = \frac{1}{2\pi i}\oint_{|\zeta-z_0|=\rho}\frac{f(\zeta)}{\zeta-z}\,d\zeta$$

由于 $|z - z_0| < |\zeta - z_0| = \rho$，有：

$$\frac{1}{\zeta - z} = \frac{1}{(\zeta-z_0) - (z-z_0)} = \frac{1}{\zeta-z_0}\cdot\frac{1}{1 - \frac{z-z_0}{\zeta-z_0}} = \sum_{n=0}^{\infty}\frac{(z-z_0)^n}{(\zeta-z_0)^{n+1}}$$

（几何级数展开，因为 $\left|\frac{z-z_0}{\zeta-z_0}\right| = \frac{r}{\rho} < 1$。）

代入积分（一致收敛保证可逐项积分）：

$$f(z) = \sum_{n=0}^{\infty}(z-z_0)^n \cdot \frac{1}{2\pi i}\oint_{|\zeta-z_0|=\rho}\frac{f(\zeta)}{(\zeta-z_0)^{n+1}}\,d\zeta = \sum_{n=0}^{\infty}\frac{f^{(n)}(z_0)}{n!}(z-z_0)^n \quad \blacksquare$$

**唯一性**：若 $f(z) = \sum a_n(z-z_0)^n = \sum b_n(z-z_0)^n$，则对 $n=0,1,2,\ldots$：

$$a_n = b_n = \frac{f^{(n)}(z_0)}{n!}$$

### 3.5 常用 Taylor 展开

| 函数 | 展开式 | 收敛域 |
|:---:|:---|:---:|
| $e^z$ | $\sum_{n=0}^{\infty}\frac{z^n}{n!}$ | $\mathbb{C}$ |
| $\sin z$ | $\sum_{n=0}^{\infty}\frac{(-1)^n z^{2n+1}}{(2n+1)!}$ | $\mathbb{C}$ |
| $\cos z$ | $\sum_{n=0}^{\infty}\frac{(-1)^n z^{2n}}{(2n)!}$ | $\mathbb{C}$ |
| $\frac{1}{1-z}$ | $\sum_{n=0}^{\infty}z^n$ | $|z| < 1$ |
| $\ln(1+z)$ | $\sum_{n=1}^{\infty}\frac{(-1)^{n-1}z^n}{n}$ | $|z| < 1$ |
| $(1+z)^\alpha$ | $\sum_{n=0}^{\infty}\binom{\alpha}{n}z^n$ | $|z| < 1$ |

### 3.6 Laurent 级数展开

**定理（Laurent 展开定理）**：设 $f(z)$ 在环形区域 $R_1 < |z - z_0| < R_2$ 内解析，则在该环域内：

$$f(z) = \sum_{n=-\infty}^{\infty} a_n(z-z_0)^n$$

其中系数：

$$a_n = \frac{1}{2\pi i}\oint_C \frac{f(z)}{(z-z_0)^{n+1}}\,dz, \quad n \in \mathbb{Z}$$

$C$ 是环域内绕 $z_0$ 的任意正向简单闭曲线。展开式唯一。

**证明**：设 $R_1 < r_1 < |z - z_0| < r_2 < R_2$。由复合闭路定理和 Cauchy 积分公式：

$$f(z) = \frac{1}{2\pi i}\oint_{|\zeta-z_0|=r_2}\frac{f(\zeta)}{\zeta-z}\,d\zeta - \frac{1}{2\pi i}\oint_{|\zeta-z_0|=r_1}\frac{f(\zeta)}{\zeta-z}\,d\zeta$$

**第一项**（$|\zeta-z_0| = r_2 > |z-z_0|$）：

$$\frac{1}{\zeta-z} = \sum_{n=0}^{\infty}\frac{(z-z_0)^n}{(\zeta-z_0)^{n+1}}$$

逐项积分得正幂部分 $\sum_{n=0}^{\infty} a_n(z-z_0)^n$。

**第二项**（$|\zeta-z_0| = r_1 < |z-z_0|$）：

$$\frac{1}{\zeta-z} = -\frac{1}{z-z_0}\cdot\frac{1}{1-\frac{\zeta-z_0}{z-z_0}} = -\sum_{n=0}^{\infty}\frac{(\zeta-z_0)^n}{(z-z_0)^{n+1}} = -\sum_{m=1}^{\infty}\frac{(z-z_0)^{-m}}{(\zeta-z_0)^{-m+1}}$$

令 $m = n+1$，逐项积分得负幂部分 $\sum_{n=1}^{\infty} a_{-n}(z-z_0)^{-n}$。$\blacksquare$

### 3.7 奇点的分类

设 $z_0$ 是 $f(z)$ 的孤立奇点，$f(z)$ 在 $0 < |z-z_0| < R$ 内的 Laurent 展开为：

$$f(z) = \sum_{n=-\infty}^{\infty} a_n(z-z_0)^n$$

**分类**：

**（1）可去奇点**（Removable singularity）：Laurent 展开中**无负幂项**（$a_{-n} = 0$，$n \geq 1$）。

- 等价条件：$\lim_{z \to z_0} f(z)$ 存在且有限。
- 等价条件：$f(z)$ 在 $z_0$ 附近有界。
- 可通过定义 $f(z_0) = \lim_{z\to z_0}f(z)$ 消除奇点。

**例**：$f(z) = \frac{\sin z}{z} = 1 - \frac{z^2}{6} + \cdots$，$z=0$ 是可去奇点。

**（2）极点**（Pole）：Laurent 展开中只有**有限个**负幂项，最低次为 $-m$（$m \geq 1$），即主部为 $\frac{a_{-m}}{(z-z_0)^m} + \cdots + \frac{a_{-1}}{z-z_0}$。

- $m$ 称为极点的**阶数**。$m = 1$ 时称为**简单极点**。
- 等价条件：$\lim_{z\to z_0}f(z) = \infty$。
- 等价条件：$g(z) = (z-z_0)^m f(z)$ 在 $z_0$ 处解析且 $g(z_0) \neq 0$。

**例**：$f(z) = \frac{1}{z^2(z-1)}$，$z=0$ 是二阶极点，$z=1$ 是一阶极点。

**（3）本性奇点**（Essential singularity）：Laurent 展开中有**无穷多个**负幂项。

- 等价条件：$\lim_{z\to z_0}f(z)$ 不存在（也不为 $\infty$）。

**Picard 定理（大定理）**：若 $z_0$ 是 $f(z)$ 的本性奇点，则 $f(z)$ 在 $z_0$ 的任意邻域内取到 $\mathbb{C}$ 中的所有值（至多一个例外）。

**Picard 定理（小定理）**：若 $z_0$ 是 $f(z)$ 的本性奇点，则 $\lim_{z\to z_0}f(z)$ 不存在。

**例**：$f(z) = e^{1/z} = \sum_{n=0}^{\infty}\frac{1}{n!z^n}$，$z=0$ 是本性奇点。沿正实轴 $z\to 0^+$，$e^{1/z} \to \infty$；沿负实轴 $z\to 0^-$，$e^{1/z} \to 0$；沿虚轴 $z = it \to 0$，$e^{1/z} = e^{-i/t}$ 在单位圆上振荡。

### 3.8 无穷远点处的奇点

设 $f(z)$ 在 $|z| > R$ 内解析。令 $w = \frac{1}{z}$，$g(w) = f\left(\frac{1}{w}\right)$。

- 若 $w=0$ 是 $g(w)$ 的可去奇点，则 $\infty$ 是 $f(z)$ 的可去奇点。
- 若 $w=0$ 是 $g(w)$ 的 $m$ 阶极点，则 $\infty$ 是 $f(z)$ 的 $m$ 阶极点。
- 若 $w=0$ 是 $g(w)$ 的本性奇点，则 $\infty$ 是 $f(z)$ 的本性奇点。

**例**：$f(z) = e^z = e^{1/w} = g(w)$，$w=0$ 是 $g$ 的本性奇点，故 $\infty$ 是 $e^z$ 的本性奇点。

### 3.9 整函数与亚纯函数

**整函数**（Entire function）：在全平面解析的函数。如 $e^z$，$\sin z$，多项式等。

- 有穷整函数只有可去奇点（$\infty$ 处），故为常数（Liouville 定理的推广）。
- 多项式在 $\infty$ 处有极点，$e^z$ 在 $\infty$ 处有本性奇点。

**亚纯函数**（Meromorphic function）：在区域 $D$ 内除极点外处处解析的函数。如 $\frac{1}{z}$，$\tan z$，有理函数等。
