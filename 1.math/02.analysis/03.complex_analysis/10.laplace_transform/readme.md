# 第十章 Laplace 变换

## 一、几何意义

### 1.1 Laplace 变换与 Fourier 变换的关系

Laplace 变换可以视为 Fourier 变换的推广。对于不满足绝对可积条件的信号 $f(t)$（如 $f(t) = e^{at}$，$a > 0$），Fourier 变换不存在。但若乘以衰减因子 $e^{-\sigma t}$（$\sigma$ 足够大），使 $f(t)e^{-\sigma t}$ 绝对可积，则可以对后者做 Fourier 变换：

$$\mathcal{F}[f(t)e^{-\sigma t}](\omega) = \int_0^{\infty} f(t)e^{-\sigma t}e^{-i\omega t}\,dt = \int_0^{\infty} f(t)e^{-(\sigma+i\omega)t}\,dt = F(s)$$

其中 $s = \sigma + i\omega$。令 $F(s) = \mathcal{L}[f(t)](s)$，这就是 **Laplace 变换**。

**几何意义**：Laplace 变换在复平面 $s = \sigma + i\omega$ 的某个半平面（$\sigma > \sigma_0$，$\sigma_0$ 为收敛横坐标）上定义。对每个固定的 $\sigma$，$F(\sigma + i\omega)$ 可以理解为 $f(t)e^{-\sigma t}$ 关于 $t$ 的 Fourier 变换（在频域 $\omega$ 上）。

### 1.2 收敛域的几何

Laplace 变换 $F(s)$ 的**收敛域**（ROC, Region of Convergence）是 $s$ 平面上的某个半平面 $\operatorname{Re}s > \sigma_0$。

- 在收敛域内，$F(s)$ 是 $s$ 的解析函数。
- 收敛域的左边界 $\operatorname{Re}s = \sigma_0$ 由 $f(t)$ 的增长速度决定：若 $|f(t)| \leq Me^{\sigma_0 t}$，则 $\sigma_0$ 是收敛横坐标。
- $F(s)$ 的奇点全部位于收敛域的左侧（$\operatorname{Re}s \leq \sigma_0$）。

**几何直观**：$e^{-\sigma t}$ 是一个指数衰减因子。$\sigma$ 越大，衰减越快，$f(t)e^{-\sigma t}$ 就越容易绝对可积。所以向右移动的半平面总是收敛域的子集。

### 1.3 极点分布与系统行为

在控制理论中，传递函数 $G(s) = \mathcal{L}[g(t)](s)$ 的极点位置完全决定了线性时不变系统的行为：

- **极点在左半平面**（$\operatorname{Re}s < 0$）：对应的时域分量 $e^{st}$ 指数衰减 $\to$ **稳定**。
- **极点在右半平面**（$\operatorname{Re}s > 0$）：对应分量指数增长 $\to$ **不稳定**。
- **极点在虚轴上**（$\operatorname{Re}s = 0$）：对应持续振荡或常值 $\to$ **临界稳定**。
- 极点的虚部决定**振荡频率**，实部决定**衰减/增长速率**。

### 1.4 初值与终值的几何

**初值定理**：$f(0^+) = \lim_{s\to\infty}sF(s)$

**终值定理**：$f(\infty) = \lim_{s\to 0}sF(s)$（条件：$sF(s)$ 的极点均在左半平面）

几何意义：初值由 $F(s)$ 在无穷远的行为决定（高频特性）；终值由 $F(s)$ 在原点附近的行为决定（低频/直流特性）。

---

## 二、应用场景

### 2.1 求解常微分方程

Laplace 变换将常系数线性常微分方程化为 $s$ 域中的代数方程：

$$a_n y^{(n)}(t) + \cdots + a_0 y(t) = f(t)$$

$$\xrightarrow{\mathcal{L}} \quad (a_n s^n + \cdots + a_0)Y(s) = F(s) + \text{初始条件项}$$

$$\xrightarrow{\text{求解}} \quad Y(s) = \frac{F(s) + \text{初始条件项}}{a_n s^n + \cdots + a_0}$$

