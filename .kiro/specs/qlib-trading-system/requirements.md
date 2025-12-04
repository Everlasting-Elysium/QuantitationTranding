# Requirements Document (需求文档)

## Introduction (简介)

本文档定义了一个基于qlib的智能量化交易系统的需求。该系统将提供从市场选择、智能推荐、策略优化、模型训练、历史回测、模拟交易到实盘交易的完整解决方案。系统支持多个市场（中国A股、美股等）和多种投资品类（股票、基金、ETF等），使用qlib框架进行数据处理和模型训练，使用MLflow进行实验管理和模型追踪。

**This document defines the requirements for an intelligent quantitative trading system based on qlib. The system provides a complete solution from market selection, intelligent recommendations, strategy optimization, model training, historical backtesting, simulation trading to live trading. The system supports multiple markets (China A-shares, US stocks, etc.) and various asset types (stocks, funds, ETFs, etc.), uses the qlib framework for data processing and model training, and uses MLflow for experiment management and model tracking.**

### 核心功能 (Core Features)

1. **智能引导式交互** - 无需编程，通过问答完成所有配置
   **Intelligent Guided Interaction** - No programming required, complete all configurations through Q&A

2. **多市场多品类支持** - 支持国内外股票、基金等多种投资品类
   **Multi-market Multi-asset Support** - Supports domestic and international stocks, funds, and other investment categories

3. **智能推荐系统** - 基于历史表现自动推荐优质标的
   **Intelligent Recommendation System** - Automatically recommends quality assets based on historical performance

4. **目标导向优化** - 根据用户期望收益率优化策略参数
   **Target-oriented Optimization** - Optimizes strategy parameters based on user's target returns

5. **完整的测试流程** - 历史回测 + 模拟交易双重验证
   **Complete Testing Process** - Historical backtesting + simulation trading dual verification

6. **实盘交易支持** - 无缝对接实盘交易接口，提供完善的风险控制
   **Live Trading Support** - Seamlessly integrates with live trading APIs with comprehensive risk control

7. **自动化报告** - 定期生成收益分析和风险预警
   **Automated Reporting** - Periodically generates performance analysis and risk alerts

## Glossary (术语表)

### 基础术语 (Basic Terms)
- **System (系统)**: 指本量化交易系统 / Refers to this quantitative trading system
- **qlib**: 微软开源的AI量化投资平台 / Microsoft's open-source AI quantitative investment platform
- **MLflow**: 开源的机器学习生命周期管理平台 / Open-source machine learning lifecycle management platform

### 交易相关 (Trading Related)
- **Market (市场)**: 投资市场，如中国A股、美股等 / Investment market, such as China A-shares, US stocks, etc.
- **Asset Type (资产类型)**: 投资品类，如股票、基金、ETF等 / Investment category, such as stocks, funds, ETFs, etc.
- **Portfolio (投资组合)**: 包含多个股票持仓的投资组合 / Investment portfolio containing multiple stock positions
- **Position (持仓)**: 当前持有的某只股票的数量和成本 / Current holdings of a stock with quantity and cost
- **Signal (交易信号)**: 模型输出的买入/卖出建议 / Buy/sell recommendations output by the model
- **Trade (交易)**: 一次买入或卖出操作 / A single buy or sell operation

### 模型相关 (Model Related)
- **Training Pipeline (训练流程)**: 模型训练流程，包括数据准备、特征工程、模型训练和评估 / Model training process including data preparation, feature engineering, training and evaluation
- **Experiment (实验)**: 一次完整的模型训练和评估过程 / A complete model training and evaluation process
- **Model Registry (模型注册表)**: 存储和管理训练好的模型 / Storage and management of trained models
- **Backtest (回测)**: 使用历史数据测试交易策略的表现 / Testing trading strategy performance using historical data

### 新增术语 (New Terms)
- **Simulation Trading (模拟交易)**: 使用真实市场数据进行模拟交易测试，不涉及真实资金 / Simulated trading using real market data without real money
- **Live Trading (实盘交易)**: 使用真实资金进行实际交易 / Actual trading with real money
- **Performance Analyzer (表现分析器)**: 分析历史市场表现并推荐优质标的的模块 / Module that analyzes historical market performance and recommends quality assets
- **Strategy Optimizer (策略优化器)**: 根据目标收益率优化策略参数的模块 / Module that optimizes strategy parameters based on target returns
- **Risk Manager (风险管理器)**: 监控和控制交易风险的模块 / Module that monitors and controls trading risks
- **Target Return (目标收益率)**: 用户期望达到的年化收益率 / User's expected annualized return rate
- **Risk Preference (风险偏好)**: 用户的风险承受能力，分为保守型、稳健型、进取型 / User's risk tolerance: conservative, moderate, aggressive
- **Sharpe Ratio (夏普比率)**: 衡量风险调整后收益的指标 / Metric measuring risk-adjusted returns
- **Max Drawdown (最大回撤)**: 投资组合从峰值到谷底的最大跌幅 / Maximum decline from peak to trough in portfolio value
- **Stop Loss (止损)**: 当亏损达到一定比例时自动卖出以限制损失 / Automatic sell when loss reaches certain percentage to limit losses
- **Position Sizing (仓位管理)**: 控制每只股票的持仓比例 / Controlling the proportion of each stock in portfolio

## Requirements

### Requirement 1

**User Story:** 作为量化研究员，我希望能够配置和初始化qlib环境，以便使用中国A股数据进行量化研究。

#### Acceptance Criteria

1. WHEN 系统启动时 THEN System SHALL 初始化qlib环境并连接到本地数据源
2. WHEN 数据源路径不存在时 THEN System SHALL 提供清晰的错误信息并指导用户下载数据
3. WHEN 初始化完成时 THEN System SHALL 验证数据可用性并输出数据时间范围
4. WHERE MLflow配置存在时 THEN System SHALL 初始化MLflow实验管理器并创建默认实验

### Requirement 2

**User Story:** 作为量化研究员，我希望能够训练多种预测模型，以便找到最适合当前市场的策略。

#### Acceptance Criteria

1. WHEN 用户启动训练流程时 THEN System SHALL 加载配置的数据集并进行特征工程
2. WHEN 训练数据准备完成时 THEN System SHALL 使用指定的模型架构进行训练
3. WHEN 模型训练过程中 THEN System SHALL 记录训练指标到MLflow
4. WHEN 模型训练完成时 THEN System SHALL 保存模型权重和元数据
5. WHERE 配置文件指定多个模型时 THEN System SHALL 依次训练所有模型并比较性能

### Requirement 3

**User Story:** 作为量化研究员，我希望能够实时监控模型训练过程，以便及时发现问题并调整参数。

#### Acceptance Criteria

1. WHEN 模型训练开始时 THEN System SHALL 在MLflow中创建新的运行记录
2. WHEN 每个训练epoch完成时 THEN System SHALL 记录损失函数值和评估指标
3. WHEN 训练过程中 THEN System SHALL 记录模型超参数到MLflow
4. WHEN 训练完成时 THEN System SHALL 记录最终模型性能指标和训练时长
5. WHERE 用户访问MLflow UI时 THEN System SHALL 展示所有实验的训练曲线和指标对比

### Requirement 4

**User Story:** 作为量化研究员，我希望能够对训练好的模型进行回测，以便评估模型在历史数据上的表现。

#### Acceptance Criteria

1. WHEN 用户指定模型和回测时间段时 THEN System SHALL 加载模型并生成预测信号
2. WHEN 预测信号生成后 THEN System SHALL 使用qlib的回测引擎模拟交易
3. WHEN 回测完成时 THEN System SHALL 计算收益率、夏普比率、最大回撤等指标
4. WHEN 回测结果生成时 THEN System SHALL 保存回测报告和交易明细
5. WHERE 配置了基准指数时 THEN System SHALL 计算相对基准的超额收益

### Requirement 5

