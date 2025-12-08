#!/usr/bin/env python
"""
导入验证脚本 / Import Validation Script
验证项目模块是否可以正确导入 / Validates that project modules can be imported correctly
"""

import sys
from pathlib import Path

# 将项目根目录添加到 Python 路径（不是 src 目录）
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def validate_imports():
    """验证关键模块的导入 / Validate imports of key modules"""
    print("开始验证导入... / Starting import validation...")
    
    try:
        # 测试基础设施层导入
        print("\n1. 测试 infrastructure 模块...")
        from src.infrastructure.logger_system import get_logger
        print("   ✓ logger_system 导入成功")
        
        from src.infrastructure.qlib_wrapper import QlibWrapper
        print("   ✓ qlib_wrapper 导入成功")
        
        # 测试核心层导入
        print("\n2. 测试 core 模块...")
        from src.core.data_manager import DataManager
        print("   ✓ data_manager 导入成功")
        
        # 测试工具层导入
        print("\n3. 测试 utils 模块...")
        from src.utils.error_handler import get_error_handler
        print("   ✓ error_handler 导入成功")
        
        from src.utils.memory_monitor import MemoryMonitor
        print("   ✓ memory_monitor 导入成功")
        
        print("\n✓ 所有导入验证成功！/ All imports validated successfully!")
        return True
        
    except ImportError as e:
        print(f"\n✗ 导入失败 / Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = validate_imports()
    sys.exit(0 if success else 1)
