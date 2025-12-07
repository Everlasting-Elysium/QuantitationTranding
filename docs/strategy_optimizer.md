# Strategy Optimizer (策略优化器)

## Overview (概述)

The Strategy Optimizer is a component that optimizes trading strategies based on target returns and risk preferences. It uses multi-objective optimization to balance returns and risk while respecting various constraints.

策略优化器是一个根据目标收益率和风险偏好优化交易策略的组件。它使用多目标优化来平衡收益和风险，同时遵守各种约束条件。

## Features (功能特性)

### 1. Target Return Validation (目标收益率验证)
- Validates target returns against historical data
- Provides feasibility assessment
- Suggests realistic targets based on historical performance

根据历史数据验证目标收益率
提供可行性评估
基于历史表现建议现实的目标

### 2. Multi-Objective Optimization (多目标优化)
- Balances return and risk objectives
- Considers multiple constraints simultaneously
- Uses scipy optimization algorithms

平衡收益和风险目标
同时考虑多个约束条件
使用scipy优化算法

### 3. Risk Preference Adjustment (风险偏好调整)
- Supports three risk tolerance levels: conservative, moderate, aggressive
- Adjusts parameters based on risk preference
- Customizes stop-loss and take-profit levels

支持三种风险承受能力：保守型、稳健型、进取型
根据风险偏好调整参数
自定义止损和止盈水平

### 4. Asset Allocation (资产配置)
- Generates optimal portfolio weights
- Ensures diversification requirements
- Respects position size limits

生成最优投资组合权重
确保分散化要求
遵守持仓规模限制

## Usage (使用方法)

### Basic Usage (基本用法)

```python
from src.application.strategy_optimizer import StrategyOptimizer
from src.models.market_models import OptimizationConstraints

# Initialize optimizer
optimizer = StrategyOptimizer()

# Define constraints
constraints = OptimizationConstraints(
    max_position_size=0.25,      # Maximum 25% per asset
    max_sector_exposure=0.40,    # Maximum 40% per sector
    min_diversification=5,       # At least 5 assets
    max_turnover=2.0,            # Maximum 200% annual turnover
    risk_tolerance="moderate"    # Risk tolerance level
)

# Optimize strategy
strategy = optimizer.optimize_for_target_return(
    target_return=0.15,          # 15% annual target
    assets=asset_list,           # List of asset symbols
    constraints=constraints
)

# Access results
print(f"Expected return: {strategy.expected_return:.2%}")
print(f"Expected risk: {strategy.expected_risk:.2%}")
print(f"Asset weights: {strategy.asset_weights}")
```

### Parameter Suggestion (参数建议)

```python
# Get suggested parameters based on target and risk tolerance
params = optimizer.suggest_parameters(
    target_return=0.15,
    risk_tolerance="moderate"
)

print(f"Model type: {params.model_type}")
print(f"Features: {params.features}")
print(f"Lookback period: {params.lookback_period}")
print(f"Rebalance frequency: {params.rebalance_frequency}")
```

## Optimization Constraints (优化约束条件)

### OptimizationConstraints Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| max_position_size | float | 0.2 | Maximum position size per asset (20%) |
| max_sector_exposure | float | 0.4 | Maximum exposure to any sector (40%) |
| min_diversification | int | 5 | Minimum number of assets |
| max_turnover | float | 2.0 | Maximum annual turnover (200%) |
| risk_tolerance | str | "moderate" | Risk tolerance level |

### Risk Tolerance Levels (风险承受能力级别)

#### Conservative (保守型)
- Model: Linear regression
- Lookback: 60 days
- Rebalance: Monthly
- Stop loss: 5%
- Take profit: 10%

#### Moderate (稳健型)
- Model: LightGBM
- Lookback: 30 days
- Rebalance: Weekly
- Stop loss: 10%
- Take profit: 20%

#### Aggressive (进取型)
- Model: MLP (Neural Network)
- Lookback: 20 days
- Rebalance: Daily
- Stop loss: 15%
- Take profit: 30%

## Optimization Process (优化流程)

### Step 1: Validate Target Return (验证目标收益率)
The optimizer first validates if the target return is achievable based on historical data.

优化器首先验证目标收益率是否基于历史数据可实现。

### Step 2: Get Historical Metrics (获取历史指标)
Retrieves historical performance metrics for all assets in the portfolio.

检索投资组合中所有资产的历史表现指标。

### Step 3: Multi-Objective Optimization (多目标优化)
Uses scipy's SLSQP algorithm to find optimal weights that:
- Minimize deviation from target return
- Minimize portfolio risk
- Satisfy all constraints

使用scipy的SLSQP算法找到最优权重：
- 最小化与目标收益率的偏差
- 最小化投资组合风险
- 满足所有约束条件

### Step 4: Calculate Expected Metrics (计算预期指标)
Calculates expected return and risk for the optimized portfolio.

计算优化投资组合的预期收益率和风险。

### Step 5: Generate Strategy Parameters (生成策略参数)
Creates complete strategy parameters including model type, features, and risk management settings.

创建完整的策略参数，包括模型类型、特征和风险管理设置。

