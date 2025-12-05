# 训练功能CLI使用指南 / Training CLI Usage Guide

## 概述 / Overview

训练功能CLI提供了一个交互式的命令行界面，让用户可以通过简单的问答方式完成模型训练，无需编写代码。

The Training CLI provides an interactive command-line interface that allows users to complete model training through simple Q&A, without writing code.

## 功能特性 / Features

### 1. 模板选择界面 / Template Selection Interface

系统提供了5个预配置的模型模板：

The system provides 5 pre-configured model templates:

- **lgbm_default**: 默认LightGBM模型，适合大多数场景
  - Default LightGBM model, suitable for most scenarios
  
- **linear_default**: 线性回归模型，简单稳定，可解释性强
  - Linear regression model, simple, stable, highly interpretable
  
- **mlp_default**: 多层神经网络模型，适合捕捉复杂非线性关系
  - Multi-layer neural network model, suitable for capturing complex non-linear relationships
  
- **lgbm_conservative**: 保守型LightGBM模型，降低风险，追求稳定收益
  - Conservative LightGBM model, reduces risk, pursues stable returns
  
- **lgbm_aggressive**: 进取型LightGBM模型，追求高收益，可承受较高风险
  - Aggressive LightGBM model, pursues high returns, can tolerate higher risk

### 2. 交互式参数配置 / Interactive Parameter Configuration

通过问答方式收集以下参数：

Collects the following parameters through Q&A:

- 模型模板选择 / Model template selection
- 股票池选择（csi300, csi500, csi800等）/ Stock pool selection (csi300, csi500, csi800, etc.)
- 训练时间范围 / Training time range
- 实验名称 / Experiment name
- 自定义参数（可选）/ Custom parameters (optional)

### 3. 实时进度显示 / Real-time Progress Display

训练过程中显示：

Displays during training:

- 训练状态提示 / Training status hints
- 进度信息 / Progress information
- 预计完成时间 / Estimated completion time

### 4. 详细结果展示 / Detailed Results Display

训练完成后展示：

Displays after training:

- 模型ID / Model ID
- 训练时长 / Training time
- 评估指标（IC、预测数量等）/ Evaluation metrics (IC, prediction count, etc.)
- 模型保存路径 / Model save path
- MLflow实验ID和运行ID / MLflow experiment ID and run ID

### 5. MLflow集成 / MLflow Integration

自动记录到MLflow：

Automatically logs to MLflow:

- 训练参数 / Training parameters
- 评估指标 / Evaluation metrics
- 模型文件 / Model files
- 训练时长 / Training time

## 使用步骤 / Usage Steps

### 步骤1：启动主CLI / Step 1: Start Main CLI

```bash
python main.py
```

### 步骤2：选择模型训练 / Step 2: Select Model Training

在主菜单中输入 `1` 选择"模型训练"功能。

Enter `1` in the main menu to select "Model Training" feature.

### 步骤3：选择训练方式 / Step 3: Select Training Method

系统会显示两个选项：

The system will display two options:

1. 使用模型模板训练（推荐）/ Train with model template (recommended)
2. 自定义参数训练（高级）/ Train with custom parameters (advanced)

**推荐选择选项1**，使用模板训练更简单快捷。

**Recommend selecting option 1**, training with templates is simpler and faster.

### 步骤4：选择模型模板 / Step 4: Select Model Template

系统会列出所有可用的模板，每个模板都有详细的描述和适用场景。

The system will list all available templates, each with detailed descriptions and use cases.

根据你的需求选择合适的模板：

Select the appropriate template based on your needs:

- 如果追求稳定收益，选择 `lgbm_conservative`
  - If pursuing stable returns, select `lgbm_conservative`
  
- 如果追求平衡，选择 `lgbm_default`
  - If pursuing balance, select `lgbm_default`
  
- 如果追求高收益，选择 `lgbm_aggressive`
  - If pursuing high returns, select `lgbm_aggressive`

### 步骤5：配置数据集 / Step 5: Configure Dataset

#### 5.1 选择股票池 / Select Stock Pool

系统提供以下选项：

The system provides the following options:

- csi300 (沪深300)
- csi500 (中证500)
- csi800 (中证800)
- 自定义 / Custom

**建议选择 csi300**，这是最常用的股票池。

**Recommend selecting csi300**, this is the most commonly used stock pool.

#### 5.2 设置时间范围 / Set Time Range

