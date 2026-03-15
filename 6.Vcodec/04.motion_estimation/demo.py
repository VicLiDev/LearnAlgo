"""
运动估计算法示例：全搜索、菱形搜索、三步搜索
"""
import numpy as np
import matplotlib.pyplot as plt
from t01_mpl import chinese_font


def full_search(reference, current, block_size=16, search_range=16):
    """
    全搜索 (Full Search)

    Args:
        reference: 参考帧
        current: 当前帧
        block_size: 块大小
        search_range: 搜索范围

    Returns:
        mv: 运动矢量
        sad_map: SAD分布图
    """
    h, w = current.shape
    mv = np.zeros((h // block_size, w // block_size, 2))
    sad_map = []

    for by in range(h // block_size):
        for bx in range(w // block_size):
            cy, cx = by * block_size, bx * block_size
            current_block = current[cy:cy+block_size, cx:cx+block_size]

            best_sad = float('inf')
            best_mv = (0, 0)
            block_sad = []

            for dy in range(-search_range, search_range + 1):
                row_sad = []
                for dx in range(-search_range, search_range + 1):
                    ry, rx = cy + dy, cx + dx

                    # 边界检查
                    if ry < 0 or rx < 0 or ry + block_size > h or rx + block_size > w:
                        row_sad.append(float('inf'))
                        continue

                    ref_block = reference[ry:ry+block_size, rx:rx+block_size]
                    sad = np.sum(np.abs(current_block - ref_block))

                    row_sad.append(sad)

                    if sad < best_sad:
                        best_sad = sad
                        best_mv = (dy, dx)

                block_sad.append(row_sad)

            mv[by, bx] = best_mv
            sad_map.append(np.array(block_sad))

    return mv, sad_map


def diamond_search(reference, current, block_size=16, search_range=16):
    """
    菱形搜索 (Diamond Search)

    Args:
        reference: 参考帧
        current: 当前帧
        block_size: 块大小
        search_range: 搜索范围

    Returns:
        mv: 运动矢量
    """
    h, w = current.shape
    mv = np.zeros((h // block_size, w // block_size, 2))

    # 大菱形模板
    large_diamond = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1),
                     (-2, 0), (2, 0), (0, -2), (0, 2)]
    # 小菱形模板
    small_diamond = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]

    for by in range(h // block_size):
        for bx in range(w // block_size):
            cy, cx = by * block_size, bx * block_size
            current_block = current[cy:cy+block_size, cx:cx+block_size]

            def compute_sad(dy, dx):
                ry, rx = cy + dy, cx + dx
                if ry < 0 or rx < 0 or ry + block_size > h or rx + block_size > w:
                    return float('inf')
                ref_block = reference[ry:ry+block_size, rx:rx+block_size]
                return np.sum(np.abs(current_block - ref_block))

            # 大菱形搜索
            center = (0, 0)
            for _ in range(search_range):
                best_sad = float('inf')
                best_point = center

                for dy, dx in large_diamond:
                    point = (center[0] + dy, center[1] + dx)
                    sad = compute_sad(point[0], point[1])
                    if sad < best_sad:
                        best_sad = sad
                        best_point = point

                if best_point == center:
                    break
                center = best_point

            # 小菱形搜索
            for _ in range(3):
                best_sad = float('inf')
                best_point = center

                for dy, dx in small_diamond:
                    point = (center[0] + dy, center[1] + dx)
                    sad = compute_sad(point[0], point[1])
                    if sad < best_sad:
                        best_sad = sad
                        best_point = point

                if best_point == center:
                    break
                center = best_point

            mv[by, bx] = center

    return mv


def three_step_search(reference, current, block_size=16, search_range=16):
    """
    三步搜索 (Three Step Search)

    Args:
        reference: 参考帧
        current: 当前帧
        block_size: 块大小
        search_range: 搜索范围

    Returns:
        mv: 运动矢量
    """
    h, w = current.shape
    mv = np.zeros((h // block_size, w // block_size, 2))

    for by in range(h // block_size):
        for bx in range(w // block_size):
            cy, cx = by * block_size, bx * block_size
            current_block = current[cy:cy+block_size, cx:cx+block_size]

            def compute_sad(dy, dx):
                ry, rx = cy + dy, cx + dx
                if ry < 0 or rx < 0 or ry + block_size > h or rx + block_size > w:
                    return float('inf')
                ref_block = reference[ry:ry+block_size, rx:rx+block_size]
                return np.sum(np.abs(current_block - ref_block))

            center = (0, 0)
            step = search_range // 2

            while step >= 1:
                best_sad = compute_sad(center[0], center[1])
                best_point = center

                # 检查8个邻域点
                for dy in [-step, 0, step]:
                    for dx in [-step, 0, step]:
                        if dy == 0 and dx == 0:
                            continue
                        point = (center[0] + dy, center[1] + dx)
                        sad = compute_sad(point[0], point[1])
                        if sad < best_sad:
                            best_sad = sad
                            best_point = point

                center = best_point
                step //= 2

            mv[by, bx] = center

    return mv


def create_test_sequence():
    """创建测试序列"""
    h, w = 64, 64

    # 参考帧：有方块
    reference = np.zeros((h, w))
    reference[10:26, 10:26] = 200

    # 当前帧：方块移动
    current = np.zeros((h, w))
    current[15:31, 20:36] = 200

    return reference, current


def demonstrate_search_algorithms():
    """演示搜索算法"""
    print("=" * 50)
    print("运动估计算法比较")
    print("=" * 50)

    reference, current = create_test_sequence()

    # 全搜索
    mv_fs, sad_map = full_search(reference, current, block_size=16, search_range=16)
    print(f"\n全搜索:")
    print(f"运动矢量:\n{mv_fs[:, :, 0]}\n{mv_fs[:, :, 1]}")

    # 菱形搜索
    mv_ds = diamond_search(reference, current, block_size=16, search_range=16)
    print(f"\n菱形搜索:")
    print(f"运动矢量:\n{mv_ds[:, :, 0]}\n{mv_ds[:, :, 1]}")

    # 三步搜索
    mv_tss = three_step_search(reference, current, block_size=16, search_range=16)
    print(f"\n三步搜索:")
    print(f"运动矢量:\n{mv_tss[:, :, 0]}\n{mv_tss[:, :, 1]}")

    # 可视化
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))

    axes[0, 0].imshow(reference, cmap='gray')
    axes[0, 0].set_title('参考帧')

    axes[0, 1].imshow(current, cmap='gray')
    axes[0, 1].set_title('当前帧')

    # SAD分布图
    if sad_map:
        axes[0, 2].imshow(sad_map[0], cmap='hot')
        axes[0, 2].set_title('SAD分布 (中心块)')

    # 运动矢量场
    def plot_mv_field(ax, mv, title):
        ax.imshow(current, cmap='gray', alpha=0.5)
        for by in range(mv.shape[0]):
            for bx in range(mv.shape[1]):
                cy, cx = by * 16 + 8, bx * 16 + 8
                dy, dx = mv[by, bx]
                ax.arrow(cx, cy, dx * 2, dy * 2, head_width=2, head_length=1,
                        fc='red', ec='red')
        ax.set_title(title)

    plot_mv_field(axes[1, 0], mv_fs, '全搜索 MV场')
    plot_mv_field(axes[1, 1], mv_ds, '菱形搜索 MV场')
    plot_mv_field(axes[1, 2], mv_tss, '三步搜索 MV场')

    for ax in axes.flat:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


def demo():
    """运行演示"""
    demonstrate_search_algorithms()


if __name__ == "__main__":
    demo()
