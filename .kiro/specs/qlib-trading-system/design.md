# Design Document (设计文档)

## Overview (概述)

本系统是一个基于qlib的智能量化交易平台，旨在为新手和专业用户提供从市场选择到实盘交易的完整解决方案。系统采用模块化设计，通过交互式引导流程，帮助用户轻松完成投资决策、模型训练、回测验证、模拟交易和实盘运营。

**This is an intelligent quantitative trading platform based on qlib, designed to provide novice and professional users with a complete solution from market selection to live trading. The system adopts a modular design and helps users easily complete investment decisions, model training, backtest verification, simulation trading, and live operations through an interactive guided process.**

### 核心使用流程 (Core User Workflow)

1. **市场和品类选择 (Market and Asset Selection)** - 用户选择投资市场（国内/国外）和品类（股票/基金/其他）
   User selects investment market (domestic/international) and asset type (stocks/funds/others)

2. **智能推荐 (Intelligent Recommendation)** - 系统基于近3年市场表现推荐优质标的
   System recommends quality assets based on 3-year market performance

3. **目标设定 (Target Setting)** - 用户设定期望收益率和投资周期
   User sets target return rate and investment period

4. **自动训练 (Automatic Training)** - 系统根据用户选择自动训练预测模型
   System automatically trains prediction models based on user selections

5. **历史回测 (Historical Backtest)** - 使用历史数据验证模型表现
   Validates model performance using historical data

6. **模拟交易 (Simulation Trading)** - 在指定周期内进行模拟交易测试
   Conducts simulation trading tests within specified period

7. **报告生成 (Report Generation)** - 生成详细的测试报告供用户评估
   Generates detailed test reports for user evaluation

8. **实盘交易 (Live Trading)** - 用户满意后启动实际交易
   Starts actual trading after user satisfaction

9. **持续监控 (Continuous Monitoring)** - 定期生成收益报告和风险分析
   Periodically generates performance reports and risk analysis

### 核心特性 (Core Features)

- **智能引导式交互界面 (Intelligent Guided Interface)** - 无需编程，通过问答完成所有配置
  No programming required, complete all configurations through Q&A

- **多市场多品类支持 (Multi-market Multi-asset Support)** - 支持国内外股票、基金等多种投资品类
  Supports domestic and international stocks, funds, and other investment categories

- **智能推荐系统 (Intelligent Recommendation System)** - 基于历史表现自动推荐优质标的
  Automatically recommends quality assets based on historical performance

- **目标导向优化 (Target-oriented Optimization)** - 根据用户期望收益率优化策略参数
  Optimizes strategy parameters based on user's target returns

- **完整的测试流程 (Complete Testing Process)** - 历史回测 + 模拟交易双重验证
  Historical backtesting + simulation trading dual verification

- **实盘交易支持 (Live Trading Support)** - 无缝对接实盘交易接口
  Seamlessly integrates with live trading APIs

- **自动化报告 (Automated Reporting)** - 定期生成收益分析和风险预警
  Periodically generates performance analysis and risk alerts

- **MLflow实验追踪 (MLflow Experiment Tracking)** - 完整记录所有训练和交易过程
  Completely records all training and trading processes

- **中文友好界面 (Chinese-friendly Interface)** - 全中文提示和文档
  Full Chinese prompts and documentation

## Architecture

系统采用分层架构设计，新增智能推荐、模拟交易和实盘交易模块：

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLI Interface Layer                           │
│  (智能引导流程、交互式菜单、进度显示、帮助系统)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Guided       │  │ Interactive  │  │ Progress     │          │
│  │ Workflow     │  │ Prompt       │  │ Display      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────────┐
│                   Application Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Market       │  │ Performance  │  │ Strategy     │  [NEW]   │
│  │ Selector     │  │ Analyzer     │  │ Optimizer    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Training     │  │ Backtest     │  │ Simulation   │  [NEW]   │
│  │ Manager      │  │ Manager      │  │ Engine       │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Live Trading │  │ Report       │  │ Signal       │  [NEW]   │
│  │ Manager      │  │ Scheduler    │  │ Generator    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Model        │  │ Visualization│  │ Report       │          │
│  │ Registry     │  │ Manager      │  │ Generator    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────────┐
│                     Core Layer                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Data         │  │ Model        │  │ Config       │          │
│  │ Manager      │  │ Factory      │  │ Manager      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │ Portfolio    │  │ Risk         │                   [NEW]    │
│  │ Manager      │  │ Manager      │                            │
│  └──────────────┘  └──────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Qlib         │  │ MLflow       │  │ Logger       │          │
│  │ Framework    │  │ Tracking     │  │ System       │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │ Trading      │  │ Notification │                   [NEW]    │
│  │ API Adapter  │  │ Service      │                            │
│  └──────────────┘  └──────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

### 架构说明 (Architecture Description)

1. **CLI Interface Layer (CLI界面层)**: 提供智能引导式用户交互界面
   **Provides intelligent guided user interaction interface**
   - **GuidedWorkflow (引导式工作流)**: 引导用户完成完整投资流程
     Guides users through complete investment process
   - **InteractivePrompt (交互式提示)**: 收集用户输入和选择
     Collects user inputs and selections
   - **ProgressDisplay (进度显示)**: 显示训练、回测、模拟交易进度
     Displays training, backtesting, and simulation trading progress

2. **Application Layer (应用层)**: 实现业务逻辑
   **Implements business logic**
   - **MarketSelector (市场选择器)** [NEW]: 市场和品类选择
     Market and asset type selection
   - **PerformanceAnalyzer (表现分析器)** [NEW]: 历史表现分析和智能推荐
     Historical performance analysis and intelligent recommendations
   - **StrategyOptimizer (策略优化器)** [NEW]: 基于目标收益率优化策略
     Optimizes strategy based on target returns
   - **TrainingManager (训练管理器)**: 模型训练管理
     Model training management
   - **BacktestManager (回测管理器)**: 历史回测
     Historical backtesting
   - **SimulationEngine (模拟引擎)** [NEW]: 模拟交易引擎
     Simulation trading engine
   - **LiveTradingManager (实盘交易管理器)** [NEW]: 实盘交易管理
     Live trading management
   - **ReportScheduler (报告调度器)** [NEW]: 定期报告生成
     Periodic report generation
   - **SignalGenerator (信号生成器)**: 交易信号生成
     Trading signal generation
   - **ModelRegistry (模型注册表)**: 模型版本管理
     Model version management
   - **VisualizationManager (可视化管理器)**: 可视化图表生成
     Visualization chart generation
   - **ReportGenerator (报告生成器)**: 报告生成
     Report generation

