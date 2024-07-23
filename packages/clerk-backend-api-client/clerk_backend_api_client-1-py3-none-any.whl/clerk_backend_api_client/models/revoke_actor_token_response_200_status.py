from enum import Enum


class RevokeActorTokenResponse200Status(str, Enum):
    ACCEPTED = "accepted"
    PENDING = "pending"
    REVOKED = "revoked"

    def __str__(self) -> str:
        return str(self.value)
