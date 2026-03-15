"""
搜索算法 (Search Algorithms) 示例代码

包含内容:
1. 线性搜索与二分搜索
2. 广度优先搜索 (BFS)
3. 深度优先搜索 (DFS)
4. A*搜索算法
5. 迷宫求解
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import heapq
import warnings
warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


# =====================================================
# 1. 线性搜索与二分搜索
# =====================================================

def linear_search(arr, target):
    """线性搜索"""
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1


def binary_search(arr, target):
    """二分搜索（要求数组有序）"""
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def binary_search_first(arr, target):
    """二分搜索找第一个出现的位置"""
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            result = mid
            right = mid - 1  # 继续在左半边找
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result


# =====================================================
# 2. BFS 图遍历
# =====================================================

def bfs_graph(graph, start):
    """
    BFS遍历图

    Args:
        graph: 邻接表表示的图 {节点: [邻居列表]}
        start: 起始节点

    Returns:
        遍历顺序列表
    """
    visited = set()
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()

        if node not in visited:
            visited.add(node)
            order.append(node)

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    queue.append(neighbor)

    return order


def bfs_shortest_path(graph, start, end):
    """
    BFS找最短路径（无权图）

    Returns:
        路径列表，如果不存在返回None
    """
    if start == end:
        return [start]

    visited = {start}
    queue = deque([(start, [start])])

    while queue:
        node, path = queue.popleft()

        for neighbor in graph.get(node, []):
            if neighbor == end:
                return path + [neighbor]

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None


# =====================================================
# 3. DFS 图遍历
# =====================================================

def dfs_graph_recursive(graph, start, visited=None):
    """DFS递归实现"""
    if visited is None:
        visited = set()

    visited.add(start)
    order = [start]

    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            order.extend(dfs_graph_recursive(graph, neighbor, visited))

    return order


def dfs_graph_iterative(graph, start):
    """DFS迭代实现"""
    visited = set()
    stack = [start]
    order = []

    while stack:
        node = stack.pop()

        if node not in visited:
            visited.add(node)
            order.append(node)

            # 逆序添加邻居，使得第一个邻居先被访问
            for neighbor in reversed(graph.get(node, [])):
                if neighbor not in visited:
                    stack.append(neighbor)

    return order


# =====================================================
# 4. A* 搜索算法
# =====================================================

def manhattan_distance(a, b):
    """曼哈顿距离"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean_distance(a, b):
    """欧氏距离"""
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


def a_star(grid, start, end, heuristic=manhattan_distance):
    """
    A*搜索算法

    Args:
        grid: 2D网格，0表示可通行，1表示障碍
        start: 起点坐标 (row, col)
        end: 终点坐标 (row, col)
        heuristic: 启发函数

    Returns:
        路径列表，如果不存在返回None
    """
    rows, cols = grid.shape

    # 优先队列: (f_score, g_score, position, path)
    open_set = [(heuristic(start, end), 0, start, [start])]
    visited = set()

    # 四个方向
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while open_set:
        f, g, current, path = heapq.heappop(open_set)

        if current == end:
            return path

        if current in visited:
            continue

        visited.add(current)

        for dr, dc in directions:
            new_row, new_col = current[0] + dr, current[1] + dc
            new_pos = (new_row, new_col)

            # 检查边界和障碍
            if (0 <= new_row < rows and 0 <= new_col < cols and
                grid[new_row, new_col] == 0 and new_pos not in visited):

                new_g = g + 1  # 假设每步代价为1
                new_f = new_g + heuristic(new_pos, end)
                heapq.heappush(open_set, (new_f, new_g, new_pos, path + [new_pos]))

    return None  # 没有找到路径


# =====================================================
# 5. 迷宫求解
# =====================================================

def solve_maze(maze, start, end, method='bfs'):
    """
    迷宫求解

    Args:
        maze: 2D迷宫，0=通道，1=墙
        start: 起点
        end: 终点
        method: 'bfs', 'dfs', 或 'astar'

    Returns:
        路径列表
    """
    if method == 'bfs':
        return bfs_shortest_path(maze_to_graph(maze), start, end)
    elif method == 'astar':
        return a_star(maze, start, end)
    else:
        return dfs_maze(maze, start, end)


def maze_to_graph(maze):
    """将迷宫转换为邻接表"""
    rows, cols = maze.shape
    graph = {}
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for r in range(rows):
        for c in range(cols):
            if maze[r, c] == 0:  # 通道
                neighbors = []
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and maze[nr, nc] == 0:
                        neighbors.append((nr, nc))
                graph[(r, c)] = neighbors

    return graph


def dfs_maze(maze, start, end):
    """DFS解迷宫"""
    rows, cols = maze.shape
    visited = set()
    path = []

    def dfs(pos):
        if pos == end:
            path.append(pos)
            return True

        if pos in visited:
            return False

        visited.add(pos)
        path.append(pos)

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            new_pos = (pos[0] + dr, pos[1] + dc)
            if (0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and
                maze[new_pos] == 0 and new_pos not in visited):
                if dfs(new_pos):
                    return True

        path.pop()
        return False

    if dfs(start):
        return path
    return None


