"""
模拟交易引擎演示 / Simulation Engine Demo

演示如何使用模拟交易引擎进行模拟交易测试
Demonstrates how to use the simulation engine for simulation trading tests
"""

import sys
from pathlib import Path

# 添加项目根目录到路径 / Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.application.simulation_engine import SimulationEngine
from src.application.signal_generator import SignalGenerator
from src.application.model_registry import ModelRegistry
from src.core.portfolio_manager import PortfolioManager
from src.infrastructure.qlib_wrapper import QlibWrapper
from src.infrastructure.logger_system import LoggerSystem


def main():
    """
    主函数 / Main Function
    """
    print("=" * 80)
    print("模拟交易引擎演示 / Simulation Engine Demo")
    print("=" * 80)
    
    try:
        # 1. 初始化日志系统 / Initialize logger system
        print("\n1. 初始化日志系统 / Initializing logger system...")
        logger_system = LoggerSystem()
        logger_system.setup(log_dir="./logs", log_level="INFO")
        
        # 2. 初始化Qlib / Initialize Qlib
        print("\n2. 初始化Qlib / Initializing Qlib...")
        qlib_wrapper = QlibWrapper()
        qlib_wrapper.init(
            provider_uri="~/.qlib/qlib_data/cn_data",
            region="cn"
        )
        
        # 3. 初始化组件 / Initialize components
        print("\n3. 初始化组件 / Initializing components...")
        
        # 模型注册表 / Model registry
        model_registry = ModelRegistry(
            registry_dir="./model_registry",
            logger=logger_system
        )
        
        # 投资组合管理器 / Portfolio manager
        portfolio_manager = PortfolioManager(logger=logger_system)
        
        # 信号生成器 / Signal generator
        signal_generator = SignalGenerator(
            model_registry=model_registry,
            qlib_wrapper=qlib_wrapper
        )
        
        # 模拟交易引擎 / Simulation engine
        simulation_engine = SimulationEngine(
            signal_generator=signal_generator,
            portfolio_manager=portfolio_manager,
            qlib_wrapper=qlib_wrapper,
            output_dir="./simulations"
        )
        
        print("✓ 所有组件初始化成功 / All components initialized successfully")
        
        # 4. 启动模拟交易 / Start simulation trading
        print("\n4. 启动模拟交易 / Starting simulation trading...")
        print("-" * 80)
        
        # 假设我们已经有一个训练好的模型 / Assume we have a trained model
        # 这里使用一个示例模型ID / Using an example model ID here
        model_id = "example_model_20240101"
        
        # 模拟参数 / Simulation parameters
        initial_capital = 100000.0  # 初始资金10万 / Initial capital 100k
        simulation_days = 30  # 模拟30天 / Simulate 30 days
        start_date = "2024-01-01"  # 开始日期 / Start date
        
        print(f"模型ID / Model ID: {model_id}")
        print(f"初始资金 / Initial capital: ¥{initial_capital:,.2f}")
        print(f"模拟天数 / Simulation days: {simulation_days}")
        print(f"开始日期 / Start date: {start_date}")
        print()
        
        # 启动模拟 / Start simulation
        session = simulation_engine.start_simulation(
            model_id=model_id,
            initial_capital=initial_capital,
            simulation_days=simulation_days,
            start_date=start_date,
            instruments="csi300",
            top_n=10
        )
        
        print(f"\n✓ 模拟交易会话创建成功 / Simulation session created successfully")
        print(f"会话ID / Session ID: {session.session_id}")
        
        # 5. 查看模拟状态 / Check simulation status
        print("\n5. 查看模拟状态 / Checking simulation status...")
        print("-" * 80)
        
        status = simulation_engine.get_simulation_status(session.session_id)
        
        print(f"状态 / Status: {status['status']}")
        print(f"完成天数 / Days completed: {status['days_completed']}/{status['simulation_days']}")
        print(f"当前价值 / Current value: ¥{status['current_value']:,.2f}")
        print(f"总收益率 / Total return: {status['total_return_pct']:.2f}%")
        print(f"总交易数 / Total trades: {status['total_trades']}")
        
        # 6. 生成模拟报告 / Generate simulation report
        print("\n6. 生成模拟报告 / Generating simulation report...")
        print("-" * 80)
        
        report = simulation_engine.generate_simulation_report(session.session_id)
        
        print(f"\n模拟交易报告 / Simulation Trading Report")
        print(f"{'=' * 80}")
        print(f"会话ID / Session ID: {report.session_id}")
        print(f"\n收益指标 / Return Metrics:")
        print(f"  总收益率 / Total Return: {report.total_return:.2%}")
        print(f"  年化收益率 / Annual Return: {report.annual_return:.2%}")
        print(f"  最终价值 / Final Value: ¥{report.final_portfolio_value:,.2f}")
        print(f"\n风险指标 / Risk Metrics:")
        print(f"  夏普比率 / Sharpe Ratio: {report.sharpe_ratio:.4f}")
        print(f"  最大回撤 / Max Drawdown: {report.max_drawdown:.2%}")
        print(f"  胜率 / Win Rate: {report.win_rate:.2%}")
        print(f"\n交易统计 / Trading Statistics:")
        print(f"  总交易数 / Total Trades: {report.total_trades}")
        print(f"  盈利交易数 / Profitable Trades: {report.profitable_trades}")
        
        # 7. 显示每日收益 / Show daily returns
        print(f"\n每日收益率（前10天）/ Daily Returns (First 10 Days):")
        print(f"{'-' * 80}")
        for i, (date, ret) in enumerate(report.daily_returns.head(10).items()):
            print(f"  {date.strftime('%Y-%m-%d')}: {ret:+.2%}")
        
        # 8. 显示交易历史 / Show trade history
        if report.trade_history:
            print(f"\n交易历史（前10笔）/ Trade History (First 10 Trades):")
            print(f"{'-' * 80}")
            for i, trade in enumerate(report.trade_history[:10]):
                print(f"  {i+1}. {trade.timestamp} | {trade.action.upper()} | "
                      f"{trade.symbol} | {trade.quantity} 股 @ ¥{trade.price:.2f}")
        
        # 9. 列出所有会话 / List all sessions
        print(f"\n9. 列出所有会话 / Listing all sessions...")
        print(f"{'-' * 80}")
        
        sessions = simulation_engine.list_sessions()
        print(f"总会话数 / Total sessions: {len(sessions)}")
        for sess in sessions:
            print(f"  - {sess['session_id']}: {sess['status']} | "
                  f"收益率 / Return: {sess['total_return_pct']:.2f}%")
        
        print(f"\n{'=' * 80}")
        print("✓ 演示完成 / Demo completed successfully")
        print(f"{'=' * 80}")
        
    except Exception as e:
        print(f"\n✗ 错误 / Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
