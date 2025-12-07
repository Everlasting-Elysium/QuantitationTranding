# 通知服务文档 / Notification Service Documentation

## 概述 / Overview

通知服务（NotificationService）是量化交易系统的核心基础设施组件，负责向用户发送各种类型的通知，包括邮件、短信和系统通知。该服务特别适用于发送交易报告、风险预警和系统状态更新。

The Notification Service is a core infrastructure component of the quantitative trading system, responsible for sending various types of notifications to users, including emails, SMS, and system notifications. This service is particularly suitable for sending trading reports, risk alerts, and system status updates.

## 主要功能 / Key Features

### 1. 邮件通知 / Email Notifications
- 支持纯文本和HTML格式邮件 / Supports plain text and HTML format emails
- 支持多个收件人 / Supports multiple recipients
- 支持附件发送 / Supports attachments
- 使用SMTP协议，兼容主流邮箱服务 / Uses SMTP protocol, compatible with mainstream email services

### 2. 短信通知 / SMS Notifications
- 支持批量发送 / Supports batch sending
- 自定义短信签名 / Custom SMS signature
- 通过API接口对接短信服务商 / Integrates with SMS providers via API

### 3. 系统通知 / System Notifications
- 多级别日志记录（INFO/WARNING/ERROR/CRITICAL）/ Multi-level logging
- 自动记录到日志文件 / Automatically logs to file
- 便于系统监控和调试 / Facilitates system monitoring and debugging

### 4. 风险预警通知 / Risk Alert Notifications
- 自动生成格式化的预警邮件 / Automatically generates formatted alert emails
- 同时支持邮件和短信通知 / Supports both email and SMS notifications
- 包含详细的风险信息和建议操作 / Contains detailed risk information and recommended actions

## 快速开始 / Quick Start

### 1. 基本配置 / Basic Configuration

```python
from src.infrastructure.notification_service import (
    NotificationService,
    NotificationConfig
)

# 创建配置
config = NotificationConfig(
    # 邮件配置
    email_enabled=True,
    email_smtp_server="smtp.example.com",
    email_smtp_port=587,
    email_username="your_email@example.com",
    email_password="your_password",
    email_from="your_email@example.com",
    
    # 短信配置
    sms_enabled=True,
    sms_api_key="your_api_key",
    sms_api_url="https://api.sms-provider.com/send",
    sms_signature="量化交易系统"
)

# 初始化服务
service = NotificationService()
service.setup(config)
```

### 2. 发送系统通知 / Send System Notification

```python
service.send_system_notification(
    title="系统启动",
    message="量化交易系统已成功启动",
    level="info"
)
```

### 3. 发送邮件 / Send Email

```python
# 发送简单文本邮件
service.send_email(
    recipients=["user@example.com"],
    subject="每日交易报告",
    body="今日交易已完成，总收益率: +2.5%"
)

# 发送HTML邮件
html_body = """
<html>
<body>
    <h2>每日交易报告</h2>
    <p>今日收益率: <strong>+2.5%</strong></p>
</body>
</html>
"""
service.send_email(
    recipients=["user@example.com"],
    subject="每日交易报告",
    body=html_body,
    html=True
)

# 发送带附件的邮件
service.send_email(
    recipients=["user@example.com"],
    subject="月度报告",
    body="请查看附件",
    attachments=["reports/monthly_report.pdf"]
)
```

### 4. 发送短信 / Send SMS

```python
service.send_sms(
    phone_numbers=["13800138000"],
    message="您的量化交易系统今日收益率为+2.5%"
)
```

### 5. 发送风险预警 / Send Risk Alert

```python
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
        '增加防御性资产配置'
    ]
}

service.send_risk_alert(
    alert=alert,
    recipients=["trader@example.com"],
    phone_numbers=["13800138000"]
)
```

## 配置文件 / Configuration File

通知服务支持通过YAML配置文件进行配置。配置文件位于 `config/notification_config.yaml`。

The notification service supports configuration via YAML file located at `config/notification_config.yaml`.

### 配置示例 / Configuration Example

