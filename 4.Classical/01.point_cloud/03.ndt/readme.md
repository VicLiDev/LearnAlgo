# NDT (Normal Distributions Transform)

## 1. 简介

NDT 是一种基于概率的点云配准算法。它将空间划分为体素网格，每个体素用正态分布描述点云的局部结构，通过最大化目标点云在源点云分布中的概率来计算最优变换。

## 2. 与 ICP 的区别

| 方面 | ICP | NDT |
|------|-----|-----|
| 对应关系 | 硬对应（点对点） | 软对应（概率分布） |
| 目标函数 | 点到点/面距离 | 概率似然 |
| 对噪声敏感度 | 高 | 低 |
| 计算复杂度 | O(n log n) | O(n) |
| 收敛速度 | 较慢 | 较快 |
| 初值要求 | 严格 | 相对宽松 |

## 3. 算法流程

```
1. 预处理: 将目标点云转换为NDT表示
   a. 划分体素网格
   b. 计算每个体素的均值和协方差

2. 迭代优化:
   a. 将源点云变换到当前估计位姿
   b. 计算每个点在对应体素中的概率
   c. 计算梯度和Hessian矩阵
   d. 使用牛顿法更新变换参数
   e. 检查收敛

3. 返回最终变换
```

## 4. 数学原理

### 4.1 NDT表示

对于体素 v 中的点集 {p₁, p₂, ..., pₙ}：

```
均值:
  μ = (1/n) Σ pᵢ

协方差:
  Σ = (1/n) Σ (pᵢ - μ)(pᵢ - μ)ᵀ
```

### 4.2 概率计算

点 p 在 NDT 单元中的概率：

```
P(p) = (1/(2π)^(d/2) |Σ|^0.5) * exp(-0.5 * (p-μ)ᵀ Σ⁻¹ (p-μ))
```

### 4.3 目标函数

最大化所有点的对数似然：

```
score(T) = Σ log(P(T(pᵢ)))

其中 T 是变换矩阵，pᵢ 是源点云中的点
```

### 4.4 优化

使用牛顿法优化：

```
T_{k+1} = T_k - H⁻¹ * ∇score

其中:
- ∇score: 梯度
- H: Hessian矩阵
```

## 5. 变体算法

| 算法 | 特点 |
|------|------|
| 2D-NDT | 平面激光雷达配准 |
| 3D-NDT | 三维点云配准 |
| Multi-resolution NDT | 多分辨率加速 |
| Color-NDT | 考虑颜色信息 |
| FPCA-NDT | 快速精确位姿估计 |

## 6. 参数说明

| 参数 | 说明 | 典型值 |
|------|------|--------|
| voxel_size | 体素大小 | 0.5m - 2.0m |
| step_size | 优化步长 | 0.1 |
| max_iterations | 最大迭代次数 | 50 |
| tolerance | 收敛阈值 | 1e-6 |
| min_points_per_voxel | 体素最小点数 | 3 |

## 7. 优缺点

**优点:**
- 对噪声和离群点鲁棒
- 不需要显式的点对应
- 收敛速度较快
- 可以处理部分重叠

**缺点:**
- 体素大小影响精度
- 边界区域处理困难
- 内存占用较大
- 对密度变化敏感

## 8. 应用场景

- 激光SLAM
- 自动驾驶定位
- 大规模点云配准
- 移动机器人导航

## 9. 代码示例

见 `demo.py`

## 10. 参考资料

- Biber, P., & Straßer, W. (2003). The normal distributions transform: A new approach to laser scan matching
- Magnusson, M. (2009). The three-dimensional normal-distributions transform
- PCL NDT: https://pointclouds.org/documentation/tutorials/normal_distributions_transform.html
