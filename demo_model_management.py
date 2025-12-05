#!/usr/bin/env python3
"""
模型管理功能演示脚本 / Model Management Feature Demo Script

This script demonstrates the model management functionality in the CLI.
本脚本演示CLI中的模型管理功能。

Usage / 使用方法:
    python demo_model_management.py
"""

import sys
from pathlib import Path

# 添加src目录到Python路径 / Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.cli.main_cli import MainCLI


def demo_model_management():
    """
    演示模型管理功能 / Demonstrate model management functionality
    """
    print("=" * 70)
    print("🗂️  模型管理功能演示 / Model Management Feature Demo")
    print("=" * 70)
    print()
    print("本演示将展示以下功能 / This demo will showcase the following features:")
    print("  1. 查看模型列表 / View model list")
    print("  2. 查看模型详情 / View model details")
    print("  3. 设置生产模型 / Set production model")
    print("  4. 删除模型 / Delete model")
    print()
    print("注意 / Note:")
    print("  • 需要先训练一些模型才能看到完整功能")
    print("    You need to train some models first to see full functionality")
    print("  • 可以使用 demo_training_cli.py 训练示例模型")
    print("    You can use demo_training_cli.py to train example models")
    print()
    print("=" * 70)
    print()
    
    input("按回车键启动CLI / Press Enter to launch CLI...")
    
    # 创建CLI实例 / Create CLI instance
    cli = MainCLI()
    
    # 直接调用模型管理功能 / Directly call model management function
    cli._handle_model_management()


if __name__ == "__main__":
    try:
        demo_model_management()
    except KeyboardInterrupt:
        print("\n\n👋 演示已退出 / Demo exited")
    except Exception as e:
        print(f"\n❌ 演示失败 / Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()
