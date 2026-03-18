/**
 * 递归 vs 非递归 (Recursion vs Iteration) 示例代码 - C语言版本
 *
 * 包含内容:
 * 1. 阶乘计算 - Factorial
 * 2. 斐波那契数列 - Fibonacci
 * 3. 二叉树遍历 - Tree Traversal
 * 4. 汉诺塔问题 - Tower of Hanoi
 * 5. 数组求和 - Array Sum
 *
 * 递归转非递归的核心思想:
 * - 使用栈(Stack)模拟函数调用栈
 * - 使用循环代替递归调用
 * - 手动维护状态变量
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STACK_SIZE 1000

// ==================== 栈的实现 (用于非递归版本) ====================
typedef struct {
    int data[MAX_STACK_SIZE];
    int top;
} IntStack;

void stack_init(IntStack *s) { s->top = -1; }
int stack_is_empty(IntStack *s) { return s->top == -1; }
void stack_push(IntStack *s, int val) { s->data[++s->top] = val; }
int stack_pop(IntStack *s) { return s->data[s->top--]; }
int stack_peek(IntStack *s) { return s->data[s->top]; }

// ==================== 1. 阶乘计算 ====================
/**
 * 递归方式计算阶乘
 */
long long factorial_recursive(int n) {
    if (n <= 1) return 1;
    return n * factorial_recursive(n - 1);
}

/**
 * 非递归方式计算阶乘 - 使用循环
 */
long long factorial_iterative(int n) {
    long long result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

/**
 * 非递归方式计算阶乘 - 使用栈模拟递归
 */
long long factorial_stack(int n) {
    if (n <= 1) return 1;

    IntStack s;
    stack_init(&s);

    // 将 n, n-1, ..., 2 压入栈
    for (int i = n; i >= 2; i--) {
        stack_push(&s, i);
    }

    long long result = 1;
    while (!stack_is_empty(&s)) {
        result *= stack_pop(&s);
    }
    return result;
}

// ==================== 2. 斐波那契数列 ====================
/**
 * 递归方式计算斐波那契 (效率低，有重复计算)
 */
long long fibonacci_recursive(int n) {
    if (n <= 1) return n;
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2);
}

/**
 * 非递归方式计算斐波那契 - 使用循环
 */
long long fibonacci_iterative(int n) {
    if (n <= 1) return n;

    long long prev = 0, curr = 1;
    for (int i = 2; i <= n; i++) {
        long long next = prev + curr;
        prev = curr;
        curr = next;
    }
    return curr;
}

/**
 * 带记忆化的递归 - 优化递归效率
 */
long long fibonacci_memo_helper(int n, long long *memo) {
    if (memo[n] != -1) return memo[n];
    if (n <= 1) {
        memo[n] = n;
        return n;
    }
    memo[n] = fibonacci_memo_helper(n - 1, memo) + fibonacci_memo_helper(n - 2, memo);
    return memo[n];
}

long long fibonacci_memo(int n) {
    long long memo[100];
    for (int i = 0; i < 100; i++) memo[i] = -1;
    return fibonacci_memo_helper(n, memo);
}

// ==================== 3. 二叉树遍历 ====================
typedef struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

TreeNode* create_node(int val) {
    TreeNode *node = (TreeNode*)malloc(sizeof(TreeNode));
    node->val = val;
    node->left = NULL;
    node->right = NULL;
    return node;
}

/**
 * 递归方式前序遍历 (根-左-右)
 */
void preorder_recursive(TreeNode *root) {
    if (root) {
        printf("%d ", root->val);
        preorder_recursive(root->left);
        preorder_recursive(root->right);
    }
}

/**
 * 非递归方式前序遍历 - 使用栈
 */
void preorder_iterative(TreeNode *root) {
    if (!root) return;

    TreeNode *stack[MAX_STACK_SIZE];
    int top = -1;
    stack[++top] = root;

    while (top >= 0) {
        TreeNode *node = stack[top--];
        printf("%d ", node->val);

        // 先右后左，保证左子树先访问
        if (node->right) stack[++top] = node->right;
        if (node->left) stack[++top] = node->left;
    }
}

/**
 * 递归方式中序遍历 (左-根-右)
 */
void inorder_recursive(TreeNode *root) {
    if (root) {
        inorder_recursive(root->left);
        printf("%d ", root->val);
        inorder_recursive(root->right);
    }
}

/**
 * 非递归方式中序遍历 - 使用栈
 */
