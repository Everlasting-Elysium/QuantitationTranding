#!/usr/bin/env python3
"""
训练功能CLI演示 / Training CLI Demo

This script demonstrates the training CLI functionality.
本脚本演示训练CLI功能。

注意：这是一个演示脚本，展示如何使用训练功能CLI。
Note: This is a demo script showing how to use the training CLI.
"""

import sys
from pathlib import Path

# 添加src目录到路径 / Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def demo_template_listing():
    """
    演示模板列表功能 / Demo template listing functionality
    """
    print("\n" + "=" * 70)
    print("📋 演示：模板列表功能 / Demo: Template Listing Functionality")
    print("=" * 70)
    print()
    
    from src.core.model_factory import ModelFactory
    
    factory = ModelFactory()
    templates = factory.list_templates()
    
    print(f"系统中共有 {len(templates)} 个预配置模板")
    print(f"There are {len(templates)} pre-configured templates in the system")
    print()
    
    for i, template in enumerate(templates, 1):
        print(f"{i}. {template.name}")
        print(f"   模型类型 / Model Type: {template.model_type}")
        print(f"   描述 / Description: {template.description[:100]}...")
        print()


def demo_training_workflow():
    """
    演示训练工作流程 / Demo training workflow
    """
    print("\n" + "=" * 70)
    print("🎓 演示：训练工作流程 / Demo: Training Workflow")
    print("=" * 70)
    print()
    
    print("训练工作流程包括以下步骤：")
    print("The training workflow includes the following steps:")
    print()
    
    steps = [
        ("1. 选择训练方式", "1. Select training method"),
        ("   - 使用模型模板训练", "   - Train with model template"),
        ("   - 自定义参数训练", "   - Train with custom parameters"),
        ("", ""),
        ("2. 选择模型模板", "2. Select model template"),
        ("   - 查看可用模板列表", "   - View available template list"),
        ("   - 查看模板详细信息", "   - View template details"),
        ("   - 选择合适的模板", "   - Select appropriate template"),
        ("", ""),
        ("3. 配置数据集", "3. Configure dataset"),
        ("   - 选择股票池（如csi300）", "   - Select stock pool (e.g., csi300)"),
        ("   - 设置时间范围", "   - Set time range"),
        ("   - 配置特征和标签", "   - Configure features and labels"),
        ("", ""),
        ("4. 自定义参数（可选）", "4. Customize parameters (optional)"),
        ("   - 调整模型参数", "   - Adjust model parameters"),
        ("   - 修改训练参数", "   - Modify training parameters"),
        ("", ""),
        ("5. 确认并开始训练", "5. Confirm and start training"),
        ("   - 查看配置总结", "   - Review configuration summary"),
        ("   - 确认开始训练", "   - Confirm to start training"),
        ("   - 监控训练进度", "   - Monitor training progress"),
        ("", ""),
        ("6. 查看训练结果", "6. View training results"),
        ("   - 查看评估指标", "   - View evaluation metrics"),
        ("   - 查看模型路径", "   - View model path"),
        ("   - 查看MLflow记录", "   - View MLflow records"),
    ]
    
    for cn, en in steps:
        if cn:
            print(f"{cn}")
            print(f"{en}")
        else:
            print()


def demo_training_features():
    """
    演示训练功能特性 / Demo training features
    """
    print("\n" + "=" * 70)
    print("✨ 演示：训练功能特性 / Demo: Training Features")
    print("=" * 70)
    print()
    
    features = [
        {
            "title": "模板选择界面 / Template Selection Interface",
            "description": "提供多个预配置模板，每个模板都有详细的描述和适用场景",
            "description_en": "Provides multiple pre-configured templates with detailed descriptions and use cases"
        },
        {
            "title": "交互式参数配置 / Interactive Parameter Configuration",
            "description": "通过问答方式收集训练参数，无需编写代码",
            "description_en": "Collects training parameters through Q&A, no coding required"
        },
        {
            "title": "实时进度显示 / Real-time Progress Display",
            "description": "显示训练进度和状态信息，让用户了解训练进展",
            "description_en": "Displays training progress and status information to keep users informed"
        },
        {
            "title": "详细结果展示 / Detailed Results Display",
            "description": "训练完成后展示评估指标、模型路径等详细信息",
            "description_en": "Shows evaluation metrics, model path and other details after training"
        },
        {
            "title": "MLflow集成 / MLflow Integration",
            "description": "自动记录训练过程到MLflow，方便后续分析和对比",
            "description_en": "Automatically logs training process to MLflow for analysis and comparison"
        },
        {
            "title": "错误处理 / Error Handling",
            "description": "提供友好的错误提示和恢复机制",
            "description_en": "Provides friendly error messages and recovery mechanisms"
        },
    ]
    
    for i, feature in enumerate(features, 1):
        print(f"{i}. {feature['title']}")
        print(f"   {feature['description']}")
        print(f"   {feature['description_en']}")
        print()


