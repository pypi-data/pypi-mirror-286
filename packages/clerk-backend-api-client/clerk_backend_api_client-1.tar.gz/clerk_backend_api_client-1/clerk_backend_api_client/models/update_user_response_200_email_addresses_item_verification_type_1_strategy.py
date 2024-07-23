from enum import Enum


class UpdateUserResponse200EmailAddressesItemVerificationType1Strategy(str, Enum):
    ADMIN = "admin"

    def __str__(self) -> str:
        return str(self.value)
