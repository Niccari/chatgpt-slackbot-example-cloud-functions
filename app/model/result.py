from enum import Enum

from app.model.talk import Talk


class ResultCode(Enum):
    OK = 0
    OK_DUPLICATED = 1
    ERROR_OPENAI_API_ERROR = 10
    ERROR_INTERNAL_SERVER = 500


class Result:
    def __init__(
        self,
        code: ResultCode,
        content: str | list[Talk] | None = None,
        user_name: str | None = None,
        error_message: str | None = None,
    ) -> None:
        self.code = code
        self.__content = content
        self.__user_name = user_name
        self.__error_message = error_message

    def is_success(self):
        return self.code == ResultCode.OK

    def content(self):
        return self.__content

    def user_name(self):
        return self.__user_name

    def error_message(self):
        return self.__error_message
