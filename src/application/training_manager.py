"""
训练管理器模块 / Training Manager Module
负责协调模型训练流程，包括数据加载、特征工程、训练和保存
Responsible for coordinating model training process including data loading, feature engineering, training and saving
"""

import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime

from ..core.data_manager import DataManager
from ..core.model_factory import ModelFactory
from ..infrastructure.mlflow_tracker import MLflowTracker
from ..infrastructure.logger_system import get_logger


@dataclass
class DatasetConfig:
    """
    数据集配置 / Dataset Configuration
    
    Attributes:
        instruments: 股票池，如"csi300" / Stock pool, e.g., "csi300"
        start_time: 开始时间 / Start time
        end_time: 结束时间 / End time
        features: 特征列表 / Feature list
        label: 标签列 / Label column
    """
    instruments: str
    start_time: str
    end_time: str
    features: List[str]
    label: str


@dataclass
class TrainingConfig:
    """
    训练配置 / Training Configuration
    
    Attributes:
        model_type: 模型类型 / Model type
        dataset_config: 数据集配置 / Dataset configuration
        model_params: 模型参数 / Model parameters
        training_params: 训练参数 / Training parameters
        experiment_name: 实验名称 / Experiment name
        target_return: 目标收益率（可选）/ Target return (optional)
        optimization_objective: 优化目标 / Optimization objective
    """
    model_type: str
    dataset_config: DatasetConfig
    model_params: Dict[str, Any]
    training_params: Dict[str, Any]
    experiment_name: str
    target_return: Optional[float] = None
    optimization_objective: str = "sharpe_ratio"


@dataclass
class TrainingResult:
    """
    训练结果 / Training Result
    
    Attributes:
        model_id: 模型ID / Model ID
        metrics: 评估指标 / Evaluation metrics
        training_time: 训练时长（秒）/ Training time (seconds)
        model_path: 模型保存路径 / Model save path
        experiment_id: 实验ID / Experiment ID
        run_id: 运行ID / Run ID
    """
    model_id: str
    metrics: Dict[str, float]
    training_time: float
    model_path: str
    experiment_id: str
    run_id: str


class TrainingManagerError(Exception):
    """训练管理器错误 / Training Manager Error"""
    pass


