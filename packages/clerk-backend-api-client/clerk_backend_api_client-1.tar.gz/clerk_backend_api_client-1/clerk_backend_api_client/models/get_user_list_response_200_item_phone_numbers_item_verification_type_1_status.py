from enum import Enum


class GetUserListResponse200ItemPhoneNumbersItemVerificationType1Status(str, Enum):
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
