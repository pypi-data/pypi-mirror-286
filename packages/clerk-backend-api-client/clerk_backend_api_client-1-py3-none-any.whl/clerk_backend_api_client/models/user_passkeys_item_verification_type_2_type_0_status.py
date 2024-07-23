from enum import Enum


class UserPasskeysItemVerificationType2Type0Status(str, Enum):
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
