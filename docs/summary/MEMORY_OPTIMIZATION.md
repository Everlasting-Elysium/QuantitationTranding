# 内存优化指南 / Memory Optimization Guide

## 问题描述 / Problem Description

系统在运行时可能会出现内存持续增长的问题，最终导致内存耗尽（OOM）。

The system may experience continuous memory growth during runtime, eventually leading to out-of-memory (OOM) errors.

## 主要原因 / Root Causes

### 1. 缓存无限增长 / Unlimited Cache Growth
- **问题**: 内存缓存没有大小限制，会无限增长
- **Problem**: Memory cache has no size limit and grows indefinitely
- **影响**: 可能占用数GB内存
- **Impact**: Can consume several GB of memory

### 2. 数据未释放 / Data Not Released
- **问题**: qlib加载的数据保留在内存中不释放
- **Problem**: Data loaded by qlib remains in memory without being released
- **影响**: 每次数据加载都会增加内存使用
- **Impact**: Each data load increases memory usage

### 3. 缓存过期检查不及时 / Delayed Cache Expiration Check
- **问题**: 过期的缓存数据没有及时清理
- **Problem**: Expired cache data is not cleaned up promptly
- **影响**: 大量过期数据占用内存
- **Impact**: Large amount of expired data occupies memory

## 已实施的解决方案 / Implemented Solutions

### 1. 限制内存缓存大小 / Limit Memory Cache Size

**修改文件 / Modified File**: `src/utils/cache_manager.py`

```python
# 添加了最大条目数限制
# Added maximum items limit
max_memory_items: int = 100  # 可配置 / Configurable

# 在设置缓存时检查大小
# Check size when setting cache
if len(self._memory_cache) >= self._max_memory_items:
    # 删除最旧的条目（FIFO策略）
    # Delete oldest entry (FIFO strategy)
    oldest_key = next(iter(self._memory_cache))
    del self._memory_cache[oldest_key]
```

### 2. 自动清理过期缓存 / Auto Cleanup Expired Cache

**新增功能 / New Feature**: `_cleanup_expired_memory_cache()`

```python
def _cleanup_expired_memory_cache(self) -> None:
    """清理过期的内存缓存"""
    now = datetime.now()
    expired_keys = [k for k, (_, expire_time) in self._memory_cache.items() 
                    if now >= expire_time]
    for key in expired_keys:
        del self._memory_cache[key]
```

### 3. 数据管理器缓存限制 / Data Manager Cache Limit

**修改文件 / Modified File**: `src/core/data_manager.py`

```python
# 限制缓存大小为50个条目
# Limit cache size to 50 items
self._cache_manager = get_cache_manager(max_memory_items=50)
```

### 4. 内存监控器 / Memory Monitor

**新增文件 / New File**: `src/utils/memory_monitor.py`

功能 / Features:
- 实时监控内存使用 / Real-time memory usage monitoring
- 自动触发清理 / Auto trigger cleanup
- 警告和紧急阈值 / Warning and critical thresholds
- 强制垃圾回收 / Force garbage collection

### 5. 内存配置文件 / Memory Configuration File

**新增文件 / New File**: `config/memory_config.yaml`

可配置项 / Configurable Items:
- 缓存大小限制 / Cache size limits
- 内存阈值 / Memory thresholds
- 自动清理间隔 / Auto cleanup intervals
- 垃圾回收策略 / Garbage collection strategy

## 使用方法 / Usage

### 1. 检查内存使用 / Check Memory Usage

```bash
# 运行内存检查工具
# Run memory check tool
python check_memory.py
```

### 2. 在代码中启用内存监控 / Enable Memory Monitoring in Code

