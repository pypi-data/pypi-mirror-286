from enum import Enum


class GetUserListResponse200ItemPhoneNumbersItemVerificationType1Strategy(str, Enum):
    ADMIN = "admin"

    def __str__(self) -> str:
        return str(self.value)
