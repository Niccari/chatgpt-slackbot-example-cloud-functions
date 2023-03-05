import json
import re
from slack_sdk import WebClient
from app.logger.interface import Logger
from app.model.session import Session
from app.model.talk import OpenAiMessageRole, Talk


class SlackProvider:
    def __init__(self, logger: Logger) -> None:
        self.__logger = logger
        self.__client = None

    def set_provider(self, client: WebClient):
        self.__client = client

    def read_conservation(self, session: Session) -> list[Talk]:
        if self.__client is None:
            self.__logger.warning("slack client is not set.")
            return []
        replies = self.__client.conversations_replies(
            channel=session.channel,
            ts=session.thread_ts
        )
        thread_messages: list[dict] = replies.get('messages') or []

        talks: list[Talk] = []
        # TODO: main.pyとコマンドを揃えておきたい
        patterns = [
            (re.compile(r"^!gpt talk ((.|\s|\r|\n)*)$"),
             OpenAiMessageRole.USER),
            (re.compile(r"^!gpt response ((.|\s|\r|\n)*)$"),
             OpenAiMessageRole.ASSISTANT),
            (re.compile(r"^!gpt setting ((.|\s|\r|\n)*)$"),
             OpenAiMessageRole.SYSTEM),
        ]
        for message in thread_messages:
            if message.get('type') != 'message':
                continue
            text = message.get('text') or ""
            for pattern, role in patterns:
                matcher = pattern.match(text)
                if matcher is not None:
                    talks.append(Talk(
                        role=role,
                        content=matcher.group(1)
                    ))
        self.__logger.debug(json.dumps([talk.to_dict() for talk in talks]))
        return talks
