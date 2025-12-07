"""
Automated Demo: Guided Workflow / 自动化演示：引导式工作流程

This script demonstrates the guided workflow with automated inputs.
本脚本使用自动化输入演示引导式工作流程。

Usage / 使用方法:
    python demo_guided_workflow_auto.py
"""

import sys
from pathlib import Path
from unittest.mock import patch
from io import StringIO

# Add src to path / 添加src到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from cli.guided_workflow import GuidedWorkflow


def simulate_user_inputs():
    """
    Simulate user inputs for the workflow.
    模拟工作流程的用户输入。
    
    Returns a list of inputs that will be provided to the workflow.
    返回将提供给工作流程的输入列表。
    """
    inputs = [
        # Welcome and resume check / 欢迎和恢复检查
        "n",  # Don't resume (start fresh) / 不恢复（重新开始）
        
        # Step 1: Market and Asset Selection / 步骤1：市场和资产选择
        "1",  # Select China Market / 选择中国市场
        "1",  # Select Stocks / 选择股票
        "1",  # Continue / 继续
        
        # Step 2: Asset Recommendation / 步骤2：资产推荐
        "1,2,3",  # Select first 3 assets / 选择前3个资产
        "1",  # Continue / 继续
        
        # Step 3: Target Setting / 步骤3：目标设定
        "20",  # Target return 20% / 目标收益率20%
        "2",  # Moderate risk / 稳健型
        "30",  # 30 days simulation / 30天模拟
        "1",  # Continue / 继续
        
        # Step 4: Strategy Optimization / 步骤4：策略优化
        "y",  # Accept optimization / 接受优化
        "1",  # Continue / 继续
        
        # Step 5: Model Training / 步骤5：模型训练
        "1",  # Continue / 继续
        
        # Step 6: Historical Backtest / 步骤6：历史回测
        "1",  # Continue / 继续
        
        # Step 7: Simulation Trading / 步骤7：模拟交易
        "100000",  # Initial capital 100,000 / 初始资金100,000
        "1",  # Satisfied, start live trading / 满意，开始实盘交易
        "1",  # Continue / 继续
        
        # Step 8: Live Trading Setup / 步骤8：实盘交易设置
        "50000",  # Initial investment 50,000 / 初始投资50,000
        "1",  # Select Huatai Securities / 选择华泰证券
        "2",  # Max daily loss 2% / 单日最大亏损2%
        "40",  # Max position size 40% / 单只股票最大仓位40%
        "5",  # Stop loss 5% / 止损线5%
        "y",  # Confirm configuration / 确认配置
        "1",  # Continue / 继续
        
        # Step 9: Live Trading Execution / 步骤9：实盘交易执行
        "n",  # Don't start live trading (demo only) / 不启动实盘交易（仅演示）
        "1",  # Continue / 继续
        
        # Step 10: Reporting Configuration / 步骤10：报告配置
        "y",  # Enable daily reports / 启用每日报告
        "y",  # Enable weekly reports / 启用每周报告
        "y",  # Enable monthly reports / 启用每月报告
        "demo@example.com",  # Email address / 邮箱地址
        "y",  # Enable risk alerts / 启用风险预警
    ]
    
    return inputs


def run_automated_demo():
    """
    Run the guided workflow with automated inputs.
    使用自动化输入运行引导式工作流程。
    """
    print("\n" + "="*80)
    print("自动化引导式工作流程演示 / Automated Guided Workflow Demo")
    print("="*80)
    print("\n本演示将自动完成所有10个步骤")
    print("This demo will automatically complete all 10 steps")
    print("\n" + "="*80 + "\n")
    
    # Prepare simulated inputs / 准备模拟输入
    inputs = simulate_user_inputs()
    input_iterator = iter(inputs)
    
    def mock_input(prompt=""):
        """Mock input function / 模拟输入函数"""
        try:
            value = next(input_iterator)
            print(f"{prompt}{value}")  # Show what was "entered" / 显示"输入"的内容
            return value
        except StopIteration:
            return ""
    
    # Create workflow instance / 创建工作流实例
    workflow = GuidedWorkflow(state_dir="./demo_workflow_states")
    
    # Run workflow with mocked input / 使用模拟输入运行工作流
    try:
        with patch('builtins.input', side_effect=mock_input):
            workflow.start(resume=False)
        
        print("\n" + "="*80)
        print("✓ 自动化演示完成！/ Automated demo completed!")
        print("="*80)
        print("\n工作流状态已保存到: ./demo_workflow_states/")
        print("Workflow state saved to: ./demo_workflow_states/")
        print("\n您可以查看生成的配置总结文件")
        print("You can view the generated configuration summary file")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n演示过程中出错 / Error during demo: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """Main entry point / 主入口"""
    try:
        run_automated_demo()
    except KeyboardInterrupt:
        print("\n\n演示被用户中断 / Demo interrupted by user")
    except Exception as e:
        print(f"\n\n演示执行出错 / Demo execution error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
