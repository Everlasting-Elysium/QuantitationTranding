# 模拟交易CLI使用指南 / Simulation Trading CLI Usage Guide

## 概述 / Overview

模拟交易功能已成功集成到主CLI界面中，允许用户通过交互式菜单进行模拟交易测试。
The simulation trading feature has been successfully integrated into the main CLI interface, allowing users to conduct simulation trading tests through an interactive menu.

## 功能特性 / Features

### 1. 开始新的模拟交易 / Start New Simulation

通过交互式问答收集模拟参数：
Collect simulation parameters through interactive Q&A:

- **模型选择 / Model Selection**: 从已训练的模型中选择
- **初始资金 / Initial Capital**: 设置模拟交易的初始资金
- **模拟天数 / Simulation Days**: 指定模拟交易的天数
- **开始日期 / Start Date**: 选择模拟开始的日期
- **股票池 / Stock Pool**: 选择交易的股票池（csi300, csi500等）
- **买入候选数 / Buy Candidates**: 设置每次买入的候选股票数量

### 2. 查看模拟结果 / View Simulation Results

查看已完成的模拟交易结果：
View completed simulation trading results:

- **基本信息 / Basic Information**: 会话ID、模型ID、初始资金等
- **收益指标 / Return Metrics**: 总收益率、年化收益率、最大回撤
- **风险指标 / Risk Metrics**: 夏普比率、波动率
- **交易统计 / Trade Statistics**: 总交易次数、盈利交易、胜率
- **持仓信息 / Position Information**: 最终持仓详情

### 3. 调整参数重新测试 / Adjust Parameters and Retest

根据模拟结果调整参数并重新测试：
Adjust parameters based on simulation results and retest:

- 修改初始资金
- 调整模拟天数
- 更换股票池
- 改变买入候选数量
- 使用不同的模型

## 使用步骤 / Usage Steps

### 步骤1：启动CLI / Step 1: Launch CLI

```bash
python main.py
# 或 / or
python src/cli/main_cli.py
```

### 步骤2：选择模拟交易 / Step 2: Select Simulation Trading

在主菜单中选择选项 `3. 模拟交易 / Simulation Trading`

### 步骤3：开始新的模拟 / Step 3: Start New Simulation

1. 选择 `开始新的模拟交易 / Start new simulation`
2. 从列表中选择一个已训练的模型
3. 配置模拟参数：
   - 输入初始资金（默认：100,000元）
   - 输入模拟天数（默认：30天）
   - 选择开始日期
   - 选择股票池
   - 设置买入候选数量（默认：10）
4. 确认配置并开始模拟

### 步骤4：查看结果 / Step 4: View Results

模拟完成后，系统会自动显示：
After simulation completes, the system will automatically display:

- 基本信息和收益指标
- 风险指标和交易统计
- 最终持仓信息

您可以选择：
You can choose to:

- 查看详细报告（包括每日收益和交易历史）
- 导出报告到文件
- 调整参数重新测试

## 示例输出 / Example Output

```
======================================================================
✅ 模拟交易完成！ / Simulation Completed!
======================================================================

【基本信息 / Basic Information】
  会话ID / Session ID: sim_a1b2c3d4
  模型ID / Model ID: lgbm_csi300_20240101
  初始资金 / Initial Capital: 100,000.00 元 / CNY
  最终价值 / Final Value: 108,500.00 元 / CNY
  模拟天数 / Simulation Days: 30
  实际执行天数 / Actual Days: 21

【收益指标 / Return Metrics】
  总收益率 / Total Return: 8.50%
  年化收益率 / Annual Return: 24.00%
  最大回撤 / Max Drawdown: -3.20%

【风险指标 / Risk Metrics】
  夏普比率 / Sharpe Ratio: 1.6500
  波动率 / Volatility: 15.20%

【交易统计 / Trade Statistics】
  总交易次数 / Total Trades: 12
  盈利交易 / Profitable Trades: 8
  胜率 / Win Rate: 66.67%

【最终持仓 / Final Positions】
  600519: 200 股 / shares, 成本 / cost: 1800.00, 市值 / value: 36,000.00
  300750: 150 股 / shares, 成本 / cost: 180.00, 市值 / value: 27,000.00
  ...
```

## 输出文件 / Output Files

### 模拟报告 / Simulation Reports

模拟报告会自动保存到：
Simulation reports are automatically saved to:

```
outputs/simulations/simulation_{session_id}_{timestamp}.json
```

报告包含：
Reports contain:

- 完整的收益和风险指标
- 每日收益率序列
- 每日投资组合价值
- 完整的交易历史

### 会话数据 / Session Data

模拟会话数据保存在：
Simulation session data is saved in:

```
simulations/sessions/{session_id}.json
```

## 注意事项 / Notes

1. **模型要求 / Model Requirements**: 
   - 必须先训练至少一个模型才能进行模拟交易
   - Must train at least one model before simulation trading

2. **数据要求 / Data Requirements**:
   - 确保qlib数据已下载并初始化
   - Ensure qlib data is downloaded and initialized
   - 模拟日期范围必须在可用数据范围内
   - Simulation date range must be within available data range

3. **性能考虑 / Performance Considerations**:
   - 模拟天数越多，执行时间越长
   - More simulation days = longer execution time
   - 建议首次测试使用较短的天数（如30天）
   - Recommend using shorter periods (e.g., 30 days) for initial tests

4. **参数调整建议 / Parameter Adjustment Suggestions**:
   - 如果收益率低，可以尝试增加买入候选数量
   - If returns are low, try increasing buy candidates
   - 如果波动率高，可以尝试减少持仓数量
   - If volatility is high, try reducing position sizes
   - 如果胜率低，可以尝试更换模型或股票池
   - If win rate is low, try different models or stock pools

## 故障排除 / Troubleshooting

### 问题1：没有可用的模型 / Issue 1: No Models Available

**解决方案 / Solution**:
```bash
# 先训练一个模型
# Train a model first
选择主菜单 -> 1. 模型训练 -> 使用模型模板训练
Select main menu -> 1. Model Training -> Train with model template
```

### 问题2：Qlib未初始化 / Issue 2: Qlib Not Initialized

**解决方案 / Solution**:
```bash
# 初始化qlib数据
# Initialize qlib data
选择主菜单 -> 5. 数据管理 -> 验证数据完整性
Select main menu -> 5. Data Management -> Validate data integrity
```

### 问题3：模拟执行失败 / Issue 3: Simulation Execution Failed

**可能原因 / Possible Causes**:
- 数据日期范围不足
- 股票池代码错误
- 模型文件损坏

**解决方案 / Solution**:
- 检查数据覆盖范围
- 验证股票池代码
- 重新训练模型

## 相关文档 / Related Documentation

- [模拟交易引擎文档](simulation_engine.md)
- [CLI使用指南](cli_usage.md)
- [模型训练指南](training_cli_usage.md)
- [数据管理指南](data_management_cli.md)

## 反馈与支持 / Feedback and Support

如有问题或建议，请：
For questions or suggestions, please:

1. 查看日志文件：`logs/qlib_trading.log`
2. 查看模拟输出：`outputs/simulations/`
3. 提交Issue或联系开发团队

---

**版本 / Version**: 1.0  
**最后更新 / Last Updated**: 2024-12-05  
**作者 / Author**: Kiro AI Assistant
