from .logger_interface import LoggerInterface


class SimpleLogger(LoggerInterface):
    def __init__(self):
        self._logs = []

    def log(self, message: str) -> None:
        self._logs.append(message)

    def get_logs(self) -> list[str]:
        return self._logs
