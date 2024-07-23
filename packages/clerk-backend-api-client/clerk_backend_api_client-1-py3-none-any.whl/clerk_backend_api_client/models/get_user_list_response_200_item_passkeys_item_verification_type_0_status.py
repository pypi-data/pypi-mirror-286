from enum import Enum


class GetUserListResponse200ItemPasskeysItemVerificationType0Status(str, Enum):
    VERIFIED = "verified"

    def __str__(self) -> str:
        return str(self.value)
