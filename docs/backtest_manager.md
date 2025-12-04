# 回测管理器文档 / Backtest Manager Documentation

## 概述 / Overview

回测管理器（BacktestManager）是量化交易系统的核心组件之一，负责执行历史回测、计算性能指标和生成回测报告。

The Backtest Manager is one of the core components of the quantitative trading system, responsible for executing historical backtests, calculating performance metrics, and generating backtest reports.

## 主要功能 / Key Features

1. **模型加载** / Model Loading
   - 加载训练好的模型进行回测
   - Load trained models for backtesting

2. **信号生成** / Signal Generation
   - 基于模型预测生成交易信号
   - Generate trading signals based on model predictions

3. **回测执行** / Backtest Execution
   - 使用qlib回测引擎模拟交易
   - Simulate trading using qlib backtest engine

4. **性能指标计算** / Performance Metrics Calculation
   - 计算收益率、夏普比率、最大回撤等指标
   - Calculate returns, Sharpe ratio, max drawdown, etc.

5. **基准对比** / Benchmark Comparison
   - 与基准指数对比，计算超额收益
   - Compare with benchmark index, calculate excess returns

6. **结果保存** / Result Saving
   - 保存回测结果、交易记录和性能报告
   - Save backtest results, trade records, and performance reports

## 架构设计 / Architecture Design

```
BacktestManager
├── 模型加载 / Model Loading
│   └── _load_model()
├── 信号生成 / Signal Generation
│   └── _generate_signals()
├── 回测执行 / Backtest Execution
│   ├── _execute_backtest()
│   └── _extract_trades()
├── 收益计算 / Returns Calculation
│   └── _calculate_returns()
├── 基准获取 / Benchmark Retrieval
│   └── _get_benchmark_returns()
├── 指标计算 / Metrics Calculation
│   ├── calculate_metrics()
│   └── _calculate_max_drawdown()
└── 结果保存 / Result Saving
    └── _save_backtest_result()
```

## 数据模型 / Data Models

### BacktestConfig

回测配置类，包含策略配置、执行器配置和基准指数。

Backtest configuration class containing strategy config, executor config, and benchmark index.

```python
@dataclass
class BacktestConfig:
    strategy_config: Dict[str, Any]  # 策略配置 / Strategy configuration
    executor_config: Dict[str, Any]  # 执行器配置 / Executor configuration
    benchmark: str                    # 基准指数 / Benchmark index
```

**示例 / Example:**

```python
config = BacktestConfig(
    strategy_config={
        "instruments": "csi300",  # 股票池 / Stock pool
        "topk": 50,               # 持仓数量 / Position count
        "n_drop": 5,              # 调仓数量 / Rebalance count
    },
    executor_config={
        "time_per_step": "day",   # 调仓频率 / Rebalance frequency
    },
    benchmark="SH000300"          # 沪深300指数 / CSI300 index
)
```

### BacktestResult

回测结果类，包含收益率、持仓、指标和交易记录。

Backtest result class containing returns, positions, metrics, and trade records.

```python
@dataclass
class BacktestResult:
    returns: pd.Series              # 收益率序列 / Returns series
    positions: pd.DataFrame         # 持仓数据 / Position data
    metrics: Dict[str, float]       # 性能指标 / Performance metrics
    trades: List[Trade]             # 交易记录 / Trade records
    benchmark_returns: Optional[pd.Series]  # 基准收益率 / Benchmark returns
```

### Trade

交易记录类，记录单笔交易的详细信息。

Trade record class recording detailed information of a single trade.

```python
@dataclass
class Trade:
    trade_id: str      # 交易ID / Trade ID
    timestamp: str     # 时间戳 / Timestamp
    symbol: str        # 股票代码 / Stock symbol
    action: str        # 操作类型 / Action type (buy/sell)
    quantity: float    # 数量 / Quantity
    price: float       # 价格 / Price
    commission: float  # 手续费 / Commission
    total_cost: float  # 总成本 / Total cost
```

## 使用方法 / Usage

### 1. 初始化 / Initialization

```python
from src.application.backtest_manager import BacktestManager, BacktestConfig
from src.infrastructure.qlib_wrapper import QlibWrapper

# 初始化qlib / Initialize qlib
qlib_wrapper = QlibWrapper()
qlib_wrapper.init(
    provider_uri="~/.qlib/qlib_data/cn_data",
    region="cn"
)

# 创建回测管理器 / Create backtest manager
backtest_manager = BacktestManager(
    qlib_wrapper=qlib_wrapper,
    output_dir="./outputs/backtests"
)
```

