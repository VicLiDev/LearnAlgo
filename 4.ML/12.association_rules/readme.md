# 关联规则学习 (Association Rule Learning)

## 1. 算法简介

关联规则学习是一种数据挖掘技术，用于发现数据集中项之间的有趣关系。最著名的应用是"购物篮分析"——发现顾客购买商品之间的关联。

### 核心概念

**关联规则形式**: {A} → {B}
- 表示：购买A的顾客很可能也会购买B
- 例如：{面包} → {牛奶}，置信度85%

## 2. 基本概念

### 2.1 术语定义

| 术语 | 英文 | 定义 |
|------|------|------|
| 项集 | Itemset | 项的集合，如{面包, 牛奶} |
| k-项集 | k-itemset | 包含k个项的项集 |
| 支持度 | Support | 项集出现的频率 |
| 置信度 | Confidence | 规则的可信程度 |
| 提升度 | Lift | 规则的有效性 |

### 2.2 评估指标

**支持度 (Support)**
```
Support(X) = Count(X) / N
Support(X → Y) = Count(X ∪ Y) / N
```
- 衡量项集在所有交易中出现的频率
- 用于筛选频繁项集

**置信度 (Confidence)**
```
Confidence(X → Y) = Support(X ∪ Y) / Support(X)
```
- 衡量规则的可信程度
- 表示在X发生的条件下Y发生的概率

**提升度 (Lift)**
```
Lift(X → Y) = Confidence(X → Y) / Support(Y)
              = Support(X ∪ Y) / (Support(X) × Support(Y))
```
- Lift > 1: X和Y正相关
- Lift = 1: X和Y独立
- Lift < 1: X和Y负相关

** convictions**
```
Conviction(X → Y) = (1 - Support(Y)) / (1 - Confidence(X → Y))
```
- 衡量规则的依赖程度

## 3. Apriori算法

### 3.1 算法原理

Apriori算法基于**先验性质**：频繁项集的所有非空子集也必须是频繁的。

**算法步骤**：
1. 扫描数据库，找出所有1-项集的频繁项集L1
2. 用L1生成候选2-项集C2
3. 扫描数据库，计算C2的支持度，找出L2
4. 重复直到无法生成更多频繁项集
5. 从频繁项集生成关联规则

### 3.2 伪代码

```
输入: 数据库D, 最小支持度min_sup
输出: 所有频繁项集L

L1 = {频繁1-项集}
for k = 2; L_{k-1} ≠ ∅; k++:
    C_k = apriori_gen(L_{k-1})  // 生成候选
    for each transaction t in D:
        C_t = subset(C_k, t)    // t的子集
        for each candidate c in C_t:
            c.count++
    L_k = {c in C_k | c.count >= min_sup}
return ∪_k L_k
```

### 3.3 生成候选

```
apriori_gen(L_{k-1}):
    // 连接步
    insert into C_k
    select p.item1, p.item2, ..., p.item_{k-1}, q.item_{k-1}
    from L_{k-1} p, L_{k-1} q
    where p.item1=q.item1, ..., p.item_{k-2}=q.item_{k-2}, p.item_{k-1}<q.item_{k-1}

    // 剪枝步
    delete all itemsets c in C_k
    where some (k-1)-subset of c is not in L_{k-1}
```

### 3.4 优缺点

**优点**：
- 原理简单，易于理解
- 使用先验性质有效剪枝

**缺点**：
- 需要多次扫描数据库
- 候选集可能很大
- 对长模式效率低

## 4. FP-Growth算法

### 4.1 算法原理

FP-Growth (Frequent Pattern Growth) 不生成候选集，直接构建FP树进行挖掘。

### 4.2 FP树结构

```
          null
         /  |  \
        f:4 c:4 a:3
       / |   |
     c:3 b:2 b:2
     /|   |
    b:3  ...
```

- 树中每个节点包含：项名、计数、父节点指针、兄弟节点指针
- 相同项通过链表连接

### 4.3 算法步骤

1. **第一次扫描**：计算所有1-项集的支持度，按支持度降序排列
2. **构建FP树**：第二次扫描，将每条交易按顺序插入树中
3. **挖掘频繁项集**：从最低支持度的项开始，构建条件FP树

### 4.4 优缺点

**优点**：
- 只需扫描数据库两次
- 不生成候选集
- 对长模式效率高

**缺点**：
- FP树可能很大
- 递归构建条件树
- 实现较复杂

## 5. ECLAT算法

### 5.1 算法原理

ECLAT (Equivalence Class Clustering and bottom-up Lattice Traversal) 使用**垂直数据格式**。

**水平格式**：{TID: items}
```
T1: {A, B, C}
T2: {A, C}
T3: {B, C}
```

**垂直格式**：{item: TIDs}
```
A: {T1, T2}
B: {T1, T3}
C: {T1, T2, T3}
```

### 5.2 支持度计算

两个项集的交集的TID数量即为联合项集的支持度：
```
Support(X ∪ Y) = |TID(X) ∩ TID(Y)|
```

### 5.3 优缺点

**优点**：
- 支持度计算只需集合交集
- 适合内存存储的情况
- 可并行化

**缺点**：
- TID列表可能很长
- 内存消耗大

## 6. 算法对比

| 特性 | Apriori | FP-Growth | ECLAT |
|------|---------|-----------|-------|
| 扫描次数 | 多次 | 2次 | 多次 |
| 候选集 | 生成 | 不生成 | 不生成 |
| 数据结构 | 候选集 | FP树 | 垂直格式 |
| 内存消耗 | 低 | 中 | 高 |
| 长模式 | 慢 | 快 | 中 |

## 7. 规则生成

从频繁项集生成关联规则：

```
对于每个频繁项集L:
    对于L的每个非空子集S:
        如果 support(L) / support(S) >= min_conf:
            输出规则: S → (L-S)
```

## 8. Python实现

### 使用mlxtend库

```python
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd

# 交易数据
transactions = [
    ['牛奶', '面包', '尿布'],
    ['面包', '尿布', '啤酒', '鸡蛋'],
    ['牛奶', '尿布', '啤酒', '可乐'],
    ['面包', '牛奶', '尿布', '啤酒'],
    ['面包', '牛奶', '可乐']
]

# 编码
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df = pd.DataFrame(te_ary, columns=te.columns_)

# Apriori算法
frequent_itemsets = apriori(df, min_support=0.4, use_colnames=True)

# 生成关联规则
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
```

## 9. 参数选择指南

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| min_support | 最小支持度 | 0.01-0.1 |
| min_confidence | 最小置信度 | 0.5-0.8 |
| min_lift | 最小提升度 | >1.0 |

**注意**：
- 支持度太低会产生大量规则
- 置信度高不代表规则有意义（需看提升度）
- 提升度>1才表示有正相关性

## 10. 应用场景

- **零售**：购物篮分析、商品推荐
- **电商**：交叉销售、捆绑销售
- **医疗**：疾病症状关联、药物相互作用
- **Web挖掘**：网页浏览模式、点击流分析
- **生物信息**：基因序列分析

## 11. 示例代码

见 `demo.py` 文件，包含：
- Apriori算法实现
- FP-Growth算法
- 规则评估指标计算
- 实际案例分析

## 12. 参考资料

- Agrawal, R., & Srikant, R. (1994). Fast algorithms for mining association rules
- Han, J., et al. (2000). Mining frequent patterns without candidate generation
- mlxtend文档: http://rasbt.github.io/mlxtend/
