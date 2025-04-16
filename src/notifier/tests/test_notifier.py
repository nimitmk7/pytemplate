"""Tests for the ThresholdNotifier."""

import pytest
from notifier.notifier import ThresholdNotifier


def test_notification_triggered() -> None:
    notifier = ThresholdNotifier(threshold=10)
    notifier.check_and_notify(15)
    assert notifier.was_notified()


def test_notification_not_triggered() -> None:
    notifier = ThresholdNotifier(threshold=10)
    notifier.check_and_notify(5)
    assert not notifier.was_notified()
