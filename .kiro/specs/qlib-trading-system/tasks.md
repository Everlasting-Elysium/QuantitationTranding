# Implementation Plan

- [x] 1. 设置项目结构和核心基础设施
  - 创建目录结构（src/, tests/, config/, docs/等）
  - 设置requirements.txt和setup.py
  - 配置pytest和测试环境
  - _Requirements: 8.1, 10.1_

- [ ]* 1.1 编写项目结构创建的单元测试
  - 测试目录创建功能
  - 测试文件权限设置
  - _Requirements: 8.1_

- [x] 2. 实现配置管理系统
  - 创建ConfigManager类，支持YAML配置文件加载
  - 实现配置验证逻辑
  - 实现默认配置生成功能
  - _Requirements: 8.1, 8.2, 8.3, 8.5_

- [ ]* 2.1 编写配置管理的属性测试
  - **Property 31: Configuration loaded from file**
  - **Validates: Requirements 8.1**

- [ ]* 2.2 编写配置验证的属性测试
  - **Property 33: Data paths validated in config**
  - **Validates: Requirements 8.5**

- [ ]* 2.3 编写配置更新的单元测试
  - 测试配置文件修改后重新加载
  - 测试无效配置的错误处理
  - _Requirements: 8.3, 8.4_

- [x] 3. 实现日志系统
  - 创建LoggerSystem类
  - 实现日志文件轮转功能
  - 配置不同级别的日志输出
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ]* 3.1 编写日志记录的属性测试
  - **Property 37: Operations logged to file**
  - **Validates: Requirements 10.1**

- [ ]* 3.2 编写日志格式的属性测试
  - **Property 39: Log entries contain required fields**
  - **Validates: Requirements 10.3**

- [ ]* 3.3 编写日志过滤的属性测试
  - **Property 40: Logs filtered by configured level**
  - **Validates: Requirements 10.4**

- [ ]* 3.4 编写日志轮转的属性测试
  - **Property 41: Log files rotated when size exceeded**
  - **Validates: Requirements 10.5**

- [x] 4. 实现Qlib封装层
  - 创建QlibWrapper类
  - 实现qlib初始化逻辑
  - 实现数据访问接口
  - 添加异常处理和错误信息转换
  - _Requirements: 1.1, 1.2_

- [ ]* 4.1 编写qlib初始化的属性测试
  - **Property 1: Qlib initialization succeeds for valid configurations**
  - **Validates: Requirements 1.1**

- [ ]* 4.2 编写数据验证的属性测试
  - **Property 2: Data validation returns time range after initialization**
  - **Validates: Requirements 1.3**

- [x] 5. 实现数据管理器
  - 创建DataManager类
  - 实现数据下载功能
  - 实现数据验证和完整性检查
  - 实现缺失值处理策略
  - _Requirements: 1.3, 9.1, 9.2, 9.3, 9.5_

- [ ]* 5.1 编写数据验证的属性测试
  - **Property 34: Downloaded data passes validation**
  - **Validates: Requirements 9.2**

- [ ]* 5.2 编写数据更新的属性测试
  - **Property 35: Validated data updates local database**
  - **Validates: Requirements 9.3**

- [ ]* 5.3 编写缺失值处理的属性测试
  - **Property 36: Missing values handled by strategy**
  - **Validates: Requirements 9.5**

- [x] 6. 实现MLflow集成
  - 创建MLflowTracker类
  - 实现实验创建和运行管理
  - 实现参数和指标记录功能
  - 实现模型保存到MLflow
  - _Requirements: 1.4, 3.1, 3.2, 3.3, 3.4_

- [ ]* 6.1 编写MLflow初始化的属性测试
  - **Property 3: MLflow initialization when configured**
  - **Validates: Requirements 1.4**

- [ ]* 6.2 编写MLflow运行创建的属性测试
  - **Property 9: MLflow run created for each training**
  - **Validates: Requirements 3.1**

- [ ]* 6.3 编写参数记录的属性测试
  - **Property 10: Hyperparameters logged to MLflow**
  - **Validates: Requirements 3.3**

- [x] 7. Checkpoint - 确保所有基础设施测试通过
  - 确保所有测试通过，如有问题请询问用户

