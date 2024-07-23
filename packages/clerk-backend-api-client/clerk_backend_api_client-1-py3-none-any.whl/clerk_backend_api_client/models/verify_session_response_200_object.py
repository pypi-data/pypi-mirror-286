from enum import Enum


class VerifySessionResponse200Object(str, Enum):
    SESSION = "session"

    def __str__(self) -> str:
        return str(self.value)
