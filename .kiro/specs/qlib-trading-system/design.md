# Design Document

## Overview

本系统是一个基于qlib的量化交易平台，旨在为新手和专业用户提供完整的模型训练、回测和交易信号生成功能。系统采用模块化设计，将数据管理、模型训练、回测引擎、信号生成和用户界面分离，确保易用性和可扩展性。

核心特性：
- 交互式命令行界面，无需编程即可使用
- 集成MLflow进行实验追踪和模型管理
- 预配置的模型模板，开箱即用
- 完整的中文文档和教程
- 可视化的训练监控和回测报告

## Architecture

系统采用分层架构设计：

```
┌─────────────────────────────────────────────────────────┐
│                    CLI Interface Layer                   │
│  (交互式菜单、命令解析、进度显示、帮助系统)                │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                   Application Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Training     │  │ Backtest     │  │ Signal       │  │
│  │ Manager      │  │ Manager      │  │ Generator    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Model        │  │ Visualization│  │ Report       │  │
│  │ Registry     │  │ Manager      │  │ Generator    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                     Core Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Data         │  │ Model        │  │ Config       │  │
│  │ Manager      │  │ Factory      │  │ Manager      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Qlib         │  │ MLflow       │  │ Logger       │  │
│  │ Framework    │  │ Tracking     │  │ System       │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 架构说明

1. **CLI Interface Layer**: 提供用户交互界面，包括菜单系统、参数收集、进度显示
2. **Application Layer**: 实现业务逻辑，包括训练、回测、信号生成等功能模块
3. **Core Layer**: 提供核心服务，包括数据管理、模型工厂、配置管理
4. **Infrastructure Layer**: 封装第三方框架，包括qlib、MLflow和日志系统

## Components and Interfaces

### 1. CLI Interface Layer

#### MainCLI
主命令行界面控制器

**职责**:
- 显示主菜单
- 路由用户选择到对应功能
- 处理全局命令（帮助、退出等）

**接口**:
```python
class MainCLI:
    def run(self) -> None
    def show_menu(self) -> None
    def handle_choice(self, choice: str) -> None
```

#### InteractivePrompt
交互式参数收集器

**职责**:
- 收集用户输入
- 验证输入有效性
- 提供默认值和提示

**接口**:
```python
class InteractivePrompt:
    def ask_text(self, prompt: str, default: str = None) -> str
    def ask_choice(self, prompt: str, choices: List[str]) -> str
    def ask_number(self, prompt: str, min_val: float, max_val: float, default: float) -> float
    def ask_date(self, prompt: str, default: str = None) -> str
    def confirm(self, prompt: str, default: bool = True) -> bool
```

### 2. Application Layer

#### TrainingManager
模型训练管理器

**职责**:
- 协调训练流程
- 管理训练配置
- 记录训练指标

**接口**:
```python
class TrainingManager:
    def train_model(self, config: TrainingConfig) -> TrainingResult
    def train_from_template(self, template_name: str, custom_params: Dict = None) -> TrainingResult
    def list_templates(self) -> List[ModelTemplate]
```

#### BacktestManager
回测管理器

**职责**:
- 执行回测流程
- 计算性能指标
- 生成回测报告

**接口**:
```python
class BacktestManager:
    def run_backtest(self, model_id: str, start_date: str, end_date: str, config: BacktestConfig) -> BacktestResult
    def calculate_metrics(self, returns: pd.Series, benchmark: pd.Series) -> Dict[str, float]
```

#### SignalGenerator
交易信号生成器

**职责**:
- 生成交易信号
- 应用风险控制
- 解释信号原因

**接口**:
```python
class SignalGenerator:
    def generate_signals(self, model_id: str, date: str, portfolio: Portfolio) -> List[Signal]
    def explain_signal(self, signal: Signal) -> SignalExplanation
