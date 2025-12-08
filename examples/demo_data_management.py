#!/usr/bin/env python
"""
数据管理功能演示脚本
Data Management Functionality Demo Script

这个脚本演示如何使用数据管理功能
This script demonstrates how to use data management functionality
"""

import sys
from pathlib import Path

# 添加src目录到路径 / Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def demo_data_management():
    """
    演示数据管理功能
    Demonstrate data management functionality
    """
    print("\n" + "=" * 70)
    print("📚 数据管理功能演示 / Data Management Functionality Demo")
    print("=" * 70)
    print()
    
    print("本演示展示了数据管理CLI的主要功能：")
    print("This demo shows the main features of data management CLI:")
    print()
    
    print("1️⃣  下载市场数据 / Download Market Data")
    print("   • 支持多个市场区域（中国、美国等）")
    print("     Supports multiple market regions (China, US, etc.)")
    print("   • 支持不同数据间隔（日线、分钟线）")
    print("     Supports different data intervals (daily, minute)")
    print("   • 可指定时间范围")
    print("     Can specify time range")
    print("   • 提供详细的下载指引")
    print("     Provides detailed download instructions")
    print()
    
    print("2️⃣  验证数据完整性 / Validate Data Integrity")
    print("   • 检查数据是否存在")
    print("     Check if data exists")
    print("   • 验证数据格式")
    print("     Validate data format")
    print("   • 检查数据完整性")
    print("     Check data integrity")
    print("   • 识别缺失值和异常")
    print("     Identify missing values and anomalies")
    print("   • 提供详细的验证报告")
    print("     Provide detailed validation report")
    print()
    
    print("3️⃣  查看数据信息 / View Data Information")
    print("   • 显示数据提供者信息")
    print("     Display data provider information")
    print("   • 显示市场区域")
    print("     Display market region")
    print("   • 显示数据时间范围")
    print("     Display data time range")
    print("   • 显示交易日数量")
    print("     Display number of trading days")
    print("   • 显示股票数量")
    print("     Display number of instruments")
    print()
    
    print("4️⃣  检查数据覆盖 / Check Data Coverage")
    print("   • 检查特定时间范围的数据覆盖")
    print("     Check data coverage for specific time range")
    print("   • 验证数据是否满足训练/回测需求")
    print("     Verify if data meets training/backtesting requirements")
    print("   • 提供数据缺口分析")
    print("     Provide data gap analysis")
    print("   • 给出改进建议")
    print("     Provide improvement suggestions")
    print()
    
    print("=" * 70)
    print("🚀 使用方法 / Usage")
    print("=" * 70)
    print()
    
    print("方法1：通过主CLI访问 / Method 1: Access via main CLI")
    print("  1. 运行主程序：python main.py")
    print("     Run main program: python main.py")
    print("  2. 选择菜单选项 4 (数据管理)")
    print("     Select menu option 4 (Data Management)")
    print("  3. 选择所需的数据管理操作")
    print("     Select desired data management operation")
    print()
    
    print("方法2：直接使用DataManager类 / Method 2: Use DataManager class directly")
    print("  示例代码 / Example code:")
    print()
    print("  ```python")
    print("  from src.core.data_manager import DataManager")
    print("  ")
    print("  # 创建数据管理器 / Create data manager")
    print("  data_manager = DataManager()")
    print("  ")
    print("  # 初始化 / Initialize")
    print("  data_manager.initialize(")
    print("      data_path='~/.qlib/qlib_data/cn_data',")
    print("      region='cn'")
    print("  )")
    print("  ")
    print("  # 验证数据 / Validate data")
    print("  result = data_manager.validate_data(")
    print("      start_date='2020-01-01',")
    print("      end_date='2023-12-31',")
    print("      instruments='csi300'")
    print("  )")
    print("  ")
    print("  # 查看数据信息 / View data info")
    print("  info = data_manager.get_data_info()")
    print("  print(f'数据范围: {info.data_start} 至 {info.data_end}')")
    print("  ```")
    print()
    
    print("=" * 70)
    print("💡 重要提示 / Important Notes")
    print("=" * 70)
    print()
    
    print("1. 首次使用前需要下载数据")
    print("   Need to download data before first use")
    print()
    
    print("2. 数据下载命令示例（中国市场）：")
    print("   Data download command example (China market):")
    print("   python -m qlib.run.get_data qlib_data \\")
    print("       --target_dir ~/.qlib/qlib_data/cn_data \\")
    print("       --region cn \\")
    print("       --interval 1d")
    print()
    
    print("3. 确保有足够的磁盘空间")
    print("   Ensure sufficient disk space")
    print("   • 日线数据约需要 1-2 GB")
    print("     Daily data requires about 1-2 GB")
    print("   • 分钟数据约需要 10-20 GB")
    print("     Minute data requires about 10-20 GB")
    print()
    
    print("4. 数据更新建议")
    print("   Data update recommendations")
    print("   • 每周更新一次数据")
    print("     Update data weekly")
    print("   • 训练前验证数据完整性")
    print("     Validate data integrity before training")
    print("   • 定期检查数据覆盖范围")
    print("     Regularly check data coverage")
    print()
    
    print("=" * 70)
    print("📖 相关文档 / Related Documentation")
    print("=" * 70)
    print()
    
    print("• 数据管理器实现：src/core/data_manager.py")
    print("  Data manager implementation: src/core/data_manager.py")
    print()
    print("• CLI实现：src/cli/main_cli.py")
    print("  CLI implementation: src/cli/main_cli.py")
    print()
    print("• Qlib数据文档：https://qlib.readthedocs.io/en/latest/component/data.html")
    print("  Qlib data documentation: https://qlib.readthedocs.io/en/latest/component/data.html")
    print()
    
    print("=" * 70)
    print("✅ 演示完成 / Demo Completed")
    print("=" * 70)
    print()


if __name__ == "__main__":
    demo_data_management()
