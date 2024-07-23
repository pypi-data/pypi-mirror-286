from enum import Enum


class GetSAMLConnectionResponse200Object(str, Enum):
    SAML_CONNECTION = "saml_connection"

    def __str__(self) -> str:
        return str(self.value)
