# 第一章 复数与复变函数

## 一、几何意义

### 1.1 复平面表示

复数 $z = x + iy$ 可以用二维平面上的点 $(x, y)$ 来表示，其中 $x$ 轴为**实轴**（Real axis），$y$ 轴为**虚轴**（Imaginary axis）。这样的平面称为**复平面**（Complex plane）或 Argand 平面。

- **模**：$|z| = \sqrt{x^2 + y^2}$，表示点 $(x,y)$ 到原点的欧几里得距离。
- **辐角**：$\arg z = \arctan\frac{y}{x}$，表示向量 $z$ 与正实轴之间的夹角，多值函数。
- **主值辐角**：$\operatorname{Arg} z \in (-\pi, \pi]$。

复数的极坐标形式为：
$$z = |z|(\cos\theta + i\sin\theta) = |z|e^{i\theta}$$

其中 $\theta = \arg z$。

### 1.2 复球面表示（Riemann 球面）

通过**球极射影**（Stereographic projection），可以将复平面与单位球面建立一一对应关系。

设球面 $S^2$ 的方程为 $X^2 + Y^2 + Z^2 = 1$，北极点 $N = (0, 0, 1)$。对于复平面上的点 $z = x + iy$，从 $N$ 向 $(x, y, 0)$ 作射线，与球面的交点 $(X, Y, Z)$ 为：

$$X = \frac{2\operatorname{Re}z}{|z|^2 + 1}, \quad Y = \frac{2\operatorname{Im}z}{|z|^2 + 1}, \quad Z = \frac{|z|^2 - 1}{|z|^2 + 1}$$

- 北极 $N$ 对应**无穷远点** $\infty$。
- 扩充复平面 $\hat{\mathbb{C}} = \mathbb{C} \cup \{\infty\}$ 与整个球面一一对应，称为 **Riemann 球面**。
- 在球面上，**赤道**对应单位圆 $|z| = 1$；北半球对应单位圆外部 $|z| > 1$；南半球对应单位圆内部 $|z| < 1$。

**几何直观**：复球面上的距离度量使得无穷远点与有限远点处于对称地位，这种紧致化在讨论函数在无穷远的行为时极为重要。

### 1.3 复数运算的几何意义

- **加法**：复数加法满足**平行四边形法则**。若 $z_1 = x_1 + iy_1$，$z_2 = x_2 + iy_2$，则 $z_1 + z_2$ 对应平行四边形的对角线顶点。
- **乘法**：$z_1 z_2 = |z_1||z_2| e^{i(\arg z_1 + \arg z_2)}$，即模相乘、辐角相加。
- **除法**：$\frac{z_1}{z_2} = \frac{|z_1|}{|z_2|} e^{i(\arg z_1 - \arg z_2)}$，即模相除、辐角相减。
- **共轭**：$\bar{z} = x - iy$，关于实轴的**轴对称**反射。
- **取负**：$-z = -x - iy$，关于原点的**中心对称**。

### 1.4 复变函数映射的几何意义

复变函数 $w = f(z)$ 可以看作从 $z$ 平面到 $w$ 平面的映射。对于区域 $D \subseteq \mathbb{C}$：

- 函数将 $z$ 平面上的**点集**映射为 $w$ 平面上的**点集**。
- 例如 $w = z^2$ 将角度 $\theta$ 的射线映射为角度 $2\theta$ 的射线（角度加倍），将模 $r$ 映射为 $r^2$。

---

## 二、应用场景

### 2.1 电路分析（交流电路）

在交流电路中，电压和电流用复数表示（相量法）：

$$V = V_0 e^{i(\omega t + \phi)}, \quad I = I_0 e^{i(\omega t + \psi)}$$

阻抗 $Z = R + iX$（$R$ 为电阻，$X$ 为电抗），利用复数运算可以极大简化交流电路的分析。

### 2.2 量子力学

