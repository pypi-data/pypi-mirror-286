from enum import Enum


class CreatePhoneNumberResponse200VerificationType2Type1Strategy(str, Enum):
    ADMIN = "admin"

    def __str__(self) -> str:
        return str(self.value)
