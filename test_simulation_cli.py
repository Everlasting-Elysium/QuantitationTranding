#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试模拟交易CLI集成 / Test Simulation Trading CLI Integration

这个脚本用于测试模拟交易功能是否正确集成到CLI中。
This script tests if simulation trading is correctly integrated into the CLI.
"""

import sys
from pathlib import Path

# 添加src目录到路径 / Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_cli_menu_options():
    """测试CLI菜单选项 / Test CLI menu options"""
    print("=" * 70)
    print("测试CLI菜单选项 / Testing CLI Menu Options")
    print("=" * 70)
    print()
    
    try:
        from src.cli.main_cli import MainCLI
        
        # 创建CLI实例 / Create CLI instance
        cli = MainCLI()
        
        # 检查菜单选项 / Check menu options
        print("✓ MainCLI实例创建成功 / MainCLI instance created successfully")
        print()
        
        # 检查是否有模拟交易选项 / Check if simulation trading option exists
        if "3" in cli.menu_options:
            option = cli.menu_options["3"]
            print(f"✓ 找到模拟交易菜单选项 / Found simulation trading menu option:")
            print(f"  名称 / Name: {option['name']}")
            print(f"  描述 / Description: {option['description']}")
            print(f"  处理器 / Handler: {option['handler'].__name__}")
            print()
            
            # 检查处理器方法是否存在 / Check if handler method exists
            if hasattr(cli, '_handle_simulation_trading'):
                print("✓ _handle_simulation_trading 方法存在 / _handle_simulation_trading method exists")
            else:
                print("✗ _handle_simulation_trading 方法不存在 / _handle_simulation_trading method does not exist")
                return False
            
            # 检查辅助方法是否存在 / Check if helper methods exist
            helper_methods = [
                '_get_simulation_engine',
                '_start_new_simulation',
                '_display_simulation_result',
                '_show_detailed_simulation_report',
                '_export_simulation_report',
                '_view_simulation_results',
                '_adjust_and_retest_simulation'
            ]
            
            print()
            print("检查辅助方法 / Checking helper methods:")
            all_exist = True
            for method_name in helper_methods:
                if hasattr(cli, method_name):
                    print(f"  ✓ {method_name}")
                else:
                    print(f"  ✗ {method_name} (缺失 / missing)")
                    all_exist = False
            
            if all_exist:
                print()
                print("✅ 所有必需的方法都存在 / All required methods exist")
                return True
            else:
                print()
                print("❌ 部分方法缺失 / Some methods are missing")
                return False
        else:
            print("✗ 未找到模拟交易菜单选项 / Simulation trading menu option not found")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败 / Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_simulation_engine_import():
    """测试模拟引擎导入 / Test simulation engine import"""
    print("\n" + "=" * 70)
    print("测试模拟引擎导入 / Testing Simulation Engine Import")
    print("=" * 70)
    print()
    
    try:
        from src.application.simulation_engine import SimulationEngine
        print("✓ SimulationEngine 导入成功 / SimulationEngine imported successfully")
        
        from src.application.simulation_engine import SimulationSession
        print("✓ SimulationSession 导入成功 / SimulationSession imported successfully")
        
        from src.application.simulation_engine import SimulationStepResult
        print("✓ SimulationStepResult 导入成功 / SimulationStepResult imported successfully")
        
        from src.application.simulation_engine import SimulationReport
        print("✓ SimulationReport 导入成功 / SimulationReport imported successfully")
        
        print()
        print("✅ 所有模拟引擎组件导入成功 / All simulation engine components imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ 导入失败 / Import failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_menu_display():
    """测试菜单显示 / Test menu display"""
    print("\n" + "=" * 70)
    print("测试菜单显示 / Testing Menu Display")
    print("=" * 70)
    print()
    
    try:
        from src.cli.main_cli import MainCLI
        
        cli = MainCLI()
        
        print("主菜单预览 / Main Menu Preview:")
        print("-" * 70)
        cli.show_menu()
        print()
        
        print("✅ 菜单显示成功 / Menu displayed successfully")
        return True
        
    except Exception as e:
        print(f"❌ 菜单显示失败 / Menu display failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数 / Main test function"""
    print("\n" + "=" * 70)
    print("🧪 模拟交易CLI集成测试 / Simulation Trading CLI Integration Test")
    print("=" * 70)
    print()
    
    results = []
    
    # 运行测试 / Run tests
    results.append(("CLI菜单选项测试 / CLI Menu Options Test", test_cli_menu_options()))
    results.append(("模拟引擎导入测试 / Simulation Engine Import Test", test_simulation_engine_import()))
    results.append(("菜单显示测试 / Menu Display Test", test_menu_display()))
    
    # 显示测试结果摘要 / Display test results summary
    print("\n" + "=" * 70)
    print("📊 测试结果摘要 / Test Results Summary")
    print("=" * 70)
    print()
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过 / PASSED" if result else "❌ 失败 / FAILED"
        print(f"{status}: {test_name}")
    
    print()
    print(f"总计 / Total: {passed}/{total} 测试通过 / tests passed")
    print()
    
    if passed == total:
        print("🎉 所有测试通过！ / All tests passed!")
        print("✅ 模拟交易CLI集成成功 / Simulation trading CLI integration successful")
        return 0
    else:
        print("⚠️  部分测试失败 / Some tests failed")
        print("请检查上述错误信息 / Please check the error messages above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
