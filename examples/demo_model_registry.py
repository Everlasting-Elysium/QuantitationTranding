"""
模型注册表演示 / Model Registry Demo

演示如何使用ModelRegistry进行模型注册、查询和管理
Demonstrates how to use ModelRegistry for model registration, querying and management
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径 / Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.application.model_registry import ModelRegistry, ModelFilter
from src.models.data_models import ModelMetadata, DatasetConfig
from src.infrastructure.logger_system import setup_logging


class DummyModel:
    """虚拟模型类用于演示 / Dummy model class for demonstration"""
    def __init__(self, name):
        self.name = name
    
    def predict(self, data):
        return f"Prediction from {self.name}"


def create_dummy_model():
    """创建一个虚拟模型用于演示 / Create a dummy model for demonstration"""
    return DummyModel("Demo Model")


def main():
    """主函数 / Main function"""
    
    # 设置日志 / Setup logging
    setup_logging(log_dir="./logs", log_level="INFO")
    
    print("=" * 80)
    print("模型注册表演示 / Model Registry Demo")
    print("=" * 80)
    print()
    
    # 1. 初始化模型注册表 / Initialize model registry
    print("1. 初始化模型注册表 / Initializing model registry...")
    registry = ModelRegistry(registry_dir="./demo_registry")
    print("✓ 模型注册表初始化成功 / Model registry initialized successfully")
    print()
    
    # 2. 注册第一个模型 / Register first model
    print("2. 注册第一个模型 / Registering first model...")
    model1 = create_dummy_model()
    metadata1 = ModelMetadata(
        model_name="lgbm_model",
        version="1.0",
        training_date="2024-01-01",
        performance_metrics={
            "ic_mean": 0.05,
            "ic_std": 0.02,
            "sharpe_ratio": 1.5
        },
        dataset_info=DatasetConfig(
            instruments="csi300",
            start_time="2020-01-01",
            end_time="2023-12-31",
            features=["close", "volume"],
            label="label"
        ),
        hyperparameters={
            "model_type": "lgbm",
            "n_estimators": 100,
            "learning_rate": 0.1
        }
    )
    
    model_id1 = registry.register_model(model1, metadata1)
    print(f"✓ 模型注册成功 / Model registered successfully: {model_id1}")
    print()
    
    # 3. 注册第二个模型（性能更好）/ Register second model (better performance)
    print("3. 注册第二个模型（性能更好）/ Registering second model (better performance)...")
    model2 = create_dummy_model()
    metadata2 = ModelMetadata(
        model_name="lgbm_model",
        version="2.0",
        training_date="2024-01-15",
        performance_metrics={
            "ic_mean": 0.08,  # 更高的IC / Higher IC
            "ic_std": 0.02,
            "sharpe_ratio": 2.0
        },
        dataset_info=DatasetConfig(
            instruments="csi300",
            start_time="2020-01-01",
            end_time="2023-12-31",
            features=["close", "volume", "open"],
            label="label"
        ),
        hyperparameters={
            "model_type": "lgbm",
            "n_estimators": 150,
            "learning_rate": 0.05
        }
    )
    
    model_id2 = registry.register_model(model2, metadata2)
    print(f"✓ 模型注册成功 / Model registered successfully: {model_id2}")
    print()
    
    # 4. 列出所有模型 / List all models
    print("4. 列出所有模型 / Listing all models...")
    all_models = registry.list_models()
    print(f"共有 {len(all_models)} 个模型 / Total {len(all_models)} models:")
    for model_info in all_models:
        print(f"  - {model_info.model_id}")
        print(f"    名称 / Name: {model_info.model_name}")
        print(f"    版本 / Version: {model_info.version}")
        print(f"    状态 / Status: {model_info.status}")
        print(f"    IC均值 / IC Mean: {model_info.performance_metrics.get('ic_mean', 0):.4f}")
        print()
    
    # 5. 设置第一个模型为生产模型 / Set first model as production
    print("5. 设置第一个模型为生产模型 / Setting first model as production...")
    registry.set_production_model(model_id1)
    print(f"✓ 模型 {model_id1} 已设置为生产模型 / Model {model_id1} set as production")
    print()
    
    # 6. 获取生产模型 / Get production model
    print("6. 获取生产模型 / Getting production model...")
    prod_model = registry.get_production_model()
    if prod_model:
        print(f"当前生产模型 / Current production model: {prod_model.model_id}")
        print(f"  版本 / Version: {prod_model.version}")
        print(f"  IC均值 / IC Mean: {prod_model.performance_metrics.get('ic_mean', 0):.4f}")
    else:
        print("没有生产模型 / No production model")
    print()
    
    # 7. 注册第三个模型（性能更好，应该自动标记为候选）/ 
    # Register third model (better performance, should be auto-marked as candidate)
    print("7. 注册第三个模型（性能更好）/ Registering third model (better performance)...")
    model3 = create_dummy_model()
    metadata3 = ModelMetadata(
        model_name="lgbm_model",
        version="3.0",
        training_date="2024-02-01",
        performance_metrics={
            "ic_mean": 0.10,  # 最高的IC / Highest IC
            "ic_std": 0.015,
            "sharpe_ratio": 2.5
        },
        dataset_info=DatasetConfig(
            instruments="csi300",
            start_time="2020-01-01",
            end_time="2023-12-31",
            features=["close", "volume", "open", "high", "low"],
            label="label"
        ),
        hyperparameters={
            "model_type": "lgbm",
            "n_estimators": 200,
            "learning_rate": 0.03
        }
    )
    
    model_id3 = registry.register_model(model3, metadata3)
    print(f"✓ 模型注册成功 / Model registered successfully: {model_id3}")
    
    # 检查是否被标记为候选 / Check if marked as candidate
    models = registry.list_models()
    model3_info = next((m for m in models if m.model_id == model_id3), None)
    if model3_info and model3_info.status == "candidate":
        print(f"✓ 模型自动标记为候选 / Model automatically marked as candidate")
    print()
    
    # 8. 使用过滤器查询模型 / Query models with filter
    print("8. 使用过滤器查询候选模型 / Querying candidate models with filter...")
    filter = ModelFilter(status="candidate")
    candidate_models = registry.list_models(filter=filter)
    print(f"找到 {len(candidate_models)} 个候选模型 / Found {len(candidate_models)} candidate models:")
    for model_info in candidate_models:
        print(f"  - {model_info.model_id}")
        print(f"    IC均值 / IC Mean: {model_info.performance_metrics.get('ic_mean', 0):.4f}")
    print()
    
    # 9. 加载模型 / Load model
    print("9. 加载模型 / Loading model...")
    loaded_model = registry.get_model(model_id1)
    print(f"✓ 模型加载成功 / Model loaded successfully: {loaded_model.name}")
    print(f"  预测测试 / Prediction test: {loaded_model.predict('test_data')}")
    print()
    
    # 10. 获取模型元数据 / Get model metadata
    print("10. 获取模型元数据 / Getting model metadata...")
    metadata = registry.get_model_metadata(model_id1)
    print(f"模型元数据 / Model metadata:")
    print(f"  模型名称 / Model name: {metadata['model_name']}")
    print(f"  版本 / Version: {metadata['version']}")
    print(f"  训练日期 / Training date: {metadata['training_date']}")
    print(f"  性能指标 / Performance metrics: {metadata['performance_metrics']}")
    print()
    
    # 11. 将候选模型提升为生产模型 / Promote candidate to production
    print("11. 将候选模型提升为生产模型 / Promoting candidate to production...")
    if candidate_models:
        best_candidate = candidate_models[0]
        registry.set_production_model(best_candidate.model_id)
        print(f"✓ 模型 {best_candidate.model_id} 已提升为生产模型 / Model promoted to production")
        
        # 验证旧的生产模型已降级 / Verify old production model was demoted
        models = registry.list_models()
        old_prod = next((m for m in models if m.model_id == model_id1), None)
        if old_prod and old_prod.status == "candidate":
            print(f"✓ 旧生产模型 {model_id1} 已降级为候选 / Old production model demoted to candidate")
    print()
    
    print("=" * 80)
    print("演示完成 / Demo completed")
    print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"错误 / Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
