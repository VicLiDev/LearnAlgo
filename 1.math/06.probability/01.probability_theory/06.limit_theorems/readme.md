# 第六章 极限定理

## 1. 几何意义

### 1.1 大数定律的几何直觉

大数定律是概率论中最基本的结果之一，其核心思想是：**大量独立重复试验的"平均结果"趋于期望值**。

- **弱大数定律**：样本均值 $\bar{X}_n = \frac{1}{n}\sum_{i=1}^n X_i$ 依概率收敛于 $E[X]$，即

$$\bar{X}_n \xrightarrow{P} E[X]$$

几何意义：当样本量 $n$ 增大时，$\bar{X}_n$ 的分布越来越"集中"在 $E[X]$ 附近。就像在数轴上，$\bar{X}_n$ 的概率质量逐渐向 $\mu$ 聚拢。

- **强大数定律**：$\bar{X}_n$ 几乎必然收敛于 $E[X]$，即

$$P\left(\lim_{n \to \infty} \bar{X}_n = E[X]\right) = 1$$

几何意义：几乎所有样本路径（即几乎所有可能的实验结果序列）的均值都会趋于期望值。"几乎必然"排除了概率为零的异常路径。

### 1.2 中心极限定理的几何直觉

中心极限定理（CLT）是概率论中最重要的定理之一，其几何意义为：

**无论原始分布是什么形状，只要满足一定条件，大量独立随机变量之和的标准化后的分布都趋近于标准正态分布。**

- 可以想象，每次从原始分布中取一个样本（可能是任意形状——偏斜的、离散的、有界的），把它们加起来，然后标准化。随着样本量的增加，这个标准化和的直方图会越来越像标准的钟形曲线。
- 几何上，CLT 说明了"钟形曲线"（正态分布）在概率论中的中心地位——它是各种分布的"吸引子"（attractor），就像不动点是动力系统的吸引子一样。

### 1.3 Markov/Chebyshev 不等式的几何意义

- **Markov 不等式** $P(|X| \geq a) \leq E[|X|]/a$：限制了随机变量取大值的概率。几何上，如果均值不大，则取大值的概率不可能很大。
- **Chebyshev 不等式** $P(|X - \mu| \geq k\sigma) \leq 1/k^2$：限制了偏离均值的概率。几何上，偏离中心越远，概率越低，且以 $1/k^2$ 的速度衰减。这为 CLT 的证明提供了基础。

---

## 2. 应用场景

### 2.1 大数定律的应用

- **蒙特卡洛方法**：用大量随机模拟的均值来估计期望（如计算定积分）。
- **频率学派解释**：大数定律为"概率是频率的极限"提供了数学基础。
- **保险业**：大量保单的平均赔付趋于期望赔付率。
- **民意调查**：样本均值近似总体均值。

### 2.2 中心极限定理的应用

- **统计推断**：样本均值的分布近似正态，是大样本统计检验（$z$ 检验）的基础。
- **置信区间**：基于正态近似构造参数的置信区间。
- **质量控制**：利用正态近似监控生产过程。
- **金融**：资产组合的收益在大量资产时近似正态分布。

### 2.3 De Moivre-Laplace 定理的应用

- **二项分布的正态近似**：当 $n$ 较大时，用正态分布近似计算二项概率。
- **正态近似公式**：$B(n, p) \approx N(np, np(1-p))$，连续性修正 $P(a \leq X \leq b) \approx \Phi\left(\frac{b+0.5-np}{\sqrt{np(1-p)}}\right) - \Phi\left(\frac{a-0.5-np}{\sqrt{np(1-p)}}\right)$。

---

## 3. 数学理论（及推导）

### 3.1 Markov 不等式（证明）

**定理 3.1.1（Markov 不等式）**：设 $X$ 为非负随机变量，$a > 0$，则

$$P(X \geq a) \leq \frac{E[X]}{a}$$

**证明**：

