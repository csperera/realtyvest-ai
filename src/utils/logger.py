"""
Centralized logging configuration for the AVM system
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logger(
    name: str,
    log_file: Optional[str] = None,
    level: str = "INFO",
    max_bytes: int = 10485760,  # 10MB
    backup_count: int = 5,
) -> logging.Logger:
    """
    Configure and return a logger instance
    
    Args:
        name: Logger name (usually __name__ of calling module)
        log_file: Path to log file (optional)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        max_bytes: Max size of log file before rotation
        backup_count: Number of backup files to keep
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Convenience function for quick logger setup
def get_logger(name: str) -> logging.Logger:
    """
    Get logger with default config from environment
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger
    """
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_file = os.getenv("LOG_FILE", "logs/avm.log")
    
    return setup_logger(name, log_file=log_file, level=log_level)