**User Story:** 作为量化研究员，我希望能够可视化模型预测结果和回测表现，以便直观理解模型行为。

#### Acceptance Criteria

1. WHEN 回测完成时 THEN System SHALL 生成累计收益曲线图
2. WHEN 生成可视化报告时 THEN System SHALL 包含持仓分布、行业分布等图表
3. WHEN 用户请求预测分析时 THEN System SHALL 展示模型对个股的预测得分分布
4. WHEN 生成报告时 THEN System SHALL 对比策略收益与基准收益
5. WHERE 存在多个模型时 THEN System SHALL 生成模型性能对比图表

### Requirement 6

**User Story:** 作为量化交易员，我希望系统能够基于模型预测生成交易信号，以便指导实际交易决策。

#### Acceptance Criteria

1. WHEN 用户请求生成交易信号时 THEN System SHALL 使用最新数据进行模型预测
2. WHEN 预测完成时 THEN System SHALL 根据预测分数排序股票并生成买入候选列表
3. WHEN 生成交易信号时 THEN System SHALL 考虑当前持仓和风险限制
4. WHEN 信号生成完成时 THEN System SHALL 输出建议的买入、卖出和持有操作
5. WHERE 配置了风险控制参数时 THEN System SHALL 确保单只股票持仓不超过限制

### Requirement 7

**User Story:** 作为系统管理员，我希望系统能够管理和版本化训练好的模型，以便追踪模型演进和回滚。

#### Acceptance Criteria

1. WHEN 模型训练完成时 THEN System SHALL 将模型注册到模型注册表
2. WHEN 注册模型时 THEN System SHALL 记录模型版本、训练日期和性能指标
3. WHEN 用户查询模型时 THEN System SHALL 列出所有可用模型及其元数据
4. WHEN 用户选择模型时 THEN System SHALL 加载指定版本的模型进行预测
5. WHERE 模型性能优于当前生产模型时 THEN System SHALL 标记为候选生产模型

### Requirement 8

**User Story:** 作为量化研究员，我希望系统提供配置文件管理，以便灵活调整模型参数和数据设置。

#### Acceptance Criteria

1. WHEN 系统启动时 THEN System SHALL 从配置文件加载所有参数
2. WHEN 配置文件不存在时 THEN System SHALL 创建默认配置文件
3. WHEN 配置文件格式错误时 THEN System SHALL 提供详细的错误信息
4. WHERE 用户修改配置文件时 THEN System SHALL 在下次运行时应用新配置
5. WHEN 配置包含数据路径时 THEN System SHALL 验证路径有效性

### Requirement 9

**User Story:** 作为量化研究员，我希望系统能够处理数据更新，以便使用最新的市场数据进行训练和预测。

#### Acceptance Criteria

1. WHEN 用户触发数据更新时 THEN System SHALL 从数据源下载最新数据
2. WHEN 数据下载完成时 THEN System SHALL 验证数据完整性和格式
3. WHEN 数据验证通过时 THEN System SHALL 更新本地数据库
4. WHEN 数据更新失败时 THEN System SHALL 保留原有数据并记录错误日志
5. WHERE 数据包含缺失值时 THEN System SHALL 使用配置的填充策略处理

### Requirement 10

**User Story:** 作为开发者，我希望系统提供清晰的日志记录，以便调试问题和监控系统运行状态。

#### Acceptance Criteria

1. WHEN 系统执行任何操作时 THEN System SHALL 记录操作日志到文件
2. WHEN 发生错误时 THEN System SHALL 记录详细的错误堆栈信息
3. WHEN 记录日志时 THEN System SHALL 包含时间戳、日志级别和模块名称
4. WHERE 配置了日志级别时 THEN System SHALL 只记录该级别及以上的日志
5. WHEN 日志文件超过大小限制时 THEN System SHALL 自动轮转日志文件

### Requirement 11

**User Story:** 作为量化交易新手，我希望系统提供一键式安装和初始化流程，以便快速开始使用系统而无需深入了解技术细节。

#### Acceptance Criteria

