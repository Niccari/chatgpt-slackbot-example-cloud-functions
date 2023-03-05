import json
from logging import DEBUG
from logging import ERROR
from logging import INFO
from logging import WARNING

from app.logger.interface import Logger, Severity


class CloudLogger(Logger):
    def __init__(self, log_level: int) -> None:
        super().__init__(log_level)

        self.__debug = self.__nop
        self.__info = self.__nop
        self.__warning = self.__nop
        self.__error = self.__nop
        if self.log_level <= DEBUG:
            self.__debug = self.__print
        if self.log_level <= INFO:
            self.__info = self.__print
        if self.log_level <= WARNING:
            self.__warning = self.__print
        if self.log_level <= ERROR:
            self.__error = self.__print

    @staticmethod
    def __print(message: str, severity: Severity):
        print(json.dumps({
            "severity": severity.value,
            "message": message
        }))

    @staticmethod
    def __nop(message: str, severity: Severity):
        pass

    def debug(self, message: str):
        self.__debug(message, Severity.DEBUG)

    def info(self, message: str):
        self.__info(message, Severity.INFO)

    def warning(self, message: str):
        self.__warning(message, Severity.WARNING)

    def error(self, message: str):
        self.__error(message, Severity.ERROR)
