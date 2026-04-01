"""
Logging Configuration Module
Comprehensive logging for DEDACT
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logging(
    log_dir: Path = Path('logs'),
    log_level: str = 'INFO',
    console_output: bool = True
) -> logging.Logger:
    """
    Setup comprehensive logging
    
    Args:
        log_dir: Directory for log files
        log_level: Logging level (DEBUG/INFO/WARNING/ERROR/CRITICAL)
        console_output: Whether to output to console
        
    Returns:
        Configured logger
    """
    # Create log directory
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger('dedact')
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers = []
    
    # File handler (all levels)
    log_file = log_dir / f"dedact_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler (INFO and above)
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '[%(levelname)s] %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str = 'dedact') -> logging.Logger:
    """Get configured logger"""
    return logging.getLogger(name)
