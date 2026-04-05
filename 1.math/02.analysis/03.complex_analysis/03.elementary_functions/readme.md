# 第三章 初等解析函数

## 一、几何意义

### 1.1 指数函数 $w = e^z$ 的映射

$w = e^z = e^x(\cos y + i\sin y)$ 的映射性质：

- **水平线** $y = c$：映射为射线 $\arg w = c$（从原点出发的角度为 $c$ 的射线）。
- **竖直线** $x = c$：映射为圆弧 $|w| = e^c$（以原点为心、$e^c$ 为半径的圆）。
- **带形区域** $a < \operatorname{Im}z < b$（宽度 $< 2\pi$）：映射为角形区域 $a < \arg w < b$。
- **周期性**：$e^{z + 2\pi i} = e^z$，基本周期为 $2\pi i$。

**几何直观**：指数函数将 $z$ 平面上的矩形网格映射为 $w$ 平面上的极坐标网格——水平线变为射线，竖直线变为同心圆。

### 1.2 对数函数 $w = \ln z$ 的映射

对数函数是指数函数的逆映射，其多值性在几何上体现为：

- 将射线（从原点出发）映射为水平线。
- 将同心圆映射为竖直线。
- 将绕原点一周的路径映射为一条长度为 $2\pi i$ 的竖直段。

**支割线**：选择一条从原点到无穷远的曲线作为**支割线**（branch cut），禁止路径跨越该曲线，即可得到对数函数的单值分支。常见选择：沿负实轴割开。

### 1.3 幂函数 $w = z^\alpha$ 的映射

设 $\alpha = a + ib$。

- 当 $\alpha$ 为正整数 $n$ 时：$z^n$ 将角度放大 $n$ 倍（角域扩展为 $n$ 倍），模变为 $|z|^n$。
- 当 $\alpha = 1/n$（$n \in \mathbb{N}^+$）时：$z^{1/n}$ 将角度缩小 $n$ 倍，产生 $n$ 个值（$n$ 值性）。
- **一般 $\alpha$**：$w = z^\alpha = e^{\alpha \ln z}$，通常是多值函数。

**例**：$w = z^{1/2}$ 将全平面映射为上半平面（取主分支），将角度 $[0, 2\pi)$ 映射为 $[0, \pi)$。

### 1.4 三角函数的几何意义

$w = \sin z = \sin(x+iy) = \sin x \cosh y + i\cos x \sinh y$

- 当 $z$ 为纯实数（$y=0$）时，退化为实 $\sin$ 函数。
- 当 $z$ 为纯虚数（$x=0$）时，$\sin(iy) = i\sinh y$，退化为双曲正弦的纯虚数倍。
- $\sin z$ 将带形区域 $-\pi/2 < \operatorname{Re}z < \pi/2$ 映射为复平面的某个区域。

### 1.5 双曲函数的几何意义

$$\sinh z = \frac{e^z - e^{-z}}{2}, \quad \cosh z = \frac{e^z + e^{-z}}{2}$$

与三角函数通过 $\sinh(iz) = i\sin z$，$\cosh(iz) = \cos z$ 相联系。双曲函数将矩形区域映射为椭圆。

---

## 二、应用场景

### 2.1 信号处理中的复指数

复指数 $e^{i\omega t}$ 是信号处理中最基本的信号形式。任何周期信号都可以分解为复指数的线性组合（Fourier 级数）。离散信号处理中，$z = e^{i\omega}$ 将单位圆上的点映射为频率。

### 2.2 流体力学中的复势

复势函数 $w(z) = \phi + i\psi$ 中，指数函数和对数函数经常出现：
- $w = \ln z$ 描述源/汇。
- $w = \frac{1}{z}$ 描述偶极子。
- $w = z + e^{iz}$ 描述波的运动。

### 2.3 电磁学中的 Joukowski 变换

Joukowski 变换 $w = z + \frac{1}{z}$（与幂函数和逆函数的组合有关）是空气动力学中的重要映射，将圆映射为翼型（机翼截面），用于翼型绕流的理论分析。

### 2.4 控制理论中的传递函数

指数函数 $e^{st}$ 是线性系统分析的基础。Laplace 变换将时域中的微分方程转化为 $s$ 域中的代数方程。

### 2.5 数论与分析

Riemann zeta 函数 $\zeta(s) = \sum_{n=1}^{\infty} \frac{1}{n^s}$ 涉及幂函数的解析延拓。对数函数在素数分布理论中起核心作用。

---

## 三、数学理论（及推导）

### 3.1 指数函数

**定义**：由幂级数定义：

$$e^z = \sum_{n=0}^{\infty} \frac{z^n}{n!} = 1 + z + \frac{z^2}{2!} + \frac{z^3}{3!} + \cdots$$

**基本性质**：

1. **Euler 公式**：
$$e^{x+iy} = e^x(\cos y + i\sin y)$$

**推导**：