- [x] 8. 实现模型模板系统
  - 创建ModelTemplate数据类
  - 定义至少三种预配置模型模板（LGBM、Linear、MLP）
  - 在YAML文件中配置模板参数
  - _Requirements: 14.1, 14.2, 14.3_

- [ ]* 8.1 编写模板描述的属性测试
  - **Property 43: Model templates include descriptions**
  - **Validates: Requirements 14.2**

- [ ]* 8.2 编写模板参数的属性测试
  - **Property 44: Templates use default parameters**
  - **Validates: Requirements 14.3**

- [x] 9. 实现模型工厂
  - 创建ModelFactory类
  - 实现各种模型类型的创建逻辑
  - 实现模板加载功能
  - 实现参数验证
  - _Requirements: 2.2_

- [ ]* 9.1 编写模型创建的单元测试
  - 测试每种支持的模型类型
  - 测试无效模型类型的错误处理
  - _Requirements: 2.2_

- [x] 10. 实现训练管理器
  - 创建TrainingManager类
  - 实现完整的训练流程（数据加载、特征工程、训练、保存）
  - 集成MLflow追踪
  - 实现从模板训练的功能
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [ ]* 10.1 编写数据加载的属性测试
  - **Property 4: Training loads dataset for valid config**
  - **Validates: Requirements 2.1**

- [ ]* 10.2 编写模型训练的属性测试
  - **Property 5: Model training completes for supported types**
  - **Validates: Requirements 2.2**

- [ ]* 10.3 编写训练指标记录的属性测试
  - **Property 6: Training metrics logged to MLflow**
  - **Validates: Requirements 2.3, 3.2**

- [ ]* 10.4 编写模型保存的属性测试
  - **Property 7: Model saved after training**
  - **Validates: Requirements 2.4**

- [ ]* 10.5 编写多模型训练的属性测试
  - **Property 8: Multiple models trained sequentially**
  - **Validates: Requirements 2.5**

- [ ]* 10.6 编写最终指标记录的属性测试
  - **Property 11: Final metrics recorded after training**
  - **Validates: Requirements 3.4**

- [x] 11. 实现模型注册表
  - 创建ModelRegistry类
  - 实现模型注册和版本管理
  - 实现模型查询和加载功能
  - 实现生产模型标记功能
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ]* 11.1 编写模型注册的属性测试
  - **Property 26: Models registered after training**
  - **Validates: Requirements 7.1**

- [ ]* 11.2 编写模型元数据的属性测试
  - **Property 27: Model metadata recorded at registration**
  - **Validates: Requirements 7.2**

- [ ]* 11.3 编写模型查询的属性测试
  - **Property 28: Model query returns all registered models**
  - **Validates: Requirements 7.3**

- [ ]* 11.4 编写模型加载的属性测试
  - **Property 29: Registered models can be loaded**
  - **Validates: Requirements 7.4**

- [ ]* 11.5 编写候选模型标记的属性测试
  - **Property 30: Better models marked as candidates**
  - **Validates: Requirements 7.5**

- [x] 12. Checkpoint - 确保训练流程测试通过
  - 确保所有测试通过，如有问题请询问用户

- [x] 13. 实现回测管理器
  - 创建BacktestManager类
  - 实现信号生成逻辑
  - 集成qlib回测引擎
  - 实现性能指标计算（收益率、夏普比率、最大回撤等）
  - 实现基准对比功能
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ]* 13.1 编写信号生成的属性测试
  - **Property 12: Backtest generates signals from model**
  - **Validates: Requirements 4.1**

- [ ]* 13.2 编写回测执行的属性测试
  - **Property 13: Backtest executes with signals**
  - **Validates: Requirements 4.2**

- [ ]* 13.3 编写指标计算的属性测试
  - **Property 14: Backtest calculates required metrics**
  - **Validates: Requirements 4.3**

- [ ]* 13.4 编写报告保存的属性测试
  - **Property 15: Backtest saves report and trades**
  - **Validates: Requirements 4.4**

- [ ]* 13.5 编写超额收益计算的属性测试
  - **Property 16: Excess returns calculated with benchmark**
  - **Validates: Requirements 4.5**

- [x] 14. 实现可视化管理器
  - 创建VisualizationManager类
  - 实现累计收益曲线图生成
  - 实现持仓分布图生成
  - 实现行业分布图生成
  - 实现多模型对比图生成
  - _Requirements: 5.1, 5.2, 5.5_

