"""
时间序列分析 (Time Series Analysis) 示例代码

包含内容:
1. 时间序列生成与可视化
2. 时间序列分解
3. 平稳性检验
4. ARIMA模型
5. 指数平滑
6. Prophet预测
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 检查statsmodels
try:
    from statsmodels.tsa.seasonal import seasonal_decompose
    from statsmodels.tsa.stattools import adfuller, acf, pacf
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False
    print("警告: 未安装statsmodels，部分示例将跳过")
    print("安装: pip install statsmodels")

# 检查Prophet
try:
    from prophet import Prophet
    HAS_PROPHET = True
except ImportError:
    HAS_PROPHET = False


def generate_time_series():
    """生成示例时间序列数据"""
    np.random.seed(42)

    # 生成日期范围
    dates = pd.date_range(start='2020-01-01', periods=365*2, freq='D')

    # 趋势组件
    trend = np.linspace(100, 150, len(dates))

    # 季节性组件（年度周期）
    seasonality = 20 * np.sin(2 * np.pi * np.arange(len(dates)) / 365)

    # 周周期性
    weekly = 5 * np.sin(2 * np.pi * np.arange(len(dates)) / 7)

    # 噪声
    noise = np.random.normal(0, 5, len(dates))

    # 组合
    values = trend + seasonality + weekly + noise

    return pd.DataFrame({'date': dates, 'value': values})


def demo_basic_visualization():
    """基础可视化"""
    print("=" * 60)
    print("1. 时间序列基础可视化")
    print("=" * 60)

    df = generate_time_series()
    df.set_index('date', inplace=True)

    print(f"数据范围: {df.index.min()} 到 {df.index.max()}")
    print(f"数据点数: {len(df)}")
    print(f"统计摘要:")
    print(df.describe())

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 原始序列
    ax1 = axes[0, 0]
    ax1.plot(df.index, df['value'], color='steelblue', linewidth=0.8)
    ax1.set_xlabel('日期', fontsize=11)
    ax1.set_ylabel('值', fontsize=11)
    ax1.set_title('原始时间序列', fontsize=12)
    ax1.grid(True, alpha=0.3)

    # 月度聚合
    ax2 = axes[0, 1]
    monthly = df.resample('M').mean()
    ax2.plot(monthly.index, monthly['value'], color='steelblue', marker='o', markersize=4)
    ax2.set_xlabel('日期', fontsize=11)
    ax2.set_ylabel('值', fontsize=11)
    ax2.set_title('月度平均值', fontsize=12)
    ax2.grid(True, alpha=0.3)

    # 滚动统计
    ax3 = axes[1, 0]
    rolling_mean = df['value'].rolling(window=30).mean()
    rolling_std = df['value'].rolling(window=30).std()
    ax3.plot(df.index, df['value'], alpha=0.3, label='原始数据')
    ax3.plot(df.index, rolling_mean, color='red', label='30天移动平均')
    ax3.fill_between(df.index, rolling_mean - rolling_std, rolling_mean + rolling_std,
                    color='red', alpha=0.2, label='±1标准差')
    ax3.set_xlabel('日期', fontsize=11)
    ax3.set_ylabel('值', fontsize=11)
    ax3.set_title('滚动统计 (窗口=30天)', fontsize=12)
    ax3.legend(loc='upper left')
    ax3.grid(True, alpha=0.3)

    # 分布
    ax4 = axes[1, 1]
    ax4.hist(df['value'], bins=50, edgecolor='black', alpha=0.7, color='steelblue')
    ax4.axvline(df['value'].mean(), color='red', linestyle='--', label=f'均值={df["value"].mean():.1f}')
    ax4.set_xlabel('值', fontsize=11)
    ax4.set_ylabel('频数', fontsize=11)
    ax4.set_title('值分布', fontsize=12)
    ax4.legend(loc='upper right')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('timeseries_basic.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("基础可视化图已保存为 timeseries_basic.png\n")


def demo_decomposition():
    """时间序列分解"""
    print("=" * 60)
    print("2. 时间序列分解")
    print("=" * 60)

    if not HAS_STATSMODELS:
        print("请安装statsmodels\n")
        return

    df = generate_time_series()
    df.set_index('date', inplace=True)

    # 季节性分解
    decomposition = seasonal_decompose(df['value'], model='additive', period=365)

    fig, axes = plt.subplots(4, 1, figsize=(14, 12))

    # 原始
    axes[0].plot(df.index, df['value'], color='steelblue')
    axes[0].set_ylabel('原始', fontsize=11)
    axes[0].set_title('时间序列分解 (加法模型)', fontsize=14)
    axes[0].grid(True, alpha=0.3)

    # 趋势
    axes[1].plot(df.index, decomposition.trend, color='red')
    axes[1].set_ylabel('趋势', fontsize=11)
    axes[1].grid(True, alpha=0.3)

    # 季节性
    axes[2].plot(df.index, decomposition.seasonal, color='green')
    axes[2].set_ylabel('季节性', fontsize=11)
    axes[2].grid(True, alpha=0.3)

    # 残差
    axes[3].plot(df.index, decomposition.resid, color='purple')
    axes[3].set_ylabel('残差', fontsize=11)
    axes[3].set_xlabel('日期', fontsize=11)
    axes[3].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('timeseries_decomposition.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("分解图已保存为 timeseries_decomposition.png\n")

    print("分解结果解读:")
    print("  - 趋势: 长期上升/下降模式")
    print("  - 季节性: 周期性重复的波动")
    print("  - 残差: 除去趋势和季节性后的随机波动\n")


def demo_stationarity():
    """平稳性检验"""
    print("=" * 60)
    print("3. 平稳性检验")
    print("=" * 60)

    if not HAS_STATSMODELS:
        print("请安装statsmodels\n")
        return

    df = generate_time_series()
    series = df['value']

    # ADF检验
    print("ADF检验 (Augmented Dickey-Fuller Test)")
    print("-" * 40)
    result = adfuller(series.dropna())
    print(f"ADF统计量: {result[0]:.4f}")
    print(f"p值: {result[1]:.4f}")
    print(f"临界值:")
    for key, value in result[4].items():
        print(f"  {key}: {value:.4f}")

    if result[1] < 0.05:
        print("结论: p < 0.05, 拒绝原假设，序列可能是平稳的")
    else:
        print("结论: p >= 0.05, 不能拒绝原假设，序列可能非平稳")

    # 差分
    series_diff = series.diff().dropna()

    print(f"\n一阶差分后的ADF检验:")
    print("-" * 40)
    result_diff = adfuller(series_diff)
    print(f"ADF统计量: {result_diff[0]:.4f}")
    print(f"p值: {result_diff[1]:.4f}")

    if result_diff[1] < 0.05:
        print("结论: 差分后序列平稳")

    # 可视化
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 原始序列
    ax1 = axes[0]
    ax1.plot(series, color='steelblue')
    ax1.set_xlabel('时间', fontsize=11)
    ax1.set_ylabel('值', fontsize=11)
    ax1.set_title('原始序列', fontsize=12)
    ax1.grid(True, alpha=0.3)

    # 差分后序列
    ax2 = axes[1]
    ax2.plot(series_diff, color='steelblue')
    ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax2.set_xlabel('时间', fontsize=11)
    ax2.set_ylabel('差分值', fontsize=11)
    ax2.set_title('一阶差分序列', fontsize=12)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('timeseries_stationarity.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("平稳性检验图已保存为 timeseries_stationarity.png\n")


def demo_arima():
    """ARIMA模型"""
    print("=" * 60)
    print("4. ARIMA模型")
    print("=" * 60)

    if not HAS_STATSMODELS:
        print("请安装statsmodels\n")
        return

    df = generate_time_series()

    # 划分训练集和测试集
    train_size = int(len(df) * 0.8)
    train = df['value'][:train_size]
    test = df['value'][train_size:]

    print(f"训练集大小: {len(train)}")
    print(f"测试集大小: {len(test)}")

    # ACF和PACF图
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # ACF
    plot_acf(train.diff().dropna(), ax=axes[0], lags=40)
    axes[0].set_title('自相关函数 (ACF)', fontsize=12)
    axes[0].set_xlabel('滞后期', fontsize=11)

    # PACF
    plot_pacf(train.diff().dropna(), ax=axes[1], lags=40)
    axes[1].set_title('偏自相关函数 (PACF)', fontsize=12)
    axes[1].set_xlabel('滞后期', fontsize=11)

    plt.tight_layout()
    plt.savefig('timeseries_acf_pacf.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("ACF/PACF图已保存为 timeseries_acf_pacf.png\n")

    # 拟合ARIMA模型
    print("拟合ARIMA(1,1,1)模型...")
    model = ARIMA(train, order=(1, 1, 1))
    fitted = model.fit()

    print(f"\n模型摘要:")
    print(f"AIC: {fitted.aic:.2f}")
    print(f"BIC: {fitted.bic:.2f}")

    # 预测
    forecast_steps = len(test)
    forecast = fitted.forecast(steps=forecast_steps)
    forecast.index = test.index

    # 评估
    mae = np.mean(np.abs(test - forecast))
    rmse = np.sqrt(np.mean((test - forecast) ** 2))
    mape = np.mean(np.abs((test - forecast) / test)) * 100

    print(f"\n预测评估:")
    print(f"MAE: {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAPE: {mape:.2f}%")

    # 可视化预测
    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(train.index, train, label='训练数据', color='steelblue')
    ax.plot(test.index, test, label='测试数据', color='green')
    ax.plot(forecast.index, forecast, label='ARIMA预测', color='red', linestyle='--')

    ax.set_xlabel('日期', fontsize=12)
    ax.set_ylabel('值', fontsize=12)
    ax.set_title(f'ARIMA(1,1,1)预测 (MAE={mae:.2f}, RMSE={rmse:.2f})', fontsize=14)
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('timeseries_arima.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("ARIMA预测图已保存为 timeseries_arima.png\n")


def demo_exponential_smoothing():
    """指数平滑"""
    print("=" * 60)
    print("5. 指数平滑")
    print("=" * 60)

    if not HAS_STATSMODELS:
        print("请安装statsmodels\n")
        return

    df = generate_time_series()

    # 划分数据
    train_size = int(len(df) * 0.8)
    train = df['value'][:train_size]
    test = df['value'][train_size:]

    # Holt-Winters方法
    print("拟合Holt-Winters指数平滑模型...")
    model = ExponentialSmoothing(
        train,
        trend='add',
        seasonal='add',
        seasonal_periods=365
    )
    fitted = model.fit()

    # 预测
    forecast_steps = len(test)
    forecast = fitted.forecast(forecast_steps)
    forecast.index = test.index

    # 评估
    mae = np.mean(np.abs(test - forecast))
    rmse = np.sqrt(np.mean((test - forecast) ** 2))

    print(f"MAE: {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")

    # 可视化
    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(train.index, train, label='训练数据', color='steelblue', alpha=0.7)
    ax.plot(test.index, test, label='测试数据', color='green')
    ax.plot(forecast.index, forecast, label='Holt-Winters预测', color='red', linestyle='--')

    ax.set_xlabel('日期', fontsize=12)
    ax.set_ylabel('值', fontsize=12)
    ax.set_title(f'Holt-Winters指数平滑预测 (MAE={mae:.2f})', fontsize=14)
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('timeseries_exp_smoothing.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("指数平滑预测图已保存为 timeseries_exp_smoothing.png\n")


def demo_simple_forecast():
    """简单预测方法对比"""
    print("=" * 60)
    print("6. 预测方法对比")
    print("=" * 60)

    df = generate_time_series()

    # 划分数据
    train_size = int(len(df) * 0.8)
    train = df['value'][:train_size]
    test = df['value'][train_size:]

    forecasts = {}

    # 1. 朴素预测（上一个值）
    forecasts['朴素预测'] = np.full(len(test), train.iloc[-1])

    # 2. 移动平均
    forecasts['移动平均(30)'] = np.full(len(test), train.rolling(30).mean().iloc[-1])

    # 3. 季节性朴素预测（去年同期）
    if len(test) <= 365 and len(train) >= 365:
        forecasts['季节性朴素'] = train.iloc[-365:-365+len(test)].values

    # 4. 线性趋势
    from sklearn.linear_model import LinearRegression
    X_train = np.arange(len(train)).reshape(-1, 1)
    lr = LinearRegression()
    lr.fit(X_train, train)
    X_test = np.arange(len(train), len(train) + len(test)).reshape(-1, 1)
    forecasts['线性趋势'] = lr.predict(X_test)

    # 评估
    print(f"{'方法':<15} {'MAE':<10} {'RMSE':<10}")
    print("-" * 35)

    results = {}
    for name, pred in forecasts.items():
        mae = np.mean(np.abs(test - pred))
        rmse = np.sqrt(np.mean((test - pred) ** 2))
        results[name] = {'mae': mae, 'rmse': rmse, 'pred': pred}
        print(f"{name:<15} {mae:<10.4f} {rmse:<10.4f}")

    # 可视化
    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(test.index, test, label='真实值', color='black', linewidth=2)
    colors = ['red', 'blue', 'green', 'orange']
    for (name, res), color in zip(results.items(), colors):
        ax.plot(test.index, res['pred'], label=f"{name}", linestyle='--', alpha=0.7)

    ax.set_xlabel('日期', fontsize=12)
    ax.set_ylabel('值', fontsize=12)
    ax.set_title('预测方法对比', fontsize=14)
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('timeseries_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("预测对比图已保存为 timeseries_comparison.png\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("时间序列分析 (Time Series Analysis) 完整示例")
    print("=" * 60 + "\n")

    # 运行所有示例
    demo_basic_visualization()
    demo_decomposition()
    demo_stationarity()
    demo_arima()
    demo_exponential_smoothing()
    demo_simple_forecast()

    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
