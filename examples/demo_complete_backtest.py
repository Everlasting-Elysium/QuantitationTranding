"""
完整回测示例 / Complete Backtest Example
演示回测配置、执行、分析的完整流程
Demonstrates the complete workflow of backtest configuration, execution, and analysis

这个示例展示了:
This example demonstrates:
1. 回测配置 / Backtest configuration
2. 回测执行 / Backtest execution
3. 性能指标分析 / Performance metrics analysis
4. 可视化报告生成 / Visualization report generation
5. 与基准对比 / Benchmark comparison
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径 / Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.data_manager import DataManager
from src.core.model_factory import ModelFactory
from src.infrastructure.qlib_wrapper import QlibWrapper
from src.infrastructure.logger_system import setup_logger
from src.application.training_manager import TrainingManager, TrainingConfig, DatasetConfig
from src.application.backtest_manager import BacktestManager, BacktestConfig
from src.application.visualization_manager import VisualizationManager
from src.application.report_generator import ReportGenerator


def print_section(title: str):
    """打印章节标题 / Print section title"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_metrics(metrics: dict, title: str = "指标 / Metrics"):
    """打印指标 / Print metrics"""
    print(f"\n{title}:")
    print("-" * 40)
    for metric_name, metric_value in metrics.items():
        if isinstance(metric_value, float):
            if "return" in metric_name.lower() or "drawdown" in metric_name.lower():
                print(f"  {metric_name}: {metric_value:.2%}")
            else:
                print(f"  {metric_name}: {metric_value:.4f}")
        else:
            print(f"  {metric_name}: {metric_value}")


