# 第四章 常见概率分布

## 1. 几何意义

### 1.1 离散型分布的几何直觉

- **Bernoulli 分布** $B(1, p)$：最简单的"成功/失败"模型。在数轴上只有两个点 $\{0, 1\}$，分别具有"质量" $1-p$ 和 $p$。

- **二项分布** $B(n, p)$：$n$ 次独立 Bernoulli 试验中成功的次数。其 PMF 呈钟形，在 $k \approx np$ 处达到峰值。当 $n$ 增大时，二项分布的形状越来越接近正态分布（由 CLT 保证）。

- **Poisson 分布** $P(\lambda)$：描述稀有事件在固定时间/空间内发生次数的分布。PMF $p(k) = e^{-\lambda} \lambda^k / k!$ 在 $k = \lfloor \lambda \rfloor$ 附近达到峰值，形状也呈钟形。

- **几何分布** $\mathrm{Geom}(p)$：首次成功所需的试验次数。PMF $p(k) = (1-p)^{k-1}p$ 呈指数衰减，体现了"等待"的几何特征。

- **超几何分布**：不放回抽样中成功的次数，是二项分布（有放回抽样）的"有限总体"版本。

### 1.2 连续型分布的几何直觉

- **均匀分布** $U(a, b)$：密度函数是一个矩形（"平顶"），概率均匀分布在 $[a, b]$ 上。

- **指数分布** $\mathrm{Exp}(\lambda)$：密度函数 $f(x) = \lambda e^{-\lambda x}$（$x \geq 0$）从 $\lambda$ 开始单调递减到 0，呈"长尾"形状。它是唯一具有**无记忆性**的连续分布。

- **正态分布** $N(\mu, \sigma^2)$：密度函数呈著名的"钟形曲线"（Gaussian 曲线），关于 $\mu$ 对称，$\sigma$ 越大曲线越"矮胖"。它是概率论中最重要的分布，由 CLT 保证其在自然界中的普遍性。

- **Gamma 分布** $\Gamma(\alpha, \beta)$：指数分布的一般化（$\alpha$ 个独立指数随机变量之和服从 Gamma 分布）。当 $\alpha$ 较大时接近正态分布。

- **Beta 分布** $\mathrm{Beta}(\alpha, \beta)$：定义在 $[0, 1]$ 上，形状灵活，可呈钟形、U 形、单调递增/递减等。是 Bayes 统计中先验分布的自然选择。

- **$\chi^2$ 分布**：$\Gamma(n/2, 1/2)$ 的特例，表示 $n$ 个独立标准正态变量的平方和。它是假设检验（卡方检验）的基础。

### 1.3 各分布之间的关系图

各分布之间存在丰富的推导关系，可以用如下依赖关系图表示（箭头表示"通过某种操作得到"）：

```
Bernoulli(p) ──n次独立和──> Binomial(n,p) ──n→∞,np=λ──> Poisson(λ)
    │                                    │
    │                                    │ n→∞
    │                                    ↓
    │                              Normal(√(npq))
    │
    └──首次成功──> Geometric(p) ──r次──> NegBin(r,p)

Uniform(0,1) ──n次积──> Beta(n,1) ──推广──> Beta(α,β)
     │
     └──−ln变换──> Exp(1) ──α个和──> Gamma(α,1)
                           │
                           └──α=n/2──> χ²(n)
                                            │
                                            └──两个独立χ²──> F(m,n)
                                            │
                                            └──√(χ²/n)──> t(n)

Exp(λ) ──正态逼近──> Normal
Gamma(α) ──α→∞──> Normal
```

---

## 2. 应用场景

### 2.1 离散型分布的应用

| 分布 | 应用场景 |
|------|----------|
| Bernoulli | 单次抛硬币、产品合格/不合格判定 |
| 二项分布 | $n$ 次独立试验中成功的次数（如 $n$ 个元件中有多少个故障） |
| Poisson | 单位时间内到达的顾客数、网页点击数、放射性衰变次数 |
| 几何分布 | 首次成功所需的尝试次数（如首次命中目标需要的射击次数） |
| 负二项 | 第 $r$ 次成功所需的试验次数 |
| 超几何 | 不放回抽样中的合格品数（如从一批产品中随机抽取检验） |

