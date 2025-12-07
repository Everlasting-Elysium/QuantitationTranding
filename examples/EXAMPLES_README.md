# 完整示例说明 / Complete Examples Guide

本目录包含三个完整的端到端示例，展示如何使用量化交易系统的主要功能。

This directory contains three complete end-to-end examples demonstrating how to use the main features of the quantitative trading system.

## 📋 示例列表 / Example List

### 1. 引导式工作流程示例 / Guided Workflow Example

**文件 / File**: `demo_guided_workflow.py`

**功能 / Features**:
- 完整的10步投资流程引导
- 从市场选择到实盘交易准备
- 进度自动保存和恢复
- 智能推荐和参数优化
- 中英双语支持

**使用方法 / Usage**:
```bash
# 从头开始 / Start from beginning
python examples/demo_guided_workflow.py --new

# 继续上次的进度 / Resume from last progress
python examples/demo_guided_workflow.py --resume

# 查看帮助 / View help
python examples/demo_guided_workflow.py --help
```

**适用场景 / Use Cases**:
- ✅ 新用户首次使用系统
- ✅ 需要完整的投资流程指导
- ✅ 想要系统化地配置交易策略
- ✅ 需要从市场选择到实盘的全流程

**预计时间 / Estimated Time**: 30-60分钟（取决于选择和配置）

---

### 2. 模拟交易示例 / Simulation Trading Example

**文件 / File**: `simulation_demo.py`

**功能 / Features**:
- 完整的模拟交易流程
- 每日交易信号生成和执行
- 持仓跟踪和收益计算
- 模拟报告生成
- 参数调整建议

**使用方法 / Usage**:
```bash
# 运行模拟交易示例 / Run simulation trading example
python examples/simulation_demo.py
```

**适用场景 / Use Cases**:
- ✅ 验证交易策略有效性
- ✅ 测试不同参数配置
- ✅ 评估风险和收益
- ✅ 实盘前的必要准备

**预计时间 / Estimated Time**: 5-10分钟

**前置条件 / Prerequisites**:
- 已完成模型训练
- 有可用的历史数据

---

### 3. 实盘交易示例 / Live Trading Example

**文件 / File**: `live_trading_demo.py`

**功能 / Features**:
- 实盘交易完整流程演示
- 交易前检查和风险确认
- 实时状态监控
- 持仓管理和风险控制
- 日报告生成

**使用方法 / Usage**:
```bash
# 运行实盘交易示例（演示模式）/ Run live trading example (demo mode)
python examples/live_trading_demo.py
```

**⚠️ 重要警告 / Important Warning**:
```
实盘交易涉及真实资金，存在亏损风险！
Live trading involves real money and carries risk of loss!

请确保：
1. 已完成充分的模拟交易测试
2. 理解并接受所有风险
3. 从小资金开始
4. 设置严格的风险控制
```

**适用场景 / Use Cases**:
- ✅ 了解实盘交易流程
- ✅ 学习风险控制机制
- ✅ 准备实际的实盘交易
- ⚠️  仅在充分测试后使用

**预计时间 / Estimated Time**: 10-15分钟（演示模式）

**前置条件 / Prerequisites**:
- 已完成模拟交易测试（至少30天）
- 已配置券商API（实际使用时）
- 理解并接受交易风险

---

## 🚀 快速开始 / Quick Start

### 推荐流程 / Recommended Flow

对于新用户，建议按以下顺序使用示例：

For new users, it's recommended to use the examples in the following order:

```
1️⃣ 引导式工作流程 / Guided Workflow
   ↓
   完成市场选择、策略配置、模型训练
   Complete market selection, strategy configuration, model training
   
2️⃣ 模拟交易 / Simulation Trading
   ↓
   验证策略，调整参数，至少运行30天
   Validate strategy, adjust parameters, run for at least 30 days
   
3️⃣ 实盘交易 / Live Trading
   ↓
   从小资金开始，密切监控
   Start with small capital, monitor closely
```

### 第一次使用 / First Time Use

```bash
# 步骤1: 运行引导式工作流程 / Step 1: Run guided workflow
python examples/demo_guided_workflow.py --new

# 步骤2: 完成配置后，运行模拟交易 / Step 2: After configuration, run simulation
python examples/simulation_demo.py

# 步骤3: 模拟成功后，了解实盘流程 / Step 3: After successful simulation, learn live trading
python examples/live_trading_demo.py
```

---

## 📊 示例对比 / Example Comparison

| 特性 / Feature | 引导式工作流程 / Guided Workflow | 模拟交易 / Simulation | 实盘交易 / Live Trading |
|---------------|--------------------------------|---------------------|----------------------|
| 完整流程 / Complete Flow | ✅ | ❌ | ❌ |
| 市场选择 / Market Selection | ✅ | ❌ | ❌ |
| 策略配置 / Strategy Config | ✅ | ❌ | ❌ |
| 模型训练 / Model Training | ✅ | ❌ | ❌ |
| 回测验证 / Backtest | ✅ | ❌ | ❌ |
| 模拟交易 / Simulation | ✅ | ✅ | ❌ |
| 实盘交易 / Live Trading | ✅ | ❌ | ✅ |
| 进度保存 / Progress Save | ✅ | ❌ | ❌ |
| 适合新手 / Beginner Friendly | ✅✅✅ | ✅✅ | ✅ |
| 所需时间 / Time Required | 30-60分钟 | 5-10分钟 | 10-15分钟 |

