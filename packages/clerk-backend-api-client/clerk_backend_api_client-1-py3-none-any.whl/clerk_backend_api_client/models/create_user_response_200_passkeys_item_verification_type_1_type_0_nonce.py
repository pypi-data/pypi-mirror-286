from enum import Enum


class CreateUserResponse200PasskeysItemVerificationType1Type0Nonce(str, Enum):
    NONCE = "nonce"

    def __str__(self) -> str:
        return str(self.value)
