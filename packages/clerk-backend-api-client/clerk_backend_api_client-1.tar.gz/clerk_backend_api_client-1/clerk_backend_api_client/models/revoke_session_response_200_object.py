from enum import Enum


class RevokeSessionResponse200Object(str, Enum):
    SESSION = "session"

    def __str__(self) -> str:
        return str(self.value)
