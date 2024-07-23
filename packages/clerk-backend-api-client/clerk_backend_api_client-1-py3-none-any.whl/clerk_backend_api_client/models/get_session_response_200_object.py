from enum import Enum


class GetSessionResponse200Object(str, Enum):
    SESSION = "session"

    def __str__(self) -> str:
        return str(self.value)
