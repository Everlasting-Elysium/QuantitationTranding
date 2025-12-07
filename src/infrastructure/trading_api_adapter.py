"""
Trading API Adapter Module / 交易API适配器模块

This module provides a unified interface for connecting to broker trading APIs.
本模块提供连接券商交易API的统一接口。

The adapter supports:
- Connecting to broker APIs / 连接券商API
- Placing and canceling orders / 下单和撤单
- Querying account information / 查询账户信息
- Querying positions / 查询持仓
- Querying order status / 查询订单状态
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from abc import ABC, abstractmethod

from .logger_system import get_logger
from ..models.trading_models import (
    Position,
    AccountInfo,
    OrderResult,
    OrderStatus
)
from ..utils.error_handler import (
    SystemError,
    ErrorInfo,
    ErrorCategory,
    ErrorSeverity
)


class TradingAPIAdapter:
    """
    Trading API Adapter / 交易API适配器
    
    Provides a unified interface for connecting to different broker trading APIs.
    提供连接不同券商交易API的统一接口。
    
    This is a base implementation that can be extended for specific brokers.
    这是一个基础实现，可以为特定券商进行扩展。
    
    Responsibilities / 职责:
    - Connect to broker trading APIs / 连接券商交易API
    - Place and cancel orders / 下单和撤单
    - Query account information / 查询账户信息
    - Query positions / 查询持仓
    - Handle API errors / 处理API错误
    """

    
    def __init__(self):
        """Initialize the trading API adapter / 初始化交易API适配器"""
        self._logger = get_logger(__name__)
        self._connected = False
        self._broker: Optional[str] = None
        self._credentials: Optional[Dict[str, Any]] = None
        self._account_id: Optional[str] = None
        
    def connect(self, broker: str, credentials: Dict[str, Any]) -> None:
        """
        Connect to broker trading API / 连接券商交易API
        
        Args:
            broker: Broker name (e.g., "huatai", "citic", "mock") / 券商名称
            credentials: Authentication credentials / 认证凭证
                For real brokers: {"account": "xxx", "password": "xxx", "api_key": "xxx"}
                For mock broker: {"account": "mock_account"}
        
        Raises:
            SystemError: If connection fails / 连接失败时抛出
        """
        try:
            self._logger.info(f"正在连接到券商: {broker}")
            
            # Validate broker name
            if not broker:
                error_info = ErrorInfo(
                    error_code="TRD0001",
                    error_message_zh="券商名称不能为空",
                    error_message_en="Broker name cannot be empty",
                    category=ErrorCategory.SYSTEM,
                    severity=ErrorSeverity.HIGH,
                    technical_details="broker parameter is empty",
                    suggested_actions=[
                        "提供有效的券商名称",
                        "检查配置文件中的券商设置"
                    ],
                    recoverable=True
                )
                self._logger.error(error_info.get_user_message())
                raise SystemError(error_info)
            
            # Validate credentials
            if not credentials:
                error_info = ErrorInfo(
                    error_code="TRD0002",
                    error_message_zh="认证凭证不能为空",
                    error_message_en="Credentials cannot be empty",
                    category=ErrorCategory.SYSTEM,
                    severity=ErrorSeverity.HIGH,
                    technical_details="credentials parameter is empty",
                    suggested_actions=[
                        "提供有效的认证凭证",
                        "检查配置文件中的凭证设置"
                    ],
                    recoverable=True
                )
                self._logger.error(error_info.get_user_message())
                raise SystemError(error_info)
            
            # Store connection info
            self._broker = broker
            self._credentials = credentials
            self._account_id = credentials.get("account", "unknown")
            
            # For now, we support a mock broker for testing
            # Real broker implementations would go here
            if broker.lower() == "mock":
                self._connect_mock_broker(credentials)
            else:
                # Placeholder for real broker connections
                self._logger.warning(
                    f"券商 '{broker}' 的实际连接尚未实现，使用模拟模式"
                )
                self._connect_mock_broker(credentials)
            
            self._connected = True
            self._logger.info(f"成功连接到券商: {broker}, 账户: {self._account_id}")
            
        except SystemError:
            raise
        except Exception as e:
            error_info = ErrorInfo(
                error_code="TRD0003",
                error_message_zh=f"连接券商失败: {str(e)}",
                error_message_en=f"Failed to connect to broker: {str(e)}",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.HIGH,
                technical_details=f"broker={broker}, error={str(e)}",
                suggested_actions=[
                    "检查网络连接",
                    "验证认证凭证是否正确",
                    "确认券商API服务是否可用"
                ],
                recoverable=True,
                original_exception=e
            )
            self._logger.error(error_info.get_user_message(), exc_info=True)
            raise SystemError(error_info) from e

    
    def _connect_mock_broker(self, credentials: Dict[str, Any]) -> None:
        """
        Connect to mock broker for testing / 连接模拟券商用于测试
        
        Args:
            credentials: Mock credentials / 模拟凭证
        """
        self._logger.info("使用模拟券商模式")
        # Mock broker is always available
        # Initialize mock state
        self._mock_orders: Dict[str, OrderStatus] = {}
        self._mock_positions: Dict[str, Position] = {}
        self._mock_cash = 1000000.0  # 100万初始资金
        self._mock_order_counter = 0
    
    def disconnect(self) -> None:
        """
        Disconnect from broker API / 断开券商API连接
        """
        if self._connected:
            self._logger.info(f"断开与券商 {self._broker} 的连接")
            self._connected = False
            self._broker = None
            self._credentials = None
            self._account_id = None
    
    def is_connected(self) -> bool:
        """
        Check if connected to broker / 检查是否已连接到券商
        
        Returns:
            bool: True if connected / 如果已连接返回True
        """
        return self._connected
    
    def place_order(
        self,
        symbol: str,
        quantity: float,
        order_type: str,
        price: Optional[float] = None,
        action: str = "buy"
    ) -> OrderResult:
        """
        Place an order / 下单
        
        Args:
            symbol: Stock symbol / 股票代码
            quantity: Order quantity / 订单数量
            order_type: Order type ("market" or "limit") / 订单类型
            price: Limit price (required for limit orders) / 限价（限价单必需）
            action: Order action ("buy" or "sell") / 订单动作
        
        Returns:
            OrderResult: Order placement result / 下单结果
        
        Raises:
            SystemError: If not connected or order fails / 未连接或下单失败时抛出
        """
        if not self._connected:
            error_info = ErrorInfo(
                error_code="TRD0004",
                error_message_zh="未连接到券商，无法下单",
                error_message_en="Not connected to broker, cannot place order",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.HIGH,
                technical_details="place_order called before connect",
                suggested_actions=[
                    "先调用 connect() 方法连接券商",
                    "检查连接状态"
                ],
                recoverable=True
            )
            self._logger.error(error_info.get_user_message())
            raise SystemError(error_info)
        
        try:
            self._logger.info(
                f"下单: {action} {symbol} x {quantity}, "
                f"类型: {order_type}, 价格: {price}"
            )
            
            # Validate parameters
            if quantity <= 0:
                raise ValueError("订单数量必须大于0")
            
            if order_type not in ["market", "limit"]:
                raise ValueError(f"订单类型必须是 'market' 或 'limit', 收到: {order_type}")
            
            if order_type == "limit" and price is None:
                raise ValueError("限价单必须指定价格")
            
            if action not in ["buy", "sell"]:
                raise ValueError(f"订单动作必须是 'buy' 或 'sell', 收到: {action}")
            
            # For mock broker, simulate order placement
            if self._broker == "mock":
                return self._place_mock_order(symbol, quantity, order_type, price, action)
            
            # Placeholder for real broker order placement
            raise NotImplementedError(f"券商 '{self._broker}' 的下单功能尚未实现")
            
        except (ValueError, NotImplementedError) as e:
            error_info = ErrorInfo(
                error_code="TRD0005",
                error_message_zh=f"下单失败: {str(e)}",
                error_message_en=f"Failed to place order: {str(e)}",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.MEDIUM,
                technical_details=f"symbol={symbol}, quantity={quantity}, type={order_type}, price={price}, action={action}",
                suggested_actions=[
                    "检查订单参数是否正确",
                    "验证股票代码是否有效",
                    "确认账户余额是否充足"
                ],
                recoverable=True,
                original_exception=e
            )
            self._logger.error(error_info.get_user_message(), exc_info=True)
            raise SystemError(error_info) from e

    
    def _place_mock_order(
        self,
        symbol: str,
        quantity: float,
        order_type: str,
        price: Optional[float],
        action: str
    ) -> OrderResult:
        """
        Place a mock order for testing / 下模拟订单用于测试
        
        Args:
            symbol: Stock symbol / 股票代码
            quantity: Order quantity / 订单数量
            order_type: Order type / 订单类型
            price: Order price / 订单价格
            action: Order action / 订单动作
        
        Returns:
            OrderResult: Mock order result / 模拟订单结果
        """
        # Generate order ID
        self._mock_order_counter += 1
        order_id = f"MOCK{self._mock_order_counter:06d}"
        
        # Simulate order execution
        # For market orders, use a simulated price
        if order_type == "market":
            # Simulate market price (in real implementation, would query market data)
            exec_price = 100.0  # Placeholder price
        else:
            exec_price = price
        
        # Create order status
        order_status = OrderStatus(
            order_id=order_id,
            status="filled",  # Mock orders are immediately filled
            filled_quantity=quantity,
            remaining_quantity=0.0,
            avg_fill_price=exec_price,
            last_update=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # Store order
        self._mock_orders[order_id] = order_status
        
        # Update mock positions
        if action == "buy":
            if symbol in self._mock_positions:
                pos = self._mock_positions[symbol]
                total_cost = pos.avg_cost * pos.quantity + exec_price * quantity
                total_quantity = pos.quantity + quantity
                pos.quantity = total_quantity
                pos.avg_cost = total_cost / total_quantity
            else:
                self._mock_positions[symbol] = Position(
                    symbol=symbol,
                    quantity=quantity,
                    avg_cost=exec_price,
                    current_price=exec_price
                )
            # Deduct cash
            self._mock_cash -= exec_price * quantity
        else:  # sell
            if symbol in self._mock_positions:
                pos = self._mock_positions[symbol]
                pos.quantity -= quantity
                if pos.quantity <= 0:
                    del self._mock_positions[symbol]
            # Add cash
            self._mock_cash += exec_price * quantity
        
        # Create result
        result = OrderResult(
            order_id=order_id,
            symbol=symbol,
            quantity=quantity,
            order_type=order_type,
            status="filled",
            filled_quantity=quantity,
            avg_fill_price=exec_price,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            message="订单已成交"
        )
        
        self._logger.info(f"模拟订单已成交: {order_id}, {action} {symbol} x {quantity} @ {exec_price}")
        return result

    
    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel an order / 撤单
        
        Args:
            order_id: Order identifier / 订单标识符
        
        Returns:
            bool: True if cancellation successful / 撤单成功返回True
        
        Raises:
            SystemError: If not connected or cancellation fails / 未连接或撤单失败时抛出
        """
        if not self._connected:
            error_info = ErrorInfo(
                error_code="TRD0004",
                error_message_zh="未连接到券商，无法撤单",
                error_message_en="Not connected to broker, cannot cancel order",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.HIGH,
                technical_details="cancel_order called before connect",
                suggested_actions=[
                    "先调用 connect() 方法连接券商",
                    "检查连接状态"
                ],
                recoverable=True
            )
            self._logger.error(error_info.get_user_message())
            raise SystemError(error_info)
        
        try:
            self._logger.info(f"撤单: {order_id}")
            
            # For mock broker
            if self._broker == "mock":
                if order_id in self._mock_orders:
                    order = self._mock_orders[order_id]
                    if order.status == "pending":
                        order.status = "cancelled"
                        order.last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self._logger.info(f"模拟订单已撤销: {order_id}")
                        return True
                    else:
                        self._logger.warning(f"订单 {order_id} 状态为 {order.status}，无法撤销")
                        return False
                else:
                    self._logger.warning(f"订单 {order_id} 不存在")
                    return False
            
            # Placeholder for real broker
            raise NotImplementedError(f"券商 '{self._broker}' 的撤单功能尚未实现")
            
        except NotImplementedError as e:
            error_info = ErrorInfo(
                error_code="TRD0006",
                error_message_zh=f"撤单失败: {str(e)}",
                error_message_en=f"Failed to cancel order: {str(e)}",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.MEDIUM,
                technical_details=f"order_id={order_id}",
                suggested_actions=[
                    "检查订单ID是否正确",
                    "确认订单是否还可以撤销"
                ],
                recoverable=True,
                original_exception=e
            )
            self._logger.error(error_info.get_user_message(), exc_info=True)
            raise SystemError(error_info) from e
    
    def get_account_info(self) -> AccountInfo:
        """
        Get account information / 获取账户信息
        
        Returns:
            AccountInfo: Account information / 账户信息
        
        Raises:
            SystemError: If not connected or query fails / 未连接或查询失败时抛出
        """
        if not self._connected:
            error_info = ErrorInfo(
                error_code="TRD0004",
                error_message_zh="未连接到券商，无法查询账户信息",
                error_message_en="Not connected to broker, cannot get account info",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.HIGH,
                technical_details="get_account_info called before connect",
                suggested_actions=[
                    "先调用 connect() 方法连接券商",
                    "检查连接状态"
                ],
                recoverable=True
            )
            self._logger.error(error_info.get_user_message())
            raise SystemError(error_info)
        
        try:
            self._logger.debug("查询账户信息")
            
            # For mock broker
            if self._broker == "mock":
                # Calculate positions value
                positions_value = sum(
                    pos.quantity * pos.current_price
                    for pos in self._mock_positions.values()
                )
                
                # Calculate unrealized P&L
                unrealized_pnl = sum(
                    (pos.current_price - pos.avg_cost) * pos.quantity
                    for pos in self._mock_positions.values()
                )
                
                total_value = self._mock_cash + positions_value
                
                account_info = AccountInfo(
                    account_id=self._account_id,
                    broker=self._broker,
                    total_value=total_value,
                    cash_balance=self._mock_cash,
                    buying_power=self._mock_cash,  # Simplified
                    positions_value=positions_value,
                    unrealized_pnl=unrealized_pnl
                )
                
                self._logger.debug(f"账户信息: 总资产={total_value:.2f}, 现金={self._mock_cash:.2f}")
                return account_info
            
            # Placeholder for real broker
            raise NotImplementedError(f"券商 '{self._broker}' 的账户查询功能尚未实现")
            
        except NotImplementedError as e:
            error_info = ErrorInfo(
                error_code="TRD0007",
                error_message_zh=f"查询账户信息失败: {str(e)}",
                error_message_en=f"Failed to get account info: {str(e)}",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.MEDIUM,
                technical_details=str(e),
                suggested_actions=[
                    "检查网络连接",
                    "确认API权限是否正确"
                ],
                recoverable=True,
                original_exception=e
            )
            self._logger.error(error_info.get_user_message(), exc_info=True)
            raise SystemError(error_info) from e

    
    def get_positions(self) -> List[Position]:
        """
        Get current positions / 获取当前持仓
        
        Returns:
            List[Position]: List of positions / 持仓列表
        
        Raises:
            SystemError: If not connected or query fails / 未连接或查询失败时抛出
        """
        if not self._connected:
            error_info = ErrorInfo(
                error_code="TRD0004",
                error_message_zh="未连接到券商，无法查询持仓",
                error_message_en="Not connected to broker, cannot get positions",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.HIGH,
                technical_details="get_positions called before connect",
                suggested_actions=[
                    "先调用 connect() 方法连接券商",
                    "检查连接状态"
                ],
                recoverable=True
            )
            self._logger.error(error_info.get_user_message())
            raise SystemError(error_info)
        
        try:
            self._logger.debug("查询持仓")
            
            # For mock broker
            if self._broker == "mock":
                positions = list(self._mock_positions.values())
                self._logger.debug(f"持仓数量: {len(positions)}")
                return positions
            
            # Placeholder for real broker
            raise NotImplementedError(f"券商 '{self._broker}' 的持仓查询功能尚未实现")
            
        except NotImplementedError as e:
            error_info = ErrorInfo(
                error_code="TRD0008",
                error_message_zh=f"查询持仓失败: {str(e)}",
                error_message_en=f"Failed to get positions: {str(e)}",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.MEDIUM,
                technical_details=str(e),
                suggested_actions=[
                    "检查网络连接",
                    "确认API权限是否正确"
                ],
                recoverable=True,
                original_exception=e
            )
            self._logger.error(error_info.get_user_message(), exc_info=True)
            raise SystemError(error_info) from e
    
    def get_order_status(self, order_id: str) -> OrderStatus:
        """
        Get order status / 获取订单状态
        
        Args:
            order_id: Order identifier / 订单标识符
        
        Returns:
            OrderStatus: Order status / 订单状态
        
        Raises:
            SystemError: If not connected or query fails / 未连接或查询失败时抛出
        """
        if not self._connected:
            error_info = ErrorInfo(
                error_code="TRD0004",
                error_message_zh="未连接到券商，无法查询订单状态",
                error_message_en="Not connected to broker, cannot get order status",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.HIGH,
                technical_details="get_order_status called before connect",
                suggested_actions=[
                    "先调用 connect() 方法连接券商",
                    "检查连接状态"
                ],
                recoverable=True
            )
            self._logger.error(error_info.get_user_message())
            raise SystemError(error_info)
        
        try:
            self._logger.debug(f"查询订单状态: {order_id}")
            
            # For mock broker
            if self._broker == "mock":
                if order_id in self._mock_orders:
                    order_status = self._mock_orders[order_id]
                    self._logger.debug(f"订单 {order_id} 状态: {order_status.status}")
                    return order_status
                else:
                    error_info = ErrorInfo(
                        error_code="TRD0009",
                        error_message_zh=f"订单不存在: {order_id}",
                        error_message_en=f"Order not found: {order_id}",
                        category=ErrorCategory.SYSTEM,
                        severity=ErrorSeverity.MEDIUM,
                        technical_details=f"order_id={order_id}",
                        suggested_actions=[
                            "检查订单ID是否正确",
                            "确认订单是否已被删除"
                        ],
                        recoverable=True
                    )
                    self._logger.error(error_info.get_user_message())
                    raise SystemError(error_info)
            
            # Placeholder for real broker
            raise NotImplementedError(f"券商 '{self._broker}' 的订单查询功能尚未实现")
            
        except SystemError:
            raise
        except NotImplementedError as e:
            error_info = ErrorInfo(
                error_code="TRD0010",
                error_message_zh=f"查询订单状态失败: {str(e)}",
                error_message_en=f"Failed to get order status: {str(e)}",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.MEDIUM,
                technical_details=f"order_id={order_id}",
                suggested_actions=[
                    "检查网络连接",
                    "确认API权限是否正确"
                ],
                recoverable=True,
                original_exception=e
            )
            self._logger.error(error_info.get_user_message(), exc_info=True)
            raise SystemError(error_info) from e
    
    def get_broker_name(self) -> Optional[str]:
        """
        Get connected broker name / 获取已连接的券商名称
        
        Returns:
            Optional[str]: Broker name or None if not connected / 券商名称，未连接时返回None
        """
        return self._broker
    
    def get_account_id(self) -> Optional[str]:
        """
        Get account ID / 获取账户ID
        
        Returns:
            Optional[str]: Account ID or None if not connected / 账户ID，未连接时返回None
        """
        return self._account_id