- [ ]* 14.1 编写收益曲线图的属性测试
  - **Property 17: Cumulative returns chart generated**
  - **Validates: Requirements 5.1**

- [ ]* 14.2 编写报告图表的属性测试
  - **Property 18: Report contains all required charts**
  - **Validates: Requirements 5.2**

- [ ]* 14.3 编写多模型对比的属性测试
  - **Property 21: Multi-model comparison chart generated**
  - **Validates: Requirements 5.5**

- [x] 15. 实现报告生成器
  - 创建ReportGenerator类
  - 实现训练报告生成
  - 实现回测报告生成
  - 实现HTML报告生成
  - 集成可视化图表
  - _Requirements: 5.4, 14.4, 15.4_

- [ ]* 15.1 编写策略对比的属性测试
  - **Property 20: Report compares strategy vs benchmark**
  - **Validates: Requirements 5.4**

- [ ]* 15.2 编写模板报告的属性测试
  - **Property 45: Template training generates report**
  - **Validates: Requirements 14.4**

- [ ]* 15.3 编写报告可视化的属性测试
  - **Property 48: Reports include visualizations**
  - **Validates: Requirements 15.4**

- [x] 16. 实现交易信号生成器
  - 创建SignalGenerator类
  - 实现基于模型预测的信号生成
  - 实现股票排序和候选列表生成
  - 实现风险控制逻辑
  - 实现持仓限制检查
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ]* 16.1 编写最新数据使用的属性测试
  - **Property 22: Signal generation uses latest data**
  - **Validates: Requirements 6.1**

- [ ]* 16.2 编写股票排序的属性测试
  - **Property 23: Stocks sorted by prediction score**
  - **Validates: Requirements 6.2**

- [ ]* 16.3 编写风险限制的属性测试
  - **Property 24: Signals respect risk limits**
  - **Validates: Requirements 6.3, 6.5**

- [ ]* 16.4 编写信号类型的属性测试
  - **Property 25: Signals include all action types**
  - **Validates: Requirements 6.4**

- [x] 17. 实现信号解释功能
  - 扩展SignalGenerator添加解释功能
  - 实现特征重要性分析
  - 实现通俗语言描述生成
  - 实现风险等级评估和警告
  - _Requirements: 5.3, 15.1, 15.2, 15.5_

- [ ]* 17.1 编写预测分析的属性测试
  - **Property 19: Prediction analysis returns score distribution**
  - **Validates: Requirements 5.3**

- [ ]* 17.2 编写置信度的属性测试
  - **Property 46: Signals include confidence scores**
  - **Validates: Requirements 15.1**

- [ ]* 17.3 编写信号解释的属性测试
  - **Property 47: Signal explanations available**
  - **Validates: Requirements 15.2**

- [ ]* 17.4 编写风险警告的属性测试
  - **Property 49: High-risk predictions marked with warnings**
  - **Validates: Requirements 15.5**

- [x] 18. Checkpoint - 确保核心功能测试通过
  - 确保所有测试通过，如有问题请询问用户

- [x] 19. 实现交互式提示系统
  - 创建InteractivePrompt类
  - 实现文本输入收集
  - 实现选择题输入
  - 实现数字输入验证
  - 实现日期输入验证
  - 实现确认提示
  - _Requirements: 12.2, 12.3, 12.5_

- [ ]* 19.1 编写输入验证的属性测试
  - **Property 42: Invalid input prompts error and retry**
  - **Validates: Requirements 12.5**

- [x] 20. 实现主CLI界面
  - 创建MainCLI类
  - 实现主菜单显示
  - 实现功能路由
  - 实现帮助系统
  - 添加中文界面和提示
  - _Requirements: 12.1, 12.4, 13.4_

- [ ]* 20.1 编写帮助功能的单元测试
  - 测试帮助命令输出
  - 测试各功能的帮助信息
  - _Requirements: 13.4_

- [x] 21. 实现训练功能CLI
  - 在MainCLI中添加训练菜单
  - 实现模板选择界面
  - 实现自定义参数输入
  - 实现训练进度显示
  - 集成TrainingManager
  - _Requirements: 2.1, 2.2, 14.1, 14.5_

