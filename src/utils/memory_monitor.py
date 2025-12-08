"""
内存监控器模块 / Memory Monitor Module
负责监控系统内存使用，防止内存泄漏
Responsible for monitoring system memory usage and preventing memory leaks
"""

import gc
import psutil
import threading
import time
from typing import Optional, Callable, Dict, Tuple
from dataclasses import dataclass

from ..infrastructure.logger_system import get_logger
from .cache_manager import get_cache_manager


@dataclass
class MemoryStats:
    """内存统计信息 / Memory Statistics"""
    rss_mb: float  # 物理内存 / Resident Set Size
    vms_mb: float  # 虚拟内存 / Virtual Memory Size
    percent: float  # 内存占比 / Memory Percentage
    available_mb: float  # 可用内存 / Available Memory


class MemoryMonitor:
    """
    内存监控器 / Memory Monitor
    
    职责 / Responsibilities:
    - 监控内存使用情况 / Monitor memory usage
    - 自动清理缓存 / Auto cleanup cache
    - 触发垃圾回收 / Trigger garbage collection
    - 发出内存警告 / Issue memory warnings
    """
    
    def __init__(
        self,
        max_memory_mb: int = 4096,
        warning_threshold: float = 0.8,
        critical_threshold: float = 0.9,
        check_interval: int = 60,
        auto_cleanup: bool = True
    ):
        """
        初始化内存监控器 / Initialize memory monitor
        
        Args:
            max_memory_mb: 最大内存限制（MB） / Maximum memory limit in MB
            warning_threshold: 警告阈值（0-1） / Warning threshold (0-1)
            critical_threshold: 紧急阈值（0-1） / Critical threshold (0-1)
            check_interval: 检查间隔（秒） / Check interval in seconds
            auto_cleanup: 是否自动清理 / Whether to auto cleanup
        """
        self._max_memory_mb = max_memory_mb
        self._warning_threshold = warning_threshold
        self._critical_threshold = critical_threshold
        self._check_interval = check_interval
        self._auto_cleanup = auto_cleanup
        
        self._logger = get_logger(__name__)
        self._cache_manager = get_cache_manager()
        
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None
        
        self._warning_callback: Optional[Callable] = None
        self._critical_callback: Optional[Callable] = None
        
        self._logger.info(
            f"内存监控器初始化 - 最大内存: {max_memory_mb}MB, "
            f"警告阈值: {warning_threshold*100}%, 紧急阈值: {critical_threshold*100}%"
        )
    
    def get_memory_stats(self) -> MemoryStats:
        """
        获取内存统计信息 / Get memory statistics
        
        Returns:
            MemoryStats: 内存统计信息 / Memory statistics
        """
        process = psutil.Process()
        mem_info = process.memory_info()
        system_mem = psutil.virtual_memory()
        
        return MemoryStats(
            rss_mb=mem_info.rss / (1024 * 1024),
            vms_mb=mem_info.vms / (1024 * 1024),
            percent=process.memory_percent(),
            available_mb=system_mem.available / (1024 * 1024)
        )
    
    def check_memory(self) -> Tuple[bool, str]:
        """
        检查内存使用情况 / Check memory usage
        
        Returns:
            tuple[bool, str]: (是否正常, 消息) / (is_ok, message)
        """
        stats = self.get_memory_stats()
        
        # 检查是否超过最大限制
        if stats.rss_mb > self._max_memory_mb:
            message = (
                f"⚠️ 内存使用超过限制！/ Memory usage exceeded limit!\n"
                f"当前使用 / Current: {stats.rss_mb:.2f}MB\n"
                f"最大限制 / Max limit: {self._max_memory_mb}MB"
            )
            self._logger.warning(message)
            return False, message
        
        # 检查是否达到紧急阈值
        usage_ratio = stats.rss_mb / self._max_memory_mb
        if usage_ratio >= self._critical_threshold:
            message = (
                f"🚨 内存使用达到紧急阈值！/ Memory usage reached critical threshold!\n"
                f"当前使用 / Current: {stats.rss_mb:.2f}MB ({usage_ratio*100:.1f}%)\n"
                f"紧急阈值 / Critical: {self._critical_threshold*100}%"
            )
            self._logger.error(message)
            
            # 触发紧急回调
            if self._critical_callback:
                self._critical_callback(stats)
            
            # 自动清理
            if self._auto_cleanup:
                self._emergency_cleanup()
            
            return False, message
        
        # 检查是否达到警告阈值
        if usage_ratio >= self._warning_threshold:
            message = (
                f"⚠️ 内存使用达到警告阈值 / Memory usage reached warning threshold\n"
                f"当前使用 / Current: {stats.rss_mb:.2f}MB ({usage_ratio*100:.1f}%)\n"
                f"警告阈值 / Warning: {self._warning_threshold*100}%"
            )
            self._logger.warning(message)
            
            # 触发警告回调
            if self._warning_callback:
                self._warning_callback(stats)
            
            # 自动清理
            if self._auto_cleanup:
                self._cleanup()
            
            return True, message
        
        # 正常
        return True, f"内存使用正常 / Memory usage normal: {stats.rss_mb:.2f}MB ({usage_ratio*100:.1f}%)"
    
    def _cleanup(self) -> None:
        """执行常规清理 / Perform regular cleanup"""
        self._logger.info("开始执行内存清理... / Starting memory cleanup...")
        
        before_stats = self.get_memory_stats()
        
        # 清理缓存
        try:
            count = self._cache_manager.clear()
            self._logger.info(f"已清理 {count} 个缓存条目 / Cleared {count} cache entries")
        except Exception as e:
            self._logger.error(f"清理缓存失败 / Failed to clean cache: {str(e)}")
        
        # 执行垃圾回收
        try:
            collected = gc.collect()
            self._logger.info(f"垃圾回收完成，回收 {collected} 个对象 / GC completed, collected {collected} objects")
        except Exception as e:
            self._logger.error(f"垃圾回收失败 / Failed to run GC: {str(e)}")
        
        after_stats = self.get_memory_stats()
        freed_mb = before_stats.rss_mb - after_stats.rss_mb
        
        self._logger.info(
            f"内存清理完成 / Memory cleanup completed\n"
            f"清理前 / Before: {before_stats.rss_mb:.2f}MB\n"
            f"清理后 / After: {after_stats.rss_mb:.2f}MB\n"
            f"释放 / Freed: {freed_mb:.2f}MB"
        )
    
    def _emergency_cleanup(self) -> None:
        """执行紧急清理 / Perform emergency cleanup"""
        self._logger.warning("开始执行紧急内存清理... / Starting emergency memory cleanup...")
        
        before_stats = self.get_memory_stats()
        
        # 清理所有缓存（包括内存和磁盘）
        try:
            count = self._cache_manager.clear()
            self._logger.info(f"已清理所有缓存：{count} 个条目 / Cleared all cache: {count} entries")
        except Exception as e:
            self._logger.error(f"清理缓存失败 / Failed to clean cache: {str(e)}")
        
        # 强制执行多次垃圾回收
        try:
            total_collected = 0
            for i in range(3):
                collected = gc.collect(generation=2)  # 完整的垃圾回收
                total_collected += collected
                self._logger.info(f"第 {i+1} 次垃圾回收，回收 {collected} 个对象")
            
            self._logger.info(f"紧急垃圾回收完成，总共回收 {total_collected} 个对象")
        except Exception as e:
            self._logger.error(f"紧急垃圾回收失败 / Emergency GC failed: {str(e)}")
        
        after_stats = self.get_memory_stats()
        freed_mb = before_stats.rss_mb - after_stats.rss_mb
        
        self._logger.warning(
            f"紧急内存清理完成 / Emergency memory cleanup completed\n"
            f"清理前 / Before: {before_stats.rss_mb:.2f}MB\n"
            f"清理后 / After: {after_stats.rss_mb:.2f}MB\n"
            f"释放 / Freed: {freed_mb:.2f}MB"
        )
    
    def start_monitoring(self) -> None:
        """开始监控 / Start monitoring"""
        if self._monitoring:
            self._logger.warning("内存监控已在运行 / Memory monitoring already running")
            return
        
        self._monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
        
        self._logger.info(f"内存监控已启动，检查间隔: {self._check_interval}秒 / Memory monitoring started")
    
    def stop_monitoring(self) -> None:
        """停止监控 / Stop monitoring"""
        if not self._monitoring:
            self._logger.warning("内存监控未运行 / Memory monitoring not running")
            return
        
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)
        
        self._logger.info("内存监控已停止 / Memory monitoring stopped")
    
    def _monitor_loop(self) -> None:
        """监控循环 / Monitor loop"""
        while self._monitoring:
            try:
                is_ok, message = self.check_memory()
                if not is_ok:
                    self._logger.warning(message)
            except Exception as e:
                self._logger.error(f"内存检查失败 / Memory check failed: {str(e)}")
            
            # 等待下一次检查
            time.sleep(self._check_interval)
    
    def set_warning_callback(self, callback: Callable) -> None:
        """设置警告回调 / Set warning callback"""
        self._warning_callback = callback
    
    def set_critical_callback(self, callback: Callable) -> None:
        """设置紧急回调 / Set critical callback"""
        self._critical_callback = callback
    
    def force_cleanup(self) -> None:
        """强制执行清理 / Force cleanup"""
        self._cleanup()
    
    def force_emergency_cleanup(self) -> None:
        """强制执行紧急清理 / Force emergency cleanup"""
        self._emergency_cleanup()


# 全局内存监控器实例
_global_memory_monitor: Optional[MemoryMonitor] = None


def get_memory_monitor(
    max_memory_mb: int = 4096,
    warning_threshold: float = 0.8,
    critical_threshold: float = 0.9,
    check_interval: int = 60,
    auto_cleanup: bool = True
) -> MemoryMonitor:
    """
    获取全局内存监控器实例 / Get global memory monitor instance
    
    Args:
        max_memory_mb: 最大内存限制（MB） / Maximum memory limit in MB
        warning_threshold: 警告阈值 / Warning threshold
        critical_threshold: 紧急阈值 / Critical threshold
        check_interval: 检查间隔 / Check interval
        auto_cleanup: 是否自动清理 / Whether to auto cleanup
        
    Returns:
        MemoryMonitor: 内存监控器实例 / Memory monitor instance
    """
    global _global_memory_monitor
    if _global_memory_monitor is None:
        _global_memory_monitor = MemoryMonitor(
            max_memory_mb=max_memory_mb,
            warning_threshold=warning_threshold,
            critical_threshold=critical_threshold,
            check_interval=check_interval,
            auto_cleanup=auto_cleanup
        )
    return _global_memory_monitor
