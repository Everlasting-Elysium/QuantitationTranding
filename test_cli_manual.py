#!/usr/bin/env python3
"""
Manual Test Script for CLI
CLI手动测试脚本

This script demonstrates the CLI functionality.
此脚本演示CLI功能。
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cli.main_cli import MainCLI

def test_cli_initialization():
    """Test CLI initialization / 测试CLI初始化"""
    print("=" * 70)
    print("测试 1: CLI 初始化 / Test 1: CLI Initialization")
    print("=" * 70)
    
    try:
        cli = MainCLI()
        print("✅ MainCLI 实例创建成功 / MainCLI instance created successfully")
        print(f"   - 菜单选项数量 / Menu options count: {len(cli.menu_options)}")
        print(f"   - 运行状态 / Running status: {cli.running}")
        return True
    except Exception as e:
        print(f"❌ 初始化失败 / Initialization failed: {e}")
        return False

def test_menu_structure():
    """Test menu structure / 测试菜单结构"""
    print("\n" + "=" * 70)
    print("测试 2: 菜单结构 / Test 2: Menu Structure")
    print("=" * 70)
    
    try:
        cli = MainCLI()
        
        # Check required menu options
        required_options = ["1", "2", "3", "4", "5", "6", "h", "q"]
        missing_options = []
        
        for option in required_options:
            if option not in cli.menu_options:
                missing_options.append(option)
        
        if missing_options:
            print(f"❌ 缺少菜单选项 / Missing menu options: {missing_options}")
            return False
        
        print("✅ 所有必需的菜单选项都存在 / All required menu options exist")
        
        # Display menu options
        print("\n菜单选项 / Menu Options:")
        for key, option in cli.menu_options.items():
            print(f"  {key}: {option['name']}")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败 / Test failed: {e}")
        return False

def test_help_system():
    """Test help system / 测试帮助系统"""
    print("\n" + "=" * 70)
    print("测试 3: 帮助系统 / Test 3: Help System")
    print("=" * 70)
    
    try:
        cli = MainCLI()
        
        # Check if help handler exists
        if "h" not in cli.menu_options:
            print("❌ 帮助选项不存在 / Help option does not exist")
            return False
        
        help_option = cli.menu_options["h"]
        if "handler" not in help_option:
            print("❌ 帮助处理器不存在 / Help handler does not exist")
            return False
        
        print("✅ 帮助系统配置正确 / Help system configured correctly")
        print(f"   - 帮助选项名称 / Help option name: {help_option['name']}")
        print(f"   - 帮助描述 / Help description: {help_option['description']}")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败 / Test failed: {e}")
        return False

def test_feature_handlers():
    """Test feature handlers / 测试功能处理器"""
    print("\n" + "=" * 70)
    print("测试 4: 功能处理器 / Test 4: Feature Handlers")
    print("=" * 70)
    
    try:
        cli = MainCLI()
        
        # Check if all handlers are callable
        handlers_ok = True
        for key, option in cli.menu_options.items():
            if "handler" not in option:
                print(f"❌ 选项 {key} 缺少处理器 / Option {key} missing handler")
                handlers_ok = False
            elif not callable(option["handler"]):
                print(f"❌ 选项 {key} 的处理器不可调用 / Option {key} handler not callable")
                handlers_ok = False
        
        if handlers_ok:
            print("✅ 所有功能处理器都已正确配置 / All feature handlers configured correctly")
            return True
        else:
            return False
    except Exception as e:
        print(f"❌ 测试失败 / Test failed: {e}")
        return False

def main():
    """Run all tests / 运行所有测试"""
    print("\n" + "=" * 70)
    print("🧪 CLI 功能测试 / CLI Functionality Tests")
    print("=" * 70)
    print()
    
    tests = [
        test_cli_initialization,
        test_menu_structure,
        test_help_system,
        test_feature_handlers
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 测试总结 / Test Summary")
    print("=" * 70)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n通过测试 / Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ 所有测试通过！ / All tests passed!")
        print("CLI 已准备就绪 / CLI is ready to use")
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败 / {total - passed} test(s) failed")
    
    print("\n" + "=" * 70)
    print()

if __name__ == "__main__":
    main()
