"""
Interactive Prompt Demo / 交互式提示演示

This script demonstrates the usage of InteractivePrompt class.
本脚本演示InteractivePrompt类的使用。
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.cli.interactive_prompt import InteractivePrompt


def demo_text_input():
    """Demonstrate text input / 演示文本输入"""
    print("\n" + "="*60)
    print("Demo 1: Text Input / 演示1：文本输入")
    print("="*60)
    
    prompt = InteractivePrompt()
    
    # Ask for name with default
    name = prompt.ask_text("请输入您的姓名 / Enter your name", default="张三")
    print(f"✅ 您输入的姓名是: {name}")
    
    # Ask for description without default
    description = prompt.ask_text("请输入描述 / Enter description", allow_empty=True)
    print(f"✅ 您输入的描述是: {description if description else '(空)'}")


def demo_choice_input():
    """Demonstrate choice input / 演示选择输入"""
    print("\n" + "="*60)
    print("Demo 2: Choice Input / 演示2：选择输入")
    print("="*60)
    
    prompt = InteractivePrompt()
    
    # Ask for market selection
    markets = ["中国市场 (A股)", "美国市场", "香港市场"]
    market = prompt.ask_choice("请选择投资市场 / Select investment market", markets, default=1)
    print(f"✅ 您选择的市场是: {market}")
    
    # Ask for asset type
    asset_types = ["股票", "基金", "ETF"]
    asset_type = prompt.ask_choice("请选择投资品类 / Select asset type", asset_types)
    print(f"✅ 您选择的品类是: {asset_type}")


def demo_number_input():
    """Demonstrate number input / 演示数字输入"""
    print("\n" + "="*60)
    print("Demo 3: Number Input / 演示3：数字输入")
    print("="*60)
    
    prompt = InteractivePrompt()
    
    # Ask for target return
    target_return = prompt.ask_number(
        "请输入期望年化收益率 (%) / Enter target annual return (%)",
        min_val=0,
        max_val=100,
        default=20.0
    )
    print(f"✅ 您输入的目标收益率是: {target_return}%")
    
    # Ask for simulation days
    simulation_days = prompt.ask_integer(
        "请输入模拟交易天数 / Enter simulation days",
        min_val=1,
        max_val=365,
        default=30
    )
    print(f"✅ 您输入的模拟天数是: {simulation_days}天")


def demo_date_input():
    """Demonstrate date input / 演示日期输入"""
    print("\n" + "="*60)
    print("Demo 4: Date Input / 演示4：日期输入")
    print("="*60)
    
    prompt = InteractivePrompt()
    
    # Ask for start date
    start_date = prompt.ask_date(
        "请输入开始日期 / Enter start date",
        default="2024-01-01"
    )
    print(f"✅ 您输入的开始日期是: {start_date}")
    
    # Ask for end date
    end_date = prompt.ask_date(
        "请输入结束日期 / Enter end date",
        default="2024-12-31"
    )
    print(f"✅ 您输入的结束日期是: {end_date}")


def demo_confirmation():
    """Demonstrate confirmation / 演示确认"""
    print("\n" + "="*60)
    print("Demo 5: Confirmation / 演示5：确认")
    print("="*60)
    
    prompt = InteractivePrompt()
    
    # Ask for confirmation with default yes
    confirmed = prompt.confirm("是否继续执行 / Continue?", default=True)
    if confirmed:
        print("✅ 用户确认继续")
    else:
        print("❌ 用户取消操作")
    
    # Ask for confirmation with default no
    delete_confirmed = prompt.confirm("是否删除数据 / Delete data?", default=False)
    if delete_confirmed:
        print("✅ 用户确认删除")
    else:
        print("❌ 用户取消删除")


def demo_messages():
    """Demonstrate message display / 演示消息显示"""
    print("\n" + "="*60)
    print("Demo 6: Message Display / 演示6：消息显示")
    print("="*60)
    
    prompt = InteractivePrompt()
    
    prompt.display_message("这是一条信息消息 / This is an info message", "info")
    prompt.display_message("操作成功完成 / Operation completed successfully", "success")
    prompt.display_message("请注意风险 / Please be aware of risks", "warning")
    prompt.display_message("发生错误 / An error occurred", "error")


def demo_progress():
    """Demonstrate progress display / 演示进度显示"""
    print("\n" + "="*60)
    print("Demo 7: Progress Display / 演示7：进度显示")
    print("="*60)
    
    prompt = InteractivePrompt()
    
    import time
    
    total_steps = 10
    for i in range(total_steps + 1):
        prompt.display_progress(i, total_steps, f"处理中... / Processing...")
        time.sleep(0.3)
    
    print("✅ 进度完成 / Progress completed")


def demo_complete_workflow():
    """Demonstrate a complete workflow / 演示完整工作流程"""
    print("\n" + "="*60)
    print("Demo 8: Complete Workflow / 演示8：完整工作流程")
    print("="*60)
    
    prompt = InteractivePrompt()
    
    prompt.display_message("欢迎使用量化交易系统 / Welcome to Quantitative Trading System", "info")
    
    # Step 1: Market selection
    markets = ["中国市场 (A股)", "美国市场", "香港市场"]
    market = prompt.ask_choice("步骤1: 选择市场 / Step 1: Select market", markets, default=1)
    
    # Step 2: Asset type selection
    asset_types = ["股票", "基金", "ETF"]
    asset_type = prompt.ask_choice("步骤2: 选择品类 / Step 2: Select asset type", asset_types)
    
    # Step 3: Target return
    target_return = prompt.ask_number(
        "步骤3: 输入目标收益率 (%) / Step 3: Enter target return (%)",
        min_val=0,
        max_val=100,
        default=20.0
    )
    
    # Step 4: Risk preference
    risk_levels = ["保守型 (低风险)", "稳健型 (中等风险)", "进取型 (高风险)"]
    risk_level = prompt.ask_choice("步骤4: 选择风险偏好 / Step 4: Select risk preference", risk_levels, default=2)
    
    # Step 5: Simulation period
    simulation_days = prompt.ask_integer(
        "步骤5: 输入模拟天数 / Step 5: Enter simulation days",
        min_val=1,
        max_val=365,
        default=30
    )
    
    # Summary
    print("\n" + "="*60)
    print("配置总结 / Configuration Summary")
    print("="*60)
    print(f"市场 / Market: {market}")
    print(f"品类 / Asset Type: {asset_type}")
    print(f"目标收益率 / Target Return: {target_return}%")
    print(f"风险偏好 / Risk Preference: {risk_level}")
    print(f"模拟天数 / Simulation Days: {simulation_days}")
    print("="*60)
    
    # Confirmation
    confirmed = prompt.confirm("\n确认以上配置并开始训练 / Confirm configuration and start training?", default=True)
    
    if confirmed:
        prompt.display_message("配置已确认，开始训练... / Configuration confirmed, starting training...", "success")
        
        # Simulate training progress
        import time
        for i in range(11):
            prompt.display_progress(i, 10, "训练中... / Training...")
            time.sleep(0.2)
        
        prompt.display_message("训练完成！/ Training completed!", "success")
    else:
        prompt.display_message("配置已取消 / Configuration cancelled", "warning")


def main():
    """Main function / 主函数"""
    print("\n" + "="*60)
    print("Interactive Prompt System Demo")
    print("交互式提示系统演示")
    print("="*60)
    
    demos = [
        ("文本输入 / Text Input", demo_text_input),
        ("选择输入 / Choice Input", demo_choice_input),
        ("数字输入 / Number Input", demo_number_input),
        ("日期输入 / Date Input", demo_date_input),
        ("确认提示 / Confirmation", demo_confirmation),
        ("消息显示 / Message Display", demo_messages),
        ("进度显示 / Progress Display", demo_progress),
        ("完整工作流程 / Complete Workflow", demo_complete_workflow),
        ("退出 / Exit", None)
    ]
    
    prompt = InteractivePrompt()
    
    while True:
        print("\n" + "="*60)
        print("请选择要运行的演示 / Select demo to run:")
        print("="*60)
        
        choices = [name for name, _ in demos]
        choice = prompt.ask_choice("选择演示 / Select demo", choices)
        
        # Find the selected demo
        for name, demo_func in demos:
            if name == choice:
                if demo_func is None:
                    print("\n再见！/ Goodbye!")
                    return
                demo_func()
                break
        
        # Ask if user wants to continue
        if not prompt.confirm("\n是否继续运行其他演示 / Run another demo?", default=True):
            print("\n再见！/ Goodbye!")
            break


if __name__ == "__main__":
    main()
