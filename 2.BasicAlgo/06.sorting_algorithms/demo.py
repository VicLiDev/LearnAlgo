"""
排序算法 (Sorting Algorithms) 示例代码
"""

import numpy as np
import matplotlib.pyplot as plt
from t01_mpl import chinese_font
import time

plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


# 基础排序
def bubble_sort(arr):
    """冒泡排序"""
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


def selection_sort(arr):
    """选择排序"""
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(arr):
    """插入排序"""
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr


# 高级排序
def quick_sort(arr):
    """快速排序"""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def merge_sort(arr):
    """归并排序"""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def heap_sort(arr):
    """堆排序"""
    def heapify(arr, n, i):
        largest = i
        left = 2*i + 1
        right = 2*i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    arr = arr.copy()
    n = len(arr)

    # 构建最大堆
    for i in range(n//2-1, -1, -1):
        heapify(arr, n, i)

    # 逐个提取
    for i in range(n-1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)

    return arr


def demo_sorting_comparison():
    """排序算法性能对比"""
    print("=" * 60)
    print("排序算法性能对比")
    print("=" * 60)

    sizes = [100, 500, 1000, 2000, 5000]
    algorithms = {
        '冒泡排序': bubble_sort,
        '选择排序': selection_sort,
        '插入排序': insertion_sort,
        '快速排序': quick_sort,
        '归并排序': merge_sort,
        '堆排序': heap_sort
    }

    results = {name: [] for name in algorithms}

    for size in sizes:
        arr = np.random.randint(0, 10000, size).tolist()

        for name, func in algorithms.items():
            start = time.time()
            func(arr)
            elapsed = time.time() - start
            results[name].append(elapsed)

        print(f"n={size}: ", end="")
        print(", ".join([f"{name[:2]}={results[name][-1]*1000:.1f}ms"
                        for name in ['快速排序', '归并排序', '堆排序']]))

    # 可视化
    fig, ax = plt.subplots(figsize=(12, 6))

    for name, times in results.items():
        ax.plot(sizes, [t*1000 for t in times], 'o-', label=name, linewidth=2)

    ax.set_xlabel('数据规模 (n)', fontsize=12)
    ax.set_ylabel('时间 (ms)', fontsize=12)
    ax.set_title('排序算法性能对比', fontsize=14)
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    ax.set_yscale('log')

    plt.tight_layout()
    plt.savefig('sorting_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("\n排序对比图已保存为 sorting_comparison.png\n")


if __name__ == "__main__":
    demo_sorting_comparison()
