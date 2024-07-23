from enum import Enum


class GetUserListResponse200ItemEmailAddressesItemVerificationType4Type1Status(str, Enum):
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
