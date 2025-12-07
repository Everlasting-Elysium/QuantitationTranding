"""
Application Layer
应用层模块
"""

from .training_manager import (
    TrainingManager,
    TrainingConfig,
    DatasetConfig,
    TrainingResult,
    TrainingManagerError
)

from .model_registry import (
    ModelRegistry,
    ModelInfo,
    ModelFilter,
    ModelRegistryError
)

from .backtest_manager import (
    BacktestManager,
    BacktestConfig,
    BacktestResult,
    Trade,
    BacktestManagerError
)

from .visualization_manager import (
    VisualizationManager,
    VisualizationManagerError
)

from .report_generator import (
    ReportGenerator,
    ReportGeneratorError
)

from .signal_generator import (
    SignalGenerator,
    SignalGeneratorError
)

from .market_selector import (
    MarketSelector
)

from .performance_analyzer import (
    PerformanceAnalyzer
)

from .strategy_optimizer import (
    StrategyOptimizer
)

from .simulation_engine import (
    SimulationEngine,
    SimulationSession,
    SimulationStepResult,
    SimulationReport,
    SimulationEngineError
)

from .live_trading_manager import (
    LiveTradingManager
)

__all__ = [
    "TrainingManager",
    "TrainingConfig",
    "DatasetConfig",
    "TrainingResult",
    "TrainingManagerError",
    "ModelRegistry",
    "ModelInfo",
    "ModelFilter",
    "ModelRegistryError",
    "BacktestManager",
    "BacktestConfig",
    "BacktestResult",
    "Trade",
    "BacktestManagerError",
    "VisualizationManager",
    "VisualizationManagerError",
    "ReportGenerator",
    "ReportGeneratorError",
    "SignalGenerator",
    "SignalGeneratorError",
    "MarketSelector",
    "PerformanceAnalyzer",
    "StrategyOptimizer",
    "SimulationEngine",
    "SimulationSession",
    "SimulationStepResult",
    "SimulationReport",
    "SimulationEngineError",
    "LiveTradingManager",
]
