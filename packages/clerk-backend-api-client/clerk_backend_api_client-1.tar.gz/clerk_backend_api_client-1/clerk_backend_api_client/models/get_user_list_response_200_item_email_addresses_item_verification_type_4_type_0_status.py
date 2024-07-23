from enum import Enum


class GetUserListResponse200ItemEmailAddressesItemVerificationType4Type0Status(str, Enum):
    EXPIRED = "expired"
    FAILED = "failed"
    UNVERIFIED = "unverified"
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
