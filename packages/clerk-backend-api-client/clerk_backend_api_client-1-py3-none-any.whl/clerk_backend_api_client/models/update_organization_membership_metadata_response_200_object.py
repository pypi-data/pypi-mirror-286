from enum import Enum


class UpdateOrganizationMembershipMetadataResponse200Object(str, Enum):
    ORGANIZATION_MEMBERSHIP = "organization_membership"

    def __str__(self) -> str:
        return str(self.value)
