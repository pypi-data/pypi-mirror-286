from enum import Enum


class ClientSessionsItemObject(str, Enum):
    SESSION = "session"

    def __str__(self) -> str:
        return str(self.value)
