from enum import Enum


class SAMLAccountVerificationType0Strategy(str, Enum):
    SAML = "saml"

    def __str__(self) -> str:
        return str(self.value)
