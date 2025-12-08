#!/usr/bin/env python3
"""
Main Entry Point for Quantitative Trading System
量化交易系统主入口

This script launches the main CLI interface.
此脚本启动主CLI界面。
"""

import sys
import os

# Add project root to Python path to enable proper package imports
# 将项目根目录添加到Python路径以启用正确的包导入
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.cli.main_cli import main

if __name__ == "__main__":
    main()
