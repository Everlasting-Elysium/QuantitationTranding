# 模型注册表 / Model Registry

## 概述 / Overview

模型注册表（ModelRegistry）是一个用于管理训练好的模型的系统组件。它提供模型注册、版本控制、查询和生产模型管理等功能。

The Model Registry is a system component for managing trained models. It provides model registration, version control, querying, and production model management capabilities.

## 主要功能 / Key Features

### 1. 模型注册 / Model Registration

- 注册训练好的模型及其元数据
- 自动生成唯一的模型ID
- 保存模型文件和配置信息
- Register trained models with metadata
- Automatically generate unique model IDs
- Save model files and configuration

### 2. 版本管理 / Version Management

- 支持同一模型的多个版本
- 自动版本号管理
- 版本历史追踪
- Support multiple versions of the same model
- Automatic version number management
- Version history tracking

### 3. 模型查询 / Model Querying

- 列出所有注册的模型
- 按条件过滤模型（类型、状态、性能等）
- 获取模型详细信息
- List all registered models
- Filter models by conditions (type, status, performance, etc.)
- Get detailed model information

### 4. 生产模型管理 / Production Model Management

- 标记生产模型
- 自动识别候选模型
- 生产模型升级和降级
- Mark production models
- Automatically identify candidate models
- Production model promotion and demotion

## 使用方法 / Usage

### 初始化 / Initialization

```python
from src.application.model_registry import ModelRegistry

# 创建模型注册表实例 / Create model registry instance
registry = ModelRegistry(registry_dir="./model_registry")
```

### 注册模型 / Register Model

```python
from src.models.data_models import ModelMetadata, DatasetConfig

# 准备模型元数据 / Prepare model metadata
metadata = ModelMetadata(
    model_name="lgbm_model",
    version="1.0",
    training_date="2024-01-01",
    performance_metrics={
        "ic_mean": 0.05,
        "ic_std": 0.02,
        "sharpe_ratio": 1.5
    },
    dataset_info=DatasetConfig(
        instruments="csi300",
        start_time="2020-01-01",
        end_time="2023-12-31",
        features=["close", "volume"],
        label="label"
    ),
    hyperparameters={
        "model_type": "lgbm",
        "n_estimators": 100,
        "learning_rate": 0.1
    }
)

# 注册模型 / Register model
model_id = registry.register_model(model, metadata)
print(f"Model registered with ID: {model_id}")
```

### 查询模型 / Query Models

```python
# 列出所有模型 / List all models
all_models = registry.list_models()

# 使用过滤器查询 / Query with filter
from src.application.model_registry import ModelFilter

filter = ModelFilter(
    model_type="lgbm",
    status="candidate",
    min_performance={"ic_mean": 0.05}
)
filtered_models = registry.list_models(filter=filter)

# 打印模型信息 / Print model information
for model_info in filtered_models:
    print(f"Model ID: {model_info.model_id}")
    print(f"Version: {model_info.version}")
    print(f"Status: {model_info.status}")
    print(f"IC Mean: {model_info.performance_metrics['ic_mean']}")
```

### 加载模型 / Load Model

```python
# 加载模型对象 / Load model object
model = registry.get_model(model_id)

# 使用模型进行预测 / Use model for prediction
predictions = model.predict(dataset)
```

### 管理生产模型 / Manage Production Model

```python
# 设置生产模型 / Set production model
registry.set_production_model(model_id)

# 获取当前生产模型 / Get current production model
prod_model = registry.get_production_model()
if prod_model:
    print(f"Production model: {prod_model.model_id}")
```

### 模型状态管理 / Model Status Management

模型可以有以下状态 / Models can have the following statuses:

- `registered`: 已注册 / Registered
- `candidate`: 候选模型（性能优于生产模型）/ Candidate (performs better than production)
- `production`: 生产模型 / Production model
- `archived`: 已归档 / Archived

```python
# 设置模型状态 / Set model status
registry.set_model_status(model_id, "archived")

# 查询特定状态的模型 / Query models with specific status
filter = ModelFilter(status="candidate")
candidates = registry.list_models(filter=filter)
```

