/*************************************************************************
    > File Name: trie.c
    > Author: LiHongjin
    > Mail: 872648180@qq.com
    > Created Time: Mon Jan 24 16:58:52 2022
 ************************************************************************/

#include<stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * Trie树，又称字典树、前缀树、单词查找树、键树，是一种多叉树形结构，是一种哈希树的变种
 * 时间复杂度：
 * 插入、查找的时间复杂度均为O(n),n为字符串的长度
 * 空间复杂度较高，O(26^n),典型空间换时间
 * 参考题目
 * ac代码：
*/
#define MAX 26 // 字符集大小

typedef struct trieNode {
    struct trieNode *next[MAX];
    int count; // 记录该字符出现次数
} trieNode;

/*
 * 初始化Trie树根结点
 */
void initTrie(trieNode **root)
{
    int i;

    *root = (trieNode *)malloc(sizeof(trieNode));
    (*root)->count = 0;

    for (i = 0; i < MAX; i ++) {
        (*root)->next[i] = NULL;
    }
}

/*
 * 清理trie树
 */
void delTrie(trieNode *root)
{
    int i;

    for (i = 0; i < MAX; i ++) {
        if (root->next[i] != NULL) {
            delTrie(root->next[i]);
        }
    }

    free(root);
}

/*
 * Trie树插入操作
 */
void insert(char *str, trieNode *root)
{
    int i;
    trieNode *p = root;

    while (*str != '\n') {
        if (p->next[*str - 'a'] == NULL) {
            trieNode *tmp = (trieNode *)malloc(sizeof(trieNode));
            for (i = 0; i < MAX; i ++) {
                tmp->next[i] = NULL;
            }
            tmp->count = 1;
            p->next[*str - 'a'] = tmp;
            p = p->next[*str - 'a'];
        } else {
            p = p->next[*str - 'a'];
            p->count ++;
        }
        str ++;
    }
}

/*
 * 统计前缀出现次数
 */
int count(char *search, trieNode *root)
{
    trieNode *p = root;

    while (*search != '\n') {
        if (p->next[*search - 'a'] == NULL) {
            return 0;
        } else {
            p = p->next[*search - 'a'];
            search ++;
        }
    }

    return p->count;
}


int main(void)
{
    char str[15];
    trieNode *root;

    // 初始化根结点
    initTrie(&root);

    printf("Please insert node (enter continue):\n");
    while (fgets(str, sizeof(str), stdin) && str[0] != '\n') {
        // 插入Trie树
        insert(str, root);
    }

    // 查找前缀出现次数
    printf("Query node count (enter continue):\n");
    while (fgets(str, sizeof(str), stdin) && str[0] != '\n') {
        printf("node count: %d\n", count(str, root));
    }

    delTrie(root);

    return 0;
}
