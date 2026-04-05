# 第四章 复积分与 Cauchy 积分定理

## 一、几何意义

### 1.1 复积分的几何解释

复积分 $\int_C f(z)\,dz$ 沿曲线 $C$ 进行。设 $f(z) = u + iv$，$dz = dx + i\,dy$，则：

$$\int_C f(z)\,dz = \int_C (u\,dx - v\,dy) + i\int_C (v\,dx + u\,dy)$$

这可以理解为**二维向量场的曲线积分的复数形式**：
- 实部是向量场 $(u, -v)$ 沿 $C$ 的（第二类）曲线积分。
- 虚部是向量场 $(v, u)$ 沿 $C$ 的（第二类）曲线积分。

如果将 $f$ 看作平面上的向量场 $(u, v)$，则：
$$\int_C f(z)\,dz = \int_C \mathbf{F} \cdot d\mathbf{r} + i\int_C \mathbf{F} \times d\mathbf{r}$$

其中 $\mathbf{F} = (u, v)$，"curl" 形式给出了虚部。

### 1.2 积分与路径无关

当 $f(z)$ 在单连通区域 $D$ 内解析时，$\int_C f(z)\,dz$ 的值仅取决于起点和终点，与路径 $C$ 的选择无关。这类似于保守力场中功与路径无关。

几何直观：在解析函数的定义域中，复积分沿任何两条从 $z_0$ 到 $z_1$ 的路径之差等于沿闭合回路的积分，而 Cauchy 定理保证这个闭合积分为零。

### 1.3 复合闭路定理的几何意义

若 $f(z)$ 在区域 $D$ 内解析，$D$ 内有 $n$ 个洞（奇点），$C_0$ 是包含所有奇点的外边界，$C_1, C_2, \ldots, C_n$ 是绕各奇点的内边界（均正向），则：

$$\oint_{C_0} f(z)\,dz = \sum_{k=1}^{n}\oint_{C_k} f(z)\,dz$$

几何意义：外边界的积分等于所有内边界积分之和。这类似于实分析中的多连通区域的 Green 公式。

### 1.4 Cauchy 定理的拓扑意义

Cauchy 积分定理本质上是一个**拓扑不变量**。它表明，在解析函数的值域中，绕"洞"（奇点）的积分是一个不变量。这正是留数理论和同调群的理论基础。

---

## 二、应用场景

### 2.1 复势与环量

在二维流体力学中，若 $w(z) = \phi + i\psi$ 为复势，则沿闭合曲线 $C$ 的速度环量为：

$$\Gamma = \operatorname{Re}\oint_C f'(z)\,dz$$

其中 $f'(z)$ 是复速度。Cauchy 定理表明，在无旋流体中，绕不包含奇点的闭合曲线的环量为零。

### 2.2 弹性力学与应力积分

二维弹性力学中，应力和位移可以用复变函数表示。沿边界的积分给出合力和合力矩。

### 2.3 物理学中的闭合路径积分

在量子力学中，Feynman 路径积分可以看作复积分的推广。闭合路径上的复积分在统计物理（配分函数的计算）和量子场论（圈积分）中广泛应用。

### 2.4 数值计算

Cauchy 积分公式可以用于数值计算解析函数的导数值和函数值（Cauchy 积分方法），这在某些情况下比差分方法更精确。

---

## 三、数学理论（及推导）

### 3.1 复积分的定义

**定义**：设 $C$ 是复平面上从 $z_0$ 到 $z_1$ 的有向光滑曲线（或分段光滑曲线），$f(z)$ 在 $C$ 上有定义。

将 $C$ 用分点 $z_0, z_1, \ldots, z_n$ 分成 $n$ 小段，在每小段上任取一点 $\zeta_k$，作 Riemann 和：

$$S_n = \sum_{k=1}^{n} f(\zeta_k)(z_k - z_{k-1})$$

若 $\max|z_k - z_{k-1}| \to 0$ 时，$S_n$ 的极限存在且与分割方式及 $\zeta_k$ 的选取无关，则称此极限为 $f(z)$ 沿 $C$ 的**复积分**，记为：

$$\int_C f(z)\,dz$$

### 3.2 复积分的计算方法

**参数化法**：设曲线 $C$ 的参数方程为 $z = z(t) = x(t) + iy(t)$，$t \in [a, b]$，则：

