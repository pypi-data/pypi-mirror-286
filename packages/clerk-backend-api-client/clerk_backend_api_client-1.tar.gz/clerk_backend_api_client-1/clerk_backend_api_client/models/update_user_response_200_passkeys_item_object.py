from enum import Enum


class UpdateUserResponse200PasskeysItemObject(str, Enum):
    PASSKEY = "passkey"

    def __str__(self) -> str:
        return str(self.value)
