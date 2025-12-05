#!/usr/bin/env python
"""
测试数据管理CLI功能
Test Data Management CLI Functionality
"""

import sys
from pathlib import Path

# 添加src目录到路径 / Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.cli.main_cli import MainCLI


def test_data_management_menu():
    """
    测试数据管理菜单是否正常工作
    Test if data management menu works properly
    """
    print("=" * 70)
    print("测试数据管理CLI功能 / Testing Data Management CLI Functionality")
    print("=" * 70)
    print()
    
    try:
        # 创建CLI实例 / Create CLI instance
        cli = MainCLI()
        
        # 测试数据管理器初始化 / Test data manager initialization
        print("1. 测试数据管理器初始化 / Testing data manager initialization...")
        data_manager = cli._get_data_manager()
        print("   ✅ 数据管理器初始化成功 / Data manager initialized successfully")
        print()
        
        # 测试数据管理菜单方法存在 / Test data management menu methods exist
        print("2. 测试数据管理菜单方法 / Testing data management menu methods...")
        
        methods_to_test = [
            '_handle_data_management',
            '_download_market_data',
            '_validate_data_integrity',
            '_view_data_info',
            '_check_data_coverage'
        ]
        
        for method_name in methods_to_test:
            if hasattr(cli, method_name):
                print(f"   ✅ 方法存在 / Method exists: {method_name}")
            else:
                print(f"   ❌ 方法缺失 / Method missing: {method_name}")
                return False
        
        print()
        
        # 测试菜单选项 / Test menu options
        print("3. 测试菜单选项 / Testing menu options...")
        if "4" in cli.menu_options:
            option = cli.menu_options["4"]
            print(f"   ✅ 菜单选项4存在 / Menu option 4 exists")
            print(f"      名称 / Name: {option['name']}")
            print(f"      描述 / Description: {option['description']}")
        else:
            print(f"   ❌ 菜单选项4缺失 / Menu option 4 missing")
            return False
        
        print()
        
        print("=" * 70)
        print("✅ 所有测试通过！ / All tests passed!")
        print("=" * 70)
        print()
        
        print("💡 提示 / Tips:")
        print("  • 数据管理功能已成功集成到主CLI")
        print("    Data management functionality successfully integrated into main CLI")
        print("  • 可以通过主菜单选项4访问数据管理功能")
        print("    Access data management via main menu option 4")
        print("  • 包含以下子功能：")
        print("    Includes the following sub-functions:")
        print("    - 下载市场数据 / Download market data")
        print("    - 验证数据完整性 / Validate data integrity")
        print("    - 查看数据信息 / View data information")
        print("    - 检查数据覆盖 / Check data coverage")
        print()
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败 / Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_data_management_menu()
    sys.exit(0 if success else 1)
