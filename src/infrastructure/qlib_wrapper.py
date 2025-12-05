"""
Qlib框架封装模块 / Qlib Framework Wrapper Module
提供统一的qlib接口，处理初始化、数据访问和异常转换
Provides unified qlib interface, handles initialization, data access, and exception conversion
"""

import pandas as pd
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime

from .logger_system import get_logger
from ..utils.error_handler import (
    DataError,
    SystemError,
    ErrorInfo,
    ErrorCategory,
    ErrorSeverity,
    get_error_handler
)

# 延迟导入qlib，避免在测试时因qlib未安装而失败
# 确保导入的是安装的qlib包，而不是本地的qlib目录
try:
    # 临时移除当前目录的父目录，避免导入冲突
    import sys
    original_path = sys.path.copy()
    # 移除可能导致冲突的路径
    sys.path = [p for p in sys.path if 'Code' not in p or 'QuantitationTranding' in p]
    
    import qlib
    
    # 恢复原始路径
    sys.path = original_path
    
    # 验证qlib是否正确导入（应该有init方法）
    if not hasattr(qlib, 'init'):
        # 如果没有init方法，说明导入了错误的qlib
        raise ImportError("Imported wrong qlib module (missing init method)")
    
    QLIB_AVAILABLE = True
except ImportError:
    QLIB_AVAILABLE = False
    qlib = None


# 移除旧的异常类，使用新的错误处理系统
# Removed old exception classes, using new error handling system
# 为了向后兼容，保留别名
QlibInitializationError = SystemError
QlibDataError = DataError


