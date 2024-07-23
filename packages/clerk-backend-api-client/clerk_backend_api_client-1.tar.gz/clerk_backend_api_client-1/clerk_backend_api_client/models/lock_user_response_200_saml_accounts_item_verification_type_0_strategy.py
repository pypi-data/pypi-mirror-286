from enum import Enum


class LockUserResponse200SamlAccountsItemVerificationType0Strategy(str, Enum):
    SAML = "saml"

    def __str__(self) -> str:
        return str(self.value)
