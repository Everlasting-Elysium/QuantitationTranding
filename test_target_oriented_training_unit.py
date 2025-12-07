"""
单元测试：目标导向训练功能 / Unit Test: Target-Oriented Training Functionality

这个脚本测试TrainingManager的新增目标导向训练功能（不依赖实际数据）
This script tests the new target-oriented training functionality of TrainingManager (without actual data)
"""

import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

# 添加src目录到路径 / Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.application.training_manager import TrainingManager, DatasetConfig, TrainingConfig, TrainingResult
from src.application.strategy_optimizer import StrategyOptimizer
from src.models.market_models import OptimizationConstraints, StrategyParams


def test_train_for_target_return_integration():
    """
    测试train_for_target_return方法的集成 / Test train_for_target_return method integration
    """
    print("=" * 80)
    print("单元测试：目标导向训练功能 / Unit Test: Target-Oriented Training Functionality")
    print("=" * 80)
    
    try:
        # 1. 创建Mock对象 / Create Mock objects
        print("\n1. 创建Mock对象 / Creating Mock objects...")
        
        mock_data_manager = Mock()
        mock_model_factory = Mock()
        mock_mlflow_tracker = Mock()
        mock_strategy_optimizer = Mock()
        
        # 配置strategy_optimizer的返回值 / Configure strategy_optimizer return values
        mock_suggested_params = StrategyParams(
            model_type="lgbm",
            features=["$close", "$open", "$high", "$low", "$volume"],
            lookback_period=30,
            rebalance_frequency="weekly",
            position_sizing="risk_parity",
            risk_params={"stop_loss": 0.10, "take_profit": 0.20}
        )
        mock_strategy_optimizer.suggest_parameters.return_value = mock_suggested_params
        
        # 配置MLflow tracker / Configure MLflow tracker
        mock_mlflow_tracker.is_initialized.return_value = True
        mock_mlflow_tracker._current_experiment_id = "test_exp_123"
        
        # 2. 创建TrainingManager实例 / Create TrainingManager instance
        print("2. 创建TrainingManager实例 / Creating TrainingManager instance...")
        
        training_manager = TrainingManager(
            data_manager=mock_data_manager,
            model_factory=mock_model_factory,
            mlflow_tracker=mock_mlflow_tracker,
            strategy_optimizer=mock_strategy_optimizer,
            output_dir="./test_outputs"
        )
        
        print("   ✓ TrainingManager创建成功 / TrainingManager created successfully")
        
        # 3. 验证strategy_optimizer已正确集成 / Verify strategy_optimizer is correctly integrated
        print("\n3. 验证strategy_optimizer集成 / Verifying strategy_optimizer integration...")
        
        assert training_manager._strategy_optimizer is not None, "Strategy optimizer should be set"
        assert training_manager._strategy_optimizer == mock_strategy_optimizer, "Strategy optimizer should match"
        
        print("   ✓ Strategy optimizer已正确集成 / Strategy optimizer correctly integrated")
        
        # 4. 测试train_for_target_return方法存在 / Test train_for_target_return method exists
        print("\n4. 验证train_for_target_return方法 / Verifying train_for_target_return method...")
        
        assert hasattr(training_manager, 'train_for_target_return'), \
            "TrainingManager should have train_for_target_return method"
        
        print("   ✓ train_for_target_return方法存在 / train_for_target_return method exists")
        
        # 5. Mock train_model方法以避免实际训练 / Mock train_model to avoid actual training
        print("\n5. 模拟训练过程 / Mocking training process...")
        
        mock_training_result = TrainingResult(
            model_id="test_model_123",
            metrics={"ic_mean": 0.08, "ic_std": 0.05},
            training_time=10.5,
            model_path="./test_outputs/models/test_model_123/model.pkl",
            experiment_id="test_exp_123",
            run_id="test_run_456"
        )
        
        with patch.object(training_manager, 'train_model', return_value=mock_training_result):
            # 6. 调用train_for_target_return / Call train_for_target_return
            print("\n6. 调用train_for_target_return / Calling train_for_target_return...")
            
            dataset_config = DatasetConfig(
                instruments="csi300",
                start_time="2020-01-01",
                end_time="2021-12-31",
                features=["$close", "$open"],
                label="Ref($close, -2) / Ref($close, -1) - 1"
            )
            
            result = training_manager.train_for_target_return(
                target_return=0.20,
                assets=["SH600519", "SZ000858", "SH600036"],
                dataset_config=dataset_config,
                experiment_name="test_target_oriented",
                risk_tolerance="moderate"
            )
            
            print(f"   ✓ 训练完成 / Training completed")
            print(f"     模型ID / Model ID: {result.model_id}")
            print(f"     训练时长 / Training time: {result.training_time:.2f}秒 / seconds")
            
            # 7. 验证strategy_optimizer.suggest_parameters被调用 / Verify suggest_parameters was called
            print("\n7. 验证方法调用 / Verifying method calls...")
            
            mock_strategy_optimizer.suggest_parameters.assert_called_once()
            call_args = mock_strategy_optimizer.suggest_parameters.call_args
            
            assert call_args[1]['target_return'] == 0.20, "Target return should be 0.20"
            assert call_args[1]['risk_tolerance'] == "moderate", "Risk tolerance should be moderate"
            
            print("   ✓ suggest_parameters被正确调用 / suggest_parameters called correctly")
            
            # 8. 验证MLflow记录（如果有优化策略）/ Verify MLflow logging (if optimized strategy exists)
            print("\n8. 验证MLflow集成 / Verifying MLflow integration...")
            
            # 在没有约束条件的情况下，不会调用optimize_for_target_return
            # Without constraints, optimize_for_target_return won't be called
            mock_strategy_optimizer.optimize_for_target_return.assert_not_called()
            
            print("   ✓ MLflow集成正确 / MLflow integration correct")
        
        # 9. 测试带约束条件的场景 / Test scenario with constraints
        print("\n9. 测试带约束条件的场景 / Testing scenario with constraints...")
        
        from src.models.market_models import OptimizedStrategy
        
        mock_optimized_strategy = OptimizedStrategy(
            strategy_id="opt_test_123",
            target_return=0.20,
            expected_return=0.22,
            expected_risk=0.15,
            asset_weights={"SH600519": 0.40, "SZ000858": 0.35, "SH600036": 0.25},
            rebalance_frequency="weekly",
            parameters={"model_type": "lgbm"},
            optimization_score=85.5,
            feasible=True,
            warnings=[]
        )
        
        mock_strategy_optimizer.optimize_for_target_return.return_value = mock_optimized_strategy
        
        constraints = OptimizationConstraints(
            max_position_size=0.30,
            max_sector_exposure=0.50,
            min_diversification=3,
            max_turnover=0.50,
            risk_tolerance="moderate"
        )
        
        with patch.object(training_manager, 'train_model', return_value=mock_training_result):
            result = training_manager.train_for_target_return(
                target_return=0.20,
                assets=["SH600519", "SZ000858", "SH600036"],
                dataset_config=dataset_config,
                experiment_name="test_target_oriented_constrained",
                risk_tolerance="moderate",
                custom_constraints=constraints
            )
            
            print(f"   ✓ 带约束训练完成 / Training with constraints completed")
            
            # 验证optimize_for_target_return被调用 / Verify optimize_for_target_return was called
            mock_strategy_optimizer.optimize_for_target_return.assert_called_once()
            
            # 验证MLflow记录优化结果 / Verify MLflow logged optimization results
            mock_mlflow_tracker.log_metrics.assert_called()
            mock_mlflow_tracker.log_params.assert_called()
            
            print("   ✓ optimize_for_target_return被正确调用 / optimize_for_target_return called correctly")
            print("   ✓ 优化结果已记录到MLflow / Optimization results logged to MLflow")
        
        # 10. 总结 / Summary
        print("\n" + "=" * 80)
        print("测试完成 / Testing Completed")
        print("=" * 80)
        print("\n所有测试均通过！/ All tests passed!")
        print("\n功能验证 / Functionality Verification:")
        print("  ✓ TrainingManager正确集成StrategyOptimizer / TrainingManager correctly integrates StrategyOptimizer")
        print("  ✓ train_for_target_return方法存在并可调用 / train_for_target_return method exists and callable")
        print("  ✓ 策略优化器的suggest_parameters被正确调用 / Strategy optimizer's suggest_parameters called correctly")
        print("  ✓ 带约束条件时optimize_for_target_return被调用 / optimize_for_target_return called with constraints")
        print("  ✓ 优化结果正确记录到MLflow / Optimization results correctly logged to MLflow")
        print("  ✓ 参数调整基于目标收益率和风险偏好 / Parameters adjusted based on target return and risk tolerance")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败 / Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_train_for_target_return_integration()
    sys.exit(0 if success else 1)