```

#### ModelRegistry
模型注册表

**职责**:
- 注册和管理模型
- 版本控制
- 模型元数据管理

**接口**:
```python
class ModelRegistry:
    def register_model(self, model: Model, metadata: ModelMetadata) -> str
    def get_model(self, model_id: str) -> Model
    def list_models(self, filter: ModelFilter = None) -> List[ModelInfo]
    def set_production_model(self, model_id: str) -> None
```

#### VisualizationManager
可视化管理器

**职责**:
- 生成图表
- 创建可视化报告
- 导出图片

**接口**:
```python
class VisualizationManager:
    def plot_cumulative_returns(self, returns: pd.Series, benchmark: pd.Series, save_path: str) -> None
    def plot_training_curve(self, metrics: Dict[str, List[float]], save_path: str) -> None
    def plot_position_distribution(self, portfolio: Portfolio, save_path: str) -> None
```

#### ReportGenerator
报告生成器

**职责**:
- 生成文本报告
- 汇总性能指标
- 创建HTML报告

**接口**:
```python
class ReportGenerator:
    def generate_training_report(self, result: TrainingResult) -> str
    def generate_backtest_report(self, result: BacktestResult) -> str
    def generate_html_report(self, result: BacktestResult, output_path: str) -> None
```

### 3. Core Layer

#### DataManager
数据管理器

**职责**:
- 初始化qlib数据
- 下载和更新数据
- 验证数据完整性

**接口**:
```python
class DataManager:
    def initialize(self, data_path: str, region: str) -> None
    def download_data(self, region: str, target_dir: str, interval: str = "day") -> None
    def validate_data(self, start_date: str, end_date: str) -> ValidationResult
    def get_data_info(self) -> DataInfo
```

#### ModelFactory
模型工厂

**职责**:
- 创建模型实例
- 管理模型模板
- 配置模型参数

**接口**:
```python
class ModelFactory:
    def create_model(self, model_type: str, params: Dict) -> Model
    def get_template(self, template_name: str) -> ModelTemplate
    def list_available_models(self) -> List[str]
```

#### ConfigManager
配置管理器

**职责**:
- 加载和保存配置
- 验证配置
- 提供默认配置

**接口**:
```python
class ConfigManager:
    def load_config(self, config_path: str) -> Config
    def save_config(self, config: Config, config_path: str) -> None
    def get_default_config(self) -> Config
    def validate_config(self, config: Config) -> List[str]
```

### 4. Infrastructure Layer

#### QlibWrapper
Qlib框架封装

**职责**:
- 初始化qlib
- 提供统一的qlib接口
- 处理qlib异常

**接口**:
```python
class QlibWrapper:
    def init(self, provider_uri: str, region: str, exp_manager_config: Dict) -> None
    def get_data(self, instruments: str, fields: List[str], start_time: str, end_time: str) -> pd.DataFrame
    def is_initialized(self) -> bool
```

#### MLflowTracker
MLflow追踪器

**职责**:
- 记录实验
- 追踪指标
- 管理模型版本

**接口**:
```python
class MLflowTracker:
    def start_run(self, experiment_name: str, run_name: str) -> str
    def log_params(self, params: Dict) -> None
    def log_metrics(self, metrics: Dict, step: int = None) -> None
    def log_model(self, model: Model, artifact_path: str) -> None
    def end_run(self) -> None
```

#### LoggerSystem
日志系统

**职责**:
- 配置日志
- 记录日志
- 管理日志文件

**接口**:
```python
class LoggerSystem:
    def setup(self, log_dir: str, log_level: str) -> None
    def get_logger(self, name: str) -> Logger
    def rotate_logs(self) -> None
```

## Data Models

### TrainingConfig
```python
@dataclass
class TrainingConfig:
    model_type: str
    dataset_config: DatasetConfig
    model_params: Dict[str, Any]
    training_params: Dict[str, Any]
    experiment_name: str
```

### DatasetConfig
```python
@dataclass
class DatasetConfig:
    instruments: str  # e.g., "csi300"
    start_time: str
    end_time: str
    features: List[str]
    label: str