量子力学中，波函数 $\Psi(x, t)$ 是复值函数。粒子的状态用复 Hilbert 空间中的向量描述，物理可观测量对应 Hermite 算子。复数框架是量子力学的基本数学语言。

### 2.3 信号处理

复指数信号 $e^{i\omega t} = \cos\omega t + i\sin\omega t$ 是 Fourier 分析的基石。复数形式的频域表示使得滤波、调制、解调等操作的数学描述更加简洁统一。

### 2.4 流体力学

二维不可压缩无旋流体的速度场可以用**复势函数**描述。若 $w(z) = \phi(x,y) + i\psi(x,y)$ 为解析函数，则 $\phi$ 为速度势，$\psi$ 为流函数。

### 2.5 控制理论

控制系统的传递函数 $G(s)$ 是复变量 $s = \sigma + i\omega$ 的函数。通过分析 $G(s)$ 在复平面上的性质（如 Nyquist 图、Bode 图），可以判断系统的稳定性。

---

## 三、数学理论（及推导）

### 3.1 复数的代数定义

**定义**：形如 $z = x + iy$ 的数称为复数，其中 $x, y \in \mathbb{R}$，$i$ 满足 $i^2 = -1$。

- $x = \operatorname{Re}z$（实部），$y = \operatorname{Im}z$（虚部）。
- 全体复数构成域 $\mathbb{C}$。

### 3.2 复数的运算

**四则运算**：设 $z_1 = x_1 + iy_1$，$z_2 = x_2 + iy_2$：

$$z_1 \pm z_2 = (x_1 \pm x_2) + i(y_1 \pm y_2)$$

$$z_1 \cdot z_2 = (x_1 x_2 - y_1 y_2) + i(x_1 y_2 + x_2 y_1)$$

$$\frac{z_1}{z_2} = \frac{z_1 \bar{z}_2}{|z_2|^2} = \frac{x_1 x_2 + y_1 y_2}{x_2^2 + y_2^2} + i\frac{x_2 y_1 - x_1 y_2}{x_2^2 + y_2^2} \quad (z_2 \neq 0)$$

**De Moivre 公式**：
$$(\cos\theta + i\sin\theta)^n = \cos(n\theta) + i\sin(n\theta)$$

**推导**：由 Euler 公式 $e^{i\theta} = \cos\theta + i\sin\theta$，
$$(e^{i\theta})^n = e^{in\theta} \implies (\cos\theta + i\sin\theta)^n = \cos(n\theta) + i\sin(n\theta)$$

### 3.3 共轭与模

**共轭复数**：$\bar{z} = x - iy$，满足以下性质：

$$\overline{z_1 + z_2} = \bar{z}_1 + \bar{z}_2, \quad \overline{z_1 z_2} = \bar{z}_1 \bar{z}_2$$

$$z\bar{z} = |z|^2, \quad \bar{\bar{z}} = z, \quad \overline{(z_1/z_2)} = \bar{z}_1 / \bar{z}_2$$

**模的性质**：

$$|z_1 z_2| = |z_1| \cdot |z_2|, \quad |z_1/z_2| = |z_1|/|z_2|$$

**三角不等式**：
$$||z_1| - |z_2|| \leq |z_1 + z_2| \leq |z_1| + |z_2|$$

**证明三角不等式**：

$$|z_1 + z_2|^2 = (z_1 + z_2)\overline{(z_1 + z_2)} = |z_1|^2 + z_1\bar{z}_2 + \bar{z}_1 z_2 + |z_2|^2$$

$$= |z_1|^2 + 2\operatorname{Re}(z_1\bar{z}_2) + |z_2|^2$$

由 $|\operatorname{Re}(z_1\bar{z}_2)| \leq |z_1\bar{z}_2| = |z_1||z_2|$，得：

$$|z_1 + z_2|^2 \leq |z_1|^2 + 2|z_1||z_2| + |z_2|^2 = (|z_1| + |z_2|)^2$$

