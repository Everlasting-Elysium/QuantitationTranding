# 模拟交易指南 / Simulation Trading Guide

## 概述 / Overview

模拟交易是在实盘交易前验证策略有效性的重要步骤。本指南将详细说明如何使用系统进行模拟交易，包括流程说明、参数调整建议和结果解读。

Simulation trading is an important step to verify strategy effectiveness before live trading. This guide details how to use the system for simulation trading, including process explanation, parameter adjustment suggestions, and result interpretation.

## 什么是模拟交易 / What is Simulation Trading

模拟交易使用真实的市场数据进行前向测试，但不涉及真实资金。它可以帮助您：

Simulation trading uses real market data for forward testing without involving real money. It helps you:

- **验证策略** / **Verify Strategy**: 在真实市场条件下测试策略
- **调整参数** / **Adjust Parameters**: 优化策略参数以提高表现
- **评估风险** / **Assess Risk**: 了解策略的风险特征
- **建立信心** / **Build Confidence**: 在实盘前建立对策略的信心

### 模拟交易 vs 历史回测 / Simulation Trading vs Historical Backtest

| 特性 / Feature | 历史回测 / Backtest | 模拟交易 / Simulation |
|---------------|-------------------|---------------------|
| 数据 / Data | 历史数据 / Historical | 最新数据 / Latest |
| 时间 / Time | 快速完成 / Quick | 实时进行 / Real-time |
| 目的 / Purpose | 验证历史表现 / Verify historical performance | 验证未来表现 / Verify future performance |
| 风险 / Risk | 无 / None | 无 / None |
| 资金 / Capital | 模拟 / Simulated | 模拟 / Simulated |

## 快速开始 / Quick Start

### 3步开始模拟交易 / Start Simulation in 3 Steps

1. **启动引导式工作流程 / Start Guided Workflow**
   ```bash
   python main.py
   # 选择选项 0 / Select option 0
   ```

2. **完成前6步配置 / Complete first 6 steps**
   - 市场选择
   - 智能推荐
   - 目标设定
   - 策略优化
   - 模型训练
   - 历史回测

3. **进入模拟交易步骤 / Enter simulation trading step**
   - 设置初始资金
   - 设置模拟周期
   - 开始模拟

## 模拟交易流程 / Simulation Trading Process

### 流程图 / Process Flowchart

```
┌─────────────────────────────────────────────────────────────┐
│  1. 准备阶段 / Preparation Phase                             │
│  - 完成模型训练 / Complete model training                    │
│  - 完成历史回测 / Complete historical backtest              │
│  - 确认策略参数 / Confirm strategy parameters               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  2. 配置阶段 / Configuration Phase                           │
│  - 设置初始资金 / Set initial capital                        │
│  - 设置模拟周期 / Set simulation period                      │
│  - 配置风险参数 / Configure risk parameters                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  3. 执行阶段 / Execution Phase                               │
│  - 每日生成信号 / Generate daily signals                     │
│  - 模拟订单执行 / Simulate order execution                   │
│  - 更新持仓状态 / Update position status                     │
│  - 计算收益情况 / Calculate returns                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  4. 监控阶段 / Monitoring Phase                              │
│  - 实时查看收益 / View returns in real-time                  │
│  - 监控风险指标 / Monitor risk metrics                       │
│  - 记录交易日志 / Log trading activities                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  5. 分析阶段 / Analysis Phase                                │
│  - 生成模拟报告 / Generate simulation report                 │
│  - 分析收益指标 / Analyze return metrics                     │
│  - 评估风险水平 / Assess risk level                          │
│  - 决定是否实盘 / Decide on live trading                     │
└─────────────────────────────────────────────────────────────┘
```

### 详细步骤说明 / Detailed Step Instructions

#### 步骤 1: 准备阶段 / Preparation Phase

在开始模拟交易前，确保已完成：

Before starting simulation trading, ensure you have completed:

1. **模型训练** / **Model Training**
   - 训练好的预测模型
   - 模型性能指标满意

2. **历史回测** / **Historical Backtest**
   - 回测结果良好
   - 策略逻辑验证通过

3. **策略参数** / **Strategy Parameters**
   - 确认资产配置
   - 确认调仓频率
   - 确认风险控制参数

#### 步骤 2: 配置阶段 / Configuration Phase

**2.1 设置初始资金 / Set Initial Capital**

```
请输入模拟初始资金 (元) / Enter initial capital for simulation (CNY)
(最小: 10,000, 最大: 10,000,000) [默认: 100,000]: 100000
```

