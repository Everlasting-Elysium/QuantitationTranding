# 示例和教程 / Examples and Tutorials

本目录包含量化交易系统的各种示例和教程，帮助您快速上手和深入理解系统功能。

This directory contains various examples and tutorials for the quantitative trading system to help you get started quickly and understand the system features in depth.

## 快速开始 / Quick Start

### 1. 最简单的示例 / Simplest Example

如果您是初学者，从这里开始：

If you are a beginner, start here:

```bash
python examples/demo_quick_start.py
```

这个示例展示了：
- 系统初始化 / System initialization
- 使用模板训练模型 / Train model using template
- 快速回测 / Quick backtest
- 查看结果 / View results

### 2. 完整端到端示例 / Complete End-to-End Example

了解完整的量化交易流程：

Understand the complete quantitative trading workflow:

```bash
python examples/demo_end_to_end.py
```

这个示例展示了：
- 系统初始化和配置 / System initialization and configuration
- 数据准备和验证 / Data preparation and validation
- 模型训练 / Model training
- 历史回测 / Historical backtesting
- 可视化分析 / Visualization analysis
- 交易信号生成 / Trading signal generation
- 信号解释 / Signal explanation

## 功能示例 / Feature Examples

### 数据管理 / Data Management

#### 完整数据管理示例 / Complete Data Management Example
```bash
python examples/demo_complete_data_management.py
```

展示内容 / Demonstrates:
- 数据下载方法 / Data download methods
- 数据验证 / Data validation
- 数据信息查询 / Data information query
- 数据更新策略 / Data update strategies

#### 基础数据管理示例 / Basic Data Management Example
```bash
python examples/demo_data_management.py
```

### 模型训练 / Model Training

#### 完整训练示例 / Complete Training Example
```bash
python examples/demo_complete_training.py
```

展示内容 / Demonstrates:
- 训练多种模型类型 / Train multiple model types
- 使用模板训练 / Train using templates
- 模型性能对比 / Model performance comparison
- 模型注册和管理 / Model registration and management

#### 基础训练示例 / Basic Training Examples
```bash
python examples/demo_training_manager.py
python examples/demo_model_factory.py
python examples/demo_model_templates.py
```

### 回测分析 / Backtest Analysis

#### 完整回测示例 / Complete Backtest Example
```bash
python examples/demo_complete_backtest.py
```

展示内容 / Demonstrates:
- 回测配置 / Backtest configuration
- 回测执行 / Backtest execution
- 性能指标分析 / Performance metrics analysis
- 可视化报告生成 / Visualization report generation
- 风险分析 / Risk analysis

#### 基础回测示例 / Basic Backtest Examples
```bash
python examples/demo_backtest_manager.py
python examples/demo_visualization_manager.py
python examples/demo_report_generator.py
```

### 交易信号 / Trading Signals

#### 信号生成和解释 / Signal Generation and Explanation
```bash
python examples/demo_signal_generator.py
python examples/demo_signal_explanation.py
```

展示内容 / Demonstrates:
- 交易信号生成 / Trading signal generation
- 信号解释 / Signal explanation
- 风险评估 / Risk assessment

### 系统组件 / System Components

#### 配置管理 / Configuration Management
```bash
python examples/demo_config_manager.py
```

#### 日志系统 / Logging System
```bash
python examples/demo_logger_system.py
```

#### Qlib封装 / Qlib Wrapper
```bash
python examples/demo_qlib_wrapper.py
```

#### 交互式提示 / Interactive Prompt
```bash
python examples/demo_interactive_prompt.py
```

#### 模型注册表 / Model Registry
```bash
python examples/demo_model_registry.py
```

## 示例分类 / Example Categories

### 按难度分类 / By Difficulty

#### 初级 / Beginner
- `demo_quick_start.py` - 快速开始 / Quick start
- `demo_config_manager.py` - 配置管理 / Configuration management
- `demo_logger_system.py` - 日志系统 / Logging system

#### 中级 / Intermediate
- `demo_training_manager.py` - 训练管理 / Training management
- `demo_backtest_manager.py` - 回测管理 / Backtest management
- `demo_signal_generator.py` - 信号生成 / Signal generation

#### 高级 / Advanced
- `demo_end_to_end.py` - 完整端到端流程 / Complete end-to-end workflow
- `demo_complete_training.py` - 完整训练流程 / Complete training workflow
- `demo_complete_backtest.py` - 完整回测流程 / Complete backtest workflow

### 按功能分类 / By Function

#### 数据相关 / Data Related
- `demo_complete_data_management.py` - 完整数据管理 / Complete data management
- `demo_qlib_wrapper.py` - Qlib封装 / Qlib wrapper

#### 模型相关 / Model Related
- `demo_complete_training.py` - 完整训练流程 / Complete training workflow
- `demo_training_manager.py` - 训练管理器 / Training manager
- `demo_model_factory.py` - 模型工厂 / Model factory
- `demo_model_templates.py` - 模型模板 / Model templates
- `demo_model_registry.py` - 模型注册表 / Model registry

#### 回测相关 / Backtest Related
- `demo_complete_backtest.py` - 完整回测流程 / Complete backtest workflow
- `demo_backtest_manager.py` - 回测管理器 / Backtest manager
- `demo_visualization_manager.py` - 可视化管理器 / Visualization manager
- `demo_report_generator.py` - 报告生成器 / Report generator