def main():
    """主函数 / Main function"""
    
    print_section("完整回测示例 / Complete Backtest Example")
    
    # ========================================================================
    # 步骤 1: 系统初始化 / Step 1: System Initialization
    # ========================================================================
    print("\n步骤 1 / Step 1: 系统初始化 / System Initialization")
    print("-" * 80)
    
    setup_logger(log_dir="./logs", log_level="INFO")
    
    qlib_wrapper = QlibWrapper()
    try:
        qlib_wrapper.init(
            provider_uri="~/.qlib/qlib_data/cn_data",
            region="cn"
        )
        print("✓ Qlib初始化成功 / Qlib initialized successfully")
    except Exception as e:
        print(f"✗ Qlib初始化失败 / Qlib initialization failed: {str(e)}")
        return
    
    data_manager = DataManager(qlib_wrapper=qlib_wrapper)
    model_factory = ModelFactory()
    
    training_manager = TrainingManager(
        data_manager=data_manager,
        model_factory=model_factory,
        mlflow_tracker=None,
        output_dir="./outputs"
    )
    
    backtest_manager = BacktestManager(
        data_manager=data_manager,
        model_factory=model_factory,
        output_dir="./outputs"
    )
    
    visualization_manager = VisualizationManager(output_dir="./outputs/visualizations")
    report_generator = ReportGenerator(output_dir="./outputs/reports")
    
    print("✓ 所有组件初始化完成 / All components initialized")
    
    # ========================================================================
    # 步骤 2: 训练模型 / Step 2: Train Model
    # ========================================================================
    print("\n步骤 2 / Step 2: 训练模型 / Train Model")
    print("-" * 80)
    
    dataset_config = DatasetConfig(
        instruments="csi300",
        start_time="2020-01-01",
        end_time="2021-12-31",
        features=["$close", "$volume", "$open", "$high", "$low"],
        label="Ref($close, -1) / $close - 1"
    )
    
    print(f"训练数据集 / Training dataset:")
    print(f"  股票池 / Instruments: {dataset_config.instruments}")
    print(f"  时间范围 / Time range: {dataset_config.start_time} 至 / to {dataset_config.end_time}")
    
    training_config = TrainingConfig(
        model_type="lgbm",
        dataset_config=dataset_config,
        model_params={
            "loss": "mse",
            "num_boost_round": 100,
            "learning_rate": 0.1,
        },
        training_params={},
        experiment_name="backtest_demo"
    )
    
    print(f"\n开始训练 / Starting training...")
    
    try:
        training_result = training_manager.train_model(training_config)
        print(f"✓ 训练完成 / Training completed")
        print(f"  模型ID / Model ID: {training_result.model_id}")
        print(f"  训练时长 / Training time: {training_result.training_time:.2f}秒 / seconds")
        
        model_id = training_result.model_id
        
    except Exception as e:
        print(f"✗ 训练失败 / Training failed: {str(e)}")
        return
    
    # ========================================================================
    # 步骤 3: 配置回测 / Step 3: Configure Backtest
    # ========================================================================
    print("\n步骤 3 / Step 3: 配置回测 / Configure Backtest")
    print("-" * 80)
    
    # 回测策略配置 / Backtest strategy configuration
    print("回测策略 / Backtest strategy:")
    print("  策略类型 / Strategy type: TopkDropoutStrategy")
    print("  持仓数量 / Position count: Top 30")
    print("  每日调仓 / Daily rebalance: Drop 3")
    
    # 回测执行器配置 / Backtest executor configuration
    print("\n回测执行器 / Backtest executor:")
    print("  执行器类型 / Executor type: SimulatorExecutor")
    print("  时间步长 / Time step: 1 day")
    print("  生成组合指标 / Generate portfolio metrics: Yes")
    
    # 交易成本配置 / Trading cost configuration
    print("\n交易成本 / Trading costs:")
    print("  开仓成本 / Open cost: 0.05%")
    print("  平仓成本 / Close cost: 0.15%")
    print("  最小成本 / Min cost: ¥5")
    print("  涨跌停限制 / Limit threshold: ±9.5%")
    
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
    
    print(f"\n基准指数 / Benchmark: {backtest_config.benchmark} (沪深300 / CSI 300)")
    
    # ========================================================================
    # 步骤 4: 执行回测 / Step 4: Execute Backtest
    # ========================================================================
    print("\n步骤 4 / Step 4: 执行回测 / Execute Backtest")
    print("-" * 80)
    
    backtest_start = "2022-01-01"
    backtest_end = "2022-12-31"
    
    print(f"回测时间范围 / Backtest time range: {backtest_start} 至 / to {backtest_end}")
    print(f"初始资金 / Initial capital: ¥100,000,000")
    
    print(f"\n开始回测 / Starting backtest...")
    
    try:
        backtest_result = backtest_manager.run_backtest(
            model_id=model_id,
            start_date=backtest_start,
            end_date=backtest_end,
            config=backtest_config
        )
        
        print(f"✓ 回测完成 / Backtest completed")
        
    except Exception as e:
        print(f"✗ 回测失败 / Backtest failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    
    # ========================================================================
    # 步骤 5: 分析回测结果 / Step 5: Analyze Backtest Results
    # ========================================================================
    print("\n步骤 5 / Step 5: 分析回测结果 / Analyze Backtest Results")
    print("-" * 80)
    
    # 打印主要指标 / Print main metrics
    print_metrics(backtest_result.metrics, "回测指标 / Backtest Metrics")
    
    # 交易统计 / Trading statistics
    print(f"\n交易统计 / Trading Statistics:")
    print("-" * 40)
    print(f"  总交易次数 / Total trades: {len(backtest_result.trades)}")
    
    if len(backtest_result.trades) > 0:
        buy_trades = [t for t in backtest_result.trades if t.action == "buy"]
        sell_trades = [t for t in backtest_result.trades if t.action == "sell"]
        print(f"  买入次数 / Buy trades: {len(buy_trades)}")
        print(f"  卖出次数 / Sell trades: {len(sell_trades)}")
        
        # 计算平均交易成本 / Calculate average trading cost
        total_cost = sum(t.commission for t in backtest_result.trades)
        print(f"  总交易成本 / Total trading cost: ¥{total_cost:,.2f}")
        print(f"  平均交易成本 / Average trading cost: ¥{total_cost/len(backtest_result.trades):,.2f}")
    
    # 持仓分析 / Position analysis
    if len(backtest_result.positions) > 0:
        print(f"\n持仓分析 / Position Analysis:")
        print("-" * 40)
        
        # 获取最后一天的持仓 / Get last day's positions
        last_positions = backtest_result.positions.iloc[-1]
        non_zero_positions = last_positions[last_positions != 0]
        
        print(f"  最终持仓数量 / Final position count: {len(non_zero_positions)}")
        print(f"  最大持仓股票 / Top positions:")
        
        # 显示前5个持仓 / Show top 5 positions
        top_positions = non_zero_positions.abs().nlargest(5)
        for stock, weight in top_positions.items():
            print(f"    {stock}: {weight:.2%}")
    
    # ========================================================================
    # 步骤 6: 生成可视化报告 / Step 6: Generate Visualization Reports
    # ========================================================================
    print("\n步骤 6 / Step 6: 生成可视化报告 / Generate Visualization Reports")
    print("-" * 80)
    
    try:
        # 生成累计收益曲线 / Generate cumulative returns chart
        returns_chart_path = "./outputs/visualizations/backtest_cumulative_returns.png"
        visualization_manager.plot_cumulative_returns(
            returns=backtest_result.returns,
            benchmark=None,
            save_path=returns_chart_path
        )
        print(f"✓ 累计收益曲线已生成 / Cumulative returns chart generated")
        print(f"  路径 / Path: {returns_chart_path}")
        
        # 生成持仓分布图 / Generate position distribution chart
        if len(backtest_result.positions) > 0:
            position_chart_path = "./outputs/visualizations/backtest_position_distribution.png"
            last_positions = backtest_result.positions.iloc[-1]
            visualization_manager.plot_position_distribution(
                positions=last_positions,
                save_path=position_chart_path
            )
            print(f"✓ 持仓分布图已生成 / Position distribution chart generated")
            print(f"  路径 / Path: {position_chart_path}")
        
    except Exception as e:
        print(f"⚠ 可视化生成失败 / Visualization generation failed: {str(e)}")
    
    # ========================================================================
    # 步骤 7: 生成文本报告 / Step 7: Generate Text Report
    # ========================================================================
    print("\n步骤 7 / Step 7: 生成文本报告 / Generate Text Report")
    print("-" * 80)
    
    try:
        report = report_generator.generate_backtest_report(backtest_result)
        report_path = "./outputs/reports/complete_backtest_report.txt"
        
        # 保存报告 / Save report
        Path(report_path).parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"✓ 回测报告已生成 / Backtest report generated")
        print(f"  路径 / Path: {report_path}")
        
        # 显示报告摘要 / Display report summary
        print(f"\n报告摘要 / Report summary:")
        print("-" * 40)
        lines = report.split('\n')
        for line in lines[:20]:  # 显示前20行 / Show first 20 lines
            print(line)
        if len(lines) > 20:
            print("...")
        
    except Exception as e:
        print(f"⚠ 报告生成失败 / Report generation failed: {str(e)}")
    
    # ========================================================================
    # 步骤 8: 风险分析 / Step 8: Risk Analysis
    # ========================================================================
    print("\n步骤 8 / Step 8: 风险分析 / Risk Analysis")
    print("-" * 80)
    
    metrics = backtest_result.metrics
    
    # 收益风险比 / Return-risk ratio
    annual_return = metrics.get('annual_return', 0)
    max_drawdown = abs(metrics.get('max_drawdown', 0))
    sharpe_ratio = metrics.get('sharpe_ratio', 0)
    
    print(f"风险评估 / Risk Assessment:")
    print(f"  年化收益率 / Annual return: {annual_return:.2%}")
    print(f"  最大回撤 / Max drawdown: {max_drawdown:.2%}")
    print(f"  夏普比率 / Sharpe ratio: {sharpe_ratio:.4f}")
    
    # 风险等级评估 / Risk level assessment
    print(f"\n风险等级 / Risk Level:")
    if max_drawdown < 0.10:
        risk_level = "低 / Low"
    elif max_drawdown < 0.20:
        risk_level = "中 / Medium"
    else:
        risk_level = "高 / High"
    print(f"  {risk_level}")
    
    # 收益质量评估 / Return quality assessment
    print(f"\n收益质量 / Return Quality:")
    if sharpe_ratio > 2.0:
        quality = "优秀 / Excellent"
    elif sharpe_ratio > 1.0:
        quality = "良好 / Good"
    elif sharpe_ratio > 0.5:
        quality = "一般 / Fair"
    else:
        quality = "较差 / Poor"
    print(f"  {quality}")
    
    # ========================================================================
    # 总结 / Summary
    # ========================================================================
    print_section("总结 / Summary")
    
    print("\n本示例展示了完整的回测流程:")
    print("This example demonstrated the complete backtest workflow:")
    print("  ✓ 模型训练 / Model training")
    print("  ✓ 回测配置 / Backtest configuration")
    print("  ✓ 回测执行 / Backtest execution")
    print("  ✓ 性能指标分析 / Performance metrics analysis")
    print("  ✓ 可视化报告生成 / Visualization report generation")
    print("  ✓ 文本报告生成 / Text report generation")
    print("  ✓ 风险分析 / Risk analysis")
    
    print("\n生成的文件 / Generated files:")
    print(f"  - 累计收益图 / Cumulative returns: ./outputs/visualizations/backtest_cumulative_returns.png")
    print(f"  - 持仓分布图 / Position distribution: ./outputs/visualizations/backtest_position_distribution.png")
    print(f"  - 回测报告 / Backtest report: ./outputs/reports/complete_backtest_report.txt")
    
    print("\n建议 / Recommendations:")
    if annual_return > 0.15 and sharpe_ratio > 1.0 and max_drawdown < 0.20:
        print("  ✓ 策略表现良好，可以考虑实盘测试")
        print("    Strategy performs well, consider live testing")
    elif annual_return > 0.10 and sharpe_ratio > 0.5:
        print("  ⚠ 策略表现一般，建议优化参数")
        print("    Strategy performance is fair, recommend parameter optimization")
    else:
        print("  ✗ 策略表现不佳，建议重新设计")
        print("    Strategy performance is poor, recommend redesign")
    
    print("\n下一步 / Next steps:")
    print("  1. 优化策略参数 / Optimize strategy parameters")
    print("  2. 尝试不同的模型 / Try different models")
    print("  3. 进行模拟交易测试 / Conduct simulation trading test")
    print("  4. 查看信号生成示例 / View signal generation example")
    print("     python examples/demo_signal_generator.py")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
