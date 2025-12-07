#!/usr/bin/env python3
"""
模拟交易完整示例 / Complete Simulation Trading Example

本示例展示如何使用系统进行完整的模拟交易流程
This example demonstrates how to use the system for a complete simulation trading process

功能包括 / Features include:
1. 加载配置和模型 / Load configuration and model
2. 创建模拟交易会话 / Create simulation trading session
3. 执行每日交易信号 / Execute daily trading signals
4. 跟踪持仓和收益 / Track positions and returns
5. 生成模拟报告 / Generate simulation reports
6. 参数调整和重新测试 / Parameter adjustment and retesting

使用方法 / Usage:
    python examples/simulation_demo.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

# 添加src到路径 / Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from application.simulation_engine import SimulationEngine
from application.model_registry import ModelRegistry
from application.config_manager import ConfigManager
from application.logger_system import LoggerSystem


def print_section(title):
    """
    打印章节标题
    Print section title
    """
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def display_simulation_config(config):
    """
    显示模拟配置
    Display simulation configuration
    """
    print("模拟交易配置 / Simulation Configuration:")
    print("-" * 80)
    print(f"初始资金 / Initial Capital: ¥{config['initial_capital']:,.0f}")
    print(f"模拟周期 / Simulation Period: {config['start_date']} 到 {config['end_date']}")
    print(f"交易频率 / Trading Frequency: {config.get('trading_frequency', 'daily')}")
    print(f"最大持仓数 / Max Positions: {config.get('max_positions', 10)}")
    print(f"单只股票最大仓位 / Max Single Position: {config.get('max_single_position', 0.3)*100:.0f}%")
    print(f"止损比例 / Stop Loss: {config.get('stop_loss_pct', 0.05)*100:.0f}%")
    print("-" * 80)


def display_daily_summary(day_num, date, portfolio_value, daily_return, positions):
    """
    显示每日摘要
    Display daily summary
    """
    print(f"\n第 {day_num} 天 / Day {day_num} - {date}")
    print("-" * 60)
    print(f"组合价值 / Portfolio Value: ¥{portfolio_value:,.2f}")
    print(f"当日收益率 / Daily Return: {daily_return:+.2%}")
    print(f"持仓数量 / Number of Positions: {len(positions)}")
    
    if positions:
        print("\n当前持仓 / Current Positions:")
        for symbol, pos in list(positions.items())[:5]:  # 显示前5个
            print(f"  {symbol}: {pos['quantity']} 股, "
                  f"成本 ¥{pos['cost']:.2f}, "
                  f"现价 ¥{pos['current_price']:.2f}, "
                  f"盈亏 {pos['pnl']:+.2%}")
        if len(positions) > 5:
            print(f"  ... 还有 {len(positions)-5} 个持仓")


def display_final_results(results):
    """
    显示最终结果
    Display final results
    """
    print_section("模拟交易最终结果 / Final Simulation Results")
    
    print("收益指标 / Return Metrics:")
    print("-" * 80)
    print(f"总收益率 / Total Return: {results['total_return']:+.2%}")
    print(f"年化收益率 / Annualized Return: {results['annual_return']:+.2%}")
    print(f"最大回撤 / Max Drawdown: {results['max_drawdown']:.2%}")
    print(f"夏普比率 / Sharpe Ratio: {results['sharpe_ratio']:.2f}")
    print(f"胜率 / Win Rate: {results['win_rate']:.2%}")
    
    print("\n交易统计 / Trading Statistics:")
    print("-" * 80)
    print(f"总交易次数 / Total Trades: {results['total_trades']}")
    print(f"盈利交易 / Winning Trades: {results['winning_trades']}")
    print(f"亏损交易 / Losing Trades: {results['losing_trades']}")
    print(f"平均持仓天数 / Avg Holding Days: {results['avg_holding_days']:.1f}")
    print(f"换手率 / Turnover Rate: {results['turnover_rate']:.2%}")
    
    print("\n风险指标 / Risk Metrics:")
    print("-" * 80)
    print(f"波动率 / Volatility: {results['volatility']:.2%}")
    print(f"VaR (95%) / VaR (95%): {results['var_95']:.2%}")
    print(f"最大单日亏损 / Max Daily Loss: {results['max_daily_loss']:.2%}")


def main():
    """
    主函数 / Main function
    """
    print("\n" + "="*80)
    print("  模拟交易完整示例 / Complete Simulation Trading Example")
    print("="*80)
    
    try:
        # 步骤1: 初始化系统 / Step 1: Initialize system
        print_section("步骤1: 初始化系统 / Step 1: Initialize System")
        
        # 初始化日志系统 / Initialize logging system
        logger = LoggerSystem()
        logger.info("开始模拟交易演示 / Starting simulation trading demo")
        
        # 加载配置 / Load configuration
        config_manager = ConfigManager()
        config = config_manager.load_config()
        print("✅ 配置加载成功 / Configuration loaded successfully")
        
        # 步骤2: 选择模型 / Step 2: Select model
        print_section("步骤2: 选择模型 / Step 2: Select Model")
        
        registry = ModelRegistry()
        models = registry.list_models()
        
        if not models:
            print("❌ 没有找到已训练的模型 / No trained models found")
            print("请先运行训练示例: python examples/demo_complete_training.py")
            print("Please run training example first: python examples/demo_complete_training.py")
            return
        
        print(f"找到 {len(models)} 个模型 / Found {len(models)} models:")
        for i, model_info in enumerate(models[:5], 1):
            print(f"{i}. {model_info['name']} (v{model_info['version']}) - "
                  f"训练于 {model_info['trained_at']}")
        
        # 使用最新的模型 / Use the latest model
        selected_model = models[0]
        print(f"\n✅ 选择模型 / Selected model: {selected_model['name']} v{selected_model['version']}")
        
        # 加载模型 / Load model
        model = registry.load_model(selected_model['name'], selected_model['version'])
        print("✅ 模型加载成功 / Model loaded successfully")
        
        # 步骤3: 配置模拟参数 / Step 3: Configure simulation parameters
        print_section("步骤3: 配置模拟参数 / Step 3: Configure Simulation Parameters")
        
        # 模拟配置 / Simulation configuration
        sim_config = {
            'initial_capital': 500000,  # 初始资金50万
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'trading_frequency': 'daily',
            'max_positions': 10,
            'max_single_position': 0.3,
            'stop_loss_pct': 0.05,
            'commission_rate': 0.0003,
            'slippage': 0.001
        }
        
        display_simulation_config(sim_config)
        
        # 步骤4: 创建模拟引擎 / Step 4: Create simulation engine
        print_section("步骤4: 创建模拟引擎 / Step 4: Create Simulation Engine")
        
        engine = SimulationEngine(
            model=model,
            config=sim_config,
            logger=logger
        )
        print("✅ 模拟引擎创建成功 / Simulation engine created successfully")
        
        # 步骤5: 运行模拟交易 / Step 5: Run simulation trading
        print_section("步骤5: 运行模拟交易 / Step 5: Run Simulation Trading")
        
        print("开始模拟交易... / Starting simulation trading...")
        print("(这可能需要几分钟，取决于模拟周期长度)")
        print("(This may take a few minutes depending on simulation period)")
        
        # 创建模拟会话 / Create simulation session
        session_id = engine.create_session(
            name="Demo Simulation",
            description="完整的模拟交易演示 / Complete simulation trading demo"
        )
        print(f"\n✅ 创建会话 / Session created: {session_id}")
        
        # 运行模拟 / Run simulation
        print("\n执行模拟交易 / Executing simulation trading...")
        print("-" * 80)
        
        # 模拟每日交易 / Simulate daily trading
        trading_days = pd.date_range(
            start=sim_config['start_date'],
            end=sim_config['end_date'],
            freq='B'  # 工作日
        )
        
        for day_num, date in enumerate(trading_days[:10], 1):  # 演示前10天
            # 生成信号并执行交易 / Generate signals and execute trades
            result = engine.execute_daily_trading(date.strftime('%Y-%m-%d'))
            
            # 显示每日摘要 / Display daily summary
            if day_num % 5 == 0 or day_num <= 3:  # 显示前3天和每5天
                display_daily_summary(
                    day_num,
                    date.strftime('%Y-%m-%d'),
                    result['portfolio_value'],
                    result['daily_return'],
                    result['positions']
                )
        
        print("\n...")
        print(f"继续执行剩余 {len(trading_days)-10} 个交易日...")
        print(f"Continuing with remaining {len(trading_days)-10} trading days...")
        
        # 执行完整模拟（实际应用中）/ Execute full simulation (in real application)
        # for date in trading_days[10:]:
        #     engine.execute_daily_trading(date.strftime('%Y-%m-%d'))
        
        print("\n✅ 模拟交易完成 / Simulation trading completed")
        
        # 步骤6: 生成模拟报告 / Step 6: Generate simulation report
        print_section("步骤6: 生成模拟报告 / Step 6: Generate Simulation Report")
        
        # 获取模拟结果 / Get simulation results
        results = engine.get_simulation_results(session_id)
        
        # 显示最终结果 / Display final results
        display_final_results(results)
        
        # 保存报告 / Save report
        report_path = engine.generate_report(session_id)
        print(f"\n✅ 报告已保存 / Report saved to: {report_path}")
        
        # 步骤7: 参数调整建议 / Step 7: Parameter adjustment suggestions
        print_section("步骤7: 参数调整建议 / Step 7: Parameter Adjustment Suggestions")
        
        print("基于模拟结果的参数调整建议 / Parameter adjustment suggestions based on results:")
        print("-" * 80)
        
        if results['sharpe_ratio'] < 1.0:
            print("⚠️  夏普比率较低，建议:")
            print("   - 增加止损比例以控制风险")
            print("   - 减少持仓数量以提高选股质量")
            print("   - 调整信号阈值以提高信号质量")
        
        if results['max_drawdown'] > 0.15:
            print("⚠️  最大回撤较大，建议:")
            print("   - 降低单只股票最大仓位")
            print("   - 增加现金比例")
            print("   - 使用更严格的止损策略")
        
        if results['win_rate'] < 0.45:
            print("⚠️  胜率较低，建议:")
            print("   - 提高信号置信度阈值")
            print("   - 优化模型参数")
            print("   - 增加特征工程")
        
        if results['sharpe_ratio'] >= 1.5 and results['max_drawdown'] < 0.10:
            print("✅ 模拟结果良好，可以考虑:")
            print("   - 适当增加仓位")
            print("   - 进入实盘交易")
            print("   - 继续监控和优化")
        
        # 步骤8: 重新测试选项 / Step 8: Retest options
        print_section("步骤8: 重新测试选项 / Step 8: Retest Options")
        
        print("如果需要调整参数并重新测试:")
        print("If you need to adjust parameters and retest:")
        print("-" * 80)
        print("1. 修改 sim_config 中的参数")
        print("   Modify parameters in sim_config")
        print("2. 重新运行此脚本")
        print("   Re-run this script")
        print("3. 比较不同参数下的结果")
        print("   Compare results under different parameters")
        
        # 总结 / Summary
        print_section("总结 / Summary")
        
        print("✅ 模拟交易演示完成 / Simulation trading demo completed")
        print("\n关键要点 / Key takeaways:")
        print("1. 模拟交易是实盘前的必要步骤")
        print("   Simulation trading is a necessary step before live trading")
        print("2. 至少进行30天的模拟交易")
        print("   Conduct at least 30 days of simulation trading")
        print("3. 根据模拟结果调整参数")
        print("   Adjust parameters based on simulation results")
        print("4. 确保风险指标在可接受范围内")
        print("   Ensure risk metrics are within acceptable ranges")
        print("5. 模拟成功后再进入实盘")
        print("   Enter live trading only after successful simulation")
        
        print("\n下一步 / Next steps:")
        print("- 查看详细报告: " + report_path)
        print("  View detailed report: " + report_path)
        print("- 调整参数并重新测试")
        print("  Adjust parameters and retest")
        print("- 准备实盘交易: python examples/live_trading_demo.py")
        print("  Prepare for live trading: python examples/live_trading_demo.py")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  演示被用户中断 / Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ 错误 / Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
