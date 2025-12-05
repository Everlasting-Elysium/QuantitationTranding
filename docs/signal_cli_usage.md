# 信号生成CLI使用指南 / Signal Generation CLI Usage Guide

## 概述 / Overview

信号生成功能允许您使用训练好的模型生成交易信号，包括买入、卖出和持有建议。系统会根据模型预测、当前持仓和风险限制自动生成合理的交易信号。

The signal generation feature allows you to generate trading signals using trained models, including buy, sell, and hold recommendations. The system automatically generates reasonable trading signals based on model predictions, current positions, and risk limits.

## 功能特性 / Features

- **模型选择 / Model Selection**: 从已训练的模型中选择用于信号生成
- **参数配置 / Parameter Configuration**: 配置信号生成日期、股票池、买入候选数量等
- **信号生成 / Signal Generation**: 自动生成买入、卖出、持有信号
- **信号解释 / Signal Explanation**: 查看每个信号的详细解释和主要影响因素
- **风险控制 / Risk Control**: 自动应用风险限制，确保信号符合风险管理要求
- **信号导出 / Signal Export**: 将生成的信号导出为JSON文件

## 使用步骤 / Usage Steps

### 1. 启动主CLI / Launch Main CLI

```bash
python demo_signal_cli.py
```

或直接运行主CLI：

```bash
python -m src.cli.main_cli
```

### 2. 选择信号生成功能 / Select Signal Generation

在主菜单中选择选项 `3`:

```
3. 信号生成 / Signal Generation
   生成交易信号 / Generate trading signals
```

### 3. 选择操作 / Select Operation

系统会显示信号生成子菜单：

```
请选择操作 / Please select an operation:
  1. 生成新信号 / Generate new signals
  2. 查看信号历史 / View signal history
  3. 返回主菜单 / Return to main menu
```

选择 `1` 生成新信号。

### 4. 选择模型 / Select Model

系统会列出所有可用的模型：

```
可用的模型 / Available Models:
----------------------------------------------------------------------

1. lgbm_model (v1.0)
   模型ID / Model ID: lgbm_csi300_20240101
   模型类型 / Model Type: LightGBM
   训练日期 / Training Date: 2024-01-01
   状态 / Status: active
   性能指标 / Performance Metrics:
     - IC: 0.085000
     - ICIR: 1.250000
     - Rank IC: 0.092000

2. linear_model (v1.0)
   模型ID / Model ID: linear_csi300_20240101
   ...
```

选择要使用的模型。

### 5. 配置信号生成参数 / Configure Signal Generation Parameters

#### 5.1 信号生成日期 / Signal Generation Date

输入要生成信号的日期（默认为当前日期）：

```
请输入信号生成日期 / Please enter signal generation date [2024-01-15]: 
```

#### 5.2 股票池 / Stock Pool

选择股票池：

```
请选择股票池 / Please select stock pool:
  1. csi300 (沪深300)
  2. csi500 (中证500)
  3. csi800 (中证800)
  4. 自定义 / Custom
```

#### 5.3 买入候选数量 / Number of Buy Candidates

输入希望生成的买入候选数量：

```
请输入买入候选数量 / Please enter number of buy candidates [10]: 
```

#### 5.4 现有持仓 / Existing Positions

系统会询问是否有现有持仓：

```
是否有现有持仓？ / Do you have existing positions? [y/N]: 
```

如果选择 `y`，可以输入现有持仓信息（当前版本使用空持仓）。

### 6. 确认配置 / Confirm Configuration

系统会显示配置摘要：

```
======================================================================
📝 信号生成配置确认 / Signal Generation Configuration Confirmation
======================================================================
模型 / Model: lgbm_model (v1.0)
模型ID / Model ID: lgbm_csi300_20240101
信号日期 / Signal Date: 2024-01-15
股票池 / Stock Pool: csi300
买入候选数 / Buy Candidates: 10
初始资金 / Initial Cash: 1,000,000.00
======================================================================

确认生成信号？ / Confirm to generate signals? [Y/n]: 
```

### 7. 查看信号结果 / View Signal Results

系统会生成信号并显示结果：

```
======================================================================
✅ 信号生成完成！ / Signal Generation Completed!
======================================================================

总信号数 / Total Signals: 15
  买入信号 / Buy Signals: 10
  卖出信号 / Sell Signals: 0
  持有信号 / Hold Signals: 5

======================================================================
📈 买入信号 / Buy Signals
======================================================================

1. 600519.SH
   预测分数 / Score: 0.1523
   置信度 / Confidence: 92.50%
   建议权重 / Target Weight: 8.50%
   原因 / Reason: 模型预测分数高 / High model prediction score: 0.1523

2. 000858.SZ
   预测分数 / Score: 0.1387
   置信度 / Confidence: 89.20%
   建议权重 / Target Weight: 8.50%
   原因 / Reason: 模型预测分数高 / High model prediction score: 0.1387

...
```

### 8. 查看详细解释 / View Detailed Explanations

系统会询问是否查看详细解释：

```
是否查看信号详细解释？ / View detailed signal explanations? [y/N]: 
```

如果选择 `y`，系统会显示每个信号的详细解释：

```
======================================================================
📖 信号详细解释 / Detailed Signal Explanations
======================================================================

----------------------------------------------------------------------
1. 600519.SH - BUY
----------------------------------------------------------------------

主要影响因素 / Main Factors:
  • 预测收益率 / Predicted return: 35.0%
  • 动量指标 / Momentum: 25.0%
  • 估值指标 / Valuation: 20.0%
  • 成交量 / Volume: 15.0%
  • 市场情绪 / Market sentiment: 5.0%

风险等级 / Risk Level: 🟢 低风险 / Low Risk

详细说明 / Description:
  该股票预测分数较高(0.1523)，置信度为92.50%。基于模型分析，
  该股票具有较好的上涨潜力，建议买入。当前风险等级为低，
  适合稳健型投资者。
```

