"""
Unit tests for PerformanceAnalyzer
表现分析器的单元测试
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock, patch

from src.application.performance_analyzer import PerformanceAnalyzer
from src.models.market_models import (
    AssetMetrics, AssetRecommendation, PerformanceReport
)
from src.infrastructure.qlib_wrapper import QlibWrapper
from src.utils.error_handler import DataError


class TestPerformanceAnalyzer:
    """Test suite for PerformanceAnalyzer / PerformanceAnalyzer测试套件"""
    
    @pytest.fixture
    def mock_qlib_wrapper(self):
        """Create a mock QlibWrapper / 创建模拟的QlibWrapper"""
        mock = Mock(spec=QlibWrapper)
        return mock
    
    @pytest.fixture
    def analyzer(self, mock_qlib_wrapper):
        """Create PerformanceAnalyzer instance / 创建PerformanceAnalyzer实例"""
        return PerformanceAnalyzer(qlib_wrapper=mock_qlib_wrapper)
    
    @pytest.fixture
    def sample_price_data(self):
        """Generate sample price data / 生成样本价格数据"""
        dates = pd.date_range(start='2021-01-01', end='2024-01-01', freq='D')
        # Generate random walk price data
        np.random.seed(42)
        returns = np.random.normal(0.001, 0.02, len(dates))
        prices = 100 * (1 + returns).cumprod()
        
        df = pd.DataFrame({
            '$close': prices
        }, index=dates)
        
        return df
    
    def test_initialization(self, analyzer):
        """Test PerformanceAnalyzer initialization / 测试初始化"""
        assert analyzer is not None
        assert analyzer.risk_free_rate == 0.03
        assert analyzer.qlib_wrapper is not None
    
    def test_set_risk_free_rate(self, analyzer):
        """Test setting risk-free rate / 测试设置无风险利率"""
        analyzer.set_risk_free_rate(0.025)
        assert analyzer.risk_free_rate == 0.025
        
        analyzer.set_risk_free_rate(0.04)
        assert analyzer.risk_free_rate == 0.04
    
    def test_get_asset_metrics_with_valid_data(self, analyzer, mock_qlib_wrapper, sample_price_data):
        """Test calculating metrics with valid data / 测试使用有效数据计算指标"""
        # Setup mock
        mock_qlib_wrapper.get_data.return_value = sample_price_data
        
        # Calculate metrics
        metrics = analyzer.get_asset_metrics(
            asset_code="TEST001",
            start_date="2021-01-01",
            end_date="2024-01-01"
        )
        
        # Verify
        assert metrics is not None
        assert isinstance(metrics, AssetMetrics)
        assert metrics.symbol == "TEST001"
        assert metrics.period_start == "2021-01-01"
        assert metrics.period_end == "2024-01-01"
        
        # Check that metrics are calculated
        assert isinstance(metrics.total_return, float)
        assert isinstance(metrics.annual_return, float)
        assert isinstance(metrics.volatility, float)
        assert isinstance(metrics.sharpe_ratio, float)
        assert isinstance(metrics.max_drawdown, float)
        assert isinstance(metrics.win_rate, float)
        
        # Check reasonable ranges
        assert -1.0 <= metrics.total_return <= 10.0
        assert -1.0 <= metrics.annual_return <= 2.0
        assert 0.0 <= metrics.volatility <= 2.0
        assert -10.0 <= metrics.sharpe_ratio <= 10.0
        assert -1.0 <= metrics.max_drawdown <= 0.0
        assert 0.0 <= metrics.win_rate <= 1.0
    
    def test_get_asset_metrics_with_empty_data(self, analyzer, mock_qlib_wrapper):
        """Test calculating metrics with empty data / 测试使用空数据计算指标"""
        # Setup mock to return empty DataFrame
        mock_qlib_wrapper.get_data.return_value = pd.DataFrame()
        
        # Calculate metrics
        metrics = analyzer.get_asset_metrics(
            asset_code="TEST001",
            start_date="2021-01-01",
            end_date="2024-01-01"
        )
        
        # Should return None for empty data
        assert metrics is None
    
    def test_get_asset_metrics_with_insufficient_data(self, analyzer, mock_qlib_wrapper):
        """Test calculating metrics with insufficient data / 测试使用不足数据计算指标"""
        # Create DataFrame with only a few data points
        dates = pd.date_range(start='2021-01-01', periods=10, freq='D')
        prices = pd.Series(range(100, 110), index=dates)
        df = pd.DataFrame({'$close': prices})
        
        mock_qlib_wrapper.get_data.return_value = df
        
        # Calculate metrics
        metrics = analyzer.get_asset_metrics(
            asset_code="TEST001",
            start_date="2021-01-01",
            end_date="2021-01-10"
        )
        
        # Should return None for insufficient data
        assert metrics is None
    
    def test_rank_assets(self, analyzer):
        """Test asset ranking / 测试资产排名"""
        # Create sample metrics
        metrics_list = [
            AssetMetrics(
                symbol="ASSET1",
                period_start="2021-01-01",
                period_end="2024-01-01",
                total_return=0.5,
                annual_return=0.15,
                volatility=0.2,
                sharpe_ratio=1.5,
                max_drawdown=-0.15,
                win_rate=0.6
            ),
            AssetMetrics(
                symbol="ASSET2",
                period_start="2021-01-01",
                period_end="2024-01-01",
                total_return=0.3,
                annual_return=0.10,
                volatility=0.15,
                sharpe_ratio=1.0,
                max_drawdown=-0.20,
                win_rate=0.55
            ),
            AssetMetrics(
                symbol="ASSET3",
                period_start="2021-01-01",
                period_end="2024-01-01",
                total_return=0.7,
                annual_return=0.20,
                volatility=0.25,
                sharpe_ratio=1.8,
                max_drawdown=-0.10,
                win_rate=0.65
            )
        ]
        
        # Rank assets
        recommendations = analyzer._rank_assets(metrics_list, top_n=3)
        
        # Verify
        assert len(recommendations) == 3
        assert all(isinstance(rec, AssetRecommendation) for rec in recommendations)
        
        # Check that they are sorted by performance score
        scores = [rec.performance_score for rec in recommendations]
        assert scores == sorted(scores, reverse=True)
        
        # Check ranks are assigned
        assert recommendations[0].rank == 1
        assert recommendations[1].rank == 2
        assert recommendations[2].rank == 3
        
        # Best performer should be ASSET3 (highest Sharpe and return)
        assert recommendations[0].symbol == "ASSET3"
    
    def test_generate_recommendation_reason(self, analyzer):
        """Test recommendation reason generation / 测试推荐理由生成"""
        metrics = AssetMetrics(
            symbol="TEST001",
            period_start="2021-01-01",
            period_end="2024-01-01",
            total_return=0.6,
            annual_return=0.18,
            volatility=0.2,
            sharpe_ratio=1.6,
            max_drawdown=-0.12,
            win_rate=0.62
        )
        
        reason = analyzer._generate_recommendation_reason(metrics, 85.0)
        
        # Verify reason is generated
        assert isinstance(reason, str)
        assert len(reason) > 0
        
        # Should contain some key phrases
        assert any(keyword in reason for keyword in [
            "风险调整后收益", "年化收益率", "回撤控制", "胜率"
        ])
    
    def test_get_default_instruments(self, analyzer):
        """Test getting default instruments / 测试获取默认工具"""
        # Test various market/asset type combinations
        assert analyzer._get_default_instruments("CN", "stock") == "csi300"
        assert analyzer._get_default_instruments("US", "stock") == "sp500"
        assert analyzer._get_default_instruments("HK", "stock") == "hsi"
        assert analyzer._get_default_instruments("CN", "fund") == "all"
        assert analyzer._get_default_instruments("UNKNOWN", "UNKNOWN") == "all"
    
    def test_get_instrument_list(self, analyzer, mock_qlib_wrapper):
        """Test getting instrument list / 测试获取工具列表"""
        # Setup mock
        expected_instruments = ["STOCK1", "STOCK2", "STOCK3"]
        mock_qlib_wrapper.get_instruments.return_value = expected_instruments
        
        # Get instruments
        instruments = analyzer._get_instrument_list("csi300")
        
        # Verify
        assert instruments == expected_instruments
        mock_qlib_wrapper.get_instruments.assert_called_once_with(market="csi300")
    
    def test_get_instrument_list_empty(self, analyzer, mock_qlib_wrapper):
        """Test getting empty instrument list / 测试获取空工具列表"""
        # Setup mock to return None
        mock_qlib_wrapper.get_instruments.return_value = None
        
        # Get instruments
        instruments = analyzer._get_instrument_list("invalid_pool")
        
        # Should return empty list
        assert instruments == []
    
    def test_analyze_historical_performance_no_instruments(self, analyzer, mock_qlib_wrapper):
        """Test analysis with no instruments found / 测试未找到工具的分析"""
        # Setup mock to return empty list
        mock_qlib_wrapper.get_instruments.return_value = []
        
        # Should raise DataError
        with pytest.raises(DataError) as exc_info:
            analyzer.analyze_historical_performance(
                market="CN",
                asset_type="stock",
                lookback_years=3,
                instruments="invalid_pool"
            )
        
        # Verify error code
        assert exc_info.value.error_info.error_code == "PERF0001"
    
    def test_analyze_historical_performance_no_successful_analysis(self, analyzer, mock_qlib_wrapper):
        """Test analysis with no successful asset analysis / 测试没有成功分析资产的情况"""
        # Setup mock
        mock_qlib_wrapper.get_instruments.return_value = ["STOCK1", "STOCK2"]
        mock_qlib_wrapper.get_data.return_value = pd.DataFrame()  # Empty data
        
        # Should raise DataError
        with pytest.raises(DataError) as exc_info:
            analyzer.analyze_historical_performance(
                market="CN",
                asset_type="stock",
                lookback_years=3,
                instruments="csi300"
            )
        
        # Verify error code
        assert exc_info.value.error_info.error_code == "PERF0002"
    
    def test_recommend_top_performers(self, analyzer, mock_qlib_wrapper, sample_price_data):
        """Test generating recommendations / 测试生成推荐"""
        # Setup mock
        mock_qlib_wrapper.get_instruments.return_value = ["STOCK1", "STOCK2", "STOCK3"]
        mock_qlib_wrapper.get_data.return_value = sample_price_data
        
        # Generate recommendations
        recommendations = analyzer.recommend_top_performers(
            market="CN",
            asset_type="stock",
            top_n=3,
            criteria="sharpe_ratio",
            lookback_years=3
        )
        
        # Verify
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 3
        assert all(isinstance(rec, AssetRecommendation) for rec in recommendations)
        
        # Check that recommendations have required fields
        for rec in recommendations:
            assert rec.symbol is not None
            assert rec.performance_score >= 0
            assert rec.rank > 0


class TestAssetMetrics:
    """Test suite for AssetMetrics dataclass / AssetMetrics数据类测试套件"""
    
    def test_asset_metrics_creation(self):
        """Test creating AssetMetrics / 测试创建AssetMetrics"""
        metrics = AssetMetrics(
            symbol="TEST001",
            period_start="2021-01-01",
            period_end="2024-01-01",
            total_return=0.5,
            annual_return=0.15,
            volatility=0.2,
            sharpe_ratio=1.5,
            max_drawdown=-0.15,
            win_rate=0.6
        )
        
        assert metrics.symbol == "TEST001"
        assert metrics.total_return == 0.5
        assert metrics.annual_return == 0.15
    
    def test_asset_metrics_validation(self):
        """Test AssetMetrics validation / 测试AssetMetrics验证"""
        # Empty symbol should raise error
        with pytest.raises(ValueError):
            AssetMetrics(
                symbol="",
                period_start="2021-01-01",
                period_end="2024-01-01",
                total_return=0.5,
                annual_return=0.15,
                volatility=0.2,
                sharpe_ratio=1.5,
                max_drawdown=-0.15,
                win_rate=0.6
            )


class TestAssetRecommendation:
    """Test suite for AssetRecommendation dataclass / AssetRecommendation数据类测试套件"""
    
    def test_asset_recommendation_creation(self):
        """Test creating AssetRecommendation / 测试创建AssetRecommendation"""
        rec = AssetRecommendation(
            symbol="TEST001",
            name="Test Asset",
            asset_type="stock",
            performance_score=85.0,
            sharpe_ratio=1.5,
            annual_return=0.15,
            max_drawdown=-0.15,
            recommendation_reason="优秀表现",
            rank=1
        )
        
        assert rec.symbol == "TEST001"
        assert rec.performance_score == 85.0
        assert rec.rank == 1
    
    def test_asset_recommendation_validation(self):
        """Test AssetRecommendation validation / 测试AssetRecommendation验证"""
        # Empty symbol should raise error
        with pytest.raises(ValueError):
            AssetRecommendation(
                symbol="",
                name="Test",
                asset_type="stock",
                performance_score=85.0,
                sharpe_ratio=1.5,
                annual_return=0.15,
                max_drawdown=-0.15,
                recommendation_reason="Test",
                rank=1
            )
        
        # Invalid performance score should raise error
        with pytest.raises(ValueError):
            AssetRecommendation(
                symbol="TEST001",
                name="Test",
                asset_type="stock",
                performance_score=150.0,  # > 100
                sharpe_ratio=1.5,
                annual_return=0.15,
                max_drawdown=-0.15,
                recommendation_reason="Test",
                rank=1
            )


class TestPerformanceReport:
    """Test suite for PerformanceReport dataclass / PerformanceReport数据类测试套件"""
    
    def test_performance_report_creation(self):
        """Test creating PerformanceReport / 测试创建PerformanceReport"""
        recommendations = [
            AssetRecommendation(
                symbol="TEST001",
                name="Test Asset",
                asset_type="stock",
                performance_score=85.0,
                sharpe_ratio=1.5,
                annual_return=0.15,
                max_drawdown=-0.15,
                recommendation_reason="优秀表现",
                rank=1
            )
        ]
        
        report = PerformanceReport(
            market="CN",
            asset_type="stock",
            analysis_period_start="2021-01-01",
            analysis_period_end="2024-01-01",
            total_assets_analyzed=100,
            top_performers=recommendations,
            average_return=0.12,
            average_sharpe=1.2,
            average_drawdown=-0.20,
            analysis_timestamp="2024-01-01 12:00:00"
        )
        
        assert report.market == "CN"
        assert report.total_assets_analyzed == 100
        assert len(report.top_performers) == 1
    
    def test_performance_report_validation(self):
        """Test PerformanceReport validation / 测试PerformanceReport验证"""
        # Empty market should raise error
        with pytest.raises(ValueError):
            PerformanceReport(
                market="",
                asset_type="stock",
                analysis_period_start="2021-01-01",
                analysis_period_end="2024-01-01",
                total_assets_analyzed=100,
                top_performers=[],
                average_return=0.12,
                average_sharpe=1.2,
                average_drawdown=-0.20,
                analysis_timestamp="2024-01-01 12:00:00"
            )
        
        # Negative total_assets_analyzed should raise error
        with pytest.raises(ValueError):
            PerformanceReport(
                market="CN",
                asset_type="stock",
                analysis_period_start="2021-01-01",
                analysis_period_end="2024-01-01",
                total_assets_analyzed=-1,
                top_performers=[],
                average_return=0.12,
                average_sharpe=1.2,
                average_drawdown=-0.20,
                analysis_timestamp="2024-01-01 12:00:00"
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
