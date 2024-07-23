from enum import Enum


class UnlockUserResponse200PhoneNumbersItemObject(str, Enum):
    PHONE_NUMBER = "phone_number"

    def __str__(self) -> str:
        return str(self.value)
