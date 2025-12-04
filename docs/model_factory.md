# Model Factory Documentation
# 模型工厂文档

## Overview / 概述

The ModelFactory provides a factory pattern for creating different types of quantitative trading models supported by qlib. It simplifies model creation by providing:

模型工厂为创建qlib支持的各种量化交易模型提供了工厂模式。它通过以下方式简化模型创建：

- Direct model creation with custom parameters / 使用自定义参数直接创建模型
- Template-based model creation / 基于模板创建模型
- Parameter validation / 参数验证
- Model type management / 模型类型管理

## Supported Model Types / 支持的模型类型

### 1. LightGBM (lgbm)
- **Description**: Gradient boosting model, best for general purpose quantitative trading
- **描述**: 梯度提升模型，适合通用量化交易
- **Use Cases**: Medium to long-term stock prediction, high accuracy requirements
- **适用场景**: 中长期股票预测，高准确率要求

### 2. Linear (linear)
- **Description**: Linear regression model, simple and interpretable
- **描述**: 线性回归模型，简单且可解释
- **Use Cases**: High interpretability requirements, small datasets
- **适用场景**: 高可解释性要求，小数据集

### 3. MLP (mlp)
- **Description**: Multi-layer perceptron neural network
- **描述**: 多层感知机神经网络
- **Use Cases**: Complex non-linear patterns, large datasets
- **适用场景**: 复杂非线性模式，大数据集

## Usage Examples / 使用示例

### Basic Usage / 基本使用

```python
from src.core.model_factory import ModelFactory

# Create factory instance
factory = ModelFactory()

# List available model types
model_types = factory.list_available_models()
print(model_types)  # ['lgbm', 'linear', 'mlp']

# Create a LightGBM model with custom parameters
model = factory.create_model('lgbm', {
    'num_boost_round': 100,
    'learning_rate': 0.1,
    'max_depth': 6
})

# Create a linear model
model = factory.create_model('linear', {
    'estimator': 'ridge',
    'alpha': 0.05
})
```

### Template-Based Creation / 基于模板创建

```python
from src.core.model_factory import ModelFactory

factory = ModelFactory()

# List available templates
templates = factory.list_template_names()
print(templates)
# ['lgbm_default', 'linear_default', 'mlp_default', 
#  'lgbm_conservative', 'lgbm_aggressive']

# Create model from template with default parameters
model = factory.create_model_from_template('lgbm_default')

# Create model from template with custom parameters
model = factory.create_model_from_template(
    'lgbm_default',
    {'num_boost_round': 200}  # Override default
)

# Get template information
template = factory.get_template('lgbm_default')
print(f"Model type: {template.model_type}")
print(f"Description: {template.description}")
print(f"Default params: {template.default_params}")
```

### Available Templates / 可用模板

#### 1. lgbm_default
- **Type**: LightGBM
- **Description**: Default LightGBM model for general quantitative trading
- **描述**: 通用量化交易的默认LightGBM模型
- **Expected Performance**: IC: 0.08, Annual Return: 20%, Sharpe: 1.5

#### 2. lgbm_conservative
- **Type**: LightGBM
- **Description**: Conservative model for risk-averse investors
- **描述**: 风险厌恶型投资者的保守模型
- **Expected Performance**: IC: 0.06, Annual Return: 15%, Sharpe: 1.3

#### 3. lgbm_aggressive
- **Type**: LightGBM
- **Description**: Aggressive model for risk-seeking investors
- **描述**: 风险偏好型投资者的进取模型
- **Expected Performance**: IC: 0.10, Annual Return: 30%, Sharpe: 1.6

#### 4. linear_default
- **Type**: Linear
- **Description**: Default linear regression model
- **描述**: 默认线性回归模型
- **Expected Performance**: IC: 0.05, Annual Return: 12%, Sharpe: 1.0

#### 5. mlp_default
- **Type**: MLP
- **Description**: Default neural network model
- **描述**: 默认神经网络模型
- **Expected Performance**: IC: 0.10, Annual Return: 25%, Sharpe: 1.8

## Parameter Validation / 参数验证

The ModelFactory automatically validates parameters for each model type:

模型工厂自动验证每种模型类型的参数：

### LightGBM Parameters

- `loss`: Must be 'mse' or 'binary' / 必须是'mse'或'binary'
- `num_boost_round`: Must be positive integer / 必须是正整数
- `learning_rate`: Must be positive number / 必须是正数
- `max_depth`: Must be positive integer / 必须是正整数

### Linear Model Parameters

- `estimator`: Must be one of ['ols', 'nnls', 'ridge', 'lasso']
- `alpha`: Must be non-negative number / 必须是非负数
- `fit_intercept`: Must be boolean / 必须是布尔值

### MLP Parameters

- `lr`: Must be positive number / 必须是正数
- `n_epochs`: Must be positive integer / 必须是正整数
- `batch_size`: Must be positive integer / 必须是正整数
- `optimizer`: Must be one of ['adam', 'sgd', 'gd']
- `loss`: Must be one of ['mse', 'mae']

## Error Handling / 错误处理

The ModelFactory provides clear error messages in both Chinese and English:

模型工厂提供中英文双语的清晰错误信息：

```python
# Invalid model type
try:
    factory.create_model('invalid_type')
except ValueError as e:
    print(e)
    # Output: 不支持的模型类型: invalid_type。支持的类型: lgbm, linear, mlp
    #         Unsupported model type: invalid_type. Available types: lgbm, linear, mlp

# Invalid parameters
try:
    factory.create_model('lgbm', {'loss': 'invalid'})
except ValueError as e:
    print(e)
    # Output: LightGBM loss必须是'mse'或'binary'，当前值: invalid
    #         LightGBM loss must be 'mse' or 'binary', got: invalid
```

## API Reference / API参考

### ModelFactory Class

#### `__init__(template_manager: Optional[ModelTemplateManager] = None)`
Initialize the model factory.
初始化模型工厂。

#### `create_model(model_type: str, params: Optional[Dict[str, Any]] = None)`
Create a model instance by type and parameters.
根据类型和参数创建模型实例。

#### `create_model_from_template(template_name: str, custom_params: Optional[Dict[str, Any]] = None)`
Create a model from a pre-configured template.
从预配置的模板创建模型。

#### `get_template(template_name: str) -> ModelTemplate`
Get a template by name.
根据名称获取模板。

#### `list_available_models() -> list`
List all available model types.
列出所有可用的模型类型。

#### `list_templates() -> list`
List all available templates.
列出所有可用的模板。

#### `list_template_names() -> list`
List all template names.
列出所有模板名称。

## Requirements / 依赖要求

- qlib >= 0.9.0
- lightgbm >= 3.3.0 (for LightGBM models)
- scikit-learn >= 1.0.0 (for Linear models)
- torch >= 1.10.0 (for MLP models)

## Notes / 注意事项

1. The ModelFactory uses lazy loading for qlib models to avoid import errors during testing.
   模型工厂使用延迟加载qlib模型以避免测试时的导入错误。

2. If a model type's dependencies are not installed, that model type will not be available.
   如果某个模型类型的依赖未安装，该模型类型将不可用。

3. All parameters are validated before model creation to provide early error detection.
   所有参数在模型创建前都会被验证，以提供早期错误检测。

4. Templates can be customized by modifying the `config/model_templates.yaml` file.
   可以通过修改`config/model_templates.yaml`文件来自定义模板。

## See Also / 参见

- [Model Templates Configuration](../config/model_templates.yaml)
- [Training Manager Documentation](training_manager.md)
- [Qlib Documentation](https://qlib.readthedocs.io/)