### 2.2 连续型分布的应用

| 分布 | 应用场景 |
|------|----------|
| 均匀分布 | 随机数生成、舍入误差建模 |
| 指数分布 | 设备寿命、服务等待时间、放射性衰变时间 |
| 正态分布 | 测量误差、身高体重、信号噪声 |
| Gamma | 保险理赔金额、降雨量总和 |
| Beta | 比例估计、可靠性的先验分布 |
| $\chi^2$ | 拟合优度检验、独立性检验 |
| $t$ 分布 | 小样本均值检验 |
| $F$ 分布 | 方差齐性检验、方差分析 |

---

## 3. 数学理论（及推导）

### 3.1 离散型分布

#### 3.1.1 Bernoulli 分布 $B(1, p)$

- **PMF**：$P(X = 1) = p$，$P(X = 0) = 1 - p$。
- **期望**：$E[X] = p$。
- **方差**：$\mathrm{Var}(X) = p(1 - p)$。

#### 3.1.2 二项分布 $B(n, p)$

- **PMF**：$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}$，$k = 0, 1, \ldots, n$。
- **期望**：$E[X] = np$。
- **方差**：$\mathrm{Var}(X) = np(1-p)$。

**推导**：$X = \sum_{i=1}^n X_i$，其中 $X_i \sim B(1, p)$ 独立同分布。由期望的线性性和方差的独立性可加性直接得到。

#### 3.1.3 Poisson 分布 $P(\lambda)$

- **PMF**：$P(X = k) = \dfrac{e^{-\lambda} \lambda^k}{k!}$，$k = 0, 1, 2, \ldots$
- **期望**：$E[X] = \lambda$。
- **方差**：$\mathrm{Var}(X) = \lambda$。

**推导（期望）**：

$$E[X] = \sum_{k=0}^{\infty} k \cdot \frac{e^{-\lambda}\lambda^k}{k!} = e^{-\lambda} \sum_{k=1}^{\infty} \frac{\lambda^k}{(k-1)!} = e^{-\lambda} \cdot \lambda \sum_{k=1}^{\infty} \frac{\lambda^{k-1}}{(k-1)!} = \lambda e^{-\lambda} \cdot e^{\lambda} = \lambda$$

**推导（方差）**：先计算 $E[X(X-1)]$：

$$E[X(X-1)] = \sum_{k=0}^{\infty} k(k-1) \frac{e^{-\lambda}\lambda^k}{k!} = e^{-\lambda}\lambda^2 \sum_{k=2}^{\infty} \frac{\lambda^{k-2}}{(k-2)!} = \lambda^2$$

故 $E[X^2] = E[X(X-1)] + E[X] = \lambda^2 + \lambda$，$\mathrm{Var}(X) = \lambda^2 + \lambda - \lambda^2 = \lambda$。$\blacksquare$

#### 3.1.4 几何分布 $\mathrm{Geom}(p)$

- **PMF**：$P(X = k) = (1-p)^{k-1} p$，$k = 1, 2, \ldots$
- **期望**：$E[X] = \dfrac{1}{p}$。
- **方差**：$\mathrm{Var}(X) = \dfrac{1-p}{p^2}$。

**推导（期望）**：

$$E[X] = \sum_{k=1}^{\infty} k(1-p)^{k-1}p = p \sum_{k=1}^{\infty} k(1-p)^{k-1} = p \cdot \frac{1}{(1-(1-p))^2} = \frac{p}{p^2} = \frac{1}{p}$$

其中利用了幂级数 $\sum_{k=1}^{\infty} kx^{k-1} = 1/(1-x)^2$（$|x| < 1$）。

#### 3.1.5 负二项分布 $\mathrm{NegBin}(r, p)$

