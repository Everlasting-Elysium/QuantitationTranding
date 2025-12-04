"""
Unit tests for QlibWrapper
Qlib封装层单元测试
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
from pathlib import Path
from datetime import datetime
import sys

# Mock qlib module before importing QlibWrapper
sys.modules['qlib'] = MagicMock()
sys.modules['qlib.data'] = MagicMock()

from src.infrastructure.qlib_wrapper import (
    QlibWrapper,
    QlibInitializationError,
    QlibDataError
)


class TestQlibWrapper:
    """QlibWrapper测试类"""
    
    def test_initialization(self):
        """测试QlibWrapper初始化"""
        wrapper = QlibWrapper()
        assert not wrapper.is_initialized()
        assert wrapper.get_provider_uri() is None
        assert wrapper.get_region() is None
    
    @patch('src.infrastructure.qlib_wrapper.qlib')
    def test_init_success(self, mock_qlib, tmp_path):
        """测试qlib初始化成功"""
        # 创建临时数据目录
        data_dir = tmp_path / "qlib_data"
        data_dir.mkdir()
        
        wrapper = QlibWrapper()
        wrapper.init(
            provider_uri=str(data_dir),
            region="cn",
            auto_mount=True
        )
        
        # 验证qlib.init被调用
        mock_qlib.init.assert_called_once()
        
        # 验证状态
        assert wrapper.is_initialized()
        assert wrapper.get_provider_uri() == str(data_dir)
        assert wrapper.get_region() == "cn"
    
    @patch('src.infrastructure.qlib_wrapper.qlib')
    def test_init_with_exp_manager_config(self, mock_qlib, tmp_path):
        """测试带实验管理器配置的初始化"""
        data_dir = tmp_path / "qlib_data"
        data_dir.mkdir()
        
        exp_config = {"uri": "./mlruns"}
        
        wrapper = QlibWrapper()
        wrapper.init(
            provider_uri=str(data_dir),
            region="cn",
            exp_manager_config=exp_config
        )
        
        # 验证qlib.init被调用，并包含exp_manager参数
        call_args = mock_qlib.init.call_args
        assert call_args is not None
        assert "exp_manager" in call_args[1]
    
    def test_init_nonexistent_path(self):
        """测试初始化不存在的数据路径"""
        wrapper = QlibWrapper()
        
        with pytest.raises(QlibInitializationError) as exc_info:
            wrapper.init(
                provider_uri="/nonexistent/path",
                region="cn"
            )
        
        assert "数据路径不存在" in str(exc_info.value)
    
    @patch('src.infrastructure.qlib_wrapper.qlib')
    def test_init_qlib_exception(self, mock_qlib, tmp_path):
        """测试qlib初始化异常"""
        data_dir = tmp_path / "qlib_data"
        data_dir.mkdir()
        
        # 模拟qlib.init抛出异常
        mock_qlib.init.side_effect = Exception("qlib error")
        
        wrapper = QlibWrapper()
        
        with pytest.raises(QlibInitializationError) as exc_info:
            wrapper.init(provider_uri=str(data_dir), region="cn")
        
        assert "qlib初始化失败" in str(exc_info.value)
    
    def test_get_data_success(self):
        """测试获取数据成功"""
        # 创建模拟数据
        mock_data = pd.DataFrame({
            'close': [100, 101, 102],
            'volume': [1000, 1100, 1200]
        })
        
        # 模拟D模块 - 需要模拟整个D对象
        mock_d = MagicMock()
        mock_d.features.return_value = mock_data
        
        with patch.dict('sys.modules', {'qlib.data': MagicMock(D=mock_d)}):
            wrapper = QlibWrapper()
            wrapper._initialized = True
            
            data = wrapper.get_data(
                instruments="csi300",
                fields=["$close", "$volume"],
                start_time="2023-01-01",
                end_time="2023-12-31"
            )
            
            # 验证返回的数据
            assert isinstance(data, pd.DataFrame)
            assert len(data) == 3
            mock_d.features.assert_called_once()
    
    def test_get_data_not_initialized(self):
        """测试未初始化时获取数据"""
        wrapper = QlibWrapper()
        
        with pytest.raises(QlibDataError) as exc_info:
            wrapper.get_data(
                instruments="csi300",
                fields=["$close"],
                start_time="2023-01-01",
                end_time="2023-12-31"
            )
        
        assert "qlib未初始化" in str(exc_info.value)
    
    def test_get_data_exception(self):
        """测试获取数据异常"""
        # 模拟D.features抛出异常
        mock_d = MagicMock()
        mock_d.features.side_effect = Exception("data error")
        
        with patch.dict('sys.modules', {'qlib.data': MagicMock(D=mock_d)}):
            wrapper = QlibWrapper()
            wrapper._initialized = True
            
            with pytest.raises(QlibDataError) as exc_info:
                wrapper.get_data(
                    instruments="csi300",
                    fields=["$close"],
                    start_time="2023-01-01",
                    end_time="2023-12-31"
                )
            
            assert "获取数据失败" in str(exc_info.value)
    
    def test_get_instruments_success(self):
        """测试获取股票列表成功"""
        mock_instruments = ["000001.SZ", "000002.SZ", "600000.SH"]
        
        mock_d = MagicMock()
        mock_d.instruments.return_value = mock_instruments
        
        with patch.dict('sys.modules', {'qlib.data': MagicMock(D=mock_d)}):
            wrapper = QlibWrapper()
            wrapper._initialized = True
            
            instruments = wrapper.get_instruments(market="csi300")
            
            assert instruments == mock_instruments
            mock_d.instruments.assert_called_once()
    
    def test_get_instruments_not_initialized(self):
        """测试未初始化时获取股票列表"""
        wrapper = QlibWrapper()
        
        with pytest.raises(QlibDataError) as exc_info:
            wrapper.get_instruments(market="csi300")
        
        assert "qlib未初始化" in str(exc_info.value)
    
    def test_get_calendar_success(self):
        """测试获取交易日历成功"""
        mock_calendar = [
            pd.Timestamp("2023-01-03"),
            pd.Timestamp("2023-01-04"),
            pd.Timestamp("2023-01-05")
        ]
        
        mock_d = MagicMock()
        mock_d.calendar.return_value = mock_calendar
        
        with patch.dict('sys.modules', {'qlib.data': MagicMock(D=mock_d)}):
            wrapper = QlibWrapper()
            wrapper._initialized = True
            
            calendar = wrapper.get_calendar(
                start_time="2023-01-01",
                end_time="2023-01-31"
            )
            
            assert calendar == mock_calendar
            assert len(calendar) == 3
    
    def test_get_calendar_not_initialized(self):
        """测试未初始化时获取交易日历"""
        wrapper = QlibWrapper()
        
        with pytest.raises(QlibDataError) as exc_info:
            wrapper.get_calendar()
        
        assert "qlib未初始化" in str(exc_info.value)
    
    def test_validate_data_success(self):
        """测试数据验证成功"""
        # 模拟交易日历
        mock_calendar = [
            pd.Timestamp("2023-01-03"),
            pd.Timestamp("2023-12-29")
        ]
        
        # 模拟数据
        mock_data = pd.DataFrame({
            'close': [100, 101]
        })
        
        mock_d = MagicMock()
        mock_d.calendar.return_value = mock_calendar
        mock_d.features.return_value = mock_data
        
        with patch.dict('sys.modules', {'qlib.data': MagicMock(D=mock_d)}):
            wrapper = QlibWrapper()
            wrapper._initialized = True
            
            is_valid, message, time_range = wrapper.validate_data(
                instruments="csi300"
            )
            
            assert is_valid
            assert "数据验证成功" in message
            assert time_range is not None
            assert time_range[0] == "2023-01-03"
            assert time_range[1] == "2023-12-29"
    
    def test_validate_data_not_initialized(self):
        """测试未初始化时验证数据"""
        wrapper = QlibWrapper()
        
        is_valid, message, time_range = wrapper.validate_data()
        
        assert not is_valid
        assert "qlib未初始化" in message
        assert time_range is None
    
    def test_validate_data_empty_calendar(self):
        """测试验证数据 - 空交易日历"""
        mock_d = MagicMock()
        mock_d.calendar.return_value = []
        
        with patch.dict('sys.modules', {'qlib.data': MagicMock(D=mock_d)}):
            wrapper = QlibWrapper()
            wrapper._initialized = True
            
            is_valid, message, time_range = wrapper.validate_data()
            
            assert not is_valid
            assert "未找到交易日数据" in message
    
    def test_validate_data_empty_data(self):
        """测试验证数据 - 空数据"""
        mock_calendar = [
            pd.Timestamp("2023-01-03"),
            pd.Timestamp("2023-12-29")
        ]
        
        mock_d = MagicMock()
        mock_d.calendar.return_value = mock_calendar
        mock_d.features.return_value = pd.DataFrame()  # 空DataFrame
        
        with patch.dict('sys.modules', {'qlib.data': MagicMock(D=mock_d)}):
            wrapper = QlibWrapper()
            wrapper._initialized = True
            
            is_valid, message, time_range = wrapper.validate_data()
            
            assert not is_valid
            assert "数据为空" in message
            assert time_range is not None  # 时间范围仍然返回
    
    def test_get_data_info_success(self):
        """测试获取数据信息成功"""
        mock_calendar = [
            pd.Timestamp("2020-01-02"),
            pd.Timestamp("2023-12-29")
        ]
        
        mock_d = MagicMock()
        mock_d.calendar.return_value = mock_calendar
        
        with patch.dict('sys.modules', {'qlib.data': MagicMock(D=mock_d)}):
            wrapper = QlibWrapper()
            wrapper._initialized = True
            wrapper._provider_uri = "/path/to/data"
            wrapper._region = "cn"
            
            info = wrapper.get_data_info()
            
            assert info["provider_uri"] == "/path/to/data"
            assert info["region"] == "cn"
            assert info["data_start"] == "2020-01-02"
            assert info["data_end"] == "2023-12-29"
            assert info["trading_days"] == 2
            assert info["initialized"] is True
    
    def test_get_data_info_not_initialized(self):
        """测试未初始化时获取数据信息"""
        wrapper = QlibWrapper()
        
        with pytest.raises(QlibDataError) as exc_info:
            wrapper.get_data_info()
        
        assert "qlib未初始化" in str(exc_info.value)
    
    def test_get_data_info_no_calendar(self):
        """测试获取数据信息 - 无交易日历"""
        mock_d = MagicMock()
        mock_d.calendar.return_value = []
        
        with patch.dict('sys.modules', {'qlib.data': MagicMock(D=mock_d)}):
            wrapper = QlibWrapper()
            wrapper._initialized = True
            
            with pytest.raises(QlibDataError) as exc_info:
                wrapper.get_data_info()
            
            assert "无法获取交易日历" in str(exc_info.value)
    
    @patch('src.infrastructure.qlib_wrapper.qlib')
    def test_init_with_tilde_path(self, mock_qlib, tmp_path):
        """测试使用~路径初始化"""
        # 创建临时目录模拟用户主目录下的数据
        data_dir = tmp_path / "qlib_data"
        data_dir.mkdir()
        
        # 使用patch模拟Path.expanduser
        with patch('pathlib.Path.expanduser', return_value=data_dir):
            wrapper = QlibWrapper()
            wrapper.init(
                provider_uri="~/qlib_data",
                region="cn"
            )
            
            assert wrapper.is_initialized()
    
    def test_get_data_with_empty_result(self):
        """测试获取数据返回空结果"""
        mock_d = MagicMock()
        mock_d.features.return_value = pd.DataFrame()  # 空DataFrame
        
        with patch.dict('sys.modules', {'qlib.data': MagicMock(D=mock_d)}):
            wrapper = QlibWrapper()
            wrapper._initialized = True
            
            data = wrapper.get_data(
                instruments="invalid",
                fields=["$close"],
                start_time="2023-01-01",
                end_time="2023-12-31"
            )
            
            # 应该返回空DataFrame，不抛出异常
            assert isinstance(data, pd.DataFrame)
            assert data.empty
    
    def test_get_data_with_none_result(self):
        """测试获取数据返回None"""
        mock_d = MagicMock()
        mock_d.features.return_value = None
        
        with patch.dict('sys.modules', {'qlib.data': MagicMock(D=mock_d)}):
            wrapper = QlibWrapper()
            wrapper._initialized = True
            
            data = wrapper.get_data(
                instruments="invalid",
                fields=["$close"],
                start_time="2023-01-01",
                end_time="2023-12-31"
            )
            
            # 应该返回None，不抛出异常
            assert data is None
