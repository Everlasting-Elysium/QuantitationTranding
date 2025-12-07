# Performance Analyzer Documentation
# 表现分析器文档

## Overview / 概述

The Performance Analyzer is a component of the qlib trading system that analyzes historical performance of assets and generates recommendations based on multiple metrics.

表现分析器是qlib交易系统的一个组件，用于分析资产的历史表现并基于多个指标生成推荐。

## Features / 功能

- **Historical Performance Analysis / 历史表现分析**: Analyze asset performance over specified time periods (default: 3 years)
- **Key Metrics Calculation / 关键指标计算**: Calculate returns, Sharpe ratio, maximum drawdown, volatility, and win rate
- **Asset Ranking / 资产排名**: Rank assets based on综合评分 combining multiple metrics
- **Recommendations / 推荐**: Generate top performer recommendations with detailed reasons

## Key Metrics / 关键指标

### 1. Annual Return / 年化收益率
The annualized rate of return over the analysis period.
分析期间的年化收益率。

**Formula / 公式**: `(1 + total_return) ^ (1 / years) - 1`

### 2. Sharpe Ratio / 夏普比率
Risk-adjusted return metric that measures excess return per unit of risk.
衡量每单位风险的超额收益的风险调整后收益指标。

**Formula / 公式**: `(annual_return - risk_free_rate) / volatility`

**Interpretation / 解释**:
- `> 1.5`: Excellent / 优秀
- `> 1.0`: Good / 良好
- `> 0.5`: Acceptable / 可接受
- `< 0.5`: Poor / 较差

### 3. Maximum Drawdown / 最大回撤
The largest peak-to-trough decline in portfolio value.
投资组合价值从峰值到谷底的最大跌幅。

**Interpretation / 解释**:
- `> -15%`: Excellent control / 控制优秀
- `> -25%`: Good control / 控制良好
- `> -35%`: Acceptable / 可接受
- `< -35%`: High risk / 高风险

### 4. Volatility / 波动率
Standard deviation of returns, annualized.
收益率的标准差，年化。

### 5. Win Rate / 胜率
Percentage of periods with positive returns.
正收益期间的百分比。

## Performance Score / 综合评分

The performance score (0-100) is calculated as a weighted combination of metrics:
综合评分（0-100）是指标的加权组合：

- **Sharpe Ratio / 夏普比率**: 40 points (max)
- **Annual Return / 年化收益率**: 40 points (max)
- **Max Drawdown / 最大回撤**: 20 points (max)

## Usage / 使用方法

### Basic Usage / 基本使用

```python
from src.application.performance_analyzer import PerformanceAnalyzer
from src.infrastructure.qlib_wrapper import QlibWrapper

# Initialize
qlib_wrapper = QlibWrapper()
qlib_wrapper.init(provider_uri="data/cn_data", region="cn")

analyzer = PerformanceAnalyzer(qlib_wrapper=qlib_wrapper)

# Analyze historical performance
report = analyzer.analyze_historical_performance(
    market="CN",
    asset_type="stock",
    lookback_years=3,
    instruments="csi300"
)

# Get recommendations
recommendations = analyzer.recommend_top_performers(
    market="CN",
    asset_type="stock",
    top_n=10,
    criteria="sharpe_ratio"
)

# Get metrics for specific asset
metrics = analyzer.get_asset_metrics(
    asset_code="SH600000",
    start_date="2021-01-01",
    end_date="2024-01-01"
)
```

### Setting Risk-Free Rate / 设置无风险利率

```python
# Set custom risk-free rate (default is 3%)
analyzer.set_risk_free_rate(0.025)  # 2.5%
```

## API Reference / API参考

### PerformanceAnalyzer Class

#### `__init__(qlib_wrapper: Optional[QlibWrapper] = None)`

Initialize the performance analyzer.
初始化表现分析器。

**Parameters / 参数**:
- `qlib_wrapper`: QlibWrapper instance for data access / 用于数据访问的QlibWrapper实例

#### `analyze_historical_performance(market, asset_type, lookback_years=3, instruments=None)`

Analyze historical performance of assets.
分析资产的历史表现。

**Parameters / 参数**:
- `market`: Market code (e.g., "CN", "US") / 市场代码
- `asset_type`: Asset type code (e.g., "stock", "fund") / 资产类型代码
- `lookback_years`: Number of years to analyze (default: 3) / 分析年数（默认：3）
- `instruments`: Instrument pool (e.g., "csi300") / 工具池

**Returns / 返回**: `PerformanceReport` object / PerformanceReport对象

#### `recommend_top_performers(market, asset_type, top_n=10, criteria="sharpe_ratio", lookback_years=3)`

Generate top performer recommendations.
生成顶级表现者推荐。

**Parameters / 参数**:
- `market`: Market code / 市场代码
- `asset_type`: Asset type code / 资产类型代码
- `top_n`: Number of recommendations (default: 10) / 推荐数量（默认：10）
- `criteria`: Ranking criteria (default: "sharpe_ratio") / 排名标准（默认："sharpe_ratio"）
- `lookback_years`: Analysis period in years (default: 3) / 分析年数（默认：3）

**Returns / 返回**: List of `AssetRecommendation` objects / AssetRecommendation对象列表

#### `get_asset_metrics(asset_code, start_date, end_date)`

Calculate performance metrics for a single asset.
计算单个资产的表现指标。

**Parameters / 参数**:
- `asset_code`: Asset symbol/code / 资产代码
- `start_date`: Start date (YYYY-MM-DD) / 开始日期
- `end_date`: End date (YYYY-MM-DD) / 结束日期

