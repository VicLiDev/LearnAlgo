/*************************************************************************
    > File Name: 1.tree_structure.c
    > Author: LiHongjin
    > Mail: 872648180@qq.com
    > Created Time: Wed 28 Aug 09:50:16 2024
 ************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 定义树节点结构
typedef struct TreeNode {
    char value[100];
    struct TreeNode** children;
    int child_count;
} TreeNode;

// 创建新的树节点
TreeNode* create_node(const char* value)
{
    TreeNode* node = (TreeNode*)malloc(sizeof(TreeNode));
    strcpy(node->value, value);
    node->children = NULL;
    node->child_count = 0;
    return node;
}

// 添加子节点
void add_child(TreeNode* parent, TreeNode* child)
{
    parent->child_count++;
    parent->children = (TreeNode**)realloc(parent->children, parent->child_count * sizeof(TreeNode*));
    parent->children[parent->child_count - 1] = child;
}

// 递归打印树结构
void print_tree(TreeNode* node, char* prefix, int is_last)
{
    // 打印当前节点
    printf("%s", prefix);

    if (is_last) {
        // 当前节点的前缀，打印当前节点使用
        printf("└── ");
        // 当前节点的前缀，打印当前节点的子节点使用
        strcat(prefix, "    ");
    } else {
        // 当前节点的前缀，打印当前节点使用
        printf("├── ");
        // 当前节点的前缀，打印当前节点的子节点使用
        strcat(prefix, "│   ");
    }

    printf("%s\n", node->value);

    // 处理子节点
    for (int i = 0; i < node->child_count; i++) {
        // 动态分配新的prefix缓冲区以防止溢出
        char* new_prefix = (char*)malloc(strlen(prefix) + 5); // 5: "│   " 或 "    " 的长度
        strcpy(new_prefix, prefix);
        print_tree(node->children[i], new_prefix, i == node->child_count - 1);
        free(new_prefix);
    }
}

// 释放树的内存
void free_tree(TreeNode* node)
{
    for (int i = 0; i < node->child_count; i++) {
        free_tree(node->children[i]);
    }
    free(node->children);
    free(node);
}

int main()
{
    // 创建根节点
    TreeNode* root = create_node("Root");

    // 添加子节点到根节点
    TreeNode* child1 = create_node("Child1");
    TreeNode* child2 = create_node("Child2");
    add_child(root, child1);
    add_child(root, child2);

    // 添加子节点到 Child2
    TreeNode* child3 = create_node("Child3");
    TreeNode* child4 = create_node("Child4");
    TreeNode* child5 = create_node("Child5");
    add_child(child1, child3);
    add_child(child1, child4);
    add_child(child1, child5);

    // 添加子节点到 Child4
    TreeNode* child6 = create_node("Child6");
    add_child(child4, child6);

    // 打印树结构
    char* prefix = (char*)malloc(1);
    prefix[0] = '\0';
    print_tree(root, prefix, 1);
    free(prefix);

    // 释放树的内存
    free_tree(root);

    return 0;
}
