from enum import Enum


class UpdatePhoneNumberResponse200VerificationType3Type1Status(str, Enum):
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
