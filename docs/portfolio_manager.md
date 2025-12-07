# Portfolio Manager Documentation
# 投资组合管理器文档

## Overview / 概述

The Portfolio Manager is a core component of the qlib trading system that handles portfolio creation, position management, trade execution tracking, and portfolio value calculations.

投资组合管理器是qlib交易系统的核心组件，负责处理投资组合创建、持仓管理、交易执行跟踪和组合价值计算。

## Features / 功能特性

### 1. Portfolio Creation / 投资组合创建
- Create portfolios with initial capital / 使用初始资金创建投资组合
- Support multiple portfolios simultaneously / 同时支持多个投资组合
- Auto-generate or custom portfolio IDs / 自动生成或自定义投资组合ID

### 2. Position Management / 持仓管理
- Buy and sell stocks / 买入和卖出股票
- Track position quantities and average costs / 跟踪持仓数量和平均成本
- Calculate unrealized P&L / 计算未实现盈亏
- Update current market prices / 更新当前市场价格

### 3. Trade History / 交易历史
- Record all buy/sell transactions / 记录所有买卖交易
- Track trade prices and commissions / 跟踪交易价格和佣金
- Maintain complete audit trail / 维护完整的审计跟踪

### 4. Portfolio Valuation / 组合估值
- Calculate total portfolio value / 计算投资组合总价值
- Track cash balance / 跟踪现金余额
- Compute position weights / 计算持仓权重
- Calculate returns over time / 计算一段时间内的收益率

## Usage / 使用方法

### Basic Example / 基本示例

```python
from src.core.portfolio_manager import PortfolioManager
from src.infrastructure.logger_system import LoggerSystem

# Initialize
logger_system = LoggerSystem()
logger_system.setup(log_dir="logs", log_level="INFO")
manager = PortfolioManager(logger=logger_system)

# Create portfolio
portfolio = manager.create_portfolio(initial_capital=100000.0)

# Buy stocks
manager.update_position(
    portfolio.portfolio_id,
    symbol="600519",
    quantity=100,
    price=180.0,
    action="buy",
    commission=5.0
)

# Update prices
manager.update_prices(portfolio.portfolio_id, {"600519": 185.0})

# Get current value
current_value = manager.get_current_value(portfolio.portfolio_id)

# View positions
positions = manager.get_positions(portfolio.portfolio_id)

# View trade history
trades = manager.get_trade_history(portfolio.portfolio_id)

# Get summary
summary = manager.get_portfolio_summary(portfolio.portfolio_id)
```

## API Reference / API参考

### PortfolioManager Class

#### `__init__(logger: Optional[LoggerSystem] = None)`
Initialize the portfolio manager.
初始化投资组合管理器。

**Parameters:**
- `logger`: Optional logger system instance / 可选的日志系统实例

#### `create_portfolio(initial_capital: float, portfolio_id: Optional[str] = None) -> Portfolio`
Create a new portfolio with initial capital.
创建具有初始资金的新投资组合。

**Parameters:**
- `initial_capital`: Initial capital amount (must be positive) / 初始资金金额（必须为正数）
- `portfolio_id`: Optional custom portfolio ID / 可选的自定义组合ID

**Returns:**
- Created portfolio object / 创建的投资组合对象

**Raises:**
- `ValueError`: If initial_capital is not positive / 如果初始资金不是正数

#### `update_position(portfolio_id: str, symbol: str, quantity: float, price: float, action: str = "buy", commission: float = 0.0) -> None`
Update position by executing a trade.
通过执行交易更新持仓。

**Parameters:**
- `portfolio_id`: Portfolio identifier / 投资组合标识符
- `symbol`: Stock symbol / 股票代码
- `quantity`: Number of shares to trade / 交易股数
- `price`: Trade price per share / 每股交易价格
- `action`: Trade action ("buy" or "sell") / 交易动作（"buy"或"sell"）
- `commission`: Trading commission / 交易佣金

**Raises:**
- `ValueError`: If portfolio not found, insufficient cash/shares, or invalid parameters / 如果未找到投资组合、现金/股份不足或参数无效

#### `update_prices(portfolio_id: str, prices: Dict[str, float]) -> None`
Update current prices for positions.
更新持仓的当前价格。

**Parameters:**
- `portfolio_id`: Portfolio identifier / 投资组合标识符
- `prices`: Dictionary mapping symbols to current prices / 股票代码到当前价格的字典

#### `get_current_value(portfolio_id: str) -> float`
Get current total value of portfolio.
获取投资组合的当前总价值。

**Parameters:**
- `portfolio_id`: Portfolio identifier / 投资组合标识符

**Returns:**
- Current portfolio value / 当前投资组合价值

#### `get_positions(portfolio_id: str) -> Dict[str, Position]`
Get all positions in portfolio.
获取投资组合中的所有持仓。

**Parameters:**
- `portfolio_id`: Portfolio identifier / 投资组合标识符

**Returns:**
- Dictionary of positions keyed by symbol / 按股票代码索引的持仓字典

#### `get_trade_history(portfolio_id: str) -> List[Trade]`
Get trade history for portfolio.
获取投资组合的交易历史。

**Parameters:**
- `portfolio_id`: Portfolio identifier / 投资组合标识符

**Returns:**
- List of trades / 交易列表

#### `calculate_returns(portfolio_id: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.Series`
Calculate returns for portfolio over a period.
计算投资组合在一段时间内的收益率。

**Parameters:**
- `portfolio_id`: Portfolio identifier / 投资组合标识符
- `start_date`: Start date (ISO format), None for all history / 开始日期（ISO格式），None表示所有历史
- `end_date`: End date (ISO format), None for current / 结束日期（ISO格式），None表示当前

**Returns:**
- Series of returns indexed by date / 按日期索引的收益率序列

