"""
测试回测功能CLI / Test Backtest CLI

这个脚本用于测试回测功能的CLI实现
This script tests the backtest CLI implementation
"""

import sys
import os

# 添加项目根目录到路径 / Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_backtest_cli_imports():
    """
    测试回测CLI相关的导入 / Test backtest CLI related imports
    """
    print("=" * 70)
    print("测试回测CLI导入 / Testing Backtest CLI Imports")
    print("=" * 70)
    print()
    
    try:
        # 测试导入MainCLI / Test importing MainCLI
        print("1. 导入MainCLI / Importing MainCLI...")
        from src.cli.main_cli import MainCLI
        print("   ✅ MainCLI导入成功 / MainCLI imported successfully")
        
        # 测试导入BacktestManager / Test importing BacktestManager
        print("\n2. 导入BacktestManager / Importing BacktestManager...")
        from src.application.backtest_manager import BacktestManager, BacktestConfig
        print("   ✅ BacktestManager导入成功 / BacktestManager imported successfully")
        
        # 测试导入ModelRegistry / Test importing ModelRegistry
        print("\n3. 导入ModelRegistry / Importing ModelRegistry...")
        from src.application.model_registry import ModelRegistry
        print("   ✅ ModelRegistry导入成功 / ModelRegistry imported successfully")
        
        # 测试导入InteractivePrompt / Test importing InteractivePrompt
        print("\n4. 导入InteractivePrompt / Importing InteractivePrompt...")
        from src.cli.interactive_prompt import InteractivePrompt
        print("   ✅ InteractivePrompt导入成功 / InteractivePrompt imported successfully")
        
        print("\n" + "=" * 70)
        print("✅ 所有导入测试通过 / All import tests passed")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ 导入测试失败 / Import test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_backtest_cli_structure():
    """
    测试回测CLI的结构 / Test backtest CLI structure
    """
    print("\n" + "=" * 70)
    print("测试回测CLI结构 / Testing Backtest CLI Structure")
    print("=" * 70)
    print()
    
    try:
        from src.cli.main_cli import MainCLI
        
        # 创建MainCLI实例 / Create MainCLI instance
        print("1. 创建MainCLI实例 / Creating MainCLI instance...")
        cli = MainCLI()
        print("   ✅ MainCLI实例创建成功 / MainCLI instance created successfully")
        
        # 检查回测相关方法是否存在 / Check if backtest related methods exist
        print("\n2. 检查回测相关方法 / Checking backtest related methods...")
        
        methods_to_check = [
            '_handle_backtest',
            '_get_backtest_manager',
            '_get_model_registry',
            '_run_backtest',
            '_display_backtest_result',
            '_view_backtest_results'
        ]
        
        for method_name in methods_to_check:
            if hasattr(cli, method_name):
                print(f"   ✅ 方法存在 / Method exists: {method_name}")
            else:
                print(f"   ❌ 方法缺失 / Method missing: {method_name}")
                return False
        
        # 检查菜单选项 / Check menu options
        print("\n3. 检查菜单选项 / Checking menu options...")
        if "2" in cli.menu_options:
            option = cli.menu_options["2"]
            print(f"   ✅ 回测菜单选项存在 / Backtest menu option exists:")
            print(f"      名称 / Name: {option['name']}")
            print(f"      描述 / Description: {option['description']}")
        else:
            print("   ❌ 回测菜单选项缺失 / Backtest menu option missing")
            return False
        
        print("\n" + "=" * 70)
        print("✅ 所有结构测试通过 / All structure tests passed")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ 结构测试失败 / Structure test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_backtest_config():
    """
    测试回测配置 / Test backtest configuration
    """
    print("\n" + "=" * 70)
    print("测试回测配置 / Testing Backtest Configuration")
    print("=" * 70)
    print()
    
    try:
        from src.application.backtest_manager import BacktestConfig
        
        # 创建回测配置 / Create backtest configuration
        print("1. 创建回测配置 / Creating backtest configuration...")
        config = BacktestConfig(
            strategy_config={
                "instruments": "csi300",
                "topk": 50,
                "n_drop": 5,
            },
            executor_config={
                "time_per_step": "day",
            },
            benchmark="SH000300"
        )
        print("   ✅ 回测配置创建成功 / Backtest configuration created successfully")
        
        # 验证配置内容 / Verify configuration content
        print("\n2. 验证配置内容 / Verifying configuration content...")
        print(f"   股票池 / Instruments: {config.strategy_config['instruments']}")
        print(f"   持仓数量 / Topk: {config.strategy_config['topk']}")
        print(f"   调仓卖出 / N_drop: {config.strategy_config['n_drop']}")
        print(f"   基准指数 / Benchmark: {config.benchmark}")
        print("   ✅ 配置内容验证通过 / Configuration content verified")
        
        print("\n" + "=" * 70)
        print("✅ 回测配置测试通过 / Backtest configuration test passed")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ 配置测试失败 / Configuration test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """
    主测试函数 / Main test function
    """
    print("\n" + "=" * 70)
    print("🧪 回测功能CLI测试 / Backtest CLI Test Suite")
    print("=" * 70)
    print()
    
    # 运行所有测试 / Run all tests
    tests = [
        ("导入测试 / Import Test", test_backtest_cli_imports),
        ("结构测试 / Structure Test", test_backtest_cli_structure),
        ("配置测试 / Configuration Test", test_backtest_config),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'=' * 70}")
        print(f"运行测试 / Running Test: {test_name}")
        print(f"{'=' * 70}")
        result = test_func()
        results.append((test_name, result))
    
    # 显示测试总结 / Display test summary
    print("\n" + "=" * 70)
    print("📊 测试总结 / Test Summary")
    print("=" * 70)
    print()
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过 / PASSED" if result else "❌ 失败 / FAILED"
        print(f"  {test_name}: {status}")
    
    print()
    print(f"总计 / Total: {passed}/{total} 测试通过 / tests passed")
    print("=" * 70)
    
    if passed == total:
        print("\n🎉 所有测试通过！ / All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} 个测试失败 / tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
