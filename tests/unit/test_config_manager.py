"""
Unit tests for ConfigManager
配置管理器单元测试
"""

import pytest
import tempfile
import yaml
from pathlib import Path
from src.core.config_manager import (
    ConfigManager,
    Config,
    QlibConfig,
    MLflowConfig,
    DataConfig,
    TrainingConfig,
    BacktestConfig,
    BacktestStrategyConfig,
    BacktestExecutorConfig,
    SignalConfig,
    RiskLimits,
    ModelRegistryConfig,
    LoggingConfig,
    VisualizationConfig,
    CLIConfig
)


class TestConfigManager:
    """ConfigManager测试类"""
    
    def test_get_default_config(self):
        """测试获取默认配置"""
        manager = ConfigManager()
        config = manager.get_default_config()
        
        assert isinstance(config, Config)
        assert config.qlib.region == "cn"
        assert config.mlflow.experiment_name == "qlib_trading"
        assert config.data.instruments == "csi300"
        assert config.logging.log_level == "INFO"
    
    def test_save_and_load_config(self, tmp_path):
        """测试保存和加载配置"""
        manager = ConfigManager()
        config = manager.get_default_config()
        
        # 保存配置
        config_path = tmp_path / "test_config.yaml"
        manager.save_config(config, str(config_path))
        
        # 验证文件存在
        assert config_path.exists()
        
        # 加载配置
        loaded_config = manager.load_config(str(config_path))
        
        # 验证配置内容
        assert loaded_config.qlib.region == config.qlib.region
        assert loaded_config.mlflow.experiment_name == config.mlflow.experiment_name
        assert loaded_config.data.instruments == config.data.instruments
    
    def test_load_nonexistent_config(self):
        """测试加载不存在的配置文件"""
        from src.utils.error_handler import ConfigurationError
        
        manager = ConfigManager()
        
        with pytest.raises(ConfigurationError) as exc_info:
            manager.load_config("/nonexistent/path/config.yaml")
        
        assert "CFG0001" in str(exc_info.value) or "不存在" in str(exc_info.value)
    
    def test_load_invalid_yaml(self, tmp_path):
        """测试加载无效的YAML文件"""
        from src.utils.error_handler import ConfigurationError
        
        manager = ConfigManager()
        
        # 创建无效的YAML文件
        config_path = tmp_path / "invalid.yaml"
        with open(config_path, 'w') as f:
            f.write("invalid: yaml: content: [")
        
        with pytest.raises(ConfigurationError) as exc_info:
            manager.load_config(str(config_path))
        
        assert "CFG0002" in str(exc_info.value) or "格式错误" in str(exc_info.value)
    
    def test_validate_config_success(self, tmp_path):
        """测试配置验证成功"""
        manager = ConfigManager()
        config = manager.get_default_config()
        
        # 创建临时数据目录
        data_dir = tmp_path / "qlib_data"
        data_dir.mkdir()
        config.qlib.provider_uri = str(data_dir)
        
        errors = manager.validate_config(config)
        assert len(errors) == 0

    def test_validate_config_missing_data_path(self):
        """测试配置验证 - 缺失数据路径"""
        manager = ConfigManager()
        config = manager.get_default_config()
        config.qlib.provider_uri = "/nonexistent/path"
        
        errors = manager.validate_config(config)
        assert len(errors) > 0
        assert any("数据路径不存在" in error for error in errors)
    
    def test_validate_config_invalid_log_level(self, tmp_path):
        """测试配置验证 - 无效的日志级别"""
        manager = ConfigManager()
        config = manager.get_default_config()
        
        # 创建临时数据目录
        data_dir = tmp_path / "qlib_data"
        data_dir.mkdir()
        config.qlib.provider_uri = str(data_dir)
        
        config.logging.log_level = "INVALID"
        
        errors = manager.validate_config(config)
        assert len(errors) > 0
        assert any("log_level" in error for error in errors)
    
    def test_validate_config_invalid_risk_limits(self, tmp_path):
        """测试配置验证 - 无效的风险限制"""
        manager = ConfigManager()
        config = manager.get_default_config()
        
        # 创建临时数据目录
        data_dir = tmp_path / "qlib_data"
        data_dir.mkdir()
        config.qlib.provider_uri = str(data_dir)
        
        # 设置无效的风险限制
        config.signal.risk_limits.max_position_per_stock = 1.5
        
        errors = manager.validate_config(config)
        assert len(errors) > 0
        assert any("max_position_per_stock" in error for error in errors)
    
    def test_validate_config_empty_required_fields(self, tmp_path):
        """测试配置验证 - 必填字段为空"""
        manager = ConfigManager()
        config = manager.get_default_config()
        
        # 创建临时数据目录
        data_dir = tmp_path / "qlib_data"
        data_dir.mkdir()
        config.qlib.provider_uri = str(data_dir)
        
        # 清空必填字段
        config.data.instruments = ""
        
        errors = manager.validate_config(config)
        assert len(errors) > 0
        assert any("instruments" in error for error in errors)
    
    def test_config_property(self):
        """测试config属性"""
        manager = ConfigManager()
        
        # 初始状态应该为None
        assert manager.config is None
        
        # 加载配置后应该有值
        config = manager.get_default_config()
        manager._config = config
        assert manager.config is not None
        assert isinstance(manager.config, Config)
