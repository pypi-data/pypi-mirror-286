from enum import Enum


class ListSAMLConnectionsResponse200DataItemObject(str, Enum):
    SAML_CONNECTION = "saml_connection"

    def __str__(self) -> str:
        return str(self.value)
