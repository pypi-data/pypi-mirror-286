from enum import Enum


class UserPasskeysItemVerificationType0Status(str, Enum):
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