3. **Core Layer (核心层)**: 提供核心服务
   **Provides core services**
   - **DataManager (数据管理器)**: 数据管理和验证
     Data management and validation
   - **ModelFactory (模型工厂)**: 模型创建工厂
     Model creation factory
   - **ConfigManager (配置管理器)**: 配置管理
     Configuration management
   - **PortfolioManager (组合管理器)** [NEW]: 投资组合管理
     Portfolio management
   - **RiskManager (风险管理器)** [NEW]: 风险控制和监控
     Risk control and monitoring

4. **Infrastructure Layer (基础设施层)**: 封装第三方框架和服务
   **Encapsulates third-party frameworks and services**
   - **QlibFramework (Qlib框架)**: qlib数据和模型框架
     qlib data and model framework
   - **MLflowTracking (MLflow追踪)**: 实验追踪
     Experiment tracking
   - **LoggerSystem (日志系统)**: 日志系统
     Logging system
   - **TradingAPIAdapter (交易API适配器)** [NEW]: 交易接口适配器
     Trading API adapter
   - **NotificationService (通知服务)** [NEW]: 通知服务（邮件/短信）
     Notification service (email/SMS)
   - **TrainingManager**: 模型训练管理
   - **BacktestManager**: 历史回测
   - **SimulationEngine** [NEW]: 模拟交易引擎
   - **LiveTradingManager** [NEW]: 实盘交易管理
   - **ReportScheduler** [NEW]: 定期报告生成
   - **SignalGenerator**: 交易信号生成
   - **ModelRegistry**: 模型版本管理
   - **VisualizationManager**: 可视化图表生成
   - **ReportGenerator**: 报告生成

3. **Core Layer**: 提供核心服务
   - **DataManager**: 数据管理和验证
   - **ModelFactory**: 模型创建工厂
   - **ConfigManager**: 配置管理
   - **PortfolioManager** [NEW]: 投资组合管理
   - **RiskManager** [NEW]: 风险控制和监控

4. **Infrastructure Layer**: 封装第三方框架和服务
   - **QlibFramework**: qlib数据和模型框架
   - **MLflowTracking**: 实验追踪
   - **LoggerSystem**: 日志系统
   - **TradingAPIAdapter** [NEW]: 交易接口适配器
   - **NotificationService** [NEW]: 通知服务（邮件/短信）

## Components and Interfaces

### 1. CLI Interface Layer

#### MainCLI
主命令行界面控制器

**职责**:
- 显示主菜单
- 路由用户选择到对应功能
- 处理全局命令（帮助、退出等）

**接口**:
```python
class MainCLI:
    def run(self) -> None
    def show_menu(self) -> None
    def handle_choice(self, choice: str) -> None
```

#### InteractivePrompt
交互式参数收集器

**职责**:
- 收集用户输入
- 验证输入有效性
- 提供默认值和提示

**接口**:
```python
class InteractivePrompt:
    def ask_text(self, prompt: str, default: str = None) -> str
    def ask_choice(self, prompt: str, choices: List[str]) -> str
    def ask_number(self, prompt: str, min_val: float, max_val: float, default: float) -> float
    def ask_date(self, prompt: str, default: str = None) -> str
    def confirm(self, prompt: str, default: bool = True) -> bool
```

### 2. Application Layer

#### MarketSelector [NEW]
市场和品类选择器

**职责**:
- 提供市场选择（国内/国外）
- 提供品类选择（股票/基金/其他）
- 管理不同市场的配置

**接口**:
```python
class MarketSelector:
    def get_available_markets(self) -> List[Market]
    def get_asset_types(self, market: Market) -> List[AssetType]
    def select_market_and_type(self, market: str, asset_type: str) -> MarketConfig
    def get_market_info(self, market: str) -> MarketInfo
```

#### PerformanceAnalyzer [NEW]
历史表现分析器

**职责**:
- 分析近期市场表现
- 推荐优质标的
- 计算历史收益指标

**接口**:
```python
class PerformanceAnalyzer:
    def analyze_historical_performance(
        self, 
        market: str, 
        asset_type: str, 
        lookback_years: int = 3
    ) -> PerformanceReport
    def recommend_top_performers(
        self, 
        market: str, 
        asset_type: str, 
        top_n: int = 10,
        criteria: str = "sharpe_ratio"
    ) -> List[AssetRecommendation]
    def get_asset_metrics(self, asset_code: str, start_date: str, end_date: str) -> AssetMetrics
```

#### StrategyOptimizer [NEW]
策略优化器

**职责**:
- 根据目标收益率优化策略参数
- 平衡收益和风险
- 生成优化建议

**接口**:
```python
class StrategyOptimizer:
    def optimize_for_target_return(
        self,
        target_return: float,
        assets: List[str],
        constraints: OptimizationConstraints
    ) -> OptimizedStrategy
    def suggest_parameters(
        self,
        target_return: float,
        risk_tolerance: str
    ) -> StrategyParams
    def backtest_optimized_strategy(
        self,
        strategy: OptimizedStrategy,
        test_period: DateRange
    ) -> BacktestResult
```

#### TrainingManager
模型训练管理器

**职责**:
- 协调训练流程
- 管理训练配置
- 记录训练指标

**接口**:
```python
class TrainingManager:
    def train_model(self, config: TrainingConfig) -> TrainingResult
    def train_from_template(self, template_name: str, custom_params: Dict = None) -> TrainingResult
    def train_for_target_return(self, target_return: float, assets: List[str]) -> TrainingResult
    def list_templates(self) -> List[ModelTemplate]
```

#### BacktestManager
回测管理器

**职责**:
- 执行回测流程
- 计算性能指标
- 生成回测报告

**接口**:
```python
class BacktestManager:
    def run_backtest(self, model_id: str, start_date: str, end_date: str, config: BacktestConfig) -> BacktestResult
    def calculate_metrics(self, returns: pd.Series, benchmark: pd.Series) -> Dict[str, float]
```

#### SignalGenerator
交易信号生成器

**职责**:
- 生成交易信号
- 应用风险控制
- 解释信号原因

**接口**:
```python
class SignalGenerator:
    def generate_signals(self, model_id: str, date: str, portfolio: Portfolio) -> List[Signal]
    def explain_signal(self, signal: Signal) -> SignalExplanation
```

#### ModelRegistry
模型注册表

**职责**:
- 注册和管理模型
- 版本控制
- 模型元数据管理

**接口**:
```python
class ModelRegistry:
    def register_model(self, model: Model, metadata: ModelMetadata) -> str
    def get_model(self, model_id: str) -> Model
    def list_models(self, filter: ModelFilter = None) -> List[ModelInfo]
    def set_production_model(self, model_id: str) -> None
```

#### VisualizationManager
可视化管理器

