from enum import Enum


class UpdateUserMetadataResponse200SamlAccountsItemObject(str, Enum):
    SAML_ACCOUNT = "saml_account"

    def __str__(self) -> str:
        return str(self.value)
