"""
变换编码示例：DCT、整数DCT、小波变换
"""
import numpy as np
from scipy.fftpack import dct, idct
import matplotlib.pyplot as plt
from t01_mpl import chinese_font
from PIL import Image


def dct2d(block):
    """2D DCT变换"""
    return dct(dct(block.T, norm='ortho').T, norm='ortho')


def idct2d(block):
    """2D IDCT逆变换"""
    return idct(idct(block.T, norm='ortho').T, norm='ortho')


def block_dct(image, block_size=8):
    """
    分块DCT变换

    Args:
        image: 输入图像
        block_size: 块大小

    Returns:
        dct_blocks: DCT系数块
    """
    h, w = image.shape
    dct_blocks = np.zeros_like(image, dtype=float)

    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            block = image[i:i+block_size, j:j+block_size]
            if block.shape == (block_size, block_size):
                dct_blocks[i:i+block_size, j:j+block_size] = dct2d(block)

    return dct_blocks


def block_idct(dct_blocks, block_size=8):
    """分块IDCT逆变换"""
    h, w = dct_blocks.shape
    image = np.zeros_like(dct_blocks)

    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            block = dct_blocks[i:i+block_size, j:j+block_size]
            if block.shape == (block_size, block_size):
                image[i:i+block_size, j:j+block_size] = idct2d(block)

    return image


def quantize_dct(dct_blocks, q_matrix, qp=10):
    """
    DCT系数量化

    Args:
        dct_blocks: DCT系数
        q_matrix: 量化矩阵
        qp: 量化参数

    Returns:
        quantized: 量化后的系数
    """
    q_scale = qp / 10.0
    quantized = np.round(dct_blocks / (q_matrix * q_scale))
    return quantized


def dequantize_dct(quantized, q_matrix, qp=10):
    """反量化"""
    q_scale = qp / 10.0
    return quantized * (q_matrix * q_scale)


def integer_dct4x4(block):
    """
    H.264 4x4 整数DCT

    使用整数运算，避免精度损失
    """
    # H.264整数DCT矩阵
    transform = np.array([
        [1,  1,  1,  1],
        [2,  1, -1, -2],
        [1, -1, -1,  1],
        [1, -2,  2, -1]
    ])

    # 正变换
    temp = transform @ block
    result = temp @ transform.T

    return result


def integer_idct4x4(block):
    """H.264 4x4 整数IDCT"""
    # 逆变换矩阵
    inv_transform = np.array([
        [1,  1,  1,  1],
        [1,  1, -1, -1],
        [1, -1, -1,  1],
        [1, -1,  1, -1]
    ]) / 4.0

    temp = inv_transform @ block
    result = temp @ inv_transform.T

    return result


def zigzag_scan(block):
    """
    Zigzag扫描 (8x8)

    将2D DCT系数转换为1D序列
    """
    zigzag = np.array([
        [0,  1,  5,  6, 14, 15, 27, 28],
        [2,  4,  7, 13, 16, 26, 29, 42],
        [3,  8, 12, 17, 25, 30, 41, 43],
        [9, 11, 18, 24, 31, 40, 44, 53],
        [10, 19, 23, 32, 39, 45, 52, 54],
        [20, 22, 33, 38, 46, 51, 55, 60],
        [21, 34, 37, 47, 50, 56, 59, 61],
        [35, 36, 48, 49, 57, 58, 62, 63]
    ])

    result = np.zeros(64)
    for i in range(8):
        for j in range(8):
            result[zigzag[i, j]] = block[i, j]

    return result


def demonstrate_dct_energy_compaction():
    """演示DCT能量集中特性"""
    print("=" * 50)
    print("DCT能量集中特性")
    print("=" * 50)

    # 创建测试图像块
    block = np.array([
        [139, 144, 149, 153, 155, 155, 155, 155],
        [144, 151, 153, 156, 159, 156, 156, 156],
        [150, 155, 160, 163, 158, 156, 156, 156],
        [159, 161, 162, 160, 160, 159, 159, 159],
        [159, 160, 161, 162, 162, 155, 155, 155],
        [161, 161, 161, 161, 160, 157, 157, 157],
        [162, 162, 161, 163, 162, 157, 157, 157],
        [162, 162, 161, 161, 163, 158, 158, 158]
    ], dtype=float)

    # DCT变换
    dct_block = dct2d(block)

    print("原始块 (8x8):")
    print(block.astype(int))

    print("\nDCT系数:")
    print(np.round(dct_block, 2))

    # 能量分析
    total_energy = np.sum(dct_block ** 2)
    dc_energy = dct_block[0, 0] ** 2
    low_freq_energy = np.sum(dct_block[:4, :4] ** 2)

    print(f"\nDC系数能量占比: {dc_energy/total_energy*100:.1f}%")
    print(f"低频区域(4x4)能量占比: {low_freq_energy/total_energy*100:.1f}%")

    # 可视化
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    im0 = axes[0].imshow(block, cmap='gray')
    axes[0].set_title('原始像素')
    plt.colorbar(im0, ax=axes[0])

    im1 = axes[1].imshow(np.abs(dct_block), cmap='hot')
    axes[1].set_title('|DCT系数|')
    plt.colorbar(im1, ax=axes[1])

    # 只保留低频系数
    dct_low = dct_block.copy()
    dct_low[4:, :] = 0
    dct_low[:, 4:] = 0
    reconstructed = idct2d(dct_low)

    im2 = axes[2].imshow(reconstructed, cmap='gray')
    axes[2].set_title('低频重建 (4x4)')
    plt.colorbar(im2, ax=axes[2])

    plt.tight_layout()
    plt.show()


