# 实盘交易CLI集成文档 / Live Trading CLI Integration Documentation

## 概述 / Overview

本文档说明如何将实盘交易功能集成到主CLI界面中。
This document explains how to integrate live trading functionality into the main CLI interface.

## 已实现的功能 / Implemented Features

### 1. 实盘交易管理器 / Live Trading Manager
- ✅ 文件位置 / File Location: `src/application/live_trading_manager.py`
- ✅ 功能 / Features:
  - 启动实盘交易会话 / Start live trading session
  - 执行交易订单 / Execute trading orders
  - 查看当前持仓 / View current positions
  - 暂停/恢复交易 / Pause/resume trading
  - 停止交易并生成报告 / Stop trading and generate report
  - 风险检查集成 / Risk check integration

### 2. CLI模块 / CLI Module
- ✅ 文件位置 / File Location: `src/cli/live_trading_cli.py`
- ✅ 功能 / Features:
  - 实盘交易菜单处理 / Live trading menu handling
  - 券商配置界面 / Broker configuration interface
  - 交易参数设置 / Trading parameter settings
  - 实时状态监控 / Real-time status monitoring
  - 交易控制（启动/暂停/停止）/ Trading controls (start/pause/stop)

### 3. 文档和示例 / Documentation and Examples
- ✅ 文档 / Documentation: `docs/live_trading_manager.md`
- ✅ 示例 / Example: `examples/demo_live_trading_manager.py`
- ✅ 实现总结 / Implementation Summary: `LIVE_TRADING_MANAGER_IMPLEMENTATION.md`

## 集成步骤 / Integration Steps

### 步骤1：更新MainCLI菜单选项 / Step 1: Update MainCLI Menu Options

在 `src/cli/main_cli.py` 的 `MainCLI.__init__()` 方法中，添加实盘交易菜单选项：

```python
self.menu_options: Dict[str, Dict[str, any]] = {
    "1": {
        "name": "模型训练 / Model Training",
        "handler": self._handle_training,
        "description": "训练新的预测模型 / Train new prediction models"
    },
    "2": {
        "name": "历史回测 / Historical Backtest",
        "handler": self._handle_backtest,
        "description": "对模型进行历史回测 / Backtest models on historical data"
    },
    "3": {
        "name": "模拟交易 / Simulation Trading",
        "handler": self._handle_simulation_trading,
        "description": "进行模拟交易测试 / Conduct simulation trading tests"
    },
    "4": {
        "name": "实盘交易 / Live Trading",  # 新增 / NEW
        "handler": self._handle_live_trading,  # 新增 / NEW
        "description": "执行实盘交易 / Execute live trading"  # 新增 / NEW
    },
    "5": {
        "name": "信号生成 / Signal Generation",
        "handler": self._handle_signal_generation,
        "description": "生成交易信号 / Generate trading signals"
    },
    # ... 其他选项 / other options
}
```

### 步骤2：更新show_menu()方法 / Step 2: Update show_menu() Method

更新菜单显示以包含新选项：

```python
def show_menu(self) -> None:
    # ...
    for key in ["1", "2", "3", "4", "5", "6", "7", "8"]:  # 添加"4" / Add "4"
        option = self.menu_options[key]
        print(f"  {key}. {option['name']}")
        print(f"     {option['description']}")
        print()
    # ...
```

### 步骤3：添加实盘交易方法 / Step 3: Add Live Trading Methods

有两种方式添加实盘交易方法：

#### 方式A：使用Mixin（推荐）/ Method A: Use Mixin (Recommended)

```python
from .live_trading_cli import LiveTradingCLIMixin

class MainCLI(LiveTradingCLIMixin):
    # ... 现有代码 / existing code
```

#### 方式B：直接复制方法 / Method B: Copy Methods Directly

从 `src/cli/live_trading_cli.py` 中的 `LiveTradingCLIMixin` 类复制所有方法到 `MainCLI` 类中。

### 步骤4：验证集成 / Step 4: Verify Integration

运行测试脚本验证集成：

```bash
python test_live_trading_cli.py
```

预期输出应显示所有方法都已成功集成。

## 使用示例 / Usage Example

### 启动实盘交易 / Starting Live Trading

1. 运行主CLI / Run main CLI:
   ```bash
   python main.py
   ```

2. 选择选项4（实盘交易）/ Select option 4 (Live Trading)

3. 选择"启动实盘交易" / Select "Start live trading"

4. 按照提示配置：
   - 选择模型 / Select model
   - 配置券商信息 / Configure broker information
   - 设置交易参数 / Set trading parameters
   - 配置风险控制 / Configure risk control

