# 报告生成器文档 / Report Generator Documentation

## 概述 / Overview

ReportGenerator是一个用于生成各种类型报告的模块，支持训练报告、回测报告、模拟交易报告、实盘交易报告、HTML报告和对比报告。

ReportGenerator is a module for generating various types of reports, supporting training reports, backtest reports, simulation trading reports, live trading reports, HTML reports, and comparison reports.

## 功能特性 / Features

- ✅ **训练报告生成** / Training Report Generation - 生成模型训练结果报告
- ✅ **回测报告生成** / Backtest Report Generation - 生成历史回测结果报告
- ✅ **模拟交易报告** / Simulation Trading Report - 生成模拟交易测试报告
- ✅ **实盘交易报告** / Live Trading Report - 生成实盘交易状态报告
- ✅ **HTML报告** / HTML Report - 生成美观的HTML格式报告
- ✅ **对比报告** / Comparison Report - 生成多策略对比报告
- ✅ **中英双语** / Bilingual - 所有报告支持中英双语显示
- ✅ **自动保存** / Auto Save - 自动保存报告到文件

## 安装 / Installation

ReportGenerator是项目的一部分，无需单独安装。

ReportGenerator is part of the project and does not require separate installation.

## 快速开始 / Quick Start

### 1. 导入模块 / Import Module

```python
from src.application.report_generator import (
    ReportGenerator,
    TrainingResult,
    BacktestResult,
    SimulationReport,
    TradingSession
)
```

### 2. 创建报告生成器 / Create Report Generator

```python
# 创建报告生成器，指定输出目录
# Create report generator with output directory
generator = ReportGenerator(output_dir="./outputs/reports")
```

### 3. 生成训练报告 / Generate Training Report

```python
# 准备训练结果数据
# Prepare training result data
training_result = TrainingResult(
    model_id="lgbm_model_20240101",
    metrics={
        "train_accuracy": 0.68,
        "val_accuracy": 0.65,
        "train_ic": 0.08,
        "val_ic": 0.075
    },
    training_time=125.5,
    model_path="./outputs/models/lgbm_model_20240101/model.pkl",
    experiment_id="exp_001",
    run_id="run_001"
)

# 生成报告
# Generate report
report = generator.generate_training_report(training_result)
print(report)
```

### 4. 生成回测报告 / Generate Backtest Report

```python
import pandas as pd
import numpy as np

# 准备回测结果数据
# Prepare backtest result data
dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
returns = pd.Series(np.random.normal(0.001, 0.02, len(dates)), index=dates)

backtest_result = BacktestResult(
    returns=returns,
    positions=pd.DataFrame(),
    metrics={
        "total_return": 0.35,
        "annual_return": 0.23,
        "sharpe_ratio": 0.71,
        "max_drawdown": -0.24,
        "win_rate": 0.51
    },
    trades=[]
)

# 生成报告
# Generate report
report = generator.generate_backtest_report(backtest_result)
print(report)
```

### 5. 生成HTML报告 / Generate HTML Report

```python
# 生成HTML格式的回测报告
# Generate HTML format backtest report
output_path = "./outputs/reports/backtest_report.html"
generator.generate_html_report(backtest_result, output_path)
```

### 6. 生成对比报告 / Generate Comparison Report

```python
# 准备多个回测结果
# Prepare multiple backtest results
results = [result1, result2, result3]

# 生成对比报告
# Generate comparison report
report = generator.generate_comparison_report(results)
print(report)
```

## API参考 / API Reference

### ReportGenerator

#### 构造函数 / Constructor

```python
ReportGenerator(output_dir: str = "./outputs/reports")
```

**参数 / Parameters:**
- `output_dir`: 报告输出目录 / Report output directory

#### 方法 / Methods

##### generate_training_report

生成训练报告 / Generate training report

```python
def generate_training_report(self, result: TrainingResult) -> str
```

**参数 / Parameters:**
- `result`: 训练结果对象 / Training result object

**返回 / Returns:**
- `str`: 报告文本 / Report text

##### generate_backtest_report

生成回测报告 / Generate backtest report

```python
def generate_backtest_report(self, result: BacktestResult) -> str
```

**参数 / Parameters:**
- `result`: 回测结果对象 / Backtest result object

**返回 / Returns:**
- `str`: 报告文本 / Report text

##### generate_simulation_report

生成模拟交易报告 / Generate simulation trading report

```python
def generate_simulation_report(self, result: SimulationReport) -> str
```

**参数 / Parameters:**
- `result`: 模拟交易报告对象 / Simulation report object

**返回 / Returns:**
- `str`: 报告文本 / Report text

##### generate_live_trading_report

生成实盘交易报告 / Generate live trading report

```python
def generate_live_trading_report(self, session: TradingSession) -> str
```

**参数 / Parameters:**
- `session`: 交易会话对象 / Trading session object

**返回 / Returns:**
- `str`: 报告文本 / Report text

##### generate_html_report

生成HTML报告 / Generate HTML report

```python
def generate_html_report(
    self,
    result: BacktestResult,
    output_path: str,
    chart_paths: Optional[Dict[str, str]] = None
) -> None
```

**参数 / Parameters:**
- `result`: 回测结果对象 / Backtest result object
- `output_path`: HTML文件输出路径 / HTML file output path
- `chart_paths`: 图表路径字典（可选）/ Chart paths dictionary (optional)

##### generate_comparison_report

生成对比报告 / Generate comparison report

```python
def generate_comparison_report(self, results: List[BacktestResult]) -> str
```

**参数 / Parameters:**
- `results`: 回测结果列表 / Backtest results list

**返回 / Returns:**
- `str`: 报告文本 / Report text

## 数据模型 / Data Models

### TrainingResult

训练结果数据模型 / Training result data model

