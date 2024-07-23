from enum import Enum


class CreatePhoneNumberResponse200VerificationType3Type1Status(str, Enum):
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