```yaml
# 邮件通知配置
email:
  enabled: true
  smtp_server: "smtp.qq.com"
  smtp_port: 587
  username: "your_email@qq.com"
  password: "your_authorization_code"
  from: "your_email@qq.com"

# 短信通知配置
sms:
  enabled: true
  api_key: "your_sms_api_key"
  api_url: "https://api.sms-provider.com/send"
  signature: "量化交易系统"

# 通知接收人配置
recipients:
  emails:
    - "user1@example.com"
    - "user2@example.com"
  phone_numbers:
    - "13800138000"
    - "13900139000"

# 通知触发条件
triggers:
  daily_report:
    enabled: true
    time: "18:00"
  
  weekly_report:
    enabled: true
    day: "Friday"
    time: "18:00"
  
  risk_alert:
    enabled: true
    levels:
      - "warning"
      - "critical"
    methods:
      email: true
      sms: true
```

## 常用邮箱配置 / Common Email Configurations

### QQ邮箱 / QQ Mail

```python
config = NotificationConfig(
    email_enabled=True,
    email_smtp_server="smtp.qq.com",
    email_smtp_port=587,
    email_username="your_email@qq.com",
    email_password="your_authorization_code",  # 需要在QQ邮箱设置中获取授权码
    email_from="your_email@qq.com"
)
```

**注意 / Note**: 需要在QQ邮箱设置中开启SMTP服务并获取授权码，而不是使用QQ密码。
You need to enable SMTP service in QQ Mail settings and get an authorization code instead of using your QQ password.

### 163邮箱 / 163 Mail

```python
config = NotificationConfig(
    email_enabled=True,
    email_smtp_server="smtp.163.com",
    email_smtp_port=465,
    email_username="your_email@163.com",
    email_password="your_authorization_code",
    email_from="your_email@163.com"
)
```

### Gmail

```python
config = NotificationConfig(
    email_enabled=True,
    email_smtp_server="smtp.gmail.com",
    email_smtp_port=587,
    email_username="your_email@gmail.com",
    email_password="your_app_password",  # 需要使用应用专用密码
    email_from="your_email@gmail.com"
)
```

**注意 / Note**: Gmail需要开启"允许不够安全的应用访问"或使用应用专用密码。
Gmail requires enabling "Allow less secure apps" or using an app-specific password.

### Outlook

```python
config = NotificationConfig(
    email_enabled=True,
    email_smtp_server="smtp-mail.outlook.com",
    email_smtp_port=587,
    email_username="your_email@outlook.com",
    email_password="your_password",
    email_from="your_email@outlook.com"
)
```

## API参考 / API Reference

### NotificationConfig

通知配置数据类 / Notification configuration data class

**属性 / Attributes:**

- `email_enabled` (bool): 是否启用邮件通知 / Whether email notification is enabled
- `email_smtp_server` (str): SMTP服务器地址 / SMTP server address
- `email_smtp_port` (int): SMTP服务器端口 / SMTP server port
- `email_username` (str): 邮箱用户名 / Email username
- `email_password` (str): 邮箱密码或授权码 / Email password or authorization code
- `email_from` (str): 发件人地址 / Sender email address
- `sms_enabled` (bool): 是否启用短信通知 / Whether SMS notification is enabled
- `sms_api_key` (str): 短信API密钥 / SMS API key
- `sms_api_url` (str): 短信API地址 / SMS API URL
- `sms_signature` (str): 短信签名 / SMS signature

### NotificationService

通知服务类 / Notification service class

#### setup(config: NotificationConfig) -> None

配置通知服务 / Configure notification service

**参数 / Parameters:**
- `config`: 通知配置对象 / Notification configuration object

#### send_email(recipients, subject, body, attachments=None, html=False) -> bool

发送邮件通知 / Send email notification

**参数 / Parameters:**
- `recipients` (List[str]): 收件人邮箱列表 / List of recipient email addresses
- `subject` (str): 邮件主题 / Email subject
- `body` (str): 邮件正文 / Email body
- `attachments` (List[str], optional): 附件文件路径列表 / List of attachment file paths
- `html` (bool, optional): 是否为HTML格式 / Whether the body is HTML format

