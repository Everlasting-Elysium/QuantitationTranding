"""
Risk Manager for monitoring and controlling trading risks.
风险管理器，用于监控和控制交易风险

This module provides functionality for risk checks, VaR calculation,
drawdown monitoring, concentration risk analysis, and risk alert generation.
本模块提供风险检查、VaR计算、回撤监控、集中度风险分析和风险预警生成功能。
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from src.models.trading_models import Portfolio, Position, Trade
from src.infrastructure.logger_system import LoggerSystem


class RiskManager:
    """
    Risk Manager for monitoring and controlling trading risks.
    风险管理器
    
    This class handles position risk checks, VaR calculation, max drawdown monitoring,
    concentration risk checks, and risk alert generation.
    该类处理持仓风险检查、VaR计算、最大回撤监控、集中度风险检查和风险预警生成。
    """
    
    def __init__(
        self,
        max_position_pct: float = 0.3,
        max_sector_pct: float = 0.4,
        max_drawdown_pct: float = 0.2,
        max_daily_loss_pct: float = 0.05,
        var_confidence: float = 0.95,
        logger: Optional[LoggerSystem] = None
    ):
        """
        Initialize Risk Manager.
        初始化风险管理器
        
        Args:
            max_position_pct: Maximum position size as percentage / 最大持仓比例
            max_sector_pct: Maximum sector exposure / 最大行业暴露
            max_drawdown_pct: Maximum drawdown threshold / 最大回撤阈值
            max_daily_loss_pct: Maximum daily loss percentage / 最大日亏损百分比
            var_confidence: VaR confidence level / VaR置信水平
            logger: Logger system instance / 日志系统实例
        """
        self.max_position_pct = max_position_pct
        self.max_sector_pct = max_sector_pct
        self.max_drawdown_pct = max_drawdown_pct
        self.max_daily_loss_pct = max_daily_loss_pct
        self.var_confidence = var_confidence
        self.logger = logger.get_logger(__name__) if logger else None
        
        # Track portfolio history for drawdown calculation
        self._portfolio_history: Dict[str, List[Tuple[str, float]]] = {}
        
        if self.logger:
            self.logger.info(
                f"RiskManager initialized with thresholds: "
                f"max_position={max_position_pct}, max_sector={max_sector_pct}, "
                f"max_drawdown={max_drawdown_pct}, max_daily_loss={max_daily_loss_pct} / "
                f"风险管理器已初始化，阈值：最大持仓={max_position_pct}，最大行业={max_sector_pct}，"
                f"最大回撤={max_drawdown_pct}，最大日亏损={max_daily_loss_pct}"
            )
    
    def check_position_risk(
        self,
        portfolio: Portfolio,
        new_trade: Trade,
        sector_map: Optional[Dict[str, str]] = None
    ) -> Dict:
        """
        Check if a new trade would violate risk limits.
        检查新交易是否会违反风险限制
        
        Args:
            portfolio: Current portfolio / 当前投资组合
            new_trade: Proposed trade / 拟议交易
            sector_map: Mapping of symbols to sectors / 股票代码到行业的映射
            
        Returns:
            Risk check result dictionary / 风险检查结果字典
        """
        warnings = []
        violations = []
        suggested_adjustments = {}
        
        # Simulate the trade
        simulated_portfolio = self._simulate_trade(portfolio, new_trade)
        
        # Ensure total value is updated
        simulated_portfolio.update_total_value()
        
        # Check position size limit
        if new_trade.symbol in simulated_portfolio.positions:
            pos = simulated_portfolio.positions[new_trade.symbol]
            position_pct = pos.market_value / simulated_portfolio.total_value if simulated_portfolio.total_value > 0 else 0
            
            if position_pct > self.max_position_pct:
                violations.append(
                    f"Position size {position_pct:.1%} exceeds limit {self.max_position_pct:.1%} / "
                    f"持仓比例 {position_pct:.1%} 超过限制 {self.max_position_pct:.1%}"
                )
                # Suggest reduced quantity
                max_value = simulated_portfolio.total_value * self.max_position_pct
                max_quantity = max_value / new_trade.price
                suggested_adjustments['max_quantity'] = max_quantity
            elif position_pct > self.max_position_pct * 0.8:
                warnings.append(
                    f"Position size {position_pct:.1%} approaching limit {self.max_position_pct:.1%} / "
                    f"持仓比例 {position_pct:.1%} 接近限制 {self.max_position_pct:.1%}"
                )
        
        # Check sector concentration if sector_map provided
        if sector_map:
            concentration = self.check_concentration_risk(simulated_portfolio, sector_map)
            if concentration['risk_level'] == 'high':
                violations.append(
                    f"High sector concentration detected / 检测到高行业集中度"
                )
                for sector, pct in concentration['sector_concentration'].items():
                    if pct > self.max_sector_pct:
                        violations.append(
                            f"Sector {sector} exposure {pct:.1%} exceeds limit {self.max_sector_pct:.1%} / "
                            f"行业 {sector} 暴露 {pct:.1%} 超过限制 {self.max_sector_pct:.1%}"
                        )
        
        # Calculate risk score
        risk_score = len(violations) * 1.0 + len(warnings) * 0.5
        passed = len(violations) == 0
        
        result = {
            'passed': passed,
            'risk_score': risk_score,
            'warnings': warnings,
            'violations': violations,
            'suggested_adjustments': suggested_adjustments
        }
        
        if self.logger:
            if not passed:
                self.logger.warning(
                    f"Risk check failed for trade {new_trade.trade_id}: {violations} / "
                    f"交易 {new_trade.trade_id} 风险检查失败：{violations}"
                )
            elif warnings:
                self.logger.info(
                    f"Risk check passed with warnings for trade {new_trade.trade_id}: {warnings} / "
                    f"交易 {new_trade.trade_id} 风险检查通过但有警告：{warnings}"
                )
        
        return result
    
    def _simulate_trade(self, portfolio: Portfolio, trade: Trade) -> Portfolio:
        """
        Simulate a trade on a copy of the portfolio.
        在投资组合副本上模拟交易
        
        Args:
            portfolio: Original portfolio / 原始投资组合
            trade: Trade to simulate / 要模拟的交易
            
        Returns:
            Simulated portfolio / 模拟的投资组合
        """
        # Create a deep copy of portfolio
        import copy
        sim_portfolio = copy.deepcopy(portfolio)
        
        # Apply the trade
        if trade.action == 'buy':
            trade_cost = trade.total_cost
            if sim_portfolio.cash >= trade_cost:
                sim_portfolio.cash -= trade_cost
                
                if trade.symbol in sim_portfolio.positions:
                    pos = sim_portfolio.positions[trade.symbol]
                    total_cost = pos.quantity * pos.avg_cost + trade_cost
                    new_quantity = pos.quantity + trade.quantity
                    pos.quantity = new_quantity
                    pos.avg_cost = total_cost / new_quantity
                    pos.current_price = trade.price
                else:
                    sim_portfolio.positions[trade.symbol] = Position(
                        symbol=trade.symbol,
                        quantity=trade.quantity,
                        avg_cost=trade.price + (trade.commission / trade.quantity),
                        current_price=trade.price
                    )
                # Update position after creation/modification
                sim_portfolio.positions[trade.symbol].__post_init__()
        
        elif trade.action == 'sell':
            if trade.symbol in sim_portfolio.positions:
                pos = sim_portfolio.positions[trade.symbol]
                if pos.quantity >= trade.quantity:
                    pos.quantity -= trade.quantity
                    proceeds = trade.quantity * trade.price - trade.commission
                    sim_portfolio.cash += proceeds
                    
                    if pos.quantity == 0:
                        del sim_portfolio.positions[trade.symbol]
                    else:
                        pos.current_price = trade.price
                        pos.__post_init__()
        
        sim_portfolio.update_total_value()
        return sim_portfolio
    
    def calculate_var(
        self,
        returns: pd.Series,
        portfolio_value: float,
        confidence: Optional[float] = None
    ) -> float:
        """
        Calculate Value at Risk (VaR) using historical simulation.
        使用历史模拟法计算风险价值（VaR）
        
        Args:
            returns: Historical returns series / 历史收益率序列
            portfolio_value: Current portfolio value / 当前投资组合价值
            confidence: Confidence level (default: self.var_confidence) / 置信水平
            
        Returns:
            VaR value in currency units / 货币单位的VaR值
        """
        if confidence is None:
            confidence = self.var_confidence
        
        if len(returns) < 2:
            if self.logger:
                self.logger.warning(
                    "Insufficient data for VaR calculation / VaR计算数据不足"
                )
            return 0.0
        
        # Calculate percentile
        percentile = (1 - confidence) * 100
        var_return = np.percentile(returns, percentile)
        var_value = abs(var_return * portfolio_value)
        
        if self.logger:
            self.logger.debug(
                f"Calculated VaR at {confidence:.1%} confidence: {var_value:.2f} / "
                f"计算 {confidence:.1%} 置信度的VaR：{var_value:.2f}"
            )
        
        return var_value
    
    def calculate_max_drawdown(self, returns: pd.Series) -> float:
        """
        Calculate maximum drawdown from returns series.
        从收益率序列计算最大回撤
        
        Args:
            returns: Returns series / 收益率序列
            
        Returns:
            Maximum drawdown as percentage / 最大回撤百分比
        """
        if len(returns) < 2:
            return 0.0
        
        # Calculate cumulative returns
        cumulative = (1 + returns).cumprod()
        
        # Calculate running maximum
        running_max = cumulative.expanding().max()
        
        # Calculate drawdown
        drawdown = (cumulative - running_max) / running_max
        
        # Get maximum drawdown
        max_dd = abs(drawdown.min())
        
        if self.logger:
            self.logger.debug(
                f"Calculated maximum drawdown: {max_dd:.2%} / "
                f"计算最大回撤：{max_dd:.2%}"
            )
        
        return max_dd
    
    def check_concentration_risk(
        self,
        portfolio: Portfolio,
        sector_map: Dict[str, str]
    ) -> Dict:
        """
        Check concentration risk in portfolio.
        检查投资组合的集中度风险
        
        Args:
            portfolio: Portfolio to check / 要检查的投资组合
            sector_map: Mapping of symbols to sectors / 股票代码到行业的映射
            
        Returns:
            Concentration risk analysis / 集中度风险分析
        """
        if not portfolio.positions:
            return {
                'max_position_pct': 0.0,
                'top_5_concentration': 0.0,
                'sector_concentration': {},
                'risk_level': 'low'
            }
        
        portfolio.update_total_value()
        
        # Calculate position percentages
        position_pcts = {}
        for symbol, pos in portfolio.positions.items():
            position_pcts[symbol] = (pos.market_value / portfolio.total_value) * 100
        
        # Get max position
        max_position_pct = max(position_pcts.values()) if position_pcts else 0.0
        
        # Get top 5 concentration
        sorted_pcts = sorted(position_pcts.values(), reverse=True)
        top_5_concentration = sum(sorted_pcts[:5])
        
        # Calculate sector concentration
        sector_values = {}
        for symbol, pos in portfolio.positions.items():
            sector = sector_map.get(symbol, 'Unknown')
            if sector not in sector_values:
                sector_values[sector] = 0.0
            sector_values[sector] += pos.market_value
        
        sector_concentration = {
            sector: (value / portfolio.total_value) * 100
            for sector, value in sector_values.items()
        }
        
        # Determine risk level
        risk_level = 'low'
        if max_position_pct > self.max_position_pct * 100:
            risk_level = 'high'
        elif any(pct > self.max_sector_pct * 100 for pct in sector_concentration.values()):
            risk_level = 'high'
        elif max_position_pct > self.max_position_pct * 80 or top_5_concentration > 70:
            risk_level = 'medium'
        
        result = {
            'max_position_pct': max_position_pct,
            'top_5_concentration': top_5_concentration,
            'sector_concentration': sector_concentration,
            'risk_level': risk_level
        }
        
        if self.logger:
            self.logger.debug(
                f"Concentration risk: max_position={max_position_pct:.1f}%, "
                f"top_5={top_5_concentration:.1f}%, risk_level={risk_level} / "
                f"集中度风险：最大持仓={max_position_pct:.1f}%，前5={top_5_concentration:.1f}%，"
                f"风险等级={risk_level}"
            )
        
        return result
    
    def generate_risk_alert(
        self,
        portfolio: Portfolio,
        returns: pd.Series,
        sector_map: Optional[Dict[str, str]] = None
    ) -> Optional[Dict]:
        """
        Generate risk alert if thresholds are exceeded.
        如果超过阈值则生成风险预警
        
        Args:
            portfolio: Current portfolio / 当前投资组合
            returns: Historical returns / 历史收益率
            sector_map: Mapping of symbols to sectors / 股票代码到行业的映射
            
        Returns:
            Risk alert dictionary or None / 风险预警字典或None
        """
        alerts = []
        severity = 'info'
        affected_positions = []
        recommended_actions = []
        
        # Check drawdown
        if len(returns) >= 2:
            max_dd = self.calculate_max_drawdown(returns)
            if max_dd > self.max_drawdown_pct:
                alerts.append(
                    f"Maximum drawdown {max_dd:.2%} exceeds threshold {self.max_drawdown_pct:.2%} / "
                    f"最大回撤 {max_dd:.2%} 超过阈值 {self.max_drawdown_pct:.2%}"
                )
                severity = 'critical'
                recommended_actions.append(
                    "Consider reducing position sizes / 考虑减少持仓规模"
                )
            elif max_dd > self.max_drawdown_pct * 0.8:
                alerts.append(
                    f"Maximum drawdown {max_dd:.2%} approaching threshold / "
                    f"最大回撤 {max_dd:.2%} 接近阈值"
                )
                severity = 'warning' if severity == 'info' else severity
        
        # Check daily loss
        if len(returns) > 0:
            latest_return = returns.iloc[-1]
            if latest_return < -self.max_daily_loss_pct:
                alerts.append(
                    f"Daily loss {latest_return:.2%} exceeds threshold {-self.max_daily_loss_pct:.2%} / "
                    f"日亏损 {latest_return:.2%} 超过阈值 {-self.max_daily_loss_pct:.2%}"
                )
                severity = 'critical'
                recommended_actions.append(
                    "Review positions and consider stop-loss / 审查持仓并考虑止损"
                )
        
        # Check concentration risk
        if sector_map:
            concentration = self.check_concentration_risk(portfolio, sector_map)
            if concentration['risk_level'] == 'high':
                alerts.append(
                    f"High concentration risk detected / 检测到高集中度风险"
                )
                severity = 'warning' if severity == 'info' else severity
                
                # Identify concentrated positions
                for symbol, pos in portfolio.positions.items():
                    pos_pct = (pos.market_value / portfolio.total_value) * 100
                    if pos_pct > self.max_position_pct * 100:
                        affected_positions.append(symbol)
                
                recommended_actions.append(
                    "Diversify portfolio to reduce concentration / 分散投资组合以降低集中度"
                )
        
        # Check individual position losses
        for symbol, pos in portfolio.positions.items():
            if pos.unrealized_pnl_pct < -10:  # More than 10% loss
                alerts.append(
                    f"Position {symbol} has unrealized loss of {pos.unrealized_pnl_pct:.2%} / "
                    f"持仓 {symbol} 未实现亏损 {pos.unrealized_pnl_pct:.2%}"
                )
                affected_positions.append(symbol)
                severity = 'warning' if severity == 'info' else severity
                
                if pos.unrealized_pnl_pct < -20:  # More than 20% loss
                    severity = 'critical'
                    recommended_actions.append(
                        f"Consider stop-loss for {symbol} / 考虑对 {symbol} 止损"
                    )
        
        # If no alerts, return None
        if not alerts:
            return None
        
        # Generate alert
        alert = {
            'alert_id': f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'timestamp': datetime.now().isoformat(),
            'severity': severity,
            'alert_type': 'risk_threshold',
            'message': '; '.join(alerts),
            'current_value': portfolio.total_value,
            'threshold_value': portfolio.initial_capital * (1 - self.max_drawdown_pct),
            'affected_positions': affected_positions,
            'recommended_actions': recommended_actions
        }
        
        if self.logger:
            self.logger.warning(
                f"Risk alert generated: {severity} - {alert['message']} / "
                f"生成风险预警：{severity} - {alert['message']}"
            )
        
        return alert
    
    def suggest_risk_mitigation(self, alert: Dict) -> List[str]:
        """
        Suggest risk mitigation actions based on alert.
        根据预警建议风险缓解措施
        
        Args:
            alert: Risk alert dictionary / 风险预警字典
            
        Returns:
            List of suggested actions / 建议措施列表
        """
        suggestions = []
        
        if alert['severity'] == 'critical':
            suggestions.append(
                "Immediate action required: Review and adjust portfolio / "
                "需要立即采取行动：审查并调整投资组合"
            )
        
        if 'drawdown' in alert['message'].lower():
            suggestions.extend([
                "Reduce overall position sizes / 减少整体持仓规模",
                "Increase cash reserves / 增加现金储备",
                "Review stop-loss levels / 审查止损水平"
            ])
        
        if 'concentration' in alert['message'].lower():
            suggestions.extend([
                "Rebalance portfolio to reduce concentration / 重新平衡投资组合以降低集中度",
                "Consider adding positions in different sectors / 考虑增加不同行业的持仓"
            ])
        
        if alert['affected_positions']:
            suggestions.append(
                f"Review positions: {', '.join(alert['affected_positions'])} / "
                f"审查持仓：{', '.join(alert['affected_positions'])}"
            )
        
        # Add any recommended actions from the alert
        suggestions.extend(alert.get('recommended_actions', []))
        
        return list(set(suggestions))  # Remove duplicates
    
    def track_portfolio_value(self, portfolio_id: str, value: float, timestamp: Optional[str] = None):
        """
        Track portfolio value for drawdown calculation.
        跟踪投资组合价值以计算回撤
        
        Args:
            portfolio_id: Portfolio identifier / 投资组合标识符
            value: Portfolio value / 投资组合价值
            timestamp: Timestamp (ISO format), defaults to now / 时间戳（ISO格式），默认为当前时间
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        if portfolio_id not in self._portfolio_history:
            self._portfolio_history[portfolio_id] = []
        
        self._portfolio_history[portfolio_id].append((timestamp, value))
        
        # Keep only recent history (e.g., last 1000 records)
        if len(self._portfolio_history[portfolio_id]) > 1000:
            self._portfolio_history[portfolio_id] = self._portfolio_history[portfolio_id][-1000:]
    
    def get_portfolio_drawdown(self, portfolio_id: str) -> float:
        """
        Get current drawdown for a portfolio.
        获取投资组合的当前回撤
        
        Args:
            portfolio_id: Portfolio identifier / 投资组合标识符
            
        Returns:
            Current drawdown as percentage / 当前回撤百分比
        """
        if portfolio_id not in self._portfolio_history:
            return 0.0
        
        history = self._portfolio_history[portfolio_id]
        if len(history) < 2:
            return 0.0
        
        # Extract values
        values = [v for _, v in history]
        
        # Calculate current drawdown
        peak = max(values)
        current = values[-1]
        drawdown = (current - peak) / peak if peak > 0 else 0.0
        
        return abs(drawdown)
    
    def reset_portfolio_history(self, portfolio_id: str):
        """
        Reset portfolio history for a given portfolio.
        重置给定投资组合的历史记录
        
        Args:
            portfolio_id: Portfolio identifier / 投资组合标识符
        """
        if portfolio_id in self._portfolio_history:
            del self._portfolio_history[portfolio_id]
            
            if self.logger:
                self.logger.info(
                    f"Reset portfolio history for {portfolio_id} / "
                    f"重置投资组合 {portfolio_id} 的历史记录"
                )