$$\xrightarrow{\mathcal{L}^{-1}} \quad y(t)$$

这是工程数学中最常用的求解方法，比经典方法（特征方程+待定系数）更系统。

### 2.2 控制系统分析

- **传递函数**：$G(s) = \frac{Y(s)}{U(s)}$（零初始条件）。
- **稳定性判据**：Routh-Hurwitz 判据、Nyquist 判据（基于 $G(s)$ 在复平面上的频率响应）。
- **根轨迹法**：研究参数变化时闭环极点在 $s$ 平面上的运动轨迹。

### 2.3 电路分析

电路方程（KVL/KCL）可以方便地用 Laplace 变换求解：
- 电阻：$V(s) = RI(s)$
- 电感：$V(s) = sLI(s) - Li(0)$
- 电容：$V(s) = \frac{1}{sC}I(s) + \frac{v(0)}{s}$

阻抗 $Z_R = R$，$Z_L = sL$，$Z_C = \frac{1}{sC}$，与直流电阻分析完全类比。

### 2.4 信号与系统

- 单位冲激响应 $h(t)$ 的 Laplace 变换 $H(s)$ 为系统函数。
- 因果系统的极点全部在左半平面 $\iff$ 系统稳定（BIBO 稳定）。
- 卷积定理：$\mathcal{L}[f * g] = F(s)G(s)$，时域卷积等价于 $s$ 域乘积。

---

## 三、数学理论（及推导）

### 3.1 Laplace 变换的定义

**定义**：设 $f(t)$ 在 $t \geq 0$ 上有定义，若积分

$$F(s) = \mathcal{L}[f(t)](s) = \int_0^{+\infty} f(t)e^{-st}\,dt$$

在复平面 $s = \sigma + i\omega$ 的某个区域收敛，则称 $F(s)$ 为 $f(t)$ 的 **Laplace 变换**，$f(t)$ 为 $F(s)$ 的**逆 Laplace 变换**。

### 3.2 收敛域

**定理（收敛性）**：若存在常数 $M > 0$ 和 $\sigma_0 \geq 0$ 使得 $|f(t)| \leq Me^{\sigma_0 t}$（$t \geq 0$），则 $\mathcal{L}[f(t)]$ 在半平面 $\operatorname{Re}s > \sigma_0$ 内绝对一致收敛。

**证明**：当 $\operatorname{Re}s = \sigma > \sigma_0$ 时：

$$\int_0^{+\infty}|f(t)e^{-st}|\,dt = \int_0^{+\infty}|f(t)|e^{-\sigma t}\,dt \leq M\int_0^{+\infty}e^{-(\sigma-\sigma_0)t}\,dt = \frac{M}{\sigma-\sigma_0} < \infty$$

一致收敛性由 Weierstrass M-判别法保证。$\blacksquare$

### 3.3 基本性质

**（1）线性性**：

$$\mathcal{L}[af(t) + bg(t)] = aF(s) + bG(s)$$

**（2）微分性质**：

