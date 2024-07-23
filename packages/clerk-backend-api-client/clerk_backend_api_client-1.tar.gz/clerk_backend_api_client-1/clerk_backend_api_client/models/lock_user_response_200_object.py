from enum import Enum


class LockUserResponse200Object(str, Enum):
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
