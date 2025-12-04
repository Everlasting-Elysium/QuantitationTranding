"""
报告生成器模块 / Report Generator Module
负责生成各种类型的报告，包括训练报告、回测报告和HTML报告
Responsible for generating various types of reports including training reports, backtest reports, and HTML reports
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass

from ..infrastructure.logger_system import get_logger


@dataclass
class TrainingResult:
    """
    训练结果 / Training Result
    
    Attributes:
        model_id: 模型ID / Model ID
        metrics: 评估指标 / Evaluation metrics
        training_time: 训练时长（秒）/ Training time (seconds)
        model_path: 模型保存路径 / Model save path
        experiment_id: 实验ID / Experiment ID
        run_id: 运行ID / Run ID
    """
    model_id: str
    metrics: Dict[str, float]
    training_time: float
    model_path: str
    experiment_id: str
    run_id: str = ""


@dataclass
class BacktestResult:
    """
    回测结果 / Backtest Result
    
    Attributes:
        returns: 收益率序列 / Returns series
        positions: 持仓数据 / Position data
        metrics: 性能指标 / Performance metrics
        trades: 交易记录列表 / Trade records list
        benchmark_returns: 基准收益率（可选）/ Benchmark returns (optional)
    """
    returns: pd.Series
    positions: pd.DataFrame
    metrics: Dict[str, float]
    trades: List[Any]
    benchmark_returns: Optional[pd.Series] = None


@dataclass
class SimulationReport:
    """
    模拟交易报告 / Simulation Trading Report
    
    Attributes:
        session_id: 会话ID / Session ID
        total_return: 总收益率 / Total return
        annual_return: 年化收益率 / Annual return
        sharpe_ratio: 夏普比率 / Sharpe ratio
        max_drawdown: 最大回撤 / Max drawdown
        win_rate: 胜率 / Win rate
        total_trades: 总交易次数 / Total trades
        profitable_trades: 盈利交易次数 / Profitable trades
        final_portfolio_value: 最终组合价值 / Final portfolio value
        daily_returns: 日收益率 / Daily returns
        trade_history: 交易历史 / Trade history
    """
    session_id: str
    total_return: float
    annual_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    total_trades: int
    profitable_trades: int
    final_portfolio_value: float
    daily_returns: pd.Series
    trade_history: List[Any]


@dataclass
class TradingSession:
    """
    交易会话 / Trading Session
    
    Attributes:
        session_id: 会话ID / Session ID
        model_id: 模型ID / Model ID
        start_date: 开始日期 / Start date
        initial_capital: 初始资金 / Initial capital
        current_capital: 当前资金 / Current capital
        status: 状态 / Status
        portfolio: 投资组合 / Portfolio
        total_return: 总收益率 / Total return
        config: 配置 / Configuration
    """
    session_id: str
    model_id: str
    start_date: str
    initial_capital: float
    current_capital: float
    status: str
    portfolio: Dict[str, Any]
    total_return: float
    config: Dict[str, Any]


class ReportGeneratorError(Exception):
    """报告生成器错误 / Report Generator Error"""
    pass


class ReportGenerator:
    """
    报告生成器 / Report Generator
    
    职责 / Responsibilities:
    - 生成训练报告 / Generate training reports
    - 生成回测报告 / Generate backtest reports
    - 生成模拟交易报告 / Generate simulation trading reports
    - 生成实盘交易报告 / Generate live trading reports
    - 生成HTML报告 / Generate HTML reports
    - 生成对比报告 / Generate comparison reports
    """
    
    def __init__(self, output_dir: str = "./outputs/reports"):
        """
        初始化报告生成器 / Initialize Report Generator
        
        Args:
            output_dir: 输出目录 / Output directory
        """
        self._output_dir = Path(output_dir).expanduser()
        self._logger = get_logger(__name__)
        
        # 确保输出目录存在 / Ensure output directory exists
        self._output_dir.mkdir(parents=True, exist_ok=True)
        
        self._logger.info(f"报告生成器初始化完成 / Report Generator initialized: {self._output_dir}")
    
    def generate_training_report(self, result: TrainingResult) -> str:
        """
        生成训练报告 / Generate Training Report
        
        Args:
            result: 训练结果 / Training result
            
        Returns:
            str: 报告文本 / Report text
            
        Raises:
            ReportGeneratorError: 生成失败时抛出 / Raised when generation fails
        """
        self._logger.info(f"开始生成训练报告 / Starting to generate training report: {result.model_id}")
        
        try:
            report_lines = []
            report_lines.append("=" * 80)
            report_lines.append("训练报告 / Training Report".center(80))
            report_lines.append("=" * 80)
            report_lines.append("")
            
            # 基本信息 / Basic Information
            report_lines.append("【基本信息 / Basic Information】")
            report_lines.append(f"模型ID / Model ID: {result.model_id}")
            report_lines.append(f"实验ID / Experiment ID: {result.experiment_id}")
            if result.run_id:
                report_lines.append(f"运行ID / Run ID: {result.run_id}")
            report_lines.append(f"训练时长 / Training Time: {result.training_time:.2f} 秒 / seconds")
            report_lines.append(f"模型路径 / Model Path: {result.model_path}")
            report_lines.append("")
            
            # 性能指标 / Performance Metrics
            report_lines.append("【性能指标 / Performance Metrics】")
            if result.metrics:
                for metric_name, metric_value in result.metrics.items():
                    # 格式化指标名称 / Format metric name
                    formatted_name = metric_name.replace("_", " ").title()
                    
                    # 根据指标类型格式化值 / Format value based on metric type
                    if isinstance(metric_value, float):
                        if "accuracy" in metric_name.lower() or "rate" in metric_name.lower():
                            formatted_value = f"{metric_value:.2%}"
                        elif "ic" in metric_name.lower():
                            formatted_value = f"{metric_value:.4f}"
                        else:
                            formatted_value = f"{metric_value:.4f}"
                    else:
                        formatted_value = str(metric_value)
                    
                    report_lines.append(f"{formatted_name}: {formatted_value}")
            else:
                report_lines.append("暂无指标数据 / No metrics data available")
            report_lines.append("")
            
            # 总结 / Summary
            report_lines.append("【总结 / Summary】")
            report_lines.append(f"模型训练成功完成 / Model training completed successfully")
            report_lines.append(f"生成时间 / Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_lines.append("")
            report_lines.append("=" * 80)
            
            report_text = "\n".join(report_lines)
            
            # 保存报告到文件 / Save report to file
            self._save_text_report(result.model_id, "training", report_text)
            
            self._logger.info(f"训练报告生成成功 / Training report generated successfully")
            
            return report_text
            
        except Exception as e:
            error_msg = f"生成训练报告失败 / Failed to generate training report: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise ReportGeneratorError(error_msg) from e

    def generate_backtest_report(self, result: BacktestResult) -> str:
        """
        生成回测报告 / Generate Backtest Report
        
        Args:
            result: 回测结果 / Backtest result
            
        Returns:
            str: 报告文本 / Report text
            
        Raises:
            ReportGeneratorError: 生成失败时抛出 / Raised when generation fails
        """
        self._logger.info("开始生成回测报告 / Starting to generate backtest report")
        
        try:
            report_lines = []
            report_lines.append("=" * 80)
            report_lines.append("回测报告 / Backtest Report".center(80))
            report_lines.append("=" * 80)
            report_lines.append("")
            
            # 回测周期 / Backtest Period
            report_lines.append("【回测周期 / Backtest Period】")
            if len(result.returns) > 0:
                start_date = result.returns.index[0]
                end_date = result.returns.index[-1]
                report_lines.append(f"开始日期 / Start Date: {start_date}")
                report_lines.append(f"结束日期 / End Date: {end_date}")
                report_lines.append(f"交易天数 / Trading Days: {len(result.returns)}")
            else:
                report_lines.append("暂无数据 / No data available")
            report_lines.append("")
            
            # 收益指标 / Return Metrics
            report_lines.append("【收益指标 / Return Metrics】")
            if result.metrics:
                # 总收益率 / Total Return
                total_return = result.metrics.get("total_return", 0)
                report_lines.append(f"总收益率 / Total Return: {total_return:.2%}")
                
                # 年化收益率 / Annual Return
                annual_return = result.metrics.get("annual_return", 0)
                report_lines.append(f"年化收益率 / Annual Return: {annual_return:.2%}")
                
                # 基准收益率（如果有）/ Benchmark Return (if available)
                if "benchmark_return" in result.metrics:
                    benchmark_return = result.metrics.get("benchmark_return", 0)
                    report_lines.append(f"基准收益率 / Benchmark Return: {benchmark_return:.2%}")
                    
                    # 超额收益 / Excess Return
                    if "excess_return" in result.metrics:
                        excess_return = result.metrics.get("excess_return", 0)
                        report_lines.append(f"超额收益 / Excess Return: {excess_return:.2%}")
            report_lines.append("")
            
            # 风险指标 / Risk Metrics
            report_lines.append("【风险指标 / Risk Metrics】")
            if result.metrics:
                # 波动率 / Volatility
                volatility = result.metrics.get("volatility", 0)
                report_lines.append(f"年化波动率 / Annual Volatility: {volatility:.2%}")
                
                # 夏普比率 / Sharpe Ratio
                sharpe_ratio = result.metrics.get("sharpe_ratio", 0)
                report_lines.append(f"夏普比率 / Sharpe Ratio: {sharpe_ratio:.4f}")
                
                # 最大回撤 / Max Drawdown
                max_drawdown = result.metrics.get("max_drawdown", 0)
                report_lines.append(f"最大回撤 / Max Drawdown: {max_drawdown:.2%}")
                
                # 信息比率（如果有）/ Information Ratio (if available)
                if "information_ratio" in result.metrics:
                    info_ratio = result.metrics.get("information_ratio", 0)
                    report_lines.append(f"信息比率 / Information Ratio: {info_ratio:.4f}")
            report_lines.append("")
            
            # 交易统计 / Trading Statistics
            report_lines.append("【交易统计 / Trading Statistics】")
            if result.metrics:
                # 胜率 / Win Rate
                win_rate = result.metrics.get("win_rate", 0)
                report_lines.append(f"胜率 / Win Rate: {win_rate:.2%}")
                
                # 交易次数 / Trade Count
                trade_count = len(result.trades) if result.trades else 0
                report_lines.append(f"交易次数 / Trade Count: {trade_count}")
            report_lines.append("")
            
            # 策略与基准对比 / Strategy vs Benchmark Comparison
            if result.benchmark_returns is not None and len(result.benchmark_returns) > 0:
                report_lines.append("【策略与基准对比 / Strategy vs Benchmark Comparison】")
                
                # 对齐索引 / Align indices
                common_index = result.returns.index.intersection(result.benchmark_returns.index)
                if len(common_index) > 0:
                    aligned_returns = result.returns.loc[common_index]
                    aligned_benchmark = result.benchmark_returns.loc[common_index]
                    
                    # 计算累计收益 / Calculate cumulative returns
                    strategy_cumulative = (1 + aligned_returns).cumprod().iloc[-1] - 1
                    benchmark_cumulative = (1 + aligned_benchmark).cumprod().iloc[-1] - 1
                    
                    report_lines.append(f"策略累计收益 / Strategy Cumulative Return: {strategy_cumulative:.2%}")
                    report_lines.append(f"基准累计收益 / Benchmark Cumulative Return: {benchmark_cumulative:.2%}")
                    report_lines.append(f"超额收益 / Excess Return: {(strategy_cumulative - benchmark_cumulative):.2%}")
                report_lines.append("")
            
            # 总结 / Summary
            report_lines.append("【总结 / Summary】")
            if result.metrics:
                total_return = result.metrics.get("total_return", 0)
                sharpe_ratio = result.metrics.get("sharpe_ratio", 0)
                max_drawdown = result.metrics.get("max_drawdown", 0)
                
                # 评估策略表现 / Evaluate strategy performance
                if total_return > 0 and sharpe_ratio > 1.0 and max_drawdown > -0.2:
                    performance = "优秀 / Excellent"
                elif total_return > 0 and sharpe_ratio > 0.5:
                    performance = "良好 / Good"
                elif total_return > 0:
                    performance = "一般 / Fair"
                else:
                    performance = "较差 / Poor"
                
                report_lines.append(f"策略表现 / Strategy Performance: {performance}")
            
            report_lines.append(f"生成时间 / Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_lines.append("")
            report_lines.append("=" * 80)
            
            report_text = "\n".join(report_lines)
            
            # 保存报告到文件 / Save report to file
            self._save_text_report("backtest", "backtest", report_text)
            
            self._logger.info("回测报告生成成功 / Backtest report generated successfully")
            
            return report_text
            
        except Exception as e:
            error_msg = f"生成回测报告失败 / Failed to generate backtest report: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise ReportGeneratorError(error_msg) from e
    
    def generate_simulation_report(self, result: SimulationReport) -> str:
        """
        生成模拟交易报告 / Generate Simulation Trading Report
        
        Args:
            result: 模拟交易报告 / Simulation trading report
            
        Returns:
            str: 报告文本 / Report text
            
        Raises:
            ReportGeneratorError: 生成失败时抛出 / Raised when generation fails
        """
        self._logger.info(f"开始生成模拟交易报告 / Starting to generate simulation report: {result.session_id}")
        
        try:
            report_lines = []
            report_lines.append("=" * 80)
            report_lines.append("模拟交易报告 / Simulation Trading Report".center(80))
            report_lines.append("=" * 80)
            report_lines.append("")
            
            # 基本信息 / Basic Information
            report_lines.append("【基本信息 / Basic Information】")
            report_lines.append(f"会话ID / Session ID: {result.session_id}")
            if len(result.daily_returns) > 0:
                start_date = result.daily_returns.index[0]
                end_date = result.daily_returns.index[-1]
                report_lines.append(f"模拟周期 / Simulation Period: {start_date} 至 / to {end_date}")
                report_lines.append(f"模拟天数 / Simulation Days: {len(result.daily_returns)}")
            report_lines.append(f"最终组合价值 / Final Portfolio Value: ¥{result.final_portfolio_value:,.2f}")
            report_lines.append("")
            
            # 收益指标 / Return Metrics
            report_lines.append("【收益指标 / Return Metrics】")
            report_lines.append(f"总收益率 / Total Return: {result.total_return:.2%}")
            report_lines.append(f"年化收益率 / Annual Return: {result.annual_return:.2%}")
            report_lines.append(f"夏普比率 / Sharpe Ratio: {result.sharpe_ratio:.4f}")
            report_lines.append(f"最大回撤 / Max Drawdown: {result.max_drawdown:.2%}")
            report_lines.append("")
            
            # 交易统计 / Trading Statistics
            report_lines.append("【交易统计 / Trading Statistics】")
            report_lines.append(f"总交易次数 / Total Trades: {result.total_trades}")
            report_lines.append(f"盈利交易次数 / Profitable Trades: {result.profitable_trades}")
            report_lines.append(f"胜率 / Win Rate: {result.win_rate:.2%}")
            
            if result.total_trades > 0:
                avg_trades_per_day = result.total_trades / len(result.daily_returns) if len(result.daily_returns) > 0 else 0
                report_lines.append(f"日均交易次数 / Avg Trades per Day: {avg_trades_per_day:.2f}")
            report_lines.append("")
            
            # 总结 / Summary
            report_lines.append("【总结 / Summary】")
            
            # 评估模拟表现 / Evaluate simulation performance
            if result.total_return > 0.1 and result.sharpe_ratio > 1.0 and result.max_drawdown > -0.15:
                performance = "优秀 / Excellent - 建议进入实盘交易 / Recommended for live trading"
            elif result.total_return > 0.05 and result.sharpe_ratio > 0.5:
                performance = "良好 / Good - 可以考虑实盘交易 / Consider live trading"
            elif result.total_return > 0:
                performance = "一般 / Fair - 建议调整参数后重新测试 / Recommend parameter adjustment"
            else:
                performance = "较差 / Poor - 需要重新优化策略 / Strategy optimization needed"
            
            report_lines.append(f"模拟表现 / Simulation Performance: {performance}")
            report_lines.append(f"生成时间 / Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_lines.append("")
            report_lines.append("=" * 80)
            
            report_text = "\n".join(report_lines)
            
            # 保存报告到文件 / Save report to file
            self._save_text_report(result.session_id, "simulation", report_text)
            
            self._logger.info("模拟交易报告生成成功 / Simulation report generated successfully")
            
            return report_text
            
        except Exception as e:
            error_msg = f"生成模拟交易报告失败 / Failed to generate simulation report: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise ReportGeneratorError(error_msg) from e
    
    def generate_live_trading_report(self, session: TradingSession) -> str:
        """
        生成实盘交易报告 / Generate Live Trading Report
        
        Args:
            session: 交易会话 / Trading session
            
        Returns:
            str: 报告文本 / Report text
            
        Raises:
            ReportGeneratorError: 生成失败时抛出 / Raised when generation fails
        """
        self._logger.info(f"开始生成实盘交易报告 / Starting to generate live trading report: {session.session_id}")
        
        try:
            report_lines = []
            report_lines.append("=" * 80)
            report_lines.append("实盘交易报告 / Live Trading Report".center(80))
            report_lines.append("=" * 80)
            report_lines.append("")
            
            # 基本信息 / Basic Information
            report_lines.append("【基本信息 / Basic Information】")
            report_lines.append(f"会话ID / Session ID: {session.session_id}")
            report_lines.append(f"模型ID / Model ID: {session.model_id}")
            report_lines.append(f"开始日期 / Start Date: {session.start_date}")
            report_lines.append(f"状态 / Status: {session.status}")
            report_lines.append("")
            
            # 资金情况 / Capital Status
            report_lines.append("【资金情况 / Capital Status】")
            report_lines.append(f"初始资金 / Initial Capital: ¥{session.initial_capital:,.2f}")
            report_lines.append(f"当前资金 / Current Capital: ¥{session.current_capital:,.2f}")
            
            profit_loss = session.current_capital - session.initial_capital
            profit_loss_pct = profit_loss / session.initial_capital if session.initial_capital > 0 else 0
            
            report_lines.append(f"盈亏金额 / Profit/Loss: ¥{profit_loss:,.2f}")
            report_lines.append(f"盈亏比例 / Profit/Loss %: {profit_loss_pct:.2%}")
            report_lines.append(f"总收益率 / Total Return: {session.total_return:.2%}")
            report_lines.append("")
            
            # 持仓情况 / Position Status
            report_lines.append("【持仓情况 / Position Status】")
            if session.portfolio and isinstance(session.portfolio, dict):
                positions = session.portfolio.get("positions", {})
                if positions:
                    report_lines.append(f"持仓数量 / Position Count: {len(positions)}")
                    report_lines.append("持仓明细 / Position Details:")
                    for symbol, quantity in positions.items():
                        report_lines.append(f"  - {symbol}: {quantity}")
                else:
                    report_lines.append("当前无持仓 / No positions currently")
                
                cash = session.portfolio.get("cash", 0)
                report_lines.append(f"现金余额 / Cash Balance: ¥{cash:,.2f}")
            else:
                report_lines.append("暂无持仓数据 / No position data available")
            report_lines.append("")
            
            # 风险提示 / Risk Warning
            report_lines.append("【风险提示 / Risk Warning】")
            if profit_loss_pct < -0.05:
                report_lines.append("⚠️ 警告：当前亏损超过5%，请注意风险控制")
                report_lines.append("⚠️ Warning: Current loss exceeds 5%, please pay attention to risk control")
            elif profit_loss_pct < -0.02:
                report_lines.append("⚠️ 提示：当前有小幅亏损，建议密切关注")
                report_lines.append("⚠️ Notice: Current minor loss, recommend close monitoring")
            else:
                report_lines.append("✓ 当前风险可控 / Current risk is under control")
            report_lines.append("")
            
            # 总结 / Summary
            report_lines.append("【总结 / Summary】")
            report_lines.append(f"实盘交易进行中 / Live trading in progress")
            report_lines.append(f"生成时间 / Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_lines.append("")
            report_lines.append("=" * 80)
            
            report_text = "\n".join(report_lines)
            
            # 保存报告到文件 / Save report to file
            self._save_text_report(session.session_id, "live_trading", report_text)
            
            self._logger.info("实盘交易报告生成成功 / Live trading report generated successfully")
            
            return report_text
            
        except Exception as e:
            error_msg = f"生成实盘交易报告失败 / Failed to generate live trading report: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise ReportGeneratorError(error_msg) from e

    def generate_html_report(
        self,
        result: BacktestResult,
        output_path: str,
        chart_paths: Optional[Dict[str, str]] = None
    ) -> None:
        """
        生成HTML报告 / Generate HTML Report
        
        Args:
            result: 回测结果 / Backtest result
            output_path: 输出路径 / Output path
            chart_paths: 图表路径字典（可选）/ Chart paths dict (optional)
            
        Raises:
            ReportGeneratorError: 生成失败时抛出 / Raised when generation fails
        """
        self._logger.info(f"开始生成HTML报告 / Starting to generate HTML report: {output_path}")
        
        try:
            # 生成HTML内容 / Generate HTML content
            html_content = self._build_html_report(result, chart_paths)
            
            # 保存HTML文件 / Save HTML file
            output_path = Path(output_path).expanduser()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self._logger.info(f"HTML报告生成成功 / HTML report generated successfully: {output_path}")
            
        except Exception as e:
            error_msg = f"生成HTML报告失败 / Failed to generate HTML report: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise ReportGeneratorError(error_msg) from e
    
    def _build_html_report(
        self,
        result: BacktestResult,
        chart_paths: Optional[Dict[str, str]] = None
    ) -> str:
        """
        构建HTML报告内容 / Build HTML Report Content
        
        Args:
            result: 回测结果 / Backtest result
            chart_paths: 图表路径字典（可选）/ Chart paths dict (optional)
            
        Returns:
            str: HTML内容 / HTML content
        """
        # HTML模板 / HTML template
        html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>回测报告 / Backtest Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', 'Microsoft YaHei', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 1.8em;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        
        .metric-label {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 5px;
        }}
        
        .metric-value {{
            font-size: 1.8em;
            font-weight: bold;
            color: #333;
        }}
        
        .metric-value.positive {{
            color: #28a745;
        }}
        
        .metric-value.negative {{
            color: #dc3545;
        }}
        
        .chart-container {{
            margin: 30px 0;
            text-align: center;
        }}
        
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .chart-title {{
            font-size: 1.2em;
            color: #555;
            margin-bottom: 15px;
            font-weight: 600;
        }}
        
        .summary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin-top: 40px;
        }}
        
        .summary h3 {{
            font-size: 1.5em;
            margin-bottom: 15px;
        }}
        
        .summary p {{
            font-size: 1.1em;
            line-height: 1.8;
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            color: #666;
            font-size: 0.9em;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        
        th {{
            background: #667eea;
            color: white;
            font-weight: 600;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 回测报告</h1>
            <h1>Backtest Report</h1>
            <p>生成时间 / Generated at: {generated_time}</p>
        </div>
        
        <div class="content">
            <!-- 回测周期 / Backtest Period -->
            <div class="section">
                <h2 class="section-title">📅 回测周期 / Backtest Period</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">开始日期 / Start Date</div>
                        <div class="metric-value">{start_date}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">结束日期 / End Date</div>
                        <div class="metric-value">{end_date}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">交易天数 / Trading Days</div>
                        <div class="metric-value">{trading_days}</div>
                    </div>
                </div>
            </div>
            
            <!-- 收益指标 / Return Metrics -->
            <div class="section">
                <h2 class="section-title">💰 收益指标 / Return Metrics</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">总收益率 / Total Return</div>
                        <div class="metric-value {total_return_class}">{total_return}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">年化收益率 / Annual Return</div>
                        <div class="metric-value {annual_return_class}">{annual_return}</div>
                    </div>
                    {benchmark_section}
                </div>
            </div>
            
            <!-- 风险指标 / Risk Metrics -->
            <div class="section">
                <h2 class="section-title">⚠️ 风险指标 / Risk Metrics</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">年化波动率 / Annual Volatility</div>
                        <div class="metric-value">{volatility}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">夏普比率 / Sharpe Ratio</div>
                        <div class="metric-value">{sharpe_ratio}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">最大回撤 / Max Drawdown</div>
                        <div class="metric-value negative">{max_drawdown}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">胜率 / Win Rate</div>
                        <div class="metric-value">{win_rate}</div>
                    </div>
                </div>
            </div>
            
            <!-- 可视化图表 / Visualization Charts -->
            {charts_section}
            
            <!-- 总结 / Summary -->
            <div class="summary">
                <h3>📝 总结 / Summary</h3>
                <p>{summary_text}</p>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2024 Qlib Trading System | 量化交易系统</p>
            <p>本报告由系统自动生成 / This report is automatically generated by the system</p>
        </div>
    </div>
</body>
</html>
"""
        
        # 准备数据 / Prepare data
        generated_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 回测周期 / Backtest period
        if len(result.returns) > 0:
            start_date = str(result.returns.index[0])
            end_date = str(result.returns.index[-1])
            trading_days = len(result.returns)
        else:
            start_date = "N/A"
            end_date = "N/A"
            trading_days = 0
        
        # 收益指标 / Return metrics
        total_return = result.metrics.get("total_return", 0)
        annual_return = result.metrics.get("annual_return", 0)
        total_return_class = "positive" if total_return > 0 else "negative"
        annual_return_class = "positive" if annual_return > 0 else "negative"
        
        # 基准部分 / Benchmark section
        benchmark_section = ""
        if "benchmark_return" in result.metrics:
            benchmark_return = result.metrics.get("benchmark_return", 0)
            excess_return = result.metrics.get("excess_return", 0)
            excess_return_class = "positive" if excess_return > 0 else "negative"
            
            benchmark_section = f"""
                    <div class="metric-card">
                        <div class="metric-label">基准收益率 / Benchmark Return</div>
                        <div class="metric-value">{benchmark_return:.2%}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">超额收益 / Excess Return</div>
                        <div class="metric-value {excess_return_class}">{excess_return:.2%}</div>
                    </div>
            """
        
        # 风险指标 / Risk metrics
        volatility = result.metrics.get("volatility", 0)
        sharpe_ratio = result.metrics.get("sharpe_ratio", 0)
        max_drawdown = result.metrics.get("max_drawdown", 0)
        win_rate = result.metrics.get("win_rate", 0)
        
        # 图表部分 / Charts section
        charts_section = ""
        if chart_paths:
            charts_section = '<div class="section"><h2 class="section-title">📈 可视化图表 / Visualization Charts</h2>'
            
            # 累计收益曲线 / Cumulative returns chart
            if "cumulative_returns" in chart_paths:
                charts_section += f"""
                <div class="chart-container">
                    <div class="chart-title">累计收益曲线 / Cumulative Returns</div>
                    <img src="{chart_paths['cumulative_returns']}" alt="Cumulative Returns">
                </div>
                """
            
            # 持仓分布 / Position distribution
            if "position_distribution" in chart_paths:
                charts_section += f"""
                <div class="chart-container">
                    <div class="chart-title">持仓分布 / Position Distribution</div>
                    <img src="{chart_paths['position_distribution']}" alt="Position Distribution">
                </div>
                """
            
            # 行业分布 / Sector distribution
            if "sector_distribution" in chart_paths:
                charts_section += f"""
                <div class="chart-container">
                    <div class="chart-title">行业分布 / Sector Distribution</div>
                    <img src="{chart_paths['sector_distribution']}" alt="Sector Distribution">
                </div>
                """
            
            charts_section += '</div>'
        
        # 总结文本 / Summary text
        if total_return > 0 and sharpe_ratio > 1.0 and max_drawdown > -0.2:
            summary_text = "策略表现优秀，收益稳定且风险可控，建议继续使用。/ Strategy performance is excellent with stable returns and controlled risk. Recommended for continued use."
        elif total_return > 0 and sharpe_ratio > 0.5:
            summary_text = "策略表现良好，有一定收益但需注意风险控制。/ Strategy performance is good with decent returns, but risk control needs attention."
        elif total_return > 0:
            summary_text = "策略有正收益但表现一般，建议优化参数或调整策略。/ Strategy has positive returns but performance is fair. Parameter optimization or strategy adjustment recommended."
        else:
            summary_text = "策略表现较差，建议重新评估策略逻辑或更换策略。/ Strategy performance is poor. Re-evaluation of strategy logic or strategy replacement recommended."
        
        # 填充模板 / Fill template
        html_content = html_template.format(
            generated_time=generated_time,
            start_date=start_date,
            end_date=end_date,
            trading_days=trading_days,
            total_return=f"{total_return:.2%}",
            total_return_class=total_return_class,
            annual_return=f"{annual_return:.2%}",
            annual_return_class=annual_return_class,
            benchmark_section=benchmark_section,
            volatility=f"{volatility:.2%}",
            sharpe_ratio=f"{sharpe_ratio:.4f}",
            max_drawdown=f"{max_drawdown:.2%}",
            win_rate=f"{win_rate:.2%}",
            charts_section=charts_section,
            summary_text=summary_text
        )
        
        return html_content
    
    def generate_comparison_report(self, results: List[BacktestResult]) -> str:
        """
        生成对比报告 / Generate Comparison Report
        
        Args:
            results: 回测结果列表 / Backtest results list
            
        Returns:
            str: 报告文本 / Report text
            
        Raises:
            ReportGeneratorError: 生成失败时抛出 / Raised when generation fails
        """
        self._logger.info(f"开始生成对比报告 / Starting to generate comparison report: {len(results)} results")
        
        try:
            if not results or len(results) == 0:
                raise ReportGeneratorError("回测结果列表为空 / Backtest results list is empty")
            
            report_lines = []
            report_lines.append("=" * 80)
            report_lines.append("多策略对比报告 / Multi-Strategy Comparison Report".center(80))
            report_lines.append("=" * 80)
            report_lines.append("")
            
            # 对比表格 / Comparison table
            report_lines.append("【策略对比 / Strategy Comparison】")
            report_lines.append("")
            
            # 表头 / Table header
            header = f"{'策略/Strategy':<20} {'总收益/Total':<15} {'年化/Annual':<15} {'夏普/Sharpe':<15} {'回撤/Drawdown':<15}"
            report_lines.append(header)
            report_lines.append("-" * 80)
            
            # 每个策略的数据 / Data for each strategy
            for i, result in enumerate(results):
                strategy_name = f"Strategy {i+1}"
                total_return = result.metrics.get("total_return", 0)
                annual_return = result.metrics.get("annual_return", 0)
                sharpe_ratio = result.metrics.get("sharpe_ratio", 0)
                max_drawdown = result.metrics.get("max_drawdown", 0)
                
                row = f"{strategy_name:<20} {total_return:>13.2%} {annual_return:>13.2%} {sharpe_ratio:>13.4f} {max_drawdown:>13.2%}"
                report_lines.append(row)
            
            report_lines.append("")
            
            # 最佳策略 / Best strategy
            report_lines.append("【最佳策略 / Best Strategy】")
            
            # 按不同指标找最佳 / Find best by different metrics
            best_return_idx = max(range(len(results)), key=lambda i: results[i].metrics.get("total_return", 0))
            best_sharpe_idx = max(range(len(results)), key=lambda i: results[i].metrics.get("sharpe_ratio", 0))
            best_drawdown_idx = max(range(len(results)), key=lambda i: results[i].metrics.get("max_drawdown", 0))
            
            report_lines.append(f"最高收益策略 / Highest Return: Strategy {best_return_idx + 1} ({results[best_return_idx].metrics.get('total_return', 0):.2%})")
            report_lines.append(f"最高夏普策略 / Highest Sharpe: Strategy {best_sharpe_idx + 1} ({results[best_sharpe_idx].metrics.get('sharpe_ratio', 0):.4f})")
            report_lines.append(f"最小回撤策略 / Smallest Drawdown: Strategy {best_drawdown_idx + 1} ({results[best_drawdown_idx].metrics.get('max_drawdown', 0):.2%})")
            report_lines.append("")
            
            # 总结 / Summary
            report_lines.append("【总结 / Summary】")
            report_lines.append(f"共对比 {len(results)} 个策略 / Compared {len(results)} strategies")
            report_lines.append(f"生成时间 / Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_lines.append("")
            report_lines.append("=" * 80)
            
            report_text = "\n".join(report_lines)
            
            # 保存报告到文件 / Save report to file
            self._save_text_report("comparison", "comparison", report_text)
            
            self._logger.info("对比报告生成成功 / Comparison report generated successfully")
            
            return report_text
            
        except Exception as e:
            error_msg = f"生成对比报告失败 / Failed to generate comparison report: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise ReportGeneratorError(error_msg) from e
    
    def _save_text_report(self, report_id: str, report_type: str, content: str) -> None:
        """
        保存文本报告到文件 / Save Text Report to File
        
        Args:
            report_id: 报告ID / Report ID
            report_type: 报告类型 / Report type
            content: 报告内容 / Report content
        """
        try:
            # 创建报告目录 / Create report directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_dir = self._output_dir / report_type
            report_dir.mkdir(parents=True, exist_ok=True)
            
            # 保存报告 / Save report
            report_path = report_dir / f"{report_id}_{timestamp}.txt"
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self._logger.info(f"报告保存成功 / Report saved successfully: {report_path}")
            
        except Exception as e:
            self._logger.warning(f"保存报告失败 / Failed to save report: {str(e)}")
