#!/usr/bin/env python3
"""
实盘交易指南验证脚本 / Live Trading Guide Verification Script

验证实盘交易指南文档的完整性和质量
Verify the completeness and quality of the live trading guide documentation
"""

import os
import sys


def verify_live_trading_guide():
    """
    验证实盘交易指南文档
    Verify live trading guide documentation
    """
    print("=" * 80)
    print("实盘交易指南验证 / Live Trading Guide Verification")
    print("=" * 80)
    
    guide_path = "docs/live_trading_guide.md"
    
    # 检查文件是否存在
    if not os.path.exists(guide_path):
        print(f"❌ 错误：找不到文件 {guide_path}")
        print(f"❌ Error: File {guide_path} not found")
        return False
    
    print(f"✅ 文件存在：{guide_path}")
    print(f"✅ File exists: {guide_path}")
    print()
    
    # 读取文件内容
    with open(guide_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 必需的章节
    required_sections = [
        "# 实盘交易指南",
        "## 概述",
        "## ⚠️ 重要提醒",
        "## 前期准备",
        "## 快速开始",
        "## 实盘交易流程",
        "## 风险控制策略",
        "## 交易执行优化",
        "## 监控和报告",
        "## 常见问题处理",
        "## 最佳实践",
        "## 常见问题"
    ]
    
    print("检查必需章节 / Checking required sections:")
    print("-" * 80)
    
    all_sections_present = True
    for section in required_sections:
        if section in content:
            print(f"✅ {section}")
        else:
            print(f"❌ 缺失：{section}")
            print(f"❌ Missing: {section}")
            all_sections_present = False
    
    print()
    
    # 检查关键内容
    key_contents = {
        "前期准备检查清单": ["策略验证", "技术准备", "资金准备", "知识准备"],
        "实盘交易流程": ["交易前准备", "信号生成", "风险检查", "订单执行", "持仓管理", "交易后处理"],
        "风险控制策略": ["仓位管理", "止损策略", "风险预警系统"],
        "交易执行优化": ["订单类型选择", "大单拆分策略"],
        "监控和报告": ["实时监控面板", "自动报告系统"],
        "常见问题处理": ["技术问题", "交易问题", "风险事件"],
        "最佳实践": ["渐进式启动", "持续监控和优化", "心理管理"]
    }
    
    print("检查关键内容 / Checking key contents:")
    print("-" * 80)
    
    all_contents_present = True
    for category, items in key_contents.items():
        print(f"\n{category}:")
        for item in items:
            if item in content:
                print(f"  ✅ {item}")
            else:
                print(f"  ❌ 缺失：{item}")
                print(f"  ❌ Missing: {item}")
                all_contents_present = False
    
    print()
    
    # 检查代码示例
    code_blocks = content.count("```python")
    print(f"代码示例数量 / Code examples: {code_blocks}")
    if code_blocks >= 20:
        print(f"✅ 包含足够的代码示例（{code_blocks}个）")
        print(f"✅ Contains sufficient code examples ({code_blocks})")
    else:
        print(f"⚠️  代码示例较少（{code_blocks}个），建议至少20个")
        print(f"⚠️  Few code examples ({code_blocks}), recommend at least 20")
    
    print()
    
    # 检查流程图
    flowcharts = content.count("```\n┌")
    print(f"流程图数量 / Flowcharts: {flowcharts}")
    if flowcharts >= 2:
        print(f"✅ 包含流程图（{flowcharts}个）")
        print(f"✅ Contains flowcharts ({flowcharts})")
    else:
        print(f"⚠️  流程图较少（{flowcharts}个）")
        print(f"⚠️  Few flowcharts ({flowcharts})")
    
    print()
    
    # 检查双语支持
    chinese_chars = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
    english_words = len([w for w in content.split() if w.isalpha()])
    
    print(f"中文字符数 / Chinese characters: {chinese_chars}")
    print(f"英文单词数 / English words: {english_words}")
    
    if chinese_chars > 1000 and english_words > 500:
        print("✅ 包含中英双语内容")
        print("✅ Contains bilingual content")
    else:
        print("⚠️  双语内容可能不够完整")
        print("⚠️  Bilingual content may be incomplete")
    
    print()
    
    # 统计信息
    lines = content.split('\n')
    print("文档统计 / Document statistics:")
    print("-" * 80)
    print(f"总行数 / Total lines: {len(lines)}")
    print(f"总字符数 / Total characters: {len(content)}")
    print(f"文件大小 / File size: {os.path.getsize(guide_path)} bytes")
    
    print()
    print("=" * 80)
    
    # 最终结果
    if all_sections_present and all_contents_present:
        print("✅ 验证通过！实盘交易指南文档完整且质量良好。")
        print("✅ Verification passed! Live trading guide is complete and of good quality.")
        return True
    else:
        print("⚠️  验证发现一些问题，请检查上述缺失的内容。")
        print("⚠️  Verification found some issues, please check the missing content above.")
        return False


if __name__ == "__main__":
    success = verify_live_trading_guide()
    sys.exit(0 if success else 1)
