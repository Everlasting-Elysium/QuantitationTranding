# Qlib Trading System Documentation

## 📚 文档目录

本目录包含Qlib量化交易系统的完整文档。

### 📖 文档列表

#### 新手入门

- **[quick_start.md](quick_start.md)** - 快速开始指南
  - 5分钟上手教程
  - 一键安装说明
  - 第一次训练模型
  - 常见问题解答
  - 术语解释

#### 完整指南

- **[user_guide.md](user_guide.md)** - 用户手册
  - 系统概述
  - 模型训练详解
  - 回测分析指南
  - 交易信号生成
  - 模型管理
  - 数据管理
  - 配置管理
  - 高级功能
  - 最佳实践
  - 故障排除

#### 开发者文档

- **[api_reference.md](api_reference.md)** - API参考文档
  - 核心模块API
  - 应用模块API
  - 基础设施模块API
  - 数据模型定义
  - 工具函数
  - 完整示例代码

#### 系统文档

- **[initialization.md](initialization.md)** - 初始化指南
  - 系统初始化详细说明
  - 依赖安装
  - 数据下载
  - 环境配置

### 📝 文档说明

所有文档均使用**中英双语**编写，旨在帮助新手和专业用户快速上手量化交易系统。

- **中文为主**: 所有说明和教程都有详细的中文解释
- **英文注释**: 代码和技术术语提供英文对照
- **通俗易懂**: 使用通俗语言解释专业术语
- **示例丰富**: 每个功能都有完整的使用示例

### 🎯 如何使用文档

#### 如果你是新手

1. 从 [quick_start.md](quick_start.md) 开始
2. 完成第一次模型训练
3. 阅读 [user_guide.md](user_guide.md) 了解所有功能
4. 查看术语表理解专业概念

#### 如果你是开发者

1. 阅读 [api_reference.md](api_reference.md) 了解API
2. 查看完整示例代码
3. 参考数据模型定义
4. 使用工具函数简化开发

#### 如果你遇到问题

1. 查看 [user_guide.md](user_guide.md) 的故障排除章节
2. 查看 [quick_start.md](quick_start.md) 的常见问题
3. 检查日志文件 `logs/qlib_trading.log`
4. 在GitHub提交Issue

### 📊 文档结构

```
docs/
├── README.md              # 本文件
├── quick_start.md         # 快速开始（新手必读）
├── user_guide.md          # 用户手册（完整功能）
├── api_reference.md       # API参考（开发者）
├── initialization.md      # 初始化指南
├── cli_usage.md          # CLI使用说明
├── backtest_cli_usage.md # 回测CLI说明
├── signal_cli_usage.md   # 信号CLI说明
├── training_cli_usage.md # 训练CLI说明
├── data_management_cli.md # 数据管理CLI说明
├── model_management_cli.md # 模型管理CLI说明
└── ... (其他模块文档)
```

### 🔍 快速查找

#### 我想...

- **安装系统** → [quick_start.md](quick_start.md#一键安装)
- **训练第一个模型** → [quick_start.md](quick_start.md#第一次训练模型)
- **运行回测** → [user_guide.md](user_guide.md#回测分析)
- **生成交易信号** → [user_guide.md](user_guide.md#交易信号)
- **理解指标含义** → [user_guide.md](user_guide.md#理解回测指标)
- **调整模型参数** → [user_guide.md](user_guide.md#参数调优建议)
- **二次开发** → [api_reference.md](api_reference.md)
- **解决问题** → [user_guide.md](user_guide.md#故障排除)

### 💡 学习路径

#### 初级用户（0-1周）

1. ✅ 完成系统安装
2. ✅ 运行第一个模型训练
3. ✅ 理解基本概念（IC、夏普比率等）
4. ✅ 尝试不同的模型模板
5. ✅ 运行简单回测

#### 中级用户（1-4周）

1. ✅ 自定义训练参数
2. ✅ 分析回测结果
3. ✅ 生成交易信号
4. ✅ 理解风险控制
5. ✅ 对比多个模型

#### 高级用户（1个月+）

1. ✅ 开发自定义特征
2. ✅ 实现自定义策略
3. ✅ 批量训练和回测
4. ✅ 性能优化
5. ✅ 实盘交易准备

### 🌟 文档特色

- **循序渐进**: 从简单到复杂，逐步深入
- **实例驱动**: 每个概念都有实际例子
- **双语对照**: 中英文对照，便于理解
- **图文并茂**: 包含流程图和示例输出
- **持续更新**: 随系统更新而更新

### 🤝 贡献文档

欢迎贡献文档！如果你发现：

- 文档中的错误或不清楚的地方
- 缺少某个功能的说明
- 有更好的示例或解释
- 想要添加新的教程

请：

1. Fork项目
2. 修改文档
3. 提交Pull Request
4. 等待审核

### 📮 反馈

如果你对文档有任何建议或问题：

- 提交GitHub Issue
- 在Discussions中讨论
- 发送邮件反馈

### 📄 许可证

文档采用 CC BY-SA 4.0 许可证

---

**开始你的量化交易学习之旅！** 📚🚀
