from enum import Enum


class CreateUserResponse200Object(str, Enum):
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
