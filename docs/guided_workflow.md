# 引导式工作流程文档 / Guided Workflow Documentation

## 概述 / Overview

引导式工作流程系统提供了一个完整的、交互式的投资流程，从市场选择到实盘交易，无需编程知识。系统通过10个步骤引导用户完成整个投资决策和执行过程。

The Guided Workflow System provides a complete, interactive investment process from market selection to live trading, requiring no programming knowledge. The system guides users through the entire investment decision and execution process in 10 steps.

## 快速开始 / Quick Start

### 3步开始使用 / Get Started in 3 Steps

1. **启动主CLI / Start Main CLI**
   ```bash
   python main.py
   ```

2. **选择引导式工作流程 / Select Guided Workflow**
   ```
   请选择功能 / Please select an option: 0
   ```

3. **按照提示完成10步流程 / Follow prompts to complete 10 steps**
   - 系统会自动保存进度
   - 可随时暂停和继续
   - 支持返回修改

### 界面预览 / Interface Preview

```
================================================================================
📊 量化交易系统 - 主菜单 / Quantitative Trading System - Main Menu
================================================================================

  ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
  🎯 引导式工作流程 / Guided Workflow
  完整的投资流程引导（推荐新手使用）
  ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐

  1. 模型训练 / Model Training
  2. 历史回测 / Historical Backtest
  3. 信号生成 / Signal Generation
  ...
```

## 核心特性 / Core Features

- **10步完整流程** / **10-Step Complete Process**: 覆盖从市场选择到实盘交易的全流程
- **进度保存和恢复** / **Progress Save and Resume**: 随时暂停，下次继续
- **返回修改功能** / **Go-Back-to-Modify**: 可以返回任何步骤重新配置
- **实时验证** / **Real-time Validation**: 输入即时验证，友好的错误提示
- **配置总结** / **Configuration Summary**: 完成后生成完整的配置总结
- **中英双语界面** / **Bilingual Interface**: 完整的中英文支持
- **友好的错误提示** / **Friendly Error Messages**: 清晰的错误说明和解决建议
- **无需编程知识** / **No Programming Required**: 通过问答完成所有配置

## 工作流程步骤 / Workflow Steps

