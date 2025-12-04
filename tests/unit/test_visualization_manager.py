"""
可视化管理器单元测试 / Visualization Manager Unit Tests
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

from src.application.visualization_manager import (
    VisualizationManager,
    VisualizationManagerError
)


@pytest.fixture
def viz_manager(tmp_path):
    """创建可视化管理器实例 / Create visualization manager instance"""
    return VisualizationManager(output_dir=str(tmp_path / "visualizations"))


@pytest.fixture
def sample_returns():
    """生成示例收益率数据 / Generate sample returns data"""
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    returns = pd.Series(np.random.normal(0.001, 0.02, len(dates)), index=dates)
    return returns


@pytest.fixture
def sample_portfolio():
    """生成示例持仓数据 / Generate sample portfolio data"""
    return {
        "股票A": 0.3,
        "股票B": 0.25,
        "股票C": 0.2,
        "股票D": 0.15,
        "股票E": 0.1,
    }


@pytest.fixture
def sample_sector_weights():
    """生成示例行业权重数据 / Generate sample sector weights data"""
    return {
        "科技": 0.35,
        "金融": 0.25,
        "消费": 0.20,
        "医疗": 0.15,
        "其他": 0.05,
    }


class TestVisualizationManager:
    """可视化管理器测试类 / Visualization Manager Test Class"""
    
    def test_initialization(self, tmp_path):
        """测试初始化 / Test initialization"""
        output_dir = tmp_path / "viz_output"
        viz_manager = VisualizationManager(output_dir=str(output_dir))
        
        assert viz_manager._output_dir == output_dir
        assert output_dir.exists()
    
    def test_plot_cumulative_returns(self, viz_manager, sample_returns):
        """测试累计收益曲线图生成 / Test cumulative returns chart generation"""
        chart_path = viz_manager.plot_cumulative_returns(
            returns=sample_returns,
            title="测试累计收益"
        )
        
        assert Path(chart_path).exists()
        assert Path(chart_path).suffix == '.png'
        assert Path(chart_path).stat().st_size > 0
    
    def test_plot_cumulative_returns_with_benchmark(self, viz_manager, sample_returns):
        """测试带基准的累计收益曲线图 / Test cumulative returns chart with benchmark"""
        benchmark = pd.Series(
            np.random.normal(0.0008, 0.015, len(sample_returns)),
            index=sample_returns.index
        )
        
        chart_path = viz_manager.plot_cumulative_returns(
            returns=sample_returns,
            benchmark=benchmark,
            title="策略 vs 基准"
        )
        
        assert Path(chart_path).exists()
    
    def test_plot_position_distribution(self, viz_manager, sample_portfolio):
        """测试持仓分布图生成 / Test position distribution chart generation"""
        chart_path = viz_manager.plot_position_distribution(
            portfolio=sample_portfolio,
            title="测试持仓分布"
        )
        
        assert Path(chart_path).exists()
        assert Path(chart_path).suffix == '.png'
        assert Path(chart_path).stat().st_size > 0
    
    def test_plot_position_distribution_empty(self, viz_manager):
        """测试空持仓分布图 / Test empty position distribution chart"""
        chart_path = viz_manager.plot_position_distribution(
            portfolio={},
            title="空持仓"
        )
        
        # 应该生成一个空图表 / Should generate an empty chart
        assert Path(chart_path).exists()
    
    def test_plot_sector_distribution(self, viz_manager, sample_sector_weights):
        """测试行业分布图生成 / Test sector distribution chart generation"""
        chart_path = viz_manager.plot_sector_distribution(
            sector_weights=sample_sector_weights,
            title="测试行业分布"
        )
        
        assert Path(chart_path).exists()
        assert Path(chart_path).suffix == '.png'
        assert Path(chart_path).stat().st_size > 0
    
    def test_plot_sector_distribution_empty(self, viz_manager):
        """测试空行业分布图 / Test empty sector distribution chart"""
        chart_path = viz_manager.plot_sector_distribution(
            sector_weights={},
            title="空行业"
        )
        
        # 应该生成一个空图表 / Should generate an empty chart
        assert Path(chart_path).exists()
    
    def test_plot_multi_model_comparison(self, viz_manager, sample_returns):
        """测试多模型对比图生成 / Test multi-model comparison chart generation"""
        model_returns = {
            "模型A": sample_returns,
            "模型B": sample_returns * 1.1,
            "模型C": sample_returns * 0.9,
        }
        
        chart_path = viz_manager.plot_multi_model_comparison(
            model_returns=model_returns,
            title="测试多模型对比"
        )
        
        assert Path(chart_path).exists()
        assert Path(chart_path).suffix == '.png'
        assert Path(chart_path).stat().st_size > 0
    
    def test_plot_multi_model_comparison_empty(self, viz_manager):
        """测试空模型对比图 / Test empty multi-model comparison"""
        with pytest.raises(VisualizationManagerError):
            viz_manager.plot_multi_model_comparison(
                model_returns={},
                title="空模型"
            )
    
    def test_plot_training_curve(self, viz_manager):
        """测试训练曲线图生成 / Test training curve chart generation"""
        metrics = {
            "训练损失": [1.0, 0.8, 0.6, 0.5, 0.4],
            "验证损失": [1.0, 0.85, 0.7, 0.6, 0.55],
        }
        
        chart_path = viz_manager.plot_training_curve(
            metrics=metrics,
            title="测试训练曲线"
        )
        
        assert Path(chart_path).exists()
        assert Path(chart_path).suffix == '.png'
        assert Path(chart_path).stat().st_size > 0
    
    def test_plot_training_curve_empty(self, viz_manager):
        """测试空训练曲线 / Test empty training curve"""
        with pytest.raises(VisualizationManagerError):
            viz_manager.plot_training_curve(
                metrics={},
                title="空训练曲线"
            )
    
    def test_create_report_with_charts(
        self,
        viz_manager,
        sample_returns,
        sample_portfolio,
        sample_sector_weights
    ):
        """测试完整报告生成 / Test complete report generation"""
        benchmark = pd.Series(
            np.random.normal(0.0008, 0.015, len(sample_returns)),
            index=sample_returns.index
        )
        
        chart_paths = viz_manager.create_report_with_charts(
            returns=sample_returns,
            portfolio=sample_portfolio,
            sector_weights=sample_sector_weights,
            benchmark=benchmark
        )
        
        # 应该生成3个图表 / Should generate 3 charts
        assert len(chart_paths) == 3
        assert 'cumulative_returns' in chart_paths
        assert 'position_distribution' in chart_paths
        assert 'sector_distribution' in chart_paths
        
        # 所有图表文件都应该存在 / All chart files should exist
        for chart_path in chart_paths.values():
            assert Path(chart_path).exists()
            assert Path(chart_path).stat().st_size > 0
    
    def test_create_report_minimal(self, viz_manager, sample_returns):
        """测试最小报告生成 / Test minimal report generation"""
        chart_paths = viz_manager.create_report_with_charts(
            returns=sample_returns
        )
        
        # 至少应该有累计收益图 / Should at least have cumulative returns chart
        assert len(chart_paths) >= 1
        assert 'cumulative_returns' in chart_paths
        assert Path(chart_paths['cumulative_returns']).exists()
    
    def test_custom_save_path(self, viz_manager, sample_returns, tmp_path):
        """测试自定义保存路径 / Test custom save path"""
        custom_path = tmp_path / "custom_chart.png"
        
        chart_path = viz_manager.plot_cumulative_returns(
            returns=sample_returns,
            save_path=str(custom_path)
        )
        
        assert chart_path == str(custom_path)
        assert custom_path.exists()
    
    def test_large_portfolio(self, viz_manager):
        """测试大量持仓 / Test large portfolio"""
        # 创建30个持仓 / Create 30 positions
        large_portfolio = {f"股票{i}": 1.0/30 for i in range(30)}
        
        chart_path = viz_manager.plot_position_distribution(
            portfolio=large_portfolio,
            title="大量持仓"
        )
        
        # 应该能够处理并生成图表 / Should be able to handle and generate chart
        assert Path(chart_path).exists()
    
    def test_negative_returns(self, viz_manager):
        """测试负收益率 / Test negative returns"""
        dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
        negative_returns = pd.Series(np.random.normal(-0.001, 0.02, 100), index=dates)
        
        chart_path = viz_manager.plot_cumulative_returns(
            returns=negative_returns,
            title="负收益测试"
        )
        
        assert Path(chart_path).exists()
    
    def test_single_day_returns(self, viz_manager):
        """测试单日收益率 / Test single day returns"""
        single_return = pd.Series([0.01], index=[datetime.now()])
        
        chart_path = viz_manager.plot_cumulative_returns(
            returns=single_return,
            title="单日收益"
        )
        
        assert Path(chart_path).exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
