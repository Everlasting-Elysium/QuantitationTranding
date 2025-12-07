"""
Demo script for PerformanceAnalyzer
表现分析器演示脚本

This script demonstrates how to use the PerformanceAnalyzer to:
- Analyze historical performance of assets
- Calculate key metrics (returns, Sharpe ratio, max drawdown)
- Generate recommendations based on performance

本脚本演示如何使用PerformanceAnalyzer：
- 分析资产的历史表现
- 计算关键指标（收益率、夏普比率、最大回撤）
- 基于表现生成推荐
"""

import sys
from pathlib import Path

# Add project root to path
# 将项目根目录添加到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.application.performance_analyzer import PerformanceAnalyzer
from src.infrastructure.qlib_wrapper import QlibWrapper
from src.infrastructure.logger_system import LoggerSystem


def main():
    """Main demo function / 主演示函数"""
    
    # Initialize logger
    # 初始化日志
    logger_system = LoggerSystem()
    logger = logger_system.get_logger(__name__)
    
    logger.info("=" * 80)
    logger.info("Performance Analyzer Demo / 表现分析器演示")
    logger.info("=" * 80)
    
    try:
        # Initialize qlib
        # 初始化qlib
        logger.info("\n1. Initializing qlib / 初始化qlib...")
        qlib_wrapper = QlibWrapper()
        
        # Check if qlib is already initialized
        # 检查qlib是否已初始化
        if not qlib_wrapper.is_initialized():
            # Initialize with default settings
            # 使用默认设置初始化
            data_path = project_root / "data" / "cn_data"
            qlib_wrapper.init(
                provider_uri=str(data_path),
                region="cn"
            )
            logger.info("Qlib initialized successfully / Qlib初始化成功")
        else:
            logger.info("Qlib already initialized / Qlib已初始化")
        
        # Create PerformanceAnalyzer
        # 创建PerformanceAnalyzer
        logger.info("\n2. Creating PerformanceAnalyzer / 创建PerformanceAnalyzer...")
        analyzer = PerformanceAnalyzer(qlib_wrapper=qlib_wrapper)
        
        # Set risk-free rate (optional)
        # 设置无风险利率（可选）
        analyzer.set_risk_free_rate(0.03)  # 3% annual risk-free rate
        
        # Example 1: Analyze historical performance
        # 示例1：分析历史表现
        logger.info("\n3. Analyzing historical performance / 分析历史表现...")
        logger.info("Market: CN (中国市场)")
        logger.info("Asset Type: stock (股票)")
        logger.info("Lookback: 3 years (3年)")
        
        report = analyzer.analyze_historical_performance(
            market="CN",
            asset_type="stock",
            lookback_years=3,
            instruments="csi300"  # CSI 300 index constituents
        )
        
        # Display report summary
        # 显示报告摘要
        logger.info("\n" + "=" * 80)
        logger.info("Performance Analysis Report / 表现分析报告")
        logger.info("=" * 80)
        logger.info(f"Analysis Period / 分析期间: {report.analysis_period_start} to {report.analysis_period_end}")
        logger.info(f"Total Assets Analyzed / 分析的资产总数: {report.total_assets_analyzed}")
        logger.info(f"Average Annual Return / 平均年化收益率: {report.average_return:.2%}")
        logger.info(f"Average Sharpe Ratio / 平均夏普比率: {report.average_sharpe:.2f}")
        logger.info(f"Average Max Drawdown / 平均最大回撤: {report.average_drawdown:.2%}")
        
        # Display top performers
        # 显示顶级表现者
        logger.info("\n" + "-" * 80)
        logger.info("Top 10 Performers / 前10名表现者")
        logger.info("-" * 80)
        
        for rec in report.top_performers:
            logger.info(
                f"\n#{rec.rank} {rec.symbol}"
            )
            logger.info(f"  Performance Score / 综合评分: {rec.performance_score:.1f}/100")
            logger.info(f"  Annual Return / 年化收益率: {rec.annual_return:.2%}")
            logger.info(f"  Sharpe Ratio / 夏普比率: {rec.sharpe_ratio:.2f}")
            logger.info(f"  Max Drawdown / 最大回撤: {rec.max_drawdown:.2%}")
            logger.info(f"  Reason / 推荐理由: {rec.recommendation_reason}")
        
        # Example 2: Get recommendations directly
        # 示例2：直接获取推荐
        logger.info("\n" + "=" * 80)
        logger.info("4. Getting top recommendations / 获取顶级推荐...")
        logger.info("=" * 80)
        
        recommendations = analyzer.recommend_top_performers(
            market="CN",
            asset_type="stock",
            top_n=5,
            criteria="sharpe_ratio",
            lookback_years=3
        )
        
        logger.info(f"\nTop 5 Recommendations / 前5名推荐:")
        for rec in recommendations:
            logger.info(
                f"  {rec.rank}. {rec.symbol} - "
                f"Score: {rec.performance_score:.1f}, "
                f"Return: {rec.annual_return:.2%}, "
                f"Sharpe: {rec.sharpe_ratio:.2f}"
            )
        
        # Example 3: Get metrics for a specific asset
        # 示例3：获取特定资产的指标
        logger.info("\n" + "=" * 80)
        logger.info("5. Getting metrics for specific asset / 获取特定资产的指标...")
        logger.info("=" * 80)
        
        # Use the first recommended asset
        # 使用第一个推荐的资产
        if recommendations:
            asset_code = recommendations[0].symbol
            logger.info(f"Asset: {asset_code}")
            
            metrics = analyzer.get_asset_metrics(
                asset_code=asset_code,
                start_date=report.analysis_period_start,
                end_date=report.analysis_period_end
            )
            
            if metrics:
                logger.info(f"\nDetailed Metrics / 详细指标:")
                logger.info(f"  Symbol / 代码: {metrics.symbol}")
                logger.info(f"  Period / 期间: {metrics.period_start} to {metrics.period_end}")
                logger.info(f"  Total Return / 总收益率: {metrics.total_return:.2%}")
                logger.info(f"  Annual Return / 年化收益率: {metrics.annual_return:.2%}")
                logger.info(f"  Volatility / 波动率: {metrics.volatility:.2%}")
                logger.info(f"  Sharpe Ratio / 夏普比率: {metrics.sharpe_ratio:.2f}")
                logger.info(f"  Max Drawdown / 最大回撤: {metrics.max_drawdown:.2%}")
                logger.info(f"  Win Rate / 胜率: {metrics.win_rate:.2%}")
        
        logger.info("\n" + "=" * 80)
        logger.info("Demo completed successfully! / 演示成功完成！")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"\nError occurred / 发生错误: {str(e)}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
