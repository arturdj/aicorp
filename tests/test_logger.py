"""Tests for the logger module."""

import logging
import os
import tempfile
from unittest.mock import patch, mock_open
import pytest
from aicorp.logger import setup_logger


class TestLogger:
    """Test cases for logger setup functionality."""

    def test_setup_logger_default_params(self):
        """Test logger setup with default parameters."""
        logger = setup_logger()
        
        assert isinstance(logger, logging.Logger)
        assert logger.level == logging.INFO  # Default verbosity=2 maps to INFO
        assert len(logger.handlers) == 2  # File and console handlers

    def test_setup_logger_verbosity_levels(self):
        """Test logger setup with different verbosity levels."""
        # Test ERROR level (verbosity=0)
        logger_error = setup_logger("test_error", verbosity=0)
        assert logger_error.level == logging.ERROR
        
        # Test WARNING level (verbosity=1)
        logger_warning = setup_logger("test_warning", verbosity=1)
        assert logger_warning.level == logging.WARNING
        
        # Test INFO level (verbosity=2)
        logger_info = setup_logger("test_info", verbosity=2)
        assert logger_info.level == logging.INFO
        
        # Test DEBUG level (verbosity=3)
        logger_debug = setup_logger("test_debug", verbosity=3)
        assert logger_debug.level == logging.DEBUG
        
        # Test DEBUG level for high verbosity (verbosity=5)
        logger_high = setup_logger("test_high", verbosity=5)
        assert logger_high.level == logging.DEBUG

    def test_setup_logger_custom_name(self):
        """Test logger setup with custom name."""
        custom_name = "custom_test_logger"
        logger = setup_logger(custom_name)
        
        assert logger.name == custom_name

    def test_setup_logger_custom_log_file(self):
        """Test logger setup with custom log file."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            custom_log_file = tmp_file.name
        
        try:
            logger = setup_logger("test_custom_file", log_file=custom_log_file)
            
            # Check that file handler is configured with the custom file
            file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
            assert len(file_handlers) == 1
            assert file_handlers[0].baseFilename == os.path.abspath(custom_log_file)
        finally:
            # Clean up
            if os.path.exists(custom_log_file):
                os.unlink(custom_log_file)

    def test_setup_logger_no_duplicate_handlers(self):
        """Test that calling setup_logger multiple times doesn't add duplicate handlers."""
        logger_name = "test_no_duplicates"
        
        # First call
        logger1 = setup_logger(logger_name)
        initial_handler_count = len(logger1.handlers)
        
        # Second call with same name
        logger2 = setup_logger(logger_name)
        
        # Should be the same logger instance
        assert logger1 is logger2
        assert len(logger2.handlers) == initial_handler_count

    def test_logger_formatter(self):
        """Test that logger handlers have correct formatter."""
        logger = setup_logger("test_formatter")
        
        expected_format = '%(asctime)s - %(levelname)s - %(message)s'
        
        for handler in logger.handlers:
            assert handler.formatter._fmt == expected_format

    def test_logger_handler_types(self):
        """Test that logger has both file and console handlers."""
        logger = setup_logger("test_handlers")
        
        handler_types = [type(h).__name__ for h in logger.handlers]
        
        assert 'FileHandler' in handler_types
        assert 'StreamHandler' in handler_types

    def test_logger_functionality(self):
        """Test that logger actually logs messages."""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp_file:
            log_file = tmp_file.name
        
        try:
            logger = setup_logger("test_functionality", log_file=log_file, verbosity=3)
            
            # Log messages at different levels
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")
            
            # Force flush handlers
            for handler in logger.handlers:
                handler.flush()
            
            # Read log file content
            with open(log_file, 'r') as f:
                log_content = f.read()
            
            # Check that messages were logged
            assert "Debug message" in log_content
            assert "Info message" in log_content
            assert "Warning message" in log_content
            assert "Error message" in log_content
            
        finally:
            # Clean up
            if os.path.exists(log_file):
                os.unlink(log_file)

    def test_logger_verbosity_filtering(self):
        """Test that logger filters messages based on verbosity level."""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp_file:
            log_file = tmp_file.name
        
        try:
            # Create logger with WARNING level (verbosity=1)
            logger = setup_logger("test_filtering", log_file=log_file, verbosity=1)
            
            # Log messages at different levels
            logger.debug("Debug message")  # Should not appear
            logger.info("Info message")    # Should not appear
            logger.warning("Warning message")  # Should appear
            logger.error("Error message")      # Should appear
            
            # Force flush handlers
            for handler in logger.handlers:
                handler.flush()
            
            # Read log file content
            with open(log_file, 'r') as f:
                log_content = f.read()
            
            # Check filtering
            assert "Debug message" not in log_content
            assert "Info message" not in log_content
            assert "Warning message" in log_content
            assert "Error message" in log_content
            
        finally:
            # Clean up
            if os.path.exists(log_file):
                os.unlink(log_file)