输入开始日期和结束日期，格式为 `YYYY-MM-DD`。

Enter start date and end date in format `YYYY-MM-DD`.

**建议使用至少2年的历史数据**，例如：

**Recommend using at least 2 years of historical data**, for example:

- 开始日期 / Start date: 2020-01-01
- 结束日期 / End date: 2023-12-31

### 步骤6：自定义参数（可选）/ Step 6: Customize Parameters (Optional)

系统会询问是否需要自定义模型参数。

The system will ask if you need to customize model parameters.

- 如果选择"是"，可以调整模型的超参数（当前版本将使用默认参数）
  - If selecting "yes", you can adjust model hyperparameters (current version will use default parameters)
  
- 如果选择"否"，将使用模板的默认参数（推荐）
  - If selecting "no", will use template default parameters (recommended)

### 步骤7：输入实验名称 / Step 7: Enter Experiment Name

输入一个有意义的实验名称，方便后续查找。

Enter a meaningful experiment name for easy lookup later.

**命名建议**：包含模型类型、股票池和日期

**Naming suggestion**: Include model type, stock pool, and date

例如 / Example: `lgbm_csi300_20240101`

### 步骤8：确认配置 / Step 8: Confirm Configuration

系统会显示完整的训练配置，包括：

The system will display the complete training configuration, including:

- 模板名称 / Template name
- 股票池 / Stock pool
- 开始日期 / Start date
- 结束日期 / End date
- 实验名称 / Experiment name

确认无误后，输入"是"开始训练。

After confirming, enter "yes" to start training.

### 步骤9：等待训练完成 / Step 9: Wait for Training to Complete

训练过程中会显示进度提示。训练时间取决于：

Progress hints will be displayed during training. Training time depends on:

- 数据量大小 / Data size
- 模型复杂度 / Model complexity
- 硬件性能 / Hardware performance

通常需要几分钟到十几分钟。

Usually takes several minutes to tens of minutes.

### 步骤10：查看训练结果 / Step 10: View Training Results

训练完成后，系统会显示：

After training completes, the system will display:

- ✅ 训练完成提示 / Training completed message
- 模型ID / Model ID
- 训练时长 / Training time
- 评估指标 / Evaluation metrics
- 模型保存路径 / Model save path
- MLflow实验信息 / MLflow experiment information

## 使用技巧 / Tips and Tricks

### 1. 选择合适的模板 / Choose the Right Template

根据你的投资风格和风险偏好选择模板：

Choose template based on your investment style and risk preference:

| 风险偏好 / Risk Preference | 推荐模板 / Recommended Template | 特点 / Features |
|---------------------------|--------------------------------|----------------|
| 保守型 / Conservative | lgbm_conservative | 低风险、稳定收益 / Low risk, stable returns |
| 稳健型 / Moderate | lgbm_default | 平衡风险收益 / Balanced risk-return |
| 进取型 / Aggressive | lgbm_aggressive | 高收益、高风险 / High returns, high risk |

### 2. 合理设置时间范围 / Set Reasonable Time Range

- **最少2年数据**：确保模型有足够的训练样本
  - **Minimum 2 years data**: Ensure model has sufficient training samples
  
- **避免过短时间**：时间太短可能导致过拟合
  - **Avoid too short time**: Too short may lead to overfitting
  
- **考虑市场周期**：包含完整的牛熊市周期更好
  - **Consider market cycles**: Including complete bull-bear cycles is better

### 3. 使用MLflow追踪 / Use MLflow Tracking

训练完成后，可以使用MLflow UI查看详细记录：

After training, you can use MLflow UI to view detailed records:

```bash
mlflow ui
```

然后在浏览器中打开 `http://localhost:5000`

Then open `http://localhost:5000` in browser

在MLflow UI中可以：

In MLflow UI you can:

- 查看所有实验和运行 / View all experiments and runs
- 对比不同模型的性能 / Compare performance of different models
- 查看训练曲线 / View training curves
- 下载模型文件 / Download model files

### 4. 实验命名规范 / Experiment Naming Convention

使用有意义的实验名称，建议格式：

Use meaningful experiment names, suggested format:

```
{模型类型}_{股票池}_{日期}_{备注}
{model_type}_{stock_pool}_{date}_{note}
```

例如 / Examples:

- `lgbm_csi300_20240101_baseline`
- `lgbm_conservative_csi500_20240115_test`
- `mlp_csi800_20240201_experiment`

