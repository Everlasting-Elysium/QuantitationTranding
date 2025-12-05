#!/usr/bin/env python3
"""
模型管理CLI测试脚本 / Model Management CLI Test Script

This script tests the model management functionality.
本脚本测试模型管理功能。

Usage / 使用方法:
    python test_model_management_cli.py
"""

import sys
from pathlib import Path

# 添加src目录到Python路径 / Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_model_registry_integration():
    """
    测试模型注册表集成 / Test model registry integration
    """
    print("=" * 70)
    print("🧪 测试模型注册表集成 / Test Model Registry Integration")
    print("=" * 70)
    print()
    
    try:
        from src.application.model_registry import ModelRegistry, ModelInfo
        
        # 创建模型注册表实例 / Create model registry instance
        print("1. 创建模型注册表实例 / Creating model registry instance...")
        registry = ModelRegistry(registry_dir="./test_model_registry")
        print("   ✅ 成功 / Success")
        print()
        
        # 列出所有模型 / List all models
        print("2. 列出所有模型 / Listing all models...")
        models = registry.list_models()
        print(f"   找到 {len(models)} 个模型 / Found {len(models)} models")
        
        if models:
            print("   模型列表 / Model list:")
            for i, model in enumerate(models[:5], 1):  # 只显示前5个 / Only show first 5
                print(f"   {i}. {model.model_name} (v{model.version}) - {model.status}")
        else:
            print("   ⚠️  没有找到模型 / No models found")
            print("   提示：请先运行训练脚本创建一些模型")
            print("   Tip: Please run training script to create some models first")
        print()
        
        # 获取生产模型 / Get production model
        print("3. 获取生产模型 / Getting production model...")
        production_model = registry.get_production_model()
        
        if production_model:
            print(f"   当前生产模型 / Current production model:")
            print(f"   {production_model.model_name} (v{production_model.version})")
            print(f"   模型ID / Model ID: {production_model.model_id}")
        else:
            print("   ⚠️  当前没有生产模型 / No production model currently set")
        print()
        
        print("=" * 70)
        print("✅ 模型注册表集成测试通过 / Model registry integration test passed")
        print("=" * 70)
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败 / Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_cli_model_management_methods():
    """
    测试CLI模型管理方法 / Test CLI model management methods
    """
    print("=" * 70)
    print("🧪 测试CLI模型管理方法 / Test CLI Model Management Methods")
    print("=" * 70)
    print()
    
    try:
        from src.cli.main_cli import MainCLI
        
        # 创建CLI实例 / Create CLI instance
        print("1. 创建CLI实例 / Creating CLI instance...")
        cli = MainCLI()
        print("   ✅ 成功 / Success")
        print()
        
        # 检查模型管理方法是否存在 / Check if model management methods exist
        print("2. 检查模型管理方法 / Checking model management methods...")
        
        methods_to_check = [
            "_handle_model_management",
            "_view_model_list",
            "_view_model_details",
            "_set_production_model",
            "_delete_model",
            "_export_model_info",
            "_get_model_registry"
        ]
        
        all_methods_exist = True
        for method_name in methods_to_check:
            if hasattr(cli, method_name):
                print(f"   ✅ {method_name} 存在 / exists")
            else:
                print(f"   ❌ {method_name} 不存在 / does not exist")
                all_methods_exist = False
        
        print()
        
        if all_methods_exist:
            print("=" * 70)
            print("✅ CLI模型管理方法测试通过 / CLI model management methods test passed")
            print("=" * 70)
            print()
            return True
        else:
            print("=" * 70)
            print("❌ 部分方法缺失 / Some methods are missing")
            print("=" * 70)
            print()
            return False
        
    except Exception as e:
        print(f"❌ 测试失败 / Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_menu_integration():
    """
    测试菜单集成 / Test menu integration
    """
    print("=" * 70)
    print("🧪 测试菜单集成 / Test Menu Integration")
    print("=" * 70)
    print()
    
    try:
        from src.cli.main_cli import MainCLI
        
        # 创建CLI实例 / Create CLI instance
        print("1. 创建CLI实例 / Creating CLI instance...")
        cli = MainCLI()
        print("   ✅ 成功 / Success")
        print()
        
        # 检查菜单选项 / Check menu options
        print("2. 检查菜单选项 / Checking menu options...")
        
        if "5" in cli.menu_options:
            option = cli.menu_options["5"]
            print(f"   ✅ 菜单选项 5 存在 / Menu option 5 exists")
            print(f"   名称 / Name: {option['name']}")
            print(f"   描述 / Description: {option['description']}")
            print(f"   处理器 / Handler: {option['handler'].__name__}")
            
            # 验证处理器是否正确 / Verify handler is correct
            if option['handler'].__name__ == "_handle_model_management":
                print("   ✅ 处理器正确 / Handler is correct")
            else:
                print(f"   ❌ 处理器不正确 / Handler is incorrect: {option['handler'].__name__}")
                return False
        else:
            print("   ❌ 菜单选项 5 不存在 / Menu option 5 does not exist")
            return False
        
        print()
        print("=" * 70)
        print("✅ 菜单集成测试通过 / Menu integration test passed")
        print("=" * 70)
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败 / Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """
    运行所有测试 / Run all tests
    """
    print("\n")
    print("=" * 70)
    print("🚀 开始测试模型管理CLI功能 / Starting Model Management CLI Tests")
    print("=" * 70)
    print("\n")
    
    results = []
    
    # 测试1：模型注册表集成 / Test 1: Model registry integration
    results.append(("模型注册表集成 / Model Registry Integration", 
                   test_model_registry_integration()))
    
    # 测试2：CLI模型管理方法 / Test 2: CLI model management methods
    results.append(("CLI模型管理方法 / CLI Model Management Methods", 
                   test_cli_model_management_methods()))
    
    # 测试3：菜单集成 / Test 3: Menu integration
    results.append(("菜单集成 / Menu Integration", 
                   test_menu_integration()))
    
    # 显示测试结果摘要 / Display test results summary
    print("\n")
    print("=" * 70)
    print("📊 测试结果摘要 / Test Results Summary")
    print("=" * 70)
    print()
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ 通过 / PASSED" if result else "❌ 失败 / FAILED"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print()
    print(f"总计 / Total: {len(results)} 个测试 / tests")
    print(f"通过 / Passed: {passed}")
    print(f"失败 / Failed: {failed}")
    print()
    
    if failed == 0:
        print("=" * 70)
        print("🎉 所有测试通过！ / All Tests Passed!")
        print("=" * 70)
        return True
    else:
        print("=" * 70)
        print("⚠️  部分测试失败 / Some Tests Failed")
        print("=" * 70)
        return False


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  测试已中断 / Tests interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试运行失败 / Test execution failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
