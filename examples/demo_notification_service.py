"""
通知服务示例 / Notification Service Demo
演示如何使用通知服务发送邮件、短信和系统通知
Demonstrates how to use notification service to send emails, SMS, and system notifications
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.infrastructure.notification_service import (
    NotificationService,
    NotificationConfig,
    get_notification_service,
    setup_notification
)
from src.infrastructure.logger_system import setup_logging, get_logger


def demo_basic_usage():
    """演示基本使用方法 / Demonstrate basic usage"""
    
    print("\n" + "=" * 60)
    print("示例1: 基本使用方法 / Example 1: Basic Usage")
    print("=" * 60)
    
    # 1. 创建配置
    config = NotificationConfig(
        # 邮件配置 / Email configuration
        email_enabled=False,  # 设置为True并填写真实信息以启用 / Set to True with real info to enable
        email_smtp_server="smtp.example.com",
        email_smtp_port=587,
        email_username="your_email@example.com",
        email_password="your_password",
        email_from="your_email@example.com",
        
        # 短信配置 / SMS configuration
        sms_enabled=False,  # 设置为True并填写真实信息以启用 / Set to True with real info to enable
        sms_api_key="your_api_key",
        sms_api_url="https://api.sms-provider.com/send",
        sms_signature="量化交易系统"
    )
    
    # 2. 初始化通知服务
    service = NotificationService()
    service.setup(config)
    
    print("✓ 通知服务初始化成功")
    print(f"  - 邮件通知: {'已启用' if config.email_enabled else '未启用'}")
    print(f"  - 短信通知: {'已启用' if config.sms_enabled else '未启用'}")


def demo_system_notification():
    """演示系统通知 / Demonstrate system notifications"""
    
    print("\n" + "=" * 60)
    print("示例2: 系统通知 / Example 2: System Notifications")
    print("=" * 60)
    
    service = get_notification_service()
    
    # 发送不同级别的系统通知
    print("\n发送不同级别的系统通知...")
    
    service.send_system_notification(
        title="信息通知",
        message="系统正常运行中",
        level="info"
    )
    print("✓ INFO级别通知已发送")
    
    service.send_system_notification(
        title="警告通知",
        message="检测到轻微异常，请注意",
        level="warning"
    )
    print("✓ WARNING级别通知已发送")
    
    service.send_system_notification(
        title="错误通知",
        message="发生错误，需要处理",
        level="error"
    )
    print("✓ ERROR级别通知已发送")
    
    service.send_system_notification(
        title="严重通知",
        message="发生严重问题，立即处理！",
        level="critical"
    )
    print("✓ CRITICAL级别通知已发送")


def demo_email_notification():
    """演示邮件通知 / Demonstrate email notifications"""
    
    print("\n" + "=" * 60)
    print("示例3: 邮件通知 / Example 3: Email Notifications")
    print("=" * 60)
    
    service = get_notification_service()
    
    # 示例：发送简单文本邮件
    print("\n发送简单文本邮件...")
    result = service.send_email(
        recipients=["user1@example.com", "user2@example.com"],
        subject="量化交易系统 - 每日报告",
        body="今日交易已完成，总收益率: +2.5%"
    )
    print(f"{'✓' if result else '✗'} 邮件发送{'成功' if result else '失败（可能未启用）'}")
    
    # 示例：发送HTML格式邮件
    print("\n发送HTML格式邮件...")
    html_body = """
    <html>
    <body>
        <h2>每日交易报告</h2>
        <p>尊敬的用户：</p>
        <p>今日交易已完成，详情如下：</p>
        <ul>
            <li>总收益率: <strong>+2.5%</strong></li>
            <li>交易次数: 5</li>
            <li>胜率: 80%</li>
        </ul>
        <p>祝投资顺利！</p>
    </body>
    </html>
    """
    result = service.send_email(
        recipients=["user@example.com"],
        subject="量化交易系统 - 每日报告（HTML）",
        body=html_body,
        html=True
    )
    print(f"{'✓' if result else '✗'} HTML邮件发送{'成功' if result else '失败（可能未启用）'}")
    
    # 示例：发送带附件的邮件
    print("\n发送带附件的邮件...")
    result = service.send_email(
        recipients=["user@example.com"],
        subject="量化交易系统 - 月度报告",
        body="请查看附件中的详细报告",
        attachments=["reports/monthly_report.pdf", "reports/charts.png"]
    )
    print(f"{'✓' if result else '✗'} 带附件邮件发送{'成功' if result else '失败（可能未启用或文件不存在）'}")


def demo_sms_notification():
    """演示短信通知 / Demonstrate SMS notifications"""
    
    print("\n" + "=" * 60)
    print("示例4: 短信通知 / Example 4: SMS Notifications")
    print("=" * 60)
    
    service = get_notification_service()
    
    # 示例：发送简单短信
    print("\n发送简单短信...")
    result = service.send_sms(
        phone_numbers=["13800138000", "13900139000"],
        message="您的量化交易系统今日收益率为+2.5%，请查收详细报告。"
    )
    print(f"{'✓' if result else '✗'} 短信发送{'成功' if result else '失败（可能未启用）'}")


def demo_risk_alert():
    """演示风险预警通知 / Demonstrate risk alert notifications"""
    
    print("\n" + "=" * 60)
    print("示例5: 风险预警通知 / Example 5: Risk Alert Notifications")
    print("=" * 60)
    
    service = get_notification_service()
    
    # 示例1: 最大回撤预警
    print("\n发送最大回撤预警...")
    alert = {
        'alert_type': '最大回撤预警',
        'severity': 'warning',
        'message': '投资组合回撤超过阈值',
        'timestamp': '2024-01-15 14:30:00',
        'current_value': -8.5,
        'threshold_value': -5.0,
        'affected_positions': ['600519.SH 贵州茅台', '000858.SZ 五粮液'],
        'recommended_actions': [
            '考虑减少高风险持仓',
            '增加防御性资产配置',
            '密切关注市场动态'
        ]
    }
    
    result = service.send_risk_alert(
        alert=alert,
        recipients=["trader@example.com"],
        phone_numbers=["13800138000"]
    )
    print(f"{'✓' if result else '✗'} 最大回撤预警发送{'成功' if result else '失败（可能未启用）'}")
    
    # 示例2: 持仓集中度风险预警
    print("\n发送持仓集中度风险预警...")
    alert = {
        'alert_type': '持仓集中度风险',
        'severity': 'critical',
        'message': '单只股票持仓比例超过安全阈值',
        'timestamp': '2024-01-15 15:45:00',
        'current_value': 45.5,
        'threshold_value': 40.0,
        'affected_positions': ['600519.SH 贵州茅台'],
        'recommended_actions': [
            '立即减持超配股票',
            '分散投资到其他标的',
            '重新评估风险承受能力'
        ]
    }
    
    result = service.send_risk_alert(
        alert=alert,
        recipients=["trader@example.com", "risk_manager@example.com"],
        phone_numbers=["13800138000"]
    )
    print(f"{'✓' if result else '✗'} 持仓集中度风险预警发送{'成功' if result else '失败（可能未启用）'}")
    
    # 示例3: 日内亏损预警
    print("\n发送日内亏损预警...")
    alert = {
        'alert_type': '日内亏损预警',
        'severity': 'critical',
        'message': '今日亏损超过日内止损线',
        'timestamp': '2024-01-15 14:00:00',
        'current_value': -3.2,
        'threshold_value': -2.0,
        'affected_positions': ['300750.SZ 宁德时代', '002594.SZ 比亚迪'],
        'recommended_actions': [
            '立即停止交易',
            '检查策略参数',
            '等待市场稳定后再操作'
        ]
    }
    
    result = service.send_risk_alert(
        alert=alert,
        recipients=["trader@example.com"],
        phone_numbers=["13800138000"]
    )
    print(f"{'✓' if result else '✗'} 日内亏损预警发送{'成功' if result else '失败（可能未启用）'}")


def demo_real_world_scenario():
    """演示真实场景应用 / Demonstrate real-world scenario"""
    
    print("\n" + "=" * 60)
    print("示例6: 真实场景应用 / Example 6: Real-world Scenario")
    print("=" * 60)
    
    service = get_notification_service()
    
    print("\n场景：每日交易结束后发送报告")
    print("-" * 60)
    
    # 1. 记录系统通知
    service.send_system_notification(
        title="每日交易结束",
        message="今日交易已完成，开始生成报告",
        level="info"
    )
    print("✓ 系统通知：交易结束")
    
    # 2. 发送每日报告邮件
    daily_report = """
    <html>
    <body>
        <h2>每日交易报告 - 2024年1月15日</h2>
        
        <h3>📊 今日概况</h3>
        <ul>
            <li>总收益率: <strong style="color: green;">+2.5%</strong></li>
            <li>交易次数: 5</li>
            <li>胜率: 80%</li>
            <li>最大单笔收益: +1.2%</li>
            <li>最大单笔亏损: -0.3%</li>
        </ul>
        
        <h3>💼 持仓情况</h3>
        <table border="1" style="border-collapse: collapse;">
            <tr>
                <th>股票代码</th>
                <th>持仓数量</th>
                <th>成本价</th>
                <th>当前价</th>
                <th>盈亏</th>
            </tr>
            <tr>
                <td>600519.SH</td>
                <td>100</td>
                <td>1800</td>
                <td>1850</td>
                <td style="color: green;">+2.78%</td>
            </tr>
            <tr>
                <td>300750.SZ</td>
                <td>200</td>
                <td>180</td>
                <td>185</td>
                <td style="color: green;">+2.78%</td>
            </tr>
        </table>
        
        <h3>📈 下一交易日建议</h3>
        <ul>
            <li>继续持有现有仓位</li>
            <li>关注市场整体走势</li>
            <li>准备适当加仓优质标的</li>
        </ul>
        
        <p style="color: #666; font-size: 12px;">
            此邮件由量化交易系统自动发送<br>
            如有问题请联系系统管理员
        </p>
    </body>
    </html>
    """
    
    result = service.send_email(
        recipients=["trader@example.com"],
        subject="【量化交易】每日交易报告 - 2024-01-15",
        body=daily_report,
        html=True,
        attachments=["reports/daily_chart.png"]
    )
    print(f"{'✓' if result else '✗'} 每日报告邮件发送{'成功' if result else '失败（可能未启用）'}")
    
    # 3. 如果有风险，发送预警
    print("\n检查风险指标...")
    max_drawdown = -8.5
    if max_drawdown < -5.0:
        print("⚠️  检测到风险：最大回撤超过阈值")
        
        alert = {
            'alert_type': '最大回撤预警',
            'severity': 'warning',
            'message': '投资组合回撤超过阈值',
            'timestamp': '2024-01-15 16:00:00',
            'current_value': max_drawdown,
            'threshold_value': -5.0,
            'affected_positions': ['600519.SH', '300750.SZ'],
            'recommended_actions': [
                '考虑减少高风险持仓',
                '增加防御性资产配置',
                '密切关注市场动态'
            ]
        }
        
        result = service.send_risk_alert(
            alert=alert,
            recipients=["trader@example.com", "risk_manager@example.com"],
            phone_numbers=["13800138000"]
        )
        print(f"{'✓' if result else '✗'} 风险预警发送{'成功' if result else '失败（可能未启用）'}")
    else:
        print("✓ 风险指标正常")
    
    # 4. 发送简短的短信摘要
    sms_summary = f"今日交易完成。收益率+2.5%，交易5次，胜率80%。{'注意：回撤超标' if max_drawdown < -5.0 else '风险正常'}。详见邮件报告。"
    result = service.send_sms(
        phone_numbers=["13800138000"],
        message=sms_summary
    )
    print(f"{'✓' if result else '✗'} 短信摘要发送{'成功' if result else '失败（可能未启用）'}")


def main():
    """主函数 / Main function"""
    
    # 设置日志
    setup_logging(log_dir="logs", log_level="INFO")
    
    print("\n" + "=" * 60)
    print("通知服务示例程序 / Notification Service Demo")
    print("=" * 60)
    
    # 初始化通知服务
    demo_basic_usage()
    
    # 演示各种通知功能
    demo_system_notification()
    demo_email_notification()
    demo_sms_notification()
    demo_risk_alert()
    demo_real_world_scenario()
    
    print("\n" + "=" * 60)
    print("所有示例演示完成！/ All demos completed!")
    print("=" * 60)
    
    print("\n💡 提示 / Tips:")
    print("1. 要启用邮件通知，请在配置中设置 email_enabled=True 并填写真实的SMTP信息")
    print("2. 要启用短信通知，请在配置中设置 sms_enabled=True 并填写真实的API信息")
    print("3. 系统通知会记录到日志文件中，可以在 logs/ 目录查看")
    print("4. 可以在 config/notification_config.yaml 中配置通知参数")
    print("5. 风险预警会同时发送邮件、短信和系统通知（如果启用）")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ 程序出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
