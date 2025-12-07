# Live Trading Manager Documentation / 实盘交易管理器文档

## Overview / 概述

The Live Trading Manager is responsible for managing live trading sessions, executing orders through broker APIs, monitoring positions in real-time, and integrating risk checks before execution.

实盘交易管理器负责管理实盘交易会话、通过券商API执行订单、实时监控持仓以及在执行前集成风险检查。

## Features / 功能特性

### Core Features / 核心功能

1. **Trading Session Management / 交易会话管理**
   - Start new trading sessions / 启动新交易会话
   - Stop trading sessions / 停止交易会话
   - Pause and resume trading / 暂停和恢复交易
   - Track session status / 跟踪会话状态

2. **Order Execution / 订单执行**
   - Execute trades based on signals / 根据信号执行交易
   - Batch trade execution / 批量交易执行
   - Automatic quantity calculation / 自动计算交易数量
   - Order status tracking / 订单状态跟踪

3. **Risk Management Integration / 风险管理集成**
   - Pre-trade risk checks / 交易前风险检查
   - Position size limits / 持仓规模限制
   - Risk alert monitoring / 风险预警监控
   - Automatic trading pause on critical alerts / 严重预警时自动暂停交易

4. **Position Monitoring / 持仓监控**
   - Real-time position updates / 实时持仓更新
   - Portfolio value tracking / 投资组合价值跟踪
   - P&L calculation / 盈亏计算
   - Trade history tracking / 交易历史跟踪

## Architecture / 架构

```
LiveTradingManager
├── Portfolio Manager (投资组合管理器)
│   ├── Create portfolios (创建投资组合)
│   ├── Update positions (更新持仓)
│   └── Track trade history (跟踪交易历史)
├── Risk Manager (风险管理器)
│   ├── Check position risk (检查持仓风险)
│   ├── Generate risk alerts (生成风险预警)
│   └── Monitor drawdown (监控回撤)
└── Trading API Adapter (交易API适配器)
    ├── Connect to broker (连接券商)
    ├── Place orders (下单)
    └── Query positions (查询持仓)
```

## Usage / 使用方法

### Basic Usage / 基本使用

```python
from src.application.live_trading_manager import LiveTradingManager
from src.core.portfolio_manager import PortfolioManager
from src.core.risk_manager import RiskManager
from src.infrastructure.trading_api_adapter import TradingAPIAdapter
from src.infrastructure.logger_system import LoggerSystem
from src.models.trading_models import LiveTradingConfig, Signal

# Initialize components / 初始化组件
logger_system = LoggerSystem()
logger_system.setup(log_dir="logs", log_level="INFO")

portfolio_manager = PortfolioManager(logger=logger_system)
risk_manager = RiskManager(logger=logger_system)
trading_api = TradingAPIAdapter()

live_trading_manager = LiveTradingManager(
    portfolio_manager=portfolio_manager,
    risk_manager=risk_manager,
    trading_api=trading_api,
    logger=logger_system
)

# Create trading configuration / 创建交易配置
trading_config = LiveTradingConfig(
    broker="mock",
    credentials={"account": "your_account"},
    max_position_size=0.3,
    max_daily_trades=10,
    stop_loss_pct=0.05,
    take_profit_pct=0.10,
    trading_hours={"start": "09:30", "end": "15:00"}
)

# Start trading session / 启动交易会话
session = live_trading_manager.start_live_trading(
    model_id="lgbm_model_v1",
    initial_capital=100000.0,
    trading_config=trading_config
)

# Execute trade / 执行交易
signal = Signal(
    stock_code="600519",
    action="buy",
    score=0.85,
    confidence=0.90,
    timestamp=datetime.now().isoformat()
)

result = live_trading_manager.execute_trade(
    session_id=session.session_id,
    signal=signal
)

# Get current positions / 获取当前持仓
portfolio = live_trading_manager.get_current_positions(session.session_id)

# Stop trading / 停止交易
summary = live_trading_manager.stop_trading(session.session_id)
```

### Advanced Usage / 高级使用

#### Batch Trade Execution / 批量交易执行

```python
# Create multiple signals / 创建多个信号
signals = [
    Signal(stock_code="600519", action="buy", score=0.85, confidence=0.90, timestamp=datetime.now().isoformat()),
    Signal(stock_code="300750", action="buy", score=0.78, confidence=0.85, timestamp=datetime.now().isoformat()),
    Signal(stock_code="000001", action="sell", score=0.45, confidence=0.70, timestamp=datetime.now().isoformat())
]

# Execute all trades / 执行所有交易
results = live_trading_manager.execute_batch_trades(
    session_id=session.session_id,
    signals=signals
)

# Check results / 检查结果
for result in results:
    print(f"{result.action} {result.symbol}: {result.status}")
```

