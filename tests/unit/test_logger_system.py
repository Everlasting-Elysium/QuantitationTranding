"""
Unit tests for LoggerSystem
"""
import logging
from pathlib import Path

import pytest

from infrastructure.logger_system import LoggerSystem, get_logger, setup_logging


class TestLoggerSystem:
    """Test suite for LoggerSystem class"""
    
    def test_singleton_pattern(self):
        """Test that LoggerSystem follows singleton pattern"""
        logger_system1 = LoggerSystem()
        logger_system2 = LoggerSystem()
        assert logger_system1 is logger_system2
    
    def test_setup_creates_log_directory(self, temp_dir):
        """Test that setup creates the log directory"""
        log_dir = temp_dir / "logs"
        logger_system = LoggerSystem()
        logger_system.setup(str(log_dir))
        
        assert log_dir.exists()
        assert log_dir.is_dir()
    
    def test_setup_configures_log_level(self, temp_dir):
        """Test that setup configures the correct log level"""
        log_dir = temp_dir / "logs"
        logger_system = LoggerSystem()
        logger_system.setup(str(log_dir), log_level="DEBUG")
        
        assert logger_system.log_level == "DEBUG"
        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG
    
    def test_get_logger_returns_logger(self, temp_dir):
        """Test that get_logger returns a valid logger"""
        log_dir = temp_dir / "logs"
        logger_system = LoggerSystem()
        logger_system.setup(str(log_dir))
        
        logger = logger_system.get_logger("test_module")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_module"
    
    def test_get_logger_caches_loggers(self, temp_dir):
        """Test that get_logger caches logger instances"""
        log_dir = temp_dir / "logs"
        logger_system = LoggerSystem()
        logger_system.setup(str(log_dir))
        
        logger1 = logger_system.get_logger("test_module")
        logger2 = logger_system.get_logger("test_module")
        assert logger1 is logger2
    
    def test_logger_writes_to_file(self, temp_dir):
        """Test that logger writes messages to file"""
        log_dir = temp_dir / "logs"
        logger_system = LoggerSystem()
        logger_system.setup(str(log_dir))
        
        logger = logger_system.get_logger("test_module")
        test_message = "Test log message"
        logger.info(test_message)
        
        log_file = log_dir / "qlib_trading.log"
        assert log_file.exists()
        
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert test_message in content
    
    def test_log_level_filtering(self, temp_dir):
        """Test that log level filtering works correctly"""
        log_dir = temp_dir / "logs"
        logger_system = LoggerSystem()
        logger_system.setup(str(log_dir), log_level="WARNING")
        
        logger = logger_system.get_logger("test_module")
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        
        log_file = log_dir / "qlib_trading.log"
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Debug message" not in content
            assert "Info message" not in content
            assert "Warning message" in content
            assert "Error message" in content
    
    def test_set_level_updates_log_level(self, temp_dir):
        """Test that set_level dynamically updates the log level"""
        log_dir = temp_dir / "logs"
        logger_system = LoggerSystem()
        logger_system.setup(str(log_dir), log_level="INFO")
        
        logger_system.set_level("DEBUG")
        assert logger_system.log_level == "DEBUG"
        
        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG
    
    def test_is_initialized(self, temp_dir):
        """Test that is_initialized returns correct status"""
        # Reset the singleton state for this test
        LoggerSystem._initialized = False
        
        logger_system = LoggerSystem()
        assert not logger_system.is_initialized()
        
        log_dir = temp_dir / "logs"
        logger_system.setup(str(log_dir))
        assert logger_system.is_initialized()
    
    def test_get_log_files(self, temp_dir):
        """Test that get_log_files returns log file list"""
        log_dir = temp_dir / "logs"
        logger_system = LoggerSystem()
        logger_system.setup(str(log_dir))
        
        logger = logger_system.get_logger("test")
        logger.info("Test message")
        
        log_files = logger_system.get_log_files()
        assert len(log_files) > 0
        assert any("qlib_trading.log" in str(f) for f in log_files)
    
    def test_log_format_includes_required_fields(self, temp_dir):
        """Test that log entries contain timestamp, level, and module name"""
        log_dir = temp_dir / "logs"
        logger_system = LoggerSystem()
        logger_system.setup(str(log_dir))
        
        logger = logger_system.get_logger("test_module")
        logger.info("Test message")
        
        log_file = log_dir / "qlib_trading.log"
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Check for timestamp (contains date and time)
            assert any(char.isdigit() for char in content)
            # Check for log level
            assert "INFO" in content
            # Check for module name
            assert "test_module" in content
    
    def test_rotating_file_handler_configured(self, temp_dir):
        """Test that rotating file handler is properly configured"""
        log_dir = temp_dir / "logs"
        max_bytes = 1024  # 1KB for testing
        backup_count = 3
        
        logger_system = LoggerSystem()
        logger_system.setup(
            str(log_dir),
            max_bytes=max_bytes,
            backup_count=backup_count
        )
        
        assert logger_system.max_bytes == max_bytes
        assert logger_system.backup_count == backup_count
        
        # Verify handler is configured
        root_logger = logging.getLogger()
        rotating_handlers = [
            h for h in root_logger.handlers
            if isinstance(h, logging.handlers.RotatingFileHandler)
        ]
        assert len(rotating_handlers) > 0
        
        handler = rotating_handlers[0]
        assert handler.maxBytes == max_bytes
        assert handler.backupCount == backup_count
    
    def test_convenience_functions(self, temp_dir):
        """Test convenience functions work correctly"""
        log_dir = temp_dir / "logs"
        
        # Test setup_logging
        setup_logging(str(log_dir), log_level="DEBUG")
        
        # Test get_logger
        logger = get_logger("convenience_test")
        assert isinstance(logger, logging.Logger)
        
        logger.info("Convenience test message")
        
        log_file = log_dir / "qlib_trading.log"
        assert log_file.exists()


class TestLoggerSystemErrorHandling:
    """Test error handling in LoggerSystem"""
    
    def test_error_logging_includes_stack_trace(self, temp_dir):
        """Test that errors are logged with stack trace information"""
        log_dir = temp_dir / "logs"
        logger_system = LoggerSystem()
        logger_system.setup(str(log_dir))
        
        logger = logger_system.get_logger("error_test")
        
        try:
            raise ValueError("Test error")
        except ValueError:
            logger.exception("An error occurred")
        
        log_file = log_dir / "qlib_trading.log"
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Test error" in content
            assert "Traceback" in content or "ValueError" in content
