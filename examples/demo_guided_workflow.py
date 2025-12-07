#!/usr/bin/env python3
"""
引导式工作流程完整示例 / Complete Guided Workflow Example

本示例展示如何使用引导式工作流程系统完成从市场选择到实盘交易的全部流程
This example demonstrates how to use the guided workflow system to complete 
the entire process from market selection to live trading

功能包括 / Features include:
1. 市场和资产选择 / Market and asset selection
2. 智能推荐资产 / Intelligent asset recommendation
3. 目标收益率设定 / Target return setting
4. 策略优化 / Strategy optimization
5. 模型训练 / Model training
6. 回测验证 / Backtest validation
7. 信号生成和解释 / Signal generation and explanation
8. 模拟交易 / Simulation trading
9. 参数调整 / Parameter adjustment
10. 实盘交易准备 / Live trading preparation

使用方法 / Usage:
    python examples/demo_guided_workflow.py
    
    # 从头开始 / Start from beginning
    python examples/demo_guided_workflow.py --new
    
    # 继续上次的进度 / Resume from last progress
    python examples/demo_guided_workflow.py --resume
"""

import sys
from pathlib import Path
import argparse

# 添加src到路径 / Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cli.guided_workflow import GuidedWorkflow


def print_welcome():
    """
    打印欢迎信息
    Print welcome message
    """
    print("\n" + "="*80)
    print(" "*20 + "引导式工作流程演示")
    print(" "*18 + "Guided Workflow Demo")
    print("="*80)
    
    print("\n欢迎使用量化交易系统引导式工作流程！")
    print("Welcome to the Quantitative Trading System Guided Workflow!")
    
    print("\n本系统将引导您完成以下10个步骤：")
    print("This system will guide you through the following 10 steps:")
    print("-" * 80)
    print("  1. 选择市场和资产类型 / Select market and asset types")
    print("  2. 获取智能推荐 / Get intelligent recommendations")
    print("  3. 设定目标收益率 / Set target return")
    print("  4. 策略优化 / Strategy optimization")
    print("  5. 模型训练 / Model training")
    print("  6. 回测验证 / Backtest validation")
    print("  7. 信号生成和解释 / Signal generation and explanation")
    print("  8. 模拟交易 / Simulation trading")
    print("  9. 参数调整 / Parameter adjustment")
    print(" 10. 实盘交易准备 / Live trading preparation")
    print("-" * 80)
    
    print("\n特点 / Features:")
    print("  ✅ 进度自动保存，可随时中断和恢复")
    print("     Progress auto-saved, can interrupt and resume anytime")
    print("  ✅ 每步都有详细说明和帮助")
    print("     Detailed instructions and help for each step")
    print("  ✅ 支持返回修改之前的选择")
    print("     Support going back to modify previous choices")
    print("  ✅ 智能推荐和参数优化")
    print("     Intelligent recommendations and parameter optimization")
    print("  ✅ 完整的中英双语支持")
    print("     Complete bilingual support (Chinese/English)")
    
    print("\n" + "="*80 + "\n")


def print_tips():
    """
    打印使用提示
    Print usage tips
    """
    print("💡 使用提示 / Usage Tips:")
    print("-" * 80)
    print("• 按 Ctrl+C 可以随时暂停，进度会自动保存")
    print("  Press Ctrl+C to pause anytime, progress will be auto-saved")
    print("• 输入 'back' 可以返回上一步")
    print("  Type 'back' to go back to previous step")
    print("• 输入 'help' 可以查看当前步骤的帮助")
    print("  Type 'help' to view help for current step")
    print("• 输入 'status' 可以查看当前进度")
    print("  Type 'status' to view current progress")
    print("• 输入 'quit' 可以退出（进度会保存）")
    print("  Type 'quit' to exit (progress will be saved)")
    print("-" * 80 + "\n")


