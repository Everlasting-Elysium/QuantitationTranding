"""
模型注册表模块 / Model Registry Module
负责模型注册、版本管理和查询 / Responsible for model registration, version management and querying
"""

import json
import pickle
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime

from ..models.data_models import ModelMetadata, DatasetConfig
from ..infrastructure.logger_system import get_logger


@dataclass
class ModelInfo:
    """
    模型信息 / Model Information
    
    Attributes:
        model_id: 模型ID / Model ID
        model_name: 模型名称 / Model name
        version: 模型版本 / Model version
        model_type: 模型类型 / Model type
        training_date: 训练日期 / Training date
        performance_metrics: 性能指标 / Performance metrics
        status: 模型状态 / Model status (e.g., "registered", "candidate", "production", "archived")
        model_path: 模型文件路径 / Model file path
        metadata_path: 元数据文件路径 / Metadata file path
    """
    model_id: str
    model_name: str
    version: str
    model_type: str
    training_date: str
    performance_metrics: Dict[str, float]
    status: str
    model_path: str
    metadata_path: str


@dataclass
class ModelFilter:
    """
    模型过滤器 / Model Filter
    
    Attributes:
        model_type: 按模型类型过滤 / Filter by model type
        status: 按状态过滤 / Filter by status
        min_performance: 最小性能要求 / Minimum performance requirement
        date_from: 起始日期 / Start date
        date_to: 结束日期 / End date
    """
    model_type: Optional[str] = None
    status: Optional[str] = None
    min_performance: Optional[Dict[str, float]] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None


class ModelRegistryError(Exception):
    """模型注册表错误 / Model Registry Error"""
    pass


