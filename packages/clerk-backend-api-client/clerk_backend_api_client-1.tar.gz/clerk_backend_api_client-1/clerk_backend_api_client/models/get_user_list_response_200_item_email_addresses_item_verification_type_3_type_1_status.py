from enum import Enum


class GetUserListResponse200ItemEmailAddressesItemVerificationType3Type1Status(str, Enum):
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
