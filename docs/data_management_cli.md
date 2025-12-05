# 数据管理CLI使用指南 / Data Management CLI User Guide

## 概述 / Overview

数据管理CLI提供了一套完整的工具来管理量化交易系统所需的市场数据。通过友好的中文界面，用户可以轻松完成数据下载、验证、查看和检查等操作。

The Data Management CLI provides a complete set of tools to manage market data required by the quantitative trading system. Through a user-friendly Chinese interface, users can easily complete data download, validation, viewing, and checking operations.

## 功能特性 / Features

### 1. 下载市场数据 / Download Market Data

支持从qlib数据源下载市场数据，包括：

Supports downloading market data from qlib data sources, including:

- **多市场支持 / Multi-market Support**
  - 中国市场 (cn) / China Market
  - 美国市场 (us) / US Market
  - 其他市场 / Other Markets

- **多种数据间隔 / Multiple Data Intervals**
  - 日线数据 (1d) / Daily Data
  - 分钟数据 (1min) / Minute Data

- **灵活的时间范围 / Flexible Time Range**
  - 可指定开始和结束日期 / Can specify start and end dates
  - 支持下载全部历史数据 / Supports downloading all historical data

### 2. 验证数据完整性 / Validate Data Integrity

全面检查数据质量，包括：

Comprehensive data quality checks, including:

- 数据存在性检查 / Data existence check
- 数据格式验证 / Data format validation
- 缺失值检测 / Missing value detection
- 数据完整性分析 / Data integrity analysis
- 详细的验证报告 / Detailed validation report

### 3. 查看数据信息 / View Data Information

显示数据的详细信息：

Display detailed data information:

- 数据提供者 / Data Provider
- 市场区域 / Market Region
- 数据时间范围 / Data Time Range
- 交易日数量 / Number of Trading Days
- 股票数量 / Number of Instruments
- 最后更新时间 / Last Update Time

### 4. 检查数据覆盖 / Check Data Coverage

验证数据是否满足特定需求：

Verify if data meets specific requirements:

- 检查指定时间范围的数据覆盖 / Check data coverage for specified time range
- 验证数据是否满足训练需求 / Verify if data meets training requirements
- 验证数据是否满足回测需求 / Verify if data meets backtesting requirements
- 提供数据缺口分析 / Provide data gap analysis

## 使用方法 / Usage

### 方法1：通过主CLI访问 / Method 1: Access via Main CLI

1. 启动主程序 / Start main program:
   ```bash
   python main.py
   ```

2. 在主菜单中选择选项 4 / Select option 4 in main menu:
   ```
   4. 数据管理 / Data Management
   ```

3. 选择所需的数据管理操作 / Select desired data management operation:
   - 下载市场数据 / Download market data
   - 验证数据完整性 / Validate data integrity
   - 查看数据信息 / View data information
   - 检查数据覆盖 / Check data coverage

### 方法2：直接使用DataManager类 / Method 2: Use DataManager Class Directly

```python
from src.core.data_manager import DataManager

# 创建数据管理器 / Create data manager
data_manager = DataManager()

# 初始化 / Initialize
data_manager.initialize(
    data_path='~/.qlib/qlib_data/cn_data',
    region='cn'
)

# 验证数据 / Validate data
result = data_manager.validate_data(
    start_date='2020-01-01',
    end_date='2023-12-31',
    instruments='csi300'
)

if result.is_valid:
    print("数据验证通过 / Data validation passed")
else:
    print(f"数据验证失败 / Data validation failed: {result.message}")

# 查看数据信息 / View data info
info = data_manager.get_data_info()
print(f"数据范围 / Data range: {info.data_start} 至 / to {info.data_end}")
print(f"交易日数 / Trading days: {info.trading_days}")
```

## 详细操作指南 / Detailed Operation Guide

### 下载市场数据 / Download Market Data

#### 步骤 / Steps:

1. **选择市场区域 / Select Market Region**
   - cn (中国市场) / China Market
   - us (美国市场) / US Market

2. **配置目标目录 / Configure Target Directory**
   - 默认：`~/.qlib/qlib_data/cn_data`
   - 可自定义路径 / Can customize path

3. **选择数据间隔 / Select Data Interval**
   - 1d (日线数据) / Daily data
   - 1min (分钟数据) / Minute data

