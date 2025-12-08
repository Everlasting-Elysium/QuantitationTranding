"""
回测功能CLI演示 / Backtest CLI Demo

这个脚本演示如何使用回测功能CLI
This script demonstrates how to use the backtest CLI
"""

import sys
import os

# 添加项目根目录到路径 / Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def demo_backtest_menu():
    """
    演示回测菜单 / Demo backtest menu
    """
    print("\n" + "=" * 70)
    print("📈 回测功能CLI演示 / Backtest CLI Demo")
    print("=" * 70)
    print()
    
    print("回测功能提供以下能力 / Backtest features provide the following capabilities:")
    print()
    
    print("1. 模型选择 / Model Selection")
    print("   - 列出所有可用的训练模型")
    print("     List all available trained models")
    print("   - 显示模型的详细信息（类型、训练日期、性能指标）")
    print("     Display model details (type, training date, performance metrics)")
    print("   - 支持选择任意已注册的模型进行回测")
    print("     Support selecting any registered model for backtesting")
    print()
    
    print("2. 回测参数配置 / Backtest Parameter Configuration")
    print("   - 回测时间段：自定义开始和结束日期")
    print("     Backtest period: Custom start and end dates")
    print("   - 股票池选择：支持沪深300、中证500、中证800等")
    print("     Stock pool selection: Support CSI300, CSI500, CSI800, etc.")
    print("   - 策略参数：持仓数量(topk)、调仓卖出数量(n_drop)")
    print("     Strategy parameters: Position size (topk), rebalance drop (n_drop)")
    print("   - 基准指数：可选择基准指数进行对比分析")
    print("     Benchmark index: Optional benchmark for comparison analysis")
    print()
    
    print("3. 回测执行 / Backtest Execution")
    print("   - 加载选定的模型")
    print("     Load selected model")
    print("   - 生成预测信号")
    print("     Generate prediction signals")
    print("   - 模拟交易执行")
    print("     Simulate trade execution")
    print("   - 计算性能指标")
    print("     Calculate performance metrics")
    print()
    
    print("4. 结果展示 / Result Display")
    print("   - 收益指标：总收益率、年化收益率")
    print("     Return metrics: Total return, annual return")
    print("   - 风险指标：波动率、最大回撤")
    print("     Risk metrics: Volatility, max drawdown")
    print("   - 风险调整收益：夏普比率")
    print("     Risk-adjusted return: Sharpe ratio")
    print("   - 交易统计：胜率、交易次数")
    print("     Trading statistics: Win rate, trade count")
    print("   - 基准对比：超额收益、信息比率")
    print("     Benchmark comparison: Excess return, information ratio")
    print()
    
    print("5. 结果保存 / Result Saving")
    print("   - 自动保存回测结果到 outputs/backtests/ 目录")
    print("     Automatically save backtest results to outputs/backtests/ directory")
    print("   - 保存内容包括：")
    print("     Saved content includes:")
    print("     * 性能指标 (metrics.json)")
    print("       Performance metrics (metrics.json)")
    print("     * 收益率序列 (returns.csv)")
    print("       Returns series (returns.csv)")
    print("     * 持仓数据 (positions.csv)")
    print("       Position data (positions.csv)")
    print("     * 交易记录 (trades.csv)")
    print("       Trade records (trades.csv)")
    print("     * 基准收益率 (benchmark_returns.csv)")
    print("       Benchmark returns (benchmark_returns.csv)")
    print()


def demo_usage_workflow():
    """
    演示使用流程 / Demo usage workflow
    """
    print("\n" + "=" * 70)
    print("📋 回测使用流程 / Backtest Usage Workflow")
    print("=" * 70)
    print()
    
    print("步骤 1: 启动系统 / Step 1: Start System")
    print("  $ python main.py")
    print()
    
    print("步骤 2: 选择回测功能 / Step 2: Select Backtest Feature")
    print("  主菜单 / Main Menu:")
    print("  请选择功能 / Please select an option: 2")
    print()
    
    print("步骤 3: 选择回测操作 / Step 3: Select Backtest Operation")
    print("  回测子菜单 / Backtest Submenu:")
    print("  1. 运行新回测 / Run new backtest")
    print("  2. 查看回测结果 / View backtest results")
    print("  3. 返回主菜单 / Return to main menu")
    print("  请选择 / Please select: 1")
    print()
    
    print("步骤 4: 选择模型 / Step 4: Select Model")
    print("  系统会列出所有可用模型，显示：")
    print("  System will list all available models, showing:")
    print("  - 模型名称和版本 / Model name and version")
    print("  - 模型类型 / Model type")
    print("  - 训练日期 / Training date")
    print("  - 性能指标 / Performance metrics")
    print("  - 模型状态 / Model status")
    print()
    
    print("步骤 5: 配置回测参数 / Step 5: Configure Backtest Parameters")
    print("  a) 设置回测时间段 / Set backtest period")
    print("     开始日期 / Start date: 2023-01-01")
    print("     结束日期 / End date: 2023-12-31")
    print()
    print("  b) 选择股票池 / Select stock pool")
    print("     选项 / Options: csi300, csi500, csi800, 自定义 / custom")
    print()
    print("  c) 配置策略参数 / Configure strategy parameters")
    print("     持仓数量 / Position size (topk): 50")
    print("     调仓卖出 / Rebalance drop (n_drop): 5")
    print()
    print("  d) 选择基准指数（可选）/ Select benchmark (optional)")
    print("     选项 / Options: SH000300, SH000905, SH000852, 自定义 / custom")
    print()
    
    print("步骤 6: 确认并执行 / Step 6: Confirm and Execute")
    print("  系统会显示配置总结，确认后开始回测")
    print("  System will display configuration summary, start backtest after confirmation")
    print()
    
    print("步骤 7: 查看结果 / Step 7: View Results")
    print("  回测完成后，系统会显示：")
    print("  After backtest completion, system will display:")
    print("  - 性能指标 / Performance metrics")
    print("  - 交易统计 / Trade statistics")
    print("  - 结果保存位置 / Result save location")
    print()