**建议 / Recommendations:**
- 新手用户: 50,000 - 100,000元
- 有经验用户: 100,000 - 500,000元
- 专业用户: 500,000 - 1,000,000元

**2.2 设置模拟周期 / Set Simulation Period**

```
请输入模拟交易周期 (天数) / Enter simulation period (days)
(最小: 7, 最大: 365) [默认: 30]: 30
```

**建议 / Recommendations:**
- 短期测试: 7-14天
- 中期测试: 30-60天（推荐）
- 长期测试: 90-180天

**2.3 配置风险参数 / Configure Risk Parameters**

系统会使用之前设定的风险参数：

The system will use previously set risk parameters:

- 单日最大亏损比例
- 单只股票最大仓位
- 止损线

#### 步骤 3: 执行阶段 / Execution Phase

模拟交易开始后，系统会自动执行以下操作：

After simulation starts, the system automatically performs:

**每日流程 / Daily Process:**

1. **市场开盘前 / Before Market Open**
   - 获取最新市场数据
   - 生成交易信号
   - 计算目标持仓

2. **模拟交易时段 / Simulated Trading Session**
   - 执行买入订单
   - 执行卖出订单
   - 更新持仓状态

3. **市场收盘后 / After Market Close**
   - 计算当日收益
   - 更新账户价值
   - 记录交易日志

**示例输出 / Example Output:**

```
================================================================================
模拟交易进行中 / Simulation Trading in Progress
================================================================================

模拟会话 / Simulation Session: sim_20251207_095419
初始资金 / Initial Capital: ¥100,000.00
模拟周期 / Simulation Period: 30 days

Day 1: 2024-01-01
  买入 / Buy: 贵州茅台 (600519) 200股 @ ¥1,800.00
  买入 / Buy: 宁德时代 (300750) 150股 @ ¥180.00
  持仓价值 / Portfolio Value: ¥102,500.00 (+2.50%)

Day 2: 2024-01-02
  持仓价值 / Portfolio Value: ¥101,800.00 (+1.80%)

Day 3: 2024-01-03
  卖出 / Sell: 比亚迪 (002594) 100股 @ ¥250.00
  持仓价值 / Portfolio Value: ¥103,200.00 (+3.20%)

...

Day 30: 2024-01-30
  持仓价值 / Portfolio Value: ¥108,500.00 (+8.50%)

================================================================================
模拟交易完成 / Simulation Trading Completed
================================================================================
```

#### 步骤 4: 监控阶段 / Monitoring Phase

在模拟交易期间，您可以实时监控：

During simulation, you can monitor in real-time:

**关键指标 / Key Metrics:**

- **当前价值** / **Current Value**: 持仓总价值
- **累计收益** / **Cumulative Return**: 总收益率
- **今日收益** / **Daily Return**: 当日收益率
- **最大回撤** / **Max Drawdown**: 最大回撤幅度
- **交易次数** / **Trade Count**: 总交易次数
- **胜率** / **Win Rate**: 盈利交易占比

#### 步骤 5: 分析阶段 / Analysis Phase

模拟完成后，系统会生成详细报告：

After simulation completes, the system generates a detailed report:

```
================================================================================
模拟交易结果 / Simulation Trading Result
================================================================================

基本信息 / Basic Information:
  初始资金 / Initial Capital: ¥100,000.00
  最终价值 / Final Value: ¥108,500.00
  模拟周期 / Simulation Period: 30 days

收益指标 / Return Metrics:
  总收益率 / Total Return: 8.50%
  年化收益率 / Annual Return: 24.00%
  日均收益率 / Daily Avg Return: 0.28%

风险指标 / Risk Metrics:
  最大回撤 / Max Drawdown: -3.20%
  波动率 / Volatility: 12.50%
  夏普比率 / Sharpe Ratio: 1.85

交易统计 / Trading Statistics:
  总交易次数 / Total Trades: 12
  盈利交易 / Profitable Trades: 8
  亏损交易 / Loss Trades: 4
  胜率 / Win Rate: 66.67%
  平均盈利 / Avg Profit: 2.50%
  平均亏损 / Avg Loss: -1.20%

================================================================================
```

## 参数调整建议 / Parameter Adjustment Suggestions

### 根据模拟结果调整 / Adjust Based on Simulation Results

#### 情况 1: 收益率低于预期 / Case 1: Returns Below Expectation

**问题 / Problem**: 总收益率 < 目标收益率

**可能原因 / Possible Causes:**
- 模型预测准确率不足
- 交易频率过低
- 仓位配置不合理

