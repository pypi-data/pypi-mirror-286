from enum import Enum


class SetUserProfileImageResponse200SamlAccountsItemVerificationType2Type1Status(str, Enum):
    EXPIRED = "expired"
    UNVERIFIED = "unverified"
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