---

## 💡 使用技巧 / Usage Tips

### 通用技巧 / General Tips

1. **查看帮助 / View Help**
   ```bash
   python examples/<example_name>.py --help
   ```

2. **中断和恢复 / Interrupt and Resume**
   - 按 `Ctrl+C` 可以随时中断
   - 引导式工作流程会自动保存进度
   - Press `Ctrl+C` to interrupt anytime
   - Guided workflow auto-saves progress

3. **查看日志 / View Logs**
   ```bash
   tail -f logs/qlib_trading.log
   ```

4. **清理状态 / Clean State**
   ```bash
   # 清理工作流程状态 / Clean workflow state
   rm -rf workflow_states/
   
   # 清理模拟会话 / Clean simulation sessions
   rm -rf simulation_sessions/
   ```

### 引导式工作流程技巧 / Guided Workflow Tips

- 输入 `back` 返回上一步
- 输入 `help` 查看当前步骤帮助
- 输入 `status` 查看当前进度
- 输入 `quit` 退出（进度会保存）

### 模拟交易技巧 / Simulation Trading Tips

- 至少运行30天模拟交易
- 测试不同市场环境（牛市、熊市、震荡市）
- 记录并分析每次模拟的结果
- 根据结果调整参数

### 实盘交易技巧 / Live Trading Tips

- 从小资金开始（5-10万元）
- 设置严格的止损
- 密切监控前几天的交易
- 定期查看交易报告
- 遇到异常立即停止

---

## 📚 相关文档 / Related Documentation

### 系统文档 / System Documentation

- [用户指南 / User Guide](../docs/user_guide.md)
- [快速开始 / Quick Start](../docs/quick_start.md)
- [API参考 / API Reference](../docs/api_reference.md)

### 工作流程文档 / Workflow Documentation

- [引导式工作流程 / Guided Workflow](../docs/guided_workflow.md)
- [模拟交易指南 / Simulation Guide](../docs/simulation_guide.md)
- [实盘交易指南 / Live Trading Guide](../docs/live_trading_guide.md)

### 技术文档 / Technical Documentation

- [配置管理 / Configuration Management](../docs/config_manager.md)
- [模型训练 / Model Training](../docs/training_manager.md)
- [风险管理 / Risk Management](../docs/risk_manager.md)

---

## 🐛 故障排除 / Troubleshooting

### 常见问题 / Common Issues

#### 1. 找不到模型 / Model Not Found

**问题 / Problem**:
```
❌ 没有找到已训练的模型 / No trained models found
```

**解决方案 / Solution**:
```bash
# 先运行训练示例 / Run training example first
python examples/demo_complete_training.py
```

#### 2. 数据缺失 / Missing Data

**问题 / Problem**:
```
❌ 数据不存在 / Data does not exist
```

**解决方案 / Solution**:
```bash
# 下载数据 / Download data
python scripts/download_data.py
```

#### 3. 配置错误 / Configuration Error

**问题 / Problem**:
```
❌ 配置文件加载失败 / Configuration file loading failed
```

**解决方案 / Solution**:
```bash
# 检查配置文件 / Check configuration file
cat config/config.yaml

# 使用默认配置 / Use default configuration
cp config/config.yaml.example config/config.yaml
```

#### 4. 权限问题 / Permission Issue

**问题 / Problem**:
```
❌ Permission denied
```

**解决方案 / Solution**:
```bash
# 添加执行权限 / Add execute permission
chmod +x examples/*.py
```

---

## 🤝 获取帮助 / Getting Help

### 技术支持 / Technical Support

- **GitHub Issues**: [提交问题 / Submit Issue](https://github.com/your-repo/issues)
- **文档 / Documentation**: [查看文档 / View Docs](../docs/)
- **示例 / Examples**: [更多示例 / More Examples](.)

### 社区 / Community

- **讨论区 / Discussions**: 分享经验和提问
- **Wiki**: 查看常见问题和最佳实践

---

## 📝 贡献 / Contributing

欢迎贡献新的示例！

Welcome to contribute new examples!

### 贡献指南 / Contribution Guidelines

1. 示例应该完整且可运行
   Examples should be complete and runnable
2. 包含详细的注释和说明
   Include detailed comments and instructions
3. 提供中英双语支持
   Provide bilingual support (Chinese/English)
4. 遵循代码规范
   Follow code standards

---

## 📄 许可证 / License

本项目采用 MIT 许可证。

This project is licensed under the MIT License.

---

**最后更新 / Last Updated**: 2024-12-07
**版本 / Version**: 1.0
