from enum import Enum


class BanUserResponse200PasskeysItemVerificationType1Type0Status(str, Enum):
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
