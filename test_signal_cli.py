#!/usr/bin/env python3
"""
信号生成CLI测试脚本 / Signal Generation CLI Test Script

测试信号生成功能的基本功能
Test basic functionality of signal generation
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# 添加src目录到路径 / Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_signal_generator_initialization():
    """
    测试信号生成器初始化 / Test signal generator initialization
    """
    print("\n" + "=" * 70)
    print("测试1: 信号生成器初始化 / Test 1: Signal Generator Initialization")
    print("=" * 70)
    
    try:
        from src.application.signal_generator import SignalGenerator
        from src.application.model_registry import ModelRegistry
        from src.infrastructure.qlib_wrapper import QlibWrapper
        
        # 创建依赖 / Create dependencies
        model_registry = ModelRegistry()
        qlib_wrapper = QlibWrapper()
        
        # 初始化qlib（如果需要）/ Initialize qlib (if needed)
        if not qlib_wrapper.is_initialized():
            print("初始化qlib... / Initializing qlib...")
            qlib_wrapper.init(
                provider_uri="~/.qlib/qlib_data/cn_data",
                region="cn"
            )
        
        # 创建信号生成器 / Create signal generator
        signal_generator = SignalGenerator(
            model_registry=model_registry,
            qlib_wrapper=qlib_wrapper
        )
        
        print("✅ 信号生成器初始化成功 / Signal generator initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ 信号生成器初始化失败 / Signal generator initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_model_selection():
    """
    测试模型选择功能 / Test model selection functionality
    """
    print("\n" + "=" * 70)
    print("测试2: 模型选择 / Test 2: Model Selection")
    print("=" * 70)
    
    try:
        from src.application.model_registry import ModelRegistry
        
        # 创建模型注册表 / Create model registry
        model_registry = ModelRegistry()
        
        # 列出可用模型 / List available models
        models = model_registry.list_models()
        
        if not models:
            print("⚠️  没有可用的模型 / No models available")
            print("请先运行训练脚本创建模型 / Please run training script to create models first")
            return False
        
        print(f"✅ 找到 {len(models)} 个可用模型 / Found {len(models)} available models")
        
        # 显示模型信息 / Display model information
        for i, model in enumerate(models[:3], 1):  # 只显示前3个
            print(f"\n模型 {i} / Model {i}:")
            print(f"  名称 / Name: {model.model_name}")
            print(f"  版本 / Version: {model.version}")
            print(f"  ID: {model.model_id}")
            print(f"  类型 / Type: {model.model_type}")
            print(f"  状态 / Status: {model.status}")
        
        return True
        
    except Exception as e:
        print(f"❌ 模型选择测试失败 / Model selection test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_signal_generation_with_mock_data():
    """
    测试使用模拟数据生成信号 / Test signal generation with mock data
    """
    print("\n" + "=" * 70)
    print("测试3: 信号生成（模拟数据）/ Test 3: Signal Generation (Mock Data)")
    print("=" * 70)
    
    try:
        from src.application.signal_generator import SignalGenerator
        from src.application.model_registry import ModelRegistry
        from src.infrastructure.qlib_wrapper import QlibWrapper
        from src.models.trading_models import Portfolio
        
        # 创建依赖 / Create dependencies
        model_registry = ModelRegistry()
        qlib_wrapper = QlibWrapper()
        
        # 初始化qlib / Initialize qlib
        if not qlib_wrapper.is_initialized():
            print("初始化qlib... / Initializing qlib...")
            qlib_wrapper.init(
                provider_uri="~/.qlib/qlib_data/cn_data",
                region="cn"
            )
        
        # 获取第一个可用模型 / Get first available model
        models = model_registry.list_models()
        if not models:
            print("⚠️  没有可用的模型，跳过此测试 / No models available, skipping this test")
            return False
        
        model = models[0]
        print(f"使用模型 / Using model: {model.model_name} (v{model.version})")
        
        # 创建信号生成器 / Create signal generator
        signal_generator = SignalGenerator(
            model_registry=model_registry,
            qlib_wrapper=qlib_wrapper
        )
        
        # 创建模拟投资组合 / Create mock portfolio
        portfolio = Portfolio(
            cash=1000000.0,
            positions={},
            total_value=1000000.0
        )
        
        # 生成信号 / Generate signals
        print("\n生成信号... / Generating signals...")
        
        # 使用最近的交易日 / Use recent trading day
        signal_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        signals = signal_generator.generate_signals(
            model_id=model.model_id,
            date=signal_date,
            portfolio=portfolio,
            top_n=5,
            instruments="csi300"
        )
        
        print(f"✅ 成功生成 {len(signals)} 个信号 / Successfully generated {len(signals)} signals")
        
        # 显示信号摘要 / Display signal summary
        if signals:
            buy_count = sum(1 for s in signals if s.action == "buy")
            sell_count = sum(1 for s in signals if s.action == "sell")
            hold_count = sum(1 for s in signals if s.action == "hold")
            
            print(f"\n信号摘要 / Signal Summary:")
            print(f"  买入 / Buy: {buy_count}")
            print(f"  卖出 / Sell: {sell_count}")
            print(f"  持有 / Hold: {hold_count}")
            
            # 显示前3个信号 / Display first 3 signals
            print(f"\n前3个信号 / First 3 signals:")
            for i, signal in enumerate(signals[:3], 1):
                print(f"  {i}. {signal.stock_code} - {signal.action} (score: {signal.score:.4f}, confidence: {signal.confidence:.2%})")
        
        return True
        
    except Exception as e:
        print(f"❌ 信号生成测试失败 / Signal generation test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_signal_explanation():
    """
    测试信号解释功能 / Test signal explanation functionality
    """
    print("\n" + "=" * 70)
    print("测试4: 信号解释 / Test 4: Signal Explanation")
    print("=" * 70)
    
    try:
        from src.application.signal_generator import SignalGenerator
        from src.application.model_registry import ModelRegistry
        from src.infrastructure.qlib_wrapper import QlibWrapper
        from src.models.trading_models import Portfolio, Signal
        
        # 创建依赖 / Create dependencies
        model_registry = ModelRegistry()
        qlib_wrapper = QlibWrapper()
        
        # 初始化qlib / Initialize qlib
        if not qlib_wrapper.is_initialized():
            qlib_wrapper.init(
                provider_uri="~/.qlib/qlib_data/cn_data",
                region="cn"
            )
        
        # 创建信号生成器 / Create signal generator
        signal_generator = SignalGenerator(
            model_registry=model_registry,
            qlib_wrapper=qlib_wrapper
        )
        
        # 创建测试信号 / Create test signal
        test_signal = Signal(
            stock_code="600519.SH",
            action="buy",
            score=0.15,
            confidence=0.85,
            timestamp=datetime.now().strftime("%Y-%m-%d")
        )
        
        # 获取信号解释 / Get signal explanation
        print("\n获取信号解释... / Getting signal explanation...")
        explanation = signal_generator.explain_signal(test_signal)
        
        print(f"✅ 成功获取信号解释 / Successfully got signal explanation")
        print(f"\n信号 / Signal: {test_signal.stock_code} - {test_signal.action}")
        print(f"风险等级 / Risk Level: {explanation.risk_level}")
        print(f"主要因素数量 / Main Factors Count: {len(explanation.main_factors)}")
        
        # 显示主要因素 / Display main factors
        print(f"\n主要因素 / Main Factors:")
        for factor_name, contribution in explanation.main_factors[:3]:
            print(f"  • {factor_name}: {contribution:.1%}")
        
        if explanation.description:
            print(f"\n描述 / Description: {explanation.description[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 信号解释测试失败 / Signal explanation test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """
    运行所有测试 / Run all tests
    """
    print("=" * 70)
    print("信号生成CLI测试套件 / Signal Generation CLI Test Suite")
    print("=" * 70)
    print()
    print("本测试将验证信号生成功能的基本功能")
    print("This test will verify basic functionality of signal generation")
    print()
    
    # 运行测试 / Run tests
    results = []
    
    results.append(("信号生成器初始化 / Signal Generator Init", test_signal_generator_initialization()))
    results.append(("模型选择 / Model Selection", test_model_selection()))
    results.append(("信号生成 / Signal Generation", test_signal_generation_with_mock_data()))
    results.append(("信号解释 / Signal Explanation", test_signal_explanation()))
    
    # 显示测试结果摘要 / Display test results summary
    print("\n" + "=" * 70)
    print("测试结果摘要 / Test Results Summary")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过 / PASSED" if result else "❌ 失败 / FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\n总计 / Total: {passed}/{total} 测试通过 / tests passed")
    
    if passed == total:
        print("\n🎉 所有测试通过！ / All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} 个测试失败 / tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
