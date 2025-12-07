"""
Demo script for Live Trading Manager / 实盘交易管理器演示脚本

This script demonstrates how to use the LiveTradingManager for live trading.
本脚本演示如何使用LiveTradingManager进行实盘交易。

Usage / 使用方法:
    python examples/demo_live_trading_manager.py
"""

import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.application.live_trading_manager import LiveTradingManager
from src.core.portfolio_manager import PortfolioManager
from src.core.risk_manager import RiskManager
from src.infrastructure.trading_api_adapter import TradingAPIAdapter
from src.infrastructure.logger_system import LoggerSystem
from src.models.trading_models import LiveTradingConfig, Signal


def main():
    """Main demo function / 主演示函数"""
    
    print("=" * 80)
    print("Live Trading Manager Demo / 实盘交易管理器演示")
    print("=" * 80)
    print()
    
    # Initialize components / 初始化组件
    print("1. Initializing components / 初始化组件...")
    logger_system = LoggerSystem()
    logger_system.setup(log_dir="logs", log_level="INFO")
    
    portfolio_manager = PortfolioManager(logger=logger_system)
    risk_manager = RiskManager(
        max_position_pct=0.3,
        max_sector_pct=0.4,
        max_drawdown_pct=0.2,
        max_daily_loss_pct=0.05,
        logger=logger_system
    )
    trading_api = TradingAPIAdapter()
    
    live_trading_manager = LiveTradingManager(
        portfolio_manager=portfolio_manager,
        risk_manager=risk_manager,
        trading_api=trading_api,
        logger=logger_system
    )
    print("✓ Components initialized / 组件已初始化")
    print()
    
    # Create trading configuration / 创建交易配置
    print("2. Creating trading configuration / 创建交易配置...")
    trading_config = LiveTradingConfig(
        broker="mock",  # Use mock broker for demo
        credentials={"account": "demo_account"},
        max_position_size=0.3,
        max_daily_trades=10,
        stop_loss_pct=0.05,
        take_profit_pct=0.10,
        trading_hours={"start": "09:30", "end": "15:00"}
    )
    print("✓ Trading configuration created / 交易配置已创建")
    print()
    
    # Start live trading session / 启动实盘交易会话
    print("3. Starting live trading session / 启动实盘交易会话...")
    session = live_trading_manager.start_live_trading(
        model_id="lgbm_model_v1",
        initial_capital=100000.0,
        trading_config=trading_config
    )
    print(f"✓ Trading session started: {session.session_id}")
    print(f"  Model: {session.model_id}")
    print(f"  Initial capital: ¥{session.initial_capital:,.2f}")
    print(f"  Status: {session.status}")
    print()
    
    # Create some trading signals / 创建一些交易信号
    print("4. Creating trading signals / 创建交易信号...")
    signals = [
        Signal(
            stock_code="600519",  # 贵州茅台
            action="buy",
            score=0.85,
            confidence=0.90,
            timestamp=datetime.now().isoformat()
        ),
        Signal(
            stock_code="300750",  # 宁德时代
            action="buy",
            score=0.78,
            confidence=0.85,
            timestamp=datetime.now().isoformat()
        ),
        Signal(
            stock_code="000001",  # 平安银行
            action="buy",
            score=0.65,
            confidence=0.75,
            timestamp=datetime.now().isoformat()
        )
    ]
    print(f"✓ Created {len(signals)} trading signals")
    print()
    
    # Execute trades / 执行交易
    print("5. Executing trades / 执行交易...")
    results = live_trading_manager.execute_batch_trades(
        session_id=session.session_id,
        signals=signals
    )
    
    print(f"✓ Executed {len(results)} trades:")
    for result in results:
        print(f"  - {result.action.upper()} {result.symbol}: "
              f"{result.quantity} shares @ ¥{result.price:.2f} "
              f"(Status: {result.status})")
    print()
    
    # Get current positions / 获取当前持仓
    print("6. Getting current positions / 获取当前持仓...")
    portfolio = live_trading_manager.get_current_positions(session.session_id)
    print(f"✓ Current portfolio:")
    print(f"  Total value: ¥{portfolio.total_value:,.2f}")
    print(f"  Cash: ¥{portfolio.cash:,.2f}")
    print(f"  Positions: {len(portfolio.positions)}")
    for symbol, pos in portfolio.positions.items():
        print(f"    - {symbol}: {pos.quantity} shares @ ¥{pos.current_price:.2f} "
              f"(P&L: {pos.unrealized_pnl_pct:+.2f}%)")
    print()
    
    # Get trading status / 获取交易状态
    print("7. Getting trading status / 获取交易状态...")
    status = live_trading_manager.get_trading_status(session.session_id)
    print(f"✓ Trading status:")
    print(f"  Session ID: {status.session_id}")
    print(f"  Active: {status.is_active}")
    print(f"  Current value: ¥{status.current_value:,.2f}")
    print(f"  Total return: {status.total_return:+.2f}%")
    print(f"  Positions: {status.positions_count}")
    print(f"  Cash: ¥{status.cash_balance:,.2f}")
    print()
    
    # Check risk alerts / 检查风险预警
    print("8. Checking risk alerts / 检查风险预警...")
    alert = live_trading_manager.check_risk_alerts(session.session_id)
    if alert:
        print(f"⚠ Risk alert detected:")
        print(f"  Severity: {alert['severity']}")
        print(f"  Message: {alert['message']}")
        print(f"  Affected positions: {', '.join(alert['affected_positions'])}")
    else:
        print("✓ No risk alerts")
    print()
    
    # Pause trading / 暂停交易
    print("9. Pausing trading / 暂停交易...")
    live_trading_manager.pause_trading(session.session_id)
    status = live_trading_manager.get_trading_status(session.session_id)
    print(f"✓ Trading paused (Active: {status.is_active})")
    print()
    
    # Resume trading / 恢复交易
    print("10. Resuming trading / 恢复交易...")
    live_trading_manager.resume_trading(session.session_id)
    status = live_trading_manager.get_trading_status(session.session_id)
    print(f"✓ Trading resumed (Active: {status.is_active})")
    print()
    
    # Stop trading / 停止交易
    print("11. Stopping trading session / 停止交易会话...")
    summary = live_trading_manager.stop_trading(session.session_id)
    print(f"✓ Trading session stopped")
    print(f"  Session ID: {summary['session_id']}")
    print(f"  Duration: {summary['start_date']} to {summary['end_date']}")
    print(f"  Initial capital: ¥{summary['initial_capital']:,.2f}")
    print(f"  Final capital: ¥{summary['final_capital']:,.2f}")
    print(f"  Total return: {summary['total_return_pct']:+.2f}%")
    print(f"  Number of trades: {summary['num_trades']}")
    print(f"  Final positions: {summary['num_positions']}")
    print()
    
    print("=" * 80)
    print("Demo completed successfully! / 演示成功完成！")
    print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
