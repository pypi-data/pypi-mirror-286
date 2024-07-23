from enum import Enum


class UserSamlAccountsItemVerificationType2Type0Status(str, Enum):
    EXPIRED = "expired"
    FAILED = "failed"
    TRANSFERABLE = "transferable"
    UNVERIFIED = "unverified"
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
