#!/usr/bin/env python
"""
测试错误处理系统 / Test Error Handling System
"""

import sys
sys.path.insert(0, '.')

from src.utils.error_handler import (
    ErrorCategory,
    ErrorSeverity,
    ErrorInfo,
    ConfigurationError,
    DataError,
    get_error_handler
)

def test_error_info():
    """测试错误信息创建"""
    print("测试1: 创建错误信息...")
    error_info = ErrorInfo(
        error_code="TEST0001",
        error_message_zh="这是一个测试错误",
        error_message_en="This is a test error",
        category=ErrorCategory.CONFIGURATION,
        severity=ErrorSeverity.MEDIUM,
        technical_details="Test technical details",
        suggested_actions=["Action 1", "Action 2"],
        recoverable=True
    )
    print(f"✓ 错误代码: {error_info.error_code}")
    print(f"✓ 错误类别: {error_info.category.value}")
    print(f"✓ 严重程度: {error_info.severity.value}")
    print()

def test_error_message():
    """测试错误消息生成"""
    print("测试2: 生成用户友好的错误消息...")
    error_info = ErrorInfo(
        error_code="TEST0002",
        error_message_zh="配置文件不存在",
        error_message_en="Configuration file not found",
        category=ErrorCategory.CONFIGURATION,
        severity=ErrorSeverity.HIGH,
        technical_details="/path/to/config.yaml",
        suggested_actions=[
            "检查文件路径",
            "创建新配置文件"
        ],
        documentation_link="https://example.com/docs",
        recoverable=True
    )
    
    print("中文消息:")
    print(error_info.get_user_message("zh"))
    print("\n英文消息:")
    print(error_info.get_user_message("en"))
    print()

def test_exception():
    """测试异常抛出"""
    print("测试3: 抛出自定义异常...")
    try:
        error_info = ErrorInfo(
            error_code="TEST0003",
            error_message_zh="测试异常",
            error_message_en="Test exception",
            category=ErrorCategory.DATA,
            severity=ErrorSeverity.LOW,
            technical_details="Test exception details",
            suggested_actions=["Fix it"],
            recoverable=False
        )
        raise DataError(error_info)
    except DataError as e:
        print(f"✓ 捕获到异常: {type(e).__name__}")
        print(f"✓ 错误代码: {e.error_info.error_code}")
        print()

def test_error_handler():
    """测试错误处理器"""
    print("测试4: 使用错误处理器...")
    error_handler = get_error_handler()
    
    try:
        # 模拟一个错误
        raise ValueError("这是一个测试错误")
    except Exception as e:
        error_info = error_handler.handle_error(
            error=e,
            context={"test": "context"},
            raise_exception=False
        )
        print(f"✓ 错误已处理: {error_info.error_code}")
        print(f"✓ 错误类别: {error_info.category.value}")
        print()

def test_error_history():
    """测试错误历史"""
    print("测试5: 错误历史记录...")
    error_handler = get_error_handler()
    
    # 清空历史
    error_handler.clear_error_history()
    
    # 添加几个错误
    for i in range(3):
        try:
            raise ValueError(f"测试错误 {i+1}")
        except Exception as e:
            error_handler.handle_error(e, raise_exception=False)
    
    # 获取历史
    history = error_handler.get_error_history()
    print(f"✓ 错误历史记录数: {len(history)}")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("错误处理系统测试 / Error Handling System Test")
    print("=" * 60)
    print()
    
    try:
        test_error_info()
        test_error_message()
        test_exception()
        test_error_handler()
        test_error_history()
        
        print("=" * 60)
        print("✓ 所有测试通过！/ All tests passed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
