# 第一章 矩阵基础与线性变换

## 1. 几何意义

矩阵最本质的几何含义是**线性变换**——对空间进行拉伸、旋转、剪切、投影等操作。

### 基本变换的几何图像

| 变换类型 | 矩阵形式 | 几何效果 |
|----------|----------|----------|
| 缩放 | $\begin{pmatrix} s_x & 0 \\ 0 & s_y \end{pmatrix}$ | 沿坐标轴方向拉伸或压缩 |
| 旋转 | $\begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$ | 绕原点逆时针旋转 $\theta$ 角 |
| 剪切 | $\begin{pmatrix} 1 & k \\ 0 & 1 \end{pmatrix}$ | 水平剪切，$y$ 坐标越大偏移越大 |
| 反射 | $\begin{pmatrix} \cos 2\theta & \sin 2\theta \\ \sin 2\theta & -\cos 2\theta \end{pmatrix}$ | 关于过原点方向角 $\theta$ 的直线做镜像 |
| 投影 | $\begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$ | 投影到 $x$ 轴 |

**核心直觉**：矩阵 $A \in \mathbb{R}^{m \times n}$ 将 $\mathbb{R}^n$ 中的向量映射到 $\mathbb{R}^m$。矩阵乘法 $y = Ax$ 就是把输入空间中的每一个基向量，按照矩阵列所指定的方式，"搬"到输出空间中去。

### 列空间与零空间

- **列空间（Column Space）** $\text{Col}(A)$：$A$ 的列向量的所有线性组合，即变换后能到达的所有点的集合。几何上是一个 $\text{rank}(A)$ 维的子空间。
- **零空间（Null Space）** $\text{Nul}(A)$：满足 $Ax = 0$ 的所有 $x$ 的集合。几何上是被变换"压扁"到原点的所有方向。

### 行列式的几何意义

对于方阵 $A \in \mathbb{R}^{n \times n}$，行列式 $\det(A)$ 表示变换后单位超立方体的**有向体积**的缩放因子：

- $|\det(A)|$：体积缩放倍数
- $\det(A) > 0$：保持空间定向（不翻转）
- $\det(A) < 0$：翻转空间定向（镜像）
- $\det(A) = 0$：降维（至少一个方向被压扁为零）

---

## 2. 应用场景

| 领域 | 应用 |
|------|------|
| 计算机图形学 | 旋转、平移、缩放、投影变换构成渲染管线的基础 |
| 机器人学 | 正运动学（DH参数矩阵连乘）和逆运动学 |
| 机器学习 | 权重矩阵 $W$ 实现特征空间的线性映射 $h = Wx + b$ |
| 信号处理 | 线性时不变系统的输入输出关系 $y(t) = h(t) * x(t)$ |
| 量子计算 | 量子门（酉矩阵）对量子态的演化 $|\psi'\rangle = U|\psi\rangle$ |

---

## 3. 数学理论

### 3.1 矩阵的定义与运算

**定义**：$m \times n$ 矩阵 $A$ 是由 $mn$ 个标量排成的 $m$ 行 $n$ 列的矩形阵列：

$$A = (a_{ij})_{m \times n} = \begin{pmatrix} a_{11} & a_{12} & \cdots & a_{1n} \\ a_{21} & a_{22} & \cdots & a_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ a_{m1} & a_{m2} & \cdots & a_{mn} \end{pmatrix}$$

**基本运算**：

- 加法：$(A + B)_{ij} = a_{ij} + b_{ij}$，要求 $A, B$ 同阶
- 数乘：$(\alpha A)_{ij} = \alpha \cdot a_{ij}$
- 矩阵乘法：$(AB)_{ij} = \sum_{k=1}^{n} a_{ik} b_{kj}$，要求 $A$ 的列数等于 $B$ 的行数

**矩阵乘法的结合律证明**：

设 $A \in \mathbb{R}^{m \times n}$，$B \in \mathbb{R}^{n \times p}$，$C \in \mathbb{R}^{p \times q}$，考察 $(AB)C$ 与 $A(BC)$ 的第 $(i,j)$ 元素。

$$[(AB)C]_{ij} = \sum_{l=1}^{p} (AB)_{il} c_{lj} = \sum_{l=1}^{p} \sum_{k=1}^{n} a_{ik} b_{kl} c_{lj}$$

$$[A(BC)]_{ij} = \sum_{k=1}^{n} a_{ik} (BC)_{kj} = \sum_{k=1}^{n} a_{ik} \sum_{l=1}^{p} b_{kl} c_{lj} = \sum_{k=1}^{n} \sum_{l=1}^{p} a_{ik} b_{kl} c_{lj}$$

两者均为有限和，交换求和顺序即得 $(AB)C = A(BC)$。

**注意**：矩阵乘法一般**不可交换**，即 $AB \neq BA$。

### 3.2 转置与共轭转置

$$A^T_{ij} = A_{ji}$$

$$A^H_{ij} = \overline{A_{ji}} \quad \text{（共轭转置，Hermitian转置）}$$

**性质**：
- $(AB)^T = B^T A^T$（顺序反转）
- $(A + B)^T = A^T + B^T$
- $(A^T)^T = A$

**推导** $(AB)^T = B^T A^T$：