**职责**:
- 生成图表
- 创建可视化报告
- 导出图片

**接口**:
```python
class VisualizationManager:
    def plot_cumulative_returns(self, returns: pd.Series, benchmark: pd.Series, save_path: str) -> None
    def plot_training_curve(self, metrics: Dict[str, List[float]], save_path: str) -> None
    def plot_position_distribution(self, portfolio: Portfolio, save_path: str) -> None
```

#### SimulationEngine [NEW]
模拟交易引擎

**职责**:
- 执行模拟交易
- 跟踪模拟持仓
- 计算模拟收益

**接口**:
```python
class SimulationEngine:
    def start_simulation(
        self,
        model_id: str,
        initial_capital: float,
        simulation_days: int,
        start_date: str
    ) -> SimulationSession
    def execute_simulation_step(self, session: SimulationSession, date: str) -> SimulationStepResult
    def get_simulation_status(self, session_id: str) -> SimulationStatus
    def generate_simulation_report(self, session_id: str) -> SimulationReport
```

#### LiveTradingManager [NEW]
实盘交易管理器

**职责**:
- 管理实盘交易
- 执行买卖订单
- 监控持仓和风险

**接口**:
```python
class LiveTradingManager:
    def start_live_trading(
        self,
        model_id: str,
        initial_capital: float,
        trading_config: LiveTradingConfig
    ) -> TradingSession
    def execute_trade(self, session_id: str, signal: Signal) -> TradeResult
    def get_current_positions(self, session_id: str) -> Portfolio
    def stop_trading(self, session_id: str) -> TradingSessionSummary
    def get_trading_status(self, session_id: str) -> TradingStatus
```

#### ReportScheduler [NEW]
定期报告生成器

**职责**:
- 定期生成收益报告
- 发送风险预警
- 生成分析报告

**接口**:
```python
class ReportScheduler:
    def schedule_daily_report(self, session_id: str, recipients: List[str]) -> None
    def schedule_weekly_report(self, session_id: str, recipients: List[str]) -> None
    def generate_performance_report(self, session_id: str, period: str) -> PerformanceReport
    def generate_risk_alert(self, session_id: str) -> Optional[RiskAlert]
    def send_report(self, report: Report, recipients: List[str]) -> None
```

#### ReportGenerator
报告生成器

**职责**:
- 生成文本报告
- 汇总性能指标
- 创建HTML报告

**接口**:
```python
class ReportGenerator:
    def generate_training_report(self, result: TrainingResult) -> str
    def generate_backtest_report(self, result: BacktestResult) -> str
    def generate_simulation_report(self, result: SimulationReport) -> str
    def generate_live_trading_report(self, session: TradingSession) -> str
    def generate_html_report(self, result: BacktestResult, output_path: str) -> None
    def generate_comparison_report(self, results: List[BacktestResult]) -> str
```

### 3. Core Layer

#### DataManager
数据管理器

**职责**:
- 初始化qlib数据
- 下载和更新数据
- 验证数据完整性
- 支持多市场数据管理

**接口**:
```python
class DataManager:
    def initialize(self, data_path: str, region: str) -> None
    def download_data(self, region: str, target_dir: str, interval: str = "day") -> None
    def validate_data(self, start_date: str, end_date: str) -> ValidationResult
    def get_data_info(self) -> DataInfo
    def get_market_data(self, market: str, asset_type: str, symbols: List[str]) -> pd.DataFrame
    def get_available_symbols(self, market: str, asset_type: str) -> List[str]
```

#### PortfolioManager [NEW]
投资组合管理器

**职责**:
- 管理持仓信息
- 计算组合价值
- 跟踪交易历史

**接口**:
```python
class PortfolioManager:
    def create_portfolio(self, initial_capital: float) -> Portfolio
    def update_position(self, portfolio_id: str, symbol: str, quantity: float, price: float) -> None
    def get_current_value(self, portfolio_id: str) -> float
    def get_positions(self, portfolio_id: str) -> Dict[str, Position]
    def get_trade_history(self, portfolio_id: str) -> List[Trade]
    def calculate_returns(self, portfolio_id: str, start_date: str, end_date: str) -> pd.Series
```

#### RiskManager [NEW]
风险管理器

**职责**:
- 监控风险指标
- 执行风险控制
- 生成风险预警

**接口**:
```python
class RiskManager:
    def check_position_risk(self, portfolio: Portfolio, new_trade: Trade) -> RiskCheckResult
    def calculate_var(self, portfolio: Portfolio, confidence: float = 0.95) -> float
    def calculate_max_drawdown(self, returns: pd.Series) -> float
    def check_concentration_risk(self, portfolio: Portfolio) -> ConcentrationRisk
    def generate_risk_alert(self, portfolio: Portfolio, thresholds: RiskThresholds) -> Optional[RiskAlert]
    def suggest_risk_mitigation(self, risk_alert: RiskAlert) -> List[str]
```

#### ModelFactory
模型工厂

**职责**:
- 创建模型实例
- 管理模型模板
- 配置模型参数

**接口**:
```python
class ModelFactory:
    def create_model(self, model_type: str, params: Dict) -> Model
    def get_template(self, template_name: str) -> ModelTemplate
    def list_available_models(self) -> List[str]
```

#### ConfigManager
配置管理器

**职责**:
- 加载和保存配置
- 验证配置
- 提供默认配置

**接口**:
```python
class ConfigManager:
    def load_config(self, config_path: str) -> Config
    def save_config(self, config: Config, config_path: str) -> None
    def get_default_config(self) -> Config
    def validate_config(self, config: Config) -> List[str]
```

### 4. Infrastructure Layer

#### QlibWrapper
Qlib框架封装

**职责**:
- 初始化qlib
- 提供统一的qlib接口
- 处理qlib异常

**接口**:
```python
class QlibWrapper:
    def init(self, provider_uri: str, region: str, exp_manager_config: Dict) -> None
    def get_data(self, instruments: str, fields: List[str], start_time: str, end_time: str) -> pd.DataFrame
    def is_initialized(self) -> bool
```

#### MLflowTracker
MLflow追踪器

**职责**:
- 记录实验
- 追踪指标
- 管理模型版本

**接口**:
```python
class MLflowTracker:
    def start_run(self, experiment_name: str, run_name: str) -> str
    def log_params(self, params: Dict) -> None
    def log_metrics(self, metrics: Dict, step: int = None) -> None
    def log_model(self, model: Model, artifact_path: str) -> None
    def end_run(self) -> None
```

#### LoggerSystem
日志系统

**职责**:
- 配置日志
- 记录日志
- 管理日志文件

**接口**:
```python
class LoggerSystem:
    def setup(self, log_dir: str, log_level: str) -> None
    def get_logger(self, name: str) -> Logger
    def rotate_logs(self) -> None
```

