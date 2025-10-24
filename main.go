import qlib

data = qlib.data.features(
    instruments="SH000300",  # 标的代码
    fields=["$close"],  # 要获取的字段（如收盘价、开盘价）
    start_time="2025-01-01",
    end_time="2025-06-30"
)

stock_price = data['SH000300']

print(stock_price['2025-01-01','2025-06-30'])