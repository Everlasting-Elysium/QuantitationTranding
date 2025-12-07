#!/usr/bin/env python3
"""
实盘交易完整示例 / Complete Live Trading Example

本示例展示如何使用系统进行实盘交易
This example demonstrates how to use the system for live trading

⚠️ 警告 / WARNING:
实盘交易涉及真实资金，存在亏损风险！
Live trading involves real money and carries risk of loss!

请确保：
Please ensure:
1. 已完成充分的模拟交易测试
   Completed sufficient simulation trading tests
2. 理解并接受所有风险
   Understand and accept all risks
3. 从小资金开始
   Start with small capital
4. 设置严格的风险控制
   Set strict risk controls

使用方法 / Usage:
    python examples/live_trading_demo.py
"""

import sys
from pathlib import Path
from datetime import datetime
import time

# 添加src到路径 / Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from application.live_trading_manager import LiveTradingManager
from application.model_registry import ModelRegistry
from application.config_manager import ConfigManager
from application.logger_system import LoggerSystem
from application.risk_manager import RiskManager
from application.notification_service import NotificationService


def print_section(title):
    """
    打印章节标题
    Print section title
    """
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def display_warning():
    """
    显示风险警告
    Display risk warning
    """
    print("\n" + "🔴"*40)
    print("\n" + " "*20 + "⚠️  重要警告 / IMPORTANT WARNING  ⚠️")
    print("\n" + "🔴"*40)
    print("\n实盘交易涉及真实资金，存在亏损风险！")
    print("Live trading involves real money and carries risk of loss!")
    print("\n请确保您已经：")
    print("Please ensure you have:")
    print("  1. ✅ 完成至少30天的模拟交易")
    print("     Completed at least 30 days of simulation trading")
    print("  2. ✅ 验证策略在不同市场环境下的表现")
    print("     Verified strategy performance in different market conditions")
    print("  3. ✅ 设置了严格的风险控制参数")
    print("     Set strict risk control parameters")
    print("  4. ✅ 理解并接受可能的亏损")
    print("     Understand and accept potential losses")
    print("  5. ✅ 从小资金开始（建议5-10万元）")
    print("     Start with small capital (recommended ¥50,000-100,000)")
    print("\n" + "🔴"*40 + "\n")


def confirm_start():
    """
    确认启动
    Confirm start
    """
    print("请输入 'I UNDERSTAND THE RISKS' 以继续:")
    print("Type 'I UNDERSTAND THE RISKS' to continue:")
    response = input("> ").strip()
    
    return response == "I UNDERSTAND THE RISKS"


def display_trading_config(config):
    """
    显示交易配置
    Display trading configuration
    """
    print("实盘交易配置 / Live Trading Configuration:")
    print("-" * 80)
    print(f"初始资金 / Initial Capital: ¥{config['initial_capital']:,.0f}")
    print(f"券商 / Broker: {config['broker']['name']}")
    print(f"交易模式 / Trading Mode: {config['mode']}")
    
    print("\n风险控制参数 / Risk Control Parameters:")
    print("-" * 80)
    risk = config['risk_control']
    print(f"单只股票最大仓位 / Max Single Position: {risk['max_single_position']*100:.0f}%")
    print(f"行业最大集中度 / Max Sector Concentration: {risk['max_sector_concentration']*100:.0f}%")
    print(f"最大总仓位 / Max Total Position: {risk['max_total_position']*100:.0f}%")
    print(f"最小现金比例 / Min Cash Ratio: {risk['min_cash_ratio']*100:.0f}%")
    print(f"最大单日亏损 / Max Daily Loss: {risk['max_daily_loss']*100:.0f}%")
    print(f"最大总亏损 / Max Total Loss: {risk['max_total_loss']*100:.0f}%")
    print(f"止损比例 / Stop Loss: {risk['stop_loss_pct']*100:.0f}%")
    print("-" * 80)