```

### TrainingResult
```python
@dataclass
class TrainingResult:
    model_id: str
    metrics: Dict[str, float]
    training_time: float
    model_path: str
    experiment_id: str
```

### BacktestConfig
```python
@dataclass
class BacktestConfig:
    strategy_config: Dict[str, Any]
    executor_config: Dict[str, Any]
    benchmark: str
```

### BacktestResult
```python
@dataclass
class BacktestResult:
    returns: pd.Series
    positions: pd.DataFrame
    metrics: Dict[str, float]
    trades: List[Trade]
```

### Signal
```python
@dataclass
class Signal:
    stock_code: str
    action: str  # "buy", "sell", "hold"
    score: float
    confidence: float
    timestamp: str
```

### SignalExplanation
```python
@dataclass
class SignalExplanation:
    signal: Signal
    main_factors: List[Tuple[str, float]]  # (factor_name, contribution)
    risk_level: str
    description: str
```

### ModelTemplate
```python
@dataclass
class ModelTemplate:
    name: str
    model_type: str
    description: str
    use_case: str
    default_params: Dict[str, Any]
    expected_performance: Dict[str, float]
```

### Portfolio
```python
@dataclass
class Portfolio:
    positions: Dict[str, float]  # stock_code -> quantity
    cash: float
    total_value: float
```

### ModelMetadata
```python
@dataclass
class ModelMetadata:
    model_name: str
    version: str
    training_date: str
    performance_metrics: Dict[str, float]
    dataset_info: DatasetConfig
    hyperparameters: Dict[str, Any]
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Qlib initialization succeeds for valid configurations
*For any* valid data path and region configuration, initializing qlib should succeed and allow data access
**Validates: Requirements 1.1**

### Property 2: Data validation returns time range after initialization
*For any* successfully initialized qlib environment, querying data info should return a valid time range
**Validates: Requirements 1.3**

### Property 3: MLflow initialization when configured
*For any* configuration that includes MLflow settings, system initialization should create an MLflow experiment
**Validates: Requirements 1.4**

### Property 4: Training loads dataset for valid config
*For any* valid training configuration, starting training should successfully load the specified dataset
**Validates: Requirements 2.1**

### Property 5: Model training completes for supported types
*For any* supported model type with valid parameters, training should complete and produce a model
**Validates: Requirements 2.2**

### Property 6: Training metrics logged to MLflow
*For any* training process, metrics should be logged to MLflow during training
**Validates: Requirements 2.3, 3.2**

### Property 7: Model saved after training
*For any* successfully completed training, a model file and metadata should be saved
**Validates: Requirements 2.4**

### Property 8: Multiple models trained sequentially
*For any* configuration specifying multiple models, all models should be trained and results compared
**Validates: Requirements 2.5**

### Property 9: MLflow run created for each training
*For any* training start, a new MLflow run should be created with a unique ID
**Validates: Requirements 3.1**

### Property 10: Hyperparameters logged to MLflow
*For any* training process, all hyperparameters should be logged to MLflow
**Validates: Requirements 3.3**

### Property 11: Final metrics recorded after training
*For any* completed training, final performance metrics and training time should be recorded
**Validates: Requirements 3.4**

### Property 12: Backtest generates signals from model
*For any* valid model and time period, backtest should generate prediction signals
**Validates: Requirements 4.1**

### Property 13: Backtest executes with signals
*For any* sequence of signals, backtest engine should simulate trades
**Validates: Requirements 4.2**

### Property 14: Backtest calculates required metrics
*For any* completed backtest, all required metrics (returns, Sharpe ratio, max drawdown) should be calculated
**Validates: Requirements 4.3**

### Property 15: Backtest saves report and trades
*For any* completed backtest, a report file and trade details should be saved
**Validates: Requirements 4.4**

### Property 16: Excess returns calculated with benchmark
*For any* backtest with a configured benchmark, excess returns relative to benchmark should be calculated
**Validates: Requirements 4.5**

