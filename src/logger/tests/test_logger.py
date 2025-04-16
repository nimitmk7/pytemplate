import pytest
from logger.logger import SimpleLogger


def test_log_and_retrieve():
    logger = SimpleLogger()
    logger.log("first")
    logger.log("second")
    assert logger.get_logs() == ["first", "second"]


def test_empty_logs():
    logger = SimpleLogger()
    assert logger.get_logs() == []
