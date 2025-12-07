"""
Portfolio Manager for managing investment portfolios.
投资组合管理器，用于管理投资组合

This module provides functionality for creating and managing portfolios,
tracking positions, calculating portfolio values, and maintaining trade history.
本模块提供创建和管理投资组合、跟踪持仓、计算组合价值和维护交易历史的功能。
"""

import uuid
from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd

from src.models.trading_models import Portfolio, Position, Trade
from src.infrastructure.logger_system import LoggerSystem


class PortfolioManager:
    """
    Portfolio Manager for managing investment portfolios.
    投资组合管理器
    
    This class handles portfolio creation, position updates, value calculations,
    trade history tracking, and returns calculation.
    该类处理投资组合创建、持仓更新、价值计算、交易历史跟踪和收益率计算。
    """
    
    def __init__(self, logger: Optional[LoggerSystem] = None):
        """
        Initialize Portfolio Manager.
        初始化投资组合管理器
        
        Args:
            logger: Logger system instance / 日志系统实例
        """
        self.logger = logger.get_logger(__name__) if logger else None
        self._portfolios: Dict[str, Portfolio] = {}
        self._trade_history: Dict[str, List[Trade]] = {}
        
        if self.logger:
            self.logger.info("PortfolioManager initialized / 投资组合管理器已初始化")
    
    def create_portfolio(self, initial_capital: float, portfolio_id: Optional[str] = None) -> Portfolio:
        """
        Create a new portfolio with initial capital.
        创建具有初始资金的新投资组合
        
        Args:
            initial_capital: Initial capital amount / 初始资金金额
            portfolio_id: Optional portfolio ID, auto-generated if not provided / 可选的组合ID，未提供则自动生成
            
        Returns:
            Created portfolio / 创建的投资组合
            
        Raises:
            ValueError: If initial_capital is not positive / 如果初始资金不是正数
        """
        if initial_capital <= 0:
            raise ValueError(f"Initial capital must be positive, got {initial_capital}")
        
        if portfolio_id is None:
            portfolio_id = f"portfolio_{uuid.uuid4().hex[:8]}"
        
        portfolio = Portfolio(
            portfolio_id=portfolio_id,
            positions={},
            cash=initial_capital,
            total_value=initial_capital,
            initial_capital=initial_capital
        )
        
        self._portfolios[portfolio_id] = portfolio
        self._trade_history[portfolio_id] = []
        
        if self.logger:
            self.logger.info(
                f"Created portfolio {portfolio_id} with initial capital {initial_capital} / "
                f"创建投资组合 {portfolio_id}，初始资金 {initial_capital}"
            )
        
        return portfolio
    
    def get_portfolio(self, portfolio_id: str) -> Optional[Portfolio]:
        """
        Get portfolio by ID.
        根据ID获取投资组合
        
        Args:
            portfolio_id: Portfolio identifier / 投资组合标识符
            
        Returns:
            Portfolio if found, None otherwise / 找到则返回投资组合，否则返回None
        """
        return self._portfolios.get(portfolio_id)
    
    def update_position(
        self,
        portfolio_id: str,
        symbol: str,
        quantity: float,
        price: float,
        action: str = "buy",
        commission: float = 0.0
    ) -> None:
        """
        Update position in portfolio by executing a trade.
        通过执行交易更新投资组合中的持仓
        
        Args:
            portfolio_id: Portfolio identifier / 投资组合标识符
            symbol: Stock symbol / 股票代码
            quantity: Number of shares to trade / 交易股数
            price: Trade price per share / 每股交易价格
            action: Trade action ("buy" or "sell") / 交易动作（"buy"或"sell"）
            commission: Trading commission / 交易佣金
            
        Raises:
            ValueError: If portfolio not found or invalid parameters / 如果未找到投资组合或参数无效
        """
        portfolio = self._portfolios.get(portfolio_id)
        if portfolio is None:
            raise ValueError(f"Portfolio {portfolio_id} not found / 未找到投资组合 {portfolio_id}")
        
        if quantity <= 0:
            raise ValueError(f"Quantity must be positive, got {quantity}")
        
        if price <= 0:
            raise ValueError(f"Price must be positive, got {price}")
        
        if action not in ["buy", "sell"]:
            raise ValueError(f"Action must be 'buy' or 'sell', got {action}")
        
        # Calculate trade cost
        trade_cost = quantity * price + commission
        
        if action == "buy":
            self._execute_buy(portfolio, symbol, quantity, price, trade_cost, commission)
        else:  # sell
            self._execute_sell(portfolio, symbol, quantity, price, trade_cost, commission)
        
        # Update portfolio total value
        portfolio.update_total_value()
        
        if self.logger:
            self.logger.info(
                f"Updated position for {symbol} in portfolio {portfolio_id}: "
                f"{action} {quantity} shares @ {price} / "
                f"更新投资组合 {portfolio_id} 中 {symbol} 的持仓：{action} {quantity} 股 @ {price}"
            )
    
    def _execute_buy(
        self,
        portfolio: Portfolio,
        symbol: str,
        quantity: float,
        price: float,
        trade_cost: float,
        commission: float
    ) -> None:
        """
        Execute a buy trade.
        执行买入交易
        
        Args:
            portfolio: Portfolio to update / 要更新的投资组合
            symbol: Stock symbol / 股票代码
            quantity: Number of shares / 股数
            price: Price per share / 每股价格
            trade_cost: Total trade cost including commission / 包含佣金的总交易成本
            commission: Trading commission / 交易佣金
        """
        # Check if enough cash
        if portfolio.cash < trade_cost:
            raise ValueError(
                f"Insufficient cash: need {trade_cost}, have {portfolio.cash} / "
                f"现金不足：需要 {trade_cost}，拥有 {portfolio.cash}"
            )
        
        # Update or create position
        if symbol in portfolio.positions:
            # Update existing position
            pos = portfolio.positions[symbol]
            total_cost = pos.quantity * pos.avg_cost + trade_cost
            new_quantity = pos.quantity + quantity
            new_avg_cost = total_cost / new_quantity
            
            pos.quantity = new_quantity
            pos.avg_cost = new_avg_cost
            pos.current_price = price
            pos.__post_init__()  # Recalculate derived fields
        else:
            # Create new position
            portfolio.positions[symbol] = Position(
                symbol=symbol,
                quantity=quantity,
                avg_cost=price + (commission / quantity),
                current_price=price
            )
        
        # Update cash
        portfolio.cash -= trade_cost
        
        # Record trade
        trade = Trade(
            trade_id=f"trade_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.now().isoformat(),
            symbol=symbol,
            action="buy",
            quantity=quantity,
            price=price,
            commission=commission
        )
        self._trade_history[portfolio.portfolio_id].append(trade)
    
    def _execute_sell(
        self,
        portfolio: Portfolio,
        symbol: str,
        quantity: float,
        price: float,
        trade_cost: float,
        commission: float
    ) -> None:
        """
        Execute a sell trade.
        执行卖出交易
        
        Args:
            portfolio: Portfolio to update / 要更新的投资组合
            symbol: Stock symbol / 股票代码
            quantity: Number of shares / 股数
            price: Price per share / 每股价格
            trade_cost: Total trade cost including commission / 包含佣金的总交易成本
            commission: Trading commission / 交易佣金
        """
        # Check if position exists and has enough shares
        if symbol not in portfolio.positions:
            raise ValueError(f"No position found for {symbol} / 未找到 {symbol} 的持仓")
        
        pos = portfolio.positions[symbol]
        if pos.quantity < quantity:
            raise ValueError(
                f"Insufficient shares: need {quantity}, have {pos.quantity} / "
                f"股数不足：需要 {quantity}，拥有 {pos.quantity}"
            )
        
        # Update position
        pos.quantity -= quantity
        
        # Remove position if quantity becomes zero
        if pos.quantity == 0:
            del portfolio.positions[symbol]
        else:
            pos.current_price = price
            pos.__post_init__()  # Recalculate derived fields
        
        # Update cash (receive proceeds minus commission)
        proceeds = quantity * price - commission
        portfolio.cash += proceeds
        
        # Record trade
        trade = Trade(
            trade_id=f"trade_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.now().isoformat(),
            symbol=symbol,
            action="sell",
            quantity=quantity,
            price=price,
            commission=commission
        )
        self._trade_history[portfolio.portfolio_id].append(trade)
    
    def update_prices(self, portfolio_id: str, prices: Dict[str, float]) -> None:
        """
        Update current prices for positions in portfolio.
        更新投资组合中持仓的当前价格
        
        Args:
            portfolio_id: Portfolio identifier / 投资组合标识符
            prices: Dictionary mapping symbols to current prices / 股票代码到当前价格的字典
            
        Raises:
            ValueError: If portfolio not found / 如果未找到投资组合
        """
        portfolio = self._portfolios.get(portfolio_id)
        if portfolio is None:
            raise ValueError(f"Portfolio {portfolio_id} not found / 未找到投资组合 {portfolio_id}")
        
        for symbol, price in prices.items():
            if symbol in portfolio.positions:
                pos = portfolio.positions[symbol]
                pos.current_price = price
                pos.__post_init__()  # Recalculate derived fields
        
        # Update total portfolio value
        portfolio.update_total_value()
        
        if self.logger:
            self.logger.debug(
                f"Updated prices for portfolio {portfolio_id}, total value: {portfolio.total_value} / "
                f"更新投资组合 {portfolio_id} 的价格，总价值：{portfolio.total_value}"
            )
    
    def get_current_value(self, portfolio_id: str) -> float:
        """
        Get current total value of portfolio.
        获取投资组合的当前总价值
        
        Args:
            portfolio_id: Portfolio identifier / 投资组合标识符
            
        Returns:
            Current portfolio value / 当前投资组合价值
            
        Raises:
            ValueError: If portfolio not found / 如果未找到投资组合
        """
        portfolio = self._portfolios.get(portfolio_id)
        if portfolio is None:
            raise ValueError(f"Portfolio {portfolio_id} not found / 未找到投资组合 {portfolio_id}")
        
        portfolio.update_total_value()
        return portfolio.total_value
    
    def get_positions(self, portfolio_id: str) -> Dict[str, Position]:
        """
        Get all positions in portfolio.
        获取投资组合中的所有持仓
        
        Args:
            portfolio_id: Portfolio identifier / 投资组合标识符
            
        Returns:
            Dictionary of positions keyed by symbol / 按股票代码索引的持仓字典
            
        Raises:
            ValueError: If portfolio not found / 如果未找到投资组合
        """
        portfolio = self._portfolios.get(portfolio_id)
        if portfolio is None:
            raise ValueError(f"Portfolio {portfolio_id} not found / 未找到投资组合 {portfolio_id}")
        
        return portfolio.positions.copy()
    
    def get_trade_history(self, portfolio_id: str) -> List[Trade]:
        """
        Get trade history for portfolio.
        获取投资组合的交易历史
        
        Args:
            portfolio_id: Portfolio identifier / 投资组合标识符
            
        Returns:
            List of trades / 交易列表
            
        Raises:
            ValueError: If portfolio not found / 如果未找到投资组合
        """
        if portfolio_id not in self._portfolios:
            raise ValueError(f"Portfolio {portfolio_id} not found / 未找到投资组合 {portfolio_id}")
        
        return self._trade_history.get(portfolio_id, []).copy()
    
    def calculate_returns(
        self,
        portfolio_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.Series:
        """
        Calculate returns for portfolio over a period.
        计算投资组合在一段时间内的收益率
        
        Args:
            portfolio_id: Portfolio identifier / 投资组合标识符
            start_date: Start date (ISO format), None for all history / 开始日期（ISO格式），None表示所有历史
            end_date: End date (ISO format), None for current / 结束日期（ISO格式），None表示当前
            
        Returns:
            Series of returns indexed by date / 按日期索引的收益率序列
            
        Raises:
            ValueError: If portfolio not found / 如果未找到投资组合
        """
        portfolio = self._portfolios.get(portfolio_id)
        if portfolio is None:
            raise ValueError(f"Portfolio {portfolio_id} not found / 未找到投资组合 {portfolio_id}")
        
        trades = self._trade_history.get(portfolio_id, [])
        
        if not trades:
            # No trades, return empty series
            return pd.Series(dtype=float)
        
        # Convert trades to DataFrame
        trade_data = []
        for trade in trades:
            trade_data.append({
                'timestamp': pd.to_datetime(trade.timestamp),
                'symbol': trade.symbol,
                'action': trade.action,
                'quantity': trade.quantity,
                'price': trade.price,
                'total_cost': trade.total_cost
            })
        
        df = pd.DataFrame(trade_data)
        df = df.set_index('timestamp').sort_index()
        
        # Filter by date range if provided
        if start_date:
            df = df[df.index >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df.index <= pd.to_datetime(end_date)]
        
        if df.empty:
            return pd.Series(dtype=float)
        
        # Calculate daily portfolio values (simplified)
        # This is a basic implementation - in production, you'd want to track
        # daily portfolio values more accurately
        dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
        values = pd.Series(index=dates, dtype=float)
        
        current_value = portfolio.initial_capital
        for date in dates:
            day_trades = df[df.index.date == date.date()]
            if not day_trades.empty:
                # Simplified: just track cash flow
                for _, trade in day_trades.iterrows():
                    if trade['action'] == 'buy':
                        current_value -= trade['total_cost']
                    else:  # sell
                        current_value += (trade['quantity'] * trade['price'] - 
                                        (trade['total_cost'] - trade['quantity'] * trade['price']))
            values[date] = current_value
        
        # Calculate returns
        returns = values.pct_change().fillna(0)
        
        if self.logger:
            self.logger.info(
                f"Calculated returns for portfolio {portfolio_id} from {start_date} to {end_date} / "
                f"计算投资组合 {portfolio_id} 从 {start_date} 到 {end_date} 的收益率"
            )
        
        return returns
    
    def get_portfolio_summary(self, portfolio_id: str) -> Dict:
        """
        Get summary statistics for portfolio.
        获取投资组合的摘要统计信息
        
        Args:
            portfolio_id: Portfolio identifier / 投资组合标识符
            
        Returns:
            Dictionary containing portfolio summary / 包含投资组合摘要的字典
            
        Raises:
            ValueError: If portfolio not found / 如果未找到投资组合
        """
        portfolio = self._portfolios.get(portfolio_id)
        if portfolio is None:
            raise ValueError(f"Portfolio {portfolio_id} not found / 未找到投资组合 {portfolio_id}")
        
        portfolio.update_total_value()
        
        total_unrealized_pnl = sum(pos.unrealized_pnl for pos in portfolio.positions.values())
        total_return = ((portfolio.total_value - portfolio.initial_capital) / 
                       portfolio.initial_capital * 100) if portfolio.initial_capital > 0 else 0
        
        summary = {
            'portfolio_id': portfolio_id,
            'initial_capital': portfolio.initial_capital,
            'current_value': portfolio.total_value,
            'cash': portfolio.cash,
            'positions_value': sum(pos.market_value for pos in portfolio.positions.values()),
            'num_positions': len(portfolio.positions),
            'total_unrealized_pnl': total_unrealized_pnl,
            'total_return_pct': total_return,
            'num_trades': len(self._trade_history.get(portfolio_id, []))
        }
        
        return summary
    
    def delete_portfolio(self, portfolio_id: str) -> bool:
        """
        Delete a portfolio and its trade history.
        删除投资组合及其交易历史
        
        Args:
            portfolio_id: Portfolio identifier / 投资组合标识符
            
        Returns:
            True if deleted, False if not found / 如果删除则返回True，如果未找到则返回False
        """
        if portfolio_id in self._portfolios:
            del self._portfolios[portfolio_id]
            if portfolio_id in self._trade_history:
                del self._trade_history[portfolio_id]
            
            if self.logger:
                self.logger.info(
                    f"Deleted portfolio {portfolio_id} / 删除投资组合 {portfolio_id}"
                )
            return True
        
        return False