两边开方即得 $|z_1 + z_2| \leq |z_1| + |z_2|$。

### 3.4 复平面上的拓扑

**定义**：设 $z_0 \in \mathbb{C}$，$\varepsilon > 0$，$z_0$ 的 $\varepsilon$-邻域为：
$$N_\varepsilon(z_0) = \{z \in \mathbb{C} : |z - z_0| < \varepsilon\}$$

- **开集**：集合 $D$ 中每个点都存在完全包含在 $D$ 中的邻域。
- **闭集**：其补集为开集的集合。
- **连通**：$D$ 不能分解为两个不相交的非空开子集之并。
- **区域**（Region）：连通的开集。区域的闭包称为**闭区域**。
- **简单曲线**（Jordan 曲线）：没有自交的连续曲线。
- **简单闭曲线**：首尾相接且不自交的曲线。

### 3.5 复变函数的定义

**定义**：设 $D \subseteq \mathbb{C}$ 为非空集合，映射 $f: D \to \mathbb{C}$ 称为定义在 $D$ 上的**复变函数**。

记 $w = f(z)$，若 $z = x + iy$，$w = u + iv$，则：
$$f(z) = u(x, y) + iv(x, y)$$

其中 $u(x,y)$ 和 $v(x,y)$ 是二元实函数。

### 3.6 复变函数的极限

**定义**：设 $f(z)$ 在 $z_0$ 的去心邻域内有定义。若 $\forall \varepsilon > 0$，$\exists \delta > 0$，当 $0 < |z - z_0| < \delta$ 时，有 $|f(z) - A| < \varepsilon$，则称 $A$ 为 $f(z)$ 当 $z \to z_0$ 时的极限，记为 $\lim_{z \to z_0} f(z) = A$。

**重要定理**：$\lim_{z \to z_0} f(z) = A$ 的充要条件是：

$$\lim_{(x,y) \to (x_0, y_0)} u(x,y) = \operatorname{Re}A, \quad \lim_{(x,y) \to (x_0, y_0)} v(x,y) = \operatorname{Im}A$$

**证明（必要性）**：设 $\lim_{z \to z_0} f(z) = A = a + ib$。则 $\forall \varepsilon > 0$，$\exists \delta > 0$，当 $0 < |z - z_0| < \delta$ 时：

$$|f(z) - A| = \sqrt{(u - a)^2 + (v - b)^2} < \varepsilon$$

由此推出 $|u - a| < \varepsilon$，$|v - b| < \varepsilon$。

（充分性类似，利用 $|f(z) - A| \leq |u-a| + |v-b|$。）

**注意**：复极限中 $z \to z_0$ 要求 $z$ 从**所有方向**趋近 $z_0$，这与实函数的单侧极限不同。

### 3.7 复变函数的连续性

**定义**：若 $\lim_{z \to z_0} f(z) = f(z_0)$，则称 $f(z)$ 在 $z_0$ 处连续。

$f(z)$ 在 $z_0 = x_0 + iy_0$ 连续的充要条件：$u(x,y)$ 和 $v(x,y)$ 在 $(x_0, y_0)$ 处连续。

**连续函数的性质**：
- 连续函数的和、差、积、商（分母不为零）仍连续。
- 连续函数的复合仍连续。
- 在紧集（有界闭集）上连续的函数一致连续，且能达到最大值和最小值（最大模原理的雏形）。

### 3.8 复数序列的极限

复数序列 $\{z_n\}$ 收敛于 $z_0$ 的充要条件是 $\operatorname{Re}z_n \to \operatorname{Re}z_0$ 且 $\operatorname{Im}z_n \to \operatorname{Im}z_0$。

**Cauchy 收敛准则**：$\{z_n\}$ 收敛的充要条件是它是 Cauchy 列，即 $\forall \varepsilon > 0$，$\exists N$，当 $m, n > N$ 时 $|z_m - z_n| < \varepsilon$。这是 $\mathbb{C}$ 完备性的体现。
