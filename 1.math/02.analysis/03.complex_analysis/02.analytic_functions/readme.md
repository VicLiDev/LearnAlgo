# 第二章 解析函数

## 一、几何意义

### 1.1 解析函数与共形映射

解析函数是复变函数论的核心研究对象，它最深刻的几何性质之一就是**共形性**（保角性）。

设 $w = f(z)$ 在区域 $D$ 内解析，$f'(z_0) \neq 0$。在点 $z_0$ 附近，$f$ 将 $z$ 平面上的曲线映射到 $w$ 平面上，且满足：

1. **旋转角不变性**：通过 $z_0$ 的任意两条曲线 $C_1$、$C_2$，经映射后在 $w_0 = f(z_0)$ 处的夹角等于映射前在 $z_0$ 处的夹角（包括转向）。
2. **伸缩率不变性**：在 $z_0$ 处的伸缩因子为 $|f'(z_0)|$，与方向无关。

因此，解析函数在导数不为零的点处实现的是**共形映射**（Conformal mapping），即同时保持角度和局部形状。

### 1.2 Cauchy-Riemann 方程的几何意义

设 $f(z) = u(x,y) + iv(x,y)$ 解析。Cauchy-Riemann 方程：

$$\frac{\partial u}{\partial x} = \frac{\partial v}{\partial y}, \quad \frac{\partial u}{\partial y} = -\frac{\partial v}{\partial x}$$

几何意义：等值线 $u(x,y) = c_1$ 与 $v(x,y) = c_2$ 在交点处**正交**。

**原因**：曲线 $u = c_1$ 的法向量为 $\nabla u = (u_x, u_y)$，曲线 $v = c_2$ 的法向量为 $\nabla v = (v_x, v_y)$。由 C-R 方程：

$$\nabla u \cdot \nabla v = u_x v_x + u_y v_y = u_x(-u_y) + u_y(u_x) = 0$$

这说明 $u$ 和 $v$ 的等值线族彼此正交。例如在静电场中，$u$ 为电势，$v$ 为电场线（流线）。

### 1.3 Jacobi 矩阵的几何含义

解析函数的 Jacobi 矩阵为：

$$J_f = \begin{pmatrix} u_x & u_y \\ v_x & v_y \end{pmatrix} = \begin{pmatrix} u_x & -v_x \\ v_x & u_x \end{pmatrix}$$

这是形式为 $\begin{pmatrix} a & -b \\ b & a \end{pmatrix}$ 的矩阵，对应复数乘法 $a + ib$。这样的矩阵表示**旋转加伸缩**的复合变换，这就是共形性的代数根源。

$$\det J_f = u_x^2 + v_x^2 = |f'(z)|^2 > 0 \quad (\text{当 } f'(z) \neq 0)$$

正的 Jacobian 行列式保证映射保持**定向**（orientation-preserving）。

---

## 二、应用场景

### 2.1 二维势论

调和函数（Laplace 方程 $\Delta \phi = 0$ 的解）是物理学中极重要的一类函数。由于解析函数的实部和虚部都是调和函数，复变函数论为求解二维 Laplace 方程提供了强有力的工具。

应用领域：
- **静电学**：二维静电场中的电势分布。
- **流体力学**：二维不可压缩无旋流体的速度势和流函数。
- **热传导**：二维稳态温度分布。
- **弹性力学**：二维应力分析（Airy 应力函数）。

### 2.2 平面场的可视化

利用解析函数 $w = f(z) = u + iv$，可以将 $u$ 和 $v$ 的等值线作为两组正交曲线族来描绘平面场。例如：
- 绕圆柱的流体流动用 $w(z) = z + \frac{R^2}{z}$ 描述。
- 偶极子场用 $w(z) = \frac{m}{z}$ 描述。

### 2.3 电磁学与光学

在电磁学中，利用解析函数可以处理二维边值问题。通过共形映射，将复杂几何区域（如多边形区域）上的场问题转化为简单区域（如上半平面或单位圆）上的问题。

### 2.4 调和分析

解析函数与调和函数的紧密联系使得复变函数论成为 Fourier 分析、调和分析等领域的理论基础。

---

## 三、数学理论（及推导）

### 3.1 复变函数的导数

**定义**：设 $f(z)$ 在 $z_0$ 的某邻域内有定义。若极限

$$f'(z_0) = \lim_{\Delta z \to 0} \frac{f(z_0 + \Delta z) - f(z_0)}{\Delta z}$$

存在且有限，则称 $f(z)$ 在 $z_0$ 处**可导**（或**可微**）。

**关键区别**：与实函数不同，$\Delta z \to 0$ 要求 $\Delta z$ 从**复平面上所有方向**趋近于 0。这是一个比实可导性强得多的条件。

### 3.2 Cauchy-Riemann 方程

