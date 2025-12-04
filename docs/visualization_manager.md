# 可视化管理器文档 / Visualization Manager Documentation

## 概述 / Overview

可视化管理器（VisualizationManager）负责生成量化交易系统中的各种图表和可视化报告。它提供了一套完整的可视化工具，帮助用户直观地理解模型表现、投资组合分布和交易策略效果。

The Visualization Manager is responsible for generating various charts and visualization reports in the quantitative trading system. It provides a complete set of visualization tools to help users intuitively understand model performance, portfolio distribution, and trading strategy effectiveness.

## 主要功能 / Main Features

### 1. 累计收益曲线图 / Cumulative Returns Chart

生成策略收益与基准收益的对比曲线图，直观展示策略表现。

Generates comparison curves of strategy returns vs benchmark returns, visually displaying strategy performance.

**特点 / Features:**
- 支持策略与基准对比 / Supports strategy vs benchmark comparison
- 自动计算累计收益 / Automatically calculates cumulative returns
- 百分比格式显示 / Displays in percentage format
- 高分辨率输出 / High-resolution output

### 2. 持仓分布图 / Position Distribution Chart

以饼图形式展示投资组合中各股票的持仓比例。

Displays the position proportion of each stock in the portfolio as a pie chart.

**特点 / Features:**
- 饼图可视化 / Pie chart visualization
- 自动排序和分组 / Automatic sorting and grouping
- 显示持仓百分比 / Shows position percentages
- 支持大量持仓（自动合并小持仓）/ Supports large portfolios (auto-merges small positions)

### 3. 行业分布图 / Sector Distribution Chart

以柱状图形式展示投资组合的行业配置情况。

Displays the sector allocation of the portfolio as a bar chart.

**特点 / Features:**
- 柱状图可视化 / Bar chart visualization
- 按权重排序 / Sorted by weight
- 百分比标注 / Percentage labels
- 清晰的行业对比 / Clear sector comparison

### 4. 多模型对比图 / Multi-Model Comparison Chart

对比多个模型的收益曲线和性能指标。

Compares return curves and performance metrics of multiple models.

**特点 / Features:**
- 双子图布局 / Dual subplot layout
- 累计收益曲线对比 / Cumulative returns comparison
- 性能指标柱状图 / Performance metrics bar chart
- 支持任意数量模型 / Supports any number of models

### 5. 训练曲线图 / Training Curve Chart

展示模型训练过程中的指标变化。

Displays metric changes during model training.

**特点 / Features:**
- 多指标同时展示 / Multiple metrics displayed simultaneously
- 轮次追踪 / Epoch tracking
- 趋势可视化 / Trend visualization

### 6. 完整报告生成 / Complete Report Generation

一键生成包含多个图表的完整可视化报告。

Generates a complete visualization report with multiple charts in one click.

**特点 / Features:**
- 自动生成多个图表 / Automatically generates multiple charts
- 统一的输出目录 / Unified output directory
- 返回所有图表路径 / Returns all chart paths

## 使用方法 / Usage

### 基本使用 / Basic Usage

```python
from src.application.visualization_manager import VisualizationManager

# 创建可视化管理器 / Create visualization manager
viz_manager = VisualizationManager(output_dir="./outputs/visualizations")

# 绘制累计收益曲线 / Plot cumulative returns
chart_path = viz_manager.plot_cumulative_returns(
    returns=strategy_returns,
    benchmark=benchmark_returns
)
```

### 累计收益曲线 / Cumulative Returns

```python
import pandas as pd

# 准备收益率数据 / Prepare returns data
strategy_returns = pd.Series([0.01, 0.02, -0.01, 0.03, ...])
benchmark_returns = pd.Series([0.008, 0.015, -0.005, 0.02, ...])

# 绘制图表 / Plot chart
chart_path = viz_manager.plot_cumulative_returns(
    returns=strategy_returns,
    benchmark=benchmark_returns,
    save_path="./my_returns.png",
    title="我的策略收益 / My Strategy Returns"
)
```

### 持仓分布 / Position Distribution

