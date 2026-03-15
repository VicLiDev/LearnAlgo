"""
特征工程 (Feature Engineering) 示例代码

包含内容:
1. 缺失值处理
2. 特征缩放
3. 类别特征编码
4. 特征选择
5. 特征构造
6. 完整流水线
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from t01_mpl import chinese_font
from sklearn.datasets import make_classification, load_breast_cancer, fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import (
    StandardScaler, MinMaxScaler, RobustScaler,
    LabelEncoder, OneHotEncoder, PolynomialFeatures,
    KBinsDiscretizer
)
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.feature_selection import (
    VarianceThreshold, SelectKBest, chi2, f_classif,
    RFE, SelectFromModel
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def demo_missing_values():
    """缺失值处理"""
    print("=" * 60)
    print("1. 缺失值处理")
    print("=" * 60)

    # 创建带缺失值的数据
    np.random.seed(42)
    data = {
        'A': [1, 2, np.nan, 4, 5, np.nan, 7, 8, 9, 10],
        'B': [10, np.nan, 30, 40, np.nan, 60, 70, 80, np.nan, 100],
        'C': ['a', 'b', np.nan, 'a', 'b', 'c', np.nan, 'a', 'b', 'c']
    }
    df = pd.DataFrame(data)

    print("原始数据 (含缺失值):")
    print(df)
    print(f"\n缺失值统计:\n{df.isnull().sum()}")

    # 1. 删除缺失值
    df_drop = df.dropna()
    print(f"\n删除缺失值后: {len(df_drop)}行")

    # 2. 均值填充
    imputer_mean = SimpleImputer(strategy='mean')
    df_mean = df.copy()
    df_mean[['A', 'B']] = imputer_mean.fit_transform(df[['A', 'B']])
    print(f"\n均值填充后 A列均值: {df_mean['A'].mean():.2f}")

    # 3. 中位数填充
    imputer_median = SimpleImputer(strategy='median')
    df_median = df.copy()
    df_median[['A', 'B']] = imputer_median.fit_transform(df[['A', 'B']])

    # 4. KNN填充
    imputer_knn = KNNImputer(n_neighbors=3)
    df_knn = df.copy()
    df_knn[['A', 'B']] = imputer_knn.fit_transform(df[['A', 'B']])

    # 可视化
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    methods = [
        ('原始数据', df),
        ('均值填充', df_mean),
        ('中位数填充', df_median),
        ('KNN填充', df_knn)
    ]

    for ax, (title, d) in zip(axes.flatten(), methods):
        ax.bar(d.index, d['A'], alpha=0.7, label='A列')
        ax.bar(d.index, d['B'], alpha=0.7, label='B列')
        ax.set_xlabel('索引')
        ax.set_ylabel('值')
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('feature_missing_values.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("缺失值处理图已保存为 feature_missing_values.png\n")


def demo_scaling():
    """特征缩放"""
    print("=" * 60)
    print("2. 特征缩放")
    print("=" * 60)

    # 创建不同分布的数据
    np.random.seed(42)
    X1 = np.random.normal(100, 20, 1000)  # 正态分布
    X2 = np.random.exponential(10, 1000)  # 指数分布
    X3 = np.random.uniform(0, 1000, 1000)  # 均匀分布

    X = np.column_stack([X1, X2, X3])
    feature_names = ['正态分布', '指数分布', '均匀分布']

    print("原始数据统计:")
    print(f"  均值: {X.mean(axis=0)}")
    print(f"  标准差: {X.std(axis=0)}")
    print(f"  范围: [{X.min(axis=0)}, {X.max(axis=0)}]")

    # 不同缩放方法
    scalers = {
        'StandardScaler': StandardScaler(),
        'MinMaxScaler': MinMaxScaler(),
        'RobustScaler': RobustScaler()
    }

    # 可视化
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 原始数据
    ax = axes[0, 0]
    ax.boxplot(X, labels=feature_names)
    ax.set_title('原始数据', fontsize=14)
    ax.set_ylabel('值')
    ax.grid(True, alpha=0.3)

    # 不同缩放方法
    for ax, (name, scaler) in zip(axes.flatten()[1:], scalers.items()):
        X_scaled = scaler.fit_transform(X)
        ax.boxplot(X_scaled, labels=feature_names)
        ax.set_title(name, fontsize=14)
        ax.set_ylabel('缩放后值')
        ax.grid(True, alpha=0.3)

        print(f"\n{name}缩放后:")
        print(f"  均值: {X_scaled.mean(axis=0).round(3)}")
        print(f"  标准差: {X_scaled.std(axis=0).round(3)}")

    plt.tight_layout()
    plt.savefig('feature_scaling.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("特征缩放图已保存为 feature_scaling.png\n")


def demo_encoding():
    """类别特征编码"""
    print("=" * 60)
    print("3. 类别特征编码")
    print("=" * 60)

    # 创建类别数据
    data = pd.DataFrame({
        '城市': ['北京', '上海', '广州', '深圳', '北京', '上海', '广州', '深圳'],
        '颜色': ['红', '蓝', '绿', '红', '蓝', '绿', '红', '蓝'],
        '等级': ['高', '中', '低', '高', '中', '低', '高', '中'],
        '目标': [1, 0, 1, 1, 0, 0, 1, 0]
    })

    print("原始数据:")
    print(data)

    # 1. 标签编码
    le = LabelEncoder()
    data_label = data.copy()
    for col in ['城市', '颜色', '等级']:
        data_label[col + '_encoded'] = le.fit_transform(data[col])

    print("\n标签编码结果:")
    print(data_label[['城市', '城市_encoded', '等级', '等级_encoded']])

    # 2. 独热编码
    ohe = OneHotEncoder(sparse_output=False, drop='first')
    city_encoded = ohe.fit_transform(data[['城市']])
    print(f"\n独热编码 (城市):")
    print(pd.DataFrame(city_encoded, columns=['上海', '广州', '深圳']).head())

    # 3. 目标编码
    target_mean = data.groupby('城市')['目标'].mean()
    data['城市_target'] = data['城市'].map(target_mean)
    print(f"\n目标编码 (城市):")
    print(data[['城市', '目标', '城市_target']].drop_duplicates())

    # 可视化
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    # 标签编码
    ax = axes[0]
    encoded = data_label[['城市_encoded', '颜色_encoded', '等级_encoded']]
    ax.imshow(encoded.values.T, cmap='coolwarm', aspect='auto')
    ax.set_yticks(range(3))
    ax.set_yticklabels(['城市', '颜色', '等级'])
    ax.set_title('标签编码', fontsize=12)
    ax.set_xlabel('样本索引')

    # 独热编码矩阵
    ax = axes[1]
    ohe_full = OneHotEncoder(sparse_output=False)
    all_encoded = ohe_full.fit_transform(data[['城市', '颜色']])
    ax.imshow(all_encoded.T, cmap='Blues', aspect='auto')
    ax.set_title('独热编码矩阵', fontsize=12)
    ax.set_xlabel('样本索引')
    ax.set_ylabel('编码维度')

    # 目标编码值
    ax = axes[2]
    cities = data['城市'].unique()
    targets = [data[data['城市']==c]['目标'].mean() for c in cities]
    ax.bar(cities, targets, color='steelblue')
    ax.set_ylabel('目标均值')
    ax.set_title('目标编码值', fontsize=12)
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('feature_encoding.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("编码方式图已保存为 feature_encoding.png\n")


def demo_feature_selection():
    """特征选择"""
    print("=" * 60)
    print("4. 特征选择")
    print("=" * 60)

    # 生成数据
    X, y = make_classification(n_samples=1000, n_features=20, n_informative=5,
                               n_redundant=5, n_repeated=2, random_state=42)

    print(f"原始特征数: {X.shape[1]}")

    # 划分数据
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 1. 方差阈值
    selector = VarianceThreshold(threshold=0.1)
    X_var = selector.fit_transform(X_train)
    print(f"\n方差阈值后特征数: {X_var.shape[1]}")

    # 2. 单变量选择
    selector = SelectKBest(f_classif, k=10)
    X_kbest = selector.fit_transform(X_train, y_train)
    print(f"SelectKBest后特征数: {X_kbest.shape[1]}")

    # 3. RFE
    rfe = RFE(LogisticRegression(max_iter=1000), n_features_to_select=10)
    X_rfe = rfe.fit_transform(X_train, y_train)
    print(f"RFE后特征数: {X_rfe.shape[1]}")

    # 4. 基于模型的特征选择
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    importances = rf.feature_importances_

    # 可视化特征重要性
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 特征重要性
    ax1 = axes[0]
    sorted_idx = np.argsort(importances)[::-1]
    ax1.bar(range(len(importances)), importances[sorted_idx], color='steelblue')
    ax1.set_xlabel('特征排名', fontsize=12)
    ax1.set_ylabel('重要性', fontsize=12)
    ax1.set_title('随机森林特征重要性', fontsize=14)
    ax1.axhline(y=0.05, color='red', linestyle='--', label='阈值=0.05')
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')

    # 不同特征数量的准确率
    ax2 = axes[1]
    n_features_list = [5, 10, 15, 20]
    accuracies = []

    for n in n_features_list:
        selector = SelectKBest(f_classif, k=n)
        X_train_sel = selector.fit_transform(X_train, y_train)
        X_test_sel = selector.transform(X_test)

        clf = LogisticRegression(max_iter=1000, random_state=42)
        clf.fit(X_train_sel, y_train)
        acc = clf.score(X_test_sel, y_test)
        accuracies.append(acc)

    ax2.plot(n_features_list, accuracies, 'bo-', linewidth=2, markersize=10)
    ax2.set_xlabel('特征数量', fontsize=12)
    ax2.set_ylabel('测试集准确率', fontsize=12)
    ax2.set_title('特征数量 vs 模型性能', fontsize=14)
    ax2.grid(True, alpha=0.3)

    for x, y in zip(n_features_list, accuracies):
        ax2.annotate(f'{y:.3f}', (x, y), textcoords="offset points", xytext=(0,10), ha='center')

    plt.tight_layout()
    plt.savefig('feature_selection.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("特征选择图已保存为 feature_selection.png\n")


def demo_feature_construction():
    """特征构造"""
    print("=" * 60)
    print("5. 特征构造")
    print("=" * 60)

    # 创建示例数据
    np.random.seed(42)
    n = 100

    df = pd.DataFrame({
        'x1': np.random.randn(n),
        'x2': np.random.randn(n),
        'price': np.random.uniform(10, 1000, n),
        'quantity': np.random.randint(1, 100, n),
        'date': pd.date_range('2020-01-01', periods=n, freq='D')
    })

    print("原始数据:")
    print(df.head())

    # 1. 多项式特征
    poly = PolynomialFeatures(degree=2, include_bias=False)
    X_poly = poly.fit_transform(df[['x1', 'x2']])
    print(f"\n多项式特征 (x1, x2): {X_poly.shape[1]}个特征")
    print(f"特征名: {poly.get_feature_names_out(['x1', 'x2'])}")

    # 2. 交互特征
    df['total'] = df['price'] * df['quantity']
    df['price_per_unit'] = df['price'] / df['quantity']
    print(f"\n交互特征: total = price × quantity")

    # 3. 日期特征
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['dayofweek'] = df['date'].dt.dayofweek
    df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)
    print(f"\n日期特征: year, month, day, dayofweek, is_weekend")

    # 4. 分箱特征
    discretizer = KBinsDiscretizer(n_bins=5, encode='onehot-dense', strategy='quantile')
    price_binned = discretizer.fit_transform(df[['price']])
    print(f"\n价格分箱: {price_binned.shape[1]}个区间")

    # 可视化
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # 多项式特征
    ax1 = axes[0, 0]
    ax1.scatter(df['x1'], X_poly[:, 1], alpha=0.5, label='x1²')
    ax1.scatter(df['x1'], X_poly[:, 2], alpha=0.5, label='x1*x2')
    ax1.set_xlabel('x1')
    ax1.set_ylabel('特征值')
    ax1.set_title('多项式特征')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 交互特征
    ax2 = axes[0, 1]
    ax2.scatter(df['price'], df['total'], alpha=0.5, c='steelblue')
    ax2.set_xlabel('价格')
    ax2.set_ylabel('总价')
    ax2.set_title('交互特征: 总价 = 价格 × 数量')
    ax2.grid(True, alpha=0.3)

    # 日期特征
    ax3 = axes[1, 0]
    df['month'].value_counts().sort_index().plot(kind='bar', ax=ax3, color='steelblue')
    ax3.set_xlabel('月份')
    ax3.set_ylabel('频数')
    ax3.set_title('日期特征分布')
    ax3.grid(True, alpha=0.3, axis='y')

    # 分箱特征
    ax4 = axes[1, 1]
    ax4.hist(df['price'], bins=20, alpha=0.7, label='原始价格')
    ax4.set_xlabel('价格')
    ax4.set_ylabel('频数')
    ax4.set_title('价格分布')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('feature_construction.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("特征构造图已保存为 feature_construction.png\n")


def demo_pipeline():
    """完整特征工程流水线"""
    print("=" * 60)
    print("6. 完整特征工程流水线")
    print("=" * 60)

    # 创建示例数据
    np.random.seed(42)
    n = 500

    df = pd.DataFrame({
        'age': np.random.randint(18, 80, n),
        'income': np.random.exponential(50000, n),
        'education': np.random.choice(['高中', '本科', '硕士', '博士'], n),
        'city': np.random.choice(['北京', '上海', '广州', '深圳', '其他'], n),
        'gender': np.random.choice(['M', 'F'], n),
        'target': np.random.randint(0, 2, n)
    })

    # 添加一些缺失值
    df.loc[np.random.choice(n, 20, replace=False), 'income'] = np.nan
    df.loc[np.random.choice(n, 15, replace=False), 'education'] = np.nan

    print("数据概览:")
    print(df.head())
    print(f"\n缺失值:\n{df.isnull().sum()}")

    # 划分数据
    X = df.drop('target', axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 定义特征处理
    numeric_features = ['age', 'income']
    categorical_features = ['education', 'city', 'gender']

    numeric_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer([
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

    # 构建完整流水线
    clf = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(max_iter=1000, random_state=42))
    ])

    # 训练和评估
    clf.fit(X_train, y_train)
    accuracy = clf.score(X_test, y_test)

    print(f"\n流水线处理后的测试准确率: {accuracy:.4f}")

    # 可视化流水线
    fig, ax = plt.subplots(figsize=(12, 6))

    steps = ['原始数据', '缺失值处理', '特征缩放/编码', '特征合并', '模型训练', '预测']
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']

    for i, (step, color) in enumerate(zip(steps, colors)):
        ax.barh(0, 1, left=i, color=color, edgecolor='black', height=0.5)
        ax.text(i + 0.5, 0, step, ha='center', va='center', fontsize=10, fontweight='bold')

    ax.set_xlim(0, len(steps))
    ax.set_ylim(-0.5, 0.5)
    ax.axis('off')
    ax.set_title('特征工程流水线', fontsize=14)

    plt.tight_layout()
    plt.savefig('feature_pipeline.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("流水线图已保存为 feature_pipeline.png\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("特征工程 (Feature Engineering) 完整示例")
    print("=" * 60 + "\n")

    # 运行所有示例
    demo_missing_values()
    demo_scaling()
    demo_encoding()
    demo_feature_selection()
    demo_feature_construction()
    demo_pipeline()

    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
