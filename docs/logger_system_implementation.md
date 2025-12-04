# LoggerSystem 实现文档

## 概述

LoggerSystem 是量化交易系统的日志管理模块，提供统一的日志记录、日志轮转和日志级别管理功能。

## 功能特性

### 1. 统一日志管理
- 单例模式设计，确保全局唯一的日志系统实例
- 支持多个模块使用独立的日志记录器
- 自动创建日志目录

### 2. 日志轮转
- 基于文件大小的自动日志轮转
- 可配置的备份文件数量
- 支持手动触发日志轮转

### 3. 灵活的日志级别
- 支持 DEBUG、INFO、WARNING、ERROR、CRITICAL 五个级别
- 可动态调整日志级别
- 支持按级别过滤日志

### 4. 完整的日志格式
- 包含时间戳、模块名称、日志级别
- 错误日志自动包含堆栈跟踪信息
- 支持自定义日志格式

### 5. 双输出模式
- 同时输出到控制台和文件
- 控制台和文件可使用不同的日志级别
- UTF-8 编码支持中文日志

## 架构设计

### 类图

```
┌─────────────────────────────────────┐
│         LoggerSystem                │
├─────────────────────────────────────┤
│ - _instance: LoggerSystem           │
│ - _initialized: bool                │
│ - log_dir: Path                     │
│ - log_level: str                    │
│ - log_format: str                   │
│ - max_bytes: int                    │
│ - backup_count: int                 │
│ - _loggers: dict                    │
├─────────────────────────────────────┤
│ + setup(...)                        │
│ + get_logger(name): Logger          │
│ + rotate_logs()                     │
│ + set_level(level)                  │
│ + is_initialized(): bool            │
│ + get_log_files(): list             │
│ + clear_old_logs(keep_count): int   │
└─────────────────────────────────────┘
```

### 设计模式

1. **单例模式**: 确保全局只有一个 LoggerSystem 实例
2. **工厂模式**: 通过 `get_logger()` 创建和管理日志记录器
3. **策略模式**: 支持不同的日志级别和格式策略

## 使用方法

### 基本使用

```python
from infrastructure.logger_system import setup_logging, get_logger

# 1. 初始化日志系统
setup_logging(
    log_dir="./logs",
    log_level="INFO",
    max_bytes=10485760,  # 10MB
    backup_count=5
)

# 2. 获取日志记录器
logger = get_logger("my_module")

# 3. 记录日志
logger.debug("调试信息")
logger.info("普通信息")
logger.warning("警告信息")
logger.error("错误信息")
logger.critical("严重错误")
```

### 错误日志记录

```python
logger = get_logger("error_handler")

try:
    # 可能出错的代码
    result = risky_operation()
except Exception as e:
    # 使用 exception() 自动记录堆栈信息
    logger.exception("操作失败")
    # 或者手动记录错误详情
    logger.error(f"错误详情: {e}")
```

### 动态调整日志级别

```python
from infrastructure.logger_system import LoggerSystem

logger_system = LoggerSystem()

# 调整为 DEBUG 级别查看详细信息
logger_system.set_level("DEBUG")

# 调整为 WARNING 级别减少日志输出
logger_system.set_level("WARNING")
```

### 多模块日志

```python
# 不同模块使用各自的日志记录器
data_logger = get_logger("data_manager")
model_logger = get_logger("model_trainer")
backtest_logger = get_logger("backtest_engine")

data_logger.info("数据加载完成")
model_logger.info("模型训练完成")
backtest_logger.info("回测完成")
```

### 日志文件管理

```python
from infrastructure.logger_system import LoggerSystem

logger_system = LoggerSystem()

# 获取所有日志文件
log_files = logger_system.get_log_files()
for log_file in log_files:
    print(f"{log_file.name}: {log_file.stat().st_size} bytes")

# 清理旧日志文件（保留最新的3个）
deleted_count = logger_system.clear_old_logs(keep_count=3)
print(f"删除了 {deleted_count} 个旧日志文件")

# 手动触发日志轮转
logger_system.rotate_logs()
```

## 配置说明

### 配置文件示例 (config/default_config.yaml)

```yaml
logging:
  log_dir: "./logs"              # 日志文件目录
  log_level: "INFO"              # 日志级别
  log_format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  max_bytes: 10485760            # 单个日志文件最大大小 (10MB)
  backup_count: 5                # 保留的备份文件数量
```

### 配置参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| log_dir | str | "./logs" | 日志文件存储目录 |
| log_level | str | "INFO" | 日志级别 (DEBUG/INFO/WARNING/ERROR/CRITICAL) |
| log_format | str | 见上文 | 日志格式字符串 |
| max_bytes | int | 10485760 | 单个日志文件最大字节数 |
| backup_count | int | 5 | 保留的备份日志文件数量 |

## 日志级别说明

