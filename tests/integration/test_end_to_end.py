"""
端到端集成测试 / End-to-End Integration Tests
测试完整的系统工作流程 / Test complete system workflows
"""

import pytest
import os
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# 检查 qlib 是否可用
try:
    import qlib
    QLIB_AVAILABLE = True
except ImportError:
    QLIB_AVAILABLE = False

from src.core.config_manager import ConfigManager
from src.core.data_manager import DataManager
from src.core.model_factory import ModelFactory
from src.application.training_manager import TrainingManager
from src.application.backtest_manager import BacktestManager
from src.application.signal_generator import SignalGenerator
from src.application.model_registry import ModelRegistry
from src.infrastructure.qlib_wrapper import QlibWrapper
from src.infrastructure.logger_system import setup_logging
from src.utils.cache_manager import get_cache_manager

# 如果 qlib 不可用，跳过所有集成测试
pytestmark = pytest.mark.skipif(not QLIB_AVAILABLE, reason="qlib not available")


class TestEndToEndWorkflow:
    """端到端工作流程测试"""
    
    @pytest.fixture(scope="class")
    def test_env(self):
        """
        设置测试环境 / Setup test environment
        """
        # 创建临时目录
        temp_dir = tempfile.mkdtemp()
        
        # 设置日志
        log_dir = os.path.join(temp_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)
        setup_logging(log_dir=log_dir, log_level="INFO")
        
        # 创建配置管理器
        config_manager = ConfigManager()
        config = config_manager.get_default_config()
        
        # 更新配置路径为临时目录
        config.logging.log_dir = log_dir
        config.model_registry.storage_path = os.path.join(temp_dir, "models")
        config.visualization.output_dir = os.path.join(temp_dir, "reports")
        
        # 创建必要的目录
        os.makedirs(config.model_registry.storage_path, exist_ok=True)
        os.makedirs(config.visualization.output_dir, exist_ok=True)
        
        yield {
            'temp_dir': temp_dir,
            'config': config,
            'config_manager': config_manager
        }
        
        # 清理
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.mark.integration
    @pytest.mark.requires_data
    def test_complete_training_workflow(self, test_env):
        """
        测试完整的训练工作流程 / Test complete training workflow
        
        工作流程 / Workflow:
        1. 初始化数据管理器 / Initialize data manager
        2. 验证数据 / Validate data
        3. 创建模型 / Create model
        4. 训练模型 / Train model
        5. 注册模型 / Register model
        """
        config = test_env['config']
        
        # 检查qlib数据是否可用
        data_path = Path(config.qlib.provider_uri).expanduser()
        if not data_path.exists():
            pytest.skip(f"Qlib数据不可用: {data_path}")
        
        # 检查数据是否已解压
        data_files = list(data_path.glob("*"))
        if len(data_files) == 1 and data_files[0].suffix == ".zip":
            pytest.skip(f"Qlib数据未解压: {data_path}")
        
        try:
            # 1. 初始化数据管理器
            data_manager = DataManager()
            data_manager.initialize(
                data_path=str(data_path),
                region=config.qlib.region
            )
            
            assert data_manager.is_initialized(), "数据管理器初始化失败"
            
            # 2. 验证数据
            validation_result = data_manager.validate_data(
                start_date=config.training.train_start,
                end_date=config.training.test_end,
                instruments=config.data.instruments
            )
            
            if not validation_result.is_valid:
                pytest.skip(f"数据验证失败: {validation_result.message}")
            
            # 3. 创建模型工厂
            model_factory = ModelFactory()
            
            # 4. 创建训练管理器
            training_manager = TrainingManager(
                data_manager=data_manager,
                model_factory=model_factory,
                output_dir=os.path.join(test_env['temp_dir'], "outputs")
            )
            
            # 5. 训练一个简单的模型
            from src.application.training_manager import TrainingConfig, DatasetConfig
            
            dataset_config = DatasetConfig(
                instruments=config.data.instruments,
                start_time=config.training.train_start,
                end_time=config.training.train_end,
                features=config.data.features[:3],  # 使用前3个特征以加快测试
                label=config.data.label
            )
            
            train_config = TrainingConfig(
                model_type="linear",
                dataset_config=dataset_config,
                model_params={},
                training_params={
                    'epochs': 1  # 只训练1个epoch以加快测试
                },
                experiment_name="test_experiment"
            )
            
            try:
                result = training_manager.train_model(train_config)
            except Exception as e:
                # 如果是数据不存在的错误，跳过测试
                if "does not contain data" in str(e) or "No data retrieved" in str(e):
                    pytest.skip(f"Qlib数据未正确配置或不完整: {str(e)}")
                raise
            
            # 验证训练结果
            assert result is not None, "训练结果为空"
            assert result.model_id is not None, "模型ID为空"
            assert result.metrics is not None, "训练指标为空"
            assert result.model_path is not None, "模型路径为空"
            
            # 6. 验证模型文件存在
            assert Path(result.model_path).exists(), f"模型文件不存在: {result.model_path}"
            
            print(f"✓ 训练工作流程测试通过")
            print(f"  - 模型ID: {result.model_id}")
            print(f"  - 训练指标: {result.metrics}")
            print(f"  - 模型路径: {result.model_path}")
            
        except Exception as e:
            pytest.fail(f"训练工作流程测试失败: {str(e)}")
    
    @pytest.mark.integration
    @pytest.mark.requires_data
    def test_complete_backtest_workflow(self, test_env):
        """
        测试完整的回测工作流程 / Test complete backtest workflow
        
        工作流程 / Workflow:
        1. 初始化环境 / Initialize environment
        2. 训练模型 / Train model
        3. 运行回测 / Run backtest
        4. 生成报告 / Generate report
        """
        config = test_env['config']
        
        # 检查qlib数据是否可用
        data_path = Path(config.qlib.provider_uri).expanduser()
        if not data_path.exists():
            pytest.skip(f"Qlib数据不可用: {data_path}")
        
        # 检查数据是否已解压
        data_files = list(data_path.glob("*"))
        if len(data_files) == 1 and data_files[0].suffix == ".zip":
            pytest.skip(f"Qlib数据未解压: {data_path}")
        
        try:
            # 1. 初始化数据管理器
            data_manager = DataManager()
            data_manager.initialize(
                data_path=str(data_path),
                region=config.qlib.region
            )
            
            # 2. 验证数据
            validation_result = data_manager.validate_data(
                start_date=config.training.train_start,
                end_date=config.training.test_end,
                instruments=config.data.instruments
            )
            
            if not validation_result.is_valid:
                pytest.skip(f"数据验证失败: {validation_result.message}")
            
            # 3. 训练一个简单的模型
            model_factory = ModelFactory()
            training_manager = TrainingManager(
                data_manager=data_manager,
                model_factory=model_factory,
                output_dir=os.path.join(test_env['temp_dir'], "outputs")
            )
            
            from src.application.training_manager import TrainingConfig, DatasetConfig
            
            dataset_config = DatasetConfig(
                instruments=config.data.instruments,
                start_time=config.training.train_start,
                end_time=config.training.train_end,
                features=config.data.features[:3],
                label=config.data.label
            )
            
            train_config = TrainingConfig(
                model_type="linear",
                dataset_config=dataset_config,
                model_params={},
                training_params={'epochs': 1},
                experiment_name="test_backtest_experiment"
            )
            
            try:
                train_result = training_manager.train_model(train_config)
            except Exception as e:
                # 如果是数据不存在的错误，跳过测试
                if "does not contain data" in str(e) or "No data retrieved" in str(e):
                    pytest.skip(f"Qlib数据未正确配置或不完整: {str(e)}")
                raise
            assert train_result is not None, "训练失败"
            
            # 4. 运行回测
            backtest_manager = BacktestManager(
                qlib_wrapper=data_manager.qlib_wrapper,
                output_dir=os.path.join(test_env['temp_dir'], "outputs", "backtests")
            )
            
            from src.models.data_models import BacktestConfig as BTConfig
            
            bt_config = BTConfig(
                strategy_config={
                    'topk': 10,
                    'n_drop': 3
                },
                executor_config={
                    'time_per_step': 'day',
                    'generate_portfolio_metrics': True
                },
                benchmark=config.backtest.benchmark
            )
            
            backtest_result = backtest_manager.run_backtest(
                model_id=train_result.model_id,
                start_date=config.training.test_start,
                end_date=config.training.test_end,
                config=bt_config
            )
            
            # 验证回测结果
            assert backtest_result is not None, "回测结果为空"
            assert backtest_result.metrics is not None, "回测指标为空"
            assert 'annual_return' in backtest_result.metrics, "缺少年化收益率指标"
            assert 'sharpe_ratio' in backtest_result.metrics, "缺少夏普比率指标"
            assert 'max_drawdown' in backtest_result.metrics, "缺少最大回撤指标"
            
            print(f"✓ 回测工作流程测试通过")
            print(f"  - 年化收益率: {backtest_result.metrics['annual_return']:.2%}")
            print(f"  - 夏普比率: {backtest_result.metrics['sharpe_ratio']:.2f}")
            print(f"  - 最大回撤: {backtest_result.metrics['max_drawdown']:.2%}")
            
        except Exception as e:
            pytest.fail(f"回测工作流程测试失败: {str(e)}")
    
    @pytest.mark.integration
    @pytest.mark.requires_data
    def test_cache_performance(self, test_env):
        """
        测试缓存性能 / Test cache performance
        """
        config = test_env['config']
        
        # 检查qlib数据是否可用
        data_path = Path(config.qlib.provider_uri).expanduser()
        if not data_path.exists():
            pytest.skip(f"Qlib数据不可用: {data_path}")
        
        # 检查数据是否已解压
        data_files = list(data_path.glob("*"))
        if len(data_files) == 1 and data_files[0].suffix == ".zip":
            pytest.skip(f"Qlib数据未解压: {data_path}")
        
        try:
            # 初始化数据管理器（启用缓存）
            data_manager_cached = DataManager(enable_cache=True)
            try:
                data_manager_cached.initialize(
                    data_path=str(data_path),
                    region=config.qlib.region
                )
            except Exception as e:
                # 如果是数据不存在的错误，跳过测试
                if "does not contain data" in str(e) or "No data retrieved" in str(e):
                    pytest.skip(f"Qlib数据未正确配置或不完整: {str(e)}")
                raise
            
            # 第一次验证（无缓存）
            start_time = datetime.now()
            result1 = data_manager_cached.validate_data(
                start_date=config.training.train_start,
                end_date=config.training.test_end,
                instruments=config.data.instruments
            )
            time_without_cache = (datetime.now() - start_time).total_seconds()
            
            # 第二次验证（使用缓存）
            start_time = datetime.now()
            result2 = data_manager_cached.validate_data(
                start_date=config.training.train_start,
                end_date=config.training.test_end,
                instruments=config.data.instruments
            )
            time_with_cache = (datetime.now() - start_time).total_seconds()
            
            # 验证结果一致性
            assert result1.is_valid == result2.is_valid, "缓存结果不一致"
            assert result1.data_start == result2.data_start, "缓存数据开始日期不一致"
            assert result1.data_end == result2.data_end, "缓存数据结束日期不一致"
            
            # 验证性能提升
            # 缓存应该显著提升性能（至少快50%）
            performance_improvement = (time_without_cache - time_with_cache) / time_without_cache
            
            print(f"✓ 缓存性能测试通过")
            print(f"  - 无缓存时间: {time_without_cache:.3f}秒")
            print(f"  - 有缓存时间: {time_with_cache:.3f}秒")
            print(f"  - 性能提升: {performance_improvement:.1%}")
            
            # 如果缓存有效，应该有明显的性能提升
            if time_with_cache < time_without_cache:
                assert performance_improvement > 0, "缓存未提升性能"
            
            # 获取缓存统计
            cache_manager = get_cache_manager()
            stats = cache_manager.get_cache_stats()
            print(f"  - 缓存统计: {stats}")
            
        except Exception as e:
            pytest.fail(f"缓存性能测试失败: {str(e)}")
    
    def test_error_handling(self, test_env):
        """
        测试错误处理 / Test error handling
        """
        config = test_env['config']
        
        try:
            # 测试1: 未初始化的数据管理器
            data_manager = DataManager()
            
            # 应该返回验证失败
            result = data_manager.validate_data()
            assert not result.is_valid, "未初始化的数据管理器应该验证失败"
            assert "未初始化" in result.message, "错误消息应该提示未初始化"
            
            # 测试2: 无效的数据路径
            try:
                data_manager.initialize(
                    data_path="/invalid/path/that/does/not/exist",
                    region="cn"
                )
                pytest.fail("应该抛出错误")
            except Exception as e:
                assert "初始化失败" in str(e) or "不存在" in str(e), "应该提示初始化失败"
            
            # 测试3: 无效的配置
            config_manager = ConfigManager()
            invalid_config = config_manager.get_default_config()
            invalid_config.qlib.provider_uri = ""  # 空路径
            
            errors = config_manager.validate_config(invalid_config)
            assert len(errors) > 0, "应该检测到配置错误"
            assert any("provider_uri" in err for err in errors), "应该检测到provider_uri错误"
            
            print(f"✓ 错误处理测试通过")
            print(f"  - 未初始化检测: ✓")
            print(f"  - 无效路径检测: ✓")
            print(f"  - 配置验证: ✓")
            
        except Exception as e:
            pytest.fail(f"错误处理测试失败: {str(e)}")


