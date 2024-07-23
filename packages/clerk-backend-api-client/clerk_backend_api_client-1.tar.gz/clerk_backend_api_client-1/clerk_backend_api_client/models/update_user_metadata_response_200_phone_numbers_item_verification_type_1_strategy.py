from enum import Enum


class UpdateUserMetadataResponse200PhoneNumbersItemVerificationType1Strategy(str, Enum):
    ADMIN = "admin"

    def __str__(self) -> str:
        return str(self.value)
