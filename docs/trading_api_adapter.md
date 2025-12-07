# Trading API Adapter / 交易API适配器

## Overview / 概述

TradingAPIAdapter provides a unified interface for connecting to broker trading APIs. It abstracts the complexity of different broker APIs and provides a consistent interface for placing orders, querying account information, and managing positions.

TradingAPIAdapter 提供了连接券商交易API的统一接口。它抽象了不同券商API的复杂性，为下单、查询账户信息和管理持仓提供了一致的接口。

## Features / 功能特性

- **Broker Connection / 券商连接**: Connect to different broker APIs with unified credentials
- **Order Placement / 订单下单**: Place market and limit orders
- **Order Cancellation / 订单撤销**: Cancel pending orders
- **Account Query / 账户查询**: Query account balance and information
- **Position Query / 持仓查询**: Query current positions
- **Order Status / 订单状态**: Query order execution status
- **Mock Mode / 模拟模式**: Built-in mock broker for testing

## Architecture / 架构

```
TradingAPIAdapter
├── Connection Management / 连接管理
│   ├── connect() - Connect to broker / 连接券商
│   ├── disconnect() - Disconnect from broker / 断开连接
│   └── is_connected() - Check connection status / 检查连接状态
├── Order Management / 订单管理
│   ├── place_order() - Place an order / 下单
│   ├── cancel_order() - Cancel an order / 撤单
│   └── get_order_status() - Query order status / 查询订单状态
├── Account Management / 账户管理
│   ├── get_account_info() - Get account information / 获取账户信息
│   └── get_positions() - Get current positions / 获取当前持仓
└── Utility Methods / 工具方法
    ├── get_broker_name() - Get broker name / 获取券商名称
    └── get_account_id() - Get account ID / 获取账户ID
```

## Usage / 使用方法

### Basic Usage / 基本使用

```python
from src.infrastructure import TradingAPIAdapter

# Create adapter
adapter = TradingAPIAdapter()

# Connect to broker
credentials = {
    "account": "your_account",
    "password": "your_password",
    "api_key": "your_api_key"  # If required
}
adapter.connect(broker="mock", credentials=credentials)

# Place an order
result = adapter.place_order(
    symbol="600519",
    quantity=100,
    order_type="market",
    action="buy"
)
print(f"Order placed: {result.order_id}")

# Query account info
account_info = adapter.get_account_info()
print(f"Total value: {account_info.total_value}")
print(f"Cash: {account_info.cash_balance}")

# Query positions
positions = adapter.get_positions()
for pos in positions:
    print(f"{pos.symbol}: {pos.quantity} shares @ {pos.avg_cost}")

# Disconnect
adapter.disconnect()
```

### Market Order / 市价单

```python
# Buy market order
result = adapter.place_order(
    symbol="600519",
    quantity=100,
    order_type="market",
    action="buy"
)

# Sell market order
result = adapter.place_order(
    symbol="600519",
    quantity=50,
    order_type="market",
    action="sell"
)
```

### Limit Order / 限价单

```python
# Buy limit order
result = adapter.place_order(
    symbol="600519",
    quantity=100,
    order_type="limit",
    price=1800.0,
    action="buy"
)

# Sell limit order
result = adapter.place_order(
    symbol="600519",
    quantity=50,
    order_type="limit",
    price=2000.0,
    action="sell"
)
```

### Order Cancellation / 撤单

```python
# Place an order
result = adapter.place_order(
    symbol="600519",
    quantity=100,
    order_type="limit",
    price=1800.0,
    action="buy"
)

# Cancel the order
success = adapter.cancel_order(result.order_id)
if success:
    print("Order cancelled successfully")
```

### Query Order Status / 查询订单状态

```python
# Query order status
order_status = adapter.get_order_status(order_id)
print(f"Status: {order_status.status}")
print(f"Filled: {order_status.filled_quantity}")
print(f"Remaining: {order_status.remaining_quantity}")
print(f"Avg price: {order_status.avg_fill_price}")
```

## Data Models / 数据模型

### AccountInfo

Account information returned by `get_account_info()`.

```python
@dataclass
class AccountInfo:
    account_id: str          # Account identifier / 账户标识符
    broker: str              # Broker name / 券商名称
    total_value: float       # Total account value / 账户总价值
    cash_balance: float      # Available cash / 可用现金
    buying_power: float      # Buying power / 购买力
    positions_value: float   # Total positions value / 持仓总价值
    unrealized_pnl: float    # Unrealized profit/loss / 未实现盈亏
```

### OrderResult

Order placement result returned by `place_order()`.

```python
@dataclass
class OrderResult:
    order_id: str            # Order identifier / 订单标识符
    symbol: str              # Stock symbol / 股票代码
    quantity: float          # Order quantity / 订单数量
    order_type: str          # Order type / 订单类型
    status: str              # Order status / 订单状态
    filled_quantity: float   # Filled quantity / 已成交数量
    avg_fill_price: float    # Average fill price / 平均成交价格
    timestamp: str           # Order timestamp / 订单时间戳
    message: str             # Status message / 状态消息
```

### OrderStatus

Order status returned by `get_order_status()`.

