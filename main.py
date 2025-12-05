#!/usr/bin/env python3
"""
Main Entry Point for Quantitative Trading System
量化交易系统主入口

This script launches the main CLI interface.
此脚本启动主CLI界面。
"""

import sys
import os

# Add src directory to Python path
# 将src目录添加到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cli.main_cli import main

if __name__ == "__main__":
    main()
