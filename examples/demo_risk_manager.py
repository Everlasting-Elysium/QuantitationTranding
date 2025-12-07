"""
Demo script for Risk Manager functionality.
风险管理器功能演示脚本

This script demonstrates how to use the Risk Manager to monitor and control
trading risks in the Qlib Trading System.
本脚本演示如何使用风险管理器监控和控制Qlib交易系统中的交易风险。
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
from datetime import datetime

from src.core import RiskManager
from src.models.trading_models import Portfolio, Position, Trade
from src.infrastructure import LoggerSystem


def demo_initialization():
    """
    Demonstrate Risk Manager initialization.
    演示风险管理器初始化
    """
    print("=" * 80)
    print("Demo 1: Risk Manager Initialization / 演示1：风险管理器初始化")
    print("=" * 80)
    
    # Initialize with default settings
    rm_default = RiskManager()
    print(f"Default settings:")
    print(f"  Max position: {rm_default.max_position_pct:.1%}")
    print(f"  Max sector: {rm_default.max_sector_pct:.1%}")
    print(f"  Max drawdown: {rm_default.max_drawdown_pct:.1%}")
    print(f"  Max daily loss: {rm_default.max_daily_loss_pct:.1%}")
    print(f"  VaR confidence: {rm_default.var_confidence:.1%}")
    
    # Initialize with custom settings
    rm_custom = RiskManager(
        max_position_pct=0.25,
        max_sector_pct=0.35,
        max_drawdown_pct=0.15,
        max_daily_loss_pct=0.03,
        var_confidence=0.99
    )
    print(f"\nCustom settings:")
    print(f"  Max position: {rm_custom.max_position_pct:.1%}")
    print(f"  Max sector: {rm_custom.max_sector_pct:.1%}")
    print(f"  Max drawdown: {rm_custom.max_drawdown_pct:.1%}")
    print(f"  Max daily loss: {rm_custom.max_daily_loss_pct:.1%}")
    print(f"  VaR confidence: {rm_custom.var_confidence:.1%}")
    print()


def demo_position_risk_check():
    """
    Demonstrate position risk checking.
    演示持仓风险检查
    """
    print("=" * 80)
    print("Demo 2: Position Risk Checking / 演示2：持仓风险检查")
    print("=" * 80)
    
    # Create risk manager
    risk_manager = RiskManager(max_position_pct=0.3)
    
    # Create a portfolio
    portfolio = Portfolio(
        portfolio_id="demo_portfolio",
        positions={
            "AAPL": Position("AAPL", 100, 150.0, 160.0),
            "GOOGL": Position("GOOGL", 50, 2800.0, 2900.0)
        },
        cash=200000.0,
        initial_capital=300000.0
    )
    portfolio.update_total_value()
    
    print(f"Portfolio:")
    print(f"  Total value: ${portfolio.total_value:,.2f}")
    print(f"  Cash: ${portfolio.cash:,.2f}")
    print(f"  Positions: {len(portfolio.positions)}")
    
    # Test 1: Small trade (should pass)
    print(f"\nTest 1: Small trade (should pass)")
    small_trade = Trade(
        trade_id="trade_001",
        timestamp=datetime.now().isoformat(),
        symbol="MSFT",
        action="buy",
        quantity=50,
        price=300.0,
        commission=10.0
    )
    
    result = risk_manager.check_position_risk(portfolio, small_trade)
    print(f"  Trade: Buy {small_trade.quantity} {small_trade.symbol} @ ${small_trade.price}")
    print(f"  Passed: {result['passed']}")
    print(f"  Risk score: {result['risk_score']}")
    if result['warnings']:
        print(f"  Warnings: {result['warnings']}")
    
    # Test 2: Large trade (should fail)
    print(f"\nTest 2: Large trade (should fail)")
    large_trade = Trade(
        trade_id="trade_002",
        timestamp=datetime.now().isoformat(),
        symbol="MSFT",
        action="buy",
        quantity=500,
        price=300.0,
        commission=10.0
    )
    
    result = risk_manager.check_position_risk(portfolio, large_trade)
    print(f"  Trade: Buy {large_trade.quantity} {large_trade.symbol} @ ${large_trade.price}")
    print(f"  Passed: {result['passed']}")
    print(f"  Risk score: {result['risk_score']}")
    if result['violations']:
        print(f"  Violations:")
        for v in result['violations']:
            print(f"    - {v}")
    if result['suggested_adjustments']:
        print(f"  Suggested adjustments:")
        for k, v in result['suggested_adjustments'].items():
            print(f"    - {k}: {v:.2f}")
    print()



def demo_var_calculation():
    """
    Demonstrate VaR calculation.
    演示VaR计算
    """
    print("=" * 80)
    print("Demo 3: VaR Calculation / 演示3：VaR计算")
    print("=" * 80)
    
    risk_manager = RiskManager()
    
    # Generate sample returns
    np.random.seed(42)
    returns = pd.Series(np.random.normal(0.001, 0.02, 100))
    portfolio_value = 100000.0
    
    print(f"Portfolio value: ${portfolio_value:,.2f}")
    print(f"Returns statistics:")
    print(f"  Mean: {returns.mean():.4f}")
    print(f"  Std: {returns.std():.4f}")
    print(f"  Min: {returns.min():.4f}")
    print(f"  Max: {returns.max():.4f}")
    
    # Calculate VaR at different confidence levels
    var_90 = risk_manager.calculate_var(returns, portfolio_value, confidence=0.90)
    var_95 = risk_manager.calculate_var(returns, portfolio_value, confidence=0.95)
    var_99 = risk_manager.calculate_var(returns, portfolio_value, confidence=0.99)
    
    print(f"\nValue at Risk:")
    print(f"  VaR (90%): ${var_90:,.2f}")
    print(f"  VaR (95%): ${var_95:,.2f}")
    print(f"  VaR (99%): ${var_99:,.2f}")
    print()


def demo_max_drawdown():
    """
    Demonstrate maximum drawdown calculation.
    演示最大回撤计算
    """
    print("=" * 80)
    print("Demo 4: Maximum Drawdown / 演示4：最大回撤")
    print("=" * 80)
    
    risk_manager = RiskManager()
    
    # Create returns with a drawdown
    returns = pd.Series([0.02, 0.03, -0.05, -0.04, -0.03, 0.01, 0.02, 0.03])
    
    print(f"Returns: {returns.tolist()}")
    
    max_dd = risk_manager.calculate_max_drawdown(returns)
    print(f"Maximum Drawdown: {max_dd:.2%}")
    
    # Track portfolio values
    print(f"\nTracking portfolio values:")
    portfolio_id = "demo_portfolio"
    values = [100000, 105000, 110000, 104000, 98000, 102000, 108000]
    
    for i, value in enumerate(values):
        risk_manager.track_portfolio_value(portfolio_id, value)
        current_dd = risk_manager.get_portfolio_drawdown(portfolio_id)
        print(f"  Day {i+1}: ${value:,.2f} (Drawdown: {current_dd:.2%})")
    print()


def demo_concentration_risk():
    """
    Demonstrate concentration risk analysis.
    演示集中度风险分析
    """
    print("=" * 80)
    print("Demo 5: Concentration Risk / 演示5：集中度风险")
    print("=" * 80)
    
    risk_manager = RiskManager()
    
    # Create a diversified portfolio
    diversified_portfolio = Portfolio(
        portfolio_id="diversified",
        positions={
            "AAPL": Position("AAPL", 100, 150.0, 160.0),
            "GOOGL": Position("GOOGL", 50, 2800.0, 2900.0),
            "MSFT": Position("MSFT", 100, 300.0, 310.0),
            "JPM": Position("JPM", 200, 150.0, 155.0),
            "BAC": Position("BAC", 500, 30.0, 32.0)
        },
        cash=50000.0,
        initial_capital=300000.0
    )
    diversified_portfolio.update_total_value()
    
    sector_map = {
        "AAPL": "Technology",
        "GOOGL": "Technology",
        "MSFT": "Technology",
        "JPM": "Finance",
        "BAC": "Finance"
    }
    
    print(f"Diversified Portfolio:")
    print(f"  Total value: ${diversified_portfolio.total_value:,.2f}")
    
    result = risk_manager.check_concentration_risk(diversified_portfolio, sector_map)
    print(f"  Max position: {result['max_position_pct']:.1f}%")
    print(f"  Top 5 concentration: {result['top_5_concentration']:.1f}%")
    print(f"  Risk level: {result['risk_level']}")
    print(f"  Sector concentration:")
    for sector, pct in result['sector_concentration'].items():
        print(f"    - {sector}: {pct:.1f}%")
    
    # Create a concentrated portfolio
    print(f"\nConcentrated Portfolio:")
    concentrated_portfolio = Portfolio(
        portfolio_id="concentrated",
        positions={
            "AAPL": Position("AAPL", 1000, 150.0, 160.0)
        },
        cash=10000.0,
        initial_capital=200000.0
    )
    concentrated_portfolio.update_total_value()
    
    print(f"  Total value: ${concentrated_portfolio.total_value:,.2f}")
    
    result = risk_manager.check_concentration_risk(concentrated_portfolio, sector_map)
    print(f"  Max position: {result['max_position_pct']:.1f}%")
    print(f"  Top 5 concentration: {result['top_5_concentration']:.1f}%")
    print(f"  Risk level: {result['risk_level']}")
    print()



def demo_risk_alerts():
    """
    Demonstrate risk alert generation.
    演示风险预警生成
    """
    print("=" * 80)
    print("Demo 6: Risk Alerts / 演示6：风险预警")
    print("=" * 80)
    
    risk_manager = RiskManager()
    
    # Create portfolio with losing position
    portfolio = Portfolio(
        portfolio_id="alert_demo",
        positions={
            "AAPL": Position("AAPL", 100, 200.0, 150.0),  # 25% loss
            "GOOGL": Position("GOOGL", 50, 2800.0, 2900.0)
        },
        cash=50000.0,
        initial_capital=200000.0
    )
    portfolio.update_total_value()
    
    # Create returns with high drawdown
    returns = pd.Series([0.02, -0.10, -0.08, -0.05, -0.03])
    
    sector_map = {
        "AAPL": "Technology",
        "GOOGL": "Technology"
    }
    
    print(f"Portfolio:")
    print(f"  Total value: ${portfolio.total_value:,.2f}")
    print(f"  Positions:")
    for symbol, pos in portfolio.positions.items():
        print(f"    - {symbol}: {pos.quantity} shares @ ${pos.current_price:.2f}")
        print(f"      Unrealized P&L: {pos.unrealized_pnl_pct:.2%}")
    
    print(f"\nRecent returns: {returns.tolist()}")
    
    # Generate risk alert
    alert = risk_manager.generate_risk_alert(portfolio, returns, sector_map)
    
    if alert:
        print(f"\n⚠️  Risk Alert Generated:")
        print(f"  Alert ID: {alert['alert_id']}")
        print(f"  Severity: {alert['severity']}")
        print(f"  Type: {alert['alert_type']}")
        print(f"  Message: {alert['message']}")
        print(f"  Current value: ${alert['current_value']:,.2f}")
        print(f"  Threshold value: ${alert['threshold_value']:,.2f}")
        
        if alert['affected_positions']:
            print(f"  Affected positions: {', '.join(alert['affected_positions'])}")
        
        if alert['recommended_actions']:
            print(f"  Recommended actions:")
            for action in alert['recommended_actions']:
                print(f"    - {action}")
        
        # Get mitigation suggestions
        suggestions = risk_manager.suggest_risk_mitigation(alert)
        print(f"\n  Mitigation suggestions:")
        for suggestion in suggestions:
            print(f"    - {suggestion}")
    else:
        print(f"\n✓ No risk alerts")
    print()


def main():
    """
    Run all demos.
    运行所有演示
    """
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "Risk Manager Demo / 风险管理器演示" + " " * 23 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    try:
        demo_initialization()
        demo_position_risk_check()
        demo_var_calculation()
        demo_max_drawdown()
        demo_concentration_risk()
        demo_risk_alerts()
        
        print("=" * 80)
        print("All demos completed successfully! / 所有演示成功完成！")
        print("=" * 80)
        print()
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
