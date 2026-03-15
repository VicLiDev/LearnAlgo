"""
码率控制示例：CRF、CBR、VBR
"""
import numpy as np
import matplotlib.pyplot as plt


def crf_to_qp(crf):
    """
    CRF到QP的转换

    CRF: 0-51 (18视觉无损, 23默认, 28可接受, 51最差)
    QP:  0-51
    """
    # 简化的转换公式
    qp = crf
    return qp


def estimate_complexity(frame):
    """估计帧复杂度"""
    # 使用梯度作为复杂度估计
    grad_x = np.abs(np.diff(frame, axis=1))
    grad_y = np.abs(np.diff(frame, axis=0))
    return np.mean(grad_x) + np.mean(grad_y)


def rate_control_cqp(n_frames, qp):
    """
    固定QP码率控制

    Args:
        n_frames: 帧数
        qp: 固定QP值

    Returns:
        qps: 每帧的QP
    """
    return np.full(n_frames, qp)


def rate_control_crf(frames, base_crf):
    """
    CRF码率控制 (简化版)

    Args:
        frames: 帧列表
        base_crf: 基础CRF值

    Returns:
        qps: 每帧的QP
    """
    n_frames = len(frames)
    qps = []

    # 计算每帧复杂度
    complexities = [estimate_complexity(f) for f in frames]
    avg_complexity = np.mean(complexities)

    for complexity in complexities:
        # 复杂度调整
        complexity_factor = complexity / avg_complexity

        # 复杂度越高，QP越低 (质量越好)
        adjusted_qp = base_crf - np.log2(complexity_factor) * 2
        adjusted_qp = np.clip(adjusted_qp, 0, 51)

        qps.append(adjusted_qp)

    return np.array(qps)


def rate_control_cbr(n_frames, target_bits_per_frame, buffer_size):
    """
    CBR码率控制 (简化版)

    Args:
        n_frames: 帧数
        target_bits_per_frame: 目标每帧比特数
        buffer_size: 缓冲区大小

    Returns:
        qps: 每帧的QP
    """
    qps = []
    buffer_level = buffer_size / 2  # 初始缓冲区水位

    base_qp = 23

    for i in range(n_frames):
        # 缓冲区反馈
        buffer_ratio = buffer_level / buffer_size

        # 缓冲区水位高 -> 降低QP (提高质量)
        # 缓冲区水位低 -> 提高QP (降低质量)
        qp_adjustment = (buffer_ratio - 0.5) * 10

        qp = base_qp - qp_adjustment
        qp = np.clip(qp, 10, 40)

        qps.append(qp)

        # 模拟编码和缓冲区更新
        bits = target_bits_per_frame * (1 + (qp - base_qp) / 50)
        buffer_level += bits - target_bits_per_frame
        buffer_level = np.clip(buffer_level, 0, buffer_size)

    return np.array(qps)


