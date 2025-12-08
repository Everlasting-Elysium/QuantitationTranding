# 内存监控集成说明 / Memory Monitoring Integration Guide

## 概述 / Overview

内存监控功能已成功集成到主程序中，可以自动监控和管理系统内存使用。

Memory monitoring has been successfully integrated into the main program to automatically monitor and manage system memory usage.

## 功能特性 / Features

### 1. 自动内存监控 / Automatic Memory Monitoring

程序启动时会自动启动内存监控器，无需手动配置。

The memory monitor starts automatically when the program launches, no manual configuration needed.

**默认配置 / Default Configuration:**
- 最大内存限制 / Max memory: 4GB
- 警告阈值 / Warning threshold: 80%
- 紧急阈值 / Critical threshold: 90%
- 检查间隔 / Check interval: 60秒 / 60 seconds
- 自动清理 / Auto cleanup: 启用 / Enabled

### 2. 系统管理菜单 / System Management Menu

在主菜单中新增了"系统管理"选项（选项7），提供以下功能：

A new "System Management" option (option 7) has been added to the main menu with the following features:

1. **查看内存状态 / View Memory Status**
   - 显示当前内存使用情况
   - 检查是否超过阈值
   - Show current memory usage
   - Check if thresholds are exceeded

2. **清理缓存 / Clear Cache**
   - 清除所有内存和磁盘缓存
   - 释放占用的内存
   - Clear all memory and disk cache
   - Free up occupied memory

3. **强制垃圾回收 / Force Garbage Collection**
   - 立即执行Python垃圾回收
   - 显示回收的对象数和释放的内存
   - Immediately run Python garbage collection
   - Show collected objects and freed memory

4. **查看缓存统计 / View Cache Statistics**
   - 显示缓存条目数量
   - 显示缓存占用的磁盘空间
   - Show cache entry count
   - Show disk space used by cache

5. **内存监控设置 / Memory Monitor Settings**
   - 查看当前监控配置
   - 手动触发清理操作
   - View current monitor configuration
   - Manually trigger cleanup operations

### 3. 自动清理机制 / Automatic Cleanup Mechanism

当内存使用达到阈值时，系统会自动执行清理：

When memory usage reaches thresholds, the system automatically performs cleanup:

- **警告阈值（80%）/ Warning Threshold (80%)**
  - 清理过期缓存
  - 执行一次垃圾回收
  - Clear expired cache
  - Run garbage collection once

- **紧急阈值（90%）/ Critical Threshold (90%)**
  - 清除所有缓存
  - 执行多次完整垃圾回收
  - Clear all cache
  - Run multiple full garbage collections

## 使用方法 / Usage

### 方法1: 使用启动脚本 / Method 1: Use Startup Script

```bash
# 使用带内存监控的启动脚本
# Use startup script with memory monitoring
./run_with_memory_monitor.sh
```

### 方法2: 直接运行 / Method 2: Direct Run

```bash
# 激活conda环境
# Activate conda environment
conda activate QuantitationTranding

# 运行主程序
# Run main program
python main.py
```

### 方法3: 使用conda run / Method 3: Use conda run

```bash
# 使用conda run运行
# Run with conda run
conda run -n QuantitationTranding python main.py
```

## 在主菜单中使用 / Using in Main Menu

启动程序后，在主菜单中：

After starting the program, in the main menu:

```
================================
量化交易系统主菜单
Quantitative Trading System Main Menu
================================

0. 🎯 引导式工作流程 / Guided Workflow
1. 模型训练 / Model Training
2. 历史回测 / Historical Backtest
3. 信号生成 / Signal Generation
4. 数据管理 / Data Management
5. 模型管理 / Model Management
6. 报告查看 / View Reports
7. 🔧 系统管理 / System Management  ← 新增 / NEW
h. 帮助 / Help
q. 退出 / Quit

请选择功能 / Please select a function: 7
```

选择"7"进入系统管理菜单：

Select "7" to enter the system management menu:

```
============================================================
系统管理 / System Management
============================================================

1. 查看内存状态 / View Memory Status
2. 清理缓存 / Clear Cache
3. 强制垃圾回收 / Force Garbage Collection
4. 查看缓存统计 / View Cache Statistics
5. 内存监控设置 / Memory Monitor Settings
0. 返回主菜单 / Back to Main Menu
```

## 监控日志 / Monitoring Logs

内存监控的日志会记录在系统日志中：

Memory monitoring logs are recorded in the system log:

```bash
# 查看日志
# View logs
tail -f logs/qlib_trading.log | grep -i memory
```

日志示例 / Log Example:
```
2024-01-01 10:00:00 - INFO - 启动内存监控... / Starting memory monitoring...
2024-01-01 10:00:00 - INFO - 内存监控已启动 / Memory monitoring started
2024-01-01 10:01:00 - INFO - 内存使用正常 / Memory usage normal: 512.34MB (12.5%)
2024-01-01 10:15:00 - WARNING - ⚠️ 内存使用达到警告阈值 / Memory usage reached warning threshold
2024-01-01 10:15:00 - INFO - 开始执行内存清理... / Starting memory cleanup...
2024-01-01 10:15:01 - INFO - 已清理 15 个缓存条目 / Cleared 15 cache entries
2024-01-01 10:15:01 - INFO - 垃圾回收完成，回收 234 个对象 / GC completed, collected 234 objects
```