$$[(AB)^T]_{ij} = (AB)_{ji} = \sum_{k} a_{jk} b_{ki} = \sum_{k} (B^T)_{ik} (A^T)_{kj} = (B^T A^T)_{ij}$$

### 3.3 逆矩阵

**定义**：方阵 $A$ 可逆，若存在 $A^{-1}$ 使得 $AA^{-1} = A^{-1}A = I$。

**可逆的等价条件**（$A \in \mathbb{R}^{n \times n}$）：

以下命题相互等价：
1. $A$ 可逆
2. $\det(A) \neq 0$
3. $\text{rank}(A) = n$（满秩）
4. $Ax = 0$ 仅有零解
5. $Ax = b$ 对任意 $b$ 有唯一解
6. $A$ 的行（列）向量线性无关
7. $A^T$ 可逆
8. 零空间 $\text{Nul}(A) = \{0\}$
9. 列空间 $\text{Col}(A) = \mathbb{R}^n$

**逆矩阵公式**（$2 \times 2$ 特例）：

$$A = \begin{pmatrix} a & b \\ c & d \end{pmatrix}, \quad A^{-1} = \frac{1}{ad - bc}\begin{pmatrix} d & -b \\ -c & a \end{pmatrix}$$

**一般逆矩阵公式（伴随矩阵法）**：

$$A^{-1} = \frac{1}{\det(A)} \text{adj}(A), \quad \text{adj}(A)_{ij} = (-1)^{i+j} M_{ji}$$

其中 $M_{ji}$ 是去掉第 $j$ 行第 $i$ 列后的余子式。

### 3.4 分块矩阵

将矩阵划分为若干子块，以子块为基本单元进行运算。

**分块乘法**：若 $A = \begin{pmatrix} A_{11} & A_{12} \\ A_{21} & A_{22} \end{pmatrix}$，$B = \begin{pmatrix} B_{11} & B_{12} \\ B_{21} & B_{22} \end{pmatrix}$，分块相容，则

$$AB = \begin{pmatrix} A_{11}B_{11} + A_{12}B_{21} & A_{11}B_{12} + A_{12}B_{22} \\ A_{21}B_{11} + A_{22}B_{21} & A_{21}B_{12} + A_{22}B_{22} \end{pmatrix}$$

**分块矩阵求逆公式**（Schur补）：

$$\begin{pmatrix} A & B \\ C & D \end{pmatrix}^{-1} = \begin{pmatrix} (A - BD^{-1}C)^{-1} & -(A-BD^{-1}C)^{-1}BD^{-1} \\ -D^{-1}C(A-BD^{-1}C)^{-1} & (D - CA^{-1}B)^{-1} \end{pmatrix}$$

其中 $S = A - BD^{-1}C$ 称为 **Schur补**。

### 3.5 矩阵的秩

**定义**：矩阵 $A$ 的秩 $\text{rank}(A)$ 是其列空间（或行空间）的维数，即线性无关的列（行）向量的最大个数。

**秩的基本性质**：

- $\text{rank}(A) = \text{rank}(A^T)$
- $\text{rank}(AB) \leq \min(\text{rank}(A), \text{rank}(B))$
- $\text{rank}(A + B) \leq \text{rank}(A) + \text{rank}(B)$
- **Sylvester秩不等式**：$\text{rank}(A) + \text{rank}(B) - n \leq \text{rank}(AB)$，其中 $A \in \mathbb{R}^{m \times n}$，$B \in \mathbb{R}^{n \times p}$
- **秩-零化度定理**：$\text{rank}(A) + \text{nullity}(A) = n$，其中 $\text{nullity}(A) = \dim(\text{Nul}(A))$

**Sylvester不等式推导**：

由秩-零化度定理，$\text{nullity}(B) = p - \text{rank}(B)$。

$B$ 的零空间中任意向量 $x$（满足 $Bx = 0$）经 $A$ 映射后 $ABx = 0$，故 $\text{Nul}(B) \subseteq \text{Nul}(AB)$。

$\text{nullity}(AB) \geq \text{nullity}(B)$

$\text{rank}(AB) = m - \text{nullity}(AB) \leq m - \text{nullity}(B) = m - p + \text{rank}(B)$

对 $B^T A^T$ 应用同样推理可得另一侧不等式，合并即得。

### 3.6 迹

**定义**：方阵 $A$ 的迹为其对角线元素之和：

$$\text{tr}(A) = \sum_{i=1}^{n} a_{ii}$$

**基本性质**：
- $\text{tr}(A + B) = \text{tr}(A) + \text{tr}(B)$
- $\text{tr}(\alpha A) = \alpha \cdot \text{tr}(A)$
- $\text{tr}(AB) = \text{tr}(BA)$（即使 $AB \neq BA$）
- $\text{tr}(A) = \text{tr}(A^T)$
- $\text{tr}(A) = \sum \lambda_i$（等于特征值之和）

**证明** $\text{tr}(AB) = \text{tr}(BA)$：

$$\text{tr}(AB) = \sum_{i} (AB)_{ii} = \sum_{i} \sum_{j} a_{ij} b_{ji} = \sum_{j} \sum_{i} b_{ji} a_{ij} = \sum_{j} (BA)_{jj} = \text{tr}(BA)$$
