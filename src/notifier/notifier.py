"""Concrete implementation of the Notifier interface."""

from .notifier_interface import NotifierInterface


class ThresholdNotifier(NotifierInterface):
    def __init__(self, threshold: float) -> None:
        """Initialize the notifier with a specific threshold."""
        self._threshold: float = threshold
        self._notified: bool = False

    def check_and_notify(self, value: float) -> None:
        """Trigger notification if value exceeds threshold."""
        if value > self._threshold:
            self._notified = True

    def was_notified(self) -> bool:
        """Check whether a notification has been triggered."""
        return self._notified
