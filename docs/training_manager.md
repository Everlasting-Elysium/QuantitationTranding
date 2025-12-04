# 训练管理器文档 / Training Manager Documentation

## 概述 / Overview

训练管理器（TrainingManager）负责协调模型训练的完整流程，包括数据加载、特征工程、模型训练、评估和保存。它集成了数据管理器、模型工厂和MLflow追踪器，提供了统一的训练接口。

The Training Manager coordinates the complete model training process, including data loading, feature engineering, model training, evaluation, and saving. It integrates the data manager, model factory, and MLflow tracker to provide a unified training interface.

## 主要功能 / Main Features

1. **完整的训练流程** / Complete Training Pipeline
   - 自动加载和准备数据 / Automatically load and prepare data
   - 创建和配置模型 / Create and configure models
   - 训练和评估模型 / Train and evaluate models
   - 保存模型和配置 / Save models and configurations

2. **MLflow集成** / MLflow Integration
   - 自动记录训练参数 / Automatically log training parameters
   - 追踪训练指标 / Track training metrics
   - 保存模型工件 / Save model artifacts
   - 实验管理 / Experiment management

3. **模板支持** / Template Support
   - 从预配置模板快速训练 / Quick training from pre-configured templates
   - 支持自定义参数覆盖 / Support custom parameter overrides

4. **错误处理** / Error Handling
   - 完善的异常处理 / Comprehensive exception handling
   - 详细的错误日志 / Detailed error logging
   - 自动清理失败的运行 / Automatic cleanup of failed runs

## 架构设计 / Architecture Design

```
TrainingManager
    ├── DataManager (数据管理)
    ├── ModelFactory (模型创建)
    └── MLflowTracker (实验追踪)
```

## 核心类 / Core Classes

### TrainingManager

训练管理器主类 / Main training manager class

**初始化参数 / Initialization Parameters:**

```python
TrainingManager(
    data_manager: DataManager,      # 数据管理器 / Data manager
    model_factory: ModelFactory,    # 模型工厂 / Model factory
    mlflow_tracker: Optional[MLflowTracker] = None,  # MLflow追踪器（可选）/ MLflow tracker (optional)
    output_dir: str = "./outputs"   # 输出目录 / Output directory
)
```

**主要方法 / Main Methods:**

#### train_model()

训练模型 / Train model

```python
def train_model(self, config: TrainingConfig) -> TrainingResult:
    """
    训练模型 / Train model
    
    Args:
        config: 训练配置 / Training configuration
        
    Returns:
        TrainingResult: 训练结果 / Training result
    """
```

**示例 / Example:**

```python
from src.application.training_manager import TrainingManager, TrainingConfig, DatasetConfig

# 创建数据集配置 / Create dataset configuration
dataset_config = DatasetConfig(
    instruments="csi300",
    start_time="2020-01-01",
    end_time="2021-12-31",
    features=["$close", "$volume", "$open", "$high", "$low"],
    label="Ref($close, -1) / $close - 1"
)

# 创建训练配置 / Create training configuration
training_config = TrainingConfig(
    model_type="lgbm",
    dataset_config=dataset_config,
    model_params={
        "loss": "mse",
        "num_boost_round": 100,
        "learning_rate": 0.1,
    },
    training_params={},
    experiment_name="my_experiment"
)

# 训练模型 / Train model
result = training_manager.train_model(training_config)

print(f"模型ID / Model ID: {result.model_id}")
print(f"训练时长 / Training time: {result.training_time:.2f}秒")
print(f"指标 / Metrics: {result.metrics}")
```

#### train_from_template()

从模板训练模型 / Train model from template

```python
def train_from_template(
    self,
    template_name: str,
    dataset_config: DatasetConfig,
    experiment_name: str,
    custom_params: Optional[Dict[str, Any]] = None
) -> TrainingResult:
    """
    从模板训练模型 / Train model from template
    
    Args:
        template_name: 模板名称 / Template name
        dataset_config: 数据集配置 / Dataset configuration
        experiment_name: 实验名称 / Experiment name
        custom_params: 自定义参数（可选）/ Custom parameters (optional)
        
    Returns:
        TrainingResult: 训练结果 / Training result
    """
```

**示例 / Example:**

```python
# 从模板训练 / Train from template
result = training_manager.train_from_template(
    template_name="lgbm_default",
    dataset_config=dataset_config,
    experiment_name="template_experiment",
    custom_params={"num_boost_round": 200}  # 覆盖默认参数 / Override default parameters
)
```

#### list_templates()

列出所有可用模板 / List all available templates