void inorder_iterative(TreeNode *root) {
    TreeNode *stack[MAX_STACK_SIZE];
    int top = -1;
    TreeNode *curr = root;

    while (curr || top >= 0) {
        // 遍历到最左节点
        while (curr) {
            stack[++top] = curr;
            curr = curr->left;
        }
        // 访问节点
        curr = stack[top--];
        printf("%d ", curr->val);
        // 转向右子树
        curr = curr->right;
    }
}

/**
 * 递归方式后序遍历 (左-右-根)
 */
void postorder_recursive(TreeNode *root) {
    if (root) {
        postorder_recursive(root->left);
        postorder_recursive(root->right);
        printf("%d ", root->val);
    }
}

/**
 * 非递归方式后序遍历 - 使用栈
 * 使用 (节点, 访问标志) 的方式
 */
void postorder_iterative(TreeNode *root) {
    if (!root) return;

    TreeNode *stack[MAX_STACK_SIZE];
    int visited[MAX_STACK_SIZE];  // 0: 未访问, 1: 已访问
    int top = -1;

    stack[++top] = root;
    visited[top] = 0;

    while (top >= 0) {
        TreeNode *node = stack[top];
        int is_visited = visited[top--];

        if (is_visited) {
            printf("%d ", node->val);
        } else {
            // 按 根-右-左 顺序入栈，出栈变为 左-右-根
            stack[++top] = node;
            visited[top] = 1;

            if (node->right) {
                stack[++top] = node->right;
                visited[top] = 0;
            }
            if (node->left) {
                stack[++top] = node->left;
                visited[top] = 0;
            }
        }
    }
}

// ==================== 4. 汉诺塔问题 ====================

/**
 * 递归方式解决汉诺塔
 */
void hanoi_recursive(int n, char src, char aux, char tgt, int *step) {
    if (n == 1) {
        printf("  第%d步: %c -> %c\n", (*step)++, src, tgt);
    } else {
        hanoi_recursive(n - 1, src, tgt, aux, step);
        printf("  第%d步: %c -> %c\n", (*step)++, src, tgt);
        hanoi_recursive(n - 1, aux, src, tgt, step);
    }
}

/**
 * 非递归方式解决汉诺塔 - 使用栈模拟
 */
typedef struct {
    int n;
    char src, aux, tgt;
    int stage;  // 0: 初始, 1: 处理中, 2: 完成
} HanoiFrame;

void hanoi_iterative(int n, char src, char aux, char tgt) {
    HanoiFrame stack[MAX_STACK_SIZE];
    int top = -1;
    int step = 1;

    // 初始帧入栈
    stack[++top] = (HanoiFrame){n, src, aux, tgt, 0};

    while (top >= 0) {
        HanoiFrame *frame = &stack[top];

        if (frame->n == 1) {
            printf("  第%d步: %c -> %c\n", step++, frame->src, frame->tgt);
            top--;
            continue;
        }

        switch (frame->stage) {
            case 0:
                // 第一阶段: 将 n-1 个从 src 移到 aux
                frame->stage = 1;
                stack[++top] = (HanoiFrame){frame->n - 1, frame->src, frame->tgt, frame->aux, 0};
                break;
            case 1:
                // 第二阶段: 移动当前盘子
                printf("  第%d步: %c -> %c\n", step++, frame->src, frame->tgt);
                frame->stage = 2;
                stack[++top] = (HanoiFrame){frame->n - 1, frame->aux, frame->src, frame->tgt, 0};
                break;
            case 2:
                // 完成
                top--;
                break;
        }
    }
}

// ==================== 5. 数组求和 ====================

/**
 * 递归方式数组求和
 */
int sum_recursive(int arr[], int n) {
    if (n == 0) return 0;
    return arr[n - 1] + sum_recursive(arr, n - 1);
}

/**
 * 非递归方式数组求和
 */
int sum_iterative(int arr[], int n) {
    int total = 0;
    for (int i = 0; i < n; i++) {
        total += arr[i];
    }
    return total;
}

// ==================== 演示函数 ====================

TreeNode* build_sample_tree() {
    /**
     *       1
     *      / \
     *     2   3
     *    / \
     *   4   5
     */
    TreeNode *root = create_node(1);
    root->left = create_node(2);
    root->right = create_node(3);
    root->left->left = create_node(4);
    root->left->right = create_node(5);
    return root;
}

void free_tree(TreeNode *root) {
    if (root) {
        free_tree(root->left);
        free_tree(root->right);
        free(root);
    }
}

void print_line() {
    printf("============================================================\n");
}

