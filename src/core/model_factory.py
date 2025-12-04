"""
Model Factory for Qlib Trading System
模型工厂 - 负责创建和管理各种类型的模型

This module provides a factory pattern for creating different types of
quantitative trading models supported by qlib.
本模块提供工厂模式来创建qlib支持的各种量化交易模型。
"""

from typing import Dict, Any, Optional
from src.templates.model_templates import ModelTemplateManager
from src.models.data_models import ModelTemplate

# Lazy import qlib models to avoid import errors during testing
# 延迟导入qlib模型以避免测试时的导入错误
def _import_qlib_models():
    """Import qlib model classes lazily"""
    models = {}
    errors = []
    
    # Try to import LightGBM model
    try:
        from qlib.contrib.model.gbdt import LGBModel
        models['lgbm'] = LGBModel
    except ImportError as e:
        errors.append(f"lgbm: {str(e)}")
    
    # Try to import Linear model
    try:
        from qlib.contrib.model.linear import LinearModel
        models['linear'] = LinearModel
    except ImportError as e:
        errors.append(f"linear: {str(e)}")
    
    # Try to import MLP model (requires torch)
    try:
        from qlib.contrib.model.pytorch_nn import DNNModelPytorch
        models['mlp'] = DNNModelPytorch
    except ImportError as e:
        errors.append(f"mlp: {str(e)}")
    
    if not models:
        raise ImportError(
            f"无法导入任何qlib模型类。请确保qlib已正确安装。\n"
            f"Failed to import any qlib model classes. Please ensure qlib is properly installed.\n"
            f"Errors: {'; '.join(errors)}"
        )
    
    return models