**定理（C-R 方程的必要性）**：若 $f(z) = u(x,y) + iv(x,y)$ 在 $z_0 = x_0 + iy_0$ 处可导，则：

$$(1) \quad \frac{\partial u}{\partial x}(x_0, y_0) = \frac{\partial v}{\partial y}(x_0, y_0)$$
$$(2) \quad \frac{\partial u}{\partial y}(x_0, y_0) = -\frac{\partial v}{\partial x}(x_0, y_0)$$

**证明**：令 $\Delta z = \Delta x + i\Delta y$。导数存在意味着沿任何路径 $\Delta z \to 0$ 时，差商趋于同一个值。

**路径一**：令 $\Delta z$ 沿实轴趋近（$\Delta y = 0$，$\Delta x \to 0$）：

$$f'(z_0) = \lim_{\Delta x \to 0} \frac{u(x_0+\Delta x, y_0) - u(x_0,y_0)}{\Delta x} + i\lim_{\Delta x \to 0} \frac{v(x_0+\Delta x, y_0) - v(x_0,y_0)}{\Delta x} = u_x + iv_x$$

**路径二**：令 $\Delta z$ 沿虚轴趋近（$\Delta x = 0$，$\Delta y \to 0$）：

$$f'(z_0) = \lim_{\Delta y \to 0} \frac{u(x_0, y_0+\Delta y) - u(x_0,y_0)}{i\Delta y} + i\lim_{\Delta y \to 0} \frac{v(x_0, y_0+\Delta y) - v(x_0,y_0)}{i\Delta y}$$

$$= -i u_y + v_y = v_y - iu_y$$

由于导数唯一，两种路径的结果必须相等：

$$u_x + iv_x = v_y - iu_y$$

比较实部和虚部，即得 C-R 方程。

**导数表达式**：当 C-R 方程成立时，

$$f'(z) = u_x + iv_x = v_y - iu_y$$

### 3.3 C-R 方程的充分条件

**定理**：若 $u(x,y)$ 和 $v(x,y)$ 在 $(x_0, y_0)$ 的某邻域内具有连续的一阶偏导数，且满足 C-R 方程，则 $f(z) = u + iv$ 在 $z_0$ 处可导。

**证明**：设 $\Delta z = \Delta x + i\Delta y$。由二元函数的全微分公式：

$$\Delta u = u(x_0+\Delta x, y_0+\Delta y) - u(x_0, y_0) = u_x \Delta x + u_y \Delta y + \varepsilon_1 \Delta x + \varepsilon_2 \Delta y$$

$$\Delta v = v(x_0+\Delta x, y_0+\Delta y) - v(x_0, y_0) = v_x \Delta x + v_y \Delta y + \varepsilon_3 \Delta x + \varepsilon_4 \Delta y$$

其中 $\varepsilon_j \to 0$（当 $\Delta z \to 0$ 时）。

利用 C-R 方程 $u_x = v_y$，$u_y = -v_x$：

$$\Delta f = \Delta u + i\Delta v = u_x \Delta x + u_y \Delta y + i(v_x \Delta x + v_y \Delta y) + o(|\Delta z|)$$

$$= u_x \Delta x - v_x \Delta y + i(v_x \Delta x + u_x \Delta y) + o(|\Delta z|)$$

$$= u_x(\Delta x + i\Delta y) + iv_x(\Delta x + i\Delta y) + o(|\Delta z|)$$

$$= (u_x + iv_x)\Delta z + o(|\Delta z|)$$

因此：

$$\frac{\Delta f}{\Delta z} = u_x + iv_x + \frac{o(|\Delta z|)}{\Delta z} \to u_x + iv_x \quad (\Delta z \to 0)$$

### 3.4 解析函数的定义

**定义**：
- 若 $f(z)$ 在 $z_0$ 的某个邻域内处处可导，则称 $f(z)$ 在 $z_0$ 处**解析**（analytic），也称**全纯**（holomorphic）。
- 若 $f(z)$ 在区域 $D$ 内每一点都解析，则称 $f(z)$ 在 $D$ 内解析。
- 若 $f(z)$ 在 $z_0$ 处不解析，但 $z_0$ 的任意邻域内都有解析点，则称 $z_0$ 为 $f$ 的**奇点**。

**注**：解析性是一个比单点可导强得多的条件。它要求函数在该点附近的一整片区域都可导。

### 3.5 调和函数

**定义**：具有二阶连续偏导数的实函数 $\phi(x,y)$ 若满足 Laplace 方程：

$$\Delta \phi = \frac{\partial^2 \phi}{\partial x^2} + \frac{\partial^2 \phi}{\partial y^2} = 0$$

则称 $\phi$ 为**调和函数**。

**定理**：若 $f(z) = u(x,y) + iv(x,y)$ 在区域 $D$ 内解析，则 $u$ 和 $v$ 都是 $D$ 内的调和函数。

