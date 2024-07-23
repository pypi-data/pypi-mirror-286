from enum import Enum


class UpdateUserResponse200PasskeysItemVerificationType0Nonce(str, Enum):
    NONCE = "nonce"

    def __str__(self) -> str:
        return str(self.value)
