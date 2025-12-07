"""
Live Trading Manager for managing live trading sessions.
实盘交易管理器，用于管理实盘交易会话

This module provides functionality for live trading session management,
order execution, position monitoring, and risk control integration.
本模块提供实盘交易会话管理、订单执行、持仓监控和风险控制集成功能。
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd

from src.models.trading_models import (
    TradingSession,
    LiveTradingConfig,
    TradeResult,
    TradingStatus,
    Signal,
    Portfolio
)
from src.core.portfolio_manager import PortfolioManager
from src.core.risk_manager import RiskManager
from src.infrastructure.trading_api_adapter import TradingAPIAdapter
from src.infrastructure.logger_system import LoggerSystem


class LiveTradingManager:
    """
    Live Trading Manager for managing live trading sessions.
    实盘交易管理器
    
    This class handles live trading session management, order execution,
    position monitoring, risk checks, and trading pause/resume.
    该类处理实盘交易会话管理、订单执行、持仓监控、风险检查和交易暂停/恢复。
    
    Responsibilities / 职责:
    - Manage trading sessions / 管理交易会话
    - Execute orders through broker API / 通过券商API执行订单
    - Monitor positions in real-time / 实时监控持仓
    - Integrate risk checks before execution / 执行前集成风险检查
    - Handle trading pause and resume / 处理交易暂停和恢复
    """
    
    def __init__(
        self,
        portfolio_manager: PortfolioManager,
        risk_manager: RiskManager,
        trading_api: TradingAPIAdapter,
        logger: Optional[LoggerSystem] = None
    ):
        """
        Initialize Live Trading Manager.
        初始化实盘交易管理器
        
        Args:
            portfolio_manager: Portfolio manager instance / 投资组合管理器实例
            risk_manager: Risk manager instance / 风险管理器实例
            trading_api: Trading API adapter instance / 交易API适配器实例
            logger: Logger system instance / 日志系统实例
        """
        self.portfolio_manager = portfolio_manager
        self.risk_manager = risk_manager
        self.trading_api = trading_api
        self.logger = logger.get_logger(__name__) if logger else None
        
        # Store active trading sessions
        self._sessions: Dict[str, TradingSession] = {}
        
        # Store session portfolios
        self._session_portfolios: Dict[str, str] = {}  # session_id -> portfolio_id
        
        if self.logger:
            self.logger.info(
                "LiveTradingManager initialized / 实盘交易管理器已初始化"
            )
    
    def start_live_trading(
        self,
        model_id: str,
        initial_capital: float,
        trading_config: LiveTradingConfig
    ) -> TradingSession:
        """
        Start a new live trading session.
        启动新的实盘交易会话
        
        Args:
            model_id: Model identifier to use for trading / 用于交易的模型标识符
            initial_capital: Initial capital for trading / 交易初始资金
            trading_config: Live trading configuration / 实盘交易配置
            
        Returns:
            TradingSession: Created trading session / 创建的交易会话
            
        Raises:
            ValueError: If parameters are invalid / 如果参数无效
            RuntimeError: If broker connection fails / 如果券商连接失败
        """
        if initial_capital <= 0:
            raise ValueError(
                f"Initial capital must be positive, got {initial_capital} / "
                f"初始资金必须为正数，收到 {initial_capital}"
            )
        
        try:
            # Connect to broker if not already connected
            if not self.trading_api.is_connected():
                self.logger.info(
                    f"Connecting to broker: {trading_config.broker} / "
                    f"连接券商：{trading_config.broker}"
                )
                self.trading_api.connect(
                    broker=trading_config.broker,
                    credentials=trading_config.credentials
                )
            
            # Create portfolio for this session
            session_id = f"live_{uuid.uuid4().hex[:8]}"
            portfolio = self.portfolio_manager.create_portfolio(
                initial_capital=initial_capital,
                portfolio_id=f"portfolio_{session_id}"
            )
            
            # Create trading session
            session = TradingSession(
                session_id=session_id,
                model_id=model_id,
                start_date=datetime.now().strftime("%Y-%m-%d"),
                initial_capital=initial_capital,
                current_capital=initial_capital,
                status="active",
                portfolio=portfolio,
                total_return=0.0,
                config=trading_config
            )
            
            # Store session
            self._sessions[session_id] = session
            self._session_portfolios[session_id] = portfolio.portfolio_id
            
            if self.logger:
                self.logger.info(
                    f"Started live trading session {session_id} with model {model_id}, "
                    f"initial capital: {initial_capital} / "
                    f"启动实盘交易会话 {session_id}，模型 {model_id}，初始资金：{initial_capital}"
                )
            
            return session
            
        except Exception as e:
            if self.logger:
                self.logger.error(
                    f"Failed to start live trading: {str(e)} / "
                    f"启动实盘交易失败：{str(e)}",
                    exc_info=True
                )
            raise RuntimeError(f"Failed to start live trading: {str(e)}") from e

    
    def execute_trade(
        self,
        session_id: str,
        signal: Signal
    ) -> TradeResult:
        """
        Execute a trade based on signal with risk checks.
        根据信号执行交易并进行风险检查
        
        Args:
            session_id: Trading session identifier / 交易会话标识符
            signal: Trading signal to execute / 要执行的交易信号
            
        Returns:
            TradeResult: Trade execution result / 交易执行结果
            
        Raises:
            ValueError: If session not found or signal invalid / 如果未找到会话或信号无效
            RuntimeError: If trade execution fails / 如果交易执行失败
        """
        # Get session
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError(
                f"Trading session {session_id} not found / "
                f"未找到交易会话 {session_id}"
            )
        
        # Check if session is active
        if session.status != "active":
            raise ValueError(
                f"Trading session {session_id} is not active (status: {session.status}) / "
                f"交易会话 {session_id} 未激活（状态：{session.status}）"
            )
        
        # Validate signal
        if signal.action not in ["buy", "sell", "hold"]:
            raise ValueError(
                f"Invalid signal action: {signal.action} / "
                f"无效的信号动作：{signal.action}"
            )
        
        # Skip hold signals
        if signal.action == "hold":
            if self.logger:
                self.logger.debug(
                    f"Skipping hold signal for {signal.stock_code} / "
                    f"跳过 {signal.stock_code} 的持有信号"
                )
            return TradeResult(
                trade_id=f"trade_{uuid.uuid4().hex[:8]}",
                order_id="N/A",
                symbol=signal.stock_code,
                action="hold",
                quantity=0.0,
                price=0.0,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                status="skipped",
                commission=0.0,
                message="Hold signal skipped / 持有信号已跳过"
            )
        
        try:
            # Get portfolio
            portfolio_id = self._session_portfolios[session_id]
            portfolio = self.portfolio_manager.get_portfolio(portfolio_id)
            
            if portfolio is None:
                raise RuntimeError(
                    f"Portfolio not found for session {session_id} / "
                    f"未找到会话 {session_id} 的投资组合"
                )
            
            # Determine trade quantity based on signal and config
            quantity = self._calculate_trade_quantity(
                session=session,
                portfolio=portfolio,
                signal=signal
            )
            
            if quantity <= 0:
                if self.logger:
                    self.logger.warning(
                        f"Calculated quantity is {quantity}, skipping trade / "
                        f"计算的数量为 {quantity}，跳过交易"
                    )
                return TradeResult(
                    trade_id=f"trade_{uuid.uuid4().hex[:8]}",
                    order_id="N/A",
                    symbol=signal.stock_code,
                    action=signal.action,
                    quantity=0.0,
                    price=0.0,
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    status="skipped",
                    commission=0.0,
                    message="Quantity too small / 数量太小"
                )
            
            # Create a simulated trade for risk check
            from src.models.trading_models import Trade
            simulated_trade = Trade(
                trade_id=f"sim_{uuid.uuid4().hex[:8]}",
                timestamp=datetime.now().isoformat(),
                symbol=signal.stock_code,
                action=signal.action,
                quantity=quantity,
                price=signal.score * 100,  # Simplified price estimation
                commission=quantity * signal.score * 100 * 0.0003  # 0.03% commission
            )
            
            # Perform risk check
            risk_check = self.risk_manager.check_position_risk(
                portfolio=portfolio,
                new_trade=simulated_trade
            )
            
            if not risk_check['passed']:
                if self.logger:
                    self.logger.warning(
                        f"Risk check failed for {signal.stock_code}: {risk_check['violations']} / "
                        f"{signal.stock_code} 风险检查失败：{risk_check['violations']}"
                    )
                
                # Adjust quantity if suggested
                if 'max_quantity' in risk_check['suggested_adjustments']:
                    adjusted_quantity = risk_check['suggested_adjustments']['max_quantity']
                    if self.logger:
                        self.logger.info(
                            f"Adjusting quantity from {quantity} to {adjusted_quantity} / "
                            f"将数量从 {quantity} 调整为 {adjusted_quantity}"
                        )
                    quantity = adjusted_quantity
                else:
                    # Risk check failed and no adjustment possible
                    return TradeResult(
                        trade_id=f"trade_{uuid.uuid4().hex[:8]}",
                        order_id="N/A",
                        symbol=signal.stock_code,
                        action=signal.action,
                        quantity=0.0,
                        price=0.0,
                        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        status="rejected",
                        commission=0.0,
                        message=f"Risk check failed: {'; '.join(risk_check['violations'])}"
                    )
            
            # Execute order through broker API
            if self.logger:
                self.logger.info(
                    f"Executing {signal.action} order for {signal.stock_code}, "
                    f"quantity: {quantity} / "
                    f"执行 {signal.action} 订单，股票：{signal.stock_code}，数量：{quantity}"
                )
            
            order_result = self.trading_api.place_order(
                symbol=signal.stock_code,
                quantity=quantity,
                order_type="market",  # Use market orders for simplicity
                action=signal.action
            )
            
            # Update portfolio with executed trade
            if order_result.status == "filled":
                self.portfolio_manager.update_position(
                    portfolio_id=portfolio_id,
                    symbol=signal.stock_code,
                    quantity=order_result.filled_quantity,
                    price=order_result.avg_fill_price,
                    action=signal.action,
                    commission=order_result.avg_fill_price * order_result.filled_quantity * 0.0003
                )
                
                # Update session
                portfolio = self.portfolio_manager.get_portfolio(portfolio_id)
                session.portfolio = portfolio
                session.current_capital = portfolio.total_value
                session.total_return = (
                    (portfolio.total_value - session.initial_capital) / 
                    session.initial_capital * 100
                )
            
            # Create trade result
            trade_result = TradeResult(
                trade_id=f"trade_{uuid.uuid4().hex[:8]}",
                order_id=order_result.order_id,
                symbol=signal.stock_code,
                action=signal.action,
                quantity=order_result.filled_quantity,
                price=order_result.avg_fill_price,
                timestamp=order_result.timestamp,
                status=order_result.status,
                commission=order_result.avg_fill_price * order_result.filled_quantity * 0.0003,
                message=order_result.message if hasattr(order_result, 'message') else "Trade executed"
            )
            
            if self.logger:
                self.logger.info(
                    f"Trade executed: {trade_result.trade_id}, {signal.action} "
                    f"{signal.stock_code} x {trade_result.quantity} @ {trade_result.price} / "
                    f"交易已执行：{trade_result.trade_id}，{signal.action} "
                    f"{signal.stock_code} x {trade_result.quantity} @ {trade_result.price}"
                )
            
            return trade_result
            
        except Exception as e:
            if self.logger:
                self.logger.error(
                    f"Failed to execute trade for {signal.stock_code}: {str(e)} / "
                    f"执行 {signal.stock_code} 交易失败：{str(e)}",
                    exc_info=True
                )
            raise RuntimeError(f"Failed to execute trade: {str(e)}") from e
    
    def _calculate_trade_quantity(
        self,
        session: TradingSession,
        portfolio: Portfolio,
        signal: Signal
    ) -> float:
        """
        Calculate trade quantity based on signal and configuration.
        根据信号和配置计算交易数量
        
        Args:
            session: Trading session / 交易会话
            portfolio: Current portfolio / 当前投资组合
            signal: Trading signal / 交易信号
            
        Returns:
            float: Trade quantity / 交易数量
        """
        config = session.config
        
        if signal.action == "buy":
            # Calculate maximum position size
            max_position_value = portfolio.total_value * config.max_position_size
            
            # Estimate price (in real implementation, would query market data)
            estimated_price = signal.score * 100  # Simplified
            
            # Calculate quantity
            quantity = max_position_value / estimated_price
            
            # Round down to nearest 100 shares (standard lot size)
            quantity = int(quantity / 100) * 100
            
            return quantity
            
        elif signal.action == "sell":
            # Sell all shares of this position
            if signal.stock_code in portfolio.positions:
                return portfolio.positions[signal.stock_code].quantity
            else:
                return 0.0
        
        return 0.0

    
    def get_current_positions(self, session_id: str) -> Portfolio:
        """
        Get current positions for a trading session.
        获取交易会话的当前持仓
        
        Args:
            session_id: Trading session identifier / 交易会话标识符
            
        Returns:
            Portfolio: Current portfolio / 当前投资组合
            
        Raises:
            ValueError: If session not found / 如果未找到会话
        """
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError(
                f"Trading session {session_id} not found / "
                f"未找到交易会话 {session_id}"
            )
        
        # Get latest portfolio state
        portfolio_id = self._session_portfolios[session_id]
        portfolio = self.portfolio_manager.get_portfolio(portfolio_id)
        
        if portfolio is None:
            raise ValueError(
                f"Portfolio not found for session {session_id} / "
                f"未找到会话 {session_id} 的投资组合"
            )
        
        # Update portfolio with latest prices from broker
        try:
            broker_positions = self.trading_api.get_positions()
            
            # Update prices
            price_updates = {}
            for pos in broker_positions:
                price_updates[pos.symbol] = pos.current_price
            
            if price_updates:
                self.portfolio_manager.update_prices(portfolio_id, price_updates)
                portfolio = self.portfolio_manager.get_portfolio(portfolio_id)
        except Exception as e:
            if self.logger:
                self.logger.warning(
                    f"Failed to update prices from broker: {str(e)} / "
                    f"从券商更新价格失败：{str(e)}"
                )
        
        return portfolio
    
    def stop_trading(self, session_id: str) -> Dict[str, Any]:
        """
        Stop a trading session and generate summary.
        停止交易会话并生成摘要
        
        Args:
            session_id: Trading session identifier / 交易会话标识符
            
        Returns:
            Dict: Trading session summary / 交易会话摘要
            
        Raises:
            ValueError: If session not found / 如果未找到会话
        """
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError(
                f"Trading session {session_id} not found / "
                f"未找到交易会话 {session_id}"
            )
        
        # Update session status
        session.status = "stopped"
        
        # Get final portfolio state
        portfolio_id = self._session_portfolios[session_id]
        portfolio = self.portfolio_manager.get_portfolio(portfolio_id)
        
        # Get trade history
        trade_history = self.portfolio_manager.get_trade_history(portfolio_id)
        
        # Calculate summary statistics
        summary = {
            'session_id': session_id,
            'model_id': session.model_id,
            'start_date': session.start_date,
            'end_date': datetime.now().strftime("%Y-%m-%d"),
            'initial_capital': session.initial_capital,
            'final_capital': portfolio.total_value,
            'total_return': session.total_return,
            'total_return_pct': (
                (portfolio.total_value - session.initial_capital) / 
                session.initial_capital * 100
            ),
            'num_trades': len(trade_history),
            'num_positions': len(portfolio.positions),
            'cash_balance': portfolio.cash,
            'positions_value': sum(pos.market_value for pos in portfolio.positions.values()),
            'status': session.status
        }
        
        if self.logger:
            self.logger.info(
                f"Stopped trading session {session_id}, "
                f"final return: {summary['total_return_pct']:.2f}% / "
                f"停止交易会话 {session_id}，最终收益：{summary['total_return_pct']:.2f}%"
            )
        
        return summary
    
    def pause_trading(self, session_id: str) -> None:
        """
        Pause a trading session.
        暂停交易会话
        
        Args:
            session_id: Trading session identifier / 交易会话标识符
            
        Raises:
            ValueError: If session not found or not active / 如果未找到会话或未激活
        """
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError(
                f"Trading session {session_id} not found / "
                f"未找到交易会话 {session_id}"
            )
        
        if session.status != "active":
            raise ValueError(
                f"Cannot pause session {session_id} with status {session.status} / "
                f"无法暂停状态为 {session.status} 的会话 {session_id}"
            )
        
        session.status = "paused"
        
        if self.logger:
            self.logger.info(
                f"Paused trading session {session_id} / "
                f"暂停交易会话 {session_id}"
            )
    
    def resume_trading(self, session_id: str) -> None:
        """
        Resume a paused trading session.
        恢复暂停的交易会话
        
        Args:
            session_id: Trading session identifier / 交易会话标识符
            
        Raises:
            ValueError: If session not found or not paused / 如果未找到会话或未暂停
        """
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError(
                f"Trading session {session_id} not found / "
                f"未找到交易会话 {session_id}"
            )
        
        if session.status != "paused":
            raise ValueError(
                f"Cannot resume session {session_id} with status {session.status} / "
                f"无法恢复状态为 {session.status} 的会话 {session_id}"
            )
        
        session.status = "active"
        
        if self.logger:
            self.logger.info(
                f"Resumed trading session {session_id} / "
                f"恢复交易会话 {session_id}"
            )
    
    def get_trading_status(self, session_id: str) -> TradingStatus:
        """
        Get current trading status for a session.
        获取会话的当前交易状态
        
        Args:
            session_id: Trading session identifier / 交易会话标识符
            
        Returns:
            TradingStatus: Current trading status / 当前交易状态
            
        Raises:
            ValueError: If session not found / 如果未找到会话
        """
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError(
                f"Trading session {session_id} not found / "
                f"未找到交易会话 {session_id}"
            )
        
        # Get current portfolio
        portfolio_id = self._session_portfolios[session_id]
        portfolio = self.portfolio_manager.get_portfolio(portfolio_id)
        
        if portfolio is None:
            raise ValueError(
                f"Portfolio not found for session {session_id} / "
                f"未找到会话 {session_id} 的投资组合"
            )
        
        # Calculate today's return (simplified - would need historical data)
        today_return = 0.0  # Placeholder
        
        status = TradingStatus(
            session_id=session_id,
            is_active=(session.status == "active"),
            current_value=portfolio.total_value,
            total_return=(
                (portfolio.total_value - session.initial_capital) / 
                session.initial_capital * 100
            ),
            today_return=today_return,
            positions_count=len(portfolio.positions),
            cash_balance=portfolio.cash,
            last_update=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        return status
    
    def get_session(self, session_id: str) -> Optional[TradingSession]:
        """
        Get trading session by ID.
        根据ID获取交易会话
        
        Args:
            session_id: Trading session identifier / 交易会话标识符
            
        Returns:
            Optional[TradingSession]: Trading session or None / 交易会话或None
        """
        return self._sessions.get(session_id)
    
    def list_sessions(self) -> List[TradingSession]:
        """
        List all trading sessions.
        列出所有交易会话
        
        Returns:
            List[TradingSession]: List of trading sessions / 交易会话列表
        """
        return list(self._sessions.values())
    
    def check_risk_alerts(self, session_id: str) -> Optional[Dict]:
        """
        Check for risk alerts in a trading session.
        检查交易会话中的风险预警
        
        Args:
            session_id: Trading session identifier / 交易会话标识符
            
        Returns:
            Optional[Dict]: Risk alert if any, None otherwise / 风险预警（如有），否则为None
            
        Raises:
            ValueError: If session not found / 如果未找到会话
        """
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError(
                f"Trading session {session_id} not found / "
                f"未找到交易会话 {session_id}"
            )
        
        # Get portfolio
        portfolio_id = self._session_portfolios[session_id]
        portfolio = self.portfolio_manager.get_portfolio(portfolio_id)
        
        if portfolio is None:
            raise ValueError(
                f"Portfolio not found for session {session_id} / "
                f"未找到会话 {session_id} 的投资组合"
            )
        
        # Calculate returns (simplified)
        returns = self.portfolio_manager.calculate_returns(portfolio_id)
        
        # Generate risk alert
        alert = self.risk_manager.generate_risk_alert(
            portfolio=portfolio,
            returns=returns
        )
        
        # If alert generated, pause trading
        if alert and alert['severity'] == 'critical':
            if session.status == "active":
                self.pause_trading(session_id)
                if self.logger:
                    self.logger.warning(
                        f"Critical risk alert triggered, paused trading session {session_id} / "
                        f"触发严重风险预警，暂停交易会话 {session_id}"
                    )
        
        return alert
    
    def execute_batch_trades(
        self,
        session_id: str,
        signals: List[Signal]
    ) -> List[TradeResult]:
        """
        Execute multiple trades in batch.
        批量执行多个交易
        
        Args:
            session_id: Trading session identifier / 交易会话标识符
            signals: List of trading signals / 交易信号列表
            
        Returns:
            List[TradeResult]: List of trade results / 交易结果列表
            
        Raises:
            ValueError: If session not found / 如果未找到会话
        """
        session = self._sessions.get(session_id)
        if session is None:
            raise ValueError(
                f"Trading session {session_id} not found / "
                f"未找到交易会话 {session_id}"
            )
        
        results = []
        
        for signal in signals:
            try:
                result = self.execute_trade(session_id, signal)
                results.append(result)
            except Exception as e:
                if self.logger:
                    self.logger.error(
                        f"Failed to execute trade for {signal.stock_code}: {str(e)} / "
                        f"执行 {signal.stock_code} 交易失败：{str(e)}"
                    )
                # Create failed result
                results.append(TradeResult(
                    trade_id=f"trade_{uuid.uuid4().hex[:8]}",
                    order_id="N/A",
                    symbol=signal.stock_code,
                    action=signal.action,
                    quantity=0.0,
                    price=0.0,
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    status="failed",
                    commission=0.0,
                    message=f"Execution failed: {str(e)}"
                ))
        
        if self.logger:
            successful = sum(1 for r in results if r.status == "filled")
            self.logger.info(
                f"Batch execution completed: {successful}/{len(signals)} trades successful / "
                f"批量执行完成：{successful}/{len(signals)} 笔交易成功"
            )
        
        return results