#### TradingAPIAdapter [NEW]
交易接口适配器

**职责**:
- 对接券商交易接口
- 执行买卖订单
- 查询账户信息

**接口**:
```python
class TradingAPIAdapter:
    def connect(self, broker: str, credentials: Dict) -> None
    def place_order(self, symbol: str, quantity: float, order_type: str, price: Optional[float]) -> OrderResult
    def cancel_order(self, order_id: str) -> bool
    def get_account_info(self) -> AccountInfo
    def get_positions(self) -> List[Position]
    def get_order_status(self, order_id: str) -> OrderStatus
    def disconnect(self) -> None
```

#### NotificationService [NEW]
通知服务

**职责**:
- 发送邮件通知
- 发送短信通知
- 发送系统通知

**接口**:
```python
class NotificationService:
    def setup(self, config: NotificationConfig) -> None
    def send_email(self, recipients: List[str], subject: str, body: str, attachments: List[str] = None) -> bool
    def send_sms(self, phone_numbers: List[str], message: str) -> bool
    def send_system_notification(self, title: str, message: str, level: str) -> None
    def send_risk_alert(self, alert: RiskAlert, recipients: List[str]) -> bool
```

## Data Models

### Market and Asset Models [NEW]

#### Market
```python
@dataclass
class Market:
    code: str  # "CN", "US", etc.
    name: str  # "中国市场", "美国市场"
    region: str
    timezone: str
    trading_hours: Dict[str, str]
```

#### AssetType
```python
@dataclass
class AssetType:
    code: str  # "stock", "fund", "etf", etc.
    name: str  # "股票", "基金", "ETF"
    description: str
```

#### MarketConfig
```python
@dataclass
class MarketConfig:
    market: Market
    asset_type: AssetType
    data_source: str
    instruments_pool: str
```

#### AssetRecommendation
```python
@dataclass
class AssetRecommendation:
    symbol: str
    name: str
    asset_type: str
    performance_score: float
    sharpe_ratio: float
    annual_return: float
    max_drawdown: float
    recommendation_reason: str
```

#### AssetMetrics
```python
@dataclass
class AssetMetrics:
    symbol: str
    period_start: str
    period_end: str
    total_return: float
    annual_return: float
    volatility: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
```

### Strategy and Optimization Models [NEW]

#### OptimizationConstraints
```python
@dataclass
class OptimizationConstraints:
    max_position_size: float
    max_sector_exposure: float
    min_diversification: int
    max_turnover: float
    risk_tolerance: str  # "conservative", "moderate", "aggressive"
```

#### OptimizedStrategy
```python
@dataclass
class OptimizedStrategy:
    strategy_id: str
    target_return: float
    expected_return: float
    expected_risk: float
    asset_weights: Dict[str, float]
    rebalance_frequency: str
    parameters: Dict[str, Any]
```

#### StrategyParams
```python
@dataclass
class StrategyParams:
    model_type: str
    features: List[str]
    lookback_period: int
    rebalance_frequency: str
    position_sizing: str
    risk_params: Dict[str, Any]
```

### Training Models

#### TrainingConfig
```python
@dataclass
class TrainingConfig:
    model_type: str
    dataset_config: DatasetConfig
    model_params: Dict[str, Any]
    training_params: Dict[str, Any]
    experiment_name: str
    target_return: Optional[float] = None  # NEW
    optimization_objective: str = "sharpe_ratio"  # NEW
```

### DatasetConfig
```python
@dataclass
class DatasetConfig:
    instruments: str  # e.g., "csi300"
    start_time: str
    end_time: str
    features: List[str]
    label: str
```

### TrainingResult
```python
@dataclass
class TrainingResult:
    model_id: str
    metrics: Dict[str, float]
    training_time: float
    model_path: str
    experiment_id: str
```

### BacktestConfig
```python
@dataclass
class BacktestConfig:
    strategy_config: Dict[str, Any]
    executor_config: Dict[str, Any]
    benchmark: str
```

### BacktestResult
```python
@dataclass
class BacktestResult:
    returns: pd.Series
    positions: pd.DataFrame
    metrics: Dict[str, float]
    trades: List[Trade]
```

### Signal
```python
@dataclass
class Signal:
    stock_code: str
    action: str  # "buy", "sell", "hold"
    score: float
    confidence: float
    timestamp: str
```

### SignalExplanation
```python
@dataclass
class SignalExplanation:
    signal: Signal
    main_factors: List[Tuple[str, float]]  # (factor_name, contribution)
    risk_level: str
    description: str
```

### ModelTemplate
```python
@dataclass
class ModelTemplate:
    name: str
    model_type: str
    description: str
    use_case: str
    default_params: Dict[str, Any]
    expected_performance: Dict[str, float]
```

### Portfolio
```python
@dataclass
class Portfolio:
    positions: Dict[str, float]  # stock_code -> quantity
    cash: float
    total_value: float
```

### ModelMetadata
```python
@dataclass
class ModelMetadata:
    model_name: str
    version: str
    training_date: str
    performance_metrics: Dict[str, float]
    dataset_info: DatasetConfig
    hyperparameters: Dict[str, Any]
```

### Simulation and Trading Models [NEW]

#### SimulationSession
```python
@dataclass
class SimulationSession:
    session_id: str
    model_id: str
    initial_capital: float
    simulation_days: int
    start_date: str
    end_date: str
    status: str  # "running", "completed", "failed"
    current_portfolio: Portfolio
```

#### SimulationStepResult
```python
@dataclass
class SimulationStepResult:
    date: str
    signals: List[Signal]
    trades_executed: List[Trade]
    portfolio_value: float
    daily_return: float
    cash_balance: float
```

#### SimulationReport
```python
@dataclass
class SimulationReport:
    session_id: str
    total_return: float
    annual_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    total_trades: int
    profitable_trades: int
    final_portfolio_value: float
    daily_returns: pd.Series
    trade_history: List[Trade]
```

#### LiveTradingConfig
```python
@dataclass
class LiveTradingConfig:
    broker: str
    credentials: Dict[str, str]
    max_position_size: float
    max_daily_trades: int
    stop_loss_pct: float
    take_profit_pct: float
    trading_hours: Dict[str, str]
```

#### TradingSession
```python
@dataclass
class TradingSession:
    session_id: str
    model_id: str
    start_date: str
    initial_capital: float
    current_capital: float
    status: str  # "active", "paused", "stopped"
    portfolio: Portfolio
    total_return: float
    config: LiveTradingConfig
```