## 自动候选模型标记 / Automatic Candidate Marking

当注册新模型时，系统会自动比较其性能与当前生产模型：

When registering a new model, the system automatically compares its performance with the current production model:

- 如果新模型的IC均值高于生产模型，自动标记为候选模型
- 候选模型可以被提升为生产模型
- 提升新模型为生产模型时，旧生产模型自动降级为候选

- If the new model's IC mean is higher than the production model, it's automatically marked as candidate
- Candidate models can be promoted to production
- When promoting a new model to production, the old production model is automatically demoted to candidate

## 数据结构 / Data Structures

### ModelInfo

模型信息数据类 / Model information dataclass

```python
@dataclass
class ModelInfo:
    model_id: str              # 模型ID / Model ID
    model_name: str            # 模型名称 / Model name
    version: str               # 版本 / Version
    model_type: str            # 模型类型 / Model type
    training_date: str         # 训练日期 / Training date
    performance_metrics: Dict  # 性能指标 / Performance metrics
    status: str                # 状态 / Status
    model_path: str            # 模型文件路径 / Model file path
    metadata_path: str         # 元数据路径 / Metadata path
```

### ModelFilter

模型过滤器 / Model filter

```python
@dataclass
class ModelFilter:
    model_type: Optional[str]              # 模型类型 / Model type
    status: Optional[str]                  # 状态 / Status
    min_performance: Optional[Dict]        # 最小性能要求 / Min performance
    date_from: Optional[str]               # 起始日期 / Start date
    date_to: Optional[str]                 # 结束日期 / End date
```

## 存储结构 / Storage Structure

模型注册表使用以下目录结构：

The model registry uses the following directory structure:

```
model_registry/
├── index.json                    # 模型索引文件 / Model index file
├── lgbm_model_v1.0/             # 模型目录 / Model directory
│   ├── model.pkl                # 模型文件 / Model file
│   └── metadata.json            # 元数据文件 / Metadata file
├── lgbm_model_v2.0/
│   ├── model.pkl
│   └── metadata.json
└── ...
```

### index.json 格式 / index.json Format

```json
{
  "lgbm_model_v1.0": {
    "model_id": "lgbm_model_v1.0",
    "model_name": "lgbm_model",
    "version": "1.0",
    "model_type": "lgbm",
    "training_date": "2024-01-01",
    "performance_metrics": {
      "ic_mean": 0.05,
      "ic_std": 0.02,
      "sharpe_ratio": 1.5
    },
    "status": "production",
    "model_path": "./model_registry/lgbm_model_v1.0/model.pkl",
    "metadata_path": "./model_registry/lgbm_model_v1.0/metadata.json"
  }
}
```

## 错误处理 / Error Handling

模型注册表会抛出 `ModelRegistryError` 异常：

The model registry raises `ModelRegistryError` exceptions:

```python
from src.application.model_registry import ModelRegistryError

try:
    model = registry.get_model("non_existent_id")
except ModelRegistryError as e:
    print(f"Error: {e}")
```

常见错误 / Common errors:

- 模型不存在 / Model does not exist
- 模型文件损坏 / Model file corrupted
- 无效的状态值 / Invalid status value
- 尝试删除生产模型 / Attempting to delete production model

## 最佳实践 / Best Practices

### 1. 版本命名 / Version Naming

使用语义化版本号：

Use semantic versioning:

- 主版本号：重大变更 / Major version: breaking changes
- 次版本号：新功能 / Minor version: new features
- 修订号：bug修复 / Patch version: bug fixes

示例 / Example: `1.0.0`, `1.1.0`, `1.1.1`

### 2. 性能指标 / Performance Metrics

始终记录关键性能指标：

Always record key performance metrics:

- IC均值和标准差 / IC mean and std
- 夏普比率 / Sharpe ratio
- 最大回撤 / Maximum drawdown
- 胜率 / Win rate

### 3. 模型清理 / Model Cleanup

定期清理旧模型：

Regularly clean up old models:

