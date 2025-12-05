# CLI 使用指南 / CLI Usage Guide

## 概述 / Overview

量化交易系统提供了一个友好的中文命令行界面（CLI），让用户无需编写代码即可完成所有操作。

The quantitative trading system provides a user-friendly Chinese command-line interface (CLI) that allows users to complete all operations without writing code.

## 启动系统 / Starting the System

### 方法 1: 使用主入口脚本 / Method 1: Using Main Entry Script

```bash
python main.py
```

### 方法 2: 直接运行CLI模块 / Method 2: Running CLI Module Directly

```bash
python -m src.cli.main_cli
```

## 主菜单 / Main Menu

启动系统后，您将看到主菜单：

After starting the system, you will see the main menu:

```
======================================================================
📊 量化交易系统 - 主菜单 / Quantitative Trading System - Main Menu
======================================================================

  1. 模型训练 / Model Training
     训练新的预测模型 / Train new prediction models

  2. 历史回测 / Historical Backtest
     对模型进行历史回测 / Backtest models on historical data

  3. 信号生成 / Signal Generation
     生成交易信号 / Generate trading signals

  4. 数据管理 / Data Management
     下载和管理市场数据 / Download and manage market data

  5. 模型管理 / Model Management
     查看和管理训练好的模型 / View and manage trained models

  6. 报告查看 / View Reports
     查看训练和回测报告 / View training and backtest reports

  h. 帮助 / Help
  q. 退出 / Quit

======================================================================
```

## 功能说明 / Feature Description

### 1. 模型训练 / Model Training

训练新的预测模型，支持多种模型类型和模板。

Train new prediction models with support for multiple model types and templates.

**功能特性 / Features:**
- 选择预配置的模型模板
- 自定义训练参数
- 实时监控训练进度
- 自动保存训练结果

**注意 / Note:** 此功能将在任务21中实现。

### 2. 历史回测 / Historical Backtest

使用历史数据测试模型的表现。

Test model performance using historical data.

**功能特性 / Features:**
- 选择已训练的模型
- 设置回测时间段
- 配置回测策略参数
- 生成详细的回测报告

**注意 / Note:** 此功能将在任务22中实现。

### 3. 信号生成 / Signal Generation

基于训练好的模型生成交易信号。

Generate trading signals based on trained models.

**功能特性 / Features:**
- 选择预测模型
- 生成买入/卖出信号
- 查看信号解释和置信度
- 导出信号列表

**注意 / Note:** 此功能将在任务23中实现。

### 4. 数据管理 / Data Management

下载、验证和管理市场数据。

Download, validate, and manage market data.

**功能特性 / Features:**
- 下载最新市场数据
- 验证数据完整性
- 查看数据信息和时间范围
- 更新现有数据

**注意 / Note:** 此功能将在任务24中实现。

### 5. 模型管理 / Model Management

查看和管理已训练的模型。

View and manage trained models.

**功能特性 / Features:**
- 查看所有已注册模型
- 查看模型详细信息和性能指标
- 设置生产环境模型
- 删除旧版本模型

**注意 / Note:** 此功能将在任务25中实现。

### 6. 报告查看 / View Reports

查看训练和回测生成的报告。

View reports generated from training and backtesting.

**功能特性 / Features:**
- 查看训练报告
- 查看回测报告
- 对比多个模型的性能
- 导出报告为HTML或PDF

## 帮助系统 / Help System

### 查看帮助 / View Help

在主菜单中输入 `h` 可以查看详细的帮助信息。

Enter `h` in the main menu to view detailed help information.

帮助信息包括：
- 系统概述
- 主要功能说明
- 使用流程指导
- 快捷键说明
- 获取更多帮助的途径

### 快捷键 / Shortcuts

- `h` - 显示帮助信息 / Show help information
- `q` - 退出系统 / Quit the system
- `Ctrl+C` - 中断当前操作 / Interrupt current operation

## 使用流程 / Usage Workflow

### 推荐的使用流程 / Recommended Workflow

