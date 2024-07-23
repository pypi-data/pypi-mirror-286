from enum import Enum


class GetUserListResponse200ItemPasskeysItemObject(str, Enum):
    PASSKEY = "passkey"

    def __str__(self) -> str:
        return str(self.value)
