"""
交易信号生成器模块 / Signal Generator Module
负责生成交易信号、应用风险控制和解释信号原因
Responsible for generating trading signals, applying risk control, and explaining signal reasons
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path

from ..models.trading_models import (
    Signal, SignalExplanation, Portfolio, Position, RiskLimits
)
from ..application.model_registry import ModelRegistry
from ..infrastructure.qlib_wrapper import QlibWrapper
from ..infrastructure.logger_system import get_logger


class SignalGeneratorError(Exception):
    """信号生成器错误 / Signal Generator Error"""
    pass


class SignalGenerator:
    """
    交易信号生成器 / Trading Signal Generator
    
    职责 / Responsibilities:
    - 生成交易信号 / Generate trading signals
    - 应用风险控制 / Apply risk control
    - 解释信号原因 / Explain signal reasons
    - 股票排序和候选列表生成 / Stock sorting and candidate list generation
    - 持仓限制检查 / Position limit checking
    """
    
    def __init__(
        self,
        model_registry: ModelRegistry,
        qlib_wrapper: QlibWrapper,
        risk_limits: Optional[RiskLimits] = None
    ):
        """
        初始化信号生成器 / Initialize Signal Generator
        
        Args:
            model_registry: 模型注册表 / Model registry
            qlib_wrapper: Qlib封装器 / Qlib wrapper
            risk_limits: 风险限制（可选）/ Risk limits (optional)
        """
        self._model_registry = model_registry
        self._qlib_wrapper = qlib_wrapper
        self._risk_limits = risk_limits or RiskLimits()
        self._logger = get_logger(__name__)
        
        self._logger.info(
            f"信号生成器初始化成功 / Signal generator initialized successfully\n"
            f"风险限制 / Risk limits:\n"
            f"  最大持仓比例 / Max position size: {self._risk_limits.max_position_size:.1%}\n"
            f"  单只股票最大权重 / Max single stock: {self._risk_limits.max_single_stock:.1%}\n"
            f"  最小现金储备 / Min cash reserve: {self._risk_limits.min_cash_reserve:.1%}"
        )
    
    def generate_signals(
        self,
        model_id: str,
        date: str,
        portfolio: Portfolio,
        top_n: int = 10,
        instruments: str = "csi300"
    ) -> List[Signal]:
        """
        生成交易信号 / Generate Trading Signals
        
        根据模型预测、当前持仓和风险限制生成交易信号
        Generate trading signals based on model predictions, current positions, and risk limits
        
        Args:
            model_id: 模型ID / Model ID
            date: 信号生成日期 / Signal generation date
            portfolio: 当前投资组合 / Current portfolio
            top_n: 买入候选数量 / Number of buy candidates
            instruments: 股票池 / Instrument pool
            
        Returns:
            List[Signal]: 交易信号列表 / List of trading signals
            
        Raises:
            SignalGeneratorError: 生成失败时抛出 / Raised when generation fails
        """
        try:
            self._logger.info(
                f"开始生成交易信号 / Starting signal generation\n"
                f"模型ID / Model ID: {model_id}\n"
                f"日期 / Date: {date}\n"
                f"股票池 / Instruments: {instruments}\n"
                f"买入候选数 / Top N: {top_n}"
            )
            
            # 1. 加载模型 / Load model
            model = self._model_registry.get_model(model_id)
            
            # 2. 获取最新数据并进行预测 / Get latest data and make predictions
            predictions = self._get_predictions(model, date, instruments)
            
            if predictions is None or predictions.empty:
                self._logger.warning("预测结果为空 / Predictions are empty")
                return []
            
            # 3. 根据预测分数排序股票 / Sort stocks by prediction scores
            sorted_stocks = self._sort_stocks_by_score(predictions)
            
            # 4. 生成买入信号 / Generate buy signals
            buy_signals = self._generate_buy_signals(
                sorted_stocks, portfolio, top_n, date
            )
            
            # 5. 生成卖出信号 / Generate sell signals
            sell_signals = self._generate_sell_signals(
                sorted_stocks, portfolio, date
            )
            
            # 6. 生成持有信号 / Generate hold signals
            hold_signals = self._generate_hold_signals(
                sorted_stocks, portfolio, date
            )
            
            # 7. 合并所有信号 / Combine all signals
            all_signals = buy_signals + sell_signals + hold_signals
            
            # 8. 应用风险控制 / Apply risk control
            filtered_signals = self._apply_risk_control(all_signals, portfolio)
            
            self._logger.info(
                f"信号生成完成 / Signal generation completed\n"
                f"买入信号 / Buy signals: {len(buy_signals)}\n"
                f"卖出信号 / Sell signals: {len(sell_signals)}\n"
                f"持有信号 / Hold signals: {len(hold_signals)}\n"
                f"风控后信号 / After risk control: {len(filtered_signals)}"
            )
            
            return filtered_signals
            
        except Exception as e:
            error_msg = f"生成交易信号失败 / Failed to generate signals: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise SignalGeneratorError(error_msg) from e
    
    def explain_signal(self, signal: Signal) -> SignalExplanation:
        """
        解释交易信号 / Explain Trading Signal
        
        提供信号的主要影响因素和风险评估
        Provide main factors and risk assessment for the signal
        
        Args:
            signal: 交易信号 / Trading signal
            
        Returns:
            SignalExplanation: 信号解释 / Signal explanation
            
        Raises:
            SignalGeneratorError: 解释失败时抛出 / Raised when explanation fails
        """
        try:
            self._logger.info(
                f"解释交易信号 / Explaining signal\n"
                f"股票代码 / Stock code: {signal.stock_code}\n"
                f"动作 / Action: {signal.action}\n"
                f"分数 / Score: {signal.score:.4f}"
            )
            
            # 1. 分析主要因素 / Analyze main factors
            # 这里使用简化的实现，实际应该基于模型的特征重要性
            # This is a simplified implementation, should be based on model's feature importance
            main_factors = self._analyze_main_factors(signal)
            
            # 2. 评估风险等级 / Assess risk level
            risk_level = self._assess_risk_level(signal)
            
            # 3. 生成描述 / Generate description
            description = self._generate_signal_description(
                signal, main_factors, risk_level
            )
            
            explanation = SignalExplanation(
                signal=signal,
                main_factors=main_factors,
                risk_level=risk_level,
                description=description
            )
            
            self._logger.info(
                f"信号解释完成 / Signal explanation completed\n"
                f"风险等级 / Risk level: {risk_level}\n"
                f"主要因素数 / Main factors count: {len(main_factors)}"
            )
            
            return explanation
            
        except Exception as e:
            error_msg = f"解释信号失败 / Failed to explain signal: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise SignalGeneratorError(error_msg) from e
    
    def _get_predictions(
        self,
        model: Any,
        date: str,
        instruments: str
    ) -> Optional[pd.DataFrame]:
        """
        获取模型预测 / Get Model Predictions
        
        Args:
            model: 模型对象 / Model object
            date: 预测日期 / Prediction date
            instruments: 股票池 / Instrument pool
            
        Returns:
            Optional[pd.DataFrame]: 预测结果 / Prediction results
        """
        try:
            # 使用qlib的数据接口获取最新数据
            # Use qlib's data interface to get latest data
            # 这里需要根据模型的特征需求获取相应的数据
            # Need to get corresponding data based on model's feature requirements
            
            # 简化实现：假设模型有predict方法
            # Simplified implementation: assume model has predict method
            if hasattr(model, 'predict'):
                # 获取数据
                # Get data
                data = self._qlib_wrapper.get_data(
                    instruments=instruments,
                    fields=["$close", "$volume", "$open", "$high", "$low"],
                    start_time=date,
                    end_time=date
                )
                
                if data is None or data.empty:
                    self._logger.warning(f"无法获取日期 {date} 的数据 / Cannot get data for date {date}")
                    return None
                
                # 进行预测
                # Make predictions
                predictions = model.predict(data)
                
                # 转换为DataFrame格式
                # Convert to DataFrame format
                if isinstance(predictions, pd.Series):
                    pred_df = predictions.to_frame(name='score')
                elif isinstance(predictions, np.ndarray):
                    pred_df = pd.DataFrame(predictions, columns=['score'])
                else:
                    pred_df = predictions
                
                return pred_df
            else:
                self._logger.error("模型没有predict方法 / Model does not have predict method")
                return None
                
        except Exception as e:
            self._logger.error(f"获取预测失败 / Failed to get predictions: {str(e)}", exc_info=True)
            return None
    
    def _sort_stocks_by_score(
        self,
        predictions: pd.DataFrame
    ) -> pd.DataFrame:
        """
        根据预测分数排序股票 / Sort Stocks by Prediction Score
        
        Args:
            predictions: 预测结果 / Prediction results
            
        Returns:
            pd.DataFrame: 排序后的股票 / Sorted stocks
        """
        try:
            # 确保有score列
            # Ensure score column exists
            if 'score' not in predictions.columns:
                # 如果没有score列，使用第一列作为score
                # If no score column, use first column as score
                predictions = predictions.copy()
                predictions['score'] = predictions.iloc[:, 0]
            
            # 按分数降序排序
            # Sort by score in descending order
            sorted_df = predictions.sort_values('score', ascending=False)
            
            self._logger.debug(
                f"股票排序完成 / Stock sorting completed\n"
                f"总数 / Total: {len(sorted_df)}\n"
                f"最高分 / Highest score: {sorted_df['score'].iloc[0]:.4f}\n"
                f"最低分 / Lowest score: {sorted_df['score'].iloc[-1]:.4f}"
            )
            
            return sorted_df
            
        except Exception as e:
            self._logger.error(f"股票排序失败 / Failed to sort stocks: {str(e)}", exc_info=True)
            return predictions
    
    def _generate_buy_signals(
        self,
        sorted_stocks: pd.DataFrame,
        portfolio: Portfolio,
        top_n: int,
        date: str
    ) -> List[Signal]:
        """
        生成买入信号 / Generate Buy Signals
        
        Args:
            sorted_stocks: 排序后的股票 / Sorted stocks
            portfolio: 当前投资组合 / Current portfolio
            top_n: 买入候选数量 / Number of buy candidates
            date: 信号日期 / Signal date
            
        Returns:
            List[Signal]: 买入信号列表 / List of buy signals
        """
        buy_signals = []
        
        try:
            # 获取前top_n只股票
            # Get top N stocks
            top_stocks = sorted_stocks.head(top_n)
            
            for stock_code, row in top_stocks.iterrows():
                # 检查是否已持有
                # Check if already holding
                if stock_code in portfolio.positions:
                    # 如果已持有，跳过（会在hold_signals中处理）
                    # If already holding, skip (will be handled in hold_signals)
                    continue
                
                # 计算置信度（基于分数的归一化）
                # Calculate confidence (normalized based on score)
                confidence = self._calculate_confidence(row['score'], sorted_stocks['score'])
                
                # 创建买入信号
                # Create buy signal
                signal = Signal(
                    stock_code=stock_code,
                    action="buy",
                    score=float(row['score']),
                    confidence=confidence,
                    timestamp=date,
                    reason=f"模型预测分数高 / High model prediction score: {row['score']:.4f}"
                )
                
                buy_signals.append(signal)
            
            self._logger.debug(
                f"生成买入信号 / Generated buy signals: {len(buy_signals)}"
            )
            
        except Exception as e:
            self._logger.error(f"生成买入信号失败 / Failed to generate buy signals: {str(e)}", exc_info=True)
        
        return buy_signals
    
    def _generate_sell_signals(
        self,
        sorted_stocks: pd.DataFrame,
        portfolio: Portfolio,
        date: str
    ) -> List[Signal]:
        """
        生成卖出信号 / Generate Sell Signals
        
        Args:
            sorted_stocks: 排序后的股票 / Sorted stocks
            portfolio: 当前投资组合 / Current portfolio
            date: 信号日期 / Signal date
            
        Returns:
            List[Signal]: 卖出信号列表 / List of sell signals
        """
        sell_signals = []
        
        try:
            # 检查当前持仓中分数较低的股票
            # Check stocks in current positions with low scores
            for stock_code, position in portfolio.positions.items():
                if stock_code in sorted_stocks.index:
                    score = sorted_stocks.loc[stock_code, 'score']
                    
                    # 如果分数低于中位数，考虑卖出
                    # If score below median, consider selling
                    median_score = sorted_stocks['score'].median()
                    
                    if score < median_score:
                        confidence = self._calculate_confidence(score, sorted_stocks['score'])
                        
                        signal = Signal(
                            stock_code=stock_code,
                            action="sell",
                            score=float(score),
                            confidence=confidence,
                            timestamp=date,
                            quantity=position.quantity,
                            reason=f"模型预测分数低于中位数 / Score below median: {score:.4f} < {median_score:.4f}"
                        )
                        
                        sell_signals.append(signal)
                else:
                    # 如果股票不在预测结果中，建议卖出
                    # If stock not in predictions, suggest selling
                    signal = Signal(
                        stock_code=stock_code,
                        action="sell",
                        score=0.0,
                        confidence=0.8,
                        timestamp=date,
                        quantity=position.quantity,
                        reason="股票不在当前股票池中 / Stock not in current instrument pool"
                    )
                    
                    sell_signals.append(signal)
            
            self._logger.debug(
                f"生成卖出信号 / Generated sell signals: {len(sell_signals)}"
            )
            
        except Exception as e:
            self._logger.error(f"生成卖出信号失败 / Failed to generate sell signals: {str(e)}", exc_info=True)
        
        return sell_signals
    
    def _generate_hold_signals(
        self,
        sorted_stocks: pd.DataFrame,
        portfolio: Portfolio,
        date: str
    ) -> List[Signal]:
        """
        生成持有信号 / Generate Hold Signals
        
        Args:
            sorted_stocks: 排序后的股票 / Sorted stocks
            portfolio: 当前投资组合 / Current portfolio
            date: 信号日期 / Signal date
            
        Returns:
            List[Signal]: 持有信号列表 / List of hold signals
        """
        hold_signals = []
        
        try:
            # 检查当前持仓中分数较高的股票
            # Check stocks in current positions with high scores
            median_score = sorted_stocks['score'].median()
            
            for stock_code, position in portfolio.positions.items():
                if stock_code in sorted_stocks.index:
                    score = sorted_stocks.loc[stock_code, 'score']
                    
                    # 如果分数高于中位数，建议持有
                    # If score above median, suggest holding
                    if score >= median_score:
                        confidence = self._calculate_confidence(score, sorted_stocks['score'])
                        
                        signal = Signal(
                            stock_code=stock_code,
                            action="hold",
                            score=float(score),
                            confidence=confidence,
                            timestamp=date,
                            quantity=position.quantity,
                            reason=f"模型预测分数良好 / Good model prediction score: {score:.4f}"
                        )
                        
                        hold_signals.append(signal)
            
            self._logger.debug(
                f"生成持有信号 / Generated hold signals: {len(hold_signals)}"
            )
            
        except Exception as e:
            self._logger.error(f"生成持有信号失败 / Failed to generate hold signals: {str(e)}", exc_info=True)
        
        return hold_signals
    
    def _apply_risk_control(
        self,
        signals: List[Signal],
        portfolio: Portfolio
    ) -> List[Signal]:
        """
        应用风险控制 / Apply Risk Control
        
        根据风险限制过滤和调整信号
        Filter and adjust signals based on risk limits
        
        Args:
            signals: 原始信号列表 / Original signal list
            portfolio: 当前投资组合 / Current portfolio
            
        Returns:
            List[Signal]: 风控后的信号列表 / Filtered signal list
        """
        try:
            filtered_signals = []
            
            # 更新投资组合总价值
            # Update portfolio total value
            portfolio.update_total_value()
            
            # 计算当前持仓总价值占比
            # Calculate current position value ratio
            positions_value = sum(pos.market_value for pos in portfolio.positions.values())
            current_position_ratio = positions_value / portfolio.total_value if portfolio.total_value > 0 else 0
            
            # 计算可用于新买入的资金
            # Calculate available cash for new purchases
            min_cash = portfolio.total_value * self._risk_limits.min_cash_reserve
            available_cash = max(0, portfolio.cash - min_cash)
            
            self._logger.debug(
                f"风险控制检查 / Risk control check\n"
                f"当前持仓占比 / Current position ratio: {current_position_ratio:.2%}\n"
                f"可用现金 / Available cash: {available_cash:.2f}\n"
                f"最大持仓比例 / Max position size: {self._risk_limits.max_position_size:.2%}"
            )
            
            for signal in signals:
                # 1. 检查持仓限制 / Check position limits
                if signal.action == "buy":
                    # 检查是否超过最大持仓比例
                    # Check if exceeds max position size
                    if current_position_ratio >= self._risk_limits.max_position_size:
                        self._logger.debug(
                            f"跳过买入信号（超过最大持仓比例）/ Skip buy signal (exceeds max position size): {signal.stock_code}"
                        )
                        continue
                    
                    # 检查单只股票权重限制
                    # Check single stock weight limit
                    max_single_value = portfolio.total_value * self._risk_limits.max_single_stock
                    
                    # 计算建议买入数量
                    # Calculate suggested quantity
                    if signal.quantity is None:
                        # 简化实现：平均分配可用资金
                        # Simplified: evenly distribute available cash
                        buy_signals_count = sum(1 for s in signals if s.action == "buy")
                        if buy_signals_count > 0:
                            target_value = min(
                                available_cash / buy_signals_count,
                                max_single_value
                            )
                            signal.target_weight = (target_value / portfolio.total_value) * 100 if portfolio.total_value > 0 else 0
                    
                    # 检查是否有足够现金
                    # Check if enough cash available
                    if available_cash <= 0:
                        self._logger.debug(
                            f"跳过买入信号（现金不足）/ Skip buy signal (insufficient cash): {signal.stock_code}"
                        )
                        continue
                
                elif signal.action == "sell":
                    # 卖出信号通常不需要额外的风控检查
                    # Sell signals usually don't need additional risk checks
                    pass
                
                elif signal.action == "hold":
                    # 持有信号不需要风控检查
                    # Hold signals don't need risk checks
                    pass
                
                # 2. 检查单只股票权重 / Check single stock weight
                if signal.action in ["buy", "hold"]:
                    current_weight = portfolio.get_position_weight(signal.stock_code)
                    max_weight_pct = self._risk_limits.max_single_stock * 100
                    
                    if current_weight > max_weight_pct:
                        self._logger.warning(
                            f"股票权重超限 / Stock weight exceeds limit: {signal.stock_code} "
                            f"({current_weight:.2f}% > {max_weight_pct:.2f}%)"
                        )
                        # 如果是买入信号，跳过；如果是持有信号，保留但添加警告
                        # If buy signal, skip; if hold signal, keep but add warning
                        if signal.action == "buy":
                            continue
                
                # 通过所有检查，添加到过滤后的列表
                # Passed all checks, add to filtered list
                filtered_signals.append(signal)
            
            self._logger.info(
                f"风险控制完成 / Risk control completed\n"
                f"原始信号数 / Original signals: {len(signals)}\n"
                f"过滤后信号数 / Filtered signals: {len(filtered_signals)}"
            )
            
            return filtered_signals
            
        except Exception as e:
            self._logger.error(f"应用风险控制失败 / Failed to apply risk control: {str(e)}", exc_info=True)
            # 如果风控失败，返回空列表以确保安全
            # If risk control fails, return empty list for safety
            return []
    
    def _calculate_confidence(
        self,
        score: float,
        all_scores: pd.Series
    ) -> float:
        """
        计算信号置信度 / Calculate Signal Confidence
        
        基于分数在所有分数中的位置计算置信度
        Calculate confidence based on score's position among all scores
        
        Args:
            score: 当前分数 / Current score
            all_scores: 所有分数 / All scores
            
        Returns:
            float: 置信度 (0-1) / Confidence (0-1)
        """
        try:
            # 使用分位数计算置信度
            # Use quantile to calculate confidence
            if len(all_scores) == 0:
                return 0.5
            
            # 计算分数的分位数位置
            # Calculate quantile position of the score
            percentile = (all_scores < score).sum() / len(all_scores)
            
            # 将分位数映射到置信度 (0.5-1.0)
            # Map quantile to confidence (0.5-1.0)
            confidence = 0.5 + (percentile * 0.5)
            
            return min(1.0, max(0.0, confidence))
            
        except Exception as e:
            self._logger.error(f"计算置信度失败 / Failed to calculate confidence: {str(e)}")
            return 0.5
    
    def _analyze_main_factors(
        self,
        signal: Signal
    ) -> List[Tuple[str, float]]:
        """
        分析主要影响因素 / Analyze Main Factors
        
        使用特征重要性分析来确定影响预测的主要因素
        Use feature importance analysis to determine main factors affecting prediction
        
        Args:
            signal: 交易信号 / Trading signal
            
        Returns:
            List[Tuple[str, float]]: 因素列表 [(因素名, 贡献度)] / Factor list [(factor_name, contribution)]
        """
        try:
            # 尝试从模型获取特征重要性
            # Try to get feature importance from model
            factors = self._get_feature_importance(signal)
            
            if factors:
                self._logger.debug(
                    f"从模型获取特征重要性 / Got feature importance from model: {len(factors)} factors"
                )
                return factors
            
            # 如果无法从模型获取，使用基于信号类型的启发式方法
            # If cannot get from model, use heuristic method based on signal type
            self._logger.debug(
                "使用启发式方法生成因素 / Using heuristic method to generate factors"
            )
            
            factors = []
            
            if signal.action == "buy":
                # 买入信号的主要因素
                # Main factors for buy signal
                factors = [
                    ("预测收益率 / Predicted return", 0.35),
                    ("动量指标 / Momentum", 0.25),
                    ("估值指标 / Valuation", 0.20),
                    ("成交量 / Volume", 0.15),
                    ("市场情绪 / Market sentiment", 0.05)
                ]
            elif signal.action == "sell":
                # 卖出信号的主要因素
                # Main factors for sell signal
                factors = [
                    ("预测收益率下降 / Predicted return decline", 0.40),
                    ("技术指标转弱 / Technical indicators weakening", 0.30),
                    ("风险指标上升 / Risk indicators rising", 0.20),
                    ("相对表现落后 / Relative performance lagging", 0.10)
                ]
            else:  # hold
                # 持有信号的主要因素
                # Main factors for hold signal
                factors = [
                    ("预测收益率稳定 / Predicted return stable", 0.35),
                    ("持仓表现良好 / Position performing well", 0.30),
                    ("风险可控 / Risk under control", 0.20),
                    ("市场环境适宜 / Market environment favorable", 0.15)
                ]
            
            return factors
            
        except Exception as e:
            self._logger.error(
                f"分析主要因素失败 / Failed to analyze main factors: {str(e)}",
                exc_info=True
            )
            # 返回默认因素
            # Return default factors
            return [("未知因素 / Unknown factor", 1.0)]
    
    def _get_feature_importance(
        self,
        signal: Signal
    ) -> Optional[List[Tuple[str, float]]]:
        """
        从模型获取特征重要性 / Get Feature Importance from Model
        
        尝试从模型中提取特征重要性信息
        Try to extract feature importance information from model
        
        Args:
            signal: 交易信号 / Trading signal
            
        Returns:
            Optional[List[Tuple[str, float]]]: 特征重要性列表或None / Feature importance list or None
        """
        try:
            # 这里需要根据实际使用的模型类型来获取特征重要性
            # Need to get feature importance based on actual model type used
            
            # 对于LightGBM模型
            # For LightGBM models
            # if hasattr(model, 'feature_importances_'):
            #     importances = model.feature_importances_
            #     feature_names = model.feature_name_
            #     return list(zip(feature_names, importances))
            
            # 对于其他模型，可能需要使用SHAP等工具
            # For other models, may need to use tools like SHAP
            
            # 当前返回None，使用启发式方法
            # Currently return None, use heuristic method
            return None
            
        except Exception as e:
            self._logger.debug(
                f"无法获取特征重要性 / Cannot get feature importance: {str(e)}"
            )
            return None
    
    def _assess_risk_level(
        self,
        signal: Signal
    ) -> str:
        """
        评估风险等级 / Assess Risk Level
        
        综合考虑置信度、分数、波动性等因素评估风险
        Assess risk considering confidence, score, volatility and other factors
        
        Args:
            signal: 交易信号 / Trading signal
            
        Returns:
            str: 风险等级 ("low", "medium", "high") / Risk level
        """
        try:
            risk_score = 0.0
            
            # 1. 基于置信度评估 (权重: 40%)
            # Assess based on confidence (weight: 40%)
            if signal.confidence >= 0.8:
                confidence_risk = 0.0  # 低风险 / Low risk
            elif signal.confidence >= 0.6:
                confidence_risk = 0.5  # 中等风险 / Medium risk
            else:
                confidence_risk = 1.0  # 高风险 / High risk
            
            risk_score += confidence_risk * 0.4
            
            # 2. 基于预测分数评估 (权重: 30%)
            # Assess based on prediction score (weight: 30%)
            abs_score = abs(signal.score)
            if abs_score >= 0.1:
                score_risk = 0.0  # 强信号，低风险 / Strong signal, low risk
            elif abs_score >= 0.05:
                score_risk = 0.5  # 中等信号，中等风险 / Medium signal, medium risk
            else:
                score_risk = 1.0  # 弱信号，高风险 / Weak signal, high risk
            
            risk_score += score_risk * 0.3
            
            # 3. 基于操作类型评估 (权重: 20%)
            # Assess based on action type (weight: 20%)
            if signal.action == "hold":
                action_risk = 0.0  # 持有风险最低 / Hold has lowest risk
            elif signal.action == "sell":
                action_risk = 0.3  # 卖出风险较低 / Sell has lower risk
            else:  # buy
                action_risk = 0.7  # 买入风险较高 / Buy has higher risk
            
            risk_score += action_risk * 0.2
            
            # 4. 基于市场条件评估 (权重: 10%)
            # Assess based on market conditions (weight: 10%)
            # 这里可以添加市场波动性、流动性等因素
            # Can add market volatility, liquidity and other factors here
            market_risk = 0.5  # 默认中等风险 / Default medium risk
            risk_score += market_risk * 0.1
            
            # 5. 综合评估
            # Comprehensive assessment
            if risk_score <= 0.3:
                risk_level = "low"
            elif risk_score <= 0.6:
                risk_level = "medium"
            else:
                risk_level = "high"
            
            self._logger.debug(
                f"风险评估完成 / Risk assessment completed\n"
                f"股票 / Stock: {signal.stock_code}\n"
                f"操作 / Action: {signal.action}\n"
                f"风险分数 / Risk score: {risk_score:.2f}\n"
                f"风险等级 / Risk level: {risk_level}"
            )
            
            return risk_level
            
        except Exception as e:
            self._logger.error(
                f"评估风险等级失败 / Failed to assess risk level: {str(e)}",
                exc_info=True
            )
            # 出错时返回高风险以保守处理
            # Return high risk when error occurs for conservative handling
            return "high"
    
    def _generate_signal_description(
        self,
        signal: Signal,
        main_factors: List[Tuple[str, float]],
        risk_level: str
    ) -> str:
        """
        生成信号描述 / Generate Signal Description
        
        生成通俗易懂的信号解释，包括风险警告
        Generate easy-to-understand signal explanation with risk warnings
        
        Args:
            signal: 交易信号 / Trading signal
            main_factors: 主要因素 / Main factors
            risk_level: 风险等级 / Risk level
            
        Returns:
            str: 信号描述 / Signal description
        """
        try:
            # 构建中英双语描述
            # Build bilingual description
            
            action_desc = {
                "buy": "买入 / Buy",
                "sell": "卖出 / Sell",
                "hold": "持有 / Hold"
            }
            
            risk_desc = {
                "low": "低风险 / Low risk",
                "medium": "中等风险 / Medium risk",
                "high": "高风险 / High risk"
            }
            
            # 1. 基本信息
            # Basic information
            description = (
                f"{'='*60}\n"
                f"交易信号解释 / Trading Signal Explanation\n"
                f"{'='*60}\n\n"
                f"📊 股票代码 / Stock Code: {signal.stock_code}\n"
                f"💡 建议操作 / Suggested Action: {action_desc.get(signal.action, signal.action)}\n"
                f"📈 预测分数 / Prediction Score: {signal.score:.4f}\n"
                f"🎯 置信度 / Confidence: {signal.confidence:.2%}\n"
                f"⚠️  风险等级 / Risk Level: {risk_desc.get(risk_level, risk_level)}\n"
            )
            
            # 2. 通俗语言解释
            # Plain language explanation
            description += f"\n{'='*60}\n"
            description += "📝 通俗解释 / Plain Language Explanation\n"
            description += f"{'='*60}\n\n"
            
            plain_explanation = self._generate_plain_explanation(signal, risk_level)
            description += plain_explanation + "\n"
            
            # 3. 主要影响因素
            # Main factors
            description += f"\n{'='*60}\n"
            description += "🔍 主要影响因素 / Main Factors\n"
            description += f"{'='*60}\n\n"
            
            for i, (factor, contribution) in enumerate(main_factors[:5], 1):
                # 使用进度条显示贡献度
                # Use progress bar to show contribution
                bar_length = int(contribution * 20)
                bar = "█" * bar_length + "░" * (20 - bar_length)
                description += f"{i}. {factor}\n"
                description += f"   {bar} {contribution:.1%}\n\n"
            
            # 4. 风险警告（如果是高风险）
            # Risk warning (if high risk)
            if risk_level == "high":
                description += f"\n{'='*60}\n"
                description += "⚠️  风险警告 / Risk Warning\n"
                description += f"{'='*60}\n\n"
                
                warnings = self._generate_risk_warnings(signal, risk_level)
                for warning in warnings:
                    description += f"⚠️  {warning}\n"
                description += "\n"
            
            # 5. 操作建议
            # Action suggestions
            description += f"\n{'='*60}\n"
            description += "💼 操作建议 / Action Suggestions\n"
            description += f"{'='*60}\n\n"
            
            suggestions = self._generate_action_suggestions(signal, risk_level)
            for suggestion in suggestions:
                description += f"✓ {suggestion}\n"
            
            # 6. 原因说明
            # Reason explanation
            if signal.reason:
                description += f"\n{'='*60}\n"
                description += "📋 详细原因 / Detailed Reason\n"
                description += f"{'='*60}\n\n"
                description += f"{signal.reason}\n"
            
            description += f"\n{'='*60}\n"
            
            return description
            
        except Exception as e:
            self._logger.error(
                f"生成信号描述失败 / Failed to generate signal description: {str(e)}",
                exc_info=True
            )
            # 返回简化描述
            # Return simplified description
            return (
                f"信号 / Signal: {signal.action} {signal.stock_code}\n"
                f"分数 / Score: {signal.score:.4f}\n"
                f"置信度 / Confidence: {signal.confidence:.2%}"
            )
    
    def _generate_plain_explanation(
        self,
        signal: Signal,
        risk_level: str
    ) -> str:
        """
        生成通俗语言解释 / Generate Plain Language Explanation
        
        将技术指标转换为通俗易懂的语言
        Convert technical indicators to plain language
        
        Args:
            signal: 交易信号 / Trading signal
            risk_level: 风险等级 / Risk level
            
        Returns:
            str: 通俗解释 / Plain explanation
        """
        try:
            explanations = []
            
            if signal.action == "buy":
                # 买入信号的通俗解释
                # Plain explanation for buy signal
                if signal.confidence >= 0.8:
                    explanations.append(
                        "根据我们的分析模型，这只股票在未来一段时间内有较大概率上涨。\n"
                        "According to our analysis model, this stock has a high probability of rising in the near future."
                    )
                else:
                    explanations.append(
                        "模型预测这只股票可能会上涨，但信号强度一般，建议谨慎考虑。\n"
                        "The model predicts this stock may rise, but the signal strength is moderate, suggest careful consideration."
                    )
                
                if risk_level == "low":
                    explanations.append(
                        "从风险角度看，这是一个相对安全的买入机会。\n"
                        "From a risk perspective, this is a relatively safe buying opportunity."
                    )
                elif risk_level == "high":
                    explanations.append(
                        "⚠️ 注意：虽然有买入信号，但风险较高，建议控制仓位。\n"
                        "⚠️ Note: Although there is a buy signal, the risk is high, suggest controlling position size."
                    )
                
            elif signal.action == "sell":
                # 卖出信号的通俗解释
                # Plain explanation for sell signal
                if signal.confidence >= 0.8:
                    explanations.append(
                        "模型分析显示这只股票的上涨动力正在减弱，建议考虑卖出以锁定收益或减少损失。\n"
                        "Model analysis shows the upward momentum of this stock is weakening, suggest considering selling to lock in profits or reduce losses."
                    )
                else:
                    explanations.append(
                        "这只股票的表现可能不如预期，可以考虑卖出，但信号强度一般。\n"
                        "This stock's performance may not meet expectations, can consider selling, but signal strength is moderate."
                    )
                
                if hasattr(signal, 'quantity') and signal.quantity:
                    explanations.append(
                        f"建议卖出数量：{signal.quantity}股\n"
                        f"Suggested sell quantity: {signal.quantity} shares"
                    )
                
            else:  # hold
                # 持有信号的通俗解释
                # Plain explanation for hold signal
                explanations.append(
                    "当前这只股票表现稳定，建议继续持有，暂时不需要调整仓位。\n"
                    "This stock is currently performing steadily, suggest continuing to hold, no need to adjust position for now."
                )
                
                if signal.confidence >= 0.8:
                    explanations.append(
                        "模型对持有策略有较高信心，可以安心持有。\n"
                        "The model has high confidence in the hold strategy, can hold with confidence."
                    )
            
            return "\n".join(explanations)
            
        except Exception as e:
            self._logger.error(
                f"生成通俗解释失败 / Failed to generate plain explanation: {str(e)}"
            )
            return "无法生成详细解释 / Cannot generate detailed explanation"
    
    def _generate_risk_warnings(
        self,
        signal: Signal,
        risk_level: str
    ) -> List[str]:
        """
        生成风险警告 / Generate Risk Warnings
        
        Args:
            signal: 交易信号 / Trading signal
            risk_level: 风险等级 / Risk level
            
        Returns:
            List[str]: 风险警告列表 / List of risk warnings
        """
        warnings = []
        
        try:
            if risk_level == "high":
                # 高风险警告
                # High risk warnings
                warnings.append(
                    "该信号的置信度较低，预测准确性可能不高。\n"
                    "The confidence of this signal is low, prediction accuracy may not be high."
                )
                
                if signal.action == "buy":
                    warnings.append(
                        "买入高风险股票可能导致较大损失，建议严格控制仓位（不超过总资金的5-10%）。\n"
                        "Buying high-risk stocks may lead to significant losses, suggest strictly controlling position size (no more than 5-10% of total capital)."
                    )
                    warnings.append(
                        "建议设置止损点，如果股价下跌超过5-8%，及时止损。\n"
                        "Suggest setting stop-loss point, if stock price falls more than 5-8%, cut losses in time."
                    )
                
                warnings.append(
                    "市场波动可能较大，请密切关注市场动态和个股表现。\n"
                    "Market volatility may be high, please closely monitor market dynamics and individual stock performance."
                )
                
                warnings.append(
                    "建议在做出决策前，结合其他分析工具和市场信息进行综合判断。\n"
                    "Suggest combining other analysis tools and market information for comprehensive judgment before making decisions."
                )
            
            elif risk_level == "medium":
                # 中等风险提示
                # Medium risk reminders
                warnings.append(
                    "该信号存在一定不确定性，建议适度控制仓位。\n"
                    "This signal has some uncertainty, suggest moderately controlling position size."
                )
                
                if signal.action == "buy":
                    warnings.append(
                        "建议分批买入，避免一次性投入过多资金。\n"
                        "Suggest buying in batches, avoid investing too much capital at once."
                    )
            
            return warnings
            
        except Exception as e:
            self._logger.error(
                f"生成风险警告失败 / Failed to generate risk warnings: {str(e)}"
            )
            return ["请谨慎操作 / Please operate cautiously"]
    
    def _generate_action_suggestions(
        self,
        signal: Signal,
        risk_level: str
    ) -> List[str]:
        """
        生成操作建议 / Generate Action Suggestions
        
        Args:
            signal: 交易信号 / Trading signal
            risk_level: 风险等级 / Risk level
            
        Returns:
            List[str]: 操作建议列表 / List of action suggestions
        """
        suggestions = []
        
        try:
            if signal.action == "buy":
                # 买入建议
                # Buy suggestions
                if risk_level == "low":
                    suggestions.append(
                        "可以考虑按计划仓位买入（建议10-20%的资金）。\n"
                        "Can consider buying according to planned position size (suggest 10-20% of capital)."
                    )
                elif risk_level == "medium":
                    suggestions.append(
                        "建议适度买入（建议5-15%的资金），并设置止损点。\n"
                        "Suggest moderate buying (suggest 5-15% of capital) and set stop-loss point."
                    )
                else:  # high
                    suggestions.append(
                        "如果决定买入，建议小仓位试探（不超过5%的资金）。\n"
                        "If deciding to buy, suggest small position testing (no more than 5% of capital)."
                    )
                
                suggestions.append(
                    "买入后密切关注股价变化，及时调整策略。\n"
                    "After buying, closely monitor stock price changes and adjust strategy in time."
                )
                
                if hasattr(signal, 'target_weight') and signal.target_weight:
                    suggestions.append(
                        f"建议目标仓位：{signal.target_weight:.1f}%\n"
                        f"Suggested target position: {signal.target_weight:.1f}%"
                    )
                
            elif signal.action == "sell":
                # 卖出建议
                # Sell suggestions
                if signal.confidence >= 0.8:
                    suggestions.append(
                        "建议尽快卖出，避免进一步损失或锁定已有收益。\n"
                        "Suggest selling as soon as possible to avoid further losses or lock in existing profits."
                    )
                else:
                    suggestions.append(
                        "可以考虑分批卖出，先卖出部分仓位观察市场反应。\n"
                        "Can consider selling in batches, sell part of position first to observe market reaction."
                    )
                
                suggestions.append(
                    "卖出后可以将资金转向更有潜力的标的。\n"
                    "After selling, can redirect capital to more promising targets."
                )
                
            else:  # hold
                # 持有建议
                # Hold suggestions
                suggestions.append(
                    "继续持有当前仓位，保持耐心等待更好的买卖时机。\n"
                    "Continue holding current position, be patient and wait for better buying/selling opportunities."
                )
                
                suggestions.append(
                    "定期检查持仓表现，如果出现明显的买入或卖出信号，及时调整。\n"
                    "Regularly check position performance, adjust in time if clear buy or sell signals appear."
                )
                
                if risk_level == "low":
                    suggestions.append(
                        "当前持仓风险较低，可以安心持有。\n"
                        "Current position risk is low, can hold with confidence."
                    )
            
            # 通用建议
            # General suggestions
            suggestions.append(
                "投资有风险，决策需谨慎。建议结合自身风险承受能力做出最终决定。\n"
                "Investment involves risks, decisions need to be cautious. Suggest making final decision based on your own risk tolerance."
            )
            
            return suggestions
            
        except Exception as e:
            self._logger.error(
                f"生成操作建议失败 / Failed to generate action suggestions: {str(e)}"
            )
            return ["请根据实际情况谨慎操作 / Please operate cautiously based on actual situation"]
    
    def set_risk_limits(self, risk_limits: RiskLimits) -> None:
        """
        设置风险限制 / Set Risk Limits
        
        Args:
            risk_limits: 新的风险限制 / New risk limits
        """
        self._risk_limits = risk_limits
        self._logger.info(
            f"风险限制已更新 / Risk limits updated\n"
            f"最大持仓比例 / Max position size: {self._risk_limits.max_position_size:.1%}\n"
            f"单只股票最大权重 / Max single stock: {self._risk_limits.max_single_stock:.1%}\n"
            f"最小现金储备 / Min cash reserve: {self._risk_limits.min_cash_reserve:.1%}"
        )
    
    def get_risk_limits(self) -> RiskLimits:
        """
        获取当前风险限制 / Get Current Risk Limits
        
        Returns:
            RiskLimits: 当前风险限制 / Current risk limits
        """
        return self._risk_limits
    
    def get_detailed_signal_analysis(
        self,
        signal: Signal
    ) -> Dict[str, Any]:
        """
        获取详细的信号分析 / Get Detailed Signal Analysis
        
        提供信号的完整分析，包括特征重要性、风险评估和操作建议
        Provide complete signal analysis including feature importance, risk assessment and action suggestions
        
        Args:
            signal: 交易信号 / Trading signal
            
        Returns:
            Dict[str, Any]: 详细分析结果 / Detailed analysis results
        """
        try:
            self._logger.info(
                f"生成详细信号分析 / Generating detailed signal analysis\n"
                f"股票 / Stock: {signal.stock_code}\n"
                f"操作 / Action: {signal.action}"
            )
            
            # 1. 获取信号解释
            # Get signal explanation
            explanation = self.explain_signal(signal)
            
            # 2. 生成风险警告
            # Generate risk warnings
            warnings = self._generate_risk_warnings(signal, explanation.risk_level)
            
            # 3. 生成操作建议
            # Generate action suggestions
            suggestions = self._generate_action_suggestions(signal, explanation.risk_level)
            
            # 4. 生成通俗解释
            # Generate plain explanation
            plain_explanation = self._generate_plain_explanation(signal, explanation.risk_level)
            
            # 5. 组装完整分析
            # Assemble complete analysis
            analysis = {
                "signal": {
                    "stock_code": signal.stock_code,
                    "action": signal.action,
                    "score": signal.score,
                    "confidence": signal.confidence,
                    "timestamp": signal.timestamp,
                    "quantity": getattr(signal, 'quantity', None),
                    "target_weight": getattr(signal, 'target_weight', None),
                    "reason": signal.reason
                },
                "risk_assessment": {
                    "risk_level": explanation.risk_level,
                    "risk_score": self._calculate_risk_score(signal, explanation.risk_level),
                    "warnings": warnings
                },
                "feature_importance": {
                    "main_factors": explanation.main_factors,
                    "top_factor": explanation.main_factors[0] if explanation.main_factors else None
                },
                "explanations": {
                    "plain_language": plain_explanation,
                    "detailed_description": explanation.description
                },
                "recommendations": {
                    "action_suggestions": suggestions,
                    "position_sizing": self._get_position_sizing_recommendation(signal, explanation.risk_level),
                    "stop_loss": self._get_stop_loss_recommendation(signal, explanation.risk_level)
                },
                "metadata": {
                    "analysis_timestamp": datetime.now().isoformat(),
                    "model_confidence": signal.confidence,
                    "signal_strength": "strong" if signal.confidence >= 0.8 else "moderate" if signal.confidence >= 0.6 else "weak"
                }
            }
            
            self._logger.info(
                f"详细信号分析完成 / Detailed signal analysis completed\n"
                f"风险等级 / Risk level: {explanation.risk_level}\n"
                f"信号强度 / Signal strength: {analysis['metadata']['signal_strength']}"
            )
            
            return analysis
            
        except Exception as e:
            error_msg = f"生成详细信号分析失败 / Failed to generate detailed signal analysis: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise SignalGeneratorError(error_msg) from e
    
    def _calculate_risk_score(
        self,
        signal: Signal,
        risk_level: str
    ) -> float:
        """
        计算风险分数 / Calculate Risk Score
        
        Args:
            signal: 交易信号 / Trading signal
            risk_level: 风险等级 / Risk level
            
        Returns:
            float: 风险分数 (0-1) / Risk score (0-1)
        """
        risk_mapping = {
            "low": 0.2,
            "medium": 0.5,
            "high": 0.8
        }
        
        base_risk = risk_mapping.get(risk_level, 0.5)
        
        # 根据置信度调整
        # Adjust based on confidence
        confidence_adjustment = (1 - signal.confidence) * 0.2
        
        return min(1.0, max(0.0, base_risk + confidence_adjustment))
    
    def _get_position_sizing_recommendation(
        self,
        signal: Signal,
        risk_level: str
    ) -> Dict[str, Any]:
        """
        获取仓位建议 / Get Position Sizing Recommendation
        
        Args:
            signal: 交易信号 / Trading signal
            risk_level: 风险等级 / Risk level
            
        Returns:
            Dict[str, Any]: 仓位建议 / Position sizing recommendation
        """
        if signal.action == "buy":
            if risk_level == "low":
                return {
                    "min_percentage": 10.0,
                    "max_percentage": 20.0,
                    "recommended_percentage": 15.0,
                    "description": "低风险，可以适度配置 / Low risk, can allocate moderately"
                }
            elif risk_level == "medium":
                return {
                    "min_percentage": 5.0,
                    "max_percentage": 15.0,
                    "recommended_percentage": 10.0,
                    "description": "中等风险，建议适度配置 / Medium risk, suggest moderate allocation"
                }
            else:  # high
                return {
                    "min_percentage": 2.0,
                    "max_percentage": 5.0,
                    "recommended_percentage": 3.0,
                    "description": "高风险，建议小仓位试探 / High risk, suggest small position testing"
                }
        elif signal.action == "sell":
            return {
                "sell_percentage": 100.0 if signal.confidence >= 0.8 else 50.0,
                "description": "建议卖出比例 / Suggested sell percentage"
            }
        else:  # hold
            return {
                "action": "maintain",
                "description": "保持当前仓位 / Maintain current position"
            }
    
    def _get_stop_loss_recommendation(
        self,
        signal: Signal,
        risk_level: str
    ) -> Dict[str, Any]:
        """
        获取止损建议 / Get Stop Loss Recommendation
        
        Args:
            signal: 交易信号 / Trading signal
            risk_level: 风险等级 / Risk level
            
        Returns:
            Dict[str, Any]: 止损建议 / Stop loss recommendation
        """
        if signal.action == "buy":
            if risk_level == "low":
                return {
                    "stop_loss_percentage": 8.0,
                    "description": "建议止损点：-8% / Suggested stop loss: -8%"
                }
            elif risk_level == "medium":
                return {
                    "stop_loss_percentage": 6.0,
                    "description": "建议止损点：-6% / Suggested stop loss: -6%"
                }
            else:  # high
                return {
                    "stop_loss_percentage": 5.0,
                    "description": "建议止损点：-5%（严格执行）/ Suggested stop loss: -5% (strictly enforce)"
                }
        else:
            return {
                "description": "不适用 / Not applicable"
            }
