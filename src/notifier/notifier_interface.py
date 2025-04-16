"""Interface for notification mechanisms."""

from abc import ABC, abstractmethod


class NotifierInterface(ABC):
    @abstractmethod
    def check_and_notify(self, value: float) -> None:
        """Check value and trigger notification if needed."""
        pass

    @abstractmethod
    def was_notified(self) -> bool:
        """Return whether a notification has been triggered."""
        pass