#### TradeResult
```python
@dataclass
class TradeResult:
    trade_id: str
    order_id: str
    symbol: str
    action: str  # "buy", "sell"
    quantity: float
    price: float
    timestamp: str
    status: str  # "filled", "partial", "rejected"
    commission: float
```

#### TradingStatus
```python
@dataclass
class TradingStatus:
    session_id: str
    is_active: bool
    current_value: float
    total_return: float
    today_return: float
    positions_count: int
    cash_balance: float
    last_update: str
```

#### Position
```python
@dataclass
class Position:
    symbol: str
    quantity: float
    avg_cost: float
    current_price: float
    market_value: float
    unrealized_pnl: float
    unrealized_pnl_pct: float
```

#### Trade
```python
@dataclass
class Trade:
    trade_id: str
    timestamp: str
    symbol: str
    action: str  # "buy", "sell"
    quantity: float
    price: float
    commission: float
    total_cost: float
```

### Risk Management Models [NEW]

#### RiskCheckResult
```python
@dataclass
class RiskCheckResult:
    passed: bool
    risk_score: float
    warnings: List[str]
    violations: List[str]
    suggested_adjustments: Dict[str, Any]
```

#### ConcentrationRisk
```python
@dataclass
class ConcentrationRisk:
    max_position_pct: float
    top_5_concentration: float
    sector_concentration: Dict[str, float]
    risk_level: str  # "low", "medium", "high"
```

#### RiskAlert
```python
@dataclass
class RiskAlert:
    alert_id: str
    timestamp: str
    severity: str  # "info", "warning", "critical"
    alert_type: str  # "drawdown", "concentration", "volatility"
    message: str
    current_value: float
    threshold_value: float
    affected_positions: List[str]
    recommended_actions: List[str]
```

#### RiskThresholds
```python
@dataclass
class RiskThresholds:
    max_drawdown_pct: float
    max_position_pct: float
    max_sector_pct: float
    max_daily_loss_pct: float
    min_sharpe_ratio: float
```

### Report Models [NEW]

#### PerformanceReport
```python
@dataclass
class PerformanceReport:
    report_id: str
    period_start: str
    period_end: str
    total_return: float
    annual_return: float
    sharpe_ratio: float
    max_drawdown: float
    volatility: float
    win_rate: float
    profit_factor: float
    best_trade: Trade
    worst_trade: Trade
    monthly_returns: Dict[str, float]
```

#### Report
```python
@dataclass
class Report:
    report_id: str
    report_type: str  # "daily", "weekly", "monthly", "simulation", "live"
    generated_at: str
    title: str
    summary: str
    content: str
    charts: List[str]  # paths to chart files
    attachments: List[str]
```

### Notification Models [NEW]

#### NotificationConfig
```python
@dataclass
class NotificationConfig:
    email_enabled: bool
    email_smtp_server: str
    email_smtp_port: int
    email_username: str
    email_password: str
    sms_enabled: bool
    sms_api_key: str
    sms_api_url: str
```

#### AccountInfo
```python
@dataclass
class AccountInfo:
    account_id: str
    broker: str
    total_value: float
    cash_balance: float
    buying_power: float
    positions_value: float
    unrealized_pnl: float
```

#### OrderResult
```python
@dataclass
class OrderResult:
    order_id: str
    symbol: str
    quantity: float
    order_type: str
    status: str
    filled_quantity: float
    avg_fill_price: float
    timestamp: str
```

