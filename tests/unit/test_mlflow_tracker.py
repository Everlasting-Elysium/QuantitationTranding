"""
MLflowTracker单元测试 / MLflowTracker Unit Tests
"""
import pytest
from unittest.mock import Mock, MagicMock, patch, call
from pathlib import Path

from src.infrastructure.mlflow_tracker import (
    MLflowTracker,
    MLflowError
)


class TestMLflowTracker:
    """MLflowTracker测试套件 / MLflowTracker Test Suite"""
    
    def test_initialization(self):
        """测试初始化 / Test initialization"""
        tracker = MLflowTracker()
        assert tracker is not None
        assert not tracker.is_initialized()
        assert tracker.tracking_uri == "./mlruns"
    
    def test_initialization_with_custom_uri(self):
        """测试自定义URI初始化 / Test initialization with custom URI"""
        custom_uri = "./custom_mlruns"
        tracker = MLflowTracker(tracking_uri=custom_uri)
        assert tracker.tracking_uri == custom_uri
    
    @patch('src.infrastructure.mlflow_tracker.mlflow')
    @patch('src.infrastructure.mlflow_tracker.MlflowClient')
    @patch('src.infrastructure.mlflow_tracker.MLFLOW_AVAILABLE', True)
    def test_initialize_success(self, mock_client_class, mock_mlflow):
        """测试成功初始化MLflow / Test successful MLflow initialization"""
        # 设置mock / Setup mocks
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        tracker = MLflowTracker()
        tracker.initialize()
        
        # 验证 / Verify
        assert tracker.is_initialized()
        mock_mlflow.set_tracking_uri.assert_called_once_with("./mlruns")
        mock_client_class.assert_called_once()
    
    @patch('src.infrastructure.mlflow_tracker.MLFLOW_AVAILABLE', False)
    def test_initialize_mlflow_not_available(self):
        """测试MLflow未安装时的初始化 / Test initialization when MLflow not available"""
        tracker = MLflowTracker()
        
        with pytest.raises(MLflowError) as exc_info:
            tracker.initialize()
        
        assert "MLflow未安装" in str(exc_info.value) or "not installed" in str(exc_info.value)
    
    @patch('src.infrastructure.mlflow_tracker.mlflow')
    @patch('src.infrastructure.mlflow_tracker.MlflowClient')
    @patch('src.infrastructure.mlflow_tracker.MLFLOW_AVAILABLE', True)
    def test_create_experiment_new(self, mock_client_class, mock_mlflow):
        """测试创建新实验 / Test creating new experiment"""
        # 设置mock / Setup mocks
        mock_client = Mock()
        mock_client.get_experiment_by_name.return_value = None
        mock_client.create_experiment.return_value = "exp_123"
        mock_client_class.return_value = mock_client
        
        tracker = MLflowTracker()
        tracker.initialize()
        
        # 创建实验 / Create experiment
        exp_id = tracker.create_experiment("test_experiment")
        
        # 验证 / Verify
        assert exp_id == "exp_123"
        mock_client.get_experiment_by_name.assert_called_once_with("test_experiment")
        mock_client.create_experiment.assert_called_once()
    
    @patch('src.infrastructure.mlflow_tracker.mlflow')
    @patch('src.infrastructure.mlflow_tracker.MlflowClient')
    @patch('src.infrastructure.mlflow_tracker.MLFLOW_AVAILABLE', True)
    def test_create_experiment_existing(self, mock_client_class, mock_mlflow):
        """测试使用已存在的实验 / Test using existing experiment"""
        # 设置mock / Setup mocks
        mock_experiment = Mock()
        mock_experiment.experiment_id = "exp_456"
        
        mock_client = Mock()
        mock_client.get_experiment_by_name.return_value = mock_experiment
        mock_client_class.return_value = mock_client
        
        tracker = MLflowTracker()
        tracker.initialize()
        
        # 创建实验 / Create experiment
        exp_id = tracker.create_experiment("existing_experiment")
        
        # 验证 / Verify
        assert exp_id == "exp_456"
        mock_client.create_experiment.assert_not_called()
    
    def test_create_experiment_not_initialized(self):
        """测试未初始化时创建实验 / Test creating experiment when not initialized"""
        tracker = MLflowTracker()
        
        with pytest.raises(MLflowError) as exc_info:
            tracker.create_experiment("test")
        
        assert "未初始化" in str(exc_info.value) or "not initialized" in str(exc_info.value)
    
    @patch('src.infrastructure.mlflow_tracker.mlflow')
    @patch('src.infrastructure.mlflow_tracker.MlflowClient')
    @patch('src.infrastructure.mlflow_tracker.MLFLOW_AVAILABLE', True)
    def test_start_run(self, mock_client_class, mock_mlflow):
        """测试开始运行 / Test starting run"""
        # 设置mock / Setup mocks
        mock_run_info = Mock()
        mock_run_info.run_id = "run_789"
        mock_run = Mock()
        mock_run.info = mock_run_info
        
        mock_experiment = Mock()
        mock_experiment.experiment_id = "exp_123"
        
        mock_client = Mock()
        mock_client.get_experiment_by_name.return_value = mock_experiment
        mock_client.create_run.return_value = mock_run
        mock_client_class.return_value = mock_client
        
        tracker = MLflowTracker()
        tracker.initialize()
        
        # 开始运行 / Start run
        run_id = tracker.start_run("test_experiment", run_name="test_run")
        
        # 验证 / Verify
        assert run_id == "run_789"
        assert tracker.get_current_run_id() == "run_789"
        mock_client.create_run.assert_called_once()
    
    @patch('src.infrastructure.mlflow_tracker.mlflow')
    @patch('src.infrastructure.mlflow_tracker.MlflowClient')
    @patch('src.infrastructure.mlflow_tracker.MLFLOW_AVAILABLE', True)
    def test_log_params(self, mock_client_class, mock_mlflow):
        """测试记录参数 / Test logging parameters"""
        # 设置mock / Setup mocks
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        tracker = MLflowTracker()
        tracker.initialize()
        tracker._current_run_id = "run_123"
        
        # 记录参数 / Log parameters
        params = {"learning_rate": 0.01, "batch_size": 32}
        tracker.log_params(params)
        
        # 验证 / Verify
        assert mock_client.log_param.call_count == 2
    
    def test_log_params_no_active_run(self):
        """测试无活动运行时记录参数 / Test logging parameters without active run"""
        tracker = MLflowTracker()
        
        with pytest.raises(MLflowError) as exc_info:
            tracker.log_params({"key": "value"})
        
        assert "没有活动的运行" in str(exc_info.value) or "No active run" in str(exc_info.value)
    
    @patch('src.infrastructure.mlflow_tracker.mlflow')
    @patch('src.infrastructure.mlflow_tracker.MlflowClient')
    @patch('src.infrastructure.mlflow_tracker.MLFLOW_AVAILABLE', True)
    def test_log_metrics(self, mock_client_class, mock_mlflow):
        """测试记录指标 / Test logging metrics"""
        # 设置mock / Setup mocks
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        tracker = MLflowTracker()
        tracker.initialize()
        tracker._current_run_id = "run_123"
        
        # 记录指标 / Log metrics
        metrics = {"accuracy": 0.95, "loss": 0.05}
        tracker.log_metrics(metrics, step=10)
        
        # 验证 / Verify
        assert mock_client.log_metric.call_count == 2
        # 验证step参数 / Verify step parameter
        calls = mock_client.log_metric.call_args_list
        for call_args in calls:
            assert call_args[1]['step'] == 10
    
    @patch('src.infrastructure.mlflow_tracker.mlflow')
    @patch('src.infrastructure.mlflow_tracker.MlflowClient')
    @patch('src.infrastructure.mlflow_tracker.MLFLOW_AVAILABLE', True)
    def test_log_single_metric(self, mock_client_class, mock_mlflow):
        """测试记录单个指标 / Test logging single metric"""
        # 设置mock / Setup mocks
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        tracker = MLflowTracker()
        tracker.initialize()
        tracker._current_run_id = "run_123"
        
        # 记录单个指标 / Log single metric
        tracker.log_metric("accuracy", 0.95, step=5)
        
        # 验证 / Verify
        mock_client.log_metric.assert_called_once()
    
    @patch('src.infrastructure.mlflow_tracker.mlflow')
    @patch('src.infrastructure.mlflow_tracker.MlflowClient')
    @patch('src.infrastructure.mlflow_tracker.MLFLOW_AVAILABLE', True)
    def test_set_tags(self, mock_client_class, mock_mlflow):
        """测试设置标签 / Test setting tags"""
        # 设置mock / Setup mocks
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        tracker = MLflowTracker()
        tracker.initialize()
        tracker._current_run_id = "run_123"
        
        # 设置标签 / Set tags
        tags = {"model_type": "lgbm", "version": "1.0"}
        tracker.set_tags(tags)
        
        # 验证 / Verify
        assert mock_client.set_tag.call_count == 2
    
    @patch('src.infrastructure.mlflow_tracker.mlflow')
    @patch('src.infrastructure.mlflow_tracker.MlflowClient')
    @patch('src.infrastructure.mlflow_tracker.MLFLOW_AVAILABLE', True)
    def test_end_run(self, mock_client_class, mock_mlflow):
        """测试结束运行 / Test ending run"""
        # 设置mock / Setup mocks
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        tracker = MLflowTracker()
        tracker.initialize()
        tracker._current_run_id = "run_123"
        
        # 结束运行 / End run
        tracker.end_run(status="FINISHED")
        
        # 验证 / Verify
        mock_client.set_terminated.assert_called_once_with("run_123", status="FINISHED")
        assert tracker.get_current_run_id() is None
    
    def test_end_run_no_active_run(self):
        """测试无活动运行时结束运行 / Test ending run without active run"""
        tracker = MLflowTracker()
        
        # 不应抛出异常 / Should not raise exception
        tracker.end_run()
    
    @patch('src.infrastructure.mlflow_tracker.mlflow')
    @patch('src.infrastructure.mlflow_tracker.MlflowClient')
    @patch('src.infrastructure.mlflow_tracker.MLFLOW_AVAILABLE', True)
    def test_log_artifact(self, mock_client_class, mock_mlflow, temp_dir):
        """测试记录工件 / Test logging artifact"""
        # 创建临时文件 / Create temporary file
        test_file = temp_dir / "test_artifact.txt"
        test_file.write_text("test content")
        
        # 设置mock / Setup mocks
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        tracker = MLflowTracker()
        tracker.initialize()
        tracker._current_run_id = "run_123"
        
        # 记录工件 / Log artifact
        tracker.log_artifact(str(test_file))
        
        # 验证 / Verify
        mock_client.log_artifact.assert_called_once()
    
    def test_log_artifact_file_not_exists(self):
        """测试记录不存在的工件 / Test logging non-existent artifact"""
        tracker = MLflowTracker()
        tracker._current_run_id = "run_123"
        
        with pytest.raises(MLflowError) as exc_info:
            tracker.log_artifact("/nonexistent/file.txt")
        
        assert "不存在" in str(exc_info.value) or "does not exist" in str(exc_info.value)
    
    @patch('src.infrastructure.mlflow_tracker.mlflow')
    @patch('src.infrastructure.mlflow_tracker.MlflowClient')
    @patch('src.infrastructure.mlflow_tracker.MLFLOW_AVAILABLE', True)
    def test_get_run_info(self, mock_client_class, mock_mlflow):
        """测试获取运行信息 / Test getting run info"""
        # 设置mock / Setup mocks
        mock_run_info = Mock()
        mock_run_info.run_id = "run_123"
        mock_run_info.experiment_id = "exp_456"
        mock_run_info.status = "FINISHED"
        mock_run_info.start_time = 1234567890
        mock_run_info.end_time = 1234567900
        mock_run_info.artifact_uri = "file:///path/to/artifacts"
        
        mock_run_data = Mock()
        mock_run_data.params = {"param1": "value1"}
        mock_run_data.metrics = {"metric1": 0.95}
        mock_run_data.tags = {"tag1": "value1"}
        
        mock_run = Mock()
        mock_run.info = mock_run_info
        mock_run.data = mock_run_data
        
        mock_client = Mock()
        mock_client.get_run.return_value = mock_run
        mock_client_class.return_value = mock_client
        
        tracker = MLflowTracker()
        tracker.initialize()
        tracker._current_run_id = "run_123"
        
        # 获取运行信息 / Get run info
        info = tracker.get_run_info()
        
        # 验证 / Verify
        assert info["run_id"] == "run_123"
        assert info["experiment_id"] == "exp_456"
        assert info["status"] == "FINISHED"
        assert "params" in info
        assert "metrics" in info
        assert "tags" in info
    
    def test_get_run_info_no_run(self):
        """测试无运行时获取信息 / Test getting info without run"""
        tracker = MLflowTracker()
        
        with pytest.raises(MLflowError) as exc_info:
            tracker.get_run_info()
        
        assert "没有指定运行ID" in str(exc_info.value) or "No run ID" in str(exc_info.value)
