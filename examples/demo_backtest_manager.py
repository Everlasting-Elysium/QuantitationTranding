"""
回测管理器演示脚本 / Backtest Manager Demo Script

演示如何使用BacktestManager进行模型回测
Demonstrates how to use BacktestManager for model backtesting
"""

import sys
from pathlib import Path

# 添加项目根目录到路径 / Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.application.backtest_manager import BacktestManager, BacktestConfig
from src.infrastructure.qlib_wrapper import QlibWrapper
from src.infrastructure.logger_system import setup_logging


def main():
    """主函数 / Main function"""
    
    # 1. 设置日志 / Setup logging
    print("=" * 80)
    print("回测管理器演示 / Backtest Manager Demo")
    print("=" * 80)
    
    setup_logging(log_dir="./logs", log_level="INFO")
    
    # 2. 初始化Qlib / Initialize Qlib
    print("\n步骤 1: 初始化Qlib / Step 1: Initialize Qlib")
    print("-" * 80)
    
    qlib_wrapper = QlibWrapper()
    
    try:
        qlib_wrapper.init(
            provider_uri="~/.qlib/qlib_data/cn_data",
            region="cn"
        )
        print("✓ Qlib初始化成功 / Qlib initialized successfully")
    except Exception as e:
        print(f"✗ Qlib初始化失败 / Qlib initialization failed: {str(e)}")
        print("\n提示 / Hint:")
        print("请先运行 python scripts/get_data.py 下载数据")
        print("Please run 'python scripts/get_data.py' to download data first")
        return
    
    # 3. 创建回测管理器 / Create backtest manager
    print("\n步骤 2: 创建回测管理器 / Step 2: Create Backtest Manager")
    print("-" * 80)
    
    backtest_manager = BacktestManager(
        qlib_wrapper=qlib_wrapper,
        output_dir="./outputs/backtests"
    )
    print("✓ 回测管理器创建成功 / Backtest manager created successfully")
    
    # 4. 配置回测参数 / Configure backtest parameters
    print("\n步骤 3: 配置回测参数 / Step 3: Configure Backtest Parameters")
    print("-" * 80)
    
    config = BacktestConfig(
        strategy_config={
            "instruments": "csi300",  # 使用沪深300成分股 / Use CSI300 constituents
            "topk": 50,               # 持仓前50只股票 / Hold top 50 stocks
            "n_drop": 5,              # 每次调仓卖出5只 / Drop 5 stocks per rebalance
        },
        executor_config={
            "time_per_step": "day",   # 每日调仓 / Daily rebalancing
        },
        benchmark="SH000300"          # 使用沪深300作为基准 / Use CSI300 as benchmark
    )
    
    print(f"策略配置 / Strategy config:")
    print(f"  - 股票池 / Instruments: {config.strategy_config['instruments']}")
    print(f"  - 持仓数量 / Top K: {config.strategy_config['topk']}")
    print(f"  - 调仓频率 / Rebalance: {config.executor_config['time_per_step']}")
    print(f"  - 基准指数 / Benchmark: {config.benchmark}")
    
    # 5. 演示指标计算功能 / Demonstrate metrics calculation
    print("\n步骤 4: 演示指标计算功能 / Step 4: Demonstrate Metrics Calculation")
    print("-" * 80)
    
    import pandas as pd
    import numpy as np
    
    # 创建模拟收益率数据 / Create mock returns data
    dates = pd.date_range(start='2023-01-01', periods=252, freq='D')
    returns = pd.Series(
        np.random.normal(0.001, 0.02, 252),  # 平均日收益0.1%，波动率2%
        index=dates
    )
    
    # 创建模拟基准数据 / Create mock benchmark data
    benchmark = pd.Series(
        np.random.normal(0.0005, 0.015, 252),  # 平均日收益0.05%，波动率1.5%
        index=dates
    )
    
    print("计算性能指标 / Calculating performance metrics...")
    metrics = backtest_manager.calculate_metrics(returns, benchmark)
    
    print("\n性能指标 / Performance Metrics:")
    print(f"  - 总收益率 / Total Return: {metrics['total_return']:.2%}")
    print(f"  - 年化收益率 / Annual Return: {metrics['annual_return']:.2%}")
    print(f"  - 波动率 / Volatility: {metrics['volatility']:.2%}")
    print(f"  - 夏普比率 / Sharpe Ratio: {metrics['sharpe_ratio']:.4f}")
    print(f"  - 最大回撤 / Max Drawdown: {metrics['max_drawdown']:.2%}")
    print(f"  - 胜率 / Win Rate: {metrics['win_rate']:.2%}")
    
    if 'excess_return' in metrics:
        print(f"\n相对基准指标 / Benchmark Comparison:")
        print(f"  - 超额收益 / Excess Return: {metrics['excess_return']:.2%}")
        print(f"  - 信息比率 / Information Ratio: {metrics['information_ratio']:.4f}")
        print(f"  - 基准收益 / Benchmark Return: {metrics['benchmark_return']:.2%}")
    
    # 6. 说明完整回测流程 / Explain complete backtest process
    print("\n步骤 5: 完整回测流程说明 / Step 5: Complete Backtest Process")
    print("-" * 80)
    print("""
完整的回测流程包括以下步骤：
Complete backtest process includes the following steps:

1. 加载训练好的模型 / Load trained model
   model = backtest_manager._load_model(model_id)

2. 生成预测信号 / Generate prediction signals
   predictions = backtest_manager._generate_signals(model, start_date, end_date, config)

3. 执行回测 / Execute backtest
   portfolio_metrics, positions, trades = backtest_manager._execute_backtest(
       predictions, start_date, end_date, config
   )

4. 计算收益率 / Calculate returns
   returns = backtest_manager._calculate_returns(portfolio_metrics)

5. 获取基准收益率 / Get benchmark returns
   benchmark_returns = backtest_manager._get_benchmark_returns(
       config.benchmark, start_date, end_date
   )

6. 计算性能指标 / Calculate performance metrics
   metrics = backtest_manager.calculate_metrics(returns, benchmark_returns)

7. 保存回测结果 / Save backtest results
   backtest_manager._save_backtest_result(model_id, result, start_date, end_date)

使用示例 / Usage Example:
--------------------------
result = backtest_manager.run_backtest(
    model_id="lgbm_model_20240101_120000",
    start_date="2023-01-01",
    end_date="2023-12-31",
    config=config
)

回测结果包含 / Backtest result contains:
- returns: 收益率序列 / Returns series
- positions: 持仓数据 / Position data
- metrics: 性能指标 / Performance metrics
- trades: 交易记录 / Trade records
- benchmark_returns: 基准收益率 / Benchmark returns
    """)
    
    # 7. 总结 / Summary
    print("\n" + "=" * 80)
    print("演示完成 / Demo Completed")
    print("=" * 80)
    print("""
回测管理器主要功能 / Backtest Manager Key Features:
1. ✓ 加载训练好的模型 / Load trained models
2. ✓ 生成预测信号 / Generate prediction signals
3. ✓ 执行回测流程 / Execute backtest process
4. ✓ 计算性能指标 / Calculate performance metrics
5. ✓ 基准对比分析 / Benchmark comparison analysis
6. ✓ 保存回测结果 / Save backtest results

支持的性能指标 / Supported Performance Metrics:
- 总收益率 / Total Return
- 年化收益率 / Annual Return
- 波动率 / Volatility
- 夏普比率 / Sharpe Ratio
- 最大回撤 / Max Drawdown
- 胜率 / Win Rate
- 超额收益 / Excess Return (vs benchmark)
- 信息比率 / Information Ratio (vs benchmark)

下一步 / Next Steps:
1. 训练一个模型 / Train a model
2. 使用run_backtest()进行完整回测 / Use run_backtest() for complete backtest
3. 分析回测结果 / Analyze backtest results
4. 优化策略参数 / Optimize strategy parameters
    """)


if __name__ == "__main__":
    main()
