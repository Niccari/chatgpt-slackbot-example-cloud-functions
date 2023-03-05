from dataclasses import dataclass


@dataclass
class Session():
    user: str
    channel: str
    thread_ts: str
    team: str

    def user_id(self):
        return f"slack-user-${self.team}-${self.user}"
