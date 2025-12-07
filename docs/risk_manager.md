# Risk Manager Documentation
# 风险管理器文档

## Overview / 概述

The Risk Manager is a core component of the Qlib Trading System that monitors and controls trading risks. It provides comprehensive risk assessment capabilities including position risk checks, Value at Risk (VaR) calculation, maximum drawdown monitoring, concentration risk analysis, and risk alert generation.

风险管理器是Qlib交易系统的核心组件，用于监控和控制交易风险。它提供全面的风险评估功能，包括持仓风险检查、风险价值（VaR）计算、最大回撤监控、集中度风险分析和风险预警生成。

## Features / 功能特性

### 1. Position Risk Checks / 持仓风险检查
- Validates trades against position size limits / 根据持仓规模限制验证交易
- Checks sector concentration / 检查行业集中度
- Provides suggested adjustments for violating trades / 为违规交易提供调整建议

### 2. Value at Risk (VaR) Calculation / 风险价值计算
- Historical simulation method / 历史模拟法
- Configurable confidence levels / 可配置置信水平
- Portfolio-level risk assessment / 投资组合级别风险评估

### 3. Maximum Drawdown Monitoring / 最大回撤监控
- Tracks portfolio value history / 跟踪投资组合价值历史
- Calculates current and historical drawdowns / 计算当前和历史回撤
- Alerts on excessive drawdowns / 超额回撤预警

### 4. Concentration Risk Analysis / 集中度风险分析
- Position-level concentration / 持仓级别集中度
- Sector-level concentration / 行业级别集中度
- Top-N holdings analysis / 前N大持仓分析

### 5. Risk Alert Generation / 风险预警生成
- Multi-level severity (info, warning, critical) / 多级严重程度（信息、警告、严重）
- Actionable recommendations / 可操作的建议
- Affected positions tracking / 受影响持仓跟踪

## Installation / 安装

The Risk Manager is part of the core module and is automatically available when you install the Qlib Trading System.

风险管理器是核心模块的一部分，安装Qlib交易系统时会自动可用。

```python
from src.core import RiskManager
```

## Usage / 使用方法

### Basic Initialization / 基本初始化

```python
from src.core import RiskManager
from src.infrastructure import LoggerSystem

# Initialize logger (optional)
logger = LoggerSystem()
logger.setup(log_dir="logs", log_level="INFO")

# Create Risk Manager with default settings
risk_manager = RiskManager(logger=logger)

# Or with custom thresholds
risk_manager = RiskManager(
    max_position_pct=0.25,      # 25% max position size
    max_sector_pct=0.35,         # 35% max sector exposure
    max_drawdown_pct=0.15,       # 15% max drawdown
    max_daily_loss_pct=0.03,     # 3% max daily loss
    var_confidence=0.99,         # 99% VaR confidence
    logger=logger
)
```

### Position Risk Checking / 持仓风险检查

```python
from src.models.trading_models import Portfolio, Position, Trade

# Create a portfolio
portfolio = Portfolio(
    portfolio_id="my_portfolio",
    positions={
        "AAPL": Position("AAPL", 100, 150.0, 160.0),
        "GOOGL": Position("GOOGL", 50, 2800.0, 2900.0)
    },
    cash=50000.0,
    initial_capital=200000.0
)
portfolio.update_total_value()

# Create a proposed trade
trade = Trade(
    trade_id="trade_001",
    timestamp="2024-01-01T10:00:00",
    symbol="MSFT",
    action="buy",
    quantity=100,
    price=300.0,
    commission=10.0
)

# Check if trade violates risk limits
result = risk_manager.check_position_risk(portfolio, trade)

if result['passed']:
    print("Trade passed risk checks")
else:
    print(f"Trade failed: {result['violations']}")
    print(f"Suggested adjustments: {result['suggested_adjustments']}")
```

### VaR Calculation / VaR计算

```python
import pandas as pd
import numpy as np

# Generate or load historical returns
returns = pd.Series(np.random.normal(0.001, 0.02, 100))
portfolio_value = 100000.0

# Calculate VaR at 95% confidence
var_95 = risk_manager.calculate_var(returns, portfolio_value, confidence=0.95)
print(f"VaR (95%): ${var_95:.2f}")

# Calculate VaR at 99% confidence
var_99 = risk_manager.calculate_var(returns, portfolio_value, confidence=0.99)
print(f"VaR (99%): ${var_99:.2f}")
```

### Maximum Drawdown Calculation / 最大回撤计算

```python
# Calculate max drawdown from returns
returns = pd.Series([0.02, 0.01, -0.05, -0.03, -0.02, 0.01, 0.02])
max_dd = risk_manager.calculate_max_drawdown(returns)
print(f"Maximum Drawdown: {max_dd:.2%}")

# Track portfolio values for ongoing drawdown monitoring
risk_manager.track_portfolio_value("portfolio_001", 100000.0)
risk_manager.track_portfolio_value("portfolio_001", 105000.0)
risk_manager.track_portfolio_value("portfolio_001", 98000.0)

# Get current drawdown
current_dd = risk_manager.get_portfolio_drawdown("portfolio_001")
print(f"Current Drawdown: {current_dd:.2%}")
```

### Concentration Risk Analysis / 集中度风险分析

```python
# Define sector mapping
sector_map = {
    "AAPL": "Technology",
    "GOOGL": "Technology",
    "MSFT": "Technology",
    "JPM": "Finance",
    "BAC": "Finance"
}

# Check concentration risk
concentration = risk_manager.check_concentration_risk(portfolio, sector_map)

print(f"Max Position: {concentration['max_position_pct']:.1f}%")
print(f"Top 5 Concentration: {concentration['top_5_concentration']:.1f}%")
print(f"Risk Level: {concentration['risk_level']}")
print(f"Sector Concentration: {concentration['sector_concentration']}")
```

