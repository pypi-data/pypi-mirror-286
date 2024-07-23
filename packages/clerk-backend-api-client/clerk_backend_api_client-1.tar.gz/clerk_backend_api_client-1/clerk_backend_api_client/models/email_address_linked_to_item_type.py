from enum import Enum


class EmailAddressLinkedToItemType(str, Enum):
    OAUTH_GOOGLE = "oauth_google"
    OAUTH_MOCK = "oauth_mock"
    SAML = "saml"

    def __str__(self) -> str:
        return str(self.value)
