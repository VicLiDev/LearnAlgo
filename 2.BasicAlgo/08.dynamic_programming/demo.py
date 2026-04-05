"""
动态规划 (Dynamic Programming) 示例代码

包含内容:
1. 斐波那契数列
2. 01背包问题
3. 最长公共子序列
4. 最长递增子序列
5. 编辑距离
"""

import numpy as np
import matplotlib.pyplot as plt
from t01_mpl import chinese_font

plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def fib_dp(n):
    """斐波那契数列 - 动态规划"""
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]


def fib_optimized(n):
    """斐波那契数列 - 空间优化"""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def knapsack_01(weights, values, capacity):
    """
    01背包问题
    返回: (最大价值, 选择的物品)
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w-weights[i-1]] + values[i-1])
            else:
                dp[i][w] = dp[i-1][w]

    # 回溯找选择的物品
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(i-1)
            w -= weights[i-1]

    return dp[n][capacity], selected[::-1]


def lcs(s1, s2):
    """
    最长公共子序列
    返回: (长度, LCS序列)
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # 回溯找LCS
    lcs_str = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            lcs_str.append(s1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1

    return dp[m][n], ''.join(reversed(lcs_str))


def lis(nums):
    """
    最长递增子序列
    返回: (长度, LIS序列)
    """
    if not nums:
        return 0, []

    n = len(nums)
    dp = [1] * n
    prev = [-1] * n

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j

    # 找最长序列
    max_len = max(dp)
    idx = dp.index(max_len)

    sequence = []
    while idx != -1:
        sequence.append(nums[idx])
        idx = prev[idx]

    return max_len, sequence[::-1]


def edit_distance(s1, s2):
    """
    编辑距离
    返回: (距离, 操作序列)
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

    return dp[m][n], dp


def demo_fibonacci():
    """斐波那契演示"""
    print("=" * 60)
    print("1. 斐波那契数列")
    print("=" * 60)

    n = 10
    fibs = [fib_dp(i) for i in range(n + 1)]
    print(f"前{n}个斐波那契数: {fibs}")
    print(f"第{n}个: {fib_dp(n)}\n")


def demo_knapsack():
    """背包问题演示"""
    print("=" * 60)
    print("2. 01背包问题")
    print("=" * 60)

    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 8

    max_val, selected = knapsack_01(weights, values, capacity)
    print(f"物品重量: {weights}")
    print(f"物品价值: {values}")
    print(f"背包容量: {capacity}")
    print(f"最大价值: {max_val}")
    print(f"选择物品索引: {selected}\n")


def demo_lcs():
    """LCS演示"""
    print("=" * 60)
    print("3. 最长公共子序列")
    print("=" * 60)

    s1, s2 = "ABCDGH", "AEDFHR"
    length, lcs_str = lcs(s1, s2)
    print(f"字符串1: {s1}")
    print(f"字符串2: {s2}")
    print(f"LCS长度: {length}")
    print(f"LCS: {lcs_str}\n")


def demo_lis():
    """LIS演示"""
    print("=" * 60)
    print("4. 最长递增子序列")
    print("=" * 60)

    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    length, sequence = lis(nums)
    print(f"数组: {nums}")
    print(f"LIS长度: {length}")
    print(f"LIS: {sequence}\n")


def demo_edit_distance():
    """编辑距离演示"""
    print("=" * 60)
    print("5. 编辑距离")
    print("=" * 60)

    s1, s2 = "horse", "ros"
    dist, dp = edit_distance(s1, s2)
    print(f"字符串1: {s1}")
    print(f"字符串2: {s2}")
    print(f"编辑距离: {dist}")
    print(f"DP表:\n{np.array(dp)}\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("动态规划 (Dynamic Programming) 完整示例")
    print("=" * 60 + "\n")

    demo_fibonacci()
    demo_knapsack()
    demo_lcs()
    demo_lis()
    demo_edit_distance()

    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