### 流程图 / Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  步骤 1: 市场和资产选择 / Market and Asset Selection        │
│  选择投资市场和资产类型                                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤 2: 智能推荐 / Intelligent Recommendation              │
│  系统分析历史数据并推荐优质标的                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤 3: 目标设定 / Target Setting                          │
│  设定期望收益率和风险偏好                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤 4: 策略优化 / Strategy Optimization                   │
│  系统优化策略参数以达到目标                                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤 5: 模型训练 / Model Training                          │
│  训练预测模型                                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤 6: 历史回测 / Historical Backtest                     │
│  使用历史数据验证模型表现                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤 7: 模拟交易 / Simulation Trading                      │
│  进行模拟交易测试                                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤 8: 实盘交易设置 / Live Trading Setup                  │
│  配置实盘交易参数和风险控制                                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤 9: 实盘交易执行 / Live Trading Execution              │
│  启动实盘交易                                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  步骤 10: 报告配置 / Reporting Configuration                │
│  配置自动报告和通知                                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    ✅ 完成 / Complete
```

## 工作流程步骤详解 / Workflow Steps Details

### 步骤 1: 市场和资产选择 / Step 1: Market and Asset Selection

选择投资市场（中国、美国、香港等）和资产类型（股票、基金、ETF等）。

Select investment market (China, US, Hong Kong, etc.) and asset type (stocks, funds, ETFs, etc.).

**输入 / Inputs:**
- 市场选择 / Market selection
- 资产类型选择 / Asset type selection

**输出 / Outputs:**
- 市场配置 / Market configuration
- 数据源配置 / Data source configuration

### 步骤 2: 智能推荐 / Step 2: Intelligent Recommendation

系统基于近3年的历史表现分析，推荐优质投资标的。

System recommends quality investment assets based on 3-year historical performance analysis.

**分析指标 / Analysis Metrics:**
- 年化收益率 / Annual return
- 夏普比率 / Sharpe ratio
- 最大回撤 / Maximum drawdown

**输入 / Inputs:**
- 选择推荐的标的 / Select recommended assets

**输出 / Outputs:**
- 选定的资产列表 / Selected asset list

### 步骤 3: 目标设定 / Step 3: Target Setting

设定投资目标和风险偏好。

Set investment targets and risk preferences.

**输入 / Inputs:**
- 期望年化收益率 (%) / Target annual return (%)
- 风险偏好（保守型/稳健型/进取型）/ Risk preference (Conservative/Moderate/Aggressive)
- 模拟交易周期（天数）/ Simulation trading period (days)

**输出 / Outputs:**
- 投资目标配置 / Investment target configuration

### 步骤 4: 策略优化 / Step 4: Strategy Optimization

系统根据目标收益率和风险偏好优化策略参数。

System optimizes strategy parameters based on target return and risk preference.

**优化内容 / Optimization Content:**
- 资产配置权重 / Asset allocation weights
- 调仓频率 / Rebalancing frequency
- 风险控制参数 / Risk control parameters

**输出 / Outputs:**
- 优化后的策略配置 / Optimized strategy configuration
- 预期收益和风险 / Expected return and risk

### 步骤 5: 模型训练 / Step 5: Model Training

使用优化的策略参数训练预测模型。

Train prediction model using optimized strategy parameters.

**训练过程 / Training Process:**
1. 数据加载 / Data loading
2. 特征工程 / Feature engineering
3. 模型训练 / Model training
4. 模型评估 / Model evaluation

**输出 / Outputs:**
- 训练好的模型 / Trained model
- 模型性能指标 / Model performance metrics

### 步骤 6: 历史回测 / Step 6: Historical Backtest

使用历史数据验证模型表现。

Validate model performance using historical data.

**回测指标 / Backtest Metrics:**
- 总收益率 / Total return
- 年化收益率 / Annual return
- 夏普比率 / Sharpe ratio
- 最大回撤 / Maximum drawdown
- 胜率 / Win rate

**输出 / Outputs:**
- 回测报告 / Backtest report
- 可视化图表 / Visualization charts

### 步骤 7: 模拟交易 / Step 7: Simulation Trading

在指定周期内进行模拟交易测试。

Conduct simulation trading test within specified period.

**输入 / Inputs:**
- 模拟初始资金 / Initial capital for simulation

**模拟内容 / Simulation Content:**
- 每日信号生成 / Daily signal generation
- 模拟订单执行 / Simulated order execution
- 持仓跟踪 / Position tracking
- 收益计算 / Return calculation

**输出 / Outputs:**
- 模拟交易报告 / Simulation trading report
- 性能指标 / Performance metrics

### 步骤 8: 实盘交易设置 / Step 8: Live Trading Setup

配置实盘交易参数和风险控制。

Configure live trading parameters and risk controls.

**输入 / Inputs:**
- 初始投资金额 / Initial investment amount
- 券商选择 / Broker selection
- 风险控制参数：
  - 单日最大亏损比例 / Max daily loss percentage
  - 单只股票最大仓位 / Max position size per stock
  - 止损线 / Stop loss threshold

**输出 / Outputs:**
- 实盘交易配置 / Live trading configuration

### 步骤 9: 实盘交易执行 / Step 9: Live Trading Execution

启动实盘交易，系统自动执行交易策略。

Start live trading, system automatically executes trading strategy.

**自动执行内容 / Automatic Execution:**
- 每日生成交易信号 / Generate daily trading signals
- 自动下单买卖 / Automatically place buy/sell orders
- 实时风险监控 / Real-time risk monitoring
- 触发止损/止盈 / Trigger stop-loss/take-profit

**输出 / Outputs:**
- 交易会话ID / Trading session ID
- 实时监控信息 / Real-time monitoring information

### 步骤 10: 报告配置 / Step 10: Reporting Configuration

配置自动报告和通知。

Configure automated reports and notifications.

**输入 / Inputs:**
- 报告频率（每日/每周/每月）/ Report frequency (daily/weekly/monthly)
- 邮箱地址 / Email address
- 风险预警开关 / Risk alert toggle

**输出 / Outputs:**
- 报告配置 / Report configuration
- 通知设置 / Notification settings

## 使用方法 / Usage

### 基本使用 / Basic Usage

```python
from cli.guided_workflow import GuidedWorkflow

