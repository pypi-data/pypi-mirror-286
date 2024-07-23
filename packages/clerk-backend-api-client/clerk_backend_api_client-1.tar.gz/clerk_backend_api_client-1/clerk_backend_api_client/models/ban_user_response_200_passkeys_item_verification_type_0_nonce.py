from enum import Enum


class BanUserResponse200PasskeysItemVerificationType0Nonce(str, Enum):
    NONCE = "nonce"

    def __str__(self) -> str:
        return str(self.value)