def demonstrate_rate_control_modes():
    """演示不同码率控制模式"""
    print("=" * 50)
    print("码率控制模式比较")
    print("=" * 50)

    n_frames = 100

    # 模拟帧序列 (不同复杂度)
    np.random.seed(42)
    frames = []
    for i in range(n_frames):
        # 复杂度周期性变化
        complexity = 10 + 20 * np.sin(i / 10) + np.random.rand() * 5
        frame = np.random.randn(100, 100) * complexity
        frames.append(frame)

    # CQP
    qps_cqp = rate_control_cqp(n_frames, 23)
    print(f"CQP: 平均QP = {np.mean(qps_cqp):.1f}")

    # CRF
    qps_crf = rate_control_crf(frames, 23)
    print(f"CRF: 平均QP = {np.mean(qps_crf):.1f}, 范围 [{np.min(qps_crf):.1f}, {np.max(qps_crf):.1f}]")

    # CBR
    qps_cbr = rate_control_cbr(n_frames, 10000, 50000)
    print(f"CBR: 平均QP = {np.mean(qps_cbr):.1f}, 范围 [{np.min(qps_cbr):.1f}, {np.max(qps_cbr):.1f}]")

    # 可视化
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    frame_indices = np.arange(n_frames)

    # 复杂度
    complexities = [estimate_complexity(f) for f in frames]
    axes[0, 0].plot(frame_indices, complexities)
    axes[0, 0].set_xlabel('帧号')
    axes[0, 0].set_ylabel('复杂度')
    axes[0, 0].set_title('帧复杂度')
    axes[0, 0].grid(True, alpha=0.3)

    # QP曲线
    axes[0, 1].plot(frame_indices, qps_cqp, 'b-', label='CQP', alpha=0.7)
    axes[0, 1].plot(frame_indices, qps_crf, 'g-', label='CRF', alpha=0.7)
    axes[0, 1].plot(frame_indices, qps_cbr, 'r-', label='CBR', alpha=0.7)
    axes[0, 1].set_xlabel('帧号')
    axes[0, 1].set_ylabel('QP')
    axes[0, 1].set_title('QP曲线')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # 模拟码率
    def estimate_bits(qps):
        return 10000 * np.exp(-qps / 20)

    axes[1, 0].plot(frame_indices, estimate_bits(qps_cqp), 'b-', label='CQP', alpha=0.7)
    axes[1, 0].plot(frame_indices, estimate_bits(qps_crf), 'g-', label='CRF', alpha=0.7)
    axes[1, 0].plot(frame_indices, estimate_bits(qps_cbr), 'r-', label='CBR', alpha=0.7)
    axes[1, 0].axhline(y=10000, color='k', linestyle='--', alpha=0.5, label='目标码率')
    axes[1, 0].set_xlabel('帧号')
    axes[1, 0].set_ylabel('估计比特数')
    axes[1, 0].set_title('码率波动')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # 累积码率
    axes[1, 1].plot(frame_indices, np.cumsum(estimate_bits(qps_cqp)), 'b-', label='CQP')
    axes[1, 1].plot(frame_indices, np.cumsum(estimate_bits(qps_crf)), 'g-', label='CRF')
    axes[1, 1].plot(frame_indices, np.cumsum(estimate_bits(qps_cbr)), 'r-', label='CBR')
    axes[1, 1].plot(frame_indices, frame_indices * 10000, 'k--', label='目标累积')
    axes[1, 1].set_xlabel('帧号')
    axes[1, 1].set_ylabel('累积比特数')
    axes[1, 1].set_title('累积码率')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def demonstrate_crf_quality():
    """演示CRF值对质量的影响"""
    print("\n" + "=" * 50)
    print("CRF值对质量的影响")
    print("=" * 50)

    crfs = [18, 23, 28, 35]

    print("CRF参考:")
    for crf in crfs:
        quality = "视觉无损" if crf <= 18 else "默认" if crf == 23 else "可接受" if crf <= 28 else "质量较差"
        print(f"  CRF {crf}: {quality}")

    # 模拟质量-码率曲线
    fig, ax = plt.subplots(figsize=(10, 6))

    crf_range = np.arange(0, 52)
    quality = 100 * np.exp(-crf_range / 30)  # 模拟质量
    bitrate = 10 * np.exp(-crf_range / 15)   # 模拟码率 (Mbps)

    ax.plot(bitrate, quality, 'b-', linewidth=2)
    ax.set_xlabel('码率 (Mbps)')
    ax.set_ylabel('质量 (PSNR代理)')
    ax.set_title('率失真曲线')

    # 标记常用CRF值
    for crf in crfs:
        q = 100 * np.exp(-crf / 30)
        b = 10 * np.exp(-crf / 15)
        ax.scatter([b], [q], s=100)
        ax.annotate(f'CRF={crf}', (b, q), textcoords="offset points",
                   xytext=(10, 5), fontsize=10)

    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def demo():
    """运行所有演示"""
    demonstrate_rate_control_modes()
    demonstrate_crf_quality()


if __name__ == "__main__":
    demo()
