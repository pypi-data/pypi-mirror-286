from enum import Enum


class CreateOrganizationInvitationResponse200Object(str, Enum):
    ORGANIZATION_INVITATION = "organization_invitation"

    def __str__(self) -> str:
        return str(self.value)
