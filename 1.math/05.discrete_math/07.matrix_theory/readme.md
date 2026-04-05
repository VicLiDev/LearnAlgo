# 矩阵论（Matrix Theory）

难度：★★★★☆

矩阵论是线性代数的高阶延伸，严格归类属于代数学分支，同时与泛函分析和数值分析深度交叉，在机器学习、图像处理、控制论等领域有广泛应用。

## 目录

| 章节                                       | 主题                 | 核心内容                                                      |
|--------------------------------------------|----------------------|---------------------------------------------------------------|
| [01](./01.linear_transformations/)         | 矩阵基础与线性变换   | 矩阵运算、逆矩阵、分块矩阵、秩、迹                            |
| [02](./02.eigenvalues_eigenvectors/)       | 特征值与特征向量     | 特征方程、Gershgorin圆盘、Rayleigh商、Courant-Fischer定理     |
| [03](./03.jordan_form/)                    | Jordan标准型         | 对角化、广义特征向量、极小多项式、矩阵幂计算                  |
| [04](./04.lu_cholesky_decomposition/)      | LU分解与Cholesky分解 | Doolittle算法、选主元、正定矩阵分解、Schur补                  |
| [05](./05.qr_decomposition/)               | QR分解               | Gram-Schmidt、Householder变换、Givens旋转、最小二乘           |
| [06](./06.svd/)                            | 奇异值分解（SVD）    | Eckart-Young定理、截断SVD、伪逆、低秩逼近                     |
| [07](./07.spectral_polar_decomposition/)   | 谱分解与极分解       | 谱定理、正规矩阵、矩阵平方根、极分解与SVD关系                 |
| [08](./08.matrix_norms/)                   | 向量范数与矩阵范数   | 诱导范数、Frobenius范数、条件数、误差放大分析                 |
| [09](./09.generalized_inverse/)            | 矩阵的广义逆         | Moore-Penrose伪逆、Penrose方程、正交投影、Tikhonov正则化      |
| [10](./10.matrix_functions/)               | 矩阵函数             | 矩阵指数、矩阵对数、Jordan块上的函数演算                      |
| [11](./11.matrix_calculus/)                | 矩阵微积分           | 梯度与Jacobian、矩阵微分法则、链式法则、最小二乘梯度          |
| [12](./12.positive_definite_inequalities/) | 正定矩阵与矩阵不等式 | Sylvester准则、Schur补、Lyapunov方程、Loewner序               |
| [13](./13.kronecker_vec/)                  | Kronecker积与向量化  | Kronecker积性质、vec恒等式、Sylvester方程向量化、Khatri-Rao积 |

## 章节依赖关系

```
01 线性变换 ──┬──> 02 特征值 ──> 03 Jordan标准型
              │                    │
              │                    └──> 10 矩阵函数
              │
              ├──> 04 LU/Cholesky
              │
              ├──> 05 QR ──> 06 SVD ──> 07 谱分解/极分解 ──> 09 广义逆
              │                                      │
              └──> 08 范数 <─────────────────────────┘
                               │
                               └──> 12 正定矩阵与不等式

01 ──> 11 矩阵微积分
01 ──> 13 Kronecker积与向量化
```

## 参考教材

- 《Matrix Analysis》 — Roger A. Horn, Charles R. Johnson
- 《Matrix Computations》 — Gene H. Golub, Charles F. Van Loan
