"""Logger interface module."""

from abc import ABC, abstractmethod


class LoggerInterface(ABC):
    """Defines the interface for a logger component."""

    @abstractmethod
    def log(self, message: str) -> None:
        """Log a message."""
        pass

    @abstractmethod
    def get_logs(self) -> list[str]:
        """Retrieve all logged messages."""
        pass
