# 模拟交易引擎文档 / Simulation Engine Documentation

## 概述 / Overview

模拟交易引擎（Simulation Engine）是一个用于执行模拟交易测试的核心组件。它允许用户在不使用真实资金的情况下，使用真实市场数据测试交易策略的效果。

The Simulation Engine is a core component for executing simulation trading tests. It allows users to test trading strategy effectiveness using real market data without using real money.

## 主要功能 / Main Features

### 1. 模拟会话管理 / Simulation Session Management
- 创建和管理模拟交易会话 / Create and manage simulation trading sessions
- 跟踪会话状态和进度 / Track session status and progress
- 支持多个并发会话 / Support multiple concurrent sessions

### 2. 每日信号生成和执行 / Daily Signal Generation and Execution
- 自动生成每日交易信号 / Automatically generate daily trading signals
- 模拟执行买入和卖出操作 / Simulate buy and sell operations
- 考虑交易成本（佣金）/ Consider trading costs (commission)

### 3. 持仓跟踪 / Position Tracking
- 实时跟踪模拟持仓 / Real-time tracking of simulated positions
- 更新持仓价格和价值 / Update position prices and values
- 计算未实现盈亏 / Calculate unrealized P&L

### 4. 收益计算 / Returns Calculation
- 计算日收益率 / Calculate daily returns
- 计算累计收益率 / Calculate cumulative returns
- 计算年化收益率 / Calculate annualized returns

### 5. 报告生成 / Report Generation
- 生成详细的模拟报告 / Generate detailed simulation reports
- 包含收益指标、风险指标和交易统计 / Include return metrics, risk metrics, and trading statistics
- 导出报告到文件 / Export reports to files

## 核心类 / Core Classes

### SimulationEngine

模拟交易引擎主类 / Main simulation engine class

#### 初始化 / Initialization

```python
from src.application.simulation_engine import SimulationEngine
from src.application.signal_generator import SignalGenerator
from src.core.portfolio_manager import PortfolioManager

simulation_engine = SimulationEngine(
    signal_generator=signal_generator,
    portfolio_manager=portfolio_manager,
    qlib_wrapper=qlib_wrapper,
    output_dir="./simulations"
)
```

#### 主要方法 / Main Methods

##### start_simulation()

启动模拟交易 / Start simulation trading

```python
session = simulation_engine.start_simulation(
    model_id="my_model_20240101",
    initial_capital=100000.0,
    simulation_days=30,
    start_date="2024-01-01",
    instruments="csi300",
    top_n=10
)
```

**参数 / Parameters:**
- `model_id` (str): 使用的模型ID / Model ID to use
- `initial_capital` (float): 初始资金 / Initial capital
- `simulation_days` (int): 模拟天数 / Number of simulation days
- `start_date` (str): 开始日期（YYYY-MM-DD格式）/ Start date (YYYY-MM-DD format)
- `instruments` (str): 股票池，默认"csi300" / Instrument pool, default "csi300"
- `top_n` (int): 买入候选数量，默认10 / Number of buy candidates, default 10

**返回 / Returns:**
- `SimulationSession`: 模拟会话对象 / Simulation session object

##### get_simulation_status()

获取模拟状态 / Get simulation status

```python
status = simulation_engine.get_simulation_status(session_id)
```

**返回 / Returns:**
- `Dict[str, Any]`: 包含以下字段的状态字典 / Status dictionary containing:
  - `session_id`: 会话ID / Session ID
  - `status`: 状态（"running", "completed", "failed"）/ Status
  - `current_value`: 当前投资组合价值 / Current portfolio value
  - `total_return_pct`: 总收益率百分比 / Total return percentage
  - `days_completed`: 已完成天数 / Days completed
  - `total_trades`: 总交易数 / Total trades

##### generate_simulation_report()

生成模拟报告 / Generate simulation report

```python
report = simulation_engine.generate_simulation_report(session_id)
```

**返回 / Returns:**
- `SimulationReport`: 包含详细统计信息的报告对象 / Report object with detailed statistics

##### list_sessions()

列出所有会话 / List all sessions

```python
sessions = simulation_engine.list_sessions()
```

**返回 / Returns:**
- `List[Dict[str, Any]]`: 所有会话的状态列表 / List of status for all sessions

##### delete_session()

删除会话 / Delete session

```python
success = simulation_engine.delete_session(session_id)
```

### SimulationSession

模拟会话数据类 / Simulation session dataclass

**属性 / Attributes:**
- `session_id` (str): 会话唯一标识符 / Session unique identifier
- `model_id` (str): 使用的模型ID / Model ID used
- `initial_capital` (float): 初始资金 / Initial capital
- `simulation_days` (int): 模拟天数 / Simulation days
- `start_date` (str): 开始日期 / Start date
- `end_date` (str): 结束日期 / End date
- `status` (str): 会话状态 / Session status
- `current_portfolio` (Portfolio): 当前投资组合 / Current portfolio

