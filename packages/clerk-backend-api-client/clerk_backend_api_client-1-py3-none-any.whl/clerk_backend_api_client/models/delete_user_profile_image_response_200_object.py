from enum import Enum


class DeleteUserProfileImageResponse200Object(str, Enum):
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
