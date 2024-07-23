from enum import Enum


class UserPasskeysItemVerificationType0Nonce(str, Enum):
    NONCE = "nonce"

    def __str__(self) -> str:
        return str(self.value)