### 2. 配置回测参数 / Configure Backtest Parameters

```python
config = BacktestConfig(
    strategy_config={
        "instruments": "csi300",
        "topk": 50,
        "n_drop": 5,
    },
    executor_config={
        "time_per_step": "day",
    },
    benchmark="SH000300"
)
```

### 3. 运行回测 / Run Backtest

```python
result = backtest_manager.run_backtest(
    model_id="lgbm_model_20240101_120000",
    start_date="2023-01-01",
    end_date="2023-12-31",
    config=config
)
```

### 4. 分析结果 / Analyze Results

```python
# 查看性能指标 / View performance metrics
print(f"总收益率 / Total Return: {result.metrics['total_return']:.2%}")
print(f"年化收益率 / Annual Return: {result.metrics['annual_return']:.2%}")
print(f"夏普比率 / Sharpe Ratio: {result.metrics['sharpe_ratio']:.4f}")
print(f"最大回撤 / Max Drawdown: {result.metrics['max_drawdown']:.2%}")

# 查看超额收益 / View excess returns
if 'excess_return' in result.metrics:
    print(f"超额收益 / Excess Return: {result.metrics['excess_return']:.2%}")
    print(f"信息比率 / Information Ratio: {result.metrics['information_ratio']:.4f}")

# 查看收益率曲线 / View returns curve
import matplotlib.pyplot as plt

cumulative_returns = (1 + result.returns).cumprod()
plt.figure(figsize=(12, 6))
plt.plot(cumulative_returns, label='Strategy')

if result.benchmark_returns is not None:
    benchmark_cumulative = (1 + result.benchmark_returns).cumprod()
    plt.plot(benchmark_cumulative, label='Benchmark')

plt.legend()
plt.title('Cumulative Returns')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.grid(True)
plt.show()
```

## 性能指标说明 / Performance Metrics Description

### 基础指标 / Basic Metrics

1. **总收益率 (Total Return)**
   - 回测期间的总收益率
   - Total return during backtest period
   - 计算公式 / Formula: `(最终价值 / 初始价值) - 1`

2. **年化收益率 (Annual Return)**
   - 年化后的收益率
   - Annualized return
   - 计算公式 / Formula: `(1 + 总收益率) ^ (1 / 年数) - 1`

3. **波动率 (Volatility)**
   - 收益率的标准差（年化）
   - Standard deviation of returns (annualized)
   - 计算公式 / Formula: `std(日收益率) * sqrt(252)`

4. **夏普比率 (Sharpe Ratio)**
   - 风险调整后的收益率
   - Risk-adjusted return
   - 计算公式 / Formula: `年化收益率 / 波动率`

5. **最大回撤 (Max Drawdown)**
   - 从峰值到谷底的最大跌幅
   - Maximum decline from peak to trough
   - 计算公式 / Formula: `min((当前价值 - 历史最高) / 历史最高)`

6. **胜率 (Win Rate)**
   - 盈利交易日占比
   - Percentage of profitable trading days
   - 计算公式 / Formula: `盈利天数 / 总交易天数`

### 基准对比指标 / Benchmark Comparison Metrics

1. **超额收益 (Excess Return)**
   - 相对基准的超额收益
   - Excess return relative to benchmark
   - 计算公式 / Formula: `策略收益率 - 基准收益率`

2. **信息比率 (Information Ratio)**
   - 超额收益的风险调整指标
   - Risk-adjusted excess return
   - 计算公式 / Formula: `年化超额收益 / 超额收益波动率`

3. **基准收益 (Benchmark Return)**
   - 基准指数的收益率
   - Return of benchmark index

## 回测流程 / Backtest Process

```
1. 加载模型 / Load Model
   ↓
2. 生成预测信号 / Generate Prediction Signals
   ↓
3. 执行回测 / Execute Backtest
   ├── 根据信号调整持仓 / Adjust positions based on signals
   ├── 计算交易成本 / Calculate transaction costs
   └── 记录交易明细 / Record trade details
   ↓
4. 计算收益率 / Calculate Returns
   ↓
5. 获取基准收益率 / Get Benchmark Returns
   ↓
6. 计算性能指标 / Calculate Performance Metrics
   ├── 基础指标 / Basic metrics
   └── 基准对比指标 / Benchmark comparison metrics
   ↓
7. 保存回测结果 / Save Backtest Results
   ├── 指标文件 / Metrics file (metrics.json)
   ├── 收益率文件 / Returns file (returns.csv)
   ├── 持仓文件 / Positions file (positions.csv)
   ├── 交易记录 / Trade records (trades.csv)
   └── 基准收益率 / Benchmark returns (benchmark_returns.csv)
```

