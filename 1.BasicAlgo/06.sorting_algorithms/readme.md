# 排序算法 (Sorting Algorithms)

## 1. 简介

排序算法是将一组数据按照特定顺序（升序或降序）重新排列的算法。

## 2. 算法分类

| 类型 | 算法 | 特点 |
|------|------|------|
| 比较排序 | 冒泡、选择、插入、快排、归并、堆排序 | 通过比较元素确定顺序 |
| 非比较排序 | 计数、基数、桶排序 | 利用数据特性 |

## 3. 基础排序算法

### 3.1 冒泡排序 (Bubble Sort)
```
重复遍历数组，相邻元素比较交换
```
- 时间复杂度: O(n²)
- 空间复杂度: O(1)
- 稳定排序

### 3.2 选择排序 (Selection Sort)
```
每轮选择最小元素放到已排序序列末尾
```
- 时间复杂度: O(n²)
- 空间复杂度: O(1)
- 不稳定排序

### 3.3 插入排序 (Insertion Sort)
```
将元素插入到已排序序列的正确位置
```
- 时间复杂度: O(n²)，最好O(n)
- 空间复杂度: O(1)
- 稳定排序
- 适合小规模或基本有序数据

## 4. 高级排序算法

### 4.1 快速排序 (Quick Sort)
**原理**: 分治思想，选择基准元素分区

```
quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
```

- 时间复杂度: 平均O(n log n)，最坏O(n²)
- 空间复杂度: O(log n)
- 不稳定排序
- 实践中通常最快

### 4.2 归并排序 (Merge Sort)
**原理**: 分治思想，先分解再合并

```
merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)
```

- 时间复杂度: O(n log n)
- 空间复杂度: O(n)
- 稳定排序
- 适合链表排序、外部排序

### 4.3 堆排序 (Heap Sort)
**原理**: 利用堆数据结构

```
1. 构建最大堆
2. 交换堆顶与末尾
3. 调整堆，重复步骤2
```

- 时间复杂度: O(n log n)
- 空间复杂度: O(1)
- 不稳定排序

## 5. 非比较排序

### 5.1 计数排序 (Counting Sort)
- 时间复杂度: O(n+k)
- 空间复杂度: O(k)
- 适合整数且范围小

### 5.2 基数排序 (Radix Sort)
- 时间复杂度: O(d(n+k))
- 空间复杂度: O(n+k)
- 按位排序

### 5.3 桶排序 (Bucket Sort)
- 时间复杂度: O(n+k)
- 空间复杂度: O(n+k)
- 适合均匀分布数据

## 6. 复杂度对比

| 算法 | 最好 | 平均 | 最坏 | 空间 | 稳定 |
|------|------|------|------|------|------|
| 冒泡 | O(n) | O(n²) | O(n²) | O(1) | ✓ |
| 选择 | O(n²) | O(n²) | O(n²) | O(1) | ✗ |
| 插入 | O(n) | O(n²) | O(n²) | O(1) | ✓ |
| 快排 | O(n log n) | O(n log n) | O(n²) | O(log n) | ✗ |
| 归并 | O(n log n) | O(n log n) | O(n log n) | O(n) | ✓ |
| 堆 | O(n log n) | O(n log n) | O(n log n) | O(1) | ✗ |

## 7. 选择指南

| 场景 | 推荐算法 |
|------|---------|
| 小规模数据 | 插入排序 |
| 大规模随机数据 | 快速排序 |
| 需要稳定排序 | 归并排序 |
| 空间受限 | 堆排序 |
| 整数范围小 | 计数排序 |
| 外部排序 | 归并排序 |

## 8. 示例代码

见 `demo.py`
