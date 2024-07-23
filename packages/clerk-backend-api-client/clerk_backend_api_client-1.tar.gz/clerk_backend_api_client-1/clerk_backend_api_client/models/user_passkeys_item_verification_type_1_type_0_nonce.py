from enum import Enum


class UserPasskeysItemVerificationType1Type0Nonce(str, Enum):
    NONCE = "nonce"

    def __str__(self) -> str:
        return str(self.value)
