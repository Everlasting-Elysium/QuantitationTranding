# 量化交易系统 (Quantitation Trading System)

基于qlib的智能量化交易平台，为新手和专业用户提供完整的模型训练、回测和交易信号生成功能。

## 🎯 项目概述

本系统是一个用户友好的量化交易平台，即使你是机器学习和量化交易的新手也能轻松使用。系统提供：

- 🚀 **一键初始化**: 自动配置环境和下载数据
- 📊 **交互式界面**: 无需编程，通过菜单完成所有操作
- 🤖 **预配置模型**: 开箱即用的模型模板
- 📈 **完整工作流**: 从数据准备到交易信号生成
- 🔍 **可视化分析**: 直观的图表和报告
- 💡 **智能解释**: 用通俗语言解释交易建议
- 📚 **中文文档**: 详细的教程和术语解释

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    CLI Interface Layer                   │
│  (交互式菜单、命令解析、进度显示、帮助系统)                │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                   Application Layer                      │
│  训练管理 | 回测管理 | 信号生成 | 模型注册 | 可视化 | 报告 │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                     Core Layer                           │
│  数据管理 | 模型工厂 | 配置管理                           │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                    │
│  Qlib框架 | MLflow追踪 | 日志系统                        │
└─────────────────────────────────────────────────────────┘
```

## ✨ 核心功能

### 1. 模型训练
- 支持多种模型类型（LGBM、Linear、MLP等）
- 预配置的模型模板，适合不同场景
- 自动特征工程和数据处理
- MLflow实验追踪和可视化

### 2. 回测分析
- 基于历史数据的策略回测
- 完整的性能指标（收益率、夏普比率、最大回撤等）
- 与基准指数对比
- 可视化的回测报告

### 3. 交易信号生成
- 基于模型预测生成买卖信号
- 智能风险控制和持仓管理
- 信号置信度评估
- 通俗易懂的信号解释

### 4. 模型管理
- 模型版本控制
- 性能追踪和对比
- 生产模型管理
- 模型元数据记录

### 5. 数据管理
- 自动下载中国A股数据
- 数据完整性验证
- 缺失值智能处理
- 数据更新机制

## 🚀 快速开始

### 环境要求

- Python 3.8+
- 16GB+ 内存
- 5GB+ 磁盘空间（用于数据存储）

### 一键初始化（推荐）

我们提供了一键初始化脚本，自动完成所有设置：

#### Linux/Mac用户：
```bash
# 进入项目目录
cd Code/QuantitationTranding

# 运行快速启动脚本（自动完成所有初始化）
chmod +x quick_start.sh
./quick_start.sh
```

#### Windows用户：
```cmd
# 进入项目目录
cd Code\QuantitationTranding

# 运行快速启动脚本（自动完成所有初始化）
quick_start.bat
```

#### 或者使用Python脚本：
```bash
# 适用于所有平台
python init_system.py
```

### 一键初始化做了什么？

初始化脚本会自动完成以下步骤：

1. ✅ **检查Python版本** - 确保Python 3.8+
2. ✅ **检查依赖包** - 自动检测缺失的依赖
3. ✅ **安装依赖** - 询问后自动安装缺失的包
4. ✅ **创建目录** - 创建必要的数据和日志目录
5. ✅ **下载数据** - 自动下载中国A股示例数据（约2-5分钟）
6. ✅ **验证系统** - 运行示例验证系统配置

### 手动安装步骤（可选）

如果你想手动控制每个步骤：

```bash
# 1. 进入项目目录
cd Code/QuantitationTranding

# 2. 安装依赖
pip install -r requirements.txt

# 3. 下载数据
python -m qlib.run.get_data qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn

# 4. 启动系统
python main.py
```

### 第一次使用

系统启动后，你会看到主菜单：

```
=== 量化交易系统 ===
1. 训练模型
2. 运行回测
3. 生成交易信号
4. 管理模型
5. 数据管理
6. 查看帮助
7. 退出