1. WHEN 用户首次运行系统时 THEN System SHALL 自动检测缺失的依赖并提供安装指引
2. WHEN 用户执行初始化命令时 THEN System SHALL 自动下载示例数据并配置环境
3. WHEN 初始化过程中 THEN System SHALL 显示进度条和友好的提示信息
4. WHEN 初始化完成时 THEN System SHALL 运行一个简单的示例验证系统可用性
5. WHERE 初始化失败时 THEN System SHALL 提供中文错误说明和解决方案链接

### Requirement 12

**User Story:** 作为量化交易新手，我希望系统提供交互式命令行界面，以便通过简单的菜单选择完成操作而不需要编写代码。

#### Acceptance Criteria

1. WHEN 用户启动系统时 THEN System SHALL 显示主菜单列出所有可用功能
2. WHEN 用户选择功能时 THEN System SHALL 通过问答方式收集必要参数
3. WHEN 用户输入参数时 THEN System SHALL 提供默认值和参数说明
4. WHEN 操作执行时 THEN System SHALL 显示实时进度和状态信息
5. WHERE 用户输入无效时 THEN System SHALL 提示错误并允许重新输入

### Requirement 13

**User Story:** 作为量化交易新手，我希望系统提供详细的中文文档和教程，以便学习如何使用系统和理解量化交易概念。

#### Acceptance Criteria

1. WHEN 系统安装完成时 THEN System SHALL 在README中提供快速开始指南
2. WHEN 用户查看文档时 THEN System SHALL 提供每个功能的使用示例和参数说明
3. WHEN 文档中涉及专业术语时 THEN System SHALL 提供中文解释和通俗说明
4. WHERE 用户需要帮助时 THEN System SHALL 提供命令行帮助命令显示使用说明
5. WHEN 系统包含示例时 THEN System SHALL 提供从数据准备到交易信号生成的完整示例

### Requirement 14

**User Story:** 作为量化交易新手，我希望系统提供预配置的模型模板，以便直接使用而不需要理解模型架构和参数调优。

#### Acceptance Criteria

1. WHEN 系统初始化时 THEN System SHALL 提供至少三种预配置的模型模板
2. WHEN 用户选择模板时 THEN System SHALL 显示模板的适用场景和预期表现
3. WHEN 使用模板训练时 THEN System SHALL 使用经过验证的默认参数
4. WHEN 模板训练完成时 THEN System SHALL 生成易读的性能报告
5. WHERE 用户需要自定义时 THEN System SHALL 提供简化的参数调整界面

### Requirement 15

**User Story:** 作为量化交易新手，我希望系统能够解释模型预测结果，以便理解为什么系统建议买入或卖出某只股票。

#### Acceptance Criteria

1. WHEN 系统生成交易信号时 THEN System SHALL 提供信号的置信度分数
2. WHEN 用户查询信号原因时 THEN System SHALL 显示影响预测的主要因素
3. WHEN 展示预测结果时 THEN System SHALL 使用通俗语言解释技术指标
4. WHEN 生成报告时 THEN System SHALL 包含图表和可视化说明
5. WHERE 预测风险较高时 THEN System SHALL 明确标注风险警告

### Requirement 16 [NEW]

**User Story (用户故事):** 作为投资者，我希望系统能够支持多个市场和投资品类的选择，以便根据我的投资偏好进行配置。
**As an investor, I want the system to support multiple markets and asset types, so that I can configure based on my investment preferences.**

#### Acceptance Criteria (验收标准)

1. WHEN 用户启动系统时 THEN System SHALL 提供市场选择界面（国内/国外）
   **When user starts the system, the system shall provide market selection interface (domestic/international)**
2. WHEN 用户选择市场后 THEN System SHALL 显示该市场支持的投资品类（股票/基金/ETF等）
   **When user selects a market, the system shall display supported asset types for that market (stocks/funds/ETFs, etc.)**
3. WHEN 用户选择品类后 THEN System SHALL 加载对应的数据源和配置
   **When user selects an asset type, the system shall load corresponding data sources and configurations**
