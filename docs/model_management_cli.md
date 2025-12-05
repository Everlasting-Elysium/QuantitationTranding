# 模型管理CLI使用指南 / Model Management CLI Usage Guide

## 概述 / Overview

模型管理功能提供了完整的模型生命周期管理，包括查看、详情、设置生产模型和删除等操作。

The model management feature provides complete model lifecycle management, including viewing, details, setting production models, and deletion.

## 功能特性 / Features

### 1. 查看模型列表 / View Model List

查看所有已注册的模型，支持按状态和类型过滤。

View all registered models with filtering by status and type.

**功能 / Functionality:**
- 显示所有模型的基本信息 / Display basic information of all models
- 支持按状态过滤（已注册、候选、生产、已归档）/ Filter by status (registered, candidate, production, archived)
- 支持按模型类型过滤 / Filter by model type
- 显示关键性能指标 / Display key performance metrics
- 显示状态统计 / Display status statistics

**使用步骤 / Usage Steps:**

1. 在主菜单选择 "5. 模型管理 / Model Management"
2. 选择 "查看模型列表 / View model list"
3. 选择是否需要过滤
4. 如果需要过滤，选择状态和模型类型
5. 查看模型列表

**示例输出 / Example Output:**

```
找到 5 个模型 / Found 5 models
======================================================================

1. 🚀 lgbm_model (v1.0)
   模型ID / Model ID: lgbm_model_v1.0
   模型类型 / Model Type: lgbm
   训练日期 / Training Date: 2024-01-15
   状态 / Status: production
   性能指标 / Performance Metrics:
     - ic_mean: 0.045678
     - icir: 0.234567
     - rank_ic_mean: 0.056789

2. ⭐ lgbm_model (v2.0)
   模型ID / Model ID: lgbm_model_v2.0
   模型类型 / Model Type: lgbm
   训练日期 / Training Date: 2024-01-20
   状态 / Status: candidate
   性能指标 / Performance Metrics:
     - ic_mean: 0.052345
     - icir: 0.267890
     - rank_ic_mean: 0.063456
   💡 性能提升 / Performance Improvement: +14.59%
```

**状态说明 / Status Description:**

- 📝 **registered**: 已注册，新训练的模型 / Registered, newly trained model
- ⭐ **candidate**: 候选模型，性能优于当前生产模型 / Candidate, better performance than current production
- 🚀 **production**: 生产模型，当前用于实际预测 / Production, currently used for predictions
- 📦 **archived**: 已归档，不再使用的旧模型 / Archived, old models no longer in use

### 2. 查看模型详情 / View Model Details

查看特定模型的完整信息，包括数据集、超参数、性能指标等。

View complete information of a specific model, including dataset, hyperparameters, and performance metrics.

**功能 / Functionality:**
- 显示模型的完整元数据 / Display complete model metadata
- 显示数据集配置信息 / Display dataset configuration
- 显示所有超参数 / Display all hyperparameters
- 显示所有性能指标 / Display all performance metrics
- 显示文件路径 / Display file paths
- 支持设置为生产模型 / Support setting as production model
- 支持导出模型信息 / Support exporting model information

**使用步骤 / Usage Steps:**

1. 在主菜单选择 "5. 模型管理 / Model Management"
2. 选择 "查看模型详情 / View model details"
3. 从列表中选择要查看的模型
4. 查看详细信息
5. 可选：设置为生产模型或导出信息

**示例输出 / Example Output:**

```
======================================================================
📊 模型详细信息 / Model Detailed Information
======================================================================

【基本信息 / Basic Information】
  模型ID / Model ID: lgbm_model_v2.0
  模型名称 / Model Name: lgbm_model
  版本 / Version: 2.0
  模型类型 / Model Type: lgbm
  训练日期 / Training Date: 2024-01-20
  状态 / Status: candidate
  注册时间 / Registered At: 2024-01-20T15:30:45

【数据集信息 / Dataset Information】
  股票池 / Instruments: csi300
  开始时间 / Start Time: 2020-01-01
  结束时间 / End Time: 2023-12-31
  标签 / Label: Ref($close, -2) / Ref($close, -1) - 1
  特征数量 / Number of Features: 158

【超参数 / Hyperparameters】
  model_type: lgbm
  learning_rate: 0.05
  num_leaves: 31
  max_depth: -1
  n_estimators: 100

【性能指标 / Performance Metrics】
  ic_mean: 0.052345
  icir: 0.267890
  rank_ic_mean: 0.063456
  rank_icir: 0.345678
  ...

【文件路径 / File Paths】
  模型文件 / Model File: ./model_registry/lgbm_model_v2.0/model.pkl
  元数据文件 / Metadata File: ./model_registry/lgbm_model_v2.0/metadata.json
```