#### OrderStatus
```python
@dataclass
class OrderStatus:
    order_id: str
    status: str  # "pending", "filled", "partial", "cancelled", "rejected"
    filled_quantity: float
    remaining_quantity: float
    avg_fill_price: float
    last_update: str
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Qlib initialization succeeds for valid configurations
*For any* valid data path and region configuration, initializing qlib should succeed and allow data access
**Validates: Requirements 1.1**

### Property 2: Data validation returns time range after initialization
*For any* successfully initialized qlib environment, querying data info should return a valid time range
**Validates: Requirements 1.3**

### Property 3: MLflow initialization when configured
*For any* configuration that includes MLflow settings, system initialization should create an MLflow experiment
**Validates: Requirements 1.4**

### Property 4: Training loads dataset for valid config
*For any* valid training configuration, starting training should successfully load the specified dataset
**Validates: Requirements 2.1**

### Property 5: Model training completes for supported types
*For any* supported model type with valid parameters, training should complete and produce a model
**Validates: Requirements 2.2**

### Property 6: Training metrics logged to MLflow
*For any* training process, metrics should be logged to MLflow during training
**Validates: Requirements 2.3, 3.2**

### Property 7: Model saved after training
*For any* successfully completed training, a model file and metadata should be saved
**Validates: Requirements 2.4**

### Property 8: Multiple models trained sequentially
*For any* configuration specifying multiple models, all models should be trained and results compared
**Validates: Requirements 2.5**

### Property 9: MLflow run created for each training
*For any* training start, a new MLflow run should be created with a unique ID
**Validates: Requirements 3.1**

### Property 10: Hyperparameters logged to MLflow
*For any* training process, all hyperparameters should be logged to MLflow
**Validates: Requirements 3.3**

### Property 11: Final metrics recorded after training
*For any* completed training, final performance metrics and training time should be recorded
**Validates: Requirements 3.4**

### Property 12: Backtest generates signals from model
*For any* valid model and time period, backtest should generate prediction signals
**Validates: Requirements 4.1**

### Property 13: Backtest executes with signals
*For any* sequence of signals, backtest engine should simulate trades
**Validates: Requirements 4.2**

### Property 14: Backtest calculates required metrics
*For any* completed backtest, all required metrics (returns, Sharpe ratio, max drawdown) should be calculated
**Validates: Requirements 4.3**

### Property 15: Backtest saves report and trades
*For any* completed backtest, a report file and trade details should be saved
**Validates: Requirements 4.4**

### Property 16: Excess returns calculated with benchmark
*For any* backtest with a configured benchmark, excess returns relative to benchmark should be calculated
**Validates: Requirements 4.5**

### Property 17: Cumulative returns chart generated
*For any* backtest result, a cumulative returns chart file should be generated
**Validates: Requirements 5.1**

### Property 18: Report contains all required charts
*For any* visualization report, it should contain position distribution and sector distribution charts
**Validates: Requirements 5.2**

### Property 19: Prediction analysis returns score distribution
*For any* prediction request, the system should return score distribution for stocks
**Validates: Requirements 5.3**

### Property 20: Report compares strategy vs benchmark
*For any* generated report, it should include comparison between strategy and benchmark returns
**Validates: Requirements 5.4**

### Property 21: Multi-model comparison chart generated
*For any* scenario with multiple models, a performance comparison chart should be generated
**Validates: Requirements 5.5**

### Property 22: Signal generation uses latest data
*For any* signal generation request, the system should use the most recent available data
**Validates: Requirements 6.1**

### Property 23: Stocks sorted by prediction score
*For any* prediction result, stocks should be sorted by their prediction scores
**Validates: Requirements 6.2**

### Property 24: Signals respect risk limits
*For any* generated signals, they should comply with configured risk limits
**Validates: Requirements 6.3, 6.5**

### Property 25: Signals include all action types
*For any* signal generation, the output should include buy, sell, and hold recommendations
**Validates: Requirements 6.4**

### Property 26: Models registered after training
*For any* completed model training, the model should be findable in the model registry
**Validates: Requirements 7.1**

### Property 27: Model metadata recorded at registration
*For any* registered model, it should have version, training date, and performance metrics
**Validates: Requirements 7.2**

### Property 28: Model query returns all registered models
*For any* model query, it should return all models that have been registered
**Validates: Requirements 7.3**

### Property 29: Registered models can be loaded
*For any* registered model, it should be loadable and usable for prediction
**Validates: Requirements 7.4**

### Property 30: Better models marked as candidates
*For any* new model with better performance than production model, it should be marked as candidate
**Validates: Requirements 7.5**

### Property 31: Configuration loaded from file
*For any* valid configuration file, system should load all parameters correctly
**Validates: Requirements 8.1**

### Property 32: Config updates applied on restart
*For any* modified configuration, changes should take effect on next system run
**Validates: Requirements 8.4**

### Property 33: Data paths validated in config
*For any* configuration containing data paths, the system should validate path existence
**Validates: Requirements 8.5**

### Property 34: Downloaded data passes validation
*For any* data download completion, the data should pass integrity and format checks
**Validates: Requirements 9.2**

### Property 35: Validated data updates local database
*For any* data that passes validation, it should be written to the local database
**Validates: Requirements 9.3**

### Property 36: Missing values handled by strategy
*For any* data containing missing values, the system should apply the configured filling strategy
**Validates: Requirements 9.5**

### Property 37: Operations logged to file
*For any* system operation, a log entry should be written to the log file
**Validates: Requirements 10.1**

### Property 38: Errors logged with stack trace
*For any* error occurrence, the log should contain detailed stack trace information
**Validates: Requirements 10.2**

### Property 39: Log entries contain required fields
*For any* log entry, it should contain timestamp, log level, and module name
**Validates: Requirements 10.3**

### Property 40: Logs filtered by configured level
*For any* configured log level, only messages at that level or above should be logged
**Validates: Requirements 10.4**

### Property 41: Log files rotated when size exceeded
*For any* log file exceeding size limit, a new log file should be created
**Validates: Requirements 10.5**

### Property 42: Invalid input prompts error and retry
*For any* invalid user input, the system should display an error and allow re-entry
**Validates: Requirements 12.5**

### Property 43: Model templates include descriptions
*For any* model template, it should have description of use case and expected performance
**Validates: Requirements 14.2**

### Property 44: Templates use default parameters
*For any* template-based training, the system should use the template's default parameters
**Validates: Requirements 14.3**

### Property 45: Template training generates report
*For any* completed template training, an easy-to-read performance report should be generated
**Validates: Requirements 14.4**

### Property 46: Signals include confidence scores
*For any* generated trading signal, it should include a confidence score
**Validates: Requirements 15.1**

### Property 47: Signal explanations available
*For any* trading signal, the system should be able to provide an explanation of main factors
**Validates: Requirements 15.2**

### Property 48: Reports include visualizations
*For any* generated report, it should contain charts and visualizations
**Validates: Requirements 15.4**

### Property 49: High-risk predictions marked with warnings
*For any* prediction with high risk level, it should be clearly marked with a warning
**Validates: Requirements 15.5**

## Error Handling

### Error Categories

1. **Configuration Errors**
   - Invalid configuration file format
   - Missing required configuration fields
   - Invalid data paths
   - Unsupported model types

2. **Data Errors**
   - Data source not available
   - Data download failures
   - Data validation failures
   - Missing or corrupted data files

3. **Training Errors**
   - Insufficient data for training
   - Model convergence failures
   - Out of memory errors
   - Invalid hyperparameters

4. **Backtest Errors**
   - Model loading failures
   - Invalid backtest period
   - Insufficient historical data
   - Strategy execution errors

5. **System Errors**
   - MLflow connection failures
   - File system errors
   - Permission errors
   - Network errors

### Error Handling Strategy

1. **Graceful Degradation**: System should continue operating with reduced functionality when possible
2. **Clear Error Messages**: All errors should provide clear, actionable messages in Chinese
3. **Error Recovery**: System should attempt automatic recovery for transient errors
4. **State Preservation**: Errors should not corrupt existing data or models
5. **Logging**: All errors should be logged with full context for debugging

### Error Response Format

```python
@dataclass
class ErrorResponse:
    error_code: str
    error_message: str  # Chinese message for users
    technical_details: str  # Technical details for debugging
    suggested_actions: List[str]  # Suggested fixes
    documentation_link: str  # Link to relevant docs
```

## Testing Strategy

### Unit Testing

Unit tests will verify specific functionality of individual components:

1. **Configuration Management**
   - Test loading valid configurations
   - Test handling invalid configurations
   - Test default configuration generation

2. **Data Management**
   - Test data validation logic
   - Test data path resolution
   - Test data info extraction

3. **Model Factory**
   - Test model creation for each supported type
   - Test template loading
   - Test parameter validation

4. **Signal Generation**
   - Test signal scoring logic
   - Test risk limit enforcement
   - Test signal explanation generation

5. **Visualization**
   - Test chart generation with sample data
   - Test report formatting
   - Test file output

### Property-Based Testing

Property-based tests will verify universal properties across many inputs using the Hypothesis library for Python:

**Configuration**:
- Each property test should run a minimum of 100 iterations
- Each test must be tagged with a comment referencing the correctness property
- Tag format: `# Feature: qlib-trading-system, Property {number}: {property_text}`

**Test Categories**:

1. **Initialization Properties**
   - Property 1: Qlib initialization
   - Property 2: Data validation
   - Property 3: MLflow initialization

2. **Training Properties**
   - Property 4-11: Training pipeline correctness
   - Test with various model types, dataset configs, and hyperparameters

3. **Backtest Properties**
   - Property 12-16: Backtest execution and metrics
   - Test with different time periods and strategies

4. **Visualization Properties**
   - Property 17-21: Chart and report generation
   - Test with various result formats

5. **Signal Generation Properties**
   - Property 22-25: Signal generation and risk management
   - Test with different market conditions and portfolios

6. **Model Registry Properties**
   - Property 26-30: Model management and versioning
   - Test with multiple models and versions

