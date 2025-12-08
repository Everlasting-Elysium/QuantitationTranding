"""
Demo: Main CLI with Guided Workflow / 演示：带引导式工作流程的主CLI

This script demonstrates the main CLI with integrated guided workflow.
本脚本演示集成了引导式工作流程的主CLI。

Usage / 使用方法:
    python demo_cli_with_guided_workflow.py
"""

import sys
from pathlib import Path
from unittest.mock import patch

# Add src to path / 添加src到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from cli.main_cli import MainCLI


def demo_menu_display():
    """
    Demonstrate the menu display with guided workflow.
    演示带引导式工作流程的菜单显示。
    """
    print("\n" + "="*80)
    print("演示：主菜单显示 / Demo: Main Menu Display")
    print("="*80)
    
    cli = MainCLI()
    
    # Show welcome message / 显示欢迎消息
    cli._show_welcome()
    
    # Show menu / 显示菜单
    cli.show_menu()
    
    print("\n注意：引导式工作流程选项（选项0）被突出显示")
    print("Note: Guided workflow option (option 0) is highlighted")
    print("="*80)


def demo_guided_workflow_info():
    """
    Demonstrate the guided workflow information display.
    演示引导式工作流程信息显示。
    """
    print("\n" + "="*80)
    print("演示：引导式工作流程信息 / Demo: Guided Workflow Information")
    print("="*80)
    
    cli = MainCLI()
    
    # Mock user declining to start workflow / 模拟用户拒绝启动工作流
    with patch.object(cli.prompt, 'confirm', return_value=False):
        with patch('builtins.input', return_value=''):  # Mock Enter key
            cli._handle_guided_workflow()
    
    print("\n这展示了当用户选择引导式工作流程时看到的信息")
    print("This shows the information users see when selecting guided workflow")
    print("="*80)


def demo_help_with_guided_workflow():
    """
    Demonstrate the help message with guided workflow.
    演示带引导式工作流程的帮助消息。
    """
    print("\n" + "="*80)
    print("演示：帮助信息 / Demo: Help Information")
    print("="*80)
    
    cli = MainCLI()
    
    # Mock input to skip "Press Enter" prompt / 模拟输入以跳过"按回车"提示
    with patch('builtins.input', return_value=''):
        cli._show_help()
    
    print("\n帮助信息现在包含了引导式工作流程的说明")
    print("Help information now includes guided workflow description")
    print("="*80)


def demo_interactive_selection():
    """
    Demonstrate interactive menu selection (simulated).
    演示交互式菜单选择（模拟）。
    """
    print("\n" + "="*80)
    print("演示：交互式菜单选择（模拟）/ Demo: Interactive Menu Selection (Simulated)")
    print("="*80)
    print()
    
    print("用户可以通过以下方式访问引导式工作流程：")
    print("Users can access guided workflow by:")
    print()
    print("1. 启动主CLI / Start main CLI:")
    print("   $ python main.py")
    print()
    print("2. 在主菜单中输入 '0' / Enter '0' in main menu:")
    print("   请选择功能 / Please select an option: 0")
    print()
    print("3. 系统将显示引导式工作流程介绍并询问是否开始")
    print("   System will show guided workflow introduction and ask to start")
    print()
    print("4. 确认后，系统将启动10步完整流程")
    print("   After confirmation, system will start 10-step complete workflow")
    print()
    print("5. 用户可以随时暂停、返回修改或退出")
    print("   Users can pause, go back to modify, or quit anytime")
    print()
    print("="*80)


def main():
    """Main demo function / 主演示函数"""
    print("\n" + "="*80)
    print("主CLI与引导式工作流程集成演示")
    print("Main CLI with Guided Workflow Integration Demo")
    print("="*80)
    
    demos = [
        ("菜单显示 / Menu Display", demo_menu_display),
        ("引导式工作流程信息 / Guided Workflow Info", demo_guided_workflow_info),
        ("帮助信息 / Help Information", demo_help_with_guided_workflow),
        ("交互式选择 / Interactive Selection", demo_interactive_selection)
    ]
    
    for i, (name, demo_func) in enumerate(demos, 1):
        print(f"\n{'='*80}")
        print(f"演示 {i}/{len(demos)}: {name}")
        print(f"Demo {i}/{len(demos)}: {name}")
        print(f"{'='*80}")
        
        try:
            demo_func()
        except Exception as e:
            print(f"\n❌ 演示失败 / Demo failed: {str(e)}")
            import traceback
            traceback.print_exc()
        
        if i < len(demos):
            input("\n按回车键继续下一个演示 / Press Enter to continue to next demo...")
    
    print("\n" + "="*80)
    print("✅ 所有演示完成！ / All demos completed!")
    print("="*80)
    print()
    print("要实际使用引导式工作流程，请运行：")
    print("To actually use guided workflow, run:")
    print("  python main.py")
    print()
    print("然后选择选项 0")
    print("Then select option 0")
    print()
    print("="*80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n演示被用户中断 / Demo interrupted by user")
    except Exception as e:
        print(f"\n\n演示执行出错 / Demo execution error: {str(e)}")
        import traceback
        traceback.print_exc()
