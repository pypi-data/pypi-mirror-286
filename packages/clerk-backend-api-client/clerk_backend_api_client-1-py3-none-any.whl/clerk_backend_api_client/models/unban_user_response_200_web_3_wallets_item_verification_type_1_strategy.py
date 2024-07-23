from enum import Enum


class UnbanUserResponse200Web3WalletsItemVerificationType1Strategy(str, Enum):
    ADMIN = "admin"

    def __str__(self) -> str:
        return str(self.value)
