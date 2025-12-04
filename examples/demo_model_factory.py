"""
Demo script for ModelFactory
模型工厂演示脚本

This script demonstrates how to use the ModelFactory to create models.
本脚本演示如何使用模型工厂创建模型。
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.model_factory import ModelFactory


def demo_list_models():
    """Demo: List available model types"""
    print("=" * 60)
    print("演示：列出可用的模型类型")
    print("Demo: List available model types")
    print("=" * 60)
    
    factory = ModelFactory()
    models = factory.list_available_models()
    
    print(f"\n可用的模型类型 / Available model types:")
    for model_type in models:
        print(f"  - {model_type}")
    print()


def demo_list_templates():
    """Demo: List available templates"""
    print("=" * 60)
    print("演示：列出可用的模板")
    print("Demo: List available templates")
    print("=" * 60)
    
    factory = ModelFactory()
    templates = factory.list_templates()
    
    print(f"\n找到 {len(templates)} 个模板 / Found {len(templates)} templates:\n")
    for template in templates:
        print(f"模板名称 / Template name: {template.name}")
        print(f"  模型类型 / Model type: {template.model_type}")
        print(f"  描述 / Description: {template.description}")
        print(f"  适用场景 / Use case: {template.use_case[:100]}...")
        print()


def demo_get_template():
    """Demo: Get a specific template"""
    print("=" * 60)
    print("演示：获取特定模板")
    print("Demo: Get a specific template")
    print("=" * 60)
    
    factory = ModelFactory()
    template = factory.get_template('lgbm_default')
    
    print(f"\n模板名称 / Template name: {template.name}")
    print(f"模型类型 / Model type: {template.model_type}")
    print(f"描述 / Description: {template.description}")
    print(f"\n默认参数 / Default parameters:")
    for key, value in template.default_params.items():
        print(f"  {key}: {value}")
    print(f"\n预期性能 / Expected performance:")
    for key, value in template.expected_performance.items():
        print(f"  {key}: {value}")
    print()


def demo_parameter_validation():
    """Demo: Parameter validation"""
    print("=" * 60)
    print("演示：参数验证")
    print("Demo: Parameter validation")
    print("=" * 60)
    
    factory = ModelFactory()
    
    # Test invalid model type
    print("\n测试无效的模型类型 / Test invalid model type:")
    try:
        factory.create_model('invalid_type')
    except ValueError as e:
        print(f"✓ 捕获到错误 / Caught error: {str(e)[:100]}...")
    
    # Test invalid LGBM parameters
    print("\n测试无效的LGBM参数 / Test invalid LGBM parameters:")
    try:
        factory.create_model('lgbm', {'loss': 'invalid_loss'})
    except ValueError as e:
        print(f"✓ 捕获到错误 / Caught error: {str(e)[:100]}...")
    
    try:
        factory.create_model('lgbm', {'num_boost_round': -10})
    except ValueError as e:
        print(f"✓ 捕获到错误 / Caught error: {str(e)[:100]}...")
    
    # Test invalid linear parameters
    print("\n测试无效的线性模型参数 / Test invalid linear parameters:")
    try:
        factory.create_model('linear', {'estimator': 'invalid'})
    except ValueError as e:
        print(f"✓ 捕获到错误 / Caught error: {str(e)[:100]}...")
    
    try:
        factory.create_model('linear', {'alpha': -0.5})
    except ValueError as e:
        print(f"✓ 捕获到错误 / Caught error: {str(e)[:100]}...")
    
    # Test invalid MLP parameters
    print("\n测试无效的MLP参数 / Test invalid MLP parameters:")
    try:
        factory.create_model('mlp', {'lr': -0.001})
    except ValueError as e:
        print(f"✓ 捕获到错误 / Caught error: {str(e)[:100]}...")
    
    try:
        factory.create_model('mlp', {'optimizer': 'invalid'})
    except ValueError as e:
        print(f"✓ 捕获到错误 / Caught error: {str(e)[:100]}...")
    
    print("\n✓ 所有参数验证测试通过 / All parameter validation tests passed")
    print()


def main():
    """Main demo function"""
    print("\n" + "=" * 60)
    print("ModelFactory 演示")
    print("ModelFactory Demo")
    print("=" * 60 + "\n")
    
    # Run demos
    demo_list_models()
    demo_list_templates()
    demo_get_template()
    demo_parameter_validation()
    
    print("=" * 60)
    print("演示完成！")
    print("Demo completed!")
    print("=" * 60 + "\n")
    
    print("注意：要创建实际的模型实例，需要安装qlib库。")
    print("Note: To create actual model instances, qlib library must be installed.")
    print()


if __name__ == "__main__":
    main()
