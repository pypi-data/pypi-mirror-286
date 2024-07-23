from enum import Enum


class ListAllowlistIdentifiersResponse200ItemObject(str, Enum):
    ALLOWLIST_IDENTIFIER = "allowlist_identifier"

    def __str__(self) -> str:
        return str(self.value)