- [x] 22. 实现回测功能CLI
  - 在MainCLI中添加回测菜单
  - 实现模型选择界面
  - 实现回测参数输入
  - 实现回测进度显示
  - 集成BacktestManager
  - _Requirements: 4.1, 4.2_

- [x] 23. 实现信号生成功能CLI
  - 在MainCLI中添加信号生成菜单
  - 实现模型选择界面
  - 实现信号查看和解释界面
  - 集成SignalGenerator
  - _Requirements: 6.1, 6.4, 15.2_

- [x] 24. 实现数据管理功能CLI
  - 在MainCLI中添加数据管理菜单
  - 实现数据下载界面
  - 实现数据验证界面
  - 实现数据信息查看
  - 集成DataManager
  - _Requirements: 9.1, 9.2_

- [x] 25. 实现模型管理功能CLI
  - 在MainCLI中添加模型管理菜单
  - 实现模型列表查看
  - 实现模型详情查看
  - 实现生产模型设置
  - 集成ModelRegistry
  - _Requirements: 7.3, 7.4, 7.5_

- [x] 26. 实现一键初始化功能
  - 创建初始化命令
  - 实现依赖检测
  - 实现自动数据下载
  - 实现示例运行验证
  - 添加友好的进度提示
  - _Requirements: 11.1, 11.2, 11.4_

- [ ]* 26.1 编写初始化功能的集成测试
  - 测试完整初始化流程
  - 测试依赖检测
  - 测试示例验证
  - _Requirements: 11.1, 11.2, 11.4_

- [x] 27. 编写中文文档
  - 编写README.md快速开始指南
  - 编写docs/quick_start.md详细教程
  - 编写docs/user_guide.md用户手册
  - 编写docs/api_reference.md API文档
  - 添加术语解释和通俗说明
  - _Requirements: 13.1, 13.2, 13.3, 13.5_

- [x] 28. 创建示例和教程
  - 创建完整的端到端示例
  - 创建各功能的独立示例
  - 添加示例说明文档
  - _Requirements: 13.5_

- [x] 29. 实现错误处理和恢复
  - 在所有模块中添加异常处理
  - 实现错误信息中文化
  - 实现错误恢复逻辑
  - 添加错误日志记录
  - _Requirements: 1.2, 8.3, 9.4, 11.5_

- [ ]* 29.1 编写错误日志的属性测试
  - **Property 38: Errors logged with stack trace**
  - **Validates: Requirements 10.2**

- [ ]* 29.2 编写错误处理的单元测试
  - 测试各种错误场景
  - 测试错误恢复逻辑
  - 测试错误信息格式
  - _Requirements: 1.2, 8.3, 9.4, 11.5_

- [x] 30. 性能优化和最终测试
  - 优化数据加载性能
  - 实现缓存机制
  - 进行端到端集成测试
  - 修复发现的bug
  - _Requirements: All_

- [ ]* 30.1 运行完整的集成测试套件
  - 测试完整训练工作流
  - 测试完整回测工作流
  - 测试完整信号生成工作流
  - 测试数据更新工作流
  - _Requirements: All_

- [x] 31. Final Checkpoint - 确保所有测试通过
  - 确保所有测试通过，如有问题请询问用户

## 新增功能任务 (New Feature Tasks) [NEW]

### Phase 1: 市场选择和智能推荐 (Market Selection and Intelligent Recommendation)

- [x] 32. 实现市场选择器 (Implement Market Selector)
  - 创建MarketSelector类 / Create MarketSelector class
  - 实现市场配置加载（国内/国外）/ Implement market configuration loading (domestic/international)
  - 实现资产类型管理（股票/基金/ETF）/ Implement asset type management (stocks/funds/ETFs)
  - 添加市场数据源配置 / Add market data source configuration
  - _Requirements: 16.1, 16.2, 16.3_

- [ ]* 32.1 编写市场选择的单元测试 (Write unit tests for market selection)
  - 测试市场列表获取 / Test market list retrieval
  - 测试资产类型获取 / Test asset type retrieval
  - 测试市场切换功能 / Test market switching functionality
  - _Requirements: 16.1, 16.2, 16.5_

