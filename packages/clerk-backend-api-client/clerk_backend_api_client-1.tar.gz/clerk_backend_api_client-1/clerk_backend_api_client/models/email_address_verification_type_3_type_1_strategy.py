from enum import Enum


class EmailAddressVerificationType3Type1Strategy(str, Enum):
    ADMIN = "admin"

    def __str__(self) -> str:
        return str(self.value)
