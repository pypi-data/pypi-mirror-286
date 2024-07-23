from enum import Enum


class UpdatePhoneNumberResponse200VerificationType1Strategy(str, Enum):
    ADMIN = "admin"

    def __str__(self) -> str:
        return str(self.value)
