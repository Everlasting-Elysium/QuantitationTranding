"""
Performance Analyzer for the qlib trading system.
表现分析器

This module provides functionality to analyze historical performance of assets
and generate recommendations based on multiple metrics.
本模块提供分析资产历史表现并基于多个指标生成推荐的功能。
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path

from ..models.market_models import (
    AssetMetrics, AssetRecommendation, PerformanceReport
)
from ..infrastructure.logger_system import LoggerSystem
from ..infrastructure.qlib_wrapper import QlibWrapper
from ..utils.error_handler import DataError, ErrorInfo, ErrorCategory, ErrorSeverity


class PerformanceAnalyzer:
    """
    Performance analyzer for analyzing historical asset performance.
    用于分析资产历史表现的表现分析器
    
    This class handles:
    - Analyzing historical performance over specified periods
    - Calculating key metrics (returns, Sharpe ratio, max drawdown)
    - Ranking assets based on performance
    - Generating recommendations
    
    本类处理：
    - 分析指定期间的历史表现
    - 计算关键指标（收益率、夏普比率、最大回撤）
    - 基于表现对资产进行排名
    - 生成推荐
    """
    
    def __init__(self, qlib_wrapper: Optional[QlibWrapper] = None):
        """
        Initialize the performance analyzer.
        初始化表现分析器
        
        Args:
            qlib_wrapper: QlibWrapper instance for data access
                         用于数据访问的QlibWrapper实例
        """
        logger_system = LoggerSystem()
        self.logger = logger_system.get_logger(__name__)
        self.qlib_wrapper = qlib_wrapper or QlibWrapper()
        
        # Risk-free rate for Sharpe ratio calculation (annualized)
        # 用于夏普比率计算的无风险利率（年化）
        self.risk_free_rate = 0.03  # 3% default
        
        self.logger.info("PerformanceAnalyzer initialized")
        self.logger.info("表现分析器已初始化")
    
    def analyze_historical_performance(
        self,
        market: str,
        asset_type: str,
        lookback_years: int = 3,
        instruments: Optional[str] = None
    ) -> PerformanceReport:
        """
        Analyze historical performance of assets over a specified period.
        分析指定期间内资产的历史表现
        
        Args:
            market: Market code (e.g., "CN", "US")
                   市场代码（例如："CN"、"US"）
            asset_type: Asset type code (e.g., "stock", "fund")
                       资产类型代码（例如："stock"、"fund"）
            lookback_years: Number of years to look back for analysis
                           回溯分析的年数
            instruments: Instrument pool to analyze (e.g., "csi300")
                        要分析的工具池（例如："csi300"）
        
        Returns:
            PerformanceReport: Comprehensive performance analysis report
                              综合表现分析报告
        
        Raises:
            DataError: If analysis fails
                      如果分析失败
        """
        try:
            self.logger.info(
                f"Starting historical performance analysis / 开始历史表现分析\n"
                f"Market: {market}, Asset Type: {asset_type}, "
                f"Lookback: {lookback_years} years"
            )
            
            # Calculate date range
            # 计算日期范围
            end_date = datetime.now()
            start_date = end_date - timedelta(days=lookback_years * 365)
            
            start_date_str = start_date.strftime("%Y-%m-%d")
            end_date_str = end_date.strftime("%Y-%m-%d")
            
            # Determine instruments pool
            # 确定工具池
            if instruments is None:
                instruments = self._get_default_instruments(market, asset_type)
            
            self.logger.info(
                f"Analysis period: {start_date_str} to {end_date_str}\n"
                f"分析期间: {start_date_str} 至 {end_date_str}\n"
                f"Instruments pool: {instruments} / 工具池: {instruments}"
            )
            
            # Get list of instruments
            # 获取工具列表
            instrument_list = self._get_instrument_list(instruments)
            
            if not instrument_list:
                error_info = ErrorInfo(
                    error_code="PERF0001",
                    error_message_zh=f"未找到可分析的资产: {instruments}",
                    error_message_en=f"No assets found for analysis: {instruments}",
                    category=ErrorCategory.DATA,
                    severity=ErrorSeverity.HIGH,
                    technical_details=f"Instruments: {instruments}, Market: {market}",
                    suggested_actions=[
                        "检查工具池名称是否正确",
                        "确认数据是否已下载",
                        "验证市场和资产类型配置"
                    ],
                    recoverable=True
                )
                raise DataError(error_info)
            
            self.logger.info(f"Found {len(instrument_list)} instruments to analyze")
            self.logger.info(f"找到 {len(instrument_list)} 个工具进行分析")
            
            # Analyze each instrument
            # 分析每个工具
            all_metrics = []
            for symbol in instrument_list:
                try:
                    metrics = self.get_asset_metrics(
                        symbol, start_date_str, end_date_str
                    )
                    if metrics:
                        all_metrics.append(metrics)
                except Exception as e:
                    self.logger.warning(
                        f"Failed to analyze {symbol}: {str(e)} / "
                        f"分析 {symbol} 失败: {str(e)}"
                    )
                    continue
            
            if not all_metrics:
                error_info = ErrorInfo(
                    error_code="PERF0002",
                    error_message_zh="没有成功分析的资产",
                    error_message_en="No assets successfully analyzed",
                    category=ErrorCategory.DATA,
                    severity=ErrorSeverity.HIGH,
                    technical_details=f"Attempted to analyze {len(instrument_list)} instruments",
                    suggested_actions=[
                        "检查数据质量",
                        "确认时间范围内有足够的数据",
                        "查看日志了解具体失败原因"
                    ],
                    recoverable=True
                )
                raise DataError(error_info)
            
            self.logger.info(
                f"Successfully analyzed {len(all_metrics)} out of {len(instrument_list)} instruments\n"
                f"成功分析了 {len(instrument_list)} 个工具中的 {len(all_metrics)} 个"
            )
            
            # Calculate average metrics
            # 计算平均指标
            avg_return = np.mean([m.annual_return for m in all_metrics])
            avg_sharpe = np.mean([m.sharpe_ratio for m in all_metrics])
            avg_drawdown = np.mean([m.max_drawdown for m in all_metrics])
            
            # Generate recommendations
            # 生成推荐
            top_performers = self._rank_assets(all_metrics, top_n=10)
            
            # Create performance report
            # 创建表现报告
            report = PerformanceReport(
                market=market,
                asset_type=asset_type,
                analysis_period_start=start_date_str,
                analysis_period_end=end_date_str,
                total_assets_analyzed=len(all_metrics),
                top_performers=top_performers,
                average_return=avg_return,
                average_sharpe=avg_sharpe,
                average_drawdown=avg_drawdown,
                analysis_timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
            self.logger.info(
                f"Performance analysis completed / 表现分析完成\n"
                f"Average annual return: {avg_return:.2%} / 平均年化收益率: {avg_return:.2%}\n"
                f"Average Sharpe ratio: {avg_sharpe:.2f} / 平均夏普比率: {avg_sharpe:.2f}\n"
                f"Average max drawdown: {avg_drawdown:.2%} / 平均最大回撤: {avg_drawdown:.2%}"
            )
            
            return report
            
        except DataError:
            raise
        except Exception as e:
            error_info = ErrorInfo(
                error_code="PERF0003",
                error_message_zh=f"历史表现分析失败: {str(e)}",
                error_message_en=f"Historical performance analysis failed: {str(e)}",
                category=ErrorCategory.DATA,
                severity=ErrorSeverity.HIGH,
                technical_details=str(e),
                suggested_actions=[
                    "检查qlib是否正确初始化",
                    "确认数据是否可用",
                    "验证参数是否正确",
                    "查看详细日志了解错误原因"
                ],
                recoverable=True,
                original_exception=e
            )
            self.logger.error(error_info.get_user_message(), exc_info=True)
            raise DataError(error_info)

    def recommend_top_performers(
        self,
        market: str,
        asset_type: str,
        top_n: int = 10,
        criteria: str = "sharpe_ratio",
        lookback_years: int = 3
    ) -> List[AssetRecommendation]:
        """
        Recommend top performing assets based on specified criteria.
        基于指定标准推荐表现最佳的资产
        
        Args:
            market: Market code
                   市场代码
            asset_type: Asset type code
                       资产类型代码
            top_n: Number of top performers to recommend
                   推荐的顶级表现者数量
            criteria: Ranking criteria ("sharpe_ratio", "annual_return", "综合评分")
                     排名标准（"sharpe_ratio"、"annual_return"、"综合评分"）
            lookback_years: Number of years to look back
                           回溯年数
        
        Returns:
            List[AssetRecommendation]: List of recommended assets
                                       推荐资产列表
        
        Raises:
            DataError: If recommendation fails
                      如果推荐失败
        """
        try:
            self.logger.info(
                f"Generating recommendations / 生成推荐\n"
                f"Criteria: {criteria}, Top N: {top_n}"
            )
            
            # Perform historical analysis
            # 执行历史分析
            report = self.analyze_historical_performance(
                market=market,
                asset_type=asset_type,
                lookback_years=lookback_years
            )
            
            # Get top performers from report
            # 从报告中获取顶级表现者
            recommendations = report.top_performers[:top_n]
            
            self.logger.info(
                f"Generated {len(recommendations)} recommendations / "
                f"生成了 {len(recommendations)} 个推荐"
            )
            
            return recommendations
            
        except Exception as e:
            error_info = ErrorInfo(
                error_code="PERF0004",
                error_message_zh=f"生成推荐失败: {str(e)}",
                error_message_en=f"Failed to generate recommendations: {str(e)}",
                category=ErrorCategory.DATA,
                severity=ErrorSeverity.MEDIUM,
                technical_details=str(e),
                suggested_actions=[
                    "检查分析参数是否正确",
                    "确认数据是否可用",
                    "尝试调整回溯期间"
                ],
                recoverable=True,
                original_exception=e
            )
            self.logger.error(error_info.get_user_message(), exc_info=True)
            raise DataError(error_info)
    
    def get_asset_metrics(
        self,
        asset_code: str,
        start_date: str,
        end_date: str
    ) -> Optional[AssetMetrics]:
        """
        Calculate performance metrics for a single asset.
        计算单个资产的表现指标
        
        Args:
            asset_code: Asset symbol/code
                       资产代码
            start_date: Start date for analysis
                       分析开始日期
            end_date: End date for analysis
                     分析结束日期
        
        Returns:
            AssetMetrics: Performance metrics for the asset
                         资产的表现指标
        
        Raises:
            DataError: If metrics calculation fails
                      如果指标计算失败
        """
        try:
            # Get price data
            # 获取价格数据
            price_data = self.qlib_wrapper.get_data(
                instruments=asset_code,
                fields=["$close"],
                start_time=start_date,
                end_time=end_date
            )
            
            if price_data is None or price_data.empty:
                self.logger.warning(
                    f"No data available for {asset_code} / "
                    f"{asset_code} 没有可用数据"
                )
                return None
            
            # Calculate returns
            # 计算收益率
            prices = price_data["$close"]
            returns = prices.pct_change().dropna()
            
            if len(returns) < 20:  # Minimum data points required
                self.logger.warning(
                    f"Insufficient data for {asset_code}: {len(returns)} points / "
                    f"{asset_code} 数据不足: {len(returns)} 个数据点"
                )
                return None
            
            # Calculate metrics
            # 计算指标
            total_return = (prices.iloc[-1] / prices.iloc[0]) - 1
            
            # Annualized return
            # 年化收益率
            trading_days = len(returns)
            years = trading_days / 252  # Assuming 252 trading days per year
            annual_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0
            
            # Volatility (annualized)
            # 波动率（年化）
            volatility = returns.std() * np.sqrt(252)
            
            # Sharpe ratio
            # 夏普比率
            excess_return = annual_return - self.risk_free_rate
            sharpe_ratio = excess_return / volatility if volatility > 0 else 0
            
            # Maximum drawdown
            # 最大回撤
            cumulative = (1 + returns).cumprod()
            running_max = cumulative.expanding().max()
            drawdown = (cumulative - running_max) / running_max
            max_drawdown = drawdown.min()
            
            # Win rate
            # 胜率
            win_rate = (returns > 0).sum() / len(returns)
            
            metrics = AssetMetrics(
                symbol=asset_code,
                period_start=start_date,
                period_end=end_date,
                total_return=total_return,
                annual_return=annual_return,
                volatility=volatility,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=max_drawdown,
                win_rate=win_rate
            )
            
            return metrics
            
        except Exception as e:
            self.logger.warning(
                f"Failed to calculate metrics for {asset_code}: {str(e)} / "
                f"计算 {asset_code} 的指标失败: {str(e)}"
            )
            return None
    
    def _rank_assets(
        self,
        metrics_list: List[AssetMetrics],
        top_n: int = 10
    ) -> List[AssetRecommendation]:
        """
        Rank assets based on综合评分 and generate recommendations.
        基于综合评分对资产进行排名并生成推荐
        
        Args:
            metrics_list: List of asset metrics
                         资产指标列表
            top_n: Number of top assets to return
                   返回的顶级资产数量
        
        Returns:
            List[AssetRecommendation]: Ranked list of recommendations
                                       排名的推荐列表
        """
        recommendations = []
        
        for metrics in metrics_list:
            # Calculate综合评分 (0-100)
            # 计算综合评分 (0-100)
            # Weighted combination of metrics
            # 指标的加权组合
            
            # Normalize Sharpe ratio (assume good Sharpe is > 1.0)
            # 标准化夏普比率（假设好的夏普比率 > 1.0）
            sharpe_score = min(metrics.sharpe_ratio / 2.0, 1.0) * 40  # Max 40 points
            
            # Normalize annual return (assume good return is > 20%)
            # 标准化年化收益率（假设好的收益率 > 20%）
            return_score = min(metrics.annual_return / 0.2, 1.0) * 40  # Max 40 points
            
            # Normalize max drawdown (lower is better, assume -30% is bad)
            # 标准化最大回撤（越低越好，假设-30%是差的）
            drawdown_score = max(1 + metrics.max_drawdown / 0.3, 0) * 20  # Max 20 points
            
            performance_score = sharpe_score + return_score + drawdown_score
            
            # Generate recommendation reason
            # 生成推荐理由
            reason = self._generate_recommendation_reason(metrics, performance_score)
            
            recommendation = AssetRecommendation(
                symbol=metrics.symbol,
                name=metrics.symbol,  # TODO: Get actual name from data
                asset_type="stock",  # TODO: Get from context
                performance_score=performance_score,
                sharpe_ratio=metrics.sharpe_ratio,
                annual_return=metrics.annual_return,
                max_drawdown=metrics.max_drawdown,
                recommendation_reason=reason
            )
            
            recommendations.append(recommendation)
        
        # Sort by performance score
        # 按表现评分排序
        recommendations.sort(key=lambda x: x.performance_score, reverse=True)
        
        # Assign ranks
        # 分配排名
        for i, rec in enumerate(recommendations[:top_n], 1):
            rec.rank = i
        
        return recommendations[:top_n]
    
    def _generate_recommendation_reason(
        self,
        metrics: AssetMetrics,
        score: float
    ) -> str:
        """
        Generate a human-readable recommendation reason.
        生成人类可读的推荐理由
        
        Args:
            metrics: Asset metrics
                    资产指标
            score: Performance score
                  表现评分
        
        Returns:
            str: Recommendation reason in Chinese
                 中文推荐理由
        """
        reasons = []
        
        # Analyze Sharpe ratio
        # 分析夏普比率
        if metrics.sharpe_ratio > 1.5:
            reasons.append("风险调整后收益优秀")
        elif metrics.sharpe_ratio > 1.0:
            reasons.append("风险调整后收益良好")
        
        # Analyze annual return
        # 分析年化收益率
        if metrics.annual_return > 0.3:
            reasons.append(f"年化收益率高达{metrics.annual_return:.1%}")
        elif metrics.annual_return > 0.15:
            reasons.append(f"年化收益率{metrics.annual_return:.1%}")
        
        # Analyze max drawdown
        # 分析最大回撤
        if metrics.max_drawdown > -0.15:
            reasons.append("回撤控制优秀")
        elif metrics.max_drawdown > -0.25:
            reasons.append("回撤控制良好")
        
        # Analyze win rate
        # 分析胜率
        if metrics.win_rate > 0.6:
            reasons.append(f"胜率{metrics.win_rate:.1%}")
        
        if not reasons:
            reasons.append("综合表现稳定")
        
        return "；".join(reasons)
    
    def _get_default_instruments(self, market: str, asset_type: str) -> str:
        """
        Get default instruments pool for a market and asset type.
        获取市场和资产类型的默认工具池
        
        Args:
            market: Market code
                   市场代码
            asset_type: Asset type code
                       资产类型代码
        
        Returns:
            str: Default instruments pool name
                 默认工具池名称
        """
        # Default mappings
        # 默认映射
        defaults = {
            ("CN", "stock"): "csi300",
            ("CN", "fund"): "all",
            ("CN", "etf"): "all",
            ("US", "stock"): "sp500",
            ("US", "etf"): "all",
            ("HK", "stock"): "hsi"
        }
        
        return defaults.get((market, asset_type), "all")
    
    def _get_instrument_list(self, instruments: str) -> List[str]:
        """
        Get list of instrument codes from instruments pool.
        从工具池获取工具代码列表
        
        Args:
            instruments: Instruments pool name
                        工具池名称
        
        Returns:
            List[str]: List of instrument codes
                      工具代码列表
        """
        try:
            # Get instruments from qlib
            # 从qlib获取工具
            instrument_list = self.qlib_wrapper.get_instruments(market=instruments)
            
            if instrument_list is None:
                self.logger.warning(
                    f"No instruments found for pool: {instruments} / "
                    f"工具池未找到工具: {instruments}"
                )
                return []
            
            return instrument_list
            
        except Exception as e:
            self.logger.error(
                f"Failed to get instrument list: {str(e)} / "
                f"获取工具列表失败: {str(e)}"
            )
            return []
    
    def set_risk_free_rate(self, rate: float) -> None:
        """
        Set the risk-free rate for Sharpe ratio calculation.
        设置用于夏普比率计算的无风险利率
        
        Args:
            rate: Annual risk-free rate (e.g., 0.03 for 3%)
                 年化无风险利率（例如，0.03表示3%）
        """
        if rate < 0 or rate > 0.2:
            self.logger.warning(
                f"Unusual risk-free rate: {rate:.2%} / "
                f"异常的无风险利率: {rate:.2%}"
            )
        
        self.risk_free_rate = rate
        self.logger.info(
            f"Risk-free rate set to {rate:.2%} / "
            f"无风险利率设置为 {rate:.2%}"
        )