def demo_example_output():
    """
    演示示例输出 / Demo example output
    """
    print("\n" + "=" * 70)
    print("📊 回测结果示例 / Backtest Result Example")
    print("=" * 70)
    print()
    
    print("✅ 回测完成！ / Backtest Completed!")
    print("=" * 70)
    print()
    print("性能指标 / Performance Metrics:")
    print("-" * 70)
    print("  总收益率 / Total Return: 28.50%")
    print("  年化收益率 / Annual Return: 28.50%")
    print("  波动率 / Volatility: 18.20%")
    print("  最大回撤 / Max Drawdown: -12.30%")
    print("  夏普比率 / Sharpe Ratio: 1.5659")
    print("  胜率 / Win Rate: 62.50%")
    print()
    print("  基准收益率 / Benchmark Return: 15.20%")
    print("  超额收益 / Excess Return: 13.30%")
    print("  信息比率 / Information Ratio: 0.8234")
    print()
    print("  回测时长 / Backtest Time: 45.23 秒 / seconds")
    print("-" * 70)
    print()
    print("交易统计 / Trade Statistics:")
    print("  总交易次数 / Total Trades: 156")
    print()
    print("=" * 70)
    print("💡 提示 / Tips:")
    print("  • 回测结果已保存到 outputs/backtests/ 目录")
    print("    Backtest results saved to outputs/backtests/ directory")
    print("  • 可以在主菜单选择 '报告查看' 查看详细报告")
    print("    You can select 'View Reports' in main menu for detailed reports")
    print("=" * 70)


def demo_integration_with_training():
    """
    演示与训练功能的集成 / Demo integration with training
    """
    print("\n" + "=" * 70)
    print("🔗 与训练功能的集成 / Integration with Training")
    print("=" * 70)
    print()
    
    print("完整的工作流程 / Complete Workflow:")
    print()
    
    print("1️⃣  模型训练 / Model Training")
    print("   - 使用训练功能训练预测模型")
    print("     Use training feature to train prediction models")
    print("   - 模型自动注册到模型注册表")
    print("     Models automatically registered to model registry")
    print("   - 记录模型元数据和性能指标")
    print("     Record model metadata and performance metrics")
    print()
    
    print("2️⃣  历史回测 / Historical Backtest")
    print("   - 从模型注册表选择训练好的模型")
    print("     Select trained model from model registry")
    print("   - 在历史数据上验证模型表现")
    print("     Validate model performance on historical data")
    print("   - 评估策略的实际效果")
    print("     Evaluate actual strategy effectiveness")
    print()
    
    print("3️⃣  结果对比 / Result Comparison")
    print("   - 对比训练指标和回测指标")
    print("     Compare training metrics and backtest metrics")
    print("   - 识别过拟合或欠拟合")
    print("     Identify overfitting or underfitting")
    print("   - 优化模型和策略参数")
    print("     Optimize model and strategy parameters")
    print()
    
    print("4️⃣  迭代改进 / Iterative Improvement")
    print("   - 根据回测结果调整训练参数")
    print("     Adjust training parameters based on backtest results")
    print("   - 重新训练模型")
    print("     Retrain models")
    print("   - 再次回测验证")
    print("     Backtest again for validation")
    print()


def main():
    """
    主演示函数 / Main demo function
    """
    print("\n" + "=" * 70)
    print("🎯 回测功能CLI完整演示 / Complete Backtest CLI Demo")
    print("=" * 70)
    
    # 演示回测菜单 / Demo backtest menu
    demo_backtest_menu()
    
    # 演示使用流程 / Demo usage workflow
    demo_usage_workflow()
    
    # 演示示例输出 / Demo example output
    demo_example_output()
    
    # 演示与训练功能的集成 / Demo integration with training
    demo_integration_with_training()
    
    print("\n" + "=" * 70)
    print("📚 更多信息 / More Information")
    print("=" * 70)
    print()
    print("文档位置 / Documentation Location:")
    print("  - docs/cli_usage.md - CLI使用指南 / CLI Usage Guide")
    print("  - docs/backtest_manager.md - 回测管理器文档 / Backtest Manager Documentation")
    print()
    print("示例代码 / Example Code:")
    print("  - examples/demo_backtest_manager.py - 回测管理器示例")
    print("    Backtest Manager Example")
    print()
    print("测试代码 / Test Code:")
    print("  - test_backtest_cli.py - 回测CLI测试")
    print("    Backtest CLI Test")
    print()
    print("=" * 70)
    print()
    print("💡 提示 / Tips:")
    print("  要实际运行回测功能，请执行：")
    print("  To actually run backtest feature, execute:")
    print("  $ python main.py")
    print("  然后选择选项 2 (历史回测 / Historical Backtest)")
    print("  Then select option 2 (Historical Backtest)")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