### Property 17: Cumulative returns chart generated
*For any* backtest result, a cumulative returns chart file should be generated
**Validates: Requirements 5.1**

### Property 18: Report contains all required charts
*For any* visualization report, it should contain position distribution and sector distribution charts
**Validates: Requirements 5.2**

### Property 19: Prediction analysis returns score distribution
*For any* prediction request, the system should return score distribution for stocks
**Validates: Requirements 5.3**

### Property 20: Report compares strategy vs benchmark
*For any* generated report, it should include comparison between strategy and benchmark returns
**Validates: Requirements 5.4**

### Property 21: Multi-model comparison chart generated
*For any* scenario with multiple models, a performance comparison chart should be generated
**Validates: Requirements 5.5**

### Property 22: Signal generation uses latest data
*For any* signal generation request, the system should use the most recent available data
**Validates: Requirements 6.1**

### Property 23: Stocks sorted by prediction score
*For any* prediction result, stocks should be sorted by their prediction scores
**Validates: Requirements 6.2**

### Property 24: Signals respect risk limits
*For any* generated signals, they should comply with configured risk limits
**Validates: Requirements 6.3, 6.5**

### Property 25: Signals include all action types
*For any* signal generation, the output should include buy, sell, and hold recommendations
**Validates: Requirements 6.4**

### Property 26: Models registered after training
*For any* completed model training, the model should be findable in the model registry
**Validates: Requirements 7.1**

### Property 27: Model metadata recorded at registration
*For any* registered model, it should have version, training date, and performance metrics
**Validates: Requirements 7.2**

### Property 28: Model query returns all registered models
*For any* model query, it should return all models that have been registered
**Validates: Requirements 7.3**

### Property 29: Registered models can be loaded
*For any* registered model, it should be loadable and usable for prediction
**Validates: Requirements 7.4**

### Property 30: Better models marked as candidates
*For any* new model with better performance than production model, it should be marked as candidate
**Validates: Requirements 7.5**

### Property 31: Configuration loaded from file
*For any* valid configuration file, system should load all parameters correctly
**Validates: Requirements 8.1**

### Property 32: Config updates applied on restart
*For any* modified configuration, changes should take effect on next system run
**Validates: Requirements 8.4**

### Property 33: Data paths validated in config
*For any* configuration containing data paths, the system should validate path existence
**Validates: Requirements 8.5**

### Property 34: Downloaded data passes validation
*For any* data download completion, the data should pass integrity and format checks
**Validates: Requirements 9.2**

### Property 35: Validated data updates local database
*For any* data that passes validation, it should be written to the local database
**Validates: Requirements 9.3**

### Property 36: Missing values handled by strategy
*For any* data containing missing values, the system should apply the configured filling strategy
**Validates: Requirements 9.5**

### Property 37: Operations logged to file
*For any* system operation, a log entry should be written to the log file
**Validates: Requirements 10.1**

### Property 38: Errors logged with stack trace
*For any* error occurrence, the log should contain detailed stack trace information
**Validates: Requirements 10.2**

### Property 39: Log entries contain required fields
*For any* log entry, it should contain timestamp, log level, and module name
**Validates: Requirements 10.3**

### Property 40: Logs filtered by configured level
*For any* configured log level, only messages at that level or above should be logged
**Validates: Requirements 10.4**

### Property 41: Log files rotated when size exceeded
*For any* log file exceeding size limit, a new log file should be created
**Validates: Requirements 10.5**

### Property 42: Invalid input prompts error and retry
*For any* invalid user input, the system should display an error and allow re-entry
**Validates: Requirements 12.5**

### Property 43: Model templates include descriptions
*For any* model template, it should have description of use case and expected performance
**Validates: Requirements 14.2**

### Property 44: Templates use default parameters
*For any* template-based training, the system should use the template's default parameters
**Validates: Requirements 14.3**