- [x] 33. 实现历史表现分析器 (Implement Performance Analyzer)
  - 创建PerformanceAnalyzer类 / Create PerformanceAnalyzer class
  - 实现3年历史数据分析 / Implement 3-year historical data analysis
  - 计算关键指标（收益率、夏普比率、最大回撤）/ Calculate key metrics (returns, Sharpe ratio, max drawdown)
  - 实现资产排名算法 / Implement asset ranking algorithm
  - 生成推荐列表 / Generate recommendation list
  - _Requirements: 17.1, 17.2, 17.3_

- [ ]* 33.1 编写表现分析的单元测试 (Write unit tests for performance analysis)
  - 测试历史数据分析 / Test historical data analysis
  - 测试指标计算准确性 / Test metric calculation accuracy
  - 测试推荐算法 / Test recommendation algorithm
  - _Requirements: 17.1, 17.2_

- [ ]* 33.2 编写推荐验证的属性测试 (Write property tests for recommendation validation)
  - 验证推荐资产的相关性 / Validate correlation of recommended assets
  - 验证组合分散度 / Validate portfolio diversification
  - _Requirements: 17.4_

### Phase 2: 策略优化 (Strategy Optimization)

- [x] 34. 实现策略优化器 (Implement Strategy Optimizer)
  - 创建StrategyOptimizer类 / Create StrategyOptimizer class
  - 实现目标收益率验证 / Implement target return validation
  - 实现多目标优化算法 / Implement multi-objective optimization algorithm
  - 实现风险偏好调整 / Implement risk preference adjustment
  - 生成优化后的资产配置 / Generate optimized asset allocation
  - _Requirements: 18.1, 18.2, 18.3, 18.4_

- [ ]* 34.1 编写优化算法的单元测试 (Write unit tests for optimization algorithm)
  - 测试目标收益率验证 / Test target return validation
  - 测试优化约束条件 / Test optimization constraints
  - 测试资产配置生成 / Test asset allocation generation
  - _Requirements: 18.1, 18.3, 18.4_

- [ ]* 34.2 编写优化结果的属性测试 (Write property tests for optimization results)
  - 验证优化结果满足约束 / Validate optimization results meet constraints
  - 验证风险收益平衡 / Validate risk-return balance
  - _Requirements: 18.2, 18.3_

- [x] 35. 增强训练管理器支持目标导向训练 (Enhance Training Manager for target-oriented training)
  - 扩展TrainingManager类 / Extend TrainingManager class
  - 集成StrategyOptimizer / Integrate StrategyOptimizer
  - 实现基于目标收益率的参数调整 / Implement parameter adjustment based on target returns
  - 添加优化结果记录到MLflow / Add optimization results logging to MLflow
  - _Requirements: 18.3, 18.4_

### Phase 3: 投资组合和风险管理 (Portfolio and Risk Management)

- [x] 36. 实现投资组合管理器 (Implement Portfolio Manager)
  - 创建PortfolioManager类 / Create PortfolioManager class
  - 实现持仓创建和更新 / Implement position creation and updates
  - 实现组合价值计算 / Implement portfolio value calculation
  - 实现交易历史记录 / Implement trade history tracking
  - 实现收益率计算 / Implement returns calculation
  - _Requirements: 19.3, 20.3_

- [ ]* 36.1 编写组合管理的单元测试 (Write unit tests for portfolio management)
  - 测试持仓更新 / Test position updates
  - 测试价值计算 / Test value calculation
  - 测试收益率计算 / Test returns calculation
  - _Requirements: 19.3, 20.3_

- [x] 37. 实现风险管理器 (Implement Risk Manager)
  - 创建RiskManager类 / Create RiskManager class
  - 实现持仓风险检查 / Implement position risk checks
  - 实现VaR计算 / Implement VaR calculation
  - 实现最大回撤监控 / Implement max drawdown monitoring
  - 实现集中度风险检查 / Implement concentration risk checks
  - 实现风险预警生成 / Implement risk alert generation
  - _Requirements: 20.2, 20.4, 21.4_

- [ ]* 37.1 编写风险检查的单元测试 (Write unit tests for risk checks)
  - 测试持仓风险检查 / Test position risk checks
  - 测试VaR计算 / Test VaR calculation
  - 测试风险预警触发 / Test risk alert triggering
  - _Requirements: 20.2, 20.4_

- [ ]* 37.2 编写风险管理的属性测试 (Write property tests for risk management)
  - 验证风险限制始终被遵守 / Validate risk limits are always respected
  - 验证风险预警及时触发 / Validate risk alerts trigger timely
  - _Requirements: 20.2, 20.4, 21.4_

