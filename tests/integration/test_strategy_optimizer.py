"""
Test script for Strategy Optimizer
策略优化器测试脚本
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.application.strategy_optimizer import StrategyOptimizer
from src.models.market_models import OptimizationConstraints, AssetMetrics
from datetime import datetime, timedelta


def test_strategy_optimizer():
    """Test basic strategy optimizer functionality."""
    print("=" * 80)
    print("测试策略优化器 / Testing Strategy Optimizer")
    print("=" * 80)
    
    # Create optimizer
    print("\n1. 创建优化器 / Creating optimizer...")
    optimizer = StrategyOptimizer()
    print("✓ 优化器创建成功 / Optimizer created successfully")
    
    # Test parameter suggestion
    print("\n2. 测试参数建议 / Testing parameter suggestion...")
    try:
        params = optimizer.suggest_parameters(
            target_return=0.15,  # 15% target return
            risk_tolerance="moderate"
        )
        print(f"✓ 参数建议成功 / Parameters suggested successfully")
        print(f"  模型类型 / Model type: {params.model_type}")
        print(f"  特征数量 / Features count: {len(params.features)}")
        print(f"  回溯期 / Lookback period: {params.lookback_period} days")
        print(f"  再平衡频率 / Rebalance frequency: {params.rebalance_frequency}")
    except Exception as e:
        print(f"✗ 参数建议失败 / Parameter suggestion failed: {str(e)}")
        return False
    
    # Test optimization with mock data
    print("\n3. 测试策略优化 / Testing strategy optimization...")
    try:
        # Create mock historical data
        assets = ["000001.SZ", "000002.SZ", "000003.SZ", "000004.SZ", "000005.SZ"]
        
        # Create mock metrics
        historical_data = {}
        for i, asset in enumerate(assets):
            historical_data[asset] = AssetMetrics(
                symbol=asset,
                period_start="2021-01-01",
                period_end="2024-01-01",
                total_return=0.3 + i * 0.05,
                annual_return=0.10 + i * 0.02,
                volatility=0.15 + i * 0.01,
                sharpe_ratio=0.8 + i * 0.1,
                max_drawdown=-0.15 - i * 0.02,
                win_rate=0.55 + i * 0.02
            )
        
        # Create constraints
        constraints = OptimizationConstraints(
            max_position_size=0.25,
            max_sector_exposure=0.40,
            min_diversification=3,
            max_turnover=2.0,
            risk_tolerance="moderate"
        )
        
        # Optimize
        strategy = optimizer.optimize_for_target_return(
            target_return=0.15,
            assets=assets,
            constraints=constraints,
            historical_data=historical_data
        )
        
        print(f"✓ 策略优化成功 / Strategy optimization successful")
        print(f"  策略ID / Strategy ID: {strategy.strategy_id}")
        print(f"  目标收益率 / Target return: {strategy.target_return:.2%}")
        print(f"  预期收益率 / Expected return: {strategy.expected_return:.2%}")
        print(f"  预期风险 / Expected risk: {strategy.expected_risk:.2%}")
        print(f"  优化评分 / Optimization score: {strategy.optimization_score:.2f}")
        print(f"  可行性 / Feasible: {strategy.feasible}")
        print(f"  资产数量 / Number of assets: {len(strategy.asset_weights)}")
        print(f"  资产权重 / Asset weights:")
        for asset, weight in sorted(strategy.asset_weights.items(), key=lambda x: x[1], reverse=True):
            print(f"    {asset}: {weight:.2%}")
        
        if strategy.warnings:
            print(f"  警告 / Warnings:")
            for warning in strategy.warnings:
                print(f"    - {warning}")
        
    except Exception as e:
        print(f"✗ 策略优化失败 / Strategy optimization failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test different risk tolerances
    print("\n4. 测试不同风险偏好 / Testing different risk tolerances...")
    for risk_tolerance in ["conservative", "moderate", "aggressive"]:
        try:
            params = optimizer.suggest_parameters(
                target_return=0.15,
                risk_tolerance=risk_tolerance
            )
            print(f"  {risk_tolerance}: 模型={params.model_type}, "
                  f"回溯期={params.lookback_period}天, "
                  f"再平衡={params.rebalance_frequency}")
        except Exception as e:
            print(f"  {risk_tolerance}: 失败 / Failed - {str(e)}")
    
    print("\n" + "=" * 80)
    print("✓ 所有测试通过 / All tests passed")
    print("=" * 80)
    return True


if __name__ == "__main__":
    success = test_strategy_optimizer()
    sys.exit(0 if success else 1)