$$e^{iy} = \sum_{n=0}^{\infty} \frac{(iy)^n}{n!} = \sum_{k=0}^{\infty} \frac{i^{2k} y^{2k}}{(2k)!} + \sum_{k=0}^{\infty} \frac{i^{2k+1} y^{2k+1}}{(2k+1)!}$$

$$= \sum_{k=0}^{\infty} \frac{(-1)^k y^{2k}}{(2k)!} + i\sum_{k=0}^{\infty} \frac{(-1)^k y^{2k+1}}{(2k+1)!} = \cos y + i\sin y$$

2. **乘法公式**：$e^{z_1} e^{z_2} = e^{z_1 + z_2}$

**推导**：利用级数的 Cauchy 乘积：

$$e^{z_1} e^{z_2} = \sum_{m=0}^{\infty}\frac{z_1^m}{m!}\sum_{n=0}^{\infty}\frac{z_2^n}{n!} = \sum_{k=0}^{\infty}\sum_{m+n=k}\frac{z_1^m z_2^n}{m!\,n!} = \sum_{k=0}^{\infty}\frac{1}{k!}\sum_{m=0}^{k}\binom{k}{m}z_1^m z_2^{k-m}$$

$$= \sum_{k=0}^{\infty}\frac{(z_1 + z_2)^k}{k!} = e^{z_1 + z_2}$$

3. **周期性**：$e^{z + 2\pi i} = e^z$

由 $e^{2\pi i} = \cos(2\pi) + i\sin(2\pi) = 1$ 即得。

4. **$|e^z| = e^x$，$\arg(e^z) = y + 2k\pi$**

5. **$e^z \neq 0$ 对一切 $z \in \mathbb{C}$ 成立**（无零点性）。

6. **解析性**：$e^z$ 在全平面解析，$(e^z)' = e^z$。

### 3.2 对数函数

**定义**：对数函数定义为指数函数的反函数。若 $e^w = z$（$z \neq 0$），则：

$$w = \operatorname{Ln} z = \ln|z| + i\arg z$$

其中 $\arg z$ 是多值的，$\arg z = \operatorname{Arg} z + 2k\pi$（$k \in \mathbb{Z}$），故：

$$\operatorname{Ln} z = \ln|z| + i(\operatorname{Arg} z + 2k\pi), \quad k \in \mathbb{Z}$$

**主值**（Principal value）：

$$\ln z = \ln|z| + i\operatorname{Arg} z, \quad \operatorname{Arg} z \in (-\pi, \pi]$$

**多值性分析**：

- $\operatorname{Ln} z$ 是无穷多值函数，各分支相差 $2\pi i$ 的整数倍。
- 在 $z = 0$ 处无定义，$z = 0$ 是**支点**（branch point）。
- 在 $\infty$ 处也是支点。

**支割线**（Branch cut）：

为获得单值解析分支，从支点 $z = 0$ 出发，沿某条曲线（通常取负实轴）将复平面割开，禁止路径跨越。

设支割线为负实轴，则主分支 $\ln z = \ln|z| + i\operatorname{Arg} z$ 在 $\mathbb{C} \setminus (-\infty, 0]$ 上解析。

**性质**（在单值分支上）：

$$\operatorname{Ln}(z_1 z_2) = \operatorname{Ln} z_1 + \operatorname{Ln} z_2 \quad (\text{集合等式，考虑多值性})$$

$$(\ln z)' = \frac{1}{z}$$

**推导**：设 $w = \ln z$，则 $z = e^w$，$\frac{dw}{dz} = \frac{1}{e^w} = \frac{1}{z}$。

**一般幂函数**：$z^\alpha = e^{\alpha \operatorname{Ln} z}$

- 当 $\alpha \in \mathbb{Z}$ 时，$z^\alpha$ 是单值的。
- 当 $\alpha \in \mathbb{Q} \setminus \mathbb{Z}$ 时，$z^\alpha$ 是有限多值的。
- 当 $\alpha \in \mathbb{C} \setminus \mathbb{Q}$ 时，$z^\alpha$ 是无穷多值的。

### 3.3 三角函数

**定义**：

$$\sin z = \frac{e^{iz} - e^{-iz}}{2i}, \quad \cos z = \frac{e^{iz} + e^{-iz}}{2}$$

$$\tan z = \frac{\sin z}{\cos z}, \quad \cot z = \frac{\cos z}{\sin z}$$

$$\sec z = \frac{1}{\cos z}, \quad \csc z = \frac{1}{\sin z}$$

**基本性质**：

1. **与实三角函数一致**：当 $z \in \mathbb{R}$ 时，退化为实三角函数。

2. **周期性**：$\sin z$ 和 $\cos z$ 的基本周期为 $2\pi$；$\tan z$ 和 $\cot z$ 的基本周期为 $\pi$。

3. **奇偶性**：$\sin z$ 为奇函数，$\cos z$ 为偶函数。

4. **Pythagoras 恒等式**：$\sin^2 z + \cos^2 z = 1$

