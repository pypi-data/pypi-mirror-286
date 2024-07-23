from enum import Enum


class GetUserResponse200PasskeysItemVerificationType0Nonce(str, Enum):
    NONCE = "nonce"

    def __str__(self) -> str:
        return str(self.value)