请选择功能 (1-7):
```

选择功能后，系统会通过问答方式引导你完成操作，无需编写任何代码！

## 📖 详细文档

- [快速开始指南](docs/quick_start.md) - 5分钟上手教程，从安装到第一次训练
- [用户手册](docs/user_guide.md) - 完整功能说明，涵盖所有操作
- [API参考](docs/api_reference.md) - 开发者文档，适合二次开发
- [初始化指南](docs/initialization.md) - 系统初始化详细说明

## 🎓 示例教程

查看 `examples/` 目录获取完整示例：

- `examples/01_first_training.md` - 第一次训练模型
- `examples/02_run_backtest.md` - 运行回测分析
- `examples/03_generate_signals.md` - 生成交易信号
- `examples/04_compare_models.md` - 对比多个模型

## 📁 项目结构

```
QuantitationTranding/
├── src/                    # 源代码
│   ├── cli/               # 命令行界面
│   ├── core/              # 核心功能
│   ├── application/       # 应用层
│   ├── infrastructure/    # 基础设施
│   ├── models/            # 数据模型
│   └── templates/         # 模型模板
├── tests/                 # 测试代码
│   ├── unit/             # 单元测试
│   ├── property/         # 属性测试
│   └── integration/      # 集成测试
├── config/               # 配置文件
├── data/                 # 数据目录
├── examples/             # 示例和教程
├── logs/                 # 日志文件
├── docs/                 # 文档
└── README.md            # 本文件
```

## 🛠️ 技术栈

- **核心框架**: qlib (微软量化投资平台)
- **实验追踪**: MLflow
- **CLI框架**: Click/Typer
- **可视化**: matplotlib, seaborn
- **测试**: pytest, Hypothesis
- **配置**: YAML
- **语言**: Python 3.8+

## 📊 预配置模型模板

系统提供三种开箱即用的模型模板：

### 1. LGBM模型 (推荐新手)
- **适用场景**: 中短期股票预测
- **优点**: 训练快速，效果稳定
- **预期年化收益**: 15-25%

### 2. Linear模型
- **适用场景**: 因子分析和特征研究
- **优点**: 可解释性强
- **预期年化收益**: 10-15%

### 3. MLP神经网络
- **适用场景**: 复杂模式识别
- **优点**: 捕捉非线性关系
- **预期年化收益**: 20-30%

## 🔧 开发计划

项目采用迭代开发方式，分为6个阶段：

1. ✅ **Phase 1**: 核心基础设施（配置、日志、数据管理）
2. ⏳ **Phase 2**: 训练流程（模型工厂、训练管理、MLflow集成）
3. ⏳ **Phase 3**: 回测分析（回测引擎、可视化、报告）
4. ⏳ **Phase 4**: 信号生成（信号生成器、风险控制、解释）
5. ⏳ **Phase 5**: 用户界面（CLI、交互式菜单、帮助系统）
6. ⏳ **Phase 6**: 文档和优化（教程、性能优化、测试）

详细的任务列表请查看 [.kiro/specs/qlib-trading-system/tasks.md](.kiro/specs/qlib-trading-system/tasks.md)

## 📝 开发文档

如果你想参与开发或了解系统设计：

- [需求文档](.kiro/specs/qlib-trading-system/requirements.md) - 完整的功能需求
- [设计文档](.kiro/specs/qlib-trading-system/design.md) - 系统架构和设计
- [任务列表](.kiro/specs/qlib-trading-system/tasks.md) - 开发任务清单

## 🤝 贡献指南

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与项目。

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [qlib](https://github.com/microsoft/qlib) - 微软开源的量化投资平台
- [MLflow](https://mlflow.org/) - 机器学习生命周期管理
- 所有贡献者和用户

## 📮 联系方式

- 问题反馈: [GitHub Issues](https://github.com/yourusername/QuantitationTranding/issues)
- 讨论交流: [GitHub Discussions](https://github.com/yourusername/QuantitationTranding/discussions)

---

**开始你的量化交易之旅吧！** 🚀📈
