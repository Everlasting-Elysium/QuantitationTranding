# 回测功能CLI使用指南 / Backtest CLI Usage Guide

## 概述 / Overview

回测功能CLI提供了一个交互式界面，用于对训练好的模型进行历史回测。通过回测，您可以评估模型在历史数据上的表现，验证策略的有效性。

The Backtest CLI provides an interactive interface for backtesting trained models on historical data. Through backtesting, you can evaluate model performance on historical data and validate strategy effectiveness.

## 功能特性 / Features

### 1. 模型选择 / Model Selection
- 自动列出所有已注册的模型 / Automatically list all registered models
- 显示模型详细信息（类型、训练日期、性能指标）/ Display model details (type, training date, performance metrics)
- 支持按状态筛选模型 / Support filtering models by status

### 2. 回测参数配置 / Backtest Parameter Configuration
- **时间段配置** / Time Period Configuration
  - 自定义回测开始和结束日期 / Custom backtest start and end dates
  - 支持任意历史时间段 / Support any historical time period

- **股票池选择** / Stock Pool Selection
  - 沪深300 (csi300)
  - 中证500 (csi500)
  - 中证800 (csi800)
  - 自定义股票池 / Custom stock pool

- **策略参数** / Strategy Parameters
  - topk: 持仓股票数量 / Number of stocks to hold
  - n_drop: 每次调仓卖出数量 / Number of stocks to drop per rebalance

- **基准指数** / Benchmark Index
  - 沪深300指数 (SH000300)
  - 中证500指数 (SH000905)
  - 中证1000指数 (SH000852)
  - 自定义基准 / Custom benchmark

### 3. 回测执行 / Backtest Execution
- 加载选定的模型 / Load selected model
- 生成预测信号 / Generate prediction signals
- 模拟交易执行 / Simulate trade execution
- 计算性能指标 / Calculate performance metrics
- 实时显示进度 / Real-time progress display

### 4. 结果展示 / Result Display
- **收益指标** / Return Metrics
  - 总收益率 / Total return
  - 年化收益率 / Annual return

- **风险指标** / Risk Metrics
  - 波动率 / Volatility
  - 最大回撤 / Max drawdown

- **风险调整收益** / Risk-Adjusted Returns
  - 夏普比率 / Sharpe ratio

- **交易统计** / Trading Statistics
  - 胜率 / Win rate
  - 交易次数 / Trade count

- **基准对比** / Benchmark Comparison
  - 基准收益率 / Benchmark return
  - 超额收益 / Excess return
  - 信息比率 / Information ratio

### 5. 结果保存 / Result Saving
回测结果自动保存到 `outputs/backtests/` 目录，包括：
Backtest results are automatically saved to `outputs/backtests/` directory, including:

- `metrics.json` - 性能指标 / Performance metrics
- `returns.csv` - 收益率序列 / Returns series
- `positions.csv` - 持仓数据 / Position data
- `trades.csv` - 交易记录 / Trade records
- `benchmark_returns.csv` - 基准收益率 / Benchmark returns
- `config.json` - 回测配置 / Backtest configuration

## 使用流程 / Usage Workflow

### 步骤 1: 启动系统 / Step 1: Start System

```bash
python main.py
```

### 步骤 2: 选择回测功能 / Step 2: Select Backtest Feature

在主菜单中选择选项 2：
Select option 2 in the main menu:

```
请选择功能 / Please select an option: 2
```

### 步骤 3: 选择回测操作 / Step 3: Select Backtest Operation

```
请选择回测操作 / Please select backtest operation:
  1. 运行新回测 / Run new backtest
  2. 查看回测结果 / View backtest results
  3. 返回主菜单 / Return to main menu
```

选择 "1. 运行新回测" / Select "1. Run new backtest"

### 步骤 4: 选择模型 / Step 4: Select Model

系统会列出所有可用模型：
System will list all available models:

```
可用的模型 / Available Models:
----------------------------------------------------------------------

1. lgbm_model (v1.0)
   模型ID / Model ID: lgbm_model_v1.0
   模型类型 / Model Type: LGBMModel
   训练日期 / Training Date: 2024-01-15
   状态 / Status: registered
   性能指标 / Performance Metrics:
     - ic_mean: 0.0523
     - icir: 1.2345
     - rank_ic: 0.0612

2. linear_model (v1.0)
   模型ID / Model ID: linear_model_v1.0
   模型类型 / Model Type: LinearModel
   训练日期 / Training Date: 2024-01-14
   状态 / Status: candidate
   性能指标 / Performance Metrics:
     - ic_mean: 0.0489
     - icir: 1.1234
     - rank_ic: 0.0578
----------------------------------------------------------------------

请选择要回测的模型 / Please select a model for backtest:
```

### 步骤 5: 配置回测参数 / Step 5: Configure Backtest Parameters

#### 5.1 设置回测时间段 / Set Backtest Period