```python
# 归档旧模型 / Archive old models
old_models = registry.list_models(
    filter=ModelFilter(date_to="2023-01-01")
)
for model in old_models:
    if model.status != "production":
        registry.set_model_status(model.model_id, "archived")
```

### 4. 生产模型升级 / Production Model Upgrade

升级生产模型前进行充分测试：

Thoroughly test before upgrading production model:

1. 在候选模型上进行回测 / Backtest on candidate model
2. 进行模拟交易验证 / Validate with simulation trading
3. 比较与当前生产模型的性能 / Compare with current production
4. 确认后再升级 / Upgrade after confirmation

```python
# 获取候选模型 / Get candidate models
candidates = registry.list_models(filter=ModelFilter(status="candidate"))

# 选择最佳候选 / Select best candidate
best_candidate = max(
    candidates,
    key=lambda m: m.performance_metrics.get("ic_mean", 0)
)

# 升级为生产模型 / Promote to production
registry.set_production_model(best_candidate.model_id)
```

## 与其他组件集成 / Integration with Other Components

### 与TrainingManager集成 / Integration with TrainingManager

```python
from src.application.training_manager import TrainingManager
from src.application.model_registry import ModelRegistry

# 训练模型 / Train model
training_result = training_manager.train_model(config)

# 注册模型 / Register model
metadata = ModelMetadata(
    model_name=config.model_type,
    version="1.0",
    training_date=datetime.now().strftime("%Y-%m-%d"),
    performance_metrics=training_result.metrics,
    dataset_info=config.dataset_config,
    hyperparameters=config.model_params
)

model_id = registry.register_model(
    model=None,  # 模型已保存 / Model already saved
    metadata=metadata,
    model_path=training_result.model_path
)
```

### 与MLflow集成 / Integration with MLflow

模型注册表可以与MLflow配合使用：

The model registry can work with MLflow:

- 使用MLflow追踪训练过程 / Use MLflow to track training
- 使用ModelRegistry管理模型版本 / Use ModelRegistry to manage versions
- MLflow记录实验，ModelRegistry管理生产 / MLflow for experiments, ModelRegistry for production

## 示例 / Examples

完整的使用示例请参考：

For complete usage examples, see:

- `examples/demo_model_registry.py` - 基本使用演示 / Basic usage demo
- `examples/demo_training_manager.py` - 与训练管理器集成 / Integration with training manager

## API参考 / API Reference

### ModelRegistry

#### `__init__(registry_dir: str = "./model_registry")`

初始化模型注册表 / Initialize model registry

#### `register_model(model: Any, metadata: ModelMetadata, model_path: Optional[str] = None) -> str`

注册模型 / Register model

**Returns:** 模型ID / Model ID

#### `get_model(model_id: str) -> Any`

获取模型对象 / Get model object

#### `get_model_metadata(model_id: str) -> Dict[str, Any]`

获取模型元数据 / Get model metadata

#### `list_models(filter: Optional[ModelFilter] = None) -> List[ModelInfo]`

列出模型 / List models

#### `set_model_status(model_id: str, status: str) -> None`

设置模型状态 / Set model status

#### `set_production_model(model_id: str) -> None`

设置生产模型 / Set production model

#### `get_production_model() -> Optional[ModelInfo]`

获取生产模型 / Get production model

#### `delete_model(model_id: str) -> None`

删除模型 / Delete model

## 注意事项 / Notes

1. **模型文件大小** / Model File Size
   - 大型模型可能占用大量磁盘空间
   - 考虑定期清理旧模型
   - Large models may consume significant disk space
   - Consider regular cleanup of old models

2. **并发访问** / Concurrent Access
   - 当前实现不支持并发写入
   - 在多进程环境中需要额外的锁机制
   - Current implementation doesn't support concurrent writes
   - Additional locking needed in multi-process environments

3. **备份** / Backup
   - 定期备份模型注册表目录
   - 特别是生产模型
   - Regularly backup model registry directory
   - Especially production models

4. **性能** / Performance
   - 索引文件在内存中维护
   - 大量模型时考虑使用数据库
   - Index file maintained in memory
   - Consider using database for large number of models