5. 确认并启动 / Confirm and start

### 监控交易状态 / Monitoring Trading Status

1. 在实盘交易菜单中选择"查看交易状态" / Select "View trading status" in live trading menu

2. 查看：
   - 当前价值 / Current value
   - 总收益率 / Total return
   - 持仓数量 / Number of positions
   - 现金余额 / Cash balance

### 暂停/恢复交易 / Pause/Resume Trading

- 暂停：选择"暂停交易"，交易将停止执行新信号
  Pause: Select "Pause trading", trading will stop executing new signals

- 恢复：选择"恢复交易"，交易将继续执行
  Resume: Select "Resume trading", trading will continue

### 停止交易 / Stopping Trading

1. 选择"停止交易" / Select "Stop trading"

2. 选择是否平仓所有持仓 / Choose whether to close all positions

3. 确认停止 / Confirm stop

4. 查看交易总结报告 / View trading summary report

## 安全注意事项 / Security Considerations

### 1. 券商凭证安全 / Broker Credentials Security

- ⚠️ 凭证应加密存储 / Credentials should be encrypted
- ⚠️ 不要在代码中硬编码凭证 / Do not hardcode credentials in code
- ⚠️ 使用环境变量或安全配置文件 / Use environment variables or secure config files

### 2. 风险控制 / Risk Control

- ✅ 系统已实现多层风险检查 / System implements multi-level risk checks
- ✅ 自动止损和止盈 / Automatic stop loss and take profit
- ✅ 持仓限制 / Position limits
- ✅ 每日交易次数限制 / Daily trade limit

### 3. 测试建议 / Testing Recommendations

- 📝 先在模拟交易中充分测试 / Test thoroughly in simulation trading first
- 📝 使用小额资金开始实盘 / Start live trading with small capital
- 📝 密切监控初期交易 / Monitor closely during initial trading
- 📝 定期检查风险预警 / Regularly check risk alerts

## 故障排除 / Troubleshooting

### 问题1：无法连接券商 / Issue 1: Cannot Connect to Broker

**解决方案 / Solution:**
- 检查券商凭证是否正确 / Check if broker credentials are correct
- 确认网络连接 / Confirm network connection
- 查看日志文件 `logs/qlib_trading.log` / Check log file `logs/qlib_trading.log`

### 问题2：交易被拒绝 / Issue 2: Trade Rejected

**解决方案 / Solution:**
- 检查风险控制参数 / Check risk control parameters
- 确认账户余额充足 / Confirm sufficient account balance
- 查看风险预警信息 / Check risk alert messages

### 问题3：持仓更新不及时 / Issue 3: Position Updates Delayed

**解决方案 / Solution:**
- 检查券商API连接状态 / Check broker API connection status
- 确认市场数据更新 / Confirm market data updates
- 重启交易会话 / Restart trading session

## 相关文件 / Related Files

### 核心实现 / Core Implementation
- `src/application/live_trading_manager.py` - 实盘交易管理器
- `src/core/portfolio_manager.py` - 投资组合管理器
- `src/core/risk_manager.py` - 风险管理器
- `src/infrastructure/trading_api_adapter.py` - 交易API适配器

### CLI界面 / CLI Interface
- `src/cli/main_cli.py` - 主CLI界面
- `src/cli/live_trading_cli.py` - 实盘交易CLI模块
- `src/cli/interactive_prompt.py` - 交互式提示

### 文档 / Documentation
- `docs/live_trading_manager.md` - 实盘交易管理器文档
- `docs/trading_api_adapter.md` - 交易API适配器文档
- `LIVE_TRADING_MANAGER_IMPLEMENTATION.md` - 实现总结

### 示例 / Examples
- `examples/demo_live_trading_manager.py` - 实盘交易示例

## 下一步 / Next Steps

1. ✅ 实盘交易核心功能已实现 / Live trading core functionality implemented
2. ✅ CLI界面已实现 / CLI interface implemented
3. ⏳ 集成到主CLI（需要手动完成）/ Integration into main CLI (requires manual completion)
4. ⏳ 通知服务集成（任务43）/ Notification service integration (Task 43)
5. ⏳ 报告调度器（任务44）/ Report scheduler (Task 44)

## 联系支持 / Contact Support

如有问题，请参考：
For issues, please refer to:
- 文档目录 `docs/` / Documentation directory `docs/`
- 示例目录 `examples/` / Examples directory `examples/`
- 日志文件 `logs/qlib_trading.log` / Log file `logs/qlib_trading.log`

---

**最后更新 / Last Updated:** 2024-12-05
**版本 / Version:** 1.0.0