- **PMF**：$P(X = k) = \binom{k-1}{r-1} p^r (1-p)^{k-r}$，$k = r, r+1, \ldots$
- **期望**：$E[X] = \dfrac{r}{p}$。
- **方差**：$\mathrm{Var}(X) = \dfrac{r(1-p)}{p^2}$。

#### 3.1.6 超几何分布 $H(N, M, n)$

从 $N$ 个物品（其中 $M$ 个有标记）中不放回抽取 $n$ 个，$X$ 为有标记的物品数。

- **PMF**：$P(X = k) = \dfrac{\binom{M}{k}\binom{N-M}{n-k}}{\binom{N}{n}}$，$\max(0, n+M-N) \leq k \leq \min(n, M)$。
- **期望**：$E[X] = n \cdot \dfrac{M}{N}$。
- **方差**：$\mathrm{Var}(X) = n \cdot \dfrac{M}{N} \cdot \left(1 - \dfrac{M}{N}\right) \cdot \dfrac{N-n}{N-1}$。

注意：与二项分布相比，方差多了一个因子 $\dfrac{N-n}{N-1}$（有限总体校正因子）。

#### 3.1.7 离散均匀分布 $U\{1, 2, \ldots, n\}$

- **PMF**：$P(X = k) = \dfrac{1}{n}$，$k = 1, 2, \ldots, n$。
- **期望**：$E[X] = \dfrac{n+1}{2}$。
- **方差**：$\mathrm{Var}(X) = \dfrac{n^2-1}{12}$。

### 3.2 连续型分布

#### 3.2.1 均匀分布 $U(a, b)$

- **PDF**：$f(x) = \dfrac{1}{b-a}$，$a \leq x \leq b$。
- **CDF**：$F(x) = \dfrac{x - a}{b-a}$。
- **期望**：$E[X] = \dfrac{a + b}{2}$。
- **方差**：$\mathrm{Var}(X) = \dfrac{(b-a)^2}{12}$。

#### 3.2.2 指数分布 $\mathrm{Exp}(\lambda)$

- **PDF**：$f(x) = \lambda e^{-\lambda x}$，$x \geq 0$。
- **CDF**：$F(x) = 1 - e^{-\lambda x}$。
- **期望**：$E[X] = \dfrac{1}{\lambda}$。
- **方差**：$\mathrm{Var}(X) = \dfrac{1}{\lambda^2}$。

**无记忆性（Memoryless Property）**：

$$P(X > s + t \mid X > s) = P(X > t), \quad \forall s, t > 0$$

**证明**：

$$P(X > s + t \mid X > s) = \frac{P(X > s + t)}{P(X > s)} = \frac{e^{-\lambda(s+t)}}{e^{-\lambda s}} = e^{-\lambda t} = P(X > t) \quad \blacksquare$$

**定理**：指数分布是唯一具有无记忆性的连续分布。

#### 3.2.3 正态分布（Gaussian 分布） $N(\mu, \sigma^2)$

- **PDF**：$f(x) = \dfrac{1}{\sqrt{2\pi}\sigma} \exp\left(-\dfrac{(x - \mu)^2}{2\sigma^2}\right)$。
- **期望**：$E[X] = \mu$。
- **方差**：$\mathrm{Var}(X) = \sigma^2$。

**标准正态分布**：$Z = \dfrac{X - \mu}{\sigma} \sim N(0, 1)$。

**标准化变换**：若 $X \sim N(\mu, \sigma^2)$，则 $Z = (X - \mu)/\sigma \sim N(0, 1)$。

**线性变换保持正态性**：若 $X \sim N(\mu, \sigma^2)$，则 $aX + b \sim N(a\mu + b, a^2\sigma^2)$。

**推导（$N(0,1)$ 的方差为 1）**：

$$E[Z^2] = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{+\infty} x^2 e^{-x^2/2} \, dx$$

利用分部积分：令 $u = x$，$dv = x e^{-x^2/2} dx$，则 $du = dx$，$v = -e^{-x^2/2}$：

