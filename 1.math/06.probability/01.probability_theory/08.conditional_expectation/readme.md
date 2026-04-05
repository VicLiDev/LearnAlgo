# 第八章 条件期望

## 1. 几何意义

### 1.1 条件期望的基本直觉

条件期望 $E[X | Y = y]$ 是在已知 $Y = y$ 的条件下，$X$ 的"最佳预测"或"平均估计值"。可以从以下角度理解：

- **加权平均**：在离散情形下，$E[X | Y = y] = \sum_x x \cdot P(X = x | Y = y)$，就是将条件概率作为权重对 $X$ 的可能取值做加权平均。

- **回归函数**：$g(y) = E[X | Y = y]$ 是 $y$ 的函数，称为 $X$ 关于 $Y$ 的**回归函数**。在统计学中，$g(Y)$ 是已知 $Y$ 时对 $X$ 的最优均方误差预测。

### 1.2 条件期望的几何意义：正交投影

条件期望 $E[X | \mathcal{G}]$ 最重要的几何意义是：它是 $X$ 在子空间（$\mathcal{G}$-可测函数构成的子空间）上的**正交投影**。

具体来说，在 $L^2(\Omega, \mathcal{F}, P)$ 空间中：

- **$L^2(\Omega, \mathcal{F}, P)$**：所有平方可积的随机变量构成一个 Hilbert 空间，内积定义为 $\langle X, Y \rangle = E[XY]$。

- **$L^2(\Omega, \mathcal{G}, P)$**：所有 $\mathcal{G}$-可测且平方可积的随机变量构成 $L^2(\Omega, \mathcal{F}, P)$ 的一个**闭子空间**。

- **正交投影定理**：$E[X | \mathcal{G}]$ 是 $X$ 在 $L^2(\Omega, \mathcal{G}, P)$ 上的唯一正交投影，即：
  1. $E[X | \mathcal{G}] \in L^2(\Omega, \mathcal{G}, P)$（投影在子空间内）；
  2. $X - E[X | \mathcal{G}] \perp L^2(\Omega, \mathcal{G}, P)$（残差与子空间正交）。

这个几何视角极其重要，它解释了：
- **为什么条件期望是"最优预测"**：正交投影是最小化距离的元素，即 $E[X|\mathcal{G}]$ 使得 $E[(X - Z)^2]$ 在所有 $\mathcal{G}$-可测的 $Z$ 中取最小值。
- **为什么 $\langle X - E[X|\mathcal{G}], Z \rangle = 0$**：残差与所有"已知信息"正交。

### 1.3 全期望公式的几何解释

全期望公式 $E[X] = E[E[X|Y]]$ 的几何意义可以理解为：先在"切片"（条件）内求投影，再对切片取平均，等于直接投影。这类似于"投影到低维子空间可以先投影到中间子空间"。

### 1.4 鞅的几何直觉

鞅（Martingale）$E[X_n | \mathcal{F}_{n-1}] = X_{n-1}$ 的几何意义是：$X_n$ 在 $\mathcal{F}_{n-1}$-可测函数子空间上的投影恰好是 $X_{n-1}$。也就是说，$X_{n-1}$ 已经包含了所有可用信息的"最优预测"，没有系统性的偏差（向上或向下）。

可以想象为一个"公平游戏"：已知过去的信息，对下一时刻的期望预测恰好等于当前的值。

---

## 2. 应用场景

### 2.1 条件期望的应用

- **预测与估计**：$E[X|Y]$ 是已知 $Y$ 时 $X$ 的最优均方预测。在回归分析中，回归函数就是条件期望。
- **贝叶斯推断**：后验均值 $E[\theta | \mathbf{x}]$ 是 $\theta$ 的最优估计（在均方误差意义下）。
- **金融工程**：风险中性定价中，衍生品的价格可以表示为条件期望。

### 2.2 鞅论的应用

- **金融数学**：在风险中性测度下，资产价格过程是鞅。期权定价可以表示为终止期的贴现条件期望。
- **随机过程**：布朗运动是鞅，Doob 鞅是条件期望的典型应用。
- **算法分析**：随机算法的复杂度分析中常用鞅停时定理。

### 2.3 方差分解的应用

- **方差分析（ANOVA）**：$\mathrm{Var}(X) = E[\mathrm{Var}(X|Y)] + \mathrm{Var}(E[X|Y])$ 将总方差分解为"组内方差"和"组间方差"。
- **回归分析**：$R^2 = \mathrm{Var}(E[X|Y]) / \mathrm{Var}(X)$ 衡量了回归模型的解释力。
- **信息论**：互信息可以表示为 $I(X; Y) = H(X) - H(X|Y)$，与方差分解有类似结构。

