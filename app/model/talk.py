
from dataclasses import dataclass
from enum import Enum


class OpenAiMessageRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class Talk:
    role: OpenAiMessageRole
    content: str

    def to_dict(self):
        return {
            "role": self.role.value,
            "content": self.content
        }

    @classmethod
    def from_dict(cls, body: dict):
        return Talk(
            role=OpenAiMessageRole(body["role"]),
            content=body["content"]
        )