```
回测时间段配置 / Backtest Period Configuration:
请输入回测开始日期 / Please enter backtest start date (格式: %Y-%m-%d) [默认: 2023-01-01]: 
请输入回测结束日期 / Please enter backtest end date (格式: %Y-%m-%d) [默认: 2023-12-31]: 
```

#### 5.2 选择股票池 / Select Stock Pool

```
股票池配置 / Stock Pool Configuration:
请选择股票池 / Please select stock pool:
  1. csi300 (沪深300)
  2. csi500 (中证500)
  3. csi800 (中证800)
  4. 自定义 / Custom
```

#### 5.3 配置策略参数 / Configure Strategy Parameters

```
策略参数配置 / Strategy Parameters Configuration:
请输入持仓股票数量 (topk) / Please enter number of stocks to hold (topk): 50
请输入每次调仓卖出数量 (n_drop) / Please enter number of stocks to drop per rebalance (n_drop): 5
```

#### 5.4 选择基准指数 / Select Benchmark Index

```
基准指数配置 / Benchmark Index Configuration:
是否使用基准指数进行对比？ / Use benchmark index for comparison? (是/否) [默认: 是]: 

请选择基准指数 / Please select benchmark index:
  1. SH000300 (沪深300指数)
  2. SH000905 (中证500指数)
  3. SH000852 (中证1000指数)
  4. 自定义 / Custom
```

### 步骤 6: 确认配置 / Step 6: Confirm Configuration

系统会显示配置总结：
System will display configuration summary:

```
======================================================================
📝 回测配置确认 / Backtest Configuration Confirmation
======================================================================
模型 / Model: lgbm_model (v1.0)
模型ID / Model ID: lgbm_model_v1.0
回测时间段 / Backtest Period: 2023-01-01 至 / to 2023-12-31
股票池 / Stock Pool: csi300
持仓数量 / Position Size: 50
调仓卖出数量 / Rebalance Drop: 5
基准指数 / Benchmark: SH000300
======================================================================

确认开始回测？ / Confirm to start backtest? (是/否) [默认: 是]: 
```

### 步骤 7: 执行回测 / Step 7: Execute Backtest

确认后，系统开始执行回测：
After confirmation, system starts backtest execution:

```
======================================================================
🚀 开始执行回测 / Starting Backtest Execution
======================================================================

⏳ 回测进行中，请稍候... / Backtest in progress, please wait...
   这可能需要几分钟时间 / This may take several minutes
```

### 步骤 8: 查看结果 / Step 8: View Results

回测完成后，系统显示结果：
After backtest completion, system displays results:

```
======================================================================
✅ 回测完成！ / Backtest Completed!
======================================================================

性能指标 / Performance Metrics:
----------------------------------------------------------------------
  总收益率 / Total Return: 28.50%
  年化收益率 / Annual Return: 28.50%
  波动率 / Volatility: 18.20%
  最大回撤 / Max Drawdown: -12.30%
  夏普比率 / Sharpe Ratio: 1.5659
  胜率 / Win Rate: 62.50%

  基准收益率 / Benchmark Return: 15.20%
  超额收益 / Excess Return: 13.30%
  信息比率 / Information Ratio: 0.8234

  回测时长 / Backtest Time: 45.23 秒 / seconds
----------------------------------------------------------------------

交易统计 / Trade Statistics:
  总交易次数 / Total Trades: 156

======================================================================
💡 提示 / Tips:
  • 回测结果已保存到 outputs/backtests/ 目录
    Backtest results saved to outputs/backtests/ directory
  • 可以在主菜单选择 '报告查看' 查看详细报告
    You can select 'View Reports' in main menu for detailed reports
======================================================================
```

## 最佳实践 / Best Practices

### 1. 选择合适的回测时间段 / Choose Appropriate Backtest Period
- 建议至少使用1年的历史数据 / Recommend at least 1 year of historical data
- 包含不同市场环境（牛市、熊市、震荡市）/ Include different market conditions (bull, bear, sideways)
- 避免过短的回测期导致结果不可靠 / Avoid too short backtest period leading to unreliable results

### 2. 合理设置策略参数 / Set Strategy Parameters Reasonably
- topk不宜过大或过小 / topk should not be too large or too small
  - 过大：分散度高但单只股票收益贡献小 / Too large: high diversification but low contribution per stock
  - 过小：集中度高但风险大 / Too small: high concentration but high risk
- n_drop应小于topk / n_drop should be less than topk
  - 建议n_drop = topk * 0.1 ~ 0.2 / Recommend n_drop = topk * 0.1 ~ 0.2

### 3. 使用基准对比 / Use Benchmark Comparison
- 始终使用基准指数进行对比 / Always use benchmark index for comparison
- 选择与股票池匹配的基准 / Choose benchmark matching the stock pool
  - csi300 → SH000300
  - csi500 → SH000905
  - csi800 → SH000300 或 SH000905

