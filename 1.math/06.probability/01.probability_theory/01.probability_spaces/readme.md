# 第一章 概率空间

## 1. 几何意义

### 1.1 样本空间的几何直觉

概率空间 $(\Omega, \mathcal{F}, P)$ 是现代概率论的基石，其几何意义可从以下三个层面理解：

- **样本空间 $\Omega$**：可以想象为一个"全集"，即所有可能结果的总和。例如掷骰子的样本空间 $\Omega = \{1, 2, 3, 4, 5, 6\}$，在几何上可以看作一个包含 6 个点的集合。对于连续情形，$\Omega$ 可以是 $\mathbb{R}^n$ 的某个子集。

- **事件 $\sigma$-代数 $\mathcal{F}$**：$\mathcal{F}$ 是 $\Omega$ 的子集族，几何上它规定了"哪些子集是可以测量的"。可以类比为一个"尺子"——只有被 $\mathcal{F}$ 包含的集合才能被赋予概率（长度/面积/体积）。对于不可测集（如 Vitali 集合），我们无法为其定义概率。

- **概率测度 $P$**：$P$ 是从 $\mathcal{F}$ 到 $[0, 1]$ 的映射。几何上，可以将 $P(A)$ 理解为事件 $A$ 在整个样本空间中所占的"比例"或"体积"。在连续均匀分布中，$P(A)$ 就是集合 $A$ 的 Lebesgue 测度与 $\Omega$ 的 Lebesgue 测度之比。

### 1.2 条件概率的几何图示

条件概率 $P(A|B)$ 的几何意义可以理解为：在已知事件 $B$ 发生的条件下，样本空间从 $\Omega$ "缩小"到 $B$，而 $P(A|B)$ 就是 $A \cap B$ 相对于 $B$ 的比例：

$$P(A|B) = \frac{P(A \cap B)}{P(B)}$$

这可以类比于面积比：在一个矩形（样本空间 $\Omega$）中，$B$ 是一个子区域，$A \cap B$ 是 $B$ 中属于 $A$ 的部分。条件概率就是 $A \cap B$ 的面积与 $B$ 的面积之比。

### 1.3 独立性的几何含义

两个事件 $A$ 和 $B$ 独立，当且仅当 $P(A \cap B) = P(A)P(B)$。在几何上，这意味着 $A$ 在 $B$ 内的"密度"与 $A$ 在整个空间中的"密度"相同——$B$ 的发生不影响 $A$ 的发生概率，就如同一个矩形的两个维度的切割是正交的。

---

## 2. 应用场景

### 2.1 基础概率模型

- **古典概型（等可能概型）**：掷骰子、抽扑克牌、彩票中奖概率计算。
- **几何概型**：随机投点问题（Buffon 投针问题）、会面问题（两人在 $[0, T]$ 内随机到达，求会面概率）。

### 2.2 条件概率与 Bayes 公式的应用

- **医疗诊断**：已知某种疾病的患病率、检测的灵敏度（真阳性率）和特异度（真阴性率），利用 Bayes 公式计算检测结果为阳性时实际患病的概率。
- **垃圾邮件过滤（朴素 Bayes）**：基于邮件中各关键词的出现频率，利用 Bayes 公式判断邮件是垃圾邮件的概率。
- **机器学习**：Bayes 分类器、最大后验估计（MAP）、贝叶斯推断。

### 2.3 Borel-Cantelli 引理的应用

- **无限次试验中的必然事件**：判断某一事件序列中"无穷多次发生"的概率。例如，在独立抛硬币中，"正面出现无穷多次"的概率为 1（由第二 Borel-Cantelli 引理）。
- **可靠性分析**：判断系统在长时间运行中故障事件的累积行为。

---

## 3. 数学理论（及推导）

### 3.1 样本空间与事件

**定义 3.1.1（样本空间）**：随机试验的所有可能结果构成的集合称为**样本空间**，记为 $\Omega$。$\Omega$ 中的每个元素称为**样本点**，记为 $\omega$。

**定义 3.1.2（事件）**：样本空间的子集称为**事件**。特别地，$\Omega$ 称为**必然事件**，$\emptyset$ 称为**不可能事件**。

### 3.2 $\sigma$-代数

