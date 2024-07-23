from enum import Enum


class CreateUserResponse200PasskeysItemVerificationType0Status(str, Enum):
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