### SimulationReport

模拟报告数据类 / Simulation report dataclass

**属性 / Attributes:**
- `session_id` (str): 会话ID / Session ID
- `total_return` (float): 总收益率 / Total return
- `annual_return` (float): 年化收益率 / Annual return
- `sharpe_ratio` (float): 夏普比率 / Sharpe ratio
- `max_drawdown` (float): 最大回撤 / Max drawdown
- `win_rate` (float): 胜率 / Win rate
- `total_trades` (int): 总交易次数 / Total trades
- `profitable_trades` (int): 盈利交易次数 / Profitable trades
- `final_portfolio_value` (float): 最终投资组合价值 / Final portfolio value
- `daily_returns` (pd.Series): 日收益率序列 / Daily returns series
- `trade_history` (List[Trade]): 交易历史 / Trade history
- `daily_values` (pd.Series): 每日价值序列 / Daily values series

## 使用示例 / Usage Examples

### 基本使用流程 / Basic Usage Flow

```python
# 1. 初始化组件 / Initialize components
from src.application.simulation_engine import SimulationEngine
from src.application.signal_generator import SignalGenerator
from src.core.portfolio_manager import PortfolioManager
from src.infrastructure.qlib_wrapper import QlibWrapper
from src.infrastructure.logger_system import LoggerSystem

# 初始化日志 / Initialize logger
logger_system = LoggerSystem()
logger_system.setup(log_dir="./logs", log_level="INFO")

# 初始化Qlib / Initialize Qlib
qlib_wrapper = QlibWrapper()
qlib_wrapper.init(provider_uri="~/.qlib/qlib_data/cn_data", region="cn")

# 初始化其他组件 / Initialize other components
portfolio_manager = PortfolioManager(logger=logger_system)
signal_generator = SignalGenerator(
    model_registry=model_registry,
    qlib_wrapper=qlib_wrapper
)

# 创建模拟引擎 / Create simulation engine
simulation_engine = SimulationEngine(
    signal_generator=signal_generator,
    portfolio_manager=portfolio_manager,
    qlib_wrapper=qlib_wrapper,
    output_dir="./simulations"
)

# 2. 启动模拟 / Start simulation
session = simulation_engine.start_simulation(
    model_id="lgbm_model_20240101",
    initial_capital=100000.0,
    simulation_days=30,
    start_date="2024-01-01"
)

print(f"会话ID / Session ID: {session.session_id}")

# 3. 查看状态 / Check status
status = simulation_engine.get_simulation_status(session.session_id)
print(f"状态 / Status: {status['status']}")
print(f"当前价值 / Current value: {status['current_value']}")
print(f"总收益率 / Total return: {status['total_return_pct']:.2f}%")

# 4. 生成报告 / Generate report
report = simulation_engine.generate_simulation_report(session.session_id)

print(f"总收益率 / Total return: {report.total_return:.2%}")
print(f"年化收益率 / Annual return: {report.annual_return:.2%}")
print(f"夏普比率 / Sharpe ratio: {report.sharpe_ratio:.4f}")
print(f"最大回撤 / Max drawdown: {report.max_drawdown:.2%}")
print(f"胜率 / Win rate: {report.win_rate:.2%}")
print(f"总交易数 / Total trades: {report.total_trades}")
```

### 批量模拟测试 / Batch Simulation Testing

```python
# 测试不同参数组合 / Test different parameter combinations
test_configs = [
    {"initial_capital": 100000, "simulation_days": 30},
    {"initial_capital": 200000, "simulation_days": 30},
    {"initial_capital": 100000, "simulation_days": 60},
]

results = []

for config in test_configs:
    session = simulation_engine.start_simulation(
        model_id="my_model",
        initial_capital=config["initial_capital"],
        simulation_days=config["simulation_days"],
        start_date="2024-01-01"
    )
    
    report = simulation_engine.generate_simulation_report(session.session_id)
    
    results.append({
        "config": config,
        "total_return": report.total_return,
        "sharpe_ratio": report.sharpe_ratio,
        "max_drawdown": report.max_drawdown
    })

# 比较结果 / Compare results
for i, result in enumerate(results):
    print(f"\n配置 {i+1} / Config {i+1}:")
    print(f"  初始资金 / Initial capital: {result['config']['initial_capital']}")
    print(f"  模拟天数 / Simulation days: {result['config']['simulation_days']}")
    print(f"  总收益率 / Total return: {result['total_return']:.2%}")
    print(f"  夏普比率 / Sharpe ratio: {result['sharpe_ratio']:.4f}")
    print(f"  最大回撤 / Max drawdown: {result['max_drawdown']:.2%}")
```

## 输出文件 / Output Files

模拟引擎会在指定的输出目录中创建以下文件结构：