**定义 3.2.1（$\sigma$-代数）**：设 $\Omega$ 为样本空间，$\mathcal{F}$ 是 $\Omega$ 的某些子集构成的集族。若 $\mathcal{F}$ 满足以下条件，则称 $\mathcal{F}$ 为 $\Omega$ 上的一个 $\sigma$-代数：

1. $\Omega \in \mathcal{F}$；
2. 若 $A \in \mathcal{F}$，则 $A^c = \Omega \setminus A \in \mathcal{F}$（对补封闭）；
3. 若 $A_1, A_2, \ldots \in \mathcal{F}$，则 $\displaystyle\bigcup_{n=1}^{\infty} A_n \in \mathcal{F}$（对可数并封闭）。

**推论**：由 De Morgan 律，$\mathcal{F}$ 也对可数交封闭：$\displaystyle\bigcap_{n=1}^{\infty} A_n \in \mathcal{F}$。

**常见的 $\sigma$-代数**：

- **平凡 $\sigma$-代数**：$\mathcal{F} = \{\emptyset, \Omega\}$。
- **幂集 $\sigma$-代数**：$\mathcal{F} = 2^\Omega$（$\Omega$ 的所有子集）。当 $\Omega$ 为有限集或可数集时常采用。
- **Borel $\sigma$-代数**：$\mathcal{B}(\mathbb{R})$ 是由 $\mathbb{R}$ 的所有开集生成的 $\sigma$-代数，包含所有开集、闭集、可数集等。

### 3.3 概率的公理化定义（Kolmogorov 公理）

**定义 3.3.1（概率空间）**：三元组 $(\Omega, \mathcal{F}, P)$ 称为**概率空间**，其中：
- $\Omega$ 是样本空间；
- $\mathcal{F}$ 是 $\Omega$ 上的 $\sigma$-代数；
- $P: \mathcal{F} \to [0, 1]$ 是满足以下 Kolmogorov 公理的测度：

**Kolmogorov 公理**：

1. **非负性**：对任意 $A \in \mathcal{F}$，$P(A) \geq 0$；
2. **规范性**：$P(\Omega) = 1$；
3. **可数可加性（$\sigma$-可加性）**：若 $A_1, A_2, \ldots \in \mathcal{F}$ 两两互不相交（即 $A_i \cap A_j = \emptyset$，$i \neq j$），则
$$P\left(\bigcup_{n=1}^{\infty} A_n\right) = \sum_{n=1}^{\infty} P(A_n)$$

### 3.4 概率的基本性质（推导）

**性质 3.4.1**：$P(\emptyset) = 0$。

**证明**：由可数可加性，令 $A_1 = A_2 = \cdots = \emptyset$，则

$$P(\emptyset) = P\left(\bigcup_{n=1}^{\infty} \emptyset\right) = \sum_{n=1}^{\infty} P(\emptyset)$$

由于 $P(\emptyset) \geq 0$ 且 $P(\emptyset) = \sum_{n=1}^{\infty} P(\emptyset)$，要使等式成立，只能有 $P(\emptyset) = 0$。$\blacksquare$

**性质 3.4.2（有限可加性）**：若 $A_1, A_2, \ldots, A_n \in \mathcal{F}$ 两两互不相交，则

$$P\left(\bigcup_{k=1}^{n} A_k\right) = \sum_{k=1}^{n} P(A_k)$$

**证明**：令 $A_{n+1} = A_{n+2} = \cdots = \emptyset$，由可数可加性：

$$P\left(\bigcup_{k=1}^{n} A_k\right) = P\left(\bigcup_{k=1}^{\infty} A_k\right) = \sum_{k=1}^{\infty} P(A_k) = \sum_{k=1}^{n} P(A_k) + \sum_{k=n+1}^{\infty} P(\emptyset) = \sum_{k=1}^{n} P(A_k) \quad \blacksquare$$

**性质 3.4.3（对补公式）**：对任意 $A \in \mathcal{F}$，$P(A^c) = 1 - P(A)$。

**证明**：$A \cup A^c = \Omega$ 且 $A \cap A^c = \emptyset$，故 $P(A) + P(A^c) = P(\Omega) = 1$。$\blacksquare$

**性质 3.4.4（单调性）**：若 $A \subseteq B$，则 $P(A) \leq P(B)$。

