"""
Market Selector for the qlib trading system.
市场选择器

This module provides functionality to select markets and asset types,
and manage market configurations.
本模块提供选择市场和资产类型以及管理市场配置的功能。
"""

import os
import yaml
from typing import List, Dict, Optional
from pathlib import Path

from ..models.market_models import Market, AssetType, MarketConfig, MarketInfo
from ..infrastructure.logger_system import LoggerSystem


class MarketSelector:
    """
    Market selector for managing market and asset type selection.
    用于管理市场和资产类型选择的市场选择器
    
    This class handles:
    - Loading market configurations from YAML files
    - Providing available markets and asset types
    - Creating market configurations
    - Validating market selections
    
    本类处理：
    - 从YAML文件加载市场配置
    - 提供可用的市场和资产类型
    - 创建市场配置
    - 验证市场选择
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the market selector.
        初始化市场选择器
        
        Args:
            config_path: Path to markets configuration file
                        市场配置文件的路径
        """
        logger_system = LoggerSystem()
        self.logger = logger_system.get_logger(__name__)
        
        # Determine config path
        # 确定配置路径
        if config_path is None:
            # Default to config/markets.yaml in project root
            # 默认为项目根目录中的config/markets.yaml
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / "config" / "markets.yaml"
        
        self.config_path = Path(config_path)
        self.markets_config: Dict = {}
        self.markets: Dict[str, Market] = {}
        self.asset_types: Dict[str, Dict[str, AssetType]] = {}
        
        # Load configuration
        # 加载配置
        self._load_config()
        
        self.logger.info(f"MarketSelector initialized with {len(self.markets)} markets")
        self.logger.info(f"市场选择器已初始化，包含 {len(self.markets)} 个市场")
    
    def _load_config(self) -> None:
        """
        Load market configuration from YAML file.
        从YAML文件加载市场配置
        
        Raises:
            FileNotFoundError: If config file doesn't exist
                              如果配置文件不存在
            ValueError: If config format is invalid
                       如果配置格式无效
        """
        if not self.config_path.exists():
            error_msg = f"Market config file not found: {self.config_path}"
            error_msg_cn = f"市场配置文件未找到: {self.config_path}"
            self.logger.error(f"{error_msg} / {error_msg_cn}")
            raise FileNotFoundError(f"{error_msg} / {error_msg_cn}")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.markets_config = yaml.safe_load(f)
            
            # Parse markets
            # 解析市场
            if 'markets' not in self.markets_config:
                raise ValueError("Config must contain 'markets' key / 配置必须包含'markets'键")
            
            for market_code, market_data in self.markets_config['markets'].items():
                # Create Market object
                # 创建Market对象
                market = Market(
                    code=market_data['code'],
                    name=market_data['name'],
                    region=market_data['region'],
                    timezone=market_data['timezone'],
                    trading_hours=market_data.get('trading_hours', {})
                )
                self.markets[market_code] = market
                
                # Parse asset types for this market
                # 解析此市场的资产类型
                self.asset_types[market_code] = {}
                if 'asset_types' in market_data:
                    for asset_code, asset_data in market_data['asset_types'].items():
                        asset_type = AssetType(
                            code=asset_data['code'],
                            name=asset_data['name'],
                            description=asset_data['description']
                        )
                        self.asset_types[market_code][asset_code] = asset_type
            
            self.logger.info(f"Loaded {len(self.markets)} markets from config")
            self.logger.info(f"从配置加载了 {len(self.markets)} 个市场")
            
        except yaml.YAMLError as e:
            error_msg = f"Error parsing market config: {e}"
            error_msg_cn = f"解析市场配置时出错: {e}"
            self.logger.error(f"{error_msg} / {error_msg_cn}")
            raise ValueError(f"{error_msg} / {error_msg_cn}")
        except Exception as e:
            error_msg = f"Error loading market config: {e}"
            error_msg_cn = f"加载市场配置时出错: {e}"
            self.logger.error(f"{error_msg} / {error_msg_cn}")
            raise
    
    def get_available_markets(self) -> List[Market]:
        """
        Get list of all available markets.
        获取所有可用市场的列表
        
        Returns:
            List of Market objects
            Market对象列表
        """
        markets = list(self.markets.values())
        self.logger.debug(f"Retrieved {len(markets)} available markets")
        self.logger.debug(f"检索到 {len(markets)} 个可用市场")
        return markets
    
    def get_asset_types(self, market: str) -> List[AssetType]:
        """
        Get available asset types for a specific market.
        获取特定市场的可用资产类型
        
        Args:
            market: Market code (e.g., "CN", "US")
                   市场代码（例如："CN"、"US"）
        
        Returns:
            List of AssetType objects
            AssetType对象列表
        
        Raises:
            ValueError: If market code is invalid
                       如果市场代码无效
        """
        if market not in self.asset_types:
            error_msg = f"Invalid market code: {market}"
            error_msg_cn = f"无效的市场代码: {market}"
            self.logger.error(f"{error_msg} / {error_msg_cn}")
            raise ValueError(f"{error_msg} / {error_msg_cn}")
        
        asset_types = list(self.asset_types[market].values())
        self.logger.debug(f"Retrieved {len(asset_types)} asset types for market {market}")
        self.logger.debug(f"为市场 {market} 检索到 {len(asset_types)} 个资产类型")
        return asset_types
    
    def select_market_and_type(self, market_code: str, asset_type_code: str) -> MarketConfig:
        """
        Create a market configuration for the selected market and asset type.
        为选定的市场和资产类型创建市场配置
        
        Args:
            market_code: Market code (e.g., "CN", "US")
                        市场代码（例如："CN"、"US"）
            asset_type_code: Asset type code (e.g., "stock", "fund")
                            资产类型代码（例如："stock"、"fund"）
        
        Returns:
            MarketConfig object
            MarketConfig对象
        
        Raises:
            ValueError: If market or asset type is invalid
                       如果市场或资产类型无效
        """
        # Validate market
        # 验证市场
        if market_code not in self.markets:
            error_msg = f"Invalid market code: {market_code}"
            error_msg_cn = f"无效的市场代码: {market_code}"
            self.logger.error(f"{error_msg} / {error_msg_cn}")
            raise ValueError(f"{error_msg} / {error_msg_cn}")
        
        # Validate asset type
        # 验证资产类型
        if market_code not in self.asset_types or asset_type_code not in self.asset_types[market_code]:
            error_msg = f"Invalid asset type '{asset_type_code}' for market '{market_code}'"
            error_msg_cn = f"市场 '{market_code}' 的资产类型 '{asset_type_code}' 无效"
            self.logger.error(f"{error_msg} / {error_msg_cn}")
            raise ValueError(f"{error_msg} / {error_msg_cn}")
        
        # Get market and asset type objects
        # 获取市场和资产类型对象
        market = self.markets[market_code]
        asset_type = self.asset_types[market_code][asset_type_code]
        
        # Get data source and default instruments pool from config
        # 从配置获取数据源和默认工具池
        market_data = self.markets_config['markets'][market_code]
        asset_data = market_data['asset_types'][asset_type_code]
        
        data_source = asset_data.get('data_source', f'qlib_{market.region}')
        
        # Get default instruments pool
        # 获取默认工具池
        instruments_pools = asset_data.get('instruments_pools', [])
        if instruments_pools:
            instruments_pool = instruments_pools[0]['name']
        else:
            instruments_pool = 'all'
        
        # Create market config
        # 创建市场配置
        config = MarketConfig(
            market=market,
            asset_type=asset_type,
            data_source=data_source,
            instruments_pool=instruments_pool
        )
        
        self.logger.info(f"Created market config: {market_code}/{asset_type_code}")
        self.logger.info(f"创建了市场配置: {market_code}/{asset_type_code}")
        
        return config
    
    def get_market_info(self, market_code: str) -> MarketInfo:
        """
        Get detailed information about a specific market.
        获取特定市场的详细信息
        
        Args:
            market_code: Market code (e.g., "CN", "US")
                        市场代码（例如："CN"、"US"）
        
        Returns:
            MarketInfo object
            MarketInfo对象
        
        Raises:
            ValueError: If market code is invalid
                       如果市场代码无效
        """
        if market_code not in self.markets:
            error_msg = f"Invalid market code: {market_code}"
            error_msg_cn = f"无效的市场代码: {market_code}"
            self.logger.error(f"{error_msg} / {error_msg_cn}")
            raise ValueError(f"{error_msg} / {error_msg_cn}")
        
        market = self.markets[market_code]
        asset_types = self.get_asset_types(market_code)
        
        # Get market description from config
        # 从配置获取市场描述
        market_data = self.markets_config['markets'][market_code]
        description = market_data.get('description', '')
        
        # For now, assume data is available (can be enhanced later)
        # 目前假设数据可用（以后可以增强）
        market_info = MarketInfo(
            market=market,
            available_asset_types=asset_types,
            data_available=True,
            description=description
        )
        
        self.logger.debug(f"Retrieved market info for {market_code}")
        self.logger.debug(f"检索到市场 {market_code} 的信息")
        
        return market_info
    
    def get_instruments_pools(self, market_code: str, asset_type_code: str) -> List[Dict[str, str]]:
        """
        Get available instruments pools for a market and asset type.
        获取市场和资产类型的可用工具池
        
        Args:
            market_code: Market code
                        市场代码
            asset_type_code: Asset type code
                            资产类型代码
        
        Returns:
            List of instruments pool dictionaries with 'name' and 'description'
            包含'name'和'description'的工具池字典列表
        
        Raises:
            ValueError: If market or asset type is invalid
                       如果市场或资产类型无效
        """
        if market_code not in self.markets_config['markets']:
            error_msg = f"Invalid market code: {market_code}"
            error_msg_cn = f"无效的市场代码: {market_code}"
            raise ValueError(f"{error_msg} / {error_msg_cn}")
        
        market_data = self.markets_config['markets'][market_code]
        
        if 'asset_types' not in market_data or asset_type_code not in market_data['asset_types']:
            error_msg = f"Invalid asset type '{asset_type_code}' for market '{market_code}'"
            error_msg_cn = f"市场 '{market_code}' 的资产类型 '{asset_type_code}' 无效"
            raise ValueError(f"{error_msg} / {error_msg_cn}")
        
        asset_data = market_data['asset_types'][asset_type_code]
        pools = asset_data.get('instruments_pools', [])
        
        self.logger.debug(f"Retrieved {len(pools)} instruments pools for {market_code}/{asset_type_code}")
        self.logger.debug(f"为 {market_code}/{asset_type_code} 检索到 {len(pools)} 个工具池")
        
        return pools
    
    def get_default_config(self) -> MarketConfig:
        """
        Get default market configuration.
        获取默认市场配置
        
        Returns:
            Default MarketConfig object
            默认的MarketConfig对象
        """
        default_market = self.markets_config.get('default_market', 'CN')
        default_asset_type = self.markets_config.get('default_asset_type', 'stock')
        
        self.logger.info(f"Using default config: {default_market}/{default_asset_type}")
        self.logger.info(f"使用默认配置: {default_market}/{default_asset_type}")
        
        return self.select_market_and_type(default_market, default_asset_type)
