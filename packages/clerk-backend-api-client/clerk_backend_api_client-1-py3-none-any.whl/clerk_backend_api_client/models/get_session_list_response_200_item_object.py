from enum import Enum


class GetSessionListResponse200ItemObject(str, Enum):
    SESSION = "session"

    def __str__(self) -> str:
        return str(self.value)