# 创建工作流实例 / Create workflow instance
workflow = GuidedWorkflow()

# 启动工作流 / Start workflow
workflow.start()
```

### 从命令行运行 / Run from Command Line

```bash
# 运行演示脚本 / Run demo script
python examples/demo_guided_workflow.py

# 或直接运行模块 / Or run module directly
python -m src.cli.guided_workflow
```

### 恢复之前的进度 / Resume Previous Progress

系统会自动检测未完成的工作流程并询问是否继续：

The system automatically detects incomplete workflows and asks if you want to continue:

```python
workflow = GuidedWorkflow()
workflow.start(resume=True)  # 默认为True / Default is True
```

### 从头开始 / Start from Scratch

```python
workflow = GuidedWorkflow()
workflow.start(resume=False)  # 不恢复之前的进度 / Don't resume previous progress
```

### 从主CLI访问 / Access from Main CLI

最简单的方式是通过主CLI访问引导式工作流程：

The easiest way is to access guided workflow through the main CLI:

```bash
# 启动主CLI / Start main CLI
python main.py

# 在主菜单中选择选项 0 / Select option 0 in main menu
请选择功能 / Please select an option: 0
```

## 详细示例 / Detailed Examples

### 示例 1: 完整工作流程演示 / Example 1: Complete Workflow Demo

以下是一个完整的工作流程示例，展示了每个步骤的输入和输出：

Here is a complete workflow example showing inputs and outputs for each step:

#### 步骤 1: 市场和资产选择

```
================================================================================
步骤 1/10: 市场和资产选择 / Market and Asset Selection
================================================================================

请选择投资市场 / Please select investment market:
  1. 中国市场 (A股) / China Market (A-shares) [默认]
  2. 美国市场 / US Market
  3. 香港市场 / Hong Kong Market
请选择 (1-3) [默认: 1]: 1

请选择投资品类 / Please select asset type:
  1. 股票 / Stocks [默认]
  2. 基金 / Funds
  3. ETF / ETFs
请选择 (1-3) [默认: 1]: 1

✅ ✓ 已选择: 中国市场 (A股) / China Market (A-shares) - 股票 / Stocks
```

#### 步骤 2: 智能推荐

```
================================================================================
步骤 2/10: 智能推荐 / Intelligent Recommendation
================================================================================

正在分析近3年市场表现，为您推荐优质标的...
进度 / Progress: [████████████████████████████████████████] 100%

================================================================================
基于历史表现，为您推荐以下优质标的：
================================================================================

1. 贵州茅台 (600519)
   年化收益 / Annual Return: 25.0%
   夏普比率 / Sharpe Ratio: 1.8
   最大回撤 / Max Drawdown: -15.0%

2. 宁德时代 (300750)
   年化收益 / Annual Return: 35.0%
   夏普比率 / Sharpe Ratio: 1.5
   最大回撤 / Max Drawdown: -20.0%

3. 比亚迪 (002594)
   年化收益 / Annual Return: 40.0%
   夏普比率 / Sharpe Ratio: 1.3
   最大回撤 / Max Drawdown: -25.0%

请输入要选择的标的编号（用逗号分隔，如: 1,2,3）: 1,2,3

✅ ✓ 已选择 3 个标的: 贵州茅台, 宁德时代, 比亚迪
```

#### 步骤 3: 目标设定

```
================================================================================
步骤 3/10: 目标设定 / Target Setting
================================================================================

请输入期望年化收益率 (%) (最小: 5.0, 最大: 100.0) [默认: 20.0]: 20

