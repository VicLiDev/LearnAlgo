# ICP (Iterative Closest Point)

## 1. 简介

ICP 是最经典的点云配准算法，用于将两个点云对齐。通过迭代寻找对应点并计算最优变换，使源点云逼近目标点云。

## 2. 算法流程

```
输入: 源点云 P, 目标点云 Q
输出: 变换矩阵 R, t

1. 初始化变换 T = I (单位矩阵)
2. 重复直到收敛:
   a. 应用当前变换: P' = T * P
   b. 对 P' 中每个点，在 Q 中找最近点
   c. 计算最优变换 T* 最小化 ||T*P' - Q||
   d. 更新 T = T* * T
3. 返回最终变换 T
```

## 3. 数学原理

### 3.1 最近点查找

对于点云 P 中的每个点 p_i，在 Q 中找到欧氏距离最近的点 q_j：

```
q_j = argmin ||p_i - q||²
```

### 3.2 变换计算 (SVD方法)

给定对应点对 {(p_i, q_i)}，计算最优刚体变换：

```
1. 计算质心:
   p̄ = mean(p_i), q̄ = mean(q_i)

2. 去中心化:
   p'_i = p_i - p̄, q'_i = q_i - q̄

3. 计算协方差矩阵:
   H = Σ p'_i * q'_i^T

4. SVD分解:
   H = U * S * V^T

5. 旋转矩阵:
   R = V * U^T

6. 平移向量:
   t = q̄ - R * p̄
```

## 4. 变体算法

| 算法 | 特点 |
|------|------|
| Point-to-Point | 经典ICP，点到点距离 |
| Point-to-Plane | 点到切平面距离，收敛更快 |
| Generalized ICP | 结合面到面距离 |
| Colored ICP | 考虑颜色信息 |
| Go-ICP | 全局最优ICP |

## 5. 收敛条件

- 迭代次数达到上限
- 变换变化量小于阈值
- 误差变化小于阈值

```
收敛条件:
1. ||ΔR|| < ε_R 且 ||Δt|| < ε_t
2. |E_k - E_{k-1}| < ε_E
3. k > max_iterations
```

## 6. 优缺点

**优点:**
- 实现简单
- 当初始对齐较好时，收敛快
- 精度高

**缺点:**
- 需要较好的初始位置
- 容易陷入局部最优
- 对噪声和离群点敏感
- 计算复杂度 O(n²) 或 O(n log n) (使用KDTree)

## 7. 应用场景

- 3D扫描拼接
- SLAM后端优化
- 医学图像配准
- 机器人定位

## 8. 代码示例

见 `demo.py`

## 9. 参考资料

- Besl, P. J., & McKay, N. D. (1992). A method for registration of 3-D shapes
- Rusinkiewicz, S., & Levoy, M. (2001). Efficient variants of the ICP algorithm
- OpenCV ICP: https://docs.opencv.org/
- PCL ICP: https://pointclouds.org/
