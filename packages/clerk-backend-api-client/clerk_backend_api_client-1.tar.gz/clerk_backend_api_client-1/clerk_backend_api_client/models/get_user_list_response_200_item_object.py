from enum import Enum


class GetUserListResponse200ItemObject(str, Enum):
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
