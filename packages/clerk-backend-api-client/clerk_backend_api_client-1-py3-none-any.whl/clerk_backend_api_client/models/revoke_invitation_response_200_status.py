from enum import Enum


class RevokeInvitationResponse200Status(str, Enum):
    REVOKED = "revoked"

    def __str__(self) -> str:
        return str(self.value)
