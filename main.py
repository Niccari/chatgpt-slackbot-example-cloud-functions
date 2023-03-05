import re
import traceback
from typing import Callable
from flask import Request
import functions_framework
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from google.oauth2 import id_token
from google.auth.transport import requests

from app.container import AppContainer
from app.model.result import Result
from app.model.result import ResultCode
from app.model.session import Session
from app.config import Config

config = Config()
container = AppContainer(config)
chat_usecase = container.chat_usecase()

app = App(process_before_response=True)
handler = SlackRequestHandler(app)
container.slack_provider().set_provider(app.client)


def to_session(message: dict) -> Session:
    return Session(
        user=message["user"],
        team=message["team"],
        thread_ts=message.get("thread_ts") or message.get("ts") or "-1",
        channel=message["channel"]
    )


def say_to_thread(channel: str, message: str, thread_ts: str):
    app.client.chat_postMessage(
        channel=channel,
        text=message,
        thread_ts=thread_ts
    )


def error_handling(channel: str, thread_ts: str, result: Result):
    if result.code == ResultCode.ERROR_OPENAI_API_ERROR:
        say_to_thread(
            channel=channel,
            message="エラー: OpenAIのAPI呼び出しでエラーが発生しました。"
                    "通常のOpenAIで次のメッセージが何か聞いて見てください。\n"
                    "---\n"
                    f"```{result.error_message()}```",
            thread_ts=thread_ts
        )
    if result.code == ResultCode.ERROR_INTERNAL_SERVER:
        say_to_thread(
            channel=channel,
            message="エラー: 内部処理でエラーが発生しました。",
            thread_ts=thread_ts
        )


@app.message(re.compile(r"!gpt (talk|setting) ((.|\s|\r|\n)*)"))
def dispatch_talk(message: dict, say: Callable):
    session = to_session(message)
    chat_usecase.dispatch_request_talk(session)


@app.message("!gpt help")
def ask_help(message: dict, say: Callable):
    say(
        "`!gpt setting [ChatGPTに投げるメッセージ]`: ChatGPTの会話における設定を行います。\n"
        "`!gpt talk [ChatGPTに投げるメッセージ]`: ChatGPTを使って会話します。\n"
        "`!gpt help`: 本アプリの使い方を表示します。\n"
    )


def talk(message: dict):
    session = to_session(message)
    result = chat_usecase.request_talk(session)
    if result.code == ResultCode.OK_DUPLICATED:
        return
    if result.code != ResultCode.OK:
        error_handling(session.channel, session.thread_ts, result)
        return
    say_to_thread(
        channel=session.channel,
        message=f"!gpt response {result.content()}",
        thread_ts=session.thread_ts
    )


@functions_framework.http
def chatgpt_slackbot(request: Request):
    if request.method != "POST":
        return "Invalid method", 405

    if request.headers.get("X-Slack-Signature"):
        slack_retry = request.headers.get("X-Slack-No-Retry")
        if slack_retry is not None:
            return "ok", 200
        return handler.handle(request)
    elif request.headers.get("X-CloudTasks-QueueName") == Config.CLOUD_TASKS_QUEUE_NAME:    # noqa: E501
        if config.IS_CLOUD:
            try:
                audience = config.FUNCTIONS_URL
                requester = requests.Request()
                authorization_str = \
                    request.headers.get("Authorization") or "Bearer "
                token = authorization_str.split(" ")[1]
                id_token.verify_oauth2_token(token, requester, audience)
            except Exception:
                container._logger().warning(traceback.format_exc())
                return "Forbidden", 403
        talk(request.get_json())
        return "ok", 200
    return "No action", 200