#### Risk Alert Monitoring / 风险预警监控

```python
# Check for risk alerts / 检查风险预警
alert = live_trading_manager.check_risk_alerts(session.session_id)

if alert:
    print(f"Risk Alert: {alert['severity']}")
    print(f"Message: {alert['message']}")
    
    # Trading will be automatically paused if severity is critical
    # 如果严重程度为严重，交易将自动暂停
    if alert['severity'] == 'critical':
        print("Trading has been automatically paused")
```

#### Pause and Resume Trading / 暂停和恢复交易

```python
# Pause trading / 暂停交易
live_trading_manager.pause_trading(session.session_id)

# Do some analysis or wait for market conditions
# 进行一些分析或等待市场条件

# Resume trading / 恢复交易
live_trading_manager.resume_trading(session.session_id)
```

## API Reference / API参考

### LiveTradingManager

#### `__init__(portfolio_manager, risk_manager, trading_api, logger=None)`

Initialize the Live Trading Manager.

**Parameters:**
- `portfolio_manager` (PortfolioManager): Portfolio manager instance
- `risk_manager` (RiskManager): Risk manager instance
- `trading_api` (TradingAPIAdapter): Trading API adapter instance
- `logger` (LoggerSystem, optional): Logger system instance

#### `start_live_trading(model_id, initial_capital, trading_config)`

Start a new live trading session.

**Parameters:**
- `model_id` (str): Model identifier to use for trading
- `initial_capital` (float): Initial capital for trading
- `trading_config` (LiveTradingConfig): Live trading configuration

**Returns:**
- `TradingSession`: Created trading session

**Raises:**
- `ValueError`: If parameters are invalid
- `RuntimeError`: If broker connection fails

#### `execute_trade(session_id, signal)`

Execute a trade based on signal with risk checks.

**Parameters:**
- `session_id` (str): Trading session identifier
- `signal` (Signal): Trading signal to execute

**Returns:**
- `TradeResult`: Trade execution result

**Raises:**
- `ValueError`: If session not found or signal invalid
- `RuntimeError`: If trade execution fails

#### `get_current_positions(session_id)`

Get current positions for a trading session.

**Parameters:**
- `session_id` (str): Trading session identifier

**Returns:**
- `Portfolio`: Current portfolio

**Raises:**
- `ValueError`: If session not found

#### `stop_trading(session_id)`

Stop a trading session and generate summary.

**Parameters:**
- `session_id` (str): Trading session identifier

**Returns:**
- `Dict`: Trading session summary

**Raises:**
- `ValueError`: If session not found

#### `pause_trading(session_id)`

Pause a trading session.

**Parameters:**
- `session_id` (str): Trading session identifier

**Raises:**
- `ValueError`: If session not found or not active

#### `resume_trading(session_id)`

Resume a paused trading session.

**Parameters:**
- `session_id` (str): Trading session identifier

**Raises:**
- `ValueError`: If session not found or not paused

#### `get_trading_status(session_id)`

Get current trading status for a session.

**Parameters:**
- `session_id` (str): Trading session identifier

**Returns:**
- `TradingStatus`: Current trading status

**Raises:**
- `ValueError`: If session not found

#### `check_risk_alerts(session_id)`

Check for risk alerts in a trading session.

**Parameters:**
- `session_id` (str): Trading session identifier

**Returns:**
- `Optional[Dict]`: Risk alert if any, None otherwise

**Raises:**
- `ValueError`: If session not found

#### `execute_batch_trades(session_id, signals)`

Execute multiple trades in batch.

**Parameters:**
- `session_id` (str): Trading session identifier
- `signals` (List[Signal]): List of trading signals

**Returns:**
- `List[TradeResult]`: List of trade results

**Raises:**
- `ValueError`: If session not found

## Configuration / 配置

### LiveTradingConfig

```python
@dataclass
class LiveTradingConfig:
    broker: str                      # Broker name / 券商名称
    credentials: Dict[str, str]      # Authentication credentials / 认证凭证
    max_position_size: float         # Maximum position size (0-1) / 最大持仓比例
    max_daily_trades: int            # Maximum daily trades / 最大日交易次数
    stop_loss_pct: float             # Stop loss percentage / 止损百分比
    take_profit_pct: float           # Take profit percentage / 止盈百分比
    trading_hours: Dict[str, str]    # Trading hours / 交易时间
```

