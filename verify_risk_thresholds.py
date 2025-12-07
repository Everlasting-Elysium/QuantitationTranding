#!/usr/bin/env python3
"""
风险阈值配置验证脚本 / Risk Thresholds Configuration Verification Script

验证risk_thresholds.yaml配置文件的完整性和正确性
Verify the completeness and correctness of risk_thresholds.yaml configuration file
"""

import os
import sys
import yaml
from pathlib import Path


def verify_risk_thresholds():
    """
    验证风险阈值配置文件
    Verify risk thresholds configuration file
    """
    print("=" * 80)
    print("风险阈值配置验证 / Risk Thresholds Configuration Verification")
    print("=" * 80)
    
    config_path = "config/risk_thresholds.yaml"
    
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
        'risk_profiles', 'alert_levels', 'risk_monitoring',
        'default_risk_profile', 'default_alert_level'
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
    
    # 检查风险偏好配置
    risk_profiles = config.get('risk_profiles', {})
    required_profiles = ['conservative', 'moderate', 'aggressive', 'very_aggressive']
    
    print("检查风险偏好配置 / Checking risk profile configurations:")
    print("-" * 80)
    
    all_profiles_present = True
    for profile_name in required_profiles:
        if profile_name in risk_profiles:
            profile = risk_profiles[profile_name]
            print(f"✅ {profile_name} - {profile.get('name', 'N/A')}")
        else:
            print(f"❌ 缺失风险偏好：{profile_name}")
            print(f"❌ Missing risk profile: {profile_name}")
            all_profiles_present = False
    
    print()
    
    # 检查每个风险偏好的必需字段
    required_profile_fields = [
        'name', 'description', 'position_limits', 'loss_limits',
        'stop_loss', 'volatility_limits', 'drawdown_limits',
        'leverage_limits', 'liquidity_requirements'
    ]
    
    print("检查风险偏好必需字段 / Checking required profile fields:")
    print("-" * 80)
    
    all_fields_present = True
    for profile_name, profile_config in risk_profiles.items():
        print(f"\n{profile_name} - {profile_config.get('name', 'N/A')}:")
        for field in required_profile_fields:
            if field in profile_config:
                print(f"  ✅ {field}")
            else:
                print(f"  ❌ 缺失：{field}")
                print(f"  ❌ Missing: {field}")
                all_fields_present = False
    
    print()
    
    # 检查预警级别
    alert_levels = config.get('alert_levels', {})
    required_alert_levels = ['normal', 'caution', 'warning', 'danger']
    
    print("检查预警级别配置 / Checking alert level configurations:")
    print("-" * 80)
    
    all_alerts_present = True
    for alert_name in required_alert_levels:
        if alert_name in alert_levels:
            alert = alert_levels[alert_name]
            print(f"{alert.get('icon', '?')} {alert_name} - {alert.get('name', 'N/A')}")
        else:
            print(f"❌ 缺失预警级别：{alert_name}")
            print(f"❌ Missing alert level: {alert_name}")
            all_alerts_present = False
    
    print()
    
    # 检查风险偏好的关键阈值
    print("检查关键风险阈值 / Checking key risk thresholds:")
    print("-" * 80)
    
    for profile_name, profile_config in risk_profiles.items():
        print(f"\n{profile_name}:")
        
        # 仓位限制
        position_limits = profile_config.get('position_limits', {})
        print(f"  仓位限制 / Position Limits:")
        print(f"    单只股票: {position_limits.get('max_single_position', 0)*100:.0f}%")
        print(f"    总仓位: {position_limits.get('max_total_position', 0)*100:.0f}%")
        print(f"    现金比例: {position_limits.get('min_cash_ratio', 0)*100:.0f}%")
        
        # 亏损限制
        loss_limits = profile_config.get('loss_limits', {})
        print(f"  亏损限制 / Loss Limits:")
        print(f"    单日: {loss_limits.get('max_daily_loss', 0)*100:.0f}%")
        print(f"    总亏损: {loss_limits.get('max_total_loss', 0)*100:.0f}%")
        
        # 回撤限制
        drawdown_limits = profile_config.get('drawdown_limits', {})
        print(f"  回撤限制 / Drawdown Limits:")
        print(f"    最大回撤: {drawdown_limits.get('max_drawdown', 0)*100:.0f}%")
    
    print()
    
    # 检查风险监控配置
    if 'risk_monitoring' in config:
        print("检查风险监控配置 / Checking risk monitoring configuration:")
        print("-" * 80)
        monitoring = config['risk_monitoring']
        
        if 'monitoring_frequency' in monitoring:
            freq = monitoring['monitoring_frequency']
            print("监控频率 / Monitoring Frequency:")
            print(f"  正常: {freq.get('normal', 0)}秒")
            print(f"  注意: {freq.get('caution', 0)}秒")
            print(f"  警告: {freq.get('warning', 0)}秒")
            print(f"  危险: {freq.get('danger', 0)}秒")
        
        if 'automatic_actions' in monitoring:
            auto_actions = monitoring['automatic_actions']
            print(f"\n自动处理: {'启用' if auto_actions.get('enabled') else '禁用'}")
        
        print()
    
    # 统计信息
    print("配置统计 / Configuration Statistics:")
    print("-" * 80)
    print(f"风险偏好数量 / Number of risk profiles: {len(risk_profiles)}")
    print(f"预警级别数量 / Number of alert levels: {len(alert_levels)}")
    
    # 文件大小
    file_size = os.path.getsize(config_path)
    print(f"文件大小 / File size: {file_size} bytes ({file_size/1024:.2f} KB)")
    
    print()
    print("=" * 80)
    
    # 最终结果
    if all_keys_present and all_profiles_present and all_fields_present and all_alerts_present:
        print("✅ 验证通过！风险阈值配置文件完整且格式正确。")
        print("✅ Verification passed! Risk thresholds configuration file is complete and correctly formatted.")
        return True
    else:
        print("⚠️  验证发现一些问题，请检查上述缺失的内容。")
        print("⚠️  Verification found some issues, please check the missing content above.")
        return False


