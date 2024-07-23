from enum import Enum


class GetUserResponse200SamlAccountsItemObject(str, Enum):
    SAML_ACCOUNT = "saml_account"

    def __str__(self) -> str:
        return str(self.value)
