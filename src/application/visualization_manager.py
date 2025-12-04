"""
可视化管理器模块 / Visualization Manager Module
负责生成各种图表和可视化报告
Responsible for generating various charts and visualization reports
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

from ..infrastructure.logger_system import get_logger


class VisualizationManagerError(Exception):
    """可视化管理器错误 / Visualization Manager Error"""
    pass


class VisualizationManager:
    """
    可视化管理器 / Visualization Manager
    
    职责 / Responsibilities:
    - 生成累计收益曲线图 / Generate cumulative returns chart
    - 生成持仓分布图 / Generate position distribution chart
    - 生成行业分布图 / Generate sector distribution chart
    - 生成多模型对比图 / Generate multi-model comparison chart
    - 导出图片文件 / Export chart files
    """
    
    def __init__(self, output_dir: str = "./outputs/visualizations"):
        """
        初始化可视化管理器 / Initialize Visualization Manager
        
        Args:
            output_dir: 输出目录 / Output directory
        """
        self._output_dir = Path(output_dir).expanduser()
        self._logger = get_logger(__name__)
        
        # 确保输出目录存在 / Ensure output directory exists
        self._output_dir.mkdir(parents=True, exist_ok=True)
        
        # 设置中文字体和样式 / Set Chinese font and style
        self._setup_plotting_style()
        
        self._logger.info(f"可视化管理器初始化完成 / Visualization Manager initialized: {self._output_dir}")
    
    def _setup_plotting_style(self) -> None:
        """
        设置绘图样式 / Setup Plotting Style
        配置matplotlib以支持中文显示和美观的样式
        Configure matplotlib for Chinese display and beautiful style
        """
        try:
            # 设置样式 / Set style
            plt.style.use('seaborn-v0_8-darkgrid')
            
            # 尝试设置中文字体 / Try to set Chinese font
            # 常见的中文字体 / Common Chinese fonts
            chinese_fonts = [
                'SimHei',  # 黑体
                'Microsoft YaHei',  # 微软雅黑
                'STSong',  # 华文宋体
                'Arial Unicode MS',  # Mac系统
            ]
            
            for font in chinese_fonts:
                try:
                    plt.rcParams['font.sans-serif'] = [font]
                    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
                    break
                except:
                    continue
            
            # 设置图表默认参数 / Set default chart parameters
            plt.rcParams['figure.figsize'] = (12, 6)
            plt.rcParams['figure.dpi'] = 100
            plt.rcParams['savefig.dpi'] = 300
            plt.rcParams['savefig.bbox'] = 'tight'
            
            self._logger.info("绘图样式设置完成 / Plotting style setup completed")
            
        except Exception as e:
            self._logger.warning(f"设置绘图样式失败 / Failed to setup plotting style: {str(e)}")
    
    def plot_cumulative_returns(
        self,
        returns: pd.Series,
        benchmark: Optional[pd.Series] = None,
        save_path: Optional[str] = None,
        title: str = "累计收益曲线 / Cumulative Returns"
    ) -> str:
        """
        绘制累计收益曲线图 / Plot Cumulative Returns Chart
        
        Args:
            returns: 策略收益率序列 / Strategy returns series
            benchmark: 基准收益率序列（可选）/ Benchmark returns series (optional)
            save_path: 保存路径（可选）/ Save path (optional)
            title: 图表标题 / Chart title
            
        Returns:
            str: 保存的文件路径 / Saved file path
            
        Raises:
            VisualizationManagerError: 绘图失败时抛出 / Raised when plotting fails
        """
        self._logger.info(f"开始绘制累计收益曲线 / Starting to plot cumulative returns")
        
        try:
            # 创建图表 / Create figure
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # 计算累计收益 / Calculate cumulative returns
            cumulative_returns = (1 + returns).cumprod()
            
            # 绘制策略收益曲线 / Plot strategy returns curve
            ax.plot(
                cumulative_returns.index,
                cumulative_returns.values,
                label='策略收益 / Strategy',
                linewidth=2,
                color='#2E86AB'
            )
            
            # 如果有基准，绘制基准收益曲线 / If benchmark exists, plot benchmark curve
            if benchmark is not None and len(benchmark) > 0:
                # 对齐索引 / Align indices
                common_index = returns.index.intersection(benchmark.index)
                if len(common_index) > 0:
                    aligned_benchmark = benchmark.loc[common_index]
                    cumulative_benchmark = (1 + aligned_benchmark).cumprod()
                    
                    ax.plot(
                        cumulative_benchmark.index,
                        cumulative_benchmark.values,
                        label='基准 / Benchmark',
                        linewidth=2,
                        color='#A23B72',
                        linestyle='--'
                    )
            
            # 添加零线 / Add zero line
            ax.axhline(y=1.0, color='gray', linestyle=':', alpha=0.5)
            
            # 设置标题和标签 / Set title and labels
            ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
            ax.set_xlabel('日期 / Date', fontsize=12)
            ax.set_ylabel('累计收益 / Cumulative Return', fontsize=12)
            
            # 设置图例 / Set legend
            ax.legend(loc='best', fontsize=10, framealpha=0.9)
            
            # 设置网格 / Set grid
            ax.grid(True, alpha=0.3)
            
            # 格式化y轴为百分比 / Format y-axis as percentage
            from matplotlib.ticker import FuncFormatter
            ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{(y-1)*100:.1f}%'))
            
            # 自动调整日期标签 / Auto-adjust date labels
            fig.autofmt_xdate()
            
            # 保存图表 / Save chart
            if save_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = str(self._output_dir / f"cumulative_returns_{timestamp}.png")
            else:
                save_path = str(Path(save_path).expanduser())
            
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            plt.close(fig)
            
            self._logger.info(f"累计收益曲线图保存成功 / Cumulative returns chart saved: {save_path}")
            
            return save_path
            
        except Exception as e:
            error_msg = f"绘制累计收益曲线失败 / Failed to plot cumulative returns: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise VisualizationManagerError(error_msg) from e

    def plot_position_distribution(
        self,
        portfolio: Dict[str, float],
        save_path: Optional[str] = None,
        title: str = "持仓分布 / Position Distribution"
    ) -> str:
        """
        绘制持仓分布图 / Plot Position Distribution Chart
        
        Args:
            portfolio: 持仓字典 {股票代码: 持仓比例} / Portfolio dict {symbol: weight}
            save_path: 保存路径（可选）/ Save path (optional)
            title: 图表标题 / Chart title
            
        Returns:
            str: 保存的文件路径 / Saved file path
            
        Raises:
            VisualizationManagerError: 绘图失败时抛出 / Raised when plotting fails
        """
        self._logger.info(f"开始绘制持仓分布图 / Starting to plot position distribution")
        
        try:
            if not portfolio or len(portfolio) == 0:
                self._logger.warning("持仓数据为空 / Portfolio data is empty")
                # 创建空图表 / Create empty chart
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.text(0.5, 0.5, '暂无持仓数据 / No Position Data',
                       ha='center', va='center', fontsize=14)
                ax.axis('off')
            else:
                # 创建图表 / Create figure
                fig, ax = plt.subplots(figsize=(10, 8))
                
                # 准备数据 / Prepare data
                symbols = list(portfolio.keys())
                weights = list(portfolio.values())
                
                # 按权重排序 / Sort by weight
                sorted_indices = np.argsort(weights)[::-1]
                symbols = [symbols[i] for i in sorted_indices]
                weights = [weights[i] for i in sorted_indices]
                
                # 限制显示前20个持仓 / Limit to top 20 positions
                if len(symbols) > 20:
                    other_weight = sum(weights[20:])
                    symbols = symbols[:20] + ['其他 / Others']
                    weights = weights[:20] + [other_weight]
                
                # 创建颜色映射 / Create color map
                colors = plt.cm.Set3(np.linspace(0, 1, len(symbols)))
                
                # 绘制饼图 / Plot pie chart
                wedges, texts, autotexts = ax.pie(
                    weights,
                    labels=symbols,
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=colors,
                    textprops={'fontsize': 9}
                )
                
                # 设置百分比文本样式 / Set percentage text style
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
                    autotext.set_fontsize(8)
                
                # 设置标题 / Set title
                ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
            
            # 保存图表 / Save chart
            if save_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = str(self._output_dir / f"position_distribution_{timestamp}.png")
            else:
                save_path = str(Path(save_path).expanduser())
            
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            plt.close(fig)
            
            self._logger.info(f"持仓分布图保存成功 / Position distribution chart saved: {save_path}")
            
            return save_path
            
        except Exception as e:
            error_msg = f"绘制持仓分布图失败 / Failed to plot position distribution: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise VisualizationManagerError(error_msg) from e
    
    def plot_sector_distribution(
        self,
        sector_weights: Dict[str, float],
        save_path: Optional[str] = None,
        title: str = "行业分布 / Sector Distribution"
    ) -> str:
        """
        绘制行业分布图 / Plot Sector Distribution Chart
        
        Args:
            sector_weights: 行业权重字典 {行业名称: 权重} / Sector weights dict {sector: weight}
            save_path: 保存路径（可选）/ Save path (optional)
            title: 图表标题 / Chart title
            
        Returns:
            str: 保存的文件路径 / Saved file path
            
        Raises:
            VisualizationManagerError: 绘图失败时抛出 / Raised when plotting fails
        """
        self._logger.info(f"开始绘制行业分布图 / Starting to plot sector distribution")
        
        try:
            if not sector_weights or len(sector_weights) == 0:
                self._logger.warning("行业数据为空 / Sector data is empty")
                # 创建空图表 / Create empty chart
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.text(0.5, 0.5, '暂无行业数据 / No Sector Data',
                       ha='center', va='center', fontsize=14)
                ax.axis('off')
            else:
                # 创建图表 / Create figure
                fig, ax = plt.subplots(figsize=(12, 6))
                
                # 准备数据 / Prepare data
                sectors = list(sector_weights.keys())
                weights = list(sector_weights.values())
                
                # 按权重排序 / Sort by weight
                sorted_indices = np.argsort(weights)[::-1]
                sectors = [sectors[i] for i in sorted_indices]
                weights = [weights[i] for i in sorted_indices]
                
                # 创建颜色映射 / Create color map
                colors = plt.cm.Paired(np.linspace(0, 1, len(sectors)))
                
                # 绘制柱状图 / Plot bar chart
                bars = ax.bar(
                    range(len(sectors)),
                    weights,
                    color=colors,
                    edgecolor='white',
                    linewidth=1.5
                )
                
                # 在柱子上添加数值标签 / Add value labels on bars
                for i, (bar, weight) in enumerate(zip(bars, weights)):
                    height = bar.get_height()
                    ax.text(
                        bar.get_x() + bar.get_width() / 2.,
                        height,
                        f'{weight*100:.1f}%',
                        ha='center',
                        va='bottom',
                        fontsize=9,
                        fontweight='bold'
                    )
                
                # 设置x轴标签 / Set x-axis labels
                ax.set_xticks(range(len(sectors)))
                ax.set_xticklabels(sectors, rotation=45, ha='right', fontsize=10)
                
                # 设置标题和标签 / Set title and labels
                ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
                ax.set_xlabel('行业 / Sector', fontsize=12)
                ax.set_ylabel('权重 / Weight', fontsize=12)
                
                # 格式化y轴为百分比 / Format y-axis as percentage
                from matplotlib.ticker import FuncFormatter
                ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y*100:.0f}%'))
                
                # 设置网格 / Set grid
                ax.grid(True, alpha=0.3, axis='y')
                ax.set_axisbelow(True)
            
            # 保存图表 / Save chart
            if save_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = str(self._output_dir / f"sector_distribution_{timestamp}.png")
            else:
                save_path = str(Path(save_path).expanduser())
            
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            plt.close(fig)
            
            self._logger.info(f"行业分布图保存成功 / Sector distribution chart saved: {save_path}")
            
            return save_path
            
        except Exception as e:
            error_msg = f"绘制行业分布图失败 / Failed to plot sector distribution: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise VisualizationManagerError(error_msg) from e

    def plot_multi_model_comparison(
        self,
        model_returns: Dict[str, pd.Series],
        save_path: Optional[str] = None,
        title: str = "多模型对比 / Multi-Model Comparison"
    ) -> str:
        """
        绘制多模型对比图 / Plot Multi-Model Comparison Chart
        
        Args:
            model_returns: 模型收益率字典 {模型名称: 收益率序列} / Model returns dict {model_name: returns}
            save_path: 保存路径（可选）/ Save path (optional)
            title: 图表标题 / Chart title
            
        Returns:
            str: 保存的文件路径 / Saved file path
            
        Raises:
            VisualizationManagerError: 绘图失败时抛出 / Raised when plotting fails
        """
        self._logger.info(f"开始绘制多模型对比图 / Starting to plot multi-model comparison")
        
        try:
            if not model_returns or len(model_returns) == 0:
                raise VisualizationManagerError("模型收益率数据为空 / Model returns data is empty")
            
            # 创建图表 / Create figure
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
            
            # 定义颜色 / Define colors
            colors = plt.cm.tab10(np.linspace(0, 1, len(model_returns)))
            
            # 1. 绘制累计收益曲线对比 / Plot cumulative returns comparison
            for i, (model_name, returns) in enumerate(model_returns.items()):
                if len(returns) > 0:
                    cumulative_returns = (1 + returns).cumprod()
                    ax1.plot(
                        cumulative_returns.index,
                        cumulative_returns.values,
                        label=model_name,
                        linewidth=2,
                        color=colors[i]
                    )
            
            # 添加零线 / Add zero line
            ax1.axhline(y=1.0, color='gray', linestyle=':', alpha=0.5)
            
            # 设置第一个子图 / Set first subplot
            ax1.set_title('累计收益对比 / Cumulative Returns Comparison', 
                         fontsize=12, fontweight='bold', pad=15)
            ax1.set_xlabel('日期 / Date', fontsize=10)
            ax1.set_ylabel('累计收益 / Cumulative Return', fontsize=10)
            ax1.legend(loc='best', fontsize=9, framealpha=0.9)
            ax1.grid(True, alpha=0.3)
            
            # 格式化y轴为百分比 / Format y-axis as percentage
            from matplotlib.ticker import FuncFormatter
            ax1.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{(y-1)*100:.1f}%'))
            
            # 2. 绘制性能指标对比柱状图 / Plot performance metrics comparison bar chart
            metrics_data = []
            model_names = []
            
            for model_name, returns in model_returns.items():
                if len(returns) > 0:
                    # 计算关键指标 / Calculate key metrics
                    cumulative_returns = (1 + returns).cumprod()
                    total_return = cumulative_returns.iloc[-1] - 1 if len(cumulative_returns) > 0 else 0
                    
                    # 年化收益率 / Annual return
                    trading_days = len(returns)
                    years = trading_days / 252.0
                    annual_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0
                    
                    # 夏普比率 / Sharpe ratio
                    volatility = returns.std() * np.sqrt(252)
                    sharpe_ratio = annual_return / volatility if volatility > 0 else 0
                    
                    # 最大回撤 / Max drawdown
                    running_max = cumulative_returns.expanding().max()
                    drawdown = (cumulative_returns - running_max) / running_max
                    max_drawdown = abs(drawdown.min())
                    
                    metrics_data.append({
                        '年化收益率\nAnnual Return': annual_return * 100,
                        '夏普比率\nSharpe Ratio': sharpe_ratio,
                        '最大回撤\nMax Drawdown': max_drawdown * 100
                    })
                    model_names.append(model_name)
            
            if metrics_data:
                # 准备数据 / Prepare data
                metrics_df = pd.DataFrame(metrics_data, index=model_names)
                
                # 绘制分组柱状图 / Plot grouped bar chart
                x = np.arange(len(model_names))
                width = 0.25
                
                metric_names = list(metrics_df.columns)
                for i, metric in enumerate(metric_names):
                    offset = width * (i - 1)
                    bars = ax2.bar(
                        x + offset,
                        metrics_df[metric],
                        width,
                        label=metric,
                        alpha=0.8
                    )
                    
                    # 在柱子上添加数值标签 / Add value labels on bars
                    for bar in bars:
                        height = bar.get_height()
                        ax2.text(
                            bar.get_x() + bar.get_width() / 2.,
                            height,
                            f'{height:.2f}',
                            ha='center',
                            va='bottom',
                            fontsize=8
                        )
                
                # 设置第二个子图 / Set second subplot
                ax2.set_title('性能指标对比 / Performance Metrics Comparison',
                             fontsize=12, fontweight='bold', pad=15)
                ax2.set_xlabel('模型 / Model', fontsize=10)
                ax2.set_ylabel('数值 / Value', fontsize=10)
                ax2.set_xticks(x)
                ax2.set_xticklabels(model_names, rotation=45, ha='right', fontsize=9)
                ax2.legend(loc='best', fontsize=9, framealpha=0.9)
                ax2.grid(True, alpha=0.3, axis='y')
                ax2.set_axisbelow(True)
            
            # 设置总标题 / Set overall title
            fig.suptitle(title, fontsize=14, fontweight='bold', y=0.995)
            
            # 调整子图间距 / Adjust subplot spacing
            plt.tight_layout(rect=[0, 0, 1, 0.99])
            
            # 保存图表 / Save chart
            if save_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = str(self._output_dir / f"multi_model_comparison_{timestamp}.png")
            else:
                save_path = str(Path(save_path).expanduser())
            
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            plt.close(fig)
            
            self._logger.info(f"多模型对比图保存成功 / Multi-model comparison chart saved: {save_path}")
            
            return save_path
            
        except Exception as e:
            error_msg = f"绘制多模型对比图失败 / Failed to plot multi-model comparison: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise VisualizationManagerError(error_msg) from e
    
    def plot_training_curve(
        self,
        metrics: Dict[str, List[float]],
        save_path: Optional[str] = None,
        title: str = "训练曲线 / Training Curve"
    ) -> str:
        """
        绘制训练曲线 / Plot Training Curve
        
        Args:
            metrics: 训练指标字典 {指标名称: 值列表} / Training metrics dict {metric_name: values}
            save_path: 保存路径（可选）/ Save path (optional)
            title: 图表标题 / Chart title
            
        Returns:
            str: 保存的文件路径 / Saved file path
            
        Raises:
            VisualizationManagerError: 绘图失败时抛出 / Raised when plotting fails
        """
        self._logger.info(f"开始绘制训练曲线 / Starting to plot training curve")
        
        try:
            if not metrics or len(metrics) == 0:
                raise VisualizationManagerError("训练指标数据为空 / Training metrics data is empty")
            
            # 创建图表 / Create figure
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # 定义颜色 / Define colors
            colors = plt.cm.tab10(np.linspace(0, 1, len(metrics)))
            
            # 绘制每个指标的曲线 / Plot curve for each metric
            for i, (metric_name, values) in enumerate(metrics.items()):
                if len(values) > 0:
                    epochs = range(1, len(values) + 1)
                    ax.plot(
                        epochs,
                        values,
                        label=metric_name,
                        linewidth=2,
                        color=colors[i],
                        marker='o',
                        markersize=4
                    )
            
            # 设置标题和标签 / Set title and labels
            ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
            ax.set_xlabel('轮次 / Epoch', fontsize=12)
            ax.set_ylabel('指标值 / Metric Value', fontsize=12)
            
            # 设置图例 / Set legend
            ax.legend(loc='best', fontsize=10, framealpha=0.9)
            
            # 设置网格 / Set grid
            ax.grid(True, alpha=0.3)
            
            # 保存图表 / Save chart
            if save_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = str(self._output_dir / f"training_curve_{timestamp}.png")
            else:
                save_path = str(Path(save_path).expanduser())
            
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            plt.close(fig)
            
            self._logger.info(f"训练曲线图保存成功 / Training curve chart saved: {save_path}")
            
            return save_path
            
        except Exception as e:
            error_msg = f"绘制训练曲线失败 / Failed to plot training curve: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise VisualizationManagerError(error_msg) from e
    
    def create_report_with_charts(
        self,
        returns: pd.Series,
        portfolio: Optional[Dict[str, float]] = None,
        sector_weights: Optional[Dict[str, float]] = None,
        benchmark: Optional[pd.Series] = None,
        output_dir: Optional[str] = None
    ) -> Dict[str, str]:
        """
        创建包含多个图表的完整报告 / Create Complete Report with Multiple Charts
        
        Args:
            returns: 收益率序列 / Returns series
            portfolio: 持仓字典（可选）/ Portfolio dict (optional)
            sector_weights: 行业权重字典（可选）/ Sector weights dict (optional)
            benchmark: 基准收益率（可选）/ Benchmark returns (optional)
            output_dir: 输出目录（可选）/ Output directory (optional)
            
        Returns:
            Dict[str, str]: 图表路径字典 / Chart paths dict
            
        Raises:
            VisualizationManagerError: 创建失败时抛出 / Raised when creation fails
        """
        self._logger.info("开始创建完整报告 / Starting to create complete report")
        
        try:
            # 确定输出目录 / Determine output directory
            if output_dir is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_dir = self._output_dir / f"report_{timestamp}"
            else:
                output_dir = Path(output_dir).expanduser()
            
            output_dir.mkdir(parents=True, exist_ok=True)
            
            chart_paths = {}
            
            # 1. 生成累计收益曲线图 / Generate cumulative returns chart
            if len(returns) > 0:
                cumulative_path = str(output_dir / "cumulative_returns.png")
                chart_paths['cumulative_returns'] = self.plot_cumulative_returns(
                    returns, benchmark, cumulative_path
                )
            
            # 2. 生成持仓分布图 / Generate position distribution chart
            if portfolio and len(portfolio) > 0:
                position_path = str(output_dir / "position_distribution.png")
                chart_paths['position_distribution'] = self.plot_position_distribution(
                    portfolio, position_path
                )
            
            # 3. 生成行业分布图 / Generate sector distribution chart
            if sector_weights and len(sector_weights) > 0:
                sector_path = str(output_dir / "sector_distribution.png")
                chart_paths['sector_distribution'] = self.plot_sector_distribution(
                    sector_weights, sector_path
                )
            
            self._logger.info(
                f"完整报告创建成功 / Complete report created successfully\n"
                f"输出目录 / Output directory: {output_dir}\n"
                f"图表数量 / Chart count: {len(chart_paths)}"
            )
            
            return chart_paths
            
        except Exception as e:
            error_msg = f"创建完整报告失败 / Failed to create complete report: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise VisualizationManagerError(error_msg) from e