**证明**：$B = A \cup (B \setminus A)$，且 $A \cap (B \setminus A) = \emptyset$，故

$$P(B) = P(A) + P(B \setminus A) \geq P(A) \quad \blacksquare$$

**性质 3.4.5（Boole 不等式 / 次可加性）**：对任意可数个事件 $A_1, A_2, \ldots \in \mathcal{F}$，

$$P\left(\bigcup_{n=1}^{\infty} A_n\right) \leq \sum_{n=1}^{\infty} P(A_n)$$

**证明**：定义 $B_1 = A_1$，$B_n = A_n \setminus \left(\bigcup_{k=1}^{n-1} A_k\right)$（$n \geq 2$）。则 $B_n$ 两两互不相交，$\bigcup_{n=1}^{\infty} B_n = \bigcup_{n=1}^{\infty} A_n$，且 $B_n \subseteq A_n$。由可数可加性和单调性：

$$P\left(\bigcup_{n=1}^{\infty} A_n\right) = P\left(\bigcup_{n=1}^{\infty} B_n\right) = \sum_{n=1}^{\infty} P(B_n) \leq \sum_{n=1}^{\infty} P(A_n) \quad \blacksquare$$

**性质 3.4.6（连续性定理）**：若 $A_1 \supseteq A_2 \supseteq \cdots$（单调递减）且 $\bigcap_{n=1}^{\infty} A_n = A$，则

$$\lim_{n \to \infty} P(A_n) = P(A)$$

类似地，若 $A_1 \subseteq A_2 \subseteq \cdots$（单调递增），则

$$\lim_{n \to \infty} P(A_n) = P\left(\bigcup_{n=1}^{\infty} A_n\right)$$

**证明**（递减情形）：令 $B_n = A_n \setminus A_{n+1}$（$n \geq 1$），则 $B_n$ 两两互不相交，且

$$A_1 = \left(\bigcup_{n=1}^{\infty} B_n\right) \cup A, \quad A_n = \left(\bigcup_{k=n}^{\infty} B_k\right) \cup A$$

由可数可加性：$P(A_1) = \sum_{k=1}^{\infty} P(B_k) + P(A)$，故

$$P(A_n) = \sum_{k=n}^{\infty} P(B_k) + P(A)$$

当 $n \to \infty$ 时，$\sum_{k=n}^{\infty} P(B_k) \to 0$（因为级数收敛），故 $\lim_{n \to \infty} P(A_n) = P(A)$。$\blacksquare$

**性质 3.4.7（容斥原理 / Inclusion-Exclusion Principle）**：对有限个事件 $A_1, A_2, \ldots, A_n$，

$$P\left(\bigcup_{k=1}^{n} A_k\right) = \sum_{k=1}^{n} P(A_k) - \sum_{1 \leq i < j \leq n} P(A_i \cap A_j) + \sum_{1 \leq i < j < k \leq n} P(A_i \cap A_j \cap A_k) - \cdots + (-1)^{n+1} P\left(\bigcap_{k=1}^{n} A_k\right)$$

**证明**（$n=2$ 的情形）：$A_1 \cup A_2 = A_1 \cup (A_2 \setminus A_1)$，其中 $A_1$ 与 $A_2 \setminus A_1$ 互不相交，故

$$P(A_1 \cup A_2) = P(A_1) + P(A_2 \setminus A_1)$$

又 $A_2 = (A_2 \cap A_1) \cup (A_2 \setminus A_1)$，故 $P(A_2) = P(A_1 \cap A_2) + P(A_2 \setminus A_1)$，代入得

$$P(A_1 \cup A_2) = P(A_1) + P(A_2) - P(A_1 \cap A_2)$$

一般情形可用数学归纳法证明。$\blacksquare$

### 3.5 条件概率

**定义 3.5.1（条件概率）**：设 $(\Omega, \mathcal{F}, P)$ 为概率空间，$B \in \mathcal{F}$ 且 $P(B) > 0$。对任意 $A \in \mathcal{F}$，定义

$$P(A | B) = \frac{P(A \cap B)}{P(B)}$$

**命题 3.5.1**：固定 $B$（$P(B) > 0$），$P(\cdot | B)$ 是 $\mathcal{F}$ 上的一个概率测度。