$$E[X] = E[X \cdot \mathbf{1}_{\{X \geq a\}}] + E[X \cdot \mathbf{1}_{\{X < a\}}] \geq E[X \cdot \mathbf{1}_{\{X \geq a\}}] \geq E[a \cdot \mathbf{1}_{\{X \geq a\}}] = a \cdot P(X \geq a)$$

故 $P(X \geq a) \leq E[X]/a$。$\blacksquare$

### 3.2 Chebyshev 不等式（证明）

**定理 3.2.1（Chebyshev 不等式）**：设 $E[X] = \mu$，$\mathrm{Var}(X) = \sigma^2 < \infty$，$k > 0$，则

$$P(|X - \mu| \geq k) \leq \frac{\sigma^2}{k^2}$$

等价形式：$P(|X - \mu| \geq k\sigma) \leq \dfrac{1}{k^2}$。

**证明**：对非负随机变量 $Y = (X - \mu)^2$ 应用 Markov 不等式：

$$P(|X - \mu| \geq k) = P((X - \mu)^2 \geq k^2) \leq \frac{E[(X - \mu)^2]}{k^2} = \frac{\sigma^2}{k^2} \quad \blacksquare$$

**推论**：取 $k = 2\sigma$，$P(|X - \mu| \geq 2\sigma) \leq 1/4 = 0.25$（正态分布下精确值为 $0.0455$）。Chebyshev 不等式给出了一个"宽松但通用"的上界。

### 3.3 弱大数定律

**定理 3.3.1（Khinchin 弱大数定律）**：设 $X_1, X_2, \ldots$ i.i.d.，$E[X_1] = \mu < \infty$，则

$$\bar{X}_n = \frac{1}{n}\sum_{i=1}^n X_i \xrightarrow{P} \mu$$

即对任意 $\varepsilon > 0$，

$$\lim_{n \to \infty} P(|\bar{X}_n - \mu| \geq \varepsilon) = 0$$

**证明（利用 Chebyshev 不等式，要求方差有限）**：设 $\mathrm{Var}(X_i) = \sigma^2 < \infty$，则

$$\mathrm{Var}(\bar{X}_n) = \frac{\sigma^2}{n}$$

由 Chebyshev 不等式：

$$P(|\bar{X}_n - \mu| \geq \varepsilon) \leq \frac{\mathrm{Var}(\bar{X}_n)}{\varepsilon^2} = \frac{\sigma^2}{n\varepsilon^2} \to 0 \quad (n \to \infty) \quad \blacksquare$$

**注**：Khinchin 弱大数定律的完整证明（不假设方差有限）需要用截断法（truncation method），此处略。

**定理 3.3.2（Chebyshev 弱大数定律）**：设 $X_1, X_2, \ldots$ 两两不相关，$\mathrm{Var}(X_i) \leq C$（一致有界），则

$$\frac{1}{n}\sum_{i=1}^n (X_i - E[X_i]) \xrightarrow{P} 0$$

### 3.4 强大数定律

**定理 3.4.1（Kolmogorov 强大数定律）**：设 $X_1, X_2, \ldots$ i.i.d.，$E[|X_1|] < \infty$，$E[X_1] = \mu$，则

$$P\left(\lim_{n \to \infty} \bar{X}_n = \mu\right) = 1$$

即 $\bar{X}_n \xrightarrow{\text{a.s.}} \mu$。

**证明思路**（Kolmogorov 的证明利用截断法和 Borel-Cantelli 引理）：

1. 对 $X_i$ 进行截断：定义 $Y_i = X_i \mathbf{1}_{\{|X_i| \leq i\}}$。
2. 证明截断后的变量之和满足强大数定律（利用 Kolmogorov 不等式）。
3. 利用 Borel-Cantelli 引理证明 $\sum_{i=1}^{\infty} P(X_i \neq Y_i) < \infty$。
4. 由 Borel-Cantelli 引理，$X_i \neq Y_i$ 只发生有限次，故两序列的极限行为一致。

**定理 3.4.2（Kolmogorov 强大数定律，方差有限情形）**：设 $X_1, X_2, \ldots$ 独立，$\sum_{i=1}^{\infty} \frac{\mathrm{Var}(X_i)}{i^2} < \infty$，则

