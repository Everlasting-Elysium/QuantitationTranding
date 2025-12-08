#!/usr/bin/env python
"""
验证训练流程 / Verify Training Pipeline
检查所有训练流程相关的组件是否正常工作
Check if all training pipeline components are working properly
"""

import sys
from pathlib import Path

def check_imports():
    """检查所有必要的导入 / Check all necessary imports"""
    print("=" * 60)
    print("检查导入 / Checking imports...")
    print("=" * 60)
    
    try:
        # 基础设施层 / Infrastructure layer
        from src.infrastructure.qlib_wrapper import QlibWrapper
        print("✓ QlibWrapper 导入成功 / imported successfully")
        
        from src.infrastructure.mlflow_tracker import MLflowTracker
        print("✓ MLflowTracker 导入成功 / imported successfully")
        
        from src.infrastructure.logger_system import LoggerSystem
        print("✓ LoggerSystem 导入成功 / imported successfully")
        
        # 核心层 / Core layer
        from src.core.config_manager import ConfigManager
        print("✓ ConfigManager 导入成功 / imported successfully")
        
        from src.core.data_manager import DataManager
        print("✓ DataManager 导入成功 / imported successfully")
        
        from src.core.model_factory import ModelFactory
        print("✓ ModelFactory 导入成功 / imported successfully")
        
        # 应用层 / Application layer
        from src.application.training_manager import TrainingManager
        print("✓ TrainingManager 导入成功 / imported successfully")
        
        from src.application.model_registry import ModelRegistry
        print("✓ ModelRegistry 导入成功 / imported successfully")
        
        # 模板 / Templates
        from src.templates.model_templates import ModelTemplateManager
        print("✓ ModelTemplateManager 导入成功 / imported successfully")
        
        print("\n所有导入检查通过！/ All imports passed!\n")
        return True
        
    except ImportError as e:
        print(f"\n✗ 导入失败 / Import failed: {e}\n")
        return False

def check_component_initialization():
    """检查组件初始化 / Check component initialization"""
    print("=" * 60)
    print("检查组件初始化 / Checking component initialization...")
    print("=" * 60)
    
    try:
        from src.infrastructure.logger_system import LoggerSystem
        from src.core.config_manager import ConfigManager
        from src.core.model_factory import ModelFactory
        from src.application.model_registry import ModelRegistry
        from src.templates.model_templates import ModelTemplateManager
        
        # 1. 日志系统 / Logger system
        logger_system = LoggerSystem()
        logger_system.setup(log_dir="./logs", log_level="INFO")
        print("✓ LoggerSystem 初始化成功 / initialized successfully")
        
        # 2. 配置管理器 / Config manager
        config_manager = ConfigManager()
        config = config_manager.get_default_config()
        print("✓ ConfigManager 初始化成功 / initialized successfully")
        
        # 3. 模板管理器 / Template manager
        template_manager = ModelTemplateManager()
        templates = template_manager.list_templates()
        print(f"✓ ModelTemplateManager 初始化成功，找到 {len(templates)} 个模板 / initialized successfully, found {len(templates)} templates")
        
        # 4. 模型工厂 / Model factory
        model_factory = ModelFactory(template_manager=template_manager)
        available_models = model_factory.list_available_models()
        print(f"✓ ModelFactory 初始化成功，支持 {len(available_models)} 种模型 / initialized successfully, supports {len(available_models)} model types")
        
        # 5. 模型注册表 / Model registry
        model_registry = ModelRegistry(registry_dir="./test_registry")
        print("✓ ModelRegistry 初始化成功 / initialized successfully")
        
        print("\n所有组件初始化检查通过！/ All component initialization checks passed!\n")
        return True
        
    except Exception as e:
        print(f"\n✗ 组件初始化失败 / Component initialization failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False

def check_training_pipeline_structure():
    """检查训练流程结构 / Check training pipeline structure"""
    print("=" * 60)
    print("检查训练流程结构 / Checking training pipeline structure...")
    print("=" * 60)
    
    try:
        from src.application.training_manager import (
            TrainingManager, 
            TrainingConfig, 
            DatasetConfig,
            TrainingResult
        )
        
        # 检查数据类 / Check data classes
        print("✓ DatasetConfig 数据类存在 / dataclass exists")
        print("✓ TrainingConfig 数据类存在 / dataclass exists")
        print("✓ TrainingResult 数据类存在 / dataclass exists")
        
        # 检查TrainingManager方法 / Check TrainingManager methods
        required_methods = [
            'train_model',
            'train_from_template',
        ]
        
        for method in required_methods:
            if hasattr(TrainingManager, method):
                print(f"✓ TrainingManager.{method} 方法存在 / method exists")
            else:
                print(f"✗ TrainingManager.{method} 方法缺失 / method missing")
                return False
        
        print("\n训练流程结构检查通过！/ Training pipeline structure check passed!\n")
        return True
        
    except Exception as e:
        print(f"\n✗ 训练流程结构检查失败 / Training pipeline structure check failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数 / Main function"""
    print("\n" + "=" * 60)
    print("训练流程验证脚本 / Training Pipeline Verification Script")
    print("=" * 60 + "\n")
    
    all_passed = True
    
    # 1. 检查导入 / Check imports
    if not check_imports():
        all_passed = False
    
    # 2. 检查组件初始化 / Check component initialization
    if not check_component_initialization():
        all_passed = False
    
    # 3. 检查训练流程结构 / Check training pipeline structure
    if not check_training_pipeline_structure():
        all_passed = False
    
    # 总结 / Summary
    print("=" * 60)
    if all_passed:
        print("✓ 所有检查通过！训练流程准备就绪。")
        print("✓ All checks passed! Training pipeline is ready.")
        print("=" * 60 + "\n")
        return 0
    else:
        print("✗ 部分检查失败，请查看上面的错误信息。")
        print("✗ Some checks failed, please review the error messages above.")
        print("=" * 60 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