7. **Configuration Properties**
   - Property 31-33: Configuration loading and validation
   - Test with various config formats

8. **Data Management Properties**
   - Property 34-36: Data download and validation
   - Test with different data sources and formats

9. **Logging Properties**
   - Property 37-41: Log recording and rotation
   - Test with various log levels and operations

10. **User Interface Properties**
    - Property 42-49: Input validation and output formatting
    - Test with various user inputs

### Integration Testing

Integration tests will verify end-to-end workflows:

1. **Complete Training Workflow**
   - Initialize system → Load data → Train model → Save model → Verify in registry

2. **Complete Backtest Workflow**
   - Load model → Generate signals → Run backtest → Generate report → Verify results

3. **Complete Signal Generation Workflow**
   - Load model → Get latest data → Generate signals → Explain signals → Verify output

4. **Data Update Workflow**
   - Download data → Validate data → Update database → Verify availability

### Test Data

1. **Synthetic Data**: Generate synthetic market data for testing
2. **Sample Data**: Use qlib's sample dataset for integration tests
3. **Edge Cases**: Create specific datasets for edge case testing

### Testing Tools

- **pytest**: Test framework
- **Hypothesis**: Property-based testing library
- **pytest-cov**: Code coverage measurement
- **pytest-mock**: Mocking framework for unit tests

## Implementation Notes

### Technology Stack

- **Language**: Python 3.8+
- **Core Framework**: qlib (Microsoft Quantitative Investment Platform)
- **Experiment Tracking**: MLflow
- **CLI Framework**: Click or Typer
- **Visualization**: matplotlib, seaborn
- **Testing**: pytest, Hypothesis
- **Configuration**: YAML files
- **Logging**: Python logging module

### Directory Structure

```
QuantitationTranding/
├── src/
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── guided_workflow.py          [NEW]
│   │   └── prompts.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── data_manager.py
│   │   ├── model_factory.py
│   │   ├── config_manager.py
│   │   ├── portfolio_manager.py        [NEW]
│   │   └── risk_manager.py             [NEW]
│   ├── application/
│   │   ├── __init__.py
│   │   ├── market_selector.py          [NEW]
│   │   ├── performance_analyzer.py     [NEW]
│   │   ├── strategy_optimizer.py       [NEW]
│   │   ├── training_manager.py
│   │   ├── backtest_manager.py
│   │   ├── simulation_engine.py        [NEW]
│   │   ├── live_trading_manager.py     [NEW]
│   │   ├── report_scheduler.py         [NEW]
│   │   ├── signal_generator.py
│   │   ├── model_registry.py
│   │   ├── visualization_manager.py
│   │   └── report_generator.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── qlib_wrapper.py
│   │   ├── mlflow_tracker.py
│   │   ├── logger_system.py
│   │   ├── trading_api_adapter.py      [NEW]
│   │   └── notification_service.py     [NEW]
│   ├── models/
│   │   ├── __init__.py
│   │   ├── data_models.py
│   │   ├── market_models.py            [NEW]
│   │   ├── trading_models.py           [NEW]
│   │   └── risk_models.py              [NEW]
│   └── templates/
│       ├── __init__.py
│       └── model_templates.py
├── tests/
│   ├── unit/
│   ├── property/
│   └── integration/
├── config/
│   ├── default_config.yaml
│   ├── model_templates.yaml
│   ├── markets.yaml                    [NEW]
│   ├── risk_thresholds.yaml            [NEW]
│   └── notification_config.yaml        [NEW]
├── data/
│   ├── cn_data/
│   └── us_data/                        [NEW]
├── examples/
│   ├── mlruns/
│   └── guided_workflow_demo.py         [NEW]
├── logs/
├── simulations/                        [NEW]
│   └── sessions/
├── live_trading/                       [NEW]
│   ├── sessions/
│   └── orders/
├── reports/                            [NEW]
│   ├── daily/
│   ├── weekly/
│   └── monthly/
├── docs/
│   ├── quick_start.md
│   ├── user_guide.md
│   ├── api_reference.md
│   ├── guided_workflow.md              [NEW]
│   ├── simulation_guide.md             [NEW]
│   └── live_trading_guide.md           [NEW]
├── requirements.txt
├── setup.py
└── README.md
```

### Development Phases

1. **Phase 1: Core Infrastructure** ✅ (Partially Complete)
   - Set up project structure ✅
   - Implement configuration management ✅
   - Implement data manager ✅
   - Implement logging system ✅
   - Implement portfolio manager [NEW]
   - Implement risk manager [NEW]

2. **Phase 2: Market Selection and Analysis** [NEW]
   - Implement market selector
   - Implement performance analyzer
   - Implement asset recommendation system
   - Support multi-market data access

3. **Phase 3: Strategy Optimization** [NEW]
   - Implement strategy optimizer
   - Implement target return optimization
   - Implement risk-return balancing
   - Integrate with training manager

4. **Phase 4: Training Pipeline**
   - Implement model factory
   - Implement training manager (enhanced)
   - Integrate MLflow tracking
   - Implement model registry
   - Add target-driven training

5. **Phase 5: Backtest and Analysis**
   - Implement backtest manager
   - Implement visualization manager
   - Implement report generator
   - Add comparison tools

6. **Phase 6: Simulation Engine** [NEW]
   - Implement simulation engine
   - Implement simulation session management
   - Implement simulation reporting
   - Add forward-testing capabilities

7. **Phase 7: Live Trading** [NEW]
   - Implement trading API adapter
   - Implement live trading manager
   - Implement order execution
   - Implement position monitoring
   - Add safety controls

8. **Phase 8: Automated Reporting** [NEW]
   - Implement report scheduler
   - Implement notification service
   - Implement periodic reports
   - Implement risk alerts

9. **Phase 9: Guided User Interface** [NEW]
   - Implement guided workflow
   - Implement interactive prompts (enhanced)
   - Implement progress tracking
   - Implement help system

10. **Phase 10: Documentation and Polish**
    - Write comprehensive documentation
    - Create guided workflow tutorials
    - Create simulation examples
    - Create live trading guide
    - Optimize performance
    - Final testing and bug fixes

### Performance Considerations

1. **Data Loading**: Use qlib's efficient data loading mechanisms
2. **Model Training**: Support GPU acceleration when available
3. **Caching**: Cache frequently accessed data and models
4. **Parallel Processing**: Use multiprocessing for batch operations
5. **Memory Management**: Stream large datasets instead of loading entirely into memory

### Security Considerations

