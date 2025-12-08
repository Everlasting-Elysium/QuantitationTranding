#!/usr/bin/env python3
"""
测试内存监控集成 / Test Memory Monitoring Integration

验证内存监控功能是否正常工作
Verify that memory monitoring functionality works correctly
"""

import sys
import os

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_memory_monitor_import():
    """测试内存监控器导入"""
    print("测试1: 导入内存监控器... / Test 1: Import memory monitor...")
    try:
        from src.utils.memory_monitor import get_memory_monitor
        print("✅ 导入成功 / Import successful")
        return True
    except Exception as e:
        print(f"❌ 导入失败 / Import failed: {str(e)}")
        return False


def test_memory_monitor_creation():
    """测试创建内存监控器"""
    print("\n测试2: 创建内存监控器... / Test 2: Create memory monitor...")
    try:
        from src.utils.memory_monitor import get_memory_monitor
        
        monitor = get_memory_monitor(
            max_memory_mb=4096,
            warning_threshold=0.8,
            critical_threshold=0.9,
            check_interval=60,
            auto_cleanup=True
        )
        print("✅ 创建成功 / Creation successful")
        return True, monitor
    except Exception as e:
        print(f"❌ 创建失败 / Creation failed: {str(e)}")
        return False, None


def test_memory_stats(monitor):
    """测试获取内存统计"""
    print("\n测试3: 获取内存统计... / Test 3: Get memory stats...")
    try:
        stats = monitor.get_memory_stats()
        print(f"✅ 获取成功 / Get successful")
        print(f"   物理内存 / RSS: {stats.rss_mb:.2f} MB")
        print(f"   虚拟内存 / VMS: {stats.vms_mb:.2f} MB")
        print(f"   内存占比 / Percent: {stats.percent:.2f}%")
        print(f"   可用内存 / Available: {stats.available_mb:.2f} MB")
        return True
    except Exception as e:
        print(f"❌ 获取失败 / Get failed: {str(e)}")
        return False


def test_memory_check(monitor):
    """测试内存检查"""
    print("\n测试4: 执行内存检查... / Test 4: Check memory...")
    try:
        is_ok, message = monitor.check_memory()
        print(f"✅ 检查成功 / Check successful")
        print(f"   状态 / Status: {'正常 / OK' if is_ok else '警告 / Warning'}")
        print(f"   消息 / Message: {message}")
        return True
    except Exception as e:
        print(f"❌ 检查失败 / Check failed: {str(e)}")
        return False


def test_cache_manager():
    """测试缓存管理器"""
    print("\n测试5: 测试缓存管理器... / Test 5: Test cache manager...")
    try:
        from src.utils.cache_manager import get_cache_manager
        
        cache_manager = get_cache_manager()
        stats = cache_manager.get_cache_stats()
        
        print(f"✅ 测试成功 / Test successful")
        print(f"   内存缓存数量 / Memory cache: {stats['memory_cache_count']}")
        print(f"   磁盘缓存数量 / Disk cache: {stats['disk_cache_count']}")
        print(f"   缓存总大小 / Total size: {stats['total_cache_size_mb']:.2f} MB")
        return True
    except Exception as e:
        print(f"❌ 测试失败 / Test failed: {str(e)}")
        return False


def test_cleanup(monitor):
    """测试清理功能"""
    print("\n测试6: 测试清理功能... / Test 6: Test cleanup...")
    try:
        print("   执行清理... / Running cleanup...")
        monitor.force_cleanup()
        print("✅ 清理成功 / Cleanup successful")
        return True
    except Exception as e:
        print(f"❌ 清理失败 / Cleanup failed: {str(e)}")
        return False


def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("内存监控集成测试 / Memory Monitoring Integration Test")
    print("="*60)
    
    results = []
    
    # 测试1: 导入
    results.append(test_memory_monitor_import())
    
    # 测试2: 创建
    success, monitor = test_memory_monitor_creation()
    results.append(success)
    
    if monitor:
        # 测试3: 获取统计
        results.append(test_memory_stats(monitor))
        
        # 测试4: 内存检查
        results.append(test_memory_check(monitor))
        
        # 测试5: 缓存管理器
        results.append(test_cache_manager())
        
        # 测试6: 清理
        results.append(test_cleanup(monitor))
    
    # 总结
    print("\n" + "="*60)
    print("测试总结 / Test Summary")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n通过测试 / Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ 所有测试通过！/ All tests passed!")
        print("内存监控集成成功 / Memory monitoring integration successful")
        return 0
    else:
        print(f"\n❌ {total - passed} 个测试失败 / {total - passed} tests failed")
        print("请检查错误信息 / Please check error messages")
        return 1


if __name__ == "__main__":
    sys.exit(main())