### 5. 保存训练记录 / Save Training Records

建议记录每次训练的关键信息：

Recommend recording key information for each training:

- 训练日期和时间 / Training date and time
- 使用的模板 / Template used
- 数据集配置 / Dataset configuration
- 训练结果指标 / Training result metrics
- 模型ID / Model ID

可以创建一个Excel或文本文件来记录这些信息。

You can create an Excel or text file to record this information.

## 常见问题 / FAQ

### Q1: 训练失败怎么办？ / What to do if training fails?

**A**: 检查以下几点：

**A**: Check the following:

1. 确保qlib数据已下载 / Ensure qlib data is downloaded
2. 检查时间范围是否有效 / Check if time range is valid
3. 查看错误日志了解具体原因 / View error logs for specific reasons
4. 尝试使用更短的时间范围 / Try using shorter time range

### Q2: 如何选择最佳模板？ / How to choose the best template?

**A**: 建议先使用 `lgbm_default` 作为基准，然后根据回测结果决定是否需要更保守或更激进的策略。

**A**: Recommend starting with `lgbm_default` as baseline, then decide if you need more conservative or aggressive strategy based on backtest results.

### Q3: 训练需要多长时间？ / How long does training take?

**A**: 取决于多个因素：

**A**: Depends on multiple factors:

- 数据量：2年数据通常需要5-10分钟 / Data size: 2 years data usually takes 5-10 minutes
- 模型类型：MLP比LGBM慢 / Model type: MLP is slower than LGBM
- 硬件：GPU可以加速MLP训练 / Hardware: GPU can accelerate MLP training

### Q4: 可以同时训练多个模型吗？ / Can I train multiple models simultaneously?

**A**: 当前版本不支持并行训练，但可以依次训练多个模型。未来版本会支持批量训练。

**A**: Current version doesn't support parallel training, but you can train multiple models sequentially. Future versions will support batch training.

### Q5: 训练的模型保存在哪里？ / Where are trained models saved?

**A**: 模型保存在 `outputs/models/{model_id}/` 目录下，包含：

**A**: Models are saved in `outputs/models/{model_id}/` directory, including:

- `model.pkl`: 模型文件 / Model file
- `config.json`: 配置文件 / Configuration file

### Q6: 如何使用训练好的模型？ / How to use trained models?

**A**: 训练完成后，可以通过以下方式使用模型：

**A**: After training, you can use the model through:

1. 在"历史回测"功能中选择该模型进行回测
   - Select the model in "Historical Backtest" feature for backtesting
   
2. 在"信号生成"功能中使用该模型生成交易信号
   - Use the model in "Signal Generation" feature to generate trading signals
   
3. 通过模型ID加载模型进行预测
   - Load model by model ID for prediction

## 下一步 / Next Steps

训练完成后，建议进行以下操作：

After training, recommend the following operations:

1. **历史回测** / Historical Backtest
   - 使用训练好的模型进行历史回测
   - Use trained model for historical backtesting
   - 评估模型在历史数据上的表现
   - Evaluate model performance on historical data

2. **信号生成** / Signal Generation
   - 生成最新的交易信号
   - Generate latest trading signals
   - 查看模型的预测结果
   - View model prediction results

3. **模型对比** / Model Comparison
   - 训练多个不同的模型
   - Train multiple different models
   - 在MLflow中对比它们的性能
   - Compare their performance in MLflow

4. **参数优化** / Parameter Optimization
   - 根据回测结果调整模型参数
   - Adjust model parameters based on backtest results
   - 重新训练并对比效果
   - Retrain and compare results

## 相关文档 / Related Documentation

- [快速开始指南](quick_start.md) / Quick Start Guide
- [用户手册](user_guide.md) / User Manual
- [API参考](api_reference.md) / API Reference
- [MLflow使用指南](mlflow_guide.md) / MLflow Usage Guide

## 技术支持 / Technical Support

如有问题，请查看：

If you have questions, please check:

- 项目文档：`docs/` 目录 / Project documentation: `docs/` directory
- 示例代码：`examples/` 目录 / Example code: `examples/` directory
- 在线文档：https://qlib.readthedocs.io/ / Online documentation: https://qlib.readthedocs.io/

---

**版本 / Version**: 1.0  
**更新日期 / Last Updated**: 2024-01-01  
**作者 / Author**: Qlib Trading System Team