## Risk Management / 风险管理

The Live Trading Manager integrates with the Risk Manager to perform pre-trade risk checks:

实盘交易管理器与风险管理器集成以执行交易前风险检查：

1. **Position Size Check / 持仓规模检查**
   - Ensures no single position exceeds the maximum position size
   - 确保单个持仓不超过最大持仓规模

2. **Sector Concentration Check / 行业集中度检查**
   - Monitors sector exposure to prevent over-concentration
   - 监控行业暴露以防止过度集中

3. **Drawdown Monitoring / 回撤监控**
   - Tracks portfolio drawdown and triggers alerts
   - 跟踪投资组合回撤并触发预警

4. **Daily Loss Limit / 日亏损限制**
   - Monitors daily losses and pauses trading if exceeded
   - 监控日亏损并在超过时暂停交易

## Error Handling / 错误处理

The Live Trading Manager handles various error scenarios:

实盘交易管理器处理各种错误场景：

1. **Connection Errors / 连接错误**
   - Broker API connection failures
   - 券商API连接失败

2. **Order Execution Errors / 订单执行错误**
   - Insufficient funds
   - 资金不足
   - Invalid order parameters
   - 无效的订单参数

3. **Risk Check Failures / 风险检查失败**
   - Position size violations
   - 持仓规模违规
   - Risk limit breaches
   - 风险限制违规

4. **Session Management Errors / 会话管理错误**
   - Invalid session state transitions
   - 无效的会话状态转换
   - Session not found
   - 未找到会话

## Best Practices / 最佳实践

1. **Always Monitor Risk Alerts / 始终监控风险预警**
   - Regularly check for risk alerts
   - 定期检查风险预警
   - Set up automated alert notifications
   - 设置自动预警通知

2. **Use Appropriate Position Sizing / 使用适当的持仓规模**
   - Don't exceed recommended position sizes
   - 不要超过推荐的持仓规模
   - Diversify across multiple positions
   - 在多个持仓之间分散投资

3. **Test with Mock Broker First / 先使用模拟券商测试**
   - Always test strategies with mock broker before live trading
   - 在实盘交易前始终使用模拟券商测试策略
   - Verify all functionality works as expected
   - 验证所有功能按预期工作

4. **Implement Stop Loss / 实施止损**
   - Always set appropriate stop loss levels
   - 始终设置适当的止损水平
   - Monitor positions regularly
   - 定期监控持仓

5. **Keep Logs / 保留日志**
   - Enable detailed logging for debugging
   - 启用详细日志以进行调试
   - Review logs regularly for issues
   - 定期查看日志以发现问题

## Examples / 示例

See `examples/demo_live_trading_manager.py` for a complete working example.

查看 `examples/demo_live_trading_manager.py` 获取完整的工作示例。

## Related Components / 相关组件

- **PortfolioManager**: Manages portfolios and positions / 管理投资组合和持仓
- **RiskManager**: Performs risk checks and monitoring / 执行风险检查和监控
- **TradingAPIAdapter**: Connects to broker APIs / 连接券商API
- **SimulationEngine**: For testing strategies before live trading / 用于在实盘交易前测试策略

## Troubleshooting / 故障排除

### Common Issues / 常见问题

1. **Broker Connection Failed / 券商连接失败**
   - Check credentials are correct
   - 检查凭证是否正确
   - Verify broker API is accessible
   - 验证券商API是否可访问

2. **Trade Execution Failed / 交易执行失败**
   - Check account has sufficient funds
   - 检查账户是否有足够资金
   - Verify stock code is valid
   - 验证股票代码是否有效

3. **Risk Check Failed / 风险检查失败**
   - Review risk thresholds
   - 审查风险阈值
   - Adjust position sizes
   - 调整持仓规模

4. **Session Not Found / 未找到会话**
   - Verify session ID is correct
   - 验证会话ID是否正确
   - Check session hasn't been deleted
   - 检查会话是否已被删除

## Support / 支持

For issues or questions, please refer to:
- Project documentation / 项目文档
- Example scripts / 示例脚本
- API reference / API参考

如有问题或疑问，请参考：
- 项目文档
- 示例脚本
- API参考
