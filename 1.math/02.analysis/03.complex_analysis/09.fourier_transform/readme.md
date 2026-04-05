# 第九章 Fourier 变换

## 一、几何意义

### 1.1 Fourier 级数的几何理解

Fourier 级数将周期函数分解为不同频率的**正弦波和余弦波的叠加**。在复数形式下：

$$f(x) = \sum_{n=-\infty}^{+\infty} c_n e^{in\omega_0 x}$$

其中 $c_n$ 是第 $n$ 次谐波的复振幅，$\omega_0 = \frac{2\pi}{T}$ 是基频。

**几何意义**：每个 $e^{in\omega_0 x}$ 对应复平面上单位圆的一个匀速旋转，角速度为 $n\omega_0$。Fourier 系数 $c_n$ 表示频率为 $n\omega_0$ 的分量在信号中的"强度"和"相位"。频谱图 $|c_n|$ vs $n$ 展示了信号的频率组成。

### 1.2 Fourier 变换的几何理解

Fourier 变换将时域信号 $f(t)$ 转换为频域表示 $\hat{f}(\omega)$：

$$\hat{f}(\omega) = \int_{-\infty}^{+\infty} f(t)e^{-i\omega t}\,dt$$

**几何意义**：
- Fourier 变换计算 $f(t)$ 与每个频率 $\omega$ 的复指数 $e^{i\omega t}$ 之间的**相关性**。
- $e^{-i\omega t}$ 在复平面上以角速度 $\omega$ 旋转。积分相当于对这个旋转信号做"加权平均"，度量 $f(t)$ 中含有多少该频率的成分。
- $|\hat{f}(\omega)|$ 表示频率为 $\omega$ 的分量的强度（振幅谱）。
- $\arg\hat{f}(\omega)$ 表示该分量的相位（相位谱）。

### 1.3 时频对偶关系

Fourier 变换揭示了对偶性（Duality）：
- **时域上的窄 $\leftrightarrow$ 频域上的宽**。
- **时域上的周期性 $\leftrightarrow$ 频域上的离散性**，反之亦然。
- 时域上的平移 $\leftrightarrow$ 频域上的相位旋转。

这一对偶性的极端体现是 **Heisenberg 不确定性原理**：

$$\Delta t \cdot \Delta \omega \geq \frac{1}{2}$$

一个信号不可能同时在时域和频域都高度集中。

### 1.4 卷积的几何意义

卷积 $(f * g)(t) = \int_{-\infty}^{+\infty} f(\tau)g(t-\tau)\,d\tau$ 的几何意义：

- 将 $g(\tau)$ **翻转**得到 $g(-\tau)$。
- 将 $g(-\tau)$ **平移** $t$ 个单位得到 $g(t-\tau)$。
- 将 $f(\tau)$ 和 $g(t-\tau)$ **逐点相乘**并积分。

**卷积定理**：$\widehat{f*g} = \hat{f} \cdot \hat{g}$ ——时域的卷积等于频域的乘积，反之亦然。这一性质是滤波理论的基础。

---

## 二、应用场景

### 2.1 信号处理

- **频谱分析**：分析信号的频率成分，识别周期性和噪声。
- **滤波**：设计低通、高通、带通滤波器，去除不需要的频率成分。
- **调制与解调**：通信中通过频移实现信号的传输（AM/FM）。
- **压缩**：JPEG、MP3 等格式利用频域稀疏性实现数据压缩。

### 2.2 图像处理

二维 Fourier 变换用于图像的频域分析：
- **低频**对应图像的平滑区域（整体亮度、色调）。
- **高频**对应图像的边缘和细节。
- 频域滤波可用于去噪、锐化、边缘检测。

### 2.3 偏微分方程

Fourier 变换将偏微分方程化为常微分方程（或代数方程）：
- **热传导方程**：$\frac{\partial u}{\partial t} = k\frac{\partial^2 u}{\partial x^2}$ 化为 $\frac{d\hat{u}}{dt} = -k\omega^2\hat{u}$。
- **波动方程**：类似地化简。
- **Schrodinger 方程**：量子力学中的基本方程。

### 2.4 概率论

特征函数（characteristic function）$\varphi_X(\omega) = \mathbb{E}[e^{i\omega X}]$ 本质上是概率密度函数的 Fourier 变换。独立随机变量之和的特征函数等于各特征函数之积。

### 2.5 光学

Fraunhofer 衍射图样是光阑函数的 Fourier 变换。透镜的聚焦作用等价于进行 Fourier 变换。

---

## 三、数学理论（及推导）

### 3.1 Fourier 级数（复数形式）

设 $f(x)$ 是以 $T$ 为周期的函数，$\omega_0 = \frac{2\pi}{T}$。

**复数形式的 Fourier 级数**：

$$f(x) = \sum_{n=-\infty}^{+\infty} c_n e^{in\omega_0 x}$$

**Fourier 系数**：

