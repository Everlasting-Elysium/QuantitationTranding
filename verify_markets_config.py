#!/usr/bin/env python3
"""
市场配置验证脚本 / Market Configuration Verification Script

验证markets.yaml配置文件的完整性和正确性
Verify the completeness and correctness of markets.yaml configuration file
"""

import os
import sys
import yaml
from pathlib import Path


def verify_markets_config():
    """
    验证市场配置文件
    Verify market configuration file
    """
    print("=" * 80)
    print("市场配置验证 / Market Configuration Verification")
    print("=" * 80)
    
    config_path = "config/markets.yaml"
    
    # 检查文件是否存在
    if not os.path.exists(config_path):
        print(f"❌ 错误：找不到文件 {config_path}")
        print(f"❌ Error: File {config_path} not found")
        return False
    
    print(f"✅ 文件存在：{config_path}")
    print(f"✅ File exists: {config_path}")
    print()
    
    # 读取YAML文件
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ YAML解析错误：{e}")
        print(f"❌ YAML parsing error: {e}")
        return False
    
    print("✅ YAML格式正确")
    print("✅ YAML format correct")
    print()
    
    # 必需的顶层键
    required_top_keys = ['markets', 'default_market', 'default_asset_type', 'default_instruments_pool']
    
    print("检查必需的顶层键 / Checking required top-level keys:")
    print("-" * 80)
    
    all_keys_present = True
    for key in required_top_keys:
        if key in config:
            print(f"✅ {key}")
        else:
            print(f"❌ 缺失：{key}")
            print(f"❌ Missing: {key}")
            all_keys_present = False
    
    print()
    
    # 检查市场配置
    markets = config.get('markets', {})
    required_markets = ['CN', 'US', 'HK']
    
    print("检查市场配置 / Checking market configurations:")
    print("-" * 80)
    
    all_markets_present = True
    for market_code in required_markets:
        if market_code in markets:
            print(f"✅ {market_code} - {markets[market_code].get('name', 'N/A')}")
        else:
            print(f"❌ 缺失市场：{market_code}")
            print(f"❌ Missing market: {market_code}")
            all_markets_present = False
    
    print()
    
    # 检查每个市场的必需字段
    required_market_fields = [
        'code', 'name', 'region', 'timezone', 'currency', 
        'trading_hours', 'characteristics', 'fees', 'asset_types'
    ]
    
    print("检查市场必需字段 / Checking required market fields:")
    print("-" * 80)
    
    all_fields_present = True
    for market_code, market_config in markets.items():
        print(f"\n{market_code} - {market_config.get('name', 'N/A')}:")
        for field in required_market_fields:
            if field in market_config:
                print(f"  ✅ {field}")
            else:
                print(f"  ❌ 缺失：{field}")
                print(f"  ❌ Missing: {field}")
                all_fields_present = False
    
    print()
    
    # 检查资产类型
    print("检查资产类型 / Checking asset types:")
    print("-" * 80)
    
    asset_type_stats = {}
    for market_code, market_config in markets.items():
        asset_types = market_config.get('asset_types', {})
        asset_type_stats[market_code] = list(asset_types.keys())
        print(f"{market_code}: {', '.join(asset_types.keys())}")
    
    print()
    
    # 检查股票池配置
    print("检查股票池配置 / Checking instruments pools:")
    print("-" * 80)
    
    for market_code, market_config in markets.items():
        asset_types = market_config.get('asset_types', {})
        for asset_type, asset_config in asset_types.items():
            pools = asset_config.get('instruments_pools', [])
            print(f"{market_code} - {asset_type}: {len(pools)} 个股票池")
            for pool in pools:
                pool_name = pool.get('name', 'N/A')
                pool_count = pool.get('count', 'N/A')
                print(f"  • {pool_name} ({pool_count})")
    
    print()
    
    # 检查数据源配置
    if 'data_sources' in config:
        print("检查数据源配置 / Checking data source configuration:")
        print("-" * 80)
        data_sources = config['data_sources']
        for source_name, source_config in data_sources.items():
            print(f"✅ {source_name}")
            print(f"   Provider: {source_config.get('provider', 'N/A')}")
            print(f"   Region: {source_config.get('region', 'N/A')}")
            print(f"   Data Dir: {source_config.get('data_dir', 'N/A')}")
        print()
    
    # 检查市场组合
    if 'market_combinations' in config:
        print("检查市场组合 / Checking market combinations:")
        print("-" * 80)
        combinations = config['market_combinations']
        for combo_name, combo_config in combinations.items():
            print(f"✅ {combo_name} - {combo_config.get('name', 'N/A')}")
            print(f"   Markets: {', '.join(combo_config.get('markets', []))}")
        print()
    
    # 统计信息
    print("配置统计 / Configuration Statistics:")
    print("-" * 80)
    print(f"市场数量 / Number of markets: {len(markets)}")
    print(f"资产类型总数 / Total asset types: {sum(len(m.get('asset_types', {})) for m in markets.values())}")
    
    total_pools = 0
    for market_config in markets.values():
        for asset_config in market_config.get('asset_types', {}).values():
            total_pools += len(asset_config.get('instruments_pools', []))
    print(f"股票池总数 / Total instruments pools: {total_pools}")
    
    if 'data_sources' in config:
        print(f"数据源数量 / Number of data sources: {len(config['data_sources'])}")
    
    if 'market_combinations' in config:
        print(f"市场组合数量 / Number of market combinations: {len(config['market_combinations'])}")
    
    print()
    
    # 文件大小
    file_size = os.path.getsize(config_path)
    print(f"文件大小 / File size: {file_size} bytes ({file_size/1024:.2f} KB)")
    
    print()
    print("=" * 80)
    
    # 最终结果
    if all_keys_present and all_markets_present and all_fields_present:
        print("✅ 验证通过！市场配置文件完整且格式正确。")
        print("✅ Verification passed! Market configuration file is complete and correctly formatted.")
        return True
    else:
        print("⚠️  验证发现一些问题，请检查上述缺失的内容。")
        print("⚠️  Verification found some issues, please check the missing content above.")
        return False