The simulation engine creates the following file structure in the specified output directory:

```
simulations/
├── sessions/
│   └── sim_xxxxxxxx/
│       └── session.json          # 会话信息 / Session information
└── reports/
    └── sim_xxxxxxxx/
        ├── summary.json           # 报告摘要 / Report summary
        ├── daily_returns.csv      # 日收益率 / Daily returns
        ├── daily_values.csv       # 每日价值 / Daily values
        └── trades.csv             # 交易历史 / Trade history
```

### session.json

```json
{
  "session_id": "sim_a1b2c3d4",
  "model_id": "lgbm_model_20240101",
  "initial_capital": 100000.0,
  "simulation_days": 30,
  "start_date": "2024-01-01",
  "end_date": "2024-02-15",
  "status": "completed",
  "created_at": "2024-01-01T10:00:00"
}
```

### summary.json

```json
{
  "session_id": "sim_a1b2c3d4",
  "total_return": 0.085,
  "annual_return": 0.24,
  "sharpe_ratio": 1.65,
  "max_drawdown": -0.032,
  "win_rate": 0.67,
  "total_trades": 45,
  "profitable_trades": 30,
  "final_portfolio_value": 108500.0,
  "generated_at": "2024-02-15T16:00:00"
}
```

## 注意事项 / Notes

### 1. 数据要求 / Data Requirements
- 确保qlib数据已正确初始化 / Ensure qlib data is properly initialized
- 模拟期间的数据必须可用 / Data for simulation period must be available
- 建议使用历史数据进行模拟 / Recommend using historical data for simulation

### 2. 性能考虑 / Performance Considerations
- 模拟天数越多，执行时间越长 / More simulation days = longer execution time
- 建议先用较短周期测试 / Recommend testing with shorter periods first
- 可以使用多进程并行执行多个模拟 / Can use multiprocessing for parallel simulations

### 3. 交易成本 / Trading Costs
- 当前实现使用简化的佣金计算（0.03%）/ Current implementation uses simplified commission (0.03%)
- 实际交易可能有更复杂的费用结构 / Actual trading may have more complex fee structures
- 可以根据需要调整佣金率 / Commission rate can be adjusted as needed

### 4. 风险控制 / Risk Control
- 模拟引擎会应用信号生成器的风险限制 / Simulation engine applies signal generator's risk limits
- 确保风险参数设置合理 / Ensure risk parameters are set reasonably
- 监控最大回撤和持仓集中度 / Monitor max drawdown and position concentration

## 常见问题 / FAQ

### Q1: 模拟结果与实际交易会有差异吗？/ Will simulation results differ from actual trading?

A: 是的，模拟结果可能与实际交易有差异，原因包括：
Yes, simulation results may differ from actual trading due to:
- 滑点（实际成交价格与预期价格的差异）/ Slippage (difference between expected and actual execution price)
- 市场冲击（大额订单对价格的影响）/ Market impact (effect of large orders on price)
- 流动性限制 / Liquidity constraints
- 实际交易费用可能更高 / Actual trading fees may be higher

### Q2: 如何选择合适的模拟天数？/ How to choose appropriate simulation days?

A: 建议：
Recommendations:
- 短期测试：7-30天 / Short-term testing: 7-30 days
- 中期测试：30-90天 / Medium-term testing: 30-90 days
- 长期测试：90天以上 / Long-term testing: 90+ days
- 根据策略的交易频率调整 / Adjust based on strategy's trading frequency

### Q3: 模拟失败怎么办？/ What to do if simulation fails?

A: 检查以下几点：
Check the following:
1. 模型是否存在且可加载 / Model exists and can be loaded
2. 数据是否覆盖模拟期间 / Data covers simulation period
3. 初始资金是否足够 / Initial capital is sufficient
4. 查看日志文件获取详细错误信息 / Check log files for detailed error messages

### Q4: 如何提高模拟速度？/ How to improve simulation speed?

A: 可以尝试：
You can try:
1. 减少模拟天数 / Reduce simulation days
2. 减少买入候选数量（top_n）/ Reduce number of buy candidates (top_n)
3. 使用更小的股票池 / Use smaller instrument pool
4. 优化模型预测速度 / Optimize model prediction speed

## 相关文档 / Related Documentation

- [信号生成器文档 / Signal Generator Documentation](./signal_generator.md)
- [投资组合管理器文档 / Portfolio Manager Documentation](./portfolio_manager.md)
- [回测管理器文档 / Backtest Manager Documentation](./backtest_manager.md)
- [风险管理器文档 / Risk Manager Documentation](./risk_manager.md)

## 更新日志 / Changelog

### v1.0.0 (2024-12-05)
- 初始版本发布 / Initial release
- 支持基本的模拟交易功能 / Support basic simulation trading features
- 支持会话管理和报告生成 / Support session management and report generation
