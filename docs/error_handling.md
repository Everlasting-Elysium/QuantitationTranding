# 错误处理系统文档 / Error Handling System Documentation

## 概述 / Overview

本系统提供了统一的错误处理机制，包括：
- 自定义异常类
- 中英双语错误消息
- 错误分类和严重程度
- 错误恢复策略
- 详细的错误日志记录

This system provides a unified error handling mechanism, including:
- Custom exception classes
- Bilingual error messages (Chinese and English)
- Error categorization and severity levels
- Error recovery strategies
- Detailed error logging

## 错误类别 / Error Categories

系统定义了以下错误类别：

| 类别 / Category | 代码前缀 / Code Prefix | 说明 / Description |
|----------------|----------------------|-------------------|
| 配置错误 / Configuration | CFG | 配置文件相关错误 / Configuration file related errors |
| 数据错误 / Data | DAT | 数据访问和处理错误 / Data access and processing errors |
| 训练错误 / Training | TRN | 模型训练相关错误 / Model training related errors |
| 回测错误 / Backtest | BCK | 回测执行错误 / Backtest execution errors |
| 系统错误 / System | SYS | 系统级错误 / System-level errors |
| 网络错误 / Network | NET | 网络连接错误 / Network connection errors |
| 权限错误 / Permission | PRM | 文件权限错误 / File permission errors |
| 验证错误 / Validation | VAL | 输入验证错误 / Input validation errors |

## 错误严重程度 / Error Severity

| 级别 / Level | 说明 / Description |
|-------------|-------------------|
| LOW | 低 - 可以继续运行 / Low - Can continue running |
| MEDIUM | 中 - 部分功能受影响 / Medium - Some features affected |
| HIGH | 高 - 主要功能受影响 / High - Major features affected |
| CRITICAL | 严重 - 系统无法继续运行 / Critical - System cannot continue |

## 使用方法 / Usage

### 1. 基本错误处理 / Basic Error Handling

```python
from src.core.error_handler import (
    ConfigurationError,
    ErrorInfo,
    ErrorCategory,
    ErrorSeverity
)

# 创建错误信息
error_info = ErrorInfo(
    error_code="CFG0001",
    error_message_zh="配置文件不存在",
    error_message_en="Configuration file not found",
    category=ErrorCategory.CONFIGURATION,
    severity=ErrorSeverity.HIGH,
    technical_details="File path: /path/to/config.yaml",
    suggested_actions=[
        "检查配置文件路径是否正确",
        "使用默认配置创建新文件"
    ],
    recoverable=True
)

# 抛出异常
raise ConfigurationError(error_info)
```

### 2. 使用错误处理器 / Using Error Handler

```python
from src.core.error_handler import get_error_handler

error_handler = get_error_handler()

try:
    # 你的代码
    pass
except Exception as e:
    # 处理错误（会自动记录日志）
    error_info = error_handler.handle_error(
        error=e,
        context={"operation": "load_config", "file": "config.yaml"},
        raise_exception=True  # 是否重新抛出异常
    )
```

### 3. 使用装饰器 / Using Decorator

```python
from src.core.error_handler import error_handler_decorator

@error_handler_decorator()
def my_function(param1, param2):
    """
    这个函数会自动处理异常
    This function will automatically handle exceptions
    """
    # 你的代码
    pass
```

### 4. 注册错误恢复策略 / Register Error Recovery Strategy

```python
from src.core.error_handler import get_error_handler, ErrorCategory

def recovery_strategy(error_info, context):
    """
    自定义恢复策略
    Custom recovery strategy
    """
    # 实现恢复逻辑
    pass

error_handler = get_error_handler()
error_handler.register_recovery_strategy(
    category=ErrorCategory.NETWORK,
    error_code="NET0001",
    strategy=recovery_strategy
)
```

### 5. 获取用户友好的错误消息 / Get User-Friendly Error Message

```python
# 中文消息
message_zh = error_info.get_user_message(language="zh")
print(message_zh)

# 英文消息
message_en = error_info.get_user_message(language="en")
print(message_en)
```

## 错误代码列表 / Error Code List

### 配置错误 / Configuration Errors (CFG)

| 错误代码 / Error Code | 说明 / Description |
|---------------------|-------------------|
| CFG0001 | 配置文件不存在 / Configuration file not found |
| CFG0002 | 配置文件格式错误 / Configuration file format error |
| CFG0003 | 配置验证失败 / Configuration validation failed |

### 数据错误 / Data Errors (DAT)

| 错误代码 / Error Code | 说明 / Description |
|---------------------|-------------------|
| DAT0001 | 数据管理器初始化失败 / Data manager initialization failed |
| DAT0002 | qlib未正确安装 / qlib not properly installed |
| DAT0003 | 数据下载失败 / Data download failed |
| DAT0004 | 不支持的缺失值处理策略 / Unsupported missing value strategy |
| DAT0005 | 缺失值处理失败 / Missing value handling failed |
| DAT0006 | 数据管理器未初始化 / Data manager not initialized |
| DAT0007 | 获取数据信息失败 / Failed to get data information |
| DAT0008 | 数据路径不存在 / Data path does not exist |

### 系统错误 / System Errors (SYS)

