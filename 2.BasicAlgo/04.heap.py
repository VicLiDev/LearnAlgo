#!/usr/bin/env python
#########################################################################
# File Name: 3.heap.py
# Author: LiHongjin
# mail: 872648180@qq.com
# Created Time: Tue 26 Nov 17:28:03 2024
#########################################################################

import heapq

# heapq 模块提供了一个最小堆实现，堆中的元素是按照从小到大的顺序排列的。如果需要
# 最大堆，则可以通过修改元素的符号来间接实现。
# 常用操作
# heapq.heappush(heap, item)：将元素 item 添加到堆中，保持堆的性质。
# heapq.heappop(heap)：移除并返回堆中的最小元素（即根节点），然后重新调整堆。
# heapq.heapify(iterable)：将一个可迭代对象转换为堆结构，原地操作。

def min_heap():
    # 创建一个空的最小堆
    heap = []

    # 添加元素
    heapq.heappush(heap, 10)
    heapq.heappush(heap, 5)
    heapq.heappush(heap, 20)
    heapq.heappush(heap, 3)

    print("min heap:", heap)  # [3, 5, 20, 10]

    # 弹出最小元素
    min_elem = heapq.heappop(heap)
    print("pop min element:", min_elem)  # 3
    print("cur heap:", heap)  # [5, 10, 20]

    # 将一个列表转换为堆
    arr = [15, 10, 20, 5, 30]
    heapq.heapify(arr)
    print("conv list to min heap:", arr)  # [5, 10, 20, 15, 30]


def max_heap():
    # 创建一个空的最大堆
    max_heap = []

    # 使用负数来模拟最大堆
    heapq.heappush(max_heap, -10)
    heapq.heappush(max_heap, -5)
    heapq.heappush(max_heap, -20)
    heapq.heappush(max_heap, -3)

    print("max heap:", max_heap)  # [-20, -5, -10, -3]

    # 弹出最大元素（注意取负）
    max_elem = -heapq.heappop(max_heap)
    print("pop max element:", max_elem)  # 20
    print("cur heap:", max_heap)  # [-10, -5, -3]

    # 将一个列表转换为最大堆（取负）
    arr = [15, 10, 20, 5, 30]
    max_heap = [-x for x in arr]
    heapq.heapify(max_heap)
    print("conv list to max helap:", max_heap)  # [-30, -10, -20, -5, -15]

if __name__ == "__main__":
    min_heap()
    print()
    max_heap()
