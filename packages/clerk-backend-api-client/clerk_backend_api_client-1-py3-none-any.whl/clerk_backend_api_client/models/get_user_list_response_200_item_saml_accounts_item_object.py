from enum import Enum


class GetUserListResponse200ItemSamlAccountsItemObject(str, Enum):
    SAML_ACCOUNT = "saml_account"

    def __str__(self) -> str:
        return str(self.value)
