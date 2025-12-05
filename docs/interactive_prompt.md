# Interactive Prompt System / 交互式提示系统

## Overview / 概述

The Interactive Prompt System provides a user-friendly way to collect input from users through the command line interface. It includes validation, default values, and error handling.

交互式提示系统提供了一种用户友好的方式，通过命令行界面收集用户输入。它包括验证、默认值和错误处理。

## Features / 特性

- **Text Input / 文本输入**: Collect free-form text with optional defaults
- **Choice Selection / 选择输入**: Present multiple options for user selection
- **Number Input / 数字输入**: Collect numeric values with range validation
- **Date Input / 日期输入**: Collect dates with format validation
- **Confirmation / 确认提示**: Ask yes/no questions
- **Message Display / 消息显示**: Show formatted messages to users
- **Progress Display / 进度显示**: Display progress bars

## Usage / 使用方法

### Basic Setup / 基本设置

```python
from src.cli.interactive_prompt import InteractivePrompt

# Create an instance
prompt = InteractivePrompt()
```

### Text Input / 文本输入

```python
# Simple text input
name = prompt.ask_text("请输入您的姓名 / Enter your name")

# Text input with default value
name = prompt.ask_text("请输入您的姓名 / Enter your name", default="张三")

# Allow empty input
description = prompt.ask_text("请输入描述 / Enter description", allow_empty=True)
```

### Choice Selection / 选择输入

```python
# Present multiple choices
markets = ["中国市场 (A股)", "美国市场", "香港市场"]
market = prompt.ask_choice("请选择投资市场 / Select market", markets)

# With default selection
market = prompt.ask_choice("请选择投资市场 / Select market", markets, default=1)
```

### Number Input / 数字输入

```python
# Float number input
target_return = prompt.ask_number(
    "请输入期望年化收益率 (%) / Enter target return (%)",
    min_val=0,
    max_val=100,
    default=20.0
)

# Integer input
simulation_days = prompt.ask_integer(
    "请输入模拟天数 / Enter simulation days",
    min_val=1,
    max_val=365,
    default=30
)
```

### Date Input / 日期输入

```python
# Date input with default format (YYYY-MM-DD)
start_date = prompt.ask_date(
    "请输入开始日期 / Enter start date",
    default="2024-01-01"
)

# Custom date format
date = prompt.ask_date(
    "请输入日期 / Enter date",
    date_format="%d/%m/%Y"
)
```

### Confirmation / 确认提示

```python
# Yes/no confirmation
confirmed = prompt.confirm("是否继续 / Continue?", default=True)

if confirmed:
    print("User confirmed")
else:
    print("User cancelled")
```

### Message Display / 消息显示

```python
# Display different types of messages
prompt.display_message("这是一条信息 / This is info", "info")
prompt.display_message("操作成功 / Success", "success")
prompt.display_message("请注意 / Warning", "warning")
prompt.display_message("发生错误 / Error", "error")
```

### Progress Display / 进度显示

```python
import time

total_steps = 10
for i in range(total_steps + 1):
    prompt.display_progress(i, total_steps, "处理中... / Processing...")
    time.sleep(0.1)
```

## Complete Workflow Example / 完整工作流程示例