---

## 3. 数学理论（及推导）

### 3.1 条件期望的定义

#### 3.1.1 离散情形

设 $X$ 和 $Y$ 为离散型随机变量，$P(Y = y) > 0$。给定 $Y = y$ 时 $X$ 的条件期望定义为

$$E[X | Y = y] = \sum_x x \cdot P(X = x | Y = y) = \frac{\sum_x x \cdot P(X = x, Y = y)}{P(Y = y)}$$

$E[X | Y]$ 作为 $Y$ 的函数，是一个随机变量，其取值为 $E[X | Y = y]$（当 $Y = y$ 时）。

#### 3.1.2 连续情形

设 $(X, Y)$ 具有联合密度 $f(x, y)$，$f_Y(y) > 0$。给定 $Y = y$ 时 $X$ 的条件期望定义为

$$E[X | Y = y] = \int_{-\infty}^{+\infty} x \, f_{X|Y}(x|y) \, dx = \frac{\int_{-\infty}^{+\infty} x \, f(x, y) \, dx}{f_Y(y)}$$

#### 3.1.3 一般情形（Radon-Nikodym 导数）

设 $X \in L^1(\Omega, \mathcal{F}, P)$，$\mathcal{G}$ 为 $\mathcal{F}$ 的子 $\sigma$-代数。**条件期望** $E[X | \mathcal{G}]$ 是满足以下条件的**$\mathcal{G}$-可测**随机变量：

$$\int_A E[X | \mathcal{G}] \, dP = \int_A X \, dP, \quad \forall A \in \mathcal{G}$$

即 $E[X | \mathcal{G}]$ 是 $X$ 在 $\mathcal{G}$ 上的 Radon-Nikodym 导数 $d\nu_X / dP\big|_{\mathcal{G}}$。

**存在唯一性**：由 Radon-Nikodym 定理，$E[X | \mathcal{G}]$ 存在且在几乎必然意义下唯一。

**特例**：$E[X | Y] = E[X | \sigma(Y)]$，其中 $\sigma(Y)$ 是由 $Y$ 生成的 $\sigma$-代数。

### 3.2 条件期望的性质

**性质 3.2.1（线性性）**：$E[aX + bY | \mathcal{G}] = aE[X | \mathcal{G}] + bE[Y | \mathcal{G}]$。

**性质 3.2.2（取常数的条件期望）**：若 $X$ 为 $\mathcal{G}$-可测，则 $E[X | \mathcal{G}] = X$（a.s.）。

**性质 3.2.3（取出已知量）**：若 $Z$ 为 $\mathcal{G}$-可测且有界，则 $E[ZX | \mathcal{G}] = Z \cdot E[X | \mathcal{G}]$。

**性质 3.2.4（全期望公式的推广 / 塔式性质 / Tower Property）**：若 $\mathcal{H} \subseteq \mathcal{G} \subseteq \mathcal{F}$，则

$$E[E[X | \mathcal{G}] | \mathcal{H}] = E[X | \mathcal{H}]$$

**证明**：对任意 $A \in \mathcal{H} \subseteq \mathcal{G}$，

$$\int_A E[E[X|\mathcal{G}]|\mathcal{H}] \, dP = \int_A E[X|\mathcal{G}] \, dP = \int_A X \, dP$$

故 $E[E[X|\mathcal{G}]|\mathcal{H}]$ 满足 $E[X|\mathcal{H}]$ 的定义条件。$\blacksquare$

**性质 3.2.5（条件 Jensen 不等式）**：若 $\varphi$ 为凸函数，$X \in L^1$，$\varphi(X) \in L^1$，则

$$\varphi(E[X | \mathcal{G}]) \leq E[\varphi(X) | \mathcal{G}] \quad \text{(a.s.)}$$

**推论**：
- $|E[X|\mathcal{G}]| \leq E[|X| | \mathcal{G}]$（取 $\varphi(x) = |x|$）。
- $(E[X|\mathcal{G}])^2 \leq E[X^2 | \mathcal{G}]$（取 $\varphi(x) = x^2$）。

### 3.3 全期望公式（推导）

**定理 3.3.1（全期望公式 / Law of Total Expectation）**：

$$E[X] = E[E[X | Y]]$$

**证明（连续型）**：

$$E[E[X|Y]] = \int_{-\infty}^{+\infty} E[X|Y=y] f_Y(y) \, dy = \int_{-\infty}^{+\infty} \left[\int_{-\infty}^{+\infty} x f_{X|Y}(x|y) \, dx\right] f_Y(y) \, dy$$

