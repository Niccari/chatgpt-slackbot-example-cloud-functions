from app.chat_usecase import ChatUseCase
from app.config import Config
from app.logger.cloud import CloudLogger
from app.logger.interface import Logger
from app.logger.local import LocalLogger
from app.openai.client import OpenAiClient
from app.slack.provider import SlackProvider
from app.tasks.tasks import TasksClient


class AppContainer:
    def __init__(self, config: Config) -> None:
        self.__config = config
        self.__logger = None
        self.__tasks_client = None
        self.__slack_provider = None
        self.__open_ai_client = None
        self.__chat_usecase = None

    def _logger(self) -> Logger:
        if self.__logger is None:
            if self.__config.IS_CLOUD:
                self.__logger = CloudLogger(self.__config.LOG_LEVEL)
            else:
                self.__logger = LocalLogger(self.__config.LOG_LEVEL)
        return self.__logger

    def _tasks_client(self) -> TasksClient:
        if self.__tasks_client is None:
            self.__tasks_client = TasksClient(
                project=self.__config.PROJECT_ID,
                region=self.__config.REGION,
                function_url=self.__config.FUNCTIONS_URL,
                emulator_url=self.__config.CLOUD_TASKS_EMULATOR_HOST,
                queue_name=self.__config.CLOUD_TASKS_QUEUE_NAME,
                oidc_token_service_account=self.__config.OIDC_TOKEN_SERVICE_ACCOUNT,    # noqa: E501
                logger=self._logger()
            )
        return self.__tasks_client

    def slack_provider(self) -> SlackProvider:
        if self.__slack_provider is None:
            self.__slack_provider = SlackProvider(
                logger=self._logger()
            )
        return self.__slack_provider

    def _open_ai_client(self) -> OpenAiClient:
        if self.__open_ai_client is None:
            self.__open_ai_client = OpenAiClient(
                logger=self._logger()
            )
        return self.__open_ai_client

    def chat_usecase(self) -> ChatUseCase:
        if self.__chat_usecase is None:
            self.__chat_usecase = ChatUseCase(
                slack_provider=self.slack_provider(),
                openai_client=self._open_ai_client(),
                tasks_client=self._tasks_client()
            )
        return self.__chat_usecase