```python
from src.cli.interactive_prompt import InteractivePrompt

def configure_trading_system():
    """Configure trading system through interactive prompts"""
    prompt = InteractivePrompt()
    
    # Welcome message
    prompt.display_message("欢迎使用量化交易系统 / Welcome to Trading System", "info")
    
    # Step 1: Market selection
    markets = ["中国市场 (A股)", "美国市场", "香港市场"]
    market = prompt.ask_choice("步骤1: 选择市场 / Step 1: Select market", markets, default=1)
    
    # Step 2: Asset type selection
    asset_types = ["股票", "基金", "ETF"]
    asset_type = prompt.ask_choice("步骤2: 选择品类 / Step 2: Select asset type", asset_types)
    
    # Step 3: Target return
    target_return = prompt.ask_number(
        "步骤3: 输入目标收益率 (%) / Step 3: Enter target return (%)",
        min_val=0,
        max_val=100,
        default=20.0
    )
    
    # Step 4: Risk preference
    risk_levels = ["保守型 (低风险)", "稳健型 (中等风险)", "进取型 (高风险)"]
    risk_level = prompt.ask_choice("步骤4: 选择风险偏好 / Step 4: Select risk preference", risk_levels, default=2)
    
    # Step 5: Simulation period
    simulation_days = prompt.ask_integer(
        "步骤5: 输入模拟天数 / Step 5: Enter simulation days",
        min_val=1,
        max_val=365,
        default=30
    )
    
    # Display summary
    print("\n" + "="*60)
    print("配置总结 / Configuration Summary")
    print("="*60)
    print(f"市场 / Market: {market}")
    print(f"品类 / Asset Type: {asset_type}")
    print(f"目标收益率 / Target Return: {target_return}%")
    print(f"风险偏好 / Risk Preference: {risk_level}")
    print(f"模拟天数 / Simulation Days: {simulation_days}")
    print("="*60)
    
    # Confirmation
    confirmed = prompt.confirm("\n确认配置 / Confirm configuration?", default=True)
    
    if confirmed:
        prompt.display_message("配置已确认 / Configuration confirmed", "success")
        return {
            'market': market,
            'asset_type': asset_type,
            'target_return': target_return,
            'risk_level': risk_level,
            'simulation_days': simulation_days
        }
    else:
        prompt.display_message("配置已取消 / Configuration cancelled", "warning")
        return None

# Run the configuration
config = configure_trading_system()
if config:
    print(f"Configuration: {config}")
```

## Input Validation / 输入验证

The Interactive Prompt System automatically validates user input:

交互式提示系统自动验证用户输入：

### Text Input Validation / 文本输入验证
- Checks for empty input (unless `allow_empty=True`)
- Trims whitespace
- Provides error messages and retry

### Choice Validation / 选择验证
- Ensures input is a valid number
- Checks if choice is within range
- Handles invalid input gracefully

### Number Validation / 数字验证
- Validates numeric format (int or float)
- Checks min/max constraints
- Provides clear error messages

### Date Validation / 日期验证
- Validates date format
- Provides format examples
- Allows custom date formats

### Confirmation Validation / 确认验证
- Accepts multiple yes/no variations
- Supports Chinese and English
- Case-insensitive

## Error Handling / 错误处理

All input methods include error handling:

所有输入方法都包含错误处理：

1. **Invalid Input / 无效输入**: Clear error message and retry
2. **Out of Range / 超出范围**: Specific constraint violation message
3. **Format Error / 格式错误**: Format example provided
4. **Empty Input / 空输入**: Uses default or prompts again

## Best Practices / 最佳实践

1. **Always provide defaults / 始终提供默认值**: Makes the interface more user-friendly
2. **Use clear prompts / 使用清晰的提示**: Include both Chinese and English
3. **Validate constraints / 验证约束**: Set appropriate min/max values
4. **Provide feedback / 提供反馈**: Use display_message for important information
5. **Show progress / 显示进度**: Use display_progress for long operations

## Requirements Validation / 需求验证

This implementation validates the following requirements:

此实现验证以下需求：

- **Requirement 12.2**: Interactive parameter collection through Q&A
- **Requirement 12.3**: Provides default values and parameter descriptions
- **Requirement 12.5**: Prompts error on invalid input and allows re-entry

## Testing / 测试

Run the unit tests:

运行单元测试：

```bash
pytest tests/unit/test_interactive_prompt.py -v
```

Run the demo:

运行演示：

```bash
python examples/demo_interactive_prompt.py
```

## API Reference / API参考

### InteractivePrompt Class

#### Methods / 方法

- `ask_text(prompt, default=None, allow_empty=False)`: Ask for text input
- `ask_choice(prompt, choices, default=None)`: Ask for choice selection
- `ask_number(prompt, min_val=None, max_val=None, default=None, number_type="float")`: Ask for number input
- `ask_integer(prompt, min_val=None, max_val=None, default=None)`: Ask for integer input
- `ask_date(prompt, default=None, date_format="%Y-%m-%d")`: Ask for date input
- `confirm(prompt, default=True)`: Ask for yes/no confirmation
- `display_message(message, message_type="info")`: Display formatted message
- `display_progress(current, total, message="")`: Display progress bar

## See Also / 另请参阅

- [User Guide](user_guide.md)
- [CLI Documentation](cli_documentation.md)
- [Examples](../examples/)
