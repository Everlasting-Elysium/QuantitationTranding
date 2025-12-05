"""
Configuration Manager for Qlib Trading System
配置管理器 - 负责加载、验证和管理系统配置
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict

from ..utils.error_handler import (
    ConfigurationError,
    ErrorInfo,
    ErrorCategory,
    ErrorSeverity,
    error_handler_decorator,
    get_error_handler
)


@dataclass
class QlibConfig:
    """Qlib配置"""
    provider_uri: str
    region: str
    auto_mount: bool = True


@dataclass
class MLflowConfig:
    """MLflow配置"""
    tracking_uri: str
    experiment_name: str
    artifact_location: Optional[str] = None


@dataclass
class DataConfig:
    """数据配置"""
    instruments: str
    start_time: str
    end_time: str
    features: List[str]
    label: str


@dataclass
class TrainingConfig:
    """训练配置"""
    train_start: str
    train_end: str
    valid_start: str
    valid_end: str
    test_start: str
    test_end: str


@dataclass
class BacktestStrategyConfig:
    """回测策略配置"""
    topk: int
    n_drop: int


@dataclass
class BacktestExecutorConfig:
    """回测执行器配置"""
    time_per_step: str
    generate_portfolio_metrics: bool


@dataclass
class BacktestConfig:
    """回测配置"""
    strategy: BacktestStrategyConfig
    executor: BacktestExecutorConfig
    benchmark: str


@dataclass
class RiskLimits:
    """风险限制配置"""
    max_position_per_stock: float
    max_sector_exposure: float


@dataclass
class SignalConfig:
    """信号生成配置"""
    top_k: int
    risk_limits: RiskLimits


@dataclass
class ModelRegistryConfig:
    """模型注册表配置"""
    storage_path: str
    auto_register: bool


@dataclass
class LoggingConfig:
    """日志配置"""
    log_dir: str
    log_level: str
    log_format: str
    max_bytes: int
    backup_count: int


@dataclass
class VisualizationConfig:
    """可视化配置"""
    output_dir: str
    figure_format: str
    dpi: int
    style: str


@dataclass
class CLIConfig:
    """CLI配置"""
    language: str
    show_progress: bool
    confirm_actions: bool


@dataclass
class Config:
    """系统总配置"""
    qlib: QlibConfig
    mlflow: MLflowConfig
    data: DataConfig
    training: TrainingConfig
    backtest: BacktestConfig
    signal: SignalConfig
    model_registry: ModelRegistryConfig
    logging: LoggingConfig
    visualization: VisualizationConfig
    cli: CLIConfig


class ConfigManager:
    """
    配置管理器
    
    职责:
    - 加载和保存配置文件
    - 验证配置有效性
    - 提供默认配置
    """
    
    def __init__(self):
        """初始化配置管理器"""
        self._config: Optional[Config] = None
    
    def load_config(self, config_path: str) -> Config:
        """
        从YAML文件加载配置 / Load configuration from YAML file
        
        Args:
            config_path: 配置文件路径 / Configuration file path
            
        Returns:
            Config: 配置对象 / Configuration object
            
        Raises:
            ConfigurationError: 配置加载失败时抛出 / Raised when configuration loading fails
        """
        try:
            config_path = Path(config_path).expanduser()
            
            if not config_path.exists():
                error_info = ErrorInfo(
                    error_code="CFG0001",
                    error_message_zh=f"配置文件不存在: {config_path}",
                    error_message_en=f"Configuration file not found: {config_path}",
                    category=ErrorCategory.CONFIGURATION,
                    severity=ErrorSeverity.HIGH,
                    technical_details=f"File path: {config_path}",
                    suggested_actions=[
                        "检查配置文件路径是否正确",
                        "使用 get_default_config() 创建默认配置",
                        "确认配置文件是否已被删除或移动"
                    ],
                    recoverable=True
                )
                raise ConfigurationError(error_info)
            
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_dict = yaml.safe_load(f)
            except yaml.YAMLError as e:
                error_info = ErrorInfo(
                    error_code="CFG0002",
                    error_message_zh=f"配置文件格式错误: {str(e)}",
                    error_message_en=f"Configuration file format error: {str(e)}",
                    category=ErrorCategory.CONFIGURATION,
                    severity=ErrorSeverity.HIGH,
                    technical_details=f"YAML parsing error: {str(e)}",
                    suggested_actions=[
                        "检查YAML文件格式是否正确",
                        "确认缩进是否使用空格而非制表符",
                        "使用YAML验证工具检查文件",
                        "参考示例配置文件"
                    ],
                    recoverable=False,
                    original_exception=e
                )
                raise ConfigurationError(error_info)
            
            # 解析配置
            config = self._parse_config(config_dict)
            
            # 验证配置
            errors = self.validate_config(config)
            if errors:
                error_msg = "\n".join(errors)
                error_info = ErrorInfo(
                    error_code="CFG0003",
                    error_message_zh=f"配置验证失败:\n{error_msg}",
                    error_message_en=f"Configuration validation failed:\n{error_msg}",
                    category=ErrorCategory.CONFIGURATION,
                    severity=ErrorSeverity.HIGH,
                    technical_details=error_msg,
                    suggested_actions=[
                        "检查配置文件中的所有必需字段",
                        "验证配置值的类型和范围",
                        "参考文档了解正确的配置格式",
                        "使用 validate_config() 方法检查具体错误"
                    ],
                    recoverable=True
                )
                raise ConfigurationError(error_info)
            
            self._config = config
            return config
            
        except ConfigurationError:
            raise
        except Exception as e:
            error_handler = get_error_handler()
            error_handler.handle_error(e, {"config_path": str(config_path)})
    
    def save_config(self, config: Config, config_path: str) -> None:
        """
        保存配置到YAML文件
        
        Args:
            config: 配置对象
            config_path: 配置文件路径
        """
        config_path = Path(config_path).expanduser()
        
        # 确保目录存在
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 转换为字典
        config_dict = self._config_to_dict(config)
        
        # 保存到文件
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_dict, f, allow_unicode=True, default_flow_style=False)
    
    def get_default_config(self) -> Config:
        """
        获取默认配置
        
        Returns:
            Config: 默认配置对象
        """
        return Config(
            qlib=QlibConfig(
                provider_uri="~/.qlib/qlib_data/cn_data",
                region="cn",
                auto_mount=True
            ),
            mlflow=MLflowConfig(
                tracking_uri="./mlruns",
                experiment_name="qlib_trading",
                artifact_location=None
            ),
            data=DataConfig(
                instruments="csi300",
                start_time="2020-01-01",
                end_time="2023-12-31",
                features=[
                    "$close",
                    "$open",
                    "$high",
                    "$low",
                    "$volume",
                    "$change"
                ],
                label="Ref($close, -1) / $close - 1"
            ),
            training=TrainingConfig(
                train_start="2020-01-01",
                train_end="2022-12-31",
                valid_start="2023-01-01",
                valid_end="2023-06-30",
                test_start="2023-07-01",
                test_end="2023-12-31"
            ),
            backtest=BacktestConfig(
                strategy=BacktestStrategyConfig(
                    topk=30,
                    n_drop=5
                ),
                executor=BacktestExecutorConfig(
                    time_per_step="day",
                    generate_portfolio_metrics=True
                ),
                benchmark="SH000300"
            ),
            signal=SignalConfig(
                top_k=30,
                risk_limits=RiskLimits(
                    max_position_per_stock=0.1,
                    max_sector_exposure=0.3
                )
            ),
            model_registry=ModelRegistryConfig(
                storage_path="./models",
                auto_register=True
            ),
            logging=LoggingConfig(
                log_dir="./logs",
                log_level="INFO",
                log_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                max_bytes=10485760,  # 10MB
                backup_count=5
            ),
            visualization=VisualizationConfig(
                output_dir="./reports",
                figure_format="png",
                dpi=300,
                style="seaborn"
            ),
            cli=CLIConfig(
                language="zh_CN",
                show_progress=True,
                confirm_actions=True
            )
        )
    
    def validate_config(self, config: Config) -> List[str]:
        """
        验证配置有效性
        
        Args:
            config: 配置对象
            
        Returns:
            List[str]: 错误信息列表，空列表表示验证通过
        """
        errors = []
        
        # 验证qlib配置
        if not config.qlib.provider_uri:
            errors.append("qlib.provider_uri 不能为空")
        
        if not config.qlib.region:
            errors.append("qlib.region 不能为空")
        
        # 验证数据路径
        data_path = Path(config.qlib.provider_uri).expanduser()
        if not data_path.exists():
            errors.append(f"数据路径不存在: {data_path}")
        
        # 验证MLflow配置
        if not config.mlflow.tracking_uri:
            errors.append("mlflow.tracking_uri 不能为空")
        
        if not config.mlflow.experiment_name:
            errors.append("mlflow.experiment_name 不能为空")
        
        # 验证数据配置
        if not config.data.instruments:
            errors.append("data.instruments 不能为空")
        
        if not config.data.start_time:
            errors.append("data.start_time 不能为空")
        
        if not config.data.end_time:
            errors.append("data.end_time 不能为空")
        
        if not config.data.features:
            errors.append("data.features 不能为空")
        
        if not config.data.label:
            errors.append("data.label 不能为空")
        
        # 验证训练配置
        if not config.training.train_start:
            errors.append("training.train_start 不能为空")
        
        if not config.training.train_end:
            errors.append("training.train_end 不能为空")
        
        # 验证日志配置
        if config.logging.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            errors.append(f"logging.log_level 必须是 DEBUG, INFO, WARNING, ERROR, CRITICAL 之一，当前值: {config.logging.log_level}")
        
        if config.logging.max_bytes <= 0:
            errors.append("logging.max_bytes 必须大于0")
        
        if config.logging.backup_count < 0:
            errors.append("logging.backup_count 必须大于等于0")
        
        # 验证风险限制
        if config.signal.risk_limits.max_position_per_stock <= 0 or config.signal.risk_limits.max_position_per_stock > 1:
            errors.append("signal.risk_limits.max_position_per_stock 必须在 (0, 1] 范围内")
        
        if config.signal.risk_limits.max_sector_exposure <= 0 or config.signal.risk_limits.max_sector_exposure > 1:
            errors.append("signal.risk_limits.max_sector_exposure 必须在 (0, 1] 范围内")
        
        return errors
    
    def _parse_config(self, config_dict: Dict[str, Any]) -> Config:
        """
        解析配置字典为配置对象
        
        Args:
            config_dict: 配置字典
            
        Returns:
            Config: 配置对象
        """
        return Config(
            qlib=QlibConfig(**config_dict.get('qlib', {})),
            mlflow=MLflowConfig(**config_dict.get('mlflow', {})),
            data=DataConfig(**config_dict.get('data', {})),
            training=TrainingConfig(**config_dict.get('training', {})),
            backtest=BacktestConfig(
                strategy=BacktestStrategyConfig(**config_dict.get('backtest', {}).get('strategy', {})),
                executor=BacktestExecutorConfig(**config_dict.get('backtest', {}).get('executor', {})),
                benchmark=config_dict.get('backtest', {}).get('benchmark', '')
            ),
            signal=SignalConfig(
                top_k=config_dict.get('signal', {}).get('top_k', 30),
                risk_limits=RiskLimits(**config_dict.get('signal', {}).get('risk_limits', {}))
            ),
            model_registry=ModelRegistryConfig(**config_dict.get('model_registry', {})),
            logging=LoggingConfig(**config_dict.get('logging', {})),
            visualization=VisualizationConfig(**config_dict.get('visualization', {})),
            cli=CLIConfig(**config_dict.get('cli', {}))
        )
    
    def _config_to_dict(self, config: Config) -> Dict[str, Any]:
        """
        将配置对象转换为字典
        
        Args:
            config: 配置对象
            
        Returns:
            Dict[str, Any]: 配置字典
        """
        return {
            'qlib': asdict(config.qlib),
            'mlflow': asdict(config.mlflow),
            'data': asdict(config.data),
            'training': asdict(config.training),
            'backtest': {
                'strategy': asdict(config.backtest.strategy),
                'executor': asdict(config.backtest.executor),
                'benchmark': config.backtest.benchmark
            },
            'signal': {
                'top_k': config.signal.top_k,
                'risk_limits': asdict(config.signal.risk_limits)
            },
            'model_registry': asdict(config.model_registry),
            'logging': asdict(config.logging),
            'visualization': asdict(config.visualization),
            'cli': asdict(config.cli)
        }
    
    @property
    def config(self) -> Optional[Config]:
        """获取当前配置"""
        return self._config
