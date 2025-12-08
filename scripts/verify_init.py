#!/usr/bin/env python3
"""
验证初始化功能 / Verify Initialization Functionality

This script verifies that the initialization system works correctly.
本脚本验证初始化系统是否正常工作。
"""

import sys
import os
from pathlib import Path

# 添加src到路径
sys.path.insert(0, 'src')
sys.path.insert(0, '.')


def test_init_script_import():
    """测试初始化脚本导入 / Test initialization script import"""
    print("=" * 70)
    print("测试 1: 初始化脚本导入 / Test 1: Initialization Script Import")
    print("=" * 70)
    
    try:
        import init_system
        print("✓ 初始化脚本导入成功 / Initialization script imported successfully")
        return True
    except Exception as e:
        print(f"✗ 初始化脚本导入失败 / Failed to import: {e}")
        return False


def test_system_initializer_creation():
    """测试SystemInitializer类创建 / Test SystemInitializer class creation"""
    print("\n" + "=" * 70)
    print("测试 2: SystemInitializer类创建 / Test 2: SystemInitializer Creation")
    print("=" * 70)
    
    try:
        import init_system
        initializer = init_system.SystemInitializer()
        print("✓ SystemInitializer类创建成功 / SystemInitializer created successfully")
        
        # 验证属性
        assert hasattr(initializer, 'project_root')
        assert hasattr(initializer, 'data_dir')
        assert hasattr(initializer, 'config_dir')
        assert hasattr(initializer, 'logs_dir')
        print("✓ 所有必需属性存在 / All required attributes exist")
        
        return True
    except Exception as e:
        print(f"✗ SystemInitializer创建失败 / Failed to create: {e}")
        return False


def test_python_version_check():
    """测试Python版本检查 / Test Python version check"""
    print("\n" + "=" * 70)
    print("测试 3: Python版本检查 / Test 3: Python Version Check")
    print("=" * 70)
    
    try:
        import init_system
        initializer = init_system.SystemInitializer()
        
        result = initializer.check_python_version()
        if result:
            print("✓ Python版本检查通过 / Python version check passed")
            return True
        else:
            print("✗ Python版本不满足要求 / Python version does not meet requirements")
            return False
    except Exception as e:
        print(f"✗ Python版本检查失败 / Failed to check: {e}")
        return False


def test_dependency_check():
    """测试依赖检查 / Test dependency check"""
    print("\n" + "=" * 70)
    print("测试 4: 依赖包检查 / Test 4: Dependency Check")
    print("=" * 70)
    
    try:
        import init_system
        initializer = init_system.SystemInitializer()
        
        installed, missing = initializer.check_dependencies()
        
        print(f"\n统计 / Statistics:")
        print(f"  已安装 / Installed: {len(installed)}")
        print(f"  缺失 / Missing: {len(missing)}")
        
        if missing:
            print(f"\n缺失的包 / Missing packages:")
            for pkg in missing:
                print(f"  - {pkg}")
        
        print("\n✓ 依赖检查功能正常 / Dependency check works correctly")
        return True
    except Exception as e:
        print(f"✗ 依赖检查失败 / Failed to check: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_directory_structure():
    """测试目录结构 / Test directory structure"""
    print("\n" + "=" * 70)
    print("测试 5: 目录结构验证 / Test 5: Directory Structure Validation")
    print("=" * 70)
    
    try:
        import init_system
        initializer = init_system.SystemInitializer()
        
        # 检查关键目录是否定义
        directories = [
            initializer.data_dir,
            initializer.config_dir,
            initializer.logs_dir,
        ]
        
        print("\n关键目录 / Key directories:")
        for directory in directories:
            print(f"  - {directory.relative_to(initializer.project_root)}")
        
        print("\n✓ 目录结构定义正确 / Directory structure defined correctly")
        return True
    except Exception as e:
        print(f"✗ 目录结构验证失败 / Failed to validate: {e}")
        return False


def test_helper_methods():
    """测试辅助方法 / Test helper methods"""
    print("\n" + "=" * 70)
    print("测试 6: 辅助方法 / Test 6: Helper Methods")
    print("=" * 70)
    
    try:
        import init_system
        initializer = init_system.SystemInitializer()
        
        # 测试打印方法
        print("\n测试打印方法 / Testing print methods:")
        initializer.print_success("成功消息测试 / Success message test")
        initializer.print_error("错误消息测试 / Error message test")
        initializer.print_warning("警告消息测试 / Warning message test")
        initializer.print_info("信息消息测试 / Info message test")
        
        # 测试进度条
        print("\n测试进度条 / Testing progress bar:")
        for i in range(1, 6):
            initializer.print_progress(i, 5, f"步骤 {i}/5")
        
        print("\n✓ 辅助方法工作正常 / Helper methods work correctly")
        return True
    except Exception as e:
        print(f"✗ 辅助方法测试失败 / Failed to test: {e}")
        return False


def test_data_check():
    """测试数据检查 / Test data check"""
    print("\n" + "=" * 70)
    print("测试 7: 数据存在性检查 / Test 7: Data Existence Check")
    print("=" * 70)
    
    try:
        import init_system
        initializer = init_system.SystemInitializer()
        
        data_exists = initializer.check_data_exists()
        
        if data_exists:
            print("✓ 发现已有数据 / Found existing data")
        else:
            print("ℹ 未发现数据（这是正常的，如果是首次运行）")
            print("ℹ No data found (this is normal for first run)")
        
        print("✓ 数据检查功能正常 / Data check works correctly")
        return True
    except Exception as e:
        print(f"✗ 数据检查失败 / Failed to check: {e}")
        return False


def main():
    """主测试函数 / Main test function"""
    print("\n" + "=" * 70)
    print("🧪 初始化系统验证测试 / Initialization System Verification Tests")
    print("=" * 70)
    print()
    
    tests = [
        ("初始化脚本导入", test_init_script_import),
        ("SystemInitializer创建", test_system_initializer_creation),
        ("Python版本检查", test_python_version_check),
        ("依赖包检查", test_dependency_check),
        ("目录结构验证", test_directory_structure),
        ("辅助方法", test_helper_methods),
        ("数据检查", test_data_check),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ 测试 '{test_name}' 发生异常: {e}")
            results.append((test_name, False))
    
    # 打印总结
    print("\n" + "=" * 70)
    print("📊 测试总结 / Test Summary")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n通过: {passed}/{total} ({passed/total*100:.1f}%)")
    print(f"Passed: {passed}/{total} ({passed/total*100:.1f}%)")
    print()
    
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {status} - {test_name}")
    
    print("\n" + "=" * 70)
    
    if passed == total:
        print("\n🎉 所有测试通过！初始化系统工作正常。")
        print("🎉 All tests passed! Initialization system works correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} 个测试失败。请检查上述错误。")
        print(f"⚠️  {total - passed} tests failed. Please check errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
