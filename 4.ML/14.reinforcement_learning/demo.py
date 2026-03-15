"""
强化学习 (Reinforcement Learning) 示例代码

包含内容:
1. Q-Learning算法
2. SARSA算法
3. Cliff Walking环境
4. 算法对比
5. 训练可视化
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class CliffWalkingEnv:
    """悬崖行走环境"""

    def __init__(self, height=4, width=12):
        self.height = height
        self.width = width
        self.start = (height - 1, 0)
        self.goal = (height - 1, width - 1)
        self.cliff = [(height - 1, i) for i in range(1, width - 1)]
        self.actions = ['上', '右', '下', '左']
        self.n_actions = len(self.actions)
        self.state = None
        self.reset()

    def reset(self):
        self.state = self.start
        return self.state

    def step(self, action):
        """执行动作，返回 (新状态, 奖励, 是否结束)"""
        row, col = self.state

        # 根据动作移动
        if action == 0:  # 上
            row = max(0, row - 1)
        elif action == 1:  # 右
            col = min(self.width - 1, col + 1)
        elif action == 2:  # 下
            row = min(self.height - 1, row + 1)
        elif action == 3:  # 左
            col = max(0, col - 1)

        self.state = (row, col)

        # 检查是否到达目标
        if self.state == self.goal:
            return self.state, 0, True

        # 检查是否掉入悬崖
        if self.state in self.cliff:
            self.state = self.start
            return self.state, -100, False

        # 普通移动
        return self.state, -1, False

    def render(self):
        """可视化环境"""
        grid = np.zeros((self.height, self.width))

        # 标记悬崖
        for c in self.cliff:
            grid[c] = -100

        # 标记起点和终点
        grid[self.start] = 1
        grid[self.goal] = 2

        # 标记当前位置
        if self.state:
            grid[self.state] = 3

        return grid


class QLearning:
    """Q-Learning算法"""

    def __init__(self, n_actions, learning_rate=0.1, discount_factor=0.99, epsilon=0.1):
        self.n_actions = n_actions
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.q_table = defaultdict(lambda: np.zeros(n_actions))

    def choose_action(self, state):
        """ε-greedy策略选择动作"""
        if np.random.random() < self.epsilon:
            return np.random.randint(self.n_actions)
        return np.argmax(self.q_table[state])

    def update(self, state, action, reward, next_state, done):
        """更新Q值"""
        if done:
            target = reward
        else:
            target = reward + self.gamma * np.max(self.q_table[next_state])

        self.q_table[state][action] += self.lr * (target - self.q_table[state][action])


class SARSA:
    """SARSA算法"""

    def __init__(self, n_actions, learning_rate=0.1, discount_factor=0.99, epsilon=0.1):
        self.n_actions = n_actions
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.q_table = defaultdict(lambda: np.zeros(n_actions))

    def choose_action(self, state):
        """ε-greedy策略选择动作"""
        if np.random.random() < self.epsilon:
            return np.random.randint(self.n_actions)
        return np.argmax(self.q_table[state])

    def update(self, state, action, reward, next_state, next_action, done):
        """更新Q值"""
        if done:
            target = reward
        else:
            target = reward + self.gamma * self.q_table[next_state][next_action]

        self.q_table[state][action] += self.lr * (target - self.q_table[state][action])


def train_qlearning(env, agent, n_episodes=500):
    """训练Q-Learning智能体"""
    rewards = []

    for episode in range(n_episodes):
        state = env.reset()
        total_reward = 0
        done = False

        while not done:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            agent.update(state, action, reward, next_state, done)

            state = next_state
            total_reward += reward

        rewards.append(total_reward)

    return rewards


def train_sarsa(env, agent, n_episodes=500):
    """训练SARSA智能体"""
    rewards = []

    for episode in range(n_episodes):
        state = env.reset()
        action = agent.choose_action(state)
        total_reward = 0
        done = False

        while not done:
            next_state, reward, done = env.step(action)
            next_action = agent.choose_action(next_state)
            agent.update(state, action, reward, next_state, next_action, done)

            state = next_state
            action = next_action
            total_reward += reward

        rewards.append(total_reward)

    return rewards


def demo_cliff_walking():
    """悬崖行走环境演示"""
    print("=" * 60)
    print("1. 悬崖行走环境")
    print("=" * 60)

    env = CliffWalkingEnv()
    print(f"环境大小: {env.height} x {env.width}")
    print(f"起点: {env.start}, 终点: {env.goal}")
    print(f"悬崖位置: {env.cliff[:3]}... (共{len(env.cliff)}个)")
    print(f"动作: {env.actions}")

    # 可视化环境
    fig, ax = plt.subplots(figsize=(12, 4))

    grid = np.zeros((env.height, env.width))

    # 绘制悬崖
    for c in env.cliff:
        grid[c] = -1

    # 绘制网格
    ax.imshow(grid, cmap='RdYlGn_r', vmin=-1, vmax=1)

    # 标记起点和终点
    ax.plot(env.start[1], env.start[0], 'go', markersize=15, label='起点')
    ax.plot(env.goal[1], env.goal[0], 'b*', markersize=20, label='终点')

    # 标记悬崖
    for c in env.cliff:
        ax.text(c[1], c[0], 'X', ha='center', va='center', fontsize=12, color='white')

    ax.set_xticks(range(env.width))
    ax.set_yticks(range(env.height))
    ax.set_title('悬崖行走环境 (绿色=起点, 红色=悬崖, 蓝色=终点)', fontsize=14)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('rl_cliff_environment.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("环境图已保存为 rl_cliff_environment.png\n")


def demo_qlearning_vs_sarsa():
    """Q-Learning vs SARSA对比"""
    print("=" * 60)
    print("2. Q-Learning vs SARSA对比")
    print("=" * 60)

    env = CliffWalkingEnv()
    n_episodes = 500

    # 训练Q-Learning
    print("训练Q-Learning...")
    q_agent = QLearning(env.n_actions, learning_rate=0.5, epsilon=0.1)
    q_rewards = train_qlearning(env, q_agent, n_episodes)

    # 训练SARSA
    print("训练SARSA...")
    sarsa_agent = SARSA(env.n_actions, learning_rate=0.5, epsilon=0.1)
    sarsa_rewards = train_sarsa(env, sarsa_agent, n_episodes)

    # 计算移动平均
    window = 20
    q_avg = np.convolve(q_rewards, np.ones(window)/window, mode='valid')
    sarsa_avg = np.convolve(sarsa_rewards, np.ones(window)/window, mode='valid')

    print(f"\nQ-Learning平均奖励(最后100回合): {np.mean(q_rewards[-100:]):.2f}")
    print(f"SARSA平均奖励(最后100回合): {np.mean(sarsa_rewards[-100:]):.2f}")

    # 可视化学习曲线
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 学习曲线
    ax1 = axes[0]
    ax1.plot(q_rewards, alpha=0.3, color='blue')
    ax1.plot(sarsa_rewards, alpha=0.3, color='red')
    ax1.plot(range(window-1, n_episodes), q_avg, color='blue', linewidth=2, label='Q-Learning')
    ax1.plot(range(window-1, n_episodes), sarsa_avg, color='red', linewidth=2, label='SARSA')
    ax1.set_xlabel('回合', fontsize=12)
    ax1.set_ylabel('累积奖励', fontsize=12)
    ax1.set_title('学习曲线对比', fontsize=14)
    ax1.legend(loc='lower right')
    ax1.grid(True, alpha=0.3)

    # 最优路径可视化
    ax2 = axes[1]

    # 使用Q-Learning的最优策略走一条路径
    state = env.reset()
    path = [state]
    done = False

    while not done:
        action = np.argmax(q_agent.q_table[state])
        state, _, done = env.step(action)
        path.append(state)

    # 绘制路径
    grid = np.zeros((env.height, env.width))
    for c in env.cliff:
        grid[c] = -1

    ax2.imshow(grid, cmap='RdYlGn_r', vmin=-1, vmax=1)

    path = np.array(path)
    ax2.plot(path[:, 1], path[:, 0], 'b-', linewidth=2, label='Q-Learning路径')
    ax2.plot(env.start[1], env.start[0], 'go', markersize=12)
    ax2.plot(env.goal[1], env.goal[0], 'b*', markersize=15)

    ax2.set_title('Q-Learning学习的最优路径', fontsize=14)
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('rl_qlearning_sarsa.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("对比图已保存为 rl_qlearning_sarsa.png\n")


def demo_epsilon_effect():
    """探索率的影响"""
    print("=" * 60)
    print("3. 探索率 (ε) 的影响")
    print("=" * 60)

    env = CliffWalkingEnv()
    n_episodes = 500
    epsilons = [0.01, 0.1, 0.3, 0.5]

    results = {}

    for eps in epsilons:
        print(f"训练 ε={eps}...")
        agent = QLearning(env.n_actions, learning_rate=0.5, epsilon=eps)
        rewards = train_qlearning(env, agent, n_episodes)
        results[eps] = rewards

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 6))

    window = 20
    for eps, rewards in results.items():
        avg = np.convolve(rewards, np.ones(window)/window, mode='valid')
        ax.plot(range(window-1, n_episodes), avg, linewidth=2, label=f'ε={eps}')

    ax.set_xlabel('回合', fontsize=12)
    ax.set_ylabel('平均累积奖励', fontsize=12)
    ax.set_title('不同探索率的学习效果', fontsize=14)
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('rl_epsilon_effect.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("探索率影响图已保存为 rl_epsilon_effect.png\n")

    print("观察:")
    print("  - ε太小: 探索不足，可能陷入局部最优")
    print("  - ε太大: 探索过多，收敛慢")
    print("  - 通常 ε=0.1 是一个较好的平衡点\n")


def demo_hyperparameters():
    """超参数影响"""
    print("=" * 60)
    print("4. 学习率和折扣因子的影响")
    print("=" * 60)

    env = CliffWalkingEnv()
    n_episodes = 500

    # 不同学习率
    learning_rates = [0.1, 0.3, 0.5, 0.9]
    lr_results = {}

    for lr in learning_rates:
        agent = QLearning(env.n_actions, learning_rate=lr, epsilon=0.1)
        rewards = train_qlearning(env, agent, n_episodes)
        lr_results[lr] = rewards

    # 不同折扣因子
    gammas = [0.5, 0.9, 0.95, 0.99]
    gamma_results = {}

    for gamma in gammas:
        agent = QLearning(env.n_actions, learning_rate=0.5, epsilon=0.1, discount_factor=gamma)
        rewards = train_qlearning(env, agent, n_episodes)
        gamma_results[gamma] = rewards

    # 可视化
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    window = 20

    # 学习率
    ax1 = axes[0]
    for lr, rewards in lr_results.items():
        avg = np.convolve(rewards, np.ones(window)/window, mode='valid')
        ax1.plot(range(window-1, n_episodes), avg, linewidth=2, label=f'α={lr}')
    ax1.set_xlabel('回合', fontsize=12)
    ax1.set_ylabel('平均累积奖励', fontsize=12)
    ax1.set_title('学习率 (α) 的影响', fontsize=14)
    ax1.legend(loc='lower right')
    ax1.grid(True, alpha=0.3)

    # 折扣因子
    ax2 = axes[1]
    for gamma, rewards in gamma_results.items():
        avg = np.convolve(rewards, np.ones(window)/window, mode='valid')
        ax2.plot(range(window-1, n_episodes), avg, linewidth=2, label=f'γ={gamma}')
    ax2.set_xlabel('回合', fontsize=12)
    ax2.set_ylabel('平均累积奖励', fontsize=12)
    ax2.set_title('折扣因子 (γ) 的影响', fontsize=14)
    ax2.legend(loc='lower right')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('rl_hyperparameters.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("超参数影响图已保存为 rl_hyperparameters.png\n")

    print("参数说明:")
    print("  - 学习率α: 控制更新步长，太大不稳定，太小收敛慢")
    print("  - 折扣因子γ: 越大越重视长期奖励，越小越重视短期\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("强化学习 (Reinforcement Learning) 完整示例")
    print("=" * 60 + "\n")

    # 运行所有示例
    demo_cliff_walking()
    demo_qlearning_vs_sarsa()
    demo_epsilon_effect()
    demo_hyperparameters()

    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