4. WHERE 市场数据不可用时 THEN System SHALL 提供清晰的错误提示和数据下载指引
   **Where market data is unavailable, the system shall provide clear error messages and data download guidance**
5. WHEN 用户切换市场时 THEN System SHALL 保存当前配置并切换到新市场环境
   **When user switches markets, the system shall save current configuration and switch to new market environment**

### Requirement 17 [NEW]

**User Story (用户故事):** 作为投资者，我希望系统能够基于历史表现推荐优质标的，以便我做出更明智的投资决策。
**As an investor, I want the system to recommend high-quality assets based on historical performance, so that I can make smarter investment decisions.**

#### Acceptance Criteria (验收标准)

1. WHEN 用户选择市场和品类后 THEN System SHALL 分析近3年该品类的市场表现
   **When user selects market and asset type, the system shall analyze 3-year historical performance for that category**
2. WHEN 分析完成时 THEN System SHALL 根据多个指标（收益率、夏普比率、最大回撤等）推荐前10名标的
   **When analysis completes, the system shall recommend top 10 assets based on multiple metrics (returns, Sharpe ratio, max drawdown, etc.)**
3. WHEN 显示推荐列表时 THEN System SHALL 展示每个标的的关键指标和推荐理由
   **When displaying recommendation list, the system shall show key metrics and recommendation reasons for each asset**
4. WHERE 用户选择多个标的时 THEN System SHALL 验证组合的相关性和分散度
   **Where user selects multiple assets, the system shall validate portfolio correlation and diversification**
5. WHEN 用户确认选择时 THEN System SHALL 保存选定的标的列表用于后续训练
   **When user confirms selection, the system shall save selected assets list for subsequent training**

### Requirement 18 [NEW]

**User Story (用户故事):** 作为投资者，我希望能够设定期望收益率目标，系统自动优化策略参数以达到目标。
**As an investor, I want to set target return goals, and have the system automatically optimize strategy parameters to achieve the target.**

#### Acceptance Criteria (验收标准)

1. WHEN 用户输入期望年化收益率时 THEN System SHALL 验证目标的合理性（基于历史数据）
   **When user inputs target annual return, the system shall validate target reasonableness (based on historical data)**
2. WHEN 用户选择风险偏好时 THEN System SHALL 根据风险偏好调整优化约束条件
   **When user selects risk preference, the system shall adjust optimization constraints based on risk preference**
3. WHEN 开始优化时 THEN System SHALL 使用多目标优化算法平衡收益和风险
   **When optimization starts, the system shall use multi-objective optimization to balance returns and risk**
4. WHEN 优化完成时 THEN System SHALL 展示预期收益、预期风险和建议的资产配置
   **When optimization completes, the system shall display expected returns, expected risk, and recommended asset allocation**
5. WHERE 目标无法达成时 THEN System SHALL 提供最接近的可行方案和调整建议
   **Where target cannot be achieved, the system shall provide closest feasible solution and adjustment suggestions**

### Requirement 19 [NEW]

**User Story (用户故事):** 作为投资者，我希望在实盘交易前进行模拟交易测试，以便验证策略的实际效果。
**As an investor, I want to conduct simulation trading before live trading, so that I can verify the strategy's actual effectiveness.**

#### Acceptance Criteria (验收标准)

1. WHEN 用户启动模拟交易时 THEN System SHALL 使用最新市场数据进行前向测试
   **When user starts simulation trading, the system shall use latest market data for forward testing**
2. WHEN 模拟交易运行时 THEN System SHALL 每日生成交易信号并模拟执行
   **When simulation trading runs, the system shall generate daily trading signals and simulate execution**
3. WHEN 模拟交易进行中 THEN System SHALL 实时更新持仓价值和收益情况
   **When simulation trading is in progress, the system shall update position values and returns in real-time**
4. WHEN 模拟周期结束时 THEN System SHALL 生成详细的模拟报告（收益、风险、交易明细）
   **When simulation period ends, the system shall generate detailed simulation report (returns, risk, trade details)**
