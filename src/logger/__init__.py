"""API for the logger component.

This module provides a simple API for logging messages and retrieving logs.
"""

from .logger import SimpleLogger
from .logger_interface import LoggerInterface

_logger = SimpleLogger()

# Exposing API functions
def log(message: str) -> None:
    """Log a message."""
    _logger.log(message)

def get_logs() -> list[str]:
    """Retrieve all logged messages."""
    return _logger.get_logs()

def clear_logs() -> None:
    """Clear all logged messages."""
    _logger.clear_logs()

__all__ = ["log", "get_logs", "clear_logs", "SimpleLogger", "LoggerInterface"]