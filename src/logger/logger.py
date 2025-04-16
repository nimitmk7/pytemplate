"""Implementation of the logger interface."""

from .logger_interface import LoggerInterface


class SimpleLogger(LoggerInterface):
    """A simple logger that stores log messages in memory."""

    def __init__(self) -> None:
        """Initialize the internal log storage."""
        self._logs = []

    def log(self, message: str) -> None:
        """Add a message to the internal log."""
        self._logs.append(message)

    def get_logs(self) -> list[str]:
        """Retrieve the stored log messages."""
        return self._logs