$$\mathcal{L}[f'(t)] = sF(s) - f(0^-)$$

**推导**：

$$\mathcal{L}[f'(t)] = \int_0^{+\infty} f'(t)e^{-st}\,dt = \left[f(t)e^{-st}\right]_0^{+\infty} + s\int_0^{+\infty} f(t)e^{-st}\,dt = -f(0^-) + sF(s)$$

（利用 $f(t)e^{-st} \to 0$ 当 $t \to +\infty$，因 $\operatorname{Re}s$ 足够大。）

**推广**：

$$\mathcal{L}[f^{(n)}(t)] = s^n F(s) - s^{n-1}f(0^-) - s^{n-2}f'(0^-) - \cdots - f^{(n-1)}(0^-)$$

$$= s^n F(s) - \sum_{k=0}^{n-1} s^{n-1-k}f^{(k)}(0^-)$$

**（3）积分性质**：

$$\mathcal{L}\left[\int_0^t f(\tau)\,d\tau\right] = \frac{F(s)}{s}$$

**推导**：令 $g(t) = \int_0^t f(\tau)\,d\tau$，则 $g'(t) = f(t)$，$g(0) = 0$。

$$\mathcal{L}[f(t)] = \mathcal{L}[g'(t)] = sG(s) - g(0) = sG(s)$$

故 $G(s) = F(s)/s$。

**（4）时移性质**（$t$-shifting）：

$$\mathcal{L}[f(t-t_0)\cdot u(t-t_0)] = e^{-st_0}F(s), \quad t_0 > 0$$

其中 $u(t)$ 为单位阶跃函数。

**推导**：

$$\mathcal{L}[f(t-t_0)u(t-t_0)] = \int_0^{+\infty} f(t-t_0)u(t-t_0)e^{-st}\,dt = \int_{t_0}^{+\infty} f(t-t_0)e^{-st}\,dt$$

令 $\tau = t - t_0$：$= \int_0^{+\infty} f(\tau)e^{-s(\tau+t_0)}\,d\tau = e^{-st_0}F(s)$。

**（5）频移性质**（$s$-shifting）：

$$\mathcal{L}[e^{at}f(t)] = F(s-a)$$

**推导**：

$$\mathcal{L}[e^{at}f(t)] = \int_0^{+\infty} e^{at}f(t)e^{-st}\,dt = \int_0^{+\infty} f(t)e^{-(s-a)t}\,dt = F(s-a)$$

**（6）尺度变换**：

$$\mathcal{L}[f(at)] = \frac{1}{a}F\left(\frac{s}{a}\right), \quad a > 0$$

**（7）卷积定理**：

$$\mathcal{L}[f(t) * g(t)] = F(s) \cdot G(s)$$

其中 $(f * g)(t) = \int_0^t f(\tau)g(t-\tau)\,d\tau$。

**推导**：

$$\mathcal{L}[f*g] = \int_0^{+\infty}\left[\int_0^t f(\tau)g(t-\tau)\,d\tau\right]e^{-st}\,dt$$

$$= \int_0^{+\infty}f(\tau)\left[\int_\tau^{+\infty}g(t-\tau)e^{-st}\,dt\right]d\tau$$

令 $u = t - \tau$：

$$= \int_0^{+\infty}f(\tau)\left[\int_0^{+\infty}g(u)e^{-s(u+\tau)}\,du\right]d\tau = \int_0^{+\infty}f(\tau)e^{-s\tau}G(s)\,d\tau = F(s)G(s)$$

### 3.4 初值定理与终值定理

**初值定理**：设 $\mathcal{L}[f(t)] = F(s)$，则：

$$f(0^+) = \lim_{s\to\infty}sF(s)$$

**推导**：

$$sF(s) - f(0^-) = \mathcal{L}[f'(t)] = \int_0^{+\infty}f'(t)e^{-st}\,dt$$

当 $s \to \infty$（沿实轴）：$e^{-st} \to 0$（$t > 0$），但 $\int_0^{\epsilon} f'(t)\,dt \approx f(\epsilon) - f(0^-)$。更严格地：

$$\lim_{s\to\infty}sF(s) = f(0^-) + \lim_{s\to\infty}\int_0^{+\infty}f'(t)e^{-st}\,dt = f(0^-) + 0 = f(0^-)$$

（在 $f$ 无冲激的条件下，$f(0^+) = f(0^-)$。）

**终值定理**：若 $sF(s)$ 的所有极点都在左半平面（$\operatorname{Re}s < 0$），则：

$$\lim_{t\to+\infty}f(t) = \lim_{s\to 0}sF(s)$$

**推导**：

$$\lim_{s\to 0}\left[sF(s) - f(0^-)\right] = \lim_{s\to 0}\int_0^{+\infty}f'(t)e^{-st}\,dt = \int_0^{+\infty}f'(t)\,dt = f(+\infty) - f(0^-)$$

故 $\lim_{s\to 0}sF(s) = f(+\infty)$。

### 3.5 逆 Laplace 变换

**（1）留数法（Bromwich 积分）**

**Mellin 逆变换公式**：

$$f(t) = \frac{1}{2\pi i}\int_{\sigma-i\infty}^{\sigma+i\infty} F(s)e^{st}\,ds, \quad t > 0$$

其中积分路径 $\operatorname{Re}s = \sigma$ 位于 $F(s)$ 所有奇点的右侧。

**用留数定理计算**：当 $F(s)$ 为有理函数时，选取适当的围道（Bromwich 围道），利用 Jordan 引理和留数定理：

$$f(t) = \sum_{k}\operatorname{Res}\left[F(s)e^{st}, s_k\right]$$

其中求和遍及 $F(s)$ 在 Bromwich 线左侧的所有极点 $s_k$。

**（2）部分分式展开法**

设 $F(s) = \frac{P(s)}{Q(s)}$ 为有理函数（$\deg P < \deg Q$），则：

$$F(s) = \sum_{k}\left[\frac{A_k}{s-s_k} + \frac{B_k}{(s-s_k)^2} + \cdots\right]$$

然后逐项逆变换，利用 $\mathcal{L}^{-1}\left[\frac{1}{(s-a)^n}\right] = \frac{t^{n-1}e^{at}}{(n-1)!}$。

**（3）查表法**

对于常见函数和组合，通过查 Laplace 变换表结合性质（时移、频移等）求逆。

### 3.6 常用 Laplace 变换对

| $f(t)$ ($t \geq 0$) | $F(s)$ | ROC |
|:---:|:---:|:---:|
| $\delta(t)$ | $1$ | $\forall s$ |
| $u(t)$（单位阶跃） | $\frac{1}{s}$ | $\operatorname{Re}s > 0$ |
| $t^n$（$n \in \mathbb{N}$） | $\frac{n!}{s^{n+1}}$ | $\operatorname{Re}s > 0$ |
| $e^{at}$ | $\frac{1}{s-a}$ | $\operatorname{Re}s > \operatorname{Re}a$ |
| $t^n e^{at}$ | $\frac{n!}{(s-a)^{n+1}}$ | $\operatorname{Re}s > \operatorname{Re}a$ |
| $\cos(\omega t)$ | $\frac{s}{s^2+\omega^2}$ | $\operatorname{Re}s > 0$ |
| $\sin(\omega t)$ | $\frac{\omega}{s^2+\omega^2}$ | $\operatorname{Re}s > 0$ |
| $e^{at}\cos(\omega t)$ | $\frac{s-a}{(s-a)^2+\omega^2}$ | $\operatorname{Re}s > a$ |
| $e^{at}\sin(\omega t)$ | $\frac{\omega}{(s-a)^2+\omega^2}$ | $\operatorname{Re}s > a$ |
| $t\cos(\omega t)$ | $\frac{s^2-\omega^2}{(s^2+\omega^2)^2}$ | $\operatorname{Re}s > 0$ |

### 3.7 求解常微分方程的步骤

**例**：求解 $y''(t) + 3y'(t) + 2y(t) = e^{-t}$，$y(0) = 0$，$y'(0) = 1$。

**步骤一**：对两边取 Laplace 变换：

$$s^2 Y(s) - sy(0) - y'(0) + 3[sY(s) - y(0)] + 2Y(s) = \frac{1}{s+1}$$

$$(s^2 + 3s + 2)Y(s) - 1 = \frac{1}{s+1}$$

**步骤二**：求解 $Y(s)$：

$$Y(s) = \frac{1}{s^2+3s+2} + \frac{1}{(s+1)(s^2+3s+2)} = \frac{1}{(s+1)(s+2)} + \frac{1}{(s+1)^2(s+2)}$$

**步骤三**：部分分式展开：

$$Y(s) = \frac{1}{s+1} - \frac{1}{s+2} + \frac{1}{(s+1)^2} - \frac{1}{s+1} + \frac{1}{s+2} = \frac{1}{(s+1)^2}$$

**步骤四**：逆变换：

$$y(t) = \mathcal{L}^{-1}\left[\frac{1}{(s+1)^2}\right] = te^{-t}$$