$$c_n = \frac{1}{T}\int_0^T f(x)e^{-in\omega_0 x}\,dx, \quad n = 0, \pm 1, \pm 2, \ldots$$

**与实数形式的关系**：

设 $f(x) = \frac{a_0}{2} + \sum_{n=1}^{\infty}(a_n\cos n\omega_0 x + b_n\sin n\omega_0 x)$，则：

$$c_0 = \frac{a_0}{2}, \quad c_n = \frac{a_n - ib_n}{2}, \quad c_{-n} = \frac{a_n + ib_n}{2} = \bar{c}_n \quad (n \geq 1)$$

**正交性**：

$$\frac{1}{T}\int_0^T e^{in\omega_0 x}e^{-im\omega_0 x}\,dx = \delta_{mn} = \begin{cases} 1 & m = n \\ 0 & m \neq n \end{cases}$$

**推导 Fourier 系数公式**：

$$\frac{1}{T}\int_0^T f(x)e^{-im\omega_0 x}\,dx = \frac{1}{T}\int_0^T \sum_{n=-\infty}^{+\infty} c_n e^{i(n-m)\omega_0 x}\,dx = \sum_{n=-\infty}^{+\infty} c_n \cdot \delta_{mn} = c_m$$

### 3.2 Fourier 变换的定义

**定义**：设 $f(t) \in L^1(\mathbb{R})$（绝对可积），则其 **Fourier 变换**（FT）为：

$$\hat{f}(\omega) = \mathcal{F}[f(t)](\omega) = \int_{-\infty}^{+\infty} f(t)e^{-i\omega t}\,dt$$

**逆 Fourier 变换**（IFT）：

$$f(t) = \mathcal{F}^{-1}[\hat{f}(\omega)](t) = \frac{1}{2\pi}\int_{-\infty}^{+\infty} \hat{f}(\omega)e^{i\omega t}\,d\omega$$

**注**：不同教材中的 Fourier 变换定义可能差一个常数因子（如 $\frac{1}{\sqrt{2\pi}}$ 的对称形式），以上采用工程中常用的非对称定义。

### 3.3 Fourier 变换的基本性质

设 $\hat{f}(\omega) = \mathcal{F}[f(t)]$，$\hat{g}(\omega) = \mathcal{F}[g(t)]$。

**（1）线性性**：

$$\mathcal{F}[af(t) + bg(t)] = a\hat{f}(\omega) + b\hat{g}(\omega)$$

**（2）时移性质**（Time shifting）：

$$\mathcal{F}[f(t-t_0)] = e^{-i\omega t_0}\hat{f}(\omega)$$

**推导**：

$$\mathcal{F}[f(t-t_0)] = \int_{-\infty}^{+\infty} f(t-t_0)e^{-i\omega t}\,dt = \int_{-\infty}^{+\infty} f(u)e^{-i\omega(u+t_0)}\,du = e^{-i\omega t_0}\hat{f}(\omega)$$

**几何意义**：时域平移对应频域的相位旋转，振幅谱不变。

**（3）频移性质**（Frequency shifting / 调制定理）：

$$\mathcal{F}[e^{i\omega_0 t}f(t)] = \hat{f}(\omega - \omega_0)$$

**推导**：

$$\mathcal{F}[e^{i\omega_0 t}f(t)] = \int_{-\infty}^{+\infty} f(t)e^{i\omega_0 t}e^{-i\omega t}\,dt = \int_{-\infty}^{+\infty} f(t)e^{-i(\omega-\omega_0)t}\,dt = \hat{f}(\omega - \omega_0)$$

**（4）尺度变换性质**（Scaling）：

$$\mathcal{F}[f(at)] = \frac{1}{|a|}\hat{f}\left(\frac{\omega}{a}\right), \quad a \neq 0$$

**推导**：$a > 0$ 时，$\mathcal{F}[f(at)] = \int f(at)e^{-i\omega t}\,dt = \frac{1}{a}\int f(u)e^{-i(\omega/a)u}\,du = \frac{1}{a}\hat{f}(\omega/a)$。

**（5）微分性质**：

