# 强化学习 (Reinforcement Learning)

## 1. 简介

强化学习是一种通过与环境交互来学习最优策略的机器学习方法。智能体通过尝试不同的动作，从环境获得奖励反馈，逐步学习最优行为策略。

### 核心概念

| 概念               | 说明                 |
|--------------------|----------------------|
| 智能体 (Agent)     | 学习者/决策者        |
| 环境 (Environment) | 智能体所处的外部世界 |
| 状态 (State)       | 环境的当前情况       |
| 动作 (Action)      | 智能体可执行的操作   |
| 奖励 (Reward)      | 环境对动作的反馈     |
| 策略 (Policy)      | 状态到动作的映射     |
| 价值 (Value)       | 长期累积奖励的期望   |

### 马尔可夫决策过程 (MDP)

强化学习问题通常建模为MDP：`(S, A, P, R, γ)`
- S：状态空间
- A：动作空间
- P：状态转移概率 P(s'|s,a)
- R：奖励函数 R(s,a)
- γ：折扣因子 (0, 1]

## 2. 核心概念详解

### 2.1 策略 (Policy)
- **确定性策略**：π(s) = a
- **随机策略**：π(a|s) = P(a|s)

### 2.2 价值函数

**状态价值函数**：
```
V^π(s) = E[γ^t R_t | s_0 = s]
```

**动作价值函数 (Q函数)**：
```
Q^π(s,a) = E[γ^t R_t | s_0 = s, a_0 = a]
```

### 2.3 贝尔曼方程

**贝尔曼期望方程**：
```
V^π(s) = Σ_a π(a|s) [R(s,a) + γ Σ_s' P(s'|s,a) V^π(s')]
```

**贝尔曼最优方程**：
```
V*(s) = max_a [R(s,a) + γ Σ_s' P(s'|s,a) V*(s')]
Q*(s,a) = R(s,a) + γ Σ_s' P(s'|s,a) max_a' Q*(s',a')
```

## 3. 主要算法分类

```
强化学习
├── 基于价值 (Value-Based)
│   ├── Q-Learning
│   ├── SARSA
│   └── DQN
├── 基于策略 (Policy-Based)
│   ├── REINFORCE
│   └── Actor-Critic
└── 基于模型 (Model-Based)
    ├── Dyna-Q
    └── MBPO
```

## 4. Q-Learning

### 4.1 算法原理

Q-Learning是一种无模型的离线策略算法，直接学习最优Q函数。

**更新规则**：
```
Q(s,a) ← Q(s,a) + α [r + γ max_a' Q(s',a') - Q(s,a)]
```

### 4.2 算法流程

```
初始化 Q(s,a) = 0
for each episode:
    初始化状态 s
    while s 不是终止状态:
        使用ε-greedy选择动作 a
        执行动作 a，观察 r 和 s'
        Q(s,a) ← Q(s,a) + α [r + γ max_a' Q(s',a') - Q(s,a)]
        s ← s'
```

### 4.3 探索与利用

**ε-greedy策略**：
```
a = {
    argmax_a Q(s,a),     概率 1-ε
    随机动作,            概率 ε
}
```

## 5. SARSA

### 5.1 算法原理

SARSA是一种在线策略算法，使用实际采取的动作更新。

**更新规则**：
```
Q(s,a) ← Q(s,a) + α [r + γ Q(s',a') - Q(s,a)]
```

### 5.2 与Q-Learning对比

| 特性     | Q-Learning       | SARSA    |
|----------|------------------|----------|
| 策略类型 | 离线策略         | 在线策略 |
| 更新方式 | max Q(s',a')     | Q(s',a') |
| 风险行为 | 可能学到危险策略 | 更保守   |

## 6. Deep Q-Network (DQN)

### 6.1 核心创新

1. **神经网络近似Q函数**：Q(s,a;θ)
2. **经验回放**：打破样本相关性
3. **目标网络**：稳定训练

### 6.2 损失函数

```
L(θ) = E[(r + γ max_a' Q(s',a';θ⁻) - Q(s,a;θ))²]
```
- θ⁻：目标网络参数

### 6.3 算法流程

```
初始化Q网络和目标网络
for each episode:
    while not done:
        使用ε-greedy选择动作 a
        执行动作，存储 (s,a,r,s') 到经验池
        从经验池采样小批量
        计算目标: y = r + γ max_a' Q(s',a';θ⁻)
        更新Q网络
        定期更新目标网络
```

## 7. 策略梯度

### 7.1 REINFORCE

**目标**：最大化期望回报
```
J(θ) = E[τ Σ_t ∇log π(a_t|s_t;θ) G_t]
```

**更新规则**：
```
θ ← θ + α ∇log π(a|s;θ) G
```

### 7.2 Actor-Critic

结合价值函数和策略函数：
- **Actor**：更新策略参数
- **Critic**：估计价值函数

```
δ = r + γ V(s') - V(s)
θ ← θ + α δ ∇log π(a|s;θ)
w ← w + α δ ∇V(s;w)
```

## 8. 算法对比

| 算法       | 类型         | 优点           | 缺点       |
|------------|--------------|----------------|------------|
| Q-Learning | 值           | 简单高效       | 仅离散动作 |
| SARSA      | 值           | 保守安全       | 收敛较慢   |
| DQN        | 值           | 处理大状态空间 | 不稳定     |
| REINFORCE  | 策略         | 连续动作       | 方差大     |
| A2C/A3C    | Actor-Critic | 平衡           | 实现复杂   |

## 9. 应用场景

- **游戏**：Atari、围棋、电竞
- **机器人**：行走、抓取、导航
- **自动驾驶**：决策控制
- **推荐系统**：长期收益优化
- **资源调度**：数据中心、物流

## 10. 实践建议

1. **奖励设计**：奖励稀疏时考虑奖励塑形
2. **超参数**：学习率、折扣因子、探索率
3. **稳定训练**：梯度裁剪、目标网络
4. **评估**：多次运行取平均

## 11. 示例代码

见 `demo.py` 文件，包含：
- Q-Learning实现
- Cliff Walking环境
- 训练可视化
- 与SARSA对比

## 12. 参考资料

- Sutton, R. S., & Barto, A. G. (2018). Reinforcement Learning: An Introduction
- Mnih, V., et al. (2015). Human-level control through deep reinforcement learning
- OpenAI Spinning Up: https://spinningup.openai.com/
- Stable Baselines3: https://stable-baselines3.readthedocs.io/