**调整建议 / Adjustment Suggestions:**

1. **优化模型 / Optimize Model**
   - 增加训练数据
   - 调整模型参数
   - 尝试不同的模型类型

2. **调整交易频率 / Adjust Trading Frequency**
   - 从每周调仓改为每日调仓
   - 增加信号敏感度

3. **优化仓位配置 / Optimize Position Allocation**
   - 增加高收益资产权重
   - 减少低收益资产权重

#### 情况 2: 风险过高 / Case 2: Risk Too High

**问题 / Problem**: 最大回撤 > 可接受范围

**可能原因 / Possible Causes:**
- 单只股票仓位过大
- 缺乏止损机制
- 市场波动剧烈

**调整建议 / Adjustment Suggestions:**

1. **降低单只股票仓位 / Reduce Single Stock Position**
   ```
   当前: 40% → 调整为: 30%
   ```

2. **设置更严格的止损 / Set Stricter Stop Loss**
   ```
   当前: -5% → 调整为: -3%
   ```

3. **增加资产分散度 / Increase Diversification**
   ```
   当前: 3只股票 → 调整为: 5-8只股票
   ```

#### 情况 3: 交易频率过高 / Case 3: Trading Frequency Too High

**问题 / Problem**: 交易次数过多，交易成本高

**可能原因 / Possible Causes:**
- 信号过于敏感
- 调仓频率过高
- 缺乏交易过滤

**调整建议 / Adjustment Suggestions:**

1. **降低信号敏感度 / Reduce Signal Sensitivity**
   - 提高信号阈值
   - 增加信号确认条件

2. **降低调仓频率 / Reduce Rebalancing Frequency**
   ```
   当前: 每日 → 调整为: 每周
   ```

3. **添加交易过滤 / Add Trading Filters**
   - 最小持仓时间: 3天
   - 最小收益阈值: 2%

#### 情况 4: 胜率过低 / Case 4: Win Rate Too Low

**问题 / Problem**: 胜率 < 50%

**可能原因 / Possible Causes:**
- 信号质量不高
- 市场环境不适合
- 风险控制不当

**调整建议 / Adjustment Suggestions:**

1. **提高信号质量 / Improve Signal Quality**
   - 增加信号过滤条件
   - 只交易高置信度信号

2. **调整市场环境 / Adjust Market Environment**
   - 避开震荡市场
   - 选择趋势明显的市场

3. **优化风险控制 / Optimize Risk Control**
   - 及时止损
   - 让利润奔跑

### 参数调整流程 / Parameter Adjustment Process

```
1. 分析模拟结果
   ↓
2. 识别问题所在
   ↓
3. 制定调整方案
   ↓
4. 重新运行模拟
   ↓
5. 对比前后结果
   ↓
6. 确认改进效果
```

## 结果解读说明 / Result Interpretation Instructions

### 收益指标解读 / Return Metrics Interpretation

#### 总收益率 / Total Return

**定义 / Definition**: (最终价值 - 初始资金) / 初始资金

**解读标准 / Interpretation Standards:**
- **优秀 / Excellent**: > 10% (30天)
- **良好 / Good**: 5% - 10%
- **一般 / Average**: 2% - 5%
- **较差 / Poor**: < 2%

**注意事项 / Notes:**
- 考虑市场整体表现
- 对比基准指数收益
- 考虑模拟周期长度

#### 年化收益率 / Annual Return

**定义 / Definition**: 总收益率 × (365 / 模拟天数)

**解读标准 / Interpretation Standards:**
- **优秀 / Excellent**: > 30%
- **良好 / Good**: 20% - 30%
- **一般 / Average**: 10% - 20%
- **较差 / Poor**: < 10%

**注意事项 / Notes:**
- 短期模拟的年化收益率可能不准确
- 建议至少30天以上的模拟

#### 夏普比率 / Sharpe Ratio

**定义 / Definition**: (收益率 - 无风险利率) / 波动率

**解读标准 / Interpretation Standards:**
- **优秀 / Excellent**: > 2.0
- **良好 / Good**: 1.0 - 2.0
- **一般 / Average**: 0.5 - 1.0
- **较差 / Poor**: < 0.5

**意义 / Significance:**
- 衡量风险调整后的收益
- 数值越高，策略越优秀

### 风险指标解读 / Risk Metrics Interpretation

#### 最大回撤 / Maximum Drawdown

**定义 / Definition**: 从峰值到谷底的最大跌幅

