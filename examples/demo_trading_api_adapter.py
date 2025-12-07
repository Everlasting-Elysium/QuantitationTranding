"""
Trading API Adapter Demo / 交易API适配器演示

This script demonstrates how to use the TradingAPIAdapter to:
本脚本演示如何使用TradingAPIAdapter来:
- Connect to a broker / 连接券商
- Place orders / 下单
- Query account information / 查询账户信息
- Query positions / 查询持仓
- Query order status / 查询订单状态
- Cancel orders / 撤单
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.infrastructure import TradingAPIAdapter, get_logger


def main():
    """Main demo function / 主演示函数"""
    logger = get_logger(__name__)
    
    print("=" * 80)
    print("Trading API Adapter Demo / 交易API适配器演示")
    print("=" * 80)
    print()
    
    # Create adapter
    adapter = TradingAPIAdapter()
    
    try:
        # 1. Connect to mock broker
        print("1. 连接到模拟券商 / Connecting to mock broker...")
        credentials = {
            "account": "demo_account_001",
            "password": "demo_password"
        }
        adapter.connect(broker="mock", credentials=credentials)
        print(f"   ✓ 已连接到券商: {adapter.get_broker_name()}")
        print(f"   ✓ 账户ID: {adapter.get_account_id()}")
        print()
        
        # 2. Get initial account info
        print("2. 查询初始账户信息 / Getting initial account info...")
        account_info = adapter.get_account_info()
        print(f"   账户总资产: ¥{account_info.total_value:,.2f}")
        print(f"   可用现金: ¥{account_info.cash_balance:,.2f}")
        print(f"   持仓市值: ¥{account_info.positions_value:,.2f}")
        print(f"   未实现盈亏: ¥{account_info.unrealized_pnl:,.2f}")
        print()
        
        # 3. Place buy orders
        print("3. 下买单 / Placing buy orders...")
        
        # Buy order 1
        result1 = adapter.place_order(
            symbol="600519",  # 贵州茅台
            quantity=100,
            order_type="market",
            action="buy"
        )
        print(f"   订单1: {result1.order_id}")
        print(f"   - 股票: {result1.symbol}")
        print(f"   - 数量: {result1.quantity}")
        print(f"   - 状态: {result1.status}")
        print(f"   - 成交价: ¥{result1.avg_fill_price:.2f}")
        print(f"   - 消息: {result1.message}")
        print()
        
        # Buy order 2
        result2 = adapter.place_order(
            symbol="000858",  # 五粮液
            quantity=200,
            order_type="limit",
            price=150.0,
            action="buy"
        )
        print(f"   订单2: {result2.order_id}")
        print(f"   - 股票: {result2.symbol}")
        print(f"   - 数量: {result2.quantity}")
        print(f"   - 状态: {result2.status}")
        print(f"   - 成交价: ¥{result2.avg_fill_price:.2f}")
        print()

        
        # 4. Query positions
        print("4. 查询持仓 / Querying positions...")
        positions = adapter.get_positions()
        print(f"   持仓数量: {len(positions)}")
        for pos in positions:
            print(f"   - {pos.symbol}: {pos.quantity}股 @ ¥{pos.avg_cost:.2f}")
            print(f"     当前价: ¥{pos.current_price:.2f}, 市值: ¥{pos.market_value:,.2f}")
        print()
        
        # 5. Query account info after trades
        print("5. 查询交易后账户信息 / Getting account info after trades...")
        account_info = adapter.get_account_info()
        print(f"   账户总资产: ¥{account_info.total_value:,.2f}")
        print(f"   可用现金: ¥{account_info.cash_balance:,.2f}")
        print(f"   持仓市值: ¥{account_info.positions_value:,.2f}")
        print()
        
        # 6. Query order status
        print("6. 查询订单状态 / Querying order status...")
        order_status = adapter.get_order_status(result1.order_id)
        print(f"   订单ID: {order_status.order_id}")
        print(f"   状态: {order_status.status}")
        print(f"   已成交数量: {order_status.filled_quantity}")
        print(f"   剩余数量: {order_status.remaining_quantity}")
        print(f"   平均成交价: ¥{order_status.avg_fill_price:.2f}")
        print(f"   最后更新: {order_status.last_update}")
        print()
        
        # 7. Place sell order
        print("7. 下卖单 / Placing sell order...")
        result3 = adapter.place_order(
            symbol="600519",
            quantity=50,
            order_type="market",
            action="sell"
        )
        print(f"   订单3: {result3.order_id}")
        print(f"   - 股票: {result3.symbol}")
        print(f"   - 数量: {result3.quantity}")
        print(f"   - 动作: 卖出")
        print(f"   - 状态: {result3.status}")
        print()
        
        # 8. Query final positions
        print("8. 查询最终持仓 / Querying final positions...")
        positions = adapter.get_positions()
        print(f"   持仓数量: {len(positions)}")
        for pos in positions:
            print(f"   - {pos.symbol}: {pos.quantity}股 @ ¥{pos.avg_cost:.2f}")
        print()
        
        # 9. Query final account info
        print("9. 查询最终账户信息 / Getting final account info...")
        account_info = adapter.get_account_info()
        print(f"   账户总资产: ¥{account_info.total_value:,.2f}")
        print(f"   可用现金: ¥{account_info.cash_balance:,.2f}")
        print(f"   持仓市值: ¥{account_info.positions_value:,.2f}")
        print()
        
        print("=" * 80)
        print("演示完成 / Demo completed successfully!")
        print("=" * 80)
        
    except Exception as e:
        logger.error(f"演示过程中发生错误: {str(e)}", exc_info=True)
        print(f"\n错误: {str(e)}")
        return 1
    
    finally:
        # Disconnect
        if adapter.is_connected():
            print("\n断开连接 / Disconnecting...")
            adapter.disconnect()
            print("已断开连接 / Disconnected")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
