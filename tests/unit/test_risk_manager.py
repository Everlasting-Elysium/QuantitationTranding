"""
Unit tests for Risk Manager.
风险管理器的单元测试
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime

from src.core.risk_manager import RiskManager
from src.models.trading_models import Portfolio, Position, Trade


@pytest.fixture
def risk_manager():
    """Create a RiskManager instance for testing."""
    return RiskManager(
        max_position_pct=0.3,
        max_sector_pct=0.4,
        max_drawdown_pct=0.2,
        max_daily_loss_pct=0.05,
        var_confidence=0.95
    )


@pytest.fixture
def sample_portfolio():
    """Create a sample portfolio for testing."""
    portfolio = Portfolio(
        portfolio_id="test_portfolio",
        positions={
            "AAPL": Position(
                symbol="AAPL",
                quantity=100,
                avg_cost=150.0,
                current_price=160.0
            ),
            "GOOGL": Position(
                symbol="GOOGL",
                quantity=50,
                avg_cost=2800.0,
                current_price=2900.0
            )
        },
        cash=50000.0,
        initial_capital=200000.0
    )
    portfolio.update_total_value()
    return portfolio


@pytest.fixture
def sample_trade():
    """Create a sample trade for testing."""
    return Trade(
        trade_id="trade_001",
        timestamp=datetime.now().isoformat(),
        symbol="MSFT",
        action="buy",
        quantity=100,
        price=300.0,
        commission=10.0
    )



class TestRiskManagerInitialization:
    """Test RiskManager initialization."""
    
    def test_initialization_with_defaults(self):
        """Test initialization with default parameters."""
        rm = RiskManager()
        assert rm.max_position_pct == 0.3
        assert rm.max_sector_pct == 0.4
        assert rm.max_drawdown_pct == 0.2
        assert rm.max_daily_loss_pct == 0.05
        assert rm.var_confidence == 0.95
    
    def test_initialization_with_custom_params(self):
        """Test initialization with custom parameters."""
        rm = RiskManager(
            max_position_pct=0.25,
            max_sector_pct=0.35,
            max_drawdown_pct=0.15,
            max_daily_loss_pct=0.03,
            var_confidence=0.99
        )
        assert rm.max_position_pct == 0.25
        assert rm.max_sector_pct == 0.35
        assert rm.max_drawdown_pct == 0.15
        assert rm.max_daily_loss_pct == 0.03
        assert rm.var_confidence == 0.99


class TestPositionRiskCheck:
    """Test position risk checking functionality."""
    
    def test_check_position_risk_within_limits(self, risk_manager, sample_portfolio):
        """Test risk check when trade is within limits."""
        # Small trade that won't violate limits
        trade = Trade(
            trade_id="trade_001",
            timestamp=datetime.now().isoformat(),
            symbol="MSFT",
            action="buy",
            quantity=50,
            price=300.0,
            commission=10.0
        )
        
        result = risk_manager.check_position_risk(sample_portfolio, trade)
        
        assert result['passed'] is True
        assert result['risk_score'] >= 0
        assert isinstance(result['warnings'], list)
        assert isinstance(result['violations'], list)
    
    def test_check_position_risk_exceeds_limit(self, risk_manager):
        """Test risk check when trade exceeds position limit."""
        # Create portfolio with enough cash for the trade
        portfolio = Portfolio(
            portfolio_id="test",
            positions={
                "AAPL": Position("AAPL", 100, 150.0, 160.0)
            },
            cash=200000.0,  # Enough cash for large trade
            initial_capital=300000.0
        )
        portfolio.update_total_value()
        
        # Large trade that will violate position limit (30% of portfolio)
        # Portfolio value ~216,000, 30% = 64,800
        # This trade = 500 * 300 = 150,000 which is > 64,800
        trade = Trade(
            trade_id="trade_002",
            timestamp=datetime.now().isoformat(),
            symbol="MSFT",
            action="buy",
            quantity=500,
            price=300.0,
            commission=10.0
        )
        
        result = risk_manager.check_position_risk(portfolio, trade)
        
        # The trade should violate position limits
        assert result['passed'] is False
        assert len(result['violations']) > 0
        assert 'max_quantity' in result['suggested_adjustments']
    
    def test_check_position_risk_with_sector_map(self, risk_manager, sample_portfolio):
        """Test risk check with sector concentration."""
        sector_map = {
            "AAPL": "Technology",
            "GOOGL": "Technology",
            "MSFT": "Technology"
        }
        
        # Trade that increases tech sector concentration
        trade = Trade(
            trade_id="trade_003",
            timestamp=datetime.now().isoformat(),
            symbol="MSFT",
            action="buy",
            quantity=200,
            price=300.0,
            commission=10.0
        )
        
        result = risk_manager.check_position_risk(sample_portfolio, trade, sector_map)
        
        # Should have warnings or violations about sector concentration
        assert result['risk_score'] > 0


class TestVaRCalculation:
    """Test Value at Risk calculation."""
    
    def test_calculate_var_with_normal_returns(self, risk_manager):
        """Test VaR calculation with normal distribution returns."""
        # Generate sample returns
        np.random.seed(42)
        returns = pd.Series(np.random.normal(0.001, 0.02, 100))
        portfolio_value = 100000.0
        
        var = risk_manager.calculate_var(returns, portfolio_value)
        
        assert var > 0
        assert isinstance(var, float)
    
    def test_calculate_var_with_insufficient_data(self, risk_manager):
        """Test VaR calculation with insufficient data."""
        returns = pd.Series([0.01])
        portfolio_value = 100000.0
        
        var = risk_manager.calculate_var(returns, portfolio_value)
        
        assert var == 0.0
    
    def test_calculate_var_with_custom_confidence(self, risk_manager):
        """Test VaR calculation with custom confidence level."""
        np.random.seed(42)
        returns = pd.Series(np.random.normal(0.001, 0.02, 100))
        portfolio_value = 100000.0
        
        var_95 = risk_manager.calculate_var(returns, portfolio_value, confidence=0.95)
        var_99 = risk_manager.calculate_var(returns, portfolio_value, confidence=0.99)
        
        # Higher confidence should give higher VaR
        assert var_99 > var_95


class TestMaxDrawdownCalculation:
    """Test maximum drawdown calculation."""
    
    def test_calculate_max_drawdown_with_losses(self, risk_manager):
        """Test max drawdown calculation with losing returns."""
        # Create returns with a drawdown
        returns = pd.Series([0.02, 0.01, -0.05, -0.03, -0.02, 0.01, 0.02])
        
        max_dd = risk_manager.calculate_max_drawdown(returns)
        
        assert max_dd > 0
        assert max_dd <= 1.0
    
    def test_calculate_max_drawdown_with_gains(self, risk_manager):
        """Test max drawdown calculation with only gains."""
        returns = pd.Series([0.01, 0.02, 0.01, 0.03])
        
        max_dd = risk_manager.calculate_max_drawdown(returns)
        
        assert max_dd >= 0
    
    def test_calculate_max_drawdown_insufficient_data(self, risk_manager):
        """Test max drawdown with insufficient data."""
        returns = pd.Series([0.01])
        
        max_dd = risk_manager.calculate_max_drawdown(returns)
        
        assert max_dd == 0.0


class TestConcentrationRisk:
    """Test concentration risk checking."""
    
    def test_check_concentration_risk_low(self, risk_manager):
        """Test concentration risk with diversified portfolio."""
        portfolio = Portfolio(
            portfolio_id="test",
            positions={
                "AAPL": Position("AAPL", 100, 150.0, 160.0),
                "GOOGL": Position("GOOGL", 50, 2800.0, 2900.0),
                "MSFT": Position("MSFT", 100, 300.0, 310.0),
                "AMZN": Position("AMZN", 30, 3000.0, 3100.0)
            },
            cash=50000.0,
            initial_capital=500000.0
        )
        portfolio.update_total_value()
        
        sector_map = {
            "AAPL": "Technology",
            "GOOGL": "Technology",
            "MSFT": "Technology",
            "AMZN": "Consumer"
        }
        
        result = risk_manager.check_concentration_risk(portfolio, sector_map)
        
        assert 'max_position_pct' in result
        assert 'top_5_concentration' in result
        assert 'sector_concentration' in result
        assert 'risk_level' in result
        assert result['risk_level'] in ['low', 'medium', 'high']
    
    def test_check_concentration_risk_high(self, risk_manager):
        """Test concentration risk with concentrated portfolio."""
        portfolio = Portfolio(
            portfolio_id="test",
            positions={
                "AAPL": Position("AAPL", 1000, 150.0, 160.0)
            },
            cash=10000.0,
            initial_capital=200000.0
        )
        portfolio.update_total_value()
        
        sector_map = {"AAPL": "Technology"}
        
        result = risk_manager.check_concentration_risk(portfolio, sector_map)
        
        assert result['risk_level'] == 'high'
        assert result['max_position_pct'] > 50
    
    def test_check_concentration_risk_empty_portfolio(self, risk_manager):
        """Test concentration risk with empty portfolio."""
        portfolio = Portfolio(
            portfolio_id="test",
            positions={},
            cash=100000.0,
            initial_capital=100000.0
        )
        
        result = risk_manager.check_concentration_risk(portfolio, {})
        
        assert result['risk_level'] == 'low'
        assert result['max_position_pct'] == 0.0



class TestRiskAlertGeneration:
    """Test risk alert generation."""
    
    def test_generate_risk_alert_no_issues(self, risk_manager, sample_portfolio):
        """Test alert generation when no issues exist."""
        # Normal returns with no issues
        returns = pd.Series([0.01, 0.02, 0.01, -0.01, 0.02])
        
        alert = risk_manager.generate_risk_alert(sample_portfolio, returns)
        
        # Should return None when no issues
        assert alert is None
    
    def test_generate_risk_alert_high_drawdown(self, risk_manager, sample_portfolio):
        """Test alert generation for high drawdown."""
        # Returns with high drawdown
        returns = pd.Series([0.02, -0.10, -0.08, -0.05, -0.03])
        
        alert = risk_manager.generate_risk_alert(sample_portfolio, returns)
        
        assert alert is not None
        assert 'drawdown' in alert['message'].lower()
        assert alert['severity'] in ['info', 'warning', 'critical']
    
    def test_generate_risk_alert_daily_loss(self, risk_manager, sample_portfolio):
        """Test alert generation for excessive daily loss."""
        # Returns with large daily loss
        returns = pd.Series([0.01, 0.02, -0.08])
        
        alert = risk_manager.generate_risk_alert(sample_portfolio, returns)
        
        assert alert is not None
        assert 'loss' in alert['message'].lower()
        assert alert['severity'] == 'critical'
    
    def test_generate_risk_alert_concentration(self, risk_manager):
        """Test alert generation for concentration risk."""
        # Highly concentrated portfolio
        portfolio = Portfolio(
            portfolio_id="test",
            positions={
                "AAPL": Position("AAPL", 1000, 150.0, 160.0)
            },
            cash=10000.0,
            initial_capital=200000.0
        )
        portfolio.update_total_value()
        
        returns = pd.Series([0.01, 0.02])
        sector_map = {"AAPL": "Technology"}
        
        alert = risk_manager.generate_risk_alert(portfolio, returns, sector_map)
        
        assert alert is not None
        assert 'concentration' in alert['message'].lower()
    
    def test_generate_risk_alert_position_loss(self, risk_manager):
        """Test alert generation for individual position losses."""
        # Portfolio with losing position
        portfolio = Portfolio(
            portfolio_id="test",
            positions={
                "AAPL": Position("AAPL", 100, 200.0, 150.0)  # 25% loss
            },
            cash=50000.0,
            initial_capital=100000.0
        )
        portfolio.update_total_value()
        
        returns = pd.Series([0.01, 0.02])
        
        alert = risk_manager.generate_risk_alert(portfolio, returns)
        
        assert alert is not None
        assert "AAPL" in alert['affected_positions']



class TestRiskMitigation:
    """Test risk mitigation suggestions."""
    
    def test_suggest_risk_mitigation_critical(self, risk_manager):
        """Test mitigation suggestions for critical alerts."""
        alert = {
            'alert_id': 'test_001',
            'severity': 'critical',
            'message': 'Maximum drawdown exceeded',
            'affected_positions': ['AAPL', 'GOOGL'],
            'recommended_actions': ['Reduce positions']
        }
        
        suggestions = risk_manager.suggest_risk_mitigation(alert)
        
        assert len(suggestions) > 0
        assert any('immediate' in s.lower() for s in suggestions)
    
    def test_suggest_risk_mitigation_drawdown(self, risk_manager):
        """Test mitigation suggestions for drawdown issues."""
        alert = {
            'alert_id': 'test_002',
            'severity': 'warning',
            'message': 'High drawdown detected',
            'affected_positions': [],
            'recommended_actions': []
        }
        
        suggestions = risk_manager.suggest_risk_mitigation(alert)
        
        assert any('position' in s.lower() or 'cash' in s.lower() for s in suggestions)
    
    def test_suggest_risk_mitigation_concentration(self, risk_manager):
        """Test mitigation suggestions for concentration issues."""
        alert = {
            'alert_id': 'test_003',
            'severity': 'warning',
            'message': 'High concentration risk',
            'affected_positions': ['AAPL'],
            'recommended_actions': []
        }
        
        suggestions = risk_manager.suggest_risk_mitigation(alert)
        
        assert any('diversif' in s.lower() or 'rebalance' in s.lower() for s in suggestions)


class TestPortfolioTracking:
    """Test portfolio value tracking for drawdown."""
    
    def test_track_portfolio_value(self, risk_manager):
        """Test tracking portfolio values."""
        portfolio_id = "test_portfolio"
        
        risk_manager.track_portfolio_value(portfolio_id, 100000.0)
        risk_manager.track_portfolio_value(portfolio_id, 105000.0)
        risk_manager.track_portfolio_value(portfolio_id, 103000.0)
        
        assert portfolio_id in risk_manager._portfolio_history
        assert len(risk_manager._portfolio_history[portfolio_id]) == 3
    
    def test_get_portfolio_drawdown(self, risk_manager):
        """Test getting current drawdown."""
        portfolio_id = "test_portfolio"
        
        risk_manager.track_portfolio_value(portfolio_id, 100000.0)
        risk_manager.track_portfolio_value(portfolio_id, 110000.0)
        risk_manager.track_portfolio_value(portfolio_id, 95000.0)
        
        drawdown = risk_manager.get_portfolio_drawdown(portfolio_id)
        
        assert drawdown > 0
        assert drawdown < 1.0
    
    def test_get_portfolio_drawdown_no_history(self, risk_manager):
        """Test getting drawdown with no history."""
        drawdown = risk_manager.get_portfolio_drawdown("nonexistent")
        
        assert drawdown == 0.0
    
    def test_reset_portfolio_history(self, risk_manager):
        """Test resetting portfolio history."""
        portfolio_id = "test_portfolio"
        
        risk_manager.track_portfolio_value(portfolio_id, 100000.0)
        risk_manager.track_portfolio_value(portfolio_id, 105000.0)
        
        risk_manager.reset_portfolio_history(portfolio_id)
        
        assert portfolio_id not in risk_manager._portfolio_history