### Risk Alert Generation / 风险预警生成

```python
# Generate risk alert based on current portfolio and returns
alert = risk_manager.generate_risk_alert(portfolio, returns, sector_map)

if alert:
    print(f"Alert ID: {alert['alert_id']}")
    print(f"Severity: {alert['severity']}")
    print(f"Message: {alert['message']}")
    print(f"Affected Positions: {alert['affected_positions']}")
    print(f"Recommended Actions: {alert['recommended_actions']}")
    
    # Get mitigation suggestions
    suggestions = risk_manager.suggest_risk_mitigation(alert)
    print(f"Mitigation Suggestions: {suggestions}")
else:
    print("No risk alerts")
```

## Configuration / 配置

### Risk Thresholds / 风险阈值

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_position_pct` | 0.3 (30%) | Maximum position size as percentage of portfolio |
| `max_sector_pct` | 0.4 (40%) | Maximum sector exposure |
| `max_drawdown_pct` | 0.2 (20%) | Maximum drawdown threshold |
| `max_daily_loss_pct` | 0.05 (5%) | Maximum daily loss percentage |
| `var_confidence` | 0.95 (95%) | VaR confidence level |

| 参数 | 默认值 | 描述 |
|------|--------|------|
| `max_position_pct` | 0.3 (30%) | 最大持仓比例 |
| `max_sector_pct` | 0.4 (40%) | 最大行业暴露 |
| `max_drawdown_pct` | 0.2 (20%) | 最大回撤阈值 |
| `max_daily_loss_pct` | 0.05 (5%) | 最大日亏损百分比 |
| `var_confidence` | 0.95 (95%) | VaR置信水平 |

## API Reference / API参考

### RiskManager Class

#### `__init__(max_position_pct, max_sector_pct, max_drawdown_pct, max_daily_loss_pct, var_confidence, logger)`
Initialize the Risk Manager with custom thresholds.

#### `check_position_risk(portfolio, new_trade, sector_map=None) -> Dict`
Check if a new trade would violate risk limits.

**Returns:**
- `passed` (bool): Whether the trade passed all checks
- `risk_score` (float): Numerical risk score
- `warnings` (list): List of warning messages
- `violations` (list): List of violation messages
- `suggested_adjustments` (dict): Suggested parameter adjustments

#### `calculate_var(returns, portfolio_value, confidence=None) -> float`
Calculate Value at Risk using historical simulation.

**Parameters:**
- `returns` (pd.Series): Historical returns
- `portfolio_value` (float): Current portfolio value
- `confidence` (float, optional): Confidence level (default: self.var_confidence)

**Returns:** VaR value in currency units

#### `calculate_max_drawdown(returns) -> float`
Calculate maximum drawdown from returns series.

**Parameters:**
- `returns` (pd.Series): Returns series

**Returns:** Maximum drawdown as percentage (0-1)

#### `check_concentration_risk(portfolio, sector_map) -> Dict`
Check concentration risk in portfolio.

**Returns:**
- `max_position_pct` (float): Largest position percentage
- `top_5_concentration` (float): Sum of top 5 positions
- `sector_concentration` (dict): Sector exposure percentages
- `risk_level` (str): 'low', 'medium', or 'high'

#### `generate_risk_alert(portfolio, returns, sector_map=None) -> Optional[Dict]`
Generate risk alert if thresholds are exceeded.

**Returns:** Risk alert dictionary or None if no issues

#### `suggest_risk_mitigation(alert) -> List[str]`
Suggest risk mitigation actions based on alert.

**Returns:** List of suggested actions

#### `track_portfolio_value(portfolio_id, value, timestamp=None)`
Track portfolio value for drawdown calculation.

#### `get_portfolio_drawdown(portfolio_id) -> float`
Get current drawdown for a portfolio.

#### `reset_portfolio_history(portfolio_id)`
Reset portfolio history for a given portfolio.

## Best Practices / 最佳实践

### 1. Regular Risk Monitoring / 定期风险监控
```python
# Check risk before every trade
result = risk_manager.check_position_risk(portfolio, trade, sector_map)
if not result['passed']:
    # Handle violations
    pass
```

### 2. Portfolio Value Tracking / 投资组合价值跟踪
```python
# Track portfolio value daily
risk_manager.track_portfolio_value(portfolio_id, portfolio.total_value)

# Check drawdown regularly
current_dd = risk_manager.get_portfolio_drawdown(portfolio_id)
if current_dd > risk_manager.max_drawdown_pct:
    # Take action
    pass
```

### 3. Alert Handling / 预警处理
```python
# Generate and handle alerts
alert = risk_manager.generate_risk_alert(portfolio, returns, sector_map)
if alert and alert['severity'] == 'critical':
    # Immediate action required
    suggestions = risk_manager.suggest_risk_mitigation(alert)
    # Implement suggestions
```

### 4. Sector Mapping / 行业映射
```python
# Maintain accurate sector mapping
sector_map = {
    "AAPL": "Technology",
    "GOOGL": "Technology",
    # ... more mappings
}

# Update regularly as portfolio changes
```

## Examples / 示例

See `examples/demo_risk_manager.py` for complete usage examples.

查看 `examples/demo_risk_manager.py` 获取完整使用示例。

## Testing / 测试

Run unit tests:
```bash
pytest tests/unit/test_risk_manager.py -v
```

## Related Documentation / 相关文档

- [Portfolio Manager](portfolio_manager.md)
- [Trading Models](../src/models/trading_models.py)
- [User Guide](user_guide.md)

## Support / 支持

For issues or questions, please refer to the main project documentation or create an issue in the project repository.

如有问题，请参考主项目文档或在项目仓库中创建issue。
