#!/usr/bin/env python

from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas as pd

# 替换为你的Alpha Vantage API密钥
API_KEY = 'IK7GYUGX9DP8RYO9'
symbol_MSFT = 'MSFT'
start_date = '2024-01-01'
end_date = '2025-01-01'

# 创建TimeSeries对象
ts = TimeSeries(key=API_KEY, output_format='pandas')

# 获取股票数据
# symbol: 股票代码，这里是'MSFT'（微软）。
# outputsize: 指定返回数据的规模。full表示返回全部历史数据（约20年）；compact则返回最近100条数据
data, meta_data = ts.get_daily(symbol=symbol_MSFT, outputsize='full')
filtered_data = data[(data.index >= start_date) & (data.index <= end_date)].copy()

# 查看数据
#print(data.describe())
#print(data.head())

filtered_data = filtered_data.assign(
    MA_10 = lambda x: x['4. close'].rolling(window=10).mean(),
    MA_100 = lambda x: x['4. close'].rolling(window=100).mean(),
    Signal = 0
)

filtered_data.loc[filtered_data['MA_10'] > filtered_data['MA_100'], 'Signal'] = 1  # 短期均线上穿长期均线，产生买入信号
filtered_data.loc[filtered_data['MA_10'] < filtered_data['MA_100'], 'Signal'] = -1  # 短期均线下穿长期均线，产生卖出信号

filtered_data['Daily_Return'] = filtered_data['4. close'].pct_change()
filtered_data['Strategy_Return'] = filtered_data['Signal'].shift(1) * filtered_data['Daily_Return']
filtered_data['Cumulative_Return'] = (1 + filtered_data['Strategy_Return']).cumprod()


plt.scatter(filtered_data[filtered_data['Signal'] == 1].index, filtered_data[filtered_data['Signal'] == 1]['MA_10'], marker='^', color='g', label='Buy Signal')
plt.scatter(filtered_data[filtered_data['Signal'] == -1].index, filtered_data[filtered_data['Signal'] == -1]['MA_10'], marker='v', color='r', label='Sell Signal')

plt.figure(figsize=(10, 6))
# 绘制股价和移动平均线
# - '1. open': 开盘价
# - '2. high': 最高价
# - '3. low': 最低价
# - '4. close': 收盘价
# - '5. volume': 成交量
# plt.plot(filtered_data['4. close'], label='Close Price')
# plt.plot(filtered_data['MA_10'], label='10-day Moving Average')
# plt.plot(filtered_data['MA_100'], label='100-day Moving Average')

# 绘制价格走势
# filtered_data['4. close'].plot()
# plt.title('Microsoft Stock Price')
# plt.xlabel("Date")
# plt.ylabel("Price")
# plt.legend()
# plt.show()

plt.plot(filtered_data['Cumulative_Return'], label='Strategy Cumulative Return', color='b')
plt.plot(filtered_data['4. close'] / filtered_data['4. close'].iloc[0], label='Stock Cumulative Return', color='g')
plt.title("Cumulative Return of Strategy vs. Stock")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.show()