**返回 / Returns:**
- `bool`: 发送成功返回True / True if sent successfully

#### send_sms(phone_numbers, message) -> bool

发送短信通知 / Send SMS notification

**参数 / Parameters:**
- `phone_numbers` (List[str]): 手机号码列表 / List of phone numbers
- `message` (str): 短信内容 / SMS message content

**返回 / Returns:**
- `bool`: 发送成功返回True / True if sent successfully

#### send_system_notification(title, message, level="info") -> None

发送系统通知 / Send system notification

**参数 / Parameters:**
- `title` (str): 通知标题 / Notification title
- `message` (str): 通知消息 / Notification message
- `level` (str): 通知级别 (info/warning/error/critical) / Notification level

#### send_risk_alert(alert, recipients, phone_numbers=None) -> bool

发送风险预警通知 / Send risk alert notification

**参数 / Parameters:**
- `alert` (Dict[str, Any]): 风险预警信息字典 / Risk alert information dictionary
- `recipients` (List[str]): 邮件收件人列表 / Email recipients list
- `phone_numbers` (List[str], optional): 短信收件人列表 / SMS recipients list

**返回 / Returns:**
- `bool`: 至少一种方式发送成功返回True / True if at least one method succeeds

**风险预警字典格式 / Risk Alert Dictionary Format:**

```python
{
    'alert_type': str,           # 预警类型
    'severity': str,             # 严重程度 (info/warning/critical)
    'message': str,              # 预警消息
    'timestamp': str,            # 时间戳
    'current_value': float,      # 当前值
    'threshold_value': float,    # 阈值
    'affected_positions': List[str],  # 受影响持仓
    'recommended_actions': List[str]  # 建议操作
}
```

## 使用场景 / Use Cases

### 1. 每日交易报告 / Daily Trading Report

```python
# 在交易日结束时发送每日报告
service.send_email(
    recipients=["trader@example.com"],
    subject="【量化交易】每日交易报告 - 2024-01-15",
    body=generate_daily_report_html(),
    html=True,
    attachments=["reports/daily_chart.png"]
)
```

### 2. 风险监控 / Risk Monitoring

```python
# 检测到风险时立即发送预警
if max_drawdown < risk_threshold:
    alert = {
        'alert_type': '最大回撤预警',
        'severity': 'critical',
        'message': '投资组合回撤超过阈值',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'current_value': max_drawdown,
        'threshold_value': risk_threshold,
        'affected_positions': get_affected_positions(),
        'recommended_actions': [
            '立即停止交易',
            '检查策略参数',
            '等待市场稳定'
        ]
    }
    
    service.send_risk_alert(
        alert=alert,
        recipients=["trader@example.com", "risk_manager@example.com"],
        phone_numbers=["13800138000"]
    )
```

### 3. 系统状态监控 / System Status Monitoring

```python
# 记录系统关键事件
service.send_system_notification(
    title="系统启动",
    message="量化交易系统已成功启动",
    level="info"
)

service.send_system_notification(
    title="数据更新完成",
    message="市场数据已更新至最新",
    level="info"
)

service.send_system_notification(
    title="模型训练失败",
    message="模型训练过程中发生错误",
    level="error"
)
```

### 4. 定期报告 / Periodic Reports

```python
# 每周报告
if is_friday():
    service.send_email(
        recipients=["trader@example.com"],
        subject="【量化交易】每周交易报告",
        body=generate_weekly_report_html(),
        html=True
    )

# 每月报告
if is_month_end():
    service.send_email(
        recipients=["trader@example.com"],
        subject="【量化交易】每月交易报告",
        body=generate_monthly_report_html(),
        html=True,
        attachments=["reports/monthly_report.pdf"]
    )
```

## 最佳实践 / Best Practices

### 1. 安全性 / Security

- 不要在代码中硬编码密码和API密钥 / Don't hardcode passwords and API keys in code
- 使用环境变量或配置文件存储敏感信息 / Use environment variables or config files for sensitive information
- 定期更换密码和API密钥 / Regularly rotate passwords and API keys
- 使用授权码而不是邮箱密码 / Use authorization codes instead of email passwords

