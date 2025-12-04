# Model Template System Documentation
# 模型模板系统文档

## Overview (概述)

The Model Template System provides pre-configured model templates for quantitative trading. Each template includes optimized hyperparameters, expected performance metrics, and usage guidelines.

模型模板系统为量化交易提供预配置的模型模板。每个模板包含优化的超参数、预期性能指标和使用指南。

## Available Templates (可用模板)

### 1. LGBM Default (默认LightGBM模板)

**Name:** `lgbm_default`

**Description:** General-purpose LightGBM model suitable for most quantitative trading scenarios.

**适用场景：**
- Medium to long-term stock prediction (1-4 weeks holding period)
- Requires high prediction accuracy
- Large dataset (1000+ samples)
- High feature dimensionality (50+ features)

**优势：**
- Fast training speed
- High prediction accuracy
- Robust to missing values and outliers
- Good interpretability

**Expected Performance:**
- IC: 0.08
- Annual Return: 20%
- Sharpe Ratio: 1.5
- Max Drawdown: 15%

### 2. Linear Default (默认线性模型)

**Name:** `linear_default`

**Description:** Simple and stable linear regression model with high interpretability.

**适用场景：**
- Requires high interpretability
- Clear linear relationships between features
- Small dataset (<1000 samples)
- Pursues model stability

**优势：**
- Extremely fast training
- Best interpretability
- Less prone to overfitting
- Low data quality requirements

**Expected Performance:**
- IC: 0.05
- Annual Return: 12%
- Sharpe Ratio: 1.0
- Max Drawdown: 12%

### 3. MLP Default (默认多层感知机)

**Name:** `mlp_default`

**Description:** Multi-layer neural network model for capturing complex non-linear relationships.

**适用场景：**
- Complex non-linear relationships between features
- Sufficient data (5000+ samples)
- Pursues highest prediction accuracy
- GPU acceleration available

**优势：**
- Can learn complex patterns
- Strong prediction capability
- Suitable for high-frequency trading
- Can handle temporal dependencies

**注意事项：**
- Longer training time
- Requires more data
- Prone to overfitting
- Lower interpretability

**Expected Performance:**
- IC: 0.10
- Annual Return: 25%
- Sharpe Ratio: 1.8
- Max Drawdown: 18%

### 4. LGBM Conservative (保守型LightGBM)

**Name:** `lgbm_conservative`

**Description:** Conservative LightGBM model for risk-averse investors.

**适用场景：**
- Risk-averse investors
- Pursues stable returns
- Accepts lower returns
- Cannot tolerate large drawdowns

**特点：**
- Reduced model complexity
- Lower overfitting risk
- More conservative predictions
- Lower turnover rate

**Expected Performance:**
- IC: 0.06
- Annual Return: 15%
- Sharpe Ratio: 1.3
- Max Drawdown: 10%

### 5. LGBM Aggressive (进取型LightGBM)

**Name:** `lgbm_aggressive`

**Description:** Aggressive LightGBM model for risk-seeking investors.

**适用场景：**
- Risk-seeking investors
- Pursues high returns
- Can tolerate large drawdowns
- Short-term trading (1-2 weeks holding)

**特点：**
- Higher model complexity
- More aggressive predictions
- Higher turnover rate
- Larger return volatility

**Expected Performance:**
- IC: 0.10
- Annual Return: 30%
- Sharpe Ratio: 1.6
- Max Drawdown: 22%

## Usage (使用方法)

### Basic Usage (基本使用)

```python
from src.templates import ModelTemplateManager

# Initialize the template manager
manager = ModelTemplateManager()

# List all available templates
templates = manager.list_templates()
for template in templates:
    print(f"{template.name}: {template.description}")

# Get a specific template
lgbm_template = manager.get_template("lgbm_default")

# Access template properties
print(f"Model Type: {lgbm_template.model_type}")
print(f"Default Parameters: {lgbm_template.default_params}")
print(f"Expected Performance: {lgbm_template.expected_performance}")
```

### Using Templates for Training (使用模板进行训练)

```python
from src.templates import ModelTemplateManager
from src.models import TrainingConfig, DatasetConfig

# Get template
manager = ModelTemplateManager()
template = manager.get_template("lgbm_default")

# Create dataset configuration
dataset_config = DatasetConfig(
    instruments="csi300",
    start_time="2020-01-01",
    end_time="2023-12-31",
    features=["$close", "$volume", "$high", "$low"],
    label="Ref($close, -1) / $close - 1"
)

# Create training configuration using template
training_config = TrainingConfig(
    model_type=template.model_type,
    dataset_config=dataset_config,
    model_params=template.default_params,  # Use template's default params
    training_params={"epochs": 100},
    experiment_name="my_experiment"
)

# Use with TrainingManager
# training_manager.train_model(training_config)
```

### Customizing Template Parameters (自定义模板参数)

