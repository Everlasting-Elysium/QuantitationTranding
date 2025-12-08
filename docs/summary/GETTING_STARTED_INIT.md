# 一键初始化指南 / One-Click Initialization Guide

本文档详细说明如何使用一键初始化功能快速设置量化交易系统。

This document explains how to use the one-click initialization feature to quickly set up the quantitative trading system.

## 📋 目录 / Table of Contents

- [系统要求](#系统要求--system-requirements)
- [快速开始](#快速开始--quick-start)
- [初始化步骤详解](#初始化步骤详解--initialization-steps)
- [常见问题](#常见问题--faq)
- [手动初始化](#手动初始化--manual-initialization)
- [验证安装](#验证安装--verify-installation)

## 系统要求 / System Requirements

### 最低要求 / Minimum Requirements

- **操作系统 / OS**: Linux, macOS, Windows 10+
- **Python**: 3.8 或更高版本 / 3.8 or higher
- **内存 / RAM**: 8GB (推荐16GB / Recommended 16GB)
- **磁盘空间 / Disk Space**: 5GB (用于数据和模型 / for data and models)
- **网络 / Network**: 稳定的互联网连接（用于下载数据 / for downloading data）

### 推荐配置 / Recommended Configuration

- **CPU**: 4核心或更多 / 4 cores or more
- **内存 / RAM**: 16GB+
- **磁盘 / Disk**: SSD（固态硬盘 / Solid State Drive）
- **网络 / Network**: 10Mbps+ 下载速度 / download speed

## 快速开始 / Quick Start

### 方法1: 使用Shell脚本（Linux/Mac）

```bash
# 1. 进入项目目录 / Navigate to project directory
cd Code/QuantitationTranding

# 2. 添加执行权限 / Add execute permission
chmod +x quick_start.sh

# 3. 运行脚本 / Run script
./quick_start.sh
```

### 方法2: 使用批处理脚本（Windows）

```cmd
# 1. 进入项目目录 / Navigate to project directory
cd Code\QuantitationTranding

# 2. 运行脚本 / Run script
quick_start.bat
```

### 方法3: 使用Python脚本（所有平台）

```bash
# 适用于所有操作系统 / Works on all operating systems
python init_system.py
```

## 初始化步骤详解 / Initialization Steps

初始化脚本会按顺序执行以下步骤：

The initialization script executes the following steps in order:

### 步骤 1/5: 检查Python版本 / Check Python Version

```
✓ Python版本: 3.9.7 ✓
```

**作用 / Purpose**: 确保Python版本满足最低要求（3.8+）

**可能的问题 / Possible Issues**:
- ❌ Python版本过低 → 请升级Python
- ❌ 未找到Python → 请安装Python

### 步骤 2/5: 检查依赖包 / Check Dependencies

```
[████████████████████] 100% - 检查 pytest
✓ 已安装 12/12 个依赖包 / 12/12 dependencies installed
```

**作用 / Purpose**: 检查所有必需的Python包是否已安装

**依赖包列表 / Dependencies List**:
- qlib - 量化投资框架 / Quantitative investment framework
- numpy - 数值计算 / Numerical computing
- pandas - 数据处理 / Data processing
- scikit-learn - 机器学习 / Machine learning
- lightgbm - 梯度提升模型 / Gradient boosting
- torch - 深度学习 / Deep learning
- mlflow - 实验追踪 / Experiment tracking
- matplotlib - 可视化 / Visualization
- seaborn - 统计可视化 / Statistical visualization
- click - CLI框架 / CLI framework
- rich - 终端美化 / Terminal formatting
- pyyaml - 配置文件 / Configuration files
- pytest - 测试框架 / Testing framework

**如果有缺失的包 / If packages are missing**:
```
⚠ 缺失 3 个依赖包 / 3 dependencies missing:
  - qlib
  - lightgbm
  - mlflow

是否自动安装缺失的依赖包？(y/n) / Install missing packages automatically? (y/n):
```

选择 `y` 将自动安装所有缺失的包。

### 步骤 3/5: 创建必要目录 / Create Directories

```
✓ 创建目录 / Created: data/cn_data
✓ 创建目录 / Created: logs
✓ 创建目录 / Created: outputs/backtests
✓ 创建目录 / Created: outputs/reports
✓ 创建目录 / Created: outputs/signals
✓ 创建目录 / Created: model_registry
✓ 创建目录 / Created: examples/mlruns
```

**作用 / Purpose**: 创建系统运行所需的目录结构

**目录说明 / Directory Descriptions**:
- `data/cn_data` - 中国A股数据存储 / China A-share data storage
- `logs` - 系统日志文件 / System log files
- `outputs/backtests` - 回测结果 / Backtest results
- `outputs/reports` - 生成的报告 / Generated reports
- `outputs/signals` - 交易信号 / Trading signals
- `model_registry` - 模型注册表 / Model registry
- `examples/mlruns` - MLflow实验数据 / MLflow experiment data

### 步骤 4/5: 下载示例数据 / Download Sample Data

```
ℹ 正在下载中国A股示例数据，这可能需要几分钟... 
  Downloading China A-share sample data, this may take a few minutes...

✓ 示例数据下载成功 / Sample data downloaded successfully
ℹ 数据位置 / Data location: /home/user/.qlib/qlib_data/cn_data
```

**作用 / Purpose**: 下载qlib提供的中国A股历史数据

**数据内容 / Data Content**:
- 时间范围 / Time Range: 2008-01-01 至今 / to present
- 股票池 / Stock Pool: 沪深300、中证500等 / CSI300, CSI500, etc.
- 数据频率 / Frequency: 日线数据 / Daily data
- 数据大小 / Size: 约2-3GB / Approximately 2-3GB

**下载时间估计 / Download Time Estimate**:
- 快速网络 / Fast Network (10Mbps+): 2-5分钟 / 2-5 minutes
- 中速网络 / Medium Network (5Mbps): 5-10分钟 / 5-10 minutes
- 慢速网络 / Slow Network (<5Mbps): 10-20分钟 / 10-20 minutes

**如果下载失败 / If Download Fails**:

脚本会提供手动下载的命令：

```
请手动下载数据 / Please download data manually:

方法1 / Method 1:
  python -m qlib.run.get_data qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn

方法2 / Method 2:
  python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn

方法3 / Method 3:
  访问 / Visit: https://github.com/microsoft/qlib#data-preparation
```

### 步骤 5/5: 验证系统设置 / Validate System Setup

```
✓ 核心模块导入成功 / Core modules imported successfully
✓ Qlib初始化成功 / Qlib initialized successfully
✓ 数据访问成功 / Data access successful
  数据范围 / Data range: 2008-01-01 to 2024-12-05
  交易日数 / Trading days: 4123

✓ 系统验证通过！ / System validation passed!
```

**作用 / Purpose**: 验证所有组件是否正确安装和配置

**验证内容 / Validation Content**:
1. 核心模块导入 / Core module imports
2. Qlib初始化 / Qlib initialization
3. 数据访问测试 / Data access test
4. 配置文件加载 / Configuration loading

## 初始化完成 / Initialization Complete

成功完成所有步骤后，你会看到：

After successfully completing all steps, you will see:

```
======================================================================
  初始化总结 / Initialization Summary
======================================================================

✓ 系统初始化完成！ / System initialization completed!

您现在可以开始使用系统了 / You can now start using the system:

  1. 启动主界面 / Start main interface:
     python main.py

  2. 查看文档 / View documentation:
     docs/README.md

  3. 运行示例 / Run examples:
     python examples/demo_training_manager.py

  4. 查看配置 / View configuration:
     config/default_config.yaml

======================================================================
```

## 常见问题 / FAQ

### Q1: Python版本检查失败怎么办？

**A**: 确保安装了Python 3.8或更高版本：

```bash
# 检查Python版本 / Check Python version
python --version
# 或 / or
python3 --version

# 如果版本过低，请从官网下载最新版本 / If version is too low, download from official website
# https://www.python.org/downloads/
```

### Q2: 依赖安装失败怎么办？

**A**: 尝试以下解决方案：

```bash
# 方案1: 升级pip / Solution 1: Upgrade pip
python -m pip install --upgrade pip

# 方案2: 使用国内镜像源（中国用户）/ Solution 2: Use Chinese mirror (for Chinese users)
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 方案3: 逐个安装依赖 / Solution 3: Install dependencies one by one
pip install qlib
pip install numpy pandas
pip install scikit-learn lightgbm
# ... 等等 / etc.
```

### Q3: 数据下载失败怎么办？

**A**: 数据下载可能因网络问题失败，尝试：

```bash
# 方案1: 重新运行初始化 / Solution 1: Re-run initialization
python init_system.py

# 方案2: 手动下载数据 / Solution 2: Manually download data
python -m qlib.run.get_data qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn

# 方案3: 使用代理（如果在中国大陆）/ Solution 3: Use proxy (if in mainland China)
# 设置代理后再运行 / Set proxy then run
export http_proxy=http://your-proxy:port
export https_proxy=http://your-proxy:port
python init_system.py
```

### Q4: 数据下载很慢怎么办？

**A**: 这是正常的，数据文件较大（2-3GB）。你可以：

1. 耐心等待（通常5-10分钟）
2. 使用更快的网络连接
3. 在网络空闲时段下载
4. 考虑使用代理或VPN

### Q5: 验证步骤失败怎么办？

**A**: 检查以下几点：

```bash
# 1. 确认数据已下载 / Confirm data is downloaded
ls ~/.qlib/qlib_data/cn_data

# 2. 确认依赖已安装 / Confirm dependencies are installed
pip list | grep qlib

# 3. 查看详细错误信息 / View detailed error messages
python init_system.py  # 重新运行查看错误 / Re-run to see errors

# 4. 检查日志文件 / Check log files
cat logs/qlib_trading.log
```

### Q6: Windows上权限错误怎么办？

**A**: 以管理员身份运行：

1. 右键点击 `quick_start.bat`
2. 选择"以管理员身份运行"
3. 或在管理员命令提示符中运行 `python init_system.py`

### Q7: Mac上权限错误怎么办？

**A**: 添加执行权限：

```bash
# 添加执行权限 / Add execute permission
chmod +x quick_start.sh

# 如果仍有问题，使用sudo / If still having issues, use sudo
sudo ./quick_start.sh
```

## 手动初始化 / Manual Initialization

如果自动初始化失败，可以手动执行每个步骤：

If automatic initialization fails, you can manually execute each step:

### 1. 安装依赖 / Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. 创建目录 / Create Directories

```bash
mkdir -p data/cn_data
mkdir -p logs
mkdir -p outputs/backtests
mkdir -p outputs/reports
mkdir -p outputs/signals
mkdir -p model_registry
mkdir -p examples/mlruns
```

### 3. 下载数据 / Download Data

```bash
python -m qlib.run.get_data qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn
```

### 4. 验证安装 / Verify Installation

```bash
python -c "
import sys
sys.path.insert(0, 'src')
from infrastructure.qlib_wrapper import QlibWrapper
qlib = QlibWrapper()
qlib.init(provider_uri='~/.qlib/qlib_data/cn_data', region='cn')
print('✓ 系统验证通过 / System validation passed')
"
```

## 验证安装 / Verify Installation

初始化完成后，运行以下命令验证：

After initialization, run these commands to verify:

```bash
# 1. 检查Python包 / Check Python packages
python -c "import qlib; print(f'qlib version: {qlib.__version__}')"

# 2. 检查数据 / Check data
python -c "
from pathlib import Path
data_dir = Path.home() / '.qlib' / 'qlib_data' / 'cn_data'
print(f'Data exists: {data_dir.exists()}')
if data_dir.exists():
    print(f'Data files: {len(list(data_dir.rglob(\"*\")))}')
"

# 3. 启动系统 / Start system
python main.py
```

## 下一步 / Next Steps

初始化完成后，你可以：

After initialization, you can:

1. **启动主程序 / Start Main Program**
   ```bash
   python main.py
   ```

2. **查看教程 / View Tutorials**
   - [第一次训练模型](docs/tutorials/01_first_training.md)
   - [运行回测分析](docs/tutorials/02_run_backtest.md)
   - [生成交易信号](docs/tutorials/03_generate_signals.md)

3. **运行示例 / Run Examples**
   ```bash
   python examples/demo_training_manager.py
   python examples/demo_backtest_manager.py
   python examples/demo_signal_generator.py
   ```

4. **阅读文档 / Read Documentation**
   - [用户手册](docs/user_guide.md)
   - [API参考](docs/api_reference.md)
   - [配置说明](docs/configuration.md)

## 获取帮助 / Get Help

如果遇到问题：

If you encounter issues:

1. **查看日志 / Check Logs**
   ```bash
   cat logs/qlib_trading.log
   ```

2. **查看文档 / Check Documentation**
   - [常见问题](docs/FAQ.md)
   - [故障排除](docs/troubleshooting.md)

3. **提交Issue / Submit Issue**
   - [GitHub Issues](https://github.com/yourusername/QuantitationTranding/issues)

4. **加入讨论 / Join Discussion**
   - [GitHub Discussions](https://github.com/yourusername/QuantitationTranding/discussions)

---

**祝你使用愉快！ / Enjoy using the system!** 🚀📈