```python
from src.utils.memory_monitor import get_memory_monitor

# 创建内存监控器
# Create memory monitor
monitor = get_memory_monitor(
    max_memory_mb=4096,  # 4GB限制 / 4GB limit
    warning_threshold=0.8,  # 80%警告 / 80% warning
    critical_threshold=0.9,  # 90%紧急 / 90% critical
    check_interval=60,  # 每60秒检查 / Check every 60 seconds
    auto_cleanup=True  # 自动清理 / Auto cleanup
)

# 启动监控
# Start monitoring
monitor.start_monitoring()

# 你的代码...
# Your code...

# 停止监控
# Stop monitoring
monitor.stop_monitoring()
```

### 3. 手动清理缓存 / Manual Cache Cleanup

```python
from src.utils.cache_manager import get_cache_manager

# 获取缓存管理器
# Get cache manager
cache_manager = get_cache_manager()

# 清理所有缓存
# Clear all cache
cache_manager.clear()

# 清理特定模式的缓存
# Clear cache with specific pattern
cache_manager.clear(pattern="data_")
```

### 4. 强制垃圾回收 / Force Garbage Collection

```python
import gc

# 执行完整的垃圾回收
# Perform full garbage collection
gc.collect(generation=2)
```

## 配置建议 / Configuration Recommendations

### 低内存环境 / Low Memory Environment (< 8GB)

```yaml
cache:
  max_memory_items: 20  # 减少缓存条目 / Reduce cache items
  
memory_limits:
  max_memory_mb: 2048  # 2GB限制 / 2GB limit
  warning_threshold_percent: 70  # 70%警告 / 70% warning
  critical_threshold_percent: 85  # 85%紧急 / 85% critical
```

### 中等内存环境 / Medium Memory Environment (8-16GB)

```yaml
cache:
  max_memory_items: 50  # 默认设置 / Default setting
  
memory_limits:
  max_memory_mb: 4096  # 4GB限制 / 4GB limit
  warning_threshold_percent: 80  # 80%警告 / 80% warning
  critical_threshold_percent: 90  # 90%紧急 / 90% critical
```

### 高内存环境 / High Memory Environment (> 16GB)

```yaml
cache:
  max_memory_items: 100  # 更多缓存 / More cache
  
memory_limits:
  max_memory_mb: 8192  # 8GB限制 / 8GB limit
  warning_threshold_percent: 85  # 85%警告 / 85% warning
  critical_threshold_percent: 95  # 95%紧急 / 95% critical
```

## 监控和调试 / Monitoring and Debugging

### 1. 查看内存统计 / View Memory Statistics

```python
from src.utils.memory_monitor import get_memory_monitor

monitor = get_memory_monitor()
stats = monitor.get_memory_stats()

print(f"物理内存 / RSS: {stats.rss_mb:.2f} MB")
print(f"虚拟内存 / VMS: {stats.vms_mb:.2f} MB")
print(f"内存占比 / Percent: {stats.percent:.2f}%")
print(f"可用内存 / Available: {stats.available_mb:.2f} MB")
```

### 2. 查看缓存统计 / View Cache Statistics

```python
from src.utils.cache_manager import get_cache_manager

cache_manager = get_cache_manager()
stats = cache_manager.get_cache_stats()

print(f"内存缓存数量 / Memory cache: {stats['memory_cache_count']}")
print(f"磁盘缓存数量 / Disk cache: {stats['disk_cache_count']}")
print(f"缓存总大小 / Total size: {stats['total_cache_size_mb']:.2f} MB")
```

### 3. 设置回调函数 / Set Callback Functions

```python
def on_warning(stats):
    print(f"⚠️ 内存警告: {stats.rss_mb:.2f} MB")
    # 执行自定义操作
    # Perform custom actions

def on_critical(stats):
    print(f"🚨 内存紧急: {stats.rss_mb:.2f} MB")
    # 执行紧急操作
    # Perform emergency actions

monitor = get_memory_monitor()
monitor.set_warning_callback(on_warning)
monitor.set_critical_callback(on_critical)
```

## 最佳实践 / Best Practices

### 1. 及时释放大对象 / Release Large Objects Promptly