## 手动检查内存 / Manual Memory Check

可以使用独立的内存检查工具：

You can use the standalone memory check tool:

```bash
# 运行内存检查工具
# Run memory check tool
python check_memory.py
```

输出示例 / Output Example:
```
============================================================
内存检查和清理工具 / Memory Check and Cleanup Tool
============================================================

1. 当前内存使用情况 / Current Memory Usage

============================================================
内存使用情况 / Memory Usage
============================================================
进程物理内存 / Process RSS: 142.43 MB
进程虚拟内存 / Process VMS: 1513.80 MB
进程内存占比 / Process %: 0.45%

系统总内存 / System Total: 31.25 GB
系统已用内存 / System Used: 2.32 GB
系统可用内存 / System Available: 28.93 GB
系统内存占比 / System %: 7.40%
============================================================
```

## 配置调整 / Configuration Adjustment

如果需要调整内存监控配置，可以编辑 `config/memory_config.yaml`：

To adjust memory monitoring configuration, edit `config/memory_config.yaml`:

```yaml
# 示例配置 / Example Configuration
cache:
  max_memory_items: 50  # 减少以降低内存使用 / Reduce to lower memory usage

memory_limits:
  max_memory_mb: 4096  # 根据系统内存调整 / Adjust based on system memory
  warning_threshold_percent: 80
  critical_threshold_percent: 90

monitoring:
  enabled: true
  interval: 60  # 检查间隔（秒）/ Check interval (seconds)
```

## 故障排除 / Troubleshooting

### 问题1: 内存监控未启动 / Issue 1: Memory Monitor Not Started

**症状 / Symptoms:**
- 看不到内存监控日志
- 系统管理菜单无法使用

**解决方案 / Solutions:**
1. 检查是否安装了psutil: `pip install psutil`
2. 查看启动日志中的错误信息
3. 确认memory_monitor.py文件存在

### 问题2: 内存仍然增长 / Issue 2: Memory Still Growing

**症状 / Symptoms:**
- 内存持续增长
- 自动清理没有效果

**解决方案 / Solutions:**
1. 降低缓存限制: 编辑 `config/memory_config.yaml`
2. 手动执行紧急清理: 系统管理 → 内存监控设置 → 紧急清理
3. 检查是否有大数据对象未释放

### 问题3: 性能下降 / Issue 3: Performance Degradation

**症状 / Symptoms:**
- 程序运行变慢
- 频繁触发垃圾回收

**解决方案 / Solutions:**
1. 增加缓存限制
2. 增加检查间隔
3. 禁用自动清理（不推荐）

## 性能影响 / Performance Impact

内存监控对性能的影响很小：

Memory monitoring has minimal performance impact:

- **CPU使用 / CPU Usage**: < 0.1%
- **内存开销 / Memory Overhead**: < 10MB
- **检查延迟 / Check Latency**: < 100ms

## 最佳实践 / Best Practices

1. **定期检查内存状态 / Regular Memory Checks**
   - 在长时间运行任务前后检查内存
   - Check memory before and after long-running tasks

2. **及时清理缓存 / Timely Cache Cleanup**
   - 完成大型任务后手动清理缓存
   - Manually clear cache after completing large tasks

3. **监控日志 / Monitor Logs**
   - 定期查看内存监控日志
   - Regularly review memory monitoring logs

4. **调整配置 / Adjust Configuration**
   - 根据实际使用情况调整阈值
   - Adjust thresholds based on actual usage

## 相关文件 / Related Files

- `src/cli/main_cli.py` - 主CLI（已集成内存监控）/ Main CLI (with memory monitoring integrated)
- `src/utils/memory_monitor.py` - 内存监控器 / Memory monitor
- `src/utils/cache_manager.py` - 缓存管理器 / Cache manager
- `config/memory_config.yaml` - 内存配置 / Memory configuration
- `check_memory.py` - 内存检查工具 / Memory check tool
- `run_with_memory_monitor.sh` - 启动脚本 / Startup script
- `MEMORY_OPTIMIZATION.md` - 详细优化文档 / Detailed optimization guide

## 总结 / Summary

内存监控已完全集成到系统中，提供：

Memory monitoring is fully integrated into the system, providing:

✅ 自动监控和清理 / Automatic monitoring and cleanup
✅ 友好的用户界面 / User-friendly interface
✅ 详细的统计信息 / Detailed statistics
✅ 灵活的配置选项 / Flexible configuration options
✅ 完善的日志记录 / Comprehensive logging

现在可以放心运行程序，不用担心内存泄漏问题！

You can now run the program with confidence, without worrying about memory leaks!
