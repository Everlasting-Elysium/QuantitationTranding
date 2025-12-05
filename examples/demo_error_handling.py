#!/usr/bin/env python
"""
错误处理系统示例 / Error Handling System Example

演示如何在实际代码中使用统一的错误处理系统
Demonstrates how to use the unified error handling system in actual code
"""

import sys
sys.path.insert(0, '.')

from src.utils.error_handler import (
    ConfigurationError,
    DataError,
    ErrorInfo,
    ErrorCategory,
    ErrorSeverity,
    get_error_handler,
    error_handler_decorator
)
from src.infrastructure.logger_system import setup_logging


def example_1_basic_error():
    """
    示例1: 基本错误处理
    Example 1: Basic error handling
    """
    print("\n" + "=" * 60)
    print("示例1: 基本错误处理 / Example 1: Basic Error Handling")
    print("=" * 60)
    
    try:
        # 模拟配置文件不存在的错误
        config_path = "/path/to/nonexistent/config.yaml"
        
        error_info = ErrorInfo(
            error_code="CFG0001",
            error_message_zh=f"配置文件不存在: {config_path}",
            error_message_en=f"Configuration file not found: {config_path}",
            category=ErrorCategory.CONFIGURATION,
            severity=ErrorSeverity.HIGH,
            technical_details=f"Attempted to load: {config_path}",
            suggested_actions=[
                "检查配置文件路径是否正确",
                "使用 get_default_config() 创建默认配置",
                "参考文档: https://docs.example.com/config"
            ],
            recoverable=True
        )
        
        raise ConfigurationError(error_info)
        
    except ConfigurationError as e:
        print("\n捕获到配置错误:")
        print(e.error_info.get_user_message("zh"))


def example_2_error_handler():
    """
    示例2: 使用错误处理器
    Example 2: Using error handler
    """
    print("\n" + "=" * 60)
    print("示例2: 使用错误处理器 / Example 2: Using Error Handler")
    print("=" * 60)
    
    error_handler = get_error_handler()
    
    try:
        # 模拟数据加载错误
        raise FileNotFoundError("数据文件不存在: data.csv")
        
    except Exception as e:
        # 使用错误处理器处理异常
        error_info = error_handler.handle_error(
            error=e,
            context={
                "operation": "load_data",
                "file": "data.csv",
                "user": "demo_user"
            },
            raise_exception=False  # 不重新抛出异常
        )
        
        print(f"\n错误已处理:")
        print(f"  错误代码: {error_info.error_code}")
        print(f"  错误类别: {error_info.category.value}")
        print(f"  是否可恢复: {error_info.recoverable}")


@error_handler_decorator()
def example_3_with_decorator():
    """
    示例3: 使用装饰器自动处理错误
    Example 3: Using decorator for automatic error handling
    """
    print("\n" + "=" * 60)
    print("示例3: 使用装饰器 / Example 3: Using Decorator")
    print("=" * 60)
    
    # 这个函数会自动处理异常
    print("\n执行可能出错的操作...")
    raise ValueError("这是一个测试错误")


def example_4_error_recovery():
    """
    示例4: 错误恢复策略
    Example 4: Error recovery strategy
    """
    print("\n" + "=" * 60)
    print("示例4: 错误恢复策略 / Example 4: Error Recovery Strategy")
    print("=" * 60)
    
    error_handler = get_error_handler()
    
    # 定义恢复策略
    def network_recovery(error_info, context):
        print(f"\n执行网络错误恢复策略...")
        print(f"  重试次数: {context.get('retry_count', 0) + 1}")
        print(f"  等待时间: 5秒")
        # 实际应用中，这里会执行重试逻辑
    
    # 注册恢复策略
    error_handler.register_recovery_strategy(
        category=ErrorCategory.NETWORK,
        error_code="NET0001",
        strategy=network_recovery
    )
    
    print("\n恢复策略已注册")
    print("当发生 NET0001 错误时，系统会自动尝试恢复")


def example_5_error_history():
    """
    示例5: 错误历史记录
    Example 5: Error history
    """
    print("\n" + "=" * 60)
    print("示例5: 错误历史记录 / Example 5: Error History")
    print("=" * 60)
    
    error_handler = get_error_handler()
    
    # 获取错误历史
    history = error_handler.get_error_history(limit=5)
    
    print(f"\n最近的错误记录 (共 {len(history)} 条):")
    for i, error_info in enumerate(history, 1):
        print(f"\n{i}. 错误代码: {error_info.error_code}")
        print(f"   类别: {error_info.category.value}")
        print(f"   严重程度: {error_info.severity.value}")
        print(f"   消息: {error_info.error_message_zh}")


def example_6_multilingual():
    """
    示例6: 多语言支持
    Example 6: Multilingual support
    """
    print("\n" + "=" * 60)
    print("示例6: 多语言支持 / Example 6: Multilingual Support")
    print("=" * 60)
    
    error_info = ErrorInfo(
        error_code="DAT0001",
        error_message_zh="数据验证失败：缺少必需字段",
        error_message_en="Data validation failed: Missing required fields",
        category=ErrorCategory.DATA,
        severity=ErrorSeverity.MEDIUM,
        technical_details="Required fields: ['name', 'age', 'email']",
        suggested_actions=[
            "检查输入数据是否完整",
            "参考数据格式文档",
            "使用数据验证工具"
        ],
        recoverable=True
    )
    
    print("\n中文错误消息:")
    print(error_info.get_user_message("zh"))
    
    print("\n英文错误消息:")
    print(error_info.get_user_message("en"))


def main():
    """主函数 / Main function"""
    print("\n" + "=" * 70)
    print("错误处理系统示例程序 / Error Handling System Example Program")
    print("=" * 70)
    
    # 设置日志系统
    setup_logging(log_dir="./logs", log_level="INFO")
    
    try:
        # 运行所有示例
        example_1_basic_error()
        example_2_error_handler()
        
        # 示例3会抛出异常，我们捕获它
        try:
            example_3_with_decorator()
        except Exception as e:
            print(f"\n装饰器捕获到异常: {type(e).__name__}")
        
        example_4_error_recovery()
        example_5_error_history()
        example_6_multilingual()
        
        print("\n" + "=" * 70)
        print("所有示例执行完成！/ All examples completed!")
        print("=" * 70)
        print("\n提示: 查看 ./logs/qlib_trading.log 了解详细的错误日志")
        print("Tip: Check ./logs/qlib_trading.log for detailed error logs")
        
    except Exception as e:
        print(f"\n程序执行出错: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
