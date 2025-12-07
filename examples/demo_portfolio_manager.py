"""
Demo script for Portfolio Manager.
投资组合管理器演示脚本

This script demonstrates how to use the PortfolioManager to:
- Create portfolios
- Execute trades (buy/sell)
- Track positions
- Calculate portfolio value
- View trade history

本脚本演示如何使用PortfolioManager：
- 创建投资组合
- 执行交易（买入/卖出）
- 跟踪持仓
- 计算组合价值
- 查看交易历史
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.portfolio_manager import PortfolioManager
from src.infrastructure.logger_system import LoggerSystem


def main():
    """Main demo function / 主演示函数"""
    
    # Initialize logger
    logger_system = LoggerSystem()
    logger_system.setup(log_dir="logs", log_level="INFO")
    
    # Create portfolio manager
    print("=" * 60)
    print("Portfolio Manager Demo / 投资组合管理器演示")
    print("=" * 60)
    print()
    
    manager = PortfolioManager(logger=logger_system)
    
    # 1. Create a portfolio with initial capital
    print("1. Creating portfolio with 100,000 initial capital...")
    print("   创建初始资金为100,000的投资组合...")
    portfolio = manager.create_portfolio(initial_capital=100000.0)
    print(f"   ✓ Portfolio created: {portfolio.portfolio_id}")
    print(f"   ✓ Initial capital: ¥{portfolio.initial_capital:,.2f}")
    print()
    
    # 2. Buy some stocks
    print("2. Buying stocks...")
    print("   买入股票...")
    
    # Buy 贵州茅台
    print("   - Buying 100 shares of 贵州茅台 (600519) @ ¥180.00")
    manager.update_position(
        portfolio.portfolio_id,
        symbol="600519",
        quantity=100,
        price=180.0,
        action="buy",
        commission=5.0
    )
    
    # Buy 宁德时代
    print("   - Buying 200 shares of 宁德时代 (300750) @ ¥50.00")
    manager.update_position(
        portfolio.portfolio_id,
        symbol="300750",
        quantity=200,
        price=50.0,
        action="buy",
        commission=5.0
    )
    
    # Buy 比亚迪
    print("   - Buying 150 shares of 比亚迪 (002594) @ ¥80.00")
    manager.update_position(
        portfolio.portfolio_id,
        symbol="002594",
        quantity=150,
        price=80.0,
        action="buy",
        commission=5.0
    )
    print()
    
    # 3. View current positions
    print("3. Current positions:")
    print("   当前持仓:")
    positions = manager.get_positions(portfolio.portfolio_id)
    for symbol, pos in positions.items():
        print(f"   - {symbol}: {pos.quantity} shares @ ¥{pos.avg_cost:.2f} avg cost")
    print()
    
    # 4. Update prices (simulate market movement)
    print("4. Updating market prices...")
    print("   更新市场价格...")
    new_prices = {
        "600519": 185.0,  # +5
        "300750": 55.0,   # +5
        "002594": 75.0    # -5
    }
    manager.update_prices(portfolio.portfolio_id, new_prices)
    print("   ✓ Prices updated")
    print()
    
    # 5. View portfolio value and P&L
    print("5. Portfolio value and P&L:")
    print("   投资组合价值和盈亏:")
    current_value = manager.get_current_value(portfolio.portfolio_id)
    portfolio_obj = manager.get_portfolio(portfolio.portfolio_id)
    
    print(f"   - Initial capital: ¥{portfolio_obj.initial_capital:,.2f}")
    print(f"   - Current value: ¥{current_value:,.2f}")
    print(f"   - Cash balance: ¥{portfolio_obj.cash:,.2f}")
    print(f"   - Positions value: ¥{sum(p.market_value for p in positions.values()):,.2f}")
    
    total_pnl = current_value - portfolio_obj.initial_capital
    total_return_pct = (total_pnl / portfolio_obj.initial_capital) * 100
    print(f"   - Total P&L: ¥{total_pnl:,.2f} ({total_return_pct:+.2f}%)")
    print()
    
    # 6. View detailed position P&L
    print("6. Position-level P&L:")
    print("   持仓级别盈亏:")
    positions = manager.get_positions(portfolio.portfolio_id)
    for symbol, pos in positions.items():
        print(f"   - {symbol}:")
        print(f"     Quantity: {pos.quantity} shares")
        print(f"     Avg cost: ¥{pos.avg_cost:.2f}")
        print(f"     Current price: ¥{pos.current_price:.2f}")
        print(f"     Market value: ¥{pos.market_value:,.2f}")
        print(f"     Unrealized P&L: ¥{pos.unrealized_pnl:,.2f} ({pos.unrealized_pnl_pct:+.2f}%)")
    print()
    
    # 7. Sell some stocks
    print("7. Selling stocks...")
    print("   卖出股票...")
    print("   - Selling 50 shares of 贵州茅台 (600519) @ ¥185.00")
    manager.update_position(
        portfolio.portfolio_id,
        symbol="600519",
        quantity=50,
        price=185.0,
        action="sell",
        commission=3.0
    )
    print("   ✓ Sold successfully")
    print()
    
    # 8. View trade history
    print("8. Trade history:")
    print("   交易历史:")
    trades = manager.get_trade_history(portfolio.portfolio_id)
    for i, trade in enumerate(trades, 1):
        print(f"   {i}. {trade.action.upper()} {trade.quantity} shares of {trade.symbol}")
        print(f"      Price: ¥{trade.price:.2f}, Commission: ¥{trade.commission:.2f}")
        print(f"      Total: ¥{trade.total_cost:.2f}, Time: {trade.timestamp[:19]}")
    print()
    
    # 9. Get portfolio summary
    print("9. Portfolio summary:")
    print("   投资组合摘要:")
    summary = manager.get_portfolio_summary(portfolio.portfolio_id)
    print(f"   - Portfolio ID: {summary['portfolio_id']}")
    print(f"   - Initial capital: ¥{summary['initial_capital']:,.2f}")
    print(f"   - Current value: ¥{summary['current_value']:,.2f}")
    print(f"   - Cash: ¥{summary['cash']:,.2f}")
    print(f"   - Positions value: ¥{summary['positions_value']:,.2f}")
    print(f"   - Number of positions: {summary['num_positions']}")
    print(f"   - Total unrealized P&L: ¥{summary['total_unrealized_pnl']:,.2f}")
    print(f"   - Total return: {summary['total_return_pct']:+.2f}%")
    print(f"   - Number of trades: {summary['num_trades']}")
    print()
    
    print("=" * 60)
    print("Demo completed successfully! / 演示成功完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
