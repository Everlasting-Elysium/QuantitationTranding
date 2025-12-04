"""
报告生成器演示 / Report Generator Demo
演示如何使用ReportGenerator生成各种报告
Demonstrates how to use ReportGenerator to generate various reports
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# 添加项目根目录到路径 / Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.application.report_generator import (
    ReportGenerator,
    TrainingResult,
    BacktestResult,
    SimulationReport,
    TradingSession
)
from src.infrastructure.logger_system import setup_logging


def demo_training_report():
    """演示训练报告生成 / Demonstrate training report generation"""
    print("\n" + "=" * 80)
    print("演示训练报告生成 / Demonstrating Training Report Generation")
    print("=" * 80)
    
    # 创建报告生成器 / Create report generator
    generator = ReportGenerator(output_dir="./outputs/reports")
    
    # 创建模拟训练结果 / Create mock training result
    training_result = TrainingResult(
        model_id="lgbm_model_20240101",
        metrics={
            "train_accuracy": 0.68,
            "val_accuracy": 0.65,
            "train_ic": 0.08,
            "val_ic": 0.075,
            "train_loss": 0.32,
            "val_loss": 0.35
        },
        training_time=125.5,
        model_path="./outputs/models/lgbm_model_20240101/model.pkl",
        experiment_id="exp_001",
        run_id="run_001"
    )
    
    # 生成训练报告 / Generate training report
    report = generator.generate_training_report(training_result)
    print(report)
    
    print("\n✓ 训练报告生成成功 / Training report generated successfully")


def demo_backtest_report():
    """演示回测报告生成 / Demonstrate backtest report generation"""
    print("\n" + "=" * 80)
    print("演示回测报告生成 / Demonstrating Backtest Report Generation")
    print("=" * 80)
    
    # 创建报告生成器 / Create report generator
    generator = ReportGenerator(output_dir="./outputs/reports")
    
    # 创建模拟回测结果 / Create mock backtest result
    # 生成模拟收益率数据 / Generate mock returns data
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    returns = pd.Series(
        np.random.normal(0.001, 0.02, len(dates)),
        index=dates
    )
    
    # 生成模拟基准收益率 / Generate mock benchmark returns
    benchmark_returns = pd.Series(
        np.random.normal(0.0005, 0.015, len(dates)),
        index=dates
    )
    
    # 创建空的持仓数据 / Create empty positions data
    positions = pd.DataFrame()
    
    # 计算指标 / Calculate metrics
    cumulative_returns = (1 + returns).cumprod()
    total_return = cumulative_returns.iloc[-1] - 1
    annual_return = (1 + total_return) ** (252 / len(returns)) - 1
    volatility = returns.std() * np.sqrt(252)
    sharpe_ratio = annual_return / volatility if volatility > 0 else 0
    
    # 计算最大回撤 / Calculate max drawdown
    running_max = cumulative_returns.expanding().max()
    drawdown = (cumulative_returns - running_max) / running_max
    max_drawdown = drawdown.min()
    
    # 计算胜率 / Calculate win rate
    win_rate = (returns > 0).sum() / len(returns)
    
    # 计算基准指标 / Calculate benchmark metrics
    benchmark_cumulative = (1 + benchmark_returns).cumprod()
    benchmark_return = benchmark_cumulative.iloc[-1] - 1
    excess_return = total_return - benchmark_return
    
    backtest_result = BacktestResult(
        returns=returns,
        positions=positions,
        metrics={
            "total_return": total_return,
            "annual_return": annual_return,
            "volatility": volatility,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown,
            "win_rate": win_rate,
            "benchmark_return": benchmark_return,
            "excess_return": excess_return
        },
        trades=[],
        benchmark_returns=benchmark_returns
    )
    
    # 生成回测报告 / Generate backtest report
    report = generator.generate_backtest_report(backtest_result)
    print(report)
    
    print("\n✓ 回测报告生成成功 / Backtest report generated successfully")


def demo_simulation_report():
    """演示模拟交易报告生成 / Demonstrate simulation report generation"""
    print("\n" + "=" * 80)
    print("演示模拟交易报告生成 / Demonstrating Simulation Report Generation")
    print("=" * 80)
    
    # 创建报告生成器 / Create report generator
    generator = ReportGenerator(output_dir="./outputs/reports")
    
    # 创建模拟交易报告 / Create mock simulation report
    dates = pd.date_range(start='2024-01-01', end='2024-01-30', freq='D')
    daily_returns = pd.Series(
        np.random.normal(0.002, 0.015, len(dates)),
        index=dates
    )
    
    cumulative_returns = (1 + daily_returns).cumprod()
    total_return = cumulative_returns.iloc[-1] - 1
    annual_return = (1 + total_return) ** (252 / len(daily_returns)) - 1
    volatility = daily_returns.std() * np.sqrt(252)
    sharpe_ratio = annual_return / volatility if volatility > 0 else 0
    
    # 计算最大回撤 / Calculate max drawdown
    running_max = cumulative_returns.expanding().max()
    drawdown = (cumulative_returns - running_max) / running_max
    max_drawdown = drawdown.min()
    
    # 计算胜率 / Calculate win rate
    win_rate = (daily_returns > 0).sum() / len(daily_returns)
    
    simulation_report = SimulationReport(
        session_id="sim_session_001",
        total_return=total_return,
        annual_return=annual_return,
        sharpe_ratio=sharpe_ratio,
        max_drawdown=max_drawdown,
        win_rate=win_rate,
        total_trades=45,
        profitable_trades=30,
        final_portfolio_value=108500.0,
        daily_returns=daily_returns,
        trade_history=[]
    )
    
    # 生成模拟交易报告 / Generate simulation report
    report = generator.generate_simulation_report(simulation_report)
    print(report)
    
    print("\n✓ 模拟交易报告生成成功 / Simulation report generated successfully")


def demo_live_trading_report():
    """演示实盘交易报告生成 / Demonstrate live trading report generation"""
    print("\n" + "=" * 80)
    print("演示实盘交易报告生成 / Demonstrating Live Trading Report Generation")
    print("=" * 80)
    
    # 创建报告生成器 / Create report generator
    generator = ReportGenerator(output_dir="./outputs/reports")
    
    # 创建模拟交易会话 / Create mock trading session
    trading_session = TradingSession(
        session_id="live_session_001",
        model_id="lgbm_model_20240101",
        start_date="2024-01-01",
        initial_capital=50000.0,
        current_capital=52500.0,
        status="active",
        portfolio={
            "positions": {
                "600519": 100,  # 贵州茅台
                "300750": 150,  # 宁德时代
                "002594": 200   # 比亚迪
            },
            "cash": 12500.0
        },
        total_return=0.05,
        config={}
    )
    
    # 生成实盘交易报告 / Generate live trading report
    report = generator.generate_live_trading_report(trading_session)
    print(report)
    
    print("\n✓ 实盘交易报告生成成功 / Live trading report generated successfully")


def demo_html_report():
    """演示HTML报告生成 / Demonstrate HTML report generation"""
    print("\n" + "=" * 80)
    print("演示HTML报告生成 / Demonstrating HTML Report Generation")
    print("=" * 80)
    
    # 创建报告生成器 / Create report generator
    generator = ReportGenerator(output_dir="./outputs/reports")
    
    # 创建模拟回测结果 / Create mock backtest result
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    returns = pd.Series(
        np.random.normal(0.001, 0.02, len(dates)),
        index=dates
    )
    
    benchmark_returns = pd.Series(
        np.random.normal(0.0005, 0.015, len(dates)),
        index=dates
    )
    
    positions = pd.DataFrame()
    
    # 计算指标 / Calculate metrics
    cumulative_returns = (1 + returns).cumprod()
    total_return = cumulative_returns.iloc[-1] - 1
    annual_return = (1 + total_return) ** (252 / len(returns)) - 1
    volatility = returns.std() * np.sqrt(252)
    sharpe_ratio = annual_return / volatility if volatility > 0 else 0
    
    running_max = cumulative_returns.expanding().max()
    drawdown = (cumulative_returns - running_max) / running_max
    max_drawdown = drawdown.min()
    
    win_rate = (returns > 0).sum() / len(returns)
    
    benchmark_cumulative = (1 + benchmark_returns).cumprod()
    benchmark_return = benchmark_cumulative.iloc[-1] - 1
    excess_return = total_return - benchmark_return
    
    backtest_result = BacktestResult(
        returns=returns,
        positions=positions,
        metrics={
            "total_return": total_return,
            "annual_return": annual_return,
            "volatility": volatility,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown,
            "win_rate": win_rate,
            "benchmark_return": benchmark_return,
            "excess_return": excess_return
        },
        trades=[],
        benchmark_returns=benchmark_returns
    )
    
    # 生成HTML报告 / Generate HTML report
    output_path = "./outputs/reports/backtest_report.html"
    generator.generate_html_report(backtest_result, output_path)
    
    print(f"\n✓ HTML报告生成成功 / HTML report generated successfully")
    print(f"报告路径 / Report path: {output_path}")


def demo_comparison_report():
    """演示对比报告生成 / Demonstrate comparison report generation"""
    print("\n" + "=" * 80)
    print("演示对比报告生成 / Demonstrating Comparison Report Generation")
    print("=" * 80)
    
    # 创建报告生成器 / Create report generator
    generator = ReportGenerator(output_dir="./outputs/reports")
    
    # 创建多个模拟回测结果 / Create multiple mock backtest results
    results = []
    
    for i in range(3):
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        returns = pd.Series(
            np.random.normal(0.001 * (i + 1), 0.02, len(dates)),
            index=dates
        )
        
        positions = pd.DataFrame()
        
        cumulative_returns = (1 + returns).cumprod()
        total_return = cumulative_returns.iloc[-1] - 1
        annual_return = (1 + total_return) ** (252 / len(returns)) - 1
        volatility = returns.std() * np.sqrt(252)
        sharpe_ratio = annual_return / volatility if volatility > 0 else 0
        
        running_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = drawdown.min()
        
        result = BacktestResult(
            returns=returns,
            positions=positions,
            metrics={
                "total_return": total_return,
                "annual_return": annual_return,
                "volatility": volatility,
                "sharpe_ratio": sharpe_ratio,
                "max_drawdown": max_drawdown
            },
            trades=[]
        )
        
        results.append(result)
    
    # 生成对比报告 / Generate comparison report
    report = generator.generate_comparison_report(results)
    print(report)
    
    print("\n✓ 对比报告生成成功 / Comparison report generated successfully")


def main():
    """主函数 / Main function"""
    print("\n" + "=" * 80)
    print("报告生成器演示程序 / Report Generator Demo Program".center(80))
    print("=" * 80)
    
    # 设置日志 / Setup logger
    setup_logging(log_dir="./logs", log_level="INFO")
    
    try:
        # 演示各种报告生成 / Demonstrate various report generation
        demo_training_report()
        demo_backtest_report()
        demo_simulation_report()
        demo_live_trading_report()
        demo_html_report()
        demo_comparison_report()
        
        print("\n" + "=" * 80)
        print("所有演示完成 / All demonstrations completed".center(80))
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误 / Error occurred during demonstration: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
