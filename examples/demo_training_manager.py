"""
训练管理器演示 / Training Manager Demo
演示如何使用TrainingManager进行模型训练
Demonstrates how to use TrainingManager for model training
"""

import sys
from pathlib import Path

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


def main():
    """主函数 / Main function"""
    
    # 1. 设置日志 / Setup logging
    print("=" * 80)
    print("训练管理器演示 / Training Manager Demo")
    print("=" * 80)
    
    setup_logger(log_dir="./logs", log_level="INFO")
    
    # 2. 初始化组件 / Initialize components
    print("\n步骤 1: 初始化组件 / Step 1: Initialize components")
    print("-" * 80)
    
    # 初始化qlib / Initialize qlib
    qlib_wrapper = QlibWrapper()
    try:
        qlib_wrapper.init(
            provider_uri="~/.qlib/qlib_data/cn_data",
            region="cn"
        )
        print("✓ Qlib初始化成功 / Qlib initialized successfully")
    except Exception as e:
        print(f"✗ Qlib初始化失败 / Qlib initialization failed: {str(e)}")
        print("\n请先下载数据 / Please download data first:")
        print("python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn")
        return
    
    # 初始化数据管理器 / Initialize data manager
    data_manager = DataManager(qlib_wrapper=qlib_wrapper)
    print("✓ 数据管理器初始化成功 / Data manager initialized successfully")
    
    # 初始化模型工厂 / Initialize model factory
    model_factory = ModelFactory()
    print("✓ 模型工厂初始化成功 / Model factory initialized successfully")
    
    # 初始化MLflow追踪器（可选）/ Initialize MLflow tracker (optional)
    mlflow_tracker = None
    try:
        mlflow_tracker = MLflowTracker(tracking_uri="./mlruns")
        mlflow_tracker.initialize()
        print("✓ MLflow追踪器初始化成功 / MLflow tracker initialized successfully")
    except Exception as e:
        print(f"⚠ MLflow追踪器初始化失败（将继续不使用MLflow）/ MLflow tracker initialization failed (will continue without MLflow): {str(e)}")
    
    # 初始化训练管理器 / Initialize training manager
    training_manager = TrainingManager(
        data_manager=data_manager,
        model_factory=model_factory,
        mlflow_tracker=mlflow_tracker,
        output_dir="./outputs"
    )
    print("✓ 训练管理器初始化成功 / Training manager initialized successfully")
    
    # 3. 配置训练 / Configure training
    print("\n步骤 2: 配置训练 / Step 2: Configure training")
    print("-" * 80)
    
    # 创建数据集配置 / Create dataset configuration
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
    
    # 创建训练配置 / Create training configuration
    training_config = TrainingConfig(
        model_type="lgbm",
        dataset_config=dataset_config,
        model_params={
            "loss": "mse",
            "num_boost_round": 100,
            "learning_rate": 0.1,
        },
        training_params={},
        experiment_name="demo_training"
    )
    
    print(f"\n训练配置 / Training configuration:")
    print(f"  模型类型 / Model type: {training_config.model_type}")
    print(f"  实验名称 / Experiment name: {training_config.experiment_name}")
    print(f"  模型参数 / Model parameters: {training_config.model_params}")
    
    # 4. 训练模型 / Train model
    print("\n步骤 3: 训练模型 / Step 3: Train model")
    print("-" * 80)
    
    try:
        result = training_manager.train_model(training_config)
        
        print("\n✓ 训练完成 / Training completed!")
        print(f"\n训练结果 / Training result:")
        print(f"  模型ID / Model ID: {result.model_id}")
        print(f"  训练时长 / Training time: {result.training_time:.2f} 秒 / seconds")
        print(f"  模型路径 / Model path: {result.model_path}")
        print(f"  评估指标 / Metrics:")
        for metric_name, metric_value in result.metrics.items():
            print(f"    {metric_name}: {metric_value:.6f}")
        
        if result.run_id:
            print(f"  MLflow运行ID / MLflow run ID: {result.run_id}")
            print(f"\n查看MLflow UI / View MLflow UI:")
            print(f"  mlflow ui --backend-store-uri ./mlruns")
        
    except Exception as e:
        print(f"\n✗ 训练失败 / Training failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    
    # 5. 从模板训练（可选）/ Train from template (optional)
    print("\n步骤 4: 从模板训练（可选）/ Step 4: Train from template (optional)")
    print("-" * 80)
    
    # 列出可用模板 / List available templates
    templates = training_manager.list_templates()
    print(f"可用模板 / Available templates: {len(templates)}")
    for template in templates:
        print(f"  - {template.name}: {template.description}")
    
    # 从模板训练 / Train from template
    if templates:
        template_name = templates[0].name
        print(f"\n使用模板训练 / Training with template: {template_name}")
        
        try:
            result = training_manager.train_from_template(
                template_name=template_name,
                dataset_config=dataset_config,
                experiment_name="demo_template_training"
            )
            
            print(f"\n✓ 模板训练完成 / Template training completed!")
            print(f"  模型ID / Model ID: {result.model_id}")
            print(f"  训练时长 / Training time: {result.training_time:.2f} 秒 / seconds")
            
        except Exception as e:
            print(f"\n✗ 模板训练失败 / Template training failed: {str(e)}")
    
    print("\n" + "=" * 80)
    print("演示完成 / Demo completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
