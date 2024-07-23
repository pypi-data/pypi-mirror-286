from enum import Enum


class UpdateUserResponse200PhoneNumbersItemObject(str, Enum):
    PHONE_NUMBER = "phone_number"

    def __str__(self) -> str:
        return str(self.value)