```python
@dataclass
class OrderStatus:
    order_id: str            # Order identifier / 订单标识符
    status: str              # Order status / 订单状态
    filled_quantity: float   # Filled quantity / 已成交数量
    remaining_quantity: float # Remaining quantity / 剩余数量
    avg_fill_price: float    # Average fill price / 平均成交价格
    last_update: str         # Last update time / 最后更新时间
```

### Position

Position information returned by `get_positions()`.

```python
@dataclass
class Position:
    symbol: str              # Stock symbol / 股票代码
    quantity: float          # Number of shares / 持有数量
    avg_cost: float          # Average cost / 平均成本
    current_price: float     # Current price / 当前价格
    market_value: float      # Market value / 市值
    unrealized_pnl: float    # Unrealized P&L / 未实现盈亏
    unrealized_pnl_pct: float # Unrealized P&L % / 未实现盈亏百分比
```

## Mock Broker / 模拟券商

The adapter includes a built-in mock broker for testing purposes. The mock broker:

适配器包含一个内置的模拟券商用于测试。模拟券商：

- Simulates order execution / 模拟订单执行
- Maintains mock positions / 维护模拟持仓
- Tracks cash balance / 跟踪现金余额
- Provides realistic order IDs / 提供真实的订单ID
- Supports all adapter operations / 支持所有适配器操作

```python
# Connect to mock broker
adapter.connect(broker="mock", credentials={"account": "test_account"})
```

## Error Handling / 错误处理

The adapter uses the system's error handling framework and raises `SystemError` with detailed error information:

适配器使用系统的错误处理框架，抛出包含详细错误信息的 `SystemError`：

```python
try:
    adapter.place_order(symbol="600519", quantity=100, order_type="market")
except SystemError as e:
    print(f"Error: {e.error_info.get_user_message()}")
    print(f"Suggestions: {e.error_info.suggested_actions}")
```

## Extending for Real Brokers / 扩展真实券商

To add support for a real broker:

要添加对真实券商的支持：

1. Add broker-specific connection logic in `connect()`
2. Implement broker API calls in each method
3. Handle broker-specific error codes
4. Map broker data structures to our data models

Example:

```python
def connect(self, broker: str, credentials: Dict[str, Any]) -> None:
    if broker == "huatai":
        self._connect_huatai(credentials)
    elif broker == "citic":
        self._connect_citic(credentials)
    # ... other brokers
```

## Best Practices / 最佳实践

1. **Always check connection status** / 始终检查连接状态
   ```python
   if not adapter.is_connected():
       adapter.connect(broker, credentials)
   ```

2. **Handle errors gracefully** / 优雅地处理错误
   ```python
   try:
       result = adapter.place_order(...)
   except SystemError as e:
       logger.error(f"Order failed: {e}")
   ```

3. **Disconnect when done** / 完成后断开连接
   ```python
   try:
       # ... trading operations
   finally:
       adapter.disconnect()
   ```

4. **Validate order parameters** / 验证订单参数
   ```python
   if quantity <= 0:
       raise ValueError("Quantity must be positive")
   ```

5. **Use mock broker for testing** / 使用模拟券商进行测试
   ```python
   # In tests
   adapter.connect(broker="mock", credentials={"account": "test"})
   ```

## Examples / 示例

See `examples/demo_trading_api_adapter.py` for a complete working example.

查看 `examples/demo_trading_api_adapter.py` 获取完整的工作示例。

## API Reference / API参考

### connect(broker, credentials)

Connect to broker trading API.

**Parameters:**
- `broker` (str): Broker name
- `credentials` (Dict): Authentication credentials

**Raises:**
- `SystemError`: If connection fails

### disconnect()

Disconnect from broker API.

### is_connected()

Check if connected to broker.

**Returns:**
- `bool`: True if connected

### place_order(symbol, quantity, order_type, price, action)

Place an order.

**Parameters:**
- `symbol` (str): Stock symbol
- `quantity` (float): Order quantity
- `order_type` (str): "market" or "limit"
- `price` (Optional[float]): Limit price (required for limit orders)
- `action` (str): "buy" or "sell"

**Returns:**
- `OrderResult`: Order placement result

**Raises:**
- `SystemError`: If order fails

### cancel_order(order_id)

Cancel an order.

**Parameters:**
- `order_id` (str): Order identifier

**Returns:**
- `bool`: True if cancellation successful

**Raises:**
- `SystemError`: If cancellation fails

### get_account_info()

Get account information.

**Returns:**
- `AccountInfo`: Account information

**Raises:**
- `SystemError`: If query fails

### get_positions()

Get current positions.

**Returns:**
- `List[Position]`: List of positions

**Raises:**
- `SystemError`: If query fails

### get_order_status(order_id)

Get order status.

**Parameters:**
- `order_id` (str): Order identifier

**Returns:**
- `OrderStatus`: Order status

**Raises:**
- `SystemError`: If query fails

## See Also / 另请参阅

- [Live Trading Manager](live_trading_manager.md) - Uses TradingAPIAdapter for live trading
- [Simulation Engine](simulation_engine.md) - Simulated trading without real broker
- [Risk Manager](risk_manager.md) - Risk control for trading