class ModelFactory:
    """
    Model Factory for creating qlib models.
    模型工厂，用于创建qlib模型。
    
    This factory supports creating models from:
    - Direct model type and parameters
    - Pre-configured templates
    
    本工厂支持通过以下方式创建模型：
    - 直接指定模型类型和参数
    - 使用预配置的模板
    
    Supported model types:
    - lgbm: LightGBM model
    - linear: Linear regression model
    - mlp: Multi-layer perceptron (neural network)
    
    支持的模型类型：
    - lgbm: LightGBM模型
    - linear: 线性回归模型
    - mlp: 多层感知机（神经网络）
    """
    
    # Mapping of model type strings to model classes (loaded lazily)
    # 模型类型字符串到模型类的映射（延迟加载）
    _MODEL_CLASSES = None
    
    @property
    def MODEL_CLASSES(self):
        """Get model classes, loading them lazily if needed"""
        if ModelFactory._MODEL_CLASSES is None:
            ModelFactory._MODEL_CLASSES = _import_qlib_models()
        return ModelFactory._MODEL_CLASSES
    
    def __init__(self, template_manager: Optional[ModelTemplateManager] = None):
        """
        Initialize the model factory.
        初始化模型工厂。
        
        Args:
            template_manager: Optional template manager for loading templates.
                            If None, creates a new one with default config.
                            可选的模板管理器，用于加载模板。
                            如果为None，则使用默认配置创建新的管理器。
        """
        if template_manager is None:
            template_manager = ModelTemplateManager()
        self.template_manager = template_manager
    
    def create_model(self, model_type: str, params: Optional[Dict[str, Any]] = None):
        """
        Create a model instance by type and parameters.
        根据类型和参数创建模型实例。
        
        Args:
            model_type: Type of model to create ('lgbm', 'linear', 'mlp')
                       要创建的模型类型
            params: Model parameters. If None, uses empty dict.
                   模型参数。如果为None，使用空字典。
        
        Returns:
            Model instance
            模型实例
        
        Raises:
            ValueError: If model_type is not supported
                       如果模型类型不支持
        
        Examples:
            >>> factory = ModelFactory()
            >>> # Create LightGBM model with custom parameters
            >>> model = factory.create_model('lgbm', {'num_boost_round': 100})
            >>> # Create linear model with default parameters
            >>> model = factory.create_model('linear')
        """
        if params is None:
            params = {}
        
        # Validate model type
        # 验证模型类型
        if model_type not in self.MODEL_CLASSES:
            available_types = ', '.join(self.MODEL_CLASSES.keys())
            raise ValueError(
                f"不支持的模型类型: {model_type}。"
                f"支持的类型: {available_types}\n"
                f"Unsupported model type: {model_type}. "
                f"Available types: {available_types}"
            )
        
        # Validate parameters
        # 验证参数
        validated_params = self._validate_params(model_type, params)
        
        # Create model instance
        # 创建模型实例
        model_class = self.MODEL_CLASSES[model_type]
        try:
            model = model_class(**validated_params)
            return model
        except Exception as e:
            raise ValueError(
                f"创建模型失败: {str(e)}\n"
                f"模型类型: {model_type}\n"
                f"参数: {validated_params}\n"
                f"Failed to create model: {str(e)}\n"
                f"Model type: {model_type}\n"
                f"Parameters: {validated_params}"
            )
    
    def create_model_from_template(
        self, 
        template_name: str, 
        custom_params: Optional[Dict[str, Any]] = None
    ):
        """
        Create a model from a pre-configured template.
        从预配置的模板创建模型。
        
        Args:
            template_name: Name of the template to use
                          要使用的模板名称
            custom_params: Optional parameters to override template defaults
                          可选参数，用于覆盖模板默认值
        
        Returns:
            Model instance
            模型实例
        
        Raises:
            KeyError: If template doesn't exist
                     如果模板不存在
            ValueError: If model creation fails
                       如果模型创建失败
        
        Examples:
            >>> factory = ModelFactory()
            >>> # Create model from template with default parameters
            >>> model = factory.create_model_from_template('lgbm_default')
            >>> # Create model from template with custom parameters
            >>> model = factory.create_model_from_template(
            ...     'lgbm_default',
            ...     {'num_boost_round': 200}
            ... )
        """
        # Get template
        # 获取模板
        template = self.template_manager.get_template(template_name)
        
        # Merge template params with custom params
        # 合并模板参数和自定义参数
        params = template.default_params.copy()
        if custom_params:
            params.update(custom_params)
        
        # Create model
        # 创建模型
        return self.create_model(template.model_type, params)
    
    def get_template(self, template_name: str) -> ModelTemplate:
        """
        Get a template by name.
        根据名称获取模板。
        
        Args:
            template_name: Name of the template
                          模板名称
        
        Returns:
            ModelTemplate object
            模板对象
        
        Raises:
            KeyError: If template doesn't exist
                     如果模板不存在
        """
        return self.template_manager.get_template(template_name)
    
    def list_available_models(self) -> list:
        """
        List all available model types.
        列出所有可用的模型类型。
        
        Returns:
            List of model type strings
            模型类型字符串列表
        
        Examples:
            >>> factory = ModelFactory()
            >>> types = factory.list_available_models()
            >>> print(types)
            ['lgbm', 'linear', 'mlp']
        """
        return ['lgbm', 'linear', 'mlp']
    
    def list_templates(self) -> list:
        """
        List all available templates.
        列出所有可用的模板。
        
        Returns:
            List of ModelTemplate objects
            模板对象列表
        
        Examples:
            >>> factory = ModelFactory()
            >>> templates = factory.list_templates()
            >>> for template in templates:
            ...     print(f"{template.name}: {template.description}")
        """
        return self.template_manager.list_templates()
    
    def list_template_names(self) -> list:
        """
        List all template names.
        列出所有模板名称。
        
        Returns:
            List of template name strings
            模板名称字符串列表
        
        Examples:
            >>> factory = ModelFactory()
            >>> names = factory.list_template_names()
            >>> print(names)
            ['lgbm_default', 'linear_default', 'mlp_default', ...]
        """
        return self.template_manager.list_template_names()
    
    def _validate_params(self, model_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and process parameters for a specific model type.
        验证和处理特定模型类型的参数。
        
        Args:
            model_type: Type of model
                       模型类型
            params: Parameters to validate
                   要验证的参数
        
        Returns:
            Validated parameters
            验证后的参数
        
        Raises:
            ValueError: If parameters are invalid
                       如果参数无效
        """
        validated = params.copy()
        
        if model_type == 'lgbm':
            validated = self._validate_lgbm_params(validated)
        elif model_type == 'linear':
            validated = self._validate_linear_params(validated)
        elif model_type == 'mlp':
            validated = self._validate_mlp_params(validated)
        
        return validated
    
    def _validate_lgbm_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate LightGBM parameters.
        验证LightGBM参数。
        
        Args:
            params: Parameters to validate
                   要验证的参数
        
        Returns:
            Validated parameters
            验证后的参数
        
        Raises:
            ValueError: If parameters are invalid
                       如果参数无效
        """
        validated = params.copy()
        
        # Validate loss function
        # 验证损失函数
        if 'loss' in validated:
            if validated['loss'] not in ['mse', 'binary']:
                raise ValueError(
                    f"LightGBM loss必须是'mse'或'binary'，当前值: {validated['loss']}\n"
                    f"LightGBM loss must be 'mse' or 'binary', got: {validated['loss']}"
                )
        
        # Validate numeric parameters
        # 验证数值参数
        if 'num_boost_round' in validated:
            if not isinstance(validated['num_boost_round'], int) or validated['num_boost_round'] <= 0:
                raise ValueError(
                    f"num_boost_round必须是正整数，当前值: {validated['num_boost_round']}\n"
                    f"num_boost_round must be a positive integer, got: {validated['num_boost_round']}"
                )
        
        if 'learning_rate' in validated:
            if not isinstance(validated['learning_rate'], (int, float)) or validated['learning_rate'] <= 0:
                raise ValueError(
                    f"learning_rate必须是正数，当前值: {validated['learning_rate']}\n"
                    f"learning_rate must be a positive number, got: {validated['learning_rate']}"
                )
        
        if 'max_depth' in validated:
            if not isinstance(validated['max_depth'], int) or validated['max_depth'] <= 0:
                raise ValueError(
                    f"max_depth必须是正整数，当前值: {validated['max_depth']}\n"
                    f"max_depth must be a positive integer, got: {validated['max_depth']}"
                )
        
        return validated
    
    def _validate_linear_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate linear model parameters.
        验证线性模型参数。
        
        Args:
            params: Parameters to validate
                   要验证的参数
        
        Returns:
            Validated parameters
            验证后的参数
        
        Raises:
            ValueError: If parameters are invalid
                       如果参数无效
        """
        validated = params.copy()
        
        # Validate estimator type
        # 验证估计器类型
        if 'estimator' in validated:
            valid_estimators = ['ols', 'nnls', 'ridge', 'lasso']
            if validated['estimator'] not in valid_estimators:
                raise ValueError(
                    f"estimator必须是{valid_estimators}之一，当前值: {validated['estimator']}\n"
                    f"estimator must be one of {valid_estimators}, got: {validated['estimator']}"
                )
        
        # Validate alpha parameter
        # 验证alpha参数
        if 'alpha' in validated:
            if not isinstance(validated['alpha'], (int, float)) or validated['alpha'] < 0:
                raise ValueError(
                    f"alpha必须是非负数，当前值: {validated['alpha']}\n"
                    f"alpha must be a non-negative number, got: {validated['alpha']}"
                )
        
        # Validate fit_intercept
        # 验证fit_intercept
        if 'fit_intercept' in validated:
            if not isinstance(validated['fit_intercept'], bool):
                raise ValueError(
                    f"fit_intercept必须是布尔值，当前值: {validated['fit_intercept']}\n"
                    f"fit_intercept must be a boolean, got: {validated['fit_intercept']}"
                )
        
        return validated
    
    def _validate_mlp_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate MLP (neural network) parameters.
        验证MLP（神经网络）参数。
        
        Args:
            params: Parameters to validate
                   要验证的参数
        
        Returns:
            Validated parameters
            验证后的参数
        
        Raises:
            ValueError: If parameters are invalid
                       如果参数无效
        """
        validated = params.copy()
        
        # Validate learning rate
        # 验证学习率
        if 'lr' in validated:
            if not isinstance(validated['lr'], (int, float)) or validated['lr'] <= 0:
                raise ValueError(
                    f"lr必须是正数，当前值: {validated['lr']}\n"
                    f"lr must be a positive number, got: {validated['lr']}"
                )
        
        # Validate epochs
        # 验证训练轮数
        if 'n_epochs' in validated:
            if not isinstance(validated['n_epochs'], int) or validated['n_epochs'] <= 0:
                raise ValueError(
                    f"n_epochs必须是正整数，当前值: {validated['n_epochs']}\n"
                    f"n_epochs must be a positive integer, got: {validated['n_epochs']}"
                )
        
        # Validate batch size
        # 验证批次大小
        if 'batch_size' in validated:
            if not isinstance(validated['batch_size'], int) or validated['batch_size'] <= 0:
                raise ValueError(
                    f"batch_size必须是正整数，当前值: {validated['batch_size']}\n"
                    f"batch_size must be a positive integer, got: {validated['batch_size']}"
                )
        
        # Validate optimizer
        # 验证优化器
        if 'optimizer' in validated:
            valid_optimizers = ['adam', 'sgd', 'gd']
            if validated['optimizer'] not in valid_optimizers:
                raise ValueError(
                    f"optimizer必须是{valid_optimizers}之一，当前值: {validated['optimizer']}\n"
                    f"optimizer must be one of {valid_optimizers}, got: {validated['optimizer']}"
                )
        
        # Validate loss function
        # 验证损失函数
        if 'loss' in validated:
            valid_losses = ['mse', 'mae']
            if validated['loss'] not in valid_losses:
                raise ValueError(
                    f"loss必须是{valid_losses}之一，当前值: {validated['loss']}\n"
                    f"loss must be one of {valid_losses}, got: {validated['loss']}"
                )
        
        return validated
