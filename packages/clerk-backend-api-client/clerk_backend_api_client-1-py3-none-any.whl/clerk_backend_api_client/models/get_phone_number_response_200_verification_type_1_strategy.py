from enum import Enum


class GetPhoneNumberResponse200VerificationType1Strategy(str, Enum):
    ADMIN = "admin"

    def __str__(self) -> str:
        return str(self.value)
