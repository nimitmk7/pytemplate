import pytest
from logger.logger import SimpleLogger

def test_log_and_retrieve() -> None:
    logger = SimpleLogger()
    logger.log("test message")
    logs = logger.get_logs()
    assert logs == ["test message"]

def test_empty_logs() -> None:
    logger = SimpleLogger()
    logs = logger.get_logs()
    assert logs == []
