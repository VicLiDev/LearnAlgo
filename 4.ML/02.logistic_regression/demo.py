"""
逻辑回归 (Logistic Regression) 示例代码

包含内容:
1. 基础二分类逻辑回归
2. Sigmoid函数可视化
3. 多分类逻辑回归
4. 正则化效果对比
5. 决策边界可视化
6. ROC曲线分析
"""

import numpy as np
import matplotlib.pyplot as plt
from t01_mpl import chinese_font
from sklearn.datasets import make_classification, make_blobs, load_iris, load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report,
    roc_curve, auc, precision_recall_curve
)
import warnings
warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def demo_sigmoid():
    """Sigmoid函数可视化"""
    print("=" * 60)
    print("1. Sigmoid函数可视化")
    print("=" * 60)

    z = np.linspace(-10, 10, 100)
    sigmoid = 1 / (1 + np.exp(-z))

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Sigmoid函数
    ax1 = axes[0]
    ax1.plot(z, sigmoid, 'b-', linewidth=2, label='σ(z) = 1/(1+e⁻ᶻ)')
    ax1.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label='阈值=0.5')
    ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax1.axhline(y=1, color='k', linestyle='-', alpha=0.3)
    ax1.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax1.set_xlabel('z (线性输出)', fontsize=12)
    ax1.set_ylabel('σ(z) (概率)', fontsize=12)
    ax1.set_title('Sigmoid函数', fontsize=14)
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-0.1, 1.1)

    # Sigmoid导数
    ax2 = axes[1]
    sigmoid_derivative = sigmoid * (1 - sigmoid)
    ax2.plot(z, sigmoid_derivative, 'r-', linewidth=2, label="σ'(z) = σ(z)(1-σ(z))")
    ax2.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax2.set_xlabel('z', fontsize=12)
    ax2.set_ylabel("σ'(z)", fontsize=12)
    ax2.set_title('Sigmoid函数的导数', fontsize=14)
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('logistic_sigmoid.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Sigmoid函数图已保存为 logistic_sigmoid.png\n")

    print("Sigmoid函数特点:")
    print("  - 输出范围: (0, 1)，可解释为概率")
    print("  - 在z=0时，σ(z)=0.5")
    print("  - 导数最大值在z=0处，最大为0.25")
    print("  - 当|z|较大时，导数趋近于0（梯度消失问题）\n")


def demo_basic_logistic():
    """基础二分类逻辑回归"""
    print("=" * 60)
    print("2. 基础二分类逻辑回归")
    print("=" * 60)

    # 加载乳腺癌数据集
    data = load_breast_cancer()
    X, y = data.data, data.target

    # 划分数据
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    # 标准化
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 训练模型
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train_scaled, y_train)

    # 预测
    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]

    # 评估
    accuracy = accuracy_score(y_test, y_pred)

    print(f"数据集: 乳腺癌数据集")
    print(f"特征数: {X.shape[1]}")
    print(f"训练集大小: {len(X_train)}")
    print(f"测试集大小: {len(X_test)}")
    print(f"\n测试集准确率: {accuracy:.4f}")
    print(f"\n分类报告:")
    print(classification_report(y_test, y_pred, target_names=data.target_names))

    # 混淆矩阵可视化
    fig, ax = plt.subplots(figsize=(8, 6))
    cm = confusion_matrix(y_test, y_pred)

    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)

    classes = data.target_names
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=classes, yticklabels=classes,
           ylabel='真实标签',
           xlabel='预测标签',
           title=f'混淆矩阵 (准确率: {accuracy:.4f})')

    # 在格子中添加数值
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], 'd'),
                   ha="center", va="center",
                   color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.savefig('logistic_confusion_matrix.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("混淆矩阵已保存为 logistic_confusion_matrix.png\n")


def demo_decision_boundary():
    """决策边界可视化"""
    print("=" * 60)
    print("3. 决策边界可视化")
    print("=" * 60)

    # 生成2D数据
    X, y = make_classification(
        n_samples=300, n_features=2, n_redundant=0, n_informative=2,
        n_clusters_per_class=1, random_state=42
    )

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 训练模型
    model = LogisticRegression(random_state=42)
    model.fit(X_scaled, y)

    # 创建网格
    h = 0.02
    x_min, x_max = X_scaled[:, 0].min() - 1, X_scaled[:, 0].max() + 1
    y_min, y_max = X_scaled[:, 1].min() - 1, X_scaled[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    # 预测概率
    Z = model.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
    Z = Z.reshape(xx.shape)

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 8))

    # 绘制概率等高线
    contour = ax.contourf(xx, yy, Z, levels=20, alpha=0.8, cmap=plt.cm.RdYlBu)
    plt.colorbar(contour, ax=ax, label='正类概率')

    # 绘制决策边界 (概率=0.5)
    ax.contour(xx, yy, Z, levels=[0.5], colors='black', linewidths=2, linestyles='--')

    # 绘制数据点
    scatter = ax.scatter(X_scaled[:, 0], X_scaled[:, 1], c=y,
                        cmap=plt.cm.RdYlBu, edgecolors='black', s=50)

    ax.set_xlabel('特征1 (标准化)', fontsize=12)
    ax.set_ylabel('特征2 (标准化)', fontsize=12)
    ax.set_title('逻辑回归决策边界与概率等高线', fontsize=14)

    # 显示参数
    w = model.coef_[0]
    b = model.intercept_[0]
    ax.text(0.02, 0.98, f'w1={w[0]:.3f}, w2={w[1]:.3f}, b={b:.3f}',
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig('logistic_decision_boundary.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("决策边界图已保存为 logistic_decision_boundary.png\n")

    print(f"模型参数: w1={w[0]:.4f}, w2={w[1]:.4f}, b={b:.4f}")
    print("决策边界方程: w1*x1 + w2*x2 + b = 0\n")


def demo_multiclass():
    """多分类逻辑回归"""
    print("=" * 60)
    print("4. 多分类逻辑回归")
    print("=" * 60)

    # 加载鸢尾花数据集
    iris = load_iris()
    X, y = iris.data, iris.target

    # 只取前两个特征用于可视化
    X_2d = X[:, :2]

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_2d)

    # 比较不同多分类策略
    strategies = {
        'One-vs-Rest (OvR)': 'ovr',
        'Multinomial (Softmax)': 'multinomial'
    }

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for idx, (name, strategy) in enumerate(strategies.items()):
        ax = axes[idx]

        # 训练模型
        model = LogisticRegression(
            multi_class=strategy,
            max_iter=1000,
            random_state=42
        )
        model.fit(X_scaled, y)

        # 预测
        y_pred = model.predict(X_scaled)
        accuracy = accuracy_score(y, y_pred)

        # 创建网格
        h = 0.02
        x_min, x_max = X_scaled[:, 0].min() - 1, X_scaled[:, 0].max() + 1
        y_min, y_max = X_scaled[:, 1].min() - 1, X_scaled[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))

        # 预测网格点
        Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        # 绘制决策区域
        ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.Set1)

        # 绘制数据点
        for i, target_name in enumerate(iris.target_names):
            ax.scatter(X_scaled[y == i, 0], X_scaled[y == i, 1],
                      label=target_name, edgecolors='black', s=50)

        ax.set_xlabel('花萼长度 (标准化)', fontsize=11)
        ax.set_ylabel('花萼宽度 (标准化)', fontsize=11)
        ax.set_title(f'{name}\n准确率: {accuracy:.4f}', fontsize=12)
        ax.legend(loc='upper right')

    plt.suptitle('多分类逻辑回归策略对比', fontsize=14)
    plt.tight_layout()
    plt.savefig('logistic_multiclass.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("多分类对比图已保存为 logistic_multiclass.png\n")

    print("多分类策略说明:")
    print("  - OvR: 为每个类别训练一个二分类器，计算量少")
    print("  - Softmax: 直接优化多分类交叉熵，理论上更优\n")


def demo_regularization():
    """正则化效果对比"""
    print("=" * 60)
    print("5. 正则化效果对比")
    print("=" * 60)

    # 生成数据
    X, y = make_classification(
        n_samples=500, n_features=20, n_informative=10,
        n_redundant=5, random_state=42
    )

    # 划分数据
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # 标准化
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 测试不同的C值
    C_values = [0.001, 0.01, 0.1, 1, 10, 100]
    train_scores = []
    test_scores = []

    for C in C_values:
        model = LogisticRegression(C=C, max_iter=1000, random_state=42)
        model.fit(X_train_scaled, y_train)

        train_scores.append(model.score(X_train_scaled, y_train))
        test_scores.append(model.score(X_test_scaled, y_test))

    # 可视化
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 准确率曲线
    ax1 = axes[0]
    ax1.semilogx(C_values, train_scores, 'b-o', label='训练集准确率', markersize=8)
    ax1.semilogx(C_values, test_scores, 'r-s', label='测试集准确率', markersize=8)
    ax1.set_xlabel('正则化参数 C (越大正则化越弱)', fontsize=12)
    ax1.set_ylabel('准确率', fontsize=12)
    ax1.set_title('正则化强度对模型性能的影响', fontsize=14)
    ax1.legend(loc='lower right')
    ax1.grid(True, alpha=0.3)

    # 系数对比
    ax2 = axes[1]

    # 无正则化 vs 强正则化
    model_no_reg = LogisticRegression(C=100, max_iter=1000, random_state=42)
    model_no_reg.fit(X_train_scaled, y_train)

    model_strong_reg = LogisticRegression(C=0.01, max_iter=1000, random_state=42)
    model_strong_reg.fit(X_train_scaled, y_train)

    x_pos = np.arange(20)
    width = 0.35

    ax2.bar(x_pos - width/2, np.abs(model_no_reg.coef_[0]), width,
           label='C=100 (弱正则化)', alpha=0.7)
    ax2.bar(x_pos + width/2, np.abs(model_strong_reg.coef_[0]), width,
           label='C=0.01 (强正则化)', alpha=0.7)

    ax2.set_xlabel('特征索引', fontsize=12)
    ax2.set_ylabel('系数绝对值', fontsize=12)
    ax2.set_title('正则化对系数的影响', fontsize=14)
    ax2.legend(loc='upper right')
    ax2.set_xticks(x_pos)

    plt.tight_layout()
    plt.savefig('logistic_regularization.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("正则化效果对比图已保存为 logistic_regularization.png\n")

    print("正则化参数C的影响:")
    print("  - C较小 (强正则化): 系数被压缩，可能欠拟合")
    print("  - C较大 (弱正则化): 系数自由度大，可能过拟合")
    print(f"  - 测试集最优C值: {C_values[np.argmax(test_scores)]}\n")


def demo_roc_curve():
    """ROC曲线分析"""
    print("=" * 60)
    print("6. ROC曲线分析")
    print("=" * 60)

    # 加载乳腺癌数据集
    data = load_breast_cancer()
    X, y = data.data, data.target

    # 划分数据
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # 标准化
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 训练模型
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train_scaled, y_train)

    # 获取预测概率
    y_prob = model.predict_proba(X_test_scaled)[:, 1]

    # 计算ROC曲线
    fpr, tpr, thresholds = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)

    # 计算PR曲线
    precision, recall, _ = precision_recall_curve(y_test, y_prob)

    # 可视化
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # ROC曲线
    ax1 = axes[0]
    ax1.plot(fpr, tpr, 'b-', linewidth=2, label=f'ROC曲线 (AUC = {roc_auc:.4f})')
    ax1.plot([0, 1], [0, 1], 'k--', linewidth=1, label='随机分类器')
    ax1.fill_between(fpr, tpr, alpha=0.3)
    ax1.set_xlabel('假正率 (FPR)', fontsize=12)
    ax1.set_ylabel('真正率 (TPR)', fontsize=12)
    ax1.set_title('ROC曲线', fontsize=14)
    ax1.legend(loc='lower right')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim([0, 1])
    ax1.set_ylim([0, 1.05])

    # PR曲线
    ax2 = axes[1]
    ax2.plot(recall, precision, 'r-', linewidth=2, label='PR曲线')
    ax2.fill_between(recall, precision, alpha=0.3)
    ax2.set_xlabel('召回率 (Recall)', fontsize=12)
    ax2.set_ylabel('精确率 (Precision)', fontsize=12)
    ax2.set_title('Precision-Recall曲线', fontsize=14)
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim([0, 1])
    ax2.set_ylim([0, 1.05])

    plt.tight_layout()
    plt.savefig('logistic_roc_curve.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("ROC曲线图已保存为 logistic_roc_curve.png\n")

    print(f"ROC-AUC: {roc_auc:.4f}")
    print("\nROC曲线解读:")
    print("  - AUC=1.0: 完美分类器")
    print("  - AUC=0.5: 随机分类器")
    print("  - 曲线越靠近左上角，性能越好\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("逻辑回归 (Logistic Regression) 完整示例")
    print("=" * 60 + "\n")

    # 运行所有示例
    demo_sigmoid()
    demo_basic_logistic()
    demo_decision_boundary()
    demo_multiclass()
    demo_regularization()
    demo_roc_curve()

    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
