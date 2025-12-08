"""
报告调度器测试脚本 / Report Scheduler Test Script
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from src.application.report_scheduler import (
    ReportScheduler,
    ScheduleConfig,
    get_report_scheduler
)
from src.infrastructure.notification_service import (
    NotificationService,
    NotificationConfig
)
from src.infrastructure.logger_system import setup_logging, get_logger


def test_report_scheduler_basic():
    """测试报告调度器基本功能"""
    
    logger = get_logger("test_report_scheduler")
    
    logger.info("=" * 60)
    logger.info("开始测试报告调度器 / Starting report scheduler test")
    logger.info("=" * 60)
    
    # 测试1: 创建报告调度器实例
    logger.info("\n测试1: 创建报告调度器实例")
    scheduler = ReportScheduler()
    assert not scheduler.is_running(), "调度器不应该在创建时就运行"
    logger.info("✓ 报告调度器实例创建成功")
    
    # 测试2: 配置报告调度器
    logger.info("\n测试2: 配置报告调度器")
    
    # 创建通知服务（用于测试）
    notification_config = NotificationConfig(
        email_enabled=False,
        sms_enabled=False
    )
    notification_service = NotificationService()
    notification_service.setup(notification_config)
    
    # 创建调度配置
    schedule_config = ScheduleConfig(
        daily_enabled=True,
        daily_time="18:00",
        weekly_enabled=True,
        weekly_day=4,  # Friday
        weekly_time="18:00",
        monthly_enabled=True,
        monthly_day=1,
        monthly_time="18:00",
        risk_alert_enabled=True,
        risk_check_interval=60
    )
    
    # 配置调度器（不需要真实的report_generator，测试时可以传None）
    scheduler.setup(
        config=schedule_config,
        report_generator=None,  # 测试时可以为None
        notification_service=notification_service
    )
    
    assert scheduler.config is not None, "配置应该已设置"
    logger.info("✓ 报告调度器配置成功")
    
    # 测试3: 测试配置属性
    logger.info("\n测试3: 测试配置属性")
    assert scheduler.config.daily_enabled == True
    assert scheduler.config.daily_time == "18:00"
    assert scheduler.config.weekly_day == 4
    assert scheduler.config.risk_check_interval == 60
    logger.info("✓ 配置属性验证成功")
    
    # 测试4: 测试全局实例
    logger.info("\n测试4: 测试全局实例")
    global_scheduler = get_report_scheduler()
    assert global_scheduler is not None, "全局实例应该存在"
    logger.info("✓ 全局实例获取成功")
    
    # 测试5: 测试报告保存功能
    logger.info("\n测试5: 测试报告保存功能")
    test_content = "<html><body><h1>测试报告</h1></body></html>"
    report_path = scheduler._save_report(test_content, 'daily', '2024-01-15')
    assert Path(report_path).exists(), "报告文件应该已创建"
    logger.info(f"✓ 报告保存成功: {report_path}")
    
    # 测试6: 测试报告格式化
    logger.info("\n测试6: 测试报告格式化")
    
    daily_data = {
        'date': '2024-01-15',
        'returns': 2.5,
        'total_value': 100000.0,
        'portfolio': None,
        'trades': []
    }
    daily_report = scheduler._format_daily_report(daily_data)
    assert '<html>' in daily_report, "应该包含HTML标签"
    assert '2024-01-15' in daily_report, "应该包含日期"
    assert '2.5' in daily_report or '2.50' in daily_report, "应该包含收益率"
    logger.info("✓ 每日报告格式化成功")
    
    weekly_data = {
        'start_date': '2024-01-08',
        'end_date': '2024-01-14',
        'weekly_return': 5.2,
        'trades_count': 10,
        'win_rate': 70.0
    }
    weekly_report = scheduler._format_weekly_report(weekly_data, '2024-01-08', '2024-01-14')
    assert '<html>' in weekly_report, "应该包含HTML标签"
    assert '5.2' in weekly_report or '5.20' in weekly_report, "应该包含周收益率"
    logger.info("✓ 每周报告格式化成功")
    
    monthly_data = {
        'start_date': '2024-01-01',
        'end_date': '2024-01-31',
        'monthly_return': 8.5,
        'annualized_return': 102.0,
        'sharpe_ratio': 1.8,
        'max_drawdown': -5.2
    }
    monthly_report = scheduler._format_monthly_report(monthly_data, '2024-01-01', '2024-01-31')
    assert '<html>' in monthly_report, "应该包含HTML标签"
    assert '8.5' in monthly_report or '8.50' in monthly_report, "应该包含月度收益率"
    logger.info("✓ 每月报告格式化成功")
    
    # 测试7: 测试启动和停止（短时间运行）
    logger.info("\n测试7: 测试启动和停止")
    
    # 使用较短的检查间隔进行测试
    test_config = ScheduleConfig(
        daily_enabled=False,
        weekly_enabled=False,
        monthly_enabled=False,
        risk_alert_enabled=False
    )
    
    test_scheduler = ReportScheduler()
    test_scheduler.setup(
        config=test_config,
        report_generator=None,
        notification_service=notification_service
    )
    
    test_scheduler.start()
    assert test_scheduler.is_running(), "调度器应该正在运行"
    logger.info("✓ 调度器启动成功")
    
    # 运行2秒
    time.sleep(2)
    
    test_scheduler.stop()
    assert not test_scheduler.is_running(), "调度器应该已停止"
    logger.info("✓ 调度器停止成功")
    
    # 测试8: 测试重复启动保护
    logger.info("\n测试8: 测试重复启动保护")
    test_scheduler.start()
    test_scheduler.start()  # 第二次启动应该被忽略
    assert test_scheduler.is_running(), "调度器应该正在运行"
    test_scheduler.stop()
    logger.info("✓ 重复启动保护正常")
    
    logger.info("\n" + "=" * 60)
    logger.info("所有测试通过！/ All tests passed!")
    logger.info("=" * 60)


def test_schedule_config():
    """测试调度配置"""
    
    logger = get_logger("test_schedule_config")
    logger.info("\n测试调度配置 / Testing schedule configuration")
    
    # 测试默认配置
    config = ScheduleConfig()
    assert config.daily_enabled == True
    assert config.daily_time == "18:00"
    assert config.weekly_day == 4  # Friday
    assert config.risk_check_interval == 60
    logger.info("✓ 默认配置正确")
    
    # 测试自定义配置
    custom_config = ScheduleConfig(
        daily_enabled=False,
        weekly_enabled=False,
        monthly_enabled=False,
        risk_alert_enabled=False
    )
    assert custom_config.daily_enabled == False
    assert custom_config.weekly_enabled == False
    logger.info("✓ 自定义配置正确")


def test_report_paths():
    """测试报告路径生成"""
    
    logger = get_logger("test_report_paths")
    logger.info("\n测试报告路径生成 / Testing report path generation")
    
    scheduler = ReportScheduler()
    
    # 测试每日报告路径
    daily_path = scheduler._save_report("<html>test</html>", 'daily', '2024-01-15')
    assert 'reports/daily' in daily_path
    assert '2024-01-15' in daily_path
    assert daily_path.endswith('.html')
    logger.info(f"✓ 每日报告路径: {daily_path}")
    
    # 测试每周报告路径
    weekly_path = scheduler._save_report("<html>test</html>", 'weekly', '2024-W03')
    assert 'reports/weekly' in weekly_path
    assert '2024-W03' in weekly_path
    logger.info(f"✓ 每周报告路径: {weekly_path}")
    
    # 测试每月报告路径
    monthly_path = scheduler._save_report("<html>test</html>", 'monthly', '2024-01')
    assert 'reports/monthly' in monthly_path
    assert '2024-01' in monthly_path
    logger.info(f"✓ 每月报告路径: {monthly_path}")


def main():
    """主函数 / Main function"""
    
    # 设置日志
    setup_logging(log_dir="logs", log_level="INFO")
    
    print("\n" + "=" * 60)
    print("报告调度器测试程序 / Report Scheduler Test Program")
    print("=" * 60)
    
    try:
        test_schedule_config()
        test_report_paths()
        test_report_scheduler_basic()
        
        print("\n✅ 所有测试通过！/ All tests passed!")
        return 0
        
    except AssertionError as e:
        print(f"\n❌ 测试失败 / Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    except Exception as e:
        print(f"\n❌ 测试出错 / Test error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
