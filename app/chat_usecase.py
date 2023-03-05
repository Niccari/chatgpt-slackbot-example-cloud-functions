from dataclasses import asdict
import openai

from app.model.result import Result
from app.model.result import ResultCode
from app.model.session import Session
from app.openai.client import OpenAiClient
from app.slack.provider import SlackProvider
from app.tasks.tasks import TasksClient


class ChatUseCase:
    def __init__(
        self,
        openai_client: OpenAiClient,
        slack_provider: SlackProvider,
        tasks_client: TasksClient
    ) -> None:
        self.__openai_client = openai_client
        self.__slack_provider = slack_provider
        self.__tasks_client = tasks_client

    def dispatch_request_talk(self, session: Session) -> Result:
        self.__tasks_client.dispatch(
            payload={
                **asdict(session)
            }
        )
        return Result(
            code=ResultCode.OK
        )

    def request_talk(self, session: Session) -> Result:
        try:
            talks = self.__slack_provider.read_conservation(session)
            response_content = self.__openai_client.call_chat_completion(
                user_id=session.user_id(),
                talks=talks
            )
            return Result(
                code=ResultCode.OK,
                content=response_content
            )
        except openai.OpenAIError as e:
            return Result(
                code=ResultCode.ERROR_OPENAI_API_ERROR,
                error_message=e.http_body
            )
        except Exception as e:
            return Result(
                code=ResultCode.ERROR_INTERNAL_SERVER,
                error_message=str(e)
            )
