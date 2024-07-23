from enum import Enum


class CreateOrganizationMembershipResponse200Object(str, Enum):
    ORGANIZATION_MEMBERSHIP = "organization_membership"

    def __str__(self) -> str:
        return str(self.value)
