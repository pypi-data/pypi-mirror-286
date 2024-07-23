from enum import Enum


class LockUserResponse200EmailAddressesItemVerificationType3Type1Status(str, Enum):
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