def print_completion_summary(workflow):
    """
    打印完成总结
    Print completion summary
    """
    print("\n" + "="*80)
    print(" "*25 + "🎉 工作流程完成！")
    print(" "*23 + "🎉 Workflow Completed!")
    print("="*80)
    
    print("\n恭喜！您已完成所有步骤。")
    print("Congratulations! You have completed all steps.")
    
    print("\n配置总结 / Configuration Summary:")
    print("-" * 80)
    
    # 获取工作流状态 / Get workflow state
    state = workflow.get_state()
    
    if state:
        print(f"市场 / Market: {state.get('market', 'N/A')}")
        print(f"资产类型 / Asset Type: {state.get('asset_type', 'N/A')}")
        print(f"目标收益率 / Target Return: {state.get('target_return', 'N/A')}")
        print(f"风险偏好 / Risk Preference: {state.get('risk_preference', 'N/A')}")
        print(f"模型类型 / Model Type: {state.get('model_type', 'N/A')}")
    
    print("\n生成的文件 / Generated Files:")
    print("-" * 80)
    print("• 配置文件 / Configuration: config/trading_config.yaml")
    print("• 训练模型 / Trained Model: model_registry/")
    print("• 回测报告 / Backtest Report: reports/backtest/")
    print("• 模拟报告 / Simulation Report: reports/simulation/")
    
    print("\n下一步建议 / Next Steps:")
    print("-" * 80)
    print("1. 查看生成的报告和配置")
    print("   Review generated reports and configuration")
    print("2. 如需调整，可以重新运行工作流程")
    print("   Re-run workflow if adjustments needed")
    print("3. 准备好后，可以开始实盘交易")
    print("   When ready, start live trading")
    print("   python examples/live_trading_demo.py")
    
    print("\n相关文档 / Related Documentation:")
    print("-" * 80)
    print("• 引导式工作流程文档: docs/guided_workflow.md")
    print("  Guided workflow documentation: docs/guided_workflow.md")
    print("• 模拟交易指南: docs/simulation_guide.md")
    print("  Simulation trading guide: docs/simulation_guide.md")
    print("• 实盘交易指南: docs/live_trading_guide.md")
    print("  Live trading guide: docs/live_trading_guide.md")
    
    print("\n" + "="*80 + "\n")


def main():
    """
    主函数 / Main function
    """
    # 解析命令行参数 / Parse command line arguments
    parser = argparse.ArgumentParser(
        description='引导式工作流程演示 / Guided Workflow Demo'
    )
    parser.add_argument(
        '--new',
        action='store_true',
        help='从头开始新的工作流程 / Start a new workflow from beginning'
    )
    parser.add_argument(
        '--resume',
        action='store_true',
        help='继续上次的工作流程 / Resume previous workflow'
    )
    parser.add_argument(
        '--state-dir',
        type=str,
        default='./workflow_states',
        help='工作流程状态保存目录 / Workflow state directory'
    )
    
    args = parser.parse_args()
    
    # 打印欢迎信息 / Print welcome message
    print_welcome()
    
    # 打印使用提示 / Print usage tips
    print_tips()
    
    # 确定是否恢复 / Determine whether to resume
    resume = not args.new
    if args.resume:
        resume = True
    
    # 创建工作流实例 / Create workflow instance
    try:
        workflow = GuidedWorkflow(state_dir=args.state_dir)
        
        # 检查是否有保存的进度 / Check if there's saved progress
        if resume and workflow.has_saved_state():
            print("✅ 发现保存的进度，将从上次中断处继续")
            print("✅ Found saved progress, will resume from last interruption")
            print()
        elif resume:
            print("ℹ️  没有发现保存的进度，将从头开始")
            print("ℹ️  No saved progress found, will start from beginning")
            print()
            resume = False
        
        # 启动工作流 / Start workflow
        print("🚀 启动工作流程... / Starting workflow...")
        print()
        
        completed = workflow.start(resume=resume)
        
        # 如果完成，显示总结 / If completed, show summary
        if completed:
            print_completion_summary(workflow)
        else:
            print("\n" + "="*80)
            print("工作流程已暂停 / Workflow paused")
            print("="*80)
            print("\n进度已保存，下次运行时将自动恢复")
            print("Progress saved, will auto-resume on next run")
            print("\n要继续，请再次运行:")
            print("To continue, run again:")
            print(f"  python {sys.argv[0]} --resume")
            print()
        
    except KeyboardInterrupt:
        print("\n\n" + "="*80)
        print("⏸️  工作流程被用户中断 / Workflow interrupted by user")
        print("="*80)
        print("\n进度已自动保存 / Progress auto-saved")
        print("\n要继续，请运行:")
        print("To continue, run:")
        print(f"  python {sys.argv[0]} --resume")
        print()
        
    except Exception as e:
        print("\n\n" + "="*80)
        print("❌ 工作流程执行出错 / Workflow execution error")
        print("="*80)
        print(f"\n错误信息 / Error message: {str(e)}")
        print("\n详细错误 / Detailed error:")
        import traceback
        traceback.print_exc()
        print()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
