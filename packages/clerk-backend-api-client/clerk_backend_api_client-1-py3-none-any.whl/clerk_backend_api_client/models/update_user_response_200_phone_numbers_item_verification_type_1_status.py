from enum import Enum


class UpdateUserResponse200PhoneNumbersItemVerificationType1Status(str, Enum):
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
