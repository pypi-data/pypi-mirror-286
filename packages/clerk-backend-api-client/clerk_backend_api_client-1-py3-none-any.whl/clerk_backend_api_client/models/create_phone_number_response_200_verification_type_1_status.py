from enum import Enum


class CreatePhoneNumberResponse200VerificationType1Status(str, Enum):
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
