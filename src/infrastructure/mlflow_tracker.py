"""
MLflow追踪器模块 / MLflow Tracker Module
负责实验追踪、指标记录和模型管理 / Responsible for experiment tracking, metrics logging, and model management
"""

from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from .logger_system import get_logger

# 延迟导入mlflow，避免在测试时因mlflow未安装而失败
# Lazy import mlflow to avoid failures in tests when mlflow is not installed
try:
    import mlflow
    from mlflow.tracking import MlflowClient
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False
    mlflow = None
    MlflowClient = None


class MLflowError(Exception):
    """MLflow错误 / MLflow Error"""
    pass


class MLflowTracker:
    """
    MLflow追踪器 / MLflow Tracker
    
    职责 / Responsibilities:
    - 记录实验 / Record experiments
    - 追踪指标 / Track metrics
    - 管理模型版本 / Manage model versions
    """
    
    def __init__(self, tracking_uri: Optional[str] = None):
        """
        初始化MLflow追踪器 / Initialize MLflow Tracker
        
        Args:
            tracking_uri: MLflow追踪URI，默认为"./mlruns" / MLflow tracking URI, defaults to "./mlruns"
        """
        self._logger = get_logger(__name__)
        self._tracking_uri = tracking_uri or "./mlruns"
        self._current_run_id: Optional[str] = None
        self._current_experiment_id: Optional[str] = None
        self._client: Optional[MlflowClient] = None
        self._initialized = False
    
    def initialize(self, tracking_uri: Optional[str] = None) -> None:
        """
        初始化MLflow / Initialize MLflow
        
        Args:
            tracking_uri: MLflow追踪URI / MLflow tracking URI
            
        Raises:
            MLflowError: 初始化失败时抛出 / Raised when initialization fails
        """
        if not MLFLOW_AVAILABLE:
            error_msg = (
                "MLflow未安装。请先安装MLflow:\n"
                "pip install mlflow\n"
                "MLflow is not installed. Please install MLflow first:\n"
                "pip install mlflow"
            )
            self._logger.error(error_msg)
            raise MLflowError(error_msg)
        
        try:
            if tracking_uri:
                self._tracking_uri = tracking_uri
            
            # 设置追踪URI / Set tracking URI
            mlflow.set_tracking_uri(self._tracking_uri)
            
            # 创建客户端 / Create client
            self._client = MlflowClient(tracking_uri=self._tracking_uri)
            
            self._initialized = True
            self._logger.info(
                f"MLflow初始化成功 - 追踪URI: {self._tracking_uri}\n"
                f"MLflow initialized successfully - Tracking URI: {self._tracking_uri}"
            )
            
        except Exception as e:
            error_msg = f"MLflow初始化失败 / MLflow initialization failed: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise MLflowError(error_msg) from e
    
    def create_experiment(
        self,
        experiment_name: str,
        artifact_location: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None
    ) -> str:
        """
        创建实验 / Create Experiment
        
        Args:
            experiment_name: 实验名称 / Experiment name
            artifact_location: 工件存储位置 / Artifact storage location
            tags: 实验标签 / Experiment tags
            
        Returns:
            str: 实验ID / Experiment ID
            
        Raises:
            MLflowError: 创建失败时抛出 / Raised when creation fails
        """
        if not self._initialized:
            raise MLflowError(
                "MLflow未初始化，请先调用initialize()方法\n"
                "MLflow not initialized, please call initialize() first"
            )
        
        try:
            # 检查实验是否已存在 / Check if experiment already exists
            experiment = self._client.get_experiment_by_name(experiment_name)
            
            if experiment:
                experiment_id = experiment.experiment_id
                self._logger.info(
                    f"实验已存在，使用现有实验 / Experiment exists, using existing: {experiment_name} (ID: {experiment_id})"
                )
            else:
                # 创建新实验 / Create new experiment
                experiment_id = self._client.create_experiment(
                    name=experiment_name,
                    artifact_location=artifact_location,
                    tags=tags
                )
                self._logger.info(
                    f"创建新实验 / Created new experiment: {experiment_name} (ID: {experiment_id})"
                )
            
            self._current_experiment_id = experiment_id
            return experiment_id
            
        except Exception as e:
            error_msg = f"创建实验失败 / Failed to create experiment: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise MLflowError(error_msg) from e
    
    def start_run(
        self,
        experiment_name: str,
        run_name: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        description: Optional[str] = None
    ) -> str:
        """
        开始新的运行 / Start New Run
        
        Args:
            experiment_name: 实验名称 / Experiment name
            run_name: 运行名称 / Run name
            tags: 运行标签 / Run tags
            description: 运行描述 / Run description
            
        Returns:
            str: 运行ID / Run ID
            
        Raises:
            MLflowError: 启动失败时抛出 / Raised when start fails
        """
        if not self._initialized:
            raise MLflowError(
                "MLflow未初始化，请先调用initialize()方法\n"
                "MLflow not initialized, please call initialize() first"
            )
        
        try:
            # 确保实验存在 / Ensure experiment exists
            experiment_id = self.create_experiment(experiment_name)
            
            # 生成运行名称 / Generate run name
            if not run_name:
                run_name = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # 准备标签 / Prepare tags
            run_tags = tags or {}
            if description:
                run_tags["mlflow.note.content"] = description
            
            # 开始运行 / Start run
            run = self._client.create_run(
                experiment_id=experiment_id,
                run_name=run_name,
                tags=run_tags
            )
            
            self._current_run_id = run.info.run_id
            self._logger.info(
                f"开始新运行 / Started new run: {run_name} (ID: {self._current_run_id})"
            )
            
            return self._current_run_id
            
        except Exception as e:
            error_msg = f"启动运行失败 / Failed to start run: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise MLflowError(error_msg) from e
    
    def log_param(self, key: str, value: Any) -> None:
        """
        记录单个参数 / Log Single Parameter
        
        Args:
            key: 参数名 / Parameter name
            value: 参数值 / Parameter value
        """
        self.log_params({key: value})
    
    def log_params(self, params: Dict[str, Any]) -> None:
        """
        记录多个参数 / Log Multiple Parameters
        
        Args:
            params: 参数字典 / Parameters dictionary
            
        Raises:
            MLflowError: 记录失败时抛出 / Raised when logging fails
        """
        if not self._current_run_id:
            raise MLflowError(
                "没有活动的运行，请先调用start_run()\n"
                "No active run, please call start_run() first"
            )
        
        try:
            # 转换参数值为字符串 / Convert parameter values to strings
            str_params = {k: str(v) for k, v in params.items()}
            
            # 记录参数 / Log parameters
            for key, value in str_params.items():
                self._client.log_param(self._current_run_id, key, value)
            
            self._logger.debug(
                f"记录参数 / Logged parameters: {len(params)} 个 / items"
            )
            
        except Exception as e:
            error_msg = f"记录参数失败 / Failed to log parameters: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise MLflowError(error_msg) from e
    
    def log_metric(self, key: str, value: float, step: Optional[int] = None) -> None:
        """
        记录单个指标 / Log Single Metric
        
        Args:
            key: 指标名 / Metric name
            value: 指标值 / Metric value
            step: 步骤数（可选）/ Step number (optional)
        """
        self.log_metrics({key: value}, step=step)
    
    def log_metrics(
        self,
        metrics: Dict[str, float],
        step: Optional[int] = None
    ) -> None:
        """
        记录多个指标 / Log Multiple Metrics
        
        Args:
            metrics: 指标字典 / Metrics dictionary
            step: 步骤数（可选）/ Step number (optional)
            
        Raises:
            MLflowError: 记录失败时抛出 / Raised when logging fails
        """
        if not self._current_run_id:
            raise MLflowError(
                "没有活动的运行，请先调用start_run()\n"
                "No active run, please call start_run() first"
            )
        
        try:
            # 记录指标 / Log metrics
            for key, value in metrics.items():
                self._client.log_metric(
                    self._current_run_id,
                    key,
                    value,
                    step=step if step is not None else 0
                )
            
            self._logger.debug(
                f"记录指标 / Logged metrics: {len(metrics)} 个 / items"
                + (f" (步骤 / step: {step})" if step is not None else "")
            )
            
        except Exception as e:
            error_msg = f"记录指标失败 / Failed to log metrics: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise MLflowError(error_msg) from e
    
    def log_artifact(self, local_path: str, artifact_path: Optional[str] = None) -> None:
        """
        记录工件（文件）/ Log Artifact (File)
        
        Args:
            local_path: 本地文件路径 / Local file path
            artifact_path: 工件存储路径（可选）/ Artifact storage path (optional)
            
        Raises:
            MLflowError: 记录失败时抛出 / Raised when logging fails
        """
        if not self._current_run_id:
            raise MLflowError(
                "没有活动的运行，请先调用start_run()\n"
                "No active run, please call start_run() first"
            )
        
        try:
            local_path_obj = Path(local_path)
            
            if not local_path_obj.exists():
                raise MLflowError(
                    f"文件不存在 / File does not exist: {local_path}"
                )
            
            # 记录工件 / Log artifact
            self._client.log_artifact(
                self._current_run_id,
                str(local_path_obj),
                artifact_path
            )
            
            self._logger.debug(
                f"记录工件 / Logged artifact: {local_path}"
            )
            
        except MLflowError:
            raise
        except Exception as e:
            error_msg = f"记录工件失败 / Failed to log artifact: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise MLflowError(error_msg) from e
    
    def log_model(
        self,
        model: Any,
        artifact_path: str,
        registered_model_name: Optional[str] = None
    ) -> None:
        """
        记录模型 / Log Model
        
        Args:
            model: 模型对象 / Model object
            artifact_path: 工件路径 / Artifact path
            registered_model_name: 注册模型名称（可选）/ Registered model name (optional)
            
        Raises:
            MLflowError: 记录失败时抛出 / Raised when logging fails
        """
        if not self._current_run_id:
            raise MLflowError(
                "没有活动的运行，请先调用start_run()\n"
                "No active run, please call start_run() first"
            )
        
        try:
            # 使用sklearn格式保存模型（通用格式）
            # Save model using sklearn format (generic format)
            import mlflow.sklearn
            
            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path=artifact_path,
                registered_model_name=registered_model_name
            )
            
            self._logger.info(
                f"记录模型 / Logged model: {artifact_path}"
                + (f" (注册为 / registered as: {registered_model_name})" if registered_model_name else "")
            )
            
        except Exception as e:
            error_msg = f"记录模型失败 / Failed to log model: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise MLflowError(error_msg) from e
    
    def set_tag(self, key: str, value: str) -> None:
        """
        设置标签 / Set Tag
        
        Args:
            key: 标签名 / Tag name
            value: 标签值 / Tag value
        """
        self.set_tags({key: value})
    
    def set_tags(self, tags: Dict[str, str]) -> None:
        """
        设置多个标签 / Set Multiple Tags
        
        Args:
            tags: 标签字典 / Tags dictionary
            
        Raises:
            MLflowError: 设置失败时抛出 / Raised when setting fails
        """
        if not self._current_run_id:
            raise MLflowError(
                "没有活动的运行，请先调用start_run()\n"
                "No active run, please call start_run() first"
            )
        
        try:
            for key, value in tags.items():
                self._client.set_tag(self._current_run_id, key, str(value))
            
            self._logger.debug(
                f"设置标签 / Set tags: {len(tags)} 个 / items"
            )
            
        except Exception as e:
            error_msg = f"设置标签失败 / Failed to set tags: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise MLflowError(error_msg) from e
    
    def end_run(self, status: str = "FINISHED") -> None:
        """
        结束当前运行 / End Current Run
        
        Args:
            status: 运行状态，可选值："FINISHED", "FAILED", "KILLED" / 
                   Run status, options: "FINISHED", "FAILED", "KILLED"
                   
        Raises:
            MLflowError: 结束失败时抛出 / Raised when ending fails
        """
        if not self._current_run_id:
            self._logger.warning(
                "没有活动的运行需要结束 / No active run to end"
            )
            return
        
        try:
            # 结束运行 / End run
            self._client.set_terminated(
                self._current_run_id,
                status=status
            )
            
            self._logger.info(
                f"结束运行 / Ended run: {self._current_run_id} (状态 / status: {status})"
            )
            
            self._current_run_id = None
            
        except Exception as e:
            error_msg = f"结束运行失败 / Failed to end run: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise MLflowError(error_msg) from e
    
    def get_run_info(self, run_id: Optional[str] = None) -> Dict[str, Any]:
        """
        获取运行信息 / Get Run Information
        
        Args:
            run_id: 运行ID，如果为None则使用当前运行 / Run ID, uses current run if None
            
        Returns:
            Dict[str, Any]: 运行信息 / Run information
            
        Raises:
            MLflowError: 获取失败时抛出 / Raised when retrieval fails
        """
        target_run_id = run_id or self._current_run_id
        
        if not target_run_id:
            raise MLflowError(
                "没有指定运行ID且没有活动的运行\n"
                "No run ID specified and no active run"
            )
        
        try:
            run = self._client.get_run(target_run_id)
            
            return {
                "run_id": run.info.run_id,
                "experiment_id": run.info.experiment_id,
                "status": run.info.status,
                "start_time": run.info.start_time,
                "end_time": run.info.end_time,
                "artifact_uri": run.info.artifact_uri,
                "params": run.data.params,
                "metrics": run.data.metrics,
                "tags": run.data.tags
            }
            
        except Exception as e:
            error_msg = f"获取运行信息失败 / Failed to get run info: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise MLflowError(error_msg) from e
    
    def is_initialized(self) -> bool:
        """
        检查是否已初始化 / Check if Initialized
        
        Returns:
            bool: 是否已初始化 / Whether initialized
        """
        return self._initialized
    
    def get_current_run_id(self) -> Optional[str]:
        """
        获取当前运行ID / Get Current Run ID
        
        Returns:
            Optional[str]: 当前运行ID / Current run ID
        """
        return self._current_run_id
    
    @property
    def tracking_uri(self) -> str:
        """获取追踪URI / Get tracking URI"""
        return self._tracking_uri