class QlibWrapper:
    """
    Qlib框架封装类
    
    职责:
    - 初始化qlib环境
    - 提供统一的数据访问接口
    - 处理qlib异常并转换为友好的错误信息
    """
    
    def __init__(self):
        """初始化QlibWrapper"""
        self._initialized = False
        self._provider_uri: Optional[str] = None
        self._region: Optional[str] = None
        self._logger = get_logger(__name__)
    
    def init(
        self,
        provider_uri: str,
        region: str = "cn",
        exp_manager_config: Optional[Dict[str, Any]] = None,
        auto_mount: bool = True
    ) -> None:
        """
        初始化qlib环境 / Initialize qlib environment
        
        Args:
            provider_uri: 数据提供者URI，通常是本地数据路径 / Data provider URI, usually local data path
            region: 市场区域，默认为"cn"（中国市场） / Market region, default is "cn" (China market)
            exp_manager_config: 实验管理器配置（可选） / Experiment manager config (optional)
            auto_mount: 是否自动挂载数据，默认为True / Whether to auto-mount data, default is True
            
        Raises:
            SystemError: 初始化失败时抛出 / Raised when initialization fails
        """
        # 检查qlib是否可用
        if not QLIB_AVAILABLE:
            error_info = ErrorInfo(
                error_code="SYS0001",
                error_message_zh="qlib未安装。请先安装qlib",
                error_message_en="qlib not installed. Please install qlib first",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.CRITICAL,
                technical_details="qlib module not found",
                suggested_actions=[
                    "安装qlib: pip install qlib",
                    "检查Python环境是否正确",
                    "确认qlib版本是否兼容"
                ],
                recoverable=False
            )
            self._logger.error(error_info.get_user_message())
            raise SystemError(error_info)
        
        try:
            # 展开用户路径
            provider_uri_path = Path(provider_uri).expanduser()
            
            # 检查数据路径是否存在
            if not provider_uri_path.exists():
                error_info = ErrorInfo(
                    error_code="DAT0008",
                    error_message_zh=f"数据路径不存在: {provider_uri_path}",
                    error_message_en=f"Data path does not exist: {provider_uri_path}",
                    category=ErrorCategory.DATA,
                    severity=ErrorSeverity.CRITICAL,
                    technical_details=f"Path: {provider_uri_path}",
                    suggested_actions=[
                        "下载qlib数据: python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn",
                        "检查数据路径配置是否正确",
                        "确认数据文件是否已被删除或移动"
                    ],
                    recoverable=True
                )
                self._logger.error(error_info.get_user_message())
                raise DataError(error_info)
            
            # 构建qlib初始化参数
            init_kwargs = {
                "provider_uri": str(provider_uri_path),
                "region": region,
            }
            
            # 如果提供了实验管理器配置，添加到参数中
            if exp_manager_config:
                init_kwargs["exp_manager"] = exp_manager_config
            
            # 如果需要自动挂载，添加mount参数
            if auto_mount:
                init_kwargs["mount_path"] = str(provider_uri_path)
            
            # 初始化qlib
            self._logger.info(f"正在初始化qlib - 数据路径: {provider_uri_path}, 区域: {region}")
            qlib.init(**init_kwargs)
            
            # 记录初始化状态
            self._initialized = True
            self._provider_uri = str(provider_uri_path)
            self._region = region
            
            self._logger.info("qlib初始化成功")
            
        except (SystemError, DataError):
            # 重新抛出我们自己的异常
            raise
        except Exception as e:
            error_info = ErrorInfo(
                error_code="SYS0002",
                error_message_zh=f"qlib初始化失败: {str(e)}",
                error_message_en=f"qlib initialization failed: {str(e)}",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.CRITICAL,
                technical_details=str(e),
                suggested_actions=[
                    "检查qlib版本是否兼容",
                    "验证数据文件格式是否正确",
                    "查看详细错误日志",
                    "尝试重新安装qlib"
                ],
                recoverable=False,
                original_exception=e
            )
            self._logger.error(error_info.get_user_message(), exc_info=True)
            raise SystemError(error_info)
    
    def get_data(
        self,
        instruments: str,
        fields: List[str],
        start_time: str,
        end_time: str,
        freq: str = "day"
    ) -> pd.DataFrame:
        """
        获取市场数据
        
        Args:
            instruments: 股票池，如"csi300"、"all"或具体股票代码
            fields: 需要获取的字段列表，如["$close", "$volume"]
            start_time: 开始时间，格式如"2020-01-01"
            end_time: 结束时间，格式如"2023-12-31"
            freq: 数据频率，默认为"day"（日线）
            
        Returns:
            pd.DataFrame: 市场数据
            
        Raises:
            QlibDataError: 数据访问失败时抛出
        """
        if not self._initialized:
            error_info = ErrorInfo(
                error_code="DAT0002",
                error_message_zh="qlib未初始化，请先调用init()方法",
                error_message_en="qlib not initialized, please call init() first",
                category=ErrorCategory.DATA,
                severity=ErrorSeverity.HIGH,
                technical_details="QlibWrapper.get_data called before initialization",
                suggested_actions=[
                    "调用 QlibWrapper.init() 方法初始化qlib",
                    "检查初始化流程是否正确执行"
                ],
                recoverable=True
            )
            raise QlibDataError(error_info)
        
        try:
            self._logger.debug(
                f"获取数据 - 股票池: {instruments}, 字段: {fields}, "
                f"时间范围: {start_time} 至 {end_time}, 频率: {freq}"
            )
            
            # 使用qlib的D模块获取数据
            from qlib.data import D
            
            data = D.features(
                instruments=instruments,
                fields=fields,
                start_time=start_time,
                end_time=end_time,
                freq=freq
            )
            
            if data is None or data.empty:
                self._logger.warning(
                    f"未获取到数据 - 股票池: {instruments}, "
                    f"时间范围: {start_time} 至 {end_time}"
                )
            else:
                self._logger.debug(f"成功获取数据，形状: {data.shape}")
            
            return data
            
        except Exception as e:
            error_info = ErrorInfo(
                error_code="DAT0003",
                error_message_zh=f"获取数据失败: {str(e)}",
                error_message_en=f"Failed to get data: {str(e)}",
                category=ErrorCategory.DATA,
                severity=ErrorSeverity.HIGH,
                technical_details=f"instruments={instruments}, fields={fields}, start_time={start_time}, end_time={end_time}, freq={freq}",
                suggested_actions=[
                    "检查股票池名称是否正确",
                    "验证时间范围是否在数据覆盖范围内",
                    "确认字段名称是否正确"
                ],
                recoverable=True,
                original_exception=e
            )
            self._logger.error(error_info.get_user_message(), exc_info=True)
            raise QlibDataError(error_info) from e
    
    def get_instruments(
        self,
        market: str = "all",
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> List[str]:
        """
        获取股票列表
        
        Args:
            market: 市场或股票池，如"csi300"、"all"
            start_time: 开始时间（可选）
            end_time: 结束时间（可选）
            
        Returns:
            List[str]: 股票代码列表
            
        Raises:
            QlibDataError: 获取失败时抛出
        """
        if not self._initialized:
            error_info = ErrorInfo(
                error_code="DAT0002",
                error_message_zh="qlib未初始化，请先调用init()方法",
                error_message_en="qlib not initialized, please call init() first",
                category=ErrorCategory.DATA,
                severity=ErrorSeverity.HIGH,
                technical_details="QlibWrapper.get_instruments called before initialization",
                suggested_actions=[
                    "调用 QlibWrapper.init() 方法初始化qlib",
                    "检查初始化流程是否正确执行"
                ],
                recoverable=True
            )
            raise QlibDataError(error_info)
        
        try:
            from qlib.data import D
            
            instruments = D.instruments(
                market=market,
                start_time=start_time,
                end_time=end_time
            )
            
            self._logger.debug(f"获取到 {len(instruments)} 只股票")
            return instruments
            
        except Exception as e:
            error_info = ErrorInfo(
                error_code="DAT0004",
                error_message_zh=f"获取股票列表失败: {str(e)}",
                error_message_en=f"Failed to get instruments: {str(e)}",
                category=ErrorCategory.DATA,
                severity=ErrorSeverity.MEDIUM,
                technical_details=f"market={market}, start_time={start_time}, end_time={end_time}",
                suggested_actions=[
                    "检查市场名称是否正确",
                    "验证时间范围是否有效"
                ],
                recoverable=True,
                original_exception=e
            )
            self._logger.error(error_info.get_user_message(), exc_info=True)
            raise QlibDataError(error_info) from e
    
    def get_calendar(
        self,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        freq: str = "day"
    ) -> List[pd.Timestamp]:
        """
        获取交易日历
        
        Args:
            start_time: 开始时间（可选）
            end_time: 结束时间（可选）
            freq: 频率，默认为"day"
            
        Returns:
            List[pd.Timestamp]: 交易日列表
            
        Raises:
            QlibDataError: 获取失败时抛出
        """
        if not self._initialized:
            error_info = ErrorInfo(
                error_code="DAT0002",
                error_message_zh="qlib未初始化，请先调用init()方法",
                error_message_en="qlib not initialized, please call init() first",
                category=ErrorCategory.DATA,
                severity=ErrorSeverity.HIGH,
                technical_details="QlibWrapper.get_calendar called before initialization",
                suggested_actions=[
                    "调用 QlibWrapper.init() 方法初始化qlib",
                    "检查初始化流程是否正确执行"
                ],
                recoverable=True
            )
            raise QlibDataError(error_info)
        
        try:
            from qlib.data import D
            
            calendar = D.calendar(
                start_time=start_time,
                end_time=end_time,
                freq=freq
            )
            
            self._logger.debug(f"获取到 {len(calendar)} 个交易日")
            return calendar
            
        except Exception as e:
            error_info = ErrorInfo(
                error_code="DAT0005",
                error_message_zh=f"获取交易日历失败: {str(e)}",
                error_message_en=f"Failed to get calendar: {str(e)}",
                category=ErrorCategory.DATA,
                severity=ErrorSeverity.MEDIUM,
                technical_details=f"start_time={start_time}, end_time={end_time}, freq={freq}",
                suggested_actions=[
                    "检查时间范围是否有效",
                    "验证频率参数是否正确"
                ],
                recoverable=True,
                original_exception=e
            )
            self._logger.error(error_info.get_user_message(), exc_info=True)
            raise QlibDataError(error_info) from e
    
    def validate_data(
        self,
        instruments: str = "csi300",
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> Tuple[bool, str, Optional[Tuple[str, str]]]:
        """
        验证数据可用性
        
        Args:
            instruments: 股票池，默认为"csi300"
            start_time: 开始时间（可选）
            end_time: 结束时间（可选）
            
        Returns:
            Tuple[bool, str, Optional[Tuple[str, str]]]: 
                (是否可用, 消息, 数据时间范围(开始, 结束))
        """
        if not self._initialized:
            return False, "qlib未初始化", None
        
        try:
            # 获取交易日历以验证数据
            calendar = self.get_calendar(start_time=start_time, end_time=end_time)
            
            if not calendar:
                return False, "未找到交易日数据", None
            
            # 获取数据时间范围
            data_start = calendar[0].strftime("%Y-%m-%d")
            data_end = calendar[-1].strftime("%Y-%m-%d")
            
            # 尝试获取一些数据以验证
            test_data = self.get_data(
                instruments=instruments,
                fields=["$close"],
                start_time=data_start,
                end_time=data_end
            )
            
            if test_data is None or test_data.empty:
                return False, f"数据为空 - 股票池: {instruments}", (data_start, data_end)
            
            message = (
                f"数据验证成功\n"
                f"数据时间范围: {data_start} 至 {data_end}\n"
                f"交易日数量: {len(calendar)}\n"
                f"测试数据形状: {test_data.shape}"
            )
            
            self._logger.info(message)
            return True, message, (data_start, data_end)
            
        except Exception as e:
            error_msg = f"数据验证失败: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            return False, error_msg, None
    
    def is_initialized(self) -> bool:
        """
        检查qlib是否已初始化
        
        Returns:
            bool: 如果已初始化返回True，否则返回False
        """
        return self._initialized
    
    def get_provider_uri(self) -> Optional[str]:
        """
        获取数据提供者URI
        
        Returns:
            Optional[str]: 数据路径，如果未初始化则返回None
        """
        return self._provider_uri
    
    def get_region(self) -> Optional[str]:
        """
        获取市场区域
        
        Returns:
            Optional[str]: 市场区域，如果未初始化则返回None
        """
        return self._region
    
    def get_data_info(self) -> Dict[str, Any]:
        """
        获取数据信息
        
        Returns:
            Dict[str, Any]: 数据信息字典，包含路径、区域、时间范围等
            
        Raises:
            QlibDataError: 如果未初始化或获取失败
        """
        if not self._initialized:
            error_info = ErrorInfo(
                error_code="DAT0002",
                error_message_zh="qlib未初始化，请先调用init()方法",
                error_message_en="qlib not initialized, please call init() first",
                category=ErrorCategory.DATA,
                severity=ErrorSeverity.HIGH,
                technical_details="QlibWrapper.get_data_info called before initialization",
                suggested_actions=[
                    "调用 QlibWrapper.init() 方法初始化qlib",
                    "检查初始化流程是否正确执行"
                ],
                recoverable=True
            )
            raise QlibDataError(error_info)
        
        try:
            # 获取交易日历
            calendar = self.get_calendar()
            
            if not calendar:
                error_info = ErrorInfo(
                    error_code="DAT0006",
                    error_message_zh="无法获取交易日历",
                    error_message_en="Failed to get calendar",
                    category=ErrorCategory.DATA,
                    severity=ErrorSeverity.HIGH,
                    technical_details="Calendar is empty",
                    suggested_actions=[
                        "检查数据是否正确下载",
                        "验证数据路径是否正确"
                    ],
                    recoverable=True
                )
                raise QlibDataError(error_info)
            
            data_start = calendar[0].strftime("%Y-%m-%d")
            data_end = calendar[-1].strftime("%Y-%m-%d")
            
            info = {
                "provider_uri": self._provider_uri,
                "region": self._region,
                "data_start": data_start,
                "data_end": data_end,
                "trading_days": len(calendar),
                "initialized": self._initialized
            }
            
            return info
            
        except QlibDataError:
            # 重新抛出我们自己的异常
            raise
        except Exception as e:
            error_info = ErrorInfo(
                error_code="DAT0007",
                error_message_zh=f"获取数据信息失败: {str(e)}",
                error_message_en=f"Failed to get data info: {str(e)}",
                category=ErrorCategory.DATA,
                severity=ErrorSeverity.MEDIUM,
                technical_details=str(e),
                suggested_actions=[
                    "检查qlib是否正确初始化",
                    "验证数据文件是否完整"
                ],
                recoverable=True,
                original_exception=e
            )
            self._logger.error(error_info.get_user_message(), exc_info=True)
            raise QlibDataError(error_info) from e
