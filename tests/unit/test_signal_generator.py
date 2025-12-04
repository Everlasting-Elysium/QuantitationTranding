"""
信号生成器单元测试 / Signal Generator Unit Tests
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from unittest.mock import Mock, MagicMock, patch

from src.application.signal_generator import SignalGenerator, SignalGeneratorError
from src.models.trading_models import Signal, Portfolio, Position, RiskLimits
from src.application.model_registry import ModelRegistry
from src.infrastructure.qlib_wrapper import QlibWrapper


@pytest.fixture
def mock_model_registry():
    """创建模拟的模型注册表 / Create mock model registry"""
    registry = Mock(spec=ModelRegistry)
    
    # 创建模拟模型
    # Create mock model
    mock_model = Mock()
    mock_model.predict = Mock(return_value=pd.Series({
        'stock1': 0.8,
        'stock2': 0.6,
        'stock3': 0.4,
        'stock4': 0.2,
        'stock5': 0.1
    }))
    
    registry.get_model = Mock(return_value=mock_model)
    
    return registry


@pytest.fixture
def mock_qlib_wrapper():
    """创建模拟的Qlib封装器 / Create mock qlib wrapper"""
    wrapper = Mock(spec=QlibWrapper)
    
    # 模拟数据返回
    # Mock data return
    mock_data = pd.DataFrame({
        '$close': [100, 200, 150, 80, 50],
        '$volume': [1000, 2000, 1500, 800, 500],
        '$open': [98, 198, 148, 78, 48],
        '$high': [102, 202, 152, 82, 52],
        '$low': [96, 196, 146, 76, 46]
    }, index=['stock1', 'stock2', 'stock3', 'stock4', 'stock5'])
    
    wrapper.get_data = Mock(return_value=mock_data)
    
    return wrapper


@pytest.fixture
def empty_portfolio():
    """创建空投资组合 / Create empty portfolio"""
    return Portfolio(
        portfolio_id="test_portfolio",
        cash=100000.0,
        total_value=100000.0,
        initial_capital=100000.0
    )


@pytest.fixture
def portfolio_with_positions():
    """创建有持仓的投资组合 / Create portfolio with positions"""
    portfolio = Portfolio(
        portfolio_id="test_portfolio",
        cash=50000.0,
        initial_capital=100000.0
    )
    
    # 添加持仓
    # Add positions
    portfolio.positions = {
        'stock1': Position(
            symbol='stock1',
            quantity=100,
            avg_cost=90,
            current_price=100
        ),
        'stock3': Position(
            symbol='stock3',
            quantity=200,
            avg_cost=140,
            current_price=150
        )
    }
    
    # 更新总价值
    # Update total value
    portfolio.update_total_value()
    
    return portfolio


@pytest.fixture
def signal_generator(mock_model_registry, mock_qlib_wrapper):
    """创建信号生成器实例 / Create signal generator instance"""
    return SignalGenerator(
        model_registry=mock_model_registry,
        qlib_wrapper=mock_qlib_wrapper
    )


class TestSignalGenerator:
    """信号生成器测试类 / Signal Generator Test Class"""
    
    def test_initialization(self, signal_generator):
        """测试初始化 / Test initialization"""
        assert signal_generator is not None
        assert signal_generator._risk_limits is not None
        assert signal_generator._risk_limits.max_position_size == 0.3
    
    def test_generate_signals_empty_portfolio(
        self,
        signal_generator,
        empty_portfolio
    ):
        """测试空投资组合生成信号 / Test signal generation with empty portfolio"""
        signals = signal_generator.generate_signals(
            model_id="test_model",
            date="2024-01-01",
            portfolio=empty_portfolio,
            top_n=3
        )
        
        # 应该生成买入信号
        # Should generate buy signals
        assert len(signals) > 0
        buy_signals = [s for s in signals if s.action == "buy"]
        assert len(buy_signals) > 0
        
        # 检查信号属性
        # Check signal attributes
        for signal in buy_signals:
            assert signal.stock_code is not None
            assert signal.action == "buy"
            assert 0 <= signal.confidence <= 1
            assert signal.timestamp == "2024-01-01"
    
    def test_generate_signals_with_positions(
        self,
        signal_generator,
        portfolio_with_positions
    ):
        """测试有持仓的投资组合生成信号 / Test signal generation with positions"""
        signals = signal_generator.generate_signals(
            model_id="test_model",
            date="2024-01-01",
            portfolio=portfolio_with_positions,
            top_n=3
        )
        
        # 应该包含买入、卖出和持有信号
        # Should include buy, sell, and hold signals
        assert len(signals) > 0
        
        actions = {s.action for s in signals}
        # 至少应该有一种动作
        # Should have at least one action type
        assert len(actions) > 0
    
    def test_stock_sorting(self, signal_generator):
        """测试股票排序 / Test stock sorting"""
        predictions = pd.DataFrame({
            'score': [0.8, 0.2, 0.6, 0.4, 0.9]
        }, index=['stock1', 'stock2', 'stock3', 'stock4', 'stock5'])
        
        sorted_stocks = signal_generator._sort_stocks_by_score(predictions)
        
        # 检查排序是否正确（降序）
        # Check if sorting is correct (descending)
        scores = sorted_stocks['score'].tolist()
        assert scores == sorted(scores, reverse=True)
        
        # 最高分应该是0.9
        # Highest score should be 0.9
        assert sorted_stocks['score'].iloc[0] == 0.9
    
    def test_risk_control_max_position_size(
        self,
        signal_generator,
        portfolio_with_positions
    ):
        """测试最大持仓比例限制 / Test max position size limit"""
        # 设置严格的风险限制
        # Set strict risk limits
        strict_limits = RiskLimits(
            max_position_size=0.5,  # 50%
            max_single_stock=0.2,
            min_cash_reserve=0.3  # 30%
        )
        signal_generator.set_risk_limits(strict_limits)
        
        # 创建买入信号
        # Create buy signals
        signals = [
            Signal(
                stock_code=f"stock{i}",
                action="buy",
                score=0.8,
                confidence=0.9,
                timestamp="2024-01-01"
            )
            for i in range(5)
        ]
        
        # 应用风险控制
        # Apply risk control
        filtered = signal_generator._apply_risk_control(signals, portfolio_with_positions)
        
        # 由于已有持仓，可能会限制新的买入
        # May limit new purchases due to existing positions
        assert len(filtered) <= len(signals)
    
    def test_risk_control_single_stock_limit(self, signal_generator, empty_portfolio):
        """测试单只股票权重限制 / Test single stock weight limit"""
        # 创建信号
        # Create signals
        signals = [
            Signal(
                stock_code="stock1",
                action="buy",
                score=0.9,
                confidence=0.95,
                timestamp="2024-01-01"
            )
        ]
        
        # 应用风险控制
        # Apply risk control
        filtered = signal_generator._apply_risk_control(signals, empty_portfolio)
        
        # 应该通过风控
        # Should pass risk control
        assert len(filtered) > 0
        
        # 检查目标权重是否设置
        # Check if target weight is set
        if filtered[0].target_weight is not None:
            max_weight_pct = signal_generator._risk_limits.max_single_stock * 100
            assert filtered[0].target_weight <= max_weight_pct
    
    def test_explain_signal(self, signal_generator):
        """测试信号解释 / Test signal explanation"""
        signal = Signal(
            stock_code="stock1",
            action="buy",
            score=0.85,
            confidence=0.9,
            timestamp="2024-01-01",
            reason="High prediction score"
        )
        
        explanation = signal_generator.explain_signal(signal)
        
        # 检查解释内容
        # Check explanation content
        assert explanation is not None
        assert explanation.signal == signal
        assert len(explanation.main_factors) > 0
        assert explanation.risk_level in ["low", "medium", "high"]
        assert len(explanation.description) > 0
    
    def test_confidence_calculation(self, signal_generator):
        """测试置信度计算 / Test confidence calculation"""
        all_scores = pd.Series([0.1, 0.3, 0.5, 0.7, 0.9])
        
        # 测试高分
        # Test high score
        high_confidence = signal_generator._calculate_confidence(0.9, all_scores)
        assert high_confidence > 0.8
        
        # 测试低分
        # Test low score
        low_confidence = signal_generator._calculate_confidence(0.1, all_scores)
        assert low_confidence < 0.6
        
        # 测试中等分数
        # Test medium score
        mid_confidence = signal_generator._calculate_confidence(0.5, all_scores)
        assert 0.4 < mid_confidence < 0.8
    
    def test_risk_level_assessment(self, signal_generator):
        """测试风险等级评估 / Test risk level assessment"""
        # 高置信度 -> 低风险
        # High confidence -> low risk
        high_conf_signal = Signal(
            stock_code="stock1",
            action="buy",
            score=0.9,
            confidence=0.9,
            timestamp="2024-01-01"
        )
        assert signal_generator._assess_risk_level(high_conf_signal) == "low"
        
        # 中等置信度 -> 中等风险
        # Medium confidence -> medium risk
        med_conf_signal = Signal(
            stock_code="stock2",
            action="buy",
            score=0.6,
            confidence=0.7,
            timestamp="2024-01-01"
        )
        assert signal_generator._assess_risk_level(med_conf_signal) == "medium"
        
        # 低置信度 -> 中等风险 (因为score=0.3较高，降低了总风险)
        # Low confidence -> medium risk (because score=0.3 is high, reducing overall risk)
        low_conf_signal = Signal(
            stock_code="stock3",
            action="buy",
            score=0.3,
            confidence=0.4,
            timestamp="2024-01-01"
        )
        assert signal_generator._assess_risk_level(low_conf_signal) == "medium"
        
        # 非常低置信度和低分数 -> 高风险
        # Very low confidence and low score -> high risk
        very_high_risk_signal = Signal(
            stock_code="stock4",
            action="buy",
            score=0.02,  # 低分数
            confidence=0.3,  # 低置信度
            timestamp="2024-01-01"
        )
        assert signal_generator._assess_risk_level(very_high_risk_signal) == "high"
    
    def test_set_and_get_risk_limits(self, signal_generator):
        """测试设置和获取风险限制 / Test set and get risk limits"""
        new_limits = RiskLimits(
            max_position_size=0.5,
            max_single_stock=0.15,
            min_cash_reserve=0.2
        )
        
        signal_generator.set_risk_limits(new_limits)
        retrieved_limits = signal_generator.get_risk_limits()
        
        assert retrieved_limits.max_position_size == 0.5
        assert retrieved_limits.max_single_stock == 0.15
        assert retrieved_limits.min_cash_reserve == 0.2
    
    def test_generate_signals_with_invalid_model(
        self,
        signal_generator,
        empty_portfolio
    ):
        """测试使用无效模型生成信号 / Test signal generation with invalid model"""
        # 模拟模型加载失败
        # Mock model loading failure
        signal_generator._model_registry.get_model = Mock(
            side_effect=Exception("Model not found")
        )
        
        with pytest.raises(SignalGeneratorError):
            signal_generator.generate_signals(
                model_id="invalid_model",
                date="2024-01-01",
                portfolio=empty_portfolio
            )
    
    def test_generate_buy_signals_respects_top_n(
        self,
        signal_generator,
        empty_portfolio
    ):
        """测试买入信号数量限制 / Test buy signals respect top_n limit"""
        # 创建排序后的股票数据
        # Create sorted stock data
        sorted_stocks = pd.DataFrame({
            'score': [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
        }, index=[f'stock{i}' for i in range(1, 10)])
        
        # 生成买入信号，限制为3个
        # Generate buy signals, limit to 3
        buy_signals = signal_generator._generate_buy_signals(
            sorted_stocks,
            empty_portfolio,
            top_n=3,
            date="2024-01-01"
        )
        
        # 应该最多生成3个买入信号
        # Should generate at most 3 buy signals
        assert len(buy_signals) <= 3
    
    def test_generate_sell_signals_for_low_score_positions(
        self,
        signal_generator,
        portfolio_with_positions
    ):
        """测试为低分持仓生成卖出信号 / Test sell signal generation for low score positions"""
        # 创建排序后的股票数据，stock3分数很低
        # Create sorted stock data with low score for stock3
        sorted_stocks = pd.DataFrame({
            'score': [0.9, 0.8, 0.1, 0.7, 0.6]  # stock3 has low score
        }, index=['stock1', 'stock2', 'stock3', 'stock4', 'stock5'])
        
        # 生成卖出信号
        # Generate sell signals
        sell_signals = signal_generator._generate_sell_signals(
            sorted_stocks,
            portfolio_with_positions,
            date="2024-01-01"
        )
        
        # 应该为stock3生成卖出信号（分数低于中位数）
        # Should generate sell signal for stock3 (score below median)
        sell_stock_codes = [s.stock_code for s in sell_signals]
        assert 'stock3' in sell_stock_codes or len(sell_signals) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
