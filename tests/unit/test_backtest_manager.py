"""
回测管理器单元测试 / Backtest Manager Unit Tests
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

from src.application.backtest_manager import (
    BacktestManager,
    BacktestConfig,
    BacktestResult,
    Trade,
    BacktestManagerError
)


class TestBacktestManager:
    """回测管理器测试类 / Backtest Manager Test Class"""
    
    @pytest.fixture
    def mock_qlib_wrapper(self):
        """创建模拟的qlib封装器 / Create mock qlib wrapper"""
        mock = Mock()
        mock.is_initialized.return_value = True
        return mock
    
    @pytest.fixture
    def backtest_manager(self, mock_qlib_wrapper, tmp_path):
        """创建回测管理器实例 / Create backtest manager instance"""
        return BacktestManager(
            qlib_wrapper=mock_qlib_wrapper,
            output_dir=str(tmp_path / "backtests")
        )
    
    @pytest.fixture
    def sample_config(self):
        """创建示例配置 / Create sample configuration"""
        return BacktestConfig(
            strategy_config={
                "instruments": "csi300",
                "topk": 50,
                "n_drop": 5,
            },
            executor_config={
                "time_per_step": "day",
            },
            benchmark="SH000300"
        )
    
    def test_init(self, backtest_manager, tmp_path):
        """测试初始化 / Test initialization"""
        assert backtest_manager is not None
        assert backtest_manager._output_dir == tmp_path / "backtests"
        assert backtest_manager._output_dir.exists()
    
    def test_calculate_metrics_with_empty_returns(self, backtest_manager):
        """测试空收益率序列的指标计算 / Test metrics calculation with empty returns"""
        empty_returns = pd.Series(dtype=float)
        metrics = backtest_manager.calculate_metrics(empty_returns)
        
        assert metrics["total_return"] == 0.0
        assert metrics["annual_return"] == 0.0
        assert metrics["sharpe_ratio"] == 0.0
        assert metrics["max_drawdown"] == 0.0
        assert metrics["volatility"] == 0.0
        assert metrics["win_rate"] == 0.0
    
    def test_calculate_metrics_with_positive_returns(self, backtest_manager):
        """测试正收益率的指标计算 / Test metrics calculation with positive returns"""
        # 创建模拟收益率数据 / Create mock returns data
        dates = pd.date_range(start='2023-01-01', periods=252, freq='D')
        returns = pd.Series(
            np.random.normal(0.001, 0.02, 252),  # 平均日收益0.1%，波动率2%
            index=dates
        )
        
        metrics = backtest_manager.calculate_metrics(returns)
        
        # 验证指标存在 / Verify metrics exist
        assert "total_return" in metrics
        assert "annual_return" in metrics
        assert "sharpe_ratio" in metrics
        assert "max_drawdown" in metrics
        assert "volatility" in metrics
        assert "win_rate" in metrics
        
        # 验证指标类型 / Verify metrics types
        assert isinstance(metrics["total_return"], float)
        assert isinstance(metrics["annual_return"], float)
        assert isinstance(metrics["sharpe_ratio"], float)
        assert isinstance(metrics["max_drawdown"], float)
        assert isinstance(metrics["volatility"], float)
        assert isinstance(metrics["win_rate"], float)
        
        # 验证胜率在合理范围内 / Verify win rate is in reasonable range
        assert 0.0 <= metrics["win_rate"] <= 1.0
    
    def test_calculate_metrics_with_benchmark(self, backtest_manager):
        """测试带基准的指标计算 / Test metrics calculation with benchmark"""
        # 创建模拟收益率和基准数据 / Create mock returns and benchmark data
        dates = pd.date_range(start='2023-01-01', periods=252, freq='D')
        returns = pd.Series(
            np.random.normal(0.001, 0.02, 252),
            index=dates
        )
        benchmark = pd.Series(
            np.random.normal(0.0005, 0.015, 252),
            index=dates
        )
        
        metrics = backtest_manager.calculate_metrics(returns, benchmark)
        
        # 验证超额收益指标存在 / Verify excess return metrics exist
        assert "excess_return" in metrics
        assert "information_ratio" in metrics
        assert "benchmark_return" in metrics
        
        # 验证指标类型 / Verify metrics types
        assert isinstance(metrics["excess_return"], float)
        assert isinstance(metrics["information_ratio"], float)
        assert isinstance(metrics["benchmark_return"], float)
    
    def test_calculate_max_drawdown(self, backtest_manager):
        """测试最大回撤计算 / Test max drawdown calculation"""
        # 创建有明显回撤的累计收益率序列 / Create cumulative returns with obvious drawdown
        cumulative_returns = pd.Series([1.0, 1.1, 1.2, 1.15, 1.05, 1.1, 1.25])
        
        max_dd = backtest_manager._calculate_max_drawdown(cumulative_returns)
        
        # 验证最大回撤是负值 / Verify max drawdown is negative
        assert max_dd <= 0.0
        
        # 验证最大回撤在合理范围内 / Verify max drawdown is in reasonable range
        assert max_dd >= -1.0
    
    def test_calculate_max_drawdown_with_empty_series(self, backtest_manager):
        """测试空序列的最大回撤计算 / Test max drawdown calculation with empty series"""
        empty_series = pd.Series(dtype=float)
        max_dd = backtest_manager._calculate_max_drawdown(empty_series)
        
        assert max_dd == 0.0
    
    def test_extract_trades(self, backtest_manager):
        """测试交易记录提取 / Test trade extraction"""
        # 创建模拟持仓数据 / Create mock position data
        dates = pd.date_range(start='2023-01-01', periods=5, freq='D')
        symbols = ['stock1', 'stock2']
        index = pd.MultiIndex.from_product([dates, symbols], names=['date', 'symbol'])
        positions = pd.DataFrame(
            {'position': [100, 200, 150, 250, 100, 200, 150, 250, 100, 200]},
            index=index
        )
        
        trades = backtest_manager._extract_trades(positions)
        
        # 验证返回的是列表 / Verify returns a list
        assert isinstance(trades, list)
        
        # 验证交易记录的结构 / Verify trade record structure
        if len(trades) > 0:
            assert isinstance(trades[0], Trade)
            assert hasattr(trades[0], 'trade_id')
            assert hasattr(trades[0], 'timestamp')
            assert hasattr(trades[0], 'symbol')
            assert hasattr(trades[0], 'action')
    
    def test_calculate_returns_with_empty_metrics(self, backtest_manager):
        """测试空指标的收益率计算 / Test returns calculation with empty metrics"""
        empty_df = pd.DataFrame()
        
        returns = backtest_manager._calculate_returns(empty_df)
        
        # 验证返回Series / Verify returns Series
        assert isinstance(returns, pd.Series)
    
    @patch('src.application.backtest_manager.pickle.load')
    @patch('builtins.open', create=True)
    def test_load_model_success(self, mock_open, mock_pickle_load, backtest_manager, tmp_path):
        """测试成功加载模型 / Test successful model loading"""
        # 创建模拟模型文件 / Create mock model file
        model_id = "test_model_123"
        model_dir = Path("./outputs/models") / model_id
        model_dir.mkdir(parents=True, exist_ok=True)
        model_path = model_dir / "model.pkl"
        model_path.touch()
        
        # 模拟加载的模型 / Mock loaded model
        mock_model = Mock()
        mock_pickle_load.return_value = mock_model
        
        try:
            model = backtest_manager._load_model(model_id)
            assert model is not None
        finally:
            # 清理 / Cleanup
            import shutil
            if model_dir.exists():
                shutil.rmtree(model_dir.parent)
    
    def test_load_model_not_found(self, backtest_manager):
        """测试模型文件不存在 / Test model file not found"""
        model_id = "nonexistent_model"
        
        with pytest.raises(BacktestManagerError):
            backtest_manager._load_model(model_id)
    
    def test_backtest_config_creation(self):
        """测试回测配置创建 / Test backtest config creation"""
        config = BacktestConfig(
            strategy_config={"topk": 50},
            executor_config={"time_per_step": "day"},
            benchmark="SH000300"
        )
        
        assert config.strategy_config["topk"] == 50
        assert config.executor_config["time_per_step"] == "day"
        assert config.benchmark == "SH000300"
    
    def test_trade_creation(self):
        """测试交易记录创建 / Test trade creation"""
        trade = Trade(
            trade_id="trade_001",
            timestamp="2023-01-01",
            symbol="stock1",
            action="buy",
            quantity=100.0,
            price=10.5,
            commission=1.05,
            total_cost=1051.05
        )
        
        assert trade.trade_id == "trade_001"
        assert trade.symbol == "stock1"
        assert trade.action == "buy"
        assert trade.quantity == 100.0
        assert trade.price == 10.5
    
    def test_backtest_result_creation(self):
        """测试回测结果创建 / Test backtest result creation"""
        returns = pd.Series([0.01, 0.02, -0.01, 0.03])
        positions = pd.DataFrame({'position': [100, 150, 120, 180]})
        metrics = {"total_return": 0.05, "sharpe_ratio": 1.5}
        trades = []
        
        result = BacktestResult(
            returns=returns,
            positions=positions,
            metrics=metrics,
            trades=trades
        )
        
        assert len(result.returns) == 4
        assert len(result.positions) == 4
        assert result.metrics["total_return"] == 0.05
        assert result.metrics["sharpe_ratio"] == 1.5
        assert isinstance(result.trades, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