### Phase 4: 模拟交易引擎 (Simulation Trading Engine)

- [x] 38. 实现模拟交易引擎 (Implement Simulation Engine)
  - 创建SimulationEngine类 / Create SimulationEngine class
  - 实现模拟会话管理 / Implement simulation session management
  - 实现每日信号生成和执行 / Implement daily signal generation and execution
  - 实现模拟持仓跟踪 / Implement simulated position tracking
  - 实现模拟收益计算 / Implement simulated returns calculation
  - 生成模拟报告 / Generate simulation reports
  - _Requirements: 19.1, 19.2, 19.3, 19.4_

- [ ]* 38.1 编写模拟交易的单元测试 (Write unit tests for simulation trading)
  - 测试会话创建 / Test session creation
  - 测试信号执行 / Test signal execution
  - 测试持仓更新 / Test position updates
  - 测试收益计算 / Test returns calculation
  - _Requirements: 19.1, 19.2, 19.3_

- [ ]* 38.2 编写模拟报告的单元测试 (Write unit tests for simulation reports)
  - 测试报告生成 / Test report generation
  - 测试指标计算 / Test metrics calculation
  - _Requirements: 19.4_

- [x] 39. 集成模拟交易到CLI (Integrate simulation trading into CLI)
  - 在MainCLI中添加模拟交易菜单 / Add simulation trading menu to MainCLI
  - 实现模拟参数输入界面 / Implement simulation parameter input interface
  - 实现模拟进度显示 / Implement simulation progress display
  - 实现模拟结果查看 / Implement simulation results viewing
  - 提供参数调整和重新测试选项 / Provide parameter adjustment and retest options
  - _Requirements: 19.1, 19.4, 19.5_

### Phase 5: 实盘交易系统 (Live Trading System)

- [x] 40. 实现交易API适配器 (Implement Trading API Adapter)
  - 创建TradingAPIAdapter类 / Create TradingAPIAdapter class
  - 实现券商连接接口 / Implement broker connection interface
  - 实现订单下单功能 / Implement order placement functionality
  - 实现订单查询和取消 / Implement order query and cancellation
  - 实现账户信息查询 / Implement account information query
  - 实现持仓查询 / Implement position query
  - _Requirements: 20.1, 20.3_

- [ ]* 40.1 编写交易API的单元测试 (Write unit tests for trading API)
  - 测试连接功能 / Test connection functionality
  - 测试订单操作 / Test order operations
  - 测试查询功能 / Test query functionality
  - _Requirements: 20.1, 20.3_

- [x] 41. 实现实盘交易管理器 (Implement Live Trading Manager)
  - 创建LiveTradingManager类 / Create LiveTradingManager class
  - 实现交易会话管理 / Implement trading session management
  - 集成RiskManager进行风险检查 / Integrate RiskManager for risk checks
  - 实现订单执行逻辑 / Implement order execution logic
  - 实现持仓实时更新 / Implement real-time position updates
  - 实现交易暂停和恢复 / Implement trading pause and resume
  - _Requirements: 20.1, 20.2, 20.3, 20.4, 20.5_

- [ ]* 41.1 编写实盘交易的单元测试 (Write unit tests for live trading)
  - 测试会话管理 / Test session management
  - 测试风险检查集成 / Test risk check integration
  - 测试订单执行 / Test order execution
  - 测试暂停恢复功能 / Test pause/resume functionality
  - _Requirements: 20.1, 20.2, 20.3, 20.4_

- [ ]* 41.2 编写实盘交易的集成测试 (Write integration tests for live trading)
  - 测试完整交易流程 / Test complete trading workflow
  - 测试风险预警触发 / Test risk alert triggering
  - 测试异常情况处理 / Test exception handling
  - _Requirements: 20.2, 20.4, 20.5_

- [x] 42. 集成实盘交易到CLI (Integrate live trading into CLI)
  - 在MainCLI中添加实盘交易菜单 / Add live trading menu to MainCLI
  - 实现券商配置界面 / Implement broker configuration interface
  - 实现交易参数设置 / Implement trading parameter settings
  - 实现实时状态监控 / Implement real-time status monitoring
  - 实现交易控制（启动/暂停/停止）/ Implement trading controls (start/pause/stop)
  - _Requirements: 20.1, 20.3, 20.4_

