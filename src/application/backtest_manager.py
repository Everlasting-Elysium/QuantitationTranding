"""
回测管理器模块 / Backtest Manager Module
负责执行回测流程，计算性能指标，生成回测报告
Responsible for executing backtest process, calculating performance metrics, and generating backtest reports
"""

import time
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from datetime import datetime

from ..infrastructure.logger_system import get_logger


@dataclass
class BacktestConfig:
    """
    回测配置 / Backtest Configuration
    
    Attributes:
        strategy_config: 策略配置 / Strategy configuration
        executor_config: 执行器配置 / Executor configuration
        benchmark: 基准指数 / Benchmark index
    """
    strategy_config: Dict[str, Any]
    executor_config: Dict[str, Any]
    benchmark: str


@dataclass
class Trade:
    """
    交易记录 / Trade Record
    
    Attributes:
        trade_id: 交易ID / Trade ID
        timestamp: 时间戳 / Timestamp
        symbol: 股票代码 / Stock symbol
        action: 操作类型（buy/sell）/ Action type (buy/sell)
        quantity: 数量 / Quantity
        price: 价格 / Price
        commission: 手续费 / Commission
        total_cost: 总成本 / Total cost
    """
    trade_id: str
    timestamp: str
    symbol: str
    action: str
    quantity: float
    price: float
    commission: float
    total_cost: float


@dataclass
class BacktestResult:
    """
    回测结果 / Backtest Result
    
    Attributes:
        returns: 收益率序列 / Returns series
        positions: 持仓数据 / Position data
        metrics: 性能指标 / Performance metrics
        trades: 交易记录列表 / Trade records list
        benchmark_returns: 基准收益率（可选）/ Benchmark returns (optional)
    """
    returns: pd.Series
    positions: pd.DataFrame
    metrics: Dict[str, float]
    trades: List[Trade]
    benchmark_returns: Optional[pd.Series] = None


class BacktestManagerError(Exception):
    """回测管理器错误 / Backtest Manager Error"""
    pass