```python
# 准备持仓数据 / Prepare portfolio data
portfolio = {
    "贵州茅台 600519": 0.15,
    "宁德时代 300750": 0.12,
    "比亚迪 002594": 0.10,
    # ... 更多持仓 / more positions
}

# 绘制图表 / Plot chart
chart_path = viz_manager.plot_position_distribution(
    portfolio=portfolio,
    title="当前持仓分布 / Current Position Distribution"
)
```

### 行业分布 / Sector Distribution

```python
# 准备行业数据 / Prepare sector data
sector_weights = {
    "食品饮料": 0.21,
    "新能源": 0.20,
    "汽车": 0.15,
    "金融": 0.15,
    # ... 更多行业 / more sectors
}

# 绘制图表 / Plot chart
chart_path = viz_manager.plot_sector_distribution(
    sector_weights=sector_weights,
    title="行业配置 / Sector Allocation"
)
```

### 多模型对比 / Multi-Model Comparison

```python
# 准备多个模型的收益数据 / Prepare returns data for multiple models
model_returns = {
    "LightGBM": lgbm_returns,
    "Linear Model": linear_returns,
    "MLP": mlp_returns,
}

# 绘制对比图 / Plot comparison chart
chart_path = viz_manager.plot_multi_model_comparison(
    model_returns=model_returns,
    title="模型性能对比 / Model Performance Comparison"
)
```

### 训练曲线 / Training Curve

```python
# 准备训练指标数据 / Prepare training metrics data
metrics = {
    "训练损失": [1.0, 0.8, 0.6, 0.5, ...],
    "验证损失": [1.0, 0.85, 0.7, 0.6, ...],
    "训练IC": [0.02, 0.04, 0.06, 0.08, ...],
}

# 绘制训练曲线 / Plot training curve
chart_path = viz_manager.plot_training_curve(
    metrics=metrics,
    title="模型训练过程 / Model Training Process"
)
```

### 完整报告 / Complete Report

```python
# 一键生成完整报告 / Generate complete report in one click
chart_paths = viz_manager.create_report_with_charts(
    returns=strategy_returns,
    portfolio=portfolio,
    sector_weights=sector_weights,
    benchmark=benchmark_returns,
    output_dir="./reports/backtest_20240101"
)

# 获取所有图表路径 / Get all chart paths
print(chart_paths['cumulative_returns'])
print(chart_paths['position_distribution'])
print(chart_paths['sector_distribution'])
```

## 配置选项 / Configuration Options

### 输出目录 / Output Directory

```python
# 自定义输出目录 / Custom output directory
viz_manager = VisualizationManager(output_dir="./my_charts")
```

### 图表样式 / Chart Style

可视化管理器自动配置以下样式：
The visualization manager automatically configures the following styles:

- 中文字体支持 / Chinese font support
- 高分辨率输出（300 DPI）/ High-resolution output (300 DPI)
- 专业配色方案 / Professional color scheme
- 网格和图例 / Grid and legend

### 保存路径 / Save Path

```python
# 指定保存路径 / Specify save path
chart_path = viz_manager.plot_cumulative_returns(
    returns=returns,
    save_path="./specific/path/my_chart.png"
)

# 自动生成路径（带时间戳）/ Auto-generate path (with timestamp)
chart_path = viz_manager.plot_cumulative_returns(
    returns=returns
)  # 保存到 output_dir/cumulative_returns_20240101_120000.png
```

## 最佳实践 / Best Practices

### 1. 数据准备 / Data Preparation

确保输入数据格式正确：
Ensure input data format is correct:

```python
# 收益率应该是 pandas.Series / Returns should be pandas.Series
returns = pd.Series(data, index=dates)

# 持仓应该是字典 / Portfolio should be dict
portfolio = {"symbol": weight, ...}

# 权重总和应该接近1.0 / Weights should sum to approximately 1.0
assert abs(sum(portfolio.values()) - 1.0) < 0.01
```

### 2. 错误处理 / Error Handling

