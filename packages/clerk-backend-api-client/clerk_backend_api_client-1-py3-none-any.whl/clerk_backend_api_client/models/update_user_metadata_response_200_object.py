from enum import Enum


class UpdateUserMetadataResponse200Object(str, Enum):
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
