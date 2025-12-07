"""
报告调度器模块 / Report Scheduler Module
负责定期生成和发送交易报告 / Responsible for periodically generating and sending trading reports
"""

import logging
import schedule
import time
import threading
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Callable
from dataclasses import dataclass
from pathlib import Path
import pandas as pd


@dataclass
class ScheduleConfig:
    """
    调度配置数据类 / Schedule Configuration Data Class
    
    Attributes:
        daily_enabled: 是否启用每日报告 / Whether daily report is enabled
        daily_time: 每日报告生成时间 / Daily report generation time (HH:MM format)
        weekly_enabled: 是否启用每周报告 / Whether weekly report is enabled
        weekly_day: 每周报告生成日期 / Weekly report generation day (Monday=0, Sunday=6)
        weekly_time: 每周报告生成时间 / Weekly report generation time
        monthly_enabled: 是否启用每月报告 / Whether monthly report is enabled
        monthly_day: 每月报告生成日期 / Monthly report generation day (1-31)
        monthly_time: 每月报告生成时间 / Monthly report generation time
        risk_alert_enabled: 是否启用风险预警 / Whether risk alert is enabled
        risk_check_interval: 风险检查间隔（分钟）/ Risk check interval (minutes)
    """
    daily_enabled: bool = True
    daily_time: str = "18:00"
    weekly_enabled: bool = True
    weekly_day: int = 4  # Friday
    weekly_time: str = "18:00"
    monthly_enabled: bool = True
    monthly_day: int = 1
    monthly_time: str = "18:00"
    risk_alert_enabled: bool = True
    risk_check_interval: int = 60  # 每小时检查一次