4. **指定时间范围（可选）/ Specify Time Range (Optional)**
   - 开始日期 / Start date
   - 结束日期 / End date

5. **执行下载 / Execute Download**
   - 系统会显示下载命令 / System will display download command
   - 在新终端中执行命令 / Execute command in new terminal

#### 示例命令 / Example Command:

```bash
# 中国市场日线数据 / China market daily data
python -m qlib.run.get_data qlib_data \
    --target_dir ~/.qlib/qlib_data/cn_data \
    --region cn \
    --interval 1d

# 美国市场日线数据 / US market daily data
python -m qlib.run.get_data qlib_data \
    --target_dir ~/.qlib/qlib_data/us_data \
    --region us \
    --interval 1d
```

### 验证数据完整性 / Validate Data Integrity

#### 步骤 / Steps:

1. **初始化数据管理器 / Initialize Data Manager**
   - 选择市场区域 / Select market region
   - 输入数据路径 / Enter data path

2. **配置验证参数 / Configure Validation Parameters**
   - 指定时间范围（可选）/ Specify time range (optional)
   - 选择股票池 / Select stock pool

3. **执行验证 / Execute Validation**
   - 系统自动检查数据 / System automatically checks data
   - 生成验证报告 / Generate validation report

4. **查看验证结果 / View Validation Results**
   - 验证状态 / Validation status
   - 数据时间范围 / Data time range
   - 发现的问题 / Issues found
   - 改进建议 / Improvement suggestions

### 查看数据信息 / View Data Information

#### 显示内容 / Display Content:

- **数据提供者 / Data Provider**
  - 数据源路径 / Data source path

- **市场区域 / Market Region**
  - cn, us, 等 / cn, us, etc.

- **数据时间范围 / Data Time Range**
  - 开始日期 / Start date
  - 结束日期 / End date
  - 交易日数量 / Number of trading days

- **股票数量 / Number of Instruments**
  - 可用股票总数 / Total available stocks

- **最后更新 / Last Updated**
  - 数据最后更新时间 / Data last update time

### 检查数据覆盖 / Check Data Coverage

#### 步骤 / Steps:

1. **输入需要检查的时间范围 / Enter Time Range to Check**
   - 开始日期 / Start date
   - 结束日期 / End date

2. **选择股票池 / Select Stock Pool**
   - csi300 (沪深300)
   - csi500 (中证500)
   - csi800 (中证800)
   - all (全部股票) / All stocks
   - 自定义 / Custom

3. **执行检查 / Execute Check**
   - 系统比较数据范围 / System compares data range
   - 生成覆盖报告 / Generate coverage report

4. **查看检查结果 / View Check Results**
   - 覆盖状态 / Coverage status
   - 数据范围对比 / Data range comparison
   - 改进建议 / Improvement suggestions

## 常见问题 / FAQ

### Q1: 数据下载失败怎么办？ / What if data download fails?

**A:** 可能的原因和解决方案 / Possible reasons and solutions:

1. **网络连接问题 / Network connection issue**
   - 检查网络连接 / Check network connection
   - 使用VPN（如果需要）/ Use VPN (if needed)

2. **磁盘空间不足 / Insufficient disk space**
   - 检查磁盘空间 / Check disk space
   - 清理不必要的文件 / Clean up unnecessary files

3. **权限问题 / Permission issue**
   - 检查目录权限 / Check directory permissions
   - 使用sudo（如果需要）/ Use sudo (if needed)

### Q2: 数据验证失败怎么办？ / What if data validation fails?

**A:** 根据验证报告采取行动 / Take action based on validation report:

1. **数据缺失 / Data missing**
   - 重新下载数据 / Re-download data
   - 检查下载命令是否正确 / Check if download command is correct

2. **数据损坏 / Data corrupted**
   - 删除损坏的数据 / Delete corrupted data
   - 重新下载 / Re-download

3. **数据格式错误 / Data format error**
   - 确认qlib版本 / Confirm qlib version
   - 更新qlib到最新版本 / Update qlib to latest version

### Q3: 如何更新数据？ / How to update data?

**A:** 定期更新数据的步骤 / Steps to update data regularly:

1. 运行数据下载命令 / Run data download command
2. 验证新数据 / Validate new data
3. 检查数据覆盖 / Check data coverage
4. 确认数据可用 / Confirm data availability