**证明**：
1. 非负性：$P(A|B) = P(A \cap B)/P(B) \geq 0$；
2. 规范性：$P(\Omega|B) = P(\Omega \cap B)/P(B) = P(B)/P(B) = 1$；
3. 可数可加性：若 $A_1, A_2, \ldots$ 两两互不相交，则 $(A_i \cap B)$ 也两两互不相交，故

$$P\left(\bigcup_{n=1}^{\infty} A_n \bigg| B\right) = \frac{P\left(\left(\bigcup_{n=1}^{\infty} A_n\right) \cap B\right)}{P(B)} = \frac{\sum_{n=1}^{\infty} P(A_n \cap B)}{P(B)} = \sum_{n=1}^{\infty} P(A_n | B) \quad \blacksquare$$

### 3.6 乘法公式与全概率公式

**定理 3.6.1（乘法公式）**：设 $A_1, A_2, \ldots, A_n \in \mathcal{F}$ 且 $P(A_1 \cap A_2 \cap \cdots \cap A_{n-1}) > 0$，则

$$P(A_1 \cap A_2 \cap \cdots \cap A_n) = P(A_1) \cdot P(A_2|A_1) \cdot P(A_3|A_1 \cap A_2) \cdots P(A_n|A_1 \cap \cdots \cap A_{n-1})$$

**证明**：由条件概率的定义，$P(A_k | A_1 \cap \cdots \cap A_{k-1}) = P(A_1 \cap \cdots \cap A_k)/P(A_1 \cap \cdots \cap A_{k-1})$，逐项相乘即得。$\blacksquare$

**定理 3.6.2（全概率公式）**：设 $B_1, B_2, \ldots$ 是 $\Omega$ 的一个划分（即 $B_i$ 两两互不相交，$\bigcup_{i=1}^{\infty} B_i = \Omega$），且 $P(B_i) > 0$，则对任意 $A \in \mathcal{F}$，

$$P(A) = \sum_{i=1}^{\infty} P(A|B_i) \cdot P(B_i)$$

**证明**：$A = A \cap \Omega = A \cap \left(\bigcup_{i=1}^{\infty} B_i\right) = \bigcup_{i=1}^{\infty}(A \cap B_i)$。由于 $B_i$ 互不相交，$A \cap B_i$ 也互不相交，由可数可加性：

$$P(A) = \sum_{i=1}^{\infty} P(A \cap B_i) = \sum_{i=1}^{\infty} P(A|B_i) \cdot P(B_i) \quad \blacksquare$$

### 3.7 Bayes 公式（推导）

**定理 3.7.1（Bayes 公式）**：在定理 3.6.2 的条件下，对任意 $j$ 使得 $P(B_j) > 0$，

$$P(B_j | A) = \frac{P(A | B_j) \cdot P(B_j)}{\sum_{i=1}^{\infty} P(A | B_i) \cdot P(B_i)}$$

**证明**：由条件概率的定义和全概率公式：

$$P(B_j | A) = \frac{P(A \cap B_j)}{P(A)} = \frac{P(A|B_j) \cdot P(B_j)}{P(A)} = \frac{P(A|B_j) \cdot P(B_j)}{\sum_{i=1}^{\infty} P(A|B_i) \cdot P(B_i)} \quad \blacksquare$$

Bayes 公式是贝叶斯统计学的核心，其中：
- $P(B_j)$ 称为**先验概率**（prior）；
- $P(A|B_j)$ 称为**似然**（likelihood）；
- $P(B_j|A)$ 称为**后验概率**（posterior）；
- $\sum_{i} P(A|B_i) \cdot P(B_i)$ 是归一化常数（证据，evidence）。

### 3.8 独立性

**定义 3.8.1（两个事件的独立性）**：两个事件 $A$ 和 $B$ 称为**独立的**（independent），若

$$P(A \cap B) = P(A) \cdot P(B)$$

**定义 3.8.2（多个事件的独立性）**：事件 $A_1, A_2, \ldots, A_n$ 称为**相互独立的**，若对任意 $k \geq 2$ 和任意 $1 \leq i_1 < i_2 < \cdots < i_k \leq n$，均有

