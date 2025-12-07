# Market Selector Documentation
# 市场选择器文档

## Overview / 概述

The MarketSelector is a component that manages market and asset type selection for the qlib trading system. It provides functionality to:

MarketSelector是一个管理qlib交易系统的市场和资产类型选择的组件。它提供以下功能：

- Load market configurations from YAML files / 从YAML文件加载市场配置
- Get available markets and asset types / 获取可用的市场和资产类型
- Create market configurations / 创建市场配置
- Validate market selections / 验证市场选择

## Supported Markets / 支持的市场

The system currently supports the following markets:

系统目前支持以下市场：

### Chinese Market (CN) / 中国市场
- **Region**: cn
- **Timezone**: Asia/Shanghai
- **Asset Types**: 
  - Stock (股票): A-shares including main board, ChiNext, STAR Market
  - Fund (基金): Public funds including equity, mixed, bond funds
  - ETF: Exchange-traded funds

### US Market (US) / 美国市场
- **Region**: us
- **Timezone**: America/New_York
- **Asset Types**:
  - Stock (股票): NYSE and NASDAQ listed companies
  - ETF: Exchange-traded funds

### Hong Kong Market (HK) / 香港市场
- **Region**: hk
- **Timezone**: Asia/Hong_Kong
- **Asset Types**:
  - Stock (股票): Main board and GEM

## Usage / 使用方法

### Basic Usage / 基本使用

```python
from src.application.market_selector import MarketSelector

# Initialize the selector
# 初始化选择器
selector = MarketSelector()

# Get available markets
# 获取可用市场
markets = selector.get_available_markets()
for market in markets:
    print(f"{market.code}: {market.name}")

# Get asset types for a specific market
# 获取特定市场的资产类型
asset_types = selector.get_asset_types("CN")
for asset_type in asset_types:
    print(f"{asset_type.code}: {asset_type.name}")

# Create a market configuration
# 创建市场配置
config = selector.select_market_and_type("CN", "stock")
print(f"Market: {config.market.name}")
print(f"Asset Type: {config.asset_type.name}")
print(f"Instruments Pool: {config.instruments_pool}")
```

### Getting Market Information / 获取市场信息

```python
# Get detailed market information
# 获取详细的市场信息
market_info = selector.get_market_info("CN")
print(f"Market: {market_info.market.name}")
print(f"Region: {market_info.market.region}")
print(f"Timezone: {market_info.market.timezone}")
print(f"Data Available: {market_info.data_available}")
print(f"Description: {market_info.description}")
```

### Getting Instruments Pools / 获取工具池

```python
# Get available instruments pools for a market and asset type
# 获取市场和资产类型的可用工具池
pools = selector.get_instruments_pools("CN", "stock")
for pool in pools:
    print(f"{pool['name']}: {pool['description']}")
```

### Using Default Configuration / 使用默认配置

```python
# Get default market configuration
# 获取默认市场配置
default_config = selector.get_default_config()
print(f"Default: {default_config.market.code}/{default_config.asset_type.code}")
```

### Custom Configuration File / 自定义配置文件

```python
# Use a custom configuration file
# 使用自定义配置文件
selector = MarketSelector(config_path="/path/to/custom/markets.yaml")
```

## Configuration File Format / 配置文件格式

The market configuration is stored in `config/markets.yaml`. Here's the structure:

市场配置存储在`config/markets.yaml`中。结构如下：

```yaml
markets:
  CN:
    code: "CN"
    name: "中国市场"
    region: "cn"
    timezone: "Asia/Shanghai"
    trading_hours:
      morning_start: "09:30"
      morning_end: "11:30"
      afternoon_start: "13:00"
      afternoon_end: "15:00"
    description: "中国A股市场，包括上海证券交易所和深圳证券交易所"
    
    asset_types:
      stock:
        code: "stock"
        name: "股票"
        description: "A股股票，包括主板、创业板、科创板等"
        instruments_pools:
          - name: "csi300"
            description: "沪深300指数成分股"
          - name: "csi500"
            description: "中证500指数成分股"
        data_source: "qlib_cn"

default_market: "CN"
default_asset_type: "stock"
```

