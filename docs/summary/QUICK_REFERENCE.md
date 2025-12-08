# 内存监控快速参考 / Memory Monitoring Quick Reference

## 🚀 快速启动 / Quick Start

```bash
# 启动程序（自动启用内存监控）
./run_with_memory_monitor.sh

# 或
python main.py
```

## 📊 查看内存状态 / Check Memory

### 在程序中 / In Program
```
主菜单 → 7 (系统管理) → 1 (查看内存状态)
Main Menu → 7 (System Management) → 1 (View Memory Status)
```

### 使用工具 / Using Tool
```bash
python check_memory.py
```

## 🧹 清理内存 / Clean Memory

### 在程序中 / In Program
```
主菜单 → 7 (系统管理) → 2 (清理缓存)
Main Menu → 7 (System Management) → 2 (Clear Cache)
```

### 使用Python / Using Python
```python
from src.utils.cache_manager import get_cache_manager
cache_manager = get_cache_manager()
cache_manager.clear()
```

## ⚙️ 配置 / Configuration

### 文件位置 / File Location
```
config/memory_config.yaml
```

### 关键配置 / Key Settings
```yaml
cache:
  max_memory_items: 50  # 缓存条目数 / Cache items

memory_limits:
  max_memory_mb: 4096  # 最大内存 / Max memory
  warning_threshold_percent: 80  # 警告阈值 / Warning
  critical_threshold_percent: 90  # 紧急阈值 / Critical
```

## 🔍 监控日志 / Monitor Logs

```bash
# 查看内存监控日志
tail -f logs/qlib_trading.log | grep -i memory
```

## 🆘 紧急情况 / Emergency

### 内存使用过高 / High Memory Usage

1. **立即清理 / Immediate Cleanup**
   ```
   主菜单 → 7 → 5 → 2 (紧急清理)
   Main Menu → 7 → 5 → 2 (Emergency Cleanup)
   ```

2. **降低缓存限制 / Reduce Cache Limit**
   ```yaml
   # 编辑 config/memory_config.yaml
   cache:
     max_memory_items: 20  # 降低到20
   ```

3. **重启程序 / Restart Program**
   ```bash
   # Ctrl+C 退出，然后重新启动
   ./run_with_memory_monitor.sh
   ```

## 📈 性能指标 / Performance Metrics

| 指标 / Metric | 正常值 / Normal | 警告值 / Warning |
|--------------|----------------|-----------------|
| 内存使用 / Memory | < 2GB | > 3GB |
| 缓存条目 / Cache | < 50 | > 80 |
| 内存占比 / % | < 50% | > 80% |

## 🔗 相关文档 / Related Docs

- 详细指南: `MEMORY_OPTIMIZATION.md`
- 集成说明: `MEMORY_INTEGRATION.md`
- 完成报告: `INTEGRATION_COMPLETE.md`

## 💡 常用命令 / Common Commands

```bash
# 检查内存
python check_memory.py

# 运行测试
python test_memory_integration.py

# 查看日志
tail -f logs/qlib_trading.log

# 启动程序
./run_with_memory_monitor.sh
```

---

**快速帮助 / Quick Help**: 在程序中按 `h` 查看帮助