void demo_factorial() {
    printf("\n");
    print_line();
    printf("1. 阶乘计算 (Factorial)\n");
    print_line();

    int n = 5;
    printf("计算 %d!\n", n);
    printf("  递归版本:       %lld\n", factorial_recursive(n));
    printf("  循环版本:       %lld\n", factorial_iterative(n));
    printf("  栈模拟版本:     %lld\n", factorial_stack(n));
}

void demo_fibonacci() {
    printf("\n");
    print_line();
    printf("2. 斐波那契数列 (Fibonacci)\n");
    print_line();

    int n = 10;
    printf("计算第 %d 个斐波那契数\n", n);
    printf("  递归版本:       %lld\n", fibonacci_recursive(n));
    printf("  循环版本:       %lld\n", fibonacci_iterative(n));
    printf("  记忆化递归:     %lld\n", fibonacci_memo(n));

    printf("\n前10个斐波那契数: [");
    for (int i = 0; i < 10; i++) {
        printf("%lld", fibonacci_iterative(i));
        if (i < 9) printf(", ");
    }
    printf("]\n");
}

void demo_tree_traversal() {
    printf("\n");
    print_line();
    printf("3. 二叉树遍历 (Tree Traversal)\n");
    print_line();

    TreeNode *root = build_sample_tree();

    printf("示例二叉树结构:\n");
    printf("      1\n");
    printf("     / \\\n");
    printf("    2   3\n");
    printf("   / \\\n");
    printf("  4   5\n");

    printf("\n前序遍历 (根-左-右):\n");
    printf("  递归版本:   ");
    preorder_recursive(root);
    printf("\n  非递归版本: ");
    preorder_iterative(root);
    printf("\n");

    printf("\n中序遍历 (左-根-右):\n");
    printf("  递归版本:   ");
    inorder_recursive(root);
    printf("\n  非递归版本: ");
    inorder_iterative(root);
    printf("\n");

    printf("\n后序遍历 (左-右-根):\n");
    printf("  递归版本:   ");
    postorder_recursive(root);
    printf("\n  非递归版本: ");
    postorder_iterative(root);
    printf("\n");

    free_tree(root);
}

void demo_hanoi() {
    printf("\n");
    print_line();
    printf("4. 汉诺塔问题 (Tower of Hanoi)\n");
    print_line();

    int n = 3;
    printf("%d个盘子的汉诺塔解法 (A为源柱, B为辅助柱, C为目标柱):\n", n);

    printf("\n递归版本:\n");
    int step = 1;
    hanoi_recursive(n, 'A', 'B', 'C', &step);

    printf("\n非递归版本:\n");
    hanoi_iterative(n, 'A', 'B', 'C');
}

void demo_array_sum() {
    printf("\n");
    print_line();
    printf("5. 数组求和 (Array Sum)\n");
    print_line();

    int arr[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("数组: [");
    for (int i = 0; i < n; i++) {
        printf("%d", arr[i]);
        if (i < n - 1) printf(", ");
    }
    printf("]\n");

    printf("  递归版本:   %d\n", sum_recursive(arr, n));
    printf("  非递归版本: %d\n", sum_iterative(arr, n));
}

void demo_comparison() {
    printf("\n");
    print_line();
    printf("递归 vs 非递归 对比总结\n");
    print_line();
    printf("\n");
    printf("+-----------------+--------------------+--------------------+\n");
    printf("|     特性        |       递归         |       非递归       |\n");
    printf("+-----------------+--------------------+--------------------+\n");
    printf("| 代码可读性      | 通常更简洁直观     | 可能较复杂         |\n");
    printf("| 空间复杂度      | O(递归深度)栈空间  | 通常 O(1) 或更优   |\n");
    printf("| 栈溢出风险      | 深度递归可能溢出   | 无此风险           |\n");
    printf("| 性能            | 函数调用有开销     | 通常更快           |\n");
    printf("| 调试难度        | 较难追踪           | 较易调试           |\n");
    printf("| 适用场景        | 树/图遍历、分治    | 简单迭代问题       |\n");
    printf("+-----------------+--------------------+--------------------+\n");
    printf("\n");
    printf("递归转非递归的关键技巧:\n");
    printf("1. 使用显式栈模拟隐式调用栈\n");
    printf("2. 用循环替代递归调用\n");
    printf("3. 手动维护状态变量\n");
    printf("4. 理解递归的执行顺序\n");
}

int main() {
    print_line();
    printf("递归 vs 非递归 演示程序 (C语言版本)\n");
    print_line();

    demo_factorial();
    demo_fibonacci();
    demo_tree_traversal();
    demo_hanoi();
    demo_array_sum();
    demo_comparison();

    printf("\n");
    print_line();
    printf("演示结束!\n");
    print_line();

    return 0;
}
