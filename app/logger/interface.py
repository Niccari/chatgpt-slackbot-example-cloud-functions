from enum import Enum


class Severity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


class Logger:
    def __init__(self, log_level: int) -> None:
        self.log_level = log_level

    def debug(self, message: str):
        pass

    def info(self, message: str):
        pass

    def warning(self, message: str):
        pass

    def error(self, message: str):
        pass
