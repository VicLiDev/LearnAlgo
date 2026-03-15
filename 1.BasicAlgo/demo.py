"""
数据结构 (Data Structures) 示例代码

包含内容:
1. 链表实现
2. 栈与队列
3. 二叉搜索树
4. 堆实现
5. 哈希表
"""


# ========== 链表 ==========
class ListNode:
    def __init__(self, val=0):
        self.val = val
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, val):
        if not self.head:
            self.head = ListNode(val)
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = ListNode(val)

    def to_list(self):
        result = []
        curr = self.head
        while curr:
            result.append(curr.val)
            curr = curr.next
        return result


# ========== 栈 ==========
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop() if self.items else None

    def peek(self):
        return self.items[-1] if self.items else None

    def is_empty(self):
        return len(self.items) == 0


# ========== 队列 ==========
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0) if self.items else None

    def is_empty(self):
        return len(self.items) == 0


# ========== 二叉搜索树 ==========
class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, val):
        if not self.root:
            self.root = TreeNode(val)
        else:
            self._insert(self.root, val)

    def _insert(self, node, val):
        if val < node.val:
            if node.left:
                self._insert(node.left, val)
            else:
                node.left = TreeNode(val)
        else:
            if node.right:
                self._insert(node.right, val)
            else:
                node.right = TreeNode(val)

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.val)
            self._inorder(node.right, result)


# ========== 堆 ==========
class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, val):
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        val = self.heap.pop()
        self._sift_down(0)
        return val

    def _sift_up(self, i):
        parent = (i - 1) // 2
        if i > 0 and self.heap[i] < self.heap[parent]:
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            self._sift_up(parent)

    def _sift_down(self, i):
        smallest = i
        left, right = 2*i + 1, 2*i + 2
        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right
        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self._sift_down(smallest)


def demo_data_structures():
    """演示各种数据结构"""
    print("=" * 60)
    print("数据结构演示")
    print("=" * 60)

    # 链表
    ll = LinkedList()
    for i in [1, 2, 3, 4, 5]:
        ll.append(i)
    print(f"链表: {ll.to_list()}")

    # 栈
    stack = Stack()
    for i in [1, 2, 3]:
        stack.push(i)
    print(f"栈pop: {[stack.pop() for _ in range(3)]}")

    # 队列
    queue = Queue()
    for i in [1, 2, 3]:
        queue.enqueue(i)
    print(f"队列dequeue: {[queue.dequeue() for _ in range(3)]}")

    # BST
    bst = BST()
    for i in [5, 3, 7, 1, 4, 6, 8]:
        bst.insert(i)
    print(f"BST中序遍历: {bst.inorder()}")

    # 堆
    heap = MinHeap()
    for i in [5, 3, 8, 1, 2]:
        heap.push(i)
    print(f"最小堆pop: {[heap.pop() for _ in range(5)]}")


if __name__ == "__main__":
    demo_data_structures()
