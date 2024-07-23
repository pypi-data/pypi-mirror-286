from enum import Enum


class UserPasskeysItemVerificationType2Type0Strategy(str, Enum):
    PASSKEY = "passkey"

    def __str__(self) -> str:
        return str(self.value)
