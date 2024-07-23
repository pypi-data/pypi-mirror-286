from enum import Enum


class UserPasskeysItemVerificationType1Type0Status(str, Enum):
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
