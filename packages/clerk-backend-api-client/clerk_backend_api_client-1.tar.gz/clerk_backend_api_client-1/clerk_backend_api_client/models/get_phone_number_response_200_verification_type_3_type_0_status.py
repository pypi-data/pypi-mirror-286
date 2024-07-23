from enum import Enum


class GetPhoneNumberResponse200VerificationType3Type0Status(str, Enum):
    EXPIRED = "expired"
    FAILED = "failed"
    UNVERIFIED = "unverified"
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