class ModelRegistry:
    """
    模型注册表 / Model Registry
    
    职责 / Responsibilities:
    - 注册和管理模型 / Register and manage models
    - 版本控制 / Version control
    - 模型元数据管理 / Model metadata management
    - 生产模型标记 / Production model marking
    """
    
    def __init__(self, registry_dir: str = "./model_registry"):
        """
        初始化模型注册表 / Initialize Model Registry
        
        Args:
            registry_dir: 注册表目录 / Registry directory
        """
        self._registry_dir = Path(registry_dir).expanduser()
        self._logger = get_logger(__name__)
        
        # 确保注册表目录存在 / Ensure registry directory exists
        self._registry_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建索引文件路径 / Create index file path
        self._index_file = self._registry_dir / "index.json"
        
        # 加载或初始化索引 / Load or initialize index
        self._index = self._load_index()
        
        self._logger.info(
            f"模型注册表初始化成功 / Model registry initialized successfully\n"
            f"注册表目录 / Registry directory: {self._registry_dir}\n"
            f"已注册模型数量 / Registered models count: {len(self._index)}"
        )
    
    def register_model(
        self,
        model: Any,
        metadata: ModelMetadata,
        model_path: Optional[str] = None
    ) -> str:
        """
        注册模型 / Register Model
        
        Args:
            model: 模型对象 / Model object
            metadata: 模型元数据 / Model metadata
            model_path: 模型文件路径（可选，如果提供则复制到注册表）/ Model file path (optional)
            
        Returns:
            str: 模型ID / Model ID
            
        Raises:
            ModelRegistryError: 注册失败时抛出 / Raised when registration fails
        """
        try:
            # 生成模型ID / Generate model ID
            model_id = self._generate_model_id(metadata.model_name, metadata.version)
            
            self._logger.info(
                f"注册模型 / Registering model\n"
                f"模型ID / Model ID: {model_id}\n"
                f"模型名称 / Model name: {metadata.model_name}\n"
                f"版本 / Version: {metadata.version}"
            )
            
            # 创建模型目录 / Create model directory
            model_dir = self._registry_dir / model_id
            model_dir.mkdir(parents=True, exist_ok=True)
            
            # 保存模型文件 / Save model file
            if model_path and Path(model_path).exists():
                # 如果提供了模型路径，复制文件 / If model path provided, copy file
                target_model_path = model_dir / "model.pkl"
                shutil.copy2(model_path, target_model_path)
            else:
                # 否则直接保存模型对象 / Otherwise save model object directly
                target_model_path = model_dir / "model.pkl"
                with open(target_model_path, 'wb') as f:
                    pickle.dump(model, f)
            
            # 保存元数据 / Save metadata
            metadata_path = model_dir / "metadata.json"
            metadata_dict = {
                "model_name": metadata.model_name,
                "version": metadata.version,
                "training_date": metadata.training_date,
                "performance_metrics": metadata.performance_metrics,
                "dataset_info": {
                    "instruments": metadata.dataset_info.instruments,
                    "start_time": metadata.dataset_info.start_time,
                    "end_time": metadata.dataset_info.end_time,
                    "features": metadata.dataset_info.features,
                    "label": metadata.dataset_info.label,
                },
                "hyperparameters": metadata.hyperparameters,
                "registered_at": datetime.now().isoformat(),
            }
            
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata_dict, f, indent=2, ensure_ascii=False)
            
            # 更新索引 / Update index
            model_info = ModelInfo(
                model_id=model_id,
                model_name=metadata.model_name,
                version=metadata.version,
                model_type=metadata.hyperparameters.get("model_type", "unknown"),
                training_date=metadata.training_date,
                performance_metrics=metadata.performance_metrics,
                status="registered",
                model_path=str(target_model_path),
                metadata_path=str(metadata_path)
            )
            
            self._index[model_id] = asdict(model_info)
            self._save_index()
            
            self._logger.info(
                f"模型注册成功 / Model registered successfully\n"
                f"模型ID / Model ID: {model_id}\n"
                f"模型路径 / Model path: {target_model_path}"
            )
            
            # 检查是否应该标记为候选模型 / Check if should be marked as candidate
            self._check_and_mark_candidate(model_id, metadata.performance_metrics)
            
            return model_id
            
        except Exception as e:
            error_msg = f"注册模型失败 / Failed to register model: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise ModelRegistryError(error_msg) from e
    
    def get_model(self, model_id: str) -> Any:
        """
        获取模型 / Get Model
        
        Args:
            model_id: 模型ID / Model ID
            
        Returns:
            Any: 模型对象 / Model object
            
        Raises:
            ModelRegistryError: 获取失败时抛出 / Raised when retrieval fails
        """
        try:
            # 检查模型是否存在 / Check if model exists
            if model_id not in self._index:
                raise ModelRegistryError(
                    f"模型不存在 / Model does not exist: {model_id}"
                )
            
            # 获取模型路径 / Get model path
            model_path = Path(self._index[model_id]["model_path"])
            
            if not model_path.exists():
                raise ModelRegistryError(
                    f"模型文件不存在 / Model file does not exist: {model_path}"
                )
            
            # 加载模型 / Load model
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            self._logger.info(
                f"加载模型成功 / Model loaded successfully: {model_id}"
            )
            
            return model
            
        except ModelRegistryError:
            raise
        except Exception as e:
            error_msg = f"获取模型失败 / Failed to get model: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise ModelRegistryError(error_msg) from e
    
    def get_model_metadata(self, model_id: str) -> Dict[str, Any]:
        """
        获取模型元数据 / Get Model Metadata
        
        Args:
            model_id: 模型ID / Model ID
            
        Returns:
            Dict[str, Any]: 模型元数据 / Model metadata
            
        Raises:
            ModelRegistryError: 获取失败时抛出 / Raised when retrieval fails
        """
        try:
            # 检查模型是否存在 / Check if model exists
            if model_id not in self._index:
                raise ModelRegistryError(
                    f"模型不存在 / Model does not exist: {model_id}"
                )
            
            # 获取元数据路径 / Get metadata path
            metadata_path = Path(self._index[model_id]["metadata_path"])
            
            if not metadata_path.exists():
                raise ModelRegistryError(
                    f"元数据文件不存在 / Metadata file does not exist: {metadata_path}"
                )
            
            # 加载元数据 / Load metadata
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            return metadata
            
        except ModelRegistryError:
            raise
        except Exception as e:
            error_msg = f"获取模型元数据失败 / Failed to get model metadata: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise ModelRegistryError(error_msg) from e
    
    def list_models(self, filter: Optional[ModelFilter] = None) -> List[ModelInfo]:
        """
        列出所有模型 / List All Models
        
        Args:
            filter: 过滤条件（可选）/ Filter conditions (optional)
            
        Returns:
            List[ModelInfo]: 模型信息列表 / List of model information
        """
        try:
            # 获取所有模型 / Get all models
            models = [
                ModelInfo(**model_data)
                for model_data in self._index.values()
            ]
            
            # 应用过滤器 / Apply filter
            if filter:
                models = self._apply_filter(models, filter)
            
            # 按训练日期排序（最新的在前）/ Sort by training date (newest first)
            models.sort(key=lambda m: m.training_date, reverse=True)
            
            self._logger.debug(
                f"列出模型 / Listed models: {len(models)} 个 / items"
            )
            
            return models
            
        except Exception as e:
            error_msg = f"列出模型失败 / Failed to list models: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise ModelRegistryError(error_msg) from e
    
    def set_model_status(self, model_id: str, status: str) -> None:
        """
        设置模型状态 / Set Model Status
        
        Args:
            model_id: 模型ID / Model ID
            status: 模型状态 / Model status (e.g., "registered", "candidate", "production", "archived")
            
        Raises:
            ModelRegistryError: 设置失败时抛出 / Raised when setting fails
        """
        try:
            # 检查模型是否存在 / Check if model exists
            if model_id not in self._index:
                raise ModelRegistryError(
                    f"模型不存在 / Model does not exist: {model_id}"
                )
            
            # 验证状态值 / Validate status value
            valid_statuses = ["registered", "candidate", "production", "archived"]
            if status not in valid_statuses:
                raise ModelRegistryError(
                    f"无效的状态值 / Invalid status value: {status}. "
                    f"有效值 / Valid values: {valid_statuses}"
                )
            
            # 如果设置为生产模型，将其他生产模型降级为候选 / 
            # If setting to production, demote other production models to candidate
            if status == "production":
                for mid, model_data in self._index.items():
                    if model_data["status"] == "production":
                        self._index[mid]["status"] = "candidate"
                        self._logger.info(
                            f"将模型降级为候选 / Demoted model to candidate: {mid}"
                        )
            
            # 更新状态 / Update status
            old_status = self._index[model_id]["status"]
            self._index[model_id]["status"] = status
            self._save_index()
            
            self._logger.info(
                f"模型状态更新成功 / Model status updated successfully\n"
                f"模型ID / Model ID: {model_id}\n"
                f"旧状态 / Old status: {old_status}\n"
                f"新状态 / New status: {status}"
            )
            
        except ModelRegistryError:
            raise
        except Exception as e:
            error_msg = f"设置模型状态失败 / Failed to set model status: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise ModelRegistryError(error_msg) from e
    
    def set_production_model(self, model_id: str) -> None:
        """
        设置生产模型 / Set Production Model
        
        Args:
            model_id: 模型ID / Model ID
            
        Raises:
            ModelRegistryError: 设置失败时抛出 / Raised when setting fails
        """
        self.set_model_status(model_id, "production")
    
    def get_production_model(self) -> Optional[ModelInfo]:
        """
        获取当前生产模型 / Get Current Production Model
        
        Returns:
            Optional[ModelInfo]: 生产模型信息，如果没有则返回None / Production model info, None if not found
        """
        try:
            for model_data in self._index.values():
                if model_data["status"] == "production":
                    return ModelInfo(**model_data)
            
            return None
            
        except Exception as e:
            error_msg = f"获取生产模型失败 / Failed to get production model: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise ModelRegistryError(error_msg) from e
    
    def delete_model(self, model_id: str) -> None:
        """
        删除模型 / Delete Model
        
        Args:
            model_id: 模型ID / Model ID
            
        Raises:
            ModelRegistryError: 删除失败时抛出 / Raised when deletion fails
        """
        try:
            # 检查模型是否存在 / Check if model exists
            if model_id not in self._index:
                raise ModelRegistryError(
                    f"模型不存在 / Model does not exist: {model_id}"
                )
            
            # 不允许删除生产模型 / Don't allow deleting production model
            if self._index[model_id]["status"] == "production":
                raise ModelRegistryError(
                    f"不能删除生产模型 / Cannot delete production model: {model_id}"
                )
            
            # 删除模型目录 / Delete model directory
            model_dir = self._registry_dir / model_id
            if model_dir.exists():
                shutil.rmtree(model_dir)
            
            # 从索引中删除 / Remove from index
            del self._index[model_id]
            self._save_index()
            
            self._logger.info(
                f"模型删除成功 / Model deleted successfully: {model_id}"
            )
            
        except ModelRegistryError:
            raise
        except Exception as e:
            error_msg = f"删除模型失败 / Failed to delete model: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise ModelRegistryError(error_msg) from e
    
    def _generate_model_id(self, model_name: str, version: str) -> str:
        """
        生成模型ID / Generate Model ID
        
        Args:
            model_name: 模型名称 / Model name
            version: 模型版本 / Model version
            
        Returns:
            str: 模型ID / Model ID
        """
        # 使用模型名称和版本生成ID / Generate ID using model name and version
        base_id = f"{model_name}_v{version}"
        
        # 如果ID已存在，添加时间戳 / If ID exists, add timestamp
        if base_id in self._index:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"{base_id}_{timestamp}"
        
        return base_id
    
    def _load_index(self) -> Dict[str, Dict[str, Any]]:
        """
        加载索引 / Load Index
        
        Returns:
            Dict[str, Dict[str, Any]]: 索引字典 / Index dictionary
        """
        if self._index_file.exists():
            try:
                with open(self._index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self._logger.warning(
                    f"加载索引失败，创建新索引 / Failed to load index, creating new: {str(e)}"
                )
                return {}
        else:
            return {}
    
    def _save_index(self) -> None:
        """
        保存索引 / Save Index
        
        Raises:
            ModelRegistryError: 保存失败时抛出 / Raised when saving fails
        """
        try:
            with open(self._index_file, 'w', encoding='utf-8') as f:
                json.dump(self._index, f, indent=2, ensure_ascii=False)
        except Exception as e:
            error_msg = f"保存索引失败 / Failed to save index: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise ModelRegistryError(error_msg) from e
    
    def _apply_filter(
        self,
        models: List[ModelInfo],
        filter: ModelFilter
    ) -> List[ModelInfo]:
        """
        应用过滤器 / Apply Filter
        
        Args:
            models: 模型列表 / Model list
            filter: 过滤条件 / Filter conditions
            
        Returns:
            List[ModelInfo]: 过滤后的模型列表 / Filtered model list
        """
        filtered = models
        
        # 按模型类型过滤 / Filter by model type
        if filter.model_type:
            filtered = [m for m in filtered if m.model_type == filter.model_type]
        
        # 按状态过滤 / Filter by status
        if filter.status:
            filtered = [m for m in filtered if m.status == filter.status]
        
        # 按性能过滤 / Filter by performance
        if filter.min_performance:
            filtered = [
                m for m in filtered
                if all(
                    m.performance_metrics.get(metric, 0) >= min_val
                    for metric, min_val in filter.min_performance.items()
                )
            ]
        
        # 按日期范围过滤 / Filter by date range
        if filter.date_from:
            filtered = [m for m in filtered if m.training_date >= filter.date_from]
        
        if filter.date_to:
            filtered = [m for m in filtered if m.training_date <= filter.date_to]
        
        return filtered
    
    def _check_and_mark_candidate(
        self,
        model_id: str,
        performance_metrics: Dict[str, float]
    ) -> None:
        """
        检查并标记候选模型 / Check and Mark Candidate Model
        
        如果新模型性能优于当前生产模型，将其标记为候选模型
        If new model performs better than current production model, mark it as candidate
        
        Args:
            model_id: 模型ID / Model ID
            performance_metrics: 性能指标 / Performance metrics
        """
        try:
            # 获取当前生产模型 / Get current production model
            production_model = self.get_production_model()
            
            if not production_model:
                # 如果没有生产模型，不做任何操作 / If no production model, do nothing
                return
            
            # 比较性能指标 / Compare performance metrics
            # 这里使用简单的规则：如果IC均值更高，则认为性能更好
            # Using simple rule here: if IC mean is higher, consider it better
            new_ic = performance_metrics.get("ic_mean", 0)
            prod_ic = production_model.performance_metrics.get("ic_mean", 0)
            
            if new_ic > prod_ic:
                # 标记为候选模型 / Mark as candidate
                self.set_model_status(model_id, "candidate")
                
                self._logger.info(
                    f"新模型性能优于生产模型，标记为候选 / New model performs better, marked as candidate\n"
                    f"新模型ID / New model ID: {model_id}\n"
                    f"新模型IC / New model IC: {new_ic:.4f}\n"
                    f"生产模型IC / Production model IC: {prod_ic:.4f}"
                )
            
        except Exception as e:
            # 这个操作失败不应该影响注册流程 / This operation failure should not affect registration
            self._logger.warning(
                f"检查候选模型失败 / Failed to check candidate model: {str(e)}"
            )
