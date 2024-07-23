from enum import Enum


class GetUserResponse200PasskeysItemObject(str, Enum):
    PASSKEY = "passkey"

    def __str__(self) -> str:
        return str(self.value)
