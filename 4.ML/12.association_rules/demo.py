"""
关联规则学习 (Association Rule Learning) 示例代码

包含内容:
1. Apriori算法示例
2. FP-Growth算法示例
3. 规则评估指标
4. 购物篮分析实战
5. 参数敏感性分析
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 尝试导入mlxtend
try:
    from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth
    from mlxtend.preprocessing import TransactionEncoder
    HAS_MLEXTEND = True
except ImportError:
    HAS_MLEXTEND = False
    print("警告: 未安装mlxtend，部分示例将跳过")
    print("安装: pip install mlxtend")


def demo_basic_concepts():
    """关联规则基本概念演示"""
    print("=" * 60)
    print("1. 关联规则基本概念")
    print("=" * 60)

    # 示例交易数据
    transactions = [
        {'牛奶', '面包', '尿布'},
        {'面包', '尿布', '啤酒', '鸡蛋'},
        {'牛奶', '尿布', '啤酒', '可乐'},
        {'面包', '牛奶', '尿布', '啤酒'},
        {'面包', '牛奶', '可乐'}
    ]

    n_transactions = len(transactions)

    # 计算各项的支持度
    item_support = defaultdict(int)
    for t in transactions:
        for item in t:
            item_support[item] += 1

    print(f"总交易数: {n_transactions}")
    print(f"\n各项支持度:")
    print("-" * 30)

    for item, count in sorted(item_support.items(), key=lambda x: -x[1]):
        support = count / n_transactions
        print(f"  {item}: {support:.2f} ({count}/{n_transactions})")

    # 计算一些规则的评估指标
    print(f"\n关联规则示例:")
    print("-" * 50)

    # {面包} -> {牛奶}
    bread_count = item_support['面包']
    milk_count = item_support['牛奶']
    bread_milk_count = sum(1 for t in transactions if '面包' in t and '牛奶' in t)

    support = bread_milk_count / n_transactions
    confidence = bread_milk_count / bread_count
    lift = confidence / (milk_count / n_transactions)

    print(f"\n规则: {{面包}} → {{牛奶}}")
    print(f"  支持度: {support:.3f}")
    print(f"  置信度: {confidence:.3f}")
    print(f"  提升度: {lift:.3f}")
    print(f"  解读: 购买面包的顾客中{confidence*100:.1f}%也会购买牛奶")

    # {尿布, 啤酒} -> {面包}
    diaper_beer_count = sum(1 for t in transactions if '尿布' in t and '啤酒' in t)
    diaper_beer_bread_count = sum(1 for t in transactions
                                   if '尿布' in t and '啤酒' in t and '面包' in t)

    if diaper_beer_count > 0:
        support = diaper_beer_bread_count / n_transactions
        confidence = diaper_beer_bread_count / diaper_beer_count
        bread_support = item_support['面包'] / n_transactions
        lift = confidence / bread_support

        print(f"\n规则: {{尿布, 啤酒}} → {{面包}}")
        print(f"  支持度: {support:.3f}")
        print(f"  置信度: {confidence:.3f}")
        print(f"  提升度: {lift:.3f}")

    print("\n指标解读:")
    print("  - 支持度: 规则在所有交易中出现的频率")
    print("  - 置信度: 前件发生时后件发生的概率")
    print("  - 提升度: >1表示正相关, =1表示独立, <1表示负相关\n")


def demo_apriori_manual():
    """手动实现Apriori算法"""
    print("=" * 60)
    print("2. Apriori算法手动实现")
    print("=" * 60)

    def get_support(transactions, itemset):
        """计算项集支持度"""
        count = sum(1 for t in transactions if itemset.issubset(t))
        return count / len(transactions)

    def generate_candidates(itemsets, k):
        """生成k-项集候选"""
        candidates = set()
        items = list(itemsets)
        for i in range(len(items)):
            for j in range(i+1, len(items)):
                union = items[i] | items[j]
                if len(union) == k:
                    candidates.add(union)
        return candidates

    def apriori(transactions, min_support=0.4):
        """Apriori算法"""
        n = len(transactions)
        frequent_itemsets = {}

        # 生成1-项集
        items = set()
        for t in transactions:
            for item in t:
                items.add(frozenset([item]))

        current_itemsets = items
        k = 1

        while current_itemsets:
            # 计算支持度并筛选
            valid_itemsets = {}
            for itemset in current_itemsets:
                support = get_support(transactions, itemset)
                if support >= min_support:
                    valid_itemsets[frozenset(itemset)] = support

            if not valid_itemsets:
                break

            frequent_itemsets.update(valid_itemsets)
            print(f"频繁{k}-项集: {len(valid_itemsets)}个")
            for itemset, support in valid_itemsets.items():
                print(f"  {set(itemset)}: {support:.2f}")

            # 生成下一轮候选
            k += 1
            current_itemsets = generate_candidates(set(valid_itemsets.keys()), k)

        return frequent_itemsets

    # 测试数据
    transactions = [
        {'A', 'B', 'C'},
        {'A', 'C'},
        {'A', 'D'},
        {'B', 'C', 'E'},
        {'A', 'B', 'C', 'E'},
        {'B', 'E'}
    ]

    print(f"交易数据 ({len(transactions)}条):")
    for i, t in enumerate(transactions, 1):
        print(f"  T{i}: {t}")

    print(f"\n运行Apriori算法 (最小支持度=0.33):")
    print("-" * 40)

    frequent_itemsets = apriori(transactions, min_support=0.33)
    print(f"\n发现频繁项集总数: {len(frequent_itemsets)}\n")


def demo_mlxtend_apriori():
    """使用mlxtend实现Apriori"""
    print("=" * 60)
    print("3. 使用mlxtend实现Apriori")
    print("=" * 60)

    if not HAS_MLEXTEND:
        print("请安装mlxtend: pip install mlxtend\n")
        return

    # 购物篮数据
    transactions = [
        ['牛奶', '面包', '尿布'],
        ['面包', '尿布', '啤酒', '鸡蛋'],
        ['牛奶', '尿布', '啤酒', '可乐'],
        ['面包', '牛奶', '尿布', '啤酒'],
        ['面包', '牛奶', '可乐'],
        ['面包', '牛奶', '尿布'],
        ['面包', '尿布', '啤酒'],
        ['牛奶', '尿布', '啤酒']
    ]

    print(f"交易数据 ({len(transactions)}条)")

    # 编码
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    # Apriori算法
    frequent_itemsets = apriori(df, min_support=0.25, use_colnames=True)
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(len)

    print(f"\n频繁项集 (支持度 >= 0.25):")
    print("-" * 50)
    print(frequent_itemsets.sort_values('support', ascending=False).to_string(index=False))

    # 生成关联规则
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)

    if len(rules) > 0:
        print(f"\n关联规则 (置信度 >= 0.5):")
        print("-" * 70)
        rules_display = rules[['antecedents', 'consequents', 'support',
                               'confidence', 'lift']].sort_values('lift', ascending=False)
        for _, row in rules_display.iterrows():
            print(f"  {set(row['antecedents'])} → {set(row['consequents'])}")
            print(f"    支持度={row['support']:.3f}, 置信度={row['confidence']:.3f}, 提升度={row['lift']:.3f}")

    # 可视化
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 支持度分布
    ax1 = axes[0]
    frequent_itemsets_by_length = frequent_itemsets.groupby('length')['support'].mean()
    ax1.bar(frequent_itemsets_by_length.index, frequent_itemsets_by_length.values,
           color='steelblue', alpha=0.7)
    ax1.set_xlabel('项集大小', fontsize=12)
    ax1.set_ylabel('平均支持度', fontsize=12)
    ax1.set_title('不同大小项集的平均支持度', fontsize=14)
    ax1.grid(True, alpha=0.3, axis='y')

    # 规则分布
    if len(rules) > 0:
        ax2 = axes[1]
        scatter = ax2.scatter(rules['support'], rules['confidence'],
                            c=rules['lift'], cmap='viridis', s=100, alpha=0.7)
        ax2.set_xlabel('支持度', fontsize=12)
        ax2.set_ylabel('置信度', fontsize=12)
        ax2.set_title('关联规则分布 (颜色=提升度)', fontsize=14)
        plt.colorbar(scatter, ax=ax2, label='提升度')
        ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('association_rules_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("\n关联规则分析图已保存为 association_rules_analysis.png\n")


def demo_fpgrowth():
    """FP-Growth算法"""
    print("=" * 60)
    print("4. FP-Growth算法")
    print("=" * 60)

    if not HAS_MLEXTEND:
        print("请安装mlxtend: pip install mlxtend\n")
        return

    # 大型数据集
    np.random.seed(42)
    items = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    # 生成有模式的交易数据
    transactions = []
    for _ in range(100):
        n_items = np.random.randint(2, 6)
        # 添加一些常见组合
        if np.random.random() < 0.3:
            t = {'A', 'B'}
        elif np.random.random() < 0.3:
            t = {'C', 'D'}
        else:
            t = set()
        # 添加随机项
        remaining = n_items - len(t)
        t.update(np.random.choice(items, min(remaining, len(items)), replace=False))
        transactions.append(list(t))

    # 编码
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    # 比较Apriori和FP-Growth
    import time

    print("比较Apriori和FP-Growth性能...")
    print("-" * 40)

    # Apriori
    start = time.time()
    freq_apriori = apriori(df, min_support=0.1, use_colnames=True)
    time_apriori = time.time() - start

    # FP-Growth
    start = time.time()
    freq_fpgrowth = fpgrowth(df, min_support=0.1, use_colnames=True)
    time_fpgrowth = time.time() - start

    print(f"Apriori:   发现{len(freq_apriori)}个频繁项集, 耗时{time_apriori:.4f}秒")
    print(f"FP-Growth: 发现{len(freq_fpgrowth)}个频繁项集, 耗时{time_fpgrowth:.4f}秒")
    print(f"FP-Growth加速比: {time_apriori/time_fpgrowth:.2f}x\n")

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 5))

    methods = ['Apriori', 'FP-Growth']
    times = [time_apriori, time_fpgrowth]
    colors = ['#3498db', '#e74c3c']

    bars = ax.bar(methods, times, color=colors, alpha=0.8)
    ax.set_ylabel('运行时间 (秒)', fontsize=12)
    ax.set_title('Apriori vs FP-Growth 性能对比', fontsize=14)

    for bar, t in zip(bars, times):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
               f'{t:.4f}s', ha='center', va='bottom', fontsize=11)

    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('apriori_vs_fpgrowth.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("性能对比图已保存为 apriori_vs_fpgrowth.png\n")


def demo_parameter_sensitivity():
    """参数敏感性分析"""
    print("=" * 60)
    print("5. 参数敏感性分析")
    print("=" * 60)

    if not HAS_MLEXTEND:
        print("请安装mlxtend: pip install mlxtend\n")
        return

    # 生成数据
    np.random.seed(42)
    items = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    transactions = []
    for _ in range(200):
        n_items = np.random.randint(2, 6)
        t = set(np.random.choice(items, n_items, replace=False))
        transactions.append(list(t))

    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    # 不同支持度阈值
    support_thresholds = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
    n_itemsets = []
    n_rules = []

    for sup in support_thresholds:
        freq = apriori(df, min_support=sup, use_colnames=True)
        n_itemsets.append(len(freq))

        if len(freq) > 0:
            rules = association_rules(freq, metric="confidence", min_threshold=0.5)
            n_rules.append(len(rules))
        else:
            n_rules.append(0)

    # 可视化
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 频繁项集数量
    ax1 = axes[0]
    ax1.plot(support_thresholds, n_itemsets, 'b-o', linewidth=2, markersize=8)
    ax1.set_xlabel('最小支持度', fontsize=12)
    ax1.set_ylabel('频繁项集数量', fontsize=12)
    ax1.set_title('支持度阈值对频繁项集数量的影响', fontsize=14)
    ax1.grid(True, alpha=0.3)

    # 规则数量
    ax2 = axes[1]
    ax2.plot(support_thresholds, n_rules, 'r-s', linewidth=2, markersize=8)
    ax2.set_xlabel('最小支持度', fontsize=12)
    ax2.set_ylabel('关联规则数量', fontsize=12)
    ax2.set_title('支持度阈值对规则数量的影响', fontsize=14)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('parameter_sensitivity.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("参数敏感性分析图已保存为 parameter_sensitivity.png\n")

    print("参数选择建议:")
    print("  - 支持度太低: 产生过多无意义的规则")
    print("  - 支持度太高: 漏掉有价值的稀有模式")
    print("  - 通常从0.05-0.1开始尝试")
    print("  - 置信度通常设为0.5-0.8")
    print("  - 关注提升度>1的规则\n")


def demo_real_world():
    """真实案例分析：零售数据"""
    print("=" * 60)
    print("6. 真实案例：零售购物篮分析")
    print("=" * 60)

    if not HAS_MLEXTEND:
        print("请安装mlxtend: pip install mlxtend\n")
        return

    # 模拟零售数据
    products = ['牛奶', '面包', '鸡蛋', '黄油', '奶酪',
                '苹果', '香蕉', '橙汁', '咖啡', '茶叶',
                '饼干', '薯片', '可乐', '矿泉水', '酸奶']

    np.random.seed(42)

    # 创建一些有意义的购买模式
    transactions = []

    # 早餐组合
    for _ in range(30):
        t = ['牛奶', '面包']
        if np.random.random() < 0.7:
            t.append('鸡蛋')
        if np.random.random() < 0.5:
            t.append('黄油')
        transactions.append(t)

    # 水果组合
    for _ in range(25):
        t = ['苹果']
        if np.random.random() < 0.6:
            t.append('香蕉')
        if np.random.random() < 0.4:
            t.append('橙汁')
        transactions.append(t)

    # 饮料零食组合
    for _ in range(20):
        t = ['可乐']
        if np.random.random() < 0.7:
            t.append('薯片')
        if np.random.random() < 0.5:
            t.append('饼干')
        transactions.append(t)

    # 随机购物
    for _ in range(25):
        n = np.random.randint(1, 5)
        t = list(np.random.choice(products, n, replace=False))
        transactions.append(t)

    print(f"总交易数: {len(transactions)}")

    # 编码
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    # 挖掘频繁项集
    frequent_itemsets = apriori(df, min_support=0.2, use_colnames=True)

    # 生成规则
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)

    # 筛选有意义的规则
    meaningful_rules = rules[
        (rules['confidence'] >= 0.5) &
        (rules['lift'] >= 1.2)
    ].sort_values('lift', ascending=False)

    print(f"\n发现频繁项集: {len(frequent_itemsets)}个")
    print(f"有意义的关联规则 (置信度>=0.5, 提升度>=1.2): {len(meaningful_rules)}条")
    print("-" * 60)

    # 显示top规则
    for i, (_, row) in enumerate(meaningful_rules.head(10).iterrows(), 1):
        ant = ', '.join(row['antecedents'])
        con = ', '.join(row['consequents'])
        print(f"{i}. [{ant}] → [{con}]")
        print(f"   支持度: {row['support']:.3f}, 置信度: {row['confidence']:.3f}, 提升度: {row['lift']:.3f}")

    print("\n业务建议:")
    print("  - 这些规则可用于商品陈列和促销策略")
    print("  - 将高关联商品放在一起可提高销量")
    print("  - 可设计捆绑销售套餐\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("关联规则学习 (Association Rule Learning) 完整示例")
    print("=" * 60 + "\n")

    # 运行所有示例
    demo_basic_concepts()
    demo_apriori_manual()
    demo_mlxtend_apriori()
    demo_fpgrowth()
    demo_parameter_sensitivity()
    demo_real_world()

    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
