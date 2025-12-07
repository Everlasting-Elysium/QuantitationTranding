"""
Demo script for MarketSelector
市场选择器演示脚本

This script demonstrates how to use the MarketSelector to:
- Get available markets
- Get asset types for a market
- Create market configurations
- Get market information

本脚本演示如何使用MarketSelector：
- 获取可用市场
- 获取市场的资产类型
- 创建市场配置
- 获取市场信息
"""

import sys
from pathlib import Path

# Add src to path
# 将src添加到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.application.market_selector import MarketSelector
from src.infrastructure.logger_system import LoggerSystem


def main():
    """Main demo function / 主演示函数"""
    
    # Setup logging
    # 设置日志
    logger_system = LoggerSystem()
    logger_system.setup(log_dir="logs", log_level="INFO")
    logger = logger_system.get_logger(__name__)
    
    print("=" * 80)
    print("Market Selector Demo / 市场选择器演示")
    print("=" * 80)
    print()
    
    try:
        # Initialize MarketSelector
        # 初始化MarketSelector
        print("1. Initializing MarketSelector...")
        print("1. 初始化MarketSelector...")
        selector = MarketSelector()
        print("✓ MarketSelector initialized successfully")
        print("✓ MarketSelector初始化成功")
        print()
        
        # Get available markets
        # 获取可用市场
        print("2. Getting available markets...")
        print("2. 获取可用市场...")
        markets = selector.get_available_markets()
        print(f"Found {len(markets)} markets:")
        print(f"找到 {len(markets)} 个市场:")
        for market in markets:
            print(f"  - {market.code}: {market.name} (Region: {market.region})")
        print()
        
        # Get asset types for Chinese market
        # 获取中国市场的资产类型
        print("3. Getting asset types for Chinese market (CN)...")
        print("3. 获取中国市场(CN)的资产类型...")
        asset_types = selector.get_asset_types("CN")
        print(f"Found {len(asset_types)} asset types:")
        print(f"找到 {len(asset_types)} 个资产类型:")
        for asset_type in asset_types:
            print(f"  - {asset_type.code}: {asset_type.name}")
            print(f"    Description: {asset_type.description}")
            print(f"    描述: {asset_type.description}")
        print()
        
        # Get instruments pools for CN stock
        # 获取CN股票的工具池
        print("4. Getting instruments pools for CN stock...")
        print("4. 获取CN股票的工具池...")
        pools = selector.get_instruments_pools("CN", "stock")
        print(f"Found {len(pools)} instruments pools:")
        print(f"找到 {len(pools)} 个工具池:")
        for pool in pools:
            print(f"  - {pool['name']}: {pool['description']}")
        print()
        
        # Create market configuration
        # 创建市场配置
        print("5. Creating market configuration for CN stock...")
        print("5. 为CN股票创建市场配置...")
        config = selector.select_market_and_type("CN", "stock")
        print("Market Configuration:")
        print("市场配置:")
        print(f"  Market: {config.market.name} ({config.market.code})")
        print(f"  市场: {config.market.name} ({config.market.code})")
        print(f"  Asset Type: {config.asset_type.name} ({config.asset_type.code})")
        print(f"  资产类型: {config.asset_type.name} ({config.asset_type.code})")
        print(f"  Data Source: {config.data_source}")
        print(f"  数据源: {config.data_source}")
        print(f"  Instruments Pool: {config.instruments_pool}")
        print(f"  工具池: {config.instruments_pool}")
        print()
        
        # Get market info
        # 获取市场信息
        print("6. Getting detailed market information for CN...")
        print("6. 获取CN的详细市场信息...")
        market_info = selector.get_market_info("CN")
        print("Market Information:")
        print("市场信息:")
        print(f"  Name: {market_info.market.name}")
        print(f"  名称: {market_info.market.name}")
        print(f"  Region: {market_info.market.region}")
        print(f"  区域: {market_info.market.region}")
        print(f"  Timezone: {market_info.market.timezone}")
        print(f"  时区: {market_info.market.timezone}")
        print(f"  Data Available: {market_info.data_available}")
        print(f"  数据可用: {market_info.data_available}")
        print(f"  Description: {market_info.description}")
        print(f"  描述: {market_info.description}")
        print(f"  Available Asset Types: {len(market_info.available_asset_types)}")
        print(f"  可用资产类型: {len(market_info.available_asset_types)}")
        print()
        
        # Get default configuration
        # 获取默认配置
        print("7. Getting default market configuration...")
        print("7. 获取默认市场配置...")
        default_config = selector.get_default_config()
        print(f"Default: {default_config.market.code}/{default_config.asset_type.code}")
        print(f"默认: {default_config.market.code}/{default_config.asset_type.code}")
        print()
        
        # Try US market
        # 尝试美国市场
        print("8. Creating configuration for US stock market...")
        print("8. 为美国股票市场创建配置...")
        us_config = selector.select_market_and_type("US", "stock")
        print(f"US Market Config: {us_config.market.name} - {us_config.asset_type.name}")
        print(f"美国市场配置: {us_config.market.name} - {us_config.asset_type.name}")
        print(f"Instruments Pool: {us_config.instruments_pool}")
        print(f"工具池: {us_config.instruments_pool}")
        print()
        
        # Test error handling
        # 测试错误处理
        print("9. Testing error handling...")
        print("9. 测试错误处理...")
        try:
            invalid_config = selector.select_market_and_type("INVALID", "stock")
        except ValueError as e:
            print(f"✓ Caught expected error: {e}")
            print(f"✓ 捕获到预期错误: {e}")
        print()
        
        print("=" * 80)
        print("Demo completed successfully! / 演示成功完成!")
        print("=" * 80)
        
    except Exception as e:
        logger.error(f"Demo failed: {e}", exc_info=True)
        print(f"✗ Demo failed: {e}")
        print(f"✗ 演示失败: {e}")
        raise


if __name__ == "__main__":
    main()
