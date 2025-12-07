# 目标导向训练功能文档 / Target-Oriented Training Documentation

## 概述 / Overview

目标导向训练是TrainingManager的增强功能，允许用户根据期望的收益率目标自动优化策略参数并训练模型。
Target-oriented training is an enhanced feature of TrainingManager that allows users to automatically optimize strategy parameters and train models based on desired return targets.

## 功能特性 / Features

### 1. 自动参数建议 / Automatic Parameter Suggestion

系统根据目标收益率和风险偏好自动建议最优的模型参数：
The system automatically suggests optimal model parameters based on target return and risk tolerance:

- **模型类型选择 / Model Type Selection**: 根据风险偏好选择合适的模型（Linear, LGBM, MLP）
- **特征选择 / Feature Selection**: 自动选择适合的技术指标和基础特征
- **回溯期设置 / Lookback Period**: 根据风险偏好调整历史数据窗口
- **再平衡频率 / Rebalance Frequency**: 优化交易频率以平衡收益和成本

### 2. 策略优化 / Strategy Optimization

当提供约束条件时，系统执行完整的多目标优化：
When constraints are provided, the system performs full multi-objective optimization:

- **资产权重优化 / Asset Weight Optimization**: 计算最优的资产配置比例
- **风险收益平衡 / Risk-Return Balance**: 在目标收益和风险之间找到最佳平衡点
- **约束条件遵守 / Constraint Compliance**: 确保优化结果满足所有约束条件
- **可行性验证 / Feasibility Validation**: 验证目标是否可实现

### 3. MLflow集成 / MLflow Integration

优化结果自动记录到MLflow进行追踪：
Optimization results are automatically logged to MLflow for tracking:

- **优化指标 / Optimization Metrics**: 优化评分、预期收益、预期风险
- **优化参数 / Optimization Parameters**: 策略ID、再平衡频率、资产权重
- **警告信息 / Warnings**: 记录优化过程中的警告和建议

## 使用方法 / Usage

### 基本用法 / Basic Usage

```python
from src.application.training_manager import TrainingManager, DatasetConfig
from src.application.strategy_optimizer import StrategyOptimizer

# 创建训练管理器 / Create training manager
training_manager = TrainingManager(
    data_manager=data_manager,
    model_factory=model_factory,
    mlflow_tracker=mlflow_tracker,
    strategy_optimizer=StrategyOptimizer()
)

# 配置数据集 / Configure dataset
dataset_config = DatasetConfig(
    instruments="csi300",
    start_time="2020-01-01",
    end_time="2021-12-31",
    features=["$close", "$open", "$high", "$low", "$volume"],
    label="Ref($close, -2) / Ref($close, -1) - 1"
)

# 目标导向训练 / Target-oriented training
result = training_manager.train_for_target_return(
    target_return=0.20,  # 20% 年化收益率 / 20% annual return
    assets=["SH600519", "SZ000858", "SH600036"],
    dataset_config=dataset_config,
    experiment_name="my_target_oriented_training",
    risk_tolerance="moderate"  # conservative, moderate, aggressive
)

print(f"模型ID / Model ID: {result.model_id}")
print(f"训练指标 / Training metrics: {result.metrics}")
```

### 带约束条件的用法 / Usage with Constraints

```python
from src.models.market_models import OptimizationConstraints

# 定义约束条件 / Define constraints
constraints = OptimizationConstraints(
    max_position_size=0.30,      # 单只股票最大30% / Max 30% per stock
    max_sector_exposure=0.50,    # 单个行业最大50% / Max 50% per sector
    min_diversification=3,       # 至少3只股票 / At least 3 stocks
    max_turnover=0.50,           # 最大换手率50% / Max 50% turnover
    risk_tolerance="moderate"
)

# 带约束的目标导向训练 / Target-oriented training with constraints
result = training_manager.train_for_target_return(
    target_return=0.20,
    assets=["SH600519", "SZ000858", "SH600036"],
    dataset_config=dataset_config,
    experiment_name="constrained_training",
    risk_tolerance="moderate",
    custom_constraints=constraints  # 提供约束条件 / Provide constraints
)
```

## 参数说明 / Parameter Description

### train_for_target_return 参数 / Parameters

| 参数 / Parameter | 类型 / Type | 必需 / Required | 说明 / Description |
|-----------------|------------|----------------|-------------------|
| `target_return` | float | 是 / Yes | 目标年化收益率（例如0.20表示20%）/ Target annual return (e.g., 0.20 for 20%) |
| `assets` | List[str] | 是 / Yes | 资产代码列表 / List of asset symbols |
| `dataset_config` | DatasetConfig | 是 / Yes | 数据集配置 / Dataset configuration |
| `experiment_name` | str | 是 / Yes | 实验名称 / Experiment name |
| `risk_tolerance` | str | 否 / No | 风险偏好：conservative/moderate/aggressive，默认moderate / Risk tolerance, default moderate |
| `custom_constraints` | OptimizationConstraints | 否 / No | 自定义约束条件 / Custom constraints |

### 风险偏好说明 / Risk Tolerance Description

| 风险偏好 / Risk Tolerance | 模型类型 / Model Type | 回溯期 / Lookback | 再平衡 / Rebalance | 止损 / Stop Loss |
|-------------------------|---------------------|------------------|-------------------|-----------------|
| conservative | Linear | 60天 / 60 days | 月度 / Monthly | 5% |
| moderate | LGBM | 30天 / 30 days | 周度 / Weekly | 10% |
| aggressive | MLP | 20天 / 20 days | 日度 / Daily | 15% |

## 工作流程 / Workflow

1. **参数建议 / Parameter Suggestion**
   - 调用StrategyOptimizer.suggest_parameters()
   - 根据目标收益率和风险偏好生成建议参数

