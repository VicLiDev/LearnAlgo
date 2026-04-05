# 数论（Number Theory）

研究整数性质与规律的学科，被誉为"数学女王"。

## 子学科

| 学科     | 英文名                       | 核心内容                                            | 难度  |
|----------|------------------------------|-----------------------------------------------------|-------|
| 初等数论 | Elementary Number Theory     | 整除性、素数、同余、中国剩余定理                    | ★★☆☆☆ |
| 解析数论 | Analytic Number Theory       | Riemann Zeta函数、素数定理、Dirichlet级数           | ★★★★★ |
| 代数数论 | Algebraic Number Theory      | 数域、代数整数、理想、类域论                        | ★★★★★ |
| 计算数论 | Computational Number Theory  | 素性测试、大数分解、离散对数                        | ★★★★☆ |
| 超越数论 | Transcendental Number Theory | 超越性证明（$e$, $\pi$）、Lindemann-Weierstrass定理 | ★★★★★ |

## 适用场景

RSA密码学、哈希函数、伪随机数生成、编码理论。

## 核心公式

- Euler函数：$\varphi(n) = n \prod_{p|n}(1 - \frac{1}{p})$
- Fermat小定理：$a^{p-1} \equiv 1 \pmod{p}$（$p$ 为素数，$\gcd(a,p)=1$）
- 二次互反律（Legendre符号）：$\left(\frac{p}{q}\right)\left(\frac{q}{p}\right) = (-1)^{\frac{(p-1)(q-1)}{4}}$