请选择风险偏好 / Please select risk preference:
  1. 保守型 (低风险) / Conservative (Low Risk)
  2. 稳健型 (中等风险) / Moderate (Medium Risk) [默认]
  3. 进取型 (高风险) / Aggressive (High Risk)
请选择 (1-3) [默认: 2]: 2

请输入模拟交易周期 (天数) (最小: 7, 最大: 365) [默认: 30]: 30

✅ ✓ 目标收益率: 20.0%
✓ 风险偏好: 稳健型 (中等风险) / Moderate (Medium Risk)
✓ 模拟周期: 30天
```

### 示例 2: 进度保存和恢复 / Example 2: Progress Save and Resume

当您暂停工作流程后，下次启动时会看到：

When you pause the workflow, you'll see this on next startup:

```
检测到未完成的工作流程，是否继续？
Detected incomplete workflow, continue? (是/否) [默认: 是]: y

✅ 已恢复到步骤 4
Resumed to step 4

================================================================================
步骤 4/10: 策略优化 / Strategy Optimization
================================================================================
```

### 示例 3: 返回修改配置 / Example 3: Go Back to Modify

在任何步骤，您都可以选择返回：

At any step, you can choose to go back:

```
请选择下一步操作 / Please select next action:
  1. 继续下一步 / Continue to next step [默认]
  2. 返回上一步 / Go back to previous step
  3. 暂停保存 / Pause and save
  4. 退出 / Quit
请选择 (1-4) [默认: 1]: 2

返回到步骤 2/10: 智能推荐 / Intelligent Recommendation
```

### 示例 4: 配置总结输出 / Example 4: Configuration Summary Output

完成所有步骤后，系统会生成配置总结：

After completing all steps, the system generates a configuration summary:

```
================================================================================
配置总结 / Configuration Summary:
================================================================================

1. 市场和资产 / Market and Asset:
   市场 / Market: 中国市场 (A股) / China Market (A-shares)
   资产类型 / Asset Type: 股票 / Stocks

2. 选定标的 / Selected Assets:
   • 600519 (贵州茅台)
   • 300750 (宁德时代)
   • 002594 (比亚迪)

3. 投资目标 / Investment Target:
   目标收益率 / Target Return: 20.0%
   风险偏好 / Risk Preference: moderate
   模拟周期 / Simulation Period: 30 days

4. 优化策略 / Optimized Strategy:
   预期收益 / Expected Return: 22.0%
   预期风险 / Expected Risk: 15.0%

5. 训练模型 / Trained Model:
   模型ID / Model ID: model_20251207_095416
   验证准确率 / Validation Accuracy: 65.0%

6. 回测结果 / Backtest Result:
   年化收益 / Annual Return: 28.0%
   夏普比率 / Sharpe Ratio: 1.60
   最大回撤 / Max Drawdown: -12.0%

7. 模拟交易 / Simulation Trading:
   总收益率 / Total Return: 8.5%
   胜率 / Win Rate: 67.0%

8. 实盘交易 / Live Trading:
   初始资金 / Initial Capital: ¥50,000.00
   券商 / Broker: 华泰证券 / Huatai Securities
   止损线 / Stop Loss: 5.0%

10. 报告配置 / Report Configuration:
   每日报告 / Daily: ✓
   每周报告 / Weekly: ✓
   每月报告 / Monthly: ✓

================================================================================

