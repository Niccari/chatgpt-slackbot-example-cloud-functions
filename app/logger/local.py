import logging

from app.logger.interface import Logger


class LocalLogger(Logger):
    def __init__(self, log_level: int) -> None:
        super().__init__(log_level)
        self.__logger = logging.getLogger("ChatGPT-SlackBot")
        self.__logger.setLevel(self.log_level)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(process)d]  [%(name)s] [%(levelname)s]"
            " %(message)s"
        )

        self.__handler = logging.StreamHandler()
        self.__handler.setLevel(log_level)
        self.__handler.setFormatter(formatter)
        self.__logger.addHandler(self.__handler)

    @property
    def handler(self) -> logging.Handler:
        return self.__handler

    def debug(self, text):
        self.__logger.debug(text)

    def info(self, text):
        self.__logger.info(text)

    def warning(self, text):
        self.__logger.warning(text)

    def error(self, text):
        self.__logger.error(text)
