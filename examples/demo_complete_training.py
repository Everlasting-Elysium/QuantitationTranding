"""
完整模型训练和评估示例 / Complete Model Training and Evaluation Example
演示模型训练、评估、对比的完整流程
Demonstrates the complete workflow of model training, evaluation, and comparison

这个示例展示了:
This example demonstrates:
1. 使用不同模型类型训练 / Training with different model types
2. 使用模板训练 / Training with templates
3. 模型性能对比 / Model performance comparison
4. 模型注册和管理 / Model registration and management
5. 最佳模型选择 / Best model selection
"""

import sys
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径 / Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.data_manager import DataManager
from src.core.model_factory import ModelFactory
from src.infrastructure.qlib_wrapper import QlibWrapper
from src.infrastructure.mlflow_tracker import MLflowTracker
from src.infrastructure.logger_system import setup_logger
from src.application.training_manager import (
    TrainingManager,
    TrainingConfig,
    DatasetConfig
)
from src.application.model_registry import ModelRegistry


def print_section(title: str):
    """打印章节标题 / Print section title"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_model_metrics(model_name: str, metrics: dict):
    """打印模型指标 / Print model metrics"""
    print(f"\n{model_name} 指标 / {model_name} Metrics:")
    print("-" * 40)
    for metric_name, metric_value in metrics.items():
        if isinstance(metric_value, float):
            print(f"  {metric_name}: {metric_value:.6f}")
        else:
            print(f"  {metric_name}: {metric_value}")


def main():
    """主函数 / Main function"""
    
    print_section("完整模型训练和评估示例 / Complete Model Training and Evaluation Example")
    
    # ========================================================================
    # 步骤 1: 系统初始化 / Step 1: System Initialization
    # ========================================================================
    print("\n步骤 1 / Step 1: 系统初始化 / System Initialization")
    print("-" * 80)
    
    setup_logger(log_dir="./logs", log_level="INFO")
    
    qlib_wrapper = QlibWrapper()
    try:
        qlib_wrapper.init(
            provider_uri="~/.qlib/qlib_data/cn_data",
            region="cn"
        )
        print("✓ Qlib初始化成功 / Qlib initialized successfully")
    except Exception as e:
        print(f"✗ Qlib初始化失败 / Qlib initialization failed: {str(e)}")
        return
    
    data_manager = DataManager(qlib_wrapper=qlib_wrapper)
    model_factory = ModelFactory()
    
    # 初始化MLflow / Initialize MLflow
    mlflow_tracker = None
    try:
        mlflow_tracker = MLflowTracker(tracking_uri="./examples/mlruns")
        mlflow_tracker.initialize()
        print("✓ MLflow追踪器初始化成功 / MLflow tracker initialized successfully")
    except Exception as e:
        print(f"⚠ MLflow追踪器初始化失败 / MLflow tracker initialization failed: {str(e)}")
    
    training_manager = TrainingManager(
        data_manager=data_manager,
        model_factory=model_factory,
        mlflow_tracker=mlflow_tracker,
        output_dir="./outputs"
    )
    
    model_registry = ModelRegistry(registry_dir="./model_registry")
    
    print("✓ 所有组件初始化完成 / All components initialized")
    
    # ========================================================================
    # 步骤 2: 准备数据集配置 / Step 2: Prepare Dataset Configuration
    # ========================================================================
    print("\n步骤 2 / Step 2: 准备数据集配置 / Prepare Dataset Configuration")
    print("-" * 80)
    
    dataset_config = DatasetConfig(
        instruments="csi300",
        start_time="2020-01-01",
        end_time="2021-12-31",
        features=["$close", "$volume", "$open", "$high", "$low"],
        label="Ref($close, -1) / $close - 1"
    )
    
    print(f"数据集配置 / Dataset configuration:")
    print(f"  股票池 / Instruments: {dataset_config.instruments}")
    print(f"  时间范围 / Time range: {dataset_config.start_time} 至 / to {dataset_config.end_time}")
    print(f"  特征数量 / Number of features: {len(dataset_config.features)}")
    
    # ========================================================================
    # 步骤 3: 训练多个模型 / Step 3: Train Multiple Models
    # ========================================================================
    print("\n步骤 3 / Step 3: 训练多个模型 / Train Multiple Models")
    print("-" * 80)
    
    # 存储训练结果 / Store training results
    training_results = {}
    
    # 3.1 训练LightGBM模型 / Train LightGBM model
    print("\n[3.1] 训练LightGBM模型 / Training LightGBM model...")
    
    lgbm_config = TrainingConfig(
        model_type="lgbm",
        dataset_config=dataset_config,
        model_params={
            "loss": "mse",
            "num_boost_round": 100,
            "learning_rate": 0.1,
            "max_depth": 6,
        },
        training_params={},
        experiment_name="model_comparison"
    )
    
    try:
        lgbm_result = training_manager.train_model(lgbm_config)
        training_results["LightGBM"] = lgbm_result
        print(f"✓ LightGBM训练完成 / LightGBM training completed")
        print(f"  模型ID / Model ID: {lgbm_result.model_id}")
        print(f"  训练时长 / Training time: {lgbm_result.training_time:.2f}秒 / seconds")
        print_model_metrics("LightGBM", lgbm_result.metrics)
        
        # 注册模型 / Register model
        model_registry.register_model(
            model_path=lgbm_result.model_path,
            model_name="LightGBM_CSI300",
            version="1.0",
            metadata={
                "model_type": "lgbm",
                "training_date": datetime.now().strftime("%Y-%m-%d"),
                "dataset": "csi300",
                "metrics": lgbm_result.metrics
            }
        )
        print(f"✓ 模型已注册 / Model registered")
        
    except Exception as e:
        print(f"✗ LightGBM训练失败 / LightGBM training failed: {str(e)}")
    
    # 3.2 训练线性模型 / Train Linear model
    print("\n[3.2] 训练线性模型 / Training Linear model...")
    
    linear_config = TrainingConfig(
        model_type="linear",
        dataset_config=dataset_config,
        model_params={
            "estimator": "ridge",
            "alpha": 0.05,
        },
        training_params={},
        experiment_name="model_comparison"
    )
    
    try:
        linear_result = training_manager.train_model(linear_config)
        training_results["Linear"] = linear_result
        print(f"✓ 线性模型训练完成 / Linear model training completed")
        print(f"  模型ID / Model ID: {linear_result.model_id}")
        print(f"  训练时长 / Training time: {linear_result.training_time:.2f}秒 / seconds")
        print_model_metrics("Linear", linear_result.metrics)
        
        # 注册模型 / Register model
        model_registry.register_model(
            model_path=linear_result.model_path,
            model_name="Linear_CSI300",
            version="1.0",
            metadata={
                "model_type": "linear",
                "training_date": datetime.now().strftime("%Y-%m-%d"),
                "dataset": "csi300",
                "metrics": linear_result.metrics
            }
        )
        print(f"✓ 模型已注册 / Model registered")
        
    except Exception as e:
        print(f"✗ 线性模型训练失败 / Linear model training failed: {str(e)}")
    
    # ========================================================================
    # 步骤 4: 使用模板训练 / Step 4: Train Using Templates
    # ========================================================================
    print("\n步骤 4 / Step 4: 使用模板训练 / Train Using Templates")
    print("-" * 80)
    
    # 列出可用模板 / List available templates
    templates = training_manager.list_templates()
    print(f"可用模板 / Available templates: {len(templates)}")
    for template in templates:
        print(f"  - {template.name}: {template.description}")
    
    # 使用模板训练 / Train using template
    if templates:
        template_name = templates[0].name
        print(f"\n使用模板训练 / Training with template: {template_name}")
        
        try:
            template_result = training_manager.train_from_template(
                template_name=template_name,
                dataset_config=dataset_config,
                experiment_name="model_comparison"
            )
            training_results[f"Template_{template_name}"] = template_result
            print(f"✓ 模板训练完成 / Template training completed")
            print(f"  模型ID / Model ID: {template_result.model_id}")
            print(f"  训练时长 / Training time: {template_result.training_time:.2f}秒 / seconds")
            print_model_metrics(f"Template_{template_name}", template_result.metrics)
            
            # 注册模型 / Register model
            model_registry.register_model(
                model_path=template_result.model_path,
                model_name=f"{template_name}_CSI300",
                version="1.0",
                metadata={
                    "model_type": template_name,
                    "training_date": datetime.now().strftime("%Y-%m-%d"),
                    "dataset": "csi300",
                    "metrics": template_result.metrics
                }
            )
            print(f"✓ 模型已注册 / Model registered")
            
        except Exception as e:
            print(f"✗ 模板训练失败 / Template training failed: {str(e)}")
    
    # ========================================================================
    # 步骤 5: 模型性能对比 / Step 5: Model Performance Comparison
    # ========================================================================
    print("\n步骤 5 / Step 5: 模型性能对比 / Model Performance Comparison")
    print("-" * 80)
    
    if training_results:
        print("\n模型性能对比表 / Model Performance Comparison Table:")
        print("-" * 80)
        
        # 打印表头 / Print header
        print(f"{'模型名称 / Model':<25} {'IC':<12} {'ICIR':<12} {'训练时长 / Time':<15}")
        print("-" * 80)
        
        # 打印每个模型的指标 / Print metrics for each model
        for model_name, result in training_results.items():
            ic = result.metrics.get('IC', 0.0)
            icir = result.metrics.get('ICIR', 0.0)
            time = result.training_time
            print(f"{model_name:<25} {ic:<12.6f} {icir:<12.6f} {time:<15.2f}s")
        
        # 找出最佳模型 / Find best model
        print("\n最佳模型 / Best Model:")
        print("-" * 40)
        
        best_model_name = max(
            training_results.keys(),
            key=lambda k: training_results[k].metrics.get('IC', 0.0)
        )
        best_result = training_results[best_model_name]
        
        print(f"  模型名称 / Model name: {best_model_name}")
        print(f"  模型ID / Model ID: {best_result.model_id}")
        print(f"  IC: {best_result.metrics.get('IC', 0.0):.6f}")
        print(f"  ICIR: {best_result.metrics.get('ICIR', 0.0):.6f}")
        
        # 标记为生产模型 / Mark as production model
        try:
            model_registry.set_production_model(best_result.model_id)
            print(f"✓ 已标记为生产模型 / Marked as production model")
        except Exception as e:
            print(f"⚠ 标记生产模型失败 / Failed to mark as production model: {str(e)}")
    
    # ========================================================================
    # 步骤 6: 查看模型注册表 / Step 6: View Model Registry
    # ========================================================================
    print("\n步骤 6 / Step 6: 查看模型注册表 / View Model Registry")
    print("-" * 80)
    
    try:
        registered_models = model_registry.list_models()
        print(f"注册模型数量 / Number of registered models: {len(registered_models)}")
        
        for i, model_info in enumerate(registered_models, 1):
            print(f"\n模型 {i} / Model {i}:")
            print(f"  模型ID / Model ID: {model_info.model_id}")
            print(f"  模型名称 / Model name: {model_info.model_name}")
            print(f"  版本 / Version: {model_info.version}")
            print(f"  训练日期 / Training date: {model_info.training_date}")
            print(f"  是否为生产模型 / Is production: {model_info.is_production}")
            
    except Exception as e:
        print(f"✗ 查看模型注册表失败 / Failed to view model registry: {str(e)}")
    
    # ========================================================================
    # 总结 / Summary
    # ========================================================================
    print_section("总结 / Summary")
    
    print("\n本示例展示了完整的模型训练和评估流程:")
    print("This example demonstrated the complete model training and evaluation workflow:")
    print("  ✓ 训练多种模型类型 / Trained multiple model types")
    print("  ✓ 使用模板快速训练 / Used templates for quick training")
    print("  ✓ 模型性能对比 / Compared model performance")
    print("  ✓ 模型注册和管理 / Registered and managed models")
    print("  ✓ 选择最佳模型 / Selected best model")
    
    print(f"\n训练的模型数量 / Number of trained models: {len(training_results)}")
    
    if mlflow_tracker:
        print(f"\n查看MLflow UI / View MLflow UI:")
        print(f"  mlflow ui --backend-store-uri ./examples/mlruns")
        print(f"  然后访问 / Then visit: http://localhost:5000")
    
    print("\n下一步 / Next steps:")
    print("  1. 运行回测评估模型 / Run backtest to evaluate models")
    print("     python examples/demo_complete_backtest.py")
    print("  2. 生成交易信号 / Generate trading signals")
    print("     python examples/demo_signal_generator.py")
    print("  3. 查看完整端到端示例 / View complete end-to-end example")
    print("     python examples/demo_end_to_end.py")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
