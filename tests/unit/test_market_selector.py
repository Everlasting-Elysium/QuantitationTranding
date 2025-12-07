"""
Unit tests for MarketSelector
市场选择器的单元测试
"""

import pytest
import tempfile
import yaml
from pathlib import Path

from src.application.market_selector import MarketSelector
from src.models.market_models import Market, AssetType, MarketConfig, MarketInfo


class TestMarketSelector:
    """Test suite for MarketSelector / MarketSelector的测试套件"""
    
    @pytest.fixture
    def temp_config_file(self):
        """Create a temporary market config file / 创建临时市场配置文件"""
        config_data = {
            'markets': {
                'TEST': {
                    'code': 'TEST',
                    'name': '测试市场',
                    'region': 'test',
                    'timezone': 'UTC',
                    'trading_hours': {
                        'start': '09:00',
                        'end': '17:00'
                    },
                    'description': '测试市场描述',
                    'asset_types': {
                        'stock': {
                            'code': 'stock',
                            'name': '股票',
                            'description': '测试股票',
                            'instruments_pools': [
                                {'name': 'test_pool', 'description': '测试池'}
                            ],
                            'data_source': 'qlib_test'
                        }
                    }
                }
            },
            'default_market': 'TEST',
            'default_asset_type': 'stock'
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f, allow_unicode=True)
            temp_path = f.name
        
        yield temp_path
        
        # Cleanup
        Path(temp_path).unlink()
    
    def test_initialization(self, temp_config_file):
        """Test MarketSelector initialization / 测试MarketSelector初始化"""
        selector = MarketSelector(config_path=temp_config_file)
        
        assert selector is not None
        assert len(selector.markets) > 0
        assert 'TEST' in selector.markets
    
    def test_get_available_markets(self, temp_config_file):
        """Test getting available markets / 测试获取可用市场"""
        selector = MarketSelector(config_path=temp_config_file)
        markets = selector.get_available_markets()
        
        assert isinstance(markets, list)
        assert len(markets) > 0
        assert all(isinstance(m, Market) for m in markets)
        
        # Check TEST market exists
        test_market = next((m for m in markets if m.code == 'TEST'), None)
        assert test_market is not None
        assert test_market.name == '测试市场'
        assert test_market.region == 'test'
    
    def test_get_asset_types(self, temp_config_file):
        """Test getting asset types for a market / 测试获取市场的资产类型"""
        selector = MarketSelector(config_path=temp_config_file)
        asset_types = selector.get_asset_types('TEST')
        
        assert isinstance(asset_types, list)
        assert len(asset_types) > 0
        assert all(isinstance(at, AssetType) for at in asset_types)
        
        # Check stock asset type exists
        stock_type = next((at for at in asset_types if at.code == 'stock'), None)
        assert stock_type is not None
        assert stock_type.name == '股票'
    
    def test_get_asset_types_invalid_market(self, temp_config_file):
        """Test getting asset types with invalid market / 测试使用无效市场获取资产类型"""
        selector = MarketSelector(config_path=temp_config_file)
        
        with pytest.raises(ValueError) as exc_info:
            selector.get_asset_types('INVALID')
        
        assert 'Invalid market code' in str(exc_info.value) or '无效的市场代码' in str(exc_info.value)
    
    def test_select_market_and_type(self, temp_config_file):
        """Test creating market configuration / 测试创建市场配置"""
        selector = MarketSelector(config_path=temp_config_file)
        config = selector.select_market_and_type('TEST', 'stock')
        
        assert isinstance(config, MarketConfig)
        assert config.market.code == 'TEST'
        assert config.asset_type.code == 'stock'
        assert config.data_source == 'qlib_test'
        assert config.instruments_pool == 'test_pool'
    
    def test_select_market_and_type_invalid_market(self, temp_config_file):
        """Test creating config with invalid market / 测试使用无效市场创建配置"""
        selector = MarketSelector(config_path=temp_config_file)
        
        with pytest.raises(ValueError) as exc_info:
            selector.select_market_and_type('INVALID', 'stock')
        
        assert 'Invalid market code' in str(exc_info.value) or '无效的市场代码' in str(exc_info.value)
    
    def test_select_market_and_type_invalid_asset_type(self, temp_config_file):
        """Test creating config with invalid asset type / 测试使用无效资产类型创建配置"""
        selector = MarketSelector(config_path=temp_config_file)
        
        with pytest.raises(ValueError) as exc_info:
            selector.select_market_and_type('TEST', 'invalid')
        
        assert 'Invalid asset type' in str(exc_info.value) or '资产类型' in str(exc_info.value)
    
    def test_get_market_info(self, temp_config_file):
        """Test getting market information / 测试获取市场信息"""
        selector = MarketSelector(config_path=temp_config_file)
        market_info = selector.get_market_info('TEST')
        
        assert isinstance(market_info, MarketInfo)
        assert market_info.market.code == 'TEST'
        assert len(market_info.available_asset_types) > 0
        assert market_info.data_available is True
        assert market_info.description == '测试市场描述'
    
    def test_get_market_info_invalid_market(self, temp_config_file):
        """Test getting info for invalid market / 测试获取无效市场的信息"""
        selector = MarketSelector(config_path=temp_config_file)
        
        with pytest.raises(ValueError) as exc_info:
            selector.get_market_info('INVALID')
        
        assert 'Invalid market code' in str(exc_info.value) or '无效的市场代码' in str(exc_info.value)
    
    def test_get_instruments_pools(self, temp_config_file):
        """Test getting instruments pools / 测试获取工具池"""
        selector = MarketSelector(config_path=temp_config_file)
        pools = selector.get_instruments_pools('TEST', 'stock')
        
        assert isinstance(pools, list)
        assert len(pools) > 0
        assert pools[0]['name'] == 'test_pool'
        assert pools[0]['description'] == '测试池'
    
    def test_get_instruments_pools_invalid_market(self, temp_config_file):
        """Test getting pools with invalid market / 测试使用无效市场获取工具池"""
        selector = MarketSelector(config_path=temp_config_file)
        
        with pytest.raises(ValueError) as exc_info:
            selector.get_instruments_pools('INVALID', 'stock')
        
        assert 'Invalid market code' in str(exc_info.value) or '无效的市场代码' in str(exc_info.value)
    
    def test_get_default_config(self, temp_config_file):
        """Test getting default configuration / 测试获取默认配置"""
        selector = MarketSelector(config_path=temp_config_file)
        config = selector.get_default_config()
        
        assert isinstance(config, MarketConfig)
        assert config.market.code == 'TEST'
        assert config.asset_type.code == 'stock'
    
    def test_config_file_not_found(self):
        """Test initialization with non-existent config file / 测试使用不存在的配置文件初始化"""
        with pytest.raises(FileNotFoundError) as exc_info:
            MarketSelector(config_path='/nonexistent/path/markets.yaml')
        
        assert 'not found' in str(exc_info.value) or '未找到' in str(exc_info.value)
    
    def test_real_config_file(self):
        """Test with real config file / 测试使用真实配置文件"""
        # This test uses the actual markets.yaml file
        # 此测试使用实际的markets.yaml文件
        selector = MarketSelector()
        
        # Should have CN, US, HK markets
        # 应该有CN、US、HK市场
        markets = selector.get_available_markets()
        market_codes = [m.code for m in markets]
        
        assert 'CN' in market_codes
        assert 'US' in market_codes
        assert 'HK' in market_codes
        
        # CN should have stock, fund, etf
        # CN应该有股票、基金、ETF
        cn_asset_types = selector.get_asset_types('CN')
        asset_codes = [at.code for at in cn_asset_types]
        
        assert 'stock' in asset_codes
        assert 'fund' in asset_codes
        assert 'etf' in asset_codes
        
        # Test creating CN stock config
        # 测试创建CN股票配置
        config = selector.select_market_and_type('CN', 'stock')
        assert config.market.code == 'CN'
        assert config.asset_type.code == 'stock'
        assert config.instruments_pool == 'csi300'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