$$\mathcal{F}[f'(t)] = i\omega\hat{f}(\omega)$$

$$\mathcal{F}[f^{(n)}(t)] = (i\omega)^n\hat{f}(\omega)$$

**推导**（需 $f(t) \to 0$ 当 $t \to \pm\infty$）：

$$\mathcal{F}[f'(t)] = \int_{-\infty}^{+\infty} f'(t)e^{-i\omega t}\,dt = \left[f(t)e^{-i\omega t}\right]_{-\infty}^{+\infty} + i\omega\int_{-\infty}^{+\infty} f(t)e^{-i\omega t}\,dt = i\omega\hat{f}(\omega)$$

**意义**：时域的微分对应频域乘以 $i\omega$。这使得常微分方程化为代数方程。

**（6）积分性质**：

$$\mathcal{F}\left[\int_{-\infty}^{t} f(\tau)\,d\tau\right] = \frac{1}{i\omega}\hat{f}(\omega) + \pi\hat{f}(0)\delta(\omega)$$

**（7）卷积定理**（Convolution theorem）：

$$\mathcal{F}[f * g] = \hat{f}(\omega) \cdot \hat{g}(\omega)$$

$$\mathcal{F}[f(t) \cdot g(t)] = \frac{1}{2\pi}(\hat{f} * \hat{g})(\omega)$$

**推导**（第一个公式）：

$$\mathcal{F}[f*g] = \int\left[\int f(\tau)g(t-\tau)\,d\tau\right]e^{-i\omega t}\,dt = \int f(\tau)\left[\int g(t-\tau)e^{-i\omega t}\,dt\right]d\tau$$

$$= \int f(\tau)e^{-i\omega\tau}\hat{g}(\omega)\,d\tau = \hat{f}(\omega)\hat{g}(\omega)$$

### 3.4 Parseval 定理

**定理（Parseval）**：

$$\int_{-\infty}^{+\infty} |f(t)|^2\,dt = \frac{1}{2\pi}\int_{-\infty}^{+\infty} |\hat{f}(\omega)|^2\,d\omega$$

**物理意义**：信号在时域中的总能量等于其在频域中的总能量（能量守恒）。

**推导**（形式推导）：

$$\int |f(t)|^2\,dt = \int f(t)\overline{f(t)}\,dt = \int f(t)\left[\frac{1}{2\pi}\int \overline{\hat{f}(\omega)}e^{-i\omega t}\,d\omega\right]dt$$

$$= \frac{1}{2\pi}\int \overline{\hat{f}(\omega)}\left[\int f(t)e^{-i\omega t}\,dt\right]d\omega = \frac{1}{2\pi}\int \overline{\hat{f}(\omega)}\hat{f}(\omega)\,d\omega = \frac{1}{2\pi}\int |\hat{f}(\omega)|^2\,d\omega$$

**推广（Plancherel 定理）**：Fourier 变换是 $L^2(\mathbb{R})$ 上的等距同构（酉算子）。

### 3.5 常用 Fourier 变换对

| $f(t)$ | $\hat{f}(\omega)$ | 条件 |
|:---:|:---:|:---:|
| $\delta(t)$ | $1$ | — |
| $1$ | $2\pi\delta(\omega)$ | — |
| $e^{iat}$ | $2\pi\delta(\omega - a)$ | — |
| $\cos(at)$ | $\pi[\delta(\omega-a)+\delta(\omega+a)]$ | — |
| $\sin(at)$ | $\frac{\pi}{i}[\delta(\omega-a)-\delta(\omega+a)]$ | — |
| $e^{-a|t|}$ ($a>0$) | $\frac{2a}{a^2+\omega^2}$ | — |
| $e^{-at^2}$ ($a>0$) | $\sqrt{\frac{\pi}{a}}e^{-\omega^2/(4a)}$ | — |
| $\operatorname{rect}(t)$（矩形脉冲） | $\frac{\sin\omega}{\omega} = \operatorname{sinc}\left(\frac{\omega}{2\pi}\right)$ | — |
| $\operatorname{sinc}(t)$ | $\pi\operatorname{rect}\left(\frac{\omega}{2}\right)$ | — |

### 3.6 快速 Fourier 变换（FFT）

**问题**：直接计算离散 Fourier 变换（DFT）

$$X_k = \sum_{n=0}^{N-1} x_n e^{-i2\pi kn/N}, \quad k = 0, 1, \ldots, N-1$$

需要 $O(N^2)$ 次复数乘法。

**FFT 思想**（Cooley-Tukey 算法）：

设 $N = 2^m$，将求和按 $n$ 的奇偶性分组：

$$X_k = \sum_{r=0}^{N/2-1} x_{2r} e^{-i2\pi k(2r)/N} + \sum_{r=0}^{N/2-1} x_{2r+1} e^{-i2\pi k(2r+1)/N}$$

$$= \underbrace{\sum_{r=0}^{N/2-1} x_{2r} e^{-i2\pi kr/(N/2)}}_{E_k} + e^{-i2\pi k/N}\underbrace{\sum_{r=0}^{N/2-1} x_{2r+1} e^{-i2\pi kr/(N/2)}}_{O_k}$$

$E_k$ 和 $O_k$ 分别是长度为 $N/2$ 的 DFT。利用 $e^{-i2\pi k/N}$ 的周期性（$W_N = e^{-i2\pi/N}$，称为**旋转因子**）：

$$X_{k+N/2} = E_k - W_N^k O_k$$

因此一次分解将 $N$ 点 DFT 化为两个 $N/2$ 点 DFT 加 $N/2$ 次复数乘法。递归地进行，直到长度为 1。

**复杂度**：$T(N) = 2T(N/2) + O(N) = O(N\log N)$。

**意义**：FFT 将计算复杂度从 $O(N^2)$ 降到 $O(N\log N)$，是 20 世纪最重要的数值算法之一，广泛应用于信号处理、图像处理、科学计算等领域。