**解读标准 / Interpretation Standards:**
- **优秀 / Excellent**: < 5%
- **良好 / Good**: 5% - 10%
- **一般 / Average**: 10% - 20%
- **较差 / Poor**: > 20%

**风险等级 / Risk Level:**
```
最大回撤 < 5%   → 低风险 / Low Risk
最大回撤 5-10%  → 中等风险 / Medium Risk
最大回撤 10-20% → 高风险 / High Risk
最大回撤 > 20%  → 极高风险 / Very High Risk
```

#### 波动率 / Volatility

**定义 / Definition**: 收益率的标准差

**解读标准 / Interpretation Standards:**
- **低波动 / Low**: < 10%
- **中等波动 / Medium**: 10% - 20%
- **高波动 / High**: > 20%

**意义 / Significance:**
- 衡量收益的稳定性
- 波动率越低，收益越稳定

### 交易统计解读 / Trading Statistics Interpretation

#### 胜率 / Win Rate

**定义 / Definition**: 盈利交易次数 / 总交易次数

**解读标准 / Interpretation Standards:**
- **优秀 / Excellent**: > 60%
- **良好 / Good**: 50% - 60%
- **一般 / Average**: 40% - 50%
- **较差 / Poor**: < 40%

**注意事项 / Notes:**
- 胜率不是唯一指标
- 需要结合盈亏比分析

#### 盈亏比 / Profit/Loss Ratio

**定义 / Definition**: 平均盈利 / 平均亏损

**解读标准 / Interpretation Standards:**
- **优秀 / Excellent**: > 2.0
- **良好 / Good**: 1.5 - 2.0
- **一般 / Average**: 1.0 - 1.5
- **较差 / Poor**: < 1.0

**意义 / Significance:**
- 衡量盈利交易的质量
- 盈亏比越高，策略越优秀

### 综合评估 / Comprehensive Assessment

#### 评分系统 / Scoring System

根据各项指标给出综合评分：

Provide comprehensive score based on metrics:

| 指标 / Metric | 权重 / Weight | 评分标准 / Scoring |
|--------------|--------------|------------------|
| 年化收益率 / Annual Return | 30% | 0-100分 |
| 夏普比率 / Sharpe Ratio | 25% | 0-100分 |
| 最大回撤 / Max Drawdown | 25% | 0-100分 |
| 胜率 / Win Rate | 10% | 0-100分 |
| 盈亏比 / P/L Ratio | 10% | 0-100分 |

**综合评级 / Overall Rating:**
- **A级 (优秀)**: 85-100分 → 可以进入实盘
- **B级 (良好)**: 70-84分 → 建议继续优化
- **C级 (一般)**: 60-69分 → 需要调整参数
- **D级 (较差)**: < 60分 → 需要重新设计策略

## 最佳实践 / Best Practices

### 1. 充分的模拟周期 / Adequate Simulation Period

**建议 / Recommendation:**
- 最少30天
- 推荐60-90天
- 包含不同市场环境

**原因 / Reason:**
- 更全面地评估策略
- 覆盖更多市场情况
- 提高结果可靠性

### 2. 多次模拟测试 / Multiple Simulation Tests

**建议 / Recommendation:**
- 至少进行3次模拟
- 使用不同的起始日期
- 对比多次结果

**原因 / Reason:**
- 避免偶然性
- 验证策略稳定性
- 提高信心

### 3. 记录和分析 / Record and Analyze

**建议 / Recommendation:**
- 记录每次模拟的参数
- 记录每次模拟的结果
- 分析参数对结果的影响

**工具 / Tools:**
- Excel表格
- 模拟日志文件
- 系统生成的报告

### 4. 渐进式调整 / Incremental Adjustment

**建议 / Recommendation:**
- 每次只调整一个参数
- 观察调整后的效果
- 逐步优化策略

**原因 / Reason:**
- 明确参数影响
- 避免过度优化
- 保持策略稳定性

### 5. 风险优先 / Risk First

**建议 / Recommendation:**
- 先控制风险
- 再追求收益
- 确保可持续性

**原则 / Principles:**
- 最大回撤 < 10%
- 单日亏损 < 3%
- 单只股票 < 30%

## 常见问题 / FAQ

### Q1: 模拟交易需要多长时间？/ How long does simulation trading take?

A: 取决于模拟周期设置。如果设置30天，系统会模拟30个交易日的交易过程。由于是模拟，实际运行时间很短，通常几分钟内完成。

It depends on the simulation period setting. If set to 30 days, the system simulates 30 trading days. Since it's simulation, actual runtime is short, usually completing within minutes.