2. **策略优化（可选）/ Strategy Optimization (Optional)**
   - 如果提供了约束条件，调用optimize_for_target_return()
   - 执行多目标优化，计算最优资产配置

3. **配置构建 / Configuration Building**
   - 使用建议的参数构建TrainingConfig
   - 更新数据集配置的特征列表

4. **模型训练 / Model Training**
   - 调用train_model()执行实际训练
   - 使用优化后的参数和配置

5. **结果记录 / Result Logging**
   - 记录训练结果到MLflow
   - 如果有优化策略，记录优化指标和参数

## 输出结果 / Output Results

### TrainingResult 对象 / TrainingResult Object

```python
@dataclass
class TrainingResult:
    model_id: str              # 模型ID / Model ID
    metrics: Dict[str, float]  # 评估指标 / Evaluation metrics
    training_time: float       # 训练时长（秒）/ Training time (seconds)
    model_path: str           # 模型保存路径 / Model save path
    experiment_id: str        # 实验ID / Experiment ID
    run_id: str              # 运行ID / Run ID
```

### MLflow 记录内容 / MLflow Logged Content

**参数 / Parameters:**
- `target_return`: 目标收益率 / Target return
- `strategy_id`: 策略ID / Strategy ID
- `rebalance_frequency`: 再平衡频率 / Rebalance frequency
- `risk_tolerance`: 风险偏好 / Risk tolerance
- `asset_count`: 资产数量 / Asset count
- `weight_{asset}`: 各资产权重 / Asset weights

**指标 / Metrics:**
- `optimization_score`: 优化评分（0-100）/ Optimization score (0-100)
- `expected_return`: 预期收益率 / Expected return
- `expected_risk`: 预期风险 / Expected risk
- `optimization_feasible`: 可行性（1.0或0.0）/ Feasibility (1.0 or 0.0)

## 最佳实践 / Best Practices

### 1. 目标收益率设置 / Target Return Setting

- **保守型 / Conservative**: 5-10% 年化收益率
- **稳健型 / Moderate**: 10-20% 年化收益率
- **进取型 / Aggressive**: 20-30% 年化收益率

建议不要设置过高的目标收益率（>30%），这可能导致过度拟合。
It's recommended not to set target returns too high (>30%), which may lead to overfitting.

### 2. 资产选择 / Asset Selection

- 至少选择3-5只资产以实现分散化 / Select at least 3-5 assets for diversification
- 选择不同行业的资产以降低相关性 / Choose assets from different sectors to reduce correlation
- 考虑资产的历史表现和流动性 / Consider historical performance and liquidity

### 3. 约束条件设置 / Constraint Setting

```python
# 推荐的约束条件 / Recommended constraints
constraints = OptimizationConstraints(
    max_position_size=0.25,      # 单只股票不超过25%
    max_sector_exposure=0.40,    # 单个行业不超过40%
    min_diversification=5,       # 至少5只股票
    max_turnover=0.30,           # 换手率不超过30%
    risk_tolerance="moderate"
)
```

### 4. 实验管理 / Experiment Management

- 使用有意义的实验名称 / Use meaningful experiment names
- 定期查看MLflow UI了解优化历史 / Regularly check MLflow UI for optimization history
- 比较不同目标收益率和风险偏好的结果 / Compare results with different targets and risk tolerances

## 故障排除 / Troubleshooting

### 问题1：优化不可行 / Issue 1: Optimization Not Feasible

**症状 / Symptom**: `optimized_strategy.feasible = False`

**原因 / Cause**: 目标收益率过高或约束条件过于严格

**解决方案 / Solution**:
- 降低目标收益率 / Lower target return
- 放宽约束条件 / Relax constraints
- 增加资产数量 / Increase number of assets

### 问题2：训练时间过长 / Issue 2: Training Takes Too Long

**症状 / Symptom**: 训练时间超过预期

**原因 / Cause**: 数据量过大或模型复杂度过高

**解决方案 / Solution**:
- 减少特征数量 / Reduce number of features
- 缩短训练时间范围 / Shorten training time range
- 使用更简单的模型类型（如Linear）/ Use simpler model type (e.g., Linear)

### 问题3：MLflow记录失败 / Issue 3: MLflow Logging Failed

**症状 / Symptom**: 警告信息显示MLflow记录失败

**原因 / Cause**: MLflow未正确初始化或网络问题

**解决方案 / Solution**:
- 检查MLflow配置 / Check MLflow configuration
- 确保MLflow服务正在运行 / Ensure MLflow service is running
- 查看详细日志了解错误原因 / Check detailed logs for error cause

## 示例代码 / Example Code

完整的示例代码请参考：
For complete example code, please refer to:

- `test_target_oriented_training_unit.py`: 单元测试示例 / Unit test example
- `examples/demo_target_oriented_training.py`: 完整使用示例 / Complete usage example

## 相关文档 / Related Documentation

- [Strategy Optimizer Documentation](./strategy_optimizer.md)
- [Training Manager Documentation](./training_manager.md)
- [MLflow Integration Guide](./mlflow_integration.md)

## 更新日志 / Changelog

### Version 1.0.0 (2024-12-05)

- ✨ 新增train_for_target_return方法 / Added train_for_target_return method
- ✨ 集成StrategyOptimizer / Integrated StrategyOptimizer
- ✨ 支持基于目标收益率的参数调整 / Support parameter adjustment based on target return
- ✨ 优化结果自动记录到MLflow / Automatic logging of optimization results to MLflow
- ✨ 支持自定义约束条件 / Support custom constraints
- ✨ 支持多种风险偏好设置 / Support multiple risk tolerance settings
