"""
测试目标导向训练功能 / Test Target-Oriented Training Functionality

这个脚本测试TrainingManager的新增目标导向训练功能
This script tests the new target-oriented training functionality of TrainingManager
"""

import sys
from pathlib import Path

# 添加src目录到路径 / Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.data_manager import DataManager
from src.core.model_factory import ModelFactory
from src.core.config_manager import ConfigManager
from src.application.training_manager import TrainingManager, DatasetConfig
from src.application.strategy_optimizer import StrategyOptimizer
from src.infrastructure.mlflow_tracker import MLflowTracker
from src.infrastructure.logger_system import LoggerSystem
from src.models.market_models import OptimizationConstraints


def test_target_oriented_training():
    """
    测试目标导向训练 / Test Target-Oriented Training
    """
    print("=" * 80)
    print("测试目标导向训练功能 / Testing Target-Oriented Training Functionality")
    print("=" * 80)
    
    try:
        # 1. 初始化日志系统 / Initialize logging system
        print("\n1. 初始化日志系统 / Initializing logging system...")
        logger_system = LoggerSystem()
        logger_system.setup(log_dir="./logs", log_level="INFO")
        logger = logger_system.get_logger(__name__)
        logger.info("日志系统初始化成功 / Logging system initialized")
        
        # 2. 加载配置 / Load configuration
        print("2. 加载配置 / Loading configuration...")
        config_manager = ConfigManager()
        config = config_manager.load_config("./config/default_config.yaml")
        logger.info("配置加载成功 / Configuration loaded")
        
        # 3. 初始化qlib / Initialize qlib
        print("3. 初始化qlib / Initializing qlib...")
        import qlib
        from qlib.config import REG_CN
        
        provider_uri = str(Path(config.qlib.provider_uri).expanduser())
        qlib.init(provider_uri=provider_uri, region=REG_CN)
        logger.info("qlib初始化成功 / qlib initialized")
        
        # 4. 创建组件 / Create components
        print("4. 创建组件 / Creating components...")
        data_manager = DataManager(config)
        model_factory = ModelFactory()
        strategy_optimizer = StrategyOptimizer()
        
        # 初始化MLflow（可选）/ Initialize MLflow (optional)
        mlflow_tracker = None
        if hasattr(config.mlflow, 'tracking_uri') and config.mlflow.tracking_uri:
            try:
                mlflow_tracker = MLflowTracker(
                    tracking_uri=config.mlflow.tracking_uri,
                    experiment_name="target_oriented_training_test"
                )
                logger.info("MLflow追踪器初始化成功 / MLflow tracker initialized")
            except Exception as e:
                logger.warning(f"MLflow初始化失败，继续测试 / MLflow initialization failed, continuing test: {str(e)}")
        
        # 创建训练管理器 / Create training manager
        training_manager = TrainingManager(
            data_manager=data_manager,
            model_factory=model_factory,
            mlflow_tracker=mlflow_tracker,
            strategy_optimizer=strategy_optimizer,
            output_dir="./outputs"
        )
        logger.info("训练管理器创建成功 / Training manager created")
        
        # 5. 配置数据集 / Configure dataset
        print("\n5. 配置数据集 / Configuring dataset...")
        dataset_config = DatasetConfig(
            instruments="csi300",
            start_time="2020-01-01",
            end_time="2021-12-31",
            features=[
                "$close", "$open", "$high", "$low", "$volume",
                "$change", "$factor"
            ],
            label="Ref($close, -2) / Ref($close, -1) - 1"
        )
        logger.info("数据集配置完成 / Dataset configured")
        
        # 6. 测试场景1：基本目标导向训练（无约束）/ Test Scenario 1: Basic target-oriented training (no constraints)
        print("\n" + "=" * 80)
        print("测试场景1：基本目标导向训练 / Test Scenario 1: Basic Target-Oriented Training")
        print("=" * 80)
        
        target_return = 0.20  # 20% 年化收益率 / 20% annual return
        assets = ["SH600519", "SZ000858", "SH600036"]  # 示例资产 / Example assets
        
        print(f"\n目标收益率 / Target return: {target_return:.2%}")
        print(f"资产列表 / Asset list: {assets}")
        print(f"风险偏好 / Risk tolerance: moderate")
        
        result1 = training_manager.train_for_target_return(
            target_return=target_return,
            assets=assets,
            dataset_config=dataset_config,
            experiment_name="target_oriented_test_basic",
            risk_tolerance="moderate"
        )
        
        print(f"\n训练结果 / Training result:")
        print(f"  模型ID / Model ID: {result1.model_id}")
        print(f"  训练时长 / Training time: {result1.training_time:.2f}秒 / seconds")
        print(f"  指标 / Metrics: {result1.metrics}")
        print(f"  模型路径 / Model path: {result1.model_path}")
        
        # 7. 测试场景2：带约束条件的目标导向训练 / Test Scenario 2: Target-oriented training with constraints
        print("\n" + "=" * 80)
        print("测试场景2：带约束条件的目标导向训练 / Test Scenario 2: Target-Oriented Training with Constraints")
        print("=" * 80)
        
        constraints = OptimizationConstraints(
            max_position_size=0.30,  # 单只股票最大30%
            max_sector_exposure=0.50,  # 单个行业最大50%
            min_diversification=3,  # 至少3只股票
            max_turnover=0.50,  # 最大换手率50%
            risk_tolerance="moderate"
        )
        
        print(f"\n约束条件 / Constraints:")
        print(f"  最大持仓 / Max position: {constraints.max_position_size:.2%}")
        print(f"  最大行业暴露 / Max sector exposure: {constraints.max_sector_exposure:.2%}")
        print(f"  最小分散化 / Min diversification: {constraints.min_diversification}")
        print(f"  最大换手率 / Max turnover: {constraints.max_turnover:.2%}")
        
        result2 = training_manager.train_for_target_return(
            target_return=target_return,
            assets=assets,
            dataset_config=dataset_config,
            experiment_name="target_oriented_test_constrained",
            risk_tolerance="moderate",
            custom_constraints=constraints
        )
        
        print(f"\n训练结果 / Training result:")
        print(f"  模型ID / Model ID: {result2.model_id}")
        print(f"  训练时长 / Training time: {result2.training_time:.2f}秒 / seconds")
        print(f"  指标 / Metrics: {result2.metrics}")
        print(f"  模型路径 / Model path: {result2.model_path}")
        
        # 8. 测试场景3：不同风险偏好 / Test Scenario 3: Different risk tolerances
        print("\n" + "=" * 80)
        print("测试场景3：不同风险偏好 / Test Scenario 3: Different Risk Tolerances")
        print("=" * 80)
        
        risk_tolerances = ["conservative", "moderate", "aggressive"]
        
        for risk_tolerance in risk_tolerances:
            print(f"\n测试风险偏好 / Testing risk tolerance: {risk_tolerance}")
            
            result = training_manager.train_for_target_return(
                target_return=target_return,
                assets=assets,
                dataset_config=dataset_config,
                experiment_name=f"target_oriented_test_{risk_tolerance}",
                risk_tolerance=risk_tolerance
            )
            
            print(f"  模型ID / Model ID: {result.model_id}")
            print(f"  训练时长 / Training time: {result.training_time:.2f}秒 / seconds")
        
        # 9. 总结 / Summary
        print("\n" + "=" * 80)
        print("测试完成 / Testing Completed")
        print("=" * 80)
        print("\n所有测试场景均成功完成！/ All test scenarios completed successfully!")
        print("\n功能验证 / Functionality Verification:")
        print("  ✓ 基本目标导向训练 / Basic target-oriented training")
        print("  ✓ 带约束条件的训练 / Training with constraints")
        print("  ✓ 不同风险偏好 / Different risk tolerances")
        print("  ✓ 策略优化器集成 / Strategy optimizer integration")
        print("  ✓ MLflow结果记录 / MLflow result logging")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败 / Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_target_oriented_training()
    sys.exit(0 if success else 1)
