from enum import Enum


class VerifyClientResponse200Object(str, Enum):
    CLIENT = "client"

    def __str__(self) -> str:
        return str(self.value)
