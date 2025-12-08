#!/usr/bin/env python3
"""
测试主程序交互 / Test main program interaction
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.cli.interactive_prompt import InteractivePrompt

# 测试InteractivePrompt
prompt = InteractivePrompt()

print("测试 InteractivePrompt.confirm() 方法")
print("=" * 50)

# 模拟用户输入
import io
from unittest.mock import patch

# 测试1: 用户输入 'y'
with patch('builtins.input', return_value='y'):
    result = prompt.confirm("是否继续？", default=True)
    print(f"测试1 - 输入'y': {result}")
    assert result == True, "应该返回True"

# 测试2: 用户输入 'n'
with patch('builtins.input', return_value='n'):
    result = prompt.confirm("是否继续？", default=True)
    print(f"测试2 - 输入'n': {result}")
    assert result == False, "应该返回False"

# 测试3: 用户输入空（使用默认值）
with patch('builtins.input', return_value=''):
    result = prompt.confirm("是否继续？", default=True)
    print(f"测试3 - 输入空（默认True）: {result}")
    assert result == True, "应该返回True（默认值）"

print("\n✅ 所有测试通过！")
print("InteractivePrompt 工作正常")
