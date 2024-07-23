from enum import Enum


class SAMLConnectionsDataItemObject(str, Enum):
    SAML_CONNECTION = "saml_connection"

    def __str__(self) -> str:
        return str(self.value)
