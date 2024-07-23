from enum import Enum


class CreateAllowlistIdentifierResponse200Object(str, Enum):
    ALLOWLIST_IDENTIFIER = "allowlist_identifier"

    def __str__(self) -> str:
        return str(self.value)
