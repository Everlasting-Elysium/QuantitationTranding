"""
信号生成器使用示例 / Signal Generator Usage Example
演示如何使用SignalGenerator生成交易信号
Demonstrates how to use SignalGenerator to generate trading signals
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.application.signal_generator import SignalGenerator
from src.application.model_registry import ModelRegistry
from src.infrastructure.qlib_wrapper import QlibWrapper
from src.models.trading_models import Portfolio, Position, RiskLimits


def example_1_basic_signal_generation():
    """
    示例1: 基本信号生成 / Example 1: Basic Signal Generation
    
    演示如何使用已训练的模型生成交易信号
    Demonstrates how to generate trading signals using a trained model
    """
    print("\n" + "=" * 70)
    print("示例1: 基本信号生成 / Example 1: Basic Signal Generation")
    print("=" * 70)
    
    # 1. 初始化组件 / Initialize components
    print("\n1. 初始化组件 / Initializing components...")
    
    # 创建模型注册表
    # Create model registry
    model_registry = ModelRegistry(registry_dir="./model_registry")
    
    # 创建Qlib封装器
    # Create Qlib wrapper
    qlib_wrapper = QlibWrapper()
    qlib_wrapper.init(
        provider_uri="./data/cn_data",
        region="cn"
    )
    
    # 创建信号生成器
    # Create signal generator
    signal_generator = SignalGenerator(
        model_registry=model_registry,
        qlib_wrapper=qlib_wrapper
    )
    
    print("✓ 组件初始化完成 / Components initialized")
    
    # 2. 创建投资组合 / Create portfolio
    print("\n2. 创建投资组合 / Creating portfolio...")
    
    portfolio = Portfolio(
        portfolio_id="demo_portfolio",
        cash=100000.0,  # 10万元现金
        total_value=100000.0,
        initial_capital=100000.0
    )
    
    print(f"✓ 投资组合创建完成 / Portfolio created")
    print(f"  初始资金 / Initial capital: ¥{portfolio.initial_capital:,.2f}")
    print(f"  可用现金 / Available cash: ¥{portfolio.cash:,.2f}")
    
    # 3. 生成交易信号 / Generate trading signals
    print("\n3. 生成交易信号 / Generating trading signals...")
    
    # 假设我们有一个已训练的模型
    # Assume we have a trained model
    model_id = "lgbm_model_v1.0"  # 替换为实际的模型ID / Replace with actual model ID
    
    try:
        signals = signal_generator.generate_signals(
            model_id=model_id,
            date="2024-01-15",  # 信号生成日期 / Signal generation date
            portfolio=portfolio,
            top_n=5,  # 生成前5个买入候选 / Generate top 5 buy candidates
            instruments="csi300"  # 使用沪深300股票池 / Use CSI300 stock pool
        )
        
        print(f"✓ 成功生成 {len(signals)} 个交易信号 / Successfully generated {len(signals)} trading signals")
        
        # 4. 显示信号详情 / Display signal details
        print("\n4. 交易信号详情 / Trading Signal Details:")
        print("-" * 70)
        
        for i, signal in enumerate(signals, 1):
            print(f"\n信号 {i} / Signal {i}:")
            print(f"  股票代码 / Stock Code: {signal.stock_code}")
            print(f"  动作 / Action: {signal.action.upper()}")
            print(f"  预测分数 / Prediction Score: {signal.score:.4f}")
            print(f"  置信度 / Confidence: {signal.confidence:.2%}")
            print(f"  时间戳 / Timestamp: {signal.timestamp}")
            if signal.reason:
                print(f"  原因 / Reason: {signal.reason}")
            if signal.target_weight:
                print(f"  建议权重 / Target Weight: {signal.target_weight:.2f}%")
        
    except Exception as e:
        print(f"✗ 生成信号失败 / Failed to generate signals: {str(e)}")
        print("  提示 / Hint: 请确保模型已训练并注册 / Please ensure model is trained and registered")


def example_2_signal_with_positions():
    """
    示例2: 有持仓时生成信号 / Example 2: Signal Generation with Existing Positions
    
    演示如何在已有持仓的情况下生成交易信号
    Demonstrates how to generate signals when portfolio has existing positions
    """
    print("\n" + "=" * 70)
    print("示例2: 有持仓时生成信号 / Example 2: Signal Generation with Positions")
    print("=" * 70)
    
    # 初始化组件（简化版）
    # Initialize components (simplified)
    model_registry = ModelRegistry(registry_dir="./model_registry")
    qlib_wrapper = QlibWrapper()
    qlib_wrapper.init(provider_uri="./data/cn_data", region="cn")
    signal_generator = SignalGenerator(model_registry, qlib_wrapper)
    
    # 创建有持仓的投资组合
    # Create portfolio with existing positions
    portfolio = Portfolio(
        portfolio_id="demo_portfolio_2",
        cash=50000.0,  # 5万元现金
        initial_capital=100000.0
    )
    
    # 添加现有持仓
    # Add existing positions
    portfolio.positions = {
        '600519.SH': Position(  # 贵州茅台
            symbol='600519.SH',
            quantity=50,
            avg_cost=1800.0,
            current_price=1850.0
        ),
        '300750.SZ': Position(  # 宁德时代
            symbol='300750.SZ',
            quantity=100,
            avg_cost=180.0,
            current_price=185.0
        )
    }
    
    # 更新投资组合总价值
    # Update portfolio total value
    portfolio.update_total_value()
    
    print(f"\n当前投资组合状态 / Current Portfolio Status:")
    print(f"  总价值 / Total Value: ¥{portfolio.total_value:,.2f}")
    print(f"  现金 / Cash: ¥{portfolio.cash:,.2f}")
    print(f"  持仓数量 / Positions: {len(portfolio.positions)}")
    
    for symbol, position in portfolio.positions.items():
        print(f"\n  {symbol}:")
        print(f"    数量 / Quantity: {position.quantity}")
        print(f"    成本 / Avg Cost: ¥{position.avg_cost:.2f}")
        print(f"    现价 / Current Price: ¥{position.current_price:.2f}")
        print(f"    市值 / Market Value: ¥{position.market_value:,.2f}")
        print(f"    盈亏 / P&L: ¥{position.unrealized_pnl:,.2f} ({position.unrealized_pnl_pct:.2f}%)")
    
    # 生成信号
    # Generate signals
    print("\n生成交易信号 / Generating trading signals...")
    
    try:
        signals = signal_generator.generate_signals(
            model_id="lgbm_model_v1.0",
            date="2024-01-15",
            portfolio=portfolio,
            top_n=3
        )
        
        print(f"✓ 生成了 {len(signals)} 个信号 / Generated {len(signals)} signals")
        
        # 分类显示信号
        # Display signals by category
        buy_signals = [s for s in signals if s.action == "buy"]
        sell_signals = [s for s in signals if s.action == "sell"]
        hold_signals = [s for s in signals if s.action == "hold"]
        
        print(f"\n信号统计 / Signal Statistics:")
        print(f"  买入信号 / Buy Signals: {len(buy_signals)}")
        print(f"  卖出信号 / Sell Signals: {len(sell_signals)}")
        print(f"  持有信号 / Hold Signals: {len(hold_signals)}")
        
        if buy_signals:
            print(f"\n买入建议 / Buy Recommendations:")
            for signal in buy_signals:
                print(f"  - {signal.stock_code}: 分数 {signal.score:.4f}, 置信度 {signal.confidence:.2%}")
        
        if sell_signals:
            print(f"\n卖出建议 / Sell Recommendations:")
            for signal in sell_signals:
                print(f"  - {signal.stock_code}: 分数 {signal.score:.4f}, 置信度 {signal.confidence:.2%}")
        
        if hold_signals:
            print(f"\n持有建议 / Hold Recommendations:")
            for signal in hold_signals:
                print(f"  - {signal.stock_code}: 分数 {signal.score:.4f}, 置信度 {signal.confidence:.2%}")
        
    except Exception as e:
        print(f"✗ 生成信号失败 / Failed: {str(e)}")


def example_3_custom_risk_limits():
    """
    示例3: 自定义风险限制 / Example 3: Custom Risk Limits
    
    演示如何设置自定义的风险控制参数
    Demonstrates how to set custom risk control parameters
    """
    print("\n" + "=" * 70)
    print("示例3: 自定义风险限制 / Example 3: Custom Risk Limits")
    print("=" * 70)
    
    # 初始化组件
    # Initialize components
    model_registry = ModelRegistry(registry_dir="./model_registry")
    qlib_wrapper = QlibWrapper()
    qlib_wrapper.init(provider_uri="./data/cn_data", region="cn")
    
    # 创建自定义风险限制
    # Create custom risk limits
    custom_limits = RiskLimits(
        max_position_size=0.6,      # 最大持仓60% / Max 60% position
        max_single_stock=0.15,      # 单只股票最大15% / Max 15% per stock
        max_sector_exposure=0.35,   # 单个行业最大35% / Max 35% per sector
        min_cash_reserve=0.2,       # 最小保留20%现金 / Min 20% cash reserve
        max_turnover=0.3            # 最大换手率30% / Max 30% turnover
    )
    
    print("\n自定义风险限制 / Custom Risk Limits:")
    print(f"  最大持仓比例 / Max Position Size: {custom_limits.max_position_size:.0%}")
    print(f"  单只股票最大权重 / Max Single Stock: {custom_limits.max_single_stock:.0%}")
    print(f"  单个行业最大暴露 / Max Sector Exposure: {custom_limits.max_sector_exposure:.0%}")
    print(f"  最小现金储备 / Min Cash Reserve: {custom_limits.min_cash_reserve:.0%}")
    print(f"  最大换手率 / Max Turnover: {custom_limits.max_turnover:.0%}")
    
    # 创建信号生成器并设置风险限制
    # Create signal generator with custom risk limits
    signal_generator = SignalGenerator(
        model_registry=model_registry,
        qlib_wrapper=qlib_wrapper,
        risk_limits=custom_limits
    )
    
    print("\n✓ 信号生成器已配置自定义风险限制 / Signal generator configured with custom risk limits")
    
    # 创建投资组合
    # Create portfolio
    portfolio = Portfolio(
        portfolio_id="demo_portfolio_3",
        cash=100000.0,
        total_value=100000.0,
        initial_capital=100000.0
    )
    
    # 生成信号（会应用自定义风险限制）
    # Generate signals (will apply custom risk limits)
    print("\n生成信号（应用自定义风险限制）/ Generating signals with custom risk limits...")
    
    try:
        signals = signal_generator.generate_signals(
            model_id="lgbm_model_v1.0",
            date="2024-01-15",
            portfolio=portfolio,
            top_n=10  # 尝试生成10个候选，但会被风控限制
        )
        
        print(f"✓ 在自定义风控下生成了 {len(signals)} 个信号")
        print(f"  Generated {len(signals)} signals under custom risk control")
        
    except Exception as e:
        print(f"✗ 失败 / Failed: {str(e)}")


def example_4_signal_explanation():
    """
    示例4: 信号解释 / Example 4: Signal Explanation
    
    演示如何获取信号的详细解释
    Demonstrates how to get detailed explanation for signals
    """
    print("\n" + "=" * 70)
    print("示例4: 信号解释 / Example 4: Signal Explanation")
    print("=" * 70)
    
    # 初始化组件
    # Initialize components
    model_registry = ModelRegistry(registry_dir="./model_registry")
    qlib_wrapper = QlibWrapper()
    qlib_wrapper.init(provider_uri="./data/cn_data", region="cn")
    signal_generator = SignalGenerator(model_registry, qlib_wrapper)
    
    # 创建投资组合并生成信号
    # Create portfolio and generate signals
    portfolio = Portfolio(
        portfolio_id="demo_portfolio_4",
        cash=100000.0,
        total_value=100000.0,
        initial_capital=100000.0
    )
    
    try:
        signals = signal_generator.generate_signals(
            model_id="lgbm_model_v1.0",
            date="2024-01-15",
            portfolio=portfolio,
            top_n=3
        )
        
        if signals:
            # 选择第一个信号进行详细解释
            # Select first signal for detailed explanation
            signal = signals[0]
            
            print(f"\n为信号生成详细解释 / Generating detailed explanation for signal:")
            print(f"  股票代码 / Stock: {signal.stock_code}")
            print(f"  动作 / Action: {signal.action}")
            
            # 获取信号解释
            # Get signal explanation
            explanation = signal_generator.explain_signal(signal)
            
            print(f"\n" + "=" * 70)
            print("信号详细解释 / Detailed Signal Explanation")
            print("=" * 70)
            
            print(f"\n{explanation.description}")
            
            print(f"\n主要影响因素详情 / Detailed Main Factors:")
            for i, (factor, contribution) in enumerate(explanation.main_factors, 1):
                print(f"  {i}. {factor}")
                print(f"     贡献度 / Contribution: {contribution:.1%}")
                print(f"     {'█' * int(contribution * 50)}")
            
        else:
            print("未生成信号 / No signals generated")
            
    except Exception as e:
        print(f"✗ 失败 / Failed: {str(e)}")


def example_5_detailed_signal_analysis():
    """
    示例5: 详细信号分析 / Example 5: Detailed Signal Analysis
    
    演示如何获取完整的信号分析报告，包括特征重要性、风险评估和操作建议
    Demonstrates how to get complete signal analysis report including feature importance, risk assessment and action suggestions
    """
    print("\n" + "=" * 70)
    print("示例5: 详细信号分析 / Example 5: Detailed Signal Analysis")
    print("=" * 70)
    
    # 初始化组件
    # Initialize components
    model_registry = ModelRegistry(registry_dir="./model_registry")
    qlib_wrapper = QlibWrapper()
    qlib_wrapper.init(provider_uri="./data/cn_data", region="cn")
    signal_generator = SignalGenerator(model_registry, qlib_wrapper)
    
    # 创建投资组合并生成信号
    # Create portfolio and generate signals
    portfolio = Portfolio(
        portfolio_id="demo_portfolio_5",
        cash=100000.0,
        total_value=100000.0,
        initial_capital=100000.0
    )
    
    try:
        signals = signal_generator.generate_signals(
            model_id="lgbm_model_v1.0",
            date="2024-01-15",
            portfolio=portfolio,
            top_n=3
        )
        
        if signals:
            # 对每个信号进行详细分析
            # Perform detailed analysis for each signal
            for i, signal in enumerate(signals[:2], 1):  # 只分析前2个信号
                print(f"\n{'='*70}")
                print(f"信号 {i} 详细分析 / Signal {i} Detailed Analysis")
                print(f"{'='*70}")
                
                # 获取详细分析
                # Get detailed analysis
                analysis = signal_generator.get_detailed_signal_analysis(signal)
                
                # 1. 基本信息
                # Basic information
                print(f"\n📊 基本信息 / Basic Information:")
                print(f"  股票代码 / Stock: {analysis['signal']['stock_code']}")
                print(f"  建议操作 / Action: {analysis['signal']['action'].upper()}")
                print(f"  预测分数 / Score: {analysis['signal']['score']:.4f}")
                print(f"  置信度 / Confidence: {analysis['signal']['confidence']:.2%}")
                print(f"  信号强度 / Strength: {analysis['metadata']['signal_strength']}")
                
                # 2. 风险评估
                # Risk assessment
                print(f"\n⚠️  风险评估 / Risk Assessment:")
                print(f"  风险等级 / Risk Level: {analysis['risk_assessment']['risk_level']}")
                print(f"  风险分数 / Risk Score: {analysis['risk_assessment']['risk_score']:.2f}")
                
                if analysis['risk_assessment']['warnings']:
                    print(f"\n  风险警告 / Risk Warnings:")
                    for warning in analysis['risk_assessment']['warnings']:
                        print(f"    ⚠️  {warning}")
                
                # 3. 特征重要性
                # Feature importance
                print(f"\n🔍 特征重要性 / Feature Importance:")
                for j, (factor, contribution) in enumerate(analysis['feature_importance']['main_factors'][:3], 1):
                    bar_length = int(contribution * 30)
                    bar = "█" * bar_length + "░" * (30 - bar_length)
                    print(f"  {j}. {factor}")
                    print(f"     {bar} {contribution:.1%}")
                
                # 4. 通俗解释
                # Plain explanation
                print(f"\n📝 通俗解释 / Plain Explanation:")
                plain_text = analysis['explanations']['plain_language']
                for line in plain_text.split('\n'):
                    if line.strip():
                        print(f"  {line}")
                
                # 5. 操作建议
                # Action suggestions
                print(f"\n💼 操作建议 / Action Suggestions:")
                for suggestion in analysis['recommendations']['action_suggestions'][:3]:
                    print(f"  ✓ {suggestion}")
                
                # 6. 仓位建议
                # Position sizing
                print(f"\n📊 仓位建议 / Position Sizing:")
                pos_rec = analysis['recommendations']['position_sizing']
                if 'recommended_percentage' in pos_rec:
                    print(f"  建议仓位 / Recommended: {pos_rec['recommended_percentage']:.1f}%")
                    print(f"  范围 / Range: {pos_rec['min_percentage']:.1f}% - {pos_rec['max_percentage']:.1f}%")
                print(f"  说明 / Description: {pos_rec['description']}")
                
                # 7. 止损建议
                # Stop loss
                print(f"\n🛡️  止损建议 / Stop Loss:")
                stop_loss = analysis['recommendations']['stop_loss']
                print(f"  {stop_loss['description']}")
                
                print(f"\n{'='*70}\n")
        
        else:
            print("未生成信号 / No signals generated")
            
    except Exception as e:
        print(f"✗ 失败 / Failed: {str(e)}")
        import traceback
        traceback.print_exc()


def example_6_risk_warning_demo():
    """
    示例6: 风险警告演示 / Example 6: Risk Warning Demo
    
    演示高风险信号的警告机制
    Demonstrates risk warning mechanism for high-risk signals
    """
    print("\n" + "=" * 70)
    print("示例6: 风险警告演示 / Example 6: Risk Warning Demo")
    print("=" * 70)
    
    from src.models.trading_models import Signal
    from datetime import datetime
    
    # 初始化组件
    # Initialize components
    model_registry = ModelRegistry(registry_dir="./model_registry")
    qlib_wrapper = QlibWrapper()
    qlib_wrapper.init(provider_uri="./data/cn_data", region="cn")
    signal_generator = SignalGenerator(model_registry, qlib_wrapper)
    
    # 创建不同风险等级的模拟信号
    # Create simulated signals with different risk levels
    test_signals = [
        Signal(
            stock_code="600000.SH",
            action="buy",
            score=0.15,
            confidence=0.9,  # 高置信度 - 低风险
            timestamp=datetime.now().isoformat(),
            reason="强烈买入信号 / Strong buy signal"
        ),
        Signal(
            stock_code="600001.SH",
            action="buy",
            score=0.08,
            confidence=0.65,  # 中等置信度 - 中等风险
            timestamp=datetime.now().isoformat(),
            reason="中等买入信号 / Moderate buy signal"
        ),
        Signal(
            stock_code="600002.SH",
            action="buy",
            score=0.03,
            confidence=0.45,  # 低置信度 - 高风险
            timestamp=datetime.now().isoformat(),
            reason="弱买入信号 / Weak buy signal"
        ),
    ]
    
    # 对每个信号进行解释，展示不同的风险警告
    # Explain each signal to show different risk warnings
    for i, signal in enumerate(test_signals, 1):
        print(f"\n{'='*70}")
        print(f"测试信号 {i} / Test Signal {i}")
        print(f"{'='*70}")
        
        try:
            explanation = signal_generator.explain_signal(signal)
            
            # 只显示关键信息
            # Only show key information
            print(f"\n股票 / Stock: {signal.stock_code}")
            print(f"置信度 / Confidence: {signal.confidence:.2%}")
            print(f"风险等级 / Risk Level: {explanation.risk_level.upper()}")
            
            # 显示完整描述（包含风险警告）
            # Show full description (including risk warnings)
            print(f"\n{explanation.description}")
            
        except Exception as e:
            print(f"✗ 解释失败 / Explanation failed: {str(e)}")


def main():
    """主函数 / Main function"""
    print("\n" + "=" * 70)
    print("SignalGenerator 使用示例 / SignalGenerator Usage Examples")
    print("=" * 70)
    
    examples = [
        ("基本信号生成", "Basic Signal Generation", example_1_basic_signal_generation),
        ("有持仓时生成信号", "Signal with Positions", example_2_signal_with_positions),
        ("自定义风险限制", "Custom Risk Limits", example_3_custom_risk_limits),
        ("信号解释", "Signal Explanation", example_4_signal_explanation),
        ("详细信号分析", "Detailed Signal Analysis", example_5_detailed_signal_analysis),
        ("风险警告演示", "Risk Warning Demo", example_6_risk_warning_demo),
    ]
    
    print("\n可用示例 / Available Examples:")
    for i, (name_cn, name_en, _) in enumerate(examples, 1):
        print(f"  {i}. {name_cn} / {name_en}")
    
    print("\n提示 / Note:")
    print("  示例1-4需要已训练的模型和qlib数据")
    print("  Examples 1-4 require trained models and qlib data")
    print("  示例5-6可以使用模拟数据运行")
    print("  Examples 5-6 can run with simulated data")
    print("  请先运行训练流程或直接运行示例6")
    print("  Please run training pipeline first or directly run example 6")
    
    # 运行风险警告演示（不需要真实模型）
    # Run risk warning demo (doesn't need real model)
    print("\n" + "=" * 70)
    print("运行风险警告演示 / Running Risk Warning Demo")
    print("=" * 70)
    
    try:
        example_6_risk_warning_demo()
    except Exception as e:
        print(f"\n示例失败 / Example failed")
        print(f"错误 / Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