#### 交易相关 / Trading Related
- `demo_signal_generator.py` - 信号生成器 / Signal generator
- `demo_signal_explanation.py` - 信号解释 / Signal explanation

## 系统要求 / System Requirements

### 硬件要求 / Hardware Requirements
- 内存 / Memory: 16GB (推荐 / Recommended: 32GB)
- 磁盘空间 / Free Disk: 10GB (用于数据和模型 / For data and models)
- CPU: 4核心 / 4 cores (推荐 / Recommended: 8核心 / 8 cores)

### 软件要求 / Software Requirements
- Python: 3.8+
- 操作系统 / OS: Linux, macOS, Windows
- 依赖包 / Dependencies: 见 / See `requirements.txt`

## 数据准备 / Data Preparation

在运行示例之前，请先下载数据：

Before running examples, please download data first:

```bash
# 中国市场数据 / China market data
python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn

# 美国市场数据 / US market data (可选 / Optional)
python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/us_data --region us
```

## 运行示例 / Running Examples

### 基本步骤 / Basic Steps

1. 确保已安装依赖 / Ensure dependencies are installed:
```bash
pip install -r requirements.txt
```

2. 下载数据 / Download data:
```bash
python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn
```

3. 运行示例 / Run example:
```bash
python examples/demo_quick_start.py
```

### 常见问题 / Common Issues

#### 1. 数据未找到 / Data Not Found
```
错误 / Error: Qlib initialization failed
解决 / Solution: 下载数据 / Download data first
```

#### 2. 内存不足 / Out of Memory
```
错误 / Error: MemoryError
解决 / Solution: 减少数据量或增加内存 / Reduce data size or increase memory
```

#### 3. 依赖包缺失 / Missing Dependencies
```
错误 / Error: ModuleNotFoundError
解决 / Solution: pip install -r requirements.txt
```

## 学习路径 / Learning Path

### 第1天：基础入门 / Day 1: Basic Introduction
1. 阅读文档 / Read documentation: `docs/quick_start.md`
2. 运行快速开始示例 / Run quick start: `demo_quick_start.py`
3. 了解系统架构 / Understand architecture: `docs/user_guide.md`

### 第2天：数据管理 / Day 2: Data Management
1. 学习数据下载 / Learn data download: `demo_complete_data_management.py`
2. 理解数据验证 / Understand validation: `demo_qlib_wrapper.py`

### 第3天：模型训练 / Day 3: Model Training
1. 基础训练 / Basic training: `demo_training_manager.py`
2. 模板使用 / Template usage: `demo_model_templates.py`
3. 完整训练流程 / Complete workflow: `demo_complete_training.py`

### 第4天：回测分析 / Day 4: Backtest Analysis
1. 基础回测 / Basic backtest: `demo_backtest_manager.py`
2. 可视化分析 / Visualization: `demo_visualization_manager.py`
3. 完整回测流程 / Complete workflow: `demo_complete_backtest.py`

### 第5天：交易信号 / Day 5: Trading Signals
1. 信号生成 / Signal generation: `demo_signal_generator.py`
2. 信号解释 / Signal explanation: `demo_signal_explanation.py`

### 第6天：端到端实践 / Day 6: End-to-End Practice
1. 完整流程 / Complete workflow: `demo_end_to_end.py`
2. 自定义开发 / Custom development

## 进阶主题 / Advanced Topics

### 自定义模型 / Custom Models
参考 / Reference: `src/core/model_factory.py`

### 自定义策略 / Custom Strategies
参考 / Reference: `src/application/backtest_manager.py`

### 自定义指标 / Custom Metrics
参考 / Reference: `src/application/visualization_manager.py`

## 获取帮助 / Getting Help

- 文档 / Documentation: `docs/`
- API参考 / API Reference: `docs/api_reference.md`
- 用户指南 / User Guide: `docs/user_guide.md`
- 问题反馈 / Issue Tracker: GitHub Issues

## 注意事项 / Notes

1. **数据时效性 / Data Timeliness**
   - 示例使用的数据可能不是最新的 / Example data may not be up-to-date
   - 建议定期更新数据 / Recommend updating data regularly

2. **结果差异 / Result Variance**
   - 不同操作系统可能产生略微不同的结果 / Different OS may produce slightly different results
   - 年化收益率差异通常小于2% / Annual return variance usually less than 2%

3. **计算资源 / Computing Resources**
   - 某些示例需要较长时间运行 / Some examples may take long time to run
   - 建议在性能较好的机器上运行 / Recommend running on high-performance machines

4. **实盘交易警告 / Live Trading Warning**
   - 示例仅用于学习和研究 / Examples are for learning and research only
   - 实盘交易需要充分测试和风险评估 / Live trading requires thorough testing and risk assessment

## 贡献示例 / Contributing Examples

欢迎贡献新的示例！请遵循以下规范：

Welcome to contribute new examples! Please follow these guidelines:

1. 代码清晰易读 / Clear and readable code
2. 包含中英文注释 / Include bilingual comments
3. 提供详细的文档说明 / Provide detailed documentation
4. 测试通过 / Pass all tests

## 许可证 / License

本项目采用MIT许可证 / This project is licensed under the MIT License
