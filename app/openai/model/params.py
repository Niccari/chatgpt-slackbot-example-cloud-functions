from dataclasses import dataclass

from app.model.talk import Talk


@dataclass
class OpenAiResponseUsageParam:
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


@dataclass
class OpenAiResponseChoiceParam:
    finish_reason: str
    index: int
    message: Talk

    @classmethod
    def from_dict(cls, response: dict):
        return OpenAiResponseChoiceParam(
            finish_reason=response["finish_reason"],
            index=response["index"],
            message=Talk.from_dict(response["message"]),
        )


@dataclass
class OpenAiResponseParam:
    id: str
    created: int
    usage: OpenAiResponseUsageParam
    choices: list[OpenAiResponseChoiceParam]

    @classmethod
    def from_dict(cls, response: dict):
        return OpenAiResponseParam(
            id=response["id"],
            created=response["created"],
            usage=OpenAiResponseUsageParam(**response["usage"]),
            choices=[
                OpenAiResponseChoiceParam.from_dict(c)
                for c in response["choices"]
            ]
        )
