#!/usr/bin/env python3
"""
通知配置验证脚本 / Notification Configuration Verification Script

验证notification_config.yaml配置文件的完整性和正确性
Verify the completeness and correctness of notification_config.yaml configuration file
"""

import os
import sys
import yaml
from pathlib import Path


def verify_notification_config():
    """
    验证通知配置文件
    Verify notification configuration file
    """
    print("=" * 80)
    print("通知配置验证 / Notification Configuration Verification")
    print("=" * 80)
    
    config_path = "config/notification_config.yaml"
    
    # 检查文件是否存在
    if not os.path.exists(config_path):
        print(f"❌ 错误：找不到文件 {config_path}")
        print(f"❌ Error: File {config_path} not found")
        return False
    
    print(f"✅ 文件存在：{config_path}")
    print(f"✅ File exists: {config_path}")
    print()
    
    # 读取YAML文件
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ YAML解析错误：{e}")
        print(f"❌ YAML parsing error: {e}")
        return False
    
    print("✅ YAML格式正确")
    print("✅ YAML format correct")
    print()
    
    # 必需的顶层键
    required_top_keys = [
        'email', 'sms', 'system', 'recipients',
        'triggers', 'templates', 'defaults'
    ]
    
    print("检查必需的顶层键 / Checking required top-level keys:")
    print("-" * 80)
    
    all_keys_present = True
    for key in required_top_keys:
        if key in config:
            print(f"✅ {key}")
        else:
            print(f"❌ 缺失：{key}")
            print(f"❌ Missing: {key}")
            all_keys_present = False
    
    print()
    
    # 检查邮件配置
    if 'email' in config:
        print("检查邮件配置 / Checking email configuration:")
        print("-" * 80)
        email_config = config['email']
        
        required_email_keys = ['enabled', 'smtp', 'auth', 'sender']
        for key in required_email_keys:
            if key in email_config:
                print(f"✅ email.{key}")
            else:
                print(f"❌ 缺失：email.{key}")
        
        # 检查SMTP配置
        if 'smtp' in email_config:
            smtp = email_config['smtp']
            print(f"  SMTP服务器: {smtp.get('server', 'N/A')}")
            print(f"  端口: {smtp.get('port', 'N/A')}")
            print(f"  TLS: {'启用' if smtp.get('use_tls') else '禁用'}")
        
        print()
    
    # 检查短信配置
    if 'sms' in config:
        print("检查短信配置 / Checking SMS configuration:")
        print("-" * 80)
        sms_config = config['sms']
        
        print(f"启用状态: {'启用' if sms_config.get('enabled') else '禁用'}")
        if 'provider' in sms_config:
            provider = sms_config['provider']
            print(f"服务商: {provider.get('name', 'N/A')}")
        
        if 'templates' in sms_config:
            templates = sms_config['templates']
            print(f"短信模板数量: {len(templates)}")
        
        print()
    
    # 检查系统通知配置
    if 'system' in config:
        print("检查系统通知配置 / Checking system notification configuration:")
        print("-" * 80)
        system_config = config['system']
        
        print(f"启用状态: {'启用' if system_config.get('enabled') else '禁用'}")
        
        if 'methods' in system_config:
            methods = system_config['methods']
            print("通知方式:")
            for method, method_config in methods.items():
                status = "✅" if method_config.get('enabled') else "❌"
                print(f"  {status} {method}")
        
        print()
    
    # 检查接收人配置
    if 'recipients' in config:
        print("检查接收人配置 / Checking recipients configuration:")
        print("-" * 80)
        recipients = config['recipients']
        
        if 'groups' in recipients:
            groups = recipients['groups']
            print(f"接收人组数量: {len(groups)}")
            for group_name, group_config in groups.items():
                print(f"  • {group_name} - {group_config.get('name', 'N/A')}")
                if 'emails' in group_config:
                    print(f"    邮箱数量: {len(group_config['emails'])}")
                if 'phone_numbers' in group_config:
                    print(f"    电话数量: {len(group_config['phone_numbers'])}")
        
        print()
    
    # 检查触发条件
    if 'triggers' in config:
        print("检查触发条件配置 / Checking trigger configuration:")
        print("-" * 80)
        triggers = config['triggers']
        
        trigger_categories = ['scheduled_reports', 'risk_alerts', 'trading', 'system']
        for category in trigger_categories:
            if category in triggers:
                category_triggers = triggers[category]
                print(f"{category}: {len(category_triggers)} 个触发器")
        
        print()
    
    # 检查模板配置
    if 'templates' in config:
        print("检查模板配置 / Checking template configuration:")
        print("-" * 80)
        templates = config['templates']
        
        if 'subjects' in templates:
            subjects = templates['subjects']
            print(f"邮件主题模板数量: {len(subjects)}")
        
        if 'email_body' in templates:
            email_body = templates['email_body']
            print(f"邮件内容模板数量: {len(email_body)}")
        
        if 'sms_body' in templates:
            sms_body = templates['sms_body']
            print(f"短信内容模板数量: {len(sms_body)}")
        
        print()
    
    # 统计信息
    print("配置统计 / Configuration Statistics:")
    print("-" * 80)
    
    # 统计接收人组
    if 'recipients' in config and 'groups' in config['recipients']:
        print(f"接收人组数量: {len(config['recipients']['groups'])}")
    
    # 统计触发器
    if 'triggers' in config:
        total_triggers = 0
        for category in config['triggers'].values():
            if isinstance(category, dict):
                total_triggers += len(category)
        print(f"触发器总数: {total_triggers}")
    
    # 统计模板
    if 'templates' in config:
        total_templates = 0
        for template_type in config['templates'].values():
            if isinstance(template_type, dict):
                total_templates += len(template_type)
        print(f"模板总数: {total_templates}")
    
    # 文件大小
    file_size = os.path.getsize(config_path)
    print(f"文件大小: {file_size} bytes ({file_size/1024:.2f} KB)")
    
    print()
    print("=" * 80)
    
    # 最终结果
    if all_keys_present:
        print("✅ 验证通过！通知配置文件完整且格式正确。")
        print("✅ Verification passed! Notification configuration file is complete and correctly formatted.")
        return True
    else:
        print("⚠️  验证发现一些问题，请检查上述缺失的内容。")
        print("⚠️  Verification found some issues, please check the missing content above.")
        return False