#### `get_portfolio_summary(portfolio_id: str) -> Dict`
Get summary statistics for portfolio.
获取投资组合的摘要统计信息。

**Parameters:**
- `portfolio_id`: Portfolio identifier / 投资组合标识符

**Returns:**
- Dictionary containing portfolio summary with keys:
  - `portfolio_id`: Portfolio identifier
  - `initial_capital`: Initial capital
  - `current_value`: Current total value
  - `cash`: Cash balance
  - `positions_value`: Total value of positions
  - `num_positions`: Number of positions
  - `total_unrealized_pnl`: Total unrealized profit/loss
  - `total_return_pct`: Total return percentage
  - `num_trades`: Number of trades executed

#### `delete_portfolio(portfolio_id: str) -> bool`
Delete a portfolio and its trade history.
删除投资组合及其交易历史。

**Parameters:**
- `portfolio_id`: Portfolio identifier / 投资组合标识符

**Returns:**
- True if deleted, False if not found / 如果删除则返回True，如果未找到则返回False

## Data Models / 数据模型

### Portfolio
Represents an investment portfolio.
表示一个投资组合。

**Attributes:**
- `portfolio_id`: Unique identifier / 唯一标识符
- `positions`: Dictionary of positions / 持仓字典
- `cash`: Available cash / 可用现金
- `total_value`: Total portfolio value / 投资组合总价值
- `initial_capital`: Initial capital / 初始资金

### Position
Represents a position in a single stock.
表示单只股票的持仓。

**Attributes:**
- `symbol`: Stock symbol / 股票代码
- `quantity`: Number of shares held / 持有数量
- `avg_cost`: Average cost per share / 平均成本
- `current_price`: Current market price / 当前市价
- `market_value`: Current market value / 当前市值
- `unrealized_pnl`: Unrealized profit/loss / 未实现盈亏
- `unrealized_pnl_pct`: Unrealized profit/loss percentage / 未实现盈亏百分比

### Trade
Represents an executed trade.
表示已执行的交易。

**Attributes:**
- `trade_id`: Unique trade identifier / 唯一交易标识符
- `timestamp`: Trade execution time / 交易执行时间
- `symbol`: Stock symbol / 股票代码
- `action`: Trading action ("buy" or "sell") / 交易动作
- `quantity`: Number of shares / 股票数量
- `price`: Execution price / 成交价格
- `commission`: Trading commission / 交易佣金
- `total_cost`: Total cost including commission / 包含佣金的总成本

## Error Handling / 错误处理

The Portfolio Manager raises `ValueError` exceptions in the following cases:
投资组合管理器在以下情况下会引发`ValueError`异常：

1. **Invalid Initial Capital** / 无效的初始资金
   - When creating a portfolio with non-positive initial capital
   - 使用非正数初始资金创建投资组合时

2. **Portfolio Not Found** / 未找到投资组合
   - When operating on a non-existent portfolio
   - 对不存在的投资组合进行操作时

3. **Insufficient Cash** / 现金不足
   - When buying stocks without enough cash
   - 现金不足时买入股票

4. **Insufficient Shares** / 股份不足
   - When selling more shares than owned
   - 卖出超过持有的股份时

5. **No Position Found** / 未找到持仓
   - When selling a stock with no position
   - 卖出没有持仓的股票时

6. **Invalid Parameters** / 无效参数
   - When providing invalid quantity, price, or action
   - 提供无效的数量、价格或动作时

## Best Practices / 最佳实践

1. **Always check portfolio existence** before operations
   在操作前始终检查投资组合是否存在

2. **Update prices regularly** to maintain accurate portfolio valuation
   定期更新价格以保持准确的组合估值

3. **Use commission parameter** to accurately track trading costs
   使用佣金参数准确跟踪交易成本

4. **Monitor cash balance** before executing buy orders
   执行买入订单前监控现金余额

5. **Keep trade history** for audit and analysis purposes
   保留交易历史用于审计和分析

## Examples / 示例

See `examples/demo_portfolio_manager.py` for a complete working example.
查看`examples/demo_portfolio_manager.py`获取完整的工作示例。

## Integration / 集成

The Portfolio Manager integrates with:
投资组合管理器与以下组件集成：

- **Logger System**: For logging all operations / 用于记录所有操作
- **Trading Models**: Uses Position, Trade, and Portfolio data models / 使用Position、Trade和Portfolio数据模型
- **Simulation Engine**: Provides portfolio tracking for simulations / 为模拟提供投资组合跟踪
- **Live Trading Manager**: Manages real trading portfolios / 管理实盘交易组合
- **Risk Manager**: Provides portfolio data for risk analysis / 为风险分析提供组合数据

## Requirements Validation / 需求验证

This implementation satisfies the following requirements from the design document:
此实现满足设计文档中的以下需求：

- **Requirement 19.3**: Portfolio creation and position updates / 投资组合创建和持仓更新
- **Requirement 20.3**: Portfolio value calculation and position tracking / 组合价值计算和持仓跟踪

## Testing / 测试

Comprehensive unit tests are available in `tests/unit/test_portfolio_manager.py`.
完整的单元测试位于`tests/unit/test_portfolio_manager.py`。

Test coverage includes:
测试覆盖包括：
- Portfolio creation and deletion / 投资组合创建和删除
- Buy and sell operations / 买入和卖出操作
- Position tracking and updates / 持仓跟踪和更新
- Price updates and P&L calculation / 价格更新和盈亏计算
- Trade history management / 交易历史管理
- Error handling for edge cases / 边缘情况的错误处理
- Multiple portfolio management / 多投资组合管理

Run tests with:
运行测试：
```bash
pytest tests/unit/test_portfolio_manager.py -v
```