### 3. 设置生产模型 / Set Production Model

将模型设置为生产模型，用于实际的信号生成和回测。

Set a model as the production model for actual signal generation and backtesting.

**功能 / Functionality:**
- 显示当前生产模型 / Display current production model
- 显示候选模型和已注册模型 / Display candidate and registered models
- 显示性能对比 / Display performance comparison
- 自动将旧生产模型降级为候选 / Automatically demote old production model to candidate
- 确认机制防止误操作 / Confirmation mechanism to prevent mistakes

**使用步骤 / Usage Steps:**

1. 在主菜单选择 "5. 模型管理 / Model Management"
2. 选择 "设置生产模型 / Set production model"
3. 查看当前生产模型（如果有）
4. 从候选模型和已注册模型中选择
5. 确认设置

**示例输出 / Example Output:**

```
当前生产模型 / Current Production Model:
  lgbm_model (v1.0)
  模型ID / Model ID: lgbm_model_v1.0
  训练日期 / Training Date: 2024-01-15
  性能指标 / Performance Metrics:
    - ic_mean: 0.045678
    - icir: 0.234567
    - rank_ic_mean: 0.056789

可选模型 / Available Models (2):
----------------------------------------------------------------------

1. ⭐ lgbm_model (v2.0)
   模型ID / Model ID: lgbm_model_v2.0
   训练日期 / Training Date: 2024-01-20
   状态 / Status: candidate
   性能指标 / Performance Metrics:
     - ic_mean: 0.052345
     - icir: 0.267890
     - rank_ic_mean: 0.063456
   💡 性能提升 / Performance Improvement: +14.59%

2. 📝 linear_model (v1.0)
   模型ID / Model ID: linear_model_v1.0
   训练日期 / Training Date: 2024-01-18
   状态 / Status: registered
   性能指标 / Performance Metrics:
     - ic_mean: 0.038901
     - icir: 0.198765
     - rank_ic_mean: 0.045678
```

**注意事项 / Notes:**

- 只能设置候选模型或已注册模型为生产模型 / Can only set candidate or registered models as production
- 设置新生产模型后，旧生产模型会自动降级为候选模型 / Old production model is automatically demoted to candidate
- 生产模型用于所有后续的信号生成和回测 / Production model is used for all subsequent signal generation and backtesting

### 4. 删除模型 / Delete Model

从注册表中删除不再需要的模型。

Delete models that are no longer needed from the registry.

**功能 / Functionality:**
- 显示可删除的模型（非生产模型）/ Display deletable models (non-production)
- 双重确认机制 / Double confirmation mechanism
- 永久删除模型文件和元数据 / Permanently delete model files and metadata
- 保护生产模型不被删除 / Protect production models from deletion

**使用步骤 / Usage Steps:**

1. 在主菜单选择 "5. 模型管理 / Model Management"
2. 选择 "删除模型 / Delete model"
3. 从可删除模型列表中选择
4. 第一次确认删除
5. 第二次确认删除
6. 模型被永久删除

**示例输出 / Example Output:**

```
可删除的模型 / Deletable Models (3):
----------------------------------------------------------------------

1. 📝 lgbm_model (v0.9)
   模型ID / Model ID: lgbm_model_v0.9
   训练日期 / Training Date: 2024-01-10
   状态 / Status: registered

2. 📦 linear_model (v0.5)
   模型ID / Model ID: linear_model_v0.5
   训练日期 / Training Date: 2024-01-05
   状态 / Status: archived

======================================================================
⚠️  删除确认 / Deletion Confirmation
======================================================================

即将删除以下模型 / About to delete the following model:
  模型名称 / Model Name: lgbm_model (v0.9)
  模型ID / Model ID: lgbm_model_v0.9
  训练日期 / Training Date: 2024-01-10

⚠️  警告 / Warning:
  • 删除操作不可恢复 / Deletion cannot be undone
  • 模型文件和元数据将被永久删除 / Model files and metadata will be permanently deleted
```

