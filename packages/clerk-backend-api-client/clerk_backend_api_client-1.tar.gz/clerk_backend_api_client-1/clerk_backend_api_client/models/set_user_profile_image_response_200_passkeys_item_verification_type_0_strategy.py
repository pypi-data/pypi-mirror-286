from enum import Enum


class SetUserProfileImageResponse200PasskeysItemVerificationType0Strategy(str, Enum):
    PASSKEY = "passkey"

    def __str__(self) -> str:
        return str(self.value)