$$= \int_{-\infty}^{+\infty} \int_{-\infty}^{+\infty} x f(x, y) \, dx \, dy = E[X] \quad \blacksquare$$

**推论 3.3.1（离散版）**：$E[X] = \sum_y E[X|Y=y] \cdot P(Y = y)$。

**推论 3.3.2（条件概率的全概率公式）**：$P(A) = E[P(A|\mathcal{G})]$。

### 3.4 条件期望的几何意义：正交投影（严格推导）

**定理 3.4.1（正交投影定理）**：设 $X \in L^2(\Omega, \mathcal{F}, P)$，$\mathcal{G} \subseteq \mathcal{F}$ 为子 $\sigma$-代数。则

$$E[X | \mathcal{G}] = \arg\min_{Z \in L^2(\mathcal{G})} \|X - Z\|_{L^2}^2 = \arg\min_{Z \in L^2(\mathcal{G})} E[(X - Z)^2]$$

即条件期望是 $X$ 在 $L^2(\mathcal{G})$ 上的最佳 $L^2$ 近似。

**证明**：设 $Z^* = E[X | \mathcal{G}]$。对任意 $Z \in L^2(\mathcal{G})$：

$$E[(X - Z)^2] = E[(X - Z^* + Z^* - Z)^2]$$
$$= E[(X - Z^*)^2] + 2E[(X - Z^*)(Z^* - Z)] + E[(Z^* - Z)^2]$$

关键在于中间项：由于 $Z^* - Z$ 是 $\mathcal{G}$-可测的，由条件期望的定义：

$$E[(X - Z^*)(Z^* - Z)] = E\left[E[(X - Z^*)(Z^* - Z)|\mathcal{G}]\right] = E\left[(Z^* - Z) \cdot E[(X - Z^*)|\mathcal{G}]\right]$$
$$= E\left[(Z^* - Z) \cdot (E[X|\mathcal{G}] - Z^*)\right] = E[(Z^* - Z) \cdot 0] = 0$$

故 $E[(X - Z)^2] = E[(X - Z^*)^2] + E[(Z^* - Z)^2] \geq E[(X - Z^*)^2]$。

等号成立当且仅当 $Z = Z^*$（a.s.）。$\blacksquare$

**正交性**：上述证明同时说明 $X - E[X|\mathcal{G}]$ 与所有 $L^2(\mathcal{G})$ 中的元素正交：

$$E[(X - E[X|\mathcal{G}]) \cdot Z] = 0, \quad \forall Z \in L^2(\mathcal{G})$$

这就是"残差与预测值不相关"的数学表述。

### 3.5 鞅的初步概念

**定义 3.5.1（ filtrations）**：$\{\mathcal{F}_n\}_{n \geq 0}$ 是 $\mathcal{F}$ 的一列递增的子 $\sigma$-代数，即 $\mathcal{F}_0 \subseteq \mathcal{F}_1 \subseteq \mathcal{F}_2 \subseteq \cdots \subseteq \mathcal{F}$，称为**filtration**。$\mathcal{F}_n$ 表示"到时刻 $n$ 为止可获得的所有信息"。

**定义 3.5.2（$\{\mathcal{F}_n\}$-适应过程）**：随机过程 $\{X_n\}_{n \geq 0}$ 称为 $\{\mathcal{F}_n\}$-适应的，若对每个 $n$，$X_n$ 是 $\mathcal{F}_n$-可测的。

**定义 3.5.3（鞅 / Martingale）**：适应过程 $\{X_n\}$ 称为**鞅**（关于 filtration $\{\mathcal{F}_n\}$），若：

1. $E[|X_n|] < \infty$，$\forall n$；
2. $E[X_{n+1} | \mathcal{F}_n] = X_n$，$\forall n$。

**直觉**："公平游戏"——已知过去的信息，对未来值的期望恰好等于当前值。没有系统的盈利或亏损趋势。

**定义 3.5.4（下鞅 / Supermartingale）**：

- **下鞅**（Submartingale）：$E[X_{n+1} | \mathcal{F}_n] \geq X_n$（期望上升，"有利游戏"）。
- **上鞅**（Supermartingale）：$E[X_{n+1} | \mathcal{F}_n] \leq X_n$（期望下降，"不利游戏"）。

**例 3.5.1（Doob 鞅）**：设 $X \in L^1$，$\{\mathcal{F}_n\}$ 为 filtration，则 $M_n = E[X | \mathcal{F}_n]$ 是鞅。

**证明**：由塔式性质，