**注意事项 / Notes:**

- 生产模型不能被删除 / Production models cannot be deleted
- 删除操作不可恢复 / Deletion cannot be undone
- 需要双重确认以防止误操作 / Requires double confirmation to prevent mistakes
- 删除后模型文件和元数据将被永久删除 / Model files and metadata are permanently deleted

## 模型状态流转 / Model Status Flow

```
训练完成 / Training Complete
         ↓
    📝 registered (已注册 / Registered)
         ↓
    [性能评估 / Performance Evaluation]
         ↓
    ⭐ candidate (候选 / Candidate) ← [性能优于生产模型 / Better than production]
         ↓
    [手动设置 / Manual Setting]
         ↓
    🚀 production (生产 / Production)
         ↓
    [被新模型替换 / Replaced by new model]
         ↓
    ⭐ candidate (候选 / Candidate)
         ↓
    [不再使用 / No longer used]
         ↓
    📦 archived (已归档 / Archived)
         ↓
    [删除 / Delete]
         ↓
    ❌ deleted (已删除 / Deleted)
```

## 最佳实践 / Best Practices

### 1. 模型版本管理 / Model Version Management

- 使用语义化版本号（如 v1.0, v1.1, v2.0）/ Use semantic versioning (e.g., v1.0, v1.1, v2.0)
- 为每个重要的训练实验创建新版本 / Create new version for each important training experiment
- 保留至少2-3个历史版本以便回滚 / Keep at least 2-3 historical versions for rollback

### 2. 生产模型选择 / Production Model Selection

- 优先选择候选模型（系统自动标记的高性能模型）/ Prioritize candidate models (automatically marked high-performance models)
- 在设置为生产模型前，先进行充分的回测验证 / Perform thorough backtesting before setting as production
- 定期评估生产模型性能，及时更新 / Regularly evaluate production model performance and update timely

### 3. 模型清理 / Model Cleanup

- 定期归档不再使用的旧模型 / Regularly archive old models no longer in use
- 删除性能明显较差的模型 / Delete models with significantly poor performance
- 保留关键里程碑版本的模型 / Keep models of key milestone versions

### 4. 性能监控 / Performance Monitoring

- 定期查看模型列表，关注候选模型 / Regularly check model list and pay attention to candidate models
- 对比新旧模型的性能指标 / Compare performance metrics of new and old models
- 记录模型性能变化趋势 / Record trends in model performance changes

## 常见问题 / FAQ

### Q1: 如何判断是否应该更新生产模型？

**A:** 考虑以下因素：
- 候选模型的性能指标是否显著优于当前生产模型（如IC提升>10%）
- 候选模型在回测中的表现是否稳定
- 候选模型是否在不同市场环境下都表现良好

### Q2: 删除模型后能否恢复？

**A:** 不能。删除操作是永久性的，会删除模型文件和所有元数据。建议在删除前：
- 确认模型确实不再需要
- 如有必要，先导出模型信息作为备份
- 考虑使用归档状态而不是直接删除

### Q3: 为什么我的模型被自动标记为候选？

**A:** 系统会自动比较新训练模型与当前生产模型的性能。如果新模型的IC均值更高，会自动标记为候选模型，提示您考虑更新生产模型。

### Q4: 可以同时有多个生产模型吗？

**A:** 不可以。系统只允许一个生产模型。当设置新的生产模型时，旧的生产模型会自动降级为候选模型。

### Q5: 如何导出模型信息？

**A:** 在查看模型详情时，选择"导出模型信息"选项。系统会将模型的完整信息导出为JSON文件，保存在`outputs/model_info/`目录下。

## 相关文档 / Related Documentation

- [模型训练CLI使用指南](./training_cli_usage.md)
- [回测CLI使用指南](./backtest_cli_usage.md)
- [信号生成CLI使用指南](./signal_cli_usage.md)
- [模型注册表实现文档](./model_registry.md)

## 技术支持 / Technical Support

如有问题或建议，请：
- 查看项目文档：`docs/` 目录
- 查看示例代码：`examples/` 目录
- 提交Issue到项目仓库

For questions or suggestions:
- Check project documentation in `docs/` directory
- Check example code in `examples/` directory
- Submit issues to project repository