### Step 6: Calculate Optimization Score (计算优化评分)
Assigns a score (0-100) based on:
- How close expected return is to target (50 points)
- Risk-adjusted return (Sharpe ratio) (50 points)

基于以下因素分配评分（0-100）：
- 预期收益率与目标的接近程度（50分）
- 风险调整后收益率（夏普比率）（50分）

### Step 7: Generate Warnings (生成警告)
Identifies potential issues such as:
- Large deviation from target return
- High portfolio risk
- Concentration risk
- Low diversification

识别潜在问题，例如：
- 与目标收益率偏差较大
- 投资组合风险较高
- 集中度风险
- 分散化程度低

## Output (输出)

### OptimizedStrategy Object

```python
@dataclass
class OptimizedStrategy:
    strategy_id: str                    # Unique identifier
    target_return: float                # Target annual return
    expected_return: float              # Expected annual return
    expected_risk: float                # Expected risk (volatility)
    asset_weights: Dict[str, float]     # Asset allocation weights
    rebalance_frequency: str            # Rebalancing frequency
    parameters: Dict[str, any]          # Strategy parameters
    optimization_score: float           # Overall score (0-100)
    feasible: bool                      # Whether strategy is feasible
    warnings: List[str]                 # List of warnings
```

## Examples (示例)

### Example 1: Conservative Strategy (保守型策略)

```python
constraints = OptimizationConstraints(
    max_position_size=0.15,
    min_diversification=8,
    risk_tolerance="conservative"
)

strategy = optimizer.optimize_for_target_return(
    target_return=0.08,  # 8% target
    assets=assets,
    constraints=constraints
)
```

### Example 2: Aggressive Strategy (进取型策略)

```python
constraints = OptimizationConstraints(
    max_position_size=0.30,
    min_diversification=3,
    risk_tolerance="aggressive"
)

strategy = optimizer.optimize_for_target_return(
    target_return=0.25,  # 25% target
    assets=assets,
    constraints=constraints
)
```

### Example 3: Custom Risk Parameters (自定义风险参数)

```python
# Get suggested parameters
params = optimizer.suggest_parameters(
    target_return=0.15,
    risk_tolerance="moderate"
)

# Customize risk parameters
params.risk_params["stop_loss"] = 0.08  # 8% stop loss
params.risk_params["take_profit"] = 0.25  # 25% take profit

# Use in training
training_config = TrainingConfig(
    model_type=params.model_type,
    dataset_config=dataset_config,
    model_params={},
    training_params=params.risk_params,
    experiment_name="custom_strategy"
)
```

## Integration with Training (与训练集成)

The Strategy Optimizer can be integrated with the Training Manager:

策略优化器可以与训练管理器集成：

```python
from src.application.training_manager import TrainingManager
from src.application.strategy_optimizer import StrategyOptimizer

# Optimize strategy
optimizer = StrategyOptimizer()
strategy = optimizer.optimize_for_target_return(
    target_return=0.15,
    assets=assets,
    constraints=constraints
)

# Use optimized parameters for training
training_manager = TrainingManager(...)
result = training_manager.train_model(
    TrainingConfig(
        model_type=strategy.parameters["model_type"],
        dataset_config=dataset_config,
        model_params=strategy.parameters,
        training_params={},
        experiment_name="optimized_strategy",
        target_return=strategy.target_return
    )
)
```

## Best Practices (最佳实践)

### 1. Start with Historical Analysis (从历史分析开始)
Always analyze historical performance before setting target returns.

在设定目标收益率之前，始终分析历史表现。

### 2. Use Realistic Targets (使用现实的目标)
Set target returns that are achievable based on historical data.

根据历史数据设定可实现的目标收益率。

### 3. Consider Risk Tolerance (考虑风险承受能力)
Choose risk tolerance level that matches your investment goals.

选择与您的投资目标相匹配的风险承受能力。

### 4. Review Warnings (查看警告)
Pay attention to warnings generated by the optimizer.

注意优化器生成的警告。

### 5. Backtest Optimized Strategy (回测优化策略)
Always backtest the optimized strategy before live trading.

在实盘交易之前，始终回测优化策略。

### 6. Monitor and Rebalance (监控和再平衡)
Regularly monitor portfolio performance and rebalance as needed.

定期监控投资组合表现并根据需要进行再平衡。

## Limitations (局限性)

1. **Historical Data Dependency**: Optimization is based on historical data, which may not predict future performance.
   
   历史数据依赖：优化基于历史数据，可能无法预测未来表现。

2. **Simplified Risk Model**: Uses simplified correlation assumptions for risk calculation.
   
   简化的风险模型：使用简化的相关性假设进行风险计算。

3. **No Transaction Costs**: Does not account for transaction costs and slippage.
   
   无交易成本：不考虑交易成本和滑点。

4. **Static Optimization**: Optimization is performed at a single point in time.
   
   静态优化：优化在单个时间点执行。

## See Also (另请参阅)

- [Performance Analyzer](performance_analyzer.md) - For historical performance analysis
- [Training Manager](training_manager.md) - For model training
- [Backtest Manager](backtest_manager.md) - For strategy backtesting
- [Risk Manager](risk_manager.md) - For risk management

## API Reference (API参考)

For detailed API documentation, see [API Reference](api_reference.md#strategy-optimizer).
