# 第十一章 Z 变换

## 一、几何意义

### 1.1 Z 变换与 Laplace 变换的几何关系

Z 变换是 Laplace 变换在离散时间信号上的对应物。两者通过**映射关系**联系起来：

$$z = e^{sT} \quad \text{或} \quad s = \frac{1}{T}\ln z$$

其中 $T$ 是采样周期。

**几何对应**：
- $s$ 平面的**虚轴** $s = i\omega$ 映射为 $z$ 平面的**单位圆** $|z| = 1$。
- $s$ 平面的**左半平面** $\operatorname{Re}s < 0$ 映射为 $z$ 平面的**单位圆内部** $|z| < 1$。
- $s$ 平面的**右半平面** $\operatorname{Re}s > 0$ 映射为 $z$ 平面的**单位圆外部** $|z| > 1$。
- $s$ 平面的实轴 $s = \sigma$ 映射为 $z$ 平面的正实轴 $z = e^{\sigma T} > 0$。
- $s$ 平面上的水平线 $\operatorname{Re}s = \sigma_0$ 映射为 $z$ 平面上的圆 $|z| = e^{\sigma_0 T}$。

这一映射关系是理解连续系统与离散系统之间对应关系的关键。

### 1.2 收敛域的几何

Z 变换 $X(z) = \sum_{n=-\infty}^{+\infty} x[n]z^{-n}$ 的收敛域（ROC）是 $z$ 平面上的**环形区域** $R_1 < |z| < R_2$。

收敛域的几何形状取决于信号的类型：

| 信号类型 | 收敛域 |
|:---:|:---:|
| 有限长序列 | 整个 $z$ 平面（可能除去 $z=0$ 或 $z=\infty$） |
| 右边序列（因果序列） | $|z| > R_1$（圆外） |
| 左边序列（反因果序列） | $|z| < R_2$（圆内） |
| 双边序列 | $R_1 < |z| < R_2$（环形） |

**极点与收敛域的关系**：
- 极点总是位于收敛域的边界上。
- 收敛域内不能有极点。
- 因果系统的收敛域为最外侧极点的外部。

### 1.3 极点位置与系统行为

对于因果离散系统，极点在 $z$ 平面上的位置决定系统的时域行为：

- **极点在单位圆内**（$|z| < 1$）：对应的时域分量 $z^n$ 指数衰减 $\to$ **稳定**。
- **极点在单位圆上**（$|z| = 1$）：对应持续振荡或常值 $\to$ **临界稳定**。
- **极点在单位圆外**（$|z| > 1$）：对应分量指数增长 $\to$ **不稳定**。
- 极点的**角度** $\theta = \arg z$ 决定振荡频率：$\omega = \theta / T$。
- 正实轴上的极点（$\theta = 0$）对应非振荡的指数衰减/增长。
- 共轭极点对 $re^{\pm i\theta}$ 对应衰减/增长的振荡。

### 1.4 频率响应的几何解释

离散系统的频率响应 $H(e^{i\omega})$ 就是在单位圆上求值：

$$H(e^{i\omega}) = H(z)\Big|_{z=e^{i\omega}}$$

**几何意义**：频率响应的幅值和相位可以从零极点图上直接读出。

$$H(z) = K\frac{\prod_{i}(z-z_i)}{\prod_{j}(z-p_j)}$$

在 $z = e^{i\omega}$ 处：

$$|H(e^{i\omega})| = |K|\frac{\prod_i|e^{i\omega}-z_i|}{\prod_j|e^{i\omega}-p_j|}$$

分子和分母的每个因子 $|e^{i\omega}-z_0|$ 就是从零点（或极点）$z_0$ 到单位圆上点 $e^{i\omega}$ 的**距离**。

- 当频率 $\omega$ 接近某个极点时，分母的距离变小 $\to$ 幅度增大（**共振峰**）。
- 当频率 $\omega$ 接近某个零点时，分子的距离变小 $\to$ 幅度减小（**陷波**）。

---

## 二、应用场景

### 2.1 数字信号处理（DSP）

Z 变换是数字信号处理的核心数学工具：

- **数字滤波器设计**：IIR（Infinite Impulse Response）和 FIR（Finite Impulse Response）滤波器的设计与分析。
- **系统函数与传递函数**：$H(z) = \frac{Y(z)}{X(z)}$ 描述输入输出关系。
- **稳定性分析**：通过极点位置判断系统稳定性。

