from enum import Enum


class BanUserResponse200PhoneNumbersItemVerificationType1Strategy(str, Enum):
    ADMIN = "admin"

    def __str__(self) -> str:
        return str(self.value)
