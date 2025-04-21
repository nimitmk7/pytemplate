from logger.logger import SimpleLogger

def test_log_and_retrieve() -> None:
    logger = SimpleLogger()
    logger.log("test message")
    logs = logger.get_logs()
    assert logs == ["test message"]

def test_multiple_messages() -> None:
    logger = SimpleLogger()
    logger.log("first message")
    logger.log("second message")
    assert len(logger.get_logs()) == 2
    assert "first message" in logger.get_logs()
    assert "second message" in logger.get_logs()

def test_logs_preserve_order() -> None:
    logger = SimpleLogger()
    logger.log("first")
    logger.log("second")
    logger.log("third")
    logs = logger.get_logs()
    assert logs[0] == "first"
    assert logs[1] == "second"
    assert logs[2] == "third"

def test_clear_logs() -> None:
    logger = SimpleLogger()
    logger.log("first message")
    logger.log("second message")
    assert len(logger.get_logs()) == 2
    logger.clear_logs()
    assert len(logger.get_logs()) == 0
    
def test_log_after_clear() -> None:
    logger = SimpleLogger()
    logger.log("first message")
    logger.clear_logs()
    logger.log("new message")
    logs = logger.get_logs()
    assert len(logs) == 1
    assert logs[0] == "new message"