class BacktestManager:
    """
    回测管理器 / Backtest Manager
    
    职责 / Responsibilities:
    - 执行回测流程 / Execute backtest process
    - 生成交易信号 / Generate trading signals
    - 计算性能指标 / Calculate performance metrics
    - 生成回测报告 / Generate backtest reports
    - 实现基准对比功能 / Implement benchmark comparison
    """
    
    def __init__(
        self,
        qlib_wrapper,
        output_dir: str = "./outputs/backtests"
    ):
        """
        初始化回测管理器 / Initialize Backtest Manager
        
        Args:
            qlib_wrapper: Qlib封装器实例 / Qlib wrapper instance
            output_dir: 输出目录 / Output directory
        """
        self._qlib_wrapper = qlib_wrapper
        self._output_dir = Path(output_dir).expanduser()
        self._logger = get_logger(__name__)
        
        # 确保输出目录存在 / Ensure output directory exists
        self._output_dir.mkdir(parents=True, exist_ok=True)
    
    def run_backtest(
        self,
        model_id: str,
        start_date: str,
        end_date: str,
        config: BacktestConfig
    ) -> BacktestResult:
        """
        运行回测 / Run Backtest
        
        Args:
            model_id: 模型ID / Model ID
            start_date: 开始日期 / Start date
            end_date: 结束日期 / End date
            config: 回测配置 / Backtest configuration
            
        Returns:
            BacktestResult: 回测结果 / Backtest result
            
        Raises:
            BacktestManagerError: 回测失败时抛出 / Raised when backtest fails
        """
        self._logger.info(
            f"开始回测 / Starting backtest\n"
            f"模型ID / Model ID: {model_id}\n"
            f"时间范围 / Time range: {start_date} 至 / to {end_date}\n"
            f"基准 / Benchmark: {config.benchmark}"
        )
        
        start_time = time.time()
        
        try:
            # 1. 加载模型 / Load model
            self._logger.info("加载模型 / Loading model...")
            model = self._load_model(model_id)
            
            # 2. 生成预测信号 / Generate prediction signals
            self._logger.info("生成预测信号 / Generating prediction signals...")
            predictions = self._generate_signals(model, start_date, end_date, config)
            
            # 3. 执行回测 / Execute backtest
            self._logger.info("执行回测 / Executing backtest...")
            portfolio_metrics, positions, trades = self._execute_backtest(
                predictions, start_date, end_date, config
            )
            
            # 4. 计算收益率 / Calculate returns
            self._logger.info("计算收益率 / Calculating returns...")
            returns = self._calculate_returns(portfolio_metrics)
            
            # 5. 获取基准收益率（如果配置了）/ Get benchmark returns (if configured)
            benchmark_returns = None
            if config.benchmark:
                self._logger.info(f"获取基准收益率 / Getting benchmark returns: {config.benchmark}")
                benchmark_returns = self._get_benchmark_returns(
                    config.benchmark, start_date, end_date
                )
            
            # 6. 计算性能指标 / Calculate performance metrics
            self._logger.info("计算性能指标 / Calculating performance metrics...")
            metrics = self.calculate_metrics(returns, benchmark_returns)
            
            # 7. 保存回测结果 / Save backtest results
            backtest_time = time.time() - start_time
            metrics["backtest_time"] = backtest_time
            
            result = BacktestResult(
                returns=returns,
                positions=positions,
                metrics=metrics,
                trades=trades,
                benchmark_returns=benchmark_returns
            )
            
            # 保存结果到文件 / Save results to file
            self._save_backtest_result(model_id, result, start_date, end_date)
            
            self._logger.info(
                f"回测完成 / Backtest completed\n"
                f"回测时长 / Backtest time: {backtest_time:.2f}秒 / seconds\n"
                f"总收益率 / Total return: {metrics.get('total_return', 0):.2%}\n"
                f"年化收益率 / Annual return: {metrics.get('annual_return', 0):.2%}\n"
                f"夏普比率 / Sharpe ratio: {metrics.get('sharpe_ratio', 0):.4f}\n"
                f"最大回撤 / Max drawdown: {metrics.get('max_drawdown', 0):.2%}"
            )
            
            return result
            
        except Exception as e:
            error_msg = f"回测失败 / Backtest failed: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise BacktestManagerError(error_msg) from e
    
    def _load_model(self, model_id: str) -> Any:
        """
        加载模型 / Load Model
        
        Args:
            model_id: 模型ID / Model ID
            
        Returns:
            Any: 加载的模型 / Loaded model
            
        Raises:
            BacktestManagerError: 加载失败时抛出 / Raised when loading fails
        """
        try:
            # 构建模型路径 / Build model path
            model_path = Path("./outputs/models") / model_id / "model.pkl"
            
            if not model_path.exists():
                raise FileNotFoundError(f"模型文件不存在 / Model file not found: {model_path}")
            
            # 加载模型 / Load model
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            self._logger.info(f"模型加载成功 / Model loaded successfully: {model_id}")
            
            return model
            
        except Exception as e:
            error_msg = f"加载模型失败 / Failed to load model: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise BacktestManagerError(error_msg) from e
    
    def _generate_signals(
        self,
        model: Any,
        start_date: str,
        end_date: str,
        config: BacktestConfig
    ) -> pd.DataFrame:
        """
        生成预测信号 / Generate Prediction Signals
        
        Args:
            model: 模型实例 / Model instance
            start_date: 开始日期 / Start date
            end_date: 结束日期 / End date
            config: 回测配置 / Backtest configuration
            
        Returns:
            pd.DataFrame: 预测信号 / Prediction signals
            
        Raises:
            BacktestManagerError: 生成失败时抛出 / Raised when generation fails
        """
        try:
            from qlib.data.dataset import DatasetH
            from qlib.data.dataset.handler import DataHandlerLP
            
            # 从配置中获取股票池 / Get instruments from config
            instruments = config.strategy_config.get("instruments", "csi300")
            
            # 创建数据处理器 / Create data handler
            handler = DataHandlerLP(
                instruments=instruments,
                start_time=start_date,
                end_time=end_date,
                infer_processors=[],
                learn_processors=[],
                fit_start_time=start_date,
                fit_end_time=end_date,
            )
            
            # 创建数据集 / Create dataset
            segments = {
                "test": (start_date, end_date),
            }
            
            dataset = DatasetH(
                handler=handler,
                segments=segments,
            )
            
            # 生成预测 / Generate predictions
            predictions = model.predict(dataset)
            
            self._logger.info(
                f"预测信号生成成功 / Prediction signals generated successfully\n"
                f"信号数量 / Signal count: {len(predictions)}"
            )
            
            return predictions
            
        except Exception as e:
            error_msg = f"生成预测信号失败 / Failed to generate prediction signals: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise BacktestManagerError(error_msg) from e
    
    def _execute_backtest(
        self,
        predictions: pd.DataFrame,
        start_date: str,
        end_date: str,
        config: BacktestConfig
    ) -> Tuple[pd.DataFrame, pd.DataFrame, List[Trade]]:
        """
        执行回测 / Execute Backtest
        
        Args:
            predictions: 预测信号 / Prediction signals
            start_date: 开始日期 / Start date
            end_date: 结束日期 / End date
            config: 回测配置 / Backtest configuration
            
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame, List[Trade]]: 
                组合指标、持仓数据、交易记录 / Portfolio metrics, position data, trade records
            
        Raises:
            BacktestManagerError: 执行失败时抛出 / Raised when execution fails
        """
        try:
            from qlib.backtest import backtest, executor
            from qlib.contrib.strategy import TopkDropoutStrategy
            from qlib.contrib.evaluate import risk_analysis
            
            # 构建策略配置 / Build strategy configuration
            strategy_config = {
                "class": "TopkDropoutStrategy",
                "module_path": "qlib.contrib.strategy",
                "kwargs": {
                    "signal": predictions,
                    "topk": config.strategy_config.get("topk", 50),
                    "n_drop": config.strategy_config.get("n_drop", 5),
                },
            }
            
            # 构建执行器配置 / Build executor configuration
            executor_config = {
                "class": "SimulatorExecutor",
                "module_path": "qlib.backtest.executor",
                "kwargs": {
                    "time_per_step": config.executor_config.get("time_per_step", "day"),
                    "generate_portfolio_metrics": True,
                },
            }
            
            # 执行回测 / Execute backtest
            portfolio_metrics = backtest(
                pred=predictions,
                strategy=strategy_config,
                executor=executor_config,
                start_time=start_date,
                end_time=end_date,
            )
            
            # 提取持仓数据 / Extract position data
            positions = portfolio_metrics[0] if isinstance(portfolio_metrics, tuple) else portfolio_metrics
            
            # 提取交易记录 / Extract trade records
            trades = self._extract_trades(positions)
            
            self._logger.info(
                f"回测执行成功 / Backtest executed successfully\n"
                f"交易次数 / Trade count: {len(trades)}"
            )
            
            return portfolio_metrics, positions, trades
            
        except Exception as e:
            error_msg = f"执行回测失败 / Failed to execute backtest: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise BacktestManagerError(error_msg) from e
    
    def _extract_trades(self, positions: pd.DataFrame) -> List[Trade]:
        """
        从持仓数据中提取交易记录 / Extract Trade Records from Position Data
        
        Args:
            positions: 持仓数据 / Position data
            
        Returns:
            List[Trade]: 交易记录列表 / Trade records list
        """
        trades = []
        
        try:
            # 如果positions是DataFrame，尝试提取交易信息
            # If positions is DataFrame, try to extract trade information
            if isinstance(positions, pd.DataFrame):
                # 这里简化处理，实际应该从qlib的回测结果中提取详细交易记录
                # Simplified here, should extract detailed trade records from qlib backtest results
                trade_count = 0
                for idx, row in positions.iterrows():
                    if isinstance(idx, tuple) and len(idx) >= 2:
                        timestamp = str(idx[0])
                        symbol = str(idx[1]) if len(idx) > 1 else "unknown"
                        
                        # 创建交易记录 / Create trade record
                        trade = Trade(
                            trade_id=f"trade_{trade_count}",
                            timestamp=timestamp,
                            symbol=symbol,
                            action="buy",  # 简化处理 / Simplified
                            quantity=0.0,
                            price=0.0,
                            commission=0.0,
                            total_cost=0.0
                        )
                        trades.append(trade)
                        trade_count += 1
            
        except Exception as e:
            self._logger.warning(f"提取交易记录失败 / Failed to extract trade records: {str(e)}")
        
        return trades
    
    def _calculate_returns(self, portfolio_metrics: Any) -> pd.Series:
        """
        计算收益率 / Calculate Returns
        
        Args:
            portfolio_metrics: 组合指标 / Portfolio metrics
            
        Returns:
            pd.Series: 收益率序列 / Returns series
            
        Raises:
            BacktestManagerError: 计算失败时抛出 / Raised when calculation fails
        """
        try:
            # 从portfolio_metrics中提取收益率
            # Extract returns from portfolio_metrics
            if isinstance(portfolio_metrics, tuple):
                # qlib的backtest返回(portfolio_metrics, indicator)
                # qlib backtest returns (portfolio_metrics, indicator)
                portfolio_metrics = portfolio_metrics[0]
            
            # 尝试从不同的可能字段中获取收益率
            # Try to get returns from different possible fields
            if isinstance(portfolio_metrics, pd.DataFrame):
                if 'return' in portfolio_metrics.columns:
                    returns = portfolio_metrics['return']
                elif 'cum_return' in portfolio_metrics.columns:
                    # 从累计收益率计算日收益率
                    # Calculate daily returns from cumulative returns
                    cum_returns = portfolio_metrics['cum_return']
                    returns = cum_returns.pct_change().fillna(0)
                else:
                    # 如果没有收益率列，创建一个空的序列
                    # If no return column, create an empty series
                    self._logger.warning("未找到收益率列，创建空序列 / Return column not found, creating empty series")
                    returns = pd.Series(dtype=float)
            else:
                # 如果不是DataFrame，尝试直接使用
                # If not DataFrame, try to use directly
                returns = pd.Series(portfolio_metrics)
            
            # 确保返回Series / Ensure returning Series
            if not isinstance(returns, pd.Series):
                returns = pd.Series(returns)
            
            return returns
            
        except Exception as e:
            error_msg = f"计算收益率失败 / Failed to calculate returns: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise BacktestManagerError(error_msg) from e
    
    def _get_benchmark_returns(
        self,
        benchmark: str,
        start_date: str,
        end_date: str
    ) -> pd.Series:
        """
        获取基准收益率 / Get Benchmark Returns
        
        Args:
            benchmark: 基准指数 / Benchmark index
            start_date: 开始日期 / Start date
            end_date: 结束日期 / End date
            
        Returns:
            pd.Series: 基准收益率序列 / Benchmark returns series
            
        Raises:
            BacktestManagerError: 获取失败时抛出 / Raised when retrieval fails
        """
        try:
            import qlib
            
            # 使用qlib获取基准数据 / Use qlib to get benchmark data
            benchmark_data = qlib.data.D.features(
                [benchmark],
                ["$close"],
                start_time=start_date,
                end_time=end_date
            )
            
            if benchmark_data is None or benchmark_data.empty:
                self._logger.warning(f"基准数据为空 / Benchmark data is empty: {benchmark}")
                return pd.Series(dtype=float)
            
            # 计算基准收益率 / Calculate benchmark returns
            benchmark_prices = benchmark_data["$close"]
            benchmark_returns = benchmark_prices.pct_change().fillna(0)
            
            # 如果是MultiIndex，取第一层 / If MultiIndex, take first level
            if isinstance(benchmark_returns.index, pd.MultiIndex):
                benchmark_returns = benchmark_returns.droplevel(1)
            
            self._logger.info(
                f"基准收益率获取成功 / Benchmark returns retrieved successfully\n"
                f"基准 / Benchmark: {benchmark}\n"
                f"数据点数 / Data points: {len(benchmark_returns)}"
            )
            
            return benchmark_returns
            
        except Exception as e:
            error_msg = f"获取基准收益率失败 / Failed to get benchmark returns: {str(e)}"
            self._logger.warning(error_msg)
            # 返回空序列而不是抛出异常 / Return empty series instead of raising exception
            return pd.Series(dtype=float)
    
    def calculate_metrics(
        self,
        returns: pd.Series,
        benchmark: Optional[pd.Series] = None
    ) -> Dict[str, float]:
        """
        计算性能指标 / Calculate Performance Metrics
        
        Args:
            returns: 收益率序列 / Returns series
            benchmark: 基准收益率序列（可选）/ Benchmark returns series (optional)
            
        Returns:
            Dict[str, float]: 性能指标字典 / Performance metrics dictionary
            
        Raises:
            BacktestManagerError: 计算失败时抛出 / Raised when calculation fails
        """
        try:
            metrics = {}
            
            # 确保returns是Series / Ensure returns is Series
            if not isinstance(returns, pd.Series):
                returns = pd.Series(returns)
            
            # 如果returns为空，返回零值指标 / If returns is empty, return zero metrics
            if len(returns) == 0:
                self._logger.warning("收益率序列为空 / Returns series is empty")
                return {
                    "total_return": 0.0,
                    "annual_return": 0.0,
                    "sharpe_ratio": 0.0,
                    "max_drawdown": 0.0,
                    "volatility": 0.0,
                    "win_rate": 0.0,
                }
            
            # 1. 总收益率 / Total return
            cumulative_returns = (1 + returns).cumprod()
            metrics["total_return"] = float(cumulative_returns.iloc[-1] - 1) if len(cumulative_returns) > 0 else 0.0
            
            # 2. 年化收益率 / Annual return
            trading_days = len(returns)
            years = trading_days / 252.0  # 假设一年252个交易日 / Assume 252 trading days per year
            if years > 0:
                metrics["annual_return"] = float((1 + metrics["total_return"]) ** (1 / years) - 1)
            else:
                metrics["annual_return"] = 0.0
            
            # 3. 波动率 / Volatility
            metrics["volatility"] = float(returns.std() * np.sqrt(252))
            
            # 4. 夏普比率 / Sharpe ratio
            if metrics["volatility"] > 0:
                metrics["sharpe_ratio"] = float(metrics["annual_return"] / metrics["volatility"])
            else:
                metrics["sharpe_ratio"] = 0.0
            
            # 5. 最大回撤 / Max drawdown
            metrics["max_drawdown"] = float(self._calculate_max_drawdown(cumulative_returns))
            
            # 6. 胜率 / Win rate
            positive_returns = (returns > 0).sum()
            total_returns = len(returns)
            metrics["win_rate"] = float(positive_returns / total_returns) if total_returns > 0 else 0.0
            
            # 7. 如果有基准，计算超额收益 / If benchmark exists, calculate excess returns
            if benchmark is not None and len(benchmark) > 0:
                # 对齐索引 / Align indices
                common_index = returns.index.intersection(benchmark.index)
                if len(common_index) > 0:
                    aligned_returns = returns.loc[common_index]
                    aligned_benchmark = benchmark.loc[common_index]
                    
                    # 超额收益 / Excess returns
                    excess_returns = aligned_returns - aligned_benchmark
                    
                    # 累计超额收益 / Cumulative excess returns
                    cumulative_excess = (1 + excess_returns).cumprod()
                    metrics["excess_return"] = float(cumulative_excess.iloc[-1] - 1) if len(cumulative_excess) > 0 else 0.0
                    
                    # 信息比率 / Information ratio
                    excess_volatility = excess_returns.std() * np.sqrt(252)
                    if excess_volatility > 0:
                        metrics["information_ratio"] = float((excess_returns.mean() * 252) / excess_volatility)
                    else:
                        metrics["information_ratio"] = 0.0
                    
                    # 基准总收益 / Benchmark total return
                    benchmark_cumulative = (1 + aligned_benchmark).cumprod()
                    metrics["benchmark_return"] = float(benchmark_cumulative.iloc[-1] - 1) if len(benchmark_cumulative) > 0 else 0.0
                else:
                    self._logger.warning("收益率和基准没有共同索引 / No common index between returns and benchmark")
            
            self._logger.info(f"性能指标计算完成 / Performance metrics calculated: {metrics}")
            
            return metrics
            
        except Exception as e:
            error_msg = f"计算性能指标失败 / Failed to calculate performance metrics: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise BacktestManagerError(error_msg) from e
    
    def _calculate_max_drawdown(self, cumulative_returns: pd.Series) -> float:
        """
        计算最大回撤 / Calculate Max Drawdown
        
        Args:
            cumulative_returns: 累计收益率序列 / Cumulative returns series
            
        Returns:
            float: 最大回撤 / Max drawdown
        """
        try:
            if len(cumulative_returns) == 0:
                return 0.0
            
            # 计算累计最大值 / Calculate cumulative maximum
            running_max = cumulative_returns.expanding().max()
            
            # 计算回撤 / Calculate drawdown
            drawdown = (cumulative_returns - running_max) / running_max
            
            # 返回最大回撤（负值）/ Return max drawdown (negative value)
            max_dd = float(drawdown.min())
            
            return max_dd
            
        except Exception as e:
            self._logger.warning(f"计算最大回撤失败 / Failed to calculate max drawdown: {str(e)}")
            return 0.0
    
    def _save_backtest_result(
        self,
        model_id: str,
        result: BacktestResult,
        start_date: str,
        end_date: str
    ) -> None:
        """
        保存回测结果 / Save Backtest Result
        
        Args:
            model_id: 模型ID / Model ID
            result: 回测结果 / Backtest result
            start_date: 开始日期 / Start date
            end_date: 结束日期 / End date
        """
        try:
            # 创建结果目录 / Create result directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            result_dir = self._output_dir / f"{model_id}_{timestamp}"
            result_dir.mkdir(parents=True, exist_ok=True)
            
            # 保存指标 / Save metrics
            import json
            metrics_path = result_dir / "metrics.json"
            with open(metrics_path, 'w', encoding='utf-8') as f:
                json.dump(result.metrics, f, indent=2, ensure_ascii=False)
            
            # 保存收益率 / Save returns
            returns_path = result_dir / "returns.csv"
            result.returns.to_csv(returns_path)
            
            # 保存持仓数据 / Save positions
            positions_path = result_dir / "positions.csv"
            result.positions.to_csv(positions_path)
            
            # 保存交易记录 / Save trades
            if result.trades:
                trades_path = result_dir / "trades.csv"
                trades_data = []
                for trade in result.trades:
                    trades_data.append({
                        "trade_id": trade.trade_id,
                        "timestamp": trade.timestamp,
                        "symbol": trade.symbol,
                        "action": trade.action,
                        "quantity": trade.quantity,
                        "price": trade.price,
                        "commission": trade.commission,
                        "total_cost": trade.total_cost,
                    })
                trades_df = pd.DataFrame(trades_data)
                trades_df.to_csv(trades_path, index=False)
            
            # 保存基准收益率（如果有）/ Save benchmark returns (if exists)
            if result.benchmark_returns is not None:
                benchmark_path = result_dir / "benchmark_returns.csv"
                result.benchmark_returns.to_csv(benchmark_path)
            
            # 保存回测配置信息 / Save backtest configuration
            config_path = result_dir / "config.json"
            config_data = {
                "model_id": model_id,
                "start_date": start_date,
                "end_date": end_date,
                "backtest_time": result.metrics.get("backtest_time", 0),
                "created_at": datetime.now().isoformat(),
            }
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            self._logger.info(
                f"回测结果保存成功 / Backtest result saved successfully\n"
                f"路径 / Path: {result_dir}"
            )
            
        except Exception as e:
            self._logger.warning(f"保存回测结果失败 / Failed to save backtest result: {str(e)}")
