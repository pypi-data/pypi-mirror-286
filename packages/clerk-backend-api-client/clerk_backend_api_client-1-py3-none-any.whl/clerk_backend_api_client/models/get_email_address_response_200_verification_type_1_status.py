from enum import Enum


class GetEmailAddressResponse200VerificationType1Status(str, Enum):
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
