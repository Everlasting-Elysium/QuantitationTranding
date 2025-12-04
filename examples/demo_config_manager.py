"""
ConfigManager Demo
演示配置管理器的使用
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.config_manager import ConfigManager


def main():
    """演示配置管理器功能"""
    
    print("=" * 60)
    print("配置管理器演示 (ConfigManager Demo)")
    print("=" * 60)
    
    # 创建配置管理器
    manager = ConfigManager()
    
    # 1. 获取默认配置
    print("\n1. 获取默认配置:")
    print("-" * 60)
    default_config = manager.get_default_config()
    print(f"  Qlib 区域: {default_config.qlib.region}")
    print(f"  MLflow 实验名: {default_config.mlflow.experiment_name}")
    print(f"  数据工具: {default_config.data.instruments}")
    print(f"  日志级别: {default_config.logging.log_level}")
    
    # 2. 保存配置到文件
    print("\n2. 保存配置到文件:")
    print("-" * 60)
    temp_config_path = "/tmp/demo_config.yaml"
    manager.save_config(default_config, temp_config_path)
    print(f"  配置已保存到: {temp_config_path}")
    
    # 3. 从文件加载配置
    print("\n3. 从文件加载配置:")
    print("-" * 60)
    # 创建临时数据目录以通过验证
    os.makedirs("/tmp/qlib_data", exist_ok=True)
    default_config.qlib.provider_uri = "/tmp/qlib_data"
    manager.save_config(default_config, temp_config_path)
    
    loaded_config = manager.load_config(temp_config_path)
    print(f"  配置已从文件加载")
    print(f"  验证: 区域 = {loaded_config.qlib.region}")
    
    # 4. 配置验证
    print("\n4. 配置验证:")
    print("-" * 60)
    errors = manager.validate_config(loaded_config)
    if not errors:
        print("  ✓ 配置验证通过")
    else:
        print("  ✗ 配置验证失败:")
        for error in errors:
            print(f"    - {error}")
    
    # 5. 测试无效配置
    print("\n5. 测试无效配置:")
    print("-" * 60)
    invalid_config = manager.get_default_config()
    invalid_config.logging.log_level = "INVALID_LEVEL"
    invalid_config.qlib.provider_uri = "/tmp/qlib_data"
    errors = manager.validate_config(invalid_config)
    if errors:
        print("  ✓ 成功检测到无效配置:")
        for error in errors:
            print(f"    - {error}")
    
    # 6. 加载实际配置文件
    print("\n6. 加载实际配置文件:")
    print("-" * 60)
    actual_config_path = Path(__file__).parent.parent / "config" / "default_config.yaml"
    if actual_config_path.exists():
        # 创建数据目录以通过验证
        os.makedirs(os.path.expanduser("~/.qlib/qlib_data/cn_data"), exist_ok=True)
        try:
            actual_config = manager.load_config(str(actual_config_path))
            print(f"  ✓ 成功加载配置文件: {actual_config_path}")
            print(f"  训练开始时间: {actual_config.training.train_start}")
            print(f"  训练结束时间: {actual_config.training.train_end}")
            print(f"  回测基准: {actual_config.backtest.benchmark}")
        except Exception as e:
            print(f"  ✗ 加载失败: {e}")
    else:
        print(f"  配置文件不存在: {actual_config_path}")
    
    print("\n" + "=" * 60)
    print("演示完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
