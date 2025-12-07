"""
通知服务模块 / Notification Service Module
提供邮件、短信和系统通知功能 / Provides email, SMS, and system notification functionality
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import json
import requests


@dataclass
class NotificationConfig:
    """
    通知配置数据类 / Notification Configuration Data Class
    
    Attributes:
        email_enabled: 是否启用邮件通知 / Whether email notification is enabled
        email_smtp_server: SMTP服务器地址 / SMTP server address
        email_smtp_port: SMTP服务器端口 / SMTP server port
        email_username: 邮箱用户名 / Email username
        email_password: 邮箱密码或授权码 / Email password or authorization code
        email_from: 发件人地址 / Sender email address
        sms_enabled: 是否启用短信通知 / Whether SMS notification is enabled
        sms_api_key: 短信API密钥 / SMS API key
        sms_api_url: 短信API地址 / SMS API URL
        sms_signature: 短信签名 / SMS signature
    """
    email_enabled: bool = False
    email_smtp_server: str = ""
    email_smtp_port: int = 587
    email_username: str = ""
    email_password: str = ""
    email_from: str = ""
    sms_enabled: bool = False
    sms_api_key: str = ""
    sms_api_url: str = ""
    sms_signature: str = ""


class NotificationService:
    """
    通知服务类 / Notification Service Class
    
    职责 / Responsibilities:
    - 发送邮件通知 / Send email notifications
    - 发送短信通知 / Send SMS notifications
    - 发送系统通知 / Send system notifications
    - 发送风险预警通知 / Send risk alert notifications
    
    使用单例模式确保全局只有一个实例 / Uses singleton pattern to ensure only one global instance
    """
    
    _instance: Optional['NotificationService'] = None
    
    def __new__(cls):
        """单例模式实现 / Singleton pattern implementation"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化通知服务 / Initialize notification service"""
        # 避免重复初始化
        if hasattr(self, '_initialized'):
            return
            
        self.config: Optional[NotificationConfig] = None
        self.logger = logging.getLogger(__name__)
        self._initialized = False
    
    def setup(self, config: NotificationConfig) -> None:
        """
        配置通知服务 / Configure notification service
        
        Args:
            config: 通知配置对象 / Notification configuration object
        """
        self.config = config
        self._initialized = True
        self.logger.info("通知服务初始化完成 / Notification service initialized")
        
        if config.email_enabled:
            self.logger.info(f"邮件通知已启用 - SMTP服务器: {config.email_smtp_server}")
        else:
            self.logger.info("邮件通知未启用")
            
        if config.sms_enabled:
            self.logger.info(f"短信通知已启用 - API地址: {config.sms_api_url}")
        else:
            self.logger.info("短信通知未启用")
    
    def send_email(
        self,
        recipients: List[str],
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None,
        html: bool = False
    ) -> bool:
        """
        发送邮件通知 / Send email notification
        
        Args:
            recipients: 收件人邮箱列表 / List of recipient email addresses
            subject: 邮件主题 / Email subject
            body: 邮件正文 / Email body
            attachments: 附件文件路径列表 / List of attachment file paths
            html: 是否为HTML格式 / Whether the body is HTML format
            
        Returns:
            bool: 发送成功返回True，失败返回False / True if sent successfully, False otherwise
        """
        if not self._initialized:
            self.logger.error("通知服务未初始化 / Notification service not initialized")
            return False
        
        if not self.config.email_enabled:
            self.logger.warning("邮件通知未启用，跳过发送 / Email notification not enabled, skipping")
            return False
        
        if not recipients:
            self.logger.error("收件人列表为空 / Recipients list is empty")
            return False
        
        try:
            # 创建邮件对象 / Create email message
            msg = MIMEMultipart()
            msg['From'] = self.config.email_from or self.config.email_username
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            
            # 添加邮件正文 / Add email body
            body_type = 'html' if html else 'plain'
            msg.attach(MIMEText(body, body_type, 'utf-8'))
            
            # 添加附件 / Add attachments
            if attachments:
                for file_path in attachments:
                    self._attach_file(msg, file_path)
            
            # 连接SMTP服务器并发送 / Connect to SMTP server and send
            with smtplib.SMTP(self.config.email_smtp_server, self.config.email_smtp_port) as server:
                server.starttls()  # 启用TLS加密 / Enable TLS encryption
                server.login(self.config.email_username, self.config.email_password)
                server.send_message(msg)
            
            self.logger.info(f"邮件发送成功 - 收件人: {recipients}, 主题: {subject}")
            return True
            
        except Exception as e:
            self.logger.error(f"邮件发送失败 / Email sending failed: {e}", exc_info=True)
            return False
    
    def _attach_file(self, msg: MIMEMultipart, file_path: str) -> None:
        """
        添加附件到邮件 / Attach file to email
        
        Args:
            msg: 邮件对象 / Email message object
            file_path: 附件文件路径 / Attachment file path
        """
        try:
            path = Path(file_path)
            if not path.exists():
                self.logger.warning(f"附件文件不存在: {file_path}")
                return
            
            with open(path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {path.name}'
            )
            msg.attach(part)
            
        except Exception as e:
            self.logger.error(f"添加附件失败 / Failed to attach file {file_path}: {e}")
    
    def send_sms(
        self,
        phone_numbers: List[str],
        message: str
    ) -> bool:
        """
        发送短信通知 / Send SMS notification
        
        Args:
            phone_numbers: 手机号码列表 / List of phone numbers
            message: 短信内容 / SMS message content
            
        Returns:
            bool: 发送成功返回True，失败返回False / True if sent successfully, False otherwise
        """
        if not self._initialized:
            self.logger.error("通知服务未初始化 / Notification service not initialized")
            return False
        
        if not self.config.sms_enabled:
            self.logger.warning("短信通知未启用，跳过发送 / SMS notification not enabled, skipping")
            return False
        
        if not phone_numbers:
            self.logger.error("手机号码列表为空 / Phone numbers list is empty")
            return False
        
        try:
            # 构建短信内容（添加签名）/ Build SMS content (add signature)
            full_message = f"【{self.config.sms_signature}】{message}" if self.config.sms_signature else message
            
            # 调用短信API / Call SMS API
            # 注意：这里使用通用的API调用方式，实际使用时需要根据具体的短信服务商API进行调整
            # Note: This uses a generic API call method, adjust according to actual SMS provider API
            payload = {
                'api_key': self.config.sms_api_key,
                'phone_numbers': phone_numbers,
                'message': full_message
            }
            
            response = requests.post(
                self.config.sms_api_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success', False):
                    self.logger.info(f"短信发送成功 - 收件人: {phone_numbers}")
                    return True
                else:
                    self.logger.error(f"短信发送失败 - API返回错误: {result.get('message', 'Unknown error')}")
                    return False
            else:
                self.logger.error(f"短信发送失败 - HTTP状态码: {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            self.logger.error("短信发送超时 / SMS sending timeout")
            return False
        except Exception as e:
            self.logger.error(f"短信发送失败 / SMS sending failed: {e}", exc_info=True)
            return False
    
    def send_system_notification(
        self,
        title: str,
        message: str,
        level: str = "info"
    ) -> None:
        """
        发送系统通知 / Send system notification
        
        这个方法主要用于在系统日志中记录通知信息
        This method is mainly used to log notification information in system logs
        
        Args:
            title: 通知标题 / Notification title
            message: 通知消息 / Notification message
            level: 通知级别 (info/warning/error/critical) / Notification level
        """
        level = level.lower()
        log_message = f"[系统通知 / System Notification] {title}: {message}"
        
        if level == "critical":
            self.logger.critical(log_message)
        elif level == "error":
            self.logger.error(log_message)
        elif level == "warning":
            self.logger.warning(log_message)
        else:
            self.logger.info(log_message)
    
    def send_risk_alert(
        self,
        alert: Dict[str, Any],
        recipients: List[str],
        phone_numbers: Optional[List[str]] = None
    ) -> bool:
        """
        发送风险预警通知 / Send risk alert notification
        
        同时通过邮件和短信发送风险预警
        Send risk alerts via both email and SMS
        
        Args:
            alert: 风险预警信息字典 / Risk alert information dictionary
            recipients: 邮件收件人列表 / Email recipients list
            phone_numbers: 短信收件人列表 / SMS recipients list
            
        Returns:
            bool: 至少一种方式发送成功返回True / True if at least one method succeeds
        """
        if not self._initialized:
            self.logger.error("通知服务未初始化 / Notification service not initialized")
            return False
        
        # 提取预警信息 / Extract alert information
        alert_type = alert.get('alert_type', '未知')
        severity = alert.get('severity', 'warning')
        message = alert.get('message', '')
        current_value = alert.get('current_value', 0)
        threshold_value = alert.get('threshold_value', 0)
        recommended_actions = alert.get('recommended_actions', [])
        
        # 构建邮件内容 / Build email content
        email_subject = f"【风险预警】{alert_type} - {severity.upper()}"
        email_body = self._build_risk_alert_email(alert)
        
        # 构建短信内容 / Build SMS content
        sms_message = f"风险预警：{message}。当前值：{current_value}，阈值：{threshold_value}。请及时处理。"
        
        # 发送邮件 / Send email
        email_sent = False
        if recipients and self.config.email_enabled:
            email_sent = self.send_email(
                recipients=recipients,
                subject=email_subject,
                body=email_body,
                html=True
            )
        
        # 发送短信 / Send SMS
        sms_sent = False
        if phone_numbers and self.config.sms_enabled:
            sms_sent = self.send_sms(
                phone_numbers=phone_numbers,
                message=sms_message
            )
        
        # 记录系统通知 / Log system notification
        self.send_system_notification(
            title=f"风险预警 - {alert_type}",
            message=message,
            level=severity
        )
        
        success = email_sent or sms_sent
        if success:
            self.logger.info(f"风险预警通知已发送 - 类型: {alert_type}, 严重程度: {severity}")
        else:
            self.logger.warning(f"风险预警通知发送失败 - 类型: {alert_type}")
        
        return success
    
    def _build_risk_alert_email(self, alert: Dict[str, Any]) -> str:
        """
        构建风险预警邮件HTML内容 / Build risk alert email HTML content
        
        Args:
            alert: 风险预警信息 / Risk alert information
            
        Returns:
            str: HTML格式的邮件内容 / HTML formatted email content
        """
        alert_type = alert.get('alert_type', '未知')
        severity = alert.get('severity', 'warning')
        message = alert.get('message', '')
        timestamp = alert.get('timestamp', '')
        current_value = alert.get('current_value', 0)
        threshold_value = alert.get('threshold_value', 0)
        affected_positions = alert.get('affected_positions', [])
        recommended_actions = alert.get('recommended_actions', [])
        
        # 根据严重程度选择颜色 / Choose color based on severity
        severity_colors = {
            'info': '#17a2b8',
            'warning': '#ffc107',
            'critical': '#dc3545'
        }
        color = severity_colors.get(severity, '#6c757d')
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: {color}; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
                .content {{ background-color: #f8f9fa; padding: 20px; border: 1px solid #dee2e6; }}
                .section {{ margin-bottom: 20px; }}
                .label {{ font-weight: bold; color: #495057; }}
                .value {{ color: #212529; }}
                .actions {{ background-color: #e9ecef; padding: 15px; border-radius: 5px; margin-top: 15px; }}
                .action-item {{ margin: 5px 0; padding-left: 20px; }}
                .footer {{ text-align: center; padding: 15px; color: #6c757d; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>🚨 风险预警通知</h2>
                    <p>{alert_type} - {severity.upper()}</p>
                </div>
                <div class="content">
                    <div class="section">
                        <p class="label">预警时间：</p>
                        <p class="value">{timestamp}</p>
                    </div>
                    <div class="section">
                        <p class="label">预警信息：</p>
                        <p class="value">{message}</p>
                    </div>
                    <div class="section">
                        <p class="label">当前值：</p>
                        <p class="value">{current_value}</p>
                    </div>
                    <div class="section">
                        <p class="label">阈值：</p>
                        <p class="value">{threshold_value}</p>
                    </div>
        """
        
        if affected_positions:
            html += """
                    <div class="section">
                        <p class="label">受影响持仓：</p>
                        <ul>
            """
            for position in affected_positions:
                html += f"<li>{position}</li>"
            html += """
                        </ul>
                    </div>
            """
        
        if recommended_actions:
            html += """
                    <div class="actions">
                        <p class="label">建议操作：</p>
            """
            for action in recommended_actions:
                html += f'<div class="action-item">• {action}</div>'
            html += """
                    </div>
            """
        
        html += """
                </div>
                <div class="footer">
                    <p>此邮件由量化交易系统自动发送，请勿直接回复</p>
                    <p>This email is automatically sent by the quantitative trading system, please do not reply directly</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def is_initialized(self) -> bool:
        """
        检查通知服务是否已初始化 / Check if notification service is initialized
        
        Returns:
            bool: 已初始化返回True / True if initialized
        """
        return self._initialized
    
    def get_config(self) -> Optional[NotificationConfig]:
        """
        获取当前配置 / Get current configuration
        
        Returns:
            NotificationConfig: 配置对象，未初始化返回None / Configuration object, None if not initialized
        """
        return self.config


# 全局通知服务实例 / Global notification service instance
_notification_service = NotificationService()


def get_notification_service() -> NotificationService:
    """
    获取全局通知服务实例 / Get global notification service instance
    
    Returns:
        NotificationService: 通知服务实例 / Notification service instance
    """
    return _notification_service


def setup_notification(config: NotificationConfig) -> None:
    """
    便捷函数：配置通知服务 / Convenience function: Configure notification service
    
    Args:
        config: 通知配置对象 / Notification configuration object
    """
    _notification_service.setup(config)