```python
from src.templates import ModelTemplateManager

# Get template
manager = ModelTemplateManager()
template = manager.get_template("lgbm_default")

# Get default parameters
params = template.default_params.copy()

# Customize parameters
params['learning_rate'] = 0.05  # Reduce learning rate
params['num_boost_round'] = 200  # Increase iterations

# Use customized parameters for training
training_config = TrainingConfig(
    model_type=template.model_type,
    dataset_config=dataset_config,
    model_params=params,  # Use customized params
    training_params={"epochs": 100},
    experiment_name="my_experiment"
)
```

### Comparing Templates (比较模板)

```python
from src.templates import ModelTemplateManager

manager = ModelTemplateManager()

# Compare expected returns
templates = manager.list_templates()
for template in sorted(templates, 
                       key=lambda t: t.expected_performance.get('annual_return', 0),
                       reverse=True):
    expected_return = template.expected_performance.get('annual_return', 'N/A')
    sharpe = template.expected_performance.get('sharpe_ratio', 'N/A')
    print(f"{template.name}: Return={expected_return}, Sharpe={sharpe}")
```

## Template Selection Guide (模板选择指南)

### Choose LGBM Default if: (选择默认LGBM如果：)
- You want a balanced approach
- You have moderate amount of data (1000+ samples)
- You need good accuracy with reasonable training time
- You're new to quantitative trading

### Choose Linear Default if: (选择线性模型如果：)
- You need high interpretability
- You have limited data (<1000 samples)
- You want the fastest training time
- You prefer simple, stable models

### Choose MLP Default if: (选择MLP如果：)
- You have large amounts of data (5000+ samples)
- You need the highest possible accuracy
- You have GPU resources available
- You're comfortable with complex models

### Choose LGBM Conservative if: (选择保守型LGBM如果：)
- You're risk-averse
- You prefer stable, predictable returns
- You cannot tolerate large drawdowns
- You're investing retirement funds

### Choose LGBM Aggressive if: (选择进取型LGBM如果：)
- You're risk-seeking
- You want maximum returns
- You can tolerate volatility
- You're doing short-term trading

## Configuration File (配置文件)

Templates are defined in `config/model_templates.yaml`. You can add custom templates by following this format:

```yaml
templates:
  - name: "my_custom_template"
    model_type: "lgbm"
    description: "My custom LightGBM template"
    use_case: |
      适用场景：
      - Your specific use case
      
      优势：
      - Your advantages
    default_params:
      loss: "mse"
      num_boost_round: 100
      learning_rate: 0.1
      # ... other parameters
    expected_performance:
      ic: 0.08
      annual_return: 0.20
      sharpe_ratio: 1.5
      max_drawdown: 0.15
```

## API Reference (API参考)

### ModelTemplateManager

**Methods:**

- `__init__(template_config_path: Optional[str] = None)`: Initialize the manager
- `get_template(name: str) -> ModelTemplate`: Get a template by name
- `list_templates() -> List[ModelTemplate]`: Get all templates
- `list_template_names() -> List[str]`: Get all template names
- `has_template(name: str) -> bool`: Check if template exists
- `get_template_info(name: str) -> Dict[str, str]`: Get basic template info

### ModelTemplate

**Attributes:**

- `name: str`: Template name
- `model_type: str`: Model type (e.g., "lgbm", "linear", "mlp")
- `description: str`: Template description
- `use_case: str`: When to use this template
- `default_params: Dict[str, Any]`: Default hyperparameters
- `expected_performance: Dict[str, float]`: Expected performance metrics

## Best Practices (最佳实践)

1. **Start with Default Templates**: Begin with the default templates before customizing
2. **Validate on Your Data**: Expected performance may vary with your specific data
3. **Monitor Performance**: Track actual performance vs. expected performance
4. **Iterate Gradually**: Make small parameter changes and test
5. **Document Changes**: Keep track of parameter modifications
6. **Use Appropriate Template**: Match template to your risk tolerance and data size

## Troubleshooting (故障排除)

### Template Not Found
```python
# Error: KeyError: "Template 'xxx' not found"
# Solution: Check available templates
manager = ModelTemplateManager()
print(manager.list_template_names())
```

### Configuration File Not Found
```python
# Error: FileNotFoundError: Template configuration file not found
# Solution: Ensure config/model_templates.yaml exists
# Or specify custom path:
manager = ModelTemplateManager("/path/to/your/templates.yaml")
```

### Invalid Template Configuration
```python
# Error: ValueError: Invalid template configuration
# Solution: Check YAML syntax and required fields
# Required fields: name, model_type, description, use_case, default_params
```

## Examples (示例)

See `examples/demo_model_templates.py` for a complete working example.

## Support (支持)

For questions or issues with the model template system, please refer to:
- Main documentation: `docs/README.md`
- User guide: `docs/user_guide.md`
- API reference: `docs/api_reference.md`