| 错误代码 / Error Code | 说明 / Description |
|---------------------|-------------------|
| SYS0001 | qlib未安装 / qlib not installed |
| SYS0002 | qlib初始化失败 / qlib initialization failed |

## 最佳实践 / Best Practices

### 1. 始终提供上下文信息 / Always Provide Context

```python
try:
    load_config(config_path)
except Exception as e:
    error_handler.handle_error(
        error=e,
        context={
            "operation": "load_config",
            "config_path": config_path,
            "user": current_user
        }
    )
```

### 2. 使用适当的错误类别 / Use Appropriate Error Categories

根据错误的性质选择正确的错误类别，这有助于：
- 更好的错误分类和统计
- 更准确的错误恢复策略
- 更清晰的错误日志

Choose the correct error category based on the nature of the error, which helps with:
- Better error classification and statistics
- More accurate error recovery strategies
- Clearer error logs

### 3. 提供有用的建议 / Provide Useful Suggestions

在创建错误信息时，提供具体的、可操作的建议：

When creating error information, provide specific, actionable suggestions:

```python
suggested_actions=[
    "检查配置文件路径: /path/to/config.yaml",
    "运行命令生成默认配置: python init_config.py",
    "参考文档: https://docs.example.com/config"
]
```

### 4. 记录详细的技术信息 / Log Detailed Technical Information

技术细节应该包含足够的信息用于调试：

Technical details should contain enough information for debugging:

```python
technical_details=f"Failed to parse YAML: {str(e)}, Line: {line_number}, Column: {column}"
```

### 5. 合理设置可恢复标志 / Set Recoverable Flag Appropriately

只有当错误确实可以通过自动或手动操作恢复时，才设置 `recoverable=True`：

Only set `recoverable=True` when the error can truly be recovered through automatic or manual operations:

- 网络错误（可以重试）/ Network errors (can retry)
- 验证错误（用户可以重新输入）/ Validation errors (user can re-enter)
- 临时文件锁定（可以等待）/ Temporary file locks (can wait)

不可恢复的错误：

Non-recoverable errors:

- 系统依赖缺失 / Missing system dependencies
- 严重的数据损坏 / Severe data corruption
- 不兼容的版本 / Incompatible versions

## 错误日志 / Error Logging

所有错误都会自动记录到日志文件中，包括：
- 错误代码和消息
- 错误类别和严重程度
- 技术细节
- 堆栈跟踪（对于高严重程度错误）
- 上下文信息

All errors are automatically logged to log files, including:
- Error code and message
- Error category and severity
- Technical details
- Stack trace (for high severity errors)
- Context information

日志文件位置：`./logs/qlib_trading.log`

Log file location: `./logs/qlib_trading.log`

## 错误历史 / Error History

系统维护最近100个错误的历史记录：

The system maintains a history of the last 100 errors:

```python
from src.core.error_handler import get_error_handler

error_handler = get_error_handler()

# 获取所有错误历史
all_errors = error_handler.get_error_history()

# 获取最近10个错误
recent_errors = error_handler.get_error_history(limit=10)

# 清空错误历史
error_handler.clear_error_history()
```

## 示例 / Examples

### 完整示例：配置加载 / Complete Example: Configuration Loading

```python
from pathlib import Path
from src.core.error_handler import (
    ConfigurationError,
    ErrorInfo,
    ErrorCategory,
    ErrorSeverity,
    get_error_handler
)

def load_configuration(config_path: str):
    """
    加载配置文件
    Load configuration file
    """
    error_handler = get_error_handler()
    
    try:
        path = Path(config_path)
        
        if not path.exists():
            error_info = ErrorInfo(
                error_code="CFG0001",
                error_message_zh=f"配置文件不存在: {config_path}",
                error_message_en=f"Configuration file not found: {config_path}",
                category=ErrorCategory.CONFIGURATION,
                severity=ErrorSeverity.HIGH,
                technical_details=f"Attempted path: {path.absolute()}",
                suggested_actions=[
                    f"检查路径是否正确: {config_path}",
                    "使用默认配置: config_manager.get_default_config()",
                    "创建新配置文件"
                ],
                documentation_link="https://docs.example.com/configuration",
                recoverable=True
            )
            raise ConfigurationError(error_info)
        
        # 加载配置...
        
    except ConfigurationError:
        # 重新抛出配置错误
        raise
    except Exception as e:
        # 处理其他未预期的错误
        error_handler.handle_error(
            error=e,
            context={"config_path": config_path},
            raise_exception=True
        )
```

## 故障排除 / Troubleshooting

### 问题：错误消息没有记录到日志 / Issue: Error messages not logged

**解决方案 / Solution:**
1. 确认日志系统已初始化 / Confirm logging system is initialized
2. 检查日志级别设置 / Check log level settings
3. 验证日志文件权限 / Verify log file permissions

### 问题：错误恢复策略未执行 / Issue: Error recovery strategy not executed

**解决方案 / Solution:**
1. 确认错误标记为可恢复 / Confirm error is marked as recoverable
2. 检查恢复策略是否正确注册 / Check if recovery strategy is properly registered
3. 验证错误代码匹配 / Verify error code matches

## 参考 / References

- [Python异常处理最佳实践](https://docs.python.org/3/tutorial/errors.html)
- [日志系统文档](./logger_system_implementation.md)
- [配置管理文档](./config_manager_implementation.md)