建议每周更新一次数据 / Recommend updating data weekly

### Q4: 支持哪些股票池？ / What stock pools are supported?

**A:** 常用股票池 / Common stock pools:

- **csi300**: 沪深300指数成分股 / CSI 300 Index constituents
- **csi500**: 中证500指数成分股 / CSI 500 Index constituents
- **csi800**: 中证800指数成分股 / CSI 800 Index constituents
- **all**: 全部可用股票 / All available stocks
- **自定义**: 可以指定任何qlib支持的股票池 / Can specify any qlib-supported stock pool

## 最佳实践 / Best Practices

### 1. 数据管理流程 / Data Management Workflow

```
下载数据 → 验证数据 → 查看信息 → 检查覆盖 → 开始训练
Download → Validate → View Info → Check Coverage → Start Training
```

### 2. 定期维护 / Regular Maintenance

- **每周更新数据 / Update data weekly**
  - 保持数据最新 / Keep data up-to-date
  - 确保训练使用最新数据 / Ensure training uses latest data

- **训练前验证 / Validate before training**
  - 确保数据完整性 / Ensure data integrity
  - 避免训练失败 / Avoid training failures

- **定期检查覆盖 / Check coverage regularly**
  - 确保数据满足需求 / Ensure data meets requirements
  - 及时发现数据缺口 / Timely discover data gaps

### 3. 存储管理 / Storage Management

- **预留足够空间 / Reserve sufficient space**
  - 日线数据：1-2 GB / Daily data: 1-2 GB
  - 分钟数据：10-20 GB / Minute data: 10-20 GB

- **定期清理 / Regular cleanup**
  - 删除过期数据 / Delete outdated data
  - 压缩历史数据 / Compress historical data

## 技术细节 / Technical Details

### 数据存储结构 / Data Storage Structure

```
~/.qlib/qlib_data/
├── cn_data/              # 中国市场数据 / China market data
│   ├── calendars/        # 交易日历 / Trading calendars
│   ├── instruments/      # 股票列表 / Stock lists
│   └── features/         # 特征数据 / Feature data
└── us_data/              # 美国市场数据 / US market data
    ├── calendars/
    ├── instruments/
    └── features/
```

### 数据格式 / Data Format

qlib使用二进制格式存储数据，具有以下优势：

qlib uses binary format to store data with the following advantages:

- **高效读取 / Efficient reading**
- **压缩存储 / Compressed storage**
- **快速查询 / Fast querying**

### API参考 / API Reference

#### DataManager类 / DataManager Class

```python
class DataManager:
    def initialize(self, data_path: str, region: str) -> None
    def download_data(self, region: str, target_dir: str, interval: str) -> None
    def validate_data(self, start_date: str, end_date: str, instruments: str) -> ValidationResult
    def get_data_info(self) -> DataInfo
    def check_data_coverage(self, required_start: str, required_end: str, instruments: str) -> Tuple[bool, str]
    def is_initialized(self) -> bool
```

## 相关资源 / Related Resources

### 文档 / Documentation

- [Qlib官方文档 / Qlib Official Documentation](https://qlib.readthedocs.io/)
- [数据管理器源码 / Data Manager Source Code](../src/core/data_manager.py)
- [CLI源码 / CLI Source Code](../src/cli/main_cli.py)

### 示例 / Examples

- [数据管理演示 / Data Management Demo](../demo_data_management.py)
- [数据管理测试 / Data Management Test](../test_data_management_cli.py)

### 支持 / Support

如有问题，请：

If you have questions, please:

1. 查看本文档 / Check this documentation
2. 查看Qlib官方文档 / Check Qlib official documentation
3. 提交Issue / Submit an issue

## 更新日志 / Changelog

### v1.0.0 (2024-01-XX)

- ✅ 实现数据下载功能 / Implemented data download functionality
- ✅ 实现数据验证功能 / Implemented data validation functionality
- ✅ 实现数据信息查看 / Implemented data information viewing
- ✅ 实现数据覆盖检查 / Implemented data coverage checking
- ✅ 集成到主CLI / Integrated into main CLI
- ✅ 添加中英双语支持 / Added bilingual support

---

**验证需求 / Validates Requirements**: 9.1, 9.2
