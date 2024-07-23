from enum import Enum


class UpdateOrganizationMembershipResponse200OrganizationObject(str, Enum):
    ORGANIZATION = "organization"

    def __str__(self) -> str:
        return str(self.value)
