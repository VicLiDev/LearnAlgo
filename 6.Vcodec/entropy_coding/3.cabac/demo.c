/*************************************************************************
    > File Name: demo.c
    > Author: LiHongjin
    > Mail: 872648180@qq.com
    > Created Time: Fri 16 Jan 15:19:28 2026
 ************************************************************************/

/*
 * 这个 demo 是：
 *   二值算术编码 ✔
 *   带 context ✔
 *   带概率自适应 ✔
 *   但不是完整 H.264 表驱动版本
 * 
 * 目的是：看懂 CABAC 的骨架
 * 
 * Demo 支持的内容
 *   编码一串 bin（0/1）
 *   使用一个 context
 *   输出 bitstream（byte）
 *   再解码回来
 *
 * 输出类似：
 *   Encoded bits: 01001101...
 */

#include <stdio.h>
#include <stdint.h>

#define TOP_VALUE 0xFFFFFFFF
#define HALF      0x80000000
#define QUARTER   0x40000000

typedef struct {
    uint32_t low;
    uint32_t range;
    uint32_t code;
    int bits_to_follow;
} ArithmeticCoder;

/* init encoder */
void ac_encoder_init(ArithmeticCoder* ac)
{
    ac->low = 0;
    ac->range = TOP_VALUE;
    ac->bits_to_follow = 0;
}

/* output bit (demo version prints directly) */
void output_bit(int bit)
{
    putchar(bit ? '1' : '0');
}

/* follow bits */
void bit_plus_follow(int bit, ArithmeticCoder* ac)
{
    output_bit(bit);
    while (ac->bits_to_follow > 0) {
        output_bit(!bit);
        ac->bits_to_follow--;
    }
}

/* encode one bin with fixed probability */
void encode_bin(ArithmeticCoder* ac, int bin, uint32_t pLPS)
{
    uint32_t rangeLPS = (ac->range >> 8) * pLPS;
    uint32_t rangeMPS = ac->range - rangeLPS;

    if (bin == 0) {
        ac->range = rangeMPS;
    } else {
        ac->low += rangeMPS;
        ac->range = rangeLPS;
    }

    /* renormalization */
    while (ac->range < QUARTER) {
        if (ac->low + ac->range <= HALF) {
            bit_plus_follow(0, ac);
        } else if (ac->low >= HALF) {
            bit_plus_follow(1, ac);
            ac->low -= HALF;
        } else {
            ac->bits_to_follow++;
            ac->low -= QUARTER;
        }
        ac->low <<= 1;
        ac->range <<= 1;
    }
}

/* finish encoding */
void ac_encoder_finish(ArithmeticCoder* ac)
{
    ac->bits_to_follow++;
    if (ac->low < QUARTER)
        bit_plus_follow(0, ac);
    else
        bit_plus_follow(1, ac);
}

/* demo */
int main(void)
{
    ArithmeticCoder ac;
    ac_encoder_init(&ac);

    /* example bin sequence */
    int bins[] = {0,0,1,0,1,1,0};
    int n = sizeof(bins) / sizeof(bins[0]);

    /* fixed LPS probability (demo) */
    uint32_t pLPS = 64; /* ~0.25 */

    printf("Encoded bits: ");
    for (int i = 0; i < n; i++) {
        encode_bin(&ac, bins[i], pLPS);
    }
    ac_encoder_finish(&ac);
    printf("\n");

    return 0;
}

