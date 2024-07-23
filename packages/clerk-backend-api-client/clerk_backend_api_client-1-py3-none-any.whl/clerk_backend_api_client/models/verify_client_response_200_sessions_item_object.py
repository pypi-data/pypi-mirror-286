from enum import Enum


class VerifyClientResponse200SessionsItemObject(str, Enum):
    SESSION = "session"

    def __str__(self) -> str:
        return str(self.value)
