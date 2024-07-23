from enum import Enum


class UserEmailAddressesItemVerificationType4Type1Strategy(str, Enum):
    ADMIN = "admin"

    def __str__(self) -> str:
        return str(self.value)
