# 复变函数与积分变换

> Complex Analysis and Integral Transforms

难度：★★★★☆

本教程系统介绍复变函数论的核心理论与三种重要积分变换（Fourier 变换、Laplace 变换、Z 变换），涵盖从基础概念到高级应用的完整知识体系。每章均包含几何意义、应用场景和严格的数学理论推导。

---

## 目录

| 章节 | 标题 | 核心内容 |
|:---:|:---|:---|
| [第一章](./01.complex_numbers_functions/readme.md) | 复数与复变函数 | 复平面、Riemann 球面、复数运算、共轭与模、复变函数的极限与连续性 |
| [第二章](./02.analytic_functions/readme.md) | 解析函数 | 可导与解析、Cauchy-Riemann 方程推导、调和函数、共形映射初步 |
| [第三章](./03.elementary_functions/readme.md) | 初等解析函数 | 指数函数、对数函数（多值性、支割线）、三角函数、双曲函数、反三角函数 |
| [第四章](./04.complex_integration/readme.md) | 复积分与 Cauchy 积分定理 | 复积分定义、Cauchy-Goursat 定理证明、积分与路径无关、复合闭路定理 |
| [第五章](./05.cauchy_integral_formula/readme.md) | Cauchy 积分公式与解析函数性质 | Cauchy 积分公式证明、高阶导数公式、最大模原理、Liouville 定理、Schwarz 引理 |
| [第六章](./06.series_expansion/readme.md) | 级数展开 | 幂级数与收敛半径、Taylor 展开、Laurent 展开、奇点分类（可去/极点/本性） |
| [第七章](./07.residue_theorem/readme.md) | 留数定理及其应用 | 留数计算公式推导、留数定理证明、实积分计算、辐角原理、Rouche 定理 |
| [第八章](./08.conformal_mapping/readme.md) | 保形映射 | 保角条件、Möbius 变换、典型区域映射、Schwarz-Christoffel 变换、Riemann 映射定理 |
| [第九章](./09.fourier_transform/readme.md) | Fourier 变换 | Fourier 级数（复数形式）、变换性质、卷积定理、Parseval 定理、FFT |
| [第十章](./10.laplace_transform/readme.md) | Laplace 变换 | 定义与收敛域、微分/积分性质、卷积定理、逆变换、初值/终值定理、微分方程求解 |
| [第十一章](./11.z_transform/readme.md) | Z 变换 | 定义与收敛域、基本性质、逆 Z 变换、与 Laplace 变换关系、差分方程求解、DSP 应用 |

---

## 知识依赖关系

```
第1章 复数与复变函数
  |
  v
第2章 解析函数（C-R 方程）
  |
  +--> 第3章 初等解析函数
  |
  v
第4章 复积分与 Cauchy 积分定理
  |
  v
第5章 Cauchy 积分公式与解析函数性质
  |
  v
第6章 级数展开（Taylor / Laurent）
  |
  v
第7章 留数定理及其应用
  |     |
  |     v
  |   第8章 保形映射（依赖解析函数理论 + 留数定理）
  |
  +--> 第9章 Fourier 变换 --> 第10章 Laplace 变换 --> 第11章 Z 变换
  |       （积分变换主线，第10章依赖第9章，第11章依赖第10章）
  |
  +--> 第7章 留数定理也用于第9/10章逆变换的计算
```

**学习路径建议**：

1. **复变函数主线**（第1-8章）：按顺序学习，这是严格的逻辑链条。每一章都以前一章为基础。
2. **积分变换主线**（第9-11章）：需要先完成第1-7章（至少到留数定理），然后按顺序学习。第7章的留数定理是计算第9、10章逆变换的关键工具。
3. 第8章（保形映射）与第9-11章（积分变换）相对独立，可以按任意顺序学习。

---

## 参考书目

### 经典教材

1. **Lars V. Ahlfors**, *Complex Analysis* (3rd Edition), McGraw-Hill, 1979.
   - 复分析领域的经典名著，数学严谨性极高，适合深度学习。涵盖共形映射、Riemann 面等高级主题。

2. **John B. Conway**, *Functions of One Complex Variable I* (2nd Edition), Springer, 1978.
   - 研究生水平教材，理论体系完整，证明严格。

3. **E. T. Copson**, *An Introduction to the Theory of Functions of a Complex Variable*, Oxford University Press, 1935.
   - 经典英文教材，叙述清晰。

### 中文教材

4. **西安交通大学高等数学教研室**, *工程数学：复变函数* (第五版), 高等教育出版社.
   - 国内工程类广泛采用的教材，内容实用，配有丰富例题。

5. **钟玉泉**, *复变函数论* (第五版), 高等教育出版社.
   - 数学专业经典教材，理论体系完整，证明严格。

6. **余家荣**, *复变函数*, 高等教育出版社.
   - 适合数学专业，内容深入。

7. **陆启韶**, *复变函数与积分变换*, 高等教育出版社.
   - 面向工科，复变函数与积分变换合编。

### 积分变换专题

8. **A. V. Oppenheim, A. S. Willsky, S. H. Nawab**, *Signals and Systems* (2nd Edition), Prentice Hall, 1997.
   - 信号与系统领域的经典教材，Fourier 变换、Laplace 变换、Z 变换的系统论述。

9. **James S. Walker**, *Fast Fourier Transforms* (2nd Edition), CRC Press, 1996.
   - FFT 算法的专题论述。

10. **E. O. Brigham**, *The Fast Fourier Transform and Its Applications*, Prentice Hall, 1988.
    - FFT 的原理与应用并重。

### 进阶参考

11. **H. A. Priestley**, *Introduction to Complex Analysis* (2nd Edition), Oxford University Press, 2003.
    - 英文教材，适合本科高年级和研究生入门，讲解清晰。

12. **R. V. Churchill, J. W. Brown**, *Complex Variables and Applications* (9th Edition), McGraw-Hill, 2013.
    - 应用导向的复变函数教材，物理应用丰富。

13. **M. Ablowitz, A. Fokas**, *Complex Variables: Introduction and Applications* (2nd Edition), Cambridge University Press, 2003.
    - 强调在科学和工程中的应用。

---

## 内容特色

- **几何直觉优先**：每章第一节均从几何意义出发，建立直观理解。
- **理论推导完整**：核心定理给出完整或详细的证明思路（如 Cauchy-Goursat 定理、Taylor/Laurent 展开、留数定理等）。
- **应用驱动**：每章第二节展示理论在物理、工程、信号处理等领域的实际应用。
- **LaTeX 公式规范**：所有数学公式使用标准 LaTeX 记号。
