from enum import Enum


class DeleteUserProfileImageResponse200PasskeysItemObject(str, Enum):
    PASSKEY = "passkey"

    def __str__(self) -> str:
        return str(self.value)
