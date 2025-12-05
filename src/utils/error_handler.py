"""
错误处理模块 / Error Handling Module
提供统一的错误处理、错误信息中文化、错误恢复逻辑和错误日志记录
Provides unified error handling, Chinese error messages, error recovery logic, and error logging
"""

import traceback
import logging
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass
from enum import Enum
from functools import wraps


class ErrorCategory(Enum):
    """错误类别 / Error Category"""
    CONFIGURATION = "configuration"  # 配置错误
    DATA = "data"  # 数据错误
    TRAINING = "training"  # 训练错误
    BACKTEST = "backtest"  # 回测错误
    SYSTEM = "system"  # 系统错误
    NETWORK = "network"  # 网络错误
    PERMISSION = "permission"  # 权限错误
    VALIDATION = "validation"  # 验证错误
    UNKNOWN = "unknown"  # 未知错误


class ErrorSeverity(Enum):
    """错误严重程度 / Error Severity"""
    LOW = "low"  # 低 - 可以继续运行
    MEDIUM = "medium"  # 中 - 部分功能受影响
    HIGH = "high"  # 高 - 主要功能受影响
    CRITICAL = "critical"  # 严重 - 系统无法继续运行


@dataclass
class ErrorInfo:
    """
    错误信息 / Error Information
    
    包含错误的详细信息，用于统一的错误处理和报告
    Contains detailed error information for unified error handling and reporting
    """
    error_code: str  # 错误代码
    error_message_zh: str  # 中文错误消息
    error_message_en: str  # 英文错误消息
    category: ErrorCategory  # 错误类别
    severity: ErrorSeverity  # 严重程度
    technical_details: str  # 技术细节
    suggested_actions: List[str]  # 建议的解决方案
    documentation_link: Optional[str] = None  # 文档链接
    recoverable: bool = True  # 是否可恢复
    original_exception: Optional[Exception] = None  # 原始异常
    stack_trace: Optional[str] = None  # 堆栈跟踪
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典 / Convert to dictionary"""
        return {
            "error_code": self.error_code,
            "error_message_zh": self.error_message_zh,
            "error_message_en": self.error_message_en,
            "category": self.category.value,
            "severity": self.severity.value,
            "technical_details": self.technical_details,
            "suggested_actions": self.suggested_actions,
            "documentation_link": self.documentation_link,
            "recoverable": self.recoverable,
            "stack_trace": self.stack_trace
        }
    
    def get_user_message(self, language: str = "zh") -> str:
        """
        获取用户友好的错误消息 / Get user-friendly error message
        
        Args:
            language: 语言，"zh"或"en"
            
        Returns:
            str: 格式化的错误消息
        """
        if language == "zh":
            message = f"错误 [{self.error_code}]: {self.error_message_zh}\n"
            if self.suggested_actions:
                message += "\n建议的解决方案:\n"
                for i, action in enumerate(self.suggested_actions, 1):
                    message += f"  {i}. {action}\n"
        else:
            message = f"Error [{self.error_code}]: {self.error_message_en}\n"
            if self.suggested_actions:
                message += "\nSuggested Actions:\n"
                for i, action in enumerate(self.suggested_actions, 1):
                    message += f"  {i}. {action}\n"
        
        if self.documentation_link:
            message += f"\n详细文档 / Documentation: {self.documentation_link}\n"
        
        return message


class QlibTradingError(Exception):
    """
    量化交易系统基础异常类 / Base exception class for Qlib Trading System
    
    所有自定义异常都应继承此类
    All custom exceptions should inherit from this class
    """
    
    def __init__(
        self,
        error_info: ErrorInfo,
        *args,
        **kwargs
    ):
        """
        初始化异常 / Initialize exception
        
        Args:
            error_info: 错误信息对象
        """
        self.error_info = error_info
        super().__init__(error_info.error_message_zh, *args, **kwargs)
    
    def __str__(self) -> str:
        """返回字符串表示 / Return string representation"""
        return self.error_info.get_user_message()


class ConfigurationError(QlibTradingError):
    """配置错误 / Configuration Error"""
    pass


class DataError(QlibTradingError):
    """数据错误 / Data Error"""
    pass


class TrainingError(QlibTradingError):
    """训练错误 / Training Error"""
    pass


class BacktestError(QlibTradingError):
    """回测错误 / Backtest Error"""
    pass


class SystemError(QlibTradingError):
    """系统错误 / System Error"""
    pass


class NetworkError(QlibTradingError):
    """网络错误 / Network Error"""
    pass


class PermissionError(QlibTradingError):
    """权限错误 / Permission Error"""
    pass


class ValidationError(QlibTradingError):
    """验证错误 / Validation Error"""
    pass


class ErrorHandler:
    """
    错误处理器 / Error Handler
    
    提供统一的错误处理、日志记录和错误恢复功能
    Provides unified error handling, logging, and error recovery functionality
    """
    
    def __init__(self):
        """初始化错误处理器 / Initialize error handler"""
        self._logger = logging.getLogger(__name__)
        self._error_history: List[ErrorInfo] = []
        self._max_history_size = 100
        self._recovery_strategies: Dict[str, Callable] = {}
    
    def handle_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        raise_exception: bool = True
    ) -> ErrorInfo:
        """
        处理错误 / Handle error
        
        Args:
            error: 异常对象
            context: 错误上下文信息
            raise_exception: 是否重新抛出异常
            
        Returns:
            ErrorInfo: 错误信息对象
            
        Raises:
            QlibTradingError: 如果raise_exception为True
        """
        # 如果已经是我们的自定义异常，直接使用其错误信息
        if isinstance(error, QlibTradingError):
            error_info = error.error_info
        else:
            # 否则，创建新的错误信息
            error_info = self._create_error_info(error, context)
        
        # 记录错误
        self._log_error(error_info, context)
        
        # 添加到历史记录
        self._add_to_history(error_info)
        
        # 尝试恢复
        if error_info.recoverable:
            self._attempt_recovery(error_info, context)
        
        # 如果需要，重新抛出异常
        if raise_exception:
            raise self._create_exception(error_info)
        
        return error_info
    
    def _create_error_info(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> ErrorInfo:
        """
        创建错误信息对象 / Create error info object
        
        Args:
            error: 异常对象
            context: 错误上下文
            
        Returns:
            ErrorInfo: 错误信息对象
        """
        # 获取堆栈跟踪
        stack_trace = traceback.format_exc()
        
        # 确定错误类别和严重程度
        category, severity = self._categorize_error(error)
        
        # 生成错误代码
        error_code = self._generate_error_code(category, error)
        
        # 生成错误消息
        error_message_zh, error_message_en = self._generate_error_messages(error, context)
        
        # 生成建议的解决方案
        suggested_actions = self._generate_suggested_actions(error, category, context)
        
        # 生成文档链接
        documentation_link = self._generate_documentation_link(category)
        
        # 确定是否可恢复
        recoverable = self._is_recoverable(error, category)
        
        return ErrorInfo(
            error_code=error_code,
            error_message_zh=error_message_zh,
            error_message_en=error_message_en,
            category=category,
            severity=severity,
            technical_details=str(error),
            suggested_actions=suggested_actions,
            documentation_link=documentation_link,
            recoverable=recoverable,
            original_exception=error,
            stack_trace=stack_trace
        )
    
    def _categorize_error(self, error: Exception) -> tuple:
        """
        分类错误 / Categorize error
        
        Args:
            error: 异常对象
            
        Returns:
            tuple: (错误类别, 严重程度)
        """
        error_type = type(error).__name__
        error_message = str(error).lower()
        
        # 根据异常类型和消息内容判断类别
        if "config" in error_message or "yaml" in error_message:
            return ErrorCategory.CONFIGURATION, ErrorSeverity.HIGH
        elif "data" in error_message or "qlib" in error_message:
            return ErrorCategory.DATA, ErrorSeverity.MEDIUM
        elif "train" in error_message or "model" in error_message:
            return ErrorCategory.TRAINING, ErrorSeverity.MEDIUM
        elif "backtest" in error_message:
            return ErrorCategory.BACKTEST, ErrorSeverity.MEDIUM
        elif "network" in error_message or "connection" in error_message:
            return ErrorCategory.NETWORK, ErrorSeverity.LOW
        elif "permission" in error_message or "access" in error_message:
            return ErrorCategory.PERMISSION, ErrorSeverity.HIGH
        elif "validation" in error_message or "invalid" in error_message:
            return ErrorCategory.VALIDATION, ErrorSeverity.MEDIUM
        elif isinstance(error, (OSError, IOError)):
            return ErrorCategory.SYSTEM, ErrorSeverity.HIGH
        else:
            return ErrorCategory.UNKNOWN, ErrorSeverity.MEDIUM
    
    def _generate_error_code(self, category: ErrorCategory, error: Exception) -> str:
        """
        生成错误代码 / Generate error code
        
        Args:
            category: 错误类别
            error: 异常对象
            
        Returns:
            str: 错误代码
        """
        category_prefix = {
            ErrorCategory.CONFIGURATION: "CFG",
            ErrorCategory.DATA: "DAT",
            ErrorCategory.TRAINING: "TRN",
            ErrorCategory.BACKTEST: "BCK",
            ErrorCategory.SYSTEM: "SYS",
            ErrorCategory.NETWORK: "NET",
            ErrorCategory.PERMISSION: "PRM",
            ErrorCategory.VALIDATION: "VAL",
            ErrorCategory.UNKNOWN: "UNK"
        }
        
        prefix = category_prefix.get(category, "UNK")
        error_hash = abs(hash(str(error))) % 10000
        
        return f"{prefix}{error_hash:04d}"
    
    def _generate_error_messages(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> tuple:
        """
        生成中英文错误消息 / Generate Chinese and English error messages
        
        Args:
            error: 异常对象
            context: 错误上下文
            
        Returns:
            tuple: (中文消息, 英文消息)
        """
        error_type = type(error).__name__
        error_message = str(error)
        
        # 中文消息
        zh_message = f"{error_type}: {error_message}"
        
        # 英文消息
        en_message = f"{error_type}: {error_message}"
        
        # 添加上下文信息
        if context:
            context_str = ", ".join([f"{k}={v}" for k, v in context.items()])
            zh_message += f" (上下文: {context_str})"
            en_message += f" (Context: {context_str})"
        
        return zh_message, en_message
    
    def _generate_suggested_actions(
        self,
        error: Exception,
        category: ErrorCategory,
        context: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        生成建议的解决方案 / Generate suggested actions
        
        Args:
            error: 异常对象
            category: 错误类别
            context: 错误上下文
            
        Returns:
            List[str]: 建议的解决方案列表
        """
        actions = []
        
        if category == ErrorCategory.CONFIGURATION:
            actions.extend([
                "检查配置文件格式是否正确",
                "验证所有必需的配置项是否存在",
                "确认配置文件路径是否正确"
            ])
        elif category == ErrorCategory.DATA:
            actions.extend([
                "检查数据路径是否存在",
                "验证数据文件是否完整",
                "尝试重新下载数据",
                "检查数据时间范围是否正确"
            ])
        elif category == ErrorCategory.TRAINING:
            actions.extend([
                "检查模型参数是否合理",
                "验证训练数据是否充足",
                "尝试减小批次大小或模型复杂度",
                "检查是否有足够的内存"
            ])
        elif category == ErrorCategory.BACKTEST:
            actions.extend([
                "检查回测时间范围是否有效",
                "验证模型是否已正确加载",
                "确认策略配置是否正确"
            ])
        elif category == ErrorCategory.NETWORK:
            actions.extend([
                "检查网络连接是否正常",
                "稍后重试",
                "检查防火墙设置"
            ])
        elif category == ErrorCategory.PERMISSION:
            actions.extend([
                "检查文件或目录权限",
                "以管理员权限运行",
                "确认有足够的磁盘空间"
            ])
        elif category == ErrorCategory.VALIDATION:
            actions.extend([
                "检查输入参数是否符合要求",
                "验证数据格式是否正确",
                "查看文档了解正确的使用方法"
            ])
        else:
            actions.extend([
                "查看详细的错误日志",
                "检查系统环境是否正确配置",
                "联系技术支持"
            ])
        
        return actions
    
    def _generate_documentation_link(self, category: ErrorCategory) -> Optional[str]:
        """
        生成文档链接 / Generate documentation link
        
        Args:
            category: 错误类别
            
        Returns:
            Optional[str]: 文档链接
        """
        base_url = "https://github.com/your-repo/docs"
        
        doc_links = {
            ErrorCategory.CONFIGURATION: f"{base_url}/configuration.md",
            ErrorCategory.DATA: f"{base_url}/data_management.md",
            ErrorCategory.TRAINING: f"{base_url}/training.md",
            ErrorCategory.BACKTEST: f"{base_url}/backtest.md",
            ErrorCategory.SYSTEM: f"{base_url}/troubleshooting.md",
        }
        
        return doc_links.get(category)
    
    def _is_recoverable(self, error: Exception, category: ErrorCategory) -> bool:
        """
        判断错误是否可恢复 / Determine if error is recoverable
        
        Args:
            error: 异常对象
            category: 错误类别
            
        Returns:
            bool: 是否可恢复
        """
        # 网络错误通常可恢复
        if category == ErrorCategory.NETWORK:
            return True
        
        # 验证错误通常可恢复（用户可以重新输入）
        if category == ErrorCategory.VALIDATION:
            return True
        
        # 某些数据错误可恢复（可以重新下载）
        if category == ErrorCategory.DATA:
            error_message = str(error).lower()
            if "not found" in error_message or "missing" in error_message:
                return True
        
        # 其他错误默认不可恢复
        return False
    
    def _log_error(
        self,
        error_info: ErrorInfo,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        记录错误日志 / Log error
        
        Args:
            error_info: 错误信息对象
            context: 错误上下文
        """
        log_message = (
            f"错误发生 / Error Occurred:\n"
            f"  错误代码 / Error Code: {error_info.error_code}\n"
            f"  类别 / Category: {error_info.category.value}\n"
            f"  严重程度 / Severity: {error_info.severity.value}\n"
            f"  消息 / Message: {error_info.error_message_zh}\n"
            f"  技术细节 / Technical Details: {error_info.technical_details}\n"
        )
        
        if context:
            log_message += f"  上下文 / Context: {context}\n"
        
        # 根据严重程度选择日志级别
        if error_info.severity == ErrorSeverity.CRITICAL:
            self._logger.critical(log_message)
            if error_info.stack_trace:
                self._logger.critical(f"堆栈跟踪 / Stack Trace:\n{error_info.stack_trace}")
        elif error_info.severity == ErrorSeverity.HIGH:
            self._logger.error(log_message)
            if error_info.stack_trace:
                self._logger.error(f"堆栈跟踪 / Stack Trace:\n{error_info.stack_trace}")
        elif error_info.severity == ErrorSeverity.MEDIUM:
            self._logger.warning(log_message)
        else:
            self._logger.info(log_message)
    
    def _add_to_history(self, error_info: ErrorInfo) -> None:
        """
        添加到错误历史记录 / Add to error history
        
        Args:
            error_info: 错误信息对象
        """
        self._error_history.append(error_info)
        
        # 限制历史记录大小
        if len(self._error_history) > self._max_history_size:
            self._error_history = self._error_history[-self._max_history_size:]
    
    def _attempt_recovery(
        self,
        error_info: ErrorInfo,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        尝试错误恢复 / Attempt error recovery
        
        Args:
            error_info: 错误信息对象
            context: 错误上下文
            
        Returns:
            bool: 恢复是否成功
        """
        if not error_info.recoverable:
            return False
        
        # 查找恢复策略
        recovery_key = f"{error_info.category.value}_{error_info.error_code}"
        recovery_strategy = self._recovery_strategies.get(recovery_key)
        
        if recovery_strategy:
            try:
                self._logger.info(f"尝试恢复错误: {error_info.error_code}")
                recovery_strategy(error_info, context)
                self._logger.info(f"错误恢复成功: {error_info.error_code}")
                return True
            except Exception as e:
                self._logger.error(f"错误恢复失败: {error_info.error_code}, 原因: {str(e)}")
                return False
        
        return False
    
    def _create_exception(self, error_info: ErrorInfo) -> QlibTradingError:
        """
        创建异常对象 / Create exception object
        
        Args:
            error_info: 错误信息对象
            
        Returns:
            QlibTradingError: 异常对象
        """
        exception_classes = {
            ErrorCategory.CONFIGURATION: ConfigurationError,
            ErrorCategory.DATA: DataError,
            ErrorCategory.TRAINING: TrainingError,
            ErrorCategory.BACKTEST: BacktestError,
            ErrorCategory.SYSTEM: SystemError,
            ErrorCategory.NETWORK: NetworkError,
            ErrorCategory.PERMISSION: PermissionError,
            ErrorCategory.VALIDATION: ValidationError,
        }
        
        exception_class = exception_classes.get(error_info.category, QlibTradingError)
        return exception_class(error_info)
    
    def register_recovery_strategy(
        self,
        category: ErrorCategory,
        error_code: str,
        strategy: Callable
    ) -> None:
        """
        注册错误恢复策略 / Register error recovery strategy
        
        Args:
            category: 错误类别
            error_code: 错误代码
            strategy: 恢复策略函数
        """
        recovery_key = f"{category.value}_{error_code}"
        self._recovery_strategies[recovery_key] = strategy
        self._logger.info(f"注册恢复策略: {recovery_key}")
    
    def get_error_history(self, limit: Optional[int] = None) -> List[ErrorInfo]:
        """
        获取错误历史记录 / Get error history
        
        Args:
            limit: 返回的最大记录数
            
        Returns:
            List[ErrorInfo]: 错误历史记录列表
        """
        if limit:
            return self._error_history[-limit:]
        return self._error_history.copy()
    
    def clear_error_history(self) -> None:
        """清空错误历史记录 / Clear error history"""
        self._error_history.clear()
        self._logger.info("错误历史记录已清空")


# 全局错误处理器实例
_error_handler = ErrorHandler()


def get_error_handler() -> ErrorHandler:
    """
    获取全局错误处理器实例 / Get global error handler instance
    
    Returns:
        ErrorHandler: 错误处理器实例
    """
    return _error_handler


def handle_error(
    error: Exception,
    context: Optional[Dict[str, Any]] = None,
    raise_exception: bool = True
) -> ErrorInfo:
    """
    便捷函数：处理错误 / Convenience function: Handle error
    
    Args:
        error: 异常对象
        context: 错误上下文
        raise_exception: 是否重新抛出异常
        
    Returns:
        ErrorInfo: 错误信息对象
    """
    return _error_handler.handle_error(error, context, raise_exception)


def error_handler_decorator(
    context_func: Optional[Callable] = None,
    raise_exception: bool = True
):
    """
    错误处理装饰器 / Error handler decorator
    
    用于自动处理函数中的异常
    Used to automatically handle exceptions in functions
    
    Args:
        context_func: 用于生成上下文信息的函数
        raise_exception: 是否重新抛出异常
        
    Example:
        @error_handler_decorator()
        def my_function():
            # Your code here
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # 生成上下文
                context = {}
                if context_func:
                    context = context_func(*args, **kwargs)
                else:
                    context = {
                        "function": func.__name__,
                        "args": str(args)[:100],  # 限制长度
                        "kwargs": str(kwargs)[:100]
                    }
                
                # 处理错误
                return handle_error(e, context, raise_exception)
        
        return wrapper
    return decorator