### 2.2 差分方程求解

与 Laplace 变换求解微分方程类似，Z 变换将线性常系数差分方程化为代数方程：

$$y[n] + a_1 y[n-1] + \cdots + a_N y[n-N] = b_0 x[n] + \cdots + b_M x[n-M]$$

$$\xrightarrow{\mathcal{Z}} \quad Y(z)(1 + a_1 z^{-1} + \cdots + a_N z^{-N}) = X(z)(b_0 + \cdots + b_M z^{-M})$$

### 2.3 控制系统

**离散控制系统**中：
- 采样数据系统的分析。
- 数字控制器（PID 控制器的数字实现）。
- 稳定性判据：Jury 稳定性判据、Nyquist 判据的离散版本。

### 2.4 时间序列分析

在统计学和经济学中，ARMA（自回归移动平均）模型的分析依赖于 Z 变换：

- AR(p) 模型：$y[n] = \sum_{k=1}^{p}\phi_k y[n-k] + \varepsilon[n]$
- MA(q) 模型：$y[n] = \sum_{k=0}^{q}\theta_k \varepsilon[n-k]$

### 2.5 图像处理

二维 Z 变换用于分析二维离散系统的频率响应，在图像滤波、压缩中有应用。

---

## 三、数学理论（及推导）

### 3.1 Z 变换的定义

**定义（双边 Z 变换）**：

$$X(z) = \mathcal{Z}[x[n]] = \sum_{n=-\infty}^{+\infty} x[n]z^{-n}$$

**定义（单边 Z 变换）**：

$$X(z) = \mathcal{Z}[x[n]] = \sum_{n=0}^{+\infty} x[n]z^{-n}$$

单边 Z 变换适用于因果信号和具有非零初始条件的系统分析。

### 3.2 收敛域（ROC）

Z 变换的收敛域由 Cauchy 根值判别法确定。

$$\sum_{n=0}^{\infty}|x[n]||z|^{-n} \text{ 收敛} \iff \limsup_{n\to\infty}\sqrt[n]{|x[n]|} < |z|$$

类似地，对左边序列 $\sum_{n=-\infty}^{-1}|x[n]||z|^{-n}$，令 $m = -n$：

$$\sum_{m=1}^{\infty}|x[-m]||z|^m \text{ 收敛} \iff |z| < \frac{1}{\limsup_{m\to\infty}\sqrt[m]{|x[-m]|}}$$

**例**：$x[n] = a^n u[n]$（因果指数序列）

$$X(z) = \sum_{n=0}^{\infty} a^n z^{-n} = \sum_{n=0}^{\infty}\left(\frac{a}{z}\right)^n = \frac{1}{1-az^{-1}} = \frac{z}{z-a}, \quad |z| > |a|$$

### 3.3 基本性质

设 $X(z) = \mathcal{Z}[x[n]]$，收敛域为 $R_x$。

**（1）线性性**：

$$\mathcal{Z}[ax[n] + by[n]] = aX(z) + bY(z)$$

收敛域至少为 $R_x \cap R_y$。

**（2）时移性质**：

**双边**：$\mathcal{Z}[x[n-k]] = z^{-k}X(z)$，ROC 不变。

**单边**：

$$\mathcal{Z}[x[n-1]] = z^{-1}X(z) + x[-1]$$

$$\mathcal{Z}[x[n-2]] = z^{-2}X(z) + z^{-1}x[-1] + x[-2]$$

一般地：

$$\mathcal{Z}[x[n-k]] = z^{-k}X(z) + \sum_{j=1}^{k} z^{-(k-j)} x[-j], \quad k > 0$$

**（3）Z 域尺度变换**：

$$\mathcal{Z}[a^n x[n]] = X\left(\frac{z}{a}\right)$$

ROC：$|z| > |a|R_1$（若原 ROC 为 $|z| > R_1$）。

**推导**：

$$\sum_{n=0}^{\infty} a^n x[n] z^{-n} = \sum_{n=0}^{\infty} x[n]\left(\frac{z}{a}\right)^{-n} = X\left(\frac{z}{a}\right)$$

**（4）卷积定理**：

$$\mathcal{Z}[x[n] * y[n]] = X(z) \cdot Y(z)$$