**证明**：由 C-R 方程 $u_x = v_y$，$u_y = -v_x$。若 $f$ 解析（从而 $f'$ 连续，稍后由 Cauchy 积分公式证明），则 $u$ 和 $v$ 具有连续二阶偏导数。对 C-R 方程再求导：

$$u_{xx} = v_{yx}, \quad u_{yy} = -v_{xy}$$

由混合偏导的连续性（Schwarz 定理）$v_{yx} = v_{xy}$，故：

$$u_{xx} + u_{yy} = v_{yx} - v_{xy} = 0$$

同理 $v_{xx} + v_{yy} = 0$。

**共轭调和函数**：若 $u$ 是区域 $D$ 内的调和函数，$v$ 使 $f = u + iv$ 在 $D$ 内解析，则称 $v$ 为 $u$ 的**共轭调和函数**。

**注意**：共轭关系不对称。$v$ 是 $u$ 的共轭调和函数时，$u$ 是 $-v$ 的共轭调和函数。

### 3.6 由调和函数构造解析函数

给定调和函数 $u(x,y)$，可通过以下方法求其共轭调和函数 $v(x,y)$：

由 C-R 方程：$\frac{\partial v}{\partial y} = \frac{\partial u}{\partial x}$，$\frac{\partial v}{\partial x} = -\frac{\partial u}{\partial y}$。

积分第一个方程：

$$v(x, y) = \int \frac{\partial u}{\partial x} \, dy + \varphi(x)$$

然后利用第二个方程确定 $\varphi'(x)$。

**例**：$u(x,y) = x^2 - y^2$，则 $u_x = 2x$，$u_y = -2y$。

$$v = \int 2x \, dy = 2xy + \varphi(x)$$

由 $v_x = -u_y = 2y$：$2y + \varphi'(x) = 2y$，故 $\varphi'(x) = 0$，$\varphi(x) = C$。

所以 $v(x,y) = 2xy + C$，$f(z) = (x^2 - y^2) + i(2xy) = (x+iy)^2 = z^2$。

### 3.7 极坐标形式的 C-R 方程

设 $z = re^{i\theta}$，$f(z) = u(r, \theta) + iv(r, \theta)$，则 C-R 方程的极坐标形式为：

$$\frac{\partial u}{\partial r} = \frac{1}{r}\frac{\partial v}{\partial \theta}, \quad \frac{\partial v}{\partial r} = -\frac{1}{r}\frac{\partial u}{\partial \theta}$$

导数表达式：

$$f'(z) = e^{-i\theta}\left(\frac{\partial u}{\partial r} + i\frac{\partial v}{\partial r}\right) = \frac{1}{z}\left(r\frac{\partial u}{\partial r} + ir\frac{\partial v}{\partial r}\right)$$

**推导**：利用链式法则 $\frac{\partial}{\partial x} = \cos\theta \frac{\partial}{\partial r} - \frac{\sin\theta}{r}\frac{\partial}{\partial \theta}$，$\frac{\partial}{\partial y} = \sin\theta \frac{\partial}{\partial r} + \frac{\cos\theta}{r}\frac{\partial}{\partial \theta}$ 代入直角坐标 C-R 方程即得。

### 3.8 解析函数的无穷可微性

解析函数具有极其优美的性质：**解析函数在其定义域内具有任意阶导数**。

这一性质在实分析中没有对应物——实可微函数不一定二阶可微。解析函数的可导性蕴含了无穷可微性，这是复分析中最令人惊叹的结果之一。

其严格证明依赖 Cauchy 积分公式（将在第五章详细论述），此处仅陈述结论：

**定理**：若 $f(z)$ 在区域 $D$ 内解析，则 $f(z)$ 在 $D$ 内具有任意阶导数，且各阶导数仍为解析函数。

### 3.9 常见解析函数示例

| 函数 $f(z)$ | 解析区域 | $f'(z)$ |
|:---:|:---:|:---:|
| $z^n$（$n \in \mathbb{Z}^+$） | 全平面 $\mathbb{C}$ | $nz^{n-1}$ |
| $e^z$ | 全平面 $\mathbb{C}$ | $e^z$ |
| $\sin z$ | 全平面 $\mathbb{C}$ | $\cos z$ |
| $\cos z$ | 全平面 $\mathbb{C}$ | $-\sin z$ |
| $\frac{1}{z}$ | $\mathbb{C} \setminus \{0\}$ | $-\frac{1}{z^2}$ |
| $\operatorname{Re}(z)$ | 无处解析 | — |
| $|z|$ | 无处解析 | — |

**注**：$\operatorname{Re}(z) = x$ 对应 $u = x$，$v = 0$，C-R 方程要求 $1 = 0$，矛盾。$|z| = \sqrt{x^2+y^2}$ 仅在 $z = 0$ 处满足 C-R 方程（但 $z=0$ 不是区域的内点，故无处解析）。
