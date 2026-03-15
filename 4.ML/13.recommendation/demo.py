"""
推荐系统 (Recommendation System) 示例代码

包含内容:
1. 协同过滤基础概念
2. User-CF实现
3. Item-CF实现
4. 矩阵分解
5. 推荐评估
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from t01_mpl import chinese_font
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def create_sample_data():
    """创建示例评分数据"""
    np.random.seed(42)

    users = ['用户' + str(i) for i in range(1, 11)]
    items = ['商品' + chr(65 + i) for i in range(10)]

    # 创建评分矩阵
    n_users = len(users)
    n_items = len(items)

    # 基础评分模式
    ratings = np.zeros((n_users, n_items))

    # 添加一些评分模式
    # 用户1-3喜欢商品A,B,C
    ratings[0:3, 0:3] = np.random.randint(4, 6, (3, 3))
    # 用户4-6喜欢商品D,E,F
    ratings[3:6, 3:6] = np.random.randint(4, 6, (3, 3))
    # 用户7-9喜欢商品G,H,I
    ratings[6:9, 6:9] = np.random.randint(4, 6, (3, 3))
    # 随机评分
    for i in range(n_users):
        for j in range(n_items):
            if ratings[i, j] == 0 and np.random.random() < 0.3:
                ratings[i, j] = np.random.randint(1, 6)

    return ratings, users, items


def demo_basic_concepts():
    """推荐系统基础概念"""
    print("=" * 60)
    print("1. 推荐系统基础概念")
    print("=" * 60)

    ratings, users, items = create_sample_data()

    # 创建DataFrame
    df = pd.DataFrame(ratings, index=users, columns=items)

    print("用户-商品评分矩阵:")
    print("-" * 60)
    print(df.astype(int).to_string())

    # 基本统计
    n_ratings = np.sum(ratings > 0)
    sparsity = 1 - n_ratings / (len(users) * len(items))

    print(f"\n基本统计:")
    print(f"  用户数: {len(users)}")
    print(f"  商品数: {len(items)}")
    print(f"  评分数: {n_ratings}")
    print(f"  稀疏度: {sparsity:.2%}")

    # 可视化评分分布
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 评分热力图
    ax1 = axes[0]
    im = ax1.imshow(ratings, cmap='YlOrRd', aspect='auto')
    ax1.set_xticks(range(len(items)))
    ax1.set_yticks(range(len(users)))
    ax1.set_xticklabels(items)
    ax1.set_yticklabels(users)
    ax1.set_xlabel('商品', fontsize=12)
    ax1.set_ylabel('用户', fontsize=12)
    ax1.set_title('用户-商品评分矩阵热力图', fontsize=14)
    plt.colorbar(im, ax=ax1, label='评分')

    # 评分分布
    ax2 = axes[1]
    rating_values = ratings[ratings > 0]
    ax2.hist(rating_values, bins=5, edgecolor='black', alpha=0.7, color='steelblue')
    ax2.set_xlabel('评分', fontsize=12)
    ax2.set_ylabel('频数', fontsize=12)
    ax2.set_title('评分分布', fontsize=14)
    ax2.set_xticks([1, 2, 3, 4, 5])
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('recommendation_basic.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("基础概念图已保存为 recommendation_basic.png\n")


def demo_user_cf():
    """基于用户的协同过滤"""
    print("=" * 60)
    print("2. 基于用户的协同过滤 (User-CF)")
    print("=" * 60)

    ratings, users, items = create_sample_data()

    # 计算用户相似度矩阵（余弦相似度）
    # 对未评分位置填充0
    user_similarity = cosine_similarity(ratings)

    print("用户相似度矩阵 (部分):")
    print("-" * 40)
    sim_df = pd.DataFrame(user_similarity[:5, :5],
                          index=users[:5], columns=users[:5])
    print(sim_df.round(3).to_string())

    # 为用户1推荐商品
    target_user = 0  # 用户1
    print(f"\n为{users[target_user]}推荐商品:")

    # 找相似用户
    similar_users = np.argsort(user_similarity[target_user])[::-1][1:4]  # 排除自己

    # 找出目标用户未评分的商品
    unrated_items = np.where(ratings[target_user] == 0)[0]

    # 预测评分
    predictions = {}
    for item in unrated_items:
        weighted_sum = 0
        sim_sum = 0
        for sim_user in similar_users:
            if ratings[sim_user, item] > 0:
                weighted_sum += user_similarity[target_user, sim_user] * ratings[sim_user, item]
                sim_sum += abs(user_similarity[target_user, sim_user])

        if sim_sum > 0:
            predictions[items[item]] = weighted_sum / sim_sum

    # 排序推荐
    sorted_pred = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
    print("推荐结果:")
    for item, score in sorted_pred[:3]:
        print(f"  {item}: 预测评分 {score:.2f}")

    # 可视化用户相似度
    fig, ax = plt.subplots(figsize=(10, 8))

    im = ax.imshow(user_similarity, cmap='coolwarm', aspect='auto')
    ax.set_xticks(range(len(users)))
    ax.set_yticks(range(len(users)))
    ax.set_xticklabels(users, rotation=45)
    ax.set_yticklabels(users)
    ax.set_title('用户相似度矩阵', fontsize=14)
    plt.colorbar(im, ax=ax, label='相似度')

    # 添加数值标注
    for i in range(len(users)):
        for j in range(len(users)):
            ax.text(j, i, f'{user_similarity[i, j]:.2f}', ha='center', va='center',
                   fontsize=8, color='white' if abs(user_similarity[i, j]) > 0.5 else 'black')

    plt.tight_layout()
    plt.savefig('recommendation_user_cf.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("User-CF图已保存为 recommendation_user_cf.png\n")


def demo_item_cf():
    """基于物品的协同过滤"""
    print("=" * 60)
    print("3. 基于物品的协同过滤 (Item-CF)")
    print("=" * 60)

    ratings, users, items = create_sample_data()

    # 计算物品相似度矩阵
    item_similarity = cosine_similarity(ratings.T)

    print("物品相似度矩阵 (部分):")
    print("-" * 40)
    sim_df = pd.DataFrame(item_similarity[:5, :5],
                          index=items[:5], columns=items[:5])
    print(sim_df.round(3).to_string())

    # 为用户1推荐商品
    target_user = 0
    print(f"\n为{users[target_user]}推荐商品 (Item-CF):")

    # 找出用户已评分的商品
    rated_items = np.where(ratings[target_user] > 0)[0]
    unrated_items = np.where(ratings[target_user] == 0)[0]

    # 预测评分
    predictions = {}
    for item in unrated_items:
        weighted_sum = 0
        sim_sum = 0
        for rated_item in rated_items:
            sim = item_similarity[item, rated_item]
            weighted_sum += sim * ratings[target_user, rated_item]
            sim_sum += abs(sim)

        if sim_sum > 0:
            predictions[items[item]] = weighted_sum / sim_sum

    # 排序推荐
    sorted_pred = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
    print("推荐结果:")
    for item, score in sorted_pred[:3]:
        print(f"  {item}: 预测评分 {score:.2f}")

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 8))

    im = ax.imshow(item_similarity, cmap='coolwarm', aspect='auto')
    ax.set_xticks(range(len(items)))
    ax.set_yticks(range(len(items)))
    ax.set_xticklabels(items, rotation=45)
    ax.set_yticklabels(items)
    ax.set_title('物品相似度矩阵', fontsize=14)
    plt.colorbar(im, ax=ax, label='相似度')

    plt.tight_layout()
    plt.savefig('recommendation_item_cf.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Item-CF图已保存为 recommendation_item_cf.png\n")


def demo_matrix_factorization():
    """矩阵分解"""
    print("=" * 60)
    print("4. 矩阵分解 (Matrix Factorization)")
    print("=" * 60)

    ratings, users, items = create_sample_data()

    n_users, n_items = ratings.shape
    n_factors = 5
    n_epochs = 100
    lr = 0.01
    reg = 0.1

    # 初始化隐因子矩阵
    np.random.seed(42)
    P = np.random.normal(0, 0.1, (n_users, n_factors))  # 用户矩阵
    Q = np.random.normal(0, 0.1, (n_items, n_factors))  # 物品矩阵

    # 记录训练过程
    losses = []

    # SGD训练
    for epoch in range(n_epochs):
        total_loss = 0
        n_ratings = 0

        for u in range(n_users):
            for i in range(n_items):
                if ratings[u, i] > 0:
                    # 预测
                    pred = np.dot(P[u], Q[i])
                    error = ratings[u, i] - pred

                    # 更新
                    P[u] += lr * (error * Q[i] - reg * P[u])
                    Q[i] += lr * (error * P[u] - reg * Q[i])

                    total_loss += error ** 2
                    n_ratings += 1

        rmse = np.sqrt(total_loss / n_ratings)
        losses.append(rmse)

        if (epoch + 1) % 20 == 0:
            print(f"Epoch {epoch+1}: RMSE = {rmse:.4f}")

    # 重构评分矩阵
    predicted_ratings = np.dot(P, Q.T)

    print(f"\n最终RMSE: {losses[-1]:.4f}")

    # 可视化
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # 训练过程
    ax1 = axes[0]
    ax1.plot(losses, color='steelblue')
    ax1.set_xlabel('迭代次数', fontsize=12)
    ax1.set_ylabel('RMSE', fontsize=12)
    ax1.set_title('矩阵分解训练过程', fontsize=14)
    ax1.grid(True, alpha=0.3)

    # 原始矩阵
    ax2 = axes[1]
    im2 = ax2.imshow(ratings, cmap='YlOrRd', aspect='auto')
    ax2.set_title('原始评分矩阵', fontsize=14)
    ax2.set_xlabel('商品')
    ax2.set_ylabel('用户')
    plt.colorbar(im2, ax=ax2)

    # 重构矩阵
    ax3 = axes[2]
    im3 = ax3.imshow(predicted_ratings, cmap='YlOrRd', aspect='auto')
    ax3.set_title('重构评分矩阵', fontsize=14)
    ax3.set_xlabel('商品')
    ax3.set_ylabel('用户')
    plt.colorbar(im3, ax=ax3)

    plt.tight_layout()
    plt.savefig('recommendation_mf.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("矩阵分解图已保存为 recommendation_mf.png\n")

    # 使用重构矩阵推荐
    print("为用户1的推荐结果:")
    target_user = 0
    unrated = np.where(ratings[target_user] == 0)[0]
    pred_scores = predicted_ratings[target_user, unrated]
    sorted_idx = np.argsort(pred_scores)[::-1]

    for idx in sorted_idx[:3]:
        item_idx = unrated[idx]
        print(f"  {items[item_idx]}: 预测评分 {pred_scores[idx]:.2f}")
    print()


def demo_evaluation():
    """推荐系统评估"""
    print("=" * 60)
    print("5. 推荐系统评估")
    print("=" * 60)

    ratings, users, items = create_sample_data()

    # 划分训练集和测试集
    n_users, n_items = ratings.shape
    mask = ratings > 0
    train_mask = mask.copy()
    test_data = []

    np.random.seed(42)
    for u in range(n_users):
        rated_items = np.where(ratings[u] > 0)[0]
        if len(rated_items) > 2:
            test_items = np.random.choice(rated_items, size=min(2, len(rated_items)//3), replace=False)
            for i in test_items:
                train_mask[u, i] = False
                test_data.append((u, i, ratings[u, i]))

    train_ratings = ratings * train_mask

    # 简单的平均值预测
    user_means = np.true_divide(train_ratings.sum(1), (train_ratings > 0).sum(1),
                                where=(train_ratings > 0).sum(1) > 0)

    # 评估指标
    def evaluate(predictions, test_data):
        y_true = []
        y_pred = []
        for u, i, r in test_data:
            if predictions[u, i] != 0:
                y_true.append(r)
                y_pred.append(predictions[u, i])

        mae = np.mean(np.abs(np.array(y_true) - np.array(y_pred)))
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        return mae, rmse

    # 1. 平均值方法
    mean_pred = np.zeros_like(ratings)
    for u in range(n_users):
        mean_pred[u, :] = user_means[u]

    mae, rmse = evaluate(mean_pred, test_data)
    print(f"平均值方法: MAE={mae:.4f}, RMSE={rmse:.4f}")

    # 2. User-CF
    user_sim = cosine_similarity(train_ratings)
    user_cf_pred = np.zeros_like(ratings)

    for u in range(n_users):
        for i in range(n_items):
            if train_mask[u, i]:
                user_cf_pred[u, i] = train_ratings[u, i]
            else:
                sim_users = np.where((train_ratings[:, i] > 0) & (np.arange(n_users) != u))[0]
                if len(sim_users) > 0:
                    sims = user_sim[u, sim_users]
                    ratings_i = train_ratings[sim_users, i]
                    if np.sum(np.abs(sims)) > 0:
                        user_cf_pred[u, i] = np.dot(sims, ratings_i) / np.sum(np.abs(sims))

    mae, rmse = evaluate(user_cf_pred, test_data)
    print(f"User-CF:      MAE={mae:.4f}, RMSE={rmse:.4f}")

    # 3. Item-CF
    item_sim = cosine_similarity(train_ratings.T)
    item_cf_pred = np.zeros_like(ratings)

    for u in range(n_users):
        for i in range(n_items):
            if train_mask[u, i]:
                item_cf_pred[u, i] = train_ratings[u, i]
            else:
                sim_items = np.where((train_ratings[u, :] > 0) & (np.arange(n_items) != i))[0]
                if len(sim_items) > 0:
                    sims = item_sim[i, sim_items]
                    ratings_u = train_ratings[u, sim_items]
                    if np.sum(np.abs(sims)) > 0:
                        item_cf_pred[u, i] = np.dot(sims, ratings_u) / np.sum(np.abs(sims))

    mae, rmse = evaluate(item_cf_pred, test_data)
    print(f"Item-CF:      MAE={mae:.4f}, RMSE={rmse:.4f}")

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 6))

    methods = ['平均值', 'User-CF', 'Item-CF']
    maes = []
    rmses = []

    for pred, name in zip([mean_pred, user_cf_pred, item_cf_pred], methods):
        mae, rmse = evaluate(pred, test_data)
        maes.append(mae)
        rmses.append(rmse)

    x = np.arange(len(methods))
    width = 0.35

    ax.bar(x - width/2, maes, width, label='MAE', color='steelblue')
    ax.bar(x + width/2, rmses, width, label='RMSE', color='coral')

    ax.set_xlabel('方法', fontsize=12)
    ax.set_ylabel('误差', fontsize=12)
    ax.set_title('推荐算法评估对比', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(methods)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('recommendation_evaluation.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("评估对比图已保存为 recommendation_evaluation.png\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("推荐系统 (Recommendation System) 完整示例")
    print("=" * 60 + "\n")

    # 运行所有示例
    demo_basic_concepts()
    demo_user_cf()
    demo_item_cf()
    demo_matrix_factorization()
    demo_evaluation()

    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
