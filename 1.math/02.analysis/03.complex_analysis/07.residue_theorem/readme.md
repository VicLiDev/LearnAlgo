# 第七章 留数定理及其应用

## 一、几何意义

### 1.1 留数的几何解释

设 $z_0$ 是 $f(z)$ 的孤立奇点，$f(z)$ 在 $z_0$ 附近的 Laurent 展开为：

$$f(z) = \sum_{n=-\infty}^{\infty} a_n(z-z_0)^n$$

**留数**（Residue）定义为 $\operatorname{Res}(f, z_0) = a_{-1}$，即 $(z-z_0)^{-1}$ 项的系数。

**几何意义**：

$$\oint_{|z-z_0|=\rho} f(z)\,dz = 2\pi i \cdot a_{-1} = 2\pi i \cdot \operatorname{Res}(f, z_0)$$

留数度量了 $f(z)$ 绕 $z_0$ 一圈的"净旋转量"。如果将 $f(z)\,dz$ 理解为微分形式，留数就是该形式在奇点周围的**积分不变量**。

直观类比：类似于流体力学中"漩涡"的强度——绕漩涡的环量正比于留数。

### 1.2 留数定理的几何意义

若 $f(z)$ 在简单闭曲线 $C$ 内有有限个孤立奇点 $z_1, z_2, \ldots, z_n$，则：

$$\oint_C f(z)\,dz = 2\pi i \sum_{k=1}^{n}\operatorname{Res}(f, z_k)$$

几何意义：沿外边界的积分等于所有内部奇点处的"漩涡强度"之和。这是复合闭路定理的具体化——每个奇点像一个"源"或"汇"，贡献了与其留数成正比的积分值。

### 1.3 辐角原理的几何意义

**辐角原理**：若 $f(z)$ 在简单闭曲线 $C$ 上及其内部解析（除有限个极点），$f(z)$ 在 $C$ 上不为零，则：

