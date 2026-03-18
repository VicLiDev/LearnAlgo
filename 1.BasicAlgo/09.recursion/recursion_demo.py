"""
递归 vs 非递归 (Recursion vs Iteration) 示例代码

包含内容:
1. 阶乘计算 - Factorial
2. 斐波那契数列 - Fibonacci
3. 二叉树遍历 - Tree Traversal
4. 汉诺塔问题 - Tower of Hanoi
5. 数组求和 - Array Sum

递归转非递归的核心思想:
- 使用栈(Stack)模拟函数调用栈
- 使用循环代替递归调用
- 手动维护状态变量
"""


# ==================== 1. 阶乘计算 ====================
def factorial_recursive(n):
    """递归方式计算阶乘"""
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)


def factorial_iterative(n):
    """非递归方式计算阶乘 - 使用循环"""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def factorial_stack(n):
    """非递归方式计算阶乘 - 使用栈模拟递归"""
    if n <= 1:
        return 1

    stack = list(range(n, 0, -1))  # [n, n-1, ..., 1]
    result = 1
    while stack:
        result *= stack.pop()
    return result


# ==================== 2. 斐波那契数列 ====================
def fibonacci_recursive(n):
    """递归方式计算斐波那契 (效率低，有重复计算)"""
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_iterative(n):
    """非递归方式计算斐波那契 - 使用循环"""
    if n <= 1:
        return n

    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr


def fibonacci_memo(n, memo=None):
    """带记忆化的递归 - 优化递归效率"""
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


# ==================== 3. 二叉树遍历 ====================
class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None


def inorder_recursive(root, result=None):
    """递归方式中序遍历 (左-根-右)"""
    if result is None:
        result = []
    if root:
        inorder_recursive(root.left, result)
        result.append(root.val)
        inorder_recursive(root.right, result)
    return result


def inorder_iterative(root):
    """非递归方式中序遍历 - 使用栈"""
    result = []
    stack = []
    curr = root

    while curr or stack:
        # 遍历到最左节点
        while curr:
            stack.append(curr)
            curr = curr.left
        # 访问节点
        curr = stack.pop()
        result.append(curr.val)
        # 转向右子树
        curr = curr.right

    return result


def preorder_recursive(root, result=None):
    """递归方式前序遍历 (根-左-右)"""
    if result is None:
        result = []
    if root:
        result.append(root.val)
        preorder_recursive(root.left, result)
        preorder_recursive(root.right, result)
    return result


def preorder_iterative(root):
    """非递归方式前序遍历 - 使用栈"""
    if not root:
        return []

    result = []
    stack = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)
        # 先右后左，保证左子树先访问
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return result


def postorder_recursive(root, result=None):
    """递归方式后序遍历 (左-右-根)"""
    if result is None:
        result = []
    if root:
        postorder_recursive(root.left, result)
        postorder_recursive(root.right, result)
        result.append(root.val)
    return result


def postorder_iterative(root):
    """非递归方式后序遍历 - 使用栈"""
    if not root:
        return []

    result = []
    stack = [(root, False)]  # (节点, 是否已访问过)

    while stack:
        node, visited = stack.pop()
        if visited:
            result.append(node.val)
        else:
            # 按 根-右-左 顺序入栈，出栈变为 左-右-根
            stack.append((node, True))
            if node.right:
                stack.append((node.right, False))
            if node.left:
                stack.append((node.left, False))

    return result


# ==================== 4. 汉诺塔问题 ====================
def hanoi_recursive(n, source='A', auxiliary='B', target='C', moves=None):
    """递归方式解决汉诺塔"""
    if moves is None:
        moves = []
    if n == 1:
        moves.append(f"{source} -> {target}")
    else:
        # 1. 将n-1个盘子从源柱移到辅助柱
        hanoi_recursive(n - 1, source, target, auxiliary, moves)
        # 2. 将最大盘子从源柱移到目标柱
        moves.append(f"{source} -> {target}")
        # 3. 将n-1个盘子从辅助柱移到目标柱
        hanoi_recursive(n - 1, auxiliary, source, target, moves)
    return moves


def hanoi_iterative(n):
    """非递归方式解决汉诺塔 - 使用栈模拟"""
    if n == 0:
        return []

    moves = []
    stack = [(n, 'A', 'B', 'C', False)]  # (数量, 源, 辅助, 目标, 已处理标志)

    while stack:
        count, source, aux, target, processed = stack.pop()

        if count == 1:
            moves.append(f"{source} -> {target}")
        elif processed:
            # 已处理过子问题，现在移动当前盘子
            moves.append(f"{source} -> {target}")
        else:
            # 模拟递归调用顺序（逆序入栈）
            # 第三步: 将n-1个从辅助柱移到目标柱
            stack.append((count - 1, aux, source, target, False))
            # 第二步: 移动当前盘子
            stack.append((1, source, aux, target, False))
            # 第一步: 将n-1个从源柱移到辅助柱
            stack.append((count - 1, source, target, aux, False))

    return moves


