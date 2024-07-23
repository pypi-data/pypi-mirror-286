from enum import Enum


class UserWeb3WalletsItemVerificationType1Status(str, Enum):
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