```python
try:
    chart_path = viz_manager.plot_cumulative_returns(returns)
except VisualizationManagerError as e:
    print(f"可视化失败 / Visualization failed: {e}")
```

### 3. 批量生成 / Batch Generation

```python
# 使用完整报告功能批量生成 / Use complete report for batch generation
chart_paths = viz_manager.create_report_with_charts(
    returns=returns,
    portfolio=portfolio,
    sector_weights=sector_weights,
    benchmark=benchmark
)
```

### 4. 内存管理 / Memory Management

可视化管理器会自动关闭图表以释放内存：
The visualization manager automatically closes charts to free memory:

```python
# 不需要手动关闭 / No need to manually close
chart_path = viz_manager.plot_cumulative_returns(returns)
# matplotlib figure 已自动关闭 / matplotlib figure is auto-closed
```

## 示例程序 / Example Programs

完整的示例程序请参考：
For complete example programs, please refer to:

```bash
python examples/demo_visualization_manager.py
```

该示例展示了所有可视化功能的使用方法。
This example demonstrates the usage of all visualization features.

## 技术细节 / Technical Details

### 依赖库 / Dependencies

- matplotlib: 图表绘制 / Chart plotting
- seaborn: 样式增强 / Style enhancement
- pandas: 数据处理 / Data processing
- numpy: 数值计算 / Numerical computation

### 图表格式 / Chart Format

- 格式 / Format: PNG
- 分辨率 / Resolution: 300 DPI
- 尺寸 / Size: 12x6 英寸（可配置）/ 12x6 inches (configurable)

### 中文支持 / Chinese Support

系统会自动尝试以下中文字体：
The system automatically tries the following Chinese fonts:

1. SimHei（黑体）
2. Microsoft YaHei（微软雅黑）
3. STSong（华文宋体）
4. Arial Unicode MS（Mac系统）

## 常见问题 / FAQ

### Q1: 中文显示为方块？/ Chinese displays as squares?

**A:** 确保系统安装了中文字体。在Linux系统上可以安装：
Ensure Chinese fonts are installed on the system. On Linux:

```bash
sudo apt-get install fonts-wqy-microhei
```

### Q2: 图表太小看不清？/ Charts too small to see clearly?

**A:** 可以在保存后用图片查看器放大，或修改DPI设置：
You can zoom in with an image viewer after saving, or modify DPI settings:

```python
plt.rcParams['savefig.dpi'] = 600  # 更高分辨率 / Higher resolution
```

### Q3: 如何自定义颜色？/ How to customize colors?

**A:** 当前版本使用预设配色方案。如需自定义，可以修改源代码中的颜色定义。
Current version uses preset color schemes. For customization, modify color definitions in source code.

### Q4: 支持其他图表格式吗？/ Support other chart formats?

**A:** 当前仅支持PNG。如需其他格式，可以修改保存路径的扩展名：
Currently only PNG is supported. For other formats, modify the save path extension:

```python
chart_path = viz_manager.plot_cumulative_returns(
    returns=returns,
    save_path="./chart.pdf"  # 或 .svg, .jpg 等 / or .svg, .jpg, etc.
)
```

## 更新日志 / Changelog

### v1.0.0 (2024-01-01)

- ✓ 实现累计收益曲线图 / Implemented cumulative returns chart
- ✓ 实现持仓分布图 / Implemented position distribution chart
- ✓ 实现行业分布图 / Implemented sector distribution chart
- ✓ 实现多模型对比图 / Implemented multi-model comparison chart
- ✓ 实现训练曲线图 / Implemented training curve chart
- ✓ 实现完整报告生成 / Implemented complete report generation
- ✓ 支持中文显示 / Added Chinese display support
- ✓ 高分辨率输出 / High-resolution output

## 相关文档 / Related Documentation

- [回测管理器文档](./backtest_manager.md)
- [训练管理器文档](./training_manager.md)
- [报告生成器文档](./report_generator.md)

## 联系支持 / Contact Support

如有问题或建议，请提交Issue或联系开发团队。
For questions or suggestions, please submit an Issue or contact the development team.