$$\int_C f(z)\,dz = \int_a^b f(z(t))\,z'(t)\,dt$$

**实部虚部分解法**：

$$\int_C f(z)\,dz = \int_C (u\,dx - v\,dy) + i\int_C (v\,dx + u\,dy)$$

**例**：计算 $\int_C z^2\,dz$，其中 $C$ 是从 $0$ 到 $1+i$ 的直线段。

参数化：$z = t(1+i)$，$t \in [0,1]$，$dz = (1+i)\,dt$。

$$\int_C z^2\,dz = \int_0^1 t^2(1+i)^2 \cdot (1+i)\,dt = (1+i)^3 \int_0^1 t^2\,dt = \frac{(1+i)^3}{3} = \frac{-2+2i}{3}$$

### 3.3 复积分的基本性质

1. **线性性**：$\int_C [af(z) + bg(z)]\,dz = a\int_C f(z)\,dz + b\int_C g(z)\,dz$

2. **方向性**：$\int_{C^-} f(z)\,dz = -\int_C f(z)\,dz$（$C^-$ 为 $C$ 的反向曲线）

3. **路径可加性**：若 $C = C_1 + C_2$，则 $\int_C f(z)\,dz = \int_{C_1} f(z)\,dz + \int_{C_2} f(z)\,dz$

4. **估值不等式**：$\left|\int_C f(z)\,dz\right| \leq \int_C |f(z)|\,|dz| \leq ML$

   其中 $M = \max_{z \in C}|f(z)|$，$L$ 为 $C$ 的弧长。

**推导估值不等式**：

$$\left|\sum_{k=1}^{n} f(\zeta_k)(z_k - z_{k-1})\right| \leq \sum_{k=1}^{n} |f(\zeta_k)||z_k - z_{k-1}| \leq M\sum_{k=1}^{n}|z_k - z_{k-1}|$$

取极限即得。

### 3.4 Cauchy-Goursat 定理

**定理（Cauchy-Goursat）**：若 $f(z)$ 在单连通区域 $D$ 内解析，$C$ 是 $D$ 内任意一条简单闭曲线（或分段光滑的闭曲线），则：

$$\oint_C f(z)\,dz = 0$$

**证明思路**（Goursat 的证明）：

**第一步**：设 $C$ 为三角形 $\Delta$。需要证明 $\oint_\Delta f(z)\,dz = 0$。

用反证法。设 $I = \oint_\Delta f(z)\,dz \neq 0$。将 $\Delta$ 四等分为四个小三角形 $\Delta_1, \Delta_2, \Delta_3, \Delta_4$，则：

$$|I| = \left|\sum_{k=1}^4 \oint_{\Delta_k} f(z)\,dz\right| \leq \sum_{k=1}^4 \left|\oint_{\Delta_k} f(z)\,dz\right|$$

故至少存在一个小三角形（记为 $\Delta^{(1)}$）满足 $\left|\oint_{\Delta^{(1)}} f(z)\,dz\right| \geq \frac{|I|}{4}$。

**第二步**：反复四等分，得到三角形序列 $\Delta^{(n)}$，满足：

$$\left|\oint_{\Delta^{(n)}} f(z)\,dz\right| \geq \frac{|I|}{4^n}$$

且 $\Delta^{(n)}$ 的直径为 $\frac{d}{2^n}$（$d$ 为 $\Delta$ 的直径）。

**第三步**：由闭集套定理（Cantor 交集定理），$\Delta^{(n)}$ 交于唯一一点 $z_0 \in \Delta$。

**第四步**：由于 $f(z)$ 在 $z_0$ 处可导，$f(z) = f(z_0) + f'(z_0)(z-z_0) + \varepsilon(z)(z-z_0)$，其中 $|\varepsilon(z)| \to 0$（当 $z \to z_0$）。