### Property 45: Template training generates report
*For any* completed template training, an easy-to-read performance report should be generated
**Validates: Requirements 14.4**

### Property 46: Signals include confidence scores
*For any* generated trading signal, it should include a confidence score
**Validates: Requirements 15.1**

### Property 47: Signal explanations available
*For any* trading signal, the system should be able to provide an explanation of main factors
**Validates: Requirements 15.2**

### Property 48: Reports include visualizations
*For any* generated report, it should contain charts and visualizations
**Validates: Requirements 15.4**

### Property 49: High-risk predictions marked with warnings
*For any* prediction with high risk level, it should be clearly marked with a warning
**Validates: Requirements 15.5**

## Error Handling

### Error Categories

1. **Configuration Errors**
   - Invalid configuration file format
   - Missing required configuration fields
   - Invalid data paths
   - Unsupported model types

2. **Data Errors**
   - Data source not available
   - Data download failures
   - Data validation failures
   - Missing or corrupted data files

3. **Training Errors**
   - Insufficient data for training
   - Model convergence failures
   - Out of memory errors
   - Invalid hyperparameters

4. **Backtest Errors**
   - Model loading failures
   - Invalid backtest period
   - Insufficient historical data
   - Strategy execution errors

5. **System Errors**
   - MLflow connection failures
   - File system errors
   - Permission errors
   - Network errors

### Error Handling Strategy

1. **Graceful Degradation**: System should continue operating with reduced functionality when possible
2. **Clear Error Messages**: All errors should provide clear, actionable messages in Chinese
3. **Error Recovery**: System should attempt automatic recovery for transient errors
4. **State Preservation**: Errors should not corrupt existing data or models
5. **Logging**: All errors should be logged with full context for debugging

### Error Response Format

```python
@dataclass
class ErrorResponse:
    error_code: str
    error_message: str  # Chinese message for users
    technical_details: str  # Technical details for debugging
    suggested_actions: List[str]  # Suggested fixes
    documentation_link: str  # Link to relevant docs
```

## Testing Strategy

### Unit Testing

Unit tests will verify specific functionality of individual components:

1. **Configuration Management**
   - Test loading valid configurations
   - Test handling invalid configurations
   - Test default configuration generation

2. **Data Management**
   - Test data validation logic
   - Test data path resolution
   - Test data info extraction

3. **Model Factory**
   - Test model creation for each supported type
   - Test template loading
   - Test parameter validation

4. **Signal Generation**
   - Test signal scoring logic
   - Test risk limit enforcement
   - Test signal explanation generation

5. **Visualization**
   - Test chart generation with sample data
   - Test report formatting
   - Test file output

### Property-Based Testing

Property-based tests will verify universal properties across many inputs using the Hypothesis library for Python:

**Configuration**:
- Each property test should run a minimum of 100 iterations
- Each test must be tagged with a comment referencing the correctness property
- Tag format: `# Feature: qlib-trading-system, Property {number}: {property_text}`

**Test Categories**:

1. **Initialization Properties**
   - Property 1: Qlib initialization
   - Property 2: Data validation
   - Property 3: MLflow initialization

2. **Training Properties**
   - Property 4-11: Training pipeline correctness
   - Test with various model types, dataset configs, and hyperparameters

3. **Backtest Properties**
   - Property 12-16: Backtest execution and metrics
   - Test with different time periods and strategies

4. **Visualization Properties**
   - Property 17-21: Chart and report generation
   - Test with various result formats

5. **Signal Generation Properties**
   - Property 22-25: Signal generation and risk management
   - Test with different market conditions and portfolios

6. **Model Registry Properties**
   - Property 26-30: Model management and versioning
   - Test with multiple models and versions

7. **Configuration Properties**
   - Property 31-33: Configuration loading and validation
   - Test with various config formats

8. **Data Management Properties**
   - Property 34-36: Data download and validation
   - Test with different data sources and formats

9. **Logging Properties**
   - Property 37-41: Log recording and rotation
   - Test with various log levels and operations