5. WHERE 模拟结果不理想时 THEN System SHALL 提供参数调整建议和重新测试选项
   **Where simulation results are unsatisfactory, the system shall provide parameter adjustment suggestions and retest options**

### Requirement 20 [NEW]

**User Story (用户故事):** 作为投资者，我希望系统能够执行实盘交易，并提供完善的风险控制机制。
**As an investor, I want the system to execute live trading with comprehensive risk control mechanisms.**

#### Acceptance Criteria (验收标准)

1. WHEN 用户启动实盘交易时 THEN System SHALL 连接到券商交易接口并验证账户信息
   **When user starts live trading, the system shall connect to broker trading API and verify account information**
2. WHEN 生成交易信号时 THEN System SHALL 在执行前进行多层风险检查（仓位、止损、日内亏损等）
   **When generating trading signals, the system shall perform multi-level risk checks before execution (position size, stop loss, daily loss, etc.)**
3. WHEN 执行交易时 THEN System SHALL 记录所有订单详情并实时更新持仓状态
   **When executing trades, the system shall log all order details and update position status in real-time**
4. WHERE 触发风险预警时 THEN System SHALL 暂停交易并通知用户
   **Where risk alert is triggered, the system shall pause trading and notify user**
5. WHEN 交易日结束时 THEN System SHALL 生成当日交易总结和持仓报告
   **When trading day ends, the system shall generate daily trading summary and position report**

### Requirement 21 [NEW]

**User Story (用户故事):** 作为投资者，我希望系统能够定期生成收益报告和风险分析，以便持续监控投资表现。
**As an investor, I want the system to generate periodic performance reports and risk analysis, so that I can continuously monitor investment performance.**

#### Acceptance Criteria (验收标准)

1. WHEN 交易日结束时 THEN System SHALL 自动生成每日报告（当日收益、持仓、交易记录）
   **When trading day ends, the system shall automatically generate daily report (daily returns, positions, trade records)**
2. WHEN 每周结束时 THEN System SHALL 生成周报（周收益、策略表现、风险指标）
   **When week ends, the system shall generate weekly report (weekly returns, strategy performance, risk metrics)**
3. WHEN 每月结束时 THEN System SHALL 生成月报（月度收益、年化收益、与目标对比、调整建议）
   **When month ends, the system shall generate monthly report (monthly returns, annualized returns, target comparison, adjustment suggestions)**
4. WHERE 检测到异常风险时 THEN System SHALL 立即生成风险预警报告并发送通知
   **Where abnormal risk is detected, the system shall immediately generate risk alert report and send notification**
5. WHEN 生成报告时 THEN System SHALL 通过邮件/短信发送给用户
   **When generating reports, the system shall send to users via email/SMS**

### Requirement 22 [NEW]

**User Story (用户故事):** 作为投资者，我希望系统提供完整的引导式工作流程，从市场选择到实盘交易一站式完成。
**As an investor, I want the system to provide a complete guided workflow, from market selection to live trading in one seamless process.**

#### Acceptance Criteria (验收标准)

1. WHEN 用户首次使用时 THEN System SHALL 启动引导式工作流程，逐步收集用户配置
   **When user first uses the system, the system shall start guided workflow to collect user configurations step by step**
2. WHEN 每个步骤完成时 THEN System SHALL 保存进度并允许用户暂停或返回修改
   **When each step completes, the system shall save progress and allow user to pause or go back to modify**
3. WHEN 用户输入无效时 THEN System SHALL 提供实时验证和友好的中文错误提示
   **When user input is invalid, the system shall provide real-time validation and friendly Chinese error messages**
4. WHERE 工作流程中断时 THEN System SHALL 保存当前状态，下次启动时可以继续
   **Where workflow is interrupted, the system shall save current state and allow continuation on next startup**
5. WHEN 完成所有步骤时 THEN System SHALL 生成完整的配置总结供用户最终确认
   **When all steps complete, the system shall generate complete configuration summary for user final confirmation**