# ==================== 5. 数组求和 ====================
def sum_recursive(arr, n=None):
    """递归方式数组求和"""
    if n is None:
        n = len(arr)
    if n == 0:
        return 0
    return arr[n - 1] + sum_recursive(arr, n - 1)


def sum_iterative(arr):
    """非递归方式数组求和"""
    total = 0
    for num in arr:
        total += num
    return total


# ==================== 演示函数 ====================
def build_sample_tree():
    """构建示例二叉树
          1
         / \
        2   3
       / \
      4   5
    """
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    return root


def demo_factorial():
    print("\n" + "=" * 60)
    print("1. 阶乘计算 (Factorial)")
    print("=" * 60)

    n = 5
    print(f"计算 {n}!")
    print(f"  递归版本:       {factorial_recursive(n)}")
    print(f"  循环版本:       {factorial_iterative(n)}")
    print(f"  栈模拟版本:     {factorial_stack(n)}")


def demo_fibonacci():
    print("\n" + "=" * 60)
    print("2. 斐波那契数列 (Fibonacci)")
    print("=" * 60)

    n = 10
    print(f"计算第 {n} 个斐波那契数")
    print(f"  递归版本:       {fibonacci_recursive(n)}")
    print(f"  循环版本:       {fibonacci_iterative(n)}")
    print(f"  记忆化递归:     {fibonacci_memo(n)}")

    # 打印前10个斐波那契数
    print(f"\n前10个斐波那契数: {[fibonacci_iterative(i) for i in range(10)]}")


def demo_tree_traversal():
    print("\n" + "=" * 60)
    print("3. 二叉树遍历 (Tree Traversal)")
    print("=" * 60)

    root = build_sample_tree()
    print("示例二叉树结构:")
    print("      1")
    print("     / \\")
    print("    2   3")
    print("   / \\")
    print("  4   5")

    print("\n前序遍历 (根-左-右):")
    print(f"  递归版本:   {preorder_recursive(root)}")
    print(f"  非递归版本: {preorder_iterative(root)}")

    print("\n中序遍历 (左-根-右):")
    print(f"  递归版本:   {inorder_recursive(root)}")
    print(f"  非递归版本: {inorder_iterative(root)}")

    print("\n后序遍历 (左-右-根):")
    print(f"  递归版本:   {postorder_recursive(root)}")
    print(f"  非递归版本: {postorder_iterative(root)}")


def demo_hanoi():
    print("\n" + "=" * 60)
    print("4. 汉诺塔问题 (Tower of Hanoi)")
    print("=" * 60)

    n = 3
    print(f"{n}个盘子的汉诺塔解法 (A为源柱, B为辅助柱, C为目标柱):")

    print("\n递归版本:")
    moves_rec = hanoi_recursive(n)
    for i, move in enumerate(moves_rec, 1):
        print(f"  第{i}步: {move}")

    print("\n非递归版本:")
    moves_iter = hanoi_iterative(n)
    for i, move in enumerate(moves_iter, 1):
        print(f"  第{i}步: {move}")

    print(f"\n两种方式结果一致: {moves_rec == moves_iter}")


def demo_array_sum():
    print("\n" + "=" * 60)
    print("5. 数组求和 (Array Sum)")
    print("=" * 60)

    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"数组: {arr}")
    print(f"  递归版本:   {sum_recursive(arr)}")
    print(f"  非递归版本: {sum_iterative(arr)}")


def demo_comparison():
    print("\n" + "=" * 60)
    print("递归 vs 非递归 对比总结")
    print("=" * 60)
    print("""
┌─────────────────┬────────────────────┬────────────────────┐
│     特性        │       递归         │       非递归       │
├─────────────────┼────────────────────┼────────────────────┤
│ 代码可读性      │ 通常更简洁直观     │ 可能较复杂         │
│ 空间复杂度      │ O(递归深度) 栈空间 │ 通常 O(1) 或更优   │
│ 栈溢出风险      │ 深度递归可能溢出   │ 无此风险           │
│ 性能            │ 函数调用有开销     │ 通常更快           │
│ 调试难度        │ 较难追踪           │ 较易调试           │
│ 适用场景        │ 树/图遍历、分治    │ 简单迭代问题       │
└─────────────────┴────────────────────┴────────────────────┘

递归转非递归的关键技巧:
1. 使用显式栈模拟隐式调用栈
2. 用循环替代递归调用
3. 手动维护状态变量
4. 理解递归的执行顺序
""")


def main():
    """主函数 - 运行所有演示"""
    print("=" * 60)
    print("递归 vs 非递归 演示程序")
    print("=" * 60)

    demo_factorial()
    demo_fibonacci()
    demo_tree_traversal()
    demo_hanoi()
    demo_array_sum()
    demo_comparison()

    print("\n" + "=" * 60)
    print("演示结束!")
    print("=" * 60)


if __name__ == "__main__":
    main()