### 9. 导出信号 / Export Signals

系统会询问是否导出信号：

```
是否导出信号到文件？ / Export signals to file? [y/N]: 
```

如果选择 `y`，信号会被导出为JSON文件：

```
✅ 信号已导出 / Signals exported
   文件路径 / File path: outputs/signals/signals_20240115_143025.json
```

## 信号类型说明 / Signal Types

### 买入信号 / Buy Signals

- **条件 / Conditions**: 预测分数高、不在当前持仓中
- **信息 / Information**: 股票代码、预测分数、置信度、建议权重
- **用途 / Usage**: 建议买入的股票列表

### 卖出信号 / Sell Signals

- **条件 / Conditions**: 预测分数低于中位数、或不在当前股票池中
- **信息 / Information**: 股票代码、预测分数、置信度、持仓数量
- **用途 / Usage**: 建议卖出的股票列表

### 持有信号 / Hold Signals

- **条件 / Conditions**: 预测分数高于中位数、在当前持仓中
- **信息 / Information**: 股票代码、预测分数、置信度、持仓数量
- **用途 / Usage**: 建议继续持有的股票列表

## 风险控制 / Risk Control

系统会自动应用以下风险控制规则：

1. **最大持仓比例 / Max Position Size**: 默认80%
   - 当持仓比例超过此限制时，不会生成新的买入信号

2. **单只股票最大权重 / Max Single Stock**: 默认20%
   - 单只股票的权重不会超过此限制

3. **最小现金储备 / Min Cash Reserve**: 默认20%
   - 保留一定比例的现金，不会全部投入

4. **持仓数量限制 / Position Count Limit**: 
   - 根据买入候选数量和可用资金自动计算

## 导出文件格式 / Export File Format

导出的JSON文件格式如下：

```json
[
  {
    "stock_code": "600519.SH",
    "action": "buy",
    "score": 0.1523,
    "confidence": 0.925,
    "timestamp": "2024-01-15",
    "reason": "模型预测分数高 / High model prediction score: 0.1523",
    "quantity": null,
    "target_weight": 8.5
  },
  {
    "stock_code": "000858.SZ",
    "action": "buy",
    "score": 0.1387,
    "confidence": 0.892,
    "timestamp": "2024-01-15",
    "reason": "模型预测分数高 / High model prediction score: 0.1387",
    "quantity": null,
    "target_weight": 8.5
  }
]
```

## 测试 / Testing

运行测试脚本验证功能：

```bash
python test_signal_cli.py
```

测试脚本会验证：
- 信号生成器初始化
- 模型选择功能
- 信号生成功能
- 信号解释功能

## 常见问题 / FAQ

### Q1: 为什么没有生成任何信号？

**A**: 可能的原因：
- 当前日期没有可用数据
- 所有候选股票都不满足风险控制条件
- 模型预测结果为空
- 股票池配置错误

**解决方法**:
- 检查数据是否已下载
- 尝试使用历史日期
- 检查模型是否正常工作
- 验证股票池配置

### Q2: 如何理解置信度？

**A**: 置信度表示模型对预测的信心程度：
- **高置信度 (>80%)**: 模型对预测很有信心，信号可靠性高
- **中等置信度 (60-80%)**: 模型有一定信心，但存在不确定性
- **低置信度 (<60%)**: 模型信心不足，信号可靠性较低

### Q3: 建议权重是如何计算的？

**A**: 建议权重基于以下因素：
- 可用资金
- 买入候选数量
- 单只股票最大权重限制
- 风险控制参数

系统会自动计算合理的权重分配。

### Q4: 如何使用生成的信号？

**A**: 生成的信号仅供参考，不构成投资建议。使用时应：
1. 结合自己的投资策略和风险承受能力
2. 考虑市场环境和个股基本面
3. 进行充分的风险评估
4. 建议先进行模拟交易测试

### Q5: 信号解释中的主要因素是什么？

**A**: 主要因素是影响模型预测的关键指标，包括：
- 预测收益率
- 动量指标
- 估值指标
- 成交量
- 市场情绪
- 技术指标

每个因素的贡献度表示其对预测的影响程度。

## 注意事项 / Notes

1. **数据要求 / Data Requirements**:
   - 确保qlib数据已下载并更新
   - 信号生成日期必须在数据范围内

2. **模型要求 / Model Requirements**:
   - 至少需要一个已训练的模型
   - 模型状态应为 "active"

3. **风险提示 / Risk Warning**:
   - 生成的信号仅供参考
   - 不构成投资建议
   - 投资有风险，决策需谨慎

4. **性能考虑 / Performance Considerations**:
   - 信号生成可能需要几秒到几分钟
   - 取决于模型复杂度和数据量
   - 建议在非交易时间进行

## 相关文档 / Related Documentation

- [模型训练指南](training_cli_usage.md)
- [回测使用指南](backtest_cli_usage.md)
- [CLI使用指南](cli_usage.md)
- [API参考文档](../README.md)

## 技术支持 / Technical Support

如有问题或建议，请：
- 查看文档目录下的其他指南
- 查看示例代码 (examples/ 目录)
- 提交Issue到项目仓库

---

**版本 / Version**: 1.0.0  
**更新日期 / Last Updated**: 2024-01-15
