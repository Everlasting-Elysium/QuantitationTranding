"""
可视化管理器演示 / Visualization Manager Demo
展示如何使用VisualizationManager生成各种图表
Demonstrates how to use VisualizationManager to generate various charts
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 添加项目根目录到路径 / Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.application.visualization_manager import VisualizationManager
from src.infrastructure.logger_system import setup_logging


def generate_sample_returns(days: int = 252, annual_return: float = 0.15) -> pd.Series:
    """
    生成示例收益率数据 / Generate Sample Returns Data
    
    Args:
        days: 天数 / Number of days
        annual_return: 年化收益率 / Annual return
        
    Returns:
        pd.Series: 收益率序列 / Returns series
    """
    # 生成日期索引 / Generate date index
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')[:days]
    
    # 生成随机收益率 / Generate random returns
    daily_return = annual_return / 252
    daily_volatility = 0.15 / np.sqrt(252)
    
    returns = np.random.normal(daily_return, daily_volatility, days)
    
    return pd.Series(returns, index=dates)


def demo_cumulative_returns():
    """演示累计收益曲线图 / Demo Cumulative Returns Chart"""
    print("\n" + "="*80)
    print("演示1: 累计收益曲线图 / Demo 1: Cumulative Returns Chart")
    print("="*80)
    
    # 创建可视化管理器 / Create visualization manager
    viz_manager = VisualizationManager(output_dir="./outputs/demo_visualizations")
    
    # 生成示例数据 / Generate sample data
    strategy_returns = generate_sample_returns(days=252, annual_return=0.20)
    benchmark_returns = generate_sample_returns(days=252, annual_return=0.10)
    
    # 绘制累计收益曲线 / Plot cumulative returns
    chart_path = viz_manager.plot_cumulative_returns(
        returns=strategy_returns,
        benchmark=benchmark_returns,
        title="策略 vs 基准累计收益 / Strategy vs Benchmark Cumulative Returns"
    )
    
    print(f"✓ 累计收益曲线图已保存 / Cumulative returns chart saved: {chart_path}")


def demo_position_distribution():
    """演示持仓分布图 / Demo Position Distribution Chart"""
    print("\n" + "="*80)
    print("演示2: 持仓分布图 / Demo 2: Position Distribution Chart")
    print("="*80)
    
    # 创建可视化管理器 / Create visualization manager
    viz_manager = VisualizationManager(output_dir="./outputs/demo_visualizations")
    
    # 生成示例持仓数据 / Generate sample portfolio data
    portfolio = {
        "贵州茅台 600519": 0.15,
        "宁德时代 300750": 0.12,
        "比亚迪 002594": 0.10,
        "隆基绿能 601012": 0.08,
        "中国平安 601318": 0.08,
        "招商银行 600036": 0.07,
        "五粮液 000858": 0.06,
        "美的集团 000333": 0.06,
        "万科A 000002": 0.05,
        "格力电器 000651": 0.05,
        "其他股票": 0.18
    }
    
    # 绘制持仓分布图 / Plot position distribution
    chart_path = viz_manager.plot_position_distribution(
        portfolio=portfolio,
        title="投资组合持仓分布 / Portfolio Position Distribution"
    )
    
    print(f"✓ 持仓分布图已保存 / Position distribution chart saved: {chart_path}")


def demo_sector_distribution():
    """演示行业分布图 / Demo Sector Distribution Chart"""
    print("\n" + "="*80)
    print("演示3: 行业分布图 / Demo 3: Sector Distribution Chart")
    print("="*80)
    
    # 创建可视化管理器 / Create visualization manager
    viz_manager = VisualizationManager(output_dir="./outputs/demo_visualizations")
    
    # 生成示例行业数据 / Generate sample sector data
    sector_weights = {
        "食品饮料 Food & Beverage": 0.21,
        "新能源 New Energy": 0.20,
        "汽车 Automotive": 0.15,
        "金融 Finance": 0.15,
        "家电 Home Appliances": 0.11,
        "房地产 Real Estate": 0.05,
        "其他 Others": 0.13
    }
    
    # 绘制行业分布图 / Plot sector distribution
    chart_path = viz_manager.plot_sector_distribution(
        sector_weights=sector_weights,
        title="投资组合行业分布 / Portfolio Sector Distribution"
    )
    
    print(f"✓ 行业分布图已保存 / Sector distribution chart saved: {chart_path}")


def demo_multi_model_comparison():
    """演示多模型对比图 / Demo Multi-Model Comparison Chart"""
    print("\n" + "="*80)
    print("演示4: 多模型对比图 / Demo 4: Multi-Model Comparison Chart")
    print("="*80)
    
    # 创建可视化管理器 / Create visualization manager
    viz_manager = VisualizationManager(output_dir="./outputs/demo_visualizations")
    
    # 生成多个模型的示例数据 / Generate sample data for multiple models
    model_returns = {
        "LightGBM": generate_sample_returns(days=252, annual_return=0.22),
        "Linear Model": generate_sample_returns(days=252, annual_return=0.15),
        "MLP": generate_sample_returns(days=252, annual_return=0.18),
        "Random Forest": generate_sample_returns(days=252, annual_return=0.20),
    }
    
    # 绘制多模型对比图 / Plot multi-model comparison
    chart_path = viz_manager.plot_multi_model_comparison(
        model_returns=model_returns,
        title="多模型性能对比 / Multi-Model Performance Comparison"
    )
    
    print(f"✓ 多模型对比图已保存 / Multi-model comparison chart saved: {chart_path}")


def demo_training_curve():
    """演示训练曲线图 / Demo Training Curve Chart"""
    print("\n" + "="*80)
    print("演示5: 训练曲线图 / Demo 5: Training Curve Chart")
    print("="*80)
    
    # 创建可视化管理器 / Create visualization manager
    viz_manager = VisualizationManager(output_dir="./outputs/demo_visualizations")
    
    # 生成示例训练指标数据 / Generate sample training metrics data
    epochs = 50
    train_loss = [1.0 - i * 0.015 + np.random.normal(0, 0.02) for i in range(epochs)]
    val_loss = [1.0 - i * 0.012 + np.random.normal(0, 0.03) for i in range(epochs)]
    train_ic = [0.02 + i * 0.001 + np.random.normal(0, 0.005) for i in range(epochs)]
    val_ic = [0.02 + i * 0.0008 + np.random.normal(0, 0.008) for i in range(epochs)]
    
    metrics = {
        "训练损失 Train Loss": train_loss,
        "验证损失 Val Loss": val_loss,
        "训练IC Train IC": train_ic,
        "验证IC Val IC": val_ic,
    }
    
    # 绘制训练曲线 / Plot training curve
    chart_path = viz_manager.plot_training_curve(
        metrics=metrics,
        title="模型训练曲线 / Model Training Curve"
    )
    
    print(f"✓ 训练曲线图已保存 / Training curve chart saved: {chart_path}")


def demo_complete_report():
    """演示完整报告生成 / Demo Complete Report Generation"""
    print("\n" + "="*80)
    print("演示6: 完整报告生成 / Demo 6: Complete Report Generation")
    print("="*80)
    
    # 创建可视化管理器 / Create visualization manager
    viz_manager = VisualizationManager(output_dir="./outputs/demo_visualizations")
    
    # 生成示例数据 / Generate sample data
    returns = generate_sample_returns(days=252, annual_return=0.20)
    benchmark = generate_sample_returns(days=252, annual_return=0.10)
    
    portfolio = {
        "贵州茅台 600519": 0.15,
        "宁德时代 300750": 0.12,
        "比亚迪 002594": 0.10,
        "隆基绿能 601012": 0.08,
        "中国平安 601318": 0.08,
        "其他股票": 0.47
    }
    
    sector_weights = {
        "食品饮料": 0.21,
        "新能源": 0.20,
        "汽车": 0.15,
        "金融": 0.15,
        "其他": 0.29
    }
    
    # 创建完整报告 / Create complete report
    chart_paths = viz_manager.create_report_with_charts(
        returns=returns,
        portfolio=portfolio,
        sector_weights=sector_weights,
        benchmark=benchmark
    )
    
    print(f"✓ 完整报告已生成 / Complete report generated")
    print(f"  包含 {len(chart_paths)} 个图表 / Contains {len(chart_paths)} charts:")
    for chart_name, chart_path in chart_paths.items():
        print(f"  - {chart_name}: {chart_path}")


def main():
    """主函数 / Main Function"""
    print("\n" + "="*80)
    print("可视化管理器演示程序 / Visualization Manager Demo")
    print("="*80)
    
    # 设置日志 / Setup logger
    setup_logging(log_dir="./logs", log_level="INFO")
    
    try:
        # 运行所有演示 / Run all demos
        demo_cumulative_returns()
        demo_position_distribution()
        demo_sector_distribution()
        demo_multi_model_comparison()
        demo_training_curve()
        demo_complete_report()
        
        print("\n" + "="*80)
        print("✓ 所有演示完成！/ All demos completed!")
        print("="*80)
        print("\n请查看 ./outputs/demo_visualizations 目录中的图表")
        print("Please check the charts in ./outputs/demo_visualizations directory")
        
    except Exception as e:
        print(f"\n✗ 演示失败 / Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
