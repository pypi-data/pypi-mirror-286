from enum import Enum


class UnlockUserResponse200PasskeysItemVerificationType0Status(str, Enum):
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