def print_notification_summary():
    """
    打印通知配置摘要
    Print notification configuration summary
    """
    config_path = "config/notification_config.yaml"
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    print("\n" + "=" * 80)
    print("通知配置摘要 / Notification Configuration Summary")
    print("=" * 80 + "\n")
    
    # 邮件配置摘要
    if 'email' in config:
        email = config['email']
        print("【邮件通知 / Email Notification】")
        print("-" * 80)
        print(f"状态: {'✅ 启用' if email.get('enabled') else '❌ 禁用'}")
        if 'smtp' in email:
            smtp = email['smtp']
            print(f"SMTP服务器: {smtp.get('server', 'N/A')}:{smtp.get('port', 'N/A')}")
        if 'sender' in email:
            sender = email['sender']
            print(f"发件人: {sender.get('name', 'N/A')} <{sender.get('email', 'N/A')}>")
        if 'rate_limit' in email:
            rate = email['rate_limit']
            print(f"速率限制: {rate.get('max_per_hour', 'N/A')}/小时, {rate.get('max_per_day', 'N/A')}/天")
        print()
    
    # 短信配置摘要
    if 'sms' in config:
        sms = config['sms']
        print("【短信通知 / SMS Notification】")
        print("-" * 80)
        print(f"状态: {'✅ 启用' if sms.get('enabled') else '❌ 禁用'}")
        if 'provider' in sms:
            provider = sms['provider']
            print(f"服务商: {provider.get('name', 'N/A')}")
        print(f"签名: {sms.get('signature', 'N/A')}")
        if 'rate_limit' in sms:
            rate = sms['rate_limit']
            print(f"速率限制: {rate.get('max_per_hour', 'N/A')}/小时, {rate.get('max_per_day', 'N/A')}/天")
        print()
    
    # 系统通知摘要
    if 'system' in config:
        system = config['system']
        print("【系统通知 / System Notification】")
        print("-" * 80)
        print(f"状态: {'✅ 启用' if system.get('enabled') else '❌ 禁用'}")
        if 'methods' in system:
            methods = system['methods']
            print("通知方式:")
            for method, method_config in methods.items():
                status = "✅" if method_config.get('enabled') else "❌"
                print(f"  {status} {method}")
        print()
    
    # 接收人组摘要
    if 'recipients' in config and 'groups' in config['recipients']:
        print("【接收人组 / Recipient Groups】")
        print("-" * 80)
        groups = config['recipients']['groups']
        for group_name, group_config in groups.items():
            print(f"{group_name} - {group_config.get('name', 'N/A')}")
            print(f"  通知类型: {', '.join(group_config.get('notification_types', []))}")
        print()


if __name__ == "__main__":
    success = verify_notification_config()
    
    if success:
        print_notification_summary()
    
    sys.exit(0 if success else 1)