```python
@dataclass
class TrainingResult:
    model_id: str                    # 模型ID / Model ID
    metrics: Dict[str, float]        # 评估指标 / Evaluation metrics
    training_time: float             # 训练时长（秒）/ Training time (seconds)
    model_path: str                  # 模型保存路径 / Model save path
    experiment_id: str               # 实验ID / Experiment ID
    run_id: str                      # 运行ID / Run ID
```

### BacktestResult

回测结果数据模型 / Backtest result data model

```python
@dataclass
class BacktestResult:
    returns: pd.Series                          # 收益率序列 / Returns series
    positions: pd.DataFrame                     # 持仓数据 / Position data
    metrics: Dict[str, float]                   # 性能指标 / Performance metrics
    trades: List[Any]                           # 交易记录列表 / Trade records list
    benchmark_returns: Optional[pd.Series]      # 基准收益率 / Benchmark returns
```

### SimulationReport

模拟交易报告数据模型 / Simulation trading report data model

```python
@dataclass
class SimulationReport:
    session_id: str                  # 会话ID / Session ID
    total_return: float              # 总收益率 / Total return
    annual_return: float             # 年化收益率 / Annual return
    sharpe_ratio: float              # 夏普比率 / Sharpe ratio
    max_drawdown: float              # 最大回撤 / Max drawdown
    win_rate: float                  # 胜率 / Win rate
    total_trades: int                # 总交易次数 / Total trades
    profitable_trades: int           # 盈利交易次数 / Profitable trades
    final_portfolio_value: float     # 最终组合价值 / Final portfolio value
    daily_returns: pd.Series         # 日收益率 / Daily returns
    trade_history: List[Any]         # 交易历史 / Trade history
```

### TradingSession

交易会话数据模型 / Trading session data model

```python
@dataclass
class TradingSession:
    session_id: str                  # 会话ID / Session ID
    model_id: str                    # 模型ID / Model ID
    start_date: str                  # 开始日期 / Start date
    initial_capital: float           # 初始资金 / Initial capital
    current_capital: float           # 当前资金 / Current capital
    status: str                      # 状态 / Status
    portfolio: Dict[str, Any]        # 投资组合 / Portfolio
    total_return: float              # 总收益率 / Total return
    config: Dict[str, Any]           # 配置 / Configuration
```

## 报告格式 / Report Format

### 文本报告 / Text Report

所有文本报告都采用统一的格式：

All text reports use a unified format:

```
================================================================================
                             报告标题 / Report Title                             
================================================================================

【章节标题 / Section Title】
内容 / Content
...

================================================================================
```

### HTML报告 / HTML Report

HTML报告采用响应式设计，包含：

HTML reports use responsive design and include:

- 美观的渐变色背景 / Beautiful gradient background
- 卡片式指标展示 / Card-style metrics display
- 图表嵌入支持 / Chart embedding support
- 移动端适配 / Mobile adaptation

## 示例 / Examples

完整的示例代码请参考：

For complete example code, please refer to:

```
examples/demo_report_generator.py
```

运行示例 / Run example:

```bash
python examples/demo_report_generator.py
```

## 注意事项 / Notes

1. **输出目录** / Output Directory
   - 报告会自动保存到指定的输出目录
   - Reports are automatically saved to the specified output directory
   - 如果目录不存在，会自动创建
   - If the directory does not exist, it will be created automatically

2. **文件命名** / File Naming
   - 报告文件名包含时间戳，避免覆盖
   - Report filenames include timestamps to avoid overwriting
   - 格式：`{report_id}_{timestamp}.txt`
   - Format: `{report_id}_{timestamp}.txt`

3. **HTML报告** / HTML Report
   - HTML报告需要指定完整的输出路径
   - HTML reports require a complete output path
   - 支持嵌入图表（需要提供图表路径）
   - Supports embedded charts (chart paths required)

4. **错误处理** / Error Handling
   - 所有方法都会抛出`ReportGeneratorError`异常
   - All methods throw `ReportGeneratorError` exceptions
   - 建议使用try-except捕获异常
   - Recommended to use try-except to catch exceptions

## 集成 / Integration

ReportGenerator可以与其他模块集成使用：

ReportGenerator can be integrated with other modules:

### 与VisualizationManager集成 / Integration with VisualizationManager

```python
from src.application.visualization_manager import VisualizationManager
from src.application.report_generator import ReportGenerator

# 创建可视化管理器
# Create visualization manager
viz_manager = VisualizationManager()

# 生成图表
# Generate charts
chart_paths = viz_manager.create_report_with_charts(
    returns=returns,
    portfolio=portfolio,
    sector_weights=sector_weights,
    benchmark=benchmark
)

# 创建报告生成器
# Create report generator
report_generator = ReportGenerator()

# 生成HTML报告（包含图表）
# Generate HTML report (with charts)
report_generator.generate_html_report(
    result=backtest_result,
    output_path="./outputs/reports/backtest_report.html",
    chart_paths=chart_paths
)
```

## 更新日志 / Changelog

### v1.0.0 (2024-12-04)

- ✅ 初始版本发布 / Initial release
- ✅ 支持训练报告生成 / Support training report generation
- ✅ 支持回测报告生成 / Support backtest report generation
- ✅ 支持模拟交易报告 / Support simulation trading report
- ✅ 支持实盘交易报告 / Support live trading report
- ✅ 支持HTML报告生成 / Support HTML report generation
- ✅ 支持对比报告生成 / Support comparison report generation
- ✅ 中英双语支持 / Bilingual support

## 许可证 / License

本项目采用MIT许可证 / This project is licensed under the MIT License

## 联系方式 / Contact

如有问题或建议，请提交Issue / For questions or suggestions, please submit an Issue