class TrainingManager:
    """
    训练管理器 / Training Manager
    
    职责 / Responsibilities:
    - 协调训练流程 / Coordinate training process
    - 管理训练配置 / Manage training configuration
    - 记录训练指标 / Record training metrics
    - 保存训练模型 / Save trained models
    """
    
    def __init__(
        self,
        data_manager: DataManager,
        model_factory: ModelFactory,
        mlflow_tracker: Optional[MLflowTracker] = None,
        output_dir: str = "./outputs"
    ):
        """
        初始化训练管理器 / Initialize Training Manager
        
        Args:
            data_manager: 数据管理器实例 / Data manager instance
            model_factory: 模型工厂实例 / Model factory instance
            mlflow_tracker: MLflow追踪器实例（可选）/ MLflow tracker instance (optional)
            output_dir: 输出目录 / Output directory
        """
        self._data_manager = data_manager
        self._model_factory = model_factory
        self._mlflow_tracker = mlflow_tracker
        self._output_dir = Path(output_dir).expanduser()
        self._logger = get_logger(__name__)
        
        # 确保输出目录存在 / Ensure output directory exists
        self._output_dir.mkdir(parents=True, exist_ok=True)
    
    def train_model(self, config: TrainingConfig) -> TrainingResult:
        """
        训练模型 / Train Model
        
        Args:
            config: 训练配置 / Training configuration
            
        Returns:
            TrainingResult: 训练结果 / Training result
            
        Raises:
            TrainingManagerError: 训练失败时抛出 / Raised when training fails
        """
        self._logger.info(
            f"开始训练模型 / Starting model training\n"
            f"模型类型 / Model type: {config.model_type}\n"
            f"实验名称 / Experiment name: {config.experiment_name}"
        )
        
        start_time = time.time()
        run_id = None
        
        try:
            # 1. 启动MLflow运行（如果配置了）/ Start MLflow run (if configured)
            if self._mlflow_tracker and self._mlflow_tracker.is_initialized():
                run_name = f"{config.model_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                run_id = self._mlflow_tracker.start_run(
                    experiment_name=config.experiment_name,
                    run_name=run_name,
                    tags={
                        "model_type": config.model_type,
                        "instruments": config.dataset_config.instruments
                    }
                )
                
                # 记录配置参数 / Log configuration parameters
                self._mlflow_tracker.log_params({
                    "model_type": config.model_type,
                    "instruments": config.dataset_config.instruments,
                    "start_time": config.dataset_config.start_time,
                    "end_time": config.dataset_config.end_time,
                    **config.model_params,
                    **config.training_params
                })
                
                if config.target_return:
                    self._mlflow_tracker.log_param("target_return", config.target_return)
            
            # 2. 加载数据集 / Load dataset
            self._logger.info("加载数据集 / Loading dataset...")
            dataset = self._load_dataset(config.dataset_config)
            
            # 3. 创建模型 / Create model
            self._logger.info(f"创建模型 / Creating model: {config.model_type}")
            model = self._model_factory.create_model(
                model_type=config.model_type,
                params=config.model_params
            )
            
            # 4. 训练模型 / Train model
            self._logger.info("训练模型 / Training model...")
            model = self._train_model(model, dataset, config.training_params)
            
            # 5. 评估模型 / Evaluate model
            self._logger.info("评估模型 / Evaluating model...")
            metrics = self._evaluate_model(model, dataset)
            
            # 记录指标到MLflow / Log metrics to MLflow
            if self._mlflow_tracker and run_id:
                self._mlflow_tracker.log_metrics(metrics)
            
            # 6. 保存模型 / Save model
            model_id = f"{config.model_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            model_path = self._save_model(model, model_id, config)
            
            # 记录模型到MLflow / Log model to MLflow
            if self._mlflow_tracker and run_id:
                try:
                    self._mlflow_tracker.log_artifact(str(model_path))
                except Exception as e:
                    self._logger.warning(f"记录模型到MLflow失败 / Failed to log model to MLflow: {str(e)}")
            
            # 计算训练时长 / Calculate training time
            training_time = time.time() - start_time
            
            # 记录训练时长 / Log training time
            if self._mlflow_tracker and run_id:
                self._mlflow_tracker.log_metric("training_time", training_time)
            
            # 结束MLflow运行 / End MLflow run
            if self._mlflow_tracker and run_id:
                self._mlflow_tracker.end_run(status="FINISHED")
            
            # 构建训练结果 / Build training result
            result = TrainingResult(
                model_id=model_id,
                metrics=metrics,
                training_time=training_time,
                model_path=str(model_path),
                experiment_id=self._mlflow_tracker._current_experiment_id if self._mlflow_tracker else "",
                run_id=run_id or ""
            )
            
            self._logger.info(
                f"模型训练完成 / Model training completed\n"
                f"模型ID / Model ID: {model_id}\n"
                f"训练时长 / Training time: {training_time:.2f}秒 / seconds\n"
                f"指标 / Metrics: {metrics}"
            )
            
            return result
            
        except Exception as e:
            # 记录错误并结束MLflow运行 / Log error and end MLflow run
            error_msg = f"模型训练失败 / Model training failed: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            
            if self._mlflow_tracker and run_id:
                try:
                    self._mlflow_tracker.end_run(status="FAILED")
                except:
                    pass
            
            raise TrainingManagerError(error_msg) from e

    
    def train_from_template(
        self,
        template_name: str,
        dataset_config: DatasetConfig,
        experiment_name: str,
        custom_params: Optional[Dict[str, Any]] = None
    ) -> TrainingResult:
        """
        从模板训练模型 / Train Model from Template
        
        Args:
            template_name: 模板名称 / Template name
            dataset_config: 数据集配置 / Dataset configuration
            experiment_name: 实验名称 / Experiment name
            custom_params: 自定义参数（可选）/ Custom parameters (optional)
            
        Returns:
            TrainingResult: 训练结果 / Training result
            
        Raises:
            TrainingManagerError: 训练失败时抛出 / Raised when training fails
        """
        try:
            self._logger.info(
                f"从模板训练模型 / Training model from template: {template_name}"
            )
            
            # 获取模板 / Get template
            template = self._model_factory.get_template(template_name)
            
            # 合并模板参数和自定义参数 / Merge template params with custom params
            model_params = template.default_params.copy()
            if custom_params:
                model_params.update(custom_params)
            
            # 构建训练配置 / Build training configuration
            config = TrainingConfig(
                model_type=template.model_type,
                dataset_config=dataset_config,
                model_params=model_params,
                training_params={},  # 使用默认训练参数 / Use default training params
                experiment_name=experiment_name
            )
            
            # 训练模型 / Train model
            return self.train_model(config)
            
        except Exception as e:
            error_msg = f"从模板训练模型失败 / Failed to train model from template: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise TrainingManagerError(error_msg) from e
    
    def list_templates(self) -> List:
        """
        列出所有可用的模板 / List All Available Templates
        
        Returns:
            List: 模板列表 / Template list
        """
        return self._model_factory.list_templates()
    
    def _load_dataset(self, config: DatasetConfig) -> Dict[str, Any]:
        """
        加载数据集 / Load Dataset
        
        Args:
            config: 数据集配置 / Dataset configuration
            
        Returns:
            Dict[str, Any]: 数据集字典 / Dataset dictionary
            
        Raises:
            TrainingManagerError: 加载失败时抛出 / Raised when loading fails
        """
        try:
            # 简化实现：直接使用qlib的D模块获取数据
            # 这样可以避免复杂的DataHandlerLP配置问题
            from qlib.data import D
            import pandas as pd
            
            self._logger.info(
                f"使用简化的数据加载方式 / Using simplified data loading\n"
                f"时间范围 / Time range: {config.start_time} 至 / to {config.end_time}\n"
                f"股票池 / Instruments: {config.instruments}"
            )
            
            # 使用D.features直接获取数据
            # 这是qlib 0.9.7推荐的简单方式
            data = D.features(
                instruments=config.instruments,
                fields=config.features,
                start_time=config.start_time,
                end_time=config.end_time,
                freq="day"
            )
            
            if data is None or data.empty:
                raise TrainingManagerError(
                    f"未获取到数据 / No data retrieved for instruments: {config.instruments}"
                )
            
            # 添加标签列
            if config.label:
                label_data = D.features(
                    instruments=config.instruments,
                    fields=[config.label],
                    start_time=config.start_time,
                    end_time=config.end_time,
                    freq="day"
                )
                if label_data is not None and not label_data.empty:
                    data = pd.concat([data, label_data], axis=1)
            
            self._logger.info(
                f"数据集加载成功 / Dataset loaded successfully\n"
                f"数据形状 / Data shape: {data.shape}\n"
                f"特征列 / Feature columns: {list(data.columns)}"
            )
            
            # 返回简化的数据集格式
            # 包含原始DataFrame和配置信息
            return {
                "data": data,
                "config": config,
                "features": config.features,
                "label": config.label
            }
            
        except TrainingManagerError:
            raise
        except Exception as e:
            error_msg = f"加载数据集失败 / Failed to load dataset: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise TrainingManagerError(error_msg) from e
    
    def _train_model(
        self,
        model: Any,
        dataset: Dict[str, Any],
        training_params: Dict[str, Any]
    ) -> Any:
        """
        训练模型 / Train Model
        
        Args:
            model: 模型实例 / Model instance
            dataset: 数据集字典，包含data, features, label / Dataset dict with data, features, label
            training_params: 训练参数 / Training parameters
            
        Returns:
            Any: 训练后的模型 / Trained model
            
        Raises:
            TrainingManagerError: 训练失败时抛出 / Raised when training fails
        """
        try:
            # 获取数据 / Get data
            data = dataset["data"]
            features = dataset["features"]
            label = dataset["label"]
            
            # 准备训练数据 / Prepare training data
            # 分离特征和标签
            X = data[features]
            y = data[label] if label else None
            
            self._logger.info(
                f"准备训练数据 / Preparing training data\n"
                f"特征形状 / Features shape: {X.shape}\n"
                f"标签形状 / Label shape: {y.shape if y is not None else 'None'}"
            )
            
            # 训练模型 / Train model
            # 对于sklearn类型的模型，使用fit(X, y)
            if hasattr(model, 'fit'):
                if y is not None:
                    model.fit(X, y)
                else:
                    model.fit(X)
            else:
                raise TrainingManagerError(
                    f"模型没有fit方法 / Model does not have fit method: {type(model)}"
                )
            
            self._logger.info("模型训练完成 / Model training completed")
            
            return model
            
        except TrainingManagerError:
            raise
        except Exception as e:
            error_msg = f"模型训练失败 / Model training failed: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise TrainingManagerError(error_msg) from e
    
    def _evaluate_model(
        self,
        model: Any,
        dataset: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        评估模型 / Evaluate Model
        
        Args:
            model: 训练后的模型 / Trained model
            dataset: 数据集 / Dataset
            
        Returns:
            Dict[str, float]: 评估指标 / Evaluation metrics
            
        Raises:
            TrainingManagerError: 评估失败时抛出 / Raised when evaluation fails
        """
        try:
            # 获取qlib数据集 / Get qlib dataset
            qlib_dataset = dataset["dataset"]
            
            # 进行预测 / Make predictions
            predictions = model.predict(qlib_dataset)
            
            # 计算评估指标 / Calculate evaluation metrics
            # 这里使用简单的指标，实际应用中可以使用更多指标
            # Using simple metrics here, more metrics can be used in practice
            metrics = {}
            
            # 尝试计算IC（信息系数）/ Try to calculate IC (Information Coefficient)
            try:
                from qlib.data.dataset import DatasetH
                import numpy as np
                
                # 获取真实标签 / Get true labels
                labels = qlib_dataset.prepare("train", col_set="label")
                
                # 计算IC / Calculate IC
                if predictions is not None and labels is not None:
                    # 确保预测和标签对齐 / Ensure predictions and labels are aligned
                    common_index = predictions.index.intersection(labels.index)
                    if len(common_index) > 0:
                        pred_aligned = predictions.loc[common_index]
                        label_aligned = labels.loc[common_index]
                        
                        # 计算相关系数 / Calculate correlation coefficient
                        ic = pred_aligned.corrwith(label_aligned.iloc[:, 0])
                        metrics["ic_mean"] = float(ic.mean()) if not ic.empty else 0.0
                        metrics["ic_std"] = float(ic.std()) if not ic.empty else 0.0
                    else:
                        self._logger.warning("预测和标签没有共同索引 / No common index between predictions and labels")
                        metrics["ic_mean"] = 0.0
                        metrics["ic_std"] = 0.0
                else:
                    self._logger.warning("预测或标签为空 / Predictions or labels are empty")
                    metrics["ic_mean"] = 0.0
                    metrics["ic_std"] = 0.0
                    
            except Exception as e:
                self._logger.warning(f"计算IC失败 / Failed to calculate IC: {str(e)}")
                metrics["ic_mean"] = 0.0
                metrics["ic_std"] = 0.0
            
            # 添加预测数量 / Add prediction count
            metrics["prediction_count"] = len(predictions) if predictions is not None else 0
            
            self._logger.info(f"模型评估完成 / Model evaluation completed: {metrics}")
            
            return metrics
            
        except Exception as e:
            error_msg = f"模型评估失败 / Model evaluation failed: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise TrainingManagerError(error_msg) from e
    
    def _save_model(
        self,
        model: Any,
        model_id: str,
        config: TrainingConfig
    ) -> Path:
        """
        保存模型 / Save Model
        
        Args:
            model: 训练后的模型 / Trained model
            model_id: 模型ID / Model ID
            config: 训练配置 / Training configuration
            
        Returns:
            Path: 模型保存路径 / Model save path
            
        Raises:
            TrainingManagerError: 保存失败时抛出 / Raised when saving fails
        """
        try:
            # 创建模型目录 / Create model directory
            model_dir = self._output_dir / "models" / model_id
            model_dir.mkdir(parents=True, exist_ok=True)
            
            # 保存模型文件 / Save model file
            model_path = model_dir / "model.pkl"
            
            # 使用pickle保存模型 / Save model using pickle
            import pickle
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)
            
            # 保存配置文件 / Save configuration file
            config_path = model_dir / "config.json"
            import json
            config_dict = {
                "model_id": model_id,
                "model_type": config.model_type,
                "dataset_config": {
                    "instruments": config.dataset_config.instruments,
                    "start_time": config.dataset_config.start_time,
                    "end_time": config.dataset_config.end_time,
                    "features": config.dataset_config.features,
                    "label": config.dataset_config.label,
                },
                "model_params": config.model_params,
                "training_params": config.training_params,
                "experiment_name": config.experiment_name,
                "target_return": config.target_return,
                "optimization_objective": config.optimization_objective,
                "created_at": datetime.now().isoformat(),
            }
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            
            self._logger.info(
                f"模型保存成功 / Model saved successfully\n"
                f"路径 / Path: {model_path}"
            )
            
            return model_path
            
        except Exception as e:
            error_msg = f"保存模型失败 / Failed to save model: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise TrainingManagerError(error_msg) from e
