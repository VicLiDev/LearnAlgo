/*************************************************************************
    > File Name: demo.c
    > Author: LiHongjin
    > Mail: 872648180@qq.com
    > Created Time: Fri 16 Jan 14:55:01 2026
 ************************************************************************/

/*
 * 这个 C demo 包含：
 *   统计字符频率
 *   构建 Huffman 树（用最简单的数组模拟优先队列）
 *   生成 Huffman 编码表
 *   编码字符串为 bit 串（用 '0'/'1' 表示）
 *   从 bit 串解码还原原文
 */


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_CHARS 256
#define MAX_CODE_LEN 256

/* Huffman tree node */
typedef struct Node {
    unsigned char ch;
    int freq;
    struct Node *left;
    struct Node *right;
} Node;

/* create a new node */
Node* create_node(unsigned char ch, int freq, Node* left, Node* right)
{
    Node* n = (Node*)malloc(sizeof(Node));
    n->ch = ch;
    n->freq = freq;
    n->left = left;
    n->right = right;
    return n;
}

/* find index of node with minimum freq */
int find_min(Node** arr, int size)
{
    int min = 0;
    for (int i = 1; i < size; i++) {
        if (arr[i]->freq < arr[min]->freq) {
            min = i;
        }
    }
    return min;
}

/* build Huffman tree */
Node* build_huffman_tree(int freq[])
{
    Node* nodes[MAX_CHARS];
    int size = 0;

    /* init leaf nodes */
    for (int i = 0; i < MAX_CHARS; i++) {
        if (freq[i] > 0) {
            nodes[size++] = create_node((unsigned char)i, freq[i], NULL, NULL);
        }
    }

    /* edge case: only one symbol */
    if (size == 1) {
        nodes[size++] = create_node(0, 0, NULL, NULL);
    }

    /* merge nodes */
    // Huffman 树构建（核心算法）
    while (size > 1) {
        // 取频率最小的两个节点
        // 合并成新节点
        int i1 = find_min(nodes, size);
        Node* a = nodes[i1];
        nodes[i1] = nodes[--size];

        int i2 = find_min(nodes, size);
        Node* b = nodes[i2];
        nodes[i2] = nodes[--size];

        nodes[size++] = create_node(0, a->freq + b->freq, a, b);
    }

    return nodes[0];
}

/* generate Huffman codes */
void build_codes(Node* root, char* code, int depth, char codes[MAX_CHARS][MAX_CODE_LEN])
{
    if (!root) return;

    /* leaf */
    if (!root->left && !root->right) {
        code[depth] = '\0';
        strcpy(codes[root->ch], code);
        return;
    }

    code[depth] = '0';
    build_codes(root->left, code, depth + 1, codes);

    code[depth] = '1';
    build_codes(root->right, code, depth + 1, codes);
}

/* encode */
void encode(const unsigned char* text, char codes[MAX_CHARS][MAX_CODE_LEN], char* out)
{
    out[0] = '\0';
    while (*text) {
        strcat(out, codes[*text]);
        text++;
    }
}

/* decode */
void decode(const char* bits, Node* root, unsigned char* out)
{
    Node* cur = root;
    int pos = 0;

    while (*bits) {
        cur = (*bits == '0') ? cur->left : cur->right;

        if (!cur->left && !cur->right) {
            out[pos++] = cur->ch;
            cur = root;
        }
        bits++;
    }
    out[pos] = '\0';
}

/* free tree */
void free_tree(Node* root)
{
    if (!root) return;
    free_tree(root->left);
    free_tree(root->right);
    free(root);
}

/* demo */
int main(void)
{
    const unsigned char text[] = "ABBCCCDDDD";
    int freq[MAX_CHARS] = {0};

    /* count frequency */
    for (int i = 0; text[i]; i++) {
        freq[text[i]]++;
    }

    /* build Huffman tree */
    Node* root = build_huffman_tree(freq);

    /* build code table */
    char codes[MAX_CHARS][MAX_CODE_LEN] = {{0}};
    char tmp[MAX_CODE_LEN];
    build_codes(root, tmp, 0, codes);

    printf("Huffman Codes:\n");
    for (int i = 0; i < MAX_CHARS; i++) {
        if (codes[i][0]) {
            printf("%c : %s\n", i, codes[i]);
        }
    }

    /* encode */
    char encoded[1024];
    encode(text, codes, encoded);
    printf("\nEncoded bitstream:\n%s\n", encoded);

    /* decode */
    unsigned char decoded[1024];
    decode(encoded, root, decoded);
    printf("\nDecoded text:\n%s\n", decoded);

    free_tree(root);
    return 0;
}