def print_market_summary():
    """
    打印市场配置摘要
    Print market configuration summary
    """
    config_path = "config/markets.yaml"
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    print("\n" + "=" * 80)
    print("市场配置摘要 / Market Configuration Summary")
    print("=" * 80 + "\n")
    
    markets = config.get('markets', {})
    
    for market_code, market_config in markets.items():
        print(f"【{market_code}】{market_config.get('name', 'N/A')} / {market_config.get('name_en', 'N/A')}")
        print("-" * 80)
        print(f"货币 / Currency: {market_config.get('currency', 'N/A')} ({market_config.get('currency_symbol', 'N/A')})")
        print(f"时区 / Timezone: {market_config.get('timezone', 'N/A')}")
        
        # 交易时间
        trading_hours = market_config.get('trading_hours', {})
        print(f"交易时间 / Trading Hours:")
        for key, value in trading_hours.items():
            print(f"  {key}: {value}")
        
        # 市场特性
        characteristics = market_config.get('characteristics', {})
        print(f"市场特性 / Characteristics:")
        print(f"  T+{characteristics.get('t_plus_n', 'N/A')} 结算")
        if characteristics.get('price_limit'):
            print(f"  涨跌停限制: ±{characteristics.get('price_limit', 0)*100:.0f}%")
        else:
            print(f"  无涨跌停限制")
        
        # 资产类型
        asset_types = market_config.get('asset_types', {})
        print(f"资产类型 / Asset Types: {', '.join(asset_types.keys())}")
        
        print()


if __name__ == "__main__":
    success = verify_markets_config()
    
    if success:
        print_market_summary()
    
    sys.exit(0 if success else 1)
