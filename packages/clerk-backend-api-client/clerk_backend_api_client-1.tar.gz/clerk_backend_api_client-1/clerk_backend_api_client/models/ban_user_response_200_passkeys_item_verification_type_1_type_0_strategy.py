from enum import Enum


class BanUserResponse200PasskeysItemVerificationType1Type0Strategy(str, Enum):
    PASSKEY = "passkey"

    def __str__(self) -> str:
        return str(self.value)
