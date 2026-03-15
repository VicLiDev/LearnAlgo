# 基础算法 (Basic Algorithms)

本目录包含编程和算法学习的基础理论和通用知识，是所有高级主题的前置内容。

## 目录结构

```
1.BasicAlgo/
├── readme.md                       # 本文件
├── demo.py                         # 完整示例代码
│
├── 01.data_proc/                   # 数据处理基础
├── 02.tree_structure.c             # 树结构实现
├── 03.trie.c                       # 字典树实现
├── 04.heap.py                      # 堆实现
├── 05.search_algorithms/           # 搜索算法
├── 06.sorting_algorithms/          # 排序算法
├── 07.graph_algorithms/            # 图算法
└── 08.dynamic_programming/         # 动态规划
```

---

## 01. 数据处理基础

**路径**: `01.data_proc/`

**内容**:
- 数据读取与写入
- 数据格式转换
- 基础数据操作

---

## 02. 树结构 (Tree Structure)

**难度**: ★★☆☆☆

**内容**:
- 二叉树基础
- 树的遍历（前序、中序、后序、层序）
- 二叉搜索树 (BST)
- 平衡树概念

**时间复杂度**:
| 操作 | 平均     | 最坏 |
|------|----------|------|
| 查找 | O(log n) | O(n) |
| 插入 | O(log n) | O(n) |
| 删除 | O(log n) | O(n) |

---

## 03. 字典树 (Trie)

**难度**: ★★☆☆☆

**内容**:
- 前缀树结构
- 字符串插入与查找
- 前缀匹配
- 应用场景

**适用场景**:
- 自动补全
- 拼写检查
- IP路由表

---

## 04. 堆 (Heap)

**难度**: ★★☆☆☆

**内容**:
- 最大堆/最小堆
- 堆化操作
- 优先队列实现
- 堆排序

**时间复杂度**:
| 操作     | 时间     |
|----------|----------|
| 建堆     | O(n)     |
| 插入     | O(log n) |
| 取极值   | O(1)     |
| 删除极值 | O(log n) |

---

## 05. 搜索算法 (Search Algorithms)

**难度**: ★☆☆☆☆

**内容**:
- 线性搜索与二分搜索
- 广度优先搜索 (BFS)
- 深度优先搜索 (DFS)
- A*搜索算法
- 启发式搜索

**适用场景**: 路径规划、游戏AI、状态空间搜索

```bash
cd 05.search_algorithms && python demo.py
```

---

## 06. 排序算法 (Sorting Algorithms)

**难度**: ★☆☆☆☆

**内容**:
- 冒泡排序、选择排序、插入排序
- 快速排序、归并排序、堆排序
- 计数排序、基数排序
- 时间/空间复杂度分析

**适用场景**: 数据预处理、查找优化

```bash
cd 06.sorting_algorithms && python demo.py
```

---

## 07. 图算法 (Graph Algorithms)

**难度**: ★★★☆☆

**内容**:
- 图的遍历 (BFS, DFS)
- 最短路径 (Dijkstra, Bellman-Ford, Floyd-Warshall)
- 最小生成树 (Kruskal, Prim)
- 拓扑排序
- 连通分量

**适用场景**: 社交网络、路径规划、网络分析

```bash
cd 07.graph_algorithms && python demo.py
```

---

## 08. 动态规划 (Dynamic Programming)

**难度**: ★★★☆☆

**内容**:
- 基本概念 (重叠子问题、最优子结构)
- 背包问题 (01背包、完全背包)
- 最长公共子序列 (LCS)
- 最长递增子序列 (LIS)
- 编辑距离
- 状态压缩DP

**适用场景**: 优化问题、资源分配、序列分析

```bash
cd 08.dynamic_programming && python demo.py
```

---

## 复杂度速查表

### 排序算法

| 算法     | 最优       | 平均       | 最坏       | 空间     | 稳定 |
|----------|------------|------------|------------|----------|------|
| 冒泡排序 | O(n)       | O(n²)      | O(n²)      | O(1)     | ✓    |
| 快速排序 | O(n log n) | O(n log n) | O(n²)      | O(log n) | ✗    |
| 归并排序 | O(n log n) | O(n log n) | O(n log n) | O(n)     | ✓    |
| 堆排序   | O(n log n) | O(n log n) | O(n log n) | O(1)     | ✗    |

### 搜索算法

| 算法     | 时间复杂度 | 空间复杂度 |
|----------|------------|------------|
| 线性搜索 | O(n)       | O(1)       |
| 二分搜索 | O(log n)   | O(1)       |
| BFS      | O(V+E)     | O(V)       |
| DFS      | O(V+E)     | O(V)       |
| A*       | O(b^d)     | O(b^d)     |

### 图算法

| 算法           | 时间复杂度     |
|----------------|----------------|
| Dijkstra       | O((V+E) log V) |
| Bellman-Ford   | O(V·E)         |
| Floyd-Warshall | O(V³)          |
| Kruskal        | O(E log E)     |
| Prim           | O(E log V)     |

### 数据结构

| 结构   | 访问     | 搜索     | 插入     | 删除     | 空间   |
|--------|----------|----------|----------|----------|--------|
| 数组   | O(1)     | O(n)     | O(n)     | O(n)     | O(n)   |
| 链表   | O(n)     | O(n)     | O(1)     | O(1)     | O(n)   |
| 哈希表 | -        | O(1)     | O(1)     | O(1)     | O(n)   |
| BST    | O(log n) | O(log n) | O(log n) | O(log n) | O(n)   |
| 堆     | O(1)     | O(n)     | O(log n) | O(log n) | O(n)   |
| 字典树 | O(m)     | O(m)     | O(m)     | O(m)     | O(n×m) |

*m为字符串长度*

---

## 学习路径

```
数据结构
1. 树结构 → 理解层次化数据组织
     ↓
2. 堆 → 掌握优先队列概念
     ↓
3. 字典树 → 字符串处理基础
     ↓
基础算法
4. 搜索算法 → 掌握遍历与查找
     ↓
5. 排序算法 → 理解分治与比较排序
     ↓
6. 图算法 → 处理复杂关系网络
     ↓
7. 动态规划 → 解决优化问题
```

---

## 与其他目录的关系

```
1.BasicAlgo (基础：数据结构、基础算法) ← 当前
    ↓
2.GenAlgorithm (通用：数学变换、几何算法)
    ↓
3.Classical (经典应用：传统CV、PPF)
    ↓
4.ML (机器学习)
    ↓
5.DL (深度学习)
```

---

## 参考资料

### 书籍
- 《数据结构与算法分析》- Mark Allen Weiss
- 《算法导论》- CLRS
- 《算法 (第4版)》- Robert Sedgewick

### 在线资源
- [VisuAlgo - 算法可视化](https://visualgo.net/)
- [LeetCode - 算法练习](https://leetcode.com/)
- [GeeksforGeeks](https://www.geeksforgeeks.org/)

---

## 许可证

MIT License