### Phase 6: 通知和报告系统 (Notification and Reporting System)

- [x] 43. 实现通知服务 (Implement Notification Service)
  - 创建NotificationService类 / Create NotificationService class
  - 实现邮件通知功能 / Implement email notification functionality
  - 实现短信通知功能 / Implement SMS notification functionality
  - 实现系统通知功能 / Implement system notification functionality
  - 实现风险预警通知 / Implement risk alert notifications
  - _Requirements: 21.1, 21.2, 21.3, 21.4, 21.5_

- [ ]* 43.1 编写通知服务的单元测试 (Write unit tests for notification service)
  - 测试邮件发送 / Test email sending
  - 测试短信发送 / Test SMS sending
  - 测试通知格式 / Test notification formatting
  - _Requirements: 21.5_

- [x] 44. 实现报告调度器 (Implement Report Scheduler)
  - 创建ReportScheduler类 / Create ReportScheduler class
  - 实现每日报告生成 / Implement daily report generation
  - 实现每周报告生成 / Implement weekly report generation
  - 实现每月报告生成 / Implement monthly report generation
  - 实现风险预警报告 / Implement risk alert reports
  - 集成NotificationService / Integrate NotificationService
  - _Requirements: 21.1, 21.2, 21.3, 21.4, 21.5_

- [ ]* 44.1 编写报告调度的单元测试 (Write unit tests for report scheduling)
  - 测试定时任务触发 / Test scheduled task triggering
  - 测试报告生成 / Test report generation
  - 测试通知发送 / Test notification sending
  - _Requirements: 21.1, 21.2, 21.3_

- [x] 45. 增强报告生成器支持新报告类型 (Enhance Report Generator for new report types)
  - 扩展ReportGenerator类 / Extend ReportGenerator class
  - 实现模拟交易报告生成 / Implement simulation trading report generation
  - 实现实盘交易报告生成 / Implement live trading report generation
  - 实现对比报告生成 / Implement comparison report generation
  - 添加中英双语报告支持 / Add bilingual report support
  - _Requirements: 19.4, 20.5, 21.1, 21.2, 21.3_

### Phase 7: 引导式工作流程 (Guided Workflow)

- [x] 46. 实现引导式工作流程 (Implement Guided Workflow)
  - 创建GuidedWorkflow类 / Create GuidedWorkflow class
  - 实现10步完整流程 / Implement 10-step complete workflow
  - 实现进度保存和恢复 / Implement progress save and resume
  - 实现步骤验证 / Implement step validation
  - 实现返回修改功能 / Implement go-back-to-modify functionality
  - 生成配置总结 / Generate configuration summary
  - _Requirements: 22.1, 22.2, 22.3, 22.4, 22.5_

- [ ]* 46.1 编写工作流程的单元测试 (Write unit tests for workflow)
  - 测试步骤流转 / Test step transitions
  - 测试进度保存 / Test progress saving
  - 测试验证逻辑 / Test validation logic
  - 测试返回功能 / Test go-back functionality
  - _Requirements: 22.1, 22.2, 22.4_

- [ ]* 46.2 编写工作流程的集成测试 (Write integration tests for workflow)
  - 测试完整流程执行 / Test complete workflow execution
  - 测试中断恢复 / Test interruption and resume
  - 测试错误处理 / Test error handling
  - _Requirements: 22.1, 22.2, 22.3, 22.4_

- [x] 47. 集成引导式工作流程到CLI (Integrate guided workflow into CLI)
  - 在MainCLI中添加引导模式入口 / Add guided mode entry to MainCLI
  - 实现友好的中文提示 / Implement friendly Chinese prompts
  - 实现实时输入验证 / Implement real-time input validation
  - 实现进度可视化 / Implement progress visualization
  - 添加帮助和说明 / Add help and instructions
  - _Requirements: 22.1, 22.2, 22.3, 22.5_

### Phase 8: 文档和示例 (Documentation and Examples)

- [x] 48. 编写引导式工作流程文档 (Write guided workflow documentation)
  - 编写docs/guided_workflow.md / Write docs/guided_workflow.md
  - 详细说明10步流程 / Detail the 10-step process
  - 添加截图和示例 / Add screenshots and examples
  - 提供常见问题解答 / Provide FAQ
  - _Requirements: 13.1, 13.2, 13.3, 22.1_

