"""
量化示例：标量量化、矩阵量化
"""
import numpy as np
import matplotlib.pyplot as plt
from t01_mpl import chinese_font


def scalar_quantize(x, qp):
    """标量量化"""
    return np.round(x / qp)


def scalar_dequantize(y, qp):
    """标量反量化"""
    return y * qp


def deadzone_quantize(x, qp):
    """死区量化 (H.264风格)"""
    return np.sign(x) * np.floor((np.abs(x) + qp/2) / qp)


def matrix_quantize(block, q_matrix, qp):
    """
    使用量化矩阵进行量化

    Args:
        block: 输入块 (通常是DCT系数)
        q_matrix: 量化矩阵
        qp: 量化参数

    Returns:
        量化后的块
    """
    q_scale = qp / 10.0
    return np.round(block / (q_matrix * q_scale))


def demonstrate_quantization_curve():
    """演示量化曲线"""
    print("=" * 50)
    print("量化曲线")
    print("=" * 50)

    x = np.linspace(-50, 50, 1000)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    for idx, qp in enumerate([5, 10, 20]):
        y = scalar_quantize(x, qp)
        y_dq = scalar_dequantize(y, qp)

        axes[idx].plot(x, x, 'b-', label='原始', alpha=0.5)
        axes[idx].plot(x, y_dq, 'r-', label=f'QP={qp}')
        axes[idx].set_xlabel('输入值')
        axes[idx].set_ylabel('量化值')
        axes[idx].set_title(f'标量量化 (QP={qp})')
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3)

        # 计算量化误差
        error = np.mean((x - y_dq) ** 2)
        print(f"QP={qp}: MSE = {error:.2f}")

    plt.tight_layout()
    plt.show()


def demonstrate_deadzone():
    """演示死区量化"""
    print("\n" + "=" * 50)
    print("死区量化")
    print("=" * 50)

    x = np.linspace(-20, 20, 1000)
    qp = 6

    y_standard = scalar_quantize(x, qp)
    y_deadzone = deadzone_quantize(x, qp)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(x, y_standard, 'b-', label='标准量化')
    axes[0].plot(x, y_deadzone, 'r--', label='死区量化')
    axes[0].set_xlabel('输入值')
    axes[0].set_ylabel('量化索引')
    axes[0].set_title('量化曲线比较')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # 死区大小
    axes[1].plot(x, y_standard * qp, 'b-', label='标准量化')
    axes[1].plot(x, y_deadzone * qp, 'r--', label='死区量化')
    axes[1].axhline(y=0, color='k', linestyle=':', alpha=0.3)
    axes[1].fill_between(x, -qp/2, qp/2, alpha=0.2, color='red', label='死区')
    axes[1].set_xlabel('输入值')
    axes[1].set_ylabel('重建值')
    axes[1].set_title('死区效应')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def demonstrate_qp_effect():
    """演示QP对压缩的影响"""
    print("\n" + "=" * 50)
    print("QP参数影响")
    print("=" * 50)

    # 创建测试信号
    x = np.random.randn(1000) * 30

    qps = [2, 5, 10, 20, 30, 50]

    results = []
    for qp in qps:
        y = scalar_quantize(x, qp)
        y_dq = scalar_dequantize(y, qp)

        mse = np.mean((x - y_dq) ** 2)
        nonzero = np.count_nonzero(y)
        rate = nonzero / len(x)  # 简化的码率估计

        results.append({
            'qp': qp,
            'mse': mse,
            'nonzero': nonzero,
            'rate': rate
        })

        print(f"QP={qp:2d}: MSE={mse:8.2f}, 非零系数={nonzero:4d}, 非零率={rate:.2%}")

    # 可视化
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    qps_list = [r['qp'] for r in results]
    mses = [r['mse'] for r in results]
    rates = [r['rate'] for r in results]

    axes[0].plot(qps_list, mses, 'bo-')
    axes[0].set_xlabel('QP')
    axes[0].set_ylabel('MSE')
    axes[0].set_title('QP vs 失真')
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(qps_list, rates, 'go-')
    axes[1].set_xlabel('QP')
    axes[1].set_ylabel('非零率')
    axes[1].set_title('QP vs 非零系数比例')
    axes[1].grid(True, alpha=0.3)

    # 率失真曲线
    axes[2].plot(rates, mses, 'ro-')
    axes[2].set_xlabel('非零率 (码率代理)')
    axes[2].set_ylabel('MSE (失真)')
    axes[2].set_title('率失真曲线')
    axes[2].grid(True, alpha=0.3)

    for i, r in enumerate(results):
        axes[2].annotate(f"QP={r['qp']}", (r['rate'], r['mse']),
                        textcoords="offset points", xytext=(5, 5))

    plt.tight_layout()
    plt.show()


def demo():
    """运行所有演示"""
    demonstrate_quantization_curve()
    demonstrate_deadzone()
    demonstrate_qp_effect()


if __name__ == "__main__":
    demo()