class ReportScheduler:
    """
    报告调度器类 / Report Scheduler Class
    
    职责 / Responsibilities:
    - 定期生成每日报告 / Periodically generate daily reports
    - 定期生成每周报告 / Periodically generate weekly reports
    - 定期生成每月报告 / Periodically generate monthly reports
    - 实时监控风险并生成预警报告 / Monitor risks in real-time and generate alert reports
    - 集成通知服务发送报告 / Integrate notification service to send reports
    """
    
    def __init__(self):
        """初始化报告调度器 / Initialize report scheduler"""
        self.logger = logging.getLogger(__name__)
        self.config: Optional[ScheduleConfig] = None
        self.report_generator = None
        self.notification_service = None
        self.risk_manager = None
        self.portfolio_manager = None
        self.simulation_engine = None
        self.live_trading_manager = None
        
        self._running = False
        self._scheduler_thread: Optional[threading.Thread] = None
        self._last_daily_report = None
        self._last_weekly_report = None
        self._last_monthly_report = None
        
        self.logger.info("报告调度器初始化完成 / Report scheduler initialized")
    
    def setup(
        self,
        config: ScheduleConfig,
        report_generator,
        notification_service,
        risk_manager=None,
        portfolio_manager=None,
        simulation_engine=None,
        live_trading_manager=None
    ) -> None:
        """
        配置报告调度器 / Configure report scheduler
        
        Args:
            config: 调度配置 / Schedule configuration
            report_generator: 报告生成器实例 / Report generator instance
            notification_service: 通知服务实例 / Notification service instance
            risk_manager: 风险管理器实例（可选）/ Risk manager instance (optional)
            portfolio_manager: 投资组合管理器实例（可选）/ Portfolio manager instance (optional)
            simulation_engine: 模拟引擎实例（可选）/ Simulation engine instance (optional)
            live_trading_manager: 实盘交易管理器实例（可选）/ Live trading manager instance (optional)
        """
        self.config = config
        self.report_generator = report_generator
        self.notification_service = notification_service
        self.risk_manager = risk_manager
        self.portfolio_manager = portfolio_manager
        self.simulation_engine = simulation_engine
        self.live_trading_manager = live_trading_manager
        
        self.logger.info("报告调度器配置完成 / Report scheduler configured")
        self.logger.info(f"  - 每日报告: {'已启用' if config.daily_enabled else '未启用'} @ {config.daily_time}")
        self.logger.info(f"  - 每周报告: {'已启用' if config.weekly_enabled else '未启用'} @ {['周一','周二','周三','周四','周五','周六','周日'][config.weekly_day]} {config.weekly_time}")
        self.logger.info(f"  - 每月报告: {'已启用' if config.monthly_enabled else '未启用'} @ 每月{config.monthly_day}日 {config.monthly_time}")
        self.logger.info(f"  - 风险预警: {'已启用' if config.risk_alert_enabled else '未启用'} (每{config.risk_check_interval}分钟)")
    
    def start(self) -> None:
        """
        启动调度器 / Start scheduler
        
        启动后台线程，开始定期执行任务
        Starts background thread to periodically execute tasks
        """
        if self._running:
            self.logger.warning("调度器已在运行中 / Scheduler is already running")
            return
        
        if not self.config:
            raise ValueError("调度器未配置，请先调用setup()方法 / Scheduler not configured, please call setup() first")
        
        # 清空之前的调度任务
        schedule.clear()
        
        # 配置每日报告
        if self.config.daily_enabled:
            schedule.every().day.at(self.config.daily_time).do(self._generate_daily_report)
            self.logger.info(f"已安排每日报告任务 @ {self.config.daily_time}")
        
        # 配置每周报告
        if self.config.weekly_enabled:
            day_names = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            day_name = day_names[self.config.weekly_day]
            getattr(schedule.every(), day_name).at(self.config.weekly_time).do(self._generate_weekly_report)
            self.logger.info(f"已安排每周报告任务 @ {day_name} {self.config.weekly_time}")
        
        # 配置每月报告（简化实现：每天检查是否是目标日期）
        if self.config.monthly_enabled:
            schedule.every().day.at(self.config.monthly_time).do(self._check_and_generate_monthly_report)
            self.logger.info(f"已安排每月报告任务 @ 每月{self.config.monthly_day}日 {self.config.monthly_time}")
        
        # 配置风险检查
        if self.config.risk_alert_enabled:
            schedule.every(self.config.risk_check_interval).minutes.do(self._check_risk_alerts)
            self.logger.info(f"已安排风险检查任务 (每{self.config.risk_check_interval}分钟)")
        
        # 启动后台线程
        self._running = True
        self._scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self._scheduler_thread.start()
        
        self.logger.info("报告调度器已启动 / Report scheduler started")
    
    def stop(self) -> None:
        """
        停止调度器 / Stop scheduler
        
        停止后台线程，清空所有调度任务
        Stops background thread and clears all scheduled tasks
        """
        if not self._running:
            self.logger.warning("调度器未在运行 / Scheduler is not running")
            return
        
        self._running = False
        schedule.clear()
        
        if self._scheduler_thread:
            self._scheduler_thread.join(timeout=5)
        
        self.logger.info("报告调度器已停止 / Report scheduler stopped")
    
    def _run_scheduler(self) -> None:
        """
        调度器主循环 / Scheduler main loop
        
        在后台线程中运行，定期检查并执行任务
        Runs in background thread, periodically checks and executes tasks
        """
        self.logger.info("调度器主循环已启动 / Scheduler main loop started")
        
        while self._running:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"调度器执行出错 / Scheduler execution error: {e}", exc_info=True)
                time.sleep(60)  # 出错后等待1分钟再继续
        
        self.logger.info("调度器主循环已退出 / Scheduler main loop exited")
    
    def _generate_daily_report(self) -> None:
        """
        生成每日报告 / Generate daily report
        
        生成当日交易报告并发送通知
        Generates daily trading report and sends notification
        """
        try:
            self.logger.info("开始生成每日报告 / Starting daily report generation")
            
            # 获取当前日期
            today = datetime.now().strftime('%Y-%m-%d')
            
            # 检查是否已生成今日报告
            if self._last_daily_report == today:
                self.logger.info(f"今日报告已生成，跳过 / Daily report already generated for {today}")
                return
            
            # 生成报告内容
            report_data = self._collect_daily_data()
            
            if not report_data:
                self.logger.warning("无法收集每日数据，跳过报告生成 / Cannot collect daily data, skipping report")
                return
            
            # 使用报告生成器生成报告
            report_content = self._format_daily_report(report_data)
            
            # 保存报告
            report_path = self._save_report(report_content, 'daily', today)
            
            # 发送通知
            self._send_report_notification(
                report_type='daily',
                report_date=today,
                report_content=report_content,
                report_path=report_path
            )
            
            self._last_daily_report = today
            self.logger.info(f"每日报告生成完成 / Daily report generated: {report_path}")
            
        except Exception as e:
            self.logger.error(f"生成每日报告失败 / Failed to generate daily report: {e}", exc_info=True)
    
    def _generate_weekly_report(self) -> None:
        """
        生成每周报告 / Generate weekly report
        
        生成本周交易报告并发送通知
        Generates weekly trading report and sends notification
        """
        try:
            self.logger.info("开始生成每周报告 / Starting weekly report generation")
            
            # 获取本周日期范围
            today = datetime.now()
            week_start = (today - timedelta(days=today.weekday())).strftime('%Y-%m-%d')
            week_end = today.strftime('%Y-%m-%d')
            week_label = f"{week_start}_to_{week_end}"
            
            # 检查是否已生成本周报告
            if self._last_weekly_report == week_label:
                self.logger.info(f"本周报告已生成，跳过 / Weekly report already generated for {week_label}")
                return
            
            # 生成报告内容
            report_data = self._collect_weekly_data(week_start, week_end)
            
            if not report_data:
                self.logger.warning("无法收集每周数据，跳过报告生成 / Cannot collect weekly data, skipping report")
                return
            
            # 使用报告生成器生成报告
            report_content = self._format_weekly_report(report_data, week_start, week_end)
            
            # 保存报告
            report_path = self._save_report(report_content, 'weekly', week_label)
            
            # 发送通知
            self._send_report_notification(
                report_type='weekly',
                report_date=week_label,
                report_content=report_content,
                report_path=report_path
            )
            
            self._last_weekly_report = week_label
            self.logger.info(f"每周报告生成完成 / Weekly report generated: {report_path}")
            
        except Exception as e:
            self.logger.error(f"生成每周报告失败 / Failed to generate weekly report: {e}", exc_info=True)
    
    def _check_and_generate_monthly_report(self) -> None:
        """
        检查并生成每月报告 / Check and generate monthly report
        
        检查今天是否是目标日期，如果是则生成月报
        Checks if today is the target date, generates monthly report if yes
        """
        today = datetime.now()
        
        # 检查是否是目标日期
        if today.day != self.config.monthly_day:
            return
        
        try:
            self.logger.info("开始生成每月报告 / Starting monthly report generation")
            
            # 获取上月日期范围
            if today.month == 1:
                last_month = 12
                last_year = today.year - 1
            else:
                last_month = today.month - 1
                last_year = today.year
            
            month_start = f"{last_year}-{last_month:02d}-01"
            # 获取上月最后一天
            if last_month == 12:
                next_month_first = f"{last_year + 1}-01-01"
            else:
                next_month_first = f"{last_year}-{last_month + 1:02d}-01"
            month_end = (datetime.strptime(next_month_first, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
            
            month_label = f"{last_year}-{last_month:02d}"
            
            # 检查是否已生成本月报告
            if self._last_monthly_report == month_label:
                self.logger.info(f"本月报告已生成，跳过 / Monthly report already generated for {month_label}")
                return
            
            # 生成报告内容
            report_data = self._collect_monthly_data(month_start, month_end)
            
            if not report_data:
                self.logger.warning("无法收集每月数据，跳过报告生成 / Cannot collect monthly data, skipping report")
                return
            
            # 使用报告生成器生成报告
            report_content = self._format_monthly_report(report_data, month_start, month_end)
            
            # 保存报告
            report_path = self._save_report(report_content, 'monthly', month_label)
            
            # 发送通知
            self._send_report_notification(
                report_type='monthly',
                report_date=month_label,
                report_content=report_content,
                report_path=report_path
            )
            
            self._last_monthly_report = month_label
            self.logger.info(f"每月报告生成完成 / Monthly report generated: {report_path}")
            
        except Exception as e:
            self.logger.error(f"生成每月报告失败 / Failed to generate monthly report: {e}", exc_info=True)
    
    def _check_risk_alerts(self) -> None:
        """
        检查风险预警 / Check risk alerts
        
        检查当前风险状况，如有异常则生成预警报告
        Checks current risk status, generates alert report if abnormal
        """
        try:
            if not self.risk_manager:
                return
            
            self.logger.debug("执行风险检查 / Performing risk check")
            
            # 获取当前投资组合
            portfolio = self._get_current_portfolio()
            
            if not portfolio:
                return
            
            # 执行风险检查
            risk_alert = self.risk_manager.generate_risk_alert(
                portfolio=portfolio,
                thresholds=self._get_risk_thresholds()
            )
            
            if risk_alert:
                self.logger.warning(f"检测到风险预警 / Risk alert detected: {risk_alert.get('alert_type')}")
                
                # 发送风险预警通知
                if self.notification_service:
                    self.notification_service.send_risk_alert(
                        alert=risk_alert,
                        recipients=self._get_notification_recipients(),
                        phone_numbers=self._get_notification_phone_numbers()
                    )
                
                self.logger.info("风险预警通知已发送 / Risk alert notification sent")
            
        except Exception as e:
            self.logger.error(f"风险检查失败 / Risk check failed: {e}", exc_info=True)
    
    def _collect_daily_data(self) -> Optional[Dict[str, Any]]:
        """
        收集每日数据 / Collect daily data
        
        Returns:
            Dict: 每日数据字典 / Daily data dictionary
        """
        data = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'portfolio': None,
            'trades': [],
            'returns': 0.0,
            'total_value': 0.0
        }
        
        # 从实盘交易管理器或模拟引擎获取数据
        if self.live_trading_manager:
            # TODO: 从实盘交易管理器获取数据
            pass
        elif self.simulation_engine:
            # TODO: 从模拟引擎获取数据
            pass
        elif self.portfolio_manager:
            # TODO: 从投资组合管理器获取数据
            pass
        
        return data
    
    def _collect_weekly_data(self, start_date: str, end_date: str) -> Optional[Dict[str, Any]]:
        """
        收集每周数据 / Collect weekly data
        
        Args:
            start_date: 开始日期 / Start date
            end_date: 结束日期 / End date
            
        Returns:
            Dict: 每周数据字典 / Weekly data dictionary
        """
        data = {
            'start_date': start_date,
            'end_date': end_date,
            'weekly_return': 0.0,
            'trades_count': 0,
            'win_rate': 0.0
        }
        
        # TODO: 实现数据收集逻辑
        
        return data
    
    def _collect_monthly_data(self, start_date: str, end_date: str) -> Optional[Dict[str, Any]]:
        """
        收集每月数据 / Collect monthly data
        
        Args:
            start_date: 开始日期 / Start date
            end_date: 结束日期 / End date
            
        Returns:
            Dict: 每月数据字典 / Monthly data dictionary
        """
        data = {
            'start_date': start_date,
            'end_date': end_date,
            'monthly_return': 0.0,
            'annualized_return': 0.0,
            'sharpe_ratio': 0.0,
            'max_drawdown': 0.0
        }
        
        # TODO: 实现数据收集逻辑
        
        return data
    
    def _format_daily_report(self, data: Dict[str, Any]) -> str:
        """
        格式化每日报告 / Format daily report
        
        Args:
            data: 每日数据 / Daily data
            
        Returns:
            str: HTML格式的报告内容 / HTML formatted report content
        """
        html = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .section {{ margin-bottom: 20px; }}
                .label {{ font-weight: bold; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>📊 每日交易报告 / Daily Trading Report</h2>
                <p>{data['date']}</p>
            </div>
            <div class="content">
                <div class="section">
                    <h3>今日概况 / Daily Summary</h3>
                    <p><span class="label">总收益率:</span> {data['returns']:.2f}%</p>
                    <p><span class="label">组合价值:</span> ¥{data['total_value']:,.2f}</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html
    
    def _format_weekly_report(self, data: Dict[str, Any], start_date: str, end_date: str) -> str:
        """
        格式化每周报告 / Format weekly report
        
        Args:
            data: 每周数据 / Weekly data
            start_date: 开始日期 / Start date
            end_date: 结束日期 / End date
            
        Returns:
            str: HTML格式的报告内容 / HTML formatted report content
        """
        html = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .header {{ background-color: #2196F3; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>📈 每周交易报告 / Weekly Trading Report</h2>
                <p>{start_date} 至 {end_date}</p>
            </div>
            <div class="content">
                <h3>本周概况 / Weekly Summary</h3>
                <p><span class="label">周收益率:</span> {data['weekly_return']:.2f}%</p>
                <p><span class="label">交易次数:</span> {data['trades_count']}</p>
                <p><span class="label">胜率:</span> {data['win_rate']:.2f}%</p>
            </div>
        </body>
        </html>
        """
        return html
    
    def _format_monthly_report(self, data: Dict[str, Any], start_date: str, end_date: str) -> str:
        """
        格式化每月报告 / Format monthly report
        
        Args:
            data: 每月数据 / Monthly data
            start_date: 开始日期 / Start date
            end_date: 结束日期 / End date
            
        Returns:
            str: HTML格式的报告内容 / HTML formatted report content
        """
        html = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .header {{ background-color: #FF9800; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>📅 每月交易报告 / Monthly Trading Report</h2>
                <p>{start_date} 至 {end_date}</p>
            </div>
            <div class="content">
                <h3>本月概况 / Monthly Summary</h3>
                <p><span class="label">月度收益率:</span> {data['monthly_return']:.2f}%</p>
                <p><span class="label">年化收益率:</span> {data['annualized_return']:.2f}%</p>
                <p><span class="label">夏普比率:</span> {data['sharpe_ratio']:.2f}</p>
                <p><span class="label">最大回撤:</span> {data['max_drawdown']:.2f}%</p>
            </div>
        </body>
        </html>
        """
        return html
    
    def _save_report(self, content: str, report_type: str, date_label: str) -> str:
        """
        保存报告到文件 / Save report to file
        
        Args:
            content: 报告内容 / Report content
            report_type: 报告类型 (daily/weekly/monthly) / Report type
            date_label: 日期标签 / Date label
            
        Returns:
            str: 报告文件路径 / Report file path
        """
        # 创建报告目录
        report_dir = Path('reports') / report_type
        report_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成文件名
        filename = f"{report_type}_report_{date_label}.html"
        report_path = report_dir / filename
        
        # 保存报告
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(report_path)
    
    def _send_report_notification(
        self,
        report_type: str,
        report_date: str,
        report_content: str,
        report_path: str
    ) -> None:
        """
        发送报告通知 / Send report notification
        
        Args:
            report_type: 报告类型 / Report type
            report_date: 报告日期 / Report date
            report_content: 报告内容 / Report content
            report_path: 报告文件路径 / Report file path
        """
        if not self.notification_service:
            self.logger.warning("通知服务未配置，跳过发送 / Notification service not configured, skipping")
            return
        
        # 构建邮件主题
        type_names = {
            'daily': '每日',
            'weekly': '每周',
            'monthly': '每月'
        }
        subject = f"【量化交易】{type_names.get(report_type, '')}交易报告 - {report_date}"
        
        # 发送邮件
        recipients = self._get_notification_recipients()
        if recipients:
            self.notification_service.send_email(
                recipients=recipients,
                subject=subject,
                body=report_content,
                html=True,
                attachments=[report_path] if Path(report_path).exists() else None
            )
    
    def _get_current_portfolio(self):
        """获取当前投资组合 / Get current portfolio"""
        if self.portfolio_manager:
            # TODO: 从投资组合管理器获取
            pass
        return None
    
    def _get_risk_thresholds(self):
        """获取风险阈值 / Get risk thresholds"""
        # TODO: 从配置获取
        return None
    
    def _get_notification_recipients(self) -> List[str]:
        """获取通知接收人邮箱列表 / Get notification recipients email list"""
        # TODO: 从配置获取
        return []
    
    def _get_notification_phone_numbers(self) -> List[str]:
        """获取通知接收人手机号列表 / Get notification recipients phone numbers"""
        # TODO: 从配置获取
        return []
    
    def is_running(self) -> bool:
        """
        检查调度器是否正在运行 / Check if scheduler is running
        
        Returns:
            bool: 正在运行返回True / True if running
        """
        return self._running
    
    def get_next_run_times(self) -> Dict[str, str]:
        """
        获取下次运行时间 / Get next run times
        
        Returns:
            Dict: 各类报告的下次运行时间 / Next run times for each report type
        """
        next_runs = {}
        
        for job in schedule.jobs:
            job_name = str(job.job_func)
            if 'daily' in job_name:
                next_runs['daily'] = str(job.next_run)
            elif 'weekly' in job_name:
                next_runs['weekly'] = str(job.next_run)
            elif 'monthly' in job_name:
                next_runs['monthly'] = str(job.next_run)
            elif 'risk' in job_name:
                next_runs['risk_check'] = str(job.next_run)
        
        return next_runs


# 全局报告调度器实例 / Global report scheduler instance
_report_scheduler = None


def get_report_scheduler() -> ReportScheduler:
    """
    获取全局报告调度器实例 / Get global report scheduler instance
    
    Returns:
        ReportScheduler: 报告调度器实例 / Report scheduler instance
    """
    global _report_scheduler
    if _report_scheduler is None:
        _report_scheduler = ReportScheduler()
    return _report_scheduler
