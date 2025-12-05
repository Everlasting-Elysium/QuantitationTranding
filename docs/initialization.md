# 系统初始化文档 / System Initialization Documentation

## 概述 / Overview

本系统提供一键初始化功能，自动完成环境配置、依赖安装和数据下载。

This system provides one-click initialization to automatically complete environment configuration, dependency installation, and data download.

## 快速开始 / Quick Start

### 方法1: 使用快速启动脚本（推荐）

**Linux/Mac:**
```bash
./quick_start.sh
```

**Windows:**
```cmd
quick_start.bat
```

### 方法2: 使用Python脚本

```bash
python init_system.py
```

## 初始化步骤 / Initialization Steps

初始化脚本会自动执行以下步骤：

1. **检查Python版本** - 确保Python 3.8+
2. **检查依赖包** - 检测并可选安装缺失的包
3. **创建目录结构** - 创建必要的数据和日志目录
4. **下载示例数据** - 下载中国A股历史数据（可选）
5. **验证系统** - 运行测试确保系统正常工作

## 功能特性 / Features

### 依赖检测 / Dependency Detection

- 自动检测所有必需的Python包
- 显示已安装和缺失的包列表
- 可选择自动安装缺失的包

### 数据下载 / Data Download

- 自动下载qlib提供的中国A股数据
- 支持断点续传
- 提供手动下载指引

### 进度显示 / Progress Display

- 彩色终端输出
- 实时进度条
- 友好的中英双语提示

### 错误处理 / Error Handling

- 详细的错误信息
- 中文错误说明
- 提供解决方案链接

## 验证安装 / Verify Installation

运行验证脚本确认系统正常：

```bash
python verify_init.py
```

## 故障排除 / Troubleshooting

### 依赖安装失败

```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像（中国用户）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 数据下载失败

```bash
# 手动下载数据
python -m qlib.run.get_data qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn
```

### 权限错误

**Linux/Mac:**
```bash
chmod +x quick_start.sh
```

**Windows:**
以管理员身份运行

## 相关文档 / Related Documentation

- [详细初始化指南](../GETTING_STARTED_INIT.md)
- [用户手册](user_guide.md)
- [常见问题](FAQ.md)

## 技术细节 / Technical Details

### 依赖包列表

- qlib - 量化投资框架
- numpy - 数值计算
- pandas - 数据处理
- scikit-learn - 机器学习
- lightgbm - 梯度提升
- torch - 深度学习
- mlflow - 实验追踪
- matplotlib - 可视化
- seaborn - 统计可视化
- click - CLI框架
- rich - 终端美化
- pyyaml - 配置文件
- pytest - 测试框架

### 目录结构

```
QuantitationTranding/
├── data/cn_data/          # 数据目录
├── logs/                  # 日志目录
├── outputs/               # 输出目录
│   ├── backtests/        # 回测结果
│   ├── reports/          # 报告
│   └── signals/          # 交易信号
├── model_registry/        # 模型注册表
└── examples/mlruns/       # MLflow实验数据
```

## 支持 / Support

如有问题，请查看：
- [GitHub Issues](https://github.com/yourusername/QuantitationTranding/issues)
- [详细文档](../GETTING_STARTED_INIT.md)