### 4. 关注关键指标 / Focus on Key Metrics
- **收益指标** / Return Metrics
  - 年化收益率应显著高于基准 / Annual return should be significantly higher than benchmark
  - 超额收益应为正值 / Excess return should be positive

- **风险指标** / Risk Metrics
  - 最大回撤应控制在可接受范围内 / Max drawdown should be within acceptable range
  - 波动率不应过高 / Volatility should not be too high

- **风险调整收益** / Risk-Adjusted Returns
  - 夏普比率 > 1.0 表示较好的风险调整收益 / Sharpe ratio > 1.0 indicates good risk-adjusted returns
  - 信息比率 > 0.5 表示相对基准有较好的超额收益 / Information ratio > 0.5 indicates good excess returns relative to benchmark

### 5. 结果分析 / Result Analysis
- 对比训练指标和回测指标 / Compare training metrics and backtest metrics
  - 如果回测表现远低于训练表现，可能存在过拟合 / If backtest performance is much lower than training, overfitting may exist
  - 如果两者接近，说明模型泛化能力好 / If they are close, model has good generalization

- 分析交易统计 / Analyze trading statistics
  - 胜率应 > 50% / Win rate should be > 50%
  - 交易次数不应过多（避免过度交易）/ Trade count should not be too high (avoid overtrading)

## 常见问题 / FAQ

### Q1: 回测时间过长怎么办？ / What if backtest takes too long?
A: 可以尝试：
   - 缩短回测时间段 / Shorten backtest period
   - 减少股票池大小 / Reduce stock pool size
   - 使用更简单的模型 / Use simpler model

### Q2: 回测结果与训练结果差异很大？ / Large difference between backtest and training results?
A: 可能的原因：
   - 模型过拟合 / Model overfitting
   - 训练数据和回测数据分布不同 / Different distribution between training and backtest data
   - 策略参数设置不当 / Improper strategy parameter settings

   解决方法：
   - 增加训练数据的多样性 / Increase diversity of training data
   - 使用正则化技术 / Use regularization techniques
   - 调整策略参数 / Adjust strategy parameters

### Q3: 如何选择合适的基准指数？ / How to choose appropriate benchmark index?
A: 基准应与股票池匹配：
   - csi300 股票池 → SH000300 (沪深300指数)
   - csi500 股票池 → SH000905 (中证500指数)
   - csi800 股票池 → SH000300 或 SH000905

### Q4: 回测结果保存在哪里？ / Where are backtest results saved?
A: 回测结果保存在 `outputs/backtests/` 目录下，每次回测会创建一个新的子目录，包含：
   - metrics.json - 性能指标
   - returns.csv - 收益率序列
   - positions.csv - 持仓数据
   - trades.csv - 交易记录
   - benchmark_returns.csv - 基准收益率
   - config.json - 回测配置

## 与其他功能的集成 / Integration with Other Features

### 与训练功能集成 / Integration with Training
1. 使用训练功能训练模型 / Train models using training feature
2. 模型自动注册到模型注册表 / Models automatically registered to registry
3. 使用回测功能验证模型表现 / Use backtest feature to validate model performance
4. 根据回测结果调整训练参数 / Adjust training parameters based on backtest results
5. 迭代优化 / Iterative optimization

### 与模型管理集成 / Integration with Model Management
1. 回测后可以标记优秀模型 / Mark excellent models after backtest
2. 设置生产模型 / Set production model
3. 管理模型版本 / Manage model versions

### 与报告功能集成 / Integration with Reporting
1. 回测结果自动保存 / Backtest results automatically saved
2. 可以生成详细的HTML报告 / Can generate detailed HTML reports
3. 支持多模型对比分析 / Support multi-model comparison analysis

## 技术要求 / Technical Requirements

### 系统要求 / System Requirements
- Python 3.8+
- qlib 已安装并初始化 / qlib installed and initialized
- 足够的历史数据 / Sufficient historical data

### 依赖项 / Dependencies
- qlib
- pandas
- numpy
- pickle

## 相关文档 / Related Documentation

- [CLI使用指南](cli_usage.md) - CLI Usage Guide
- [回测管理器文档](backtest_manager.md) - Backtest Manager Documentation
- [模型注册表文档](model_registry.md) - Model Registry Documentation
- [训练CLI使用指南](training_cli_usage.md) - Training CLI Usage Guide

## 示例代码 / Example Code

查看以下示例代码了解更多：
See the following example code for more details:

- `examples/demo_backtest_manager.py` - 回测管理器示例 / Backtest Manager Example
- `test_backtest_cli.py` - 回测CLI测试 / Backtest CLI Test
- `demo_backtest_cli.py` - 回测CLI演示 / Backtest CLI Demo

## 支持 / Support

如有问题，请：
For questions, please:

1. 查看文档 / Check documentation
2. 运行测试脚本 / Run test scripts
3. 查看示例代码 / Check example code
4. 提交Issue / Submit an issue
