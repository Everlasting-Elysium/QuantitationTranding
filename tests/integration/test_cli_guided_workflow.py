"""
Test: CLI Guided Workflow Integration / 测试：CLI引导式工作流程集成

This script tests the integration of guided workflow into the main CLI.
本脚本测试引导式工作流程与主CLI的集成。
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path / 添加src到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from cli.main_cli import MainCLI


def test_menu_has_guided_workflow():
    """Test that menu includes guided workflow option / 测试菜单包含引导式工作流程选项"""
    print("测试菜单包含引导式工作流程选项 / Testing menu includes guided workflow option...")
    
    cli = MainCLI()
    
    # Check that option "0" exists / 检查选项"0"存在
    assert "0" in cli.menu_options, "Menu should have option '0' for guided workflow"
    
    # Check option details / 检查选项详情
    option = cli.menu_options["0"]
    assert "引导式工作流程" in option["name"] or "Guided Workflow" in option["name"]
    assert option["handler"] == cli._handle_guided_workflow
    assert "highlight" in option and option["highlight"] is True
    
    print("✓ 菜单包含引导式工作流程选项 / Menu includes guided workflow option")
    return True


def test_guided_workflow_handler_exists():
    """Test that guided workflow handler exists / 测试引导式工作流程处理器存在"""
    print("\n测试引导式工作流程处理器存在 / Testing guided workflow handler exists...")
    
    cli = MainCLI()
    
    # Check that handler method exists / 检查处理器方法存在
    assert hasattr(cli, '_handle_guided_workflow'), "CLI should have _handle_guided_workflow method"
    assert callable(cli._handle_guided_workflow), "_handle_guided_workflow should be callable"
    
    print("✓ 引导式工作流程处理器存在 / Guided workflow handler exists")
    return True


def test_menu_display():
    """Test menu display includes guided workflow / 测试菜单显示包含引导式工作流程"""
    print("\n测试菜单显示 / Testing menu display...")
    
    cli = MainCLI()
    
    # Capture menu output / 捕获菜单输出
    from io import StringIO
    import sys
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        cli.show_menu()
        menu_output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    
    # Check menu output contains guided workflow / 检查菜单输出包含引导式工作流程
    assert "引导式工作流程" in menu_output or "Guided Workflow" in menu_output
    assert "⭐" in menu_output  # Should have star highlighting
    
    print("✓ 菜单显示包含引导式工作流程 / Menu display includes guided workflow")
    print(f"  菜单输出长度 / Menu output length: {len(menu_output)} characters")
    return True


def test_welcome_message():
    """Test welcome message mentions guided workflow / 测试欢迎消息提到引导式工作流程"""
    print("\n测试欢迎消息 / Testing welcome message...")
    
    cli = MainCLI()
    
    # Capture welcome output / 捕获欢迎输出
    from io import StringIO
    import sys
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        cli._show_welcome()
        welcome_output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    
    # Check welcome output mentions guided workflow / 检查欢迎输出提到引导式工作流程
    assert "引导式工作流程" in welcome_output or "Guided Workflow" in welcome_output
    assert "新功能" in welcome_output or "New Feature" in welcome_output
    
    print("✓ 欢迎消息提到引导式工作流程 / Welcome message mentions guided workflow")
    return True


def test_help_message():
    """Test help message includes guided workflow / 测试帮助消息包含引导式工作流程"""
    print("\n测试帮助消息 / Testing help message...")
    
    cli = MainCLI()
    
    # Capture help output / 捕获帮助输出
    from io import StringIO
    import sys
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    # Mock input to skip "Press Enter" prompt / 模拟输入以跳过"按回车"提示
    with patch('builtins.input', return_value=''):
        try:
            cli._show_help()
            help_output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout
    
    # Check help output mentions guided workflow / 检查帮助输出提到引导式工作流程
    assert "引导式工作流程" in help_output or "Guided Workflow" in help_output
    
    print("✓ 帮助消息包含引导式工作流程 / Help message includes guided workflow")
    return True


def test_guided_workflow_handler_callable():
    """Test that guided workflow handler can be called / 测试引导式工作流程处理器可调用"""
    print("\n测试引导式工作流程处理器可调用 / Testing guided workflow handler callable...")
    
    cli = MainCLI()
    
    # Mock the prompt to decline starting workflow / 模拟提示以拒绝启动工作流
    with patch.object(cli.prompt, 'confirm', return_value=False):
        with patch('builtins.print'):  # Suppress output
            try:
                cli._handle_guided_workflow()
                print("✓ 引导式工作流程处理器可调用 / Guided workflow handler callable")
                return True
            except Exception as e:
                print(f"✗ 调用失败 / Call failed: {str(e)}")
                return False


def test_integration_with_guided_workflow_class():
    """Test integration with GuidedWorkflow class / 测试与GuidedWorkflow类的集成"""
    print("\n测试与GuidedWorkflow类的集成 / Testing integration with GuidedWorkflow class...")
    
    try:
        # Try to import GuidedWorkflow / 尝试导入GuidedWorkflow
        from cli.guided_workflow import GuidedWorkflow
        
        # Check that GuidedWorkflow can be instantiated / 检查GuidedWorkflow可以实例化
        workflow = GuidedWorkflow(state_dir="./test_workflow_states")
        assert workflow is not None
        assert hasattr(workflow, 'start')
        assert callable(workflow.start)
        
        print("✓ 与GuidedWorkflow类集成成功 / Integration with GuidedWorkflow class successful")
        
        # Cleanup / 清理
        import shutil
        test_dir = Path("./test_workflow_states")
        if test_dir.exists():
            shutil.rmtree(test_dir)
        
        return True
    except Exception as e:
        print(f"✗ 集成失败 / Integration failed: {str(e)}")
        return False


def main():
    """Run all tests / 运行所有测试"""
    print("="*80)
    print("CLI引导式工作流程集成测试 / CLI Guided Workflow Integration Tests")
    print("="*80)
    
    tests = [
        test_menu_has_guided_workflow,
        test_guided_workflow_handler_exists,
        test_menu_display,
        test_welcome_message,
        test_help_message,
        test_guided_workflow_handler_callable,
        test_integration_with_guided_workflow_class
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ 测试失败 / Test failed: {test.__name__}")
            print(f"  错误 / Error: {str(e)}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*80)
    print(f"测试结果 / Test Results: {passed} 通过 / passed, {failed} 失败 / failed")
    print("="*80)
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