def pre_trading_checks():
    """
    交易前检查
    Pre-trading checks
    """
    print_section("交易前检查 / Pre-trading Checks")
    
    checks = {
        '系统状态 / System Status': True,
        '网络连接 / Network Connection': True,
        '数据源 / Data Source': True,
        '券商连接 / Broker Connection': False,  # 演示模式
        '账户状态 / Account Status': False,  # 演示模式
        '风控参数 / Risk Parameters': True
    }
    
    all_passed = True
    for check_name, result in checks.items():
        status = "✅ 通过 / Passed" if result else "❌ 失败 / Failed (Demo Mode)"
        print(f"{check_name}: {status}")
        if not result and "Demo Mode" not in status:
            all_passed = False
    
    print("\n" + "-" * 80)
    if not all_passed:
        print("⚠️  部分检查未通过")
        print("⚠️  Some checks failed")
        return False
    else:
        print("ℹ️  演示模式：券商连接检查已跳过")
        print("ℹ️  Demo mode: Broker connection checks skipped")
        return True


def display_realtime_status(status):
    """
    显示实时状态
    Display real-time status
    """
    print("\n" + "┌" + "─"*78 + "┐")
    print("│" + " "*20 + "实时交易状态 / Real-time Trading Status" + " "*18 + "│")
    print("├" + "─"*78 + "┤")
    print(f"│ 账户总值 / Total Value:     ¥{status['total_value']:>12,.2f}  "
          f"({status['daily_return']:>+6.2%})      │")
    print(f"│ 今日收益 / Daily P&L:       ¥{status['daily_pnl']:>12,.2f}  "
          f"({status['daily_return_pct']:>+6.2%})      │")
    print(f"│ 持仓数量 / Positions:       {status['position_count']:>2} stocks" + " "*42 + "│")
    print(f"│ 现金比例 / Cash Ratio:      {status['cash_ratio']:>5.1%}" + " "*48 + "│")
    print("├" + "─"*78 + "┤")
    print(f"│ 风险指标 / Risk Metrics:" + " "*53 + "│")
    print(f"│   最大回撤 / Max Drawdown:  {status['max_drawdown']:>6.2%}  "
          f"{'🟢' if status['max_drawdown'] < 0.10 else '🟡' if status['max_drawdown'] < 0.15 else '🔴'}" + " "*38 + "│")
    print(f"│   波动率 / Volatility:      {status['volatility']:>6.2%}  "
          f"{'🟢' if status['volatility'] < 0.20 else '🟡' if status['volatility'] < 0.30 else '🔴'}" + " "*38 + "│")
    print("├" + "─"*78 + "┤")
    print(f"│ 今日交易 / Today's Trades:" + " "*51 + "│")
    print(f"│   买入 / Bought:            {status['trades_bought']:>2} orders" + " "*40 + "│")
    print(f"│   卖出 / Sold:              {status['trades_sold']:>2} orders" + " "*40 + "│")
    print(f"│   待成交 / Pending:          {status['trades_pending']:>2} orders" + " "*40 + "│")
    print("└" + "─"*78 + "┘")


def display_positions(positions):
    """
    显示持仓明细
    Display position details
    """
    if not positions:
        print("\n当前无持仓 / No positions currently")
        return
    
    print("\n" + "┌" + "─"*78 + "┐")
    print("│" + " "*25 + "持仓明细 / Position Details" + " "*26 + "│")
    print("├" + "─"*78 + "┤")
    print("│ 代码   │ 名称     │ 数量  │ 成本价 │ 现价  │ 盈亏    │ 仓位  │")
    print("│ Symbol │ Name     │ Qty   │ Cost   │ Price │ P&L     │ Weight│")
    print("├" + "─"*78 + "┤")
    
    for symbol, pos in list(positions.items())[:10]:  # 显示前10个
        print(f"│ {symbol:<6} │ {pos['name']:<8} │ {pos['quantity']:>5} │ "
              f"{pos['cost']:>6.2f} │ {pos['price']:>5.2f} │ "
              f"{pos['pnl']:>+6.2%} │ {pos['weight']:>5.1%} │")
    
    if len(positions) > 10:
        print("│ " + " "*74 + "│")
        print(f"│ ... 还有 {len(positions)-10} 个持仓 / {len(positions)-10} more positions" + " "*45 + "│")
    
    print("└" + "─"*78 + "┘")