其中 $(x * y)[n] = \sum_{k=-\infty}^{+\infty} x[k]y[n-k]$。

**推导**：

$$\mathcal{Z}[x*y] = \sum_n\left[\sum_k x[k]y[n-k]\right]z^{-n} = \sum_k x[k]\sum_n y[n-k]z^{-n} = \sum_k x[k]z^{-k}Y(z) = X(z)Y(z)$$

**（5）初值定理**（单边 Z 变换）：

$$x[0] = \lim_{z\to\infty}X(z)$$

**推导**：$X(z) = x[0] + x[1]z^{-1} + x[2]z^{-2} + \cdots$，当 $z \to \infty$ 时，$z^{-k} \to 0$（$k \geq 1$），故 $\lim_{z\to\infty}X(z) = x[0]$。

**（6）终值定理**（单边 Z 变换）：

若 $(z-1)X(z)$ 的极点都在单位圆内，则：

$$\lim_{n\to\infty}x[n] = \lim_{z\to 1}(z-1)X(z)$$

**（7）Z 域微分**：

$$\mathcal{Z}[nx[n]] = -z\frac{dX(z)}{dz}$$

**推导**：

$$-z\frac{dX(z)}{dz} = -z\frac{d}{dz}\sum_{n}x[n]z^{-n} = -z\sum_n x[n](-n)z^{-n-1} = \sum_n nx[n]z^{-n}$$

**（8）时间反转**：

$$\mathcal{Z}[x[-n]] = X\left(\frac{1}{z}\right)$$

ROC：$\frac{1}{R_2} < |z| < \frac{1}{R_1}$（若原 ROC 为 $R_1 < |z| < R_2$）。

### 3.4 逆 Z 变换

**（1）留数法（围道积分法）**

$$x[n] = \frac{1}{2\pi i}\oint_C X(z)z^{n-1}\,dz$$

其中 $C$ 是收敛域内绕原点的正向简单闭曲线。

**用留数定理**：

$$x[n] = \sum_k \operatorname{Res}\left[X(z)z^{n-1}, z_k\right]$$

其中求和遍及围道 $C$ 内的所有极点 $z_k$。

- 对于**因果序列**（ROC 为 $|z| > R_1$），取 $C$ 为半径大于 $R_1$ 的圆，求内部所有极点的留数。
- 对于 $n < 0$，需注意 $z^{n-1}$ 在 $z = 0$ 处的极点。

**（2）部分分式展开法**

将 $X(z)$ 展开为部分分式，然后逐项查表逆变换。

**注意**：通常对 $X(z)/z$ 做部分分式展开（以便得到 $z/(z-a)$ 的标准形式）。

**例**：$X(z) = \frac{z}{(z-1)(z-2)}$，ROC：$|z| > 2$。

$$\frac{X(z)}{z} = \frac{1}{(z-1)(z-2)} = \frac{-1}{z-1} + \frac{1}{z-2}$$

$$X(z) = \frac{-z}{z-1} + \frac{z}{z-2}$$

$$x[n] = -1 \cdot 1^n + 1 \cdot 2^n = 2^n - 1, \quad n \geq 0$$

**（3）长除法（幂级数法）**

对 $X(z)$ 做长除法，按 $z^{-1}$ 的升幂展开。适用于求有限个值或无法做部分分式的情况。

### 3.5 与 Laplace 变换的关系

**采样信号的 Laplace 变换**：

设连续信号 $f(t)$ 经理想采样（周期 $T$）得到：

$$f_s(t) = \sum_{n=-\infty}^{+\infty} f(nT)\delta(t-nT)$$

其 Laplace 变换：

$$F_s(s) = \sum_{n=-\infty}^{+\infty} f(nT)e^{-snT}$$

令 $z = e^{sT}$，则 $F_s(s) = X(z)$，其中 $X(z) = \sum_{n=-\infty}^{+\infty} f(nT)z^{-n}$。

**映射关系总结**：

| $s$ 平面 | $z = e^{sT}$ | $z$ 平面 |
|:---:|:---:|:---:|
| 虚轴 $s = i\omega$ | $|z| = 1$ | 单位圆 |
| 左半平面 $\operatorname{Re}s < 0$ | $|z| < 1$ | 单位圆内 |
| 右半平面 $\operatorname{Re}s > 0$ | $|z| > 1$ | 单位圆外 |
| 原点 $s = 0$ | $z = 1$ | 正实轴上 $(1,0)$ |
| $s = i\omega_s/2 = i\pi/T$ | $z = -1$ | 负实轴上 $(-1,0)$ |
| $s = i\omega_s = i2\pi/T$ | $z = 1$ | 回到正实轴 |

