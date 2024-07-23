from enum import Enum


class UserPasskeysItemVerificationType0Strategy(str, Enum):
    PASSKEY = "passkey"

    def __str__(self) -> str:
        return str(self.value)
