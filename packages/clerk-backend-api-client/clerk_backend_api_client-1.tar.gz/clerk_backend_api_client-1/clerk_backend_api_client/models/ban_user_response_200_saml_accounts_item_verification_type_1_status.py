from enum import Enum


class BanUserResponse200SamlAccountsItemVerificationType1Status(str, Enum):
    EXPIRED = "expired"
    UNVERIFIED = "unverified"
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