**频域关系**：$s$ 平面上宽度为 $2\pi/T$ 的水平带映射为整个 $z$ 平面。因此，离散信号的频谱是连续信号频谱的**周期延拓**（以 $\omega_s = 2\pi/T$ 为周期）。

### 3.6 差分方程求解

**例**：求解差分方程 $y[n] - \frac{3}{2}y[n-1] + \frac{1}{2}y[n-2] = x[n]$，$x[n] = \left(\frac{1}{4}\right)^n u[n]$，$y[-1] = y[-2] = 0$。

**步骤一**：Z 变换（单边）：

$$Y(z) - \frac{3}{2}z^{-1}Y(z) + \frac{1}{2}z^{-2}Y(z) = X(z) = \frac{1}{1-\frac{1}{4}z^{-1}} = \frac{z}{z-\frac{1}{4}}$$

**步骤二**：求解 $Y(z)$：

$$Y(z) = \frac{X(z)}{1 - \frac{3}{2}z^{-1} + \frac{1}{2}z^{-2}} = \frac{\frac{z}{z-1/4}}{\frac{(z-1)(z-1/2)}{z^2}} = \frac{z^3}{(z-1/4)(z-1)(z-1/2)}$$

**步骤三**：部分分式展开：

$$\frac{Y(z)}{z} = \frac{z^2}{(z-1/4)(z-1)(z-1/2)}$$

分解后逐项查表逆变换，得到 $y[n]$。

### 3.7 常用 Z 变换对

| $x[n]$ | $X(z)$ | ROC |
|:---:|:---:|:---:|
| $\delta[n]$ | $1$ | $\forall z$ |
| $u[n]$ | $\frac{1}{1-z^{-1}} = \frac{z}{z-1}$ | $|z| > 1$ |
| $a^n u[n]$ | $\frac{1}{1-az^{-1}} = \frac{z}{z-a}$ | $|z| > |a|$ |
| $na^n u[n]$ | $\frac{az^{-1}}{(1-az^{-1})^2} = \frac{az}{(z-a)^2}$ | $|z| > |a|$ |
| $n^2 a^n u[n]$ | $\frac{az^{-1}(1+az^{-1})}{(1-az^{-1})^3}$ | $|z| > |a|$ |
| $\cos(\omega_0 n)u[n]$ | $\frac{1-\cos(\omega_0)z^{-1}}{1-2\cos(\omega_0)z^{-1}+z^{-2}}$ | $|z| > 1$ |
| $\sin(\omega_0 n)u[n]$ | $\frac{\sin(\omega_0)z^{-1}}{1-2\cos(\omega_0)z^{-1}+z^{-2}}$ | $|z| > 1$ |
| $a^n\cos(\omega_0 n)u[n]$ | $\frac{1-a\cos(\omega_0)z^{-1}}{1-2a\cos(\omega_0)z^{-1}+a^2z^{-2}}$ | $|z| > |a|$ |
| $-a^n u[-n-1]$ | $\frac{1}{1-az^{-1}}$ | $|z| < |a|$ |

### 3.8 数字信号处理中的应用

**FIR 滤波器**：

$$H(z) = \sum_{n=0}^{N-1} h[n]z^{-n}$$

极点全部在 $z = 0$（单位圆内），故 FIR 滤波器总是**稳定**的。

**IIR 滤波器**：

$$H(z) = \frac{\sum_{k=0}^{M} b_k z^{-k}}{1 + \sum_{k=1}^{N} a_k z^{-k}}$$

稳定性条件：所有极点都在单位圆内。

**离散 Fourier 变换（DFT）的关系**：

Z 变换在单位圆上的等间隔采样即为 DFT：

$$X[k] = X(z)\Big|_{z=e^{i2\pi k/N}} = \sum_{n=0}^{N-1} x[n]e^{-i2\pi kn/N}, \quad k = 0, 1, \ldots, N-1$$

这是连接 Z 变换理论和实际数字信号处理算法（FFT）的桥梁。
