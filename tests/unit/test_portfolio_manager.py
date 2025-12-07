"""
Unit tests for Portfolio Manager.
投资组合管理器的单元测试
"""

import pytest
from datetime import datetime
from src.core.portfolio_manager import PortfolioManager
from src.models.trading_models import Portfolio, Position, Trade


class TestPortfolioManager:
    """Test cases for PortfolioManager / PortfolioManager的测试用例"""
    
    @pytest.fixture
    def manager(self):
        """Create a portfolio manager instance / 创建投资组合管理器实例"""
        return PortfolioManager()
    
    def test_create_portfolio(self, manager):
        """
        Test portfolio creation with initial capital.
        测试使用初始资金创建投资组合
        """
        initial_capital = 100000.0
        portfolio = manager.create_portfolio(initial_capital)
        
        assert portfolio is not None
        assert portfolio.portfolio_id is not None
        assert portfolio.initial_capital == initial_capital
        assert portfolio.cash == initial_capital
        assert portfolio.total_value == initial_capital
        assert len(portfolio.positions) == 0
    
    def test_create_portfolio_with_custom_id(self, manager):
        """
        Test portfolio creation with custom ID.
        测试使用自定义ID创建投资组合
        """
        portfolio_id = "test_portfolio_001"
        portfolio = manager.create_portfolio(100000.0, portfolio_id=portfolio_id)
        
        assert portfolio.portfolio_id == portfolio_id
    
    def test_create_portfolio_invalid_capital(self, manager):
        """
        Test portfolio creation with invalid capital.
        测试使用无效资金创建投资组合
        """
        with pytest.raises(ValueError, match="Initial capital must be positive"):
            manager.create_portfolio(0)
        
        with pytest.raises(ValueError, match="Initial capital must be positive"):
            manager.create_portfolio(-1000)
    
    def test_get_portfolio(self, manager):
        """
        Test retrieving portfolio by ID.
        测试根据ID检索投资组合
        """
        portfolio = manager.create_portfolio(100000.0)
        retrieved = manager.get_portfolio(portfolio.portfolio_id)
        
        assert retrieved is not None
        assert retrieved.portfolio_id == portfolio.portfolio_id
        
        # Test non-existent portfolio
        assert manager.get_portfolio("non_existent") is None
    
    def test_update_position_buy(self, manager):
        """
        Test buying stocks to create/update position.
        测试买入股票以创建/更新持仓
        """
        portfolio = manager.create_portfolio(100000.0)
        
        # Buy first batch
        manager.update_position(
            portfolio.portfolio_id,
            symbol="600519",
            quantity=100,
            price=180.0,
            action="buy",
            commission=5.0
        )
        
        # Verify position created
        positions = manager.get_positions(portfolio.portfolio_id)
        assert "600519" in positions
        assert positions["600519"].quantity == 100
        assert positions["600519"].current_price == 180.0
        
        # Verify cash updated
        updated_portfolio = manager.get_portfolio(portfolio.portfolio_id)
        expected_cash = 100000.0 - (100 * 180.0 + 5.0)
        assert abs(updated_portfolio.cash - expected_cash) < 0.01
    
    def test_update_position_buy_multiple_batches(self, manager):
        """
        Test buying same stock multiple times.
        测试多次买入同一股票
        """
        portfolio = manager.create_portfolio(100000.0)
        
        # First buy
        manager.update_position(
            portfolio.portfolio_id,
            symbol="600519",
            quantity=100,
            price=180.0,
            action="buy",
            commission=5.0
        )
        
        # Second buy at different price
        manager.update_position(
            portfolio.portfolio_id,
            symbol="600519",
            quantity=50,
            price=185.0,
            action="buy",
            commission=3.0
        )
        
        # Verify position updated correctly
        positions = manager.get_positions(portfolio.portfolio_id)
        assert positions["600519"].quantity == 150
        
        # Verify average cost calculated correctly
        expected_avg_cost = ((100 * 180.0 + 5.0) + (50 * 185.0 + 3.0)) / 150
        assert abs(positions["600519"].avg_cost - expected_avg_cost) < 0.01
    
    def test_update_position_sell(self, manager):
        """
        Test selling stocks to reduce/close position.
        测试卖出股票以减少/关闭持仓
        """
        portfolio = manager.create_portfolio(100000.0)
        
        # Buy first
        manager.update_position(
            portfolio.portfolio_id,
            symbol="600519",
            quantity=100,
            price=180.0,
            action="buy",
            commission=5.0
        )
        
        # Sell partial
        manager.update_position(
            portfolio.portfolio_id,
            symbol="600519",
            quantity=30,
            price=185.0,
            action="sell",
            commission=3.0
        )
        
        # Verify position reduced
        positions = manager.get_positions(portfolio.portfolio_id)
        assert positions["600519"].quantity == 70
        
        # Verify cash updated (received proceeds)
        updated_portfolio = manager.get_portfolio(portfolio.portfolio_id)
        initial_cash_after_buy = 100000.0 - (100 * 180.0 + 5.0)
        proceeds = 30 * 185.0 - 3.0
        expected_cash = initial_cash_after_buy + proceeds
        assert abs(updated_portfolio.cash - expected_cash) < 0.01
    
    def test_update_position_sell_all(self, manager):
        """
        Test selling all shares to close position.
        测试卖出所有股份以关闭持仓
        """
        portfolio = manager.create_portfolio(100000.0)
        
        # Buy
        manager.update_position(
            portfolio.portfolio_id,
            symbol="600519",
            quantity=100,
            price=180.0,
            action="buy",
            commission=5.0
        )
        
        # Sell all
        manager.update_position(
            portfolio.portfolio_id,
            symbol="600519",
            quantity=100,
            price=185.0,
            action="sell",
            commission=5.0
        )
        
        # Verify position removed
        positions = manager.get_positions(portfolio.portfolio_id)
        assert "600519" not in positions
    
    def test_update_position_insufficient_cash(self, manager):
        """
        Test buying with insufficient cash.
        测试现金不足时买入
        """
        portfolio = manager.create_portfolio(10000.0)
        
        with pytest.raises(ValueError, match="Insufficient cash"):
            manager.update_position(
                portfolio.portfolio_id,
                symbol="600519",
                quantity=1000,
                price=180.0,
                action="buy"
            )
    
    def test_update_position_insufficient_shares(self, manager):
        """
        Test selling more shares than owned.
        测试卖出超过持有的股份
        """
        portfolio = manager.create_portfolio(100000.0)
        
        # Buy 50 shares
        manager.update_position(
            portfolio.portfolio_id,
            symbol="600519",
            quantity=50,
            price=180.0,
            action="buy"
        )
        
        # Try to sell 100 shares
        with pytest.raises(ValueError, match="Insufficient shares"):
            manager.update_position(
                portfolio.portfolio_id,
                symbol="600519",
                quantity=100,
                price=185.0,
                action="sell"
            )
    
    def test_update_position_no_position(self, manager):
        """
        Test selling stock with no position.
        测试卖出没有持仓的股票
        """
        portfolio = manager.create_portfolio(100000.0)
        
        with pytest.raises(ValueError, match="No position found"):
            manager.update_position(
                portfolio.portfolio_id,
                symbol="600519",
                quantity=10,
                price=180.0,
                action="sell"
            )
    
    def test_update_position_invalid_parameters(self, manager):
        """
        Test update position with invalid parameters.
        测试使用无效参数更新持仓
        """
        portfolio = manager.create_portfolio(100000.0)
        
        # Invalid quantity
        with pytest.raises(ValueError, match="Quantity must be positive"):
            manager.update_position(
                portfolio.portfolio_id,
                symbol="600519",
                quantity=0,
                price=180.0,
                action="buy"
            )
        
        # Invalid price
        with pytest.raises(ValueError, match="Price must be positive"):
            manager.update_position(
                portfolio.portfolio_id,
                symbol="600519",
                quantity=10,
                price=-100.0,
                action="buy"
            )
        
        # Invalid action
        with pytest.raises(ValueError, match="Action must be"):
            manager.update_position(
                portfolio.portfolio_id,
                symbol="600519",
                quantity=10,
                price=180.0,
                action="hold"
            )
    
    def test_update_prices(self, manager):
        """
        Test updating current prices for positions.
        测试更新持仓的当前价格
        """
        portfolio = manager.create_portfolio(100000.0)
        
        # Buy some stocks
        manager.update_position(
            portfolio.portfolio_id,
            symbol="600519",
            quantity=100,
            price=180.0,
            action="buy"
        )
        
        manager.update_position(
            portfolio.portfolio_id,
            symbol="300750",
            quantity=200,
            price=50.0,
            action="buy"
        )
        
        # Update prices
        new_prices = {
            "600519": 185.0,
            "300750": 55.0
        }
        manager.update_prices(portfolio.portfolio_id, new_prices)
        
        # Verify prices updated
        positions = manager.get_positions(portfolio.portfolio_id)
        assert positions["600519"].current_price == 185.0
        assert positions["300750"].current_price == 55.0
        
        # Verify unrealized P&L calculated
        assert positions["600519"].unrealized_pnl > 0  # Price increased
        assert positions["300750"].unrealized_pnl > 0  # Price increased
    
    def test_get_current_value(self, manager):
        """
        Test getting current portfolio value.
        测试获取当前投资组合价值
        """
        portfolio = manager.create_portfolio(100000.0)
        
        # Initial value should equal initial capital
        assert manager.get_current_value(portfolio.portfolio_id) == 100000.0
        
        # Buy some stocks
        manager.update_position(
            portfolio.portfolio_id,
            symbol="600519",
            quantity=100,
            price=180.0,
            action="buy"
        )
        
        # Update price
        manager.update_prices(portfolio.portfolio_id, {"600519": 185.0})
        
        # Calculate expected value
        cash_after_buy = 100000.0 - (100 * 180.0)
        position_value = 100 * 185.0
        expected_value = cash_after_buy + position_value
        
        current_value = manager.get_current_value(portfolio.portfolio_id)
        assert abs(current_value - expected_value) < 0.01
    
    def test_get_positions(self, manager):
        """
        Test getting all positions.
        测试获取所有持仓
        """
        portfolio = manager.create_portfolio(100000.0)
        
        # Initially no positions
        positions = manager.get_positions(portfolio.portfolio_id)
        assert len(positions) == 0
        
        # Buy multiple stocks
        manager.update_position(
            portfolio.portfolio_id,
            symbol="600519",
            quantity=100,
            price=180.0,
            action="buy"
        )
        
        manager.update_position(
            portfolio.portfolio_id,
            symbol="300750",
            quantity=200,
            price=50.0,
            action="buy"
        )
        
        # Verify positions
        positions = manager.get_positions(portfolio.portfolio_id)
        assert len(positions) == 2
        assert "600519" in positions
        assert "300750" in positions
    
    def test_get_trade_history(self, manager):
        """
        Test getting trade history.
        测试获取交易历史
        """
        portfolio = manager.create_portfolio(100000.0)
        
        # Initially no trades
        history = manager.get_trade_history(portfolio.portfolio_id)
        assert len(history) == 0
        
        # Execute some trades
        manager.update_position(
            portfolio.portfolio_id,
            symbol="600519",
            quantity=100,
            price=180.0,
            action="buy"
        )
        
        manager.update_position(
            portfolio.portfolio_id,
            symbol="600519",
            quantity=30,
            price=185.0,
            action="sell"
        )
        
        # Verify trade history
        history = manager.get_trade_history(portfolio.portfolio_id)
        assert len(history) == 2
        assert history[0].action == "buy"
        assert history[0].quantity == 100
        assert history[1].action == "sell"
        assert history[1].quantity == 30
    
    def test_get_portfolio_summary(self, manager):
        """
        Test getting portfolio summary statistics.
        测试获取投资组合摘要统计信息
        """
        portfolio = manager.create_portfolio(100000.0)
        
        # Buy some stocks
        manager.update_position(
            portfolio.portfolio_id,
            symbol="600519",
            quantity=100,
            price=180.0,
            action="buy"
        )
        
        # Update price to create unrealized gain
        manager.update_prices(portfolio.portfolio_id, {"600519": 185.0})
        
        # Get summary
        summary = manager.get_portfolio_summary(portfolio.portfolio_id)
        
        assert summary['portfolio_id'] == portfolio.portfolio_id
        assert summary['initial_capital'] == 100000.0
        assert summary['num_positions'] == 1
        assert summary['num_trades'] == 1
        assert summary['total_unrealized_pnl'] > 0  # Should have profit
        assert summary['total_return_pct'] > 0  # Should have positive return
    
    def test_delete_portfolio(self, manager):
        """
        Test deleting portfolio.
        测试删除投资组合
        """
        portfolio = manager.create_portfolio(100000.0)
        portfolio_id = portfolio.portfolio_id
        
        # Execute some trades
        manager.update_position(
            portfolio_id,
            symbol="600519",
            quantity=100,
            price=180.0,
            action="buy"
        )
        
        # Delete portfolio
        result = manager.delete_portfolio(portfolio_id)
        assert result is True
        
        # Verify portfolio deleted
        assert manager.get_portfolio(portfolio_id) is None
        
        # Try to delete again
        result = manager.delete_portfolio(portfolio_id)
        assert result is False
    
    def test_portfolio_not_found_errors(self, manager):
        """
        Test operations on non-existent portfolio.
        测试对不存在的投资组合进行操作
        """
        fake_id = "non_existent_portfolio"
        
        with pytest.raises(ValueError, match="not found"):
            manager.update_position(fake_id, "600519", 100, 1800.0, "buy")
        
        with pytest.raises(ValueError, match="not found"):
            manager.update_prices(fake_id, {"600519": 1800.0})
        
        with pytest.raises(ValueError, match="not found"):
            manager.get_current_value(fake_id)
        
        with pytest.raises(ValueError, match="not found"):
            manager.get_positions(fake_id)
        
        with pytest.raises(ValueError, match="not found"):
            manager.get_trade_history(fake_id)
        
        with pytest.raises(ValueError, match="not found"):
            manager.get_portfolio_summary(fake_id)
    
    def test_calculate_returns_empty_portfolio(self, manager):
        """
        Test calculating returns for portfolio with no trades.
        测试计算没有交易的投资组合的收益率
        """
        portfolio = manager.create_portfolio(100000.0)
        returns = manager.calculate_returns(portfolio.portfolio_id)
        
        # Should return empty series
        assert len(returns) == 0
    
    def test_multiple_portfolios(self, manager):
        """
        Test managing multiple portfolios simultaneously.
        测试同时管理多个投资组合
        """
        # Create multiple portfolios
        portfolio1 = manager.create_portfolio(100000.0, "portfolio_1")
        portfolio2 = manager.create_portfolio(200000.0, "portfolio_2")
        
        # Trade in portfolio 1
        manager.update_position(
            "portfolio_1",
            symbol="600519",
            quantity=100,
            price=180.0,
            action="buy"
        )
        
        # Trade in portfolio 2
        manager.update_position(
            "portfolio_2",
            symbol="300750",
            quantity=500,
            price=50.0,
            action="buy"
        )
        
        # Verify portfolios are independent
        positions1 = manager.get_positions("portfolio_1")
        positions2 = manager.get_positions("portfolio_2")
        
        assert "600519" in positions1
        assert "600519" not in positions2
        assert "300750" in positions2
        assert "300750" not in positions1
        
        # Verify different cash balances
        assert manager.get_portfolio("portfolio_1").cash != manager.get_portfolio("portfolio_2").cash
