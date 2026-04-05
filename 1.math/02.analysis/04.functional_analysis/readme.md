# 泛函分析（Functional Analysis）

难度：★★★★★

泛函分析是将线性代数推广到无穷维空间的核心数学分支。它以 Banach 空间和 Hilbert 空间为基本框架，以有界线性算子和谱理论为研究对象，是现代分析学、偏微分方程、量子力学等领域的数学基础。

## 章节目录

| 章节 | 标题 | 核心内容 |
|:---:|------|---------|
| 第一章 | [度量空间与完备性](01.metric_spaces/readme.md) | 度量、Cauchy 序列、完备性、Banach 不动点定理、完备化 |
| 第二章 | [赋范线性空间与 Banach 空间](02.banach_spaces/readme.md) | 范数、Banach 空间、等价范数定理、Riesz 引理、紧性 |
| 第三章 | [内积空间与 Hilbert 空间](03.hilbert_spaces/readme.md) | 内积、Cauchy-Schwarz 不等式、正交投影定理、Riesz 表示定理、Parseval 恒等式 |
| 第四章 | [有界线性算子](04.bounded_operators/readme.md) | 算子范数、B(X,Y)、连续性与有界性等价、线性泛函与对偶空间 |
| 第五章 | [三大基本定理](05.fundamental_theorems/readme.md) | 开映射定理、逆算子定理、闭图像定理、一致有界性原理 |
| 第六章 | [Hahn-Banach 定理](06.hahn_banach/readme.md) | 延拓定理（解析与几何形式）、凸集分离、泛函充分多 |
| 第七章 | [共轭空间与弱拓扑](07.dual_spaces/readme.md) | $L^p$ 的对偶、弱收敛、弱\*收敛、自反性、Alaoglu 定理 |
| 第八章 | [谱理论](08.spectral_theory/readme.md) | 谱的分类、谱半径公式、谱的非空性、Banach 代数 |
| 第九章 | [紧算子与 Fredholm 理论](09.compact_operators/readme.md) | 紧算子性质、Riesz-Schauder 理论、Fredholm 择一性、积分方程 |
| 第十章 | [无界算子与自伴算子](10.unbounded_operators/readme.md) | 稠定算子、对称与自伴、谱定理、Stone 定理、量子力学应用 |

## 依赖关系图

学习本课程时，建议按以下顺序进行。箭头 `A --> B` 表示 B 依赖 A 的内容：

```
第一章 (度量空间)
    |
    v
第二章 (Banach 空间) --> 第四章 (有界线性算子)
    |                          |
    v                          v
第三章 (Hilbert 空间) --> 第五章 (三大基本定理)
    |                          |
    v                          v
第六章 (Hahn-Banach)  --> 第七章 (共轭空间与弱拓扑)
                               |
                               v
                          第八章 (谱理论)
                               |
                               v
                     +---------+---------+
                     v                   v
              第九章 (紧算子)    第十章 (无界算子)
```

**详细依赖说明**：

- **第一章 -> 第二章**：度量空间是赋范空间的基础（范数诱导度量）
- **第二章 -> 第三章**：赋范空间是内积空间的一般化（内积诱导范数）
- **第二章 -> 第四章**：有界线性算子定义在赋范空间之间
- **第三章 -> 第四章**：Hilbert 空间上的算子有更丰富的结构（伴随算子、Riesz 表示）
- **第四章 -> 第五章**：三大基本定理的证明需要 B(X,Y) 的完备性和 Baire 纲定理
- **第二章 -> 第六章**：Hahn-Banach 延拓定理是赋范空间理论的核心
- **第四章 -> 第六章**：共轭空间 X* 的非平凡性依赖 Hahn-Banach
- **第六章 -> 第七章**：共轭空间的构造和弱拓扑的理论基础是 Hahn-Banach
- **第四章 -> 第八章**：谱理论是有界线性算子理论的深化
- **第八章 -> 第九章**：紧算子的谱理论是谱理论的特殊但最重要的情形
- **第八章 -> 第十章**：无界算子的谱定理推广了有界算子的谱定理
- **第五章 -> 第十章**：闭图像定理是无界算子理论的关键工具

## 核心知识脉络

```
空间结构:  度量空间 --> 赋范空间 --> 内积空间
           (距离)     (长度)     (角度/正交)

算子理论:  有界算子 --> 谱理论 --> 紧算子/无界算子
           (连续)     (特征值推广)

基本定理:  Hahn-Banach  |  开映射/逆算子/闭图像  |  一致有界性
           (延拓/分离)    (Banach空间结构)        (逐点 -> 一致)

拓扑结构:  强拓扑 --> 弱拓扑 --> 弱*拓扑
           (范数收敛)  (泛函探测)  (元素探测)
```

## 参考书籍

### 基础教材（入门推荐）

1. **Kreyszig**, *Introductory Functional Analysis with Applications*, Wiley
   - 最经典的基础教材，证明详尽，例题丰富，适合入门
   - 涵盖本书全部十章内容

2. **Conway**, *A Course in Functional Analysis*, Springer (GTM 96)
   - 标准研究生教材，内容全面，叙述简洁
   - 在 Hilbert 空间算子理论方面尤为出色

### 进阶参考

3. **Rudin**, *Functional Analysis*, McGraw-Hill
   - 视角现代，以分布理论和 Fourier 分析为出发点
   - 适合有一定基础后阅读

4. **Reed & Simon**, *Methods of Modern Mathematical Physics I: Functional Analysis*, Academic Press
   - 物理方向首选，强调泛函分析在量子力学中的应用
   - 第十章量子力学应用主要参考此书

5. **Yosida**, *Functional Analysis*, Springer (Grundlehren 123)
   - 内容极为全面，半群理论和无界算子理论方面权威
   - 适合作为工具书查阅

### 专题深入

6. **Lax**, *Functional Analysis*, Wiley
   - 兼顾理论与应用，包含许多经典问题的详细分析

7. **Kato**, *Perturbation Theory for Linear Operators*, Springer
   - 算子扰动理论的百科全书，第十章无界算子的主要参考

8. **Douglas**, *Banach Algebra Techniques in Operator Theory*, Springer (GTM 179)
   - 从 Banach 代数角度重新审视算子理论

## 预备知识

- **实分析**：测度论、Lebesgue 积分、$L^p$ 空间
- **线性代数**：向量空间、线性映射、特征值、内积空间
- **点集拓扑**：开集、闭集、紧性、度量空间的基本拓扑性质
- **复分析**：全纯函数、Laurent 级数、Liouville 定理（第八章谱理论需要）
