"""API for the notifier component.

This module provides a simple API for threshold-based notifications.
"""

from .notifier import ThresholdNotifier
from .notifier_interface import NotifierInterface

_notifier = ThresholdNotifier(10)

# Exposing API functions
def check_and_notify(value: float) -> None:
    """Check if a value exceeds the threshold and trigger notification if needed."""
    _notifier.check_and_notify(value)

def was_notified() -> bool:
    """Check whether a notification has been triggered."""
    return _notifier.was_notified()

def create_notifier(threshold: float) -> ThresholdNotifier:
    """Create a new notifier with the specified threshold."""
    return ThresholdNotifier(threshold)

__all__ = ["check_and_notify", "was_notified", "create_notifier", 
           "ThresholdNotifier", "NotifierInterface"]