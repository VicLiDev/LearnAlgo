"""
环路滤波示例：去块滤波
"""
import numpy as np
import matplotlib.pyplot as plt


def create_blocking_artifact():
    """创建块效应"""
    h, w = 64, 64
    image = np.zeros((h, w))

    # 创建不同亮度的块
    for by in range(4):
        for bx in range(4):
            val = np.random.randint(50, 200)
            image[by*16:(by+1)*16, bx*16:(bx+1)*16] = val

    return image


def deblock_filter_simple(image, block_size=16, strength=1.0):
    """
    简单去块滤波

    Args:
        image: 输入图像
        block_size: 块大小
        strength: 滤波强度

    Returns:
        滤波后的图像
    """
    result = image.copy()
    h, w = image.shape

    # 垂直边界
    for x in range(block_size, w, block_size):
        for y in range(h):
            if x > 0 and x < w:
                # 边界两侧像素
                p0 = result[y, x - 1]
                q0 = result[y, x]

                # 简单平均
                avg = (p0 + q0) / 2
                result[y, x - 1] = p0 + strength * (avg - p0)
                result[y, x] = q0 + strength * (avg - q0)

    # 水平边界
    for y in range(block_size, h, block_size):
        for x in range(w):
            if y > 0 and y < h:
                p0 = result[y - 1, x]
                q0 = result[y, x]

                avg = (p0 + q0) / 2
                result[y - 1, x] = p0 + strength * (avg - p0)
                result[y, x] = q0 + strength * (avg - q0)

    return result


def deblock_filter_h264_style(image, block_size=16, threshold=30):
    """
    H.264风格去块滤波

    Args:
        image: 输入图像
        block_size: 块大小
        threshold: 滤波阈值

    Returns:
        滤波后的图像
    """
    result = image.copy()
    h, w = image.shape

    def filter_edge(p2, p1, p0, q0, q1, q2, threshold):
        """边滤波"""
        # 检查是否需要滤波
        if abs(p0 - q0) > threshold:
            return p0, q0

        # 简化的H.264滤波
        delta = (q0 - p0) / 4

        p0_new = np.clip(p0 + delta, 0, 255)
        q0_new = np.clip(q0 - delta, 0, 255)

        return p0_new, q0_new

    # 垂直边界
    for x in range(block_size, w, block_size):
        for y in range(h):
            if x >= 2 and x < w - 2:
                p2, p1, p0 = result[y, x-3:x]
                q0, q1, q2 = result[y, x:x+3]

                p0_new, q0_new = filter_edge(p2, p1, p0, q0, q1, q2, threshold)

                result[y, x-1] = p0_new
                result[y, x] = q0_new

    # 水平边界
    for y in range(block_size, h, block_size):
        for x in range(w):
            if y >= 2 and y < h - 2:
                p2, p1, p0 = result[y-3:y, x]
                q0, q1, q2 = result[y:y+3, x]

                p0_new, q0_new = filter_edge(p2, p1, p0, q0, q1, q2, threshold)

                result[y-1, x] = p0_new
                result[y, x] = q0_new

    return result


def demonstrate_deblocking():
    """演示去块滤波"""
    print("=" * 50)
    print("去块滤波")
    print("=" * 50)

    # 创建有块效应的图像
    blocked = create_blocking_artifact()

    # 不同强度的滤波
    filtered_weak = deblock_filter_simple(blocked, strength=0.3)
    filtered_medium = deblock_filter_simple(blocked, strength=0.5)
    filtered_strong = deblock_filter_simple(blocked, strength=0.8)

    fig, axes = plt.subplots(2, 3, figsize=(12, 8))

    axes[0, 0].imshow(blocked, cmap='gray', vmin=0, vmax=255)
    axes[0, 0].set_title('原始 (有块效应)')

    axes[0, 1].imshow(filtered_weak, cmap='gray', vmin=0, vmax=255)
    axes[0, 1].set_title('弱滤波 (strength=0.3)')

    axes[0, 2].imshow(filtered_medium, cmap='gray', vmin=0, vmax=255)
    axes[0, 2].set_title('中等滤波 (strength=0.5)')

    axes[1, 0].imshow(filtered_strong, cmap='gray', vmin=0, vmax=255)
    axes[1, 0].set_title('强滤波 (strength=0.8)')

    # 边界放大
    axes[1, 1].imshow(blocked[:32, :32], cmap='gray', vmin=0, vmax=255)
    axes[1, 1].set_title('原始边界放大')

    axes[1, 2].imshow(filtered_medium[:32, :32], cmap='gray', vmin=0, vmax=255)
    axes[1, 2].set_title('滤波后边界放大')

    for ax in axes.flat:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def demonstrate_filter_strength():
    """演示滤波强度影响"""
    print("\n" + "=" * 50)
    print("滤波强度影响")
    print("=" * 50)

    blocked = create_blocking_artifact()

    strengths = [0, 0.2, 0.4, 0.6, 0.8, 1.0]

    fig, axes = plt.subplots(2, 3, figsize=(12, 8))

    for idx, strength in enumerate(strengths):
        if strength == 0:
            filtered = blocked
        else:
            filtered = deblock_filter_simple(blocked, strength=strength)

        ax = axes.flat[idx]
        ax.imshow(filtered, cmap='gray', vmin=0, vmax=255)
        ax.set_title(f'strength={strength}')

        ax.axis('off')

    plt.tight_layout()
    plt.show()


def demo():
    """运行所有演示"""
    demonstrate_deblocking()
    demonstrate_filter_strength()


if __name__ == "__main__":
    demo()
