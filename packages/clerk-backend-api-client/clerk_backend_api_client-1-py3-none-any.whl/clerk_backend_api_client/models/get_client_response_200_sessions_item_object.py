from enum import Enum


class GetClientResponse200SessionsItemObject(str, Enum):
    SESSION = "session"

    def __str__(self) -> str:
        return str(self.value)
