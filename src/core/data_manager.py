"""
数据管理器模块 / Data Manager Module
负责数据下载、验证、完整性检查和缺失值处理
Responsible for data download, validation, integrity check, and missing value handling
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any, Tuple, List
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from ..infrastructure.logger_system import get_logger
from ..infrastructure.qlib_wrapper import QlibWrapper, QlibDataError
from ..utils.error_handler import (
    DataError,
    ErrorInfo,
    ErrorCategory,
    ErrorSeverity,
    error_handler_decorator,
    get_error_handler
)
from ..utils.cache_manager import get_cache_manager


class MissingValueStrategy(Enum):
    """缺失值处理策略"""
    FORWARD_FILL = "ffill"  # 前向填充
    BACKWARD_FILL = "bfill"  # 后向填充
    MEAN = "mean"  # 均值填充
    ZERO = "zero"  # 零填充
    DROP = "drop"  # 删除


@dataclass
class ValidationResult:
    """数据验证结果"""
    is_valid: bool
    message: str
    data_start: Optional[str] = None
    data_end: Optional[str] = None
    trading_days: Optional[int] = None
    issues: List[str] = None
    
    def __post_init__(self):
        if self.issues is None:
            self.issues = []


@dataclass
class DataInfo:
    """数据信息"""
    provider_uri: str
    region: str
    data_start: str
    data_end: str
    trading_days: int
    instruments_count: Optional[int] = None
    last_updated: Optional[str] = None


# 移除旧的异常类，使用新的错误处理系统
# Removed old exception class, using new error handling system


class DataManager:
    """
    数据管理器
    
    职责:
    - 初始化qlib数据
    - 下载和更新数据
    - 验证数据完整性
    - 处理缺失值
    """
    
    def __init__(self, qlib_wrapper: Optional[QlibWrapper] = None, enable_cache: bool = True):
        """
        初始化数据管理器
        
        Args:
            qlib_wrapper: QlibWrapper实例，如果为None则创建新实例
            enable_cache: 是否启用缓存 / Whether to enable cache
        """
        self._qlib_wrapper = qlib_wrapper or QlibWrapper()
        self._logger = get_logger(__name__)
        self._initialized = False
        self._enable_cache = enable_cache
        # 限制内存缓存大小为50个条目，避免内存泄漏
        self._cache_manager = get_cache_manager(max_memory_items=50) if enable_cache else None
    
    def initialize(
        self,
        data_path: str,
        region: str = "cn",
        auto_mount: bool = True
    ) -> None:
        """
        初始化qlib数据环境 / Initialize qlib data environment
        
        Args:
            data_path: 数据路径 / Data path
            region: 市场区域，默认为"cn" / Market region, default is "cn"
            auto_mount: 是否自动挂载数据 / Whether to auto-mount data
            
        Raises:
            DataError: 初始化失败时抛出 / Raised when initialization fails
        """
        try:
            self._logger.info(f"初始化数据管理器 - 数据路径: {data_path}, 区域: {region}")
            
            # 初始化qlib
            self._qlib_wrapper.init(
                provider_uri=data_path,
                region=region,
                auto_mount=auto_mount
            )
            
            self._initialized = True
            self._logger.info("数据管理器初始化成功")
            
        except Exception as e:
            error_info = ErrorInfo(
                error_code="DAT0001",
                error_message_zh=f"数据管理器初始化失败: {str(e)}",
                error_message_en=f"Data manager initialization failed: {str(e)}",
                category=ErrorCategory.DATA,
                severity=ErrorSeverity.CRITICAL,
                technical_details=str(e),
                suggested_actions=[
                    "检查数据路径是否存在且可访问",
                    "确认qlib是否正确安装",
                    "验证数据文件是否完整",
                    "尝试重新下载数据"
                ],
                recoverable=True,
                original_exception=e
            )
            self._logger.error(error_info.get_user_message(), exc_info=True)
            raise DataError(error_info)
    
    def download_data(
        self,
        region: str,
        target_dir: str,
        interval: str = "1d",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> None:
        """
        下载市场数据 / Download market data
        
        Args:
            region: 市场区域 (cn, us等) / Market region (cn, us, etc.)
            target_dir: 目标目录 / Target directory
            interval: 数据间隔，默认为"1d"（日线） / Data interval, default is "1d" (daily)
            start_date: 开始日期（可选） / Start date (optional)
            end_date: 结束日期（可选） / End date (optional)
            
        Raises:
            DataError: 下载失败时抛出 / Raised when download fails
        """
        try:
            self._logger.info(
                f"开始下载数据 - 区域: {region}, 目标目录: {target_dir}, "
                f"间隔: {interval}"
            )
            
            # 确保目标目录存在
            target_path = Path(target_dir).expanduser()
            target_path.mkdir(parents=True, exist_ok=True)
            
            # 使用qlib的数据下载工具
            try:
                from qlib.data import D
                from qlib.utils import get_or_create_path
                
                # 这里使用qlib的命令行工具进行数据下载
                # 实际实现中，应该调用qlib的数据下载API
                # 由于qlib的数据下载API可能因版本而异，这里提供一个通用的实现框架
                
                self._logger.info(
                    f"请使用以下命令下载数据:\n"
                    f"python -m qlib.run.get_data qlib_data "
                    f"--target_dir {target_path} --region {region} --interval {interval}"
                )
                
                # 注意：实际的数据下载需要根据qlib的具体版本和API来实现
                # 这里提供一个占位实现
                self._logger.warning(
                    "数据下载功能需要手动执行qlib的数据下载命令。"
                    "请参考qlib文档进行数据下载。"
                )
                
            except ImportError as e:
                error_info = ErrorInfo(
                    error_code="DAT0002",
                    error_message_zh=f"qlib未正确安装: {str(e)}",
                    error_message_en=f"qlib not properly installed: {str(e)}",
                    category=ErrorCategory.DATA,
                    severity=ErrorSeverity.CRITICAL,
                    technical_details=str(e),
                    suggested_actions=[
                        "安装qlib: pip install qlib",
                        "检查Python环境是否正确",
                        "确认qlib版本是否兼容"
                    ],
                    recoverable=False,
                    original_exception=e
                )
                raise DataError(error_info)
            
        except DataError:
            raise
        except Exception as e:
            error_info = ErrorInfo(
                error_code="DAT0003",
                error_message_zh=f"数据下载失败: {str(e)}",
                error_message_en=f"Data download failed: {str(e)}",
                category=ErrorCategory.DATA,
                severity=ErrorSeverity.HIGH,
                technical_details=str(e),
                suggested_actions=[
                    "检查网络连接是否正常",
                    "确认目标目录是否有写入权限",
                    "验证区域参数是否正确",
                    "稍后重试"
                ],
                recoverable=True,
                original_exception=e
            )
            self._logger.error(error_info.get_user_message(), exc_info=True)
            raise DataError(error_info)
    
    def validate_data(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        instruments: str = "csi300"
    ) -> ValidationResult:
        """
        验证数据完整性和格式
        
        Args:
            start_date: 开始日期（可选）
            end_date: 结束日期（可选）
            instruments: 股票池，默认为"csi300"
            
        Returns:
            ValidationResult: 验证结果
        """
        if not self._initialized:
            return ValidationResult(
                is_valid=False,
                message="数据管理器未初始化",
                issues=["数据管理器未初始化，请先调用initialize()方法"]
            )
        
        # 尝试从缓存获取验证结果
        if self._enable_cache and self._cache_manager:
            cache_key = f"validate_{instruments}_{start_date}_{end_date}"
            cached_result = self._cache_manager.get(cache_key)
            if cached_result is not None:
                self._logger.debug(f"使用缓存的验证结果: {cache_key}")
                return cached_result
        
        try:
            self._logger.info(
                f"开始验证数据 - 时间范围: {start_date} 至 {end_date}, "
                f"股票池: {instruments}"
            )
            
            issues = []
            
            # 使用qlib_wrapper验证数据
            is_valid, message, time_range = self._qlib_wrapper.validate_data(
                instruments=instruments,
                start_time=start_date,
                end_time=end_date
            )
            
            if not is_valid:
                issues.append(message)
                return ValidationResult(
                    is_valid=False,
                    message=message,
                    issues=issues
                )
            
            # 提取时间范围
            data_start, data_end = time_range if time_range else (None, None)
            
            # 获取交易日数量
            calendar = self._qlib_wrapper.get_calendar(
                start_time=start_date or data_start,
                end_time=end_date or data_end
            )
            trading_days = len(calendar) if calendar else 0
            
            # 检查数据完整性
            if trading_days == 0:
                issues.append("未找到交易日数据")
                return ValidationResult(
                    is_valid=False,
                    message="数据验证失败：未找到交易日数据",
                    data_start=data_start,
                    data_end=data_end,
                    trading_days=0,
                    issues=issues
                )
            
            # 尝试获取样本数据以验证数据质量
            try:
                sample_data = self._qlib_wrapper.get_data(
                    instruments=instruments,
                    fields=["$close", "$volume"],
                    start_time=start_date or data_start,
                    end_time=end_date or data_end
                )
                
                if sample_data is None or sample_data.empty:
                    issues.append("样本数据为空")
                else:
                    # 检查缺失值
                    missing_ratio = sample_data.isnull().sum().sum() / (sample_data.shape[0] * sample_data.shape[1])
                    if missing_ratio > 0.5:
                        issues.append(f"数据缺失率过高: {missing_ratio:.2%}")
                    elif missing_ratio > 0.1:
                        issues.append(f"数据存在缺失值: {missing_ratio:.2%}")
                    
            except Exception as e:
                issues.append(f"样本数据获取失败: {str(e)}")
            
            # 构建验证结果
            if issues:
                result = ValidationResult(
                    is_valid=False,
                    message=f"数据验证发现问题: {'; '.join(issues)}",
                    data_start=data_start,
                    data_end=data_end,
                    trading_days=trading_days,
                    issues=issues
                )
            else:
                result = ValidationResult(
                    is_valid=True,
                    message=f"数据验证通过 - 时间范围: {data_start} 至 {data_end}, 交易日: {trading_days}",
                    data_start=data_start,
                    data_end=data_end,
                    trading_days=trading_days,
                    issues=[]
                )
            
            self._logger.info(result.message)
            
            # 缓存验证结果（TTL: 1小时）
            if self._enable_cache and self._cache_manager:
                cache_key = f"validate_{instruments}_{start_date}_{end_date}"
                self._cache_manager.set(cache_key, result, ttl=3600)
            
            return result
            
        except Exception as e:
            error_msg = f"数据验证失败: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            return ValidationResult(
                is_valid=False,
                message=error_msg,
                issues=[error_msg]
            )
    
    def handle_missing_values(
        self,
        data: pd.DataFrame,
        strategy: MissingValueStrategy = MissingValueStrategy.FORWARD_FILL,
        fill_value: Optional[float] = None
    ) -> pd.DataFrame:
        """
        处理数据中的缺失值 / Handle missing values in data
        
        Args:
            data: 包含缺失值的数据 / Data containing missing values
            strategy: 缺失值处理策略 / Missing value handling strategy
            fill_value: 填充值（当strategy为ZERO时使用） / Fill value (used when strategy is ZERO)
            
        Returns:
            pd.DataFrame: 处理后的数据 / Processed data
            
        Raises:
            DataError: 处理失败时抛出 / Raised when processing fails
        """
        try:
            self._logger.info(f"处理缺失值 - 策略: {strategy.value}")
            
            if data is None or data.empty:
                self._logger.warning("输入数据为空，无需处理缺失值")
                return data
            
            # 记录原始缺失值数量
            missing_count_before = data.isnull().sum().sum()
            self._logger.info(f"原始缺失值数量: {missing_count_before}")
            
            if missing_count_before == 0:
                self._logger.info("数据中没有缺失值")
                return data
            
            # 根据策略处理缺失值
            if strategy == MissingValueStrategy.FORWARD_FILL:
                result = data.fillna(method='ffill')
            elif strategy == MissingValueStrategy.BACKWARD_FILL:
                result = data.fillna(method='bfill')
            elif strategy == MissingValueStrategy.MEAN:
                result = data.fillna(data.mean())
            elif strategy == MissingValueStrategy.ZERO:
                result = data.fillna(fill_value if fill_value is not None else 0)
            elif strategy == MissingValueStrategy.DROP:
                result = data.dropna()
            else:
                error_info = ErrorInfo(
                    error_code="DAT0004",
                    error_message_zh=f"不支持的缺失值处理策略: {strategy}",
                    error_message_en=f"Unsupported missing value strategy: {strategy}",
                    category=ErrorCategory.DATA,
                    severity=ErrorSeverity.MEDIUM,
                    technical_details=f"Strategy: {strategy}",
                    suggested_actions=[
                        "使用支持的策略: FORWARD_FILL, BACKWARD_FILL, MEAN, ZERO, DROP",
                        "检查策略参数是否正确"
                    ],
                    recoverable=False
                )
                raise DataError(error_info)
            
            # 记录处理后的缺失值数量
            missing_count_after = result.isnull().sum().sum()
            self._logger.info(
                f"缺失值处理完成 - 处理前: {missing_count_before}, "
                f"处理后: {missing_count_after}"
            )
            
            return result
            
        except DataError:
            raise
        except Exception as e:
            error_info = ErrorInfo(
                error_code="DAT0005",
                error_message_zh=f"缺失值处理失败: {str(e)}",
                error_message_en=f"Missing value handling failed: {str(e)}",
                category=ErrorCategory.DATA,
                severity=ErrorSeverity.MEDIUM,
                technical_details=str(e),
                suggested_actions=[
                    "检查数据格式是否正确",
                    "验证数据类型是否支持所选策略",
                    "尝试使用其他处理策略"
                ],
                recoverable=True,
                original_exception=e
            )
            self._logger.error(error_info.get_user_message(), exc_info=True)
            raise DataError(error_info)
    
    def get_data_info(self) -> DataInfo:
        """
        获取数据信息 / Get data information
        
        Returns:
            DataInfo: 数据信息对象 / Data information object
            
        Raises:
            DataError: 获取失败时抛出 / Raised when retrieval fails
        """
        if not self._initialized:
            error_info = ErrorInfo(
                error_code="DAT0006",
                error_message_zh="数据管理器未初始化，请先调用initialize()方法",
                error_message_en="Data manager not initialized, please call initialize() first",
                category=ErrorCategory.DATA,
                severity=ErrorSeverity.HIGH,
                technical_details="DataManager.initialize() not called",
                suggested_actions=[
                    "调用 initialize() 方法初始化数据管理器",
                    "检查初始化流程是否正确执行"
                ],
                recoverable=True
            )
            raise DataError(error_info)
        
        try:
            # 从qlib_wrapper获取数据信息
            info_dict = self._qlib_wrapper.get_data_info()
            
            # 尝试获取股票数量
            instruments_count = None
            try:
                instruments = self._qlib_wrapper.get_instruments(market="all")
                instruments_count = len(instruments) if instruments else None
            except Exception as e:
                self._logger.warning(f"获取股票数量失败: {str(e)}")
            
            # 构建DataInfo对象
            data_info = DataInfo(
                provider_uri=info_dict["provider_uri"],
                region=info_dict["region"],
                data_start=info_dict["data_start"],
                data_end=info_dict["data_end"],
                trading_days=info_dict["trading_days"],
                instruments_count=instruments_count,
                last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
            self._logger.info(
                f"数据信息 - 时间范围: {data_info.data_start} 至 {data_info.data_end}, "
                f"交易日: {data_info.trading_days}, 股票数: {data_info.instruments_count}"
            )
            
            return data_info
            
        except DataError:
            raise
        except Exception as e:
            error_info = ErrorInfo(
                error_code="DAT0007",
                error_message_zh=f"获取数据信息失败: {str(e)}",
                error_message_en=f"Failed to get data information: {str(e)}",
                category=ErrorCategory.DATA,
                severity=ErrorSeverity.MEDIUM,
                technical_details=str(e),
                suggested_actions=[
                    "检查数据是否正确初始化",
                    "验证数据文件是否完整",
                    "尝试重新初始化数据管理器"
                ],
                recoverable=True,
                original_exception=e
            )
            self._logger.error(error_info.get_user_message(), exc_info=True)
            raise DataError(error_info)
    
    def check_data_coverage(
        self,
        required_start: str,
        required_end: str,
        instruments: str = "csi300"
    ) -> Tuple[bool, str]:
        """
        检查数据是否覆盖所需的时间范围
        
        Args:
            required_start: 所需的开始日期
            required_end: 所需的结束日期
            instruments: 股票池
            
        Returns:
            Tuple[bool, str]: (是否覆盖, 消息)
        """
        if not self._initialized:
            return False, "数据管理器未初始化"
        
        try:
            # 获取数据信息
            data_info = self.get_data_info()
            
            # 比较日期
            data_start = datetime.strptime(data_info.data_start, "%Y-%m-%d")
            data_end = datetime.strptime(data_info.data_end, "%Y-%m-%d")
            req_start = datetime.strptime(required_start, "%Y-%m-%d")
            req_end = datetime.strptime(required_end, "%Y-%m-%d")
            
            if data_start <= req_start and data_end >= req_end:
                message = (
                    f"数据覆盖检查通过\n"
                    f"所需范围: {required_start} 至 {required_end}\n"
                    f"数据范围: {data_info.data_start} 至 {data_info.data_end}"
                )
                self._logger.info(message)
                return True, message
            else:
                message = (
                    f"数据覆盖不足\n"
                    f"所需范围: {required_start} 至 {required_end}\n"
                    f"数据范围: {data_info.data_start} 至 {data_info.data_end}"
                )
                self._logger.warning(message)
                return False, message
                
        except Exception as e:
            error_msg = f"数据覆盖检查失败: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            return False, error_msg
    
    def is_initialized(self) -> bool:
        """
        检查数据管理器是否已初始化
        
        Returns:
            bool: 如果已初始化返回True，否则返回False
        """
        return self._initialized
    
    @property
    def qlib_wrapper(self) -> QlibWrapper:
        """获取QlibWrapper实例"""
        return self._qlib_wrapper
    
    def clear_cache(self) -> None:
        """
        清理缓存以释放内存 / Clear cache to free memory
        """
        if self._cache_manager:
            count = self._cache_manager.clear()
            self._logger.info(f"已清理 {count} 个缓存条目")
        else:
            self._logger.warning("缓存未启用，无需清理")
