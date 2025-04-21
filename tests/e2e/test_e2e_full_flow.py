"""E2E test: Calculator + Logger + Notifier working together in a full workflow."""

import calculator
import logger
import notifier


def test_e2e_full_workflow() -> None:
    """Simulate full workflow: calculation, logging, and notification."""
    logger.clear_logs()

    # Perform calculations
    result1 = calculator.add(5, 6)           # 11
    result2 = calculator.multiply(2, 3)      # 6
    result3 = calculator.subtract(15, 5)     # 10
    result4 = calculator.divide(20, 2)       # 10.0

    # Log operations
    logger.log(f"Addition: 5 + 6 = {result1}")
    logger.log(f"Multiplication: 2 * 3 = {result2}")
    logger.log(f"Subtraction: 15 - 5 = {result3}")
    logger.log(
        f"Division: 20 / 2 = {int(result4)}"
    )  # convert to int to match formatting

    # Trigger notifications
    notifier.check_and_notify(result1)
    notifier.check_and_notify(result2)
    notifier.check_and_notify(result3)
    notifier.check_and_notify(result4)

    # Assertions
    assert result1 == 11
    assert result2 == 6
    assert result3 == 10
    assert result4 == 10.0

    logs = logger.get_logs()
    assert logs == [
        "Addition: 5 + 6 = 11",
        "Multiplication: 2 * 3 = 6",
        "Subtraction: 15 - 5 = 10",
        "Division: 20 / 2 = 10",
    ]

    assert notifier.was_notified() is True
