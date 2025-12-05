# 示例和教程指南 / Examples and Tutorials Guide

本指南详细介绍了系统提供的所有示例和教程，帮助您快速掌握量化交易系统的使用。

This guide provides detailed information about all examples and tutorials to help you quickly master the quantitative trading system.

## 目录 / Table of Contents

1. [快速开始](#快速开始--quick-start)
2. [完整示例](#完整示例--complete-examples)
3. [功能示例](#功能示例--feature-examples)
4. [学习路径](#学习路径--learning-path)
5. [常见问题](#常见问题--faq)

## 快速开始 / Quick Start

### 最简单的示例 / Simplest Example

**文件**: `examples/demo_quick_start.py`

**适合人群 / Suitable For**: 完全的初学者 / Complete beginners

**运行时间 / Runtime**: 约5-10分钟 / About 5-10 minutes

**功能说明 / Features**:
- 最小化的代码示例 / Minimal code example
- 快速体验完整流程 / Quick experience of complete workflow
- 自动使用默认配置 / Automatically uses default configuration

**运行方法 / How to Run**:
```bash
python examples/demo_quick_start.py
```

**预期输出 / Expected Output**:
```
[1/4] 初始化系统 / Initializing system...
✓ 系统初始化完成 / System initialized

[2/4] 训练模型 / Training model...
✓ 训练完成 / Training completed
  模型ID / Model ID: lgbm_20240101_120000

[3/4] 运行回测 / Running backtest...
✓ 回测完成 / Backtest completed

[4/4] 回测结果 / Backtest Results
年化收益率 / Annual Return: 15.23%
夏普比率 / Sharpe Ratio: 1.2345
最大回撤 / Max Drawdown: -8.45%
```

**下一步 / Next Steps**:
- 查看完整端到端示例 / View complete end-to-end example
- 学习各个功能模块 / Learn individual feature modules

---

## 完整示例 / Complete Examples

### 1. 完整端到端示例 / Complete End-to-End Example

**文件**: `examples/demo_end_to_end.py`

**适合人群 / Suitable For**: 想要了解完整流程的用户 / Users who want to understand the complete workflow

**运行时间 / Runtime**: 约15-20分钟 / About 15-20 minutes

**功能说明 / Features**:
1. **系统初始化** / System Initialization
   - 配置加载 / Configuration loading
   - 组件初始化 / Component initialization
   - 日志设置 / Logging setup

2. **数据准备** / Data Preparation
   - 数据验证 / Data validation
   - 数据信息查询 / Data information query

3. **模型训练** / Model Training
   - 数据集配置 / Dataset configuration
   - 模型训练 / Model training
   - 性能评估 / Performance evaluation

4. **历史回测** / Historical Backtesting
   - 回测配置 / Backtest configuration
   - 回测执行 / Backtest execution
   - 指标计算 / Metrics calculation

5. **可视化分析** / Visualization Analysis
   - 累计收益曲线 / Cumulative returns chart
   - 持仓分布图 / Position distribution chart

6. **报告生成** / Report Generation
   - 文本报告 / Text report
   - HTML报告 / HTML report

7. **交易信号生成** / Trading Signal Generation
   - 信号生成 / Signal generation
   - 信号排序 / Signal ranking

8. **信号解释** / Signal Explanation
   - 特征重要性 / Feature importance
   - 风险评估 / Risk assessment

**运行方法 / How to Run**:
```bash
python examples/demo_end_to_end.py
```

**生成的文件 / Generated Files**:
- `outputs/models/lgbm_*.pkl` - 训练的模型 / Trained model
- `outputs/visualizations/cumulative_returns.png` - 累计收益图 / Cumulative returns chart
- `outputs/visualizations/position_distribution.png` - 持仓分布图 / Position distribution chart
- `outputs/reports/backtest_report.txt` - 回测报告 / Backtest report

**关键代码片段 / Key Code Snippets**:

```python
# 训练模型 / Train model
training_result = training_manager.train_model(training_config)

# 运行回测 / Run backtest
backtest_result = backtest_manager.run_backtest(
    model_id=model_id,
    start_date="2022-01-01",
    end_date="2022-12-31",
    config=backtest_config
)

# 生成信号 / Generate signals
signals = signal_generator.generate_signals(
    model_id=model_id,
    date=signal_date,
    portfolio=current_portfolio
)
```

---

### 2. 完整数据管理示例 / Complete Data Management Example

**文件**: `examples/demo_complete_data_management.py`

**适合人群 / Suitable For**: 需要管理数据的用户 / Users who need to manage data

**运行时间 / Runtime**: 约5分钟 / About 5 minutes

**功能说明 / Features**:
1. **数据下载** / Data Download
   - 中国市场数据 / China market data
   - 美国市场数据 / US market data
   - 增量更新 / Incremental update

2. **数据验证** / Data Validation
   - 时间范围验证 / Time range validation
   - 数据完整性检查 / Data integrity check

3. **数据信息查询** / Data Information Query
   - 数据时间范围 / Data time range
   - 可用股票数量 / Available stock count

4. **数据更新策略** / Data Update Strategies
   - 增量更新 / Incremental update
   - 完全重新下载 / Complete re-download

**运行方法 / How to Run**:
```bash
python examples/demo_complete_data_management.py
```

**关键命令 / Key Commands**:
```bash
# 下载中国市场数据 / Download China market data
python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn

# 增量更新 / Incremental update
python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn --interval 1d

# 完全重新下载 / Complete re-download
python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn --delete_old
```

---

### 3. 完整模型训练示例 / Complete Model Training Example

**文件**: `examples/demo_complete_training.py`

**适合人群 / Suitable For**: 需要训练和对比多个模型的用户 / Users who need to train and compare multiple models

**运行时间 / Runtime**: 约20-30分钟 / About 20-30 minutes

**功能说明 / Features**:
1. **多模型训练** / Multi-Model Training
   - LightGBM模型 / LightGBM model
   - 线性模型 / Linear model
   - MLP模型 / MLP model

2. **模板训练** / Template Training
   - 使用预配置模板 / Use pre-configured templates
   - 快速训练 / Quick training

3. **模型对比** / Model Comparison
   - 性能指标对比 / Performance metrics comparison
   - 训练时间对比 / Training time comparison

4. **模型注册** / Model Registration
   - 模型版本管理 / Model version management
   - 生产模型标记 / Production model marking

5. **最佳模型选择** / Best Model Selection
   - 自动选择最佳模型 / Automatically select best model
   - 标记为生产模型 / Mark as production model

**运行方法 / How to Run**:
```bash
python examples/demo_complete_training.py
```

**预期输出 / Expected Output**:
```
模型性能对比表 / Model Performance Comparison Table:
--------------------------------------------------------------------------------
模型名称 / Model          IC           ICIR         训练时长 / Time
--------------------------------------------------------------------------------
LightGBM                 0.085234     1.234567     45.23s
Linear                   0.072145     0.987654     12.34s
Template_lgbm_alpha158   0.089123     1.345678     52.67s

最佳模型 / Best Model:
----------------------------------------
  模型名称 / Model name: Template_lgbm_alpha158
  IC: 0.089123
  ICIR: 1.345678
```

---

### 4. 完整回测示例 / Complete Backtest Example

**文件**: `examples/demo_complete_backtest.py`

**适合人群 / Suitable For**: 需要评估策略表现的用户 / Users who need to evaluate strategy performance

**运行时间 / Runtime**: 约10-15分钟 / About 10-15 minutes

**功能说明 / Features**:
1. **回测配置** / Backtest Configuration
   - 策略配置 / Strategy configuration
   - 执行器配置 / Executor configuration
   - 交易成本配置 / Trading cost configuration

2. **回测执行** / Backtest Execution
   - 信号生成 / Signal generation
   - 交易模拟 / Trade simulation
   - 持仓管理 / Position management

3. **性能分析** / Performance Analysis
   - 收益指标 / Return metrics
   - 风险指标 / Risk metrics
   - 交易统计 / Trading statistics

4. **可视化报告** / Visualization Reports
   - 累计收益曲线 / Cumulative returns chart
   - 持仓分布图 / Position distribution chart
   - 行业分布图 / Sector distribution chart

5. **风险分析** / Risk Analysis
   - 风险等级评估 / Risk level assessment
   - 收益质量评估 / Return quality assessment
   - 建议生成 / Recommendation generation

**运行方法 / How to Run**:
```bash
python examples/demo_complete_backtest.py
```

**生成的文件 / Generated Files**:
- `outputs/visualizations/backtest_cumulative_returns.png`
- `outputs/visualizations/backtest_position_distribution.png`
- `outputs/reports/complete_backtest_report.txt`

---

## 功能示例 / Feature Examples

### 数据管理 / Data Management

#### 1. Qlib封装示例 / Qlib Wrapper Example
**文件**: `examples/demo_qlib_wrapper.py`

**功能**: 演示如何使用Qlib封装层 / Demonstrates how to use Qlib wrapper

**关键功能 / Key Features**:
- Qlib初始化 / Qlib initialization
- 数据访问 / Data access
- 异常处理 / Exception handling

---

### 模型训练 / Model Training

#### 1. 训练管理器示例 / Training Manager Example
**文件**: `examples/demo_training_manager.py`

**功能**: 演示如何使用训练管理器 / Demonstrates how to use training manager

**关键功能 / Key Features**:
- 训练配置 / Training configuration
- 模型训练 / Model training
- MLflow追踪 / MLflow tracking

#### 2. 模型工厂示例 / Model Factory Example
**文件**: `examples/demo_model_factory.py`

**功能**: 演示如何创建不同类型的模型 / Demonstrates how to create different types of models

**关键功能 / Key Features**:
- 模型创建 / Model creation
- 参数配置 / Parameter configuration
- 模型类型 / Model types

#### 3. 模型模板示例 / Model Templates Example
**文件**: `examples/demo_model_templates.py`

**功能**: 演示如何使用模型模板 / Demonstrates how to use model templates

**关键功能 / Key Features**:
- 模板列表 / Template list
- 模板使用 / Template usage
- 自定义参数 / Custom parameters

#### 4. 模型注册表示例 / Model Registry Example
**文件**: `examples/demo_model_registry.py`

**功能**: 演示如何管理模型版本 / Demonstrates how to manage model versions

**关键功能 / Key Features**:
- 模型注册 / Model registration
- 版本管理 / Version management
- 生产模型标记 / Production model marking

---

### 回测分析 / Backtest Analysis

#### 1. 回测管理器示例 / Backtest Manager Example
**文件**: `examples/demo_backtest_manager.py`

**功能**: 演示如何运行回测 / Demonstrates how to run backtest

**关键功能 / Key Features**:
- 回测配置 / Backtest configuration
- 回测执行 / Backtest execution
- 指标计算 / Metrics calculation

#### 2. 可视化管理器示例 / Visualization Manager Example
**文件**: `examples/demo_visualization_manager.py`

**功能**: 演示如何生成可视化图表 / Demonstrates how to generate visualization charts

**关键功能 / Key Features**:
- 累计收益曲线 / Cumulative returns chart
- 持仓分布图 / Position distribution chart
- 行业分布图 / Sector distribution chart

#### 3. 报告生成器示例 / Report Generator Example
**文件**: `examples/demo_report_generator.py`

**功能**: 演示如何生成报告 / Demonstrates how to generate reports

**关键功能 / Key Features**:
- 训练报告 / Training report
- 回测报告 / Backtest report
- HTML报告 / HTML report

---

### 交易信号 / Trading Signals

#### 1. 信号生成器示例 / Signal Generator Example
**文件**: `examples/demo_signal_generator.py`

**功能**: 演示如何生成交易信号 / Demonstrates how to generate trading signals

**关键功能 / Key Features**:
- 信号生成 / Signal generation
- 风险控制 / Risk control
- 信号排序 / Signal ranking

#### 2. 信号解释示例 / Signal Explanation Example
**文件**: `examples/demo_signal_explanation.py`

**功能**: 演示如何解释交易信号 / Demonstrates how to explain trading signals

**关键功能 / Key Features**:
- 特征重要性 / Feature importance
- 风险评估 / Risk assessment
- 通俗解释 / Plain language explanation

---

### 系统组件 / System Components

#### 1. 配置管理器示例 / Config Manager Example
**文件**: `examples/demo_config_manager.py`

**功能**: 演示如何管理配置 / Demonstrates how to manage configuration

#### 2. 日志系统示例 / Logger System Example
**文件**: `examples/demo_logger_system.py`

**功能**: 演示如何使用日志系统 / Demonstrates how to use logging system

#### 3. 交互式提示示例 / Interactive Prompt Example
**文件**: `examples/demo_interactive_prompt.py`

**功能**: 演示如何使用交互式提示 / Demonstrates how to use interactive prompts

---

## 学习路径 / Learning Path

### 初学者路径 / Beginner Path

**第1周：基础入门 / Week 1: Basic Introduction**

Day 1-2: 系统安装和配置 / System Installation and Configuration
- 安装依赖 / Install dependencies
- 下载数据 / Download data
- 运行快速开始示例 / Run quick start example

Day 3-4: 数据管理 / Data Management
- 学习数据下载 / Learn data download
- 理解数据验证 / Understand data validation
- 运行数据管理示例 / Run data management examples

Day 5-7: 模型训练基础 / Model Training Basics
- 学习训练流程 / Learn training workflow
- 使用模板训练 / Use template training
- 运行训练示例 / Run training examples

**第2周：进阶功能 / Week 2: Advanced Features**

Day 1-3: 回测分析 / Backtest Analysis
- 学习回测配置 / Learn backtest configuration
- 理解性能指标 / Understand performance metrics
- 运行回测示例 / Run backtest examples

Day 4-5: 可视化和报告 / Visualization and Reports
- 生成图表 / Generate charts
- 创建报告 / Create reports
- 运行可视化示例 / Run visualization examples

Day 6-7: 交易信号 / Trading Signals
- 生成交易信号 / Generate trading signals
- 理解信号解释 / Understand signal explanation
- 运行信号示例 / Run signal examples

**第3周：实战应用 / Week 3: Practical Application**

Day 1-3: 完整流程实践 / Complete Workflow Practice
- 运行端到端示例 / Run end-to-end example
- 理解完整流程 / Understand complete workflow
- 自定义参数 / Customize parameters

Day 4-7: 项目开发 / Project Development
- 设计自己的策略 / Design your own strategy
- 训练和评估模型 / Train and evaluate models
- 生成交易信号 / Generate trading signals

---

### 进阶用户路径 / Advanced User Path

**模型优化 / Model Optimization**
1. 特征工程 / Feature engineering
2. 超参数调优 / Hyperparameter tuning
3. 模型集成 / Model ensemble

**策略开发 / Strategy Development**
1. 自定义策略 / Custom strategies
2. 风险管理 / Risk management
3. 组合优化 / Portfolio optimization

**系统扩展 / System Extension**
1. 自定义模型 / Custom models
2. 自定义指标 / Custom metrics
3. 自定义可视化 / Custom visualization

---

## 常见问题 / FAQ

### Q1: 示例运行失败怎么办？ / What if examples fail to run?

**A**: 检查以下几点 / Check the following:
1. 是否已安装所有依赖 / Are all dependencies installed?
   ```bash
   pip install -r requirements.txt
   ```

2. 是否已下载数据 / Is data downloaded?
   ```bash
   python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn
   ```

3. 检查Python版本 / Check Python version
   ```bash
   python --version  # Should be 3.8+
   ```

### Q2: 如何选择合适的示例？ / How to choose the right example?

**A**: 根据您的需求选择 / Choose based on your needs:
- **快速体验**: `demo_quick_start.py`
- **学习完整流程**: `demo_end_to_end.py`
- **学习特定功能**: 选择对应的功能示例 / Choose corresponding feature example

### Q3: 示例运行时间太长怎么办？ / What if examples take too long?

**A**: 可以尝试 / You can try:
1. 减少数据量 / Reduce data size
2. 减少训练轮数 / Reduce training epochs
3. 使用更快的模型 / Use faster models
4. 使用更强的硬件 / Use more powerful hardware

### Q4: 如何修改示例参数？ / How to modify example parameters?

**A**: 直接编辑示例文件 / Edit example files directly:
```python
# 修改数据集时间范围 / Modify dataset time range
dataset_config = DatasetConfig(
    instruments="csi300",
    start_time="2020-01-01",  # 修改这里 / Modify here
    end_time="2021-12-31",    # 修改这里 / Modify here
    ...
)

# 修改模型参数 / Modify model parameters
model_params = {
    "num_boost_round": 100,  # 修改这里 / Modify here
    "learning_rate": 0.1,    # 修改这里 / Modify here
}
```

### Q5: 如何保存和加载模型？ / How to save and load models?

**A**: 使用模型注册表 / Use model registry:
```python
# 保存模型 / Save model
model_registry.register_model(
    model_path=model_path,
    model_name="my_model",
    version="1.0"
)

# 加载模型 / Load model
model = model_registry.get_model(model_id)
```

### Q6: 如何查看MLflow UI？ / How to view MLflow UI?

**A**: 运行以下命令 / Run the following command:
```bash
mlflow ui --backend-store-uri ./examples/mlruns
```
然后访问 / Then visit: http://localhost:5000

### Q7: 如何自定义可视化？ / How to customize visualization?

**A**: 参考可视化管理器示例 / Refer to visualization manager example:
```python
visualization_manager.plot_cumulative_returns(
    returns=returns,
    benchmark=benchmark,
    save_path="custom_chart.png",
    title="自定义标题 / Custom Title",
    figsize=(12, 6)
)
```

### Q8: 如何处理不同市场的数据？ / How to handle data from different markets?

**A**: 使用不同的region参数 / Use different region parameters:
```python
# 中国市场 / China market
qlib_wrapper.init(provider_uri="~/.qlib/qlib_data/cn_data", region="cn")

# 美国市场 / US market
qlib_wrapper.init(provider_uri="~/.qlib/qlib_data/us_data", region="us")
```

---

## 获取更多帮助 / Getting More Help

- **文档 / Documentation**: `docs/`
- **API参考 / API Reference**: `docs/api_reference.md`
- **用户指南 / User Guide**: `docs/user_guide.md`
- **快速开始 / Quick Start**: `docs/quick_start.md`

---

## 贡献示例 / Contributing Examples

欢迎贡献新的示例！请遵循以下规范：

Welcome to contribute new examples! Please follow these guidelines:

1. **代码规范 / Code Standards**
   - 清晰的代码结构 / Clear code structure
   - 详细的注释 / Detailed comments
   - 中英文双语 / Bilingual (Chinese and English)

2. **文档要求 / Documentation Requirements**
   - 功能说明 / Feature description
   - 使用方法 / Usage instructions
   - 预期输出 / Expected output

3. **测试要求 / Testing Requirements**
   - 确保示例可以运行 / Ensure example can run
   - 提供测试数据 / Provide test data
   - 验证输出结果 / Verify output results

---

**最后更新 / Last Updated**: 2024-01-01

**版本 / Version**: 1.0.0
