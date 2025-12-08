#!/usr/bin/env python3
"""
信号生成CLI演示脚本 / Signal Generation CLI Demo Script

演示如何使用CLI生成交易信号
Demonstrates how to use CLI to generate trading signals
"""

import sys
from pathlib import Path

# 添加src目录到路径 / Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.cli.main_cli import MainCLI


def main():
    """
    运行信号生成CLI演示 / Run signal generation CLI demo
    """
    print("=" * 70)
    print("信号生成CLI演示 / Signal Generation CLI Demo")
    print("=" * 70)
    print()
    print("本演示将启动主CLI界面，您可以选择 '信号生成' 功能进行测试")
    print("This demo will launch the main CLI, you can select 'Signal Generation' to test")
    print()
    print("提示 / Tips:")
    print("  1. 确保已经训练了至少一个模型")
    print("     Make sure you have trained at least one model")
    print("  2. 确保qlib数据已经下载")
    print("     Make sure qlib data is downloaded")
    print("  3. 选择菜单选项 '3' 进入信号生成功能")
    print("     Select menu option '3' to enter signal generation")
    print()
    input("按回车键继续 / Press Enter to continue...")
    
    # 启动主CLI / Launch main CLI
    cli = MainCLI()
    cli.run()


if __name__ == "__main__":
    main()
