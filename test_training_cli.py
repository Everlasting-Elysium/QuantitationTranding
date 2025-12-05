#!/usr/bin/env python3
"""
测试训练功能CLI / Test Training CLI

This script tests the training CLI functionality.
本脚本测试训练CLI功能。
"""

import sys
from pathlib import Path

# 添加src目录到路径 / Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_training_menu_display():
    """
    测试训练菜单显示 / Test training menu display
    """
    print("=" * 70)
    print("测试1: 训练菜单显示 / Test 1: Training Menu Display")
    print("=" * 70)
    
    try:
        from src.cli.main_cli import MainCLI
        
        cli = MainCLI()
        print("✅ MainCLI 初始化成功 / MainCLI initialized successfully")
        
        # 检查训练处理器是否存在 / Check if training handler exists
        assert hasattr(cli, '_handle_training'), "缺少 _handle_training 方法 / Missing _handle_training method"
        assert hasattr(cli, '_train_from_template'), "缺少 _train_from_template 方法 / Missing _train_from_template method"
        assert hasattr(cli, '_train_with_custom_params'), "缺少 _train_with_custom_params 方法 / Missing _train_with_custom_params method"
        assert hasattr(cli, '_get_training_manager'), "缺少 _get_training_manager 方法 / Missing _get_training_manager method"
        assert hasattr(cli, '_display_training_result'), "缺少 _display_training_result 方法 / Missing _display_training_result method"
        
        print("✅ 所有训练相关方法都存在 / All training-related methods exist")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败 / Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_training_manager_initialization():
    """
    测试训练管理器初始化 / Test training manager initialization
    """
    print("\n" + "=" * 70)
    print("测试2: 训练管理器初始化 / Test 2: Training Manager Initialization")
    print("=" * 70)
    
    try:
        from src.cli.main_cli import MainCLI
        
        cli = MainCLI()
        
        # 检查延迟初始化属性 / Check lazy initialization attributes
        assert cli._training_manager is None, "训练管理器应该延迟初始化 / Training manager should be lazy initialized"
        assert cli._data_manager is None, "数据管理器应该延迟初始化 / Data manager should be lazy initialized"
        assert cli._model_factory is None, "模型工厂应该延迟初始化 / Model factory should be lazy initialized"
        
        print("✅ 延迟初始化属性正确设置 / Lazy initialization attributes correctly set")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败 / Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_template_listing():
    """
    测试模板列表功能 / Test template listing functionality
    """
    print("\n" + "=" * 70)
    print("测试3: 模板列表功能 / Test 3: Template Listing Functionality")
    print("=" * 70)
    
    try:
        from src.core.model_factory import ModelFactory
        
        factory = ModelFactory()
        templates = factory.list_templates()
        
        print(f"找到 {len(templates)} 个模板 / Found {len(templates)} templates")
        
        for template in templates:
            print(f"\n模板 / Template: {template.name}")
            print(f"  类型 / Type: {template.model_type}")
            print(f"  描述 / Description: {template.description}")
            print(f"  适用场景 / Use Case: {template.use_case}")
        
        assert len(templates) > 0, "应该至少有一个模板 / Should have at least one template"
        
        print("\n✅ 模板列表功能正常 / Template listing functionality works")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败 / Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_interactive_prompt():
    """
    测试交互式提示功能 / Test interactive prompt functionality
    """
    print("\n" + "=" * 70)
    print("测试4: 交互式提示功能 / Test 4: Interactive Prompt Functionality")
    print("=" * 70)
    
    try:
        from src.cli.interactive_prompt import InteractivePrompt
        
        prompt = InteractivePrompt()
        
        # 测试各种方法是否存在 / Test if various methods exist
        assert hasattr(prompt, 'ask_text'), "缺少 ask_text 方法 / Missing ask_text method"
        assert hasattr(prompt, 'ask_choice'), "缺少 ask_choice 方法 / Missing ask_choice method"
        assert hasattr(prompt, 'ask_number'), "缺少 ask_number 方法 / Missing ask_number method"
        assert hasattr(prompt, 'ask_date'), "缺少 ask_date 方法 / Missing ask_date method"
        assert hasattr(prompt, 'confirm'), "缺少 confirm 方法 / Missing confirm method"
        assert hasattr(prompt, 'display_message'), "缺少 display_message 方法 / Missing display_message method"
        assert hasattr(prompt, 'display_progress'), "缺少 display_progress 方法 / Missing display_progress method"
        
        print("✅ 所有交互式提示方法都存在 / All interactive prompt methods exist")
        
        # 测试显示消息 / Test display message
        prompt.display_message("这是一条测试消息 / This is a test message", "info")
        prompt.display_message("这是一条成功消息 / This is a success message", "success")
        
        # 测试进度显示 / Test progress display
        for i in range(0, 101, 20):
            prompt.display_progress(i, 100, f"测试进度 / Testing progress")
        
        print("\n✅ 交互式提示功能正常 / Interactive prompt functionality works")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败 / Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """
    运行所有测试 / Run all tests
    """
    print("\n" + "=" * 70)
    print("🧪 训练功能CLI测试套件 / Training CLI Test Suite")
    print("=" * 70)
    print()
    
    tests = [
        ("训练菜单显示 / Training Menu Display", test_training_menu_display),
        ("训练管理器初始化 / Training Manager Initialization", test_training_manager_initialization),
        ("模板列表功能 / Template Listing", test_template_listing),
        ("交互式提示功能 / Interactive Prompt", test_interactive_prompt),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ 测试 '{test_name}' 发生异常 / Test '{test_name}' raised exception: {str(e)}")
            results.append((test_name, False))
    
    # 显示测试总结 / Display test summary
    print("\n" + "=" * 70)
    print("📊 测试总结 / Test Summary")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过 / PASSED" if result else "❌ 失败 / FAILED"
        print(f"{status}: {test_name}")
    
    print("-" * 70)
    print(f"总计 / Total: {passed}/{total} 测试通过 / tests passed")
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
