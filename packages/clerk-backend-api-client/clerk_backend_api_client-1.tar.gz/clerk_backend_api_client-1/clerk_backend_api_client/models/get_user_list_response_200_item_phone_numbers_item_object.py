from enum import Enum


class GetUserListResponse200ItemPhoneNumbersItemObject(str, Enum):
    PHONE_NUMBER = "phone_number"

    def __str__(self) -> str:
        return str(self.value)