$$E[Z^2] = \frac{1}{\sqrt{2\pi}} \left[-x e^{-x^2/2}\Big|_{-\infty}^{+\infty} + \int_{-\infty}^{+\infty} e^{-x^2/2} \, dx\right] = \frac{1}{\sqrt{2\pi}} \cdot \sqrt{2\pi} = 1 \quad \blacksquare$$

#### 3.2.4 Gamma 分布 $\Gamma(\alpha, \beta)$

- **PDF**：$f(x) = \dfrac{\beta^\alpha}{\Gamma(\alpha)} x^{\alpha-1} e^{-\beta x}$，$x > 0$。
- 其中 $\Gamma(\alpha) = \int_0^{\infty} t^{\alpha-1} e^{-t} \, dt$ 为 Gamma 函数。
- **期望**：$E[X] = \dfrac{\alpha}{\beta}$。
- **方差**：$\mathrm{Var}(X) = \dfrac{\alpha}{\beta^2}$。

**特殊情形**：
- $\alpha = 1$：Gamma$(1, \lambda) = \mathrm{Exp}(\lambda)$。
- $\alpha = n/2$，$\beta = 1/2$：Gamma$(n/2, 1/2) = \chi^2(n)$。

**可加性**：若 $X_i \sim \Gamma(\alpha_i, \beta)$ 独立，则 $\sum_i X_i \sim \Gamma(\sum_i \alpha_i, \beta)$。

#### 3.2.5 Beta 分布 $\mathrm{Beta}(\alpha, \beta)$

- **PDF**：$f(x) = \dfrac{x^{\alpha-1}(1-x)^{\beta-1}}{B(\alpha, \beta)}$，$0 < x < 1$。
- 其中 $B(\alpha, \beta) = \dfrac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha + \beta)}$ 为 Beta 函数。
- **期望**：$E[X] = \dfrac{\alpha}{\alpha + \beta}$。
- **方差**：$\mathrm{Var}(X) = \dfrac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}$。

#### 3.2.6 $\chi^2$ 分布（卡方分布） $\chi^2(n)$

- **定义**：设 $Z_1, Z_2, \ldots, Z_n$ i.i.d. $\sim N(0, 1)$，则 $\chi^2 = \sum_{i=1}^n Z_i^2 \sim \chi^2(n)$。
- **PDF**：$f(x) = \dfrac{1}{2^{n/2}\Gamma(n/2)} x^{n/2 - 1} e^{-x/2}$，$x > 0$。
- 即 Gamma$(n/2, 1/2)$。
- **期望**：$E[\chi^2] = n$。
- **方差**：$\mathrm{Var}(\chi^2) = 2n$。

**推导（利用 MGF）**：$Z_i^2 \sim \chi^2(1) = \mathrm{Gamma}(1/2, 1/2)$，其 MGF 为 $(1 - 2t)^{-1/2}$。由独立性：

$$M_{\chi^2(n)}(t) = \left[(1 - 2t)^{-1/2}\right]^n = (1 - 2t)^{-n/2}$$

这正是 $\mathrm{Gamma}(n/2, 1/2)$ 的 MGF。$\blacksquare$

#### 3.2.7 $t$ 分布（Student $t$ 分布） $t(n)$

- **定义**：设 $Z \sim N(0, 1)$，$V \sim \chi^2(n)$ 独立，则 $T = \dfrac{Z}{\sqrt{V/n}} \sim t(n)$。
- **PDF**：$f(t) = \dfrac{\Gamma((n+1)/2)}{\sqrt{n\pi}\,\Gamma(n/2)} \left(1 + \dfrac{t^2}{n}\right)^{-(n+1)/2}$。
- **期望**：$E[T] = 0$（$n > 1$）。
- **方差**：$\mathrm{Var}(T) = \dfrac{n}{n-2}$（$n > 2$）。
- 当 $n \to \infty$ 时，$t(n) \to N(0, 1)$。

#### 3.2.8 $F$ 分布 $F(m, n)$