| 级别 | 数值 | 用途 |
|------|------|------|
| DEBUG | 10 | 详细的调试信息，用于开发和问题诊断 |
| INFO | 20 | 一般信息，记录程序正常运行的关键步骤 |
| WARNING | 30 | 警告信息，程序可以继续运行但可能有问题 |
| ERROR | 40 | 错误信息，程序某个功能无法正常执行 |
| CRITICAL | 50 | 严重错误，程序可能无法继续运行 |

## 日志格式说明

默认日志格式：
```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

示例输出：
```
2025-12-04 10:30:45,123 - data_manager - INFO - 数据加载完成
2025-12-04 10:30:46,456 - model_trainer - ERROR - 模型训练失败
```

格式占位符说明：
- `%(asctime)s`: 时间戳
- `%(name)s`: 日志记录器名称（通常是模块名）
- `%(levelname)s`: 日志级别
- `%(message)s`: 日志消息内容

## 日志轮转机制

### 自动轮转

当日志文件大小超过 `max_bytes` 时，系统会自动：
1. 关闭当前日志文件
2. 将当前文件重命名为 `qlib_trading.log.1`
3. 创建新的 `qlib_trading.log` 文件
4. 旧的备份文件依次重命名（.1 → .2, .2 → .3, ...）
5. 超过 `backup_count` 的旧文件会被删除

### 文件命名规则

```
qlib_trading.log        # 当前日志文件
qlib_trading.log.1      # 最近的备份
qlib_trading.log.2      # 次新的备份
qlib_trading.log.3      # 更早的备份
...
```

## 最佳实践

### 1. 模块级日志记录器

在每个模块的开头创建日志记录器：

```python
from infrastructure.logger_system import get_logger

logger = get_logger(__name__)  # 使用模块名作为日志记录器名称

class DataManager:
    def load_data(self):
        logger.info("开始加载数据")
        # ...
        logger.info("数据加载完成")
```

### 2. 结构化日志

使用清晰的日志结构，便于后续分析：

```python
logger.info("=" * 50)
logger.info("开始模型训练")
logger.info("-" * 50)
logger.info(f"模型类型: {model_type}")
logger.info(f"数据集: {dataset_name}")
logger.info(f"训练周期: {start_date} 至 {end_date}")
logger.info("-" * 50)
```

### 3. 异常处理

使用 `logger.exception()` 记录异常，自动包含堆栈信息：

```python
try:
    result = process_data()
except Exception as e:
    logger.exception("数据处理失败")
    raise
```

### 4. 性能敏感代码

在性能敏感的循环中，使用条件判断避免不必要的字符串格式化：

```python
if logger.isEnabledFor(logging.DEBUG):
    logger.debug(f"处理第 {i} 条数据: {expensive_operation()}")
```

### 5. 日志级别选择

- **DEBUG**: 详细的变量值、中间结果
- **INFO**: 关键步骤、状态变化
- **WARNING**: 可恢复的异常、降级操作
- **ERROR**: 功能失败、需要关注的错误
- **CRITICAL**: 系统级错误、无法继续运行

## 测试

运行单元测试：

```bash
pytest tests/unit/test_logger_system.py -v
```

运行演示程序：

```bash
python examples/demo_logger_system.py
```

## 性能考虑

1. **单例模式**: 避免重复初始化，提高性能
2. **日志记录器缓存**: 避免重复创建日志记录器
3. **异步日志**: 未来可考虑使用 QueueHandler 实现异步日志
4. **日志压缩**: 未来可考虑压缩旧日志文件节省空间

## 故障排查

### 问题：日志文件未创建

**原因**: 日志目录权限不足或路径不存在

**解决**: 
```python
# 确保日志目录存在且有写权限
import os
log_dir = "./logs"
os.makedirs(log_dir, exist_ok=True)
```

### 问题：日志级别不生效

**原因**: 日志系统未正确初始化

**解决**:
```python
# 确保在使用前调用 setup
setup_logging(log_dir="./logs", log_level="DEBUG")
```

### 问题：日志文件过大

**原因**: max_bytes 设置过大或日志过于频繁

**解决**:
```python
# 减小单个文件大小，增加备份数量
setup_logging(
    log_dir="./logs",
    max_bytes=5242880,  # 5MB
    backup_count=10
)
```

## 未来改进

1. **异步日志**: 使用 QueueHandler 实现异步日志写入
2. **日志压缩**: 自动压缩旧日志文件
3. **远程日志**: 支持发送日志到远程服务器
4. **日志分析**: 提供日志分析和统计工具
5. **结构化日志**: 支持 JSON 格式的结构化日志

## 相关文档

- [Python logging 官方文档](https://docs.python.org/3/library/logging.html)
- [RotatingFileHandler 文档](https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler)
- [日志最佳实践](https://docs.python-guide.org/writing/logging/)

## 版本历史

- v1.0.0 (2025-12-04): 初始实现
  - 基本日志记录功能
  - 日志轮转支持
  - 多级别日志
  - 单例模式设计
