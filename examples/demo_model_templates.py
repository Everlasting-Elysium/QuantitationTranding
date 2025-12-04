#!/usr/bin/env python3
"""
Demo script showing how to use the model template system.

This script demonstrates:
1. Loading model templates
2. Listing available templates
3. Retrieving specific templates
4. Accessing template properties
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.templates import ModelTemplateManager


def main():
    """Demonstrate model template usage."""
    
    print("=" * 70)
    print("Model Template System Demo")
    print("=" * 70)
    
    # Initialize the template manager
    print("\n1. Initializing Template Manager...")
    manager = ModelTemplateManager()
    print("   ✓ Template manager initialized")
    
    # List all available templates
    print("\n2. Available Templates:")
    print("-" * 70)
    templates = manager.list_templates()
    for i, template in enumerate(templates, 1):
        print(f"\n   {i}. {template.name}")
        print(f"      Type: {template.model_type}")
        print(f"      Description: {template.description}")
        print(f"      Use Case: {template.use_case[:100]}...")
    
    # Get a specific template
    print("\n3. Retrieving LGBM Default Template:")
    print("-" * 70)
    lgbm_template = manager.get_template("lgbm_default")
    print(f"   Name: {lgbm_template.name}")
    print(f"   Model Type: {lgbm_template.model_type}")
    print(f"   Description: {lgbm_template.description}")
    
    # Show default parameters
    print("\n4. Default Parameters:")
    print("-" * 70)
    for param, value in lgbm_template.default_params.items():
        print(f"   {param}: {value}")
    
    # Show expected performance
    print("\n5. Expected Performance:")
    print("-" * 70)
    for metric, value in lgbm_template.expected_performance.items():
        print(f"   {metric}: {value}")
    
    # Compare different templates
    print("\n6. Comparing Templates:")
    print("-" * 70)
    print(f"{'Template':<25} {'Model Type':<15} {'Expected Return':<20}")
    print("-" * 70)
    for template in templates:
        expected_return = template.expected_performance.get('annual_return', 'N/A')
        print(f"{template.name:<25} {template.model_type:<15} {expected_return:<20}")
    
    # Show how to use template for training
    print("\n7. Using Template for Training:")
    print("-" * 70)
    print("   Example code:")
    print("""
   from src.templates import ModelTemplateManager
   from src.models import TrainingConfig, DatasetConfig
   
   # Get template
   manager = ModelTemplateManager()
   template = manager.get_template("lgbm_default")
   
   # Create training config using template
   dataset_config = DatasetConfig(
       instruments="csi300",
       start_time="2020-01-01",
       end_time="2023-12-31",
       features=["$close", "$volume", "$high", "$low"],
       label="Ref($close, -1) / $close - 1"
   )
   
   training_config = TrainingConfig(
       model_type=template.model_type,
       dataset_config=dataset_config,
       model_params=template.default_params,
       training_params={"epochs": 100},
       experiment_name="my_experiment"
   )
   
   # Now use training_config with TrainingManager
   # training_manager.train_model(training_config)
   """)
    
    print("\n" + "=" * 70)
    print("Demo completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
