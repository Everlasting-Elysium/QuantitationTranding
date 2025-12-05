"""
完整端到端示例 / Complete End-to-End Example
演示从数据准备到交易信号生成的完整流程
Demonstrates the complete workflow from data preparation to trading signal generation

这个示例展示了:
This example demonstrates:
1. 系统初始化 / System initialization
2. 数据准备和验证 / Data preparation and validation
3. 模型训练 / Model training
4. 历史回测 / Historical backtesting
5. 可视化分析 / Visualization analysis
6. 交易信号生成 / Trading signal generation
7. 信号解释 / Signal explanation
"""

import sys
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径 / Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.data_manager import DataManager
from src.core.model_factory import ModelFactory
from src.core.config_manager import ConfigManager
from src.infrastructure.qlib_wrapper import QlibWrapper
from src.infrastructure.mlflow_tracker import MLflowTracker
from src.infrastructure.logger_system import setup_logger
from src.application.training_manager import (
    TrainingManager,
    TrainingConfig,
    DatasetConfig
)
from src.application.backtest_manager import BacktestManager, BacktestConfig
from src.application.visualization_manager import VisualizationManager
from src.application.signal_generator import SignalGenerator
from src.application.report_generator import ReportGenerator


def print_section(title: str):
    """打印章节标题 / Print section title"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_step(step_num: int, description: str):
    """打印步骤 / Print step"""
    print(f"\n步骤 {step_num} / Step {step_num}: {description}")
    print("-" * 80)


def main():
    """主函数 / Main function"""
    
    print_section("量化交易系统 - 完整端到端示例 / Quantitative Trading System - Complete End-to-End Example")
    
    # ========================================================================
    # 步骤 1: 系统初始化 / Step 1: System Initialization
    # ========================================================================
    print_step(1, "系统初始化 / System Initialization")
    
    # 设置日志 / Setup logging
    setup_logger(log_dir="./logs", log_level="INFO")
    print("✓ 日志系统初始化完成 / Logging system initialized")
    
    # 加载配置 / Load configuration
    config_manager = ConfigManager()
    try:
        config = config_manager.load_config("./config/default_config.yaml")
        print("✓ 配置文件加载成功 / Configuration loaded successfully")
    except Exception as e:
        print(f"⚠ 使用默认配置 / Using default configuration: {str(e)}")
        config = config_manager.get_default_config()
    
    # 初始化qlib / Initialize qlib
    qlib_wrapper = QlibWrapper()
    try:
        qlib_wrapper.init(
            provider_uri=config.get("data_path", "~/.qlib/qlib_data/cn_data"),
            region=config.get("region", "cn")
        )
        print("✓ Qlib初始化成功 / Qlib initialized successfully")
    except Exception as e:
        print(f"✗ Qlib初始化失败 / Qlib initialization failed: {str(e)}")
        print("\n请先下载数据 / Please download data first:")
        print("python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn")
        return
    
    # 初始化各个管理器 / Initialize managers
    data_manager = DataManager(qlib_wrapper=qlib_wrapper)
    model_factory = ModelFactory()
    
    # 初始化MLflow（可选）/ Initialize MLflow (optional)
    mlflow_tracker = None
    try:
        mlflow_tracker = MLflowTracker(tracking_uri="./examples/mlruns")
        mlflow_tracker.initialize()
        print("✓ MLflow追踪器初始化成功 / MLflow tracker initialized successfully")
    except Exception as e:
        print(f"⚠ MLflow追踪器初始化失败（将继续不使用MLflow）/ MLflow tracker initialization failed: {str(e)}")
    
    training_manager = TrainingManager(
        data_manager=data_manager,
        model_factory=model_factory,
        mlflow_tracker=mlflow_tracker,
        output_dir="./outputs"
    )
    
    backtest_manager = BacktestManager(
        data_manager=data_manager,
        model_factory=model_factory,
        output_dir="./outputs"
    )
    
    visualization_manager = VisualizationManager(output_dir="./outputs/visualizations")
    signal_generator = SignalGenerator(data_manager=data_manager, model_factory=model_factory)
    report_generator = ReportGenerator(output_dir="./outputs/reports")
    
    print("✓ 所有管理器初始化完成 / All managers initialized")
    
    # ========================================================================
    # 步骤 2: 数据准备和验证 / Step 2: Data Preparation and Validation
    # ========================================================================
    print_step(2, "数据准备和验证 / Data Preparation and Validation")
    
    try:
        data_info = data_manager.get_data_info()
        print(f"✓ 数据验证成功 / Data validation successful")
        print(f"  数据时间范围 / Data time range: {data_info.get('start_date', 'N/A')} 至 / to {data_info.get('end_date', 'N/A')}")
        print(f"  可用股票数量 / Available stocks: {data_info.get('stock_count', 'N/A')}")
    except Exception as e:
        print(f"✗ 数据验证失败 / Data validation failed: {str(e)}")
        return
    
    # ========================================================================
    # 步骤 3: 模型训练 / Step 3: Model Training
    # ========================================================================
    print_step(3, "模型训练 / Model Training")
    
    # 配置数据集 / Configure dataset
    dataset_config = DatasetConfig(
        instruments="csi300",
        start_time="2020-01-01",
        end_time="2021-12-31",
        features=["$close", "$volume", "$open", "$high", "$low"],
        label="Ref($close, -1) / $close - 1"
    )
    
    print(f"数据集配置 / Dataset configuration:")
    print(f"  股票池 / Instruments: {dataset_config.instruments}")
    print(f"  训练时间范围 / Training time range: {dataset_config.start_time} 至 / to {dataset_config.end_time}")
    print(f"  特征数量 / Number of features: {len(dataset_config.features)}")
    
    # 配置训练 / Configure training
    training_config = TrainingConfig(
        model_type="lgbm",
        dataset_config=dataset_config,
        model_params={
            "loss": "mse",
            "num_boost_round": 100,
            "learning_rate": 0.1,
        },
        training_params={},
        experiment_name="end_to_end_demo"
    )
    
    print(f"\n开始训练模型 / Starting model training...")
    print(f"  模型类型 / Model type: {training_config.model_type}")
    
    try:
        training_result = training_manager.train_model(training_config)
        
        print(f"\n✓ 训练完成 / Training completed!")
        print(f"  模型ID / Model ID: {training_result.model_id}")
        print(f"  训练时长 / Training time: {training_result.training_time:.2f} 秒 / seconds")
        print(f"  模型路径 / Model path: {training_result.model_path}")
        print(f"  评估指标 / Metrics:")
        for metric_name, metric_value in training_result.metrics.items():
            print(f"    {metric_name}: {metric_value:.6f}")
        
        model_id = training_result.model_id
        
    except Exception as e:
        print(f"✗ 训练失败 / Training failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    
    # ========================================================================
    # 步骤 4: 历史回测 / Step 4: Historical Backtesting
    # ========================================================================
    print_step(4, "历史回测 / Historical Backtesting")
    
    # 配置回测 / Configure backtest
    backtest_config = BacktestConfig(
        strategy_config={
            "class": "TopkDropoutStrategy",
            "module_path": "qlib.contrib.strategy.signal_strategy",
            "kwargs": {
                "topk": 30,
                "n_drop": 3,
            }
        },
        executor_config={
            "class": "SimulatorExecutor",
            "module_path": "qlib.backtest.executor",
            "kwargs": {
                "time_per_step": "day",
                "generate_portfolio_metrics": True,
            }
        },
        benchmark="SH000300"
    )
    
    print(f"回测配置 / Backtest configuration:")
    print(f"  策略 / Strategy: TopkDropoutStrategy (Top 30, Drop 3)")
    print(f"  基准 / Benchmark: {backtest_config.benchmark}")
    print(f"  回测时间范围 / Backtest time range: 2022-01-01 至 / to 2022-12-31")
    
    print(f"\n开始回测 / Starting backtest...")
    
    try:
        backtest_result = backtest_manager.run_backtest(
            model_id=model_id,
            start_date="2022-01-01",
            end_date="2022-12-31",
            config=backtest_config
        )
        
        print(f"\n✓ 回测完成 / Backtest completed!")
        print(f"  回测指标 / Backtest metrics:")
        for metric_name, metric_value in backtest_result.metrics.items():
            if isinstance(metric_value, float):
                print(f"    {metric_name}: {metric_value:.4f}")
            else:
                print(f"    {metric_name}: {metric_value}")
        
        print(f"  交易次数 / Number of trades: {len(backtest_result.trades)}")
        
    except Exception as e:
        print(f"✗ 回测失败 / Backtest failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    
    # ========================================================================
    # 步骤 5: 可视化分析 / Step 5: Visualization Analysis
    # ========================================================================
    print_step(5, "可视化分析 / Visualization Analysis")
    
    try:
        # 生成累计收益曲线 / Generate cumulative returns chart
        returns_chart_path = "./outputs/visualizations/cumulative_returns.png"
        visualization_manager.plot_cumulative_returns(
            returns=backtest_result.returns,
            benchmark=None,  # 可以添加基准数据 / Can add benchmark data
            save_path=returns_chart_path
        )
        print(f"✓ 累计收益曲线已生成 / Cumulative returns chart generated: {returns_chart_path}")
        
        # 生成持仓分布图 / Generate position distribution chart
        if len(backtest_result.positions) > 0:
            position_chart_path = "./outputs/visualizations/position_distribution.png"
            # 获取最后一天的持仓 / Get last day's positions
            last_positions = backtest_result.positions.iloc[-1]
            visualization_manager.plot_position_distribution(
                positions=last_positions,
                save_path=position_chart_path
            )
            print(f"✓ 持仓分布图已生成 / Position distribution chart generated: {position_chart_path}")
        
    except Exception as e:
        print(f"⚠ 可视化生成失败 / Visualization generation failed: {str(e)}")
    
    # ========================================================================
    # 步骤 6: 生成回测报告 / Step 6: Generate Backtest Report
    # ========================================================================
    print_step(6, "生成回测报告 / Generate Backtest Report")
    
    try:
        report = report_generator.generate_backtest_report(backtest_result)
        report_path = "./outputs/reports/backtest_report.txt"
        
        # 保存报告 / Save report
        Path(report_path).parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"✓ 回测报告已生成 / Backtest report generated: {report_path}")
        print(f"\n报告摘要 / Report summary:")
        print(report[:500] + "..." if len(report) > 500 else report)
        
    except Exception as e:
        print(f"⚠ 报告生成失败 / Report generation failed: {str(e)}")
    
    # ========================================================================
    # 步骤 7: 交易信号生成 / Step 7: Trading Signal Generation
    # ========================================================================
    print_step(7, "交易信号生成 / Trading Signal Generation")
    
    # 创建一个简单的投资组合 / Create a simple portfolio
    from src.models.data_models import Portfolio
    current_portfolio = Portfolio(
        positions={},
        cash=1000000.0,
        total_value=1000000.0
    )
    
    print(f"当前投资组合 / Current portfolio:")
    print(f"  现金 / Cash: ¥{current_portfolio.cash:,.2f}")
    print(f"  总价值 / Total value: ¥{current_portfolio.total_value:,.2f}")
    
    print(f"\n生成交易信号 / Generating trading signals...")
    
    try:
        # 使用最近的日期生成信号 / Generate signals for recent date
        signal_date = "2022-12-30"
        signals = signal_generator.generate_signals(
            model_id=model_id,
            date=signal_date,
            portfolio=current_portfolio,
            top_k=10
        )
        
        print(f"\n✓ 信号生成完成 / Signal generation completed!")
        print(f"  生成日期 / Generation date: {signal_date}")
        print(f"  信号数量 / Number of signals: {len(signals)}")
        
        # 显示前5个信号 / Display top 5 signals
        print(f"\n  前5个交易信号 / Top 5 trading signals:")
        for i, signal in enumerate(signals[:5], 1):
            print(f"    {i}. {signal.stock_code}: {signal.action} (得分 / score: {signal.score:.4f}, 置信度 / confidence: {signal.confidence:.2f})")
        
    except Exception as e:
        print(f"✗ 信号生成失败 / Signal generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        signals = []
    
    # ========================================================================
    # 步骤 8: 信号解释 / Step 8: Signal Explanation
    # ========================================================================
    print_step(8, "信号解释 / Signal Explanation")
    
    if signals:
        try:
            # 解释第一个信号 / Explain first signal
            first_signal = signals[0]
            explanation = signal_generator.explain_signal(first_signal)
            
            print(f"✓ 信号解释生成完成 / Signal explanation generated!")
            print(f"\n  股票代码 / Stock code: {explanation.signal.stock_code}")
            print(f"  操作建议 / Action: {explanation.signal.action}")
            print(f"  风险等级 / Risk level: {explanation.risk_level}")
            print(f"  主要因素 / Main factors:")
            for factor_name, contribution in explanation.main_factors[:3]:
                print(f"    - {factor_name}: {contribution:.4f}")
            print(f"  描述 / Description: {explanation.description}")
            
        except Exception as e:
            print(f"⚠ 信号解释失败 / Signal explanation failed: {str(e)}")
    
    # ========================================================================
    # 总结 / Summary
    # ========================================================================
    print_section("演示完成 / Demo Completed")
    
    print("\n本示例展示了完整的量化交易流程:")
    print("This example demonstrated the complete quantitative trading workflow:")
    print("  ✓ 系统初始化和配置 / System initialization and configuration")
    print("  ✓ 数据准备和验证 / Data preparation and validation")
    print("  ✓ 模型训练 / Model training")
    print("  ✓ 历史回测 / Historical backtesting")
    print("  ✓ 可视化分析 / Visualization analysis")
    print("  ✓ 回测报告生成 / Backtest report generation")
    print("  ✓ 交易信号生成 / Trading signal generation")
    print("  ✓ 信号解释 / Signal explanation")
    
    print("\n生成的文件 / Generated files:")
    print(f"  - 模型文件 / Model file: {training_result.model_path}")
    print(f"  - 累计收益图 / Cumulative returns chart: ./outputs/visualizations/cumulative_returns.png")
    print(f"  - 持仓分布图 / Position distribution chart: ./outputs/visualizations/position_distribution.png")
    print(f"  - 回测报告 / Backtest report: ./outputs/reports/backtest_report.txt")
    
    if mlflow_tracker:
        print(f"\n查看MLflow UI / View MLflow UI:")
        print(f"  mlflow ui --backend-store-uri ./examples/mlruns")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