def demo_usage_example():
    """
    演示使用示例 / Demo usage example
    """
    print("\n" + "=" * 70)
    print("💡 演示：使用示例 / Demo: Usage Example")
    print("=" * 70)
    print()
    
    print("要使用训练功能CLI，请按照以下步骤操作：")
    print("To use the training CLI, follow these steps:")
    print()
    
    print("1. 启动主CLI / Start main CLI:")
    print("   python main.py")
    print()
    
    print("2. 在主菜单中选择 '1. 模型训练' / Select '1. Model Training' in main menu")
    print()
    
    print("3. 选择训练方式 / Select training method:")
    print("   - 选项1：使用模型模板训练（推荐）")
    print("   - Option 1: Train with model template (recommended)")
    print("   - 选项2：自定义参数训练（高级）")
    print("   - Option 2: Train with custom parameters (advanced)")
    print()
    
    print("4. 按照提示输入参数 / Follow prompts to enter parameters:")
    print("   - 选择模型模板 / Select model template")
    print("   - 选择股票池 / Select stock pool")
    print("   - 设置时间范围 / Set time range")
    print("   - 输入实验名称 / Enter experiment name")
    print()
    
    print("5. 确认配置并开始训练 / Confirm configuration and start training")
    print()
    
    print("6. 等待训练完成并查看结果 / Wait for training to complete and view results")
    print()


def demo_tips_and_tricks():
    """
    演示技巧和提示 / Demo tips and tricks
    """
    print("\n" + "=" * 70)
    print("💡 演示：技巧和提示 / Demo: Tips and Tricks")
    print("=" * 70)
    print()
    
    tips = [
        {
            "title": "选择合适的模板 / Choose the Right Template",
            "tip": "根据你的投资风格和风险偏好选择模板",
            "tip_en": "Choose template based on your investment style and risk preference",
            "details": [
                "- 保守型：lgbm_conservative",
                "- 稳健型：lgbm_default",
                "- 进取型：lgbm_aggressive"
            ]
        },
        {
            "title": "合理设置时间范围 / Set Reasonable Time Range",
            "tip": "建议使用至少2年的历史数据进行训练",
            "tip_en": "Recommend using at least 2 years of historical data for training",
            "details": [
                "- 训练集：2-3年历史数据",
                "- Training set: 2-3 years historical data",
                "- 避免使用过短的时间范围",
                "- Avoid using too short time range"
            ]
        },
        {
            "title": "使用MLflow追踪 / Use MLflow Tracking",
            "tip": "训练完成后可以使用MLflow UI查看详细记录",
            "tip_en": "After training, use MLflow UI to view detailed records",
            "details": [
                "- 运行命令：mlflow ui",
                "- Run command: mlflow ui",
                "- 在浏览器中打开 http://localhost:5000",
                "- Open http://localhost:5000 in browser"
            ]
        },
        {
            "title": "实验命名规范 / Experiment Naming Convention",
            "tip": "使用有意义的实验名称，方便后续查找",
            "tip_en": "Use meaningful experiment names for easy lookup",
            "details": [
                "- 包含模型类型和日期",
                "- Include model type and date",
                "- 例如：lgbm_csi300_20240101",
                "- Example: lgbm_csi300_20240101"
            ]
        },
    ]
    
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip['title']}")
        print(f"   {tip['tip']}")
        print(f"   {tip['tip_en']}")
        for detail in tip['details']:
            print(f"   {detail}")
        print()


def main():
    """
    运行所有演示 / Run all demos
    """
    print("\n" + "=" * 70)
    print("🎬 训练功能CLI演示 / Training CLI Demo")
    print("=" * 70)
    print()
    print("本演示将展示训练功能CLI的各项功能和使用方法")
    print("This demo will showcase the features and usage of training CLI")
    
    demos = [
        ("模板列表功能", "Template Listing", demo_template_listing),
        ("训练工作流程", "Training Workflow", demo_training_workflow),
        ("训练功能特性", "Training Features", demo_training_features),
        ("使用示例", "Usage Example", demo_usage_example),
        ("技巧和提示", "Tips and Tricks", demo_tips_and_tricks),
    ]
    
    for cn_name, en_name, demo_func in demos:
        try:
            demo_func()
            input(f"\n按回车键继续下一个演示... / Press Enter to continue to next demo...")
        except KeyboardInterrupt:
            print("\n\n演示已中断 / Demo interrupted")
            break
        except Exception as e:
            print(f"\n❌ 演示 '{cn_name}' 发生错误 / Demo '{cn_name}' error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("🎉 演示完成！ / Demo Completed!")
    print("=" * 70)
    print()
    print("感谢观看！现在你可以开始使用训练功能CLI了。")
    print("Thank you for watching! Now you can start using the training CLI.")
    print()
    print("要启动系统，请运行：python main.py")
    print("To start the system, run: python main.py")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 再见！ / Goodbye!")
    except Exception as e:
        print(f"\n❌ 发生错误 / Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