- [x] 49. 编写模拟交易指南 (Write simulation trading guide)
  - 编写docs/simulation_guide.md / Write docs/simulation_guide.md
  - 说明模拟交易流程 / Explain simulation trading process
  - 提供参数调整建议 / Provide parameter adjustment suggestions
  - 添加结果解读说明 / Add result interpretation instructions
  - _Requirements: 13.2, 13.3, 19.1, 19.4_

- [x] 50. 编写实盘交易指南 (Write live trading guide)
  - 编写docs/live_trading_guide.md / Write docs/live_trading_guide.md
  - 说明券商配置步骤 / Explain broker configuration steps
  - 详细说明风险控制机制 / Detail risk control mechanisms
  - 提供安全使用建议 / Provide safe usage recommendations
  - 添加故障排除指南 / Add troubleshooting guide
  - _Requirements: 13.2, 13.3, 20.1, 20.2_

- [x] 51. 创建完整示例 (Create complete examples)
  - 创建examples/guided_workflow_demo.py / Create examples/guided_workflow_demo.py
  - 创建examples/simulation_demo.py / Create examples/simulation_demo.py
  - 创建examples/live_trading_demo.py / Create examples/live_trading_demo.py
  - 添加详细注释和说明 / Add detailed comments and instructions
  - _Requirements: 13.5, 22.1_

### Phase 9: 配置和数据 (Configuration and Data)

- [x] 52. 创建市场配置文件 (Create market configuration files)
  - 创建config/markets.yaml / Create config/markets.yaml
  - 配置国内市场（A股）/ Configure domestic market (A-shares)
  - 配置国外市场（美股、港股）/ Configure international markets (US, HK stocks)
  - 配置资产类型 / Configure asset types
  - _Requirements: 16.1, 16.2_

- [x] 53. 创建风险阈值配置 (Create risk threshold configuration)
  - 创建config/risk_thresholds.yaml / Create config/risk_thresholds.yaml
  - 配置不同风险偏好的阈值 / Configure thresholds for different risk preferences
  - 配置预警级别 / Configure alert levels
  - _Requirements: 18.2, 20.2, 21.4_

- [x] 54. 创建通知配置 (Create notification configuration)
  - 创建config/notification_config.yaml / Create config/notification_config.yaml
  - 配置邮件服务器 / Configure email server
  - 配置短信服务 / Configure SMS service
  - _Requirements: 21.5_

### Phase 10: 最终集成和测试 (Final Integration and Testing)

- [ ] 55. 端到端集成测试 (End-to-end integration testing)
  - 测试完整引导式工作流程 / Test complete guided workflow
  - 测试市场选择到模拟交易 / Test market selection to simulation trading
  - 测试模拟交易到实盘交易 / Test simulation trading to live trading
  - 测试报告生成和通知 / Test report generation and notifications
  - _Requirements: All new requirements_

- [ ]* 55.1 编写端到端测试套件 (Write end-to-end test suite)
  - 测试用户完整使用场景 / Test complete user scenarios
  - 测试异常情况处理 / Test exception handling
  - 测试性能和稳定性 / Test performance and stability
  - _Requirements: All new requirements_

- [ ] 56. 性能优化 (Performance optimization)
  - 优化历史数据分析性能 / Optimize historical data analysis performance
  - 优化策略优化算法 / Optimize strategy optimization algorithm
  - 优化实时数据处理 / Optimize real-time data processing
  - 添加缓存机制 / Add caching mechanisms
  - _Requirements: 17.1, 18.3, 20.3_

- [ ] 57. 用户体验优化 (User experience optimization)
  - 优化中文提示信息 / Optimize Chinese prompts
  - 添加更多帮助信息 / Add more help information
  - 优化进度显示 / Optimize progress display
  - 添加操作确认 / Add operation confirmations
  - _Requirements: 12.1, 12.4, 22.3_

- [ ] 58. Final Checkpoint - 新功能测试通过 (Final Checkpoint - New features tests pass)
  - 确保所有新功能测试通过 / Ensure all new feature tests pass
  - 确保向后兼容性 / Ensure backward compatibility
  - 生成完整测试报告 / Generate complete test report
  - 如有问题请询问用户 / Ask user if there are any issues
