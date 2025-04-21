"""Integration test for Calculator and Logger components."""
import calculator
import logger


def test_calc_operations_logging() -> None:
    """Ensure Calculator and Logger work together correctly."""
    logger.clear_logs()

    result1 = calculator.add(3, 2)
    result2 = calculator.divide(10, 2)

    logger.log(f"3 + 2 = {result1}")
    logger.log(f"10 / 2 = {int(result2) if result2.is_integer() else result2}")

    logs = logger.get_logs()

    assert result1 == 5
    assert result2 == 5
    assert logs == ["3 + 2 = 5", "10 / 2 = 5"]