**Returns / 返回**: `AssetMetrics` object or None / AssetMetrics对象或None

#### `set_risk_free_rate(rate)`

Set the risk-free rate for Sharpe ratio calculation.
设置用于夏普比率计算的无风险利率。

**Parameters / 参数**:
- `rate`: Annual risk-free rate (e.g., 0.03 for 3%) / 年化无风险利率

## Data Models / 数据模型

### AssetMetrics

```python
@dataclass
class AssetMetrics:
    symbol: str                 # Asset code / 资产代码
    period_start: str          # Analysis start date / 分析开始日期
    period_end: str            # Analysis end date / 分析结束日期
    total_return: float        # Total return / 总收益率
    annual_return: float       # Annualized return / 年化收益率
    volatility: float          # Volatility / 波动率
    sharpe_ratio: float        # Sharpe ratio / 夏普比率
    max_drawdown: float        # Maximum drawdown / 最大回撤
    win_rate: float            # Win rate / 胜率
```

### AssetRecommendation

```python
@dataclass
class AssetRecommendation:
    symbol: str                    # Asset code / 资产代码
    name: str                      # Asset name / 资产名称
    asset_type: str                # Asset type / 资产类型
    performance_score: float       # Performance score (0-100) / 综合评分
    sharpe_ratio: float            # Sharpe ratio / 夏普比率
    annual_return: float           # Annual return / 年化收益率
    max_drawdown: float            # Max drawdown / 最大回撤
    recommendation_reason: str     # Recommendation reason / 推荐理由
    rank: int                      # Ranking position / 排名
```

### PerformanceReport

```python
@dataclass
class PerformanceReport:
    market: str                           # Market code / 市场代码
    asset_type: str                       # Asset type / 资产类型
    analysis_period_start: str            # Period start / 期间开始
    analysis_period_end: str              # Period end / 期间结束
    total_assets_analyzed: int            # Total assets / 资产总数
    top_performers: List[AssetRecommendation]  # Top performers / 顶级表现者
    average_return: float                 # Average return / 平均收益率
    average_sharpe: float                 # Average Sharpe / 平均夏普比率
    average_drawdown: float               # Average drawdown / 平均回撤
    analysis_timestamp: str               # Analysis time / 分析时间
```

## Examples / 示例

### Example 1: Analyze CSI 300 Stocks / 分析沪深300股票

```python
analyzer = PerformanceAnalyzer(qlib_wrapper)

report = analyzer.analyze_historical_performance(
    market="CN",
    asset_type="stock",
    lookback_years=3,
    instruments="csi300"
)

print(f"Analyzed {report.total_assets_analyzed} stocks")
print(f"Average annual return: {report.average_return:.2%}")
print(f"Top performer: {report.top_performers[0].symbol}")
```

### Example 2: Get Top 5 by Sharpe Ratio / 获取夏普比率前5名

```python
recommendations = analyzer.recommend_top_performers(
    market="CN",
    asset_type="stock",
    top_n=5,
    criteria="sharpe_ratio"
)

for rec in recommendations:
    print(f"{rec.rank}. {rec.symbol}: Sharpe={rec.sharpe_ratio:.2f}")
```

### Example 3: Compare Multiple Assets / 比较多个资产

```python
assets = ["SH600000", "SH600036", "SH600519"]
start_date = "2021-01-01"
end_date = "2024-01-01"

for asset in assets:
    metrics = analyzer.get_asset_metrics(asset, start_date, end_date)
    if metrics:
        print(f"{asset}: Return={metrics.annual_return:.2%}, "
              f"Sharpe={metrics.sharpe_ratio:.2f}")
```

## Error Handling / 错误处理

The Performance Analyzer uses the system's error handling framework and raises `DataError` exceptions with detailed error information.

表现分析器使用系统的错误处理框架，并抛出包含详细错误信息的`DataError`异常。

Common errors / 常见错误:
- `PERF0001`: No assets found for analysis / 未找到可分析的资产
- `PERF0002`: No assets successfully analyzed / 没有成功分析的资产
- `PERF0003`: Historical performance analysis failed / 历史表现分析失败
- `PERF0004`: Failed to generate recommendations / 生成推荐失败

## Best Practices / 最佳实践

1. **Data Quality / 数据质量**: Ensure sufficient historical data is available (at least 1 year recommended)
   确保有足够的历史数据（建议至少1年）

2. **Analysis Period / 分析期间**: Use 3-5 years for stable results
   使用3-5年以获得稳定结果

3. **Risk-Free Rate / 无风险利率**: Adjust based on current market conditions
   根据当前市场条件调整

4. **Instrument Pool / 工具池**: Start with well-known indices (e.g., CSI 300, S&P 500)
   从知名指数开始（例如，沪深300、标普500）

5. **Interpretation / 解释**: Consider multiple metrics together, not just one
   综合考虑多个指标，而不仅仅是一个

## Integration / 集成

The Performance Analyzer integrates with:
表现分析器与以下组件集成：

- **QlibWrapper**: For data access / 用于数据访问
- **MarketSelector**: For market and asset type selection / 用于市场和资产类型选择
- **LoggerSystem**: For logging / 用于日志记录
- **Error Handler**: For error management / 用于错误管理

## See Also / 另请参阅

- [Market Selector Documentation](market_selector.md)
- [Qlib Wrapper Documentation](qlib_wrapper_implementation.md)
- [User Guide](user_guide.md)