1. **数据管理** - 首先下载和准备市场数据
   - Data Management - First download and prepare market data

2. **模型训练** - 使用历史数据训练预测模型
   - Model Training - Train prediction models using historical data

3. **历史回测** - 在历史数据上测试模型表现
   - Historical Backtest - Test model performance on historical data

4. **信号生成** - 使用训练好的模型生成交易信号
   - Signal Generation - Generate trading signals using trained models

## 交互式输入 / Interactive Input

系统使用交互式提示收集用户输入，具有以下特性：

The system uses interactive prompts to collect user input with the following features:

### 输入验证 / Input Validation

- 自动验证输入的有效性
- 提供清晰的错误提示
- 允许重新输入

### 默认值 / Default Values

- 大多数输入都提供默认值
- 按回车键使用默认值
- 默认值会在提示中显示

### 中文友好 / Chinese-Friendly

- 所有提示都是中英双语
- 错误信息清晰易懂
- 支持中文输入

## 错误处理 / Error Handling

### 中断操作 / Interrupt Operation

按 `Ctrl+C` 可以中断当前操作：
- 系统会询问是否确认退出
- 可以选择继续或返回主菜单

### 错误恢复 / Error Recovery

遇到错误时：
- 系统会显示清晰的错误信息
- 提供可能的解决方案
- 允许重试操作

## 示例 / Examples

### 示例 1: 启动系统并查看帮助

```bash
$ python main.py

======================================================================
🎉 欢迎使用量化交易系统！ / Welcome to Quantitative Trading System!
======================================================================

[主菜单显示...]

请选择功能 / Please select an option: h

[帮助信息显示...]
```

### 示例 2: 浏览功能菜单

```bash
请选择功能 / Please select an option: 1

======================================================================
🎓 模型训练 / Model Training
======================================================================

⚠️  此功能将在后续任务中实现。
⚠️  This feature will be implemented in a future task.

[功能预览显示...]
```

## 获取更多帮助 / Get More Help

### 文档 / Documentation

- 查看 `docs/` 目录下的详细文档
- View detailed documentation in the `docs/` directory

### 示例代码 / Example Code

- 查看 `examples/` 目录下的示例
- View examples in the `examples/` directory

### 在线资源 / Online Resources

- qlib 官方文档: https://qlib.readthedocs.io/
- qlib GitHub: https://github.com/microsoft/qlib

## 常见问题 / FAQ

### Q: 如何退出系统？
**A:** 在主菜单输入 `q`，然后确认退出。

### Q: 如何中断当前操作？
**A:** 按 `Ctrl+C`，系统会询问是否退出。

### Q: 输入错误怎么办？
**A:** 系统会提示错误并允许重新输入。

### Q: 如何查看帮助？
**A:** 在主菜单输入 `h` 查看详细帮助信息。

### Q: 功能还未实现怎么办？
**A:** 部分功能将在后续任务中实现，当前会显示功能预览。

## 技术细节 / Technical Details

### 架构 / Architecture

CLI系统采用模块化设计：
- `MainCLI`: 主控制器，管理菜单和路由
- `InteractivePrompt`: 交互式输入收集器
- 功能处理器: 各个功能的具体实现

### 扩展性 / Extensibility

添加新功能只需：
1. 在 `menu_options` 中添加新选项
2. 实现对应的处理器方法
3. 更新帮助信息

### 国际化 / Internationalization

- 所有文本都是中英双语
- 易于扩展到其他语言
- 保持一致的用户体验

## 更新日志 / Changelog

### v1.0.0 (当前版本 / Current Version)

- ✅ 实现主菜单系统
- ✅ 实现帮助系统
- ✅ 实现功能路由
- ✅ 实现中文界面
- ✅ 实现交互式提示
- ⏳ 各功能模块待实现

## 贡献 / Contributing

欢迎贡献代码和建议！

Contributions and suggestions are welcome!

## 许可证 / License

本项目遵循 MIT 许可证。

This project is licensed under the MIT License.
