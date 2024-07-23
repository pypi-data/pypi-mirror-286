from enum import Enum


class UserPasskeysItemVerificationType1Type0Strategy(str, Enum):
    PASSKEY = "passkey"

    def __str__(self) -> str:
        return str(self.value)
