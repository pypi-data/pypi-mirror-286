from enum import Enum


class ListInvitationsResponse200ItemObject(str, Enum):
    INVITATION = "invitation"

    def __str__(self) -> str:
        return str(self.value)
