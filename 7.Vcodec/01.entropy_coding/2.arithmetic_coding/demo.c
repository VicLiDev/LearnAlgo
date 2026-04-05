/*************************************************************************
    > File Name: demo.c
    > Author: LiHongjin
    > Mail: 872648180@qq.com
    > Created Time: Fri 16 Jan 15:08:37 2026
 ************************************************************************/

/*
 * 功能
 *   编码字符串 → 一个浮点数
 *   用这个数反向解码 → 原字符串
 * 示例输出
 *   Encoded value: 0.2737500000
 *   Decoded text: ABAC
 */

#include <stdio.h>
#include <string.h>

/* symbol set */
#define SYMBOLS 3
char symbols[SYMBOLS] = {'A', 'B', 'C'};

/* cumulative probabilities */
double prob[SYMBOLS] = {0.5, 0.3, 0.2};
double cum[SYMBOLS + 1] = {0.0, 0.5, 0.8, 1.0};

/* get symbol index */
int sym_index(char c)
{
    for (int i = 0; i < SYMBOLS; i++) {
        if (symbols[i] == c)
            return i;
    }
    return -1;
}

/* arithmetic encode */
double encode(const char* text)
{
    double low = 0.0;
    double high = 1.0;

    for (int i = 0; text[i]; i++) {
        int s = sym_index(text[i]);
        double range = high - low;

        double new_low  = low + range * cum[s];
        double new_high = low + range * cum[s + 1];

        low = new_low;
        high = new_high;
    }

    /* return any value in [low, high) */
    return (low + high) / 2.0;
}

/* arithmetic decode */
void decode(double code, int length, char* out)
{
    double low = 0.0;
    double high = 1.0;

    for (int i = 0; i < length; i++) {
        double range = high - low;
        double value = (code - low) / range;

        int s;
        for (s = 0; s < SYMBOLS; s++) {
            if (value >= cum[s] && value < cum[s + 1])
                break;
        }

        out[i] = symbols[s];

        double new_low  = low + range * cum[s];
        double new_high = low + range * cum[s + 1];

        low = new_low;
        high = new_high;
    }
    out[length] = '\0';
}

/* demo */
int main(void)
{
    const char* text = "ABAC";
    int len = strlen(text);

    double code = encode(text);
    printf("Encoded value: %.10f\n", code);

    char decoded[64];
    decode(code, len, decoded);
    printf("Decoded text: %s\n", decoded);

    return 0;
}