$$\frac{1}{2\pi i}\oint_C \frac{f'(z)}{f(z)}\,dz = N - P$$

其中 $N$ 是 $f$ 在 $C$ 内的零点个数，$P$ 是极点个数（均计重数）。

几何意义：当 $z$ 沿 $C$ 绕行一周时，$w = f(z)$ 在 $w$ 平面上描出的曲线绕原点的圈数等于 $N - P$。这是因为：

$$\oint_C \frac{f'(z)}{f(z)}\,dz = \oint_C d(\ln f(z)) = [\ln|f(z)| + i\arg f(z)]_{\text{绕一周}}$$

$|f(z)|$ 回到原值（实部贡献为零），而 $\arg f(z)$ 的变化就是绕原点的圈数。

### 1.4 Rouché 定理的几何意义

若在 $C$ 上 $|f(z) - g(z)| < |f(z)|$，则 $f$ 和 $g$ 在 $C$ 内有相同个数的零点（计重数）。

几何意义：如果 $g$ 对 $f$ 的"扰动"足够小（始终小于 $f$ 本身在边界上的模），则 $f$ 和 $g$ 的零点个数不变。这在工程中对应于**鲁棒性**（robustness）的概念——小扰动不改变系统的基本性质。

---

## 二、应用场景

### 2.1 计算实积分

留数定理最经典的应用是计算各种困难的实积分：

1. **有理函数积分**：$\int_{-\infty}^{+\infty} \frac{P(x)}{Q(x)}\,dx$（$\deg Q \geq \deg P + 2$）
2. **含三角函数的积分**：$\int_0^{2\pi} R(\cos\theta, \sin\theta)\,d\theta$
3. **含指数函数的积分**：$\int_{-\infty}^{+\infty} f(x)e^{iax}\,dx$（$a > 0$）
4. **Fresnel 积分**：$\int_0^{\infty}\cos(x^2)\,dx = \int_0^{\infty}\sin(x^2)\,dx = \frac{\sqrt{2\pi}}{4}$

### 2.2 反常积分与级数求和

留数定理可以用于求某些级数的和，如：

$$\sum_{n=-\infty}^{+\infty} \frac{1}{n^2 + a^2} = \frac{\pi}{a}\coth(\pi a)$$

### 2.3 零点与极点计数

辐角原理和 Rouché 定理广泛用于：
- 证明方程根的个数和位置。
- 控制理论中判断闭环系统的稳定性（Nyquist 判据的数学基础）。
- 代数几何中曲线的亏格计算。

### 2.4 物理学中的应用

在量子场论中，Feynman 积分通过留数定理计算；在流体力学中，点涡的环量与留数直接相关。

---

## 三、数学理论（及推导）

### 3.1 留数的定义

**定义**：设 $z_0$ 是 $f(z)$ 的孤立奇点，$f(z)$ 在 $0 < |z - z_0| < R$ 内的 Laurent 展开为：

$$f(z) = \cdots + \frac{a_{-2}}{(z-z_0)^2} + \frac{a_{-1}}{z-z_0} + a_0 + a_1(z-z_0) + \cdots$$

则 $\operatorname{Res}(f, z_0) = a_{-1}$。

由 Cauchy 积分公式（取 $n=0$ 的形式）：

$$\operatorname{Res}(f, z_0) = a_{-1} = \frac{1}{2\pi i}\oint_{|z-z_0|=\rho} f(z)\,dz \quad (0 < \rho < R)$$

### 3.2 极点处留数的计算公式

**（1）$z_0$ 为 $m$ 阶极点**：

$$\operatorname{Res}(f, z_0) = \frac{1}{(m-1)!}\lim_{z \to z_0}\frac{d^{m-1}}{dz^{m-1}}\left[(z-z_0)^m f(z)\right]$$

**推导**：设 $f(z) = \frac{g(z)}{(z-z_0)^m}$，其中 $g(z)$ 在 $z_0$ 处解析，$g(z_0) \neq 0$。

$$g(z) = \sum_{n=0}^{\infty}\frac{g^{(n)}(z_0)}{n!}(z-z_0)^n$$

$$f(z) = \sum_{n=0}^{\infty}\frac{g^{(n)}(z_0)}{n!}(z-z_0)^{n-m}$$

$a_{-1}$ 对应 $n - m = -1$ 即 $n = m - 1$ 的项：

$$a_{-1} = \frac{g^{(m-1)}(z_0)}{(m-1)!}$$

而 $g(z) = (z-z_0)^m f(z)$，故：

$$\operatorname{Res}(f, z_0) = \frac{1}{(m-1)!}\lim_{z\to z_0}\frac{d^{m-1}}{dz^{m-1}}[(z-z_0)^m f(z)]$$

**（2）简单极点（$m=1$）的简便公式**：

$$\operatorname{Res}(f, z_0) = \lim_{z\to z_0}(z-z_0)f(z)$$

**（3）$f(z) = \frac{P(z)}{Q(z)}$ 型简单极点**：若 $P(z_0) \neq 0$，$Q(z_0) = 0$，$Q'(z_0) \neq 0$，则：

$$\operatorname{Res}(f, z_0) = \frac{P(z_0)}{Q'(z_0)}$$

**推导**：$\operatorname{Res}(f, z_0) = \lim_{z\to z_0}(z-z_0)\frac{P(z)}{Q(z)} = P(z_0)\lim_{z\to z_0}\frac{z-z_0}{Q(z)} = P(z_0)\cdot\frac{1}{Q'(z_0)}$

（利用 L'Hôpital 法则：$\lim_{z\to z_0}\frac{z-z_0}{Q(z)} = \lim_{z\to z_0}\frac{1}{Q'(z)} = \frac{1}{Q'(z_0)}$。）

### 3.3 留数定理

**定理**：设 $f(z)$ 在简单闭曲线 $C$ 上解析，在 $C$ 内除有限个孤立奇点 $z_1, z_2, \ldots, z_n$ 外解析，则：

$$\oint_C f(z)\,dz = 2\pi i\sum_{k=1}^{n}\operatorname{Res}(f, z_k)$$

**证明**：对每个奇点 $z_k$，作小圆 $C_k$（半径 $\rho_k$，使各圆互不相交且在 $C$ 内）。由复合闭路定理：

$$\oint_C f(z)\,dz = \sum_{k=1}^{n}\oint_{C_k} f(z)\,dz = \sum_{k=1}^{n} 2\pi i \cdot \operatorname{Res}(f, z_k) = 2\pi i\sum_{k=1}^{n}\operatorname{Res}(f, z_k) \quad \blacksquare$$

### 3.4 无穷远点的留数

$$\operatorname{Res}(f, \infty) = \frac{1}{2\pi i}\oint_{C^-} f(z)\,dz = -\frac{1}{2\pi i}\oint_C f(z)\,dz$$

其中 $C$ 是足够大的正向圆（使所有有限远奇点在内部），$C^-$ 为反向。

**定理**：若 $f(z)$ 在扩充复平面上只有有限个奇点 $z_1, \ldots, z_n$ 和 $\infty$，则：

$$\operatorname{Res}(f, \infty) + \sum_{k=1}^{n}\operatorname{Res}(f, z_k) = 0$$

**证明**：$\oint_C f(z)\,dz = 2\pi i\sum_{k=1}^{n}\operatorname{Res}(f, z_k) = -2\pi i\operatorname{Res}(f, \infty)$。$\blacksquare$

### 3.5 利用留数计算实积分

**类型一：有理函数的无穷积分**

$$I = \int_{-\infty}^{+\infty}\frac{P(x)}{Q(x)}\,dx$$

条件：$Q(x)$ 无实零点，$\deg Q \geq \deg P + 2$。

**方法**：取上半圆周 $C_R$（半径 $R$），$f(z) = \frac{P(z)}{Q(z)}$。

$$\oint_{C_R + [-R, R]} f(z)\,dz = 2\pi i\sum_{\operatorname{Im}z_k > 0}\operatorname{Res}(f, z_k)$$

当 $R \to \infty$ 时，$C_R$ 上的积分 $\to 0$（因为 $|zf(z)| \sim |z|^{-1} \to 0$），故：

$$I = 2\pi i\sum_{\operatorname{Im}z_k > 0}\operatorname{Res}(f, z_k)$$

**例**：计算 $I = \int_{-\infty}^{+\infty}\frac{dx}{1+x^2}$。

$f(z) = \frac{1}{1+z^2} = \frac{1}{(z+i)(z-i)}$，上半平面有一阶极点 $z = i$。

$$\operatorname{Res}(f, i) = \frac{1}{2i}$$

$$I = 2\pi i \cdot \frac{1}{2i} = \pi$$

**类型二：含三角函数的积分**

$$I = \int_0^{2\pi} R(\cos\theta, \sin\theta)\,d\theta$$

**方法**：令 $z = e^{i\theta}$，则 $\cos\theta = \frac{z+z^{-1}}{2}$，$\sin\theta = \frac{z-z^{-1}}{2i}$，$d\theta = \frac{dz}{iz}$。

积分化为单位圆 $|z|=1$ 上的复积分。

**例**：计算 $I = \int_0^{2\pi}\frac{d\theta}{a+\cos\theta}$（$a > 1$）。

令 $z = e^{i\theta}$：

$$I = \oint_{|z|=1}\frac{1}{a + \frac{z+z^{-1}}{2}}\cdot\frac{dz}{iz} = \oint_{|z|=1}\frac{2\,dz}{i(z^2 + 2az + 1)}$$

$z^2 + 2az + 1 = 0$ 的根为 $z = -a \pm \sqrt{a^2-1}$。由于 $a > 1$，两根均为负实数。单位圆内的根为 $z_0 = -a + \sqrt{a^2-1}$（$|z_0| = a - \sqrt{a^2-1} = \frac{1}{a+\sqrt{a^2-1}} < 1$）。

$$\operatorname{Res}\left(\frac{2}{i(z-z_0)(z-z_1)}, z_0\right) = \frac{2}{i(z_0-z_1)} = \frac{2}{i \cdot 2\sqrt{a^2-1}} = \frac{1}{i\sqrt{a^2-1}}$$

$$I = 2\pi i \cdot \frac{1}{i\sqrt{a^2-1}} = \frac{2\pi}{\sqrt{a^2-1}}$$

**类型三：含指数函数的积分（Jordan 引理的应用）**

$$I = \int_{-\infty}^{+\infty} f(x)e^{iax}\,dx \quad (a > 0)$$

**Jordan 引理**：若 $f(z)$ 在上半平面解析（除有限个极点），且 $\lim_{z\to\infty}f(z) = 0$（$\operatorname{Im}z \geq 0$），则：

$$\lim_{R\to\infty}\int_{C_R} f(z)e^{iaz}\,dz = 0$$

其中 $C_R$ 为上半圆 $|z|=R$，$\operatorname{Im}z \geq 0$。

**Jordan 引理的证明要点**：在 $C_R$ 上，$z = Re^{i\theta}$，$\theta \in [0, \pi]$：

$$|e^{iaz}| = |e^{iaR(\cos\theta+i\sin\theta)}| = e^{-aR\sin\theta}$$

$$\left|\int_{C_R} f(z)e^{iaz}\,dz\right| \leq \max_{C_R}|f(z)| \int_0^{\pi} e^{-aR\sin\theta}\,R\,d\theta$$

利用 $\sin\theta \geq \frac{2}{\pi}\theta$（$\theta \in [0, \pi/2]$）和对称性：

$$\int_0^{\pi} e^{-aR\sin\theta}\,d\theta \leq 2\int_0^{\pi/2} e^{-aR\cdot\frac{2\theta}{\pi}}\,d\theta = \frac{\pi}{aR}(1-e^{-aR}) \to \frac{\pi}{aR}$$

故积分 $\leq \max|f| \cdot \pi/a \to 0$。

### 3.6 辐角原理

**定理（辐角原理）**：设 $f(z)$ 在简单闭曲线 $C$ 上及其内部解析，除内部有限个极点外。$f(z)$ 在 $C$ 上不为零。设 $N$ 为 $C$ 内零点个数（计重数），$P$ 为极点个数（计重数），则：

$$\frac{1}{2\pi i}\oint_C \frac{f'(z)}{f(z)}\,dz = N - P$$

**证明**：设 $f(z)$ 在 $C$ 内有零点 $a_1, \ldots, a_N$（阶数分别为 $n_1, \ldots, n_N$），极点 $b_1, \ldots, b_P$（阶数分别为 $p_1, \ldots, p_P$）。

在 $C$ 内：

$$\frac{f'(z)}{f(z)} = \sum_{j=1}^{N}\frac{n_j}{z-a_j} - \sum_{k=1}^{P}\frac{p_k}{z-b_k} + h(z)$$

其中 $h(z)$ 在 $C$ 内解析。由留数定理：

$$\frac{1}{2\pi i}\oint_C \frac{f'(z)}{f(z)}\,dz = \sum_{j=1}^{N} n_j - \sum_{k=1}^{P} p_k = N - P \quad \blacksquare$$

### 3.7 Rouché 定理

**定理（Rouché）**：设 $f(z)$ 和 $g(z)$ 在简单闭曲线 $C$ 上及其内部解析，且在 $C$ 上满足 $|f(z) - g(z)| < |f(z)|$，则 $f(z)$ 和 $g(z)$ 在 $C$ 内的零点个数相同（计重数）。

**证明**：令 $h(z) = \frac{g(z)}{f(z)}$，则 $h(z)$ 在 $C$ 上及其内部解析（$f$ 在 $C$ 上不为零，且 $|f-g|<|f|$ 保证 $g$ 在 $C$ 上也不为零）。

在 $C$ 上：$|h(z) - 1| = \frac{|g(z)-f(z)|}{|f(z)|} < 1$。

因此 $h(C)$ 在以 $1$ 为心、半径为 $1$ 的圆盘内，不经过原点。由辐角原理：

$$N_g - 0 = \frac{1}{2\pi i}\oint_C \frac{g'(z)}{g(z)}\,dz = \frac{1}{2\pi i}\oint_C \frac{h'(z)}{h(z)}\,dz + \frac{1}{2\pi i}\oint_C \frac{f'(z)}{f(z)}\,dz$$

第二项 $= N_f$。第一项：由于 $h(C)$ 不绕原点，$\oint_C \frac{h'}{h}\,dz = 0$。

故 $N_g = N_f$。$\blacksquare$

**例（代数基本定理的另一个证明）**：设 $P(z) = z^n + a_{n-1}z^{n-1} + \cdots + a_0$，$n \geq 1$。

取 $f(z) = z^n$，$g(z) = P(z)$，$C$ 为 $|z| = R$。

在 $C$ 上：$|g(z) - f(z)| = |a_{n-1}z^{n-1}+\cdots+a_0| \leq |a_{n-1}|R^{n-1}+\cdots+|a_0|$

$|f(z)| = R^n$

取 $R$ 足够大使 $|g-f| < |f| = R^n$，则 $P(z)$ 在 $|z| < R$ 内有 $n$ 个零点。
