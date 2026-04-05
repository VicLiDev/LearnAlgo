# 分析学（Analysis）

以极限、连续、微分、积分、收敛为核心概念的学科，是微积分的延伸与深化。

## 子学科

| 学科     | 英文名                 | 核心内容                                     | 难度  |
|----------|------------------------|----------------------------------------------|-------|
| 微积分   | Calculus               | 极限、导数、积分、级数                       | ★☆☆☆☆ |
| 实分析   | Real Analysis          | 实数完备性、测度论、Lebesgue积分、收敛性     | ★★★★☆ |
| 复分析   | Complex Analysis       | 复变函数、解析函数、Cauchy积分定理、留数定理 | ★★★★☆ |
| 泛函分析 | Functional Analysis    | 赋范空间、Banach空间、Hilbert空间、算子理论  | ★★★★★ |
| 调和分析 | Harmonic Analysis      | Fourier级数、Fourier变换、小波分析           | ★★★★☆ |
| 微分方程 | Differential Equations | 常微分方程(ODE)、偏微分方程(PDE)、稳定性理论 | ★★★☆☆ |
| 变分法   | Calculus of Variations | 泛函极值、Euler-Lagrange方程、最速降线       | ★★★★☆ |

## 适用场景

信号处理（Fourier变换）、物理场建模（PDE）、最优化理论、量子力学算子。

## 核心公式

- Fourier变换：$\hat{f}(\xi) = \int_{-\infty}^{+\infty} f(x) e^{-2\pi i x \xi} \, dx$
- Cauchy积分公式：$f(z_0) = \frac{1}{2\pi i} \oint_\gamma \frac{f(z)}{z - z_0} \, dz$
- Euler-Lagrange方程：$\frac{\partial L}{\partial q} - \frac{d}{dt}\frac{\partial L}{\partial \dot{q}} = 0$

## 参考教材

- 《Real Analysis》 — Royden
- 《Complex Analysis》 — Ahlfors