$$E[M_{n+1} | \mathcal{F}_n] = E[E[X | \mathcal{F}_{n+1}] | \mathcal{F}_n] = E[X | \mathcal{F}_n] = M_n \quad \blacksquare$$

**例 3.5.2（对称随机游走）**：设 $S_n = \sum_{i=1}^n X_i$，$X_i$ i.i.d.，$P(X_i = 1) = P(X_i = -1) = 1/2$。则 $\{S_n\}$ 是鞅。

**例 3.5.3（乘积鞅）**：设 $Y_n = \prod_{i=1}^n Z_i$，$Z_i$ i.i.d.，$E[Z_i] = 1$。则 $\{Y_n\}$ 是鞅。

**定理 3.5.1（Doob 停时定理 / Optional Stopping Theorem）**：设 $\{M_n\}$ 是鞅，$\tau$ 是停时（stopping time），满足某些正则条件（如 $\tau$ 有界，或 $M_n$ 有界），则

$$E[M_\tau] = E[M_0]$$

**直觉**：即使策略是基于已有信息决定何时停止（停时），公平游戏的期望盈利仍为零。

### 3.6 条件方差与方差分解公式

**定义 3.6.1（条件方差）**：

$$\mathrm{Var}(X | Y = y) = E\left[(X - E[X|Y=y])^2 \big| Y = y\right]$$
$$= E[X^2 | Y = y] - (E[X | Y = y])^2$$

$\mathrm{Var}(X | Y)$ 是一个随机变量（$Y$ 的函数）。

**定理 3.6.1（方差分解公式 / Law of Total Variance / ANOVA）**：

$$\mathrm{Var}(X) = E[\mathrm{Var}(X | Y)] + \mathrm{Var}(E[X | Y])$$

即：**总方差 = 条件方差的期望 + 条件期望的方差**。

**证明**：

$$E[\mathrm{Var}(X|Y)] = E[E[X^2|Y] - (E[X|Y])^2] = E[E[X^2|Y]] - E[(E[X|Y])^2] = E[X^2] - E[(E[X|Y])^2]$$

$$\mathrm{Var}(E[X|Y]) = E[(E[X|Y])^2] - (E[E[X|Y]])^2 = E[(E[X|Y])^2] - (E[X])^2$$

相加：

$$E[\mathrm{Var}(X|Y)] + \mathrm{Var}(E[X|Y]) = E[X^2] - (E[X])^2 = \mathrm{Var}(X) \quad \blacksquare$$

**统计解释**（ANOVA）：

- $\mathrm{Var}(E[X|Y])$：**组间方差**（Between-group variance）——由 $Y$ 的不同取值（组别）造成的 $X$ 的变异。
- $E[\mathrm{Var}(X|Y)]$：**组内方差**（Within-group variance）——同一 $Y$ 取值（组内）$X$ 的变异。

定义**相关比**（correlation ratio）：

$$\eta^2 = \frac{\mathrm{Var}(E[X|Y])}{\mathrm{Var}(X)} = 1 - \frac{E[\mathrm{Var}(X|Y)]}{\mathrm{Var}(X)}$$

$\eta^2 \in [0, 1]$ 衡量了 $Y$ 对 $X$ 的"解释力"。

**例 3.6.1**：设 $X = Y + Z$，$Y$ 与 $Z$ 独立。则

$$\mathrm{Var}(X) = \mathrm{Var}(Y) + \mathrm{Var}(Z)$$

验证方差分解：

$$\mathrm{Var}(E[X|Y]) = \mathrm{Var}(Y + E[Z]) = \mathrm{Var}(Y)$$
$$E[\mathrm{Var}(X|Y)] = E[\mathrm{Var}(Y + Z|Y)] = E[\mathrm{Var}(Z|Y)] = \mathrm{Var}(Z)$$

故 $\mathrm{Var}(X) = \mathrm{Var}(Y) + \mathrm{Var}(Z)$。$\blacksquare$

### 3.7 全方差公式的一般化

**多因素方差分解**：设 $Y_1, Y_2, \ldots, Y_k$ 为多个随机变量，则

$$\mathrm{Var}(X) = \mathrm{Var}(E[X | Y_1, \ldots, Y_k]) + E[\mathrm{Var}(X | Y_1, \ldots, Y_k)]$$

递推地：

$$\mathrm{Var}(X) = \mathrm{Var}(E[X]) + E[\mathrm{Var}(X | Y_1)]$$
$$= \mathrm{Var}(E[X]) + E[\mathrm{Var}(E[X|Y_1] | Y_1, Y_2)] + E[\mathrm{Var}(X | Y_1, Y_2)]$$

这在多层模型（hierarchical models）和方差成分分析（variance components analysis）中有重要应用。
