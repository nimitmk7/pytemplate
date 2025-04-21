"""
Logger interface module.
Records operations performed by calculator.
"""
from abc import ABC, abstractmethod


class LoggerInterface(ABC):
    """Defines the interface for a logger component."""

    @abstractmethod
    def log(self, message: str) -> None:
        """Log a message."""
        pass # pragma: no cover

    @abstractmethod
    def get_logs(self) -> list[str]:
        """Retrieve all logged messages."""
        pass # pragma: no cover

    @abstractmethod
    def clear_logs(self) -> None:
        """Clear all logged messages."""
        pass # pragma: no cover
