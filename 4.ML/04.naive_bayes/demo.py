"""
贝叶斯算法示例
演示各种贝叶斯分类器的使用方法
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris, load_wine, fetch_20newsgroups
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import (GaussianNB, MultinomialNB, BernoulliNB,
                                  ComplementNB)
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, roc_curve, auc)
from sklearn.preprocessing import StandardScaler, label_binarize
from sklearn.multiclass import OneVsRestClassifier
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def demo_gaussian_nb():
    """高斯朴素贝叶斯示例"""
    print("=" * 60)
    print("1. 高斯朴素贝叶斯示例")
    print("=" * 60)

    # 加载数据
    iris = load_iris()
    X, y = iris.data, iris.target
    feature_names = iris.feature_names
    class_names = iris.target_names

    # 数据标准化（虽然朴素贝叶斯不严格要求，但有助于可视化）
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.3, random_state=42
    )

    # 训练模型
    gnb = GaussianNB()
    gnb.fit(X_train, y_train)

    # 预测
    y_pred = gnb.predict(X_test)
    y_pred_proba = gnb.predict_proba(X_test)

    # 评估
    accuracy = accuracy_score(y_test, y_pred)
    cv_score = cross_val_score(gnb, X_scaled, y, cv=5, scoring='accuracy').mean()

    print(f"\n模型参数:")
    print(f"  类别先验概率: {gnb.class_prior_}")
    print(f"  类别数量: {gnb.classes_}")

    print(f"\n评估指标:")
    print(f"  测试准确率: {accuracy:.4f}")
    print(f"  交叉验证准确率: {cv_score:.4f}")

    print("\n分类报告:")
    print(classification_report(y_test, y_pred, target_names=class_names))

    # 可视化决策边界（使用前两个特征）
    fig, ax = plt.subplots(figsize=(10, 8))

    # 创建网格
    x_min, x_max = X_scaled[:, 0].min() - 1, X_scaled[:, 0].max() + 1
    y_min, y_max = X_scaled[:, 1].min() - 1, X_scaled[:, 1].max() + 1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                         np.linspace(y_min, y_max, 200))

    # 只使用前两个特征训练用于可视化
    gnb_2d = GaussianNB()
    gnb_2d.fit(X_scaled[:, :2], y)

    Z = gnb_2d.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # 绘制决策边界
    ax.contourf(xx, yy, Z, alpha=0.3, cmap='rainbow')

    # 绘制数据点
    scatter = ax.scatter(X_scaled[:, 0], X_scaled[:, 1], c=y,
                         cmap='rainbow', edgecolors='black', s=50, alpha=0.7)

    ax.set_xlabel(feature_names[0] + ' (标准化)')
    ax.set_ylabel(feature_names[1] + ' (标准化)')
    ax.set_title('高斯朴素贝叶斯决策边界')
    plt.colorbar(scatter, ax=ax, label='类别')

    plt.tight_layout()
    plt.savefig('gaussian_nb_boundary.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: gaussian_nb_boundary.png")


def demo_multinomial_nb():
    """多项式朴素贝叶斯示例"""
    print("\n" + "=" * 60)
    print("2. 多项式朴素贝叶斯示例 (文本分类)")
    print("=" * 60)

    # 创建示例文本数据
    categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']
    try:
        newsgroups = fetch_20newsgroups(subset='train', categories=categories,
                                         remove=('headers', 'footers', 'quotes'))
        X_text = newsgroups.data
        y = newsgroups.target
        target_names = newsgroups.target_names
    except:
        # 如果无法下载数据，使用模拟数据
        print("无法下载20newsgroups数据集，使用模拟数据...")
        X_text = [
            "god is love and faith",
            "computer graphics rendering",
            "medical treatment doctor",
            "atheism disbelief religion",
            "image processing pixel",
            "health medicine patient",
            "christian church prayer",
            "3d modeling animation",
            "disease symptoms cure",
            "faith belief spiritual"
        ] * 10
        y = np.array([1, 2, 3, 0, 2, 3, 1, 2, 3, 1] * 10)
        target_names = ['atheism', 'christian', 'graphics', 'med']

    # 特征提取
    vectorizer = CountVectorizer(max_features=1000, stop_words='english')
    X = vectorizer.fit_transform(X_text)

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # 训练模型
    mnb = MultinomialNB(alpha=1.0)
    mnb.fit(X_train, y_train)

    # 预测
    y_pred = mnb.predict(X_test)

    # 评估
    accuracy = accuracy_score(y_test, y_pred)
    cv_score = cross_val_score(mnb, X, y, cv=5, scoring='accuracy').mean()

    print(f"\n评估指标:")
    print(f"  测试准确率: {accuracy:.4f}")
    print(f"  交叉验证准确率: {cv_score:.4f}")

    # 测试不同的alpha值
    alphas = [0.001, 0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
    train_scores = []
    test_scores = []

    for alpha in alphas:
        mnb_temp = MultinomialNB(alpha=alpha)
        mnb_temp.fit(X_train, y_train)
        train_scores.append(mnb_temp.score(X_train, y_train))
        test_scores.append(mnb_temp.score(X_test, y_test))

    # 可视化alpha的影响
    plt.figure(figsize=(10, 6))
    plt.semilogx(alphas, train_scores, 'o-', label='训练集', linewidth=2)
    plt.semilogx(alphas, test_scores, 's-', label='测试集', linewidth=2)
    plt.xlabel('Alpha (平滑参数)')
    plt.ylabel('准确率')
    plt.title('Alpha参数对多项式朴素贝叶斯的影响')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # 标记最佳alpha
    best_idx = np.argmax(test_scores)
    plt.scatter([alphas[best_idx]], [test_scores[best_idx]],
                color='red', s=100, zorder=5, label=f'最佳 alpha={alphas[best_idx]}')
    plt.legend()

    plt.tight_layout()
    plt.savefig('multinomial_nb_alpha.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n最佳alpha: {alphas[best_idx]}")
    print("图表已保存: multinomial_nb_alpha.png")


def demo_bernoulli_nb():
    """伯努利朴素贝叶斯示例"""
    print("\n" + "=" * 60)
    print("3. 伯努利朴素贝叶斯示例")
    print("=" * 60)

    # 加载数据
    wine = load_wine()
    X, y = wine.data, wine.target

    # 将连续特征二值化
    X_binary = (X > X.mean(axis=0)).astype(int)

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X_binary, y, test_size=0.3, random_state=42
    )

    # 训练模型
    bnb = BernoulliNB(alpha=1.0)
    bnb.fit(X_train, y_train)

    # 预测
    y_pred = bnb.predict(X_test)

    # 评估
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\n评估指标:")
    print(f"  测试准确率: {accuracy:.4f}")

    # 测试不同的二值化阈值
    thresholds = np.percentile(X, [10, 25, 50, 75, 90])
    threshold_scores = []

    for threshold in thresholds:
        X_bin = (X > threshold).astype(int)
        X_train_bin, X_test_bin, y_train_bin, y_test_bin = train_test_split(
            X_bin, y, test_size=0.3, random_state=42
        )
        bnb_temp = BernoulliNB(alpha=1.0)
        bnb_temp.fit(X_train_bin, y_train_bin)
        threshold_scores.append(bnb_temp.score(X_test_bin, y_test_bin))

    # 可视化
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(thresholds)), threshold_scores, 'o-', linewidth=2)
    plt.xticks(range(len(thresholds)), [f'{t:.2f}' for t in thresholds])
    plt.xlabel('二值化阈值 (百分位数)')
    plt.ylabel('准确率')
    plt.title('二值化阈值对伯努利朴素贝叶斯的影响')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('bernoulli_nb_threshold.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: bernoulli_nb_threshold.png")


def demo_complement_nb():
    """补充朴素贝叶斯示例（处理不平衡数据）"""
    print("\n" + "=" * 60)
    print("4. 补充朴素贝叶斯示例 (不平衡数据)")
    print("=" * 60)

    # 加载数据
    wine = load_wine()
    X, y = wine.data, wine.target

    # 创建不平衡数据集（保留更多类别0的样本）
    np.random.seed(42)
    keep_prob = {0: 0.9, 1: 0.3, 2: 0.3}  # 类别0保留90%，其他30%
    mask = np.array([np.random.rand() < keep_prob[label] for label in y])
    X_imb = X[mask]
    y_imb = y[mask]

    print(f"\n原始数据分布: {np.bincount(y)}")
    print(f"不平衡数据分布: {np.bincount(y_imb)}")

    # 将数据转换为非负（互补贝叶斯要求）
    X_shifted = X_imb - X_imb.min() + 1

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X_shifted, y_imb, test_size=0.3, random_state=42
    )

    # 比较多项式朴素贝叶斯和补充朴素贝叶斯
    models = {
        '多项式朴素贝叶斯': MultinomialNB(),
        '补充朴素贝叶斯': ComplementNB()
    }

    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        results[name] = acc
        print(f"\n{name}:")
        print(f"  准确率: {acc:.4f}")
        print(classification_report(y_test, y_pred, target_names=wine.target_names))

    # 可视化对比
    plt.figure(figsize=(10, 6))
    plt.bar(results.keys(), results.values(), color=['#1f77b4', '#ff7f0e'])
    plt.ylabel('准确率')
    plt.title('不平衡数据上的贝叶斯分类器对比')
    plt.ylim([0, 1])
    for i, (name, acc) in enumerate(results.items()):
        plt.text(i, acc + 0.02, f'{acc:.4f}', ha='center', va='bottom')
    plt.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('complement_nb_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: complement_nb_comparison.png")


def demo_all_nb_comparison():
    """所有朴素贝叶斯分类器对比"""
    print("\n" + "=" * 60)
    print("5. 所有朴素贝叶斯分类器对比")
    print("=" * 60)

    # 加载数据
    iris = load_iris()
    X, y = iris.data, iris.target

    # 准备不同类型的数据
    # 1. 标准化数据（高斯）
    X_gaussian = StandardScaler().fit_transform(X)

    # 2. 非负数据（多项式、补充）
    X_multinomial = X - X.min() + 1

    # 3. 二值数据（伯努利）
    X_bernoulli = (X > X.mean(axis=0)).astype(int)

    models = {
        '高斯朴素贝叶斯': (GaussianNB(), X_gaussian),
        '多项式朴素贝叶斯': (MultinomialNB(), X_multinomial),
        '伯努利朴素贝叶斯': (BernoulliNB(), X_bernoulli),
        '补充朴素贝叶斯': (ComplementNB(), X_multinomial)
    }

    results = {}
    for name, (model, X_data) in models.items():
        cv_scores = cross_val_score(model, X_data, y, cv=5, scoring='accuracy')
        results[name] = {
            'mean': cv_scores.mean(),
            'std': cv_scores.std()
        }
        print(f"{name}:")
        print(f"  平均准确率: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

    # 可视化对比
    fig, ax = plt.subplots(figsize=(12, 6))

    names = list(results.keys())
    means = [results[n]['mean'] for n in names]
    stds = [results[n]['std'] for n in names]

    x = np.arange(len(names))
    bars = ax.bar(x, means, yerr=stds, capsize=5, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])

    ax.set_ylabel('准确率')
    ax.set_title('朴素贝叶斯分类器对比')
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=15, ha='right')
    ax.set_ylim([0.8, 1.0])
    ax.grid(True, alpha=0.3, axis='y')

    # 添加数值标签
    for bar, mean in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.01,
                f'{mean:.4f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('all_nb_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: all_nb_comparison.png")


def demo_probability_estimation():
    """概率估计可视化"""
    print("\n" + "=" * 60)
    print("6. 概率估计可视化")
    print("=" * 60)

    # 加载数据
    iris = load_iris()
    X, y = iris.data, iris.target

    # 使用标准化数据
    X_scaled = StandardScaler().fit_transform(X)

    # 训练模型
    gnb = GaussianNB()
    gnb.fit(X_scaled, y)

    # 获取预测概率
    y_pred_proba = gnb.predict_proba(X_scaled)

    # 可视化每个类别的概率分布
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for i, ax in enumerate(axes):
        # 对每个类别，显示属于该类的样本的概率
        mask = y == i
        proba_class = y_pred_proba[mask, i]
        proba_other = y_pred_proba[~mask, i]

        ax.hist(proba_class, bins=20, alpha=0.6, label=f'类别{i} (正确)', color='blue')
        ax.hist(proba_other, bins=20, alpha=0.6, label='其他类别', color='red')

        ax.set_xlabel('预测概率')
        ax.set_ylabel('样本数')
        ax.set_title(f'类别{i}的概率分布')
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('probability_estimation.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: probability_estimation.png")


def demo_roc_curve():
    """ROC曲线示例"""
    print("\n" + "=" * 60)
    print("7. ROC曲线示例")
    print("=" * 60)

    # 加载数据（二分类）
    iris = load_iris()
    X, y = iris.data, iris.target

    # 只使用两个类别
    mask = y < 2
    X_binary = X[mask]
    y_binary = y[mask]

    # 标准化
    X_scaled = StandardScaler().fit_transform(X_binary)

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_binary, test_size=0.3, random_state=42
    )

    # 训练模型
    gnb = GaussianNB()
    gnb.fit(X_train, y_train)

    # 获取预测概率
    y_pred_proba = gnb.predict_proba(X_test)[:, 1]

    # 计算ROC曲线
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    roc_auc = auc(fpr, tpr)

    print(f"\nAUC: {roc_auc:.4f}")

    # 可视化ROC曲线
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC曲线 (AUC = {roc_auc:.4f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='随机猜测')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('假正率 (False Positive Rate)')
    plt.ylabel('真正率 (True Positive Rate)')
    plt.title('高斯朴素贝叶斯 ROC曲线')
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('roc_curve.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\n图表已保存: roc_curve.png")


def main():
    """主函数"""
    print("贝叶斯算法演示程序")
    print("=" * 60)

    # 运行所有示例
    demo_gaussian_nb()
    demo_multinomial_nb()
    demo_bernoulli_nb()
    demo_complement_nb()
    demo_all_nb_comparison()
    demo_probability_estimation()
    demo_roc_curve()

    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
