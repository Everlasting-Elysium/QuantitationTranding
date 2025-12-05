# API参考文档 (API Reference)

本文档提供系统所有模块和类的详细API说明，适合开发者进行二次开发。

## 📑 目录

1. [核心模块](#核心模块)
2. [应用模块](#应用模块)
3. [基础设施模块](#基础设施模块)
4. [数据模型](#数据模型)
5. [工具函数](#工具函数)

## 核心模块

### ConfigManager

配置管理器，负责加载和管理系统配置。

**模块路径**: `src.core.config_manager`

#### 类定义

```python
class ConfigManager:
    """
    配置管理器
    Configuration Manager
    
    负责加载、验证和管理系统配置文件
    Responsible for loading, validating and managing system configuration files
    """
```

#### 方法

##### `__init__(config_path: str = None)`

初始化配置管理器
Initialize configuration manager

**参数 Parameters**:
- `config_path` (str, optional): 配置文件路径，默认使用 `config/default_config.yaml`
  Path to configuration file, defaults to `config/default_config.yaml`

**示例 Example**:
```python
from src.core.config_manager import ConfigManager

# 使用默认配置
config_mgr = ConfigManager()

# 使用自定义配置
config_mgr = ConfigManager("my_config.yaml")
```

##### `load_config(config_path: str) -> Dict`

加载配置文件
Load configuration file

**参数 Parameters**:
- `config_path` (str): 配置文件路径
  Path to configuration file

**返回 Returns**:
- `Dict`: 配置字典
  Configuration dictionary

**异常 Raises**:
- `FileNotFoundError`: 配置文件不存在
  Configuration file not found
- `yaml.YAMLError`: YAML格式错误
  YAML format error

**示例 Example**:
```python
config = config_mgr.load_config("config/default_config.yaml")
print(config['data']['region'])  # 输出: cn
```


##### `save_config(config: Dict, config_path: str) -> None`

保存配置到文件
Save configuration to file

**参数 Parameters**:
- `config` (Dict): 配置字典
  Configuration dictionary
- `config_path` (str): 保存路径
  Save path

**示例 Example**:
```python
config = config_mgr.get_config()
config['data']['region'] = 'us'
config_mgr.save_config(config, "config/my_config.yaml")
```

##### `get_config() -> Dict`

获取当前配置
Get current configuration

**返回 Returns**:
- `Dict`: 当前配置字典
  Current configuration dictionary

##### `validate_config(config: Dict) -> List[str]`

验证配置有效性
Validate configuration

**参数 Parameters**:
- `config` (Dict): 要验证的配置
  Configuration to validate

**返回 Returns**:
- `List[str]`: 错误信息列表，空列表表示验证通过
  List of error messages, empty list means validation passed

**示例 Example**:
```python
errors = config_mgr.validate_config(config)
if errors:
    print("配置错误:", errors)
else:
    print("配置验证通过")
```

##### `get_default_config() -> Dict`

获取默认配置
Get default configuration

**返回 Returns**:
- `Dict`: 默认配置字典
  Default configuration dictionary

---

### DataManager

数据管理器，负责数据下载、验证和管理。

**模块路径**: `src.core.data_manager`

#### 类定义

```python
class DataManager:
    """
    数据管理器
    Data Manager
    
    负责qlib数据的下载、更新、验证和管理
    Responsible for downloading, updating, validating and managing qlib data
    """
```

#### 方法

##### `__init__(config: Dict)`

初始化数据管理器
Initialize data manager

**参数 Parameters**:
- `config` (Dict): 配置字典
  Configuration dictionary

##### `download_data(region: str, target_dir: str, interval: str = "day") -> None`

下载市场数据
Download market data

**参数 Parameters**:
- `region` (str): 市场区域，如 "cn", "us"
  Market region, e.g., "cn", "us"
- `target_dir` (str): 目标目录
  Target directory
- `interval` (str, optional): 数据频率，默认 "day"
  Data frequency, defaults to "day"

**示例 Example**:
```python
from src.core.data_manager import DataManager

data_mgr = DataManager(config)
data_mgr.download_data(
    region="cn",
    target_dir="~/.qlib/qlib_data/cn_data",
    interval="day"
)
```

##### `validate_data(start_date: str, end_date: str) -> ValidationResult`

验证数据完整性
Validate data integrity

**参数 Parameters**:
- `start_date` (str): 开始日期，格式 "YYYY-MM-DD"
  Start date, format "YYYY-MM-DD"
- `end_date` (str): 结束日期，格式 "YYYY-MM-DD"
  End date, format "YYYY-MM-DD"

**返回 Returns**:
- `ValidationResult`: 验证结果对象
  Validation result object

**示例 Example**:
```python
result = data_mgr.validate_data("2020-01-01", "2023-12-31")
if result.is_valid:
    print(f"数据完整性: {result.completeness}%")
else:
    print(f"验证失败: {result.errors}")
```

##### `get_data_info() -> DataInfo`

获取数据信息
Get data information

**返回 Returns**:
- `DataInfo`: 数据信息对象
  Data information object

**示例 Example**:
```python
info = data_mgr.get_data_info()
print(f"时间范围: {info.start_date} 至 {info.end_date}")
print(f"股票数量: {info.stock_count}")
```

##### `update_data() -> None`

更新数据到最新
Update data to latest

**示例 Example**:
```python
data_mgr.update_data()
print("数据更新完成")
```

---

### ModelFactory

模型工厂，负责创建和管理模型实例。

**模块路径**: `src.core.model_factory`

#### 类定义

```python
class ModelFactory:
    """
    模型工厂
    Model Factory
    
    负责创建各种类型的预测模型
    Responsible for creating various types of prediction models
    """
```

#### 方法

##### `create_model(model_type: str, params: Dict) -> Model`

创建模型实例
Create model instance

**参数 Parameters**:
- `model_type` (str): 模型类型，如 "lgbm", "linear", "mlp"
  Model type, e.g., "lgbm", "linear", "mlp"
- `params` (Dict): 模型参数
  Model parameters

**返回 Returns**:
- `Model`: 模型实例
  Model instance

**异常 Raises**:
- `ValueError`: 不支持的模型类型
  Unsupported model type

**示例 Example**:
```python
from src.core.model_factory import ModelFactory

factory = ModelFactory()
model = factory.create_model(
    model_type="lgbm",
    params={
        "learning_rate": 0.05,
        "num_leaves": 63,
        "max_depth": 7
    }
)
```

##### `get_template(template_name: str) -> ModelTemplate`

获取模型模板
Get model template

**参数 Parameters**:
- `template_name` (str): 模板名称
  Template name

**返回 Returns**:
- `ModelTemplate`: 模型模板对象
  Model template object

**示例 Example**:
```python
template = factory.get_template("lgbm_default")
print(f"模板描述: {template.description}")
print(f"默认参数: {template.default_params}")
```

##### `list_available_models() -> List[str]`

列出所有可用的模型类型
List all available model types

**返回 Returns**:
- `List[str]`: 模型类型列表
  List of model types

**示例 Example**:
```python
models = factory.list_available_models()
print("可用模型:", models)
# 输出: ['lgbm', 'linear', 'mlp', 'gru', 'lstm']
```

---

## 应用模块

### TrainingManager

训练管理器，负责模型训练流程。

**模块路径**: `src.application.training_manager`

#### 类定义

```python
class TrainingManager:
    """
    训练管理器
    Training Manager
    
    负责协调模型训练的完整流程
    Responsible for coordinating the complete model training process
    """
```

#### 方法

##### `__init__(config: Dict, data_manager: DataManager, model_factory: ModelFactory)`

初始化训练管理器
Initialize training manager

**参数 Parameters**:
- `config` (Dict): 配置字典
  Configuration dictionary
- `data_manager` (DataManager): 数据管理器实例
  Data manager instance
- `model_factory` (ModelFactory): 模型工厂实例
  Model factory instance

##### `train_model(config: TrainingConfig) -> TrainingResult`

训练模型
Train model

**参数 Parameters**:
- `config` (TrainingConfig): 训练配置对象
  Training configuration object

**返回 Returns**:
- `TrainingResult`: 训练结果对象
  Training result object

**示例 Example**:
```python
from src.application.training_manager import TrainingManager
from src.models.data_models import TrainingConfig, DatasetConfig

# 创建训练配置
dataset_config = DatasetConfig(
    instruments="csi300",
    start_time="2020-01-01",
    end_time="2023-12-31",
    features=["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"],
    label="Ref($close, -1) / $close - 1"
)

training_config = TrainingConfig(
    model_type="lgbm",
    dataset_config=dataset_config,
    model_params={"learning_rate": 0.05},
    training_params={"n_estimators": 200},
    experiment_name="my_experiment"
)

# 训练模型
trainer = TrainingManager(config, data_mgr, factory)
result = trainer.train_model(training_config)

print(f"模型ID: {result.model_id}")
print(f"验证集IC: {result.metrics['valid_ic']}")
```

##### `train_from_template(template_name: str, custom_params: Dict = None) -> TrainingResult`

使用模板训练
Train from template

**参数 Parameters**:
- `template_name` (str): 模板名称
  Template name
- `custom_params` (Dict, optional): 自定义参数
  Custom parameters

**返回 Returns**:
- `TrainingResult`: 训练结果对象
  Training result object

**示例 Example**:
```python
# 使用默认模板
result = trainer.train_from_template("lgbm_default")

# 使用模板并自定义参数
result = trainer.train_from_template(
    "lgbm_default",
    custom_params={"learning_rate": 0.1}
)
```

##### `list_templates() -> List[ModelTemplate]`

列出所有模板
List all templates

**返回 Returns**:
- `List[ModelTemplate]`: 模板列表
  List of templates

---

### BacktestManager

回测管理器，负责策略回测。

**模块路径**: `src.application.backtest_manager`

#### 类定义

```python
class BacktestManager:
    """
    回测管理器
    Backtest Manager
    
    负责执行策略回测和性能评估
    Responsible for executing strategy backtesting and performance evaluation
    """
```

#### 方法

##### `run_backtest(model_id: str, start_date: str, end_date: str, config: BacktestConfig) -> BacktestResult`

运行回测
Run backtest

**参数 Parameters**:
- `model_id` (str): 模型ID
  Model ID
- `start_date` (str): 开始日期
  Start date
- `end_date` (str): 结束日期
  End date
- `config` (BacktestConfig): 回测配置
  Backtest configuration

**返回 Returns**:
- `BacktestResult`: 回测结果对象
  Backtest result object

**示例 Example**:
```python
from src.application.backtest_manager import BacktestManager
from src.models.data_models import BacktestConfig

backtest_config = BacktestConfig(
    strategy_config={
        "topk": 30,
        "rebalance_freq": 5
    },
    executor_config={
        "trade_exchange": "exchange",
        "deal_price": "close"
    },
    benchmark="SH000300"
)

bt_mgr = BacktestManager(config)
result = bt_mgr.run_backtest(
    model_id="lgbm_20240101_123456",
    start_date="2023-01-01",
    end_date="2023-12-31",
    config=backtest_config
)

print(f"总收益率: {result.metrics['total_return']:.2%}")
print(f"夏普比率: {result.metrics['sharpe_ratio']:.2f}")
print(f"最大回撤: {result.metrics['max_drawdown']:.2%}")
```

##### `calculate_metrics(returns: pd.Series, benchmark: pd.Series) -> Dict[str, float]`

计算性能指标
Calculate performance metrics

**参数 Parameters**:
- `returns` (pd.Series): 策略收益率序列
  Strategy returns series
- `benchmark` (pd.Series): 基准收益率序列
  Benchmark returns series

**返回 Returns**:
- `Dict[str, float]`: 指标字典
  Metrics dictionary

**示例 Example**:
```python
metrics = bt_mgr.calculate_metrics(strategy_returns, benchmark_returns)
print(f"年化收益: {metrics['annual_return']:.2%}")
print(f"信息比率: {metrics['information_ratio']:.2f}")
```

---

### SignalGenerator

信号生成器，负责生成交易信号。

**模块路径**: `src.application.signal_generator`

#### 类定义

```python
class SignalGenerator:
    """
    信号生成器
    Signal Generator
    
    负责基于模型预测生成交易信号
    Responsible for generating trading signals based on model predictions
    """
```

#### 方法

##### `generate_signals(model_id: str, date: str, portfolio: Portfolio) -> List[Signal]`

生成交易信号
Generate trading signals

**参数 Parameters**:
- `model_id` (str): 模型ID
  Model ID
- `date` (str): 日期
  Date
- `portfolio` (Portfolio): 当前持仓
  Current portfolio

**返回 Returns**:
- `List[Signal]`: 信号列表
  List of signals

**示例 Example**:
```python
from src.application.signal_generator import SignalGenerator
from src.models.data_models import Portfolio

# 创建空持仓
portfolio = Portfolio(positions={}, cash=1000000, total_value=1000000)

sig_gen = SignalGenerator(config)
signals = sig_gen.generate_signals(
    model_id="lgbm_20240101_123456",
    date="2024-01-01",
    portfolio=portfolio
)

for signal in signals[:5]:  # 显示前5个信号
    print(f"{signal.stock_code}: {signal.action} "
          f"(得分: {signal.score:.2f}, 置信度: {signal.confidence:.2%})")
```

##### `explain_signal(signal: Signal) -> SignalExplanation`

解释信号
Explain signal

**参数 Parameters**:
- `signal` (Signal): 信号对象
  Signal object

**返回 Returns**:
- `SignalExplanation`: 信号解释对象
  Signal explanation object

**示例 Example**:
```python
explanation = sig_gen.explain_signal(signals[0])
print(f"主要因素:")
for factor, contribution in explanation.main_factors:
    print(f"  {factor}: {contribution:.2%}")
print(f"风险等级: {explanation.risk_level}")
print(f"描述: {explanation.description}")
```


---

### ModelRegistry

模型注册表，负责模型版本管理。

**模块路径**: `src.application.model_registry`

#### 类定义

```python
class ModelRegistry:
    """
    模型注册表
    Model Registry
    
    负责模型的注册、查询和版本管理
    Responsible for model registration, querying and version management
    """
```

#### 方法

##### `register_model(model: Model, metadata: ModelMetadata) -> str`

注册模型
Register model

**参数 Parameters**:
- `model` (Model): 模型对象
  Model object
- `metadata` (ModelMetadata): 模型元数据
  Model metadata

**返回 Returns**:
- `str`: 模型ID
  Model ID

**示例 Example**:
```python
from src.application.model_registry import ModelRegistry
from src.models.data_models import ModelMetadata

metadata = ModelMetadata(
    model_name="LGBM Model",
    version="1.0",
    training_date="2024-01-01",
    performance_metrics={"ic": 0.078, "accuracy": 0.652},
    dataset_info=dataset_config,
    hyperparameters={"learning_rate": 0.05}
)

registry = ModelRegistry(config)
model_id = registry.register_model(model, metadata)
print(f"模型已注册: {model_id}")
```

##### `get_model(model_id: str) -> Model`

获取模型
Get model

**参数 Parameters**:
- `model_id` (str): 模型ID
  Model ID

**返回 Returns**:
- `Model`: 模型对象
  Model object

**异常 Raises**:
- `ModelNotFoundError`: 模型不存在
  Model not found

##### `list_models(filter: ModelFilter = None) -> List[ModelInfo]`

列出模型
List models

**参数 Parameters**:
- `filter` (ModelFilter, optional): 过滤条件
  Filter conditions

**返回 Returns**:
- `List[ModelInfo]`: 模型信息列表
  List of model information

**示例 Example**:
```python
# 列出所有模型
all_models = registry.list_models()

# 按类型过滤
from src.models.data_models import ModelFilter
filter = ModelFilter(model_type="lgbm", min_ic=0.07)
lgbm_models = registry.list_models(filter)

for model_info in lgbm_models:
    print(f"{model_info.model_id}: IC={model_info.ic:.3f}")
```

##### `set_production_model(model_id: str) -> None`

设置生产模型
Set production model

**参数 Parameters**:
- `model_id` (str): 模型ID
  Model ID

**示例 Example**:
```python
registry.set_production_model("lgbm_20240101_123456")
print("生产模型已更新")
```

---

## 基础设施模块

### QlibWrapper

Qlib框架封装，提供统一的qlib接口。

**模块路径**: `src.infrastructure.qlib_wrapper`

#### 类定义

```python
class QlibWrapper:
    """
    Qlib框架封装
    Qlib Framework Wrapper
    
    封装qlib框架，提供统一的接口
    Wraps qlib framework and provides unified interface
    """
```

#### 方法

##### `init(provider_uri: str, region: str, exp_manager_config: Dict) -> None`

初始化qlib
Initialize qlib

**参数 Parameters**:
- `provider_uri` (str): 数据提供者URI
  Data provider URI
- `region` (str): 市场区域
  Market region
- `exp_manager_config` (Dict): 实验管理器配置
  Experiment manager configuration

**示例 Example**:
```python
from src.infrastructure.qlib_wrapper import QlibWrapper

qlib_wrapper = QlibWrapper()
qlib_wrapper.init(
    provider_uri="~/.qlib/qlib_data/cn_data",
    region="cn",
    exp_manager_config={
        "class": "MLflowExpManager",
        "module_path": "qlib.workflow.expm",
        "kwargs": {
            "uri": "file:./mlruns",
            "default_exp_name": "qlib_trading"
        }
    }
)
```

##### `get_data(instruments: str, fields: List[str], start_time: str, end_time: str) -> pd.DataFrame`

获取数据
Get data

**参数 Parameters**:
- `instruments` (str): 股票池
  Instruments pool
- `fields` (List[str]): 字段列表
  List of fields
- `start_time` (str): 开始时间
  Start time
- `end_time` (str): 结束时间
  End time

**返回 Returns**:
- `pd.DataFrame`: 数据DataFrame
  Data DataFrame

**示例 Example**:
```python
data = qlib_wrapper.get_data(
    instruments="csi300",
    fields=["$open", "$high", "$low", "$close", "$volume"],
    start_time="2023-01-01",
    end_time="2023-12-31"
)
print(data.head())
```

##### `is_initialized() -> bool`

检查是否已初始化
Check if initialized

**返回 Returns**:
- `bool`: 是否已初始化
  Whether initialized

---

### MLflowTracker

MLflow追踪器，负责实验追踪。

**模块路径**: `src.infrastructure.mlflow_tracker`

#### 类定义

```python
class MLflowTracker:
    """
    MLflow追踪器
    MLflow Tracker
    
    负责记录实验、参数、指标和模型
    Responsible for logging experiments, parameters, metrics and models
    """
```

#### 方法

##### `start_run(experiment_name: str, run_name: str) -> str`

开始运行
Start run

**参数 Parameters**:
- `experiment_name` (str): 实验名称
  Experiment name
- `run_name` (str): 运行名称
  Run name

**返回 Returns**:
- `str`: 运行ID
  Run ID

**示例 Example**:
```python
from src.infrastructure.mlflow_tracker import MLflowTracker

tracker = MLflowTracker()
run_id = tracker.start_run(
    experiment_name="qlib_trading",
    run_name="lgbm_experiment_1"
)
```

##### `log_params(params: Dict) -> None`

记录参数
Log parameters

**参数 Parameters**:
- `params` (Dict): 参数字典
  Parameters dictionary

**示例 Example**:
```python
tracker.log_params({
    "model_type": "lgbm",
    "learning_rate": 0.05,
    "num_leaves": 63,
    "max_depth": 7
})
```

##### `log_metrics(metrics: Dict, step: int = None) -> None`

记录指标
Log metrics

**参数 Parameters**:
- `metrics` (Dict): 指标字典
  Metrics dictionary
- `step` (int, optional): 步骤编号
  Step number

**示例 Example**:
```python
# 记录单次指标
tracker.log_metrics({
    "train_ic": 0.085,
    "valid_ic": 0.078
})

# 记录训练过程中的指标
for epoch in range(100):
    tracker.log_metrics({
        "loss": loss_value,
        "ic": ic_value
    }, step=epoch)
```

##### `log_model(model: Model, artifact_path: str) -> None`

记录模型
Log model

**参数 Parameters**:
- `model` (Model): 模型对象
  Model object
- `artifact_path` (str): 模型保存路径
  Model save path

**示例 Example**:
```python
tracker.log_model(model, "models/lgbm_model")
```

##### `end_run() -> None`

结束运行
End run

**示例 Example**:
```python
tracker.end_run()
```

---

### LoggerSystem

日志系统，负责日志记录和管理。

**模块路径**: `src.infrastructure.logger_system`

#### 类定义

```python
class LoggerSystem:
    """
    日志系统
    Logger System
    
    负责配置和管理系统日志
    Responsible for configuring and managing system logs
    """
```

#### 方法

##### `setup(log_dir: str, log_level: str) -> None`

设置日志系统
Setup logger system

**参数 Parameters**:
- `log_dir` (str): 日志目录
  Log directory
- `log_level` (str): 日志级别 ("DEBUG", "INFO", "WARNING", "ERROR")
  Log level ("DEBUG", "INFO", "WARNING", "ERROR")

**示例 Example**:
```python
from src.infrastructure.logger_system import LoggerSystem

logger_sys = LoggerSystem()
logger_sys.setup(log_dir="logs", log_level="INFO")
```

##### `get_logger(name: str) -> Logger`

获取日志记录器
Get logger

**参数 Parameters**:
- `name` (str): 日志记录器名称
  Logger name

**返回 Returns**:
- `Logger`: 日志记录器对象
  Logger object

**示例 Example**:
```python
logger = logger_sys.get_logger("training")
logger.info("开始训练模型")
logger.warning("验证集IC较低")
logger.error("训练失败", exc_info=True)
```

---

## 数据模型

### TrainingConfig

训练配置数据类。

**模块路径**: `src.models.data_models`

```python
@dataclass
class TrainingConfig:
    """
    训练配置
    Training Configuration
    """
    model_type: str  # 模型类型 Model type
    dataset_config: DatasetConfig  # 数据集配置 Dataset configuration
    model_params: Dict[str, Any]  # 模型参数 Model parameters
    training_params: Dict[str, Any]  # 训练参数 Training parameters
    experiment_name: str  # 实验名称 Experiment name
```

**示例 Example**:
```python
from src.models.data_models import TrainingConfig, DatasetConfig

config = TrainingConfig(
    model_type="lgbm",
    dataset_config=DatasetConfig(
        instruments="csi300",
        start_time="2020-01-01",
        end_time="2023-12-31",
        features=["$open", "$high", "$low", "$close"],
        label="Ref($close, -1) / $close - 1"
    ),
    model_params={"learning_rate": 0.05},
    training_params={"n_estimators": 200},
    experiment_name="my_experiment"
)
```

---

### BacktestConfig

回测配置数据类。

```python
@dataclass
class BacktestConfig:
    """
    回测配置
    Backtest Configuration
    """
    strategy_config: Dict[str, Any]  # 策略配置 Strategy configuration
    executor_config: Dict[str, Any]  # 执行器配置 Executor configuration
    benchmark: str  # 基准指数 Benchmark index
```

**示例 Example**:
```python
from src.models.data_models import BacktestConfig

config = BacktestConfig(
    strategy_config={
        "topk": 30,
        "rebalance_freq": 5
    },
    executor_config={
        "trade_exchange": "exchange",
        "deal_price": "close"
    },
    benchmark="SH000300"
)
```

---

### Signal

交易信号数据类。

```python
@dataclass
class Signal:
    """
    交易信号
    Trading Signal
    """
    stock_code: str  # 股票代码 Stock code
    action: str  # 操作 ("buy", "sell", "hold") Action
    score: float  # 预测得分 Prediction score
    confidence: float  # 置信度 Confidence
    timestamp: str  # 时间戳 Timestamp
```

**示例 Example**:
```python
from src.models.data_models import Signal

signal = Signal(
    stock_code="600519.SH",
    action="buy",
    score=0.85,
    confidence=0.92,
    timestamp="2024-01-01 09:30:00"
)
```

---

## 工具函数

### 数据处理工具

**模块路径**: `src.utils.data_utils`

#### `normalize_data(data: pd.DataFrame, method: str = "zscore") -> pd.DataFrame`

数据标准化
Normalize data

**参数 Parameters**:
- `data` (pd.DataFrame): 原始数据
  Raw data
- `method` (str): 标准化方法 ("zscore", "minmax")
  Normalization method

**返回 Returns**:
- `pd.DataFrame`: 标准化后的数据
  Normalized data

**示例 Example**:
```python
from src.utils.data_utils import normalize_data

normalized = normalize_data(data, method="zscore")
```

#### `handle_missing_values(data: pd.DataFrame, strategy: str = "ffill") -> pd.DataFrame`

处理缺失值
Handle missing values

**参数 Parameters**:
- `data` (pd.DataFrame): 原始数据
  Raw data
- `strategy` (str): 处理策略 ("ffill", "bfill", "mean", "drop")
  Handling strategy

**返回 Returns**:
- `pd.DataFrame`: 处理后的数据
  Processed data

---

### 指标计算工具

**模块路径**: `src.utils.metrics_utils`

#### `calculate_ic(predictions: pd.Series, returns: pd.Series) -> float`

计算IC (信息系数)
Calculate IC (Information Coefficient)

**参数 Parameters**:
- `predictions` (pd.Series): 预测值
  Predictions
- `returns` (pd.Series): 实际收益率
  Actual returns

**返回 Returns**:
- `float`: IC值
  IC value

**示例 Example**:
```python
from src.utils.metrics_utils import calculate_ic

ic = calculate_ic(predictions, actual_returns)
print(f"IC: {ic:.3f}")
```

#### `calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.03) -> float`

计算夏普比率
Calculate Sharpe ratio

**参数 Parameters**:
- `returns` (pd.Series): 收益率序列
  Returns series
- `risk_free_rate` (float): 无风险利率
  Risk-free rate

**返回 Returns**:
- `float`: 夏普比率
  Sharpe ratio

**示例 Example**:
```python
from src.utils.metrics_utils import calculate_sharpe_ratio

sharpe = calculate_sharpe_ratio(returns, risk_free_rate=0.03)
print(f"夏普比率: {sharpe:.2f}")
```

#### `calculate_max_drawdown(returns: pd.Series) -> float`

计算最大回撤
Calculate maximum drawdown

**参数 Parameters**:
- `returns` (pd.Series): 收益率序列
  Returns series

**返回 Returns**:
- `float`: 最大回撤
  Maximum drawdown

**示例 Example**:
```python
from src.utils.metrics_utils import calculate_max_drawdown

max_dd = calculate_max_drawdown(returns)
print(f"最大回撤: {max_dd:.2%}")
```

---

## 完整示例

### 端到端训练和回测

```python
from src.core.config_manager import ConfigManager
from src.core.data_manager import DataManager
from src.core.model_factory import ModelFactory
from src.application.training_manager import TrainingManager
from src.application.backtest_manager import BacktestManager
from src.models.data_models import TrainingConfig, DatasetConfig, BacktestConfig

# 1. 初始化配置
config_mgr = ConfigManager()
config = config_mgr.get_config()

# 2. 初始化数据管理器
data_mgr = DataManager(config)

# 3. 初始化模型工厂
model_factory = ModelFactory()

# 4. 训练模型
trainer = TrainingManager(config, data_mgr, model_factory)

dataset_config = DatasetConfig(
    instruments="csi300",
    start_time="2020-01-01",
    end_time="2022-12-31",
    features=["$open", "$high", "$low", "$close", "$volume"],
    label="Ref($close, -1) / $close - 1"
)

training_config = TrainingConfig(
    model_type="lgbm",
    dataset_config=dataset_config,
    model_params={"learning_rate": 0.05, "num_leaves": 63},
    training_params={"n_estimators": 200},
    experiment_name="my_experiment"
)

result = trainer.train_model(training_config)
print(f"训练完成，模型ID: {result.model_id}")
print(f"验证集IC: {result.metrics['valid_ic']:.3f}")

# 5. 运行回测
bt_mgr = BacktestManager(config)

backtest_config = BacktestConfig(
    strategy_config={"topk": 30, "rebalance_freq": 5},
    executor_config={"trade_exchange": "exchange", "deal_price": "close"},
    benchmark="SH000300"
)

bt_result = bt_mgr.run_backtest(
    model_id=result.model_id,
    start_date="2023-01-01",
    end_date="2023-12-31",
    config=backtest_config
)

print(f"回测完成")
print(f"总收益率: {bt_result.metrics['total_return']:.2%}")
print(f"夏普比率: {bt_result.metrics['sharpe_ratio']:.2f}")
print(f"最大回撤: {bt_result.metrics['max_drawdown']:.2%}")
```

---

## 错误处理

所有模块都遵循统一的错误处理规范：

### 自定义异常

```python
class QlibTradingError(Exception):
    """基础异常类 Base exception class"""
    pass

class ConfigError(QlibTradingError):
    """配置错误 Configuration error"""
    pass

class DataError(QlibTradingError):
    """数据错误 Data error"""
    pass

class ModelError(QlibTradingError):
    """模型错误 Model error"""
    pass

class TrainingError(QlibTradingError):
    """训练错误 Training error"""
    pass
```

### 错误处理示例

```python
from src.core.config_manager import ConfigManager, ConfigError

try:
    config_mgr = ConfigManager("invalid_config.yaml")
except ConfigError as e:
    print(f"配置错误: {e}")
    # 使用默认配置
    config_mgr = ConfigManager()
except Exception as e:
    print(f"未知错误: {e}")
    raise
```

---

## 配置参考

### 完整配置示例

```yaml
# config/default_config.yaml

# 数据配置 Data configuration
data:
  provider_uri: "~/.qlib/qlib_data/cn_data"
  region: "cn"
  instruments: "csi300"
  start_time: "2020-01-01"
  end_time: "2023-12-31"

# 模型配置 Model configuration
model:
  default_type: "lgbm"
  save_dir: "model_registry"
  
# MLflow配置 MLflow configuration
mlflow:
  enabled: true
  tracking_uri: "file:./mlruns"
  experiment_name: "qlib_trading"
  
# 日志配置 Logging configuration
logging:
  level: "INFO"
  log_dir: "logs"
  max_size: "100MB"
  backup_count: 5
  
# 回测配置 Backtest configuration
backtest:
  initial_capital: 1000000
  benchmark: "SH000300"
  top_k: 30
  rebalance_freq: 5
  
# 风险控制 Risk control
risk:
  max_position_size: 0.1
  max_positions: 30
  stop_loss: -0.05
  max_drawdown: -0.15
```

---

**更多信息请参考**:
- [快速开始指南](quick_start.md)
- [用户手册](user_guide.md)
- [GitHub仓库](https://github.com/yourusername/QuantitationTranding)

---

**文档版本**: 1.0  
**最后更新**: 2024-01-01
