# 运筹学与控制论（Operations Research & Control Theory）

运用数学模型对系统进行优化决策的学科。

## 子学科

| 学科       | 英文名                | 核心内容                                          | 难度  |
|------------|-----------------------|---------------------------------------------------|-------|
| 线性规划   | Linear Programming    | 单纯形法、对偶理论、内点法                        | ★★★☆☆ |
| 非线性规划 | Nonlinear Programming | KKT条件、罚函数法、序列二次规划(SQP)              | ★★★★☆ |
| 动态规划   | Dynamic Programming   | Bellman方程、最优性原理、策略迭代                 | ★★★☆☆ |
| 博弈论     | Game Theory           | 纳什均衡、零和博弈、合作博弈、机制设计            | ★★★☆☆ |
| 排队论     | Queueing Theory       | M/M/1模型、Little公式、排队网络                   | ★★★☆☆ |
| 控制理论   | Control Theory        | 状态空间、能控性/能观性、PID、LQR、$H_\infty$控制 | ★★★★☆ |
| 最优控制   | Optimal Control       | Pontryagin极大值原理、动态规划法、轨迹优化        | ★★★★★ |

## 适用场景

供应链优化、资源调度、自动驾驶控制、机器人规划、经济模型。

## 核心公式

- Bellman方程：$V(s) = \max_a \left[ R(s,a) + \gamma \sum_{s'} P(s'|s,a) V(s') \right]$
- LQR最优控制：$u = -Kx$，其中 $K = R^{-1}B^T P$，$P$ 为Riccati方程的解
- Little定律：$L = \lambda W$（系统平均顾客数 = 到达率 × 平均等待时间）