def demonstrate_quantization_effect():
    """演示量化效果"""
    print("\n" + "=" * 50)
    print("量化效果演示")
    print("=" * 50)

    # 创建测试块
    block = np.array([
        [139, 144, 149, 153, 155, 155, 155, 155],
        [144, 151, 153, 156, 159, 156, 156, 156],
        [150, 155, 160, 163, 158, 156, 156, 156],
        [159, 161, 162, 160, 160, 159, 159, 159],
        [159, 160, 161, 162, 162, 155, 155, 155],
        [161, 161, 161, 161, 160, 157, 157, 157],
        [162, 162, 161, 163, 162, 157, 157, 157],
        [162, 162, 161, 161, 163, 158, 158, 158]
    ], dtype=float)

    # JPEG量化矩阵
    q_matrix = np.array([
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ], dtype=float)

    # DCT
    dct_block = dct2d(block)

    # 不同QP的量化效果
    qps = [5, 10, 20, 30]
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))

    axes[0, 0].imshow(block, cmap='gray', vmin=130, vmax=170)
    axes[0, 0].set_title('原始块')

    for idx, qp in enumerate(qps[:2]):
        quantized = quantize_dct(dct_block, q_matrix, qp)
        dequantized = dequantize_dct(quantized, q_matrix, qp)
        reconstructed = idct2d(dequantized)

        axes[0, idx+1].imshow(reconstructed, cmap='gray', vmin=130, vmax=170)
        mse = np.mean((block - reconstructed) ** 2)
        axes[0, idx+1].set_title(f'QP={qp}, MSE={mse:.2f}')

        print(f"QP={qp}: 量化后非零系数={np.count_nonzero(quantized)}, MSE={mse:.2f}")

    for idx, qp in enumerate(qps[2:]):
        quantized = quantize_dct(dct_block, q_matrix, qp)
        dequantized = dequantize_dct(quantized, q_matrix, qp)
        reconstructed = idct2d(dequantized)

        axes[1, idx].imshow(reconstructed, cmap='gray', vmin=130, vmax=170)
        mse = np.mean((block - reconstructed) ** 2)
        axes[1, idx].set_title(f'QP={qp}, MSE={mse:.2f}')

        print(f"QP={qp}: 量化后非零系数={np.count_nonzero(quantized)}, MSE={mse:.2f}")

    # DCT系数可视化
    axes[1, 2].imshow(np.abs(dct_block), cmap='hot')
    axes[1, 2].set_title('|DCT系数|')

    for ax in axes.flat:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def demonstrate_zigzag():
    """演示Zigzag扫描"""
    print("\n" + "=" * 50)
    print("Zigzag扫描")
    print("=" * 50)

    # 创建示例DCT块
    dct_block = np.array([
        [800,  50,  20,   5,   2,   1,   0,   0],
        [ 60,  30,  10,   3,   1,   0,   0,   0],
        [ 25,  15,   5,   2,   1,   0,   0,   0],
        [ 10,   5,   2,   1,   0,   0,   0,   0],
        [  5,   2,   1,   0,   0,   0,   0,   0],
        [  2,   1,   0,   0,   0,   0,   0,   0],
        [  1,   0,   0,   0,   0,   0,   0,   0],
        [  0,   0,   0,   0,   0,   0,   0,   0]
    ], dtype=float)

    # Zigzag扫描
    zigzag_result = zigzag_scan(dct_block)

    print("DCT系数矩阵:")
    print(dct_block.astype(int))

    print("\nZigzag扫描结果 (前20个):")
    print(zigzag_result[:20].astype(int))

    # 可视化
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    im0 = axes[0].imshow(np.abs(dct_block), cmap='hot')
    axes[0].set_title('DCT系数 (对数尺度)')
    plt.colorbar(im0, ax=axes[0])

    axes[1].plot(zigzag_result, 'b.-')
    axes[1].set_xlabel('Zigzag索引')
    axes[1].set_ylabel('系数值')
    axes[1].set_title('Zigzag扫描序列')
    axes[1].grid(True, alpha=0.3)
    axes[1].axhline(y=0, color='r', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()


def demonstrate_integer_dct():
    """演示整数DCT"""
    print("\n" + "=" * 50)
    print("整数DCT (H.264)")
    print("=" * 50)

    # 测试块
    block = np.array([
        [10, 20, 30, 40],
        [20, 30, 40, 50],
        [30, 40, 50, 60],
        [40, 50, 60, 70]
    ], dtype=float)

    # 整数DCT
    int_dct = integer_dct4x4(block)
    int_idct = integer_idct4x4(int_dct)

    print("原始4x4块:")
    print(block.astype(int))

    print("\n整数DCT结果:")
    print(np.round(int_dct, 2))

    print(f"\n重建误差: {np.linalg.norm(block - int_idct):.4f}")


def demo():
    """运行所有演示"""
    demonstrate_dct_energy_compaction()
    demonstrate_quantization_effect()
    demonstrate_zigzag()
    demonstrate_integer_dct()


if __name__ == "__main__":
    demo()
