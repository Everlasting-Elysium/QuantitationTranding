"""
通知服务测试脚本 / Notification Service Test Script
"""

import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# 直接导入模块，避免通过__init__.py
from src.infrastructure.notification_service import (
    NotificationService,
    NotificationConfig,
    get_notification_service,
    setup_notification
)
from src.infrastructure.logger_system import setup_logging, get_logger


def test_notification_service():
    """测试通知服务基本功能"""
    
    # 设置日志
    setup_logging(log_dir="logs", log_level="INFO")
    logger = get_logger("test_notification_service")
    
    logger.info("=" * 60)
    logger.info("开始测试通知服务 / Starting notification service test")
    logger.info("=" * 60)
    
    # 测试1: 创建通知服务实例
    logger.info("\n测试1: 创建通知服务实例")
    service = NotificationService()
    assert not service.is_initialized(), "服务不应该在创建时就初始化"
    logger.info("✓ 通知服务实例创建成功")
    
    # 测试2: 配置通知服务（仅启用系统通知）
    logger.info("\n测试2: 配置通知服务")
    config = NotificationConfig(
        email_enabled=False,  # 测试时不启用邮件
        sms_enabled=False     # 测试时不启用短信
    )
    service.setup(config)
    assert service.is_initialized(), "服务应该已初始化"
    logger.info("✓ 通知服务配置成功")
    
    # 测试3: 发送系统通知
    logger.info("\n测试3: 发送系统通知")
    service.send_system_notification(
        title="测试通知",
        message="这是一条测试系统通知",
        level="info"
    )
    logger.info("✓ 系统通知发送成功")
    
    # 测试4: 发送不同级别的系统通知
    logger.info("\n测试4: 发送不同级别的系统通知")
    service.send_system_notification(
        title="警告通知",
        message="这是一条警告通知",
        level="warning"
    )
    service.send_system_notification(
        title="错误通知",
        message="这是一条错误通知",
        level="error"
    )
    service.send_system_notification(
        title="严重通知",
        message="这是一条严重通知",
        level="critical"
    )
    logger.info("✓ 不同级别的系统通知发送成功")
    
    # 测试5: 发送风险预警（不启用邮件和短信）
    logger.info("\n测试5: 发送风险预警通知")
    alert = {
        'alert_type': '最大回撤预警',
        'severity': 'warning',
        'message': '投资组合回撤超过阈值',
        'timestamp': '2024-01-15 14:30:00',
        'current_value': -8.5,
        'threshold_value': -5.0,
        'affected_positions': ['600519.SH', '000858.SZ'],
        'recommended_actions': [
            '考虑减少高风险持仓',
            '增加防御性资产配置',
            '密切关注市场动态'
        ]
    }
    
    result = service.send_risk_alert(
        alert=alert,
        recipients=['test@example.com'],  # 不会实际发送
        phone_numbers=['13800138000']     # 不会实际发送
    )
    logger.info(f"✓ 风险预警通知处理完成 (实际发送: {result})")
    
    # 测试6: 测试未启用时的邮件发送
    logger.info("\n测试6: 测试未启用时的邮件发送")
    email_result = service.send_email(
        recipients=['test@example.com'],
        subject='测试邮件',
        body='这是一封测试邮件'
    )
    assert not email_result, "邮件未启用时应该返回False"
    logger.info("✓ 未启用邮件时正确返回False")
    
    # 测试7: 测试未启用时的短信发送
    logger.info("\n测试7: 测试未启用时的短信发送")
    sms_result = service.send_sms(
        phone_numbers=['13800138000'],
        message='测试短信'
    )
    assert not sms_result, "短信未启用时应该返回False"
    logger.info("✓ 未启用短信时正确返回False")
    
    # 测试8: 测试全局实例
    logger.info("\n测试8: 测试全局实例")
    global_service = get_notification_service()
    assert global_service is service, "全局实例应该与创建的实例相同"
    logger.info("✓ 全局实例获取成功")
    
    # 测试9: 测试便捷配置函数
    logger.info("\n测试9: 测试便捷配置函数")
    new_config = NotificationConfig(
        email_enabled=False,
        sms_enabled=False
    )
    setup_notification(new_config)
    logger.info("✓ 便捷配置函数测试成功")
    
    # 测试10: 测试配置获取
    logger.info("\n测试10: 测试配置获取")
    retrieved_config = service.get_config()
    assert retrieved_config is not None, "应该能获取到配置"
    assert retrieved_config.email_enabled == new_config.email_enabled
    logger.info("✓ 配置获取成功")
    
    logger.info("\n" + "=" * 60)
    logger.info("所有测试通过！/ All tests passed!")
    logger.info("=" * 60)


def test_email_html_generation():
    """测试风险预警邮件HTML生成"""
    
    logger = get_logger("test_email_html")
    logger.info("\n测试风险预警邮件HTML生成")
    
    service = NotificationService()
    config = NotificationConfig(email_enabled=False, sms_enabled=False)
    service.setup(config)
    
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
    
    html = service._build_risk_alert_email(alert)
    assert '<html>' in html, "应该包含HTML标签"
    assert '风险预警通知' in html, "应该包含标题"
    assert alert['message'] in html, "应该包含预警信息"
    assert str(alert['current_value']) in html, "应该包含当前值"
    
    logger.info("✓ 风险预警邮件HTML生成成功")
    logger.info(f"HTML长度: {len(html)} 字符")


if __name__ == '__main__':
    try:
        test_notification_service()
        test_email_html_generation()
        print("\n✅ 所有测试通过！")
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