1. **Data Privacy**: Ensure market data is stored securely
2. **Model Protection**: Protect trained models from unauthorized access
3. **Configuration Security**: Validate all configuration inputs
4. **Logging**: Avoid logging sensitive information
5. **Dependencies**: Regularly update dependencies for security patches
6. **Trading Credentials**: Encrypt broker credentials and API keys [NEW]
7. **Order Validation**: Implement multi-level order validation before execution [NEW]
8. **Risk Limits**: Enforce hard limits on position sizes and daily losses [NEW]

## Guided User Workflow [NEW]

### Complete User Journey

系统提供完整的引导式工作流程，从市场选择到实盘交易的全流程支持：

#### Step 1: Market and Asset Selection
```
用户启动系统
  ↓
系统显示: "请选择投资市场"
  - 1. 中国市场 (A股)
  - 2. 美国市场
  - 3. 香港市场
  ↓
用户选择: 1 (中国市场)
  ↓
系统显示: "请选择投资品类"
  - 1. 股票
  - 2. 基金
  - 3. ETF
  ↓
用户选择: 1 (股票)
```

#### Step 2: Intelligent Recommendation
```
系统分析近3年市场表现
  ↓
系统显示: "基于历史表现，为您推荐以下优质标的："
  1. 贵州茅台 (600519) - 年化收益: 25%, 夏普比率: 1.8
  2. 宁德时代 (300750) - 年化收益: 35%, 夏普比率: 1.5
  3. 比亚迪 (002594) - 年化收益: 40%, 夏普比率: 1.3
  ...
  ↓
用户选择: 1, 2, 3 (选择多个标的)
```

#### Step 3: Target Setting
```
系统询问: "请输入您的期望年化收益率 (%)"
  ↓
用户输入: 20
  ↓
系统询问: "请选择风险偏好"
  - 1. 保守型 (低风险)
  - 2. 稳健型 (中等风险)
  - 3. 进取型 (高风险)
  ↓
用户选择: 2 (稳健型)
  ↓
系统询问: "请输入模拟交易周期 (天数)"
  ↓
用户输入: 30
```

#### Step 4: Strategy Optimization
```
系统显示: "正在根据您的目标优化策略..."
  ↓
系统分析:
  - 目标收益率: 20%
  - 风险偏好: 稳健型
  - 选定标的: 3个
  ↓
系统输出优化结果:
  - 预期收益率: 22%
  - 预期风险: 15%
  - 建议仓位配置:
    * 贵州茅台: 40%
    * 宁德时代: 35%
    * 比亚迪: 25%
  - 建议调仓频率: 每周
  ↓
用户确认: 是
```

#### Step 5: Model Training
```
系统显示: "正在训练预测模型..."
  ↓
训练进度:
  [████████████████████] 100%
  - 数据加载完成
  - 特征工程完成
  - 模型训练完成
  - 模型评估完成
  ↓
训练结果:
  - 模型类型: LightGBM
  - 训练集准确率: 68%
  - 验证集准确率: 65%
  - IC: 0.08
  ↓
用户查看详细报告
```

#### Step 6: Historical Backtest
```
系统显示: "正在进行历史回测..."
  ↓
回测期间: 2023-01-01 至 2023-12-31
  ↓
回测结果:
  - 总收益率: 28%
  - 年化收益率: 28%
  - 夏普比率: 1.6
  - 最大回撤: -12%
  - 胜率: 62%
  ↓
系统生成可视化报告:
  - 累计收益曲线
  - 持仓分布图
  - 行业分布图
  - 交易明细
  ↓
用户查看报告并确认: 继续
```

#### Step 7: Simulation Trading
```
系统显示: "开始模拟交易测试..."
  ↓
模拟参数:
  - 初始资金: 100,000元
  - 模拟周期: 30天
  - 开始日期: 2024-01-01
  ↓
模拟进度:
  Day 1: 买入贵州茅台 200股 @ 1,800元
  Day 1: 买入宁德时代 150股 @ 180元
  Day 2: 持仓价值: 102,500元 (+2.5%)
  Day 3: 持仓价值: 101,800元 (+1.8%)
  ...
  Day 30: 持仓价值: 108,500元 (+8.5%)
  ↓
模拟结果:
  - 30天收益率: 8.5%
  - 年化收益率: 24%
  - 最大回撤: -3.2%
  - 交易次数: 12
  - 胜率: 67%
  ↓
系统询问: "模拟结果满意吗？"
  - 1. 满意，开始实盘交易
  - 2. 不满意，调整参数重新测试
  - 3. 放弃
  ↓
用户选择: 1 (满意)
```

#### Step 8: Live Trading Setup
```
系统显示: "配置实盘交易参数..."
  ↓
系统询问: "请输入初始投资金额"
  ↓
用户输入: 50,000
  ↓
系统询问: "请选择券商"
  - 1. 华泰证券
  - 2. 中信证券
  - 3. 其他
  ↓
用户选择并输入交易账号信息
  ↓
系统设置风险控制:
  - 单日最大亏损: 2%
  - 单只股票最大仓位: 40%
  - 止损线: -5%
  ↓
用户确认所有设置
```

#### Step 9: Live Trading Execution
```
系统显示: "实盘交易已启动"
  ↓
实时监控:
  - 当前持仓价值: 50,000元
  - 今日收益: +0.5%
  - 累计收益: +0.5%
  ↓
系统自动执行:
  - 每日生成交易信号
  - 自动下单买卖
  - 实时风险监控
  - 触发止损/止盈
  ↓
异常情况处理:
  - 检测到风险: 发送预警通知
  - 触发止损: 自动平仓并通知
  - 系统异常: 暂停交易并通知
```

#### Step 10: Periodic Reporting
```
系统自动生成报告:
  ↓
每日报告 (每天收盘后):
  - 今日收益
  - 持仓情况
  - 交易记录
  ↓
每周报告 (每周五):
  - 本周收益
  - 策略表现
  - 风险分析
  ↓
每月报告 (每月末):
  - 月度收益
  - 年化收益
  - 与目标对比
  - 策略调整建议
  ↓
风险预警 (实时):
  - 回撤超过阈值
  - 单只股票亏损过大
  - 市场异常波动
  ↓
所有报告通过邮件/短信发送给用户
```

### Workflow State Management

系统维护完整的工作流状态，支持：

1. **断点续传**: 用户可以在任何步骤暂停，下次继续
2. **历史回溯**: 可以查看之前的选择和决策
3. **参数调整**: 可以返回任何步骤重新配置
4. **多方案对比**: 可以保存多个配置方案进行对比

### Error Handling in Workflow

每个步骤都有完善的错误处理：

1. **输入验证**: 实时验证用户输入的合法性
2. **友好提示**: 错误时给出清晰的中文提示和建议
3. **自动恢复**: 网络错误等临时问题自动重试
4. **安全退出**: 任何时候都可以安全退出，保存当前状态