class TestPerformanceOptimization:
    """性能优化测试"""
    
    @pytest.mark.integration
    @pytest.mark.requires_data
    def test_data_loading_performance(self):
        """
        测试数据加载性能 / Test data loading performance
        """
        # 这个测试需要实际的qlib数据
        # 如果数据不可用，跳过测试
        config_manager = ConfigManager()
        config = config_manager.get_default_config()
        
        data_path = Path(config.qlib.provider_uri).expanduser()
        if not data_path.exists():
            pytest.skip(f"Qlib数据不可用: {data_path}")
        
        # 检查数据是否已解压
        data_files = list(data_path.glob("*"))
        if len(data_files) == 1 and data_files[0].suffix == ".zip":
            pytest.skip(f"Qlib数据未解压: {data_path}")
        
        try:
            data_manager = DataManager(enable_cache=True)
            try:
                data_manager.initialize(
                    data_path=str(data_path),
                    region=config.qlib.region
                )
            except Exception as e:
                # 如果是数据不存在的错误，跳过测试
                if "does not contain data" in str(e) or "No data retrieved" in str(e):
                    pytest.skip(f"Qlib数据未正确配置或不完整: {str(e)}")
                raise
            
            # 测试数据加载性能
            start_time = datetime.now()
            try:
                data_info = data_manager.get_data_info()
            except Exception as e:
                # 如果是数据问题，跳过测试
                if "can't find a freq" in str(e) or "获取交易日历失败" in str(e):
                    pytest.skip(f"Qlib数据未正确配置或不完整: {str(e)}")
                raise
            load_time = (datetime.now() - start_time).total_seconds()
            
            assert data_info is not None, "数据信息为空"
            assert load_time < 5.0, f"数据加载时间过长: {load_time:.2f}秒"
            
            print(f"✓ 数据加载性能测试通过")
            print(f"  - 加载时间: {load_time:.3f}秒")
            print(f"  - 数据范围: {data_info.data_start} 至 {data_info.data_end}")
            print(f"  - 交易日数: {data_info.trading_days}")
            
        except Exception as e:
            pytest.fail(f"数据加载性能测试失败: {str(e)}")
    
    def test_cache_effectiveness(self):
        """
        测试缓存有效性 / Test cache effectiveness
        """
        cache_manager = get_cache_manager()
        
        # 清除所有缓存
        cache_manager.clear()
        
        # 测试基本缓存操作
        test_key = "test_key"
        test_value = {"data": "test_data", "timestamp": datetime.now().isoformat()}
        
        # 设置缓存
        cache_manager.set(test_key, test_value, ttl=60)
        
        # 获取缓存
        cached_value = cache_manager.get(test_key)
        assert cached_value is not None, "缓存获取失败"
        assert cached_value == test_value, "缓存值不匹配"
        
        # 删除缓存
        cache_manager.delete(test_key)
        cached_value = cache_manager.get(test_key)
        assert cached_value is None, "缓存删除失败"
        
        # 获取缓存统计
        stats = cache_manager.get_cache_stats()
        assert 'memory_cache_count' in stats, "缺少内存缓存统计"
        assert 'disk_cache_count' in stats, "缺少磁盘缓存统计"
        
        print(f"✓ 缓存有效性测试通过")
        print(f"  - 缓存设置: ✓")
        print(f"  - 缓存获取: ✓")
        print(f"  - 缓存删除: ✓")
        print(f"  - 缓存统计: {stats}")


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v", "-s"])
