from enum import Enum


class GetPhoneNumberResponse200VerificationType3Type1Status(str, Enum):
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
