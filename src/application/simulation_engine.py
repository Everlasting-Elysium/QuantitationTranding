"""
模拟交易引擎模块 / Simulation Trading Engine Module
负责执行模拟交易、跟踪模拟持仓、计算模拟收益
Responsible for executing simulation trading, tracking simulated positions, and calculating simulated returns
"""

import uuid
import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict

from ..models.trading_models import Portfolio, Position, Trade, Signal
from ..core.portfolio_manager import PortfolioManager
from ..application.signal_generator import SignalGenerator
from ..infrastructure.logger_system import get_logger


@dataclass
class SimulationSession:
    """
    模拟交易会话 / Simulation Trading Session
    
    Attributes:
        session_id: 会话唯一标识符 / Session unique identifier
        model_id: 使用的模型ID / Model ID used
        initial_capital: 初始资金 / Initial capital
        simulation_days: 模拟天数 / Simulation days
        start_date: 开始日期 / Start date
        end_date: 结束日期 / End date
        status: 会话状态 / Session status
        current_portfolio: 当前投资组合 / Current portfolio
        created_at: 创建时间 / Creation time
    """
    session_id: str
    model_id: str
    initial_capital: float
    simulation_days: int
    start_date: str
    end_date: str
    status: str = "running"  # "running", "completed", "failed"
    current_portfolio: Optional[Portfolio] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class SimulationStepResult:
    """
    模拟交易单步结果 / Simulation Step Result
    
    Attributes:
        date: 日期 / Date
        signals: 生成的信号 / Generated signals
        trades_executed: 执行的交易 / Executed trades
        portfolio_value: 投资组合价值 / Portfolio value
        daily_return: 日收益率 / Daily return
        cash_balance: 现金余额 / Cash balance
    """
    date: str
    signals: List[Signal]
    trades_executed: List[Trade]
    portfolio_value: float
    daily_return: float
    cash_balance: float


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
        final_portfolio_value: 最终投资组合价值 / Final portfolio value
        daily_returns: 日收益率序列 / Daily returns series
        trade_history: 交易历史 / Trade history
        daily_values: 每日价值序列 / Daily values series
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
    trade_history: List[Trade]
    daily_values: pd.Series


class SimulationEngineError(Exception):
    """模拟引擎错误 / Simulation Engine Error"""
    pass