$$\oint_{\Delta^{(n)}} f(z)\,dz = \oint_{\Delta^{(n)}} [f(z_0) + f'(z_0)(z-z_0)]\,dz + \oint_{\Delta^{(n)}} \varepsilon(z)(z-z_0)\,dz$$

前两项积分恒为零（常数的积分和 $(z-z_0)$ 沿闭路的积分为零）。故：

$$\left|\oint_{\Delta^{(n)}} f(z)\,dz\right| = \left|\oint_{\Delta^{(n)}} \varepsilon(z)(z-z_0)\,dz\right| \leq \max_{z \in \Delta^{(n)}}|\varepsilon(z)| \cdot \frac{L}{2^n} \cdot \frac{d}{2^n}$$

其中 $L$ 为 $\Delta$ 的周长。当 $n \to \infty$ 时，$\max|\varepsilon(z)| \to 0$，右边趋于 $0$。但左边 $\geq |I|/4^n$，这要求 $|I| = 0$，矛盾。

**第五步**：由三角形的 Cauchy 定理推广到一般闭曲线。将闭曲线围成的区域用三角网格剖分，内部三角形的积分两两抵消，边界积分之和即为闭合曲线的积分。

### 3.5 积分与路径无关的条件

**定理**：设 $f(z)$ 在单连通区域 $D$ 内连续。以下三个条件等价：

1. $f(z)$ 在 $D$ 内解析。
2. $\oint_C f(z)\,dz = 0$ 对 $D$ 内任意闭曲线 $C$ 成立。
3. $\int_C f(z)\,dz$ 在 $D$ 内与路径无关。

**原函数**：条件 (3) 成立时，可定义**原函数**：

$$F(z) = \int_{z_0}^z f(\zeta)\,d\zeta$$

$F(z)$ 在 $D$ 内解析，且 $F'(z) = f(z)$。

**证明 $F'(z) = f(z)$**：

$$\frac{F(z+\Delta z) - F(z)}{\Delta z} = \frac{1}{\Delta z}\int_z^{z+\Delta z} f(\zeta)\,d\zeta$$

取从 $z$ 到 $z+\Delta z$ 的直线路径，参数化 $\zeta = z + t\Delta z$，$t \in [0,1]$：

$$= \int_0^1 f(z + t\Delta z)\,dt$$

当 $\Delta z \to 0$ 时，$f(z + t\Delta z) \to f(z)$（$f$ 连续），故上式 $\to \int_0^1 f(z)\,dt = f(z)$。

### 3.6 Newton-Leibniz 公式

**定理**：若 $F(z)$ 是 $f(z)$ 在区域 $D$ 内的原函数（即 $F'(z) = f(z)$），$C$ 是 $D$ 内从 $z_0$ 到 $z_1$ 的分段光滑曲线，则：

$$\int_C f(z)\,dz = F(z_1) - F(z_0)$$

**证明**：设 $z = z(t)$，$t \in [a, b]$，则：

$$\int_C f(z)\,dz = \int_a^b f(z(t))\,z'(t)\,dt = \int_a^b F'(z(t))\,z'(t)\,dt = \int_a^b \frac{d}{dt}[F(z(t))]\,dt = F(z(b)) - F(z(a)) = F(z_1) - F(z_0)$$

### 3.7 复合闭路定理

**定理**：设 $D$ 是多连通区域（含 $n$ 个"洞"），$f(z)$ 在 $D$ 及其边界上解析。设 $C_0$ 为外边界（逆时针），$C_1, C_2, \ldots, C_n$ 为内边界（顺时针方向各绕一个洞），则：

$$\oint_{C_0} f(z)\,dz = \sum_{k=1}^{n}\oint_{C_k} f(z)\,dz$$

或写成统一方向（均取正向，即左侧为区域内部）：

$$\oint_{C_0} f(z)\,dz + \sum_{k=1}^{n}\oint_{C_k} f(z)\,dz = 0$$

**证明思路**：用"割线法"将多连通区域化为单连通区域。在 $C_0$ 和每个 $C_k$ 之间各作一条割线，然后对得到的单连通区域应用 Cauchy-Goursat 定理。割线上正反方向的积分相互抵消，只剩下各边界曲线上的积分。

### 3.8 Cauchy 积分定理的推广

**Morera 定理**（Cauchy 定理的逆定理）：

若 $f(z)$ 在区域 $D$ 内连续，且对 $D$ 内任意三角形的边界 $\Delta$ 有 $\oint_\Delta f(z)\,dz = 0$，则 $f(z)$ 在 $D$ 内解析。

**意义**：Cauchy 定理的逆定理为判断函数的解析性提供了一个积分判据。