**证明**：
$$\sin^2 z + \cos^2 z = \left(\frac{e^{iz}-e^{-iz}}{2i}\right)^2 + \left(\frac{e^{iz}+e^{-iz}}{2}\right)^2$$

$$= \frac{e^{2iz} - 2 + e^{-2iz}}{-4} + \frac{e^{2iz} + 2 + e^{-2iz}}{4} = \frac{-e^{2iz}+2-e^{-2iz}+e^{2iz}+2+e^{-2iz}}{4} = \frac{4}{4} = 1$$

5. **无界性**（与实函数的关键区别）：

$$\sin(x+iy) = \sin x \cosh y + i\cos x \sinh y$$

当 $y \to \infty$ 时，$|\sin z| \sim \frac{1}{2}e^{|y|} \to \infty$。因此 **$\sin z$ 和 $\cos z$ 在全平面上是无界函数**。

6. **零点**：$\sin z = 0 \iff z = k\pi$（$k \in \mathbb{Z}$）；$\cos z = 0 \iff z = \frac{\pi}{2} + k\pi$（$k \in \mathbb{Z}$）。

7. **解析性**：$\sin z$ 和 $\cos z$ 在全平面解析；$\tan z$ 在 $\cos z = 0$ 处有极点。

8. **导数**：$(\sin z)' = \cos z$，$(\cos z)' = -\sin z$

**推导**：
$$(\sin z)' = \left(\frac{e^{iz}-e^{-iz}}{2i}\right)' = \frac{ie^{iz}+ie^{-iz}}{2i} = \frac{e^{iz}+e^{-iz}}{2} = \cos z$$

### 3.4 双曲函数

**定义**：

$$\sinh z = \frac{e^z - e^{-z}}{2}, \quad \cosh z = \frac{e^z + e^{-z}}{2}$$

$$\tanh z = \frac{\sinh z}{\cosh z}, \quad \coth z = \frac{\cosh z}{\sinh z}$$

**与三角函数的关系**：

$$\sinh z = -i\sin(iz), \quad \cosh z = \cos(iz)$$

$$\sin z = -i\sinh(iz), \quad \cos z = \cosh(iz)$$

**基本性质**：

1. $\cosh^2 z - \sinh^2 z = 1$
2. $\sinh z$ 为奇函数，$\cosh z$ 为偶函数。
3. $\sinh z$ 的零点在 $z = k\pi i$；$\cosh z$ 的零点在 $z = \frac{\pi}{2}i + k\pi i$。
4. $(\sinh z)' = \cosh z$，$(\cosh z)' = \sinh z$

### 3.5 反三角函数

**定义**：反三角函数通过对数函数来定义。

**反正弦函数**：

$$w = \arcsin z \iff z = \sin w = \frac{e^{iw} - e^{-iw}}{2i}$$

令 $t = e^{iw}$，则 $2iz = t - \frac{1}{t}$，即 $t^2 - 2izt - 1 = 0$：

$$t = iz \pm \sqrt{1 - z^2}$$

$$\arcsin z = -i\operatorname{Ln}(iz + \sqrt{1-z^2})$$

**反余弦函数**：

$$\arccos z = -i\operatorname{Ln}\left(z + \sqrt{z^2 - 1}\right)$$

**推导**：$z = \cos w = \frac{e^{iw}+e^{-iw}}{2}$，令 $t = e^{iw}$，$2z = t + \frac{1}{t}$，$t^2 - 2zt + 1 = 0$：

$$t = z \pm \sqrt{z^2 - 1}$$

$$w = -i\operatorname{Ln}(z + \sqrt{z^2 - 1})$$

**反正切函数**：

$$\arctan z = \frac{1}{2i}\operatorname{Ln}\frac{1+iz}{1-iz}$$

**推导**：$z = \tan w = \frac{\sin w}{\cos w} = \frac{e^{iw}-e^{-iw}}{i(e^{iw}+e^{-iw})}$，化简得 $\frac{1+iz}{1-iz} = e^{2iw}$，故 $w = \frac{1}{2i}\operatorname{Ln}\frac{1+iz}{1-iz}$。

### 3.6 初等函数的解析性总结

| 函数 | 解析区域 | 奇点 |
|:---:|:---:|:---:|
| $e^z$ | $\mathbb{C}$ | $\infty$（本性奇点） |
| $\operatorname{Ln} z$ | $\mathbb{C}\setminus\text{支割线}$ | $0, \infty$（支点） |
| $z^\alpha$ | $\mathbb{C}\setminus\text{支割线}$ | $0, \infty$（支点，$\alpha \notin \mathbb{Z}$） |
| $\sin z, \cos z$ | $\mathbb{C}$ | $\infty$（本性奇点） |
| $\tan z$ | $\mathbb{C}\setminus\{\frac{\pi}{2}+k\pi\}$ | 极点 |
| $\sinh z, \cosh z$ | $\mathbb{C}$ | $\infty$（本性奇点） |
| $\arcsin z$ | 割去支割线后 | 支点 |
