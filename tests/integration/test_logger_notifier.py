"""Integration test for Logger and Notifier components."""

from logger.logger import SimpleLogger
from notifier.notifier import ThresholdNotifier


def test_log_and_notify_behavior() -> None:
    """Ensure Logger and Notifier interact correctly."""
    logger = SimpleLogger()
    notifier = ThresholdNotifier(threshold=15)

    value = 20
    logger.log(f"Value received: {value}")
    notifier.check_and_notify(value)

    logs = logger.get_logs()

    assert logs == ["Value received: 20"]
    assert notifier.was_notified() is True