### 2. 错误处理 / Error Handling

```python
# 总是检查发送结果
result = service.send_email(...)
if not result:
    logger.error("邮件发送失败")
    # 采取备用方案
    service.send_system_notification(
        title="邮件发送失败",
        message="无法发送邮件通知，请检查配置",
        level="error"
    )
```

### 3. 避免频繁发送 / Avoid Frequent Sending

```python
# 使用限流机制
from datetime import datetime, timedelta

last_alert_time = {}

def send_alert_with_throttle(alert_type, alert):
    now = datetime.now()
    last_time = last_alert_time.get(alert_type)
    
    # 同类型预警至少间隔5分钟
    if last_time and (now - last_time) < timedelta(minutes=5):
        return False
    
    result = service.send_risk_alert(alert, ...)
    if result:
        last_alert_time[alert_type] = now
    
    return result
```

### 4. 日志记录 / Logging

```python
# 记录所有通知操作
logger.info(f"发送邮件: 收件人={recipients}, 主题={subject}")
result = service.send_email(...)
logger.info(f"邮件发送结果: {result}")
```

## 故障排除 / Troubleshooting

### 邮件发送失败 / Email Sending Failed

**问题 / Problem**: 邮件发送失败，返回False

**可能原因 / Possible Causes**:
1. SMTP服务器地址或端口错误 / Incorrect SMTP server address or port
2. 用户名或密码错误 / Incorrect username or password
3. 未开启SMTP服务 / SMTP service not enabled
4. 网络连接问题 / Network connection issues
5. 邮箱安全设置阻止 / Email security settings blocking

**解决方案 / Solutions**:
1. 检查SMTP配置是否正确 / Check if SMTP configuration is correct
2. 确认使用授权码而不是密码 / Confirm using authorization code instead of password
3. 在邮箱设置中开启SMTP服务 / Enable SMTP service in email settings
4. 检查网络连接和防火墙设置 / Check network connection and firewall settings
5. 查看日志文件获取详细错误信息 / Check log files for detailed error information

### 短信发送失败 / SMS Sending Failed

**问题 / Problem**: 短信发送失败，返回False

**可能原因 / Possible Causes**:
1. API密钥错误 / Incorrect API key
2. API地址错误 / Incorrect API URL
3. 账户余额不足 / Insufficient account balance
4. 手机号码格式错误 / Incorrect phone number format
5. 短信内容违规 / SMS content violates regulations

**解决方案 / Solutions**:
1. 检查API密钥是否正确 / Check if API key is correct
2. 确认API地址是否正确 / Confirm API URL is correct
3. 检查短信服务商账户余额 / Check SMS provider account balance
4. 确保手机号码格式正确 / Ensure phone number format is correct
5. 检查短信内容是否符合规范 / Check if SMS content complies with regulations

### 系统通知不显示 / System Notifications Not Showing

**问题 / Problem**: 系统通知没有记录到日志

**可能原因 / Possible Causes**:
1. 日志级别设置过高 / Log level set too high
2. 日志系统未初始化 / Logging system not initialized
3. 日志文件权限问题 / Log file permission issues

**解决方案 / Solutions**:
1. 检查日志级别配置 / Check log level configuration
2. 确保日志系统已正确初始化 / Ensure logging system is properly initialized
3. 检查日志目录权限 / Check log directory permissions

## 示例代码 / Example Code

完整的示例代码请参考：
For complete example code, please refer to:

- `examples/demo_notification_service.py` - 通知服务完整示例 / Complete notification service demo
- `test_notification_service.py` - 通知服务测试脚本 / Notification service test script

## 相关文档 / Related Documentation

- [日志系统文档](logger_system_implementation.md) - 日志系统详细说明
- [配置管理文档](config_manager_implementation.md) - 配置管理详细说明
- [风险管理文档](risk_manager.md) - 风险管理详细说明

## 更新日志 / Changelog

### v1.0.0 (2024-01-15)
- 初始版本发布 / Initial release
- 支持邮件通知 / Email notification support
- 支持短信通知 / SMS notification support
- 支持系统通知 / System notification support
- 支持风险预警通知 / Risk alert notification support
