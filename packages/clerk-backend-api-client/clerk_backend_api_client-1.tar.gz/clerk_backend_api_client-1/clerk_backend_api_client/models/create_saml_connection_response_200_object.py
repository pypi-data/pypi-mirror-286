from enum import Enum


class CreateSAMLConnectionResponse200Object(str, Enum):
    SAML_CONNECTION = "saml_connection"

    def __str__(self) -> str:
        return str(self.value)