$$P(A_{i_1} \cap A_{i_2} \cap \cdots \cap A_{i_k}) = P(A_{i_1}) \cdot P(A_{i_2}) \cdots P(A_{i_k})$$

**注**：相互独立要求所有组合都满足乘法公式，而**两两独立**仅要求任意两个事件独立。两两独立不蕴含相互独立。

**反例**：设 $\Omega = \{1, 2, 3, 4\}$，每个基本事件的概率为 $1/4$。令

$$A = \{1, 2\}, \quad B = \{1, 3\}, \quad C = \{1, 4\}$$

则 $P(A) = P(B) = P(C) = 1/2$，$P(A \cap B) = P(\{1\}) = 1/4 = P(A)P(B)$，类似地 $A$ 与 $C$、$B$ 与 $C$ 均两两独立。但

$$P(A \cap B \cap C) = P(\{1\}) = \frac{1}{4} \neq \frac{1}{8} = P(A)P(B)P(C)$$

故 $A, B, C$ 两两独立但不相互独立。

### 3.9 Borel-Cantelli 引理

**引理 3.9.1（第一 Borel-Cantelli 引理）**：设 $A_1, A_2, \ldots \in \mathcal{F}$ 且 $\sum_{n=1}^{\infty} P(A_n) < \infty$，则

$$P\left(\limsup_{n \to \infty} A_n\right) = P\left(\bigcap_{n=1}^{\infty} \bigcup_{k=n}^{\infty} A_k\right) = 0$$

即 $A_n$ "无穷多次发生"的概率为零。

**证明**：令 $B = \limsup_{n \to \infty} A_n = \bigcap_{n=1}^{\infty} \bigcup_{k=n}^{\infty} A_k$。对任意 $n$，$B \subseteq \bigcup_{k=n}^{\infty} A_k$，故由单调性和次可加性：

$$P(B) \leq P\left(\bigcup_{k=n}^{\infty} A_k\right) \leq \sum_{k=n}^{\infty} P(A_k)$$

由于 $\sum_{k=1}^{\infty} P(A_k)$ 收敛，其尾部 $\sum_{k=n}^{\infty} P(A_k) \to 0$（$n \to \infty$）。取极限得 $P(B) = 0$。$\blacksquare$

**引理 3.9.2（第二 Borel-Cantelli 引理）**：设 $A_1, A_2, \ldots \in \mathcal{F}$ **相互独立**且 $\sum_{n=1}^{\infty} P(A_n) = \infty$，则

$$P\left(\limsup_{n \to \infty} A_n\right) = 1$$

即 $A_n$ "无穷多次发生"的概率为一。

**证明**：只需证明对任意 $m$，$P\left(\bigcup_{k=m}^{\infty} A_k\right) = 1$。利用对偶性：

$$P\left(\bigcup_{k=m}^{\infty} A_k\right)^c = P\left(\bigcap_{k=m}^{\infty} A_k^c\right)$$

由独立性：

$$P\left(\bigcap_{k=m}^{n} A_k^c\right) = \prod_{k=m}^{n} P(A_k^c) = \prod_{k=m}^{n} (1 - P(A_k))$$

利用不等式 $1 - x \leq e^{-x}$（对 $x \geq 0$）：

$$\prod_{k=m}^{n} (1 - P(A_k)) \leq \prod_{k=m}^{n} e^{-P(A_k)} = \exp\left(-\sum_{k=m}^{n} P(A_k)\right)$$

由于 $\sum_{k=1}^{\infty} P(A_k) = \infty$，$\sum_{k=m}^{n} P(A_k) \to \infty$（$n \to \infty$），故

$$\lim_{n \to \infty} P\left(\bigcap_{k=m}^{n} A_k^c\right) = 0$$

由概率的连续性，$P\left(\bigcap_{k=m}^{\infty} A_k^c\right) = 0$，故 $P\left(\bigcup_{k=m}^{\infty} A_k\right) = 1$。由 $m$ 的任意性，$P(\limsup_{n \to \infty} A_n) = 1$。$\blacksquare$

**推论（Borel 零一律的特例）**：若 $A_1, A_2, \ldots$ 相互独立，则 $P(\limsup A_n)$ 要么为 $0$ 要么为 $1$（即 $\{A_n \text{ i.o.}\}$ 是一个 tail 事件，其概率为 0 或 1）。
