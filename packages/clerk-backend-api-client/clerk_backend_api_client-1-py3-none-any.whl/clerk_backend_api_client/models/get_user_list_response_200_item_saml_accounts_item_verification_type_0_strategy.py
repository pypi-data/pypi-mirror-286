from enum import Enum


class GetUserListResponse200ItemSamlAccountsItemVerificationType0Strategy(str, Enum):
    SAML = "saml"

    def __str__(self) -> str:
        return str(self.value)