class SimulationEngine:
    """
    模拟交易引擎 / Simulation Trading Engine
    
    职责 / Responsibilities:
    - 执行模拟交易 / Execute simulation trading
    - 管理模拟会话 / Manage simulation sessions
    - 每日信号生成和执行 / Daily signal generation and execution
    - 跟踪模拟持仓 / Track simulated positions
    - 计算模拟收益 / Calculate simulated returns
    - 生成模拟报告 / Generate simulation reports
    """
    
    def __init__(
        self,
        signal_generator: SignalGenerator,
        portfolio_manager: PortfolioManager,
        qlib_wrapper,
        output_dir: str = "./simulations"
    ):
        """
        初始化模拟交易引擎 / Initialize Simulation Trading Engine
        
        Args:
            signal_generator: 信号生成器 / Signal generator
            portfolio_manager: 投资组合管理器 / Portfolio manager
            qlib_wrapper: Qlib封装器 / Qlib wrapper
            output_dir: 输出目录 / Output directory
        """
        self._signal_generator = signal_generator
        self._portfolio_manager = portfolio_manager
        self._qlib_wrapper = qlib_wrapper
        self._output_dir = Path(output_dir).expanduser()
        self._logger = get_logger(__name__)
        
        # 会话存储 / Session storage
        self._sessions: Dict[str, SimulationSession] = {}
        self._step_results: Dict[str, List[SimulationStepResult]] = {}
        
        # 确保输出目录存在 / Ensure output directory exists
        self._output_dir.mkdir(parents=True, exist_ok=True)
        
        self._logger.info(
            f"模拟交易引擎初始化成功 / Simulation engine initialized successfully\n"
            f"输出目录 / Output directory: {self._output_dir}"
        )
    
    def start_simulation(
        self,
        model_id: str,
        initial_capital: float,
        simulation_days: int,
        start_date: str,
        instruments: str = "csi300",
        top_n: int = 10
    ) -> SimulationSession:
        """
        启动模拟交易 / Start Simulation Trading
        
        Args:
            model_id: 模型ID / Model ID
            initial_capital: 初始资金 / Initial capital
            simulation_days: 模拟天数 / Simulation days
            start_date: 开始日期 / Start date
            instruments: 股票池 / Instrument pool
            top_n: 买入候选数量 / Number of buy candidates
            
        Returns:
            SimulationSession: 模拟会话 / Simulation session
            
        Raises:
            SimulationEngineError: 启动失败时抛出 / Raised when start fails
        """
        try:
            self._logger.info(
                f"启动模拟交易 / Starting simulation trading\n"
                f"模型ID / Model ID: {model_id}\n"
                f"初始资金 / Initial capital: {initial_capital}\n"
                f"模拟天数 / Simulation days: {simulation_days}\n"
                f"开始日期 / Start date: {start_date}\n"
                f"股票池 / Instruments: {instruments}"
            )
            
            # 验证参数 / Validate parameters
            if initial_capital <= 0:
                raise ValueError(f"初始资金必须为正数 / Initial capital must be positive: {initial_capital}")
            
            if simulation_days <= 0:
                raise ValueError(f"模拟天数必须为正数 / Simulation days must be positive: {simulation_days}")
            
            # 计算结束日期 / Calculate end date
            start_dt = pd.to_datetime(start_date)
            # 使用交易日历计算结束日期（简化实现，实际应使用交易日历）
            # Use trading calendar to calculate end date (simplified, should use trading calendar)
            end_dt = start_dt + timedelta(days=simulation_days * 1.5)  # 考虑非交易日 / Consider non-trading days
            end_date = end_dt.strftime("%Y-%m-%d")
            
            # 创建会话ID / Create session ID
            session_id = f"sim_{uuid.uuid4().hex[:8]}"
            
            # 创建投资组合 / Create portfolio
            portfolio = self._portfolio_manager.create_portfolio(
                initial_capital=initial_capital,
                portfolio_id=f"{session_id}_portfolio"
            )
            
            # 创建会话 / Create session
            session = SimulationSession(
                session_id=session_id,
                model_id=model_id,
                initial_capital=initial_capital,
                simulation_days=simulation_days,
                start_date=start_date,
                end_date=end_date,
                status="running",
                current_portfolio=portfolio
            )
            
            # 保存会话 / Save session
            self._sessions[session_id] = session
            self._step_results[session_id] = []
            
            # 保存会话到文件 / Save session to file
            self._save_session(session)
            
            self._logger.info(
                f"模拟交易会话创建成功 / Simulation session created successfully\n"
                f"会话ID / Session ID: {session_id}\n"
                f"结束日期 / End date: {end_date}"
            )
            
            # 执行模拟 / Execute simulation
            self._execute_simulation(session, instruments, top_n)
            
            return session
            
        except Exception as e:
            error_msg = f"启动模拟交易失败 / Failed to start simulation: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise SimulationEngineError(error_msg) from e

    
    def _execute_simulation(
        self,
        session: SimulationSession,
        instruments: str,
        top_n: int
    ) -> None:
        """
        执行模拟交易 / Execute Simulation Trading
        
        Args:
            session: 模拟会话 / Simulation session
            instruments: 股票池 / Instrument pool
            top_n: 买入候选数量 / Number of buy candidates
        """
        try:
            self._logger.info(
                f"开始执行模拟交易 / Starting simulation execution\n"
                f"会话ID / Session ID: {session.session_id}"
            )
            
            # 获取交易日历 / Get trading calendar
            trading_dates = self._get_trading_dates(session.start_date, session.end_date)
            
            if len(trading_dates) == 0:
                raise SimulationEngineError("没有可用的交易日 / No trading dates available")
            
            # 限制模拟天数 / Limit simulation days
            if len(trading_dates) > session.simulation_days:
                trading_dates = trading_dates[:session.simulation_days]
            
            self._logger.info(
                f"交易日数量 / Trading days count: {len(trading_dates)}\n"
                f"第一个交易日 / First trading day: {trading_dates[0]}\n"
                f"最后一个交易日 / Last trading day: {trading_dates[-1]}"
            )
            
            # 记录前一日的投资组合价值用于计算收益率 / Record previous day's portfolio value for return calculation
            previous_value = session.initial_capital
            
            # 逐日执行模拟 / Execute simulation day by day
            for i, date in enumerate(trading_dates):
                try:
                    self._logger.info(
                        f"执行第 {i+1}/{len(trading_dates)} 天模拟 / "
                        f"Executing day {i+1}/{len(trading_dates)} simulation: {date}"
                    )
                    
                    # 执行单步模拟 / Execute single step simulation
                    step_result = self.execute_simulation_step(
                        session=session,
                        date=date,
                        instruments=instruments,
                        top_n=top_n,
                        previous_value=previous_value
                    )
                    
                    # 保存步骤结果 / Save step result
                    self._step_results[session.session_id].append(step_result)
                    
                    # 更新前一日价值 / Update previous value
                    previous_value = step_result.portfolio_value
                    
                    self._logger.debug(
                        f"第 {i+1} 天模拟完成 / Day {i+1} simulation completed\n"
                        f"投资组合价值 / Portfolio value: {step_result.portfolio_value:.2f}\n"
                        f"日收益率 / Daily return: {step_result.daily_return:.2%}\n"
                        f"执行交易数 / Trades executed: {len(step_result.trades_executed)}"
                    )
                    
                except Exception as e:
                    self._logger.error(
                        f"第 {i+1} 天模拟失败 / Day {i+1} simulation failed: {str(e)}",
                        exc_info=True
                    )
                    # 继续下一天 / Continue to next day
                    continue
            
            # 更新会话状态 / Update session status
            session.status = "completed"
            self._save_session(session)
            
            self._logger.info(
                f"模拟交易执行完成 / Simulation execution completed\n"
                f"会话ID / Session ID: {session.session_id}\n"
                f"执行天数 / Days executed: {len(self._step_results[session.session_id])}"
            )
            
        except Exception as e:
            session.status = "failed"
            self._save_session(session)
            error_msg = f"执行模拟交易失败 / Failed to execute simulation: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise SimulationEngineError(error_msg) from e
    
    def execute_simulation_step(
        self,
        session: SimulationSession,
        date: str,
        instruments: str,
        top_n: int,
        previous_value: float
    ) -> SimulationStepResult:
        """
        执行单步模拟 / Execute Single Step Simulation
        
        Args:
            session: 模拟会话 / Simulation session
            date: 当前日期 / Current date
            instruments: 股票池 / Instrument pool
            top_n: 买入候选数量 / Number of buy candidates
            previous_value: 前一日投资组合价值 / Previous day's portfolio value
            
        Returns:
            SimulationStepResult: 单步结果 / Step result
            
        Raises:
            SimulationEngineError: 执行失败时抛出 / Raised when execution fails
        """
        try:
            # 1. 更新持仓价格 / Update position prices
            self._update_position_prices(session, date)
            
            # 2. 生成交易信号 / Generate trading signals
            signals = self._signal_generator.generate_signals(
                model_id=session.model_id,
                date=date,
                portfolio=session.current_portfolio,
                top_n=top_n,
                instruments=instruments
            )
            
            # 3. 执行交易 / Execute trades
            trades_executed = self._execute_trades(session, signals, date)
            
            # 4. 更新投资组合价值 / Update portfolio value
            session.current_portfolio.update_total_value()
            current_value = session.current_portfolio.total_value
            
            # 5. 计算日收益率 / Calculate daily return
            daily_return = ((current_value - previous_value) / previous_value) if previous_value > 0 else 0.0
            
            # 6. 创建步骤结果 / Create step result
            step_result = SimulationStepResult(
                date=date,
                signals=signals,
                trades_executed=trades_executed,
                portfolio_value=current_value,
                daily_return=daily_return,
                cash_balance=session.current_portfolio.cash
            )
            
            return step_result
            
        except Exception as e:
            error_msg = f"执行单步模拟失败 / Failed to execute simulation step: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise SimulationEngineError(error_msg) from e
    
    def _get_trading_dates(self, start_date: str, end_date: str) -> List[str]:
        """
        获取交易日列表 / Get Trading Dates List
        
        Args:
            start_date: 开始日期 / Start date
            end_date: 结束日期 / End date
            
        Returns:
            List[str]: 交易日列表 / Trading dates list
        """
        try:
            # 尝试从qlib获取交易日历 / Try to get trading calendar from qlib
            import qlib
            from qlib.data import D
            
            # 获取交易日历 / Get trading calendar
            calendar = D.calendar(start_time=start_date, end_time=end_date)
            
            if calendar is not None and len(calendar) > 0:
                trading_dates = [date.strftime("%Y-%m-%d") for date in calendar]
                self._logger.debug(f"从qlib获取交易日历 / Got trading calendar from qlib: {len(trading_dates)} days")
                return trading_dates
            
        except Exception as e:
            self._logger.warning(f"从qlib获取交易日历失败 / Failed to get trading calendar from qlib: {str(e)}")
        
        # 如果无法从qlib获取，使用简化方法 / If cannot get from qlib, use simplified method
        self._logger.info("使用简化方法生成交易日 / Using simplified method to generate trading dates")
        
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        
        # 生成所有日期 / Generate all dates
        all_dates = pd.date_range(start=start_dt, end=end_dt, freq='D')
        
        # 过滤周末 / Filter weekends
        trading_dates = [date.strftime("%Y-%m-%d") for date in all_dates if date.weekday() < 5]
        
        return trading_dates
    
    def _update_position_prices(self, session: SimulationSession, date: str) -> None:
        """
        更新持仓价格 / Update Position Prices
        
        Args:
            session: 模拟会话 / Simulation session
            date: 当前日期 / Current date
        """
        try:
            if not session.current_portfolio.positions:
                return
            
            # 获取所有持仓股票的当前价格 / Get current prices for all positions
            symbols = list(session.current_portfolio.positions.keys())
            
            # 从qlib获取价格数据 / Get price data from qlib
            prices = self._get_stock_prices(symbols, date)
            
            if prices:
                # 更新价格 / Update prices
                self._portfolio_manager.update_prices(
                    portfolio_id=session.current_portfolio.portfolio_id,
                    prices=prices
                )
                
                self._logger.debug(
                    f"更新持仓价格 / Updated position prices: {len(prices)} stocks"
                )
            
        except Exception as e:
            self._logger.warning(f"更新持仓价格失败 / Failed to update position prices: {str(e)}")
    
    def _get_stock_prices(self, symbols: List[str], date: str) -> Dict[str, float]:
        """
        获取股票价格 / Get Stock Prices
        
        Args:
            symbols: 股票代码列表 / Stock symbols list
            date: 日期 / Date
            
        Returns:
            Dict[str, float]: 股票价格字典 / Stock prices dictionary
        """
        try:
            prices = {}
            
            # 使用qlib获取价格 / Use qlib to get prices
            for symbol in symbols:
                try:
                    data = self._qlib_wrapper.get_data(
                        instruments=symbol,
                        fields=["$close"],
                        start_time=date,
                        end_time=date
                    )
                    
                    if data is not None and not data.empty:
                        # 提取收盘价 / Extract close price
                        if isinstance(data.index, pd.MultiIndex):
                            price = data.loc[(pd.Timestamp(date), symbol), "$close"]
                        else:
                            price = data["$close"].iloc[0]
                        
                        prices[symbol] = float(price)
                    
                except Exception as e:
                    self._logger.debug(f"获取 {symbol} 价格失败 / Failed to get price for {symbol}: {str(e)}")
                    continue
            
            return prices
            
        except Exception as e:
            self._logger.warning(f"获取股票价格失败 / Failed to get stock prices: {str(e)}")
            return {}
    
    def _execute_trades(
        self,
        session: SimulationSession,
        signals: List[Signal],
        date: str
    ) -> List[Trade]:
        """
        执行交易 / Execute Trades
        
        Args:
            session: 模拟会话 / Simulation session
            signals: 交易信号列表 / Trading signals list
            date: 当前日期 / Current date
            
        Returns:
            List[Trade]: 执行的交易列表 / Executed trades list
        """
        trades_executed = []
        
        try:
            for signal in signals:
                try:
                    # 获取股票当前价格 / Get stock current price
                    price = self._get_stock_price(signal.stock_code, date)
                    
                    if price is None or price <= 0:
                        self._logger.warning(
                            f"无法获取 {signal.stock_code} 的价格，跳过交易 / "
                            f"Cannot get price for {signal.stock_code}, skipping trade"
                        )
                        continue
                    
                    # 根据信号类型执行交易 / Execute trade based on signal type
                    if signal.action == "buy":
                        trade = self._execute_buy(session, signal, price, date)
                        if trade:
                            trades_executed.append(trade)
                    
                    elif signal.action == "sell":
                        trade = self._execute_sell(session, signal, price, date)
                        if trade:
                            trades_executed.append(trade)
                    
                    # hold信号不需要执行交易 / Hold signals don't need trade execution
                    
                except Exception as e:
                    self._logger.warning(
                        f"执行 {signal.stock_code} 交易失败 / Failed to execute trade for {signal.stock_code}: {str(e)}"
                    )
                    continue
            
            return trades_executed
            
        except Exception as e:
            self._logger.error(f"执行交易失败 / Failed to execute trades: {str(e)}", exc_info=True)
            return trades_executed
    
    def _get_stock_price(self, symbol: str, date: str) -> Optional[float]:
        """
        获取单只股票价格 / Get Single Stock Price
        
        Args:
            symbol: 股票代码 / Stock symbol
            date: 日期 / Date
            
        Returns:
            Optional[float]: 股票价格或None / Stock price or None
        """
        try:
            data = self._qlib_wrapper.get_data(
                instruments=symbol,
                fields=["$close"],
                start_time=date,
                end_time=date
            )
            
            if data is not None and not data.empty:
                if isinstance(data.index, pd.MultiIndex):
                    price = data.loc[(pd.Timestamp(date), symbol), "$close"]
                else:
                    price = data["$close"].iloc[0]
                
                return float(price)
            
            return None
            
        except Exception as e:
            self._logger.debug(f"获取 {symbol} 价格失败 / Failed to get price for {symbol}: {str(e)}")
            return None
    
    def _execute_buy(
        self,
        session: SimulationSession,
        signal: Signal,
        price: float,
        date: str
    ) -> Optional[Trade]:
        """
        执行买入交易 / Execute Buy Trade
        
        Args:
            session: 模拟会话 / Simulation session
            signal: 交易信号 / Trading signal
            price: 股票价格 / Stock price
            date: 日期 / Date
            
        Returns:
            Optional[Trade]: 交易记录或None / Trade record or None
        """
        try:
            portfolio = session.current_portfolio
            
            # 计算买入数量 / Calculate buy quantity
            if signal.quantity is not None and signal.quantity > 0:
                quantity = signal.quantity
            elif signal.target_weight is not None and signal.target_weight > 0:
                # 根据目标权重计算数量 / Calculate quantity based on target weight
                target_value = portfolio.total_value * (signal.target_weight / 100)
                quantity = int(target_value / price / 100) * 100  # 按手数取整 / Round to lots
            else:
                # 默认：使用可用现金的一部分 / Default: use portion of available cash
                # 简化实现：平均分配给所有买入信号 / Simplified: evenly distribute to all buy signals
                available_cash = portfolio.cash * 0.9  # 保留10%现金 / Keep 10% cash
                quantity = int(available_cash / price / 100) * 100  # 按手数取整 / Round to lots
            
            # 确保数量至少为1手 / Ensure quantity is at least 1 lot
            if quantity < 100:
                self._logger.debug(
                    f"买入数量不足1手，跳过 / Buy quantity less than 1 lot, skipping: {signal.stock_code}"
                )
                return None
            
            # 计算佣金（简化：0.03%）/ Calculate commission (simplified: 0.03%)
            commission = quantity * price * 0.0003
            
            # 检查是否有足够现金 / Check if enough cash
            total_cost = quantity * price + commission
            if total_cost > portfolio.cash:
                self._logger.debug(
                    f"现金不足，无法买入 / Insufficient cash to buy: {signal.stock_code}"
                )
                return None
            
            # 执行买入 / Execute buy
            self._portfolio_manager.update_position(
                portfolio_id=portfolio.portfolio_id,
                symbol=signal.stock_code,
                quantity=quantity,
                price=price,
                action="buy",
                commission=commission
            )
            
            # 创建交易记录 / Create trade record
            trade = Trade(
                trade_id=f"trade_{uuid.uuid4().hex[:8]}",
                timestamp=date,
                symbol=signal.stock_code,
                action="buy",
                quantity=quantity,
                price=price,
                commission=commission,
                total_cost=total_cost
            )
            
            self._logger.info(
                f"买入成功 / Buy executed: {signal.stock_code} "
                f"{quantity} 股 @ {price:.2f}, 总成本 / total cost: {total_cost:.2f}"
            )
            
            return trade
            
        except Exception as e:
            self._logger.warning(f"执行买入失败 / Failed to execute buy: {str(e)}")
            return None
    
    def _execute_sell(
        self,
        session: SimulationSession,
        signal: Signal,
        price: float,
        date: str
    ) -> Optional[Trade]:
        """
        执行卖出交易 / Execute Sell Trade
        
        Args:
            session: 模拟会话 / Simulation session
            signal: 交易信号 / Trading signal
            price: 股票价格 / Stock price
            date: 日期 / Date
            
        Returns:
            Optional[Trade]: 交易记录或None / Trade record or None
        """
        try:
            portfolio = session.current_portfolio
            
            # 检查是否持有该股票 / Check if holding the stock
            if signal.stock_code not in portfolio.positions:
                self._logger.debug(
                    f"未持有该股票，无法卖出 / Not holding the stock, cannot sell: {signal.stock_code}"
                )
                return None
            
            position = portfolio.positions[signal.stock_code]
            
            # 确定卖出数量 / Determine sell quantity
            if signal.quantity is not None and signal.quantity > 0:
                quantity = min(signal.quantity, position.quantity)
            else:
                # 默认：全部卖出 / Default: sell all
                quantity = position.quantity
            
            # 计算佣金（简化：0.03%）/ Calculate commission (simplified: 0.03%)
            commission = quantity * price * 0.0003
            
            # 执行卖出 / Execute sell
            self._portfolio_manager.update_position(
                portfolio_id=portfolio.portfolio_id,
                symbol=signal.stock_code,
                quantity=quantity,
                price=price,
                action="sell",
                commission=commission
            )
            
            # 创建交易记录 / Create trade record
            proceeds = quantity * price - commission
            trade = Trade(
                trade_id=f"trade_{uuid.uuid4().hex[:8]}",
                timestamp=date,
                symbol=signal.stock_code,
                action="sell",
                quantity=quantity,
                price=price,
                commission=commission,
                total_cost=proceeds
            )
            
            self._logger.info(
                f"卖出成功 / Sell executed: {signal.stock_code} "
                f"{quantity} 股 @ {price:.2f}, 收入 / proceeds: {proceeds:.2f}"
            )
            
            return trade
            
        except Exception as e:
            self._logger.warning(f"执行卖出失败 / Failed to execute sell: {str(e)}")
            return None

    
    def get_simulation_status(self, session_id: str) -> Dict[str, Any]:
        """
        获取模拟状态 / Get Simulation Status
        
        Args:
            session_id: 会话ID / Session ID
            
        Returns:
            Dict[str, Any]: 状态信息 / Status information
            
        Raises:
            SimulationEngineError: 会话不存在时抛出 / Raised when session not found
        """
        try:
            if session_id not in self._sessions:
                raise SimulationEngineError(f"会话不存在 / Session not found: {session_id}")
            
            session = self._sessions[session_id]
            step_results = self._step_results.get(session_id, [])
            
            # 计算当前统计信息 / Calculate current statistics
            if step_results:
                latest_result = step_results[-1]
                current_value = latest_result.portfolio_value
                total_return = ((current_value - session.initial_capital) / session.initial_capital) * 100
                
                # 计算累计交易数 / Calculate total trades
                total_trades = sum(len(result.trades_executed) for result in step_results)
            else:
                current_value = session.initial_capital
                total_return = 0.0
                total_trades = 0
            
            status = {
                "session_id": session_id,
                "status": session.status,
                "model_id": session.model_id,
                "initial_capital": session.initial_capital,
                "current_value": current_value,
                "total_return_pct": total_return,
                "simulation_days": session.simulation_days,
                "days_completed": len(step_results),
                "total_trades": total_trades,
                "start_date": session.start_date,
                "end_date": session.end_date,
                "created_at": session.created_at
            }
            
            return status
            
        except Exception as e:
            error_msg = f"获取模拟状态失败 / Failed to get simulation status: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise SimulationEngineError(error_msg) from e
    
    def generate_simulation_report(self, session_id: str) -> SimulationReport:
        """
        生成模拟报告 / Generate Simulation Report
        
        Args:
            session_id: 会话ID / Session ID
            
        Returns:
            SimulationReport: 模拟报告 / Simulation report
            
        Raises:
            SimulationEngineError: 生成失败时抛出 / Raised when generation fails
        """
        try:
            self._logger.info(f"生成模拟报告 / Generating simulation report: {session_id}")
            
            if session_id not in self._sessions:
                raise SimulationEngineError(f"会话不存在 / Session not found: {session_id}")
            
            session = self._sessions[session_id]
            step_results = self._step_results.get(session_id, [])
            
            if not step_results:
                raise SimulationEngineError("没有模拟结果数据 / No simulation result data")
            
            # 1. 提取日收益率和价值序列 / Extract daily returns and values series
            dates = [result.date for result in step_results]
            daily_returns = pd.Series(
                [result.daily_return for result in step_results],
                index=pd.to_datetime(dates)
            )
            daily_values = pd.Series(
                [result.portfolio_value for result in step_results],
                index=pd.to_datetime(dates)
            )
            
            # 2. 收集所有交易 / Collect all trades
            all_trades = []
            for result in step_results:
                all_trades.extend(result.trades_executed)
            
            # 3. 计算性能指标 / Calculate performance metrics
            final_value = step_results[-1].portfolio_value
            total_return = ((final_value - session.initial_capital) / session.initial_capital)
            
            # 年化收益率 / Annual return
            trading_days = len(step_results)
            years = trading_days / 252.0
            annual_return = ((1 + total_return) ** (1 / years) - 1) if years > 0 else 0.0
            
            # 夏普比率 / Sharpe ratio
            if len(daily_returns) > 1:
                volatility = daily_returns.std() * np.sqrt(252)
                sharpe_ratio = (annual_return / volatility) if volatility > 0 else 0.0
            else:
                sharpe_ratio = 0.0
            
            # 最大回撤 / Max drawdown
            cumulative_returns = (1 + daily_returns).cumprod()
            running_max = cumulative_returns.expanding().max()
            drawdown = (cumulative_returns - running_max) / running_max
            max_drawdown = float(drawdown.min())
            
            # 胜率 / Win rate
            positive_days = (daily_returns > 0).sum()
            win_rate = (positive_days / len(daily_returns)) if len(daily_returns) > 0 else 0.0
            
            # 盈利交易数 / Profitable trades
            profitable_trades = 0
            for trade in all_trades:
                if trade.action == "sell":
                    # 简化：假设卖出时盈利 / Simplified: assume profit on sell
                    profitable_trades += 1
            
            # 4. 创建报告 / Create report
            report = SimulationReport(
                session_id=session_id,
                total_return=total_return,
                annual_return=annual_return,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=max_drawdown,
                win_rate=win_rate,
                total_trades=len(all_trades),
                profitable_trades=profitable_trades,
                final_portfolio_value=final_value,
                daily_returns=daily_returns,
                trade_history=all_trades,
                daily_values=daily_values
            )
            
            # 5. 保存报告 / Save report
            self._save_report(report)
            
            self._logger.info(
                f"模拟报告生成成功 / Simulation report generated successfully\n"
                f"总收益率 / Total return: {total_return:.2%}\n"
                f"年化收益率 / Annual return: {annual_return:.2%}\n"
                f"夏普比率 / Sharpe ratio: {sharpe_ratio:.4f}\n"
                f"最大回撤 / Max drawdown: {max_drawdown:.2%}\n"
                f"胜率 / Win rate: {win_rate:.2%}\n"
                f"总交易数 / Total trades: {len(all_trades)}"
            )
            
            return report
            
        except Exception as e:
            error_msg = f"生成模拟报告失败 / Failed to generate simulation report: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise SimulationEngineError(error_msg) from e
    
    def _save_session(self, session: SimulationSession) -> None:
        """
        保存会话到文件 / Save Session to File
        
        Args:
            session: 模拟会话 / Simulation session
        """
        try:
            session_dir = self._output_dir / "sessions" / session.session_id
            session_dir.mkdir(parents=True, exist_ok=True)
            
            # 保存会话信息 / Save session information
            session_file = session_dir / "session.json"
            
            # 转换为可序列化的字典 / Convert to serializable dictionary
            session_dict = {
                "session_id": session.session_id,
                "model_id": session.model_id,
                "initial_capital": session.initial_capital,
                "simulation_days": session.simulation_days,
                "start_date": session.start_date,
                "end_date": session.end_date,
                "status": session.status,
                "created_at": session.created_at
            }
            
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_dict, f, indent=2, ensure_ascii=False)
            
            self._logger.debug(f"会话保存成功 / Session saved: {session_file}")
            
        except Exception as e:
            self._logger.warning(f"保存会话失败 / Failed to save session: {str(e)}")
    
    def _save_report(self, report: SimulationReport) -> None:
        """
        保存报告到文件 / Save Report to File
        
        Args:
            report: 模拟报告 / Simulation report
        """
        try:
            report_dir = self._output_dir / "reports" / report.session_id
            report_dir.mkdir(parents=True, exist_ok=True)
            
            # 1. 保存报告摘要 / Save report summary
            summary_file = report_dir / "summary.json"
            summary = {
                "session_id": report.session_id,
                "total_return": report.total_return,
                "annual_return": report.annual_return,
                "sharpe_ratio": report.sharpe_ratio,
                "max_drawdown": report.max_drawdown,
                "win_rate": report.win_rate,
                "total_trades": report.total_trades,
                "profitable_trades": report.profitable_trades,
                "final_portfolio_value": report.final_portfolio_value,
                "generated_at": datetime.now().isoformat()
            }
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            # 2. 保存日收益率 / Save daily returns
            returns_file = report_dir / "daily_returns.csv"
            report.daily_returns.to_csv(returns_file, header=["return"])
            
            # 3. 保存每日价值 / Save daily values
            values_file = report_dir / "daily_values.csv"
            report.daily_values.to_csv(values_file, header=["value"])
            
            # 4. 保存交易历史 / Save trade history
            if report.trade_history:
                trades_file = report_dir / "trades.csv"
                trades_data = []
                for trade in report.trade_history:
                    trades_data.append({
                        "trade_id": trade.trade_id,
                        "timestamp": trade.timestamp,
                        "symbol": trade.symbol,
                        "action": trade.action,
                        "quantity": trade.quantity,
                        "price": trade.price,
                        "commission": trade.commission,
                        "total_cost": trade.total_cost
                    })
                
                trades_df = pd.DataFrame(trades_data)
                trades_df.to_csv(trades_file, index=False)
            
            self._logger.info(f"报告保存成功 / Report saved: {report_dir}")
            
        except Exception as e:
            self._logger.warning(f"保存报告失败 / Failed to save report: {str(e)}")
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """
        列出所有会话 / List All Sessions
        
        Returns:
            List[Dict[str, Any]]: 会话列表 / Sessions list
        """
        sessions_info = []
        
        for session_id, session in self._sessions.items():
            try:
                status = self.get_simulation_status(session_id)
                sessions_info.append(status)
            except Exception as e:
                self._logger.warning(f"获取会话 {session_id} 状态失败 / Failed to get session {session_id} status: {str(e)}")
                continue
        
        return sessions_info
    
    def delete_session(self, session_id: str) -> bool:
        """
        删除会话 / Delete Session
        
        Args:
            session_id: 会话ID / Session ID
            
        Returns:
            bool: 是否成功删除 / Whether successfully deleted
        """
        try:
            if session_id not in self._sessions:
                self._logger.warning(f"会话不存在 / Session not found: {session_id}")
                return False
            
            # 删除内存中的数据 / Delete data in memory
            del self._sessions[session_id]
            if session_id in self._step_results:
                del self._step_results[session_id]
            
            # 删除文件 / Delete files
            import shutil
            session_dir = self._output_dir / "sessions" / session_id
            if session_dir.exists():
                shutil.rmtree(session_dir)
            
            report_dir = self._output_dir / "reports" / session_id
            if report_dir.exists():
                shutil.rmtree(report_dir)
            
            self._logger.info(f"会话删除成功 / Session deleted: {session_id}")
            return True
            
        except Exception as e:
            self._logger.error(f"删除会话失败 / Failed to delete session: {str(e)}", exc_info=True)
            return False
