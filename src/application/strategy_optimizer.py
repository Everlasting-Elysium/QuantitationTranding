"""
Strategy Optimizer for the qlib trading system.
策略优化器

This module provides functionality to optimize trading strategies based on
target returns and risk preferences.
本模块提供基于目标收益率和风险偏好优化交易策略的功能。
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from scipy.optimize import minimize
from pathlib import Path

from ..models.market_models import (
    OptimizationConstraints, OptimizedStrategy, StrategyParams,
    AssetMetrics, AssetRecommendation
)
from ..infrastructure.logger_system import LoggerSystem
from ..application.performance_analyzer import PerformanceAnalyzer
from ..utils.error_handler import DataError, ErrorInfo, ErrorCategory, ErrorSeverity


class StrategyOptimizer:
    """
    Strategy optimizer for optimizing trading strategies.
    用于优化交易策略的策略优化器
    
    This class handles:
    - Validating target returns against historical data
    - Multi-objective optimization balancing returns and risk
    - Adjusting parameters based on risk preferences
    - Generating optimized asset allocations
    
    本类处理：
    - 根据历史数据验证目标收益率
    - 平衡收益和风险的多目标优化
    - 根据风险偏好调整参数
    - 生成优化的资产配置
    """
    
    def __init__(
        self,
        performance_analyzer: Optional[PerformanceAnalyzer] = None
    ):
        """
        Initialize the strategy optimizer.
        初始化策略优化器
        
        Args:
            performance_analyzer: PerformanceAnalyzer instance for historical analysis
                                  用于历史分析的PerformanceAnalyzer实例
        """
        logger_system = LoggerSystem()
        self.logger = logger_system.get_logger(__name__)
        self.performance_analyzer = performance_analyzer or PerformanceAnalyzer()
        
        # Risk-free rate for optimization
        # 用于优化的无风险利率
        self.risk_free_rate = 0.03  # 3% default
        
        self.logger.info("StrategyOptimizer initialized")
        self.logger.info("策略优化器已初始化")
    
    def optimize_for_target_return(
        self,
        target_return: float,
        assets: List[str],
        constraints: OptimizationConstraints,
        historical_data: Optional[Dict[str, AssetMetrics]] = None
    ) -> OptimizedStrategy:
        """
        Optimize strategy to achieve target return while managing risk.
        优化策略以在管理风险的同时实现目标收益率
        
        Args:
            target_return: Target annual return (e.g., 0.15 for 15%)
                           目标年化收益率（例如，0.15表示15%）
            assets: List of asset symbols to include in portfolio
                    投资组合中包含的资产代码列表
            constraints: Optimization constraints
                         优化约束条件
            historical_data: Optional pre-computed historical metrics
                             可选的预计算历史指标
        
        Returns:
            OptimizedStrategy: Optimized strategy with asset allocation
                               带有资产配置的优化策略
        
        Raises:
            DataError: If optimization fails
                      如果优化失败
        """
        try:
            self.logger.info(
                f"Starting strategy optimization / 开始策略优化\n"
                f"Target return: {target_return:.2%} / 目标收益率: {target_return:.2%}\n"
                f"Assets: {len(assets)} / 资产数量: {len(assets)}\n"
                f"Risk tolerance: {constraints.risk_tolerance} / 风险偏好: {constraints.risk_tolerance}"
            )
            
            # Step 1: Validate target return
            # 步骤1：验证目标收益率
            validation_result = self._validate_target_return(
                target_return, assets, historical_data
            )
            
            if not validation_result["feasible"]:
                self.logger.warning(
                    f"Target return may not be feasible / 目标收益率可能不可行: "
                    f"{validation_result['message']}"
                )
            
            # Step 2: Get historical metrics for assets
            # 步骤2：获取资产的历史指标
            if historical_data is None:
                historical_data = self._get_historical_metrics(assets)
            
            # Step 3: Perform multi-objective optimization
            # 步骤3：执行多目标优化
            optimal_weights = self._optimize_portfolio(
                target_return=target_return,
                historical_data=historical_data,
                constraints=constraints
            )
            
            # Step 4: Calculate expected metrics
            # 步骤4：计算预期指标
            expected_return, expected_risk = self._calculate_portfolio_metrics(
                optimal_weights, historical_data
            )
            
            # Step 5: Generate strategy parameters
            # 步骤5：生成策略参数
            strategy_params = self._generate_strategy_params(
                constraints, historical_data
            )
            
            # Step 6: Calculate optimization score
            # 步骤6：计算优化评分
            optimization_score = self._calculate_optimization_score(
                target_return, expected_return, expected_risk, constraints
            )
            
            # Step 7: Generate warnings if needed
            # 步骤7：如果需要生成警告
            warnings = self._generate_warnings(
                target_return, expected_return, expected_risk,
                optimal_weights, constraints
            )
            
            # Create optimized strategy
            # 创建优化策略
            strategy_id = f"opt_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            strategy = OptimizedStrategy(
                strategy_id=strategy_id,
                target_return=target_return,
                expected_return=expected_return,
                expected_risk=expected_risk,
                asset_weights=optimal_weights,
                rebalance_frequency=self._get_rebalance_frequency(constraints),
                parameters=strategy_params,
                optimization_score=optimization_score,
                feasible=validation_result["feasible"],
                warnings=warnings
            )
            
            self.logger.info(
                f"Strategy optimization completed / 策略优化完成\n"
                f"Expected return: {expected_return:.2%} / 预期收益率: {expected_return:.2%}\n"
                f"Expected risk: {expected_risk:.2%} / 预期风险: {expected_risk:.2%}\n"
                f"Optimization score: {optimization_score:.2f} / 优化评分: {optimization_score:.2f}\n"
                f"Feasible: {strategy.feasible} / 可行: {strategy.feasible}"
            )
            
            return strategy
            
        except Exception as e:
            error_info = ErrorInfo(
                error_code="OPT0001",
                error_message_zh=f"策略优化失败: {str(e)}",
                error_message_en=f"Strategy optimization failed: {str(e)}",
                category=ErrorCategory.DATA,
                severity=ErrorSeverity.HIGH,
                technical_details=str(e),
                suggested_actions=[
                    "检查目标收益率是否合理",
                    "确认资产列表是否有效",
                    "验证约束条件是否正确",
                    "查看详细日志了解错误原因"
                ],
                recoverable=True,
                original_exception=e
            )
            self.logger.error(error_info.get_user_message(), exc_info=True)
            raise DataError(error_info)

    
    def suggest_parameters(
        self,
        target_return: float,
        risk_tolerance: str
    ) -> StrategyParams:
        """
        Suggest strategy parameters based on target return and risk tolerance.
        根据目标收益率和风险承受能力建议策略参数
        
        Args:
            target_return: Target annual return
                           目标年化收益率
            risk_tolerance: Risk tolerance level
                            风险承受能力
        
        Returns:
            StrategyParams: Suggested strategy parameters
                            建议的策略参数
        
        Raises:
            DataError: If parameter suggestion fails
                      如果参数建议失败
        """
        try:
            self.logger.info(
                f"Suggesting parameters / 建议参数\n"
                f"Target return: {target_return:.2%} / 目标收益率: {target_return:.2%}\n"
                f"Risk tolerance: {risk_tolerance} / 风险承受能力: {risk_tolerance}"
            )
            
            # Determine model type based on target return and risk tolerance
            # 根据目标收益率和风险承受能力确定模型类型
            model_type = self._select_model_type(target_return, risk_tolerance)
            
            # Determine features based on model type
            # 根据模型类型确定特征
            features = self._select_features(model_type, risk_tolerance)
            
            # Determine lookback period
            # 确定回溯期
            lookback_period = self._select_lookback_period(risk_tolerance)
            
            # Determine rebalance frequency
            # 确定再平衡频率
            rebalance_frequency = self._select_rebalance_frequency(risk_tolerance)
            
            # Determine position sizing method
            # 确定仓位管理方法
            position_sizing = self._select_position_sizing(risk_tolerance)
            
            # Generate risk parameters
            # 生成风险参数
            risk_params = self._generate_risk_params(target_return, risk_tolerance)
            
            params = StrategyParams(
                model_type=model_type,
                features=features,
                lookback_period=lookback_period,
                rebalance_frequency=rebalance_frequency,
                position_sizing=position_sizing,
                risk_params=risk_params
            )
            
            self.logger.info(
                f"Parameters suggested / 参数已建议\n"
                f"Model type: {model_type} / 模型类型: {model_type}\n"
                f"Features: {len(features)} / 特征数量: {len(features)}\n"
                f"Lookback: {lookback_period} days / 回溯期: {lookback_period}天"
            )
            
            return params
            
        except Exception as e:
            error_info = ErrorInfo(
                error_code="OPT0002",
                error_message_zh=f"参数建议失败: {str(e)}",
                error_message_en=f"Parameter suggestion failed: {str(e)}",
                category=ErrorCategory.DATA,
                severity=ErrorSeverity.MEDIUM,
                technical_details=str(e),
                suggested_actions=[
                    "检查目标收益率是否合理",
                    "验证风险承受能力设置",
                    "查看日志了解详细错误"
                ],
                recoverable=True,
                original_exception=e
            )
            self.logger.error(error_info.get_user_message(), exc_info=True)
            raise DataError(error_info)
    
    def _validate_target_return(
        self,
        target_return: float,
        assets: List[str],
        historical_data: Optional[Dict[str, AssetMetrics]] = None
    ) -> Dict[str, any]:
        """
        Validate if target return is achievable based on historical data.
        根据历史数据验证目标收益率是否可实现
        
        Args:
            target_return: Target annual return
                           目标年化收益率
            assets: List of asset symbols
                    资产代码列表
            historical_data: Optional historical metrics
                             可选的历史指标
        
        Returns:
            Dict: Validation result with feasibility and message
                  包含可行性和消息的验证结果
        """
        try:
            # Get historical metrics if not provided
            # 如果未提供则获取历史指标
            if historical_data is None:
                historical_data = self._get_historical_metrics(assets)
            
            if not historical_data:
                return {
                    "feasible": False,
                    "message": "无法获取历史数据 / Unable to get historical data"
                }
            
            # Calculate maximum historical return
            # 计算最大历史收益率
            max_return = max(
                metrics.annual_return for metrics in historical_data.values()
            )
            
            # Calculate average historical return
            # 计算平均历史收益率
            avg_return = np.mean([
                metrics.annual_return for metrics in historical_data.values()
            ])
            
            # Check feasibility
            # 检查可行性
            if target_return > max_return * 1.5:
                return {
                    "feasible": False,
                    "message": (
                        f"目标收益率{target_return:.2%}远高于历史最高{max_return:.2%} / "
                        f"Target return {target_return:.2%} far exceeds historical max {max_return:.2%}"
                    )
                }
            elif target_return > max_return:
                return {
                    "feasible": True,
                    "message": (
                        f"目标收益率{target_return:.2%}高于历史最高{max_return:.2%}，具有挑战性 / "
                        f"Target return {target_return:.2%} exceeds historical max {max_return:.2%}, challenging"
                    )
                }
            elif target_return > avg_return * 1.5:
                return {
                    "feasible": True,
                    "message": (
                        f"目标收益率{target_return:.2%}高于历史平均{avg_return:.2%}，需要优化 / "
                        f"Target return {target_return:.2%} above historical average {avg_return:.2%}, needs optimization"
                    )
                }
            else:
                return {
                    "feasible": True,
                    "message": (
                        f"目标收益率{target_return:.2%}合理，历史平均为{avg_return:.2%} / "
                        f"Target return {target_return:.2%} reasonable, historical average {avg_return:.2%}"
                    )
                }
                
        except Exception as e:
            self.logger.warning(
                f"Target return validation failed / 目标收益率验证失败: {str(e)}"
            )
            return {
                "feasible": True,
                "message": f"无法验证目标收益率 / Unable to validate target return: {str(e)}"
            }

    
    def _get_historical_metrics(
        self,
        assets: List[str],
        lookback_years: int = 3
    ) -> Dict[str, AssetMetrics]:
        """
        Get historical metrics for assets.
        获取资产的历史指标
        
        Args:
            assets: List of asset symbols
                    资产代码列表
            lookback_years: Years of historical data to analyze
                            要分析的历史数据年数
        
        Returns:
            Dict[str, AssetMetrics]: Historical metrics by asset
                                     按资产分类的历史指标
        """
        from datetime import datetime, timedelta
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=lookback_years * 365)
        
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        historical_data = {}
        for asset in assets:
            try:
                metrics = self.performance_analyzer.get_asset_metrics(
                    asset, start_date_str, end_date_str
                )
                if metrics:
                    historical_data[asset] = metrics
            except Exception as e:
                self.logger.warning(
                    f"Failed to get metrics for {asset}: {str(e)} / "
                    f"获取{asset}的指标失败: {str(e)}"
                )
                continue
        
        return historical_data
    
    def _optimize_portfolio(
        self,
        target_return: float,
        historical_data: Dict[str, AssetMetrics],
        constraints: OptimizationConstraints
    ) -> Dict[str, float]:
        """
        Optimize portfolio weights using multi-objective optimization.
        使用多目标优化来优化投资组合权重
        
        Args:
            target_return: Target annual return
                           目标年化收益率
            historical_data: Historical metrics for assets
                             资产的历史指标
            constraints: Optimization constraints
                         优化约束条件
        
        Returns:
            Dict[str, float]: Optimal asset weights
                              最优资产权重
        """
        assets = list(historical_data.keys())
        n_assets = len(assets)
        
        if n_assets == 0:
            raise ValueError("No assets available for optimization / 没有可用于优化的资产")
        
        # Extract returns and risks
        # 提取收益率和风险
        returns = np.array([historical_data[asset].annual_return for asset in assets])
        risks = np.array([historical_data[asset].volatility for asset in assets])
        
        # Calculate correlation matrix (simplified: assume some correlation)
        # 计算相关性矩阵（简化：假设一些相关性）
        correlation = np.full((n_assets, n_assets), 0.3)
        np.fill_diagonal(correlation, 1.0)
        
        # Calculate covariance matrix
        # 计算协方差矩阵
        cov_matrix = np.outer(risks, risks) * correlation
        
        # Define objective function (minimize risk for given return)
        # 定义目标函数（在给定收益率下最小化风险）
        def objective(weights):
            portfolio_return = np.dot(weights, returns)
            portfolio_risk = np.sqrt(np.dot(weights, np.dot(cov_matrix, weights)))
            
            # Multi-objective: balance return and risk
            # 多目标：平衡收益和风险
            # Penalize deviation from target return
            # 惩罚偏离目标收益率
            return_penalty = abs(portfolio_return - target_return) * 10
            
            # Adjust risk penalty based on risk tolerance
            # 根据风险承受能力调整风险惩罚
            risk_multiplier = self._get_risk_multiplier(constraints.risk_tolerance)
            risk_penalty = portfolio_risk * risk_multiplier
            
            return return_penalty + risk_penalty
        
        # Define constraints
        # 定义约束条件
        cons = [
            # Weights sum to 1
            # 权重总和为1
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0},
            # Minimum diversification (at least min_diversification assets with weight > 0.01)
            # 最小分散化（至少min_diversification个资产权重 > 0.01）
            {'type': 'ineq', 'fun': lambda w: np.sum(w > 0.01) - constraints.min_diversification}
        ]
        
        # Define bounds
        # 定义边界
        bounds = [(0, constraints.max_position_size) for _ in range(n_assets)]
        
        # Initial guess: equal weights
        # 初始猜测：等权重
        x0 = np.ones(n_assets) / n_assets
        
        # Optimize
        # 优化
        result = minimize(
            objective,
            x0,
            method='SLSQP',
            bounds=bounds,
            constraints=cons,
            options={'maxiter': 1000}
        )
        
        if not result.success:
            self.logger.warning(
                f"Optimization did not converge: {result.message} / "
                f"优化未收敛: {result.message}"
            )
        
        # Convert to dictionary
        # 转换为字典
        optimal_weights = {
            asset: float(weight)
            for asset, weight in zip(assets, result.x)
            if weight > 0.001  # Filter out very small weights
        }
        
        # Normalize weights to sum to 1
        # 标准化权重使其总和为1
        total_weight = sum(optimal_weights.values())
        optimal_weights = {
            asset: weight / total_weight
            for asset, weight in optimal_weights.items()
        }
        
        return optimal_weights
    
    def _calculate_portfolio_metrics(
        self,
        weights: Dict[str, float],
        historical_data: Dict[str, AssetMetrics]
    ) -> Tuple[float, float]:
        """
        Calculate expected return and risk for portfolio.
        计算投资组合的预期收益率和风险
        
        Args:
            weights: Asset weights
                     资产权重
            historical_data: Historical metrics
                             历史指标
        
        Returns:
            Tuple[float, float]: (expected_return, expected_risk)
                                 (预期收益率, 预期风险)
        """
        # Calculate weighted return
        # 计算加权收益率
        expected_return = sum(
            weights[asset] * historical_data[asset].annual_return
            for asset in weights.keys()
        )
        
        # Calculate portfolio risk (simplified)
        # 计算投资组合风险（简化）
        # Assume some correlation between assets
        # 假设资产之间存在一些相关性
        weighted_risks = [
            weights[asset] * historical_data[asset].volatility
            for asset in weights.keys()
        ]
        
        # Simplified risk calculation (assumes 0.5 correlation)
        # 简化的风险计算（假设0.5相关性）
        expected_risk = np.sqrt(sum(r**2 for r in weighted_risks) * 1.5)
        
        return expected_return, expected_risk

    
    def _generate_strategy_params(
        self,
        constraints: OptimizationConstraints,
        historical_data: Dict[str, AssetMetrics]
    ) -> Dict[str, any]:
        """
        Generate strategy parameters based on constraints and historical data.
        根据约束条件和历史数据生成策略参数
        
        Args:
            constraints: Optimization constraints
                         优化约束条件
            historical_data: Historical metrics
                             历史指标
        
        Returns:
            Dict: Strategy parameters
                  策略参数
        """
        # Determine model type based on risk tolerance
        # 根据风险承受能力确定模型类型
        model_type_map = {
            "conservative": "linear",
            "moderate": "lgbm",
            "aggressive": "mlp"
        }
        model_type = model_type_map.get(constraints.risk_tolerance, "lgbm")
        
        # Generate parameters
        # 生成参数
        params = {
            "model_type": model_type,
            "max_position_size": constraints.max_position_size,
            "max_sector_exposure": constraints.max_sector_exposure,
            "min_diversification": constraints.min_diversification,
            "max_turnover": constraints.max_turnover,
            "risk_tolerance": constraints.risk_tolerance,
            "rebalance_frequency": self._get_rebalance_frequency(constraints),
            "stop_loss": self._get_stop_loss(constraints.risk_tolerance),
            "take_profit": self._get_take_profit(constraints.risk_tolerance)
        }
        
        return params
    
    def _calculate_optimization_score(
        self,
        target_return: float,
        expected_return: float,
        expected_risk: float,
        constraints: OptimizationConstraints
    ) -> float:
        """
        Calculate overall optimization score (0-100).
        计算综合优化评分（0-100）
        
        Args:
            target_return: Target return
                           目标收益率
            expected_return: Expected return
                             预期收益率
            expected_risk: Expected risk
                           预期风险
            constraints: Optimization constraints
                         优化约束条件
        
        Returns:
            float: Optimization score
                   优化评分
        """
        # Score based on how close we are to target return
        # 基于我们与目标收益率的接近程度评分
        return_diff = abs(expected_return - target_return)
        return_score = max(0, 50 - return_diff * 100)  # Max 50 points
        
        # Score based on risk-adjusted return (Sharpe ratio)
        # 基于风险调整后收益率（夏普比率）评分
        sharpe = (expected_return - self.risk_free_rate) / expected_risk if expected_risk > 0 else 0
        sharpe_score = min(sharpe * 20, 50)  # Max 50 points
        
        total_score = return_score + sharpe_score
        
        return min(100, max(0, total_score))
    
    def _generate_warnings(
        self,
        target_return: float,
        expected_return: float,
        expected_risk: float,
        weights: Dict[str, float],
        constraints: OptimizationConstraints
    ) -> List[str]:
        """
        Generate warnings about the optimized strategy.
        生成关于优化策略的警告
        
        Args:
            target_return: Target return
                           目标收益率
            expected_return: Expected return
                             预期收益率
            expected_risk: Expected risk
                           预期风险
            weights: Asset weights
                     资产权重
            constraints: Optimization constraints
                         优化约束条件
        
        Returns:
            List[str]: List of warnings
                       警告列表
        """
        warnings = []
        
        # Check if expected return is far from target
        # 检查预期收益率是否远离目标
        if abs(expected_return - target_return) > 0.05:
            warnings.append(
                f"预期收益率{expected_return:.2%}与目标{target_return:.2%}相差较大 / "
                f"Expected return {expected_return:.2%} differs significantly from target {target_return:.2%}"
            )
        
        # Check if risk is high
        # 检查风险是否较高
        if expected_risk > 0.3:
            warnings.append(
                f"预期风险{expected_risk:.2%}较高 / "
                f"Expected risk {expected_risk:.2%} is high"
            )
        
        # Check concentration
        # 检查集中度
        max_weight = max(weights.values())
        if max_weight > constraints.max_position_size * 0.9:
            warnings.append(
                f"最大持仓{max_weight:.2%}接近限制 / "
                f"Maximum position {max_weight:.2%} near limit"
            )
        
        # Check diversification
        # 检查分散化
        if len(weights) < constraints.min_diversification * 1.5:
            warnings.append(
                f"资产数量{len(weights)}较少，建议增加分散化 / "
                f"Asset count {len(weights)} is low, consider more diversification"
            )
        
        return warnings
    
    def _get_risk_multiplier(self, risk_tolerance: str) -> float:
        """Get risk multiplier based on risk tolerance."""
        multipliers = {
            "conservative": 2.0,
            "moderate": 1.0,
            "aggressive": 0.5
        }
        return multipliers.get(risk_tolerance, 1.0)
    
    def _get_rebalance_frequency(self, constraints: OptimizationConstraints) -> str:
        """Get rebalance frequency based on constraints."""
        frequency_map = {
            "conservative": "monthly",
            "moderate": "weekly",
            "aggressive": "daily"
        }
        return frequency_map.get(constraints.risk_tolerance, "weekly")
    
    def _get_stop_loss(self, risk_tolerance: str) -> float:
        """Get stop loss percentage based on risk tolerance."""
        stop_loss_map = {
            "conservative": 0.05,  # 5%
            "moderate": 0.10,      # 10%
            "aggressive": 0.15     # 15%
        }
        return stop_loss_map.get(risk_tolerance, 0.10)
    
    def _get_take_profit(self, risk_tolerance: str) -> float:
        """Get take profit percentage based on risk tolerance."""
        take_profit_map = {
            "conservative": 0.10,  # 10%
            "moderate": 0.20,      # 20%
            "aggressive": 0.30     # 30%
        }
        return take_profit_map.get(risk_tolerance, 0.20)
    
    def _select_model_type(self, target_return: float, risk_tolerance: str) -> str:
        """Select model type based on target return and risk tolerance."""
        if risk_tolerance == "conservative":
            return "linear"
        elif risk_tolerance == "aggressive" or target_return > 0.25:
            return "mlp"
        else:
            return "lgbm"
    
    def _select_features(self, model_type: str, risk_tolerance: str) -> List[str]:
        """Select features based on model type and risk tolerance."""
        # Basic features
        basic_features = [
            "$close", "$open", "$high", "$low", "$volume",
            "$change", "$factor"
        ]
        
        # Technical indicators
        technical_features = [
            "RESI5", "WVMA5", "RSQR5", "KLEN", "RSQR10",
            "CORR5", "CORD5", "CORR10", "ROC5", "MA5"
        ]
        
        if model_type == "linear":
            # Conservative: use basic features
            return basic_features[:5]
        elif model_type == "mlp":
            # Aggressive: use all features
            return basic_features + technical_features
        else:
            # Moderate: use basic + some technical
            return basic_features + technical_features[:5]
    
    def _select_lookback_period(self, risk_tolerance: str) -> int:
        """Select lookback period based on risk tolerance."""
        lookback_map = {
            "conservative": 60,   # 60 days
            "moderate": 30,       # 30 days
            "aggressive": 20      # 20 days
        }
        return lookback_map.get(risk_tolerance, 30)
    
    def _select_rebalance_frequency(self, risk_tolerance: str) -> str:
        """Select rebalance frequency based on risk tolerance."""
        frequency_map = {
            "conservative": "monthly",
            "moderate": "weekly",
            "aggressive": "daily"
        }
        return frequency_map.get(risk_tolerance, "weekly")
    
    def _select_position_sizing(self, risk_tolerance: str) -> str:
        """Select position sizing method based on risk tolerance."""
        sizing_map = {
            "conservative": "equal_weight",
            "moderate": "risk_parity",
            "aggressive": "kelly_criterion"
        }
        return sizing_map.get(risk_tolerance, "risk_parity")
    
    def _generate_risk_params(
        self,
        target_return: float,
        risk_tolerance: str
    ) -> Dict[str, any]:
        """Generate risk management parameters."""
        return {
            "stop_loss": self._get_stop_loss(risk_tolerance),
            "take_profit": self._get_take_profit(risk_tolerance),
            "max_drawdown": 0.20 if risk_tolerance == "conservative" else 0.30,
            "var_confidence": 0.95,
            "position_limit": 0.15 if risk_tolerance == "conservative" else 0.25
        }
    
    def set_risk_free_rate(self, rate: float) -> None:
        """
        Set the risk-free rate for optimization.
        设置用于优化的无风险利率
        
        Args:
            rate: Annual risk-free rate (e.g., 0.03 for 3%)
                 年化无风险利率（例如，0.03表示3%）
        """
        if rate < 0 or rate > 0.2:
            self.logger.warning(
                f"Unusual risk-free rate: {rate:.2%} / "
                f"异常的无风险利率: {rate:.2%}"
            )
        
        self.risk_free_rate = rate
        self.logger.info(
            f"Risk-free rate set to {rate:.2%} / "
            f"无风险利率设置为 {rate:.2%}"
        )