```python
def list_templates(self) -> List:
    """
    列出所有可用的模板 / List all available templates
    
    Returns:
        List: 模板列表 / Template list
    """
```

**示例 / Example:**

```python
# 列出模板 / List templates
templates = training_manager.list_templates()
for template in templates:
    print(f"{template.name}: {template.description}")
```

### DatasetConfig

数据集配置类 / Dataset configuration class

```python
@dataclass
class DatasetConfig:
    instruments: str        # 股票池 / Stock pool
    start_time: str        # 开始时间 / Start time
    end_time: str          # 结束时间 / End time
    features: List[str]    # 特征列表 / Feature list
    label: str             # 标签列 / Label column
```

### TrainingConfig

训练配置类 / Training configuration class

```python
@dataclass
class TrainingConfig:
    model_type: str                          # 模型类型 / Model type
    dataset_config: DatasetConfig            # 数据集配置 / Dataset configuration
    model_params: Dict[str, Any]             # 模型参数 / Model parameters
    training_params: Dict[str, Any]          # 训练参数 / Training parameters
    experiment_name: str                     # 实验名称 / Experiment name
    target_return: Optional[float] = None    # 目标收益率（可选）/ Target return (optional)
    optimization_objective: str = "sharpe_ratio"  # 优化目标 / Optimization objective
```

### TrainingResult

训练结果类 / Training result class

```python
@dataclass
class TrainingResult:
    model_id: str              # 模型ID / Model ID
    metrics: Dict[str, float]  # 评估指标 / Evaluation metrics
    training_time: float       # 训练时长（秒）/ Training time (seconds)
    model_path: str           # 模型保存路径 / Model save path
    experiment_id: str        # 实验ID / Experiment ID
    run_id: str               # 运行ID / Run ID
```

## 训练流程 / Training Process

训练管理器执行以下步骤：

The training manager executes the following steps:

1. **启动MLflow运行** / Start MLflow Run
   - 创建实验（如果不存在）/ Create experiment (if not exists)
   - 开始新的运行 / Start new run
   - 记录配置参数 / Log configuration parameters

2. **加载数据集** / Load Dataset
   - 使用qlib的DatasetH加载数据 / Load data using qlib's DatasetH
   - 配置数据处理器 / Configure data handler
   - 准备训练数据 / Prepare training data

3. **创建模型** / Create Model
   - 使用模型工厂创建模型实例 / Create model instance using model factory
   - 应用模型参数 / Apply model parameters

4. **训练模型** / Train Model
   - 调用模型的fit方法 / Call model's fit method
   - 使用qlib数据集进行训练 / Train using qlib dataset

5. **评估模型** / Evaluate Model
   - 生成预测 / Generate predictions
   - 计算评估指标（IC等）/ Calculate evaluation metrics (IC, etc.)
   - 记录指标到MLflow / Log metrics to MLflow

6. **保存模型** / Save Model
   - 保存模型文件（pickle格式）/ Save model file (pickle format)
   - 保存配置文件（JSON格式）/ Save configuration file (JSON format)
   - 记录模型到MLflow / Log model to MLflow

7. **结束运行** / End Run
   - 记录训练时长 / Log training time
   - 结束MLflow运行 / End MLflow run
   - 返回训练结果 / Return training result

## 使用示例 / Usage Examples

### 基本训练 / Basic Training

```python
from src.core.data_manager import DataManager
from src.core.model_factory import ModelFactory
from src.infrastructure.qlib_wrapper import QlibWrapper
from src.infrastructure.mlflow_tracker import MLflowTracker
from src.application.training_manager import (
    TrainingManager,
    TrainingConfig,
    DatasetConfig
)

# 1. 初始化组件 / Initialize components
qlib_wrapper = QlibWrapper()
qlib_wrapper.init(provider_uri="~/.qlib/qlib_data/cn_data", region="cn")

data_manager = DataManager(qlib_wrapper=qlib_wrapper)
model_factory = ModelFactory()
mlflow_tracker = MLflowTracker()
mlflow_tracker.initialize()

training_manager = TrainingManager(
    data_manager=data_manager,
    model_factory=model_factory,
    mlflow_tracker=mlflow_tracker
)

# 2. 配置训练 / Configure training
dataset_config = DatasetConfig(
    instruments="csi300",
    start_time="2020-01-01",
    end_time="2021-12-31",
    features=["$close", "$volume"],
    label="Ref($close, -1) / $close - 1"
)

training_config = TrainingConfig(
    model_type="lgbm",
    dataset_config=dataset_config,
    model_params={"loss": "mse", "num_boost_round": 100},
    training_params={},
    experiment_name="my_experiment"
)

# 3. 训练模型 / Train model
result = training_manager.train_model(training_config)
print(f"训练完成 / Training completed: {result.model_id}")
```

