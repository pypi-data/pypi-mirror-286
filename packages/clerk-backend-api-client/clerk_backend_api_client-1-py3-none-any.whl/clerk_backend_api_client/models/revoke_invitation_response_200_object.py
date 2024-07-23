from enum import Enum


class RevokeInvitationResponse200Object(str, Enum):
    INVITATION = "invitation"

    def __str__(self) -> str:
        return str(self.value)