- **定义**：设 $U \sim \chi^2(m)$，$V \sim \chi^2(n)$ 独立，则 $F = \dfrac{U/m}{V/n} \sim F(m, n)$。
- **期望**：$E[F] = \dfrac{n}{n-2}$（$n > 2$）。
- **关系**：若 $F \sim F(m, n)$，则 $1/F \sim F(n, m)$。

### 3.3 重要推导：Poisson 逼近二项分布

**定理（Poisson 逼近定理）**：设 $X_n \sim B(n, p_n)$，其中 $n p_n = \lambda$（常数），则

$$\lim_{n \to \infty} P(X_n = k) = \frac{e^{-\lambda} \lambda^k}{k!}$$

即 $X_n \xrightarrow{d} P(\lambda)$。

**证明**：

$$P(X_n = k) = \binom{n}{k} p_n^k (1-p_n)^{n-k}$$
$$= \frac{n(n-1)\cdots(n-k+1)}{k!} \left(\frac{\lambda}{n}\right)^k \left(1 - \frac{\lambda}{n}\right)^{n-k}$$
$$= \frac{\lambda^k}{k!} \cdot \frac{n(n-1)\cdots(n-k+1)}{n^k} \cdot \left(1 - \frac{\lambda}{n}\right)^{n} \cdot \left(1 - \frac{\lambda}{n}\right)^{-k}$$

逐项取极限（$n \to \infty$）：
- $\dfrac{n(n-1)\cdots(n-k+1)}{n^k} \to 1$（$k$ 固定）；
- $\left(1 - \dfrac{\lambda}{n}\right)^n \to e^{-\lambda}$；
- $\left(1 - \dfrac{\lambda}{n}\right)^{-k} \to 1$。

故 $\lim_{n \to \infty} P(X_n = k) = \dfrac{\lambda^k}{k!} e^{-\lambda}$。$\blacksquare$

### 3.4 正态分布与 $\chi^2$ 分布的关系

**定理**：设 $X \sim N(\mu, \sigma^2)$，则 $\dfrac{X - \mu}{\sigma} \sim N(0, 1)$，且

$$\sum_{i=1}^n \left(\frac{X_i - \mu}{\sigma}\right)^2 \sim \chi^2(n)$$

若用样本均值 $\bar{X}$ 代替 $\mu$，则

$$\sum_{i=1}^n \left(\frac{X_i - \bar{X}}{\sigma}\right)^2 \sim \chi^2(n-1)$$

自由度减少 1 是因为 $\bar{X}$ 用掉了一个自由度。

**Cochran 定理**：更一般地，若 $X_1, \ldots, X_n$ i.i.d. $N(\mu, \sigma^2)$，$\bar{X}$ 为样本均值，$S^2 = \frac{1}{n-1}\sum_{i=1}^n (X_i - \bar{X})^2$ 为样本方差，则：

1. $\bar{X} \sim N(\mu, \sigma^2/n)$；
2. $\dfrac{(n-1)S^2}{\sigma^2} \sim \chi^2(n-1)$；
3. $\bar{X}$ 与 $S^2$ 独立。

### 3.5 分布的特征化

**定理（指数分布的无记忆性特征化）**：若 $X$ 是非负连续型随机变量且具有无记忆性 $P(X > s+t | X > s) = P(X > t)$，则 $X$ 服从指数分布。

**证明**：令 $G(t) = P(X > t)$。无记忆性意味着 $G(s+t) = G(s)G(t)$。由于 $G$ 单调不增、右连续且 $G(0) = 1$，Cauchy 函数方程 $G(s+t) = G(s)G(t)$ 的唯一解为 $G(t) = e^{-\lambda t}$（$\lambda \geq 0$）。故 $X \sim \mathrm{Exp}(\lambda)$。$\blacksquare$

**定理（Poisson 过程的特征化）**：$N(t)$ 是参数为 $\lambda$ 的 Poisson 过程，当且仅当：
1. $N(0) = 0$；
2. $N(t)$ 具有独立增量；
3. $N(t)$ 具有平稳增量；
4. $P(N(h) = 1) = \lambda h + o(h)$，$P(N(h) \geq 2) = o(h)$。
