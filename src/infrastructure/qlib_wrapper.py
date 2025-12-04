"""
Qlib框架封装模块
提供统一的qlib接口，处理初始化、数据访问和异常转换
"""

import pandas as pd
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime

from .logger_system import get_logger

# 延迟导入qlib，避免在测试时因qlib未安装而失败
try:
    import qlib
    QLIB_AVAILABLE = True
except ImportError:
    QLIB_AVAILABLE = False
    qlib = None


class QlibInitializationError(Exception):
    """Qlib初始化错误"""
    pass


class QlibDataError(Exception):
    """Qlib数据访问错误"""
    pass


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
        初始化qlib环境
        
        Args:
            provider_uri: 数据提供者URI，通常是本地数据路径
            region: 市场区域，默认为"cn"（中国市场）
            exp_manager_config: 实验管理器配置（可选）
            auto_mount: 是否自动挂载数据，默认为True
            
        Raises:
            QlibInitializationError: 初始化失败时抛出
        """
        # 检查qlib是否可用
        if not QLIB_AVAILABLE:
            error_msg = (
                "qlib未安装。请先安装qlib:\n"
                "pip install qlib"
            )
            self._logger.error(error_msg)
            raise QlibInitializationError(error_msg)
        
        try:
            # 展开用户路径
            provider_uri_path = Path(provider_uri).expanduser()
            
            # 检查数据路径是否存在
            if not provider_uri_path.exists():
                error_msg = (
                    f"数据路径不存在: {provider_uri_path}\n"
                    f"请先下载qlib数据。您可以使用以下命令下载数据:\n"
                    f"python scripts/get_data.py qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn"
                )
                self._logger.error(error_msg)
                raise QlibInitializationError(error_msg)
            
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
            
        except QlibInitializationError:
            # 重新抛出我们自己的异常
            raise
        except Exception as e:
            error_msg = f"qlib初始化失败: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise QlibInitializationError(error_msg) from e
    
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
            raise QlibDataError("qlib未初始化，请先调用init()方法")
        
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
            error_msg = (
                f"获取数据失败: {str(e)}\n"
                f"参数: instruments={instruments}, fields={fields}, "
                f"start_time={start_time}, end_time={end_time}, freq={freq}"
            )
            self._logger.error(error_msg, exc_info=True)
            raise QlibDataError(error_msg) from e
    
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
            raise QlibDataError("qlib未初始化，请先调用init()方法")
        
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
            error_msg = f"获取股票列表失败: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise QlibDataError(error_msg) from e
    
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
            raise QlibDataError("qlib未初始化，请先调用init()方法")
        
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
            error_msg = f"获取交易日历失败: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise QlibDataError(error_msg) from e
    
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
            raise QlibDataError("qlib未初始化，请先调用init()方法")
        
        try:
            # 获取交易日历
            calendar = self.get_calendar()
            
            if not calendar:
                raise QlibDataError("无法获取交易日历")
            
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
            
        except Exception as e:
            error_msg = f"获取数据信息失败: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise QlibDataError(error_msg) from e
