from enum import Enum


class UpdateUserMetadataResponse200Web3WalletsItemVerificationType1Status(str, Enum):
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
