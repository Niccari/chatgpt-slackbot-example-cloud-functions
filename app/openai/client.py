
import json
import openai
from app.logger.interface import Logger
from app.model.talk import Talk
from app.openai.model.params import OpenAiResponseParam


class OpenAiClient:
    def __init__(self, logger: Logger) -> None:
        self.__logger = logger

    def call_chat_completion(self, user_id: str, talks: list[Talk]) -> str:
        try:
            raw_response: dict = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[talk.to_dict() for talk in talks],
                user=user_id,
            )  # type: ignore
            response = OpenAiResponseParam.from_dict(raw_response)
            response_message = response.choices[0].message
            self.__logger.debug(
                f"response: {json.dumps(response_message.to_dict())}")
            return response_message.content
        except openai.OpenAIError as e:
            raise e
