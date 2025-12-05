"""
缓存管理器模块 / Cache Manager Module
负责数据和模型的缓存管理，提升系统性能
Responsible for caching data and models to improve system performance
"""

import pickle
import hashlib
import json
from pathlib import Path
from typing import Any, Optional, Callable, Dict
from datetime import datetime, timedelta
from functools import wraps
import pandas as pd

from ..infrastructure.logger_system import get_logger


class CacheManager:
    """
    缓存管理器 / Cache Manager
    
    职责 / Responsibilities:
    - 缓存数据和模型 / Cache data and models
    - 管理缓存过期 / Manage cache expiration
    - 提供缓存装饰器 / Provide cache decorators
    """
    
    def __init__(self, cache_dir: str = ".cache", default_ttl: int = 3600):
        """
        初始化缓存管理器 / Initialize cache manager
        
        Args:
            cache_dir: 缓存目录 / Cache directory
            default_ttl: 默认缓存过期时间（秒） / Default cache TTL in seconds
        """
        self._cache_dir = Path(cache_dir).expanduser()
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._default_ttl = default_ttl
        self._logger = get_logger(__name__)
        self._memory_cache: Dict[str, tuple] = {}  # key -> (value, expire_time)
        
        self._logger.info(f"缓存管理器初始化 - 缓存目录: {self._cache_dir}, 默认TTL: {default_ttl}秒")
    
    def _generate_cache_key(self, *args, **kwargs) -> str:
        """
        生成缓存键 / Generate cache key
        
        Args:
            *args: 位置参数 / Positional arguments
            **kwargs: 关键字参数 / Keyword arguments
            
        Returns:
            str: 缓存键 / Cache key
        """
        # 将参数转换为字符串
        key_parts = []
        for arg in args:
            if isinstance(arg, pd.DataFrame):
                # 对DataFrame使用shape和列名生成键
                key_parts.append(f"df_{arg.shape}_{list(arg.columns)}")
            else:
                key_parts.append(str(arg))
        
        for k, v in sorted(kwargs.items()):
            if isinstance(v, pd.DataFrame):
                key_parts.append(f"{k}_df_{v.shape}_{list(v.columns)}")
            else:
                key_parts.append(f"{k}_{v}")
        
        # 生成哈希
        key_str = "_".join(key_parts)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, key: str, use_memory: bool = True) -> Optional[Any]:
        """
        从缓存获取数据 / Get data from cache
        
        Args:
            key: 缓存键 / Cache key
            use_memory: 是否使用内存缓存 / Whether to use memory cache
            
        Returns:
            Optional[Any]: 缓存的数据，如果不存在或已过期则返回None / Cached data or None if not found or expired
        """
        # 先检查内存缓存
        if use_memory and key in self._memory_cache:
            value, expire_time = self._memory_cache[key]
            if datetime.now() < expire_time:
                self._logger.debug(f"内存缓存命中: {key}")
                return value
            else:
                # 过期，删除
                del self._memory_cache[key]
                self._logger.debug(f"内存缓存过期: {key}")
        
        # 检查磁盘缓存
        cache_file = self._cache_dir / f"{key}.pkl"
        meta_file = self._cache_dir / f"{key}.meta"
        
        if not cache_file.exists() or not meta_file.exists():
            return None
        
        try:
            # 读取元数据
            with open(meta_file, 'r') as f:
                meta = json.load(f)
            
            # 检查是否过期
            expire_time = datetime.fromisoformat(meta['expire_time'])
            if datetime.now() >= expire_time:
                self._logger.debug(f"磁盘缓存过期: {key}")
                # 删除过期缓存
                cache_file.unlink()
                meta_file.unlink()
                return None
            
            # 读取缓存数据
            with open(cache_file, 'rb') as f:
                value = pickle.load(f)
            
            self._logger.debug(f"磁盘缓存命中: {key}")
            
            # 加载到内存缓存
            if use_memory:
                self._memory_cache[key] = (value, expire_time)
            
            return value
            
        except Exception as e:
            self._logger.warning(f"读取缓存失败: {key}, 错误: {str(e)}")
            return None
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        use_memory: bool = True
    ) -> None:
        """
        设置缓存 / Set cache
        
        Args:
            key: 缓存键 / Cache key
            value: 缓存值 / Cache value
            ttl: 过期时间（秒），None表示使用默认值 / TTL in seconds, None for default
            use_memory: 是否同时缓存到内存 / Whether to cache in memory
        """
        ttl = ttl if ttl is not None else self._default_ttl
        expire_time = datetime.now() + timedelta(seconds=ttl)
        
        try:
            # 保存到磁盘
            cache_file = self._cache_dir / f"{key}.pkl"
            meta_file = self._cache_dir / f"{key}.meta"
            
            with open(cache_file, 'wb') as f:
                pickle.dump(value, f)
            
            with open(meta_file, 'w') as f:
                json.dump({
                    'expire_time': expire_time.isoformat(),
                    'created_time': datetime.now().isoformat()
                }, f)
            
            # 保存到内存
            if use_memory:
                self._memory_cache[key] = (value, expire_time)
            
            self._logger.debug(f"缓存已设置: {key}, TTL: {ttl}秒")
            
        except Exception as e:
            self._logger.warning(f"设置缓存失败: {key}, 错误: {str(e)}")
    
    def delete(self, key: str) -> None:
        """
        删除缓存 / Delete cache
        
        Args:
            key: 缓存键 / Cache key
        """
        # 从内存删除
        if key in self._memory_cache:
            del self._memory_cache[key]
        
        # 从磁盘删除
        cache_file = self._cache_dir / f"{key}.pkl"
        meta_file = self._cache_dir / f"{key}.meta"
        
        if cache_file.exists():
            cache_file.unlink()
        if meta_file.exists():
            meta_file.unlink()
        
        self._logger.debug(f"缓存已删除: {key}")
    
    def clear(self, pattern: Optional[str] = None) -> int:
        """
        清除缓存 / Clear cache
        
        Args:
            pattern: 缓存键模式，None表示清除所有 / Cache key pattern, None for all
            
        Returns:
            int: 清除的缓存数量 / Number of caches cleared
        """
        count = 0
        
        # 清除内存缓存
        if pattern is None:
            count += len(self._memory_cache)
            self._memory_cache.clear()
        else:
            keys_to_delete = [k for k in self._memory_cache.keys() if pattern in k]
            for key in keys_to_delete:
                del self._memory_cache[key]
            count += len(keys_to_delete)
        
        # 清除磁盘缓存
        for cache_file in self._cache_dir.glob("*.pkl"):
            key = cache_file.stem
            if pattern is None or pattern in key:
                cache_file.unlink()
                meta_file = self._cache_dir / f"{key}.meta"
                if meta_file.exists():
                    meta_file.unlink()
                count += 1
        
        self._logger.info(f"缓存已清除: {count}个")
        return count
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        获取缓存统计信息 / Get cache statistics
        
        Returns:
            Dict[str, Any]: 缓存统计信息 / Cache statistics
        """
        memory_count = len(self._memory_cache)
        disk_count = len(list(self._cache_dir.glob("*.pkl")))
        
        # 计算磁盘缓存大小
        total_size = sum(f.stat().st_size for f in self._cache_dir.glob("*"))
        
        return {
            'memory_cache_count': memory_count,
            'disk_cache_count': disk_count,
            'total_cache_size_mb': total_size / (1024 * 1024),
            'cache_directory': str(self._cache_dir)
        }
    
    def cached(
        self,
        ttl: Optional[int] = None,
        key_prefix: str = "",
        use_memory: bool = True
    ) -> Callable:
        """
        缓存装饰器 / Cache decorator
        
        Args:
            ttl: 过期时间（秒） / TTL in seconds
            key_prefix: 缓存键前缀 / Cache key prefix
            use_memory: 是否使用内存缓存 / Whether to use memory cache
            
        Returns:
            Callable: 装饰器函数 / Decorator function
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 生成缓存键
                cache_key = f"{key_prefix}_{func.__name__}_{self._generate_cache_key(*args, **kwargs)}"
                
                # 尝试从缓存获取
                cached_value = self.get(cache_key, use_memory=use_memory)
                if cached_value is not None:
                    self._logger.debug(f"使用缓存结果: {func.__name__}")
                    return cached_value
                
                # 执行函数
                self._logger.debug(f"执行函数并缓存结果: {func.__name__}")
                result = func(*args, **kwargs)
                
                # 保存到缓存
                self.set(cache_key, result, ttl=ttl, use_memory=use_memory)
                
                return result
            
            return wrapper
        return decorator


# 全局缓存管理器实例
_global_cache_manager: Optional[CacheManager] = None


def get_cache_manager(
    cache_dir: str = ".cache",
    default_ttl: int = 3600
) -> CacheManager:
    """
    获取全局缓存管理器实例 / Get global cache manager instance
    
    Args:
        cache_dir: 缓存目录 / Cache directory
        default_ttl: 默认TTL / Default TTL
        
    Returns:
        CacheManager: 缓存管理器实例 / Cache manager instance
    """
    global _global_cache_manager
    if _global_cache_manager is None:
        _global_cache_manager = CacheManager(cache_dir=cache_dir, default_ttl=default_ttl)
    return _global_cache_manager
