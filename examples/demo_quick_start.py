"""
快速开始示例 / Quick Start Example
最简单的使用示例，适合初学者
The simplest usage example, suitable for beginners

这个示例展示了:
This example demonstrates:
1. 快速初始化系统 / Quick system initialization
2. 使用模板训练模型 / Train model using template
3. 快速回测 / Quick backtest
4. 查看结果 / View results
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径 / Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.data_manager import DataManager
from src.core.model_factory import ModelFactory
from src.infrastructure.qlib_wrapper import QlibWrapper
from src.infrastructure.logger_system import setup_logger
from src.application.training_manager import TrainingManager, DatasetConfig
from src.application.backtest_manager import BacktestManager, BacktestConfig


def main():
    """主函数 / Main function"""
    
    print("=" * 80)
    print("量化交易系统 - 快速开始 / Quantitative Trading System - Quick Start")
    print("=" * 80)
    
    # 1. 初始化系统 / Initialize system
    print("\n[1/4] 初始化系统 / Initializing system...")
    
    setup_logger(log_dir="./logs", log_level="INFO")
    
    qlib_wrapper = QlibWrapper()
    qlib_wrapper.init(
        provider_uri="~/.qlib/qlib_data/cn_data",
        region="cn"
    )
    
    data_manager = DataManager(qlib_wrapper=qlib_wrapper)
    model_factory = ModelFactory()
    
    training_manager = TrainingManager(
        data_manager=data_manager,
        model_factory=model_factory,
        mlflow_tracker=None,
        output_dir="./outputs"
    )
    
    backtest_manager = BacktestManager(
        data_manager=data_manager,
        model_factory=model_factory,
        output_dir="./outputs"
    )
    
    print("✓ 系统初始化完成 / System initialized")
    
    # 2. 使用模板训练模型 / Train model using template
    print("\n[2/4] 训练模型 / Training model...")
    
    # 配置数据集 / Configure dataset
    dataset_config = DatasetConfig(
        instruments="csi300",
        start_time="2020-01-01",
        end_time="2021-12-31",
        features=["$close", "$volume", "$open", "$high", "$low"],
        label="Ref($close, -1) / $close - 1"
    )
    
    # 使用LGBM模板训练 / Train using LGBM template
    training_result = training_manager.train_from_template(
        template_name="lgbm_alpha158",
        dataset_config=dataset_config,
        experiment_name="quick_start"
    )
    
    print(f"✓ 训练完成 / Training completed")
    print(f"  模型ID / Model ID: {training_result.model_id}")
    print(f"  训练时长 / Training time: {training_result.training_time:.2f}秒 / seconds")
    
    # 3. 运行回测 / Run backtest
    print("\n[3/4] 运行回测 / Running backtest...")
    
    backtest_config = BacktestConfig(
        strategy_config={
            "class": "TopkDropoutStrategy",
            "module_path": "qlib.contrib.strategy.signal_strategy",
            "kwargs": {
                "topk": 30,
                "n_drop": 3,
            }
        },
        executor_config={
            "class": "SimulatorExecutor",
            "module_path": "qlib.backtest.executor",
            "kwargs": {
                "time_per_step": "day",
                "generate_portfolio_metrics": True,
            }
        },
        benchmark="SH000300"
    )
    
    backtest_result = backtest_manager.run_backtest(
        model_id=training_result.model_id,
        start_date="2022-01-01",
        end_date="2022-12-31",
        config=backtest_config
    )
    
    print(f"✓ 回测完成 / Backtest completed")
    
    # 4. 显示结果 / Display results
    print("\n[4/4] 回测结果 / Backtest Results")
    print("-" * 80)
    
    metrics = backtest_result.metrics
    print(f"年化收益率 / Annual Return: {metrics.get('annual_return', 0):.2%}")
    print(f"夏普比率 / Sharpe Ratio: {metrics.get('sharpe_ratio', 0):.4f}")
    print(f"最大回撤 / Max Drawdown: {metrics.get('max_drawdown', 0):.2%}")
    print(f"信息比率 / Information Ratio: {metrics.get('information_ratio', 0):.4f}")
    print(f"交易次数 / Number of Trades: {len(backtest_result.trades)}")
    
    print("\n" + "=" * 80)
    print("✓ 快速开始示例完成 / Quick start example completed!")
    print("=" * 80)
    
    print("\n下一步 / Next steps:")
    print("  1. 查看完整示例: python examples/demo_end_to_end.py")
    print("     View complete example: python examples/demo_end_to_end.py")
    print("  2. 查看各功能示例: ls examples/demo_*.py")
    print("     View feature examples: ls examples/demo_*.py")
    print("  3. 阅读文档: docs/quick_start.md")
    print("     Read documentation: docs/quick_start.md")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ 错误 / Error: {str(e)}")
        print("\n请确保:")
        print("Please ensure:")
        print("  1. 已下载数据 / Data is downloaded")
        print("     python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn")
        print("  2. 已安装依赖 / Dependencies are installed")
        print("     pip install -r requirements.txt")
        import traceback
        traceback.print_exc()
