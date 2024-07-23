from enum import Enum


class CreateBlocklistIdentifierResponse200Object(str, Enum):
    BLOCKLIST_IDENTIFIER = "blocklist_identifier"

    def __str__(self) -> str:
        return str(self.value)