def print_risk_comparison():
    """
    打印风险偏好对比
    Print risk profile comparison
    """
    config_path = "config/risk_thresholds.yaml"
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    print("\n" + "=" * 80)
    print("风险偏好对比 / Risk Profile Comparison")
    print("=" * 80 + "\n")
    
    risk_profiles = config.get('risk_profiles', {})
    
    # 创建对比表
    print(f"{'指标 / Metric':<30} {'保守型':<12} {'稳健型':<12} {'积极型':<12} {'激进型':<12}")
    print("-" * 80)
    
    # 单只股票最大仓位
    print(f"{'单只股票最大仓位':<30}", end="")
    for profile_name in ['conservative', 'moderate', 'aggressive', 'very_aggressive']:
        if profile_name in risk_profiles:
            value = risk_profiles[profile_name]['position_limits']['max_single_position']
            print(f"{value*100:>10.0f}%  ", end="")
    print()
    
    # 最大总仓位
    print(f"{'最大总仓位':<30}", end="")
    for profile_name in ['conservative', 'moderate', 'aggressive', 'very_aggressive']:
        if profile_name in risk_profiles:
            value = risk_profiles[profile_name]['position_limits']['max_total_position']
            print(f"{value*100:>10.0f}%  ", end="")
    print()
    
    # 最大单日亏损
    print(f"{'最大单日亏损':<30}", end="")
    for profile_name in ['conservative', 'moderate', 'aggressive', 'very_aggressive']:
        if profile_name in risk_profiles:
            value = risk_profiles[profile_name]['loss_limits']['max_daily_loss']
            print(f"{value*100:>10.0f}%  ", end="")
    print()
    
    # 最大总亏损
    print(f"{'最大总亏损':<30}", end="")
    for profile_name in ['conservative', 'moderate', 'aggressive', 'very_aggressive']:
        if profile_name in risk_profiles:
            value = risk_profiles[profile_name]['loss_limits']['max_total_loss']
            print(f"{value*100:>10.0f}%  ", end="")
    print()
    
    # 最大回撤
    print(f"{'最大回撤':<30}", end="")
    for profile_name in ['conservative', 'moderate', 'aggressive', 'very_aggressive']:
        if profile_name in risk_profiles:
            value = risk_profiles[profile_name]['drawdown_limits']['max_drawdown']
            print(f"{value*100:>10.0f}%  ", end="")
    print()
    
    # 最大杠杆
    print(f"{'最大杠杆':<30}", end="")
    for profile_name in ['conservative', 'moderate', 'aggressive', 'very_aggressive']:
        if profile_name in risk_profiles:
            value = risk_profiles[profile_name]['leverage_limits']['max_leverage']
            print(f"{value:>10.1f}x  ", end="")
    print()
    
    print()


def print_alert_levels():
    """
    打印预警级别说明
    Print alert levels description
    """
    config_path = "config/risk_thresholds.yaml"
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    print("\n" + "=" * 80)
    print("预警级别说明 / Alert Levels Description")
    print("=" * 80 + "\n")
    
    alert_levels = config.get('alert_levels', {})
    
    for alert_name in ['normal', 'caution', 'warning', 'danger']:
        if alert_name in alert_levels:
            alert = alert_levels[alert_name]
            print(f"{alert.get('icon', '?')} {alert.get('name', 'N/A')} / {alert.get('name_en', 'N/A')}")
            print("-" * 80)
            print(f"级别 / Level: {alert.get('level', 'N/A')}")
            print(f"描述 / Description: {alert.get('description', 'N/A')}")
            
            if 'actions' in alert:
                print(f"处理动作 / Actions:")
                for action in alert['actions']:
                    print(f"  • {action}")
            
            print()


if __name__ == "__main__":
    success = verify_risk_thresholds()
    
    if success:
        print_risk_comparison()
        print_alert_levels()
    
    sys.exit(0 if success else 1)