10. **User Interface Properties**
    - Property 42-49: Input validation and output formatting
    - Test with various user inputs

### Integration Testing

Integration tests will verify end-to-end workflows:

1. **Complete Training Workflow**
   - Initialize system → Load data → Train model → Save model → Verify in registry

2. **Complete Backtest Workflow**
   - Load model → Generate signals → Run backtest → Generate report → Verify results

3. **Complete Signal Generation Workflow**
   - Load model → Get latest data → Generate signals → Explain signals → Verify output

4. **Data Update Workflow**
   - Download data → Validate data → Update database → Verify availability

### Test Data

1. **Synthetic Data**: Generate synthetic market data for testing
2. **Sample Data**: Use qlib's sample dataset for integration tests
3. **Edge Cases**: Create specific datasets for edge case testing

### Testing Tools

- **pytest**: Test framework
- **Hypothesis**: Property-based testing library
- **pytest-cov**: Code coverage measurement
- **pytest-mock**: Mocking framework for unit tests

## Implementation Notes

### Technology Stack

- **Language**: Python 3.8+
- **Core Framework**: qlib (Microsoft Quantitative Investment Platform)
- **Experiment Tracking**: MLflow
- **CLI Framework**: Click or Typer
- **Visualization**: matplotlib, seaborn
- **Testing**: pytest, Hypothesis
- **Configuration**: YAML files
- **Logging**: Python logging module

### Directory Structure

```
QuantitationTranding/
├── src/
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── prompts.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── data_manager.py
│   │   ├── model_factory.py
│   │   └── config_manager.py
│   ├── application/
│   │   ├── __init__.py
│   │   ├── training_manager.py
│   │   ├── backtest_manager.py
│   │   ├── signal_generator.py
│   │   ├── model_registry.py
│   │   ├── visualization_manager.py
│   │   └── report_generator.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── qlib_wrapper.py
│   │   ├── mlflow_tracker.py
│   │   └── logger_system.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── data_models.py
│   └── templates/
│       ├── __init__.py
│       └── model_templates.py
├── tests/
│   ├── unit/
│   ├── property/
│   └── integration/
├── config/
│   ├── default_config.yaml
│   └── model_templates.yaml
├── data/
│   └── cn_data/
├── examples/
│   └── mlruns/
├── logs/
├── docs/
│   ├── quick_start.md
│   ├── user_guide.md
│   └── api_reference.md
├── requirements.txt
├── setup.py
└── README.md
```

### Development Phases

1. **Phase 1: Core Infrastructure**
   - Set up project structure
   - Implement configuration management
   - Implement data manager
   - Implement logging system

2. **Phase 2: Training Pipeline**
   - Implement model factory
   - Implement training manager
   - Integrate MLflow tracking
   - Implement model registry

3. **Phase 3: Backtest and Analysis**
   - Implement backtest manager
   - Implement visualization manager
   - Implement report generator

4. **Phase 4: Signal Generation**
   - Implement signal generator
   - Implement signal explanation
   - Implement risk management

5. **Phase 5: User Interface**
   - Implement CLI interface
   - Implement interactive prompts
   - Implement help system

6. **Phase 6: Documentation and Polish**
   - Write comprehensive documentation
   - Create tutorials and examples
   - Optimize performance
   - Final testing and bug fixes

### Performance Considerations

1. **Data Loading**: Use qlib's efficient data loading mechanisms
2. **Model Training**: Support GPU acceleration when available
3. **Caching**: Cache frequently accessed data and models
4. **Parallel Processing**: Use multiprocessing for batch operations
5. **Memory Management**: Stream large datasets instead of loading entirely into memory

### Security Considerations

1. **Data Privacy**: Ensure market data is stored securely
2. **Model Protection**: Protect trained models from unauthorized access
3. **Configuration Security**: Validate all configuration inputs
4. **Logging**: Avoid logging sensitive information
5. **Dependencies**: Regularly update dependencies for security patches
