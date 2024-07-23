from enum import Enum


class UnlockUserResponse200Object(str, Enum):
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