配置总结已保存到 / Summary saved to: workflow_states/workflow_20251207_095408_summary.txt
```

## 进度管理 / Progress Management

### 保存进度 / Save Progress

系统在每个步骤完成后自动保存进度。您也可以选择"暂停保存"选项手动保存。

The system automatically saves progress after each step. You can also manually save by selecting the "Pause and save" option.

### 返回修改 / Go Back to Modify

在任何步骤，您都可以选择"返回上一步"来修改之前的配置。

At any step, you can select "Go back to previous step" to modify previous configurations.

### 查看进度 / View Progress

工作流状态保存在 `./workflow_states/` 目录下：

Workflow states are saved in the `./workflow_states/` directory:

- `latest.json`: 最新的工作流状态 / Latest workflow state
- `{workflow_id}.json`: 特定工作流的状态 / Specific workflow state
- `{workflow_id}_summary.txt`: 配置总结 / Configuration summary

## 配置总结 / Configuration Summary

完成所有步骤后，系统会生成一个完整的配置总结，包括：

After completing all steps, the system generates a complete configuration summary including:

1. 市场和资产选择 / Market and asset selection
2. 选定的投资标的 / Selected investment assets
3. 投资目标和风险偏好 / Investment targets and risk preferences
4. 优化后的策略 / Optimized strategy
5. 训练模型信息 / Trained model information
6. 回测结果 / Backtest results
7. 模拟交易结果 / Simulation trading results
8. 实盘交易配置 / Live trading configuration
9. 交易会话信息 / Trading session information
10. 报告配置 / Report configuration

## 错误处理 / Error Handling

### 输入验证 / Input Validation

系统对所有用户输入进行实时验证：

The system validates all user inputs in real-time:

- 数字范围检查 / Number range checking
- 日期格式验证 / Date format validation
- 选项有效性检查 / Choice validity checking

### 友好的错误提示 / Friendly Error Messages

所有错误消息都提供中英双语说明和建议的解决方案。

All error messages provide bilingual explanations and suggested solutions.

### 异常恢复 / Exception Recovery

如果发生异常，系统会：

If an exception occurs, the system will:

1. 显示错误信息 / Display error message
2. 询问是否继续 / Ask if you want to continue
3. 保存当前进度 / Save current progress
4. 允许安全退出 / Allow safe exit

## 最佳实践 / Best Practices

### 1. 充分利用智能推荐 / Utilize Intelligent Recommendations

系统的推荐基于历史数据分析，建议认真考虑推荐的标的。

System recommendations are based on historical data analysis, consider them carefully.

### 2. 设定合理的目标收益率 / Set Reasonable Target Returns

系统会验证目标的合理性，过高的目标可能无法实现。

The system validates target reasonableness, overly high targets may not be achievable.

### 3. 先进行充分的模拟测试 / Conduct Thorough Simulation Testing

在启动实盘交易前，建议进行至少30天的模拟交易测试。

Before starting live trading, recommend at least 30 days of simulation testing.

### 4. 设置合理的风险控制 / Set Reasonable Risk Controls

建议：
- 单日最大亏损：2-3%
- 单只股票最大仓位：30-40%
- 止损线：5-10%

Recommendations:
- Max daily loss: 2-3%
- Max position size: 30-40%
- Stop loss: 5-10%

### 5. 定期查看报告 / Regularly Review Reports

启用所有报告类型（每日/每周/每月），及时了解投资表现。

Enable all report types (daily/weekly/monthly) to stay informed about investment performance.

## 常见问题 / FAQ

### Q1: 可以跳过某些步骤吗？/ Can I skip certain steps?

A: 不可以。所有步骤都是必需的，以确保完整的投资流程。但您可以快速完成某些步骤。

No. All steps are required to ensure a complete investment process. However, you can quickly complete certain steps.

### Q2: 如何修改之前的配置？/ How to modify previous configurations?

A: 在任何步骤选择"返回上一步"，可以返回修改之前的配置。

Select "Go back to previous step" at any step to modify previous configurations.

### Q3: 工作流程可以暂停多久？/ How long can the workflow be paused?

A: 没有时间限制。工作流状态会永久保存，直到您删除状态文件。

No time limit. Workflow state is saved permanently until you delete the state files.

### Q4: 可以同时运行多个工作流吗？/ Can I run multiple workflows simultaneously?

A: 可以。每个工作流都有唯一的ID，互不干扰。

Yes. Each workflow has a unique ID and they don't interfere with each other.

### Q5: 模拟交易使用真实数据吗？/ Does simulation trading use real data?

A: 是的。模拟交易使用真实的市场数据，但不涉及真实资金。

Yes. Simulation trading uses real market data but no real money is involved.

### Q6: 实盘交易如何保证安全？/ How is live trading safety ensured?

A: 系统提供多层风险控制：
- 订单执行前的风险检查
- 实时持仓监控
- 自动止损机制
- 风险预警通知

The system provides multi-level risk controls:
- Risk checks before order execution
- Real-time position monitoring
- Automatic stop-loss mechanism
- Risk alert notifications

### Q7: 如果在某个步骤遇到错误怎么办？/ What if I encounter an error at a step?

A: 系统会显示详细的错误信息和建议的解决方案。您可以：
1. 根据提示修正输入
2. 选择返回上一步重新配置
3. 暂停保存，稍后继续
4. 查看帮助文档获取更多信息

The system will display detailed error messages and suggested solutions. You can:
1. Correct input based on prompts
2. Go back to previous step to reconfigure
3. Pause and save, continue later
4. Check help documentation for more information

### Q8: 配置总结文件保存在哪里？/ Where are configuration summary files saved?

A: 配置总结保存在 `workflow_states/` 目录下：
- `latest.json`: 最新的工作流状态
- `{workflow_id}.json`: 特定工作流的状态
- `{workflow_id}_summary.txt`: 配置总结文本文件

Configuration summaries are saved in the `workflow_states/` directory:
- `latest.json`: Latest workflow state
- `{workflow_id}.json`: Specific workflow state
- `{workflow_id}_summary.txt`: Configuration summary text file

### Q9: 可以导出配置用于其他系统吗？/ Can I export configuration for other systems?

A: 可以。配置总结以JSON格式保存，可以轻松导出和导入。您可以：
1. 复制 `{workflow_id}.json` 文件
2. 在其他系统中使用相同的配置
3. 修改JSON文件以适应不同需求

Yes. Configuration summaries are saved in JSON format for easy export and import. You can:
1. Copy the `{workflow_id}.json` file
2. Use the same configuration in other systems
3. Modify the JSON file to adapt to different needs

### Q10: 如何获取更多帮助？/ How to get more help?

A: 您可以：
1. 在工作流程中随时输入 'h' 查看帮助
2. 查看 `docs/` 目录下的详细文档
3. 运行示例脚本了解使用方法
4. 查看 `examples/` 目录下的示例代码
5. 提交Issue到项目仓库

You can:
1. Enter 'h' anytime during workflow to view help
2. Check detailed documentation in `docs/` directory
3. Run example scripts to learn usage
4. View example code in `examples/` directory
5. Submit issues to project repository

## 技术细节 / Technical Details

### 状态管理 / State Management

工作流状态使用 `WorkflowState` 数据类管理，包含：

Workflow state is managed using the `WorkflowState` dataclass, containing:

- 当前步骤 / Current step
- 已完成步骤 / Completed steps
- 所有用户配置 / All user configurations
- 中间结果 / Intermediate results

### 数据持久化 / Data Persistence

状态以JSON格式保存，支持：

State is saved in JSON format, supporting:

- 自动保存 / Automatic saving
- 手动保存 / Manual saving
- 版本控制 / Version control
- 断点续传 / Resume from breakpoint

### 验证机制 / Validation Mechanism

所有输入都经过严格验证：

All inputs are strictly validated:

- 类型检查 / Type checking
- 范围验证 / Range validation
- 格式验证 / Format validation
- 业务逻辑验证 / Business logic validation

## 相关文档 / Related Documentation

- [快速开始指南 / Quick Start Guide](quick_start.md)
- [用户手册 / User Guide](user_guide.md)
- [模拟交易指南 / Simulation Trading Guide](simulation_guide.md)
- [实盘交易指南 / Live Trading Guide](live_trading_guide.md)
- [API参考 / API Reference](api_reference.md)

## 支持 / Support

如有问题或建议，请：

For questions or suggestions, please:

1. 查看文档 / Check documentation
2. 查看示例代码 / Review example code
3. 提交Issue / Submit an issue
4. 联系技术支持 / Contact technical support
