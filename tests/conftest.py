"""
Pytest configuration and shared fixtures for Qlib Trading System tests
"""
import os
import sys
import tempfile
from pathlib import Path
from typing import Generator

import pytest

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_config_dict() -> dict:
    """Provide a sample configuration dictionary for testing"""
    return {
        "qlib": {
            "provider_uri": "~/.qlib/qlib_data/cn_data",
            "region": "cn",
        },
        "mlflow": {
            "tracking_uri": "./mlruns",
            "experiment_name": "qlib_trading_test",
        },
        "data": {
            "instruments": "csi300",
            "start_time": "2020-01-01",
            "end_time": "2021-12-31",
        },
        "logging": {
            "log_dir": "./logs",
            "log_level": "INFO",
        },
    }


@pytest.fixture
def sample_training_config() -> dict:
    """Provide a sample training configuration for testing"""
    return {
        "model_type": "lightgbm",
        "dataset_config": {
            "instruments": "csi300",
            "start_time": "2020-01-01",
            "end_time": "2021-12-31",
            "features": ["$close", "$volume"],
            "label": "Ref($close, -1) / $close - 1",
        },
        "model_params": {
            "n_estimators": 100,
            "learning_rate": 0.1,
        },
        "training_params": {
            "early_stopping_rounds": 10,
        },
        "experiment_name": "test_experiment",
    }


@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment variables before each test"""
    # Store original environment
    original_env = os.environ.copy()
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


# Hypothesis settings for property-based tests
from hypothesis import settings, Verbosity

# Register custom Hypothesis profile for testing
settings.register_profile("default", max_examples=100, deadline=None)
settings.register_profile("ci", max_examples=200, deadline=None)
settings.register_profile("dev", max_examples=10, deadline=None, verbosity=Verbosity.verbose)

# Load profile from environment or use default
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "default"))