### 从模板训练 / Training from Template

```python
# 列出可用模板 / List available templates
templates = training_manager.list_templates()
for template in templates:
    print(f"{template.name}: {template.description}")

# 从模板训练 / Train from template
result = training_manager.train_from_template(
    template_name="lgbm_default",
    dataset_config=dataset_config,
    experiment_name="template_experiment"
)
```

### 自定义参数训练 / Training with Custom Parameters

```python
# 使用自定义参数覆盖模板默认值 / Override template defaults with custom parameters
result = training_manager.train_from_template(
    template_name="lgbm_default",
    dataset_config=dataset_config,
    experiment_name="custom_experiment",
    custom_params={
        "num_boost_round": 200,
        "learning_rate": 0.05,
        "max_depth": 8
    }
)
```

## 错误处理 / Error Handling

训练管理器提供完善的错误处理：

The training manager provides comprehensive error handling:

```python
try:
    result = training_manager.train_model(training_config)
except TrainingManagerError as e:
    print(f"训练失败 / Training failed: {str(e)}")
    # 错误已记录到日志 / Error is logged
    # MLflow运行已标记为失败 / MLflow run is marked as failed
```

## 输出文件 / Output Files

训练完成后，会生成以下文件：

After training completes, the following files are generated:

```
outputs/
└── models/
    └── {model_id}/
        ├── model.pkl      # 模型文件 / Model file
        └── config.json    # 配置文件 / Configuration file
```

## MLflow集成 / MLflow Integration

如果配置了MLflow追踪器，训练过程会自动记录：

If MLflow tracker is configured, the training process automatically logs:

- **参数 / Parameters**: 模型类型、数据集配置、模型参数等 / Model type, dataset config, model parameters, etc.
- **指标 / Metrics**: IC、训练时长等 / IC, training time, etc.
- **工件 / Artifacts**: 模型文件 / Model files

查看MLflow UI：

View MLflow UI:

```bash
mlflow ui --backend-store-uri ./mlruns
```

然后访问 http://localhost:5000

Then visit http://localhost:5000

## 最佳实践 / Best Practices

1. **使用MLflow追踪** / Use MLflow Tracking
   - 始终配置MLflow追踪器以记录实验 / Always configure MLflow tracker to record experiments
   - 使用有意义的实验名称 / Use meaningful experiment names

2. **合理配置数据集** / Configure Dataset Properly
   - 确保时间范围覆盖足够的数据 / Ensure time range covers sufficient data
   - 选择合适的特征 / Select appropriate features
   - 验证数据可用性 / Validate data availability

3. **选择合适的模型** / Choose Appropriate Model
   - 根据数据特点选择模型类型 / Choose model type based on data characteristics
   - 从模板开始，逐步调优 / Start with templates, then fine-tune

4. **监控训练过程** / Monitor Training Process
   - 检查日志输出 / Check log output
   - 使用MLflow UI查看指标 / Use MLflow UI to view metrics
   - 及时处理错误 / Handle errors promptly

5. **保存重要配置** / Save Important Configurations
   - 记录成功的配置 / Record successful configurations
   - 版本化配置文件 / Version configuration files

## 故障排除 / Troubleshooting

### 问题：数据加载失败 / Issue: Data Loading Failed

**原因 / Cause**: qlib数据未初始化或路径错误

**解决方案 / Solution**:
```bash
# 下载数据 / Download data
python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn

# 验证数据 / Verify data
python -c "from qlib.data import D; print(D.calendar())"
```

### 问题：MLflow初始化失败 / Issue: MLflow Initialization Failed

**原因 / Cause**: MLflow未安装

**解决方案 / Solution**:
```bash
pip install mlflow
```

### 问题：模型训练失败 / Issue: Model Training Failed

**原因 / Cause**: 参数配置错误或数据不足

**解决方案 / Solution**:
1. 检查模型参数是否有效 / Check if model parameters are valid
2. 验证数据集时间范围 / Verify dataset time range
3. 查看详细错误日志 / Check detailed error logs

## 参考资料 / References

- [Qlib文档 / Qlib Documentation](https://qlib.readthedocs.io/)
- [MLflow文档 / MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [模型工厂文档 / Model Factory Documentation](./model_factory.md)
- [数据管理器文档 / Data Manager Documentation](./data_manager.md)
