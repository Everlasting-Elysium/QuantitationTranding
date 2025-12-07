"""
Strategy Optimizer Demo
策略优化器演示

This demo shows how to use the StrategyOptimizer to optimize trading strategies
based on target returns and risk preferences.
本演示展示如何使用StrategyOptimizer根据目标收益率和风险偏好优化交易策略。
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.application.strategy_optimizer import StrategyOptimizer
from src.application.performance_analyzer import PerformanceAnalyzer
from src.models.market_models import OptimizationConstraints, AssetMetrics
from src.infrastructure.logger_system import LoggerSystem


def demo_basic_optimization():
    """
    Demonstrate basic strategy optimization.
    演示基本策略优化
    """
    print("\n" + "=" * 80)
    print("示例 1: 基本策略优化 / Example 1: Basic Strategy Optimization")
    print("=" * 80)
    
    # Initialize optimizer
    optimizer = StrategyOptimizer()
    
    # Define target and assets
    target_return = 0.15  # 15% annual return
    assets = ["000001.SZ", "000002.SZ", "000651.SZ", "600000.SH", "600519.SH"]
    
    print(f"\n目标收益率 / Target return: {target_return:.2%}")
    print(f"资产列表 / Assets: {assets}")
    
    # Create mock historical data for demonstration
    # In real usage, this would come from PerformanceAnalyzer
    historical_data = {}
    for i, asset in enumerate(assets):
        historical_data[asset] = AssetMetrics(
            symbol=asset,
            period_start="2021-01-01",
            period_end="2024-01-01",
            total_return=0.25 + i * 0.08,
            annual_return=0.08 + i * 0.03,
            volatility=0.18 + i * 0.02,
            sharpe_ratio=0.6 + i * 0.15,
            max_drawdown=-0.20 - i * 0.03,
            win_rate=0.52 + i * 0.03
        )
    
    # Create constraints
    constraints = OptimizationConstraints(
        max_position_size=0.30,
        max_sector_exposure=0.50,
        min_diversification=3,
        max_turnover=2.0,
        risk_tolerance="moderate"
    )
    
    # Optimize strategy
    print("\n正在优化策略... / Optimizing strategy...")
    strategy = optimizer.optimize_for_target_return(
        target_return=target_return,
        assets=assets,
        constraints=constraints,
        historical_data=historical_data
    )
    
    # Display results
    print("\n优化结果 / Optimization Results:")
    print(f"  策略ID / Strategy ID: {strategy.strategy_id}")
    print(f"  目标收益率 / Target return: {strategy.target_return:.2%}")
    print(f"  预期收益率 / Expected return: {strategy.expected_return:.2%}")
    print(f"  预期风险 / Expected risk: {strategy.expected_risk:.2%}")
    print(f"  夏普比率 / Sharpe ratio: {(strategy.expected_return - 0.03) / strategy.expected_risk:.2f}")
    print(f"  优化评分 / Optimization score: {strategy.optimization_score:.2f}/100")
    print(f"  可行性 / Feasible: {'是 / Yes' if strategy.feasible else '否 / No'}")
    
    print(f"\n资产配置 / Asset Allocation:")
    for asset, weight in sorted(strategy.asset_weights.items(), key=lambda x: x[1], reverse=True):
        print(f"  {asset}: {weight:>6.2%}")
    
    print(f"\n策略参数 / Strategy Parameters:")
    for key, value in strategy.parameters.items():
        print(f"  {key}: {value}")
    
    if strategy.warnings:
        print(f"\n警告 / Warnings:")
        for warning in strategy.warnings:
            print(f"  ⚠ {warning}")


def demo_risk_tolerance_comparison():
    """
    Compare strategies with different risk tolerances.
    比较不同风险偏好的策略
    """
    print("\n" + "=" * 80)
    print("示例 2: 风险偏好比较 / Example 2: Risk Tolerance Comparison")
    print("=" * 80)
    
    optimizer = StrategyOptimizer()
    target_return = 0.18  # 18% target
    
    print(f"\n目标收益率 / Target return: {target_return:.2%}")
    print("\n比较不同风险偏好的策略参数 / Comparing strategy parameters for different risk tolerances:\n")
    
    risk_tolerances = ["conservative", "moderate", "aggressive"]
    
    for risk_tolerance in risk_tolerances:
        params = optimizer.suggest_parameters(
            target_return=target_return,
            risk_tolerance=risk_tolerance
        )
        
        print(f"{risk_tolerance.upper()} / {risk_tolerance.upper()}:")
        print(f"  模型类型 / Model type: {params.model_type}")
        print(f"  特征数量 / Features: {len(params.features)}")
        print(f"  回溯期 / Lookback: {params.lookback_period} days")
        print(f"  再平衡 / Rebalance: {params.rebalance_frequency}")
        print(f"  仓位管理 / Position sizing: {params.position_sizing}")
        print(f"  止损 / Stop loss: {params.risk_params['stop_loss']:.1%}")
        print(f"  止盈 / Take profit: {params.risk_params['take_profit']:.1%}")
        print()


def demo_target_validation():
    """
    Demonstrate target return validation.
    演示目标收益率验证
    """
    print("\n" + "=" * 80)
    print("示例 3: 目标收益率验证 / Example 3: Target Return Validation")
    print("=" * 80)
    
    optimizer = StrategyOptimizer()
    
    # Create mock historical data
    assets = ["000001.SZ", "000002.SZ", "000651.SZ"]
    historical_data = {}
    for i, asset in enumerate(assets):
        historical_data[asset] = AssetMetrics(
            symbol=asset,
            period_start="2021-01-01",
            period_end="2024-01-01",
            total_return=0.30,
            annual_return=0.10,
            volatility=0.20,
            sharpe_ratio=0.50,
            max_drawdown=-0.25,
            win_rate=0.55
        )
    
    # Test different target returns
    test_targets = [0.08, 0.12, 0.18, 0.30, 0.50]
    
    print("\n测试不同目标收益率的可行性 / Testing feasibility of different target returns:\n")
    
    for target in test_targets:
        result = optimizer._validate_target_return(
            target_return=target,
            assets=assets,
            historical_data=historical_data
        )
        
        feasible_str = "✓ 可行 / Feasible" if result["feasible"] else "✗ 不可行 / Not feasible"
        print(f"目标 / Target {target:.1%}: {feasible_str}")
        print(f"  {result['message']}")
        print()


def main():
    """Main demo function."""
    print("\n" + "=" * 80)
    print("策略优化器演示 / Strategy Optimizer Demo")
    print("=" * 80)
    
    try:
        # Run demos
        demo_basic_optimization()
        demo_risk_tolerance_comparison()
        demo_target_validation()
        
        print("\n" + "=" * 80)
        print("✓ 演示完成 / Demo completed successfully")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n✗ 演示失败 / Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
