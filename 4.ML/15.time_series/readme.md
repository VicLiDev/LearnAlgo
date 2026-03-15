# 时间序列分析 (Time Series Analysis)

## 1. 简介

时间序列是按时间顺序排列的数据点序列。时间序列分析的目标是理解过去、预测未来。

### 时间序列特点
- **时间依赖性**：当前值与历史值相关
- **趋势**：长期上升或下降
- **季节性**：周期性重复模式
- **周期性**：非固定周期的波动
- **噪声**：随机波动

## 2. 时间序列分解

### 2.1 加法模型
```
Y(t) = Trend(t) + Seasonal(t) + Residual(t)
```

### 2.2 乘法模型
```
Y(t) = Trend(t) × Seasonal(t) × Residual(t)
```

### 2.3 STL分解
Seasonal-Trend decomposition using LOESS

## 3. 平稳性

### 3.1 定义
时间序列是平稳的，如果：
- 均值恒定
- 方差恒定
- 协方差只与时间差有关

### 3.2 平稳性检验

**ADF检验 (Augmented Dickey-Fuller)**
```python
from statsmodels.tsa.stattools import adfuller

result = adfuller(series)
p_value = result[1]
# p < 0.05 拒绝原假设，序列平稳
```

**KPSS检验**
```python
from statsmodels.tsa.stattools import kpss

result = kpss(series)
# p < 0.05 拒绝平稳假设
```

### 3.3 差分
```
Y'(t) = Y(t) - Y(t-1)
```

## 4. ARIMA模型

### 4.1 组成部分

**AR (自回归)**
```
Y(t) = c + φ₁Y(t-1) + φ₂Y(t-2) + ... + φₚY(t-p) + ε(t)
```

**I (差分)**
```
Y'(t) = Y(t) - Y(t-d)
```

**MA (移动平均)**
```
Y(t) = μ + ε(t) + θ₁ε(t-1) + θ₂ε(t-2) + ... + θqε(t-q)
```

### 4.2 ARIMA(p, d, q)

- p：自回归阶数
- d：差分次数
- q：移动平均阶数

### 4.3 参数选择

**自相关函数 (ACF)**：用于确定q
**偏自相关函数 (PACF)**：用于确定p

| 模式  | ACF     | PACF    |
|-------|---------|---------|
| AR(p) | 拖尾    | p阶截尾 |
| MA(q) | q阶截尾 | 拖尾    |
| ARMA  | 拖尾    | 拖尾    |

### 4.4 实现

```python
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(series, order=(1, 1, 1))
fitted = model.fit()
forecast = fitted.forecast(steps=10)
```

## 5. SARIMA

季节性ARIMA：ARIMA(p,d,q)(P,D,Q,s)

- (p,d,q)：非季节性参数
- (P,D,Q)：季节性参数
- s：季节周期（如12表示月度数据）

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX

model = SARIMAX(series, order=(1,1,1), seasonal_order=(1,1,1,12))
fitted = model.fit()
```

## 6. 指数平滑

### 6.1 简单指数平滑
```
Ŷ(t+1) = αY(t) + (1-α)Ŷ(t)
```
适用于无趋势、无季节性的数据

### 6.2 Holt线性趋势
```
Level:   L(t) = αY(t) + (1-α)(L(t-1) + T(t-1))
Trend:   T(t) = β(L(t) - L(t-1)) + (1-β)T(t-1)
Forecast: Ŷ(t+h) = L(t) + h×T(t)
```

### 6.3 Holt-Winters季节性
```
Level:   L(t) = α(Y(t)/S(t-m)) + (1-α)(L(t-1) + T(t-1))
Trend:   T(t) = β(L(t) - L(t-1)) + (1-β)T(t-1)
Seasonal: S(t) = γ(Y(t)/L(t)) + (1-γ)S(t-m)
Forecast: Ŷ(t+h) = (L(t) + h×T(t)) × S(t+h-m)
```

### 6.4 实现

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

model = ExponentialSmoothing(series, trend='add', seasonal='add', seasonal_periods=12)
fitted = model.fit()
forecast = fitted.forecast(steps=12)
```

## 7. Prophet

### 7.1 简介
Facebook开发的时间序列预测工具，适合有趋势和季节性的数据。

### 7.2 模型组成
```
y(t) = g(t) + s(t) + h(t) + ε(t)
```
- g(t)：趋势（分段线性或logistic）
- s(t)：季节性（傅里叶级数）
- h(t)：节假日效应
- ε(t)：误差

### 7.3 实现

```python
from prophet import Prophet

df = pd.DataFrame({'ds': dates, 'y': values})
model = Prophet()
model.fit(df)
future = model.make_future_dataframe(periods=365)
forecast = model.predict(future)
```

## 8. 模型评估

### 8.1 评估指标

| 指标 | 公式               | 说明               |
|------|--------------------|--------------------|
| MAE  | Σ\|y-ŷ\|/n         | 平均绝对误差       |
| RMSE | √MSE               | 均方根误差         |
| MSE  | Σ(y-ŷ)²/n          | 均方误差           |
| MAPE | Σ\|y-ŷ\|/y/n × 100 | 平均绝对百分比误差 |

### 8.2 交叉验证

时间序列交叉验证（滚动窗口）：
```
训练: [1, 2, 3]  测试: [4]
训练: [1, 2, 3, 4]  测试: [5]
训练: [1, 2, 3, 4, 5]  测试: [6]
```

## 9. 方法对比

| 方法     | 优点             | 缺点             |
|----------|------------------|------------------|
| ARIMA    | 经典、可解释     | 需要平稳数据     |
| SARIMA   | 处理季节性       | 参数多           |
| 指数平滑 | 简单、快速       | 复杂模式能力有限 |
| Prophet  | 自动化、处理异常 | 需要安装         |

## 10. 应用场景

- **金融**：股票价格预测、风险评估
- **销售**：销量预测、库存管理
- **能源**：电力负荷预测
- **交通**：客流量预测
- **气象**：天气预报

## 11. 示例代码

见 `demo.py` 文件，包含：
- 时间序列分解
- ARIMA建模
- 指数平滑
- Prophet预测
- 模型评估

## 12. 参考资料

- Box, G. E., et al. (2015). Time Series Analysis: Forecasting and Control
- Hyndman, R. J., & Athanasopoulos, G. Forecasting: Principles and Practice
- Taylor, S. J., & Letham, B. (2018). Forecasting at Scale
- statsmodels文档: https://www.statsmodels.org/
