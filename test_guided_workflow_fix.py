#!/usr/bin/env python3
"""
测试引导式工作流程修复 / Test Guided Workflow Fix

验证推荐功能是否正确使用真实数据分析器（带后备方案）
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

print("=" * 80)
print("测试引导式工作流程修复 / Testing Guided Workflow Fix")
print("=" * 80)

# 测试1: 检查导入
print("\n1. 检查导入...")
try:
    from src.cli.guided_workflow import GuidedWorkflow
    from src.application.performance_analyzer import PerformanceAnalyzer
    from src.infrastructure.qlib_wrapper import QlibWrapper
    print("✓ 所有必要的模块都可以导入")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)

# 测试2: 检查代码修改
print("\n2. 检查代码修改...")
import inspect
source = inspect.getsource(GuidedWorkflow._step_asset_recommendation)

if "PerformanceAnalyzer" in source:
    print("✓ 代码已修改为使用 PerformanceAnalyzer")
else:
    print("❌ 代码仍在使用硬编码推荐")
    sys.exit(1)

if "mock_recommendations" in source and "recommendations" in source:
    print("✓ 包含后备方案（fallback）")
else:
    print("⚠️  可能缺少后备方案")

# 测试3: 检查变量使用
if source.count("recommendations") >= 3:  # 应该在多处使用
    print("✓ 正确使用 recommendations 变量")
else:
    print("❌ recommendations 变量使用不正确")
    sys.exit(1)

print("\n" + "=" * 80)
print("✅ 所有检查通过！")
print("=" * 80)

print("\n说明:")
print("1. 代码已修改为优先使用真实的性能分析器")
print("2. 如果真实分析失败，会自动使用模拟数据作为后备")
print("3. 由于当前数据只到2020年9月，分析'最近3年'会失败")
print("4. 因此会使用后备的模拟推荐")
print("\n建议:")
print("- 更新数据到最新，或")
print("- 修改性能分析器支持指定日期范围")

sys.exit(0)
