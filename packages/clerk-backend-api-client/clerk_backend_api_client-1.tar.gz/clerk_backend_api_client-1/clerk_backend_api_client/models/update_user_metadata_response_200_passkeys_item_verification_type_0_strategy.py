from enum import Enum


class UpdateUserMetadataResponse200PasskeysItemVerificationType0Strategy(str, Enum):
    PASSKEY = "passkey"

    def __str__(self) -> str:
        return str(self.value)
