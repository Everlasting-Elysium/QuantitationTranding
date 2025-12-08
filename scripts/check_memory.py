#!/usr/bin/env python3
"""
内存检查和清理工具 / Memory Check and Cleanup Tool

用于检查系统内存使用情况并清理缓存
Used to check system memory usage and clean cache
"""

import sys
import os
import psutil
import gc
from pathlib import Path

# 添加src到路径
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    from src.utils.cache_manager import get_cache_manager
    from src.infrastructure.logger_system import get_logger
except ImportError:
    # 如果上面的导入失败，尝试直接导入
    from utils.cache_manager import get_cache_manager
    from infrastructure.logger_system import get_logger


def get_memory_usage():
    """获取当前进程的内存使用情况"""
    process = psutil.Process()
    mem_info = process.memory_info()
    
    return {
        'rss_mb': mem_info.rss / (1024 * 1024),  # 物理内存
        'vms_mb': mem_info.vms / (1024 * 1024),  # 虚拟内存
        'percent': process.memory_percent()
    }


def print_memory_info():
    """打印内存信息"""
    mem = get_memory_usage()
    system_mem = psutil.virtual_memory()
    
    print("\n" + "="*60)
    print("内存使用情况 / Memory Usage")
    print("="*60)
    print(f"进程物理内存 / Process RSS: {mem['rss_mb']:.2f} MB")
    print(f"进程虚拟内存 / Process VMS: {mem['vms_mb']:.2f} MB")
    print(f"进程内存占比 / Process %: {mem['percent']:.2f}%")
    print(f"\n系统总内存 / System Total: {system_mem.total / (1024**3):.2f} GB")
    print(f"系统已用内存 / System Used: {system_mem.used / (1024**3):.2f} GB")
    print(f"系统可用内存 / System Available: {system_mem.available / (1024**3):.2f} GB")
    print(f"系统内存占比 / System %: {system_mem.percent:.2f}%")
    print("="*60 + "\n")


def clean_cache():
    """清理缓存"""
    print("正在清理缓存... / Cleaning cache...")
    
    try:
        cache_manager = get_cache_manager()
        count = cache_manager.clear()
        print(f"✅ 已清理 {count} 个缓存条目 / Cleared {count} cache entries")
        
        # 获取缓存统计
        stats = cache_manager.get_cache_stats()
        print(f"内存缓存数量 / Memory cache count: {stats['memory_cache_count']}")
        print(f"磁盘缓存数量 / Disk cache count: {stats['disk_cache_count']}")
        print(f"缓存总大小 / Total cache size: {stats['total_cache_size_mb']:.2f} MB")
        
    except Exception as e:
        print(f"❌ 清理缓存失败 / Failed to clean cache: {str(e)}")


def force_gc():
    """强制垃圾回收"""
    print("正在执行垃圾回收... / Running garbage collection...")
    
    before_mem = get_memory_usage()
    
    # 执行垃圾回收
    collected = gc.collect()
    
    after_mem = get_memory_usage()
    freed_mb = before_mem['rss_mb'] - after_mem['rss_mb']
    
    print(f"✅ 垃圾回收完成 / Garbage collection completed")
    print(f"回收对象数 / Objects collected: {collected}")
    print(f"释放内存 / Memory freed: {freed_mb:.2f} MB")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("内存检查和清理工具 / Memory Check and Cleanup Tool")
    print("="*60)
    
    # 显示当前内存使用
    print("\n1. 当前内存使用情况 / Current Memory Usage")
    print_memory_info()
    
    # 清理缓存
    print("\n2. 清理缓存 / Clean Cache")
    clean_cache()
    
    # 强制垃圾回收
    print("\n3. 强制垃圾回收 / Force Garbage Collection")
    force_gc()
    
    # 再次显示内存使用
    print("\n4. 清理后内存使用情况 / Memory Usage After Cleanup")
    print_memory_info()
    
    print("✅ 内存检查和清理完成 / Memory check and cleanup completed\n")


if __name__ == "__main__":
    main()