```python
# 不好的做法 / Bad practice
data = load_large_dataset()
# ... 长时间持有data引用
# ... Hold data reference for long time

# 好的做法 / Good practice
data = load_large_dataset()
# 使用完后立即删除
# Delete immediately after use
result = process_data(data)
del data
gc.collect()  # 可选：强制垃圾回收 / Optional: force GC
```

### 2. 使用生成器处理大数据 / Use Generators for Large Data

```python
# 不好的做法 / Bad practice
def load_all_data():
    return [load_item(i) for i in range(10000)]

# 好的做法 / Good practice
def load_data_generator():
    for i in range(10000):
        yield load_item(i)
```

### 3. 定期清理缓存 / Regular Cache Cleanup

```python
# 在长时间运行的任务中定期清理
# Regular cleanup in long-running tasks
for i in range(1000):
    process_batch(i)
    
    if i % 100 == 0:
        # 每100次迭代清理一次
        # Cleanup every 100 iterations
        cache_manager.clear()
        gc.collect()
```

### 4. 使用上下文管理器 / Use Context Managers

```python
from contextlib import contextmanager

@contextmanager
def memory_managed_operation():
    """确保操作后清理内存"""
    try:
        yield
    finally:
        cache_manager.clear()
        gc.collect()

# 使用 / Usage
with memory_managed_operation():
    # 执行内存密集型操作
    # Perform memory-intensive operations
    result = heavy_computation()
```

## 故障排除 / Troubleshooting

### 问题1: 内存仍然持续增长 / Issue 1: Memory Still Growing

**可能原因 / Possible Causes**:
- 缓存限制设置过大 / Cache limit set too high
- 数据加载批次过大 / Data loading batch too large
- 存在循环引用 / Circular references exist

**解决方案 / Solutions**:
1. 降低 `max_memory_items` 值
2. 减小数据加载批次大小
3. 使用 `gc.set_debug(gc.DEBUG_LEAK)` 检测内存泄漏

### 问题2: 性能下降 / Issue 2: Performance Degradation

**可能原因 / Possible Causes**:
- 缓存限制过小导致频繁重新计算 / Cache limit too small causing frequent recomputation
- 垃圾回收过于频繁 / Garbage collection too frequent

**解决方案 / Solutions**:
1. 适当增加 `max_memory_items` 值
2. 增加垃圾回收间隔
3. 使用磁盘缓存代替内存缓存

### 问题3: OOM错误仍然发生 / Issue 3: OOM Still Occurs

**可能原因 / Possible Causes**:
- 单个数据对象过大 / Single data object too large
- 系统内存不足 / Insufficient system memory

**解决方案 / Solutions**:
1. 分批处理数据 / Process data in batches
2. 使用数据流式处理 / Use streaming data processing
3. 增加系统内存或使用更大内存的机器

## 总结 / Summary

通过以上优化措施，系统的内存使用应该得到有效控制：

Through the above optimization measures, the system's memory usage should be effectively controlled:

1. ✅ 缓存大小受限 / Cache size limited
2. ✅ 自动清理过期数据 / Auto cleanup expired data
3. ✅ 实时内存监控 / Real-time memory monitoring
4. ✅ 可配置的内存策略 / Configurable memory strategy
5. ✅ 完善的监控工具 / Comprehensive monitoring tools

如果问题仍然存在，请检查：
If the problem persists, please check:

- 是否有其他模块在大量占用内存 / Whether other modules are consuming large amounts of memory
- 是否有第三方库的内存泄漏 / Whether there are memory leaks in third-party libraries
- 系统配置是否合理 / Whether system configuration is reasonable

## 相关文件 / Related Files

- `src/utils/cache_manager.py` - 缓存管理器 / Cache manager
- `src/utils/memory_monitor.py` - 内存监控器 / Memory monitor
- `src/core/data_manager.py` - 数据管理器 / Data manager
- `config/memory_config.yaml` - 内存配置 / Memory configuration
- `check_memory.py` - 内存检查工具 / Memory check tool
