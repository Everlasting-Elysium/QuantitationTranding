"""
Unit tests for ModelFactory
模型工厂单元测试
"""

import pytest
from src.core.model_factory import ModelFactory
from src.templates.model_templates import ModelTemplateManager

# Try to import qlib models, skip tests if not available
try:
    from qlib.contrib.model.gbdt import LGBModel
    from qlib.contrib.model.linear import LinearModel
    from qlib.contrib.model.pytorch_nn import DNNModelPytorch
    QLIB_AVAILABLE = True
except ImportError:
    QLIB_AVAILABLE = False
    LGBModel = None
    LinearModel = None
    DNNModelPytorch = None

# Skip all tests if qlib is not available
pytestmark = pytest.mark.skipif(not QLIB_AVAILABLE, reason="qlib not installed")


class TestModelFactory:
    """Test suite for ModelFactory"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.factory = ModelFactory()
    
    def test_create_lgbm_model(self):
        """Test creating LightGBM model"""
        model = self.factory.create_model('lgbm', {'num_boost_round': 50})
        assert isinstance(model, LGBModel)
        assert model.num_boost_round == 50
    
    def test_create_linear_model(self):
        """Test creating linear model"""
        model = self.factory.create_model('linear', {'estimator': 'ridge', 'alpha': 0.1})
        assert isinstance(model, LinearModel)
        assert model.estimator == 'ridge'
        assert model.alpha == 0.1
    
    def test_create_mlp_model(self):
        """Test creating MLP model"""
        model = self.factory.create_model('mlp', {'lr': 0.001, 'max_steps': 100})
        assert isinstance(model, DNNModelPytorch)
        assert model.lr == 0.001
        assert model.max_steps == 100
    
    def test_create_model_with_default_params(self):
        """Test creating model with no parameters"""
        model = self.factory.create_model('lgbm')
        assert isinstance(model, LGBModel)
    
    def test_create_model_invalid_type(self):
        """Test creating model with invalid type"""
        with pytest.raises(ValueError) as exc_info:
            self.factory.create_model('invalid_type')
        assert '不支持的模型类型' in str(exc_info.value) or 'Unsupported model type' in str(exc_info.value)
    
    def test_create_model_from_template(self):
        """Test creating model from template"""
        model = self.factory.create_model_from_template('lgbm_default')
        assert isinstance(model, LGBModel)
    
    def test_create_model_from_template_with_custom_params(self):
        """Test creating model from template with custom parameters"""
        model = self.factory.create_model_from_template(
            'lgbm_default',
            {'num_boost_round': 200}
        )
        assert isinstance(model, LGBModel)
        assert model.num_boost_round == 200
    
    def test_create_model_from_invalid_template(self):
        """Test creating model from non-existent template"""
        with pytest.raises(KeyError):
            self.factory.create_model_from_template('non_existent_template')
    
    def test_list_available_models(self):
        """Test listing available model types"""
        models = self.factory.list_available_models()
        assert 'lgbm' in models
        assert 'linear' in models
        assert 'mlp' in models
        assert len(models) == 3
    
    def test_list_templates(self):
        """Test listing available templates"""
        templates = self.factory.list_templates()
        assert len(templates) > 0
        assert all(hasattr(t, 'name') for t in templates)
        assert all(hasattr(t, 'model_type') for t in templates)
    
    def test_list_template_names(self):
        """Test listing template names"""
        names = self.factory.list_template_names()
        assert 'lgbm_default' in names
        assert 'linear_default' in names
        assert 'mlp_default' in names
    
    def test_get_template(self):
        """Test getting a specific template"""
        template = self.factory.get_template('lgbm_default')
        assert template.name == 'lgbm_default'
        assert template.model_type == 'lgbm'
        assert 'num_boost_round' in template.default_params
    
    def test_validate_lgbm_params_invalid_loss(self):
        """Test validation of invalid LightGBM loss parameter"""
        with pytest.raises(ValueError) as exc_info:
            self.factory.create_model('lgbm', {'loss': 'invalid_loss'})
        assert 'loss' in str(exc_info.value).lower()
    
    def test_validate_lgbm_params_invalid_num_boost_round(self):
        """Test validation of invalid num_boost_round parameter"""
        with pytest.raises(ValueError) as exc_info:
            self.factory.create_model('lgbm', {'num_boost_round': -10})
        assert 'num_boost_round' in str(exc_info.value)
    
    def test_validate_lgbm_params_invalid_learning_rate(self):
        """Test validation of invalid learning_rate parameter"""
        with pytest.raises(ValueError) as exc_info:
            self.factory.create_model('lgbm', {'learning_rate': -0.1})
        assert 'learning_rate' in str(exc_info.value)
    
    def test_validate_linear_params_invalid_estimator(self):
        """Test validation of invalid linear estimator parameter"""
        with pytest.raises(ValueError) as exc_info:
            self.factory.create_model('linear', {'estimator': 'invalid_estimator'})
        assert 'estimator' in str(exc_info.value).lower()
    
    def test_validate_linear_params_invalid_alpha(self):
        """Test validation of invalid alpha parameter"""
        with pytest.raises(ValueError) as exc_info:
            self.factory.create_model('linear', {'alpha': -0.5})
        assert 'alpha' in str(exc_info.value).lower()
    
    def test_validate_mlp_params_invalid_lr(self):
        """Test validation of invalid learning rate for MLP"""
        with pytest.raises(ValueError) as exc_info:
            self.factory.create_model('mlp', {'lr': -0.001})
        assert 'lr' in str(exc_info.value).lower()
    
    def test_validate_mlp_params_invalid_epochs(self):
        """Test validation of invalid epochs for MLP"""
        with pytest.raises(ValueError) as exc_info:
            self.factory.create_model('mlp', {'n_epochs': 0})
        assert 'n_epochs' in str(exc_info.value)
    
    def test_validate_mlp_params_invalid_optimizer(self):
        """Test validation of invalid optimizer for MLP"""
        with pytest.raises(ValueError) as exc_info:
            self.factory.create_model('mlp', {'optimizer': 'invalid_optimizer'})
        assert 'optimizer' in str(exc_info.value).lower()


class TestModelFactoryWithCustomTemplateManager:
    """Test ModelFactory with custom template manager"""
    
    def test_factory_with_custom_template_manager(self):
        """Test creating factory with custom template manager"""
        template_manager = ModelTemplateManager()
        factory = ModelFactory(template_manager=template_manager)
        assert factory.template_manager is template_manager
    
    def test_factory_with_none_template_manager(self):
        """Test creating factory with None template manager creates default"""
        factory = ModelFactory(template_manager=None)
        assert factory.template_manager is not None
        assert isinstance(factory.template_manager, ModelTemplateManager)
