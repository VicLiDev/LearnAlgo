# 搜索算法 (Search Algorithms)

## 1. 简介

搜索算法是计算机科学中最基础的算法类别之一，用于在数据结构中查找特定元素或在状态空间中寻找解。

## 2. 搜索算法分类

| 类型 | 算法 | 特点 |
|------|------|------|
| 线性搜索 | 顺序查找 | 简单，适用于无序数据 |
| 二分搜索 | 折半查找 | 要求数据有序，O(log n) |
| 图搜索 | BFS, DFS | 遍历图/树结构 |
| 启发式搜索 | A*, IDA* | 使用启发函数加速 |

## 3. 线性搜索与二分搜索

### 3.1 线性搜索
```
for i in range(len(arr)):
    if arr[i] == target:
        return i
return -1
```
- 时间复杂度: O(n)
- 适用: 无需预处理，适用于任何数据

### 3.2 二分搜索
```
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
```
- 时间复杂度: O(log n)
- 前提: 数据必须有序

## 4. 广度优先搜索 (BFS)

### 4.1 原理
- 从起点开始，逐层向外扩展
- 使用队列存储待访问节点
- 保证找到最短路径（无权图）

### 4.2 伪代码
```
BFS(start):
    queue = [start]
    visited = {start}

    while queue:
        node = queue.pop(0)
        for neighbor in node.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

### 4.3 应用
- 最短路径（无权图）
- 社交网络中的好友推荐
- 网络爬虫

## 5. 深度优先搜索 (DFS)

### 5.1 原理
- 沿着一条路径走到底
- 使用栈（递归）存储待访问节点
- 不保证最短路径

### 5.2 伪代码
```
DFS(node, visited):
    visited.add(node)

    for neighbor in node.neighbors:
        if neighbor not in visited:
            DFS(neighbor, visited)
```

### 5.3 应用
- 拓扑排序
- 检测环
- 路径查找
- 迷宫求解

## 6. A*搜索算法

### 6.1 原理
A*是一种启发式搜索算法，结合了Dijkstra和贪心搜索的优点。

**评估函数**:
```
f(n) = g(n) + h(n)
```
- g(n): 从起点到n的实际代价
- h(n): 从n到目标的启发式估计
- f(n): 总估计代价

### 6.2 启发函数选择
- **可采纳性**: h(n) ≤ 实际代价
- **一致性**: h(n) ≤ cost(n,n') + h(n')

**常见启发函数**:
- 曼哈顿距离: |x1-x2| + |y1-y2|（网格）
- 欧氏距离: √((x1-x2)² + (y1-y2)²)
- 切比雪夫距离: max(|x1-x2|, |y1-y2|)

### 6.3 伪代码
```
A*(start, goal):
    open_set = PriorityQueue()
    open_set.add(start, f(start))
    came_from = {}
    g_score = {start: 0}

    while not open_set.empty():
        current = open_set.pop()

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in current.neighbors:
            tentative_g = g_score[current] + cost(current, neighbor)

            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + h(neighbor)
                open_set.add_or_update(neighbor, f_score)
```

## 7. 算法对比

| 特性 | BFS | DFS | A* |
|------|-----|-----|-----|
| 数据结构 | 队列 | 栈 | 优先队列 |
| 最短路径 | ✓ (无权) | ✗ | ✓ (有权) |
| 空间复杂度 | O(b^d) | O(bd) | O(b^d) |
| 完备性 | ✓ | ✓ (有限图) | ✓ |
| 最优性 | ✓ (无权) | ✗ | ✓ |

## 8. 应用场景

- **BFS**: 社交网络分析、最短路径
- **DFS**: 拓扑排序、连通分量
- **A***: 游戏AI路径规划、机器人导航
- **二分搜索**: 数据库索引、字典查找

## 9. 示例代码

见 `demo.py` 文件，包含：
- 二分搜索实现
- BFS/DFS图遍历
- A*路径规划
- 迷宫求解

## 10. 参考资料

- Cormen, T. H., et al. (2009). Introduction to Algorithms
- Russell, S., & Norvig, P. (2020). Artificial Intelligence: A Modern Approach
