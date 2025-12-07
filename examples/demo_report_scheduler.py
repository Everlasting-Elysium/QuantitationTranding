"""
报告调度器示例 / Report Scheduler Demo
演示如何使用报告调度器定期生成和发送交易报告
Demonstrates how to use report scheduler to periodically generate and send trading reports
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

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


def demo_basic_usage():
    """演示基本使用方法 / Demonstrate basic usage"""
    
    print("\n" + "=" * 60)
    print("示例1: 基本使用方法 / Example 1: Basic Usage")
    print("=" * 60)
    
    # 1. 创建通知服务
    notification_config = NotificationConfig(
        email_enabled=False,  # 设置为True并填写真实信息以启用
        sms_enabled=False
    )
    notification_service = NotificationService()
    notification_service.setup(notification_config)
    
    # 2. 创建调度配置
    schedule_config = ScheduleConfig(
        daily_enabled=True,
        daily_time="18:00",  # 每天18:00生成每日报告
        weekly_enabled=True,
        weekly_day=4,  # 周五
        weekly_time="18:00",
        monthly_enabled=True,
        monthly_day=1,  # 每月1日
        monthly_time="18:00",
        risk_alert_enabled=True,
        risk_check_interval=60  # 每60分钟检查一次风险
    )
    
    # 3. 创建并配置报告调度器
    scheduler = ReportScheduler()
    scheduler.setup(
        config=schedule_config,
        report_generator=None,  # 实际使用时需要传入ReportGenerator实例
        notification_service=notification_service
    )
    
    print("✓ 报告调度器配置完成")
    print(f"  - 每日报告: {'已启用' if schedule_config.daily_enabled else '未启用'} @ {schedule_config.daily_time}")
    print(f"  - 每周报告: {'已启用' if schedule_config.weekly_enabled else '未启用'} @ 周五 {schedule_config.weekly_time}")
    print(f"  - 每月报告: {'已启用' if schedule_config.monthly_enabled else '未启用'} @ 每月{schedule_config.monthly_day}日 {schedule_config.monthly_time}")
    print(f"  - 风险预警: {'已启用' if schedule_config.risk_alert_enabled else '未启用'} (每{schedule_config.risk_check_interval}分钟)")


def demo_start_stop():
    """演示启动和停止调度器 / Demonstrate starting and stopping scheduler"""
    
    print("\n" + "=" * 60)
    print("示例2: 启动和停止调度器 / Example 2: Start and Stop Scheduler")
    print("=" * 60)
    
    # 创建配置
    notification_service = NotificationService()
    notification_service.setup(NotificationConfig(email_enabled=False, sms_enabled=False))
    
    schedule_config = ScheduleConfig(
        daily_enabled=True,
        weekly_enabled=True,
        monthly_enabled=True,
        risk_alert_enabled=True
    )
    
    scheduler = ReportScheduler()
    scheduler.setup(
        config=schedule_config,
        report_generator=None,
        notification_service=notification_service
    )
    
    # 启动调度器
    print("\n启动调度器...")
    scheduler.start()
    print(f"✓ 调度器已启动，状态: {'运行中' if scheduler.is_running() else '已停止'}")
    
    # 获取下次运行时间
    next_runs = scheduler.get_next_run_times()
    if next_runs:
        print("\n下次运行时间:")
        for report_type, next_time in next_runs.items():
            print(f"  - {report_type}: {next_time}")
    
    # 运行5秒
    print("\n调度器运行中...")
    for i in range(5):
        time.sleep(1)
        print(f"  {i+1}秒...")
    
    # 停止调度器
    print("\n停止调度器...")
    scheduler.stop()
    print(f"✓ 调度器已停止，状态: {'运行中' if scheduler.is_running() else '已停止'}")


def demo_report_generation():
    """演示报告生成 / Demonstrate report generation"""
    
    print("\n" + "=" * 60)
    print("示例3: 报告生成 / Example 3: Report Generation")
    print("=" * 60)
    
    scheduler = ReportScheduler()
    
    # 生成每日报告
    print("\n生成每日报告...")
    daily_data = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'returns': 2.5,
        'total_value': 105000.0,
        'portfolio': None,
        'trades': []
    }
    daily_report = scheduler._format_daily_report(daily_data)
    daily_path = scheduler._save_report(daily_report, 'daily', daily_data['date'])
    print(f"✓ 每日报告已生成: {daily_path}")
    print(f"  - 日期: {daily_data['date']}")
    print(f"  - 收益率: {daily_data['returns']}%")
    print(f"  - 组合价值: ¥{daily_data['total_value']:,.2f}")
    
    # 生成每周报告
    print("\n生成每周报告...")
    weekly_data = {
        'start_date': '2024-01-08',
        'end_date': '2024-01-14',
        'weekly_return': 5.2,
        'trades_count': 12,
        'win_rate': 75.0
    }
    weekly_report = scheduler._format_weekly_report(weekly_data, weekly_data['start_date'], weekly_data['end_date'])
    weekly_path = scheduler._save_report(weekly_report, 'weekly', '2024-W02')
    print(f"✓ 每周报告已生成: {weekly_path}")
    print(f"  - 周期: {weekly_data['start_date']} 至 {weekly_data['end_date']}")
    print(f"  - 周收益率: {weekly_data['weekly_return']}%")
    print(f"  - 交易次数: {weekly_data['trades_count']}")
    print(f"  - 胜率: {weekly_data['win_rate']}%")
    
    # 生成每月报告
    print("\n生成每月报告...")
    monthly_data = {
        'start_date': '2024-01-01',
        'end_date': '2024-01-31',
        'monthly_return': 8.5,
        'annualized_return': 102.0,
        'sharpe_ratio': 1.8,
        'max_drawdown': -5.2
    }
    monthly_report = scheduler._format_monthly_report(monthly_data, monthly_data['start_date'], monthly_data['end_date'])
    monthly_path = scheduler._save_report(monthly_report, 'monthly', '2024-01')
    print(f"✓ 每月报告已生成: {monthly_path}")
    print(f"  - 月份: 2024年1月")
    print(f"  - 月度收益率: {monthly_data['monthly_return']}%")
    print(f"  - 年化收益率: {monthly_data['annualized_return']}%")
    print(f"  - 夏普比率: {monthly_data['sharpe_ratio']}")
    print(f"  - 最大回撤: {monthly_data['max_drawdown']}%")


def demo_custom_schedule():
    """演示自定义调度配置 / Demonstrate custom schedule configuration"""
    
    print("\n" + "=" * 60)
    print("示例4: 自定义调度配置 / Example 4: Custom Schedule Configuration")
    print("=" * 60)
    
    # 场景1: 只启用每日报告
    print("\n场景1: 只启用每日报告")
    config1 = ScheduleConfig(
        daily_enabled=True,
        daily_time="17:30",
        weekly_enabled=False,
        monthly_enabled=False,
        risk_alert_enabled=False
    )
    print(f"✓ 配置: 每日报告 @ {config1.daily_time}")
    
    # 场景2: 启用所有报告，自定义时间
    print("\n场景2: 启用所有报告，自定义时间")
    config2 = ScheduleConfig(
        daily_enabled=True,
        daily_time="20:00",
        weekly_enabled=True,
        weekly_day=0,  # 周一
        weekly_time="09:00",
        monthly_enabled=True,
        monthly_day=5,  # 每月5日
        monthly_time="10:00",
        risk_alert_enabled=True,
        risk_check_interval=30  # 每30分钟检查一次
    )
    print(f"✓ 配置:")
    print(f"  - 每日报告: {config2.daily_time}")
    print(f"  - 每周报告: 周一 {config2.weekly_time}")
    print(f"  - 每月报告: 每月{config2.monthly_day}日 {config2.monthly_time}")
    print(f"  - 风险检查: 每{config2.risk_check_interval}分钟")
    
    # 场景3: 只启用风险预警
    print("\n场景3: 只启用风险预警")
    config3 = ScheduleConfig(
        daily_enabled=False,
        weekly_enabled=False,
        monthly_enabled=False,
        risk_alert_enabled=True,
        risk_check_interval=15  # 每15分钟检查一次
    )
    print(f"✓ 配置: 风险预警 (每{config3.risk_check_interval}分钟)")


def demo_real_world_scenario():
    """演示真实场景应用 / Demonstrate real-world scenario"""
    
    print("\n" + "=" * 60)
    print("示例5: 真实场景应用 / Example 5: Real-world Scenario")
    print("=" * 60)
    
    print("\n场景：量化交易系统的完整报告调度")
    print("-" * 60)
    
    # 1. 配置通知服务
    print("\n步骤1: 配置通知服务")
    notification_config = NotificationConfig(
        email_enabled=False,  # 实际使用时设置为True
        email_smtp_server="smtp.qq.com",
        email_smtp_port=587,
        email_username="your_email@qq.com",
        email_password="your_authorization_code",
        sms_enabled=False  # 实际使用时设置为True
    )
    notification_service = NotificationService()
    notification_service.setup(notification_config)
    print("✓ 通知服务配置完成")
    
    # 2. 配置报告调度
    print("\n步骤2: 配置报告调度")
    schedule_config = ScheduleConfig(
        daily_enabled=True,
        daily_time="18:00",  # 每天收盘后生成报告
        weekly_enabled=True,
        weekly_day=4,  # 周五
        weekly_time="18:30",
        monthly_enabled=True,
        monthly_day=1,  # 每月第一天
        monthly_time="09:00",
        risk_alert_enabled=True,
        risk_check_interval=60  # 每小时检查风险
    )
    print("✓ 调度配置完成")
    
    # 3. 创建并启动调度器
    print("\n步骤3: 创建并启动调度器")
    scheduler = ReportScheduler()
    scheduler.setup(
        config=schedule_config,
        report_generator=None,  # 实际使用时传入ReportGenerator实例
        notification_service=notification_service,
        risk_manager=None,  # 实际使用时传入RiskManager实例
        portfolio_manager=None,  # 实际使用时传入PortfolioManager实例
        simulation_engine=None,  # 如果是模拟交易
        live_trading_manager=None  # 如果是实盘交易
    )
    print("✓ 调度器配置完成")
    
    # 4. 启动调度器
    print("\n步骤4: 启动调度器")
    scheduler.start()
    print("✓ 调度器已启动")
    print("\n调度器将在后台运行，定期执行以下任务:")
    print("  - 每天18:00生成每日报告")
    print("  - 每周五18:30生成每周报告")
    print("  - 每月1日09:00生成每月报告")
    print("  - 每小时检查一次风险状况")
    print("  - 检测到风险时立即发送预警")
    
    # 5. 模拟运行
    print("\n步骤5: 模拟运行（5秒）")
    for i in range(5):
        time.sleep(1)
        print(f"  运行中... {i+1}秒")
    
    # 6. 停止调度器
    print("\n步骤6: 停止调度器")
    scheduler.stop()
    print("✓ 调度器已停止")
    
    print("\n" + "=" * 60)
    print("真实场景演示完成！")
    print("=" * 60)


def demo_integration_tips():
    """演示集成建议 / Demonstrate integration tips"""
    
    print("\n" + "=" * 60)
    print("示例6: 集成建议 / Example 6: Integration Tips")
    print("=" * 60)
    
    print("\n💡 集成建议:")
    print("\n1. 在系统启动时初始化报告调度器")
    print("   - 在main.py或启动脚本中创建和配置调度器")
    print("   - 调用scheduler.start()启动后台任务")
    
    print("\n2. 传入必要的依赖")
    print("   - report_generator: 用于生成报告内容")
    print("   - notification_service: 用于发送通知")
    print("   - risk_manager: 用于风险检查")
    print("   - portfolio_manager: 用于获取持仓信息")
    
    print("\n3. 配置通知接收人")
    print("   - 在配置文件中设置邮件接收人列表")
    print("   - 在配置文件中设置短信接收人列表")
    
    print("\n4. 自定义报告内容")
    print("   - 可以重写_format_daily_report()等方法")
    print("   - 可以添加自定义的数据收集逻辑")
    
    print("\n5. 监控调度器状态")
    print("   - 使用scheduler.is_running()检查运行状态")
    print("   - 使用scheduler.get_next_run_times()查看下次运行时间")
    
    print("\n6. 优雅关闭")
    print("   - 在系统退出前调用scheduler.stop()")
    print("   - 确保所有后台任务正常结束")


def main():
    """主函数 / Main function"""
    
    # 设置日志
    setup_logging(log_dir="logs", log_level="INFO")
    
    print("\n" + "=" * 60)
    print("报告调度器示例程序 / Report Scheduler Demo")
    print("=" * 60)
    
    try:
        # 演示各种功能
        demo_basic_usage()
        demo_start_stop()
        demo_report_generation()
        demo_custom_schedule()
        demo_real_world_scenario()
        demo_integration_tips()
        
        print("\n" + "=" * 60)
        print("所有示例演示完成！/ All demos completed!")
        print("=" * 60)
        
        print("\n💡 提示 / Tips:")
        print("1. 报告调度器会在后台自动运行")
        print("2. 可以通过配置文件自定义调度时间")
        print("3. 支持每日、每周、每月报告和实时风险预警")
        print("4. 集成通知服务可以自动发送报告")
        print("5. 所有报告都会保存到reports/目录")
        
    except Exception as e:
        print(f"\n❌ 程序出错: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