$$\frac{1}{n}\sum_{i=1}^n (X_i - E[X_i]) \xrightarrow{\text{a.s.}} 0$$

### 3.5 中心极限定理

#### 3.5.1 Lindeberg-Levy 中心极限定理（证明）

**定理 3.5.1（Lindeberg-Levy CLT）**：设 $X_1, X_2, \ldots$ i.i.d.，$E[X_1] = \mu$，$\mathrm{Var}(X_1) = \sigma^2 \in (0, \infty)$。令 $S_n = \sum_{i=1}^n X_i$，则

$$\frac{S_n - n\mu}{\sigma\sqrt{n}} \xrightarrow{d} N(0, 1)$$

即

$$\lim_{n \to \infty} P\left(\frac{S_n - n\mu}{\sigma\sqrt{n}} \leq x\right) = \Phi(x) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^x e^{-t^2/2} \, dt$$

**证明**（利用特征函数）：

令 $Y_i = \frac{X_i - \mu}{\sigma}$，则 $E[Y_i] = 0$，$\mathrm{Var}(Y_i) = 1$，$E[Y_i^3] = \gamma$（三阶矩存在）。

标准化和 $Z_n = \frac{S_n - n\mu}{\sigma\sqrt{n}} = \frac{1}{\sqrt{n}}\sum_{i=1}^n Y_i$。

计算 $Z_n$ 的特征函数：

$$\varphi_{Z_n}(t) = E\left[e^{it Z_n}\right] = E\left[\exp\left(\frac{it}{\sqrt{n}} \sum_{i=1}^n Y_i\right)\right] = \left[\varphi_{Y_1}\left(\frac{t}{\sqrt{n}}\right)\right]^n$$

对 $\varphi_{Y_1}(s)$ 在 $s = 0$ 处展开到三阶：

$$\varphi_{Y_1}(s) = 1 + iE[Y_1]s - \frac{E[Y_1^2]}{2}s^2 + o(s^2) = 1 - \frac{s^2}{2} + o(s^2)$$

（因为 $E[Y_1] = 0$，$E[Y_1^2] = 1$。）

取 $s = t/\sqrt{n}$：

$$\varphi_{Y_1}\left(\frac{t}{\sqrt{n}}\right) = 1 - \frac{t^2}{2n} + o\left(\frac{1}{n}\right)$$

故

$$\varphi_{Z_n}(t) = \left[1 - \frac{t^2}{2n} + o\left(\frac{1}{n}\right)\right]^n$$

利用极限 $\lim_{n \to \infty} \left(1 + \frac{a_n}{n}\right)^n = e^{\lim a_n}$（当 $a_n \to a$ 时）：

$$\lim_{n \to \infty} \varphi_{Z_n}(t) = \lim_{n \to \infty} \left[1 - \frac{t^2}{2n} + o\left(\frac{1}{n}\right)\right]^n = e^{-t^2/2}$$

这正是标准正态分布 $N(0, 1)$ 的特征函数。由 Levy 连续性定理（特征函数逐点收敛于连续函数则分布函数收敛），得 $Z_n \xrightarrow{d} N(0, 1)$。$\blacksquare$

#### 3.5.2 Lindeberg-Feller 中心极限定理

**定理 3.5.2（Lindeberg-Feller CLT）**：设 $X_1, X_2, \ldots$ 独立（不要求同分布），$E[X_k] = \mu_k$，$\mathrm{Var}(X_k) = \sigma_k^2 \in (0, \infty)$。令 $s_n^2 = \sum_{k=1}^n \sigma_k^2$。若对每个 $\varepsilon > 0$，**Lindeberg 条件**成立：

$$\lim_{n \to \infty} \frac{1}{s_n^2} \sum_{k=1}^n E\left[(X_k - \mu_k)^2 \mathbf{1}_{\{|X_k - \mu_k| \geq \varepsilon s_n\}}\right] = 0$$