## 输出文件结构 / Output File Structure

```
outputs/backtests/
└── {model_id}_{timestamp}/
    ├── config.json              # 回测配置 / Backtest configuration
    ├── metrics.json             # 性能指标 / Performance metrics
    ├── returns.csv              # 收益率序列 / Returns series
    ├── positions.csv            # 持仓数据 / Position data
    ├── trades.csv               # 交易记录 / Trade records
    └── benchmark_returns.csv    # 基准收益率 / Benchmark returns
```

## 错误处理 / Error Handling

BacktestManager提供完善的错误处理机制：

BacktestManager provides comprehensive error handling:

1. **模型加载错误** / Model Loading Error
   - 模型文件不存在
   - Model file not found
   - 抛出 `BacktestManagerError`

2. **信号生成错误** / Signal Generation Error
   - 数据不可用
   - Data unavailable
   - 抛出 `BacktestManagerError`

3. **回测执行错误** / Backtest Execution Error
   - 回测引擎异常
   - Backtest engine exception
   - 抛出 `BacktestManagerError`

4. **指标计算错误** / Metrics Calculation Error
   - 数据格式错误
   - Data format error
   - 抛出 `BacktestManagerError`

## 最佳实践 / Best Practices

1. **选择合适的回测周期** / Choose Appropriate Backtest Period
   - 至少1年的数据以获得可靠结果
   - At least 1 year of data for reliable results
   - 包含不同市场环境（牛市、熊市、震荡市）
   - Include different market conditions (bull, bear, sideways)

2. **设置合理的策略参数** / Set Reasonable Strategy Parameters
   - topk: 根据资金规模选择持仓数量
   - topk: Choose position count based on capital size
   - n_drop: 控制换手率，避免过度交易
   - n_drop: Control turnover rate, avoid excessive trading

3. **选择合适的基准** / Choose Appropriate Benchmark
   - 与策略风格匹配的指数
   - Index matching strategy style
   - 例如：沪深300、中证500、创业板指
   - Examples: CSI300, CSI500, ChiNext

4. **关注多个指标** / Focus on Multiple Metrics
   - 不要只看收益率
   - Don't focus only on returns
   - 综合考虑风险指标（波动率、回撤）
   - Consider risk metrics (volatility, drawdown)
   - 关注风险调整后收益（夏普比率）
   - Focus on risk-adjusted returns (Sharpe ratio)

5. **保存回测结果** / Save Backtest Results
   - 便于后续分析和对比
   - Facilitate subsequent analysis and comparison
   - 记录回测参数和市场环境
   - Record backtest parameters and market conditions

## 示例代码 / Example Code

完整的示例代码请参考：
For complete example code, please refer to:

```
examples/demo_backtest_manager.py
```

## 相关文档 / Related Documentation

- [训练管理器文档](./training_manager.md)
- [模型注册表文档](./model_registry.md)
- [Qlib封装器文档](./qlib_wrapper_implementation.md)

## 常见问题 / FAQ

### Q1: 如何选择合适的topk值？

**A:** topk值取决于以下因素：
- 资金规模：资金越大，可以持有更多股票
- 流动性：确保每只股票有足够的流动性
- 分散度：通常建议持有30-100只股票以分散风险

### Q2: 回测结果与实盘差异大怎么办？

**A:** 可能的原因和解决方案：
- 交易成本：确保回测中包含合理的手续费和滑点
- 流动性：考虑大单对价格的冲击
- 数据质量：检查历史数据的准确性
- 过拟合：使用更长的回测周期和样本外测试

### Q3: 如何解释负的夏普比率？

**A:** 负的夏普比率表示：
- 策略的平均收益为负
- 承担风险没有获得正收益
- 需要重新评估策略或参数

### Q4: 最大回撤多少是可接受的？

**A:** 取决于风险承受能力：
- 保守型：< 10%
- 稳健型：10-20%
- 进取型：20-30%
- 超过30%需要谨慎考虑

## 更新日志 / Changelog

### v1.0.0 (2024-12-04)
- ✓ 初始版本发布 / Initial release
- ✓ 实现基本回测功能 / Implement basic backtest functionality
- ✓ 支持性能指标计算 / Support performance metrics calculation
- ✓ 支持基准对比 / Support benchmark comparison
- ✓ 实现结果保存 / Implement result saving