### Q2: 模拟交易的数据是实时的吗？/ Is simulation trading data real-time?

A: 是的。模拟交易使用最新的市场数据，但不涉及真实资金。这样可以在真实市场环境中测试策略。

Yes. Simulation trading uses the latest market data but doesn't involve real money. This allows testing strategies in real market conditions.

### Q3: 模拟结果好就一定能在实盘赚钱吗？/ Will good simulation results guarantee profits in live trading?

A: 不一定。模拟交易可以验证策略逻辑，但实盘交易还会受到滑点、交易成本、市场冲击等因素影响。建议：
1. 模拟结果作为参考
2. 实盘初期使用小资金
3. 持续监控和调整

Not necessarily. Simulation validates strategy logic, but live trading is also affected by slippage, trading costs, and market impact. Recommendations:
1. Use simulation results as reference
2. Start live trading with small capital
3. Continuously monitor and adjust

### Q4: 如何判断模拟结果是否满意？/ How to determine if simulation results are satisfactory?

A: 参考以下标准：
1. 年化收益率 > 目标收益率
2. 最大回撤 < 10%
3. 夏普比率 > 1.0
4. 胜率 > 50%
5. 综合评分 > 70分

如果满足以上条件，可以考虑进入实盘。

Refer to these standards:
1. Annual return > target return
2. Max drawdown < 10%
3. Sharpe ratio > 1.0
4. Win rate > 50%
5. Overall score > 70

If these conditions are met, consider entering live trading.

### Q5: 模拟交易失败了怎么办？/ What if simulation trading fails?

A: 不要气馁，这正是模拟交易的价值所在。建议：
1. 分析失败原因
2. 调整策略参数
3. 重新进行模拟
4. 必要时重新训练模型
5. 考虑更换策略

Don't be discouraged, this is the value of simulation. Recommendations:
1. Analyze failure reasons
2. Adjust strategy parameters
3. Re-run simulation
4. Retrain model if necessary
5. Consider changing strategy

### Q6: 可以在模拟过程中修改参数吗？/ Can I modify parameters during simulation?

A: 不建议。模拟交易应该完整运行，以获得准确的结果。如果需要调整参数，建议：
1. 停止当前模拟
2. 修改参数
3. 重新开始新的模拟

Not recommended. Simulation should run completely for accurate results. If you need to adjust parameters:
1. Stop current simulation
2. Modify parameters
3. Start a new simulation

### Q7: 模拟交易的结果保存在哪里？/ Where are simulation results saved?

A: 模拟交易结果保存在 `simulations/` 目录下：
- `sessions/{session_id}.json`: 模拟会话数据
- `reports/{session_id}_report.html`: 模拟报告
- `logs/{session_id}.log`: 模拟日志

Simulation results are saved in the `simulations/` directory:
- `sessions/{session_id}.json`: Simulation session data
- `reports/{session_id}_report.html`: Simulation report
- `logs/{session_id}.log`: Simulation log

### Q8: 如何对比多次模拟的结果？/ How to compare results from multiple simulations?

A: 系统提供对比功能：
1. 在报告查看菜单中选择"对比报告"
2. 选择要对比的模拟会话
3. 系统会生成对比图表和分析

The system provides comparison functionality:
1. Select "Comparison Report" in report viewing menu
2. Select simulation sessions to compare
3. System generates comparison charts and analysis

### Q9: 模拟交易会影响真实市场吗？/ Will simulation trading affect the real market?

A: 不会。模拟交易完全在系统内部进行，不会向市场发送任何订单，不会影响真实市场。

No. Simulation trading is completely internal to the system, doesn't send any orders to the market, and doesn't affect the real market.

### Q10: 模拟交易和实盘交易可以同时进行吗？/ Can simulation and live trading run simultaneously?

A: 可以。它们是独立的会话，互不影响。但建议：
1. 使用不同的模型
2. 使用不同的资产
3. 避免混淆

Yes. They are independent sessions and don't interfere. But recommend:
1. Use different models
2. Use different assets
3. Avoid confusion

## 相关文档 / Related Documentation

- [引导式工作流程文档 / Guided Workflow Documentation](guided_workflow.md)
- [实盘交易指南 / Live Trading Guide](live_trading_guide.md)
- [用户手册 / User Guide](user_guide.md)
- [API参考 / API Reference](api_reference.md)

## 支持 / Support

如有问题或建议，请：

For questions or suggestions, please:

1. 查看文档 / Check documentation
2. 查看示例代码 / Review example code
3. 提交Issue / Submit an issue
4. 联系技术支持 / Contact technical support
