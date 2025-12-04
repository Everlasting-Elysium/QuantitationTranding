"""
日志系统模块
提供统一的日志记录、日志轮转和日志级别管理功能
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


class LoggerSystem:
    """
    日志系统类
    
    职责:
    - 配置日志系统
    - 提供日志记录器
    - 管理日志文件轮转
    """
    
    _instance: Optional['LoggerSystem'] = None
    _initialized: bool = False
    
    def __new__(cls):
        """单例模式实现"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化日志系统（仅在首次创建时执行）"""
        # 避免重复初始化
        if LoggerSystem._initialized:
            return
        
        self.log_dir: Optional[Path] = None
        self.log_level: str = "INFO"
        self.log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self.max_bytes: int = 10485760  # 10MB
        self.backup_count: int = 5
        self._loggers: dict = {}
        
    def setup(
        self,
        log_dir: str,
        log_level: str = "INFO",
        log_format: Optional[str] = None,
        max_bytes: int = 10485760,
        backup_count: int = 5
    ) -> None:
        """
        配置日志系统
        
        Args:
            log_dir: 日志文件目录
            log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_format: 日志格式字符串
            max_bytes: 单个日志文件最大字节数
            backup_count: 保留的备份日志文件数量
        """
        self.log_dir = Path(log_dir)
        self.log_level = log_level.upper()
        if log_format:
            self.log_format = log_format
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        
        # 创建日志目录
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 配置根日志记录器
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, self.log_level))
        
        # 清除现有的处理器
        root_logger.handlers.clear()
        
        # 添加控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, self.log_level))
        console_formatter = logging.Formatter(self.log_format)
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
        
        # 添加文件处理器（带轮转）
        log_file = self.log_dir / "qlib_trading.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, self.log_level))
        file_formatter = logging.Formatter(self.log_format)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
        
        LoggerSystem._initialized = True
        
        # 记录初始化信息
        logger = self.get_logger("LoggerSystem")
        logger.info(f"日志系统初始化完成 - 日志目录: {self.log_dir}, 日志级别: {self.log_level}")
    
    def get_logger(self, name: str) -> logging.Logger:
        """
        获取指定名称的日志记录器
        
        Args:
            name: 日志记录器名称（通常使用模块名）
            
        Returns:
            logging.Logger: 配置好的日志记录器
        """
        if name not in self._loggers:
            logger = logging.getLogger(name)
            self._loggers[name] = logger
        
        return self._loggers[name]
    
    def rotate_logs(self) -> None:
        """
        手动触发日志轮转
        
        遍历所有RotatingFileHandler并触发轮转检查
        """
        root_logger = logging.getLogger()
        for handler in root_logger.handlers:
            if isinstance(handler, RotatingFileHandler):
                handler.doRollover()
        
        logger = self.get_logger("LoggerSystem")
        logger.info("手动触发日志轮转完成")
    
    def set_level(self, level: str) -> None:
        """
        动态设置日志级别
        
        Args:
            level: 新的日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        level = level.upper()
        self.log_level = level
        
        # 更新根日志记录器和所有处理器的级别
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, level))
        
        for handler in root_logger.handlers:
            handler.setLevel(getattr(logging, level))
        
        logger = self.get_logger("LoggerSystem")
        logger.info(f"日志级别已更新为: {level}")
    
    def is_initialized(self) -> bool:
        """
        检查日志系统是否已初始化
        
        Returns:
            bool: 如果已初始化返回True，否则返回False
        """
        return LoggerSystem._initialized
    
    def get_log_files(self) -> list:
        """
        获取所有日志文件列表
        
        Returns:
            list: 日志文件路径列表
        """
        if not self.log_dir or not self.log_dir.exists():
            return []
        
        log_files = list(self.log_dir.glob("*.log*"))
        return sorted(log_files, key=lambda x: x.stat().st_mtime, reverse=True)
    
    def clear_old_logs(self, keep_count: Optional[int] = None) -> int:
        """
        清理旧的日志文件
        
        Args:
            keep_count: 保留的日志文件数量，如果为None则使用backup_count
            
        Returns:
            int: 删除的文件数量
        """
        if keep_count is None:
            keep_count = self.backup_count + 1  # +1 for current log file
        
        log_files = self.get_log_files()
        deleted_count = 0
        
        for log_file in log_files[keep_count:]:
            try:
                log_file.unlink()
                deleted_count += 1
            except Exception as e:
                logger = self.get_logger("LoggerSystem")
                logger.warning(f"删除日志文件失败: {log_file}, 错误: {e}")
        
        if deleted_count > 0:
            logger = self.get_logger("LoggerSystem")
            logger.info(f"清理了 {deleted_count} 个旧日志文件")
        
        return deleted_count


# 全局日志系统实例
_logger_system = LoggerSystem()


def get_logger(name: str) -> logging.Logger:
    """
    便捷函数：获取日志记录器
    
    Args:
        name: 日志记录器名称
        
    Returns:
        logging.Logger: 日志记录器
    """
    return _logger_system.get_logger(name)


def setup_logging(
    log_dir: str,
    log_level: str = "INFO",
    log_format: Optional[str] = None,
    max_bytes: int = 10485760,
    backup_count: int = 5
) -> None:
    """
    便捷函数：配置日志系统
    
    Args:
        log_dir: 日志文件目录
        log_level: 日志级别
        log_format: 日志格式字符串
        max_bytes: 单个日志文件最大字节数
        backup_count: 保留的备份日志文件数量
    """
    _logger_system.setup(log_dir, log_level, log_format, max_bytes, backup_count)
