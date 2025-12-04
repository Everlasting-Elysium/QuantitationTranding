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
        