# =====================================================
# 演示函数
# =====================================================

def demo_binary_search():
    """二分搜索演示"""
    print("=" * 60)
    print("1. 二分搜索演示")
    print("=" * 60)

    arr = sorted(np.random.randint(1, 100, 20))
    target = arr[10]

    print(f"数组: {arr}")
    print(f"目标: {target}")

    # 线性搜索
    import time
    start = time.time()
    idx_linear = linear_search(arr, target)
    time_linear = time.time() - start

    # 二分搜索
    start = time.time()
    idx_binary = binary_search(arr, target)
    time_binary = time.time() - start

    print(f"\n线性搜索: 索引={idx_linear}, 时间={time_linear*1000:.4f}ms")
    print(f"二分搜索: 索引={idx_binary}, 时间={time_binary*1000:.4f}ms")
    print()


def demo_bfs_dfs():
    """BFS和DFS演示"""
    print("=" * 60)
    print("2. BFS和DFS图遍历演示")
    print("=" * 60)

    # 创建示例图
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    print("图结构:")
    for node, neighbors in graph.items():
        print(f"  {node}: {neighbors}")

    bfs_order = bfs_graph(graph, 'A')
    dfs_order = dfs_graph_iterative(graph, 'A')

    print(f"\nBFS遍历顺序: {bfs_order}")
    print(f"DFS遍历顺序: {dfs_order}")

    # 最短路径
    path = bfs_shortest_path(graph, 'A', 'F')
    print(f"\nA到F的最短路径: {path}")
    print()


def demo_a_star():
    """A*算法演示"""
    print("=" * 60)
    print("3. A*搜索算法演示")
    print("=" * 60)

    # 创建网格地图
    grid = np.zeros((10, 10))

    # 添加障碍物
    grid[3, 1:8] = 1
    grid[5, 2:9] = 1
    grid[7, 0:6] = 1

    start = (0, 0)
    end = (9, 9)

    # A*搜索
    path = a_star(grid, start, end)

    if path:
        print(f"找到路径，长度: {len(path)}")
        print(f"路径: {path}")
    else:
        print("未找到路径")

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 10))

    # 绘制网格
    ax.imshow(grid, cmap='binary')

    # 绘制路径
    if path:
        path_array = np.array(path)
        ax.plot(path_array[:, 1], path_array[:, 0], 'r-', linewidth=2, label='A*路径')

    # 标记起点和终点
    ax.plot(start[1], start[0], 'go', markersize=15, label='起点')
    ax.plot(end[1], end[0], 'b*', markersize=20, label='终点')

    ax.set_xlabel('列', fontsize=12)
    ax.set_ylabel('行', fontsize=12)
    ax.set_title('A*路径规划', fontsize=14)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('search_astar.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("A*路径规划图已保存为 search_astar.png\n")


def demo_maze_solving():
    """迷宫求解演示"""
    print("=" * 60)
    print("4. 迷宫求解演示")
    print("=" * 60)

    # 创建迷宫
    np.random.seed(42)
    size = 15
    maze = np.random.choice([0, 1], size=(size, size), p=[0.7, 0.3])
    maze[0, 0] = 0  # 起点
    maze[size-1, size-1] = 0  # 终点

    start = (0, 0)
    end = (size-1, size-1)

    # 不同方法求解
    methods = ['bfs', 'dfs', 'astar']
    results = {}

    for method in methods:
        if method == 'bfs':
            graph = maze_to_graph(maze)
            path = bfs_shortest_path(graph, start, end)
        elif method == 'astar':
            path = a_star(maze, start, end)
        else:
            path = dfs_maze(maze, start, end)

        results[method] = path
        if path:
            print(f"{method.upper()}: 找到路径，长度={len(path)}")
        else:
            print(f"{method.upper()}: 未找到路径")

    # 可视化对比
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    for ax, (method, path) in zip(axes, results.items()):
        ax.imshow(maze, cmap='binary')

        if path:
            path_array = np.array(path)
            ax.plot(path_array[:, 1], path_array[:, 0], 'r-', linewidth=2)

        ax.plot(start[1], start[0], 'go', markersize=10)
        ax.plot(end[1], end[0], 'b*', markersize=15)
        ax.set_title(f'{method.upper()}\n路径长度: {len(path) if path else "无解"}', fontsize=14)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('search_maze_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("迷宫求解对比图已保存为 search_maze_comparison.png\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("搜索算法 (Search Algorithms) 完整示例")
    print("=" * 60 + "\n")

    demo_binary_search()
    demo_bfs_dfs()
    demo_a_star()
    demo_maze_solving()

    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
