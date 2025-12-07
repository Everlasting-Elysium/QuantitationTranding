"""
Unit tests for TradingAPIAdapter / TradingAPIAdapter单元测试
"""

import pytest
from datetime import datetime

from src.infrastructure import TradingAPIAdapter
from src.models.trading_models import AccountInfo, OrderResult, OrderStatus, Position
from src.utils.error_handler import SystemError


class TestTradingAPIAdapter:
    """Test cases for TradingAPIAdapter / TradingAPIAdapter测试用例"""
    
    def setup_method(self):
        """Setup test fixtures / 设置测试夹具"""
        self.adapter = TradingAPIAdapter()
    
    def teardown_method(self):
        """Cleanup after tests / 测试后清理"""
        if self.adapter.is_connected():
            self.adapter.disconnect()
    
    def test_initial_state(self):
        """Test initial adapter state / 测试初始适配器状态"""
        assert not self.adapter.is_connected()
        assert self.adapter.get_broker_name() is None
        assert self.adapter.get_account_id() is None
    
    def test_connect_mock_broker(self):
        """Test connecting to mock broker / 测试连接模拟券商"""
        credentials = {"account": "test_account"}
        self.adapter.connect(broker="mock", credentials=credentials)
        
        assert self.adapter.is_connected()
        assert self.adapter.get_broker_name() == "mock"
        assert self.adapter.get_account_id() == "test_account"
    
    def test_connect_empty_broker_name(self):
        """Test connecting with empty broker name / 测试使用空券商名称连接"""
        with pytest.raises(SystemError) as exc_info:
            self.adapter.connect(broker="", credentials={"account": "test"})
        
        assert "TRD0001" in str(exc_info.value)
    
    def test_connect_empty_credentials(self):
        """Test connecting with empty credentials / 测试使用空凭证连接"""
        with pytest.raises(SystemError) as exc_info:
            self.adapter.connect(broker="mock", credentials={})
        
        # Should still connect but with unknown account
        # Actually, empty dict should raise error
        assert "TRD0002" in str(exc_info.value)
    
    def test_disconnect(self):
        """Test disconnecting / 测试断开连接"""
        self.adapter.connect(broker="mock", credentials={"account": "test"})
        assert self.adapter.is_connected()
        
        self.adapter.disconnect()
        assert not self.adapter.is_connected()
        assert self.adapter.get_broker_name() is None
    
    def test_place_order_not_connected(self):
        """Test placing order when not connected / 测试未连接时下单"""
        with pytest.raises(SystemError) as exc_info:
            self.adapter.place_order(
                symbol="600519",
                quantity=100,
                order_type="market"
            )
        
        assert "TRD0004" in str(exc_info.value)

    
    def test_place_market_buy_order(self):
        """Test placing market buy order / 测试下市价买单"""
        self.adapter.connect(broker="mock", credentials={"account": "test"})
        
        result = self.adapter.place_order(
            symbol="600519",
            quantity=100,
            order_type="market",
            action="buy"
        )
        
        assert isinstance(result, OrderResult)
        assert result.symbol == "600519"
        assert result.quantity == 100
        assert result.order_type == "market"
        assert result.status == "filled"
        assert result.filled_quantity == 100
        assert result.avg_fill_price > 0
        assert result.order_id.startswith("MOCK")
    
    def test_place_limit_buy_order(self):
        """Test placing limit buy order / 测试下限价买单"""
        self.adapter.connect(broker="mock", credentials={"account": "test"})
        
        result = self.adapter.place_order(
            symbol="600519",
            quantity=100,
            order_type="limit",
            price=1800.0,
            action="buy"
        )
        
        assert isinstance(result, OrderResult)
        assert result.order_type == "limit"
        assert result.avg_fill_price == 1800.0
    
    def test_place_sell_order(self):
        """Test placing sell order / 测试下卖单"""
        self.adapter.connect(broker="mock", credentials={"account": "test"})
        
        # First buy some shares
        self.adapter.place_order(
            symbol="600519",
            quantity=100,
            order_type="market",
            action="buy"
        )
        
        # Then sell
        result = self.adapter.place_order(
            symbol="600519",
            quantity=50,
            order_type="market",
            action="sell"
        )
        
        assert result.status == "filled"
        assert result.filled_quantity == 50
    
    def test_place_order_invalid_quantity(self):
        """Test placing order with invalid quantity / 测试使用无效数量下单"""
        self.adapter.connect(broker="mock", credentials={"account": "test"})
        
        with pytest.raises(SystemError):
            self.adapter.place_order(
                symbol="600519",
                quantity=0,
                order_type="market"
            )
    
    def test_place_order_invalid_type(self):
        """Test placing order with invalid type / 测试使用无效类型下单"""
        self.adapter.connect(broker="mock", credentials={"account": "test"})
        
        with pytest.raises(SystemError):
            self.adapter.place_order(
                symbol="600519",
                quantity=100,
                order_type="invalid"
            )
    
    def test_place_limit_order_without_price(self):
        """Test placing limit order without price / 测试下限价单但不提供价格"""
        self.adapter.connect(broker="mock", credentials={"account": "test"})
        
        with pytest.raises(SystemError):
            self.adapter.place_order(
                symbol="600519",
                quantity=100,
                order_type="limit"
            )
    
    def test_get_account_info(self):
        """Test getting account info / 测试获取账户信息"""
        self.adapter.connect(broker="mock", credentials={"account": "test"})
        
        account_info = self.adapter.get_account_info()
        
        assert isinstance(account_info, AccountInfo)
        assert account_info.account_id == "test"
        assert account_info.broker == "mock"
        assert account_info.total_value > 0
        assert account_info.cash_balance > 0
    
    def test_get_account_info_not_connected(self):
        """Test getting account info when not connected / 测试未连接时获取账户信息"""
        with pytest.raises(SystemError) as exc_info:
            self.adapter.get_account_info()
        
        assert "TRD0004" in str(exc_info.value)
    
    def test_get_positions_empty(self):
        """Test getting positions when empty / 测试获取空持仓"""
        self.adapter.connect(broker="mock", credentials={"account": "test"})
        
        positions = self.adapter.get_positions()
        
        assert isinstance(positions, list)
        assert len(positions) == 0
    
    def test_get_positions_after_trade(self):
        """Test getting positions after trade / 测试交易后获取持仓"""
        self.adapter.connect(broker="mock", credentials={"account": "test"})
        
        # Place buy order
        self.adapter.place_order(
            symbol="600519",
            quantity=100,
            order_type="market",
            action="buy"
        )
        
        positions = self.adapter.get_positions()
        
        assert len(positions) == 1
        assert positions[0].symbol == "600519"
        assert positions[0].quantity == 100
    
    def test_get_positions_not_connected(self):
        """Test getting positions when not connected / 测试未连接时获取持仓"""
        with pytest.raises(SystemError) as exc_info:
            self.adapter.get_positions()
        
        assert "TRD0004" in str(exc_info.value)
    
    def test_get_order_status(self):
        """Test getting order status / 测试获取订单状态"""
        self.adapter.connect(broker="mock", credentials={"account": "test"})
        
        # Place order
        result = self.adapter.place_order(
            symbol="600519",
            quantity=100,
            order_type="market",
            action="buy"
        )
        
        # Get status
        status = self.adapter.get_order_status(result.order_id)
        
        assert isinstance(status, OrderStatus)
        assert status.order_id == result.order_id
        assert status.status == "filled"
        assert status.filled_quantity == 100
        assert status.remaining_quantity == 0
    
    def test_get_order_status_not_found(self):
        """Test getting status of non-existent order / 测试获取不存在订单的状态"""
        self.adapter.connect(broker="mock", credentials={"account": "test"})
        
        with pytest.raises(SystemError) as exc_info:
            self.adapter.get_order_status("INVALID_ORDER_ID")
        
        assert "TRD0009" in str(exc_info.value)
    
    def test_get_order_status_not_connected(self):
        """Test getting order status when not connected / 测试未连接时获取订单状态"""
        with pytest.raises(SystemError) as exc_info:
            self.adapter.get_order_status("ORDER123")
        
        assert "TRD0004" in str(exc_info.value)
    
    def test_cancel_order_not_connected(self):
        """Test canceling order when not connected / 测试未连接时撤单"""
        with pytest.raises(SystemError) as exc_info:
            self.adapter.cancel_order("ORDER123")
        
        assert "TRD0004" in str(exc_info.value)
    
    def test_multiple_orders(self):
        """Test placing multiple orders / 测试下多个订单"""
        self.adapter.connect(broker="mock", credentials={"account": "test"})
        
        # Place multiple orders
        result1 = self.adapter.place_order(
            symbol="600519",
            quantity=100,
            order_type="market",
            action="buy"
        )
        
        result2 = self.adapter.place_order(
            symbol="000858",
            quantity=200,
            order_type="market",
            action="buy"
        )
        
        # Check positions
        positions = self.adapter.get_positions()
        assert len(positions) == 2
        
        # Check account
        account_info = self.adapter.get_account_info()
        assert account_info.positions_value > 0
        assert account_info.cash_balance < 1000000  # Initial cash
