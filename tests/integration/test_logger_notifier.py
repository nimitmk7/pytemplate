"""Integration test for Logger and Notifier components."""
import logger
from notifier import create_notifier


def test_log_and_notify_behavior() -> None:
    """Ensure Logger and Notifier interact correctly."""
    logger.clear_logs()

    notifier = create_notifier(threshold=15)

    value = 20
    logger.log(f"Value received: {value}")
    notifier.check_and_notify(value)

    logs = logger.get_logs()

    assert logs == ["Value received: 20"]
    assert notifier.was_notified() is True
