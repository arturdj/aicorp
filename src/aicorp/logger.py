"""Logging module for AI Corp API client."""

import logging


def setup_logger(name: str = __name__, log_file: str = 'aicorp.log', verbosity: int = 2) -> logging.Logger:
    """Set up and configure logger.
    
    Args:
        name: Logger name
        log_file: Log file path
        verbosity: Verbosity level (0=ERROR, 1=WARNING, 2=INFO, 3=DEBUG)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Map verbosity level to logging level
    level_map = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG
    }
    
    # Set logging level based on verbosity, cap at DEBUG level for values > 3
    if verbosity >= 3:
        log_level = logging.DEBUG
    else:
        log_level = level_map.get(verbosity, logging.ERROR)
    logger.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger
