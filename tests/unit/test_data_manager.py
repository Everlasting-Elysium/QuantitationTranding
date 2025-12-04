"""
Unit tests for DataManager
"""
import pytest
import pandas as pd
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

from src.core.data_manager import (
    DataManager,
    DataManagerError,
    MissingValueStrategy,
    ValidationResult,
    DataInfo
)
from src.infrastructure.qlib_wrapper import QlibWrapper, QlibDataError


class TestDataManager:
    """Test suite for DataManager class"""
    
    def test_initialization(self):
        """Test DataManager initialization"""
        manager = DataManager()
        assert manager is not None
        assert not manager.is_initialized()
    
    def test_initialize_success(self, temp_dir):
        """Test successful initialization"""
        # Create mock qlib wrapper
        mock_wrapper = Mock(spec=QlibWrapper)
        mock_wrapper.init = Mock()
        
        manager = DataManager(qlib_wrapper=mock_wrapper)
        
        # Initialize
        data_path = str(temp_dir)
        manager.initialize(data_path=data_path, region="cn")
        
        # Verify
        assert manager.is_initialized()
        mock_wrapper.init.assert_called_once_with(
            provider_uri=data_path,
            region="cn",
            auto_mount=True
        )
    
    def test_initialize_failure(self):
        """Test initialization failure"""
        # Create mock qlib wrapper that raises exception
        mock_wrapper = Mock(spec=QlibWrapper)
        mock_wrapper.init = Mock(side_effect=Exception("Init failed"))
        
        manager = DataManager(qlib_wrapper=mock_wrapper)
        
        # Should raise DataManagerError
        with pytest.raises(DataManagerError) as exc_info:
            manager.initialize(data_path="/nonexistent", region="cn")
        
        assert "数据管理器初始化失败" in str(exc_info.value)
        assert not manager.is_initialized()
    
    def test_validate_data_not_initialized(self):
        """Test validation when not initialized"""
        manager = DataManager()
        
        result = manager.validate_data()
        
        assert not result.is_valid
        assert "未初始化" in result.message
        assert len(result.issues) > 0
    
    def test_validate_data_success(self):
        """Test successful data validation"""
        # Create mock qlib wrapper
        mock_wrapper = Mock(spec=QlibWrapper)
        mock_wrapper.validate_data = Mock(return_value=(
            True,
            "数据验证成功",
            ("2020-01-01", "2023-12-31")
        ))
        mock_wrapper.get_calendar = Mock(return_value=[
            pd.Timestamp("2020-01-01"),
            pd.Timestamp("2020-01-02"),
            pd.Timestamp("2020-01-03")
        ])
        mock_wrapper.get_data = Mock(return_value=pd.DataFrame({
            "$close": [100, 101, 102],
            "$volume": [1000, 1100, 1200]
        }))
        
        manager = DataManager(qlib_wrapper=mock_wrapper)
        manager._initialized = True
        
        result = manager.validate_data(
            start_date="2020-01-01",
            end_date="2023-12-31"
        )
        
        assert result.is_valid
        assert result.data_start == "2020-01-01"
        assert result.data_end == "2023-12-31"
        assert result.trading_days == 3
    
    def test_validate_data_no_trading_days(self):
        """Test validation with no trading days"""
        # Create mock qlib wrapper
        mock_wrapper = Mock(spec=QlibWrapper)
        mock_wrapper.validate_data = Mock(return_value=(
            True,
            "数据验证成功",
            ("2020-01-01", "2023-12-31")
        ))
        mock_wrapper.get_calendar = Mock(return_value=[])
        
        manager = DataManager(qlib_wrapper=mock_wrapper)
        manager._initialized = True
        
        result = manager.validate_data()
        
        assert not result.is_valid
        assert "未找到交易日数据" in result.message
        assert result.trading_days == 0
    
    def test_handle_missing_values_forward_fill(self):
        """Test forward fill strategy for missing values"""
        manager = DataManager()
        
        # Create data with missing values
        data = pd.DataFrame({
            "col1": [1.0, None, 3.0, None, 5.0],
            "col2": [10.0, 20.0, None, 40.0, 50.0]
        })
        
        result = manager.handle_missing_values(
            data,
            strategy=MissingValueStrategy.FORWARD_FILL
        )
        
        # Check that forward fill was applied
        assert result["col1"].iloc[1] == 1.0  # Filled from previous
        assert result["col1"].iloc[3] == 3.0  # Filled from previous
        assert result["col2"].iloc[2] == 20.0  # Filled from previous
    
    def test_handle_missing_values_backward_fill(self):
        """Test backward fill strategy for missing values"""
        manager = DataManager()
        
        # Create data with missing values
        data = pd.DataFrame({
            "col1": [1.0, None, 3.0, None, 5.0],
            "col2": [10.0, 20.0, None, 40.0, 50.0]
        })
        
        result = manager.handle_missing_values(
            data,
            strategy=MissingValueStrategy.BACKWARD_FILL
        )
        
        # Check that backward fill was applied
        assert result["col1"].iloc[1] == 3.0  # Filled from next
        assert result["col1"].iloc[3] == 5.0  # Filled from next
        assert result["col2"].iloc[2] == 40.0  # Filled from next
    
    def test_handle_missing_values_zero(self):
        """Test zero fill strategy for missing values"""
        manager = DataManager()
        
        # Create data with missing values
        data = pd.DataFrame({
            "col1": [1.0, None, 3.0],
            "col2": [10.0, None, 30.0]
        })
        
        result = manager.handle_missing_values(
            data,
            strategy=MissingValueStrategy.ZERO
        )
        
        # Check that zeros were filled
        assert result["col1"].iloc[1] == 0.0
        assert result["col2"].iloc[1] == 0.0
    
    def test_handle_missing_values_drop(self):
        """Test drop strategy for missing values"""
        manager = DataManager()
        
        # Create data with missing values
        data = pd.DataFrame({
            "col1": [1.0, None, 3.0],
            "col2": [10.0, 20.0, 30.0]
        })
        
        result = manager.handle_missing_values(
            data,
            strategy=MissingValueStrategy.DROP
        )
        
        # Check that rows with missing values were dropped
        assert len(result) == 2
        assert result["col1"].iloc[0] == 1.0
        assert result["col1"].iloc[1] == 3.0
    
    def test_handle_missing_values_empty_data(self):
        """Test handling missing values with empty data"""
        manager = DataManager()
        
        data = pd.DataFrame()
        
        result = manager.handle_missing_values(data)
        
        assert result.empty
    
    def test_handle_missing_values_no_missing(self):
        """Test handling data with no missing values"""
        manager = DataManager()
        
        data = pd.DataFrame({
            "col1": [1.0, 2.0, 3.0],
            "col2": [10.0, 20.0, 30.0]
        })
        
        result = manager.handle_missing_values(data)
        
        # Data should be unchanged
        assert result.equals(data)
    
    def test_get_data_info_not_initialized(self):
        """Test getting data info when not initialized"""
        manager = DataManager()
        
        with pytest.raises(DataManagerError) as exc_info:
            manager.get_data_info()
        
        assert "未初始化" in str(exc_info.value)
    
    def test_get_data_info_success(self):
        """Test successful data info retrieval"""
        # Create mock qlib wrapper
        mock_wrapper = Mock(spec=QlibWrapper)
        mock_wrapper.get_data_info = Mock(return_value={
            "provider_uri": "/path/to/data",
            "region": "cn",
            "data_start": "2020-01-01",
            "data_end": "2023-12-31",
            "trading_days": 1000
        })
        mock_wrapper.get_instruments = Mock(return_value=[
            "000001.SZ", "000002.SZ", "600000.SH"
        ])
        
        manager = DataManager(qlib_wrapper=mock_wrapper)
        manager._initialized = True
        
        info = manager.get_data_info()
        
        assert isinstance(info, DataInfo)
        assert info.provider_uri == "/path/to/data"
        assert info.region == "cn"
        assert info.data_start == "2020-01-01"
        assert info.data_end == "2023-12-31"
        assert info.trading_days == 1000
        assert info.instruments_count == 3
    
    def test_check_data_coverage_not_initialized(self):
        """Test coverage check when not initialized"""
        manager = DataManager()
        
        is_covered, message = manager.check_data_coverage(
            required_start="2020-01-01",
            required_end="2023-12-31"
        )
        
        assert not is_covered
        assert "未初始化" in message
    
    def test_check_data_coverage_sufficient(self):
        """Test coverage check with sufficient data"""
        # Create mock qlib wrapper
        mock_wrapper = Mock(spec=QlibWrapper)
        mock_wrapper.get_data_info = Mock(return_value={
            "provider_uri": "/path/to/data",
            "region": "cn",
            "data_start": "2019-01-01",
            "data_end": "2024-12-31",
            "trading_days": 1500
        })
        mock_wrapper.get_instruments = Mock(return_value=["000001.SZ"])
        
        manager = DataManager(qlib_wrapper=mock_wrapper)
        manager._initialized = True
        
        is_covered, message = manager.check_data_coverage(
            required_start="2020-01-01",
            required_end="2023-12-31"
        )
        
        assert is_covered
        assert "覆盖检查通过" in message
    
    def test_check_data_coverage_insufficient(self):
        """Test coverage check with insufficient data"""
        # Create mock qlib wrapper
        mock_wrapper = Mock(spec=QlibWrapper)
        mock_wrapper.get_data_info = Mock(return_value={
            "provider_uri": "/path/to/data",
            "region": "cn",
            "data_start": "2021-01-01",
            "data_end": "2022-12-31",
            "trading_days": 500
        })
        mock_wrapper.get_instruments = Mock(return_value=["000001.SZ"])
        
        manager = DataManager(qlib_wrapper=mock_wrapper)
        manager._initialized = True
        
        is_covered, message = manager.check_data_coverage(
            required_start="2020-01-01",
            required_end="2023-12-31"
        )
        
        assert not is_covered
        assert "覆盖不足" in message
    
    def test_qlib_wrapper_property(self):
        """Test qlib_wrapper property"""
        mock_wrapper = Mock(spec=QlibWrapper)
        manager = DataManager(qlib_wrapper=mock_wrapper)
        
        assert manager.qlib_wrapper is mock_wrapper
