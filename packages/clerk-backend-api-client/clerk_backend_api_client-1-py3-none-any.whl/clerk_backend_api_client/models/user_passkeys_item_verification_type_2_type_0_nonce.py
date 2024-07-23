from enum import Enum


class UserPasskeysItemVerificationType2Type0Nonce(str, Enum):
    NONCE = "nonce"

    def __str__(self) -> str:
        return str(self.value)
