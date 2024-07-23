from enum import Enum


class GetClientListResponse200ItemSessionsItemObject(str, Enum):
    SESSION = "session"

    def __str__(self) -> str:
        return str(self.value)