## Data Models / 数据模型

### Market

```python
@dataclass
class Market:
    code: str              # Market code (e.g., "CN", "US")
    name: str              # Market name (e.g., "中国市场")
    region: str            # Region identifier for qlib
    timezone: str          # Market timezone
    trading_hours: Dict    # Trading hours configuration
```

### AssetType

```python
@dataclass
class AssetType:
    code: str              # Asset type code (e.g., "stock", "fund")
    name: str              # Asset type name (e.g., "股票")
    description: str       # Detailed description
```

### MarketConfig

```python
@dataclass
class MarketConfig:
    market: Market         # Market information
    asset_type: AssetType  # Asset type information
    data_source: str       # Data source identifier
    instruments_pool: str  # Instrument pool identifier
```

### MarketInfo

```python
@dataclass
class MarketInfo:
    market: Market                      # Market instance
    available_asset_types: List[AssetType]  # Available asset types
    data_available: bool                # Whether data is available
    data_start_date: Optional[str]      # Start date of available data
    data_end_date: Optional[str]        # End date of available data
    description: str                    # Additional description
```

## Error Handling / 错误处理

The MarketSelector provides clear error messages in both English and Chinese:

MarketSelector提供中英文双语的清晰错误消息：

```python
try:
    config = selector.select_market_and_type("INVALID", "stock")
except ValueError as e:
    print(e)  # "Invalid market code: INVALID / 无效的市场代码: INVALID"
```

Common errors include:
常见错误包括：

- Invalid market code / 无效的市场代码
- Invalid asset type / 无效的资产类型
- Configuration file not found / 配置文件未找到
- Invalid configuration format / 无效的配置格式

## Integration with Other Components / 与其他组件的集成

The MarketSelector is designed to work seamlessly with other components:

MarketSelector设计为与其他组件无缝协作：

### With DataManager / 与DataManager集成

```python
from src.application.market_selector import MarketSelector
from src.core.data_manager import DataManager

selector = MarketSelector()
config = selector.select_market_and_type("CN", "stock")

# Use the config with DataManager
data_manager = DataManager()
data_manager.initialize(
    data_path="data/cn_data",
    region=config.market.region
)
```

### With TrainingManager / 与TrainingManager集成

```python
from src.application.market_selector import MarketSelector
from src.application.training_manager import TrainingManager

selector = MarketSelector()
config = selector.select_market_and_type("CN", "stock")

# Use the instruments pool in training configuration
training_config = {
    "instruments": config.instruments_pool,
    "market": config.market.code,
    # ... other training parameters
}
```

## Examples / 示例

See `examples/demo_market_selector.py` for a complete working example.

查看`examples/demo_market_selector.py`获取完整的工作示例。

## Testing / 测试

Unit tests are available in `tests/unit/test_market_selector.py`:

单元测试位于`tests/unit/test_market_selector.py`：

```bash
# Run tests
pytest tests/unit/test_market_selector.py -v

# Run with coverage
pytest tests/unit/test_market_selector.py --cov=src.application.market_selector
```

## Future Enhancements / 未来增强

Planned enhancements include:
计划的增强功能包括：

1. Dynamic data availability checking / 动态数据可用性检查
2. Support for more markets (Japan, Europe, etc.) / 支持更多市场（日本、欧洲等）
3. Real-time market status monitoring / 实时市场状态监控
4. Market-specific trading rules / 市场特定的交易规则
5. Integration with external data providers / 与外部数据提供商集成

## References / 参考

- Requirements: 16.1, 16.2, 16.3
- Design Document: Market Selection and Analysis section
- Related Components: DataManager, TrainingManager, PerformanceAnalyzer
