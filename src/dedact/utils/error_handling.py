"""
Error Handling Module
Centralized error handling and classification
"""

from enum import Enum
from typing import Optional
import traceback


class ErrorSeverity(Enum):
    """Error severity levels"""
    CRITICAL = "critical"  # Stop processing
    MAJOR = "major"  # Skip item, continue
    MINOR = "minor"  # Log and continue
    WARNING = "warning"  # Note but don't affect processing


class DEDACTError(Exception):
    """Base DEDACT exception"""
    def __init__(self, message: str, severity: ErrorSeverity = ErrorSeverity.MAJOR):
        super().__init__(message)
        self.severity = severity
        self.traceback = traceback.format_exc()


class FileProcessingError(DEDACTError):
    """Error during file processing"""
    pass


class ExtractionError(DEDACTError):
    """Error during content extraction"""
    pass


class DatabaseError(DEDACTError):
    """Database operation error"""
    pass


def handle_error(
    error: Exception,
    context: Optional[str] = None,
    logger = None
) -> bool:
    """
    Handle error based on severity
    
    Args:
        error: Exception to handle
        context: Context information
        logger: Logger instance
        
    Returns:
        True if processing should continue, False if should stop
    """
    if isinstance(error, DEDACTError):
        severity = error.severity
        message = f"{context}: {str(error)}" if context else str(error)
        
        if logger:
            if severity == ErrorSeverity.CRITICAL:
                logger.critical(message)
            elif severity == ErrorSeverity.MAJOR:
                logger.error(message)
            elif severity == ErrorSeverity.MINOR:
                logger.warning(message)
            else:
                logger.info(message)
        
        # Continue processing except for CRITICAL
        return severity != ErrorSeverity.CRITICAL
    else:
        # Unknown error - log and continue
        if logger:
            logger.error(f"Unexpected error: {str(error)}")
        return True
