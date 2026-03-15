"""
图算法 (Graph Algorithms) 示例代码

包含内容:
1. 图的表示与遍历
2. Dijkstra最短路径
3. Floyd-Warshall算法
4. Kruskal最小生成树
5. 拓扑排序
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict, deque
import heapq

plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class Graph:
    """图类 - 支持邻接表和邻接矩阵"""

    def __init__(self, directed=False):
        self.directed = directed
        self.adj_list = defaultdict(list)
        self.nodes = set()

    def add_edge(self, u, v, weight=1):
        self.nodes.add(u)
        self.nodes.add(v)
        self.adj_list[u].append((v, weight))
        if not self.directed:
            self.adj_list[v].append((u, weight))

    def bfs(self, start):
        """广度优先搜索"""
        visited = set()
        queue = deque([start])
        result = []

        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                result.append(node)
                for neighbor, _ in self.adj_list[node]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        return result

    def dfs(self, start, visited=None):
        """深度优先搜索"""
        if visited is None:
            visited = set()
        visited.add(start)
        result = [start]

        for neighbor, _ in self.adj_list[start]:
            if neighbor not in visited:
                result.extend(self.dfs(neighbor, visited))
        return result


def dijkstra(graph, start):
    """
    Dijkstra最短路径算法
    返回: (距离字典, 前驱字典)
    """
    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    predecessors = {node: None for node in graph.nodes}
    pq = [(0, start)]
    visited = set()

    while pq:
        current_dist, current = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)

        for neighbor, weight in graph.adj_list[current]:
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current
                heapq.heappush(pq, (distance, neighbor))

    return distances, predecessors


def get_path(predecessors, start, end):
    """根据前驱字典获取路径"""
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = predecessors[current]
    return path[::-1] if path[0] == end else None


def kruskal(nodes, edges):
    """
    Kruskal最小生成树算法
    edges: [(weight, u, v), ...]
    """
    parent = {n: n for n in nodes}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
            return True
        return False

    edges = sorted(edges)
    mst = []
    total_weight = 0

    for weight, u, v in edges:
        if union(u, v):
            mst.append((u, v, weight))
            total_weight += weight

    return mst, total_weight


def topological_sort(graph):
    """拓扑排序 (Kahn算法)"""
    in_degree = {node: 0 for node in graph.nodes}
    for node in graph.nodes:
        for neighbor, _ in graph.adj_list[node]:
            in_degree[neighbor] += 1

    queue = deque([n for n in graph.nodes if in_degree[n] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor, _ in graph.adj_list[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result if len(result) == len(graph.nodes) else None


def demo_graph_traversal():
    """图遍历演示"""
    print("=" * 60)
    print("1. 图遍历 (BFS vs DFS)")
    print("=" * 60)

    g = Graph()
    edges = [('A','B'), ('A','C'), ('B','D'), ('B','E'), ('C','F'), ('E','F')]
    for u, v in edges:
        g.add_edge(u, v)

    print("图结构:", dict(g.adj_list))
    print(f"BFS从A: {g.bfs('A')}")
    print(f"DFS从A: {g.dfs('A')}\n")


def demo_shortest_path():
    """最短路径演示"""
    print("=" * 60)
    print("2. Dijkstra最短路径")
    print("=" * 60)

    g = Graph(directed=True)
    edges = [
        ('A', 'B', 4), ('A', 'C', 2),
        ('B', 'C', 1), ('B', 'D', 5),
        ('C', 'D', 8), ('C', 'E', 10),
        ('D', 'E', 2)
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)

    distances, preds = dijkstra(g, 'A')
    print("从A出发的最短距离:")
    for node in sorted(distances.keys()):
        path = get_path(preds, 'A', node)
        print(f"  到{node}: 距离={distances[node]}, 路径={path}")
    print()


def demo_mst():
    """最小生成树演示"""
    print("=" * 60)
    print("3. Kruskal最小生成树")
    print("=" * 60)

    nodes = ['A', 'B', 'C', 'D', 'E']
    edges = [
        (1, 'A', 'B'), (3, 'A', 'C'), (4, 'B', 'C'),
        (2, 'B', 'D'), (5, 'C', 'D'), (6, 'D', 'E')
    ]

    mst, total = kruskal(nodes, edges)
    print("最小生成树边:")
    for u, v, w in mst:
        print(f"  {u} -- {v}: {w}")
    print(f"总权重: {total}\n")


def demo_topo_sort():
    """拓扑排序演示"""
    print("=" * 60)
    print("4. 拓扑排序")
    print("=" * 60)

    g = Graph(directed=True)
    # 课程依赖关系
    edges = [('C1', 'C3'), ('C2', 'C3'), ('C3', 'C4'), ('C3', 'C5'), ('C4', 'C6')]
    for u, v in edges:
        g.add_edge(u, v)

    order = topological_sort(g)
    print(f"课程学习顺序: {order}\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("图算法 (Graph Algorithms) 完整示例")
    print("=" * 60 + "\n")

    demo_graph_traversal()
    demo_shortest_path()
    demo_mst()
    demo_topo_sort()

    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
