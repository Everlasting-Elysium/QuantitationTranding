"""
完整数据管理示例 / Complete Data Management Example
演示数据下载、验证、更新的完整流程
Demonstrates the complete workflow of data download, validation, and update

这个示例展示了:
This example demonstrates:
1. 数据下载 / Data download
2. 数据验证 / Data validation
3. 数据信息查询 / Data information query
4. 数据更新 / Data update
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径 / Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.data_manager import DataManager
from src.infrastructure.qlib_wrapper import QlibWrapper
from src.infrastructure.logger_system import setup_logger


def print_section(title: str):
    """打印章节标题 / Print section title"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def main():
    """主函数 / Main function"""
    
    print_section("数据管理完整示例 / Complete Data Management Example")
    
    # 设置日志 / Setup logging
    setup_logger(log_dir="./logs", log_level="INFO")
    
    # ========================================================================
    # 步骤 1: 初始化 / Step 1: Initialization
    # ========================================================================
    print("\n步骤 1 / Step 1: 初始化数据管理器 / Initialize Data Manager")
    print("-" * 80)
    
    qlib_wrapper = QlibWrapper()
    data_manager = DataManager(qlib_wrapper=qlib_wrapper)
    
    print("✓ 数据管理器初始化完成 / Data manager initialized")
    
    # ========================================================================
    # 步骤 2: 数据下载 / Step 2: Data Download
    # ========================================================================
    print("\n步骤 2 / Step 2: 下载数据 / Download Data")
    print("-" * 80)
    
    print("数据下载选项 / Data download options:")
    print("  1. 中国市场数据 / China market data")
    print("     Region: cn")
    print("     Target: ~/.qlib/qlib_data/cn_data")
    print("  2. 美国市场数据 / US market data")
    print("     Region: us")
    print("     Target: ~/.qlib/qlib_data/us_data")
    
    # 示例：下载中国市场数据 / Example: Download China market data
    print("\n示例：下载中国市场数据 / Example: Download China market data")
    print("命令 / Command:")
    print("  python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn")
    
    print("\n注意 / Note:")
    print("  - 首次下载可能需要较长时间 / First download may take a long time")
    print("  - 需要稳定的网络连接 / Requires stable network connection")
    print("  - 数据大小约 / Data size approximately: 2-5GB")
    
    # ========================================================================
    # 步骤 3: 初始化Qlib / Step 3: Initialize Qlib
    # ========================================================================
    print("\n步骤 3 / Step 3: 初始化Qlib / Initialize Qlib")
    print("-" * 80)
    
    data_path = "~/.qlib/qlib_data/cn_data"
    region = "cn"
    
    try:
        qlib_wrapper.init(
            provider_uri=data_path,
            region=region
        )
        print(f"✓ Qlib初始化成功 / Qlib initialized successfully")
        print(f"  数据路径 / Data path: {data_path}")
        print(f"  区域 / Region: {region}")
    except Exception as e:
        print(f"✗ Qlib初始化失败 / Qlib initialization failed: {str(e)}")
        print("\n请先下载数据 / Please download data first")
        return
    
    # ========================================================================
    # 步骤 4: 数据验证 / Step 4: Data Validation
    # ========================================================================
    print("\n步骤 4 / Step 4: 数据验证 / Data Validation")
    print("-" * 80)
    
    try:
        # 验证特定时间范围的数据 / Validate data for specific time range
        start_date = "2020-01-01"
        end_date = "2023-12-31"
        
        print(f"验证时间范围 / Validating time range: {start_date} 至 / to {end_date}")
        
        validation_result = data_manager.validate_data(
            start_date=start_date,
            end_date=end_date
        )
        
        if validation_result.get("valid", False):
            print(f"✓ 数据验证通过 / Data validation passed")
            print(f"  可用交易日 / Available trading days: {validation_result.get('trading_days', 0)}")
            print(f"  可用股票数 / Available stocks: {validation_result.get('stock_count', 0)}")
        else:
            print(f"✗ 数据验证失败 / Data validation failed")
            print(f"  错误信息 / Error message: {validation_result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"✗ 数据验证失败 / Data validation failed: {str(e)}")
    
    # ========================================================================
    # 步骤 5: 查询数据信息 / Step 5: Query Data Information
    # ========================================================================
    print("\n步骤 5 / Step 5: 查询数据信息 / Query Data Information")
    print("-" * 80)
    
    try:
        data_info = data_manager.get_data_info()
        
        print("数据信息 / Data information:")
        print(f"  数据开始日期 / Data start date: {data_info.get('start_date', 'N/A')}")
        print(f"  数据结束日期 / Data end date: {data_info.get('end_date', 'N/A')}")
        print(f"  总交易日数 / Total trading days: {data_info.get('total_days', 'N/A')}")
        print(f"  可用股票数 / Available stocks: {data_info.get('stock_count', 'N/A')}")
        print(f"  数据路径 / Data path: {data_info.get('data_path', 'N/A')}")
        print(f"  区域 / Region: {data_info.get('region', 'N/A')}")
        
    except Exception as e:
        print(f"✗ 查询数据信息失败 / Query data information failed: {str(e)}")
    
    # ========================================================================
    # 步骤 6: 数据更新 / Step 6: Data Update
    # ========================================================================
    print("\n步骤 6 / Step 6: 数据更新 / Data Update")
    print("-" * 80)
    
    print("数据更新方法 / Data update methods:")
    print("  1. 增量更新 / Incremental update")
    print("     - 只下载新增数据 / Only download new data")
    print("     - 速度快 / Fast")
    print("     - 命令 / Command:")
    print("       python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn --interval 1d")
    
    print("\n  2. 完全重新下载 / Complete re-download")
    print("     - 下载所有数据 / Download all data")
    print("     - 确保数据完整性 / Ensure data integrity")
    print("     - 命令 / Command:")
    print("       python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn --delete_old")
    
    print("\n建议 / Recommendations:")
    print("  - 每日更新：使用增量更新 / Daily update: Use incremental update")
    print("  - 每月一次：使用完全重新下载 / Monthly: Use complete re-download")
    print("  - 数据异常时：使用完全重新下载 / Data anomaly: Use complete re-download")
    
    # ========================================================================
    # 步骤 7: 数据使用示例 / Step 7: Data Usage Example
    # ========================================================================
    print("\n步骤 7 / Step 7: 数据使用示例 / Data Usage Example")
    print("-" * 80)
    
    try:
        # 获取特定股票的数据 / Get data for specific stocks
        print("获取CSI300成分股数据 / Getting CSI300 constituent stocks data")
        
        # 这里只是演示如何使用数据管理器
        # This is just to demonstrate how to use the data manager
        print("✓ 数据可以通过qlib接口访问 / Data can be accessed through qlib interface")
        print("  示例代码 / Example code:")
        print("    from qlib.data import D")
        print("    data = D.features(['SH600000'], ['$close', '$volume'], start_time='2020-01-01', end_time='2020-12-31')")
        
    except Exception as e:
        print(f"✗ 数据使用示例失败 / Data usage example failed: {str(e)}")
    
    # ========================================================================
    # 总结 / Summary
    # ========================================================================
    print_section("总结 / Summary")
    
    print("\n本示例展示了数据管理的完整流程:")
    print("This example demonstrated the complete data management workflow:")
    print("  ✓ 数据下载方法 / Data download methods")
    print("  ✓ Qlib初始化 / Qlib initialization")
    print("  ✓ 数据验证 / Data validation")
    print("  ✓ 数据信息查询 / Data information query")
    print("  ✓ 数据更新策略 / Data update strategies")
    print("  ✓ 数据使用示例 / Data usage examples")
    
    print("\n常见问题 / Common Issues:")
    print("  1. 数据下载失败 / Data download failed")
    print("     - 检查网络连接 / Check network connection")
    print("     - 检查磁盘空间 / Check disk space")
    print("     - 尝试使用代理 / Try using proxy")
    
    print("\n  2. 数据验证失败 / Data validation failed")
    print("     - 重新下载数据 / Re-download data")
    print("     - 检查数据路径 / Check data path")
    print("     - 检查时间范围 / Check time range")
    
    print("\n  3. 数据更新失败 / Data update failed")
    print("     - 使用完全重新下载 / Use complete re-download")
    print("     - 检查数据源状态 / Check data source status")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