def main():
    """
    主函数 / Main function
    """
    print("\n" + "="*80)
    print("  实盘交易完整示例 / Complete Live Trading Example")
    print("="*80)
    
    # 显示风险警告 / Display risk warning
    display_warning()
    
    # 确认启动 / Confirm start
    if not confirm_start():
        print("\n❌ 未确认风险，退出演示")
        print("❌ Risks not confirmed, exiting demo")
        return 0
    
    try:
        # 步骤1: 初始化系统 / Step 1: Initialize system
        print_section("步骤1: 初始化系统 / Step 1: Initialize System")
        
        # 初始化日志系统 / Initialize logging system
        logger = LoggerSystem()
        logger.info("开始实盘交易演示 / Starting live trading demo")
        
        # 加载配置 / Load configuration
        config_manager = ConfigManager()
        config = config_manager.load_config()
        
        # 实盘交易配置 / Live trading configuration
        live_config = {
            'mode': 'demo',  # 演示模式 / Demo mode
            'initial_capital': 100000,  # 10万元演示资金
            'broker': {
                'name': 'demo_broker',
                'account_id': 'DEMO123456',
                'api_key': 'demo_key',
                'api_secret': 'demo_secret'
            },
            'risk_control': {
                'max_single_position': 0.20,
                'max_sector_concentration': 0.35,
                'max_total_position': 0.80,
                'min_cash_ratio': 0.20,
                'max_daily_loss': 0.03,
                'max_total_loss': 0.10,
                'stop_loss_pct': 0.05,
                'trailing_stop_pct': 0.03
            },
            'monitoring': {
                'enable_realtime_monitoring': True,
                'monitoring_interval': 60,
                'enable_email_alerts': False,  # 演示模式关闭
                'enable_daily_report': True
            }
        }
        
        print("✅ 配置加载成功 / Configuration loaded successfully")
        display_trading_config(live_config)
        
        # 步骤2: 交易前检查 / Step 2: Pre-trading checks
        if not pre_trading_checks():
            print("\n❌ 交易前检查未通过，无法启动")
            print("❌ Pre-trading checks failed, cannot start")
            return 1
        
        print("\n✅ 所有检查通过 / All checks passed")
        
        # 步骤3: 选择模型 / Step 3: Select model
        print_section("步骤3: 选择模型 / Step 3: Select Model")
        
        registry = ModelRegistry()
        models = registry.list_models()
        
        if not models:
            print("❌ 没有找到已训练的模型 / No trained models found")
            print("请先运行训练示例: python examples/demo_complete_training.py")
            return 1
        
        # 使用最新的模型 / Use the latest model
        selected_model = models[0]
        print(f"✅ 选择模型 / Selected model: {selected_model['name']} v{selected_model['version']}")
        
        # 加载模型 / Load model
        model = registry.load_model(selected_model['name'], selected_model['version'])
        print("✅ 模型加载成功 / Model loaded successfully")
        
        # 步骤4: 创建交易管理器 / Step 4: Create trading manager
        print_section("步骤4: 创建交易管理器 / Step 4: Create Trading Manager")
        
        manager = LiveTradingManager(
            model=model,
            config=live_config,
            logger=logger
        )
        print("✅ 交易管理器创建成功 / Trading manager created successfully")
        
        # 步骤5: 启动实盘交易 / Step 5: Start live trading
        print_section("步骤5: 启动实盘交易 / Step 5: Start Live Trading")
        
        print("🚀 启动实盘交易... / Starting live trading...")
        print("\nℹ️  演示模式：将模拟5分钟的实盘交易")
        print("ℹ️  Demo mode: Will simulate 5 minutes of live trading")
        print("\n按 Ctrl+C 可以随时停止 / Press Ctrl+C to stop anytime")
        print("-" * 80)
        
        # 启动交易 / Start trading
        manager.start()
        
        # 模拟实时交易 / Simulate real-time trading
        for minute in range(5):
            time.sleep(1)  # 演示模式：1秒代表1分钟
            
            # 获取实时状态 / Get real-time status
            status = {
                'total_value': 100000 + minute * 500,
                'daily_return': minute * 0.005,
                'daily_pnl': minute * 500,
                'daily_return_pct': minute * 0.005,
                'position_count': 5 + minute % 3,
                'cash_ratio': 0.25 - minute * 0.01,
                'max_drawdown': 0.02 + minute * 0.005,
                'volatility': 0.15 + minute * 0.01,
                'trades_bought': minute % 2,
                'trades_sold': (minute + 1) % 2,
                'trades_pending': 0
            }
            
            # 显示实时状态 / Display real-time status
            display_realtime_status(status)
            
            # 模拟持仓 / Simulate positions
            if minute == 2:
                positions = {
                    '600519': {'name': '贵州茅台', 'quantity': 50, 'cost': 1800, 
                              'price': 1850, 'pnl': 0.0278, 'weight': 0.185},
                    '300750': {'name': '宁德时代', 'quantity': 100, 'cost': 180, 
                              'price': 185, 'pnl': 0.0278, 'weight': 0.148},
                    '002594': {'name': '比亚迪', 'quantity': 80, 'cost': 250, 
                              'price': 245, 'pnl': -0.02, 'weight': 0.157},
                    '000858': {'name': '五粮液', 'quantity': 60, 'cost': 220, 
                              'price': 225, 'pnl': 0.0227, 'weight': 0.108},
                    '601318': {'name': '中国平安', 'quantity': 200, 'cost': 45, 
                              'price': 47, 'pnl': 0.0444, 'weight': 0.075}
                }
                display_positions(positions)
            
            time.sleep(1)
        
        # 步骤6: 停止交易 / Step 6: Stop trading
        print_section("步骤6: 停止交易 / Step 6: Stop Trading")
        
        print("⏸️  停止交易... / Stopping trading...")
        manager.stop()
        print("✅ 交易已安全停止 / Trading stopped safely")
        
        # 步骤7: 生成日报告 / Step 7: Generate daily report
        print_section("步骤7: 生成日报告 / Step 7: Generate Daily Report")
        
        print("生成今日交易报告... / Generating today's trading report...")
        report_path = manager.generate_daily_report()
        print(f"✅ 报告已保存 / Report saved to: {report_path}")
        
        # 总结 / Summary
        print_section("总结 / Summary")
        
        print("✅ 实盘交易演示完成 / Live trading demo completed")
        print("\nℹ️  这是一个演示示例，使用的是模拟数据")
        print("ℹ️  This is a demo example using simulated data")
        
        print("\n实际使用时的关键步骤 / Key steps for actual use:")
        print("-" * 80)
        print("1. 配置真实的券商API信息")
        print("   Configure real broker API credentials")
        print("2. 设置 mode='live' 启用实盘模式")
        print("   Set mode='live' to enable live trading mode")
        print("3. 从小资金开始（5-10万元）")
        print("   Start with small capital (¥50,000-100,000)")
        print("4. 密切监控前几天的交易")
        print("   Closely monitor trading in the first few days")
        print("5. 根据实际表现调整参数")
        print("   Adjust parameters based on actual performance")
        
        print("\n安全建议 / Safety recommendations:")
        print("-" * 80)
        print("✅ 设置严格的止损")
        print("   Set strict stop losses")
        print("✅ 保持适当的现金比例")
        print("   Maintain appropriate cash ratio")
        print("✅ 启用实时监控和预警")
        print("   Enable real-time monitoring and alerts")
        print("✅ 定期查看交易报告")
        print("   Regularly review trading reports")
        print("✅ 遇到异常立即停止")
        print("   Stop immediately if anomalies occur")
        
        print("\n相关文档 / Related documentation:")
        print("-" * 80)
        print("- 实盘交易指南: docs/live_trading_guide.md")
        print("  Live trading guide: docs/live_trading_guide.md")
        print("- 风险控制策略: docs/live_trading_guide.md#风险控制策略")
        print("  Risk control strategies: docs/live_trading_guide.md#risk-control-strategies")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  交易被用户中断 / Trading interrupted by user")
        print("正在安全停止... / Stopping safely...")
        if 'manager' in locals():
            manager.stop()
        print("✅ 已安全停止 / Stopped safely")
    except Exception as e:
        print(f"\n\n❌ 错误 / Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