则

$$\frac{\sum_{k=1}^n (X_k - \mu_k)}{s_n} \xrightarrow{d} N(0, 1)$$

**Lindeberg 条件的直观含义**：每个个体对总和的贡献都是"微小的"——没有任何单个 $X_k$ 的偏差能显著影响总和。这保证了"大量微小因素叠加趋于正态"。

**推论（Lyapunov 条件）**：若存在 $\delta > 0$ 使得

$$\lim_{n \to \infty} \frac{1}{s_n^{2+\delta}} \sum_{k=1}^n E\left[|X_k - \mu_k|^{2+\delta}\right] = 0$$

则 Lindeberg 条件成立，从而 CLT 成立。

### 3.6 De Moivre-Laplace 定理

**定理 3.6.1（De Moivre-Laplace 定理）**：设 $X_n \sim B(n, p)$（$0 < p < 1$ 固定），则

$$\frac{X_n - np}{\sqrt{np(1-p)}} \xrightarrow{d} N(0, 1)$$

**证明**：这是 Lindeberg-Levy CLT 的特例。$X_n = \sum_{i=1}^n X_i$，$X_i \sim B(1, p)$ 独立同分布。$E[X_i] = p$，$\mathrm{Var}(X_i) = p(1-p)$。直接应用 CLT 即得。$\blacksquare$

**正态近似**：对 $a, b \in \mathbb{Z}$，

$$P(a \leq X_n \leq b) \approx \Phi\left(\frac{b + 0.5 - np}{\sqrt{np(1-p)}}\right) - \Phi\left(\frac{a - 0.5 - np}{\sqrt{np(1-p)}}\right)$$

其中 $+0.5$ 和 $-0.5$ 称为**连续性修正**（continuity correction），用于弥补离散分布和连续分布之间的差异。

### 3.7 大偏差初步

**大偏差理论**研究的是概率论中"罕见事件"的概率的精确渐近行为，即当 $a$ 远大于 $E[X]$ 时，$P(\bar{X}_n \geq a)$ 的衰减速度。

**定理 3.7.1（Cramer 大偏差定理）**：设 $X_1, X_2, \ldots$ i.i.d.，MGF $M_X(t) = E[e^{tX}]$ 在原点某邻域内有限。定义**率函数**（rate function）：

$$I(x) = \sup_{t \in \mathbb{R}} \{tx - \ln M_X(t)\}$$

则对 $x > E[X]$，

$$\lim_{n \to \infty} \frac{1}{n} \ln P(\bar{X}_n \geq x) = -I(x)$$

即 $P(\bar{X}_n \geq x) \approx e^{-nI(x)}$（指数级衰减）。

**与 Chebyshev 不等式的对比**：

- Chebyshev：$P(|\bar{X}_n - \mu| \geq \varepsilon) \leq \sigma^2/(n\varepsilon^2)$，即 $O(1/n)$ 衰减。
- 大偏差：$P(\bar{X}_n \geq x) = e^{-nI(x) + o(n)}$，即**指数级**衰减，远快于 Chebyshev 的多项式衰减。
- 大偏差理论提供了"精确的"渐近，而不仅仅是上界。

### 3.8 Levy 连续性定理

**定理 3.8.1（Levy 连续性定理）**：设 $F_n$ 是分布函数序列，$\varphi_n$ 是对应的特征函数序列。

1. 若 $F_n \xrightarrow{d} F$（$F$ 为某分布函数），且 $F$ 在所有点连续，则 $\varphi_n(t) \to \varphi_F(t)$ 对所有 $t$ 一致成立。
2. 若 $\varphi_n(t)$ 逐点收敛于某函数 $\varphi(t)$，且 $\varphi(t)$ 在 $t = 0$ 处连续，则 $\varphi$ 是某分布函数 $F$ 的特征函数，且 $F_n \xrightarrow{d} F$。

这个定理是 CLT 特征函数证明法的理论基础——它建立了"特征函数收敛"与"分布收敛"之间的桥